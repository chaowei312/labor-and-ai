#!/usr/bin/env bash
# Shallow read-only clones into 5200_finalproj/vendor/<repo-name>/ for browsing.
# For edits: fork on GitHub first, then clone YOUR fork (see vendor/README.md).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
VENDOR="$ROOT/vendor"
mkdir -p "$VENDOR"
cd "$VENDOR"

repos=(
  "https://github.com/VoltAgent/awesome-agent-skills.git"
  "https://github.com/K-Dense-AI/scientific-agent-skills.git"
  "https://github.com/openai/skills.git"
)

for url in "${repos[@]}"; do
  name="$(basename "$url" .git)"
  if [[ -d "$name/.git" ]]; then
    echo "Skip (exists): $name"
    continue
  fi
  echo "Cloning $url ..."
  git clone --depth 1 "$url" "$name"
done

echo ""
echo "Done. Repos are under: $VENDOR"
echo "Next: fork upstream on GitHub, clone your fork here for any customization."
