# Installs the boska-notes skill for Claude Code, Codex CLI and Gemini CLI (user scope).
# usage: powershell -ExecutionPolicy Bypass -File install.ps1 [claude] [codex] [gemini]
$src = Join-Path $PSScriptRoot "skills\boska-notes"
$targets = if ($args.Count -gt 0) { $args } else { @("claude","codex","gemini") }
foreach ($t in $targets) {
  switch ($t) {
    "claude" { $dest = Join-Path $HOME ".claude\skills" }
    "codex"  { $dest = Join-Path $HOME ".codex\skills" }
    "gemini" { $dest = Join-Path $HOME ".gemini\skills" }
    default  { Write-Error "unknown target: $t"; exit 1 }
  }
  New-Item -ItemType Directory -Force -Path $dest | Out-Null
  Copy-Item -Recurse -Force $src $dest
  Write-Host "installed -> $dest\boska-notes"
}
Write-Host "Restart the CLI (Gemini: /skills reload) to pick up the skill."
