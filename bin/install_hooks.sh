#!/usr/bin/env bash
# Install the shared .gitattributes pre-commit guard in every repo under repos/.
# Writes .git/hooks/pre-commit stubs; a repo's own .githooks/pre-commit (if any)
# is chained after the guard. Re-run after a fresh clone.
# Usage: bash install_hooks.sh [repos_dir]
set -eu

here="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
root="${1:-$(dirname "$here")}"
guard="$here/githooks/pre-commit-gitattributes"

for gitdir in "$root"/*/.git; do
    [ -d "$gitdir" ] || continue
    repo="$(dirname "$gitdir")"
    hook="$gitdir/hooks/pre-commit"
    cat > "$hook" <<STUB
#!/bin/sh
# Installed by kansasii-docs/bin/install_hooks.sh
sh "$guard" || exit 1
[ -x "\$(git rev-parse --show-toplevel)/.githooks/pre-commit" ] \\
    && exec "\$(git rev-parse --show-toplevel)/.githooks/pre-commit"
exit 0
STUB
    chmod +x "$hook"
    echo "installed $(basename "$repo")"
done
