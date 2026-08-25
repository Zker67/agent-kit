# GPT-5.6 Sol

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-5.6-sol` / GPT-5.6 Sol |
| surface | Codex CLI / ChatGPT coding agent |
| verified_at | 2026-08-25 |
| status | `supported`; 项目行为仍待运行态评测 |
| confidence | 官方定位：高；本项目缺陷归因：中 |
| evidence | 官方 Codex 模型页、本机 `codex-cli 0.149.1`；尚无本型号 fixture 结果 |

## 特性与边界

官方定位是复杂编码、研究和高细节任务的旗舰型号。本项目把它作为当前主要基准，但不把 GPT 系列共性风险自动证明为 Sol 独有缺陷。

用户工作流中重点观察两类风险：control-plane 到交付物的泄漏，以及已撤销状态的会话残留。它们需要在同一组 Markdown、前端和最终化 fixture 上重复确认，当前仍是 `observed / needs-verification`。

## 配置对策

- 继承 Codex 全局 guard；当前没有证据支持额外的 Sol 专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时重测。
