# Codex skills

- 通用自研 skill：仓库根目录 [`skills/`](../../../skills/)。

## 外部 skill

- [`no-negative-echo`](https://github.com/LB623/no-negative-echo)：最终化交付物时重新以当前最终状态生成标题、文件名、commit、PR 和 handoff，减少已撤销内容和会话过程残留。
  - 类型：外部 skill，只记录链接，不复制到本仓库。
  - 当前状态：已通过 `manage-skills` 仅部署到 Codex；当前会话尚未证明宿主发现或激活，新会话需要回读。
  - 使用边界：写入阶段仍由 [`environments/codex/AGENTS.md`](../AGENTS.md) 提供统一 guard；该外部 skill 只负责显式最终化阶段。

这是 Codex 外部 skill 的唯一记录入口。模型档案和 profile 只引用这里，不重复维护安装状态。
