# Cursor 环境配置

本目录提供 Cursor IDE Agent 的公开配置基线。全局偏好放在 **User Rules**；MCP、IDE 设置和 skills 由 Cursor 各自入口承载。不要把 Cursor 内置系统提示词已经覆盖的通用行为再写一遍。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`user-rules.md`](./user-rules.md) | 精简 User Rules 基线 | Cursor **Settings → Rules → User Rules**（粘贴合并） |
| [`mcp.example.json`](./mcp.example.json) | 推荐 MCP：`context7` + `fast-context` | 参考后合并到 `~/.cursor/mcp.json` |
| [`settings.example.json`](./settings.example.json) | 与 Claude Code / 外部 MCP 发现脱钩的 IDE 设置 | 参考后合并到 Cursor User `settings.json` |

## 为什么规则保持精简

Cursor Agent 已内置工具循环、仓库探索、编辑、终端、Web、浏览器、skill 发现与审批机制。因此公开基线**不**重复：

- 「会用工具 / 会搜代码 / 会并行 / 会验证」等默认 harness 行为。
- 完整风格指南或日常 CLI 目录。
- Codex / Claude 专属工具 ID。

只保留 Cursor 无法替用户决定的内容：语言偏好、授权边界、以及本机实际安装的 `fast-context` / `context7` / `smart-search` 路由。

## 配置分工

| 范围 | 位置 | 内容 |
|---|---|---|
| 全局 User Rules | Settings → Rules | 跨项目偏好、授权、工具路由（见 `user-rules.md`） |
| 用户 MCP | `~/.cursor/mcp.json` | 建议仅 `context7`、`fast-context`；凭据用环境变量 |
| IDE 设置 | Cursor User `settings.json` | 可选：关闭 Claude md/hooks、关闭外部 MCP 发现 |
| 用户 skills | `~/.cursor/skills/` | 安装本仓库 `skills/*`；也可用 skills-manager 同步 |
| Cursor 内置 skills | `~/.cursor/skills-cursor/` | 产品自带，不要往这里塞自研 skill |
| 项目规则 | 仓库 `.cursor/rules/*.mdc` 或根 `AGENTS.md` | 项目事实、目录边界、测试命令 |
| 项目通用入口 | 根 `AGENTS.md` | 跨宿主共享；Cursor 可自动加载 |

**不要**把全局 always-on 规则写进 `~/.cursor/rules/`：Cursor 官方全局入口是 User Rules；`~/.cursor/rules` 不是受支持的全局规则目录。项目级 `.cursor/rules/` 仍可用于仓库内规则。

## 安装 User Rules

1. 打开 Cursor **Settings → Rules → User Rules**。
2. 备份现有文本。
3. 将 [`user-rules.md`](./user-rules.md) 正文合并进去（可按个人 Git/PR/前端细则追加，但避免与内置行为重复）。
4. 新开 Agent 会话验证是否生效。

## 安装 MCP

推荐只注册文档检索与语义代码搜索；真实 API key 放在环境变量（例如 `CONTEXT7_API_KEY`），不要写入公开示例或提交到仓库。

Git Bash / macOS / Linux（示例：在用户已备份后合并）：

```bash
mkdir -p "$HOME/.cursor"
# 备份后手动合并 environments/cursor/mcp.example.json → ~/.cursor/mcp.json
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.cursor" | Out-Null
# 备份后手动合并 environments\cursor\mcp.example.json → $HOME\.cursor\mcp.json
```

Windows 上示例使用 `cmd /c npx ...`；macOS / Linux 可改为直接 `"command": "npx"` 与对应 `args`。改完后重载 Cursor 或重启，再在 Agent 会话中确认 MCP 已连接。

## 安装 Skills

```bash
./scripts/install-skills.sh "$HOME/.cursor/skills"
```

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.cursor\skills"
```

若使用 skills-manager 等共享库：以管理器当前验证过的 Cursor 目标目录为准，避免同一 skill 多套副本。同步前可先清空 `~/.cursor/skills` 中不属于当前 preset 的残留 symlink。

## 与 Claude Code 脱钩（可选）

若希望 Cursor **不**自动读取 `CLAUDE.md`、Claude hooks，或不从其他应用发现 MCP，可合并 [`settings.example.json`](./settings.example.json) 到 Cursor User `settings.json`：

| 设置 | 作用 |
|---|---|
| `chat.useClaudeMd` | 关闭后不附加工作区 / `~/.claude` 的 `CLAUDE.md` |
| `chat.useClaudeHooks` | 关闭后不执行 Claude Code 格式 hooks |
| `chat.agentHost.claudeAgent.enabled` | 关闭 Cursor 内 Claude Agent SDK 集成面 |
| `mcp.discovery.enabled` | 关闭从其他应用配置自动发现 MCP |

这不影响 Cursor 自己的订阅模型，也不删除本机 `~/.claude/`；只是 Cursor 侧不再绑定那些入口。

## Skills 与工具

按需在 Cursor 中配置：

- 文档检索：`context7` MCP。
- 语义代码搜索：`fast-context` MCP（`fast_context_search`）。
- 联网检索：本机 `smart-search` CLI；名称不同时同步改 User Rules。
- 浏览器：使用会话中真实暴露的浏览器工具（常见 `cursor-ide-browser`）。
- 精确字符串 / 文件名：Grep / Glob。

公开配置不包含 server URL、token、个人 provider 或本机绝对路径。

## 验证

PowerShell：

```powershell
Test-Path "$HOME\.cursor\mcp.json"
Test-Path "$HOME\.cursor\skills\pro-test\SKILL.md"
```

还应在新的 Cursor Agent 会话中确认：

1. User Rules 已生效（例如默认简体中文、工具路由倾向）。
2. MCP 列表包含 `context7` 与 `fast-context`（及你有意保留的其他 server）。
3. 已安装 skill 的描述可被发现；不要只凭文件存在判断运行时已加载。

## 官方参考

- [Cursor Rules](https://cursor.com/docs/context/rules)
- [Cursor Agent](https://cursor.com/docs/agent/overview)
- [Cursor MCP](https://cursor.com/docs/context/mcp)
