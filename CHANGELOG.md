# Changelog

## 0.4.1 - 2026-07-22

- 为 Pi 环境补充结构化用户提问、紧凑工具显示、Markdown 预览导出和分段上下文占用条四个推荐 package。
- 更新 `settings.example.json` 和安装清单，并补充 `/reload` 后的命令、工具与 widget 验证方式。
- 在 Pi 全局 instructions 中明确 `ask_user_question` 和 `preview_export` 的使用边界，并记录 Markdown 预览所需的 Pandoc 与 Chromium 依赖。

## 0.4.0 - 2026-07-22

- 新增 Pi Coding Agent 环境，提供用户级 `AGENTS.md`、`settings.json` 和 `models.json` 公开示例。
- 记录主代理 `xhigh`、默认子代理 `medium`、仅关闭 `minimal`、OpenAI Responses、图片输入和 reasoning 的配置思路。
- 增加 `pi-subagents`、动态上下文裁剪、目标模式、FFF 和 fast-context 的 package 组合与运行时验证方法。
- 明确只全局安装 Pi CLI，不全局安装 `ai-sdk`；provider 凭据和真实服务地址继续留在个人环境配置中。
- 同步 README、环境索引、兼容性说明、发布检查清单和迁移文档中的环境数量与路径。

## 0.3.1 - 2026-07-18

- 调整 Codex / ChatGPT coding agent 的联网检索路由，默认先用 `smart-search exa-search "<query>" --num-results 5 --format json` 做轻量来源发现，证据不足或需要多源综合时再升级到完整搜索。
- 明确技术文档优先 Context7、已知 URL 优先 `smart-search fetch`，并说明完整搜索只部分并行，避免重复调用已经覆盖的路线。

## 0.3.0 - 2026-07-14

- 将 `system-prompts/` 升级为按宿主分层的 `environments/`，覆盖 Codex、Claude Code、Gemini、Grok CLI 和 Windsurf。
- 每个环境新增中文配置指南，把全局 instructions、运行时配置、skills、工具、项目规则和验证方式分开说明。
- 将五份规则资产迁移为宿主实际入口文件名，并为 Codex 增加 `config.toml` / subagent 示例、为 Claude Code 增加安全 settings 骨架。
- 保留 `system-prompts/README.md` 作为旧路径迁移入口，不再在旧目录维护规则正文。
- 同步 README、AGENTS、兼容性说明、发布检查清单和迁移文档中的路径、数量与职责边界。

## 0.2.0 - 2026-07-11

- 新增 `system-prompts/README.md`，集中说明五类宿主提示词的特点、确切用户级入口和选用方式。
- 将 Codex 提示词资产从 `system-prompts/AGENTS.md` 重命名为 `system-prompts/CHATGPT.md`，实际安装入口保持 `~/.codex/AGENTS.md`。
- 迁入 Grok CLI 的 `GROK.md`，并补齐 Claude Code、Gemini、Grok、Windsurf 的确切用户级安装路径。
- 按 GPT-5.6 官方实践精简 ChatGPT / Codex 提示词中的重复规则，补充目标与验证导向、授权边界、按需规划和稀疏进度更新。
- 为 ChatGPT / Codex 板块补充官方参考来源、设计思路、主代理与子代理推荐配置及日常任务输入模板。
- 收紧 `pro-explain` 为纯只读解释 skill，不再添加注释或修改代码文件。
- 将 `pro-test` 明确为挂机式测试修复闭环，持续执行测试、根因定位、最小修复和回归验证，直到全绿或遇到真实阻断。

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
