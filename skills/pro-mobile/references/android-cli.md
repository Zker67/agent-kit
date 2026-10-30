# Android CLI

Android CLI（`android` 命令，[官方文档](https://developer.android.com/tools/agents/android-cli)）是 Google 面向 agent 提供的 Android 开发命令行工具：读界面树、截图、按界面元素点击与输入、构建部署、管理模拟器和 SDK、查官方文档、运行 Journeys。pro-mobile 在 Android 上优先使用它。

官方随 CLI 提供 `android-cli` skill，写有操作细节：界面树字段、截图标注、Journeys 格式等。本文件只记录 pro-mobile 的约定：本机安装、项目级 skill、命令速查和边界。两者冲突时，安装与授权边界以 pro-mobile 为准，命令用法以官方 skill 和 `android <command> -h` 为准。

本文件的命令、参数和安装路径基于 Windows 上的 1.1.16717390 核实（2026-10）；涉及设备的命令只核实了参数，未接设备实测。

## 1. 本机安装 CLI

Android CLI 装在用户本机，和 `adb` 一样属于开发环境工具，不做项目级安装。先检查：

```bash
android -V
```

没有时向用户说明安装命令，由用户执行或在用户同意后执行：

| 系统 | 安装 |
|---|---|
| Windows | `winget install -e --id Google.AndroidCLI` |
| macOS Apple 芯片 | `curl -fsSL https://dl.google.com/android/cli/latest/darwin_arm64/install.sh \| bash` |
| macOS Intel | `curl -fsSL https://dl.google.com/android/cli/latest/darwin_x86_64/install.sh \| bash` |
| Linux x86-64 | `curl -fsSL https://dl.google.com/android/cli/latest/linux_x86_64/install.sh \| bash` |

官方也提供 Homebrew 和 apt-get 安装，见 [下载页](https://developer.android.com/tools/agents)。

- winget 安装后会修改 PATH，需要新开终端才能直接用 `android`；当前终端可用完整路径 `%LOCALAPPDATA%\Microsoft\WinGet\Packages\Google.AndroidCLI_*\android.exe`。
- 首次运行会解压内置组件，并显示 SDK 许可协议和数据收集说明。
- 官方 skill 写着“找不到 `android` 就直接安装”。pro-mobile 不跟随这一条，安装前仍需用户同意。

### 关闭数据收集

Android CLI 默认上报命令、子命令和参数名。每条命令都加 `--no-metrics`：

```bash
android --no-metrics layout
```

想长期关闭时，建议用户在 `~/.androidrc`（Windows 为 `%USERPROFILE%\.androidrc`）中写一行 `--no-metrics`，这个文件里的参数每次调用都会自动带上。该文件在用户目录，写入前先取得同意；没写时，AI 调用命令时自己加 `--no-metrics`。下文示例省略这个参数。

### 前置条件

- 操作真机和模拟器仍需 Android SDK Platform Tools（`adb`）：列设备、日志和官方 skill 中的坐标点击都用 `adb`。设备连接见 [连接设备](./connect.md)。
- `android info` 显示 CLI 使用的 SDK 路径。路径不存在、而用户已有 SDK 时，用 `--sdk=<path>` 指定，或写入 `.androidrc`；`android sdk` 会安装或改动 SDK 组件，执行前先说明。

## 2. 项目级安装官方 skill

在项目中使用 Android CLI 时，如果项目里还没有 `android-cli` skill，就按当前宿主把它装到项目级目录：

```bash
android skills add android-cli --project=. --agent=claude-code,codex
```

- 一定要带 `--agent`。不带时会装给所有检测到的 agent。
- 不运行 `android init`：它会把 skill 装进所有检测到的 agent 的用户级目录，属于全局安装。
- skill 是 CLI 自带的单个 `SKILL.md`，版本跟随本机 CLI，不另外锁定版本。
- 写入的是项目文件：在汇报中写出新增的目录；用户不希望改动项目时跳过，改为直接参考 `android <command> -h`。

| 宿主 | `--agent` | 写入目录（已核实） |
|---|---|---|
| Claude Code | `claude-code` | `.claude/skills/android-cli/` |
| Codex | `codex` | `.agents/skills/android-cli/` |
| Cursor | `cursor` | `.agents/skills/android-cli/` |
| Gemini CLI | `gemini` | `.agents/skills/android-cli/` |

其他宿主用 `android skills add -h` 和报错信息中列出的 agent 名称，写入后核对实际目录。

新写入的 skill 可能要新会话才会被宿主自动加载。当前会话直接读取刚写入的 `SKILL.md` 并照做即可，不必等新会话。

查看和更新：

```bash
android skills list --project=. --agent=claude-code,codex      # 项目里已装的 skill
android update                                                   # 升级 CLI
android skills update android-cli --project=. --agent=claude-code,codex
```

升级 CLI 后，同步更新项目里的 skill。

## 3. 命令速查

多台设备时，`layout`、`screen capture`、`run`、`install` 都加 `--device=<序列号>`；`input` 的 `--device` 写在子命令前，如 `android input --device=<序列号> tap 'text=登录'`。只有一台设备时会自动选择。

| 用途 | 命令 | 说明 |
|---|---|---|
| 读界面 | `android layout` | JSON 界面树，含 `text`、`resource-id`、`content-desc`、`interactions`、`state`、`bounds`、`center`；`--full` 包含全部元素，`--flat` 输出平铺列表，`-o` 写到文件 |
| 截图 | `android screen capture -o <file>` | 用于看图片内容、WebView、游戏等界面树缺失的部分 |
| 标注截图 | `android screen capture --annotate -o <file>`，`android screen resolve --screenshot <file> --string "#3"` | 给界面元素编号，再把编号换成坐标；`layout` 找不到元素时使用 |
| 点击 | `android input tap '<选择器>'` | 选择器是逗号分隔的 `key=value`：`text`、`id`、`class`、`desc`，以及 `clickable`、`focused` 等布尔字段；字符串默认按不区分大小写的子串匹配，`/.../` 表示正则 |
| 输入 | `android input text "<文本>" '<选择器>' --submit` | 替换目标输入框的内容，`--submit` 顺带回车 |
| 滚动 | `android input scroll '<容器选择器>' --dir=down --until='<目标选择器>'` | 滚到目标元素出现为止 |
| 滑动 | `android input swipe '<选择器>' --dir=left` | |
| 按键 | `android input key back` | 还有 `home`、`recents`、`enter`、`tab`、`esc` 或 Android keycode |
| 部署运行 | `android run`、`android install` | 构建或安装 APK 并启动；`install` 只安装不启动 |
| 模拟器 | `android emulator list`、`start`、`stop`、`create` | `start` 等模拟器完全启动后才返回；`remove` 会删除模拟器，先取得同意 |
| 投屏 | `android device hub` | 在电脑上打开窗口实时显示和操作设备 |
| Journeys | 见官方 skill 的 “Running journey tests” | 用自然语言写成的用户流程，保存在项目里，由 agent 按流程操作并判断结果 |

操作循环与 mobile-mcp 相同：先 `layout` 读元素，再按选择器 `input`，每步后重新 `layout` 确认结果。`tap`、`text` 匹配到多个元素时默认报错，可以收紧选择器，或用 `--match=first`；元素可能稍后才出现时加 `--wait=<毫秒>`。

官方 skill 用 `adb shell input` 加 `layout` 返回的 `center` 坐标来点击，也可以用。优先用 `android input` 的选择器，选择器无法定位时再用坐标。

日志、崩溃缓冲区、`adb reverse` 和录屏 Android CLI 没有对应命令，用 [命令路线](./adb.md) 中的 `adb` 命令。

## 4. 边界

- `android device remote` 预约 Google 数据中心的远程真机，需要 Google Cloud 项目和登录；`android auth` 登录 Google 服务；`android signals` 读取 Crashlytics 线上数据。这三项只在用户主动要求时使用，登录由用户完成。
- `android create` 生成项目、`android sdk install/remove` 改动 SDK、写 Journeys 文件，都是写入操作，执行前说明会改哪里。
- 截图和界面树的隐私规则与 [SKILL.md](../SKILL.md) 相同：截图默认放系统临时目录，保存到项目目录前先确认。
