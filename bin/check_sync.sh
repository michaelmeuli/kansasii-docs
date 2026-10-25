#!/usr/bin/env bash
# Check that every git repo under this directory is in sync with origin.
# Reports: uncommitted changes, unpushed/unpulled commits per local branch,
# and branches without an upstream. Exit code 1 if anything is out of sync.
# Also checks that .gitattributes, .vscode/settings.json and the vendored kansasii_paths.py
# match kansasii-docs/templates/{gitattributes,vscode-settings.json,kansasii_paths.py}, that
# .gitignore holds every line of templates/gitignore, that no tracked file has CRLF and the
# shared repo layout (README.md, CLAUDE.md, environment.yml, pyproject.toml; sbatch files only
# at the root, named submit_*.sbatch; no literal project root in code); --fix copies the
# canonical files in (staged, not committed).
# Usage: ./check_sync.sh [--no-fetch] [--fix] [root_dir]
set -u

fetch=1
fix=0
while [ $# -gt 0 ]; do
    case "$1" in
        --no-fetch) fetch=0; shift ;;
        --fix) fix=1; shift ;;
        *) break ;;
    esac
done
root="${1:-$(cd "$(dirname "$(readlink -f "${BASH_SOURCE[0]}")")/../.." && pwd)}"
canon="$root/kansasii-docs/templates/gitattributes"
canon_vscode="$root/kansasii-docs/templates/vscode-settings.json"

canon_paths="$root/kansasii-docs/templates/kansasii_paths.py"
canon_ignore="$root/kansasii-docs/templates/gitignore"
ROOT_LITERAL='/shares/sander.imm.uzh/MM/kansasii'

status=0
for gitdir in "$root"/*/.git; do
    [ -e "$gitdir" ] || continue
    repo="$(dirname "$gitdir")"
    name="$(basename "$repo")"
    problems=()

    if [ -f "$canon" ] && ! cmp -s "$canon" "$repo/.gitattributes"; then
        if [ "$fix" = 1 ]; then
            cp "$canon" "$repo/.gitattributes"
            git -C "$repo" add .gitattributes
            git -C "$repo" add --renormalize . >/dev/null 2>&1
            echo "fixed .gitattributes in $name (staged, not committed)"
        else
            problems+=(".gitattributes differs from kansasii-docs/templates/gitattributes")
        fi
    fi
    if [ -f "$canon_vscode" ] && ! cmp -s "$canon_vscode" "$repo/.vscode/settings.json"; then
        if [ "$fix" = 1 ]; then
            mkdir -p "$repo/.vscode"
            cp "$canon_vscode" "$repo/.vscode/settings.json"
            git -C "$repo" add -f .vscode/settings.json
            echo "fixed .vscode/settings.json in $name (staged, not committed)"
        else
            problems+=(".vscode/settings.json differs from kansasii-docs/templates/vscode-settings.json")
        fi
    fi
    # vendored copies of kansasii_paths.py (next to the code of each repo; the template itself lives in kansasii-docs)
    if [ -f "$canon_paths" ] && [ "$name" != "kansasii-docs" ]; then
        mapfile -t copies < <(git -C "$repo" ls-files '*kansasii_paths.py')
        if [ ${#copies[@]} -eq 0 ]; then
            problems+=("no vendored kansasii_paths.py (copy kansasii-docs/templates/kansasii_paths.py next to the code)")
        fi
        for c in "${copies[@]}"; do
            if ! cmp -s "$canon_paths" "$repo/$c"; then
                if [ "$fix" = 1 ]; then
                    cp "$canon_paths" "$repo/$c"; git -C "$repo" add "$c"
                    echo "fixed $c in $name (staged, not committed)"
                else
                    problems+=("$c differs from kansasii-docs/templates/kansasii_paths.py")
                fi
            fi
        done
    fi
    # .gitignore must contain every line of the template
    if [ -f "$canon_ignore" ]; then
        while IFS= read -r line; do
            if ! grep -qxF -- "$line" "$repo/.gitignore" 2>/dev/null; then
                if [ "$fix" = 1 ]; then
                    echo "$line" >> "$repo/.gitignore"; git -C "$repo" add .gitignore
                    echo "fixed .gitignore in $name: added $line (staged, not committed)"
                else
                    problems+=(".gitignore lacks '$line' (templates/gitignore)")
                fi
            fi
        done < "$canon_ignore"
    fi
    # shared layout
    if [ "$name" != "kansasii-docs" ]; then
        for f in README.md CLAUDE.md environment.yml; do
            [ -e "$repo/$f" ] || problems+=("missing $f")
        done
    fi
    while IFS= read -r f; do
        case "$f" in
            submit_*.sbatch) ;;
            *) problems+=("sbatch file '$f' must be a root file named submit_*.sbatch") ;;
        esac
    done < <(git -C "$repo" ls-files '*.sbatch')
    # the only allowed literal is the fallback of the `source .../kansasii_paths.sh` bootstrap line
    lit=$(git -C "$repo" grep -nI -e "$ROOT_LITERAL" -- '*.py' '*.sh' ':!*kansasii_paths.*' ':!immensekansasii/bin' 2>/dev/null \
          | grep -v 'kansasii_paths.sh' | grep -vE '^[^:]+:[0-9]+:\s*#' || true)
    [ -n "$lit" ] && problems+=("literal $ROOT_LITERAL in code (use kansasii_paths): $(echo "$lit" | head -3 | cut -d: -f1,2 | tr '\n' ' ')")

    ncrlf=$(git -C "$repo" ls-files --eol | grep -c 'w/crlf')
    [ "$ncrlf" -gt 0 ] && problems+=("$ncrlf tracked files with CRLF in working tree")

    if [ "$fetch" = 1 ]; then
        git -C "$repo" fetch --quiet --prune origin 2>/dev/null \
            || problems+=("fetch from origin failed")
    fi

    if [ -n "$(git -C "$repo" status --porcelain)" ]; then
        problems+=("uncommitted changes ($(git -C "$repo" status --porcelain | wc -l) files)")
    fi

    while IFS='|' read -r branch upstream; do
        if [ -z "$upstream" ]; then
            problems+=("branch '$branch' has no upstream")
            continue
        fi
        read -r behind ahead < <(git -C "$repo" rev-list --left-right --count "$upstream...$branch")
        [ "$ahead" -gt 0 ] && problems+=("branch '$branch' is $ahead ahead of $upstream (unpushed)")
        [ "$behind" -gt 0 ] && problems+=("branch '$branch' is $behind behind $upstream (unpulled)")
    done < <(git -C "$repo" for-each-ref --format='%(refname:short)|%(upstream:short)' refs/heads)

    if [ ${#problems[@]} -eq 0 ]; then
        printf '\033[32mOK \033[0m %s\n' "$name"
    else
        status=1
        printf '\033[31mDIFF\033[0m %s\n' "$name"
        printf '       - %s\n' "${problems[@]}"
    fi
done
exit $status
