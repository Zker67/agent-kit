# [done] 阶段二：外部 skill 引用策略
## 规则
- 外部 skill 只记录仓库链接。
- 不复制外部仓库内容。
- 不从 README 的 URL 直接 pipe 到 shell。
- 用户只要求指向仓库时，只更新说明，不安装。
- 安装行为由具体宿主或用户选择的 skill manager 负责，不由本仓库的通用安装脚本处理。
## no-negative-echo
本阶段只把它列为 Codex / GPT 系列专用 skill 的外部参考。具体何时显式调用、对 GPT/Codex 的效果和评测由另一个计划负责。
## 验收
发布检查能发现 external skill 被错误复制进 `skills/`，或外部链接被写成安装结果。
