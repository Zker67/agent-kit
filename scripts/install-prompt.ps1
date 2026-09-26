<#
.SYNOPSIS
    把 environments/<Host>/ 的全局 instructions 按平台装配后安装到宿主读取位置。

.DESCRIPTION
    本体中独占一行的 {{PLATFORM}} 会替换为 environments/<Host>/platform/<平台>.md，
    装配结果只包含一个平台的规则。目标文件已存在且内容不同时，先备份为
    <目标>.bak-<时间戳> 再写入。

.PARAMETER Agent
    codex, cline, cursor, opencode, pi, claude-code, gemini, grok, windsurf

.PARAMETER Platform
    macos 或 windows；省略时按当前系统自动识别。

.PARAMETER Print
    只把装配结果输出到标准输出，不写盘（Cursor 需在设置界面粘贴）。

.PARAMETER DryRun
    只打印将要执行的备份与写入，不写盘。
#>
param(
    [Parameter(Mandatory = $true, Position = 0)]
    [ValidateSet("codex", "cline", "cursor", "opencode", "pi", "claude-code", "gemini", "grok", "windsurf")]
    [string]$Agent,
    [ValidateSet("macos", "windows")]
    [string]$Platform,
    [switch]$Print,
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$Marker = "{{PLATFORM}}"
# Windows PowerShell 5.1 默认按 ANSI 读写，统一用无 BOM 的 UTF-8。
$Utf8 = New-Object System.Text.UTF8Encoding $false

# Agent -> 本体文件、安装位置。安装位置与各宿主 README 保持一致；Cursor 的 User Rules 只能在设置界面粘贴。
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$Hosts = @{
    "codex"       = @("AGENTS.md",       (Join-Path $CodexHome "AGENTS.md"))
    "cline"       = @("000-global.md",   (Join-Path $HOME "Documents/Cline/Rules/000-global.md"))
    "cursor"      = @("user-rules.md",   "")
    "opencode"    = @("AGENTS.md",       (Join-Path $HOME ".config/opencode/AGENTS.md"))
    "pi"          = @("AGENTS.md",       (Join-Path $HOME ".pi/agent/AGENTS.md"))
    "claude-code" = @("CLAUDE.md",       (Join-Path $HOME ".claude/CLAUDE.md"))
    "gemini"      = @("GEMINI.md",       (Join-Path $HOME ".gemini/GEMINI.md"))
    "grok"        = @("AGENTS.md",       (Join-Path $HOME ".grok/AGENTS.md"))
    "windsurf"    = @("global_rules.md", (Join-Path $HOME ".codeium/windsurf/memories/global_rules.md"))
}
$SourceName, $Target = $Hosts[$Agent]
$SourceFile = Join-Path $RepoRoot "environments/$Agent/$SourceName"
$Content = [System.IO.File]::ReadAllText($SourceFile, $Utf8)

$MarkerCount = ([regex]::Matches($Content, "(?m)^\{\{PLATFORM\}\}\r?$")).Count
if ($MarkerCount -gt 1) {
    Write-Error "$SourceFile 中 $Marker 出现 $MarkerCount 次，只允许一次。"
    exit 1
}

if ($MarkerCount -eq 1) {
    if (-not $Platform) {
        # Windows PowerShell 5.1 没有 $IsWindows，按 $env:OS 判断。
        if ($env:OS -eq "Windows_NT" -or $IsWindows) {
            $Platform = "windows"
        } elseif ($IsMacOS) {
            $Platform = "macos"
        } else {
            Write-Error "无法自动识别平台，请用 -Platform macos|windows 指定。"
            exit 2
        }
    }
    $Fragment = Join-Path $RepoRoot "environments/$Agent/platform/$Platform.md"
    if (-not (Test-Path -Path $Fragment -PathType Leaf)) {
        Write-Error "缺少平台片段: $Fragment"
        exit 1
    }
    $FragmentText = [System.IO.File]::ReadAllText($Fragment, $Utf8)
    # 用字面量替换：片段中的 $HOME 等文本不能被当作正则替换变量。
    if ($Content.Contains("$Marker`r`n")) {
        $Content = $Content.Replace("$Marker`r`n", $FragmentText)
    } else {
        $Content = $Content.Replace("$Marker`n", $FragmentText)
    }
}

if ($Print) {
    [Console]::OutputEncoding = $Utf8
    [Console]::Out.Write($Content)
    exit 0
}

if (-not $Target) {
    Write-Error "$Agent 没有文件形式的全局 instructions，请用 -Print 输出后在宿主设置界面粘贴。"
    exit 2
}

$Prefix = ""
if ($DryRun) { $Prefix = "[dry-run] " }
$Label = $Agent
if ($MarkerCount -eq 1) { $Label = "$Agent ($Platform)" }

if (Test-Path -Path $Target -PathType Leaf) {
    if ([System.IO.File]::ReadAllText($Target, $Utf8) -ceq $Content) {
        Write-Host ("{0}unchanged {1} -> {2}" -f $Prefix, $Label, $Target)
        exit 0
    }
    $Backup = "$Target.bak-$(Get-Date -Format yyyyMMddHHmmss)"
    Write-Host ("{0}backup {1} -> {2}" -f $Prefix, $Target, $Backup)
    if (-not $DryRun) {
        Copy-Item -Path $Target -Destination $Backup
    }
}

Write-Host ("{0}install {1} -> {2}" -f $Prefix, $Label, $Target)
if (-not $DryRun) {
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $Target) | Out-Null
    [System.IO.File]::WriteAllText($Target, $Content, $Utf8)
}
