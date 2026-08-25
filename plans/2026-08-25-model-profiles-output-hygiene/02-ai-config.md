# [dropped] 阶段二：AI 配置与规则分层修改（已拆分）

> 仓库结构和 agent skill 配置由结构计划负责；模型与 Codex 定向配置由 Codex/GPT 系列计划负责。

## 目标

把防污染要求放到正确的自动加载层，同时保持规则短、正向、可执行；把模型专用差异放到可选 profile/agent 层，不让每个宿主的全局 instructions 变成一份巨型模型说明书。

## 配置分层方案

### A. 仓库当前入口

计划修改根 AGENTS.md，增加一个短的“交付内容边界”段落，只包含写入时必须遵守的最小规则：

- 区分 instructions、会话控制信息和交付内容。
- 直接体现要求，不把要求本身、内部过程或合规证明写进交付物，除非用户明确要求。
- 备注只写意图、约束、取舍、公共契约、无障碍或安全边界。
- 交付标题、文件名、注释、commit、PR 和 handoff 从最终采用状态重新生成。
- 用户删除或否决的内容不是当前事实；只有安全、兼容、审计、迁移或明确要求时才保留必要说明。

根 AGENTS.md 不放完整 no-negative-echo 流程、不放模型参数、不放外部安装命令。

### B. 新项目模板

计划修改 skills/pro-newproj/assets/base-project/：

- 新增 .agent/rules/output-hygiene.md，使用现有 always_on frontmatter。
- 在模板 .agent/README.md 中说明该规则的职责是写入阶段的交付边界，不替代宿主全局 instructions。
- 在模板 AGENTS.md 中只增加入口说明，不复制整段规则。
- 在模板 plans/README.md 或 docs 中说明模型档案属于项目/资产包事实记录，计划只记录变更方案。

这样新项目从 pro-newproj 创建时就具备最小保护，但不会继承某一个具体模型的能力判断。

### C. 各宿主全局 instructions

以 environments/shared/ 中的共享规则片段作为维护参考，再按宿主语言和规则长度做薄适配；不要求各文件字节级相同。

首批审查/修改对象：

    environments/codex/AGENTS.md
    environments/cline/000-global.md
    environments/cursor/user-rules.md
    environments/opencode/AGENTS.md
    environments/pi/AGENTS.md
    environments/claude-code/CLAUDE.md
    environments/gemini/GEMINI.md
    environments/grok/AGENTS.md
    environments/windsurf/global_rules.md

规则适配原则：

- 使用正向目标，避免把被禁止词汇重复写成规则正文。
- 只在写入和交付边界上约束，不要求模型在普通回复里汇报“我正在遵守规则”。
- 把 comment_minimality 作为写入规则，而不是鼓励模型在最终回复里解释注释策略。
- 每个宿主文件保持当前已有的简洁度和工具路由，不把 Codex 专属配置字段复制到其他宿主。
- 更新各宿主 README 的配置分工和验证步骤，明确“规则文件存在”不等于当前会话已加载。

### D. Codex 模型与 profile

当前仓库已有 environments/codex/config.example.toml 和 agents/default.example.toml。计划按以下方式扩展：

    environments/codex/
    ├── config.example.toml
    ├── profiles/
    │   ├── README.md
    │   ├── gpt-5.6-output-hygiene.example.toml
    │   ├── gpt-5.5-output-hygiene.example.toml
    │   └── gpt-5.4-output-hygiene.example.toml
    └── agents/

profile 示例只包含：

- exact model alias 或 snapshot。
- 经当前版本验证过的 model_reasoning_effort。
- 必要时的短 developer_instructions 增量，用于加强写入/最终化边界。
- 使用方式、适用任务和验证命令。

第一阶段不使用 model_instructions_file 作为默认方案，因为它会替换内置 instructions，而不是简单追加。若后续确有需要，必须单独验证替换后的完整 instructions 链，再决定是否提供示例。

Codex profile 是可选的模型/任务配置层，不代替 AGENTS.md。Profile 文件应放在用户 CODEX_HOME 的对应目录；仓库只提供公开 example，不修改用户实际配置。

### E. no-negative-echo skill

- 在模型档案和环境指南中记录为 external dependency。
- 不修改 scripts/install-skills.* 让它自动 clone 远程代码。
- 不把第三方 SKILL.md 复制到本仓 skills/。
- 执行阶段如用户明确授权安装，再按上游安装合约完成 clone、检查、测试、来源/commit/provenance、发现和回读；未完成所有门禁不得报告“已安装/已激活”。
- 最终化场景显式调用 skill；普通编辑阶段依赖 always-on 输出边界和 comment minimality，避免等到最后才清垃圾。

## 计划修改文件清单

### 第一批核心文件

- AGENTS.md
- environments/README.md
- environments/codex/README.md
- environments/codex/config.example.toml
- environments/codex/agents/README.md
- skills/pro-newproj/assets/base-project/AGENTS.md
- skills/pro-newproj/assets/base-project/.agent/README.md

### 第二批宿主适配文件

- 九个宿主的全局 instructions 和对应 README，按实际支持的规则/skill 发现机制逐个适配。

## 成功标准

- 任一宿主的全局规则不会要求模型把“规则执行情况”写进代码或文档。
- Codex 主配置、profile 示例、agent 示例和 README 的模型/推理字段一致且可回读。
- 用户不安装外部 skill 时，规则仍能降低写入污染；安装并显式调用后，最终化场景有更强检查。
- 不同宿主不会因为复制 Codex 专属字段而产生无效配置。

## 回滚

- 先回滚宿主适配文件，再回滚模板规则和 Codex profile 示例。
- 保留 docs/models/ 观察记录，不把配置回滚误写成模型观察不存在。
