# [done] 阶段一：最小 CI 门禁

## 目标

把 `AGENTS.md` 的"开源前至少运行"三条命令收成一个本地脚本，并在 CI 中执行，任何一项不通过即失败。

## 涉及文件

- 新增 `scripts/verify.sh`
- 新增 `scripts/verify-allowlist.txt`
- 新增 `.github/workflows/verify.yml`
- 更新 `AGENTS.md` 验证段：保留原命令说明，补充"等价于运行 `bash scripts/verify.sh`"。
- 更新 `README.md` 开发栈 / 质量检查段，提及 `scripts/verify.sh`。
- 更新 `CHANGELOG.md`。

## 步骤

1. 编写 `scripts/verify.sh`，`set -euo pipefail`，包含以下检查。每项失败打印原因并累计错误数，最后按错误数决定退出码：
   1. **敏感扫描**：执行 `AGENTS.md` 中的 grep 规则，排除 `.git/`、`CHANGELOG.md`、`plans/`。命中行与 `scripts/verify-allowlist.txt` 逐行精确比对；不在允许清单内的命中判失败。允许清单初始内容为当前全部预期噪声行，格式为 `相对路径:行内容`，不含行号以避免行号漂移。
   2. **数量对账**：统计 `skills/*/SKILL.md` 数量与 `environments/*/README.md` 数量，分别与 `README.md` 中 `N 个 skills` 和 `N 类 coding environments` 的数字比对。
   3. **Skill 清单对账**：`README.md` Skill 清单表中每个反引号 skill 名都必须在 `skills/` 存在，反之亦然。
   4. **相对链接检查**：遍历所有 `.md`，提取 `](...)` 中非 `http`、非 `#`、非 `mailto:` 的目标，去掉锚点后按文件所在目录解析，目标不存在即失败。整文件跳过 `skills/pro-readme/assets/readme-template.md`，因其链接为模板占位。
   5. **Skill frontmatter 检查**：每个 `SKILL.md` 前 10 行必须含 `name:` 与 `description:`，且 `name` 等于目录名。
   6. **evals 结构检查**：存在的 `skills/*/evals/evals.json` 必须是合法 JSON，`skill_name` 等于目录名，`evals` 非空且每条含 `id`、`prompt`、`expected_output`。优先用 `python3 -c`，缺失时回退 `jq`，两者都没有则打印警告并跳过该项。
   7. **git diff --check**：检查尾随空白与冲突标记。
2. 编写 `.github/workflows/verify.yml`：触发 `push` 与 `pull_request`，`ubuntu-latest`，步骤为 checkout、`bash scripts/verify.sh`。不缓存、不安装依赖。
3. 本地运行 `bash scripts/verify.sh`，首轮预期因允许清单为空而失败；把命中行填入允许清单后应通过。
4. 更新 `AGENTS.md`、`README.md`、`CHANGELOG.md`。

## 成功标准

- 干净工作树上 `bash scripts/verify.sh` 退出码 0。
- 以下三个人为破坏各自导致非 0 退出且输出能定位到文件：任意 `.md` 加入 `AKIA1234`；README 中把 `11 个 skills` 改为 `12`；任意 `.md` 加入指向不存在文件的链接。
- 首次 push 后 GitHub Actions 显示绿色。

## 失败分支与回滚

- 若链接检查在 Windows Git Bash 与 Linux 上结果不一致（路径分隔符或大小写），以 Linux 结果为准，脚本内注释说明。
- 回滚：删除 `scripts/verify.sh`、`scripts/verify-allowlist.txt`、`.github/`，还原 `AGENTS.md`、`README.md`、`CHANGELOG.md`。

## 待确认

- 仓库是否托管在 GitHub。若否，`verify.yml` 换成对应平台配置。
