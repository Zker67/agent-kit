# 客户端路线

桌面与移动客户端的路线选择。确定路线后，子路线的组件与平台能力见下方子路线索引。

## 技术候选

| 领域 | 作者偏好 | 适用条件与例外 |
|---|---|---|
| Web 技术桌面客户端 | MyGo / Electron | 沿用 Web 界面做桌面应用时比较，不预设固定优先级。重视分发体积与资源占用、愿意用 Go 实现本地逻辑并处理系统 WebView 差异时优先评估 MyGo（Web 页面窗口，前端经生成的 TypeScript 客户端调用 Go）；依赖 Node.js 能力、特定 Chromium 行为或已有 Electron 生态集成时优先评估 Electron。两者只覆盖 macOS、Windows、Linux 桌面，需要同时覆盖手机时另行比较 Flutter 或 Expo + React Native。资源占用与响应速度按应用负载评估，不凭框架名称判断。 |
| 高性能原生桌面 | MyGo 原生 UI | 桌面是主要产品平台且满足下节条件时优先评估；指 egoist/mygo 的 `ui` 包，用 Go 编写、由 MyGo 在 GPU 上绘制，不启动 WebView。同一应用可混用原生 UI 窗口与 Web 页面窗口，复杂文档或需复用 Web 代码的部分可留在 Web 页面。项目仍处于 0.x，版本与 API 在选型时确认；不支持移动端。 |
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
| 已有 Web 页面、CSS、shadcn/ui 与浏览器生态能力 | React + MyGo / Electron；只覆盖桌面 |
| React / TypeScript 经验与业务逻辑，移动端是重点 | Expo + React Native |
| 以桌面为核心，标准而精致的组件能满足需求，重视资源与交互性能 | MyGo 原生 UI |

这是选型起点，最终取决于关键能力在目标平台上是否有可用实现。共享 UI 前确认两端产品形态足够相似：手机以浏览和轻操作为主、桌面是复杂多窗口工作台时，共享界面的收益下降。

## MyGo 原生 UI 路线的明确偏好

> 当标准化、精致的原生 UI 足够满足产品需求时，优先评估 MyGo 原生 UI 这条高性能技术路线。

适用倾向：桌面是主要产品平台，应用以基础功能和标准交互为主，对运行效率、资源占用或响应速度有较高要求；标准组件与布局能够满足需求，不需要特别风格化的视觉设计。

“不需要特别风格化”仍要求美观、精致和良好的交互体验，不意味着界面可以简陋。性能优先也不意味着仅凭框架名称认定更快。

选型时需确认：

- 目标平台支持，尤其是 Windows 上所需功能与交付方式。
- 组件覆盖、输入交互、系统集成、无障碍与打包要求。
- Go 实现与维护成本、项目 0.x 阶段的成熟度风险，以及实际的性能证据。
- 是否需要复用已有 Web UI；采用原生 UI 路线时，重新评估 UI 与状态实现，不假定可以直接沿用 Web 组件。

这些条件不足时，比较 MyGo Web 页面 / Electron、Flutter 或其他符合需求的路线，说明取舍，不盲目选择 MyGo 原生 UI。

## 官方入口

链接于 2026-10-20 核对可访问（MyGo 于 2026-10-25 核对）；失效或迁移时只更新本表。

| 领域 | 技术 | 官网 | 文档入口 | 备注 |
|---|---|---|---|---|
| Web 技术桌面客户端 / 高性能原生桌面 | MyGo | [mygo.egoist.dev](https://mygo.egoist.dev/) | [Getting started](https://mygo.egoist.dev/docs/getting-started) | 源码位于 [egoist/mygo](https://github.com/egoist/mygo)；原生 UI 见 [Native UI](https://mygo.egoist.dev/docs/ui)。 |
| Web 技术桌面客户端 | Electron | [electronjs.org](https://www.electronjs.org/) | [Docs](https://www.electronjs.org/docs/latest/) | |
| 移动端 | Expo | [expo.dev](https://expo.dev/) | [docs.expo.dev](https://docs.expo.dev/) | |
| 移动端 | React Native | [reactnative.dev](https://reactnative.dev/) | [Introduction](https://reactnative.dev/docs/getting-started) | |
| 跨平台客户端 | Flutter | [flutter.dev](https://flutter.dev/) | [docs.flutter.dev](https://docs.flutter.dev/) | 桌面见 [Desktop support](https://docs.flutter.dev/platform-integration/desktop)；Web 适用范围见 [Web FAQ](https://docs.flutter.dev/platform-integration/web/faq)；多端交互见 [Adaptive and responsive design](https://docs.flutter.dev/ui/adaptive-responsive)。 |
| 跨平台客户端 | Dart | [dart.dev](https://dart.dev/) | [Docs](https://dart.dev/docs) | |

[返回技术偏好入口](./preferences.md)
