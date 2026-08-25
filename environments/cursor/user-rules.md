# Cursor User Rules

粘贴到 Cursor：**Settings → Rules → User Rules**。只写 Cursor 内置 harness 定不了的偏好与工具路由。

## 沟通与授权

默认简体中文；标识符、命令、路径、专名保持原文。先结论，再最少必要证据与下一步。
回答/解释/审查/计划：只读。修改/构建/修复：可做范围内本地改动与非破坏性验证。
外部写入、破坏性 Git、提交、推送、付费、发布部署或明显扩 scope：先确认。

## 工具路由

代码探索：优先 MCP fast-context；精确字符串/文件名用 Grep/Glob。
库文档：优先 MCP context7（resolve-library-id → query-docs）。
联网：已知 URL 用 smart-search fetch；否则先 exa-search（5 条）；不足或要求深研再升级 search。
前端视觉默认用户真机验证；仅在用户要求时代为浏览器操作。

## Git 与分支

默认留在当前分支（通常 main）。未明确说「开分支/开 PR/开 worktree」时：不切分支、不开 worktree、不迁工作区。不 stash/reset/clean 掉他人未提交改动。
提交/PR/推送仅在用户明确要求后执行；优先 conventional commits；用 gh 开 PR。凭据走环境变量，不写入仓库。
