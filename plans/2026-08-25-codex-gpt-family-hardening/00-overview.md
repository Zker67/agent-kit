# [partial] Codex 与 GPT 系列特性及定向防污染修改
## 范围
本计划处理 Codex 使用的 GPT 系列模型和统一输出行为治理。gpt-5.6-sol 是当前主要基准模型，但计划不把防护写成只适用于一个型号；模型档案按 Codex 当前可用的 GPT 型号、alias、snapshot 和宿主 surface 扩展。
结构、agent 独立 skill manifest 和外部仓库引用由 agent-kit 结构计划负责；本计划只引用其中的 external skill id，不重复维护外部仓库来源。
## 目标
- 记录 Codex/GPT 系列的官方特性、模型差异、surface 和验证条件。
- 把 control-plane to deliverable leakage 与 rejected-state/session residue 作为全系列高风险行为模式，先提供统一 guard，再根据证据增加模型差异。
- 定向修改 Codex 全局 instructions、Codex profile/agent example 和最终化 workflow。
- 将 no-negative-echo 作为最终化阶段的外部 skill，不把它当成写入阶段唯一保护。
- 用同一套 fixture 比较 baseline、guard-only 和 guard-plus-skill。
## 非目标
- 不修改九类 agent 的仓库结构。
- 不把 GPT-5.6-Sol 的特性说明复制到所有模型档案。
- 不自动安装 no-negative-echo。
- 不自动清理现有文档、前端注释或用户配置。
- 不以一次成功输出证明模型缺陷消失。
## 计划文件
    docs/models/codex-gpt-family/
    ├── README.md
    ├── gpt-5.6-sol.md
    ├── gpt-5.6-terra.md
    ├── gpt-5.6-luna.md
    ├── gpt-5.5.md
    └── gpt-5.4.md
    environments/codex/
    └── profiles/
        ├── README.md
        ├── gpt-family-output-hygiene.example.toml
        └── gpt-5.6-sol-output-hygiene.example.toml
## 主要不变量
- 官方特性、用户观察、推断和配置对策分层记录。
- 每个结论带 model/alias/snapshot、Codex surface、reasoning effort、版本、日期和证据。
- 写入阶段区分 instructions 与 deliverable content，直接生成最终内容，不把规则或过程写进文件。
- 注释只解释不变量、非显然取舍、公共契约、无障碍或安全边界。
- 最终化标题、文件名、commit、PR 和 handoff 从最终 diff/回读状态重新生成。
- 必要的安全、兼容、审计和迁移事实不得因清理负向内容而删除。
## 阶段索引
1. [Codex/GPT 系列档案](./01-model-family-records.md)
2. [Codex 定向配置](./02-codex-targeted-config.md)
3. [评测与 rollout](./03-codex-gpt-eval.md)
## 回滚
已完成模型档案、Codex guard 和 profile example；运行态跨模型评测仍未完成时，删除本计划新增文件并撤销 Codex instructions 增量即可。
