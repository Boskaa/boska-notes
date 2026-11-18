#!/usr/bin/env bash
# Installs the boska-notes skill for Claude Code, Codex CLI and Gemini CLI (user scope).
# usage: ./install.sh [claude] [codex] [gemini]   (no argument = all three)
set -euo pipefail
SRC="$(cd "$(dirname "$0")" && pwd)/skills/boska-notes"
targets=("$@"); [ ${#targets[@]} -eq 0 ] && targets=(claude codex gemini)
for t in "${targets[@]}"; do
  case "$t" in
    claude) dest="$HOME/.claude/skills" ;;
    codex)  dest="$HOME/.codex/skills" ;;
    gemini) dest="$HOME/.gemini/skills" ;;
    *) echo "unknown target: $t"; exit 1 ;;
  esac
  mkdir -p "$dest"
  cp -R "$SRC" "$dest/"
  echo "installed -> $dest/skills/boska-notes"
done
echo "Restart the CLI (Gemini: /skills reload) to pick up the skill."
