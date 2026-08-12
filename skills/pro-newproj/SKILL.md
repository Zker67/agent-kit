---
name: pro-newproj
description: 🆕 新建项目 / 初始化项目 / 项目骨架 / project scaffold / bootstrap repo / 完整文档结构。用于创建新项目，或给刚创建的空仓库补齐 `AGENTS.md`、`README.md`、`.agent/rules/`、`docs/`、`references/` 和 `plans/` 的完整文档骨架；模板随 skill 自带，默认不初始化 Git、不安装依赖、不覆盖已有文件。
---

# Pro New Project

为新项目建立一套可直接协作、可长期维护的文档骨架。完整模板位于 `assets/base-project/`，它是这套结构的唯一事实源；优先调用 `scripts/new-project.ps1` 复制，不要在其他位置维护第二份模板。

## 触发场景

- 用户要求“新建项目”、“初始化项目”、“创建项目骨架”、“创建空仓库结构”。
- 用户提到 `pro-newproj`、`project scaffold`、`bootstrap repo` 或“完整文档结构”。
- 用户刚创建代码仓库，希望补齐 AI 协作入口、长期文档、外部参考和计划索引。
- 用户希望多个新项目采用一致的 `README.md`、`AGENTS.md`、`docs/`、`references/`、`plans/` 和 `.agent/rules/` 分层。

## 与相邻 skill 的边界

- **README 单独生成或美化**：使用 `pro-readme`；本 skill 只提供新项目初始 README 骨架。
- **只写实施计划**：使用 `pro-plans`；不要为计划任务创建整套项目结构。
- **审查现有文档一致性**：使用 `pro-summary`；本 skill 面向新项目或刚初始化的仓库。
- **重构既有代码目录**：使用 `pro-struct`；不要借“初始化”改造成熟项目结构。
- **维护项目级规则**：初始通用规则由本 skill 创建，后续规则提炼交给 `pro-rule`。

## 内置文档结构

```text
项目根目录/
├── AGENTS.md
├── README.md
├── .agent/
│   ├── README.md
│   └── rules/
│       └── dev.md
├── docs/
│   ├── README.md
│   ├── api.md
│   ├── operations.md
│   └── architecture/
│       ├── README.md
│       ├── project-structure.md
│       └── source-of-truth.md
├── references/
│   ├── README.md
│   ├── external-docs/
│   │   └── README.md
│   └── external-repos/
│       └── README.md
└── plans/
    └── README.md
```

## 工作流

### 1. 确认目标目录

从用户输入和当前工作区确定：

- 项目名称。
- 父目录或现有项目目录。
- 是创建全新目录，还是给刚创建的仓库补文档。
- 已确认的项目定位、核心需求、技术栈和运行方式。

目标位置缺失但可从当前目录安全推断时，说明假设后继续。若目标选择会覆盖现有文件或可能落到错误仓库，先向用户确认。

### 2. 检查现有状态

创建前检查目标路径和工作树：

- 新目录或空目录可以直接初始化。
- 非空目录默认停止，不覆盖任何文件。
- 用户明确要求给现有新仓库补文档时，使用 `-Merge`；脚本只复制缺失文件，并列出跳过的冲突文件。
- 如果现有 `README.md`、`AGENTS.md` 或文档包含真实内容，保留它们，先读取再做聚焦合并。

### 3. 复制内置骨架

在 PowerShell 中调用本 skill 自带脚本：

```powershell
& "<skill-dir>\scripts\new-project.ps1" -Name "<project-name>" -TargetRoot "<parent-dir>"
```

给现有新仓库补缺失文档：

```powershell
& "<skill-dir>\scripts\new-project.ps1" -Name "<project-name>" -TargetRoot "<parent-dir>" -Merge
```

宿主无法执行 PowerShell 时，按 `assets/base-project/` 的相对路径完整复制文件，并遵守相同的“不覆盖已有文件”规则。

### 4. 用已确认事实完成初始化

复制后只填写用户已经提供或能从实际代码确认的内容：

- `README.md`：项目名、一句话定位、核心需求、真实技术选型和可验证命令。
- `AGENTS.md`：项目定位、重要不变量、项目特有验证方式和授权边界。
- `docs/architecture/project-structure.md`：实际存在的源码目录和模块职责。
- `docs/operations.md`：已确认的安装、启动、测试、构建和部署入口。
- `docs/api.md`：已经存在或已经确定的 API、schema、事件合同。
- `plans/README.md`：只有实际创建计划时才登记计划，不制造虚假状态。

信息未知时保留明确占位注释或 `-`，不要猜测端口、命令、框架、部署方式、API 或业务功能。

### 5. 验证

至少检查：

1. 内置结构中的文件全部存在。
2. `.agent/` 等隐藏目录已复制。
3. Markdown 相对链接指向真实文件。
4. README、AGENTS、docs、references 和 plans 的职责没有互相冲突。
5. 没有真实凭据、本机绝对路径、运行态数据或私有组织信息。
6. 若目标已是 Git 仓库，只报告 `git status --short`；不要自动提交或推送。

## 安全边界

- 默认不覆盖、删除或移动目标项目中的已有文件。
- `-Merge` 只补缺失文件，不覆盖冲突路径；需要合并内容时先读现有文件，再做最小编辑。
- 不默认运行 `git init`、创建远端仓库、commit、push、发布或部署。
- 不默认安装依赖、调用框架生成器或启动服务；只有用户明确要求完整创建对应技术项目时才执行。
- 不把宿主全局 instructions、个人偏好、真实凭据或机器路径写入通用项目骨架。

## 输出要求

最终回复说明：

- 创建或补齐的项目路径。
- 新增了哪些文档层级。
- 哪些文件因已存在而保留或跳过。
- 已填写哪些已确认事实，哪些占位仍待用户补充。
- 跑过哪些结构、链接或安全检查。
- Git、依赖安装、运行、提交、推送和部署是否未执行。
