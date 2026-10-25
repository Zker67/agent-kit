# Web 与 React 路线

网站、Web 应用，以及用 React 实现的界面（含 MyGo / Electron 内的前端）。这里的组件、状态与交互库只用于 React 界面。

## 技术候选

| 领域 | 作者偏好 | 适用条件与例外 |
|---|---|---|
| Web 前端基础 | React 19 + TypeScript 7 + Tailwind CSS 4 | React 生态项目的目标组合；根据框架、依赖与构建链核验可用版本，不能直接假定整组兼容。 |
| Web 工程工具链 | Vite Plus（Vite+） | Vite 体系项目优先评估；与应用框架分别判断，使用 Next.js 等框架时保留框架自身的构建方式，不额外强塞另一套构建流程。已稳定运行的普通 Vite 项目可以保留，迁移收益单独评估。 |
| Web UI 组件 | shadcn/ui（Nova 风格） | 用于相应的 Web React 界面；组件源码拷入项目，可控、可改、不绑死，基于 Radix / Base UI + Tailwind，设计语言统一。Nova 偏紧凑（padding 更小），适合后台与数据密集型界面；它不是唯一最优解，需要宽松视觉的页面按设计需求选择风格。移动端和原生桌面 UI 分别选择适配的组件。 |
| 图标 | Lucide | Feather 的活跃维护版，线条风格统一、干净，支持 tree-shaking；与 shadcn/ui 配合使用。 |
| 动画 | Motion（原 Framer Motion） | React 界面需要过渡、手势、布局动画或弹簧动画时评估；声明式 API、生产使用广泛。简单状态过渡可由 CSS 完成时不增加依赖。 |
| 可调整分栏 | react-resizable-panels | 后台、IDE 风格等需要可拖动调整大小的分栏布局时使用；没有该交互时不引入。 |
| 拖拽 | dnd-kit | 需要排序、看板、拖放等交互时评估；模块化、可访问性好，相比 react-dnd 更轻量灵活。 |
| 服务端状态 | TanStack Query | 需要远程数据获取、缓存或同步时评估；不把它当成独立后端。 |
| 客户端状态 | Zustand | 需要共享状态时评估；API 极简、无需 Provider、按需订阅，适用于中小到中大型项目。局部状态足够时不增加状态库。 |
| Web 应用框架 | Next.js | 需要 React 全栈、服务端渲染、搜索可见性或服务端业务能力时优先评估。以客户端交互为主、已有独立 API 的后台、工作台和浏览器工具，评估 React + Vite+，按需加路由。MyGo 等桌面 Web 容器使用 SPA 或静态导出的前端，不承接 Next.js 的服务端运行能力。 |
| 内容网站 | Astro | 官网、博客、文档、内容展示与落地页优先评估；以内容和搜索可见性为主，需要交互的局部可嵌入 React 等组件。简单静态页面可选更轻的方案；需要 React 全栈或较多服务端业务时回到 Next.js 评估。 |

## 官方入口

链接于 2026-10-20 核对可访问；失效或迁移时只更新本表。

| 领域 | 技术 | 官网 | 文档入口 | 备注 |
|---|---|---|---|---|
| Web 前端基础 | React | [react.dev](https://react.dev/) | [API Reference](https://react.dev/reference/react) | |
| Web 前端基础 | TypeScript | [typescriptlang.org](https://www.typescriptlang.org/) | [Documentation](https://www.typescriptlang.org/docs/) | |
| Web 前端基础 | Tailwind CSS | [tailwindcss.com](https://tailwindcss.com/) | [Docs](https://tailwindcss.com/docs) | |
| Web 工程工具链 | Vite+ | [viteplus.dev](https://viteplus.dev/) | [Getting Started](https://viteplus.dev/guide/) | |
| Web UI 组件 | shadcn/ui | [ui.shadcn.com](https://ui.shadcn.com/) | [Docs](https://ui.shadcn.com/docs) | Nova 风格在 [create](https://ui.shadcn.com/create) 页的 Style 中选择；更新见 [Changelog](https://ui.shadcn.com/docs/changelog)。 |
| Web UI 组件 | Radix Primitives | [radix-ui.com](https://www.radix-ui.com/primitives) | [Primitives](https://www.radix-ui.com/primitives) | shadcn/ui 的底层原语之一。 |
| Web UI 组件 | Base UI | [base-ui.com](https://base-ui.com/) | [base-ui.com](https://base-ui.com/) | shadcn/ui 的底层原语之一。 |
| 图标 | Lucide | [lucide.dev](https://lucide.dev/) | [lucide-react](https://lucide.dev/guide/packages/lucide-react) | |
| 动画 | Motion | [motion.dev](https://motion.dev/) | [Motion for React](https://motion.dev/docs/react) | |
| 可调整分栏 | react-resizable-panels | [GitHub](https://github.com/bvaughn/react-resizable-panels) | [文档与示例](https://react-resizable-panels.vercel.app/) | |
| 拖拽 | dnd-kit | [dndkit.com](https://dndkit.com/) | [Docs](https://dndkit.com/) | 文档分 Latest 与 Legacy 两套，按所用包对应查阅。 |
| 服务端状态 | TanStack Query | [tanstack.com/query](https://tanstack.com/query/latest) | [React Overview](https://tanstack.com/query/latest/docs/framework/react/overview) | |
| 客户端状态 | Zustand | [GitHub](https://github.com/pmndrs/zustand) | [zustand.docs.pmnd.rs](https://zustand.docs.pmnd.rs/) | |
| Web 应用框架 | Next.js | [nextjs.org](https://nextjs.org/) | [Docs](https://nextjs.org/docs) | |
| 内容网站 | Astro | [astro.build](https://astro.build/) | [docs.astro.build](https://docs.astro.build/) | 定位见 [Why Astro?](https://docs.astro.build/en/concepts/why-astro/)。 |

[返回技术偏好入口](./preferences.md)
