# [done] 阶段三：结构与 skill 配置验证
## 验证清单
- git status --short 只包含本阶段文件。
- rg --files 检查 `global.md`、九个 agent 文件、模型 skill 文件、README 和引用目标存在。
- 检查公共 skill 没有在 agent 文件和模型文件中重复列出。
- 检查 skills/ 仍只有本仓自研 skill。
- 检查 scripts/install-skills.* 没有新增远程 clone、凭据读取或自动外部安装。
- 执行发布敏感内容扫描，确认没有 token、私有路径、真实 provider 地址或本机状态。
- 人工确认各宿主 README 的发现和安装表述准确，不把登记写成已安装。
## 完成条件
本计划完成只代表仓库能清晰记录和路由 skill，不代表任何外部 skill 已安装，也不代表模型行为已经改善。
