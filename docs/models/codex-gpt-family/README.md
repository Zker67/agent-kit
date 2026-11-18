# Codex / GPT 系列模型档案

核对日期：GPT-6 系列与 GPT-5.5、GPT-5.4 的入口状态为 2026-11-18；GPT-5.6 系列定位为 2026-08-25。

## 记录边界

| 项 | 当前记录 |
|---|---|
| Codex surface | Codex CLI / ChatGPT coding agent |
| 本机 CLI 证据 | `codex-cli 0.169.0` 模型目录（2026-11-18）；GPT-5.6 系列早期记录为 `codex-cli 0.149.1` |
| 运行态评测 | 尚未完成；模型档案不把文件存在当作已加载 |
| 统一 guard | [`environments/codex/AGENTS.md`](../../../environments/codex/AGENTS.md) 中的写入边界、注释最小化、最终回复自成一体、收尾自查、代码可读性、测试新增条件和前端界面取舍规则 |
| 外部 skill | 见 [`environments/codex/skills/README.md`](../../../environments/codex/skills/README.md)；模型档案不重复维护安装状态 |

## 官方目录

| 型号 | 官方定位摘要 | 当前记录边界 |
|---|---|---|
| GPT-6.2 Sol | 支持文本、图像输入和工具调用的推理型号（API 定位）。 | 当前主要基准；Codex 入口待新版 CLI 模型目录回读，不把观察自动推广到其他型号。 |
| GPT-6 Astra | 能力最强，适合跨代码、应用和研究的复杂端到端工作。 | 官方推荐型号；需要独立评测。 |
| GPT-6.1 Sol | 接近 Astra 的性能、成本更低，适合重复、长时间运行的代码、应用和文档工作。 | 官方推荐型号与 `config.toml` 示例默认；上下文窗口官方与目录说法不一致，待运行态回读。 |
| GPT-6.1 Terra | 快速高效，擅长清晰写作、视觉理解和 computer use。 | 官方推荐型号；需 Codex CLI 0.159.0 或更高版本。 |
| GPT-6 Luna | 最高效，适合聚焦、大批量、结果标准清楚的任务。 | 官方推荐型号；推理最高到 `max`，不支持 `ultra`。 |
| GPT-6 Sol | 本机目录描述为上一代主力型号。 | 不在官方推荐列表；是 `gpt-5.4` 退役后的官方替代。 |
| GPT-5.6 Sol | 复杂编码、研究和高细节任务的旗舰型号。 | 2026-11-18 前的主要基准；本机目录已标为更老一代，升级目标为 `gpt-6-sol`。 |
| GPT-5.6 Terra | 日常工作与编码的均衡型号，面向较高吞吐和成本平衡。 | 需要独立评测，不用 Sol 的结果代替。 |
| GPT-5.6 Luna | 更快、更经济，适合可重复任务。 | 需要独立评测，不用 Terra 或 Sol 的结果代替。 |
| GPT-5.5 | GPT-5.6 系列之前的高能力型号。 | 2026-10-14 从 Codex 的 ChatGPT 登录入口退役；API 与 API key 登录的 Codex 不受影响。只记录实测差异，不回填推断。 |
| GPT-5.4 | 面向专业工作、编码、推理和工具使用的前代型号。 | 2026-08-31 已从 Codex 的 ChatGPT 登录入口退役；API 与 API key 登录的 Codex 不受影响。 |

官方定位来自 [Codex 模型文档](https://developers.openai.com/codex/models)；GPT-6.2 Sol 来自 [API 模型页](https://developers.openai.com/api/docs/models/gpt-6.2-sol)。

## 本项目的观察边界

- `control-plane-to-deliverable leakage` 和 `rejected-state/session residue` 先作为 GPT/Codex 系列的统一评测假设。
- “文档或前端备注膨胀”只记录为具体 fixture 上的观察，不写成无条件模型排名。
- 默认使用统一 guard；只有同一型号在重复 fixture 中出现稳定差异，才增加型号专用 profile。
- 官方事实、Codex 运行态、用户观察和配置对策分开记录。

统一对策目前只记录为配置建议：写入阶段使用全局 guard；标题、文件名、commit、PR 和 handoff 的最终化阶段可显式调用外部 skill。未完成新会话回读和跨模型 fixture 前，不把它们标记为 `active` 或 `validated`。

## 相关档案

- [`gpt-6.2-sol.md`](./gpt-6.2-sol.md)
- [`gpt-6-astra.md`](./gpt-6-astra.md)
- [`gpt-6.1-sol.md`](./gpt-6.1-sol.md)
- [`gpt-6.1-terra.md`](./gpt-6.1-terra.md)
- [`gpt-6-luna.md`](./gpt-6-luna.md)
- [`gpt-6-sol.md`](./gpt-6-sol.md)
- [`gpt-5.6-sol.md`](./gpt-5.6-sol.md)
- [`gpt-5.6-terra.md`](./gpt-5.6-terra.md)
- [`gpt-5.6-luna.md`](./gpt-5.6-luna.md)
- [`gpt-5.5.md`](./gpt-5.5.md)
- [`gpt-5.4.md`](./gpt-5.4.md)
