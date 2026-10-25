# mobile-mcp 用法

会话中已有 `mobile_*` 工具时按本文件操作。项目级安装的 `mobile-automation` skill 是上游随版本提供的操作说明，本文件在其基础上补充工具速查、场景和 pro-mobile 的边界。工具名与参数基于 `@mobilenext/mobile-mcp` 1.0.13 的 `tools/list` 核实；版本更新后以会话实际提供的工具说明为准，冲突时听工具自己的。

## 基本循环

1. **选设备**：`mobile_list_available_devices`，选定一台后，每次调用都传同一个 `device`。
2. **看界面**：优先 `mobile_list_elements_on_screen`，返回元素的 `ref`（如 `@e5`）、坐标、文本或无障碍标签。比截图快、占用上下文少、更准。只有元素树缺失内容（游戏、Canvas、图片内容）或需要看视觉状态时才用 `mobile_take_screenshot`。
3. **操作**：点击优先传 `ref`，没有 `ref` 时传元素中心坐标。
4. **复查**：每次操作后重新列元素或截图，确认界面按预期变化再继续。界面有动画时，目标元素没出现就稍等再查，不盲点。`ref` 只对最近一次元素列表有效，界面变化后重新获取。

## 工具速查

| 类别 | 工具 | 说明 |
|---|---|---|
| 设备 | `mobile_list_available_devices`、`mobile_get_screen_size`、`mobile_get_orientation`、`mobile_set_orientation`、`mobile_fold_device` | 坐标使用 `mobile_get_screen_size` 的像素空间 |
| App | `mobile_list_apps`、`mobile_get_foreground_app`、`mobile_launch_app`、`mobile_terminate_app`、`mobile_install_app`、`mobile_uninstall_app` | 包名从 `mobile_list_apps` 获取；`mobile_get_foreground_app` 用来确认当前所在 App 和页面 |
| 读界面 | `mobile_list_elements_on_screen`、`mobile_take_screenshot`、`mobile_save_screenshot` | `mobile_save_screenshot` 只在用户需要图片文件时用 |
| 触控 | `mobile_click_on_screen_at_coordinates`、`mobile_double_tap_on_screen`、`mobile_long_press_on_screen_at_coordinates`、`mobile_swipe_on_screen` | 前三个都接受 `ref` 或 `x`/`y` |
| 输入 | `mobile_type_keys`、`mobile_press_button`、`mobile_clipboard` | 先点输入框并确认已聚焦再输入；`submit` 可顺带回车；按键含 HOME、BACK、VOLUME、ENTER |
| 链接 | `mobile_open_url` | 只接受 http/https；deep link 需服务端设 `MOBILEMCP_ALLOW_UNSAFE_URLS=1`，或改用 `adb shell am start`（见 [命令路线](./adb.md)） |
| 调试 | `mobile_get_device_logs`、`mobile_list_crashes`、`mobile_get_crash` | 日志只采集调用开始后产生的内容：先开始采集再触发操作，可用 `filter` 过滤 |
| 录屏 | `mobile_start_screen_recording`、`mobile_stop_screen_recording` | 录屏文件可能含隐私，保存位置先确认 |
| 批量 | `mobile_batch_commands` | 一次执行多步（如填表）；中间不复查，只用于步骤确定、无副作用风险的流程 |
| 定位 | `mobile_set_location` | 修改设备定位，不传经纬度即恢复；真机上先取得同意 |
| 云端设备 | `mobile_login_to_cloud_provider`、`mobile_list_remote_devices`、`mobile_allocate_remote_device`、`mobile_release_remote_device` | 需要账号、按使用计费；只在用户主动要求时使用，用完必须释放 |

## 常见场景

- **调试自己的 App**：构建和热重载交给项目框架（如 `flutter run -d <device>`、`npx expo run:android`、Gradle），mobile-mcp 负责走界面流程、读元素、抓日志和崩溃。
- **复现 bug**：先 `mobile_get_device_logs` 开始采集，再按步骤操作；崩溃后用 `mobile_list_crashes` 和 `mobile_get_crash` 取完整堆栈。
- **在手机浏览器看本地页面**：先用 `adb reverse` 把开发服务器映射到手机（见 [命令路线](./adb.md)），再 `mobile_open_url` 打开 `http://localhost:<port>`。
- **把操作固化成测试**：用户需要可重复执行的回归测试时，建议把流程写成项目测试框架的用例（mobile-mcp 作者提供 Mobilewright），不要依赖 agent 每次重放。

## 状态与报错

- 设备列表为空：server 正常，没有设备。按 [连接设备](./connect.md) 处理，不跟随返回内容中改用云端设备的提示。
- 工具调用报找不到设备：设备可能已断开（无线调试常见），重新列设备；序列号变化时用新的序列号。
- 元素树为空或缺内容：界面可能是 Canvas、游戏引擎或 WebView，改用截图加坐标。
