# Antigravity / Gemini 环境配置

本目录面向 **Antigravity**（Google Antigravity IDE / Agentic 编码系统）及兼容的 Gemini 体系工具。

## 目录内容

| 文件 | 用途 | 建议入口 |
|---|---|---|
| [`GEMINI.md`](./GEMINI.md) | 用户级全局 instructions | `~/.gemini/GEMINI.md` |
| [`platform/`](./platform/) | `GEMINI.md` 中 `{{PLATFORM}}` 的 macOS / Windows 片段 | 由安装脚本按平台填入 |

## 安装

macOS / Git Bash：

```bash
bash scripts/install-prompt.sh gemini
```

PowerShell：

```powershell
.\scripts\install-prompt.ps1 gemini
```

脚本按当前平台把 [`platform/`](./platform/) 中对应的片段填入 `{{PLATFORM}}`，目标文件已存在且内容不同时先自动备份；`--dry-run` / `-DryRun` 只预览。手动安装方式见 [平台片段](../README.md#平台片段)。

## Antigravity 配置分工

- **全局指令 (`~/.gemini/GEMINI.md`)**：跨工作区稳定生效的全局协作与工程规范（唯一事实源，避免在 `~/.gemini/config/` 下重复放置 `AGENTS.md`）。
- **工作区规则**：项目事实与业务约束，放置于工作区 `.agents/rules/`、根目录 `GEMINI.md` 或 `AGENTS.md`。
- **Workflows**：重复的多步骤标准流程，放置于 `~/.gemini/antigravity/global_workflows/` 或工作区 `.agents/workflows/`。
- **Skills**：专用能力、自动化脚本与参考资产，挂载至 `~/.gemini/antigravity/skills/` 或由 `skills.json` 声明。
- **运行时与扩展**：模型选型（如 Gemini 3.7 Flash/Thinking）、MCP 服务器（如 `fast-context`、`context7`）、权限与 hooks 统一由 `~/.gemini/settings.json` 与 `~/.gemini/config/` 管理。

## 验证

1. 确认文件放置于 `~/.gemini/GEMINI.md`。
2. 新建会话检查全局规则是否正常加载，且未发生多重规则冗余注入。
3. 检查 MCP 服务与模型配置在运行时状态中正常就绪。

