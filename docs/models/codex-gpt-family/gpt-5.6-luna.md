# GPT-5.6 Luna

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-5.6-luna` / GPT-5.6 Luna |
| surface | Codex CLI / ChatGPT coding agent |
| verified_at | 2026-08-25 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方定位：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页；尚无本型号 fixture 结果 |

## 特性与边界

官方定位是更快、更经济、适合清晰可重复任务的型号。速度和成本定位不能替代对具体文档、前端和最终化任务的行为评测。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时，与 Sol 使用同一 fixture 重测。
