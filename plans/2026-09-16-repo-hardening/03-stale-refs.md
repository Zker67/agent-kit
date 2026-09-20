# [done] 阶段三：清除过期引用

## 目标

删除仓库中指向不存在资产的路由，并清理本机残留的空目录。

## 涉及文件

- `environments/grok/AGENTS.md`
- 本机未跟踪的空目录 `skills/pro-copy/evals/`
- `CHANGELOG.md`

## 步骤

1. 删除 `environments/grok/AGENTS.md` Tool Routing 段中"生图 / 图编辑：走 Skill `image-gen-pro`"一行。理由：该 skill 不在本仓库，0.1.0 已从全部公开 prompts 移除图片/视频生成路由，其他 8 个环境均无此项，删除而非改名以保持一致。
2. 检查 `environments/grok/README.md` 与 `environments/grok/skills/README.md` 是否有配套描述，如有一并删除。
3. 删除本机 `skills/pro-copy/evals/` 空目录。该目录未被 Git 跟踪，不产生 diff；若阶段四决定给 `pro-copy` 补 evals，则由阶段四重建。
4. CHANGELOG 记录。

## 成功标准

- `grep -RIn 'image-gen-pro\|imagen' environments/ skills/ README.md AGENTS.md` 无命中。
- `git status --short` 只含 `environments/grok/` 与 `CHANGELOG.md`。
- `environments/grok/AGENTS.md` 的 Tool Routing 列表仍保留联网搜索、本地代码搜索、库文档三条。

## 失败分支与回滚

- 若发现 Grok 环境 README 明确说明依赖该图片 skill，则先在实施报告中记录，再决定是删除路由还是补一个公开可用的等价说明；不擅自引入新 skill。
- 回滚：`git checkout -- environments/grok CHANGELOG.md`。
