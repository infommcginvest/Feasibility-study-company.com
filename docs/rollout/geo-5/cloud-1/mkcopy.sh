#!/bin/bash
# mkcopy.sh <copy-dir> <git-worktree> [<src-file>=<dest-rel> ...]
# Throwaway copy of the worktree HEAD, extra sources placed, then
# env PATCHES (space-separated .py files, each run as: python3 <patch> <copy>) and
# env REQ (a requests.json run through scripts/requests.py), then the chain.
set -e
T=$1; W=$2; shift 2
rm -rf "$T"; mkdir -p "$T"
git -C "$W" archive HEAD | tar -x -C "$T"
for pair in "$@"; do
  src=${pair%%=*}; dst=${pair#*=}
  mkdir -p "$T/$(dirname "$dst")"; cp "$src" "$T/$dst"
done
cd "$T"
if [ -n "$REQ" ]; then cp "$REQ" "$T/_req.json"; timeout 300 python3 scripts/requests.py "$T/_req.json"; rm -f "$T/_req.json"; fi
for p in $PATCHES; do timeout 120 python3 "$p" "$T"; done
timeout 1800 python3 scripts/chain.py
