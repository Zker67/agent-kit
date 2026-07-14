# 兼容性说明

## 目录分工

| 目录 | 层级 | 用途 |
|---|---|---|
| `skills/` | 可安装能力 | 被 Codex 或其他支持 skill 机制的宿主加载 |
| `environments/` | Coding environment 配置 | 按宿主说明全局 instructions、运行时配置、skills、工具和验证方式 |
| `system-prompts/` | 迁移入口 | 只保存旧路径到 `environments/` 的映射 |
| `templates/base-project/.agent/rules/` | 项目级规则 | 随具体项目提交，描述该项目的长期约束 |

## Coding environments

| 环境目录 | 目标宿主 | 全局 instructions |
|---|---|---|
| `environments/codex/` | Codex / ChatGPT coding agent | `AGENTS.md` → `~/.codex/AGENTS.md` |
| `environments/claude-code/` | Claude Code | `CLAUDE.md` → `~/.claude/CLAUDE.md` |
| `environments/gemini/` | Gemini / Antigravity 风格工具 | `GEMINI.md` → `~/.gemini/GEMINI.md` |
| `environments/grok/` | Grok CLI | `AGENTS.md` → `~/.grok/AGENTS.md` |
| `environments/windsurf/` | Windsurf | `global_rules.md` → `~/.codeium/windsurf/memories/global_rules.md` |

各环境目录的公开资产保留工作方式、验证和安全规则，并使用通用路径、通用工具名和公开可读描述。模型、权限、MCP、subagents 等运行时配置与全局 instructions 分开维护。
完整分层和安装入口见 [`environments/README.md`](../environments/README.md)。

## 外部工具路由

环境 instructions 中提到的外部工具都是宿主侧可选路由规则：宿主环境提供时优先使用；其他环境可按同一意图选择等价能力。

| 能力 | 常见工具名 | 用途 |
|---|---|---|
| 文档检索 MCP | `context7` | 查询库、SDK、API、CLI 或云服务官方文档。 |
| 语义代码搜索 MCP | `fast-context` | 本地仓库理解、探索性定位、调用链梳理和跨文件检索。 |
| 专业搜索 CLI | `smart-search` 或用户自己的等价工具 | 联网搜索、资料核验、网页抓取、`fetch` / `deep` 类检索。 |
| 浏览器工具 / MCP | 宿主提供的浏览器控制能力 | 打开网页、表单操作、截图和本地页面 smoke test。 |
| subagents / 并行代理 | 宿主提供的多代理能力 | 独立阅读、检索、审查或并行证据收集。 |

这些外部工具由用户在自己的宿主 MCP / CLI 配置中管理。采用环境指南后，建议按实际环境补齐 `context7`、`fast-context` 和专业搜索工具，或把 instructions 中的工具名改成当前宿主实际提供的名字。图片生成、图像编辑、视频生成和视频编辑路由适合放在个人配置或专门 skill 中，公开环境资产聚焦 coding agent 的通用工作流。

## 模板入口

`templates/base-project/` 默认使用 `AGENTS.md`。若某个宿主只识别 `AGENT.md`、`CLAUDE.md` 或其他入口文件，建议创建一个很薄的转发文件，内容指向 `AGENTS.md`，让正文保持单一来源。
