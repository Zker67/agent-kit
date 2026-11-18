# GPT-6 Astra

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-6-astra` / GPT-6 Astra（官方页面简称 Astra） |
| surface | Codex CLI / Codex IDE extension / ChatGPT desktop app / ChatGPT web；支持 API |
| verified_at | 2026-11-18 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方定位：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页、本机 `codex-cli 0.169.0` 模型目录；尚无本型号 fixture 结果 |
| 推理档位 | 目录默认 `low`；支持 `low`、`medium`、`high`、`xhigh`、`max`、`ultra`。官方建议从 Light 开始，配置中 Light 对应 `low` |
| 上下文窗口 | 目录 `context_window` 272,000，`max_context_window` 872,000 |

## 特性与边界

官方定位是能力最强的型号，适合跨代码、应用和研究的复杂端到端工作。官方说明它更擅长提出聚焦的问题，并在吸收用户指导的同时保持原始目标和约束。

API 文档已有 GPT-6.2 Astra 的 prompting 指南，但本机 Codex 模型目录还没有 GPT-6.2 型号。[`environments/codex/AGENTS.md`](../../../environments/codex/AGENTS.md) 中参考该指南补充的输出 guard，尚未在本型号上评测。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

Codex 目录出现 GPT-6.2 Astra，或模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性、上下文策略变化时，与 GPT-6.2 Sol 使用同一 fixture 重测。
