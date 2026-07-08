---
name: use-internet
description: 🔍 联网 / 搜索 / 查文档 / 查资料 / 查最新 / 调研 / 英文深度搜索 / reference / 官方文档。技术文档优先 Context7（mcp0_resolve-library-id + mcp0_query-docs），其他优先 smart-search-cli。
---

# Use Internet

在以下情况触发：
- 用户明确要求联网搜索。
- 问题需要最新信息、外部文档、英文深度搜索或可引用来源。
- 问题涉及价格、法规、版本、发布、模型能力、新闻、推荐、医疗、法律、金融等容易变化或高风险信息。
- 用户给出具体 URL、论文、PDF、数据集、仓库、产品页或文档页，需要读取或核验原文。

## 执行要求

1. 优先使用英文检索；中文生态、国内服务或用户明确要求中文时，可同时使用中文检索。
2. **技术文档 / 框架 / API / 库版本 / 代码示例优先 Context7**：
   - 先调 `mcp0_resolve-library-id`（带 `libraryName` + `query`）拿到 `/org/project[/version]` ID。
   - 再调 `mcp0_query-docs`（带 `libraryId` + 具体问题）。
   - 若 Context7 未收录或资料不足，再查官方文档、主仓库、release/changelog、标准文档或论文。
3. **非技术文档场景优先 `smart-search-cli`**；其内部命令遵循该 skill 自身说明，不在本 skill 固化细节。
4. Context7 与 smart-search-cli 均不可用 / 不足时，再用当前 AI 宿主自带搜索 / 浏览工具补充，不要静默切换。
5. 技术问题优先一手资料：官方文档、主仓库 issue/PR/discussion、维护者博客；OpenAI 产品问题优先查 OpenAI 官方文档。
6. 若问题带有时效性，必须显式校验最新信息，区分事件发生日期、页面发布日期和当前查询日期；不要凭旧记忆回答。

## 协同与互斥

- 与 `pro-copy` 协同：`pro-copy` 会委托本 skill 联网检索 GitHub 同类项目。
- 与 `use-chinese` 并存：检索可用英文，但最终给用户的总结用简体中文。

## 输出要求

每条结论必须带：

- **来源 URL**（可点击）。
- **一句话摘要**。
- **时效性标签**：`最新` / `历史` / `需复核（日期 > X 个月）`。

无法确认时必须写 `不确定 / 未证实` 并说明缺哪类证据。

结尾附 "下次查同类问题时优先看的 2-3 条链接"，作为复用入口。
