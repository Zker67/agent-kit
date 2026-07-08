---
name: pro-memory
description: 🧠 AI 记忆 / .ai_memory / 长期上下文 / 归档记忆 / Archive Context / Compress History。用于在用户明确要求或项目已存在 .ai_memory 约定时维护项目级长期上下文；默认不创建记忆文件，不替代 README、AGENTS.md、plans 或 AI 工具自带记忆。
---

# Pro Memory

在以下情况触发：

- 用户明确要求维护 `.ai_memory/`、AI 记忆、长期上下文、归档记忆或项目记忆。
- 用户说出 "Archive Context"、"Compress History"、"把这段记到项目记忆"、"更新 AI 记忆"、"总结归档到记忆"。
- 项目已经存在 `.ai_memory/` 约定，且用户要求按该约定更新当前上下文。

## 协同与互斥

- **与 `pro-summary` 区分**：README、AGENTS.md、文档结构、层层索引和一致性审查交给 `pro-summary`；本 skill 只维护项目级长期上下文。
- **规则维护委托 `pro-rule`**：稳定用户偏好或工作区硬性规则应写入 `.agent/rules/`，不要混进 `.ai_memory/`。
- **经验沉淀委托 `pro-exp`**：通用解决方案经验应写入 `.exp/`，不要用项目记忆替代经验文档。
- **默认不启用**：若项目没有 `.ai_memory/` 且用户只是要求更新 README、AGENTS.md 或 plans，不要创建记忆系统。

## 一、启用条件

1. 先检查项目根目录是否存在 `.ai_memory/` 或相关文档约定。
2. 若不存在，只有在用户明确要求创建项目记忆时才创建。
3. 若用户没有明确要求创建，只给出建议或说明跳过，不要为了归档而默认落盘。
4. 开源、模板或公共仓库中默认只保留说明和空占位，不写入真实上下文。

## 二、文件协议

如项目采用默认 `.ai_memory/` 结构，维护以下文件：

- `1_project_context.md`
  - Mode: Read-Mostly
  - 用途: 项目目标、架构决策、核心共识、不变量和已确认事实
  - 触发: 形成新的稳定事实或最终共识时更新
- `2_active_task.md`
  - Mode: Snapshot / Overwrite
  - 用途: 当前任务状态、立即下一步、最新阻断
  - 触发: 用户要求保存当前进展时覆盖
- `3_work_log.md`
  - Mode: Append-Only
  - 用途: 日常开发流水账和阶段性简报
  - 触发: 本次工作值得后续追踪时追加
- `0_archive_context.md`
  - Mode: Append-Only
  - 用途: 记录上下文压缩、决策演变、方向变化和关键取舍
  - 触发: 用户明确要求 `Archive Context`、`Compress History` 或深度归档时追加

若项目已有不同文件名或协议，优先遵循项目内说明。

## 三、写入原则

1. 只记录对后续协作有复用价值的信息：稳定事实、关键决策、当前阻断、下一步和已验证结论。
2. 不记录真实凭据、token、密码、私有服务地址、客户信息、个人隐私、本地机器细节或不可公开流程。
3. 不把 README、AGENTS.md、plans、`.agent/rules/` 或 `.exp/` 已经表达清楚的信息重复完整复制进 `.ai_memory/`。
4. 记忆内容要引用权威文档或源码位置，避免形成新的事实来源。
5. 无法判断是否应长期记录时，先问用户，不要擅自写入。

## 四、工作流

1. 读取 `.ai_memory/README.md` 或项目内关于记忆系统的说明。
2. 判断本次信息属于：
   - 稳定项目事实：更新 `1_project_context.md`。
   - 当前任务快照：覆盖 `2_active_task.md`。
   - 简短过程记录：追加 `3_work_log.md`。
   - 上下文压缩或决策演变：追加 `0_archive_context.md`。
3. 写入前先检查是否已有同类条目，能合并就合并，避免重复堆叠。
4. 写入后简要说明新增、更新、跳过的内容和原因。

## 五、输出要求

最终回复包含：

- 是否启用了或跳过 `.ai_memory/`。
- 更新了哪些记忆文件。
- 哪些内容因应写入 README、AGENTS.md、plans、`.agent/rules/` 或 `.exp/` 而未写入记忆。
- 如涉及敏感信息，说明已跳过或已脱敏。
