## Windows 命令环境

- 以 PowerShell 作为命令执行器外层，Windows 原生操作使用 PowerShell 或 cmd.exe。
- 需要 Git Bash 时，从 PowerShell 显式调用 `C:\Program Files\Git\bin\bash.exe`，例如 `& 'C:\Program Files\Git\bin\bash.exe' ./scripts/check.sh`。保持 shell 选择器为 PowerShell，避免被路由到 WSL。
- 命令失败后，依据错误判断 shell 语法、路径转换、权限或工具缺失，再选择重试方式。
