param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]*$')]
    [string]$Name,

    [string]$TargetRoot = (Get-Location).Path,

    [switch]$Force
)

$ErrorActionPreference = "Stop"

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$RepoRoot = Resolve-Path (Join-Path $ScriptDir "..")
$TemplateDir = Join-Path $RepoRoot "templates\base-project"
$ProjectDir = Join-Path $TargetRoot $Name

if ((Test-Path $ProjectDir) -and -not $Force) {
    throw "Target already exists: $ProjectDir. Use -Force to copy into it."
}

New-Item -ItemType Directory -Force -Path $ProjectDir | Out-Null
Get-ChildItem -Path $TemplateDir -Force | ForEach-Object {
    Copy-Item -Path $_.FullName -Destination $ProjectDir -Recurse -Force
}

Write-Host "created project template at $ProjectDir"
