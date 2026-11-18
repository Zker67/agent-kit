# GPT-6.1 Terra

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-6.1-terra` / GPT-6.1 Terra |
| surface | Codex CLI（需 0.159.0 或更高版本）/ ChatGPT desktop app 中的 Work 与 Codex / ChatGPT Work web；支持 API。官方可用入口未列出 Codex IDE extension |
| verified_at | 2026-11-18 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方定位：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页、本机 `codex-cli 0.169.0` 模型目录；尚无本型号 fixture 结果 |
| 推理档位 | 目录默认 `low`；支持 `low`、`medium`、`high`、`xhigh`、`max`、`ultra` |
| 上下文窗口 | 目录 `context_window` 500,000，`max_context_window` 872,000 |

## 特性与边界

官方定位是快速、高效的型号，擅长清晰写作、视觉理解和 computer use，例如起草提案、解读图表和截图、在应用中处理信息。该定位不等于对编码、文档或前端输出卫生的行为结论。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时，与 GPT-6.2 Sol 使用同一 fixture 重测。
