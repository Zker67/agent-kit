# 迁移说明

本仓库来自一次白名单抽取：只保留可公开复用的技能、coding environment 配置资产和通用项目模板。

## 保留内容

- 14 个自研 skill。
- 6 类 coding environment 配置指南及其全局 instructions。
- 基础项目模板中的通用 AI 协作结构：`AGENTS.md`、`.agent/rules/`、`docs/`、`references/`、`.ai_memory/` 说明、`.exp/`、`.ui/` 和 `plans/`。

## 移除或泛化内容

- 移除特定部署平台、镜像发布和仓库重命名流程。
- 移除特定组织、特定项目编号、共享组件库和机器路径引用。
- 将模板的 AI 入口统一为 `AGENTS.md`，并明确它面向 AI 助手。
- 将计划写作从环境级全局 instructions 抽出，由 `pro-plans` 或项目模板内的项目级规则承载。
- 将当前项目长期文档收口到 `docs/`，将外部文档和外部仓库参考收口到 `references/`，避免 README、AGENTS、plans 和外部资料互相争夺事实源。
- 将 `MEMO.md` 改为 `MEMO.example.md`，避免暗示本地个人笔记应直接提交。
- `.ai_memory/` 只保留说明和空占位，不携带真实上下文。

## 迁移后检查

发布前需要再次执行敏感内容扫描，并确认扫描命中项不是实际凭据、真实环境地址或不可公开流程。
