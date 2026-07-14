# Grok CLI 环境配置

本目录提供 Grok CLI 的公开配置基线，并保留其内置联网工具、Composer 子代理和用户级 skill 目录等宿主差异。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`AGENTS.md`](./AGENTS.md) | 用户级全局 instructions | `~/.grok/AGENTS.md` |

## 安装

```bash
mkdir -p "$HOME/.grok"
cp environments/grok/AGENTS.md "$HOME/.grok/AGENTS.md"
```

```powershell
New-Item -ItemType Directory -Force "$HOME\.grok" | Out-Null
Copy-Item .\environments\grok\AGENTS.md "$HOME\.grok\AGENTS.md"
```

## 配置分工

- `AGENTS.md`：长期协作规则和工具选择意图。
- `~/.grok/config.toml`：模型、subagents 和宿主运行参数。
- `~/.grok/skills`：Grok 实际加载的用户级 skills。
- 项目 `AGENTS.md`：项目技术栈、测试命令和业务边界。

仓库中的规则正文包含经过泛化的工具路由。安装后应按本机已经启用的 MCP、skill 和模型目录调整，不要复制个人 provider 或私有服务地址。

## 验证

新建 Grok CLI 会话，分别检查全局规则、内置联网能力、代码搜索 MCP、subagent 和目标 skill 是否真正可用。无法调用时先检查当前配置和工具注册状态。
