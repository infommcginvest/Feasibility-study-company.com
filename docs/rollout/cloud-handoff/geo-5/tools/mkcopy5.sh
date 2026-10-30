#!/bin/zsh
# mkcopy5.sh <copy-dir> <page...>: throwaway copy of the GEO-5 worktree HEAD (local main plus GEO-5 records), with the draft
# sources placed, GEO-5's requests applied (scripts/requests.py), the eight states' borders added to topics.json
# (neighbors5.py, the integrator's change made at landing), any neighbour link patches applied (patches/*.py), and the
# chain run. A page is given as <state> or <state>/<metro>. From GEO-4's mkcopy.sh.
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
$D/tools/to 120 python3 $D/tools/neighbors5.py $T
for f in $D/patches/*.py(N); do $D/tools/to 120 python3 $f $T; done
rm -f $T/geo5-requests.json
$D/tools/to 1800 python3 scripts/chain.py
