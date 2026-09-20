# [skipped] 阶段四：补齐 skill evals

## 目标

为使用频率最高、触发边界最容易混淆的 skill 各补不少于 3 条评测用例，使"该触发 / 不该触发 / 与相邻 skill 的分界"可复验。格式沿用 `skills/pro-newproj/evals/evals.json`。

## 涉及文件

新增：

- `skills/pro-summary/evals/evals.json`
- `skills/pro-readme/evals/evals.json`
- `skills/pro-plans/evals/evals.json`
- `skills/pro-explain/evals/evals.json`

更新：`CHANGELOG.md`；若 README 目录树逐 skill 列出了 `evals/`，同步。

## 用例设计要求

每个 skill 至少覆盖三类：

1. **正向触发**：典型请求，`expected_output` 描述应产生的文件或回复形态。
2. **边界拒绝**：看似相关但应交给相邻 skill 或留在对话中的请求。已知易混对：`pro-summary` 与 `pro-readme`（审查一致性 vs 生成 README）、`pro-plans` 与对话内规划（落盘 vs 不落盘）、`pro-explain` 与修复请求（只读解释 vs 改代码）。
3. **授权边界**：请求隐含超出 skill 授权的动作（如 commit、改业务代码），`expected_output` 明确该动作不应发生。

`prompt` 用简体中文书写，与用户实际口吻一致；`expected_output` 写可观察结果，不写内部推理；`files` 无需夹带样例时保持 `[]`。

## 步骤

1. 按上述要求为 4 个 skill 各写 3 到 4 条用例。
2. 用阶段一的 `scripts/verify.sh` 校验 JSON 结构与 `skill_name`。
3. 在任一支持 skill 的宿主中，对每条用例至少人工跑一次，把与预期不符的结果记入实施报告，不在本阶段修改 `SKILL.md`。
4. CHANGELOG 记录。

## 成功标准

- 4 个新 `evals.json` 通过 `scripts/verify.sh`。
- 每个文件不少于 3 条用例，且三类要求各至少 1 条。
- 实施报告列出人工试跑结果，标明通过 / 不符 / 未跑。

## 失败分支与回滚

- 若试跑发现 `SKILL.md` 的 description 触发词不足以区分相邻 skill，只记录，不改正文；后续另开计划。
- 回滚：删除 4 个新增 `evals/` 目录，还原 `CHANGELOG.md`。

## 待确认

- 是否也给 `pro-copy` 补 evals。它依赖外部搜索能力，用例可写但难以离线复验，默认本阶段不含。
