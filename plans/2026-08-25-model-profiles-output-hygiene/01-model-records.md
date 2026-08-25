# [dropped] 阶段一：模型档案与外部 skill 记录（已拆分）

> 新模型记录范围由 Codex/GPT 系列定向治理计划负责；外部 skill manifest 范围由 agent-kit 结构计划负责。

## 目标

建立一个不参与自动加载的公开记录层，专门保存模型特点、实测缺陷、必备 skill 和适用边界；它不替代全局 instructions，也不把未经验证的模型判断写成产品事实。

## 计划文件

新增：

    docs/models/
    ├── README.md
    ├── gpt-5.6.md
    ├── gpt-5.5.md
    └── gpt-5.4.md

必要时再增加 evals/ 子目录；第一阶段不提前创建空目录或占位文件。

## docs/models/README.md 内容

- 说明该目录是观察和路由记录，不是官方能力排名，也不是自动加载的 prompt。
- 规定每条记录必须包含：
  - model_id、alias、snapshot 或 provider 标识。
  - 宿主 surface：Codex desktop、CLI、IDE、API 或其他 agent。
  - verified_at、evidence_type、confidence 和 status。
  - strengths、observed failure modes、affected surfaces 和 user impact。
  - required guards、required skills、activation timing 和 fallback。
  - known exceptions：安全、法律、兼容、审计、迁移或用户明确要求的对比可以保留历史/否定信息。
  - invalidation conditions：模型 alias、snapshot、宿主版本、reasoning effort、工具或上下文策略变化时需要重测。
- 区分以下三个词：
  - observed：当前测试或用户工作流观察到。
  - supported：宿主/skill/config 明确支持。
  - active：当前运行态已经发现并加载，必须有回读证据。
- 明确 no-negative-echo 是外部 skill，不计入本仓自研 skill 清单；记录来源、固定 commit、许可、安装方式、发现状态和激活状态。

## 三个模型档案的首批内容

每个档案暂按同一结构记录，不先人为制造三套不同规则：

    model_id: gpt-5.x
    surface: Codex local / ChatGPT coding agent
    verified_at: 2026-08-25
    status: observed
    confidence: medium

    observed_failure_modes:
      - id: control_plane_to_deliverable_leakage
        severity: high
        affected_surfaces: [docs, frontend, comments, handoff]
      - id: rejected_state_session_residue
        severity: high
        affected_surfaces: [docs, frontend, title, commit, pull_request, handoff]

    required_guards:
      - instruction_to_output_boundary
      - comment_minimality

    required_external_skills:
      - name: no-negative-echo
        activation: explicit-finalization
        status: external-not-vendored

    observations:
      frontend: context-dependent; evidence required

具体 wording 必须以正向最终状态为中心，避免档案自身成为一份重复的“禁止事项清单”。

## 证据记录规则

- 以完整 fixture、实际 diff、运行态配置和最终文件回读为证据，不以模型自述为证据。
- 同一模型至少记录一次基线输出和一次启用 guard/skill 后的输出。
- 记录 reasoning effort、工具可用性、上下文长度、宿主版本和是否使用子代理；否则不能比较三个模型。
- 对“前端能力弱”只记录具体任务、surface 和失败表现，例如“新增备注污染 JSX”，不要写成无条件能力排名。
- 被用户删除的内容只能作为历史证据，不能成为下一轮模型的自动事实；如果最终状态必须解释删除原因，单独标记为 required_context。

## 不变量

- 模型档案不被自动当成 instructions。
- docs/models/ 不复制 AGENTS.md 的完整规则正文。
- 任何“必备 skill”都要同时记录触发时机、宿主发现方式和验证方式。
- 外部 skill 不进入 skills/，不由当前仓库安装脚本静默下载。

## 成功标准

- 三个模型档案可单独阅读并能回答“模型是谁、在哪个 surface 观察、有什么风险、何时启用什么 guard/skill、如何验证”。
- 档案之间没有重复事实分叉；共性写在 README，模型差异写在各自文件。
- 外部 skill 的“已记录”“已安装”“已发现”“已激活”四种状态不混淆。

## 回滚

删除本阶段新增的 docs/models/ 文件即可，不触及宿主配置和现有 skills。若后续已被其他文档引用，应先移除引用再回滚。
