# Coding Environments

本目录保存不同 coding agent 宿主的配置指南和可复制默认配置。这里主要告诉 AI 助手：应修改哪个宿主配置、如何选择全局/专用 skill，以及哪些内容必须留在宿主自己的配置中。

## 环境清单

| 环境 | 配置指南 | 全局 instructions | 主要配置入口 |
|---|---|---|---|
| Codex / ChatGPT coding agent | [`codex/README.md`](./codex/README.md) | [`codex/AGENTS.md`](./codex/AGENTS.md) | `~/.codex/config.toml`、`~/.codex/agents/*.toml` |
| Cline IDE / CLI | [`cline/README.md`](./cline/README.md) | [`cline/000-global.md`](./cline/000-global.md) | `~/Documents/Cline/Rules/`、`~/.cline/`、项目 `.cline/` |
| Cursor IDE Agent | [`cursor/README.md`](./cursor/README.md) | [`cursor/user-rules.md`](./cursor/user-rules.md) | Cursor Settings → Rules、`~/.cursor/mcp.json`、User `settings.json` |
| OpenCode | [`opencode/README.md`](./opencode/README.md) | [`opencode/AGENTS.md`](./opencode/AGENTS.md) | `~/.config/opencode/opencode.json`、`~/.config/opencode/agent/*.md` |
| Pi Coding Agent | [`pi/README.md`](./pi/README.md) | [`pi/AGENTS.md`](./pi/AGENTS.md) | `~/.pi/agent/settings.json`、`~/.pi/agent/models.json` |
| Claude Code | [`claude-code/README.md`](./claude-code/README.md) | [`claude-code/CLAUDE.md`](./claude-code/CLAUDE.md) | `~/.claude/settings.json` |
| Antigravity / Gemini 体系 | [`gemini/README.md`](./gemini/README.md) | [`gemini/GEMINI.md`](./gemini/GEMINI.md) | `~/.gemini/GEMINI.md`、`~/.gemini/settings.json` |
| Grok CLI | [`grok/README.md`](./grok/README.md) | [`grok/AGENTS.md`](./grok/AGENTS.md) | `~/.grok/config.toml` |
| Windsurf | [`windsurf/README.md`](./windsurf/README.md) | [`windsurf/global_rules.md`](./windsurf/global_rules.md) | `~/.codeium/windsurf/memories/global_rules.md` |

这些描述用于说明配置入口和资产分工，不是模型能力排名。模型、工具、上下文、规则加载和多代理能力应以宿主当前版本为准。

## 修改默认配置和 skills

1. 先进入目标宿主目录，读取对应的 `README.md`。
2. 只修改仓库内的公开示例和默认 instructions；用户真实配置仍由宿主目录管理，先备份再合并。
3. 全局自研 skill 从仓库根目录 [`skills/`](../skills/) 安装。
4. 通用自研 skill 从仓库根目录 [`skills/`](../skills/) 获取；agent 专用 skill 从对应的 `environments/<agent>/skills/` 获取。
5. Agent 和模型的说明见 [`docs/agents/`](../docs/agents/) 与 [`docs/models/`](../docs/models/)，不要把说明文档当作运行时配置入口。
6. 修改后按宿主 README 的最小验证检查实际发现和加载结果。

## 统一分层

每个环境按同一组边界组织：

1. **环境指南**：说明安装入口、能力映射、验证方法和限制。
2. **全局 instructions**：保存跨项目、长期稳定的协作规则。
3. **运行时配置**：保存模型、推理强度、权限、工具、MCP 和环境变量。
4. **宿主专属能力**：保存 subagents、hooks、workflows 或浏览器等配置。
5. **项目级规则**：继续放在具体项目自己的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 或规则目录中。
6. **可安装 skills**：统一来自仓库根目录 [`skills/`](../skills/)，按宿主实际扫描路径安装。
7. **skill 分层参考**：通用 skill 在根目录 `skills/`，专用 skill 在对应的 `environments/<agent>/skills/`。

同一事实只在一个层级完整定义。不要把模型参数、token、真实 server URL、本机绝对路径或项目部署流程写进公开的全局 instructions。

## 项目规则兼容

基础项目模板以根 `AGENTS.md` 作为跨工具的项目协作入口。Codex、Cline 与 OpenCode 可以直接读取；其他宿主若只识别 `CLAUDE.md`、`GEMINI.md` 或专用规则目录，可以创建一个很薄的宿主入口，指向 `AGENTS.md` 或只补充宿主专属差异。

同一项目规则不要在多个宿主文件中完整复制。通用规则留在 `AGENTS.md`，宿主文件只做入口或差异层。
