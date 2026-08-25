# [done] agent-kit 结构与独立 skill 配置
## 范围
本计划只处理公开资产包的目录结构、agent 独立 skill 配置和外部 skill 仓库引用，不处理 GPT/Codex 的模型行为修复。
当前仓库已经把宿主指南放在 `environments/`、本仓自研 skill 放在 `skills/`，但全局 skill 和 agent 专属 skill 没有单独的参考层。直接复制第三方 skill 会破坏自研 skill 边界，因此只增加轻量 Markdown 引用。
## 目标
- 区分所有 agent 共用的 skill 与 agent 专属 skill。
- 为每个 agent 保存独立的 skill 参考文件。
- 允许参考文件指向外部 skill 仓库，不复制第三方代码。
- 保持 `skills/`、`scripts/install-skills.*` 和 `environments/<host>/` 的职责清晰。
## 建议结构
每个 agent 目录增加 `skills/`：
    environments/<agent>/skills/README.md
根目录 `skills/` 保存公共自研 skill；各 agent 目录的 `skills/` 保存该 agent 的专用 skill 或外部 skill 引用。宿主原生配置仍由 `environments/<host>/README.md` 说明。
## 阶段
1. 保持根目录 `skills/` 作为公共自研 skill 源。
2. 为九类 agent 增加各自的 `skills/` 目录。
3. 本阶段不把模型专用 skill 放入 agent 目录；模型专用 skill 留给模型配置计划处理。
4. 更新 `environments/README.md`，不把本次结构说明加入发布清单。
## 不变量
- skills/ 仍只放本仓自研 skill。
- 外部 skill 不由通用安装脚本静默下载。
- 公共 skill 实现不复制到各 agent 的 `skills/` 目录。
- 文件存在或 README 显示不等于运行时已加载。
## 验收与回滚
九个 agent 的 `skills/` 目录存在，Markdown 链接指向真实路径，外部 skill 只通过仓库链接被记录。
回滚时删除各 agent 新增的 `skills/` 目录并撤销总入口引用，不触及根目录 `skills/` 和用户级目录。
