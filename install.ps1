param(
    [string]$Destination = "$env:USERPROFILE\.codex\skills\question-to-prompt-pack",
    [switch]$InitProfile,
    [switch]$BuildIndex
)

$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillSource = Join-Path $RepoRoot "question-to-prompt-pack"

if (-not (Test-Path -LiteralPath $SkillSource)) {
    throw "Skill source not found: $SkillSource"
}

$DestinationParent = Split-Path -Parent $Destination
New-Item -ItemType Directory -Path $DestinationParent -Force | Out-Null
Copy-Item -LiteralPath $SkillSource -Destination $Destination -Recurse -Force
Write-Host "Installed question-to-prompt-pack to $Destination"

if ($InitProfile) {
    python (Join-Path $Destination "scripts\profile_manager.py") --init --validate
}

if ($BuildIndex) {
    $IndexOut = Join-Path $RepoRoot "skill-index.json"
    python (Join-Path $Destination "scripts\build_local_index.py") --out $IndexOut
    Write-Host "Built local skill index at $IndexOut"
}

Write-Host "Restart or refresh Codex to reload the skill list."
