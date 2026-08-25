# [done] 阶段一：agent 独立 skill 路由
## 目标
让每个 agent 有自己的专属 skill 参考文件，同时从 `global.md` 继承公共 skill，避免重复列出相同内容。
## 步骤
1. 把本仓 `skills/` 写入 `global.md`。
2. 将 agent 专用 skill 写入对应 agent 文件；当前没有额外项时保持空声明。
3. 本阶段只记录 agent 专用 skill；模型专用 skill 不放入 agent 的 `skills/`。
4. 在 `environments/README.md` 增加总入口。
## 成功标准
维护者可以从总入口找到公共 skill 和每个 agent 的专属差异。
## 失败分支
宿主没有稳定 skill 配置入口时，只保留简短说明，不发明安装命令。
