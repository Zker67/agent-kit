## Windows 命令环境

- 仓库操作、Git、`rg` 和类 Unix 脚本优先使用 Git Bash；Windows 服务、注册表、权限、COM、`.ps1` 和 Windows 路径语义任务使用 PowerShell 或 `cmd.exe`。
- 命令失败时先判断当前 shell、语法、路径转换、权限或工具缺失，再决定是否重试。
