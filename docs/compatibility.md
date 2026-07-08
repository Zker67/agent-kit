# 兼容性说明

## 目录边界

| 目录 | 层级 | 用途 |
|---|---|---|
| `skills/` | 可安装能力 | 被 Codex 或其他支持 skill 机制的宿主加载 |
| `system-prompts/` | 宿主级全局提示词 | 放入对应 AI 工具的全局配置入口 |
| `templates/base-project/.agent/rules/` | 项目级规则 | 随具体项目提交，描述该项目的长期约束 |

## 宿主提示词

| 文件 | 目标宿主 | 说明 |
|---|---|---|
| `system-prompts/AGENTS.md` | Codex / 通用 coding agent | 来自本机用户级 Codex 标准的开源泛化版 |
| `system-prompts/CLAUDE.md` | Claude Code | 来自本机用户级 Claude 标准的开源泛化版 |
| `system-prompts/GEMINI.md` | Gemini / Antigravity 风格工具 | 来自本机用户级 Gemini 标准的开源泛化版 |
| `system-prompts/WINDSURF.md` | Windsurf | 未发现更新的用户级来源，暂保留轻量语言约束 |

开源泛化版会保留工作方式、验证和安全规则，但移除本机绝对路径、个人机器资源描述和特定私有流程引用。

## 外部工具路由

system prompts 中提到的专业搜索 CLI、Context7、语义代码搜索、MCP 或 subagents 都是可选路由规则：宿主环境提供时优先使用，不提供时按宿主自身能力降级。

本仓库不内置这些外部工具，也不要求用户安装全部工具才能使用 skills 或模板。公开版本已移除图片生成、图像编辑、视频生成和视频编辑的专用路由，避免把个人供应商、模型服务或 API 配置写进公共提示词。

## 模板入口

`templates/base-project/` 默认使用 `AGENTS.md`。若某个宿主只识别 `AGENT.md`、`CLAUDE.md` 或其他入口文件，建议创建一个很薄的转发文件，内容只指向 `AGENTS.md`，不要复制正文。
