#!/bin/zsh
# ASSET-1 throwaway build: copy HEAD, add the tranche's draft sources, run the chain, check.
#   docs/rollout/asset-1/tools/selfcheck.sh <n> <url> [<url> ...]
# The copy is ~/Downloads/fsc-rollout/tmp/asset-1/t<n>; drafts come from ~/Downloads/fsc-rollout/drafts/asset-1/pages/.
set -u
timeout() { local s=$1; shift; perl -e 'alarm shift; exec @ARGV' $s "$@"; }
n=$1; shift
WT=~/Downloads/wt-rollout-asset-1
T=~/Downloads/fsc-rollout/tmp/asset-1/t$n
DR=~/Downloads/fsc-rollout/drafts/asset-1/pages
OUT=~/Downloads/fsc-rollout/tmp/asset-1/t$n.log
rm -rf $T; mkdir -p $T
git -C $WT archive HEAD | tar -x -C $T
for u in "$@"; do
  p=${u#/}; p=${p%/}
  mkdir -p $T/src/pages/${p:h}
  cp $DR/$p.html $T/src/pages/$p.html || { echo "MISSING draft $p"; exit 2; }
done
cd $T
: > $OUT
for s in "build.py" "chrome.py" "byline.py" "regulatory.py" "markets.py" "casemodel.py" "mesh.py" "links.py --relink" "sitemap.py"; do
  echo "== $s" >> $OUT
  timeout 600 python3 scripts/${=s} >> $OUT 2>&1; rc=$?
  echo "   exit $rc" >> $OUT
  [ $rc -ne 0 ] && { echo "CHAIN FAILED at $s (exit $rc)"; tail -20 $OUT; exit 3; }
done
for s in build.py byline.py regulatory.py chrome.py markets.py casemodel.py mesh.py links.py; do
  timeout 600 python3 scripts/$s --check >> $OUT 2>&1; echo "check $s exit $?"
done
timeout 900 python3 $T/docs/rollout/asset-1/tools/lanecheck.py --root $T --json $T.json "$@"
