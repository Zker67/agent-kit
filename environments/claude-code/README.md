# Claude Code 环境配置

本目录提供 Claude Code 的公开配置基线。`CLAUDE.md` 保存跨项目协作规则；运行参数、权限、环境变量和工具配置由 Claude Code 自己的 settings 与集成机制负责。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`CLAUDE.md`](./CLAUDE.md) | 用户级全局 instructions | `~/.claude/CLAUDE.md` |
| [`settings.example.json`](./settings.example.json) | 安全的 settings 骨架 | 参考后合并到 `~/.claude/settings.json` |

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

## 配置分工

- 用户级 `CLAUDE.md`：跨项目、长期稳定的协作规则。
- `settings.json`：权限、环境变量和宿主运行设置。
- 项目级 `CLAUDE.md` 或 `AGENTS.md`：项目技术栈、测试、目录和部署约束。
- Skills、commands、agents 或 hooks：重复流程和宿主专属自动化，按当前 Claude Code 能力配置。

不要把 token 或密码直接写进公开文件。`settings.example.json` 只提供可合并的最小骨架；新增字段前应对照当前 Claude Code 官方文档和本机版本。

## Skills 与工具

如果当前 Claude Code 版本支持 `SKILL.md` 目录，可以把仓库根 `skills/*` 安装到它实际扫描的位置；否则将需要的 `SKILL.md` 作为项目规则或命令的参考来源，不要假设 Codex 的默认目录会被自动读取。

MCP、联网搜索、浏览器、subagents 和 hooks 应使用 Claude Code 当前支持的原生配置入口。全局 instructions 只描述“何时使用哪类能力”，不保存连接参数和凭据。

## 验证

PowerShell：

```powershell
Test-Path "$HOME\.claude\CLAUDE.md"
Test-Path "$HOME\.claude\settings.json"
```

启动一个新的 Claude Code 会话，确认语言、授权边界和项目规则优先级实际生效。配置类问题要检查运行时诊断或日志，不以文件存在代替加载成功。
