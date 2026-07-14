# Codex 环境配置

本目录提供 Codex / ChatGPT coding agent 的公开配置基线。`AGENTS.md` 负责长期协作规则；模型、推理强度、权限、工具和子代理由 Codex 配置文件负责。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`AGENTS.md`](./AGENTS.md) | 用户级全局 instructions | `~/.codex/AGENTS.md` |
| [`config.example.toml`](./config.example.toml) | 主任务模型与推理强度示例 | 参考后合并到 `~/.codex/config.toml` |
| [`agents/default.example.toml`](./agents/default.example.toml) | 子代理角色示例 | 参考后写入 `~/.codex/agents/<role>.toml` |

## 安装全局 instructions

先备份已有文件，再复制公开基线。

Git Bash / macOS / Linux：

```bash
mkdir -p "$HOME/.codex"
cp environments/codex/AGENTS.md "$HOME/.codex/AGENTS.md"
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.codex" | Out-Null
Copy-Item .\environments\codex\AGENTS.md "$HOME\.codex\AGENTS.md"
```

## 配置分工

- `AGENTS.md`：语言、授权边界、工作方式、验证、安全和工具路由。
- `config.toml`：主模型、推理强度、权限、sandbox、MCP 和宿主功能。
- `agents/*.toml`：子代理角色、模型和推理强度。
- 项目根 `AGENTS.md`：项目技术栈、测试命令、目录边界和部署约束。
- `skills/`：重复工作流、脚本、模板和专门能力。

配置示例是质量优先的起点，不代表永久的最新模型或所有项目的最优档位。模型名称和可用推理档位应以当前 Codex 模型目录及官方文档为准。

## Skills 与工具

从仓库根目录安装 skills：

```bash
./scripts/install-skills.sh "$HOME/.codex/skills"
```

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.codex\skills"
```

按需在 Codex 中配置以下能力：

- 文档检索 MCP，例如 Context7。
- 语义代码搜索 MCP，例如 fast-context。
- 专业搜索 CLI。
- Codex 内置 Browser；依赖用户已有 Chrome 登录态时使用 Chrome 扩展连接的浏览器。
- 独立 TOML 定义的 subagent 角色。

公开配置不包含 server URL、token、个人 provider 或本机路径。把这些内容留在自己的 `config.toml`、环境变量或密钥管理方案中。

## 验证

PowerShell：

```powershell
Test-Path "$HOME\.codex\AGENTS.md"
Test-Path "$HOME\.codex\skills\pro-test\SKILL.md"
```

还应在 Codex 中检查实际模型、权限、MCP 和子代理是否被当前会话加载；不要只凭文件存在判断运行时已经生效。

## 任务输入建议

复杂任务尽量包含：

```text
目标：要修复、实现或确认什么。
上下文：相关路径、文件、截图、报错或复现步骤。
约束：不能改变的 API、行为、安全边界或阶段限制。
验证：完成后要运行什么，或者什么现象代表成功。
```

简单任务直接描述目标即可；跨模块、高风险或多阶段任务再使用计划能力。

## 官方参考

- [Prompting Codex](https://learn.chatgpt.com/docs/prompting#prompting-codex)
- [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model)
- [Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6)
- [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema)
