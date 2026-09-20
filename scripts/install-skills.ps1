<#
.SYNOPSIS
    把仓库 skills/ 下的全部 skill 安装到目标 agent 的 skill 目录。

.PARAMETER Target
    目标 skill 目录。省略时依次回落到 $env:CODEX_HOME\skills、$HOME\.codex\skills。

.PARAMETER DryRun
    只打印将要执行的复制与删除，不写盘。

.PARAMETER Clean
    复制前删除目标目录中名称以 pro- 开头、且不在本仓库 skills/ 内的子目录。
    只处理 pro- 前缀，不影响用户放在同一目录的其他 skill。
#>
param(
    [string]$Target,
    [switch]$DryRun,
    [switch]$Clean
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$SourceDir = Join-Path $RepoRoot "skills"

if (-not $Target) {
    if ($env:CODEX_HOME) {
        $Target = Join-Path $env:CODEX_HOME "skills"
    } else {
        $Target = Join-Path $HOME ".codex\skills"
    }
}

$Prefix = ""
if ($DryRun) { $Prefix = "[dry-run] " }

if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path $Target | Out-Null
}

$SourceNames = Get-ChildItem -Path $SourceDir -Directory | ForEach-Object { $_.Name }

# --Clean：删除目标目录里已从仓库移除的 pro- 前缀 skill。
if ($Clean) {
    # 删除动作前校验目标路径非空且已存在，防止路径解析为空导致误删。
    if ([string]::IsNullOrWhiteSpace($Target)) {
        Write-Error "目标目录为空，拒绝执行清理。"
        exit 1
    }
    if (Test-Path -Path $Target -PathType Container) {
        Get-ChildItem -Path $Target -Directory -Filter "pro-*" | ForEach-Object {
            if ($SourceNames -notcontains $_.Name) {
                Write-Host ("{0}remove {1} <- {2}" -f $Prefix, $_.Name, $_.FullName)
                if (-not $DryRun) {
                    Remove-Item -Path $_.FullName -Recurse -Force
                }
            }
        }
    }
}

Get-ChildItem -Path $SourceDir -Directory | ForEach-Object {
    $Destination = Join-Path $Target $_.Name

    # 先删除同名目录再复制，保证已从仓库删除的单个文件不残留。
    if (-not $DryRun) {
        if (-not [string]::IsNullOrWhiteSpace($Destination) -and (Test-Path -Path $Destination -PathType Container)) {
            Remove-Item -Path $Destination -Recurse -Force
        }
        Copy-Item -Path $_.FullName -Destination $Target -Recurse -Force
    }
    Write-Host ("{0}install {1} -> {2}" -f $Prefix, $_.Name, $Destination)
}
