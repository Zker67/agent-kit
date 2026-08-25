# Cline 环境配置

本目录提供 Cline IDE / CLI 的公开配置基线。`000-global.md` 只补充个人沟通偏好、授权边界和工作区约束；模型、provider、工具说明、Plan / Act 合同、MCP、hooks、plugins、workflows 和运行状态继续由 Cline 自己管理。

## 目录内容

| 文件 | 用途 | 默认安装位置 |
|---|---|---|
| [`000-global.md`](./000-global.md) | Cline 专属用户级全局规则 | `~/Documents/Cline/Rules/000-global.md` |

`000-` 只是稳定排序前缀，不是 Cline 强制文件名。规则目录中的 Markdown 会进入 Cline 上下文，因此内容应保持简短、高信号，不重复 Cline 已经内置的系统提示词。

## 为什么规则保持精简

Cline 当前系统提示词和工具定义已经覆盖：

- 工作区和平台信息。
- 文件读取、代码搜索、命令、编辑、网页、MCP 和 skill 的工具参数。
- 独立工具调用并行化与改动后验证。
- Plan / Act 消息标记、Plan 模式只读限制和模式切换流程。
- 遵循既有代码约定、使用已确认依赖、避免占位实现和完成任务的基本流程。

因此本仓库不在全局 Rule 中重复这些内容，只保留 Cline 无法替用户决定的个人偏好和授权边界。尤其需要明确覆盖两点：

- Cline 内置提示词倾向在任务开始展示计划；本规则要求简单任务直接处理，复杂任务只给短计划。
- CLI 可能启用 auto-approve；工具自动批准不等于用户授权外部写入、破坏性操作、提交、推送或部署。

工具路由是例外：查找和读取 skill、MCP 本身存在成本，因此规则会像 Codex 基线一样明确指定 `skills`、`fast-context`、Context7 和 `smart-search` 的默认路线。没有复制 Codex 专属的 `browser:control-in-app-browser`；其他工具也只有在 Cline 当前会话真实暴露时才能使用。

## 安装全局规则

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\Documents\Cline\Rules" | Out-Null
Copy-Item .\environments\cline\000-global.md "$HOME\Documents\Cline\Rules\000-global.md" -Force
```

Git Bash / macOS / Linux：

```bash
mkdir -p "$HOME/Documents/Cline/Rules"
cp environments/cline/000-global.md "$HOME/Documents/Cline/Rules/000-global.md"
```

本资产默认只安装到 Cline Rules Bank：

- 不使用 `~/.agents/AGENTS.md`，因为它是可能被多个 AI 宿主读取的跨工具入口。
- 不再向 `~/.cline/rules/` 复制第二份；如果某个环境明确只使用该目录，可将它作为替代位置，但两个全局入口不要同时保留同一规则。

官方当前同时记录了两类全局路径：Cline Rules 页面将 Windows 默认 Rules Bank 写为 `~/Documents/Cline/Rules/`；配置总览则把 `~/.cline/rules/` 纳入新的跨 IDE / CLI 全局配置树，并继续将 `~/Documents/Cline/` 作为兼容搜索路径。本资产选用 Cline 已在本机创建的 Rules Bank 路径，避免在两个会被同时扫描的位置重复注入相同规则。

## 项目级规则

Cline 可以发现工作区根 `AGENTS.md`，因此项目事实、目录边界、测试命令和业务约束继续以仓库根 `AGENTS.md` 为单一入口。

只有以下内容适合放入项目 `.clinerules/` 或 `.cline/rules/`：

- 仅对 Cline 生效的项目规则。
- 需要通过 YAML frontmatter 按路径条件加载的规则。
- 需要在 Cline Rules 面板中单独启用或禁用的规则。

不要把同一规则完整复制到全局 Rule、项目 `AGENTS.md` 和 `.clinerules/`。

## 安装 Skills

Cline 官方用户级 skill 目录是 `~/.cline/skills/`，项目级目录是 `.cline/skills/`。

```bash
./scripts/install-skills.sh "$HOME/.cline/skills"
```

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.cline\skills"
```

如果使用 Skills Manager 或其他共享 skill 管理器，以管理器当前验证过的 Cline 目标目录为准，不再复制一套重复文件。

## 配置分工

| 范围 | 位置 | 内容 |
|---|---|---|
| Cline 全局规则 | `~/Documents/Cline/Rules/` | 仅对 Cline 生效的跨项目偏好和约束 |
| 全局配置 | `~/.cline/` | rules、skills、hooks、agents、plugins、cron 等配置 |
| 全局运行状态 | `~/.cline/data/` | provider、settings、session、数据库和日志等本机状态 |
| 兼容全局目录 | `~/Documents/Cline/` | Rules、Hooks、Plugins、Workflows |
| 项目配置 | `.cline/` | 项目 rules、skills、hooks、agents、plugins、cron 和 MCP 配置 |
| 项目通用规则 | `AGENTS.md` | 跨 coding agent 共享的项目事实、约束和验证要求 |

公开仓库不应提交 provider 凭据、API key、真实 MCP 地址、session、日志、数据库或本机状态文件。

## CLI 安全

CLI 默认值可能随版本变化，应先运行：

```bash
cline --version
cline --help
```

本机 Cline CLI 3.0.49 的帮助信息显示：直接传入 prompt 时默认进入 Act 模式并开启 auto-approve。审查、诊断或计划任务可显式关闭：

```bash
cline --auto-approve false --plan "<task>"
```

命令权限、sandbox、provider 和模型按本机环境配置，不写入公开全局规则。

## 验证

```powershell
cline --version
Test-Path "$HOME\Documents\Cline\Rules\000-global.md"
Test-Path "$HOME\.cline\skills\pro-summary\SKILL.md"
```

还应在 Cline Rules / Skills 面板或 CLI 运行态中确认规则与 skills 已被实际发现；不要只凭文件存在判断已经生效。

## 官方参考

- [Cline Rules](https://docs.cline.bot/customization/cline-rules)
- [Cline Config](https://docs.cline.bot/getting-started/config)
- [Cline Skills](https://docs.cline.bot/customization/skills)
- [Cline CLI Reference](https://docs.cline.bot/cli/cli-reference)
- [Cline System Prompt Fundamentals](https://cline.ghost.io/system-prompt/)
