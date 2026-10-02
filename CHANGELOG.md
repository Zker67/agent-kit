# Changelog

## 0.16.0 - 2026-10-02

- `pro-notify` 新增 `ntfy` 渠道：同时支持官方 `https://ntfy.sh` 和自建服务器。`configure --provider ntfy` 用 `--server`（不填即官方）、`--topic` 指定地址和主题，用 `--token-env` 传入可选的永久 access token；token 默认存入系统凭据库，也可以用 `--store env` 只保存变量名。
- ntfy 只有一种消息：JSON 发布到服务器根路径，固定 Markdown 渲染、最高优先级 `5`（urgent），不带标题、标签、按钮；token 放在 `Authorization: Bearer` 请求头；返回的消息对象与目标主题一致才记为成功。限流与去重按“服务器 + 主题”识别目标。服务器只接受 HTTPS，主题和 token 按 ntfy 规则校验。
- `configure` 的 `--webhook-env` 改为仅 Webhook 类渠道必填；无凭据的渠道输出 `store: none`，不需要系统凭据库。补充对应的离线测试、evals 与配置说明。
- `pro-notify` 新增默认渠道：第一个配置的渠道自动成为默认，`configure --default` 或 `default --name` 可切换；`send` 不带 `--channel` 只发默认渠道，没有默认时报 `no_default_channel`。`list` 输出增加 `format`（`text` / `markdown`）与 `default`。
- `pro-notify` 文档按需分层：`SKILL.md` 只保留授权边界和“`list` → 按格式写 → 发默认渠道”的快捷发送路径；CLI 用法、凭据、限流去重、错误码移入配置指南 `references/configuration.md`；渠道指南 `references/channels.md` 索引 `channel-ntfy.md`、`channel-feishu.md`、`channel-dingtalk.md`、`channel-wecom.md`，各自说明去哪里创建 / 订阅、怎么拿凭据、配置参数、格式与专属错误。ntfy 文档推荐主题 `agent`。

## 0.15.1 - 2026-09-28

- Cline 全局规则按 Codex 基线的结构与密度重写：补充作用域与优先级、计划落盘条件、消息发送与重要数据删除授权、阻断时先推进已授权部分、视觉效果由用户验收；删除 `fast-context` 调参与联网命令模板等展开说明，只保留 auto-approve、`browser_action`、`skills` 等 Cline 专属差异。README 中 CLI 版本更新为 3.0.65。

## 0.15.0 - 2026-09-27

- 全局 instructions 改为按平台装配：Codex、Cline、Pi、Claude Code、Gemini、Grok 的本体只留一行 `{{PLATFORM}}`，Windows 规则原样移入 `environments/<host>/platform/windows.md`，新增对应的 `platform/macos.md`；装进宿主的文件只包含当前平台的一套规则。
- 新增 `scripts/install-prompt.sh` 与 `scripts/install-prompt.ps1`：按当前系统自动识别平台（可用 `--platform` / `-Platform` 指定），装配后写入宿主位置，目标已存在且内容不同时先备份；支持 `--print` / `-Print` 与 `--dry-run` / `-DryRun`。Cursor、OpenCode、Windsurf 没有平台差异，原样安装。
- `scripts/verify.sh` 新增平台装配检查：占位唯一、两个片段齐全、装配结果不残留占位且不混入另一平台的规则；有 `pwsh` 时对账两个安装脚本的输出。各宿主 README 的安装步骤改为调用 `install-prompt` 脚本。
- skills 与脚本适配 macOS / Windows 双版本：`pro-newproj` 新增与 `new-project.ps1` 行为一致的 `new-project.sh`（`--name`、`--target-root`、`--merge`，兼容 macOS 自带 bash 3.2），`new-project.ps1` 模板路径改用正斜杠以便在 macOS / Linux 的 `pwsh` 下运行；`pro-notify` 命令示例改用 `python3` 并注明 Windows 换成 `py -3`，补充 macOS 自带 Python 可能低于 3.10 的提醒和 bash 标准输入示例；`pro-readme` 模板的端口覆盖与请求示例补充 bash 写法。
- `scripts/verify.sh` 新增 `pro-newproj` 双版本脚本检查（新建结果与模板一致、非空目录默认拒绝，有 `pwsh` 时同时检查 `.ps1`）；CI 改为在 Ubuntu 与 macOS 上各跑一遍。

## 0.14.0 - 2026-09-21

- 新增 `pro-notify`：仅由用户明确触发，支持飞书 / Lark、钉钉、企业微信群机器人纯文本通知；可立即发送，或显式启用本次任务完成、失败、需要处理三类事件通知，不默认安装 hooks。
- 附带 Python CLI、本机系统凭据库 / 环境变量引用配置、可选签名、多渠道结果、24 小时事件去重和每机器人滚动 60 秒 20 次请求限流；凭据与状态不存入 skill 安装目录。
- 附带离线测试、行为 evals 与配置说明；skill 数量从 13 更新为 14。

## 0.13.0 - 2026-09-20

- 新增 `pro-pick`：图片、音乐、视频、布局、文案等需要人拍板的接入点，AI 只记接入点、取候选、陈列成离线单文件交互 HTML；人在页面上浏览、播放、勾选、批注并导出 `result.json`，AI 再按 JSON 正式接入或补候选迭代。判断权在人，AI 意见只出现在单独的“AI 建议”字段；仅在用户明确要求时触发。
- `pro-pick` 附带 `gallery-template.html`、`protocol.md` 与 evals；产物写入项目根 `pick/`，不建索引。
- skill 数量从 12 更新为 13。

## 0.12.0 - 2026-09-20

- 新增 `pro-handoff`：一个 agent 做完或做到一半停下时，在项目根 `handoff/` 留下按角色分阶段的一次性交接件（spec / tickets / progress），让零上下文的下一个角色只看文件接着干。交接的是工件不是对话；`handoff/` 不建索引，不替代 `plans/`、`.ai_memory/` 或 `.exp/`。
- `pro-handoff` 附带 `handoff-template.md`、`ticket-template.md` 与 evals；同时在 `pro-plans`、`pro-memory`、`pro-summary` 中补充与交接件的边界说明。
- skill 数量从 11 更新为 12。

## 0.11.0 - 2026-09-16

- 新增 `scripts/verify.sh` 发布前验证门禁：敏感扫描、skill 与 environment 数量对账、README Skill 清单对账、Markdown 相对链接、`SKILL.md` frontmatter、`evals.json` 结构和 `git diff --check`，任一不通过即非 0 退出。
- 敏感扫描的预期噪声登记在 `scripts/verify-allowlist.txt`，按「路径:行内容」比对以避免行号漂移；`--update-allowlist` 复用脚本内同一份规则重新生成清单。
- 新增 `.github/workflows/verify.yml`，在 push 与 pull request 上执行同一脚本，不安装额外依赖。
- 安装脚本支持 `--dry-run` / `-DryRun` 预览和 `--clean` / `-Clean` 清理：清理只删除目标目录中已从本仓库移除的 `pro-` 前缀 skill，不触碰用户放置的其他 skill；每个 skill 复制前先删除目标同名目录，避免已删除的文件残留。
- 移除 `environments/grok/AGENTS.md` 中指向 `image-gen-pro` 的失效图片生成路由，与其余八类环境保持一致。

## 0.10.2 - 2026-09-16

- 项目级 AI 规则目录从 `.agent/` 统一改名为 `.agents/`：`pro-newproj` 模板目录及其 README、AGENTS、docs 说明同步更新；`pro-rule`、`pro-memory`、`pro-summary` 的规则写入位置改为 `.agents/rules/`。

## 0.10.1 - 2026-09-05

- Claude Code 全局 `CLAUDE.md` 对齐 Codex / Cursor 的作用域与授权边界模型：只读类请求不自动修复，计划不自动实施，Skill 不额外授权，Git 写操作须明确授权；移除“完成模块即提交”的自动提交规则。
- 补充 Claude Code 2.1.x 的 ToolSearch / deferred MCP 说明与 README 约定覆盖宿主默认的说明。
- Claude Code README 改为确定的 `~/.claude/skills/` 安装路径，补充 `~/.claude/rules/`、`settings.local.json`、`~/.claude.json` MCP 入口和工具路由前置条件。
- `settings.example.json` 从空骨架改为去敏的中性字段集合，不含权限白名单与 hooks。
- 环境索引补全 Claude Code 配置入口；顶层 README 目录树列出全部 11 个 skill。

## 0.10.0 - 2026-08-25

- 移除 `pro-test`，测试与修复继续遵循各宿主的通用编码代理流程。
- 同步更新 skill 数量、安装验证示例和失效引用。

## 0.9.0 - 2026-08-12

- 新增 `pro-newproj`，用于新建项目或为刚创建的仓库补齐 `AGENTS.md`、`.agent/rules/`、`docs/`、`references/` 和 `plans/` 完整文档骨架。
- 将原 `templates/base-project/` 迁入 `skills/pro-newproj/assets/base-project/`，作为唯一事实源，避免根模板与 skill 双重维护。
- 将原 `scripts/new-project.ps1` 收入 `pro-newproj`，默认拒绝非空目录；显式 `-Merge` 时只补缺失文件，不覆盖已有内容。

## 0.8.0 - 2026-08-12

- 移除职责属于宿主全局规则或工具路由的 `pro-must`、`use-chinese` 和 `use-internet` skills，并同步清理引用与数量。
- 精修 `pro-explain` 的解释方法，补充对象分类、最小证据、调用链 / 数据流 / 报错链、初学者表达、证据强度和输出自检。

## 0.7.0 - 2026-08-10

- 新增 OpenCode 环境：提供与 1.18 内置系统提示词去重的精简全局 `AGENTS.md`，并说明自动发现、配置分层、skills、MCP、凭据和重启验证方式。
- OpenCode 全局规则参考 Codex 基线，只补充简体中文、授权边界、成功标准、根因导向、`fast-context` / Context7 / `smart-search` 路由、前端真实浏览器验证边界和安全要求。
- 将 coding environment 数量更新为九类，并同步 README、环境索引、目录树和发布检查清单。

## 0.6.0 - 2026-08-07

- 新增 Cursor IDE Agent 环境：提供与内置 harness 去重的精简 `user-rules.md`、`mcp.example.json`（仅 `context7` + `fast-context`）和可选的 Claude / 外部 MCP 发现脱钩 `settings.example.json`。
- User Rules 只保留中文偏好、授权边界与 `fast-context` / `context7` / `smart-search` 路由，不重复 Cursor 默认工具循环与验证说教。
- 明确 Cursor 全局入口为 Settings → User Rules，不把 `~/.cursor/rules` 当作全局规则目录；skills 安装到 `~/.cursor/skills/`。
- 将 coding environment 数量更新为八类，并同步 README、环境索引和发布检查清单。

## 0.5.0 - 2026-08-03

- 新增 Cline IDE / CLI 环境，提供与内置系统提示词去重但明确保留 skill、MCP 和搜索工具路由的 `000-global.md`，以及配置分层、skills 安装、CLI 权限和运行时验证说明。
- 将 coding environment 数量更新为七类，并同步 README、环境索引和发布检查清单。
- 删除只承担旧路径说明的 `system-prompts/`、一次性迁移文档和重复的兼容性说明。
- 精简基础项目模板，移除默认预创建的 `.ai_memory/`、`.exp/`、`.ui/` 和个人笔记模板；这些能力继续由对应 skill 按需创建。
- 删除依赖旧记忆占位目录的模板规则，并同步项目模板中的目录树、单一信息源和计划边界。

## 0.4.2 - 2026-07-30

- 精简 Codex 用户级 `AGENTS.md`，合并重复的授权、代码质量、结构性修复、验证和安全规则。
- 增加通俗表达、Markdown 与按需 Mermaid 规则，并明确简单任务不套用冗长模板。
- 保留并具体写明 fast-context、Context7、smart-search、Codex Browser 和 Chrome 的工具路由，减少运行时选择成本。
- 保留“当前目录优先作为项目根目录”，移除全局后端单元测试 60 秒硬超时，让具体项目定义测试时限。

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
