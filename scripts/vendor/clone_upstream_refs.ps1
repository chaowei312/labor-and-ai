# Shallow read-only clones into 5200_finalproj/vendor/ — browse only.
# For edits: fork on GitHub first (see vendor/README.md).
$ErrorActionPreference = "Stop"
$Vendor = Join-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) "vendor"
New-Item -ItemType Directory -Force -Path $Vendor | Out-Null
Set-Location $Vendor

$repos = @(
    "https://github.com/VoltAgent/awesome-agent-skills.git",
    "https://github.com/K-Dense-AI/scientific-agent-skills.git",
    "https://github.com/openai/skills.git"
)

foreach ($url in $repos) {
    $name = [System.IO.Path]::GetFileNameWithoutExtension($url)
    if (Test-Path (Join-Path $name ".git")) {
        Write-Host "Skip (exists): $name"
        continue
    }
    Write-Host "Cloning $url ..."
    git clone --depth 1 $url $name
}

Write-Host ""
Write-Host "Done. Repos under: $Vendor"
