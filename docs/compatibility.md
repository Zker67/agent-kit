# 兼容性说明

## 目录分工

| 目录 | 层级 | 用途 |
|---|---|---|
| `skills/` | 可安装能力 | 被 Codex 或其他支持 skill 机制的宿主加载 |
| `system-prompts/` | 宿主级全局提示词 | 放入对应 AI 工具的全局配置入口 |
| `templates/base-project/.agent/rules/` | 项目级规则 | 随具体项目提交，描述该项目的长期约束 |

## 宿主提示词

| 文件 | 目标宿主 | 说明 |
|---|---|---|
| `system-prompts/CHATGPT.md` | Codex / ChatGPT coding agent | 安装到 `~/.codex/AGENTS.md`；来自本机用户级 Codex 标准的开源泛化版 |
| `system-prompts/CLAUDE.md` | Claude Code | 安装到 `~/.claude/CLAUDE.md`；来自本机用户级 Claude 标准的开源泛化版 |
| `system-prompts/GEMINI.md` | Gemini / Antigravity 风格工具 | 安装到 `~/.gemini/GEMINI.md`；来自本机用户级 Gemini 标准的开源泛化版 |
| `system-prompts/GROK.md` | Grok CLI | 安装到 `~/.grok/AGENTS.md`；保留 Grok 工具、subagent 和 skill 路由约定 |
| `system-prompts/WINDSURF.md` | Windsurf | 安装到 `~/.codeium/windsurf/memories/global_rules.md`；提供轻量语言约束 |

开源泛化版保留工作方式、验证和安全规则，并使用通用路径、通用工具名和公开可读描述。
各文件的侧重点和安装入口见 [`system-prompts/README.md`](../system-prompts/README.md)。

## 外部工具路由

system prompts 中提到的外部工具都是宿主侧可选路由规则：宿主环境提供时优先使用；其他环境可按同一意图选择等价能力。

| 能力 | 常见工具名 | 用途 |
|---|---|---|
| 文档检索 MCP | `context7` | 查询库、SDK、API、CLI 或云服务官方文档。 |
| 语义代码搜索 MCP | `fast-context` | 本地仓库理解、探索性定位、调用链梳理和跨文件检索。 |
| 专业搜索 CLI | `smart-search` 或用户自己的等价工具 | 联网搜索、资料核验、网页抓取、`fetch` / `deep` 类检索。 |
| 浏览器工具 / MCP | 宿主提供的浏览器控制能力 | 打开网页、表单操作、截图和本地页面 smoke test。 |
| subagents / 并行代理 | 宿主提供的多代理能力 | 独立阅读、检索、审查或并行证据收集。 |

这些外部工具由用户在自己的宿主 MCP / CLI 配置中管理。安装 system prompts 后，建议按实际环境补齐 `context7`、`fast-context` 和专业搜索工具，或把提示词里的工具名改成当前宿主实际提供的名字。图片生成、图像编辑、视频生成和视频编辑路由适合放在个人配置或专门 skill 中，公共提示词聚焦 coding agent 的通用工作流。

## 模板入口

`templates/base-project/` 默认使用 `AGENTS.md`。若某个宿主只识别 `AGENT.md`、`CLAUDE.md` 或其他入口文件，建议创建一个很薄的转发文件，内容指向 `AGENTS.md`，让正文保持单一来源。
