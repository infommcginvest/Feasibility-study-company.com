#!/bin/zsh
# CASE-NEW-1 workbench self-check for one case draft. Serialized by a mkdir lock so writers never race.
# usage: wbcheck.sh <slug>     (reads ~/Downloads/fsc-rollout/drafts/case-new-1/<slug>/page.html and case.json)
slug=$1; D=~/Downloads/fsc-rollout/drafts/case-new-1/$slug; WB=~/Downloads/wt-rollout-case-new-1; L=~/Downloads/fsc-rollout/tmp/case-new-1/wb.lock
[ -f $D/page.html ] && [ -f $D/case.json ] || { echo "need $D/page.html and $D/case.json"; exit 2; }
n=0; until mkdir $L 2>/dev/null; do n=$((n+1)); [ $n -gt 300 ] && { echo "lock busy 10 min; retry later"; exit 3; }; sleep 2; done
trap 'rmdir $L' EXIT
cd $WB || exit 4
cp $D/page.html src/pages/case-studies/$slug.html && cp $D/case.json data/cases/$slug.json; [ -f $D/card.json ] && { mkdir -p src/case-cards; cp $D/card.json src/case-cards/$slug.json; }
T() { perl -e 'alarm 300; exec @ARGV' "$@"; }
echo "== build.py --page"; T python3 scripts/build.py --page /case-studies/$slug/ 2>&1 | tail -5
for s in chrome byline regulatory markets; do T python3 scripts/$s.py >/dev/null 2>&1 || echo "$s.py exit $?"; done
echo "== casemodel.py --only"; T python3 scripts/casemodel.py --only $slug 2>&1 | tail -8
echo "== casemodel.py --check --only"; T python3 scripts/casemodel.py --check --only $slug 2>&1 | tail -5
echo "== build.py --check --page"; T python3 scripts/build.py --check --page /case-studies/$slug/ 2>&1 | tail -3
echo "== pagecheck"; T python3 scripts/qa/pagecheck.py --stage ready /case-studies/$slug/ --figures --overlap 5 2>&1 | tail -20
echo "== sbamandate"; T python3 scripts/qa/sbamandate.py case-studies/$slug/index.html 2>&1 | tail -3
echo "== gate8 own list"; python3 - "$slug" case-studies/$slug/index.html src/pages/case-studies/$slug.html data/cases/$slug.json <<'PY'
import sys,re,html,urllib.parse,glob,os
slug=sys.argv[1]
def flat(s):
    s=html.unescape(urllib.parse.unquote(s)).lower(); toks=re.findall(r"\d+(?:[.,]\d+)*|[a-z]+",s)
    return " "+" ".join(t.replace(",","") if t[0].isdigit() else t for t in toks)+" "
toks=[]
for f in [os.path.expanduser(f"~/Downloads/fsc-rollout/drafts/case-new-1/{slug}/dnu.tsv")]+glob.glob(os.path.expanduser("~/Downloads/fsc-rollout/private/*.txt")):
    if not os.path.exists(f): continue
    for l in open(f,encoding='utf-8'):
        if '\t' not in l or l.startswith('#'): continue
        s,t=l.rstrip('\n').split('\t',1)
        if s in (slug,'*') and t.strip(): toks.append(t.strip())
hits=set()
for p in sys.argv[2:]:
    raw=open(p,encoding='utf-8',errors='replace').read().lower(); fr=flat(raw)
    for t in toks:
        if re.search(r"(?<![0-9a-z])"+re.escape(t.lower())+r"(?![0-9a-z])",raw) or flat(t) in fr: hits.add((t,p))
print(f"{len(toks)} tokens checked; {len(hits)} hits")
for t,p in sorted(hits): print("  HIT",t,"in",p)
PY
echo "== dashes and banned names in draft files"; grep -cP '\x{2013}|\x{2014}' $D/page.html $D/case.json 2>/dev/null; grep -ciE 'm[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er' $D/page.html $D/case.json
