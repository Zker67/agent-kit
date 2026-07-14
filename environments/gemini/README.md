# Gemini 环境配置

本目录面向 Gemini CLI 及采用类似规则分层的 Antigravity 风格工具。

## 目录内容

| 文件 | 用途 | 建议入口 |
|---|---|---|
| [`GEMINI.md`](./GEMINI.md) | 用户级全局 instructions | `~/.gemini/GEMINI.md` |

## 安装

```bash
mkdir -p "$HOME/.gemini"
cp environments/gemini/GEMINI.md "$HOME/.gemini/GEMINI.md"
```

```powershell
New-Item -ItemType Directory -Force "$HOME\.gemini" | Out-Null
Copy-Item .\environments\gemini\GEMINI.md "$HOME\.gemini\GEMINI.md"
```

## 配置分工

- 用户级 `GEMINI.md`：跨工作区稳定规则。
- 工作区 `.agents/rules/`、仓库级 `GEMINI.md` 或 `AGENTS.md`：项目事实与约束。
- workflows：重复的多步骤流程。
- skills：脚本、模板、参考资料和专门能力。
- 宿主设置：模型、权限、MCP、环境变量和工具连接。

不同 Gemini 或 Antigravity 风格工具的配置文件和 skill 加载能力可能不同。安装前以当前宿主文档为准，不要把某个实现的私有目录当成通用标准。

## 验证

确认目标文件存在后，新建会话检查语言、规则优先级和工具路由是否实际生效。涉及模型、权限或 MCP 时，应同时检查宿主当前配置与运行时状态。
