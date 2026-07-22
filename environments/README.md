# Coding Environments

本目录保存不同 coding agent 宿主的完整配置指南和可复制资产。全局 instructions 只是环境配置的一部分；模型、权限、工具、skills、subagents 和项目级规则继续由各宿主自己的配置机制承载。

## 环境清单

| 环境 | 配置指南 | 全局 instructions | 主要配置入口 |
|---|---|---|---|
| Codex / ChatGPT coding agent | [`codex/README.md`](./codex/README.md) | [`codex/AGENTS.md`](./codex/AGENTS.md) | `~/.codex/config.toml`、`~/.codex/agents/*.toml` |
| Pi Coding Agent | [`pi/README.md`](./pi/README.md) | [`pi/AGENTS.md`](./pi/AGENTS.md) | `~/.pi/agent/settings.json`、`~/.pi/agent/models.json` |
| Claude Code | [`claude-code/README.md`](./claude-code/README.md) | [`claude-code/CLAUDE.md`](./claude-code/CLAUDE.md) | `~/.claude/settings.json` |
| Gemini / Antigravity 风格工具 | [`gemini/README.md`](./gemini/README.md) | [`gemini/GEMINI.md`](./gemini/GEMINI.md) | `~/.gemini/GEMINI.md` 及宿主自己的设置入口 |
| Grok CLI | [`grok/README.md`](./grok/README.md) | [`grok/AGENTS.md`](./grok/AGENTS.md) | `~/.grok/config.toml` |
| Windsurf | [`windsurf/README.md`](./windsurf/README.md) | [`windsurf/global_rules.md`](./windsurf/global_rules.md) | `~/.codeium/windsurf/memories/global_rules.md` |

这些描述用于说明配置入口和资产分工，不是模型能力排名。模型、工具、上下文、规则加载和多代理能力应以宿主当前版本为准。

## 统一分层

每个环境按同一组边界组织：

1. **环境指南**：说明安装入口、能力映射、验证方法和限制。
2. **全局 instructions**：保存跨项目、长期稳定的协作规则。
3. **运行时配置**：保存模型、推理强度、权限、工具、MCP 和环境变量。
4. **宿主专属能力**：保存 subagents、hooks、workflows 或浏览器等配置。
5. **项目级规则**：继续放在具体项目自己的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 或规则目录中。
6. **可安装 skills**：统一来自仓库根目录 [`skills/`](../skills/)，按宿主实际扫描路径安装。

同一事实只在一个层级完整定义。不要把模型参数、token、真实 server URL、本机绝对路径或项目部署流程写进公开的全局 instructions。

## 使用方式

1. 进入对应环境目录并阅读 `README.md`。
2. 备份本机已有配置。
3. 复制全局 instructions 到宿主实际识别的入口。
4. 按指南安装 skills，并补齐 MCP、CLI、Browser 或 subagents。
5. 运行指南中的最小验证，确认宿主确实加载了目标文件。

## 从 `system-prompts/` 迁移

旧目录只表示“提示词文件”，无法覆盖完整的 coding environment 配置。当前映射如下：

| 旧文件 | 新位置 |
|---|---|
| `system-prompts/CHATGPT.md` | `environments/codex/AGENTS.md` |
| `system-prompts/CLAUDE.md` | `environments/claude-code/CLAUDE.md` |
| `system-prompts/GEMINI.md` | `environments/gemini/GEMINI.md` |
| `system-prompts/GROK.md` | `environments/grok/AGENTS.md` |
| `system-prompts/WINDSURF.md` | `environments/windsurf/global_rules.md` |

[`system-prompts/README.md`](../system-prompts/README.md) 暂时保留为迁移入口，不再保存规则正文。

Pi 环境是直接新增的配置入口，没有对应的旧 `system-prompts/` 文件。
