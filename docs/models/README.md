# 模型介绍

这里记录模型或模型系列的特性、适用边界和实测结论。

模型默认值和运行参数由各宿主的 [`environments/`](../../environments/) 配置入口管理；模型专用 skill 放在对应 agent 的 `environments/<agent>/skills/`。Codex 与 GPT 系列的具体记录由独立计划补充。

## 当前档案

- [`Codex / GPT 系列`](./codex-gpt-family/)：Codex surface 下的 GPT-5.6、GPT-5.5 和 GPT-5.4 记录。

这里的记录不是自动加载的 prompt，也不是官方能力排名。官方定位、用户观察、运行态事实和配置对策分开记录；没有运行态回读或重复 fixture 的内容保持待验证状态。

档案中的状态含义：

- `observed`：在指定任务、surface 和日期观察到的行为。
- `supported`：宿主或官方资料明确支持的能力或配置入口。
- `active`：当前会话已经发现并加载，必须有运行态回读证据。
