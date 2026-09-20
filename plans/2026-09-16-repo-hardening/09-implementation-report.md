# 实施报告 — agent-kit 仓库工程化加固

执行日期：2026-09-16
执行范围：阶段一、二、三。**阶段四（补齐 skill evals）按用户指示跳过，未执行。**

## 结果概览

| 阶段 | 状态 | 说明 |
|---|---|---|
| 一 最小 CI 门禁 | `[done]` | `scripts/verify.sh` + 允许清单 + GitHub Actions workflow |
| 二 安装脚本清理与 dry-run | `[done]` | Bash 与 PowerShell 双脚本，行为一致 |
| 三 清除过期引用 | `[done]` | 删除 grok 的 `image-gen-pro` 路由与本机空目录 |
| 四 补齐 skill evals | `[skipped]` | 用户明确要求不加评测 |

## 阶段三：清除过期引用

- 删除 `environments/grok/AGENTS.md` Tool Routing 段中 `image-gen-pro` 一行。
- 计划步骤 2 要求检查 grok 的两个 README：`environments/grok/README.md` 与 `environments/grok/skills/README.md` 均无配套描述，无需改动。
- 删除本机未跟踪的空目录 `skills/pro-copy/evals/`。
- 验证：`grep -RIn 'image-gen-pro\|imagen' environments/ skills/ README.md AGENTS.md` 无命中。

补充发现：`environments/claude-code/README.md:28` 含「例如生图 / 生视频 skill」字样，属于泛化说明文字而非路由，按计划「不擅自引入新 skill / 保持最小改动」原则未动。

## 阶段一：最小 CI 门禁

新增 `scripts/verify.sh`，七项检查，失败累计并以非 0 退出：敏感扫描、数量对账、Skill 清单对账、相对链接、frontmatter、evals 结构、`git diff --check`。

### 与计划的偏差

1. **新增 `--update-allowlist` 模式（计划外）。**
   计划设想人工把命中行填入允许清单。实际执行时，手工在命令行重拼同一份 grep 正则会因反斜杠转义导致含 `C:\` 的两行丢失，造成清单与脚本判定不一致。改为由脚本自身复用同一份 pattern 和同一套解析逻辑生成清单，从根上消除两边不一致。清单仍需人工审阅后提交。

2. **链接检查剥离代码块与行内代码（计划外的必要修正）。**
   首轮出现两条误报：`skills/pro-readme/SKILL.md` 与本计划 `01-ci-gate.md` 中，反引号内的 `](...)` 字面量被当作真链接。修正为先剥掉围栏代码块与行内代码再提取链接。计划原定「整文件跳过 `readme-template.md`」的豁免同时保留。

3. **JSON 工具探测改为实际执行探测，并增加 `python` 回退。**
   Windows 上 `command -v python3` 会命中 Microsoft Store 别名存根，能找到却不能运行，导致 evals 检查被静默跳过。改为 `python3 -c '' ` 实际执行探测，并在 `python3` 之后、`jq` 之前增加 `python` 回退。本机据此真正执行了该项检查。

4. **性能优化（计划外）。**
   初版逐文件起管道，单次运行 92 秒。链接检查与 frontmatter 检查各合并为一次 `awk` 调用后降至 21 秒，检出能力经破坏测试确认未削弱。

### 验证结果

干净工作树上 `bash scripts/verify.sh` 退出码 0。计划要求的三个破坏测试，以及后续为优化补测的两项，全部检出并在还原后回到 0：

| 破坏 | 检出 | 退出码 |
|---|---|---|
| `docs/agents/README.md` 加入 `AKIA1234` | 敏感扫描定位到文件与行 | 1 |
| README `11 个 skills` 改为 `12` | 数量对账报出期望值与实际值 | 1 |
| 加入指向不存在文件的链接 | 相对链接检查定位到文件与目标 | 1 |
| `pro-idea/SKILL.md` 的 `name` 改为 `pro-wrong` | frontmatter 报出不符 | 1 |
| `evals.json` 写入非法 JSON / 错误 `skill_name` | evals 结构分别报出解析失败与名称不符 | 1 |

### 未验证项

- **GitHub Actions 未实际运行。** `.github/workflows/verify.yml` 已写入，但尚未 push，CI 绿灯未经验证。计划成功标准第 3 条「首次 push 后显示绿色」待用户授权推送后确认。
- 本机 `jq` 不可用，evals 检查的 `jq` 回退分支未执行到；`python` 分支已验证。
- 链接检查在 Linux 上的大小写敏感行为未验证（本机 Git Bash 大小写不敏感）。脚本内已注释说明以 Linux 结果为准。

## 阶段二：安装脚本清理与 dry-run

Bash 与 PowerShell 双脚本均支持 `--dry-run`/`-DryRun`、`--clean`/`-Clean`，输出格式统一为 `install <name> -> <path>` / `remove <name> <- <path>`，dry-run 加 `[dry-run] ` 前缀。Bash 版参数顺序无关，未知选项退出码 2。

删除前置校验：目标路径非空且为已存在目录，否则拒绝执行清理。

### 执行中发现并修复的 bug

PowerShell 版初版写作 `"$Prefix`remove ..."`，反引号被解析为转义字符 `` `r ``（回车），实际输出 `emove pro-obsolete`，缺失首字母且混入回车符。改用 `-f` 格式化运算符，`install` 行同样改写以避免同类问题。修复后两脚本输出严格一致。

### 验证结果

Bash 与 PowerShell 各跑一遍计划的 5 条成功标准，全部通过：

| 标准 | Bash | PowerShell |
|---|---|---|
| 1. 空目录安装后恰好 11 个子目录 | 通过 | 通过 |
| 2. `--clean` 删除 `pro-obsolete`、保留 `other-skill` | 通过 | 通过 |
| 3. `pro-summary/stale.txt` 重装后消失、`SKILL.md` 仍在 | 通过 | 通过 |
| 4. `--dry-run --clean` 前后 `find` 输出完全一致，且列出应删应装项 | 通过 | 通过 |
| 5. `scripts/verify.sh` 仍通过 | 通过 | — |

测试用临时目录均已清理。

注：标准 3 确认的行为是「重装会抹掉 skill 目录内的用户文件」。这是计划的预期设计，已在 README 安装段补充显式提示。

## 文档同步

- `AGENTS.md` 验证段：保留原三条命令，补充等价的 `bash scripts/verify.sh` 与允许清单维护方式。
- `README.md`：质量检查段改为以脚本为主；安装段补充 dry-run/clean 用法与覆盖提示；配置表补两个选项；目录树补 `.github/` 与两个新脚本文件。
- `CHANGELOG.md`：新增 `0.11.0 - 2026-09-16`。

## 遗留事项

1. **CI 绿灯未验证** —— 需 push 后确认。所有 Git 写操作（stage、commit、push）均未执行，等待用户授权。
2. **根目录 `evals/` 与 `skillsets/` 空目录** —— 本机未跟踪的残留，与阶段三处理的 `skills/pro-copy/evals/` 同类，但不在计划范围内，未处理。
3. **阶段四未执行** —— `pro-summary`、`pro-readme`、`pro-plans`、`pro-explain` 仍无 evals。`verify.sh` 的 evals 结构检查已就绪，后续补充时可直接复用。
4. **允许清单的维护成本** —— 清单按「路径:行内容」精确匹配，任何被登记行的文案改动都会使对应条目失效，需重新生成并复核。这是避免行号漂移的代价。
