#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "$script_dir/.." && pwd)"
source_dir="$repo_root/skills"

if [ "$#" -gt 0 ]; then
  target_dir="$1"
elif [ -n "${CODEX_HOME:-}" ]; then
  target_dir="$CODEX_HOME/skills"
else
  target_dir="$HOME/.codex/skills"
fi

mkdir -p "$target_dir"

for skill_dir in "$source_dir"/*; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  cp -R "$skill_dir" "$target_dir/"
  printf 'installed %s -> %s\n' "$skill_name" "$target_dir/$skill_name"
done
