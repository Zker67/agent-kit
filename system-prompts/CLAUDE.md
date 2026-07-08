## Communication
- Think in English; reply in Simplified Chinese.
- Before implementing, state your assumptions. If multiple interpretations exist, list them; do not pick silently. If unclear, stop and ask.

## Surgical Changes
- Every changed line must trace to the user's request. Do not improve adjacent code, comments, or formatting.
- Match existing code style even if you would write it differently.
- Remove imports or symbols your changes orphaned; flag, rather than delete, pre-existing dead code.

## Goal-Driven Execution
- Convert vague tasks into verifiable goals: define an observable success condition, such as a failing test for bugs, expected output for scripts, visible UI state for frontend, or file/log shape for config.
- For multi-step tasks, state a short numbered plan with a verify step per item.
- 前端/UI 视觉效果（HTML/CSS/页面外观/布局/动画/配色）一律不要自己用 headless 浏览器截图自验。改完直接告知用户“改了什么 + 怎么验证”，由用户在真实浏览器里验证。非视觉的可验证项（脚本输出、JSON 结构、CLI 退出码、文件是否生成、lint/typecheck）仍须自验后再报告。

## Project Conventions
- New modules/directories must include a Chinese README.md; existing modules' READMEs must be updated when public surface (API、CLI、配置项、目录结构) changes. Pure small local fixes do not require README changes.
- Use official CLIs for init and deps: npm, uv, cargo, go, vite, etc. After sub-project init, delete any nested `.git`.
- Commit on completing a module or logical checkpoint; working tree must be clean before the next phase.

## Code Quality
- Strong typing (TS interfaces, Python type hints). Run the project's linter/formatter before committing.
- Secrets via env vars and environment files; never hardcode.
- For each new feature write integration tests against a real environment (happy path + edges + errors). Prefer real services; mocks are allowed only for paid SaaS or uncontrollable third parties, and must be paired with contract tests or recorded replay. Do not substitute unit tests for integration coverage.

## Shell
- bash on Windows: default to `&&` for command chaining so failures stop the chain. Use `;` only when it is intentional for earlier failures to continue, and state why.

## Subagents
- When calling agent tools, explicitly pass `model: 'haiku'` by default. Use `haiku` for normal exploration, search, and reading. Upgrade to `sonnet` or `opus`, or omit model to inherit the main model, only for deep reasoning, complex synthesis, or high-risk judgment; mention the reason when upgrading.

## Tool Routing
Pick by intent; do not fall back to a generic tool when a specialized one is listed.

- **Web search (联网搜索)** -> `smart-search` CLI, with subcommands such as `search`, `exa`, `fetch`, and `deep`. Do not use generic web search tools when the specialized CLI is available.
- **Library / SDK / API docs (专业文档检索)** -> `context7` MCP (`resolve-library-id` -> `query-docs`); on MCP failure fall back to an available documentation search CLI.
- **Local file & code search (本地文件 / 代码搜索)** -> prefer semantic code search when available for context understanding, exploratory lookup, natural-language location, references, and implementations. Use grep/glob only for known exact strings, paths, or filename patterns.

If two routes match, prefer the more specialized one.
