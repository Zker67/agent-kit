# Pi Coding Agent 环境配置

本目录提供 Pi Coding Agent 的公开配置基线。Pi 核心保持轻量，长期协作规则放在 `AGENTS.md`，模型和推理档位放在 JSON 配置中，代码检索、联网检索、子代理和上下文治理通过 skills、CLI 或 Pi packages 组合。

## 目录内容

| 文件 | 用途 | 安装位置 |
|---|---|---|
| [`AGENTS.md`](./AGENTS.md) | 用户级全局 instructions | `~/.pi/agent/AGENTS.md` |
| [`settings.example.json`](./settings.example.json) | 主模型、推理档位、packages 和子代理默认值示例 | 参考后合并到 `~/.pi/agent/settings.json` |
| [`models.example.json`](./models.example.json) | OpenAI Responses 兼容 provider、图片输入和 reasoning 模型示例 | 参考后合并到 `~/.pi/agent/models.json` |

## 配置分层

| 层级 | 单一事实来源 |
|---|---|
| 跨项目协作规则 | `~/.pi/agent/AGENTS.md` |
| 默认模型、推理档位、资源和 packages | `~/.pi/agent/settings.json` |
| 自定义 provider 和模型能力 | `~/.pi/agent/models.json` |
| 凭据 | 环境变量、`/login` 或本机密钥管理器 |
| 用户级 skills | `~/.pi/agent/skills/` 或 `~/.agents/skills/` |
| 项目级规则 | 项目根 `AGENTS.md` 或 `CLAUDE.md` |
| 项目级 Pi 配置 | `.pi/settings.json` 与 `.pi/` 资源目录 |

不要把模型参数、provider 参数和工具连接信息写进 `AGENTS.md`。不要把 token、真实 server URL、个人 provider 名称或本机绝对路径提交到公开仓库。

## 安装 Pi

```bash
npm install -g --ignore-scripts @earendil-works/pi-coding-agent
pi --version
```

只需要全局安装 Pi CLI，不需要全局安装 `ai-sdk`。Pi packages 应通过 `pi install` 管理，并安装到 Pi 自己的用户目录；package 的运行依赖由 package 自己声明和安装。

## 安装全局 instructions

先备份已有文件，再复制公开基线。

Git Bash / macOS / Linux：

```bash
mkdir -p "$HOME/.pi/agent"
cp environments/pi/AGENTS.md "$HOME/.pi/agent/AGENTS.md"
```

PowerShell：

```powershell
New-Item -ItemType Directory -Force "$HOME\.pi\agent" | Out-Null
Copy-Item .\environments\pi\AGENTS.md "$HOME\.pi\agent\AGENTS.md"
```

修改 instructions 后，重启 Pi 或执行 `/reload`。

## 安装 skills

将仓库中的公开 skills 安装到 Pi 的用户级 skill 目录：

```bash
./scripts/install-skills.sh "$HOME/.pi/agent/skills"
```

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.pi\agent\skills"
```

Pi 也会扫描 `~/.agents/skills/`。如果多种 coding agent 共用一套 skill 库，应由统一管理器维护真实源目录，避免在多个宿主目录中形成不可更新的独立副本。

## 推荐 package 组合

下面的组合对应一套质量优先、可控扩展的配置思路：

```bash
pi install npm:pi-subagents
pi install npm:@complexthings/pi-dynamic-context-pruning
pi install npm:pi-codex-goal
pi install npm:@ff-labs/pi-fff
pi install git:github.com/justhil/pi-fast-context
pi install npm:@juicesharp/rpiv-ask-user-question
pi install npm:pi-tool-display
pi install npm:pi-markdown-preview
pi install npm:pi-nano-context
```

| Package | 作用 |
|---|---|
| `pi-subagents` | 子代理、并行任务、链式工作流和运行状态管理。 |
| `pi-dynamic-context-pruning` | 动态上下文裁剪，降低长会话中的无效上下文占用。 |
| `pi-codex-goal` | 为长任务增加可验证目标和持续执行状态。 |
| `pi-fff` | 精确文件与内容检索，补充 `rg` 和内置只读工具。 |
| `pi-fast-context` | 语义代码搜索，用于未知位置、调用链和跨文件探索。 |
| `rpiv-ask-user-question` | 提供结构化用户提问工具，适合有限选项和关键决策。 |
| `pi-tool-display` | 提供紧凑的工具调用、结果和 diff 显示。 |
| `pi-markdown-preview` | 提供 Markdown、LaTeX 和代码预览，以及 HTML、PDF、PNG 等导出能力。 |
| `pi-nano-context` | 用分段占用条显示当前上下文使用情况。 |

Pi packages 和 extensions 能执行任意本机代码。安装前应检查来源、版本和代码；更新时使用 `pi update --extensions`，同时更新 Pi 和 packages 时使用 `pi update --all`。

示例保留 `defaultProjectTrust: "ask"`。项目 trust 只决定是否加载项目级 `.pi/settings.json`、packages 和 extensions，不是文件系统或命令执行 sandbox。

### 显示与交互优化

- `rpiv-ask-user-question` 注册 `ask_user_question` 工具。缺失信息会显著改变方案、且问题适合有限选项时使用；简单单一问题仍可直接文本询问。
- `pi-tool-display` 默认提供 OpenCode 风格的紧凑工具调用与 diff 显示，可通过 `/tool-display` 调整。
- `pi-markdown-preview` 注册 `/preview`、`/preview-browser`、`/preview-pdf`、`/preview-clear-cache` 和 `preview_export`。渲染依赖 Pandoc，终端或 PNG 预览还需要可用的 Chromium 浏览器。
- `pi-nano-context` 用分段上下文占用条替换默认计量显示，不参与上下文裁剪策略。

安装或更新 package 后执行 `/reload`，再检查对应命令、工具和 widget 是否已经注册。扩展兼容性以目标 Pi 版本中的实际运行结果为准。

## 模型与努力程度

[`settings.example.json`](./settings.example.json) 采用以下默认值：

- 主代理使用质量优先模型，默认努力程度为 `xhigh`。
- 子代理默认使用同一模型的 `medium`，控制并行任务成本和延迟。
- `subagents.defaultModel` 使用完整的 `provider/model:thinking` 字符串；模型后缀是子代理实际努力程度的明确来源。
- 如果个别角色需要不同档位，优先在 `subagents.agentOverrides.<name>.model` 中写完整后缀，例如 `custom-responses/gpt-5.6-sol:high`。
- 项目 `.pi/settings.json` 可以覆盖用户级默认值，但不应复制整份全局配置。

[`models.example.json`](./models.example.json) 展示一个通用 Responses API 配置：

- `api` 使用 `openai-responses`。
- `input` 同时声明 `text` 和 `image`。
- `reasoning` 开启。
- `thinkingLevelMap` 将 `minimal` 设为 `null`，只关闭该档位；`low` 到 `max` 仍可使用。
- `contextWindow` 和 `maxTokens` 必须按实际 provider 合约填写，不能只按模型名称猜测。
- API key 从环境变量读取，不写入 JSON。

## 工具路由

本基线使用以下顺序：

- 未知代码位置、组件关系、调用链或跨文件行为：先用 `fast_context_search` 导航，再读取命中文件确认。
- 已知文件名、精确标识符或字面字符串：使用 FFF 工具或通过 `bash` 调用 `rg`。
- 联网检索：通过 `bash` 调用 `smart-search`；默认先做轻量来源搜索，证据不足时再升级完整搜索。
- 多步骤且边界独立的工作：按需使用 `subagent`；简单任务保持单代理执行。
- Pi 默认提供 `read`、`write`、`edit` 和 `bash`；`grep`、`find`、`ls` 可通过工具选项启用。

工具名必须与本机实际安装的 extension、skill 或 CLI 一致。缺少某项能力时，应修改全局 instructions 或补齐对应 package，不要让提示词长期引用不存在的工具。

## 验证

先做文件和 package 检查：

```bash
pi --version
pi list
```

进入 Pi 后检查：

```text
/reload
/model
/subagents-models
/dcp
/goal
/fff-health
/fast-context-status
/tool-display
/preview
```

也可以用 RPC 只读检查主模型和努力程度，不触发模型调用：

```bash
printf '%s\n' '{"type":"get_state"}' | pi --mode rpc --no-session --no-approve
```

```powershell
'{"type":"get_state"}' | pi --mode rpc --no-session --no-approve
```

成功标准不是文件存在，而是新会话实际报告了目标 provider、模型和 `thinkingLevel`，`/subagents-models` 也显示预期的子代理映射。
