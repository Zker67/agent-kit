# pro-mobile

agent 需要操作手机、模拟器或移动 App 时触发，教它选对路线：

- Android 优先用 Google 官方 Android CLI（`android` 命令）。本机没有时建议安装到本机；使用时用 `android skills add` 把官方 `android-cli` skill 装到当前项目，不用 `android init` 做全局安装。
- iOS 用 mobile-mcp：项目已配置时直接使用；未配置时推荐项目级安装，mobile-mcp 与配套的 `mobile-automation` skill 取仓库最新版本、两者同版本。
- `adb` / `xcrun simctl` 命令是降级路线，用于用户不想安装，或只需日志、`adb reverse`、录屏等 adb 独有能力的场景。

USB 调试和无线调试是同一条真机路线，连接方法按需读取。

参考文档中的安装路径、配置格式、工具名和命令都已核实（Android CLI 1.1.16717390、mobile-mcp 1.0.13，2026-10），agent 照做即可，不必重新探索。Android CLI 的设备命令只核实了参数，未接设备实测。

## 内容索引

| 入口 | 内容 |
|---|---|
| [SKILL.md](./SKILL.md) | 选路规则、设备选择和使用边界。 |
| [Android CLI](./references/android-cli.md) | 本机安装、关闭数据收集、按宿主项目级安装官方 `android-cli` skill、命令速查（`layout`、`screen`、`input`、`run`、`emulator`）和边界。 |
| [项目级安装](./references/mcp-setup.md) | 确定最新版本，安装同版本的 `mobile-automation` skill，写入 Claude Code、Codex、Cursor、Gemini CLI、OpenCode 的项目级 MCP 配置，验证与升级。 |
| [mobile-mcp 用法](./references/mcp-usage.md) | 操作循环、工具速查、常见场景和报错处理。 |
| [连接设备](./references/connect.md) | USB 调试、无线调试（配对与重连）、Android 模拟器、iOS。 |
| [命令路线](./references/adb.md) | 降级时的 `adb` 与 `xcrun simctl` 常用命令。 |
| [行为用例](./evals/evals.json) | 选路、设备、授权边界的行为用例。 |

## 使用

- “在模拟器上跑一下登录流程，看看会不会崩。”（Android）→ 用 Android CLI，项目里没有官方 skill 时先装到项目级；本机没装 CLI 时建议安装。
- “在 iPhone 模拟器上走一遍注册流程。”（macOS）→ 已配置时用 mobile-mcp；未配置时推荐项目级安装 MCP 与 skill。
- “我什么都不想装，帮我截个图看看现在手机上是什么界面。” → 命令路线。
- “无线调试连不上了。” → 按连接设备排查并重连。
