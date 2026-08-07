# Cursor User Rules

粘贴到 Cursor：**Settings → Rules → User Rules**。只写 Cursor 内置 harness 定不了的偏好与工具路由。

## 沟通与授权

- 默认简体中文；标识符、命令、路径、专名保持原文。先结论，再最少必要证据与下一步。
- 回答 / 解释 / 审查 / 计划：只读。修改 / 构建 / 修复：可做范围内本地改动与非破坏性验证。
- 外部写入、破坏性 Git、提交、推送、付费、发布部署或明显扩 scope：先确认。

## 工具路由

- 代码探索 / 跨文件定位：优先 MCP `fast-context`（`fast_context_search`）；精确字符串或文件名用 Grep / Glob。
- 库 / SDK / API 文档：优先 MCP `context7`（`resolve-library-id` → `query-docs`）。
- 联网：已知 URL 用 `smart-search fetch`；否则先 `smart-search exa-search "<query>" --num-results 5 --format json`；证据不足或用户要求完整研究再升级 `smart-search search`。
- 前端视觉默认用户真机验证；仅在用户要求时代为浏览器操作。

## Git

- 提交 / PR 仅在用户明确要求后执行；优先 conventional commits。不暴露 secrets；凭据用环境变量。
