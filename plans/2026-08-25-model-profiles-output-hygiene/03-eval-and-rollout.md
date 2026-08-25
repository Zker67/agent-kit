# [dropped] 阶段三：评测、运行态验证与 rollout（已拆分）

> 后续分别验证仓库结构/skill 路由和 Codex/GPT 系列定向防护，不再使用一套混合验收标准。

## 目标

证明配置改变的是模型写入行为，而不只是增加了更多提示词；验证必须覆盖中间写入、最终包装和真实宿主加载三个层次。

## 评测 fixture

准备四类最小 fixture，每类都有 baseline 和 guarded 版本：

1. Markdown 文档：用户要求只保留最终方案，检查是否出现控制语句、旧方案名和防御性解释。
2. JSX/TSX/HTML/CSS：要求完成一个明确 UI 改动，检查是否新增叙事性注释、被否方案注释、内部流程文案或无必要 tooltip/placeholder。
3. 多轮修订：先提出方案 A/B，再否决 B，最后要求从 A 的最终状态生成标题、文件名、commit 和 handoff。
4. 安全/兼容例外：要求保留必要的迁移、兼容、审计或安全事实，检查 guard 不会把必要事实误删。

## 记录指标

- instruction_leak_count：交付物中控制指令或内部过程的直接/改写残留数量。
- negative_echo_count：最终状态之外的否决方案、删除内容或负向包装数量。
- unnecessary_comment_count：无法对应不变量、契约、取舍、无障碍或安全边界的新增注释数量。
- reintroduction_count：用户清理后下一轮再次出现同类垃圾的次数。
- final_surface_consistency：标题、文件名、文档正文、代码注释、commit/PR/handoff 是否都从最终状态生成。
- exception_preservation：必要安全、兼容、审计和迁移事实是否保留。

## 模型对比协议

- 对 GPT-5.6、GPT-5.5、GPT-5.4 使用同一 fixture、同一上下文脚本和尽可能一致的 reasoning effort。
- 记录具体 alias/snapshot、宿主版本、启用的 skills、工具、上下文大小和是否使用子代理。
- 至少比较三组：
  1. baseline：现有配置。
  2. guard-only：只启用 output-hygiene 规则。
  3. guard-plus-skill：在最终化阶段显式使用 no-negative-echo。
- 不以一次成功输出证明模型缺陷消失；至少记录重复运行和失败样本。

## 宿主运行态验证

### Codex

- 新建会话，确认全局 AGENTS.md、项目 AGENTS.md 和 profile/agent 配置的加载顺序。
- 运行配置回读，确认 active model、reasoning effort、profile 和 skill discovery。
- 检查没有把 model_instructions_file 错当作 additive instructions。
- 使用实际 fixture 生成一次文件变更，读回 diff 和最终交付文本。

### 其他宿主

- 按各自 README 的验证方式确认全局规则被发现。
- 确认 skill 目录和宿主的实际发现/激活状态。
- 不把“文件存在”“面板显示”或“模型说已加载”单独当作行为生效证据。

## 发布前验证

- git status --short
- rg --files 检查新文件和链接目标。
- Markdown 相对链接检查。
- TOML/JSON/YAML 语法检查，只检查公开 example，不读取个人配置。
- 按根 `AGENTS.md` 中的仓库验证命令执行敏感路径、凭据、外部私有信息和数量扫描。
- 检查 README 的 9 个宿主、11 个自研 skill 计数未因外部 skill 记录而误增。
- 检查计划索引和正文状态一致。

## Rollout 顺序

1. 先执行 Codex + 根 AGENTS.md + 新项目模板的 guard-only 验证。
2. 通过基线对比后，再把短规则适配到其他宿主。
3. 单独授权并完成外部 skill 安装/发现/激活验证后，再执行 guard-plus-skill 对比。
4. 只有模型输出和最终 diff 都显示污染下降，才把对应模型档案从 planned 更新为 observed 或 validated。
5. 稳定结论回写 docs/models/；不要把一次实验输出直接写进全局 instructions。

## 失败处理

- 规则导致模型开始复述规则：缩短规则，改为正向最终状态描述，并降低全局 instructions 中的解释密度。
- 模型仍然大量新增备注：优先检查是否把共享规则复制了多遍，或是否把 finalization skill 错放到每次写入路径。
- 用户清理后内容再次出现：将该样本记录为 reintroduction_count，检查会话历史、项目规则和 skill 是否重复注入。
- 必要安全/兼容信息被误删：加入例外 fixture，恢复必要事实，不以“零残留”作为唯一目标。
- 宿主不支持模型条件 profile：保留模型档案和统一 guard，改用宿主支持的全局规则/手动 workflow，不伪造自动路由。

## 完成判定

- 计划中的文件、配置入口和验证命令都能被维护者定位。
- 至少一个宿主完成真实加载验证，至少一个多轮前端/文档 fixture 完成 guarded 对比。
- 用户确认文档和前端清理成本实际下降；代理不代替用户完成视觉和真实交互验收。
