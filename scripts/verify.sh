#!/usr/bin/env bash
# 发布前验证门禁。等价于 AGENTS.md「验证」段的人工检查，任何一项不通过即非 0 退出。
# 只依赖 Bash、find、grep、git；evals JSON 校验可选使用 python3 或 jq。
# 链接检查以 Linux 结果为准：Windows Git Bash 下大小写不敏感，可能漏报大小写错误的链接。
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
cd "$repo_root"

allowlist="$script_dir/verify-allowlist.txt"
errors=0
update_allowlist=0

# --update-allowlist 用当前全部命中重写允许清单，供人工审阅后提交。
# 复用下方同一份 pattern 与同一套解析逻辑，避免手工重拼正则造成两边不一致。
if [ "${1:-}" = "--update-allowlist" ]; then
  update_allowlist=1
fi

fail() {
  printf 'FAIL  %s\n' "$1"
  errors=$((errors + 1))
}

pass() {
  printf 'ok    %s\n' "$1"
}

# --- 1. 敏感扫描 -------------------------------------------------------------
# 规则与 AGENTS.md 保持一致。命中行需逐字出现在允许清单中（格式 路径:行内容，不含行号）。
sensitive_pattern='secret|token|password|api[_-]?key|sk-|AKIA|PRIVATE|C:\\|D:\\|IndieArk|github.com/indieark|192\.168|\.env|私有|内部|客户|公司|GHCR|PROJECTS.md|端口|奇数|偶数|20001|Steam_UI'

check_sensitive() {
  local hits unexpected=0 line
  hits="$(grep -RInE "$sensitive_pattern" . \
    --exclude-dir=.git \
    --exclude-dir=plans \
    --exclude=CHANGELOG.md \
    --exclude="$(basename "$allowlist")" \
    2>/dev/null || true)"

  [ -z "$hits" ] && { pass "敏感扫描：无命中"; return; }

  if [ "$update_allowlist" -eq 1 ]; then
    {
      printf '# 敏感扫描允许清单：已人工判定为说明文字、非真实敏感内容的命中行。\n'
      printf '# 格式：相对路径:行内容（不含行号，避免行号漂移）。\n'
      printf '# 由 bash scripts/verify.sh --update-allowlist 生成；新增条目须逐条人工确认\n'
      printf '# 不含真实凭据、内网地址、本机绝对路径或私有组织标识。\n'
      while IFS= read -r line; do
        [ -z "$line" ] && continue
        local s="${line#./}"
        local p="${s%%:*}"
        local r="${s#*:}"
        printf '%s:%s\n' "$p" "${r#*:}"
      done <<< "$hits"
    } > "$allowlist"
    printf '已写入允许清单：%s\n' "$allowlist"
    pass "敏感扫描：允许清单已更新，请人工审阅后提交"
    return
  fi

  while IFS= read -r line; do
    [ -z "$line" ] && continue
    # 去掉 grep 的 ./ 前缀和行号，得到 路径:行内容
    local stripped="${line#./}"
    local path="${stripped%%:*}"
    local rest="${stripped#*:}"
    local content="${rest#*:}"
    local key="$path:$content"

    if [ -f "$allowlist" ] && grep -Fxq "$key" "$allowlist"; then
      continue
    fi
    printf '      未在允许清单中的命中: %s\n' "$line"
    unexpected=$((unexpected + 1))
  done <<< "$hits"

  if [ "$unexpected" -gt 0 ]; then
    fail "敏感扫描：$unexpected 处命中不在 scripts/verify-allowlist.txt 中"
  else
    pass "敏感扫描：全部命中均为已登记的说明文字"
  fi
}

# --- 2. 数量对账 -------------------------------------------------------------
check_counts() {
  local skill_count env_count readme_skills readme_envs
  skill_count="$(find skills -mindepth 2 -maxdepth 2 -name SKILL.md | wc -l | tr -d ' ')"
  env_count="$(find environments -mindepth 2 -maxdepth 2 -name README.md | wc -l | tr -d ' ')"

  readme_skills="$(grep -oE '[0-9]+ 个 skills' README.md | head -1 | grep -oE '[0-9]+' || true)"
  readme_envs="$(grep -oE '[0-9]+ 类 coding environments' README.md | head -1 | grep -oE '[0-9]+' || true)"

  if [ "$readme_skills" = "$skill_count" ]; then
    pass "数量对账：skills = $skill_count"
  else
    fail "数量对账：README 写 '$readme_skills 个 skills'，实际 $skill_count"
  fi

  if [ "$readme_envs" = "$env_count" ]; then
    pass "数量对账：environments = $env_count"
  else
    fail "数量对账：README 写 '$readme_envs 类 coding environments'，实际 $env_count"
  fi
}

# --- 3. Skill 清单对账 -------------------------------------------------------
check_skill_list() {
  local listed actual missing=0 extra=0 name
  # README「Skill 清单」表中的反引号 skill 名
  listed="$(sed -n '/^## Skill 清单/,/^## /p' README.md \
    | grep -oE '`pro-[a-z-]+`' | tr -d '`' | sort -u)"
  actual="$(find skills -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort -u)"

  while IFS= read -r name; do
    [ -z "$name" ] && continue
    if [ ! -d "skills/$name" ]; then
      printf '      README 列出但 skills/ 不存在: %s\n' "$name"
      missing=$((missing + 1))
    fi
  done <<< "$listed"

  while IFS= read -r name; do
    [ -z "$name" ] && continue
    if ! printf '%s\n' "$listed" | grep -Fxq "$name"; then
      printf '      skills/ 存在但 README 未列出: %s\n' "$name"
      extra=$((extra + 1))
    fi
  done <<< "$actual"

  if [ "$missing" -eq 0 ] && [ "$extra" -eq 0 ]; then
    pass "Skill 清单对账：README 与 skills/ 一致"
  else
    fail "Skill 清单对账：缺失 $missing 项，未列出 $extra 项"
  fi
}

# --- 4. 相对链接检查 ---------------------------------------------------------
check_links() {
  local broken=0 md target resolved
  # 单次 awk 处理全部 .md，输出「文件<TAB>链接目标」；shell 只做存在性判断。
  # 逐文件起管道在 Windows 上 fork 开销极大，故合并为一次扫描。
  while IFS=$'\t' read -r md target; do
    [ -z "$md" ] && continue
    resolved="$(dirname "$md")/$target"
    if [ ! -e "$resolved" ]; then
      printf '      失效链接: %s -> %s\n' "${md#./}" "$target"
      broken=$((broken + 1))
    fi
  done < <(find . -name '*.md' -not -path './.git/*' -print0 \
    | xargs -0 awk '
      FNR == 1 { infence = 0 }
      # 模板文件的链接为占位符，整文件跳过
      FILENAME ~ /skills\/pro-readme\/assets\/readme-template\.md$/ { next }
      /^[[:space:]]*```/ { infence = !infence; next }
      infence { next }
      {
        line = $0
        gsub(/`[^`]*`/, "", line)          # 剥掉行内代码
        while (match(line, /\]\([^)]+\)/)) {
          t = substr(line, RSTART + 2, RLENGTH - 3)
          line = substr(line, RSTART + RLENGTH)
          sub(/#.*$/, "", t)                # 去掉锚点
          if (t == "" || t ~ /^https?:\/\// || t ~ /^mailto:/) continue
          printf "%s\t%s\n", FILENAME, t
        }
      }
    ')

  if [ "$broken" -eq 0 ]; then
    pass "相对链接检查：全部可解析"
  else
    fail "相对链接检查：$broken 条失效"
  fi
}

# --- 5. Skill frontmatter ----------------------------------------------------
check_frontmatter() {
  local bad=0 problems
  # 同样合并为单次 awk：只看每个 SKILL.md 的前 10 行，在文件切换与结尾处统一判定。
  problems="$(
    find skills -mindepth 2 -maxdepth 2 -name SKILL.md -print0 \
      | xargs -0 awk '
        FNR == 1 {
          if (NR > 1) emit(prev)
          prev = FILENAME; has_name = 0; has_desc = 0; declared = ""
        }
        FNR <= 10 {
          line = $0; sub(/\r$/, "", line)
          if (line ~ /^name:/ && !has_name) {
            has_name = 1; declared = line; sub(/^name:[[:space:]]*/, "", declared)
          }
          if (line ~ /^description:/) has_desc = 1
        }
        END { if (NR > 0) emit(prev) }
        function emit(f,   dir, base) {
          dir = f; sub(/\/SKILL\.md$/, "", dir)
          base = dir; sub(/^.*\//, "", base)
          if (!has_name) { printf "      缺少 name: %s\n", f; return }
          if (!has_desc) { printf "      缺少 description: %s\n", f; return }
          if (declared != base) printf "      name 与目录名不符: %s (name: %s)\n", f, declared
        }
      '
  )"

  if [ -n "$problems" ]; then
    printf '%s\n' "$problems"
    bad="$(printf '%s\n' "$problems" | grep -c .)"
  fi

  if [ "$bad" -eq 0 ]; then
    pass "Skill frontmatter：全部合规"
  else
    fail "Skill frontmatter：$bad 处问题"
  fi
}

# --- 6. evals 结构 -----------------------------------------------------------
check_evals() {
  local files json_tool="" bad=0 f name
  files="$(find skills -mindepth 3 -maxdepth 3 -path '*/evals/evals.json' || true)"
  [ -z "$files" ] && { pass "evals 结构：无 evals.json，跳过"; return; }

  # 用实际执行探测而非 command -v：Windows 的 python3 可能是 Store 别名存根，能找到却不能运行
  if python3 -c '' >/dev/null 2>&1; then
    json_tool="python3"
  elif python -c '' >/dev/null 2>&1; then
    json_tool="python"
  elif jq --version >/dev/null 2>&1; then
    json_tool="jq"
  else
    printf 'WARN  evals 结构：未找到 python3 或 jq，跳过该项\n'
    return
  fi

  while IFS= read -r f; do
    [ -z "$f" ] && continue
    name="$(basename "$(dirname "$(dirname "$f")")")"
    if [ "$json_tool" != "jq" ]; then
      if ! "$json_tool" - "$f" "$name" <<'PY'
import json, sys
path, expected = sys.argv[1], sys.argv[2]
try:
    with open(path, encoding='utf-8') as fh:
        data = json.load(fh)
except Exception as exc:
    print(f'      JSON 解析失败: {path}: {exc}')
    sys.exit(1)
if data.get('skill_name') != expected:
    print(f"      skill_name 与目录名不符: {path} (skill_name: {data.get('skill_name')!r}, 目录: {expected})")
    sys.exit(1)
evals = data.get('evals')
if not isinstance(evals, list) or not evals:
    print(f'      evals 缺失或为空: {path}')
    sys.exit(1)
for item in evals:
    for key in ('id', 'prompt', 'expected_output'):
        if key not in item:
            print(f"      用例缺少字段 {key}: {path} (id: {item.get('id')})")
            sys.exit(1)
PY
      then
        bad=$((bad + 1))
      fi
    else
      if ! jq -e --arg n "$name" \
        '.skill_name == $n and (.evals | type == "array" and length > 0)
         and (all(.evals[]; has("id") and has("prompt") and has("expected_output")))' \
        "$f" >/dev/null 2>&1; then
        printf '      evals 结构不合规: %s\n' "$f"
        bad=$((bad + 1))
      fi
    fi
  done <<< "$files"

  if [ "$bad" -eq 0 ]; then
    pass "evals 结构：全部合规（$json_tool）"
  else
    fail "evals 结构：$bad 个文件不合规"
  fi
}

# --- 7. git diff --check -----------------------------------------------------
check_whitespace() {
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    printf 'WARN  git diff --check：非 Git 工作树，跳过\n'
    return
  fi
  if git diff --check >/dev/null 2>&1 && git diff --cached --check >/dev/null 2>&1; then
    pass "git diff --check：无尾随空白或冲突标记"
  else
    git diff --check || true
    git diff --cached --check || true
    fail "git diff --check：存在尾随空白或冲突标记"
  fi
}

printf '== agent-kit verify ==\n'
check_sensitive
check_counts
check_skill_list
check_links
check_frontmatter
check_evals
check_whitespace

printf '\n'
if [ "$errors" -gt 0 ]; then
  printf '验证失败：%d 项未通过\n' "$errors"
  exit 1
fi
printf '验证通过：全部检查项均正常\n'
