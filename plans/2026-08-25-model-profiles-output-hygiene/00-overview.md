# [dropped] 模型专用档案与输出污染防护（已拆分）

> 本计划是第一版合并方案，现已拆分为 agent-kit 结构计划和 Codex/GPT 系列定向治理计划，本文件只保留历史方案。

## 背景

当前工作中观察到 GPT-5.6、GPT-5.5、GPT-5.4 在长上下文、多轮纠正和文档/前端编辑场景中容易出现两类输出污染：

1. Control-plane to deliverable leakage：把“如何工作”的 instructions 写进文档、代码注释、UI 文案、commit、PR 或交付说明。
2. Rejected-state / session residue：把已经否决、删除或不属于最终状态的方案继续带入产物。

用户实际受到的影响集中在 Markdown、JSX/TSX、HTML、CSS 和交付包装：备注文字膨胀、负向说明反复出现、清理后的内容再次被补回，导致工作区持续产生垃圾。

本仓库是公开的多宿主 coding-agent 资产包，当前已经区分 environments/、skills/、项目模板和文档；根目录目前没有实际 plans/，本计划补齐计划入口。

## 目标

- 建立按模型、模型别名/快照、宿主 surface 和验证日期记录的模型档案。
- 把模型观察结果、长期规则、复杂 workflow 和运行时模型选择放在不同事实层，避免重复定义。
- 在写入阶段阻断 instructions/历史状态向交付物污染，而不是只在 commit 或最终回复阶段清理。
- 将 no-negative-echo 作为外部 skill 依赖记录和显式最终化流程，不将第三方代码 vendoring 到本仓 skills/。
- 为 Codex 提供可选的模型 profile 示例；对其他宿主按其真实配置能力适配，不伪造统一的模型条件加载机制。
- 建立可重复的输出污染评测，区分静态文案检查、模型运行时行为和用户视觉/交互验收。

## 非目标

- 本计划不修改真实用户的 ~/.codex、~/.claude、~/.cursor 等目录。
- 不自动安装、升级或删除 no-negative-echo，不自动 clone 远程仓库，不修改第三方源码。
- 不把 no-negative-echo 复制进公开 skills/，不增加 vendored 或外部 skill 到 README 的 11 个自研 skill 计数。
- 不自动删除项目中的现有注释、文档或前端文案。
- 不把“前端能力弱”写成未经验证的模型普遍事实；它只能作为带 surface、版本和证据的观察项。
- 不通过增大 instructions、追加解释或生成更多注释来掩盖模型缺陷。

## 当前事实与不变量

- skills/ 只保存可公开分发的自研 skill；第三方 skill 只能作为外部依赖/参考记录。
- environments/ 保存宿主指南、全局 instructions 和公开运行配置示例；模型、权限、provider、MCP 和本机路径不写进通用规则正文。
- skills/pro-newproj/assets/base-project/ 是新项目文档骨架的唯一事实源；模板中的 .agent/rules/、docs/、plans/ 职责不能被新目录破坏。
- README.md 当前记录 9 类宿主、11 个自研 skill；本计划不改变该计数，新增公开文件后要检查链接和发布清单。
- 根工作树在计划开始时干净；后续执行阶段仍须只处理任务文件，保留用户并行修改。
- Codex 当前支持用户级/项目级 AGENTS.md、profile 文件、developer_instructions 和 model_instructions_file 等配置入口，但 model_instructions_file 是替换内置 instructions 的路径，不能在未验证语义前直接采用。

## 目标事实分层

| 层 | 计划中的位置 | 作用 | 是否自动加载 |
|---|---|---|---|
| 模型档案 | docs/models/ | 记录模型特点、缺陷观察、必备 guard、必备 skill、证据和失效条件 | 否，作为记录与路由依据 |
| 通用防污染规则 | 各宿主的全局 instructions、根 AGENTS.md、新项目模板规则 | 每次写入时保持 control plane 与 deliverable 分离 | 由宿主或项目规则加载 |
| 复杂最终化 workflow | 外部 no-negative-echo skill | 从最终状态重新生成标题、注释、commit、PR 和交付说明 | 显式调用/按宿主 skill 机制发现 |
| 模型运行选择 | config.toml、profile、agent 或宿主原生设置 | 选择模型、推理强度和子代理角色 | 由宿主加载 |
| 评测证据 | 计划 fixtures、结果和人工记录 | 证明规则是否降低污染，不能只凭文件存在判断生效 | 否 |

## 阶段索引

1. [模型档案与外部 skill 记录](./01-model-records.md)
2. [AI 配置与规则分层修改](./02-ai-config.md)
3. [评测、运行态验证与 rollout](./03-eval-and-rollout.md)

## 总体验收标准

- 每个模型档案都标明 exact model/alias、surface、验证日期、观察等级和证据；不把推测写成官方事实。
- 文档和前端源码默认不出现“根据要求”“之前被否决”“不是某方案”等控制层/历史层残留，除非当前交付确实需要安全、兼容、审计、迁移或用户明确要求该对比。
- 新增备注只解释不变量、非显然取舍、公共契约、无障碍或安全边界；不复述代码、用户指令或模型工作过程。
- Codex profile 只放模型和必要的增强 instructions，基础规则仍由正常 instructions 层承载；不覆盖内置 instructions 造成静默丢规则。
- no-negative-echo 的来源、版本、安装状态和实际发现/激活状态可被回读验证；未安装时不得写成已启用。
- 至少完成 Markdown、JSX/TSX/CSS 和最终交付文本四类 fixture 的基线/防护对比。
- README、环境指南、模板说明、plans 索引、公开发布扫描和相对链接保持一致。

## 风险与回滚

| 风险 | 控制方式 | 回滚点 |
|---|---|---|
| 全局规则变长，反而增加模型复述概率 | 规则保持短句、正向目标、写入时适用；复杂流程放 skill | 删除各宿主新增 guard block，保留档案记录 |
| 模型档案变成第二套事实源 | 每条观察记录证据和失效条件；当前项目事实仍归源码/docs | 删除重复字段，保留索引和证据链接 |
| Codex profile 替换内置 instructions | 第一阶段只使用已验证的 additive 入口；禁用未经验证的 model_instructions_file | 删除 profile 示例或撤销 profile 选择 |
| 外部 skill 版本漂移或重复安装 | 记录 exact commit、provenance 和 discovery roots；不自动安装 | 停止安装，不删除未知目标，恢复到无外部 skill 状态 |
| 静态扫描误报或漏掉语义残留 | 扫描只作辅助；必须加人工/模型输出复核 | 保留原文并降低结论等级，不为通过扫描改写交付物 |

## 当前状态

- [dropped] 仅完成结构核对和计划编写。
- [dropped] 尚未创建模型档案、共享规则、Codex profile 或评测 fixture。
- [dropped] 尚未安装或激活 no-negative-echo。
