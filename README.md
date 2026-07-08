<div align="center">

# agent-kit

**面向任意编码代理的可安装 skill 资产包**

`任意目标目录` · `14 个 skills` · `多宿主 prompts` · `通用项目模板`

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

> 把“给不同 coding agent 安装同一套工作流”这件事——skills 目录 + 宿主提示词 + 项目模板——做到一个仓库、一条目标路径可落地。

---

## 核心能力

| 能力 | 实现 |
|---|---|
| **跨宿主 skill 分发** | [`skills/`](./skills/) 保存可公开分发的自研 skill；安装脚本按目录复制到目标宿主读取的位置。 |
| **任意目标目录安装** | [`scripts/install-skills.sh`](./scripts/install-skills.sh) 接收第一个路径参数；[`scripts/install-skills.ps1`](./scripts/install-skills.ps1) 接收 `-Target`。 |
| **Codex 默认路径兼容** | 省略目标参数时，脚本优先使用 `$CODEX_HOME/skills`，再回落到用户目录下的 `.codex/skills`。 |
| **宿主级提示词** | [`system-prompts/`](./system-prompts/) 提供 Codex、Claude Code、Gemini 和 Windsurf 的全局提示词入口。 |
| **新项目模板** | [`templates/base-project/`](./templates/base-project/) 提供通用 `AGENTS.md`、`.agent/rules/`、`docs/`、`references/`、`plans/` 和 `.ai_memory/` 占位结构。 |
| **外部工具前置说明** | [`system-prompts/`](./system-prompts/) 和部分 skill 会优先路由到 MCP、专业搜索 CLI、浏览器工具或 subagents；README 给出宿主侧准备清单。 |
| **公开发布检查** | [`docs/publishing-checklist.md`](./docs/publishing-checklist.md) 约束敏感内容、路径、数量和文档一致性。 |

---

## 启动

这是一个 source-first 资产包。成功标准是：从仓库根目录运行安装脚本，把 `skills/` 复制到目标 agent 能读取的 skill 目录。

### 安装对象

| 项 | 值 |
|---|---|
| 运行形态 | source-first 资产包 |
| 安装内容 | `skills/*` 下的全部 skill 目录 |
| 默认宿主 | Codex / 通用 coding agent |
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
| **1. 确认宿主能力** | 支持 skill 目录的 agent 直接使用目标目录安装；其他 agent 可以把对应 `SKILL.md` 作为规则文档引用。 |
| **2. 安装 skills** | 用安装脚本把 `skills/*` 复制到目标目录；Codex 用户可以省略目标参数使用默认路径。 |
| **3. 选择宿主提示词** | 只复制你实际使用的 [`system-prompts/`](./system-prompts/) 文件，并先备份宿主已有配置。 |
| **4. 补齐外部工具** | 按宿主能力注册 `context7`、`fast-context`、专业搜索 CLI、浏览器 MCP 或 subagents，并让提示词中的工具名与本机配置一致。 |
| **5. 创建项目骨架** | 新项目可运行 [`scripts/new-project.ps1`](./scripts/new-project.ps1)，或直接复制 [`templates/base-project/`](./templates/base-project/)。 |
| **6. 项目内收口** | 进入具体项目后，以项目根 `AGENTS.md` 为 AI 入口，README 面向人类读者，`docs/` 和 `plans/` 分别承载长期文档和计划索引。 |

### 宿主提示词安装示例

| 宿主 | 文件 | 说明 |
|---|---|---|
| Codex / 通用 coding agent | [`system-prompts/AGENTS.md`](./system-prompts/AGENTS.md) | 放到用户级或项目级 `AGENTS.md`。 |
| Claude Code | [`system-prompts/CLAUDE.md`](./system-prompts/CLAUDE.md) | 放到 Claude Code 识别的 `CLAUDE.md`。 |
| Gemini / Antigravity 风格工具 | [`system-prompts/GEMINI.md`](./system-prompts/GEMINI.md) | 放到 Gemini 识别的全局或项目入口。 |
| Windsurf | [`system-prompts/WINDSURF.md`](./system-prompts/WINDSURF.md) | 放到 Windsurf custom instructions 或项目规则入口。 |

---

## 配置

| 参数 / 变量 | 默认 | 说明 |
|---|---|---|
| Bash 第一个参数 | 目标 skill 目录 | 传入任意 agent 的 skill 目录，例如 `./scripts/install-skills.sh "<agent-skill-dir>"`。 |
| PowerShell `-Target` | 目标 skill 目录 | 传入任意 agent 的 skill 目录，例如 `.\scripts\install-skills.ps1 -Target "<agent-skill-dir>"`。 |
| `CODEX_HOME` | Codex 用户目录 | 省略目标参数时，脚本优先安装到 `$CODEX_HOME/skills`。 |
| 用户默认目录 | `.codex/skills` | 省略目标参数且 `CODEX_HOME` 为空时使用。 |
| `system-prompts/` | 手动选择 | 宿主提示词按实际工具选择、备份并复制到对应入口。 |

### 安装策略

| 场景 | 做法 |
|---|---|
| Source-first 使用 | 从 Git 仓库 clone 后运行脚本安装。 |
| 多宿主共用 | 为每个 agent 传入各自的 skill 目录。 |
| MCP / CLI 配置 | 在宿主自己的配置文件中填写 server、命令、env 和路径。 |
| 公开分发 | README、模板和 prompts 保持通用路径、通用命令和公开可读描述。 |

---

## 外部工具

`skills/` 可以单独安装。安装 [`system-prompts/`](./system-prompts/) 或启用 `use-internet`、`pro-copy` 这类路由 skill 后，下面这些外部能力会成为优先路线；按自己的宿主配置补齐 MCP/CLI，或把提示词里的工具名改成宿主实际提供的名字。

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
├─ system-prompts/
│  ├─ AGENTS.md
│  ├─ CLAUDE.md
│  ├─ GEMINI.md
│  └─ WINDSURF.md
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
| [兼容性说明](./docs/compatibility.md) | `skills/`、`system-prompts/` 和项目模板规则的职责分工。 |
| [发布检查清单](./docs/publishing-checklist.md) | 公开发布前的文件范围、文档一致性和敏感内容扫描。 |
| [迁移说明](./docs/migration-from-00000-model.md) | 从旧项目模板迁移到公开通用模板的注意事项。 |
| [Changelog](./CHANGELOG.md) | 当前资产包变更记录。 |

---

## 协同关系

本仓按独立开源资产包分发，并与下列宿主或模板入口发生文件级协同关系。

| 关联入口 | 关系 |
|---|---|
| Codex / 通用 coding agent | 默认 skill 安装路径和 `AGENTS.md` 提示词入口以 Codex 约定为基线，同时允许传入任意目标目录。 |
| Claude Code / Gemini / Windsurf | 通过 `system-prompts/` 提供宿主级规则；skill 加载能力由各宿主自身机制决定。 |
| `templates/base-project/` | 新项目从模板继承 AI 入口、文档分层和计划索引，再按项目实际情况补充业务事实。 |

---

## License

[MIT](./LICENSE)
