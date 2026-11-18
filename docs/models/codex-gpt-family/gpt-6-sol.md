# GPT-6 Sol

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-6-sol` / GPT-6 Sol |
| surface | Codex CLI / ChatGPT coding agent；目录标记支持 API |
| verified_at | 2026-11-18 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方入口状态：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页、本机 `codex-cli 0.169.0` 模型目录；尚无本型号 fixture 结果 |
| 推理档位 | 目录默认 `medium`；支持 `low`、`medium`、`high`、`xhigh`、`max`、`ultra` |
| 上下文窗口 | 目录 `context_window` 272,000，`max_context_window` 872,000 |

## 特性与边界

本机目录描述为上一代主力型号，官方推荐型号列表已不包含它。官方页面把它列为 `gpt-5.4` 退役后的替代；本机目录中 GPT-5.6 Sol 的升级目标也是 `gpt-6-sol`。ChatGPT desktop app 的 Power 预设包含 GPT-6 Sol Light 和 Medium。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型入口、alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时，与 GPT-6.2 Sol 使用同一 fixture 重测。
