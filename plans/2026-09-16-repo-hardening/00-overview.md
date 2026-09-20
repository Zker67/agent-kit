# [partial] agent-kit 仓库工程化加固

## 背景

2026-09-16 的成熟度评估结论：本仓库在文档结构、版本记录、数量一致性和去敏纪律上已经达标，但缺少机器护栏。`AGENTS.md` 的验证命令全靠人工执行，skill 几乎没有评测，安装脚本只会叠加，且存在一处过期路由引用。

## 目标

- 把 `AGENTS.md` 中的发布前验证变成可自动执行、失败即红的门禁。
- 让安装脚本支持清理旧 skill 与预览安装结果。
- 清除仓库内不再成立的引用。
- 为高频 skill 补齐最小评测集，使触发边界可复验。

## 范围与非目标

范围：`scripts/`、`skills/*/evals/`、`environments/grok/AGENTS.md`、新增 `.github/workflows/`、必要的 README 与 CHANGELOG 同步。

非目标：

- 不新增或删除任何 skill，不改动 `SKILL.md` 正文的行为规则。
- 不改动 `skills/pro-newproj/assets/base-project/` 骨架内容。
- 不引入 Node、Python 等运行时依赖；门禁只使用 Bash、`find`、`grep`、`git`，JSON 校验允许用 runner 自带的 `python3` 或 `jq`。
- 不处理既有 `[partial]` 计划（Codex GPT 系列加固）的评测阶段。

## 当前事实

- `skills/` 下 11 个 skill，`environments/` 下 9 类宿主，README 与目录一致。
- 只有 `skills/pro-newproj/evals/evals.json` 存在，含 3 条用例；`skills/pro-copy/evals/` 是本机残留的空目录，未被 Git 跟踪。
- `scripts/install-skills.sh` 与 `scripts/install-skills.ps1` 用递归复制覆盖目标目录，不删除已从仓库移除的 skill，无 dry-run。
- `environments/grok/AGENTS.md` Tool Routing 段仍路由到 `image-gen-pro` skill；该 skill 不在本仓库，其他 8 个环境也没有图片生成路由（0.1.0 已移除）。
- 仓库无 `.github/`、无任何 CI 配置。
- `AGENTS.md` 的敏感扫描命令目前命中的均为"不要泄露 token"类说明文字，属预期噪声。

## 不变量

- `skills/` 只放可公开分发的自研 skill。
- 公开文件不出现真实凭据、内网地址、本机绝对路径或私有组织标识。
- 安装脚本不联网、不读取凭据、不静默安装外部 skill。
- 每次修改文档后，README 与目录树中的数量、链接保持一致。

## 假设

- 仓库托管在 GitHub，CI 使用 GitHub Actions；若托管方不同，阶段一改为对应平台的等价配置，脚本本身不变。
- 评测格式沿用 `skills/pro-newproj/evals/evals.json` 的字段：`skill_name`、`evals[]`（`id`、`prompt`、`expected_output`、`files`）。

## 风险

- 敏感扫描规则中的"端口 / 内部 / 客户"等词在正常说明文字中会命中，若门禁直接按命中数判失败会产生误报。阶段一采用允许清单处理。
- PowerShell 脚本在 CI 中需要 `pwsh`；Ubuntu runner 自带，无需额外安装。

## 阶段索引

| 阶段 | 文档 | 状态 |
|---|---|---|
| 一 | [最小 CI 门禁](./01-ci-gate.md) | `[done]` |
| 二 | [安装脚本清理与 dry-run](./02-install-script.md) | `[done]` |
| 三 | [清除过期引用](./03-stale-refs.md) | `[done]` |
| 四 | [补齐 skill evals](./04-skill-evals.md) | `[skipped]` |

实施结果见 [实施报告](./09-implementation-report.md)。

阶段三最小、无依赖，可最先做；阶段一与二独立；阶段四依赖阶段一（evals 结构校验纳入门禁）。

## 总体验证标准

- 在干净 clone 上执行 `bash scripts/verify.sh` 退出码为 0；人为加入一行 `sk-test123` 或删掉 README 中一个 skill 条目后退出码非 0。
- CI 在 push 与 pull request 上运行同一脚本，结果与本地一致。
- 安装脚本 `--dry-run` 不产生任何文件变化；`--clean` 后目标目录只含当前 11 个 skill。
- 全仓 `grep -RIn image-gen-pro` 无命中。
- 至少 4 个 skill 拥有各不少于 3 条的 evals，且 JSON 可被标准解析器读取。

## 回滚

四个阶段互相独立，各自回滚方式见阶段文档。整体回滚为删除 `.github/`、`scripts/verify.sh`、`scripts/verify-allowlist.txt`、新增的 `evals/` 目录，并还原 `scripts/install-skills.*` 与 `environments/grok/AGENTS.md`。

## 当前状态

`[partial]`。阶段一、二、三已于 2026-09-16 执行完毕并通过各自的成功标准；阶段四按用户指示跳过，未补 evals。

总体验证标准中，除「CI 在 push 与 pull request 上运行同一脚本」外全部达成——workflow 已写入但尚未推送，绿灯待验证。阶段四对应的「至少 4 个 skill 拥有各不少于 3 条的 evals」不适用。

详见 [实施报告](./09-implementation-report.md)。
