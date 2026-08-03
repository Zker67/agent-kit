# Coding Environments

本目录保存不同 coding agent 宿主的完整配置指南和可复制资产。全局 instructions 只是环境配置的一部分；模型、权限、工具、skills、subagents 和项目级规则继续由各宿主自己的配置机制承载。

## 环境清单

| 环境 | 配置指南 | 全局 instructions | 主要配置入口 |
|---|---|---|---|
| Codex / ChatGPT coding agent | [`codex/README.md`](./codex/README.md) | [`codex/AGENTS.md`](./codex/AGENTS.md) | `~/.codex/config.toml`、`~/.codex/agents/*.toml` |
| Cline IDE / CLI | [`cline/README.md`](./cline/README.md) | [`cline/000-global.md`](./cline/000-global.md) | `~/Documents/Cline/Rules/`、`~/.cline/`、项目 `.cline/` |
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

## 项目规则兼容

基础项目模板以根 `AGENTS.md` 作为跨工具的项目协作入口。Codex 与 Cline 可以直接读取；其他宿主若只识别 `CLAUDE.md`、`GEMINI.md` 或专用规则目录，可以创建一个很薄的宿主入口，指向 `AGENTS.md` 或只补充宿主专属差异。

同一项目规则不要在多个宿主文件中完整复制。通用规则留在 `AGENTS.md`，宿主文件只做入口或差异层。
