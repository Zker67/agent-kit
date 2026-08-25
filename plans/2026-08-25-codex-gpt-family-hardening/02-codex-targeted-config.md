# [done] 阶段二：Codex 定向配置
## 目标
只修改 Codex 公开配置资产，给 GPT 系列提供统一 guard，并允许对 gpt-5.6-sol 等具体型号提供可选增强 profile。
## 计划修改
- environments/codex/AGENTS.md：增加短的写入边界、comment minimality 和最终状态生成规则。
- environments/codex/config.example.toml：保持模型选择、推理强度和配置职责清晰，必要时增加 profile 入口说明。
- environments/codex/agents/default.example.toml：只在当前 Codex 版本和任务证据支持时调整子代理模型/effort。
- environments/codex/profiles/：增加 GPT family 与 gpt-5.6-sol 的公开 example。
- environments/codex/README.md：说明 profile、global instructions、external skill 和运行态验证的分工。
## profile 规则
- 先用统一的 GPT family guard，避免维护五套近似 prompt。
- 只有评测证明某个模型需要额外补丁时，才在型号 profile 中增加差异。
- 优先使用 additive 的 developer instructions；不把 model_instructions_file 当作默认方案，因为它会替换内置 instructions。
- 用户 profile 只作为公开 example，仓库不写入真实 ~/.codex/config.toml。
## skill 规则
- 写入阶段依赖 Codex instructions 的 output boundary 和 comment minimality。
- 生成标题、文件名、commit、PR、交付说明或文章开篇时显式调用 no-negative-echo。
- 不把“已遵守规则”“没有负面回声”等证明性句子写入交付物。
## 成功标准
GPT 系列在 Codex 中可以使用同一套基础 guard；gpt-5.6-sol 可选增强 profile 可以启用、回读和撤销；普通输出不会因规则变长而增加元叙事。
