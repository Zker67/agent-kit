# Changelog

## 0.1.0 - 2026-07-08

- 初始开源整理：加入 14 个自研 skills。
- 加入 Codex、Claude、Gemini、Windsurf 宿主级 prompts。
- 加入通用基础项目模板。
- 加入 skill 安装脚本和模板创建脚本。
- 更新 Codex、Claude、Gemini prompts 到本机较新的用户级标准，并移除本机路径耦合。
- 补齐 README 的 skill 安装、system prompts 使用、外部工具路由说明，并移除图片/视频生成路由。
- 拆分 `pro-memory`，让项目记忆从 `pro-summary` 中独立出来。
- 迁入 `pro-readme`，让 README 生成与 `pro-summary` 的一致性审查解耦。
- 新增 `pro-plans`，将根目录 `plans/` 计划写作、拆分和索引维护独立出来。
- 将宿主级 system prompts 中固定的 `plans/` 工作流移出，计划维护统一交给 `pro-plans` 或项目模板。
- 扩展基础项目模板：新增 `docs/` 当前项目文档层和 `references/` 外部参考层，明确 README、AGENTS、plans、记忆与外部资料的单一信息源分工。
- 改造仓库 README 为 `pro-readme` 家族结构，补充任意 agent 目标目录安装、`context7` / `fast-context` 等外部工具前置说明，将 hero 图移动为根级 `assets/hero.webp`，并调整为更适合公开访客阅读的正向说明口径。
