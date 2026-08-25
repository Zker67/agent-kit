# OpenCode 环境配置

本目录提供 OpenCode 的公开配置基线。OpenCode 已内置完整的 coding-agent harness，因此 [`AGENTS.md`](./AGENTS.md) 只补充个人沟通偏好、授权边界、证据要求、外部工具路由、前端验证边界和安全规则。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`AGENTS.md`](./AGENTS.md) | 精简用户级全局 instructions | `~/.config/opencode/AGENTS.md` |

## 为什么规则保持精简

OpenCode 1.18 已通过内置系统提示词、工具定义和 agent 权限覆盖：

- 文件读取、搜索、编辑、命令和任务工具的使用方式。
- 独立工具调用并行化与依赖调用串行化。
- 脏工作树保护、禁止擅自回滚用户改动和危险 Git 操作约束。
- 修改任务的自主执行、既有代码风格保持和基础验证闭环。
- 前端基础设计要求、桌面与移动端适配和最终回复格式。
- Build、Plan、General、Explore 等内置 agent 的职责和权限。

这些内容不在全局 `AGENTS.md` 中重复。规则仅保留 OpenCode 无法替用户决定的内容，并参考本仓 [`../codex/AGENTS.md`](../codex/AGENTS.md) 的长期协作原则做宿主适配。

## 安装全局规则

先备份已有文件，再复制公开基线。

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.config\opencode" | Out-Null
Copy-Item .\environments\opencode\AGENTS.md "$HOME\.config\opencode\AGENTS.md" -Force
```

Git Bash / macOS / Linux：

```bash
mkdir -p "$HOME/.config/opencode"
cp environments/opencode/AGENTS.md "$HOME/.config/opencode/AGENTS.md"
```

OpenCode 会自动发现这个全局文件，因此无需再把它写进 `opencode.json` 的 `instructions`。`instructions` 只用于加载额外的规则文件或 glob；不要用它重复加载同一份 `AGENTS.md`。

修改全局规则或 `opencode.json` 后退出并重启 OpenCode。当前运行中的会话不会热加载配置文件。

## 配置分工

| 范围 | 位置 | 内容 |
|---|---|---|
| 全局 instructions | `~/.config/opencode/AGENTS.md` | 跨项目长期偏好、授权、工具路由和安全边界 |
| 全局配置 | `~/.config/opencode/opencode.json` | 模型、provider、MCP、permissions、plugins、references 和额外 instructions |
| 全局 agents | `~/.config/opencode/agent/*.md` | 自定义 primary agent 或 subagent |
| 全局 skills | `~/.config/opencode/skills/*/SKILL.md` | 用户级可发现 skills |
| 项目规则 | 仓库根 `AGENTS.md` | 项目事实、目录边界、测试命令和部署约束 |
| 项目配置 | `opencode.json` 或 `.opencode/` | 仅当前仓库需要的配置、agents、commands、plugins 和 skills |

OpenCode 会合并全局 `AGENTS.md` 与从当前目录向工作树根查找到的第一组项目规则。项目通用事实继续放在仓库根 `AGENTS.md`，不要复制进全局文件。

## 安装 Skills

```bash
./scripts/install-skills.sh "$HOME/.config/opencode/skills"
```

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.config\opencode\skills"
```

OpenCode 也会发现 `~/.claude/skills/` 和 `~/.agents/skills/`。如果使用共享 skill 管理器，只保留一个受管理来源，避免同一 skill 多套副本发生版本漂移。

## MCP 与凭据

全局规则默认路由到 `fast-context`、`io.github.upstash/context7` 和本机 `smart-search` CLI。只在 `opencode.json` 中注册当前环境真实提供的工具；工具名不同时同步调整规则。

API key、provider token 和私有服务地址应通过环境变量、`{env:VAR}` 或本机私有配置管理，不写入公开资产。公开仓库中的配置示例不得包含真实凭据。

## 验证

PowerShell：

```powershell
opencode --version
Test-Path "$HOME\.config\opencode\AGENTS.md"
Test-Path "$HOME\.config\opencode\skills\pro-summary\SKILL.md"
```

重启后新建会话，并确认：

1. 默认使用简体中文，且回答/计划类请求不会擅自编辑。
2. 代码探索优先选择 `fast-context`，技术文档优先选择 Context7。
3. 项目根 `AGENTS.md` 仍会与全局规则共同生效。
4. 已安装 skill 能被 `skill` 工具发现。

不要只凭文件存在判断运行时已经加载。

## 官方参考

- [Rules](https://opencode.ai/docs/rules/)
- [Config](https://opencode.ai/docs/config/)
- [Agents](https://opencode.ai/docs/agents/)
- [Permissions](https://opencode.ai/docs/permissions/)
- [Skills](https://opencode.ai/docs/skills/)
