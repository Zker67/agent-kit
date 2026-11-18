# GPT-6 Luna

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-6-luna` / GPT-6 Luna（官方页面简称 Luna） |
| surface | Codex CLI / Codex IDE extension / ChatGPT desktop app 中的 Work 与 Codex / ChatGPT Work web；支持 API。Enterprise 与 Edu 需管理员先启用 |
| verified_at | 2026-11-18 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方定位：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页、本机 `codex-cli 0.169.0` 模型目录；尚无本型号 fixture 结果 |
| 推理档位 | 目录默认 `medium`；支持 `low`、`medium`、`high`、`xhigh`、`max`，不支持 `ultra`。官方建议从 High 开始 |
| 上下文窗口 | 目录 `context_window` 272,000，`max_context_window` 872,000 |

## 特性与边界

官方定位是最高效的型号，适合聚焦、大批量、结果标准清楚的任务，例如摘要、抽取、分类、格式转换和聚焦编码。官方页面把它列为 `gpt-5.4-mini` 退役后的替代，以及 GPT-5.5 退役后 Free 与 Go 方案在 desktop app 中的替代。速度和成本定位不能替代对具体文档、前端和最终化任务的行为评测。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时，与 GPT-6.2 Sol 使用同一 fixture 重测。
