# 客户端路线

桌面与移动客户端的路线选择。确定路线后，子路线的组件与平台能力见下方子路线索引。

## 技术候选

| 领域 | 作者偏好 | 适用条件与例外 |
|---|---|---|
| Web 技术桌面客户端 | Tauri / Electron | 沿用 Web 界面做桌面应用时比较，不预设固定优先级。重视分发体积、愿意处理 Rust 与系统 WebView 差异时优先评估 Tauri；依赖 Node.js 能力、特定 Chromium 行为或已有 Electron 生态集成时优先评估 Electron。Tauri 2 也支持 Android 与 iOS，复用 Web 界面同时覆盖手机时同样参与比较。资源占用与响应速度按应用负载评估，不凭框架名称判断。 |
| 高性能原生桌面 | GPUI + GPUI Kit | 桌面是主要产品平台且满足下节条件时优先评估；GPUI Kit 指 longbridge/gpui-kit，不等同于其他同名或近名项目。`gpui-kit` crate 锁定匹配的 GPUI 版本并重新导出 GPUI 与组件库，版本在选型时确认。其移动端支持仍为实验性，不作为完整的移动应用方案。 |
| 移动端 | Expo + React Native | 以移动端为主、希望沿用 React / TypeScript 经验时的偏好路线；单独评估目标系统、原生模块、发布与 UI 组件需求。需要桌面覆盖时，不默认 Expo 项目已具备完整桌面能力，按目标平台单独核对，并与 Flutter 比较。 |
| 跨平台客户端 | Flutter + Dart | 桌面与移动端都重要、希望复用大部分 UI 与业务逻辑时优先评估；Web 不是主要交付渠道，或 Web 也是应用型界面时尤其适合。官网、博客、帮助中心等内容型网站单独选择 Web 技术。先按目标平台核对关键插件（如托盘、全局快捷键、后台任务、蓝牙、音视频、富文本），桌面的键鼠、窗口尺寸与手机触控分别设计。会引入 Dart 与另一套组件生态，现有 React 组件不能直接沿用。 |

## 子路线索引

| 子路线 | 文件 | 何时读取 |
|---|---|---|
| Flutter | [client-flutter.md](./client-flutter.md) | 已选择或正在评估 Flutter + Dart，需要确定 UI 底座、组件库与桌面平台能力。 |

## 客户端路线分工

选择客户端路线，主要是在选择复用什么：

| 主要复用 | 优先评估 |
|---|---|
| 同一套界面组件与交互，同时覆盖桌面和手机 | Flutter |
| 已有 Web 页面、CSS、shadcn/ui 与浏览器生态能力 | React + Tauri / Electron；Tauri 2 可同时覆盖手机 |
| React / TypeScript 经验与业务逻辑，移动端是重点 | Expo + React Native |
| 以桌面为核心，标准而精致的组件能满足需求，重视资源与交互性能 | GPUI + GPUI Kit |

这是选型起点，最终取决于关键能力在目标平台上是否有可用实现。共享 UI 前确认两端产品形态足够相似：手机以浏览和轻操作为主、桌面是复杂多窗口工作台时，共享界面的收益下降。

## GPUI 路线的明确偏好

> 当标准化、精致的原生 UI 足够满足产品需求时，优先评估 GPUI + GPUI Kit 这条高性能技术路线。

适用倾向：桌面是主要产品平台，应用以基础功能和标准交互为主，对运行效率、资源占用或响应速度有较高要求；标准组件与布局能够满足需求，不需要特别风格化的视觉设计。

“不需要特别风格化”仍要求美观、精致和良好的交互体验，不意味着界面可以简陋。性能优先也不意味着仅凭框架名称认定更快。

选型时需确认：

- 目标平台支持，尤其是 Windows 上所需功能与交付方式。
- 组件覆盖、输入交互、系统集成、无障碍与打包要求。
- Rust 实现与维护成本，以及实际的性能证据。
- 是否需要复用已有 Web UI；采用原生 UI 路线时，重新评估 UI 与状态实现，不假定可以直接沿用 Web 组件。

这些条件不足时，比较 Tauri / Electron、Flutter 或其他符合需求的路线，说明取舍，不盲目选择 GPUI。

## 官方入口

链接于 2026-10-20 核对可访问；失效或迁移时只更新本表。

| 领域 | 技术 | 官网 | 文档入口 | 备注 |
|---|---|---|---|---|
| Web 技术桌面客户端 | Tauri | [tauri.app](https://tauri.app/) | [Guides](https://tauri.app/start/) | |
| Web 技术桌面客户端 | Electron | [electronjs.org](https://www.electronjs.org/) | [Docs](https://www.electronjs.org/docs/latest/) | |
| 高性能原生桌面 | GPUI | [gpui.rs](https://www.gpui.rs/) | [docs.rs/gpui](https://docs.rs/gpui) | 源码位于 [zed crates/gpui](https://github.com/zed-industries/zed/tree/main/crates/gpui)。 |
| 高性能原生桌面 | GPUI Kit | [gpui-kit.com](https://gpui-kit.com/) | [Getting Started](https://gpui-kit.com/docs/getting-started) | 源码位于 [longbridge/gpui-kit](https://github.com/longbridge/gpui-kit)；不等同于其他同名或近名项目。移动端状态见 [Mobile](https://gpui-kit.com/docs/mobile)。 |
| 移动端 | Expo | [expo.dev](https://expo.dev/) | [docs.expo.dev](https://docs.expo.dev/) | |
| 移动端 | React Native | [reactnative.dev](https://reactnative.dev/) | [Introduction](https://reactnative.dev/docs/getting-started) | |
| 跨平台客户端 | Flutter | [flutter.dev](https://flutter.dev/) | [docs.flutter.dev](https://docs.flutter.dev/) | 桌面见 [Desktop support](https://docs.flutter.dev/platform-integration/desktop)；Web 适用范围见 [Web FAQ](https://docs.flutter.dev/platform-integration/web/faq)；多端交互见 [Adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive)。 |
| 跨平台客户端 | Dart | [dart.dev](https://dart.dev/) | [Docs](https://dart.dev/docs) | |

[返回技术偏好入口](./preferences.md)
