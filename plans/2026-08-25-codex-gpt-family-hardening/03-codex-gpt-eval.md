# [partial] 阶段三：Codex/GPT 系列评测与 rollout
## 对比组
使用相同任务、上下文、工具和尽可能一致的 reasoning effort，比较 baseline、guard-only 和 guard-plus-skill。
## Fixture
- Markdown 文档：只保留最终方案，不把任务要求写进正文。
- JSX/TSX/HTML/CSS：完成明确 UI 改动，不新增过程性备注、旧方案说明或无必要 UI 文案。
- 多轮否决：方案 B 被否决后，标题、文件名、commit、PR 和 handoff 只描述最终状态。
- 例外保护：必要安全、兼容、审计和迁移事实必须保留。
## 指标
- instruction_leak_count
- negative_echo_count
- unnecessary_comment_count
- reintroduction_count
- final_surface_consistency
- exception_preservation
## 验证
- 回读 active model、alias/snapshot、profile、reasoning effort 和 skill discovery。
- 读取真实 diff 和最终文件，不只看模型自述。
- 对 Markdown 和前端源码做语义人工复核；静态扫描只作辅助。
- 用户负责真实前端视觉和交互验收，代理不把技术检查表述为视觉完成。
## rollout
1. 先在 gpt-5.6-sol 上完成 guard-only 基线对比。
2. 再在 GPT-5.6 Terra/Luna、GPT-5.5、GPT-5.4 或当前实际可用型号上重复最小 fixture。
3. 只有跨型号污染下降且没有误删必要事实，才把统一 guard 标记为 validated。
4. 只有某型号有稳定、可复现的额外差异，才增加型号专用 profile。
## 完成条件
至少重复运行每类 fixture，保留失败样本；Codex 新会话能回读实际配置和 skill 状态；用户确认文档和前端清理成本下降。
