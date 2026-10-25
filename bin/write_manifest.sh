#!/usr/bin/env bash
# write_manifest.sh - record how an output directory was produced.
# Usage: write_manifest.sh OUTDIR REPO_DIR SCRIPT [INPUT ...]
# Writes OUTDIR/MANIFEST.txt (overwrites; one run = one manifest).
# MANIFEST_NAME=<file> overrides the file name, for scripts that share a directory.
set -euo pipefail
[[ $# -ge 3 ]] || { echo "usage: $0 OUTDIR REPO_DIR SCRIPT [INPUT ...]" >&2; exit 1; }
out=$1 repo=$2 script=$3; shift 3
mkdir -p "$out"
commit=$(git -C "$repo" rev-parse HEAD 2>/dev/null || echo unknown)
if [[ -n "$(git -C "$repo" status --porcelain 2>/dev/null)" ]]; then state=dirty; else state=clean; fi
envhash=none
if command -v conda >/dev/null 2>&1 && [[ -n "${CONDA_DEFAULT_ENV:-}" ]]; then
  envhash=$(conda list --export 2>/dev/null | sha256sum | cut -c1-12)
fi
{
  echo "date:    $(date -Is)"
  echo "host:    $(hostname)"
  echo "user:    $USER"
  echo "repo:    $(basename "$repo")"
  echo "commit:  $commit ($state)"
  echo "script:  $script"
  echo "env:     ${CONDA_DEFAULT_ENV:-none} (conda list sha256 $envhash)"
  echo "inputs:"
  for f in "$@"; do echo "  $f"; done
} > "$out/${MANIFEST_NAME:-MANIFEST.txt}"
