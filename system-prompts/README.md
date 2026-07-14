# System Prompts 迁移说明

宿主级提示词已升级为完整的 coding environment 配置指南，并迁移到 [`environments/`](../environments/)。本目录仅作为旧链接和旧用户的过渡入口，不再保存规则正文。

| 旧文件 | 新位置 |
|---|---|
| `CHATGPT.md` | [`environments/codex/AGENTS.md`](../environments/codex/AGENTS.md) |
| `CLAUDE.md` | [`environments/claude-code/CLAUDE.md`](../environments/claude-code/CLAUDE.md) |
| `GEMINI.md` | [`environments/gemini/GEMINI.md`](../environments/gemini/GEMINI.md) |
| `GROK.md` | [`environments/grok/AGENTS.md`](../environments/grok/AGENTS.md) |
| `WINDSURF.md` | [`environments/windsurf/global_rules.md`](../environments/windsurf/global_rules.md) |

新的每个环境目录同时说明全局 instructions、运行时配置、skills、工具、项目规则和验证方式。
