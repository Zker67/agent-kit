# Grok CLI 环境配置

本目录提供 Grok CLI 的公开配置基线，并保留其内置联网工具、Composer 子代理和用户级 skill 目录等宿主差异。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`AGENTS.md`](./AGENTS.md) | 用户级全局 instructions | `~/.grok/AGENTS.md` |
| [`platform/`](./platform/) | `AGENTS.md` 中 `{{PLATFORM}}` 的 macOS / Windows 片段 | 由安装脚本按平台填入 |

## 安装

macOS / Git Bash：

```bash
bash scripts/install-prompt.sh grok
```

PowerShell：

```powershell
.\scripts\install-prompt.ps1 grok
```

脚本按当前平台把 [`platform/`](./platform/) 中对应的片段填入 `{{PLATFORM}}`，目标文件已存在且内容不同时先自动备份；`--dry-run` / `-DryRun` 只预览。手动安装方式见 [平台片段](../README.md#平台片段)。

## 配置分工

- `AGENTS.md`：长期协作规则和工具选择意图。
- `~/.grok/config.toml`：模型、subagents 和宿主运行参数。
- `~/.grok/skills`：Grok 实际加载的用户级 skills。
- 项目 `AGENTS.md`：项目技术栈、测试命令和业务边界。

仓库中的规则正文包含经过泛化的工具路由。安装后应按本机已经启用的 MCP、skill 和模型目录调整，不要复制个人 provider 或私有服务地址。

## 验证

新建 Grok CLI 会话，分别检查全局规则、内置联网能力、代码搜索 MCP、subagent 和目标 skill 是否真正可用。无法调用时先检查当前配置和工具注册状态。
