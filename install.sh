#!/usr/bin/env sh
set -eu

repo_root=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
dest="${CODEX_HOME:-"$HOME/.codex"}/skills/question-to-prompt-pack"

mkdir -p "$(dirname "$dest")"
rm -rf "$dest"
cp -R "$repo_root/question-to-prompt-pack" "$dest"

echo "Installed question-to-prompt-pack to $dest"
echo "Restart or refresh Codex to reload the skill list."
