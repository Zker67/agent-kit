# System Prompts

本目录保存不同 coding agent 宿主的用户级或全局提示词。它们共享“聚焦改动、先理解后修改、完成验证、安全处理 Git”的基本原则，但会根据各宿主的规则入口、工具和多代理能力保留差异。

## 如何选择

| 文件 | 适用宿主 | 实用特点 | 建议入口 |
|---|---|---|---|
| [`CHATGPT.md`](./CHATGPT.md) | Codex / ChatGPT coding agent | 中文规则完整，强调根因修复、结构性不变量、运行时验证和安全边界，适合作为通用基线。 | `~/.codex/AGENTS.md` |
| [`CLAUDE.md`](./CLAUDE.md) | Claude Code | 规则更紧凑，强调 surgical changes、可观察成功条件，以及 Claude Code 的 subagent 模型选择。 | `~/.claude/CLAUDE.md` |
| [`GEMINI.md`](./GEMINI.md) | Gemini / Antigravity 风格工具 | 强调用户级、项目级、workflow 与 skill 的分层，并偏向使用澄清工具和实际状态核验。 | `~/.gemini/GEMINI.md` |
| [`GROK.md`](./GROK.md) | Grok CLI | 强调集成测试、Windows shell 习惯、Grok 内置联网工具、Composer 子代理和 Grok skill 目录。 | `~/.grok/AGENTS.md` |
| [`WINDSURF.md`](./WINDSURF.md) | Windsurf | 仅提供轻量语言约束，适合与 Windsurf 自身规则或项目规则叠加。 | `~/.codeium/windsurf/memories/global_rules.md` |

这些描述用于说明提示词的侧重点，不是模型能力排名或性能基准。同一个模型在不同宿主中可用的工具、上下文、规则加载和多代理机制可能不同，实际选择应以宿主支持能力为准。

## ChatGPT / Codex

[`CHATGPT.md`](./CHATGPT.md) 是 `~/.codex/AGENTS.md` 的公开通用版本。它保留长期稳定的协作规则，不包含个人 provider、私有地址、凭据、项目专属部署流程或只适用于单台机器的配置。

### 参考来源

| 官方资料 | 本提示词采用的实践 |
|---|---|
| [Prompting Codex](https://learn.chatgpt.com/docs/prompting#prompting-codex) | 任务应说明目标行为、相关代码或复现步骤、重要约束和验证方式；复杂任务需要先对齐方案时使用 `/plan`，长任务可在计划后使用 `/goal`。 |
| [Using the latest model](https://developers.openai.com/api/docs/guides/latest-model) | 以官方动态页面确认当前模型族、推理档位和迁移建议，不把某个模型版本永久写成“最新”。 |
| [Prompting guidance for GPT-5.6 Sol](https://developers.openai.com/api/docs/guides/prompt-guidance-gpt-5p6) | 提示词保持精简、目标优先，规则只表达一次；明确成功标准、授权边界、停止条件、工具路由和验证要求。 |
| [Codex Subagents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agent-file-schema) | 子代理通过独立 TOML 文件设置角色、模型和推理强度，避免把不同角色的运行参数堆进全局提示词。 |

### 设计思路

- **结果优先**：告诉 Codex 最终要达到什么状态，而不是预先规定所有执行步骤；路径、复现、约束和验收标准比泛泛的“认真检查”更有效。
- **授权分层**：回答、解释、审查、诊断和计划默认只读；修改、构建和修复允许直接完成范围内的本地改动与非破坏性验证；外部写入、破坏性操作、付费行为和扩大范围需要确认。
- **按需规划**：普通任务直接执行，不强制先输出计划；跨模块、高风险或多阶段任务使用 `/plan`，避免计划流程拖慢简单修改。
- **稀疏汇报**：多步骤任务开始前说明第一步，之后只在阶段切换、关键发现或方案变化时更新，不逐条播报例行工具调用。
- **验证闭环**：修改后优先运行最相关的测试、类型检查、lint、构建或 smoke test；无法验证时明确缺口和下一项最佳检查。
- **提示词与配置分离**：`CHATGPT.md` 管长期行为，`~/.codex/config.toml` 管模型、推理强度、权限和工具，`~/.codex/agents/*.toml` 管子代理角色。

### 推荐配置

当前实践使用旗舰模型处理主任务，复杂规划提高推理强度，子代理以中等推理强度承担边界明确的并行工作：

```toml
# ~/.codex/config.toml
model = "gpt-5.6-sol"
model_reasoning_effort = "high"
plan_mode_reasoning_effort = "xhigh"
```

```toml
# ~/.codex/agents/<role>.toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
```

这组档位是质量优先的本地默认值，不是所有项目的通用性能结论。延迟或成本敏感时，应在代表性任务上比较相邻推理档位，再决定是否下调。

### 使用思路

给 Codex 的任务尽量包含以下信息，不需要替它编写完整执行脚本：

```text
目标：要修复、实现或确认什么。
上下文：相关路径、文件、截图、报错或复现步骤。
约束：不能改变的 API、行为、安全边界或阶段限制。
验证：完成后要运行什么，或者什么现象代表成功。
```

简单任务直接描述目标即可；复杂任务先用 `/plan` 对齐方案，再进入实施。需要临时改变模型或推理强度时，使用 `/model` 或 `/reasoning`，不要为了单次任务反复改全局提示词。

## 使用方式

1. 选择与你使用的宿主对应的文件。
2. 备份宿主当前的用户级或全局规则。
3. 复制到宿主实际识别的入口，并按本机工具名、skill 路径和 subagent 能力调整专属段落。
4. 项目专有的技术栈、测试命令和部署约束继续放在项目自己的 `AGENTS.md`、`CLAUDE.md`、`GEMINI.md` 或规则目录中。

不要把 token、密码、真实 API 配置或仅适用于单个私有项目的规则提交到本目录。
