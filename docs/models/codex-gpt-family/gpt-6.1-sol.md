# GPT-6.1 Sol

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-6.1-sol` / GPT-6.1 Sol |
| surface | Codex CLI / Codex IDE extension / ChatGPT desktop app 中的 Work 与 Codex / ChatGPT Work web；支持 API |
| verified_at | 2026-11-18 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方定位：高；上下文窗口：中（来源冲突）；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页、本机 `codex-cli 0.169.0` 模型目录；尚无本型号 fixture 结果 |
| 推理档位 | 目录默认 `low`；支持 `low`、`medium`、`high`、`xhigh`、`max`、`ultra`。官方建议从所用应用的默认档位开始 |
| 上下文窗口 | 官方页面：Codex 与 ChatGPT Work 默认 500,000；本机目录 `context_window` 272,000，`max_context_window` 872,000。以运行态回读为准 |

## 特性与边界

官方定位是性能接近 Astra、成本低于 Astra 的型号，适合重复、长时间运行的代码、应用和文档工作。官方 `config.toml` 示例使用 `model = "gpt-6.1-sol"`；GPT-5.5 从 ChatGPT 登录入口退役后，Plus、Pro、Business、Enterprise 和 Edu 方案的官方替代是本型号。

本仓 Codex 示例配置使用 [GPT-6.2 Sol](./gpt-6.2-sol.md)。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

与 GPT-6.2 Sol 使用同一 fixture 对照；模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时重测；上下文窗口的官方说法与目录不一致，运行态回读后更新本档案。
