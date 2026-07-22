<div align="center">

# agent-kit

**面向多种 coding agent 的环境配置指南与可安装 skill 资产包**

`6 类 coding environments` · `14 个 skills` · `可复制配置资产` · `通用项目模板`

[![License](https://img.shields.io/badge/license-MIT-blue?style=flat-square)](#license)
[![Stack](https://img.shields.io/badge/stack-Markdown%20%2B%20Shell-000000?style=flat-square)](#开发栈)
[![Install](https://img.shields.io/badge/install-copy%20skills-orange?style=flat-square)](#启动)
[![Skills](https://img.shields.io/badge/skills-14-brightgreen?style=flat-square)](#skill-清单)
[![MCP](https://img.shields.io/badge/mcp-optional%20routes-yellow?style=flat-square)](#外部工具)
[![Status](https://img.shields.io/badge/status-source%20first-ff69b4?style=flat-square)](#启动)

[Skill 清单](#skill-清单) · [核心能力](#核心能力) · [启动](#启动) · [使用流程](#使用流程) · [配置](#配置) · [外部工具](#外部工具) · [协同关系](#协同关系)

</div>

> AI 接手前先读 [AGENTS.md](./AGENTS.md)。本 README 是用户视角速览；协作规则、验证清单和目录约定见 AGENTS.md。

---

<p align="center">
  <img src="./assets/hero.webp" alt="neon blueprint panels connected by light beams, representing an agent skill kit copied into different coding assistants" width="80%">
</p>

> 把“配置不同 coding agent 并安装同一套工作流”这件事——环境指南 + 全局 instructions + skills + 项目模板——收口到一个公开仓库。

---

## 核心能力

| 能力 | 实现 |
|---|---|
| **跨宿主 skill 分发** | [`skills/`](./skills/) 保存可公开分发的自研 skill；安装脚本按目录复制到目标宿主读取的位置。 |
| **任意目标目录安装** | [`scripts/install-skills.sh`](./scripts/install-skills.sh) 接收第一个路径参数；[`scripts/install-skills.ps1`](./scripts/install-skills.ps1) 接收 `-Target`。 |
| **Codex 默认路径兼容** | 省略目标参数时，脚本优先使用 `$CODEX_HOME/skills`，再回落到用户目录下的 `.codex/skills`。 |
| **Coding environment 指南** | [`environments/`](./environments/) 按 Codex、Pi、Claude Code、Gemini、Grok 和 Windsurf 分别说明全局 instructions、运行时配置、skills、工具和验证方式。 |
| **新项目模板** | [`templates/base-project/`](./templates/base-project/) 提供通用 `AGENTS.md`、`.agent/rules/`、`docs/`、`references/`、`plans/` 和 `.ai_memory/` 占位结构。 |
| **外部工具前置说明** | [`environments/`](./environments/) 和部分 skill 会优先路由到 MCP、专业搜索 CLI、浏览器工具或 subagents；README 给出宿主侧准备清单。 |
| **公开发布检查** | [`docs/publishing-checklist.md`](./docs/publishing-checklist.md) 约束敏感内容、路径、数量和文档一致性。 |

---

## 启动

这是一个 source-first 资产包。环境指南和全局 instructions 由用户按宿主选择、备份并合并；安装脚本只负责把 `skills/` 复制到目标 agent 能读取的目录。成功标准是宿主实际加载了目标 instructions、运行时配置和所需 skills。

### 安装对象

| 项 | 值 |
|---|---|
| 运行形态 | source-first 资产包 |
| 环境配置 | `environments/<host>/` 下的指南与可复制资产 |
| 脚本安装内容 | `skills/*` 下的全部 skill 目录 |
| 默认宿主 | Codex / ChatGPT coding agent |
| 安装脚本 | Bash / PowerShell |

### 本地安装

Git Bash / macOS / Linux：

```bash
./scripts/install-skills.sh "$HOME/.codex/skills"
```

PowerShell：

```powershell
.\scripts\install-skills.ps1 -Target "$HOME\.codex\skills"
```

安装到其他 agent 时，把目标参数替换为该宿主实际扫描的 skill 目录：

```bash
./scripts/install-skills.sh "<agent-skill-dir>"
```

```powershell
.\scripts\install-skills.ps1 -Target "<agent-skill-dir>"
```

### 验证安装

Git Bash / macOS / Linux：

```bash
test -d "$HOME/.codex/skills/pro-test"
test -f "$HOME/.codex/skills/pro-test/SKILL.md"
```

PowerShell：

```powershell
Test-Path "$HOME\.codex\skills\pro-test"
Test-Path "$HOME\.codex\skills\pro-test\SKILL.md"
```

---

## 使用流程

| 步骤 | 做法 |
|---|---|
| **1. 选择 coding environment** | 进入对应的 [`environments/<host>/`](./environments/) 指南，确认规则入口、配置文件、skill 机制和宿主能力。 |
| **2. 安装 skills** | 支持 skill 目录的 agent 用安装脚本复制 `skills/*`；其他 agent 可以把对应 `SKILL.md` 作为规则或 workflow 参考。 |
| **3. 安装全局 instructions** | 只复制当前环境目录中的规则文件，并先备份宿主已有配置。模型、权限、MCP 和凭据按指南合并到宿主自己的配置文件。 |
| **4. 补齐外部工具** | 按宿主能力注册 `context7`、`fast-context`、专业搜索 CLI、浏览器 MCP 或 subagents，并让提示词中的工具名与本机配置一致。 |
| **5. 创建项目骨架** | 新项目可运行 [`scripts/new-project.ps1`](./scripts/new-project.ps1)，或直接复制 [`templates/base-project/`](./templates/base-project/)。 |
| **6. 项目内收口** | 进入具体项目后，以项目根 `AGENTS.md` 为 AI 入口，README 面向人类读者，`docs/` 和 `plans/` 分别承载长期文档和计划索引。 |

### Coding environment 入口

| 宿主 | 配置指南 | 全局 instructions |
|---|---|---|
| Codex / ChatGPT coding agent | [`environments/codex/README.md`](./environments/codex/README.md) | [`environments/codex/AGENTS.md`](./environments/codex/AGENTS.md) → `~/.codex/AGENTS.md` |
| Pi Coding Agent | [`environments/pi/README.md`](./environments/pi/README.md) | [`environments/pi/AGENTS.md`](./environments/pi/AGENTS.md) → `~/.pi/agent/AGENTS.md` |
| Claude Code | [`environments/claude-code/README.md`](./environments/claude-code/README.md) | [`environments/claude-code/CLAUDE.md`](./environments/claude-code/CLAUDE.md) → `~/.claude/CLAUDE.md` |
| Gemini / Antigravity 风格工具 | [`environments/gemini/README.md`](./environments/gemini/README.md) | [`environments/gemini/GEMINI.md`](./environments/gemini/GEMINI.md) → `~/.gemini/GEMINI.md` |
| Grok CLI | [`environments/grok/README.md`](./environments/grok/README.md) | [`environments/grok/AGENTS.md`](./environments/grok/AGENTS.md) → `~/.grok/AGENTS.md` |
| Windsurf | [`environments/windsurf/README.md`](./environments/windsurf/README.md) | [`environments/windsurf/global_rules.md`](./environments/windsurf/global_rules.md) → `~/.codeium/windsurf/memories/global_rules.md` |

---

## 配置

| 参数 / 变量 | 默认 | 说明 |
|---|---|---|
| Bash 第一个参数 | 目标 skill 目录 | 传入任意 agent 的 skill 目录，例如 `./scripts/install-skills.sh "<agent-skill-dir>"`。 |
| PowerShell `-Target` | 目标 skill 目录 | 传入任意 agent 的 skill 目录，例如 `.\scripts\install-skills.ps1 -Target "<agent-skill-dir>"`。 |
| `CODEX_HOME` | Codex 用户目录 | 省略目标参数时，脚本优先安装到 `$CODEX_HOME/skills`。 |
| 用户默认目录 | `.codex/skills` | 省略目标参数且 `CODEX_HOME` 为空时使用。 |
| `environments/` | 手动选择 | 按宿主阅读配置指南，备份现有文件后复制全局 instructions，并合并必要配置。 |

### 安装策略

| 场景 | 做法 |
|---|---|
| Source-first 使用 | 从 Git 仓库 clone 后运行脚本安装。 |
| 多宿主共用 | 为每个 agent 传入各自的 skill 目录。 |
| MCP / CLI 配置 | 在宿主自己的配置文件中填写 server、命令、env 和路径。 |
| 公开分发 | README、模板和 prompts 保持通用路径、通用命令和公开可读描述。 |

---

## 外部工具

`skills/` 可以单独安装。采用 [`environments/`](./environments/) 中的全局 instructions，或启用 `use-internet`、`pro-copy` 这类路由 skill 后，下面这些外部能力会成为优先路线；按自己的宿主配置补齐 MCP/CLI，或把规则里的工具名改成宿主实际提供的名字。

| 能力 | 何时需要 | 建议动作 |
|---|---|---|
| `context7` MCP | 查询库、SDK、API、CLI 或云服务官方文档时优先使用。 | 在宿主 MCP 配置里注册 Context7；也可以配置官方文档搜索或专业文档 CLI 作为同类路线。 |
| 专业搜索 CLI | 联网搜索、资料核验、网页抓取或 `fetch`/`deep` 类检索时使用。 | 安装你实际采用的搜索 CLI；如果本机叫 `smart-search` 或其他名字，同步修改宿主提示词中的路由名。 |
| `fast-context` MCP | 大仓库理解、跨文件定位、调用链梳理时优先使用。 | 注册 `fast-context` 或等价 semantic search MCP；精确字符串和文件名继续使用 `rg`、`rg --files`。 |
| 浏览器 MCP / 浏览器工具 | 需要打开网站、表单操作、截图或本地页面 smoke test 时使用。 | 在提供浏览器控制能力的宿主中启用；静态检查、接口检查和人工浏览器验证可以配合使用。 |
| subagents / 并行代理 | 独立阅读、检索、审查任务可并行时使用。 | 在支持多代理的宿主中启用；单代理宿主按同一流程串行执行。 |

真实 server URL、env、token 和本机绝对路径放在个人宿主配置中；公开 README 保留通用工具名和配置方向。

---

## Skill 清单

| Skill | 用途 |
|---|---|
| `pro-copy` | 搜索同类项目、借鉴成熟开源实现。 |
| `pro-exp` | 将解法沉淀为 `.exp/` 经验文档。 |
| `pro-explain` | 面向初学者解释代码或补充必要注释。 |
| `pro-idea` | 生成可分阶段落地的改进建议。 |
| `pro-memory` | 按需维护 `.ai_memory/` 项目级长期上下文。 |
| `pro-must` | 严格按用户指定方案执行。 |
| `pro-plans` | 在项目根 `plans/` 下创建、拆分和维护计划文档。 |
| `pro-readme` | 生成或重写面向人类读者的 README。 |
| `pro-rule` | 将稳定偏好整理为 `.agent/rules/`。 |
| `pro-struct` | 目录结构整理、组件化和复用性治理。 |
| `pro-summary` | README、面向 AI 的 AGENTS.md、docs 与 plans 的一致性审查。 |
| `pro-test` | 测试、调试和验证流程。 |
| `use-chinese` | 默认使用简体中文输出。 |
| `use-internet` | 联网检索与资料核验路由。 |

---

## 开发栈

| 用途 | 技术 |
|---|---|
| **文档资产** | Markdown、AGENTS.md、SKILL.md |
| **安装脚本** | POSIX Shell、PowerShell |
| **项目模板** | 通用目录骨架、项目级规则、文档索引 |
| **外部能力** | `context7`、`fast-context`、专业搜索 CLI、浏览器工具、subagents |
| **质量检查** | `find`、`grep`、人工发布检查清单 |
| **许可** | MIT |

```bash
git status --short
find . -maxdepth 4 -type f | sort
grep -RInE 'secret|token|password|api[_-]?key|sk-|AKIA|PRIVATE|C:\\|D:\\|IndieArk|github.com/indieark|192\.168|\.env|私有|内部|客户|公司|GHCR|PROJECTS.md|端口|奇数|偶数|20001|Steam_UI' .
```

---

## 目录结构

```text
agent-kit/
├─ README.md                      # 用户视角入口
├─ AGENTS.md                      # AI 协作规则
├─ LICENSE
├─ assets/
│  └─ hero.webp                   # README hero image
├─ skills/
│  ├─ pro-readme/                 # README 生成 skill，含模板与检查清单
│  ├─ pro-test/                   # 测试、调试与验证 skill
│  └─ use-internet/               # 联网核验路由 skill
├─ environments/                 # 各 coding agent 的完整环境配置指南
│  ├─ README.md
│  ├─ codex/
│  │  ├─ README.md
│  │  ├─ AGENTS.md
│  │  ├─ config.example.toml
│  │  └─ agents/
│  ├─ pi/
│  │  ├─ README.md
│  │  ├─ AGENTS.md
│  │  ├─ settings.example.json
│  │  └─ models.example.json
│  ├─ claude-code/
│  │  ├─ README.md
│  │  ├─ CLAUDE.md
│  │  └─ settings.example.json
│  ├─ gemini/
│  ├─ grok/
│  └─ windsurf/
├─ system-prompts/
│  └─ README.md                   # 旧路径迁移入口
├─ templates/base-project/        # 通用项目骨架
├─ scripts/
│  ├─ install-skills.sh
│  ├─ install-skills.ps1
│  └─ new-project.ps1
└─ docs/
   ├─ compatibility.md
   ├─ migration-from-00000-model.md
   └─ publishing-checklist.md
```

---

## 文档导航

| 文档 | 说明 |
|---|---|
| [AGENTS.md](./AGENTS.md) | AI 协作约束、公开分发约定和发布前验证规则。 |
| [Coding Environments](./environments/README.md) | 不同 coding agent 的配置入口、资产分层和迁移映射。 |
| [兼容性说明](./docs/compatibility.md) | `skills/`、`environments/` 和项目模板规则的职责分工。 |
| [System Prompts 迁移说明](./system-prompts/README.md) | 旧路径到新环境目录的映射。 |
| [发布检查清单](./docs/publishing-checklist.md) | 公开发布前的文件范围、文档一致性和敏感内容扫描。 |
| [迁移说明](./docs/migration-from-00000-model.md) | 从旧项目模板迁移到公开通用模板的注意事项。 |
| [Changelog](./CHANGELOG.md) | 当前资产包变更记录。 |

---

## 协同关系

本仓按独立开源资产包分发，并与下列宿主或模板入口发生文件级协同关系。

| 关联入口 | 关系 |
|---|---|
| Codex / ChatGPT coding agent | `environments/codex/` 提供用户级 instructions、配置示例和子代理示例；skill 安装脚本仍以 Codex 默认目录为回落基线。 |
| Pi Coding Agent | `environments/pi/` 提供用户级 instructions、Responses API 模型示例、主/子代理努力程度和 package 组合；skills 可安装到 `~/.pi/agent/skills/`。 |
| Claude Code / Gemini / Grok / Windsurf | 通过各自的 `environments/<host>/` 提供完整配置指南；skill 加载能力由宿主自身机制决定。 |
| `templates/base-project/` | 新项目从模板继承 AI 入口、文档分层和计划索引，再按项目实际情况补充业务事实。 |

---

## License

[MIT](./LICENSE)
