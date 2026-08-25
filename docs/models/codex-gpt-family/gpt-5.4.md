# GPT-5.4

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-5.4` / GPT-5.4 |
| surface | Codex CLI / ChatGPT coding agent；API 另行核对 |
| verified_at | 2026-08-25 |
| status | `supported`; ChatGPT 登录入口将于 2026-08-31 退役 |
| confidence | 官方入口状态：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页；尚无本型号 fixture 结果 |

## 特性与边界

官方定位是面向专业工作、编码、推理和工具使用的前代型号。2026-08-31 的 Codex ChatGPT 登录入口退役不等同于 API 退役；两者必须分开核对。

## 配置对策

- 在入口仍可用时先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型入口、alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时重测；入口退役后不以历史结果冒充当前运行态。
