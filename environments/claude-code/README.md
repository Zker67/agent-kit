# Claude Code 环境配置

本目录提供 Claude Code 的公开配置基线。`CLAUDE.md` 保存跨项目协作规则与授权边界；运行参数、权限、环境变量、hooks 和 MCP 由 Claude Code 自己的配置文件负责。基线按 Claude Code 2.1.x 编写，更早版本请以本机 `claude --version` 对应的官方文档为准。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | 用户级全局 instructions | `~/.claude/CLAUDE.md` |
| [`settings.example.json`](./settings.example.json) | 去敏后的 settings 骨架 | 参考后合并到 `~/.claude/settings.json` |

## 安装全局 instructions

Git Bash / macOS / Linux：

```bash
mkdir -p "$HOME/.claude"
cp environments/claude-code/CLAUDE.md "$HOME/.claude/CLAUDE.md"
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.claude" | Out-Null
Copy-Item .\environments\claude-code\CLAUDE.md "$HOME\.claude\CLAUDE.md"
```

覆盖前先备份本机已有文件。本机副本可以在仓库版之上追加只属于自己的路由，例如生图 / 生视频 skill、部署 skill，这些不回写到公开仓库。

## 安装 skills

Claude Code 从 `~/.claude/skills/<name>/SKILL.md` 加载用户级 skill，项目级放在 `<project>/.claude/skills/`。仓库根 `skills/*` 用安装脚本直接复制：

```bash
./scripts/install-skills.sh "$HOME/.claude/skills"
```

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.claude\skills"
```

安装后在新会话里调用 `/pro-summary` 一类的 skill 名确认已被列出。

## 配置分工

| 层 | 位置 | 放什么 |
|---|---|---|
| 全局 instructions | `~/.claude/CLAUDE.md` | 跨项目、长期稳定的协作规则与授权边界 |
| 模块化全局规则 | `~/.claude/rules/*.md` | 可选。按主题拆分的补充规则，与 `CLAUDE.md` 一起加载 |
| 运行时设置 | `~/.claude/settings.json` | 语言、effort、权限、环境变量、hooks、statusLine |
| 本机覆盖 | `~/.claude/settings.local.json` | 不进版本控制的个人开关 |
| MCP servers | `claude mcp add ...` 写入 `~/.claude.json` | `context7`、`fast-context` 等 server 的命令、URL 与 env |
| 项目规则 | `<project>/CLAUDE.md` 或 `AGENTS.md` | 技术栈、测试、目录和部署约束 |
| Skills / agents / commands / hooks | `~/.claude/skills/`、`~/.claude/agents/`、`~/.claude/commands/`、settings 的 `hooks` | 重复流程与宿主专属自动化 |

不要把 token、密码、私有组织名、内网地址或本机绝对路径写进公开文件。`settings.example.json` 只保留与身份、路径无关的中性字段；权限白名单和 hooks 与本机强绑定，不进入公开骨架。

## 工具路由前置

`CLAUDE.md` 的路由假设本机已具备：

- `context7` MCP：`claude mcp add context7 -- npx -y @upstash/context7-mcp`，或按官方文档注册。
- `fast-context` MCP：按其官方说明注册；缺失时把 `CLAUDE.md` 中对应条目改成 Grep/Glob。
- `smart-search` CLI：在 PATH 中可执行；本机若使用其他搜索 CLI，同步改路由名。

MCP 工具在会话开始时常处于 deferred / connecting 状态，需先用 ToolSearch 加载 schema 再调用，这是 Claude Code 2.1.x 的正常行为，不是配置错误。

## 验证

PowerShell：

```powershell
Test-Path "$HOME\.claude\CLAUDE.md"
Test-Path "$HOME\.claude\settings.json"
Test-Path "$HOME\.claude\skills\pro-summary\SKILL.md"
claude mcp list
```

启动一个新的 Claude Code 会话，确认回复语言、只读 / 修改 / Git 三级授权边界和项目规则优先级实际生效。配置类问题看运行时诊断或日志，不以文件存在代替加载成功。
