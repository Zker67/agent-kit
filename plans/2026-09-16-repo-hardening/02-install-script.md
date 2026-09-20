# [done] 阶段二：安装脚本清理与 dry-run

## 目标

让 `scripts/install-skills.sh` 与 `scripts/install-skills.ps1` 在升级时能清除目标目录中已从仓库移除的 skill，并能预览将发生的变化。两个脚本行为必须一致。

## 涉及文件

- `scripts/install-skills.sh`
- `scripts/install-skills.ps1`
- `README.md` 的"启动 / 配置"两段
- `CHANGELOG.md`

## 步骤

1. Bash 脚本增加参数解析：
   - `--dry-run`：只打印将执行的复制与删除，不写盘。
   - `--clean`：复制前删除目标目录中"名称以 `pro-` 开头、且不在本仓库 `skills/` 内"的子目录。只处理 `pro-` 前缀，避免误删用户在同一目录中放置的其他 skill。
   - 位置参数仍为目标目录；参数顺序无关。
   - 每个 skill 先删除目标同名目录再复制，保证被仓库删除的单个文件不残留。
2. PowerShell 脚本增加对应 `-DryRun` 与 `-Clean` 开关，语义相同。
3. 两个脚本对每个动作打印统一格式：`install <name> -> <path>`、`remove <name> <- <path>`，dry-run 时加前缀 `[dry-run]`。
4. README 的安装与配置表补充两个选项，并注明 `--clean` 只影响 `pro-` 前缀目录。
5. CHANGELOG 记录。

## 成功标准

在临时目录中验证，Bash 与 PowerShell 各跑一遍：

1. 空目录安装后恰好 11 个子目录。
2. 手工在目标目录建 `pro-obsolete/` 与 `other-skill/`，带 `--clean` 重装后 `pro-obsolete/` 消失、`other-skill/` 保留。
3. 手工在目标 `pro-summary/` 内加一个 `stale.txt`，重装后该文件消失。
4. `--dry-run --clean` 执行前后目标目录 `find` 输出完全一致，且标准输出列出了本应删除与复制的项。
5. 阶段一的 `scripts/verify.sh` 仍通过。

## 失败分支与回滚

- 删除动作执行前必须校验目标目录为非空字符串且已存在，否则立即退出，防止路径解析为空导致误删。
- 回滚：`git checkout -- scripts/ README.md CHANGELOG.md`。
