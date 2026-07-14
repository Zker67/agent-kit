# Windsurf 环境配置

本目录提供适合与 Windsurf 自身规则系统叠加的轻量全局 instructions。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`global_rules.md`](./global_rules.md) | 全局语言与表达约束 | `~/.codeium/windsurf/memories/global_rules.md` |

## 安装

```bash
mkdir -p "$HOME/.codeium/windsurf/memories"
cp environments/windsurf/global_rules.md "$HOME/.codeium/windsurf/memories/global_rules.md"
```

```powershell
New-Item -ItemType Directory -Force "$HOME\.codeium\windsurf\memories" | Out-Null
Copy-Item .\environments\windsurf\global_rules.md "$HOME\.codeium\windsurf\memories\global_rules.md"
```

## 配置分工

- 全局规则只放跨项目稳定偏好。
- 项目约束放在仓库规则或 `AGENTS.md` 中。
- 模型、MCP、浏览器和其他工具由 Windsurf 当前设置入口管理。
- 若 Windsurf 不原生加载本仓 `skills/`，可以将相关 `SKILL.md` 作为规则或工作流设计参考。

## 验证

重新打开工作区或新建会话，确认语言规则实际生效。若项目规则与全局规则冲突，应以更具体、优先级更高的项目规则为准。
