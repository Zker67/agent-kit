# GPT-5.5

| 项 | 记录 |
|---|---|
| model id / alias | `gpt-5.5` / GPT-5.5 |
| surface | Codex CLI / ChatGPT coding agent |
| verified_at | 2026-08-25 |
| status | `supported`; 项目行为待评测 |
| confidence | 官方定位：高；本项目缺陷归因：待验证 |
| evidence | 官方 Codex 模型页；尚无本型号 fixture 结果 |

## 特性与边界

官方定位是 GPT-5.6 之前的上一代前沿型号，适合作为迁移前后对照。项目只记录具体 fixture 的差异，不从型号名称推断输出卫生或前端能力。

## 配置对策

- 先继承 Codex 全局 guard；没有重复证据时不增加型号专用规则。
- 最终化阶段可显式使用外部 `no-negative-echo`；当前已部署到 Codex，宿主发现和激活待新会话回读。

## 重新核对条件

模型 alias/snapshot、Codex 版本、reasoning effort、工具可用性或上下文策略变化时，与 GPT-5.6 基准使用同一 fixture 重测。
