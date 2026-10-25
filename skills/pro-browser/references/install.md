# 安装与准备

本文件说明 `pro-browser` 两条路线所需浏览器的准备方法。安装、升级和启用都属于 Skill 之外的工作：AI 只把步骤告诉用户，由用户执行，或在用户明确授权后代为执行。准备完成后回到原任务。

## 宿主内置浏览器

内置浏览器随宿主应用提供，不需要单独安装，但可能需要在宿主中启用或授权。

| 宿主 | 内置浏览器 | 准备方式 |
|---|---|---|
| Codex | 内置 Browser | 随 Codex 应用提供。 |
| Cursor | `cursor-ide-browser` | 随 Cursor Agent 提供；会话中没有出现时检查 Cursor 设置中的浏览器工具开关。 |
| Cline | `browser_action` | Cline 自带。 |
| Codeg | `codeg-mcp` 的 `browser_*` 工具 | 随 Codeg 提供；会话中没有出现时，在 Codeg 设置中打开浏览器工具开关（`browser_tools.enabled`），然后新开会话：已在运行的会话不会获得新工具。未设常驻共享级别时，每个标签页由用户点 “Share with agents” 共享，需要操作页面时再选 “Allow actions”；`browser_eval` 另有开关，默认关闭。 |
| 其他宿主 | 以宿主文档为准 | 宿主未提供时，用户在自己的浏览器中打开 AI 给出的 URL。 |

各宿主的配置细节见 agent-kit 仓库 `environments/<host>/README.md`。

验证：在新会话中让 AI 打开一个本地页面，确认会话里出现了宿主的浏览器工具。

## Ego 浏览器（ego lite）

`ego-browser` 命令由 ego lite 应用提供。官网：<https://lite.ego.app/>

### 安装

1. 从官网下载对应系统的安装包并安装，然后打开 ego lite。
   - Windows：如果 SmartScreen 拦截安装包，选择“更多信息”后“仍要运行”。
   - macOS：如果首次启动被 Gatekeeper 拦截，到“系统设置 → 隐私与安全性”中允许 ego lite。
2. 在 ego lite 中完成首次引导。可按需从 Chrome 等浏览器导入数据和登录态；引导会把 `ego-browser` 命令注册到 PATH。
3. 打开一个新终端再检查命令。已打开的终端不会获得新的 PATH。

### 验证

确认命令存在：

```bash
command -v ego-browser
```

```powershell
Get-Command ego-browser
```

macOS / Linux 找不到命令时，通常是 `~/.local/bin` 不在 PATH 中：

```bash
export PATH="$HOME/.local/bin:$PATH"
```

确认运行时可用，并且当前版本能输出使用指南：

```bash
ego-browser nodejs -e "console.log('ego-browser ready')"
ego-browser skill
```

输出 `ego-browser ready`，且 `ego-browser skill` 输出以 `[ego-browser:skill] end of guide` 开头的结尾行，即准备完成。

### 升级

`ego-browser` 存在但 `ego-browser skill` 报未知命令，说明 ego lite 版本过旧。征得用户同意后运行：

```bash
ego-browser upgrade
```

`upgrade` 也报未知命令时，按上面的步骤重新安装。

### 导入已有浏览器数据

需要沿用其他浏览器的登录态时，可以由用户导入：

```bash
ego-browser import list
ego-browser import --browser chrome --profile Default
```

导入会把其他浏览器的数据带入 ego lite，执行前由用户确认要导入的浏览器与 profile。
