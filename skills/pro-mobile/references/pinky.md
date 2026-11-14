# Pinky

[Pinky](https://github.com/DIYgod/pinky)（DIYgod/pinky，Apache-2.0）是一个桌面程序，让 agent 通过 MCP 操作用户的 iPhone 或 Android 真机，用户在电脑上看着。付款等危险步骤要用户在 Pinky 窗口里点允许；银行、钱包、密码管理器类 App 对 agent 不可见；验证码会被打码。这些规则由 Pinky 的 gateway 执行，agent 自己没法批准或绕过。

pro-mobile 在「替用户在其私人真机上办事」时优先用它，因为「边界」一节要求 AI 自觉遵守的事，Pinky 能强制执行。

Pinky 连接 agent 时会装上自己的 `SKILL.md`（agent 指南）。本文件只记录 pro-mobile 的约定：什么时候用、怎么接入、和边界的关系。两者冲突时，安装与授权边界以 pro-mobile 为准，工具用法以 Pinky 的 `SKILL.md` 和会话中的工具说明为准。

本文件基于 Pinky v2026.1114.2 的 README、`docs/mcp.md` 和 `docs/SKILL.md` 核实（2026-11）。只读了文档，未接设备实测。Pinky 的作者把项目标为 pre-alpha，部分能力写着还没在真机上试过。

## 1. 什么时候用

| 场景 | 用不用 Pinky |
|---|---|
| 在用户自己的手机上替用户做事：看消息、查订单、查余额、发消息、点外卖 | 会话有 `phone_*` 工具就用；没有时可推荐安装（见第 2 节） |
| Windows / Linux 上操作 iPhone 真机 | 只有 Pinky 能做 |
| 开发调试自己的 App | 按 SKILL.md 的开发路线（Android CLI / mobile-mcp / adb）。会话里只有 `phone_*` 工具时，也可以用 `phone_app` 装包、`phone_logs` 读日志和崩溃、`phone_device` 切换旋转 / 深色模式 / 定位 |
| 构建部署、`adb reverse` 映射开发服务器、启动或管理模拟器 | Pinky 做不了，用 Android CLI 或 adb。模拟器只能由用户在 Pinky 里启动（Add phone › Virtual phone） |

## 2. 安装与接入

Pinky 是常驻的桌面程序，要一直开着；agent 通过 `pinkyctl mcp`（stdio）连到它。安装和接入都由用户完成，AI 只说明步骤和影响：

1. 从 [Releases](https://github.com/DIYgod/pinky/releases/latest) 安装：macOS 用 dmg 或 `brew install --cask diygod/tap/pinky`，Windows 用 `pinky-setup-<版本>-amd64.exe`（不需要管理员权限；安装包还没签名，SmartScreen 会拦，要点「更多信息 › 仍要运行」），Debian / Ubuntu 用 `.deb`。
2. 在 Pinky 里 **Add phone** 连上手机：Android 打开 USB 调试，Pinky 自带 adb；iPhone 需要信任电脑、打开开发者模式和开发者磁盘镜像，iOS 26 及以下还要在装有 Xcode 的 Mac 上装一次 WebDriverAgent（免费 Apple ID 签名 7 天过期，要重装），没有它只能读屏和打开 App，不能点击输入；iOS 27 及以上不用装。Windows 上的 iPhone 要先装 Apple Devices（或 iTunes）。
3. 在 Pinky 的 **Settings › Agents** 点对应 agent 的 **Connect**。

推荐时要讲清这些代价：

- **pre-alpha**：可能有 bug，部分组合（Windows / Linux 连 iPhone、iOS 26 及以下的真机）作者还没实测。
- **会写用户级配置**：Connect 用 `claude mcp add --scope user`、`codex mcp add` 等把 MCP 加进 agent 的用户级配置（改之前会备份原文件），并把 Pinky 的 `SKILL.md` 放进用户级 skill 目录（Claude Code 是 `~/.claude/skills/pinky/`，多数其他 agent 是 `~/.agents/skills/pinky/`）。这和 mobile-mcp 的项目级安装不同。原因是 Pinky 绑定的是这台电脑上的程序和用户本人的手机，MCP 命令写的是本机路径，不适合放进项目仓库。所以接入交给用户在 Pinky 里点 Connect，AI 不替用户改 agent 配置。
- **默认上报匿名统计和崩溃报告**：可以在 Settings › Privacy 关闭，或设置 `DO_NOT_TRACK=1`。Pinky 说明不会上报屏幕、输入的文字、App 名和 PIN。
- **默认自动更新**。
- **没有 Xcode 的电脑连 iPhone**：Pinky 可以从第三方镜像（doronz88/DeveloperDiskImage）下载开发者磁盘镜像，只在用户点 Download 时才下载，并校验文件。

手动接入时，MCP 命令是 `pinkyctl mcp`。文档只说 Homebrew cask 和 Linux 安装包会把 `pinkyctl` 放进 PATH；Windows 上用程序本身的路径 `%LOCALAPPDATA%\Programs\Pinky\Pinky.exe mcp`。不要写成 `pinky mcp`：`pinky` 和 GNU coreutils 的同名命令冲突。接入后要新开会话才会出现 `phone_*` 工具。没有手机想先试用，可以用 `pinkyctl mcp --fake`（两台演示手机）。

## 3. 基本循环

1. `phone_connect { task: "查一下上周的外卖订单" }`。`task` 是用户在 Pinky 里看到的任务名，写成用户看得懂的话。多台手机时传 `device`。只需要特定 App 时传 `apps: [...]`，Pinky 会拦住超出范围的跳转；只看不改时传 `read_only: true`。第一次连接时用户要批准这个 agent，返回 `approval_pending`。
2. 操作：`phone_launch`、`phone_tap`（按 ref）、`phone_type`、`phone_swipe`、`phone_key`。每次操作后会返回屏幕的变化，通常不用再调 `phone_observe`。读长列表用 `phone_read_list`，等加载用 `phone_wait_for`。
3. `phone_release { outcome: "done", summary: "..." }` 结束任务。放弃时 `outcome` 写 `failed`，也要 release。

## 4. 结果状态与 pro-mobile 的处理

| 状态 | 处理 |
|---|---|
| `approval_pending` | 用户还在决定。用**完全相同**的参数加上 `approval_id` 再调一次；不换别的方式去做 |
| `approval_denied` | 用户拒绝或超时。读 `note`，不换方式重试，向用户汇报 |
| `blocked_by_policy` | 被规则拒绝。不用 adb、脚本或其他工具绕开；确实需要时用 `phone_request_approval` 问用户，或向用户说明 |
| `scope_denied` | 超出 agent 或任务的 App 范围。告诉用户，不扩大范围 |
| `uncertain` | 不确定有没有执行（例如点了发送后断线）。先 `phone_observe` 确认，绝不直接重做 |
| `stale` | 等待批准期间屏幕变了，这一步没有执行。重新观察再决定 |
| `device_locked` / `device_needs_setup` / `paused` / `user_took_over` | `phone_handoff { reason: "..." }` 请用户在手机上处理，等用户交还控制 |
| `stopped` | 用户按了停止。结束任务，不重新连接 |

## 5. 和「边界」的关系

Pinky 的确认是额外一层保护，不替代 pro-mobile 的授权规则：

- **对外写入照旧要授权**：发消息、发帖、下单、支付、改资料，先在对话里和用户确认目标、内容和动作，再去操作。Pinky 弹出确认时，告诉用户在 Pinky 窗口里点允许。用户设置了「始终允许」的步骤不会再弹窗，做完要告诉用户做了什么。
- **登录与验证码**：Pinky 不让 agent 输入密码和验证码，验证码也会打码。需要时用 `phone_handoff` 请用户自己输入，不索要、不复述。
- **银行、钱包类 App**：默认对 agent 隐藏。任务确实需要时，`phone_launch` 打开它，由用户决定是否允许本次任务使用。
- **安装、卸载、改设备开关**：`phone_app` 的 install / uninstall 无论 Safety 怎么设置都会请用户批准（用户可以选择本次任务内或以后同一 App 不再询问）；`phone_device` 改旋转、深色模式、定位在真机上也要用户批准，任务结束后 Pinky 会自动还原。在对话里仍按「边界」先说明影响。
- **截图和报告**：`phone_observe { save }` 和 `phone_release { export: true }` 写到 Pinky 在电脑上的数据目录。要复制进项目目录前先确认，避免把隐私提交进仓库。
- **不调用 `phone_task_run`**：它把任务交给 Pinky 内置的 agent，用用户在 Pinky 里配置的模型和 API Key，会产生费用。只在用户主动要求时使用。
- **问题反馈**：Pinky 的 `SKILL.md` 会让 agent 建议用户去报 issue。按它的要求去掉个人信息，并且只在用户同意后由用户提交或经用户确认后提交。
- **不换工具绕开 Pinky**：用 Pinky 时，同一台手机不再用 adb 或 mobile-mcp 操作；Pinky 拒绝或用户拒绝的事，不换别的工具去做。
