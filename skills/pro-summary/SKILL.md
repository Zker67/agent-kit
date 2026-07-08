---
name: pro-summary
description: 💼 归档总结 / 总结归档 / 归档 / 总结 / Archive Context / Compress History / 更新 README / 沉淀长期记忆 / push 前同步文档。覆盖三件事：.ai_memory 归档、README+AI 文档更新、可选推送（推送必须用户显式要求）。
---

# Pro Summary

在以下情况触发：

- 用户要求补充或更新项目说明文档（README / AI 说明文档）。
- 用户希望生成给人读的 README 和给 AI 读的项目说明。
- 用户希望把当前工作完整归档，方便后续继续。
- 用户希望总结当前进展、下一步、偏好规则或长期记忆。
- 用户说出 "归档总结"、"总结归档"、"归档"、"总结"、`Archive Context`、`Compress History` 中的任何一个。
- 用户要求推送代码到 GitHub（push 前先同步更新文档）。

## 协同与互斥

- **规则维护委托 `pro-rule`**：本 skill 在归档时按需调用 `pro-rule` 流程，避免在这里重复实现 `.agent/rules/` 细节。
- **经验沉淀委托 `pro-exp`**：如果本次会话产生了可复用的解决方案经验，独立调用 `pro-exp` 生成 `.exp/` 文档；本 skill 不代劳。
- **推送默认不执行**：下方"四、"仅在用户明确说 "推送 / push / 提交到 GitHub" 时才执行；仅说 "归档 / 总结" 不等于要求 push。

## 一、工作总结与记忆归档（.ai_memory）

1. 先汇总当前阶段已经完成的工作、关键决策、未解决问题和下一步建议。
2. 优先检查项目根目录的 `.ai_memory/`；若不存在则创建，并按以下固定协议维护四个文件：
   - `1_project_context.md`
     - Mode: Read-Mostly
     - 用途: 项目核心知识库，保存已确认的 System prompts、最终代码模式、核心共识、Single Source of Truth（唯一真相源）
     - 触发: 只要形成新的"Truth（稳定事实/最终共识）"就更新
   - `2_active_task.md`
     - Mode: Snapshot / Overwrite
     - 用途: 当前任务状态、立即下一步、最新阻断
     - 触发: 每次总结时都覆盖为最新快照
   - `3_work_log.md`
     - Mode: Append-Only
     - 用途: 日常开发流水账，记录当天的简短变更日志
   - `0_archive_context.md`
     - Mode: Append-Only（按块追加）
     - 用途: 记录思维演变路径、为什么改变方向、关键取舍与上下文压缩
     - 读取规则: 开启新会话时优先读取最后一个归档块
3. `.ai_memory` 内建议遵循以下模板意图：
   - `1_project_context.md`: 项目目标、核心共识、最终确定的规则与模式
   - `2_active_task.md`: 当前任务状态、待办、下一步动作
   - `3_work_log.md`: 开发流水账
   - `0_archive_context.md`: 归档日期、核心议题背景、关键思维演变路径、下一步行动指引
4. 若只是常规总结：
   - 必须更新 `2_active_task.md`
   - 若有新的稳定事实，更新 `1_project_context.md`
   - 若本次工作值得留痕，向 `3_work_log.md` 追加简报
5. 若触发词为 `Archive Context`、`Compress History` 或"总结归档"，必须执行完整归档工作流：
   1. Review 整个会话历史
   2. 提取新的系统规则、代码模式、最终决策，并更新 `1_project_context.md`
   3. 构建 "Cognitive Evolution Path（思维演变路径）"，将深度复盘追加到 `0_archive_context.md`
   4. 用最新状态覆盖 `2_active_task.md`
   5. 如有必要，向 `3_work_log.md` 追加简短归档记录
   6. 最终向用户输出：
      `核心知识已更新至 project_context，思维路径已归档至 0_archive_context。您可以放心清理对话历史。`
6. 若会话中出现了稳定偏好或工作区硬性指令，委托 `pro-rule` 流程处理（维护 `.agent/rules/`）；本 skill 不重复实现规则提取细节，只负责判断"是否需要叫 `pro-rule`"并在归档里列出本次规则变更摘要。

## 二、文档生成（README / AGENTS.md）

1. 先理解项目目标、功能、运行方式和目录结构。
2. 检查项目根目录是否已存在 `README.md`：
   - **已存在**：在原有风格结构上更新，保留已有章节，只同步变化的内容。
   - **不存在**：从头生成完整 README。
3. README 面向人类，要求简单易懂，并尽量包含：
   - 项目简介
   - 目录
   - 功能特性
   - 使用方法与指南
   - 配置说明
   - 文档结构
   - 后续开发路线
4. README 开头可以提示其他 AI 先阅读项目内的 AI 说明文档。
5. 同时生成或更新面向 AI 的项目说明文档。若仓库已有 `AGENTS.md` 规范，则优先沿用 `AGENTS.md`；若用户明确指定 `AGENT.md`，则按用户要求执行。
6. AI 文档要帮助后续代理快速理解项目定位、实现方式、关键约束与协作规则。

## 三、文档一致性审查

文档写完或更新后，**必须执行以下审查**，再决定是否推送。

1. **层层索引完整性**：从顶层索引（如 README.md）开始，逐层向下检查每个被引用的文件/目录是否实际存在，链接是否有效。
2. **单一信息源**：同一事物（名称、路径、计数、描述）只能在一个地方定义，其他地方引用它；检查是否有多处重复定义且内容不同步。
3. **信息一致性**：在所有文档中找出对同一实体（如 skill 名称、端口号、命令格式）的全部提及，确认描述完全一致。
4. **计数类数据**：索引文件中的数量（如"共 11 个 Skills"）与实际条目数对齐。
5. **过时引用清理**：删除或重命名的内容若仍出现在任何文档中，一律修正。
6. 将发现的所有错漏记录为列表，逐一修复后再继续。

## 四、推送（需用户显式要求）

**默认不执行**。只有当用户明确说出 "推送 / push / 提交到 GitHub / push 到 main" 等动作词时，才按下列流程执行：

1. 检查当前目录是否为 Git 仓库（`git remote -v`）。
2. **是 GitHub 仓库**：
   - 先跑 `git status --short --branch` + `git diff --check`，确认没有意外混入的大文件或跨仓库改动。
   - `git add` 限定为本次归档/文档变更文件，**不要 `git add -A`**。
   - commit 信息格式：`docs: update README and AI docs`，或更贴合当次改动范围的 conventional commit。
   - 推送到远端并汇报 commit 哈希。
3. **不是 Git 仓库**：跳过推送，仅告知用户文档已在本地更新。

若用户只说 "归档 / 总结" 而未显式要求推送，**完成本地归档后停下，并在结尾提示用户是否需要 push**，不要自作主张。
