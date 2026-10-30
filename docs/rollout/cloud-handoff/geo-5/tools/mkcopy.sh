#!/bin/zsh
# mkcopy.sh <copy-dir> <tranche-pages...>: throwaway copy of the GEO-4 worktree HEAD with draft sources placed, the lane's
# requests applied (scripts/requests.py, FACTORY-2) and the chain run (scripts/chain.py, which reruns mesh.py after
# links --relink, I28). Borrowed from GEO-1's mkcopy.sh. A page is given as <state> or <state>/<slug>.
set -e
T=$1; shift
D=~/Downloads/fsc-rollout/drafts/geo-5
rm -rf $T; mkdir -p $T
git -C ~/Downloads/wt-rollout-geo-5 archive HEAD | tar -x -C $T
cd $T
for p in "$@"; do
  mkdir -p src/pages/states/$(dirname $p)
  cp $D/pages/$p.html src/pages/states/$p.html
done
cp ${REQ:-$HOME/Downloads/wt-rollout-geo-5/docs/rollout/geo-5/requests.json} $T/geo5-requests.json
$D/tools/to 300 python3 scripts/requests.py $T/geo5-requests.json
$D/tools/to 1800 python3 scripts/chain.py
