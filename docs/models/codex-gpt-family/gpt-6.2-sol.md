# GPT-6.2 Sol

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-6.2-sol` / GPT-6.2 Sol |
| surface | OpenAI API（Responses、Chat Completions 等）；Codex 可用性待新版 Codex CLI 模型目录回读 |
| verified_at | 2026-11-18 |
| status | `supported`（API）；本项目当前主要基准，项目行为待评测 |
| confidence | API 规格：高；Codex 入口：待验证；本项目缺陷归因：待验证 |
| evidence | 官方 API 模型页；本机 `codex-cli 0.169.0` 模型目录（2026-11-16 缓存）尚未列出；尚无本型号 fixture 结果 |
| 推理档位 | API 拒绝 `none`；Codex 中支持的档位待模型目录回读 |
| 上下文窗口 | API：1,050,000 context window，最大输入 922,000，最大输出 128,000；输入超过 272K 时整次请求按长上下文费率计费 |
| 知识截止 | 2026-06-01 |

## 特性与边界

官方 API 定位是支持文本、图像输入和工具调用的推理型号，可在 Responses API 中使用 web search、computer use、apply patch、hosted shell 等工具，或通过 Multi-agent beta 委派子代理。[Using GPT-6.2](https://developers.openai.com/api/docs/guides/latest-model) 的 prompting 指南适用于 GPT-6.2 Astra 和 Sol，[`environments/codex/AGENTS.md`](../../../environments/codex/AGENTS.md) 的输出 guard 参考了该指南。

本仓 Codex 与 Pi 示例配置使用本型号。

## 配置对策

- 继承 Codex 全局 guard；当前没有证据支持额外的型号专用规则。
- 可选 benchmark overlay 见 [`gpt-6.2-sol-output-hygiene.example.toml`](../../../environments/codex/profiles/gpt-6.2-sol-output-hygiene.example.toml)。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

更新 Codex CLI 后先用 `codex debug models` 回读本型号的 slug、默认推理档位和上下文窗口，再更新本档案。模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时重测。
