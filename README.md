# agent-kit

> 面向编码代理的开源资产包：自研 skills、宿主级 system prompts，以及可复用的基础项目模板。

计划发布位置：`Zker67/agent-kit`。

## 适合谁

- 想把常用 coding agent 工作流沉淀成可安装 skills 的用户。
- 想统一 Codex、Claude、Gemini、Windsurf 等工具协作规则的用户。
- 想给新项目快速放入 `AGENTS.md`、`.agent/rules/`、`docs/`、`references/`、`plans/` 和可选 `.ai_memory/` 结构的用户。

## 内容

| 路径 | 说明 |
|---|---|
| `skills/` | 14 个自研 skill，覆盖 README 生成、计划管理、检索、经验沉淀、解释、结构治理、测试、中文输出等工作流 |
| `system-prompts/` | 面向 Codex、Claude、Gemini、Windsurf 等宿主的全局提示词 |
| `templates/base-project/` | 可复制到新项目的通用项目骨架，默认 AI 入口为 `AGENTS.md` |
| `scripts/` | 本地安装 skill 与创建新项目模板的辅助脚本 |
| `docs/` | 发布检查、兼容性说明和迁移说明 |

## 安装 skills

### Git Bash / macOS / Linux

默认安装到 `$CODEX_HOME/skills`，未设置 `CODEX_HOME` 时安装到 `~/.codex/skills`：

```bash
./scripts/install-skills.sh
```

安装到自定义目录：

```bash
./scripts/install-skills.sh /path/to/skills
```

### PowerShell

默认安装到 `$env:CODEX_HOME\skills`，未设置 `CODEX_HOME` 时安装到 `$HOME\.codex\skills`：

```powershell
./scripts/install-skills.ps1
```

安装到自定义目录：

```powershell
./scripts/install-skills.ps1 -Target "D:\path\to\skills"
```

### 验证安装

```bash
ls ~/.codex/skills/pro-test
ls ~/.codex/skills/use-chinese
```

PowerShell：

```powershell
Get-ChildItem "$HOME\.codex\skills" -Directory
```

## 使用 system prompts

`system-prompts/` 是宿主级全局提示词，不是项目模板。建议只安装你实际使用的宿主文件，并先备份现有配置。

| 文件 | 用途 | 常见放置位置 |
|---|---|---|
| `system-prompts/AGENTS.md` | Codex / 通用 coding agent | `~/.codex/AGENTS.md` 或项目根 `AGENTS.md` |
| `system-prompts/CLAUDE.md` | Claude Code | `~/.claude/CLAUDE.md` 或项目根 `CLAUDE.md` |
| `system-prompts/GEMINI.md` | Gemini CLI / Antigravity 风格工具 | `~/.gemini/GEMINI.md` 或项目根 `GEMINI.md` |
| `system-prompts/WINDSURF.md` | Windsurf | Windsurf custom instructions 或项目规则入口 |

PowerShell 示例：

```powershell
# Codex
New-Item -ItemType Directory -Force "$HOME\.codex" | Out-Null
Copy-Item "$HOME\.codex\AGENTS.md" "$HOME\.codex\AGENTS.md.bak" -ErrorAction SilentlyContinue
Copy-Item ".\system-prompts\AGENTS.md" "$HOME\.codex\AGENTS.md"

# Claude Code
New-Item -ItemType Directory -Force "$HOME\.claude" | Out-Null
Copy-Item "$HOME\.claude\CLAUDE.md" "$HOME\.claude\CLAUDE.md.bak" -ErrorAction SilentlyContinue
Copy-Item ".\system-prompts\CLAUDE.md" "$HOME\.claude\CLAUDE.md"

# Gemini
New-Item -ItemType Directory -Force "$HOME\.gemini" | Out-Null
Copy-Item "$HOME\.gemini\GEMINI.md" "$HOME\.gemini\GEMINI.md.bak" -ErrorAction SilentlyContinue
Copy-Item ".\system-prompts\GEMINI.md" "$HOME\.gemini\GEMINI.md"
```

Git Bash 示例：

```bash
mkdir -p ~/.codex ~/.claude ~/.gemini
cp ~/.codex/AGENTS.md ~/.codex/AGENTS.md.bak 2>/dev/null || true
cp ~/.claude/CLAUDE.md ~/.claude/CLAUDE.md.bak 2>/dev/null || true
cp ~/.gemini/GEMINI.md ~/.gemini/GEMINI.md.bak 2>/dev/null || true

cp system-prompts/AGENTS.md ~/.codex/AGENTS.md
cp system-prompts/CLAUDE.md ~/.claude/CLAUDE.md
cp system-prompts/GEMINI.md ~/.gemini/GEMINI.md
```

### 关于外部工具路由

这些 system prompts 会提到一些可选工具，例如专业搜索 CLI、Context7、语义代码搜索、MCP 或 subagents。它们是“如果你的宿主环境提供，就优先使用”的路由规则，不是本仓库的硬依赖。

本仓库的 system prompts 已移除图片生成、图像编辑、视频生成和视频编辑的专用路由。如果你需要这些能力，可以在自己的本地提示词中额外补充，但不建议把个人供应商、API key、私有路径写进公开仓库。

计划写作、拆分和 `plans/README.md` 维护不放进宿主级 system prompts；需要时使用 `pro-plans` 或项目模板内的项目级约定。

## 创建新项目模板

```powershell
./scripts/new-project.ps1 -Name my-agent-project -TargetRoot ../
```

也可以直接复制 `templates/base-project/`，再按项目实际情况填写 `README.md`、面向 AI 的 `AGENTS.md`、`docs/README.md`、`references/README.md` 和 `plans/README.md`。

模板内 `.agent/rules/` 是项目级规则，`system-prompts/` 是宿主级全局提示词，两者边界不同：前者随项目走，后者安装到具体 AI 工具或用户配置中。

模板内 `docs/` 承载当前代码和程序的长期文档，`references/` 承载外部文档和外部仓库参考。重要外部来源可以按自身结构建子目录，记录版本、commit、许可和借鉴点；采纳后的当前项目事实应回写到 `docs/` 或源码。

`.ai_memory/` 在模板中只保留说明和空占位，不包含任何真实记忆内容。`MEMO.example.md` 仅作为本地个人笔记示例，复制为实际笔记文件后应按项目策略决定是否纳入版本控制。

## Skill 清单

| Skill | 用途 |
|---|---|
| `pro-copy` | 搜索同类项目、借鉴成熟开源实现 |
| `pro-exp` | 将解法沉淀为 `.exp/` 经验文档 |
| `pro-explain` | 面向初学者解释代码或补充必要注释 |
| `pro-idea` | 生成可分阶段落地的改进建议 |
| `pro-memory` | 按需维护 `.ai_memory/` 项目级长期上下文 |
| `pro-must` | 严格按用户指定方案执行 |
| `pro-plans` | 在项目根 `plans/` 下创建、拆分和维护计划文档 |
| `pro-readme` | 生成或重写面向人类读者的 README |
| `pro-rule` | 将稳定偏好整理为 `.agent/rules/` |
| `pro-struct` | 目录结构整理、组件化和复用性治理 |
| `pro-summary` | README、面向 AI 的 AGENTS.md、docs 与 plans 的一致性审查 |
| `pro-test` | 测试、调试和验证流程 |
| `use-chinese` | 默认使用简体中文输出 |
| `use-internet` | 联网检索与资料核验路由 |

## 文档

- [发布检查清单](docs/publishing-checklist.md)
- [兼容性说明](docs/compatibility.md)
- [迁移说明](docs/migration-from-00000-model.md)

## License

MIT
