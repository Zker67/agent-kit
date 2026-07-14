# Grok 全局规则

适用范围：所有在本机用 Grok CLI 打开的项目。更深层的项目 `AGENTS.md` 可覆盖本文件。

## Communication

- Think in English; reply in Simplified Chinese.
- Before implementing, state your assumptions. If multiple interpretations exist, list them — don't pick silently. If unclear, stop and ask.

## Surgical Changes

- Every changed line must trace to the user's request. Don't "improve" adjacent code, comments, or formatting.
- Match existing code style even if you'd write it differently.
- Remove imports/symbols your changes orphaned; flag — don't delete — pre-existing dead code.

## Goal-Driven Execution

- Convert vague tasks into verifiable goals — define an observable success condition (failing test for bugs, expected output for scripts, visible UI state for frontend, file/log shape for config).
- For multi-step tasks, state a short numbered plan with a verify step per item.
- 前端/UI 视觉效果（HTML/CSS/页面外观/布局/动画/配色）一律不要自己用 headless 浏览器截图自验，改完直接告知用户「改了什么 + 怎么验证」，由用户在真实浏览器里验证。非视觉的可验证项（脚本输出、JSON 结构、CLI 退出码、文件是否生成、lint/typecheck）仍须自验后再报告。

## Project Conventions

- New modules/directories must include a Chinese README.md; existing modules' READMEs must be updated when public surface (API、CLI、配置项、目录结构) changes. Pure 内部小修不必动 README。
- Use official CLIs for init and deps: npm, uv, cargo, go, vite, etc. After sub-project init, delete any nested `.git`.
- Commit on completing a module or logical checkpoint; working tree must be clean before the next phase.

## Code Quality

- Strong typing (TS interfaces, Python type hints). Run the project's linter/formatter before committing.
- Secrets via env vars and `.env`; never hardcode.
- For each new feature write integration tests against a real environment (happy path + edges + errors). Prefer real services; mock 仅允许用于外部付费 SaaS / 不可控第三方，且必须配 contract test 或录制回放。Don't substitute unit tests for integration coverage.

## Shell

- Windows 上优先 `&&` 串联（前者失败则停）。仅当确实需要「前者失败也继续」时才用 `;`，且必须显式说明原因。

## Subagents

- 子代理默认模型由 `~/.grok/config.toml` 的 `[subagents.models]` 固定为 **Composer 2.5**（`grok-composer-2.5-fast`），无需在 spawn 参数里再传模型名。
- 默认类型用 `explore`（只读探索）或 `general-purpose`（可改代码）；规划用 `plan`。
- 不要使用 haiku / sonnet / opus 等其他产品的模型名。

## Tool Routing

- **联网搜索**：直接用 Grok 内置 `web_search` / `web_fetch` / `open_page` 等，不必额外说明，也不必绕去 smart-search CLI。
- **本地代码搜索**：优先 `fast-context` MCP（先 `search_tool` 取 schema，再 `use_tool` 调用）。理解上下文、探索性查找、自然语言定位、找引用与实现，优先走它。`grep` / 精确路径 `read_file` 仅用于已知确切字符串或已知路径。
- **库 / SDK 文档**：优先 `context7` MCP；失败再用内置联网工具。
- **生图 / 图编辑**：走 Skill `image-gen-pro`（内部用 `imagen` CLI），不要绕开。

## Skills

- 只使用 Grok 用户目录与 bundled skills（`~/.grok/skills` 等）。不要依赖 Claude / Cursor 兼容层 skill。
