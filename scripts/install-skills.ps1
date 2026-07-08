param(
    [string]$Target
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

New-Item -ItemType Directory -Force -Path $Target | Out-Null

Get-ChildItem -Path $SourceDir -Directory | ForEach-Object {
    $Destination = Join-Path $Target $_.Name
    Copy-Item -Path $_.FullName -Destination $Target -Recurse -Force
    Write-Host "installed $($_.Name) -> $Destination"
}
