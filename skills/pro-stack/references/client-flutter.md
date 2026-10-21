# Flutter 路线

采用 Flutter + Dart 后的组件与平台能力候选，按功能需要引入，不作为整套安装清单。这里的条目只用于 Flutter 界面；状态管理与路由按需求另行选择。

## 技术候选

| 领域 | 作者偏好 | 适用条件与例外 |
|---|---|---|
| Flutter UI 组件 | Forui | 工具软件、设置页、列表详情、仪表盘等同时面向鼠标与触屏的界面优先试用。浅色、深色主题各有 desktop 与 touch 变体，字号与留白随平台调整；主题覆盖颜色、排版、图标、交互状态与组件动效。自带侧边栏、可调整分栏、表单、菜单、弹层、Toast、Context Menu 等，并内置 Lucide 图标，同类能力不再另引依赖。新版本对 Flutter SDK 有最低版本要求，先固定 SDK 再确定依赖组合。 |
| Flutter UI 组件 | Material 3（Flutter 内置） | 更强调品牌风格，需要圆润的表面层次和活泼动效时评估；需要自行投入更多主题与组件设计。 |
| Flutter UI 组件 | shadcn_flutter | 偏桌面工作台、需要 Tree、Command、Menubar、Resizable 等高密度组件时，作为另一套完整底座与 Forui 比较。一个项目先选定一套主要的控件与主题体系，不混用多套底座。 |
| Flutter 骨架屏 | skeletonizer | 加载占位优先评估；基于现有 Widget 布局生成骨架，支持 Sliver 与局部忽略、替换。加载、空数据、错误与重试等状态仍由项目自己的异步状态组件统一。 |
| Flutter 弹簧动效 | motor | 自定义的按压、拖动、选中指示器等需要连续打断、重新定向的动效时评估；改变目标时保留速度。简单过渡用 Flutter 内置动画即可。 |
| Flutter 复杂 Sheet | smooth_sheets | 基础弹层不够，确实需要多档吸附、拖拽与内部滚动协调或 Sheet 内导航时再引入。“手机显示 Sheet、桌面显示 Dialog”的策略由项目适配层决定。 |
| Flutter 图表 | fl_chart | 需要图表时评估；封装少数常用图形，统一颜色、坐标轴、提示框与空数据表现。 |
| Flutter Markdown | flutter_markdown_plus | 帮助、更新记录、README、富文本输出等 Markdown 内容。原 `flutter_markdown` 已停止维护，此包由社区接续维护；代码块复制、链接行为等按应用需要再封装。 |
| Flutter 复杂表单 | reactive_forms | 出现字段联动、跨字段校验或动态表单时再引入；简单表单使用所选 UI 库的表单组件。 |
| Flutter 形状变换 | material_new_shapes | 品牌主按钮和少数强调性动效的可选装饰能力；普通卡片、输入框的圆角体系独立设计，不围绕此包展开。 |
| Flutter 表格 | data_table_2 | 普通业务表格：固定表头、分页、异步数据。延续 Material 表格体系，搭配 Forui 等非 Material 底座时需专门统一视觉。 |
| Flutter 表格 | two_dimensional_scrollables | 大量行列、双向滚动、固定行列，或高度定制的表格与树；Flutter 官方提供惰性构建的 TableView、TreeView，排序、筛选、选择、编辑等交互需自行实现。两种表格按项目实际需求先选其一。 |
| Flutter 键盘与焦点 | Shortcuts / Actions / Focus（Flutter 内置） | 应用内快捷键、焦点与键盘操作先用内置体系；它把用户意图与执行动作分开，适合命令面板、菜单与快捷键共用同一份命令定义。 |
| Flutter 文件选择 | file_selector | 系统文件打开、保存与目录选择优先评估这个官方插件；具体功能按目标平台核对。 |
| Flutter 全局快捷键 | hotkey_manager | 应用失去焦点后仍需触发的系统级快捷键；没有该需求时不引入。 |
| Flutter 跨应用拖放 | super_drag_and_drop | 确有与系统或其他应用互相拖放文件的需求时再引入；涉及原生集成，Web 上有自身限制。 |
| Flutter 窗口管理 | window_manager | 桌面窗口尺寸、位置、标题栏与关闭行为。该插件已公开说明正在迁移到 nativeapi-flutter，窗口相关调用集中在一个适配层，后续替换实现时只调整这一处。 |
| Flutter 组件目录 | Widgetbook | 积累跨项目复用的组件时尽早接入；按官方建议用独立 Flutter 应用集中展示组件、状态、主题与密度，不必每次启动完整业务流程。 |

文件、窗口、全局快捷键、跨应用拖放等平台插件跟随具体功能进入项目；希望按需引入时，放在独立 package 的依赖声明中，仅把 Dart 文件移到另一个目录不能去掉主包的插件依赖。

## 官方入口

链接于 2026-10-21 核对可访问；失效或迁移时只更新本表。

| 领域 | 技术 | 官网 | 文档入口 | 备注 |
|---|---|---|---|---|
| Flutter UI 组件 | Forui | [forui.dev](https://forui.dev/) | [Docs](https://forui.dev/docs) | 主题与 desktop / touch 变体见 [Themes](https://forui.dev/docs/concepts/themes)；面向 LLM 的文档见 [llms.txt](https://forui.dev/docs/llms.txt)；版本见 [pub.dev](https://pub.dev/packages/forui)。 |
| Flutter UI 组件 | Material 3 | [m3.material.io](https://m3.material.io/) | [Material Design for Flutter](https://docs.flutter.dev/ui/design/material) | |
| Flutter UI 组件 | shadcn_flutter | [pub.dev](https://pub.dev/packages/shadcn_flutter) | [Docs](https://sunarya-thito.github.io/shadcn_flutter/) | |
| Flutter 骨架屏 | skeletonizer | [pub.dev](https://pub.dev/packages/skeletonizer) | [README](https://pub.dev/packages/skeletonizer) | |
| Flutter 弹簧动效 | motor | [pub.dev](https://pub.dev/packages/motor) | [README](https://pub.dev/packages/motor) | |
| Flutter 复杂 Sheet | smooth_sheets | [pub.dev](https://pub.dev/packages/smooth_sheets) | [README](https://pub.dev/packages/smooth_sheets) | |
| Flutter 图表 | fl_chart | [pub.dev](https://pub.dev/packages/fl_chart) | [GitHub](https://github.com/imaNNeo/fl_chart) | 示例见 [app.flchart.dev](https://app.flchart.dev/)。 |
| Flutter Markdown | flutter_markdown_plus | [pub.dev](https://pub.dev/packages/flutter_markdown_plus) | [README](https://pub.dev/packages/flutter_markdown_plus) | 原 `flutter_markdown` 的接续维护版。 |
| Flutter 复杂表单 | reactive_forms | [pub.dev](https://pub.dev/packages/reactive_forms) | [README](https://pub.dev/packages/reactive_forms) | |
| Flutter 形状变换 | material_new_shapes | [pub.dev](https://pub.dev/packages/material_new_shapes) | [README](https://pub.dev/packages/material_new_shapes) | |
| Flutter 表格 | data_table_2 | [pub.dev](https://pub.dev/packages/data_table_2) | [README](https://pub.dev/packages/data_table_2) | |
| Flutter 表格 | two_dimensional_scrollables | [pub.dev](https://pub.dev/packages/two_dimensional_scrollables) | [README](https://pub.dev/packages/two_dimensional_scrollables) | Flutter 官方包。 |
| Flutter 键盘与焦点 | Shortcuts / Actions / Focus | [docs.flutter.dev](https://docs.flutter.dev/) | [Actions and shortcuts](https://docs.flutter.dev/ui/interactivity/actions-and-shortcuts) | 焦点见 [Focus system](https://docs.flutter.dev/ui/interactivity/focus)。 |
| Flutter 文件选择 | file_selector | [pub.dev](https://pub.dev/packages/file_selector) | [README](https://pub.dev/packages/file_selector) | Flutter 官方插件；平台支持见 README。 |
| Flutter 全局快捷键 | hotkey_manager | [pub.dev](https://pub.dev/packages/hotkey_manager) | [README](https://pub.dev/packages/hotkey_manager) | |
| Flutter 跨应用拖放 | super_drag_and_drop | [pub.dev](https://pub.dev/packages/super_drag_and_drop) | [README](https://pub.dev/packages/super_drag_and_drop) | |
| Flutter 窗口管理 | window_manager | [pub.dev](https://pub.dev/packages/window_manager) | [GitHub](https://github.com/leanflutter/window_manager) | 迁移说明见 pub.dev 页面顶部的 Migration Notice。 |
| Flutter 组件目录 | Widgetbook | [widgetbook.io](https://www.widgetbook.io/) | [docs.widgetbook.io](https://docs.widgetbook.io/) | |

[返回客户端路线](./client.md)
