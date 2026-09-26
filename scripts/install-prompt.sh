#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'USAGE'
用法: install-prompt.sh [选项] <host>

把 environments/<host>/ 的全局 instructions 按平台装配后安装到宿主读取位置。
本体中独占一行的 {{PLATFORM}} 会替换为 environments/<host>/platform/<平台>.md，
装配结果只包含一个平台的规则。

host:
  codex, cline, cursor, opencode, pi, claude-code, gemini, grok, windsurf

选项:
  --platform <macos|windows>  指定平台；省略时按 uname 自动识别。
  --print                     只把装配结果输出到标准输出，不写盘（Cursor 需在设置界面粘贴）。
  --dry-run                   只打印将要执行的备份与写入，不写盘。
  -h, --help                  显示本帮助。

目标文件已存在且内容不同时，先备份为 <目标>.bak-<时间戳> 再写入。
USAGE
}

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
marker='{{PLATFORM}}'

host=""
platform=""
print_only=0
dry_run=0

while [ "$#" -gt 0 ]; do
  case "$1" in
    --platform)
      [ "$#" -ge 2 ] || { printf -- '--platform 需要参数\n' >&2; exit 2; }
      platform="$2"; shift ;;
    --print)   print_only=1 ;;
    --dry-run) dry_run=1 ;;
    -h|--help) usage; exit 0 ;;
    -*) printf '未知选项: %s\n\n' "$1" >&2; usage >&2; exit 2 ;;
    *)
      if [ -n "$host" ]; then
        printf '只接受一个 host，已收到第二个: %s\n' "$1" >&2
        exit 2
      fi
      host="$1"
      ;;
  esac
  shift
done

[ -n "$host" ] || { usage >&2; exit 2; }

case "$platform" in
  ""|macos|windows) ;;
  *) printf '未知平台: %s（只支持 macos、windows）\n' "$platform" >&2; exit 2 ;;
esac

# host -> 本体文件、安装位置。安装位置与各宿主 README 保持一致；Cursor 的 User Rules 只能在设置界面粘贴。
case "$host" in
  codex)       source_name="AGENTS.md";       target="${CODEX_HOME:-$HOME/.codex}/AGENTS.md" ;;
  cline)       source_name="000-global.md";   target="$HOME/Documents/Cline/Rules/000-global.md" ;;
  cursor)      source_name="user-rules.md";   target="" ;;
  opencode)    source_name="AGENTS.md";       target="$HOME/.config/opencode/AGENTS.md" ;;
  pi)          source_name="AGENTS.md";       target="$HOME/.pi/agent/AGENTS.md" ;;
  claude-code) source_name="CLAUDE.md";       target="$HOME/.claude/CLAUDE.md" ;;
  gemini)      source_name="GEMINI.md";       target="$HOME/.gemini/GEMINI.md" ;;
  grok)        source_name="AGENTS.md";       target="$HOME/.grok/AGENTS.md" ;;
  windsurf)    source_name="global_rules.md"; target="$HOME/.codeium/windsurf/memories/global_rules.md" ;;
  *) printf '未知 host: %s\n\n' "$host" >&2; usage >&2; exit 2 ;;
esac

source_file="$repo_root/environments/$host/$source_name"
marker_count="$(grep -cFx "$marker" "$source_file" || true)"

if [ "$marker_count" -gt 1 ]; then
  printf '%s 中 %s 出现 %s 次，只允许一次。\n' "$source_file" "$marker" "$marker_count" >&2
  exit 1
fi

fragment=""
if [ "$marker_count" -eq 1 ]; then
  if [ -z "$platform" ]; then
    case "$(uname -s)" in
      Darwin) platform="macos" ;;
      MINGW*|MSYS*|CYGWIN*) platform="windows" ;;
      *) printf '无法自动识别平台（%s），请用 --platform macos|windows 指定。\n' "$(uname -s)" >&2; exit 2 ;;
    esac
  fi
  fragment="$repo_root/environments/$host/platform/$platform.md"
  if [ ! -f "$fragment" ]; then
    printf '缺少平台片段: %s\n' "$fragment" >&2
    exit 1
  fi
fi

assemble() {
  if [ -z "$fragment" ]; then
    cat "$source_file"
    return
  fi
  awk -v marker="$marker" -v frag="$fragment" '
    { line = $0; sub(/\r$/, "", line) }
    line == marker {
      while ((getline l < frag) > 0) print l
      close(frag)
      next
    }
    { print }
  ' "$source_file"
}

if [ "$print_only" -eq 1 ]; then
  assemble
  exit 0
fi

if [ -z "$target" ]; then
  printf '%s 没有文件形式的全局 instructions，请用 --print 输出后在宿主设置界面粘贴。\n' "$host" >&2
  exit 2
fi

prefix=""
[ "$dry_run" -eq 1 ] && prefix="[dry-run] "
label="$host"
[ -n "$fragment" ] && label="$host ($platform)"

tmp="$(mktemp)"
trap 'rm -f "$tmp"' EXIT
assemble > "$tmp"

if [ -f "$target" ] && cmp -s "$tmp" "$target"; then
  printf '%sunchanged %s -> %s\n' "$prefix" "$label" "$target"
  exit 0
fi

if [ -f "$target" ]; then
  backup="$target.bak-$(date +%Y%m%d%H%M%S)"
  printf '%sbackup %s -> %s\n' "$prefix" "$target" "$backup"
  [ "$dry_run" -eq 0 ] && cp -p "$target" "$backup"
fi

printf '%sinstall %s -> %s\n' "$prefix" "$label" "$target"
if [ "$dry_run" -eq 0 ]; then
  mkdir -p "$(dirname "$target")"
  cp "$tmp" "$target"
fi
