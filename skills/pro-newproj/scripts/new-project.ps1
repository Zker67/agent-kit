param(
    [Parameter(Mandatory = $true)]
    [ValidatePattern('^[A-Za-z0-9][A-Za-z0-9._-]*$')]
    [string]$Name,

    [string]$TargetRoot = (Get-Location).Path,

    [switch]$Merge
)

$ErrorActionPreference = "Stop"

$SkillDir = Resolve-Path (Join-Path $PSScriptRoot "..")
$TemplateDir = Join-Path $SkillDir "assets\base-project"
$TargetRootPath = [System.IO.Path]::GetFullPath($TargetRoot)
$ProjectDir = [System.IO.Path]::GetFullPath((Join-Path $TargetRootPath $Name))

if (-not (Test-Path -LiteralPath $TemplateDir -PathType Container)) {
    throw "Bundled project template is missing: $TemplateDir"
}

if (Test-Path -LiteralPath $ProjectDir -PathType Leaf) {
    throw "Target is a file, not a directory: $ProjectDir"
}

$TargetExists = Test-Path -LiteralPath $ProjectDir
$TargetHasFiles = $TargetExists -and [bool](Get-ChildItem -LiteralPath $ProjectDir -Force | Select-Object -First 1)

if ($TargetHasFiles -and -not $Merge) {
    throw "Target is not empty: $ProjectDir. Use -Merge to add only missing template files."
}

$TemplateFiles = Get-ChildItem -LiteralPath $TemplateDir -File -Recurse -Force
$TemplatePrefix = $TemplateDir.TrimEnd('\', '/') + [System.IO.Path]::DirectorySeparatorChar
$Conflicts = @()

foreach ($SourceFile in $TemplateFiles) {
    $RelativePath = $SourceFile.FullName.Substring($TemplatePrefix.Length)
    $DestinationFile = Join-Path $ProjectDir $RelativePath
    if (Test-Path -LiteralPath $DestinationFile) {
        $Conflicts += $RelativePath
    }
}

if ($Conflicts.Count -gt 0 -and -not $Merge) {
    throw "Target contains template paths: $($Conflicts -join ', ')"
}

New-Item -ItemType Directory -Force -Path $ProjectDir | Out-Null

$Copied = @()
$Skipped = @()

foreach ($SourceFile in $TemplateFiles) {
    $RelativePath = $SourceFile.FullName.Substring($TemplatePrefix.Length)
    $DestinationFile = Join-Path $ProjectDir $RelativePath

    if (Test-Path -LiteralPath $DestinationFile) {
        $Skipped += $RelativePath
        continue
    }

    $DestinationDir = Split-Path -Parent $DestinationFile
    New-Item -ItemType Directory -Force -Path $DestinationDir | Out-Null
    Copy-Item -LiteralPath $SourceFile.FullName -Destination $DestinationFile
    $Copied += $RelativePath
}

Write-Host "Project documentation scaffold: $ProjectDir"
Write-Host "Copied files: $($Copied.Count)"

if ($Skipped.Count -gt 0) {
    Write-Host "Skipped existing files: $($Skipped.Count)"
    $Skipped | ForEach-Object { Write-Host "  $_" }
}
