# WEB-FSC-4 attacker two report (freeze 5e25e4783ca950b7274de9a0287245da221b72bc)

Scope: the four items of the attacker-two brief, run against `tree/` (frozen), `base/` (1d48cc2) and the read-only repo `/Users/michalmohelsky/Downloads/wt-web-fsc-4`. All code below is my own and is inlined so it can be rerun. Set first:

```
F=<scratch>/freeze
R=/Users/michalmohelsky/Downloads/wt-web-fsc-4
```

Use `/usr/bin/python3` without `-I` (bs4 sits in the user site-packages; `-I` hides it). Every script only reads.

## Count

| Severity | Count |
|---|---|
| Blocker | 1 |
| Major | 3 |
| Minor | 3 |

1. **F1 BLOCKER (C6):** `case-studies/index.html` still shows the old DSCRs for all four recomputed cases (1.45x RV, 1.50x medical office). The case pages now say 1.52x and 1.57x.
2. **F2 MAJOR (C7):** the dash sweep turned two separate single dashes in back-to-back sentences into one parenthesis that runs across sentence breaks. This happens 29 times on 25 pages. Every word is unchanged, but the punctuation is broken where readers see it.
3. **F3 MAJOR (C6):** the California page's own stated exit ($10.0M) gives a levered IRR of 19.6% to 29.8%, but the page prints "~16%". Florida's own wording conflicts with ~16% the same way. C6's "not recomputable from the pages' inputs" is wrong for California.
4. **F4 MAJOR (C7):** the JSON-LD on `case-studies/index.html` still holds 60 em dashes, written as `—` JSON escapes. Four of them are in the old names of the recomputed cases. The sweep's encoding list does not catch this escape.
5. **F5 MINOR:** on the Florida page, the two debt-service parts ($304k + $164k = $468k) do not add up to the combined line ($469k).
6. **F6 MINOR (C8, item 2):** `research-notes/sba-feasibility-myth` was reworded ("Loan Analytics" became "a loan-data site" and "that site", and "the named firms'" became "the firms'"). None of the allowed explanations covers this. No figure or year changed.
7. **F7 MINOR (C7):** `.gitignore` holds a literal U+2014. That falsifies C7 under its own definition of served (everything except docs/ and src/). The draft returns 404 for `/.gitignore`, and the file belongs to WEB-FSC-5.

Item 3 (sister-property strings outside the hold, plus commit metadata) and item 4 (hand edits to WEB-FSC-6 pages) found nothing. The exact runs are below.

---

## Item 1: the four recomputed cases

### Independent rebuild (no finding; matches the pages)

```
python3 - <<'EOF'
def pmt(P,a,y): r=a/12;n=12*y; return P*r/(1-(1+r)**-n)
def bal(P,a,y,k): r=a/12; m=pmt(P,a,y); return P*(1+r)**k-m*((1+r)**k-1)/r
pages={'AZ':(5.00e6,[382e3,488e3,615e3]),'CA':(6.10e6,[466e3,595e3,750e3]),'FL':(5.80e6,[444e3,567e3,713e3]),'NC':(9.60e6,[0.94e6,1.10e6,1.22e6])}
for k,(C,noi) in pages.items():
    b,d,e=.5*C,.35*C,.15*C; bs,dd=12*pmt(b,.095,25),12*pmt(d,.065,25); t=bs+dd
    print(f'{k}: bank ${b/1e6:.3f}M deb ${d/1e6:.3f}M equity ${e/1e6:.3f}M | DS bank {bs/1e3:.1f}k deb {dd/1e3:.1f}k total {t/1e3:.1f}k '
          f'(rounded parts sum {round(bs/1e3)+round(dd/1e3)}k vs rounded total {round(t/1e3)}k) | DSCR {" / ".join("%.2f"%(n/t) for n in noi)} | 10-yr balance ${(bal(b,.095,25,120)+bal(d,.065,25,120))/1e6:.2f}M')
EOF
```
Output:
```
AZ: bank $2.500M deb $1.750M equity $0.750M | DS bank 262.1k deb 141.8k total 403.9k (rounded parts sum 404k vs rounded total 404k) | DSCR 0.95 / 1.21 / 1.52 | 10-yr balance $3.45M
CA: bank $3.050M deb $2.135M equity $0.915M | DS bank 319.8k deb 173.0k total 492.8k (rounded parts sum 493k vs rounded total 493k) | DSCR 0.95 / 1.21 / 1.52 | 10-yr balance $4.21M
FL: bank $2.900M deb $2.030M equity $0.870M | DS bank 304.0k deb 164.5k total 468.5k (rounded parts sum 468k vs rounded total 469k) | DSCR 0.95 / 1.21 / 1.52 | 10-yr balance $4.00M
NC: bank $4.800M deb $3.360M equity $1.440M | DS bank 503.2k deb 272.2k total 775.5k (rounded parts sum 775k vs rounded total 775k) | DSCR 1.21 / 1.42 / 1.57 | 10-yr balance $6.62M
```

I also checked by hand, and all agree with the pages:
- **Uses tables:** each sums to its total ($5.00M, $6.10M, $5.80M, $9.60M), and sources equal uses.
- **Hero tiles:** each shows 85% (FL: $4.93M of $5.80M).
- **NOI builds:**
  - AZ: GPR $957.6k, EGI $925.0k, NOI $615k.
  - CA: GPR $1.116M, EGI $1.072M, NOI $0.750M, yield on cost 12.3%.
  - FL: GPR $1,148,400, EGI $1,131,000, NOI $713,000, margin 63%.
  - NC: $6.36M less $5.14M is $1.22M.
- **FL break-even:** 469/713 x 93% = 61.2% occupancy, which the page gives as "near 61 percent".
- **NC exit:** $9.5M x 0.97 less $6.62M is $2.60M, which the page gives as "roughly $2.6 million".
- **Descriptions:** meta, og and JSON-LD carry 1.52x / 1.57x, and the four pages have no FAQ block.
- **Tier sentences:** every one matches 13 CFR 120.910.
- **Footnotes:** each `#sN` reference resolves, and the new 120.910 entry is s20 (AZ), s18 (CA) and s14 (FL, NC).
- **Lane scripts:** I copied all four to my scratchpad and ran them with `--check` against the tree. All print OK.
- **NC IRR:** I rebuilt the lane's calibration myself. A payout share of 0.2799 reproduces the base 16.0%; the same share at 50/35/15 gives 12.0%, and a base IRR of 15.5% to 16.5% gives 11.6% to 12.4%. So the 12% holds and nothing else on the NC page contradicts it.

### F1 BLOCKER: stale DSCRs on the case-studies index (C6; a false figure on the site)

Where:
- `case-studies/index.html:1000` (medical office, "a 1.50&times; global DSCR")
- `case-studies/index.html:1187` (California, "a 1.45&times; stabilized DSCR")
- `case-studies/index.html:1484` (Florida, "a 1.45&times; DSCR")
- `case-studies/index.html:1495` (Arizona, "a 1.45&times; DSCR")

These lines are the same in base and tree. The lane changed the case pages but not their cards, and neither the recompute scripts nor DECISIONS mention the index.

The draft serves this file byte for byte: `curl -s https://6ad1f9a4bba14c3fdb9fa372--splendid-cannoli-80c225.netlify.app/case-studies/ | cmp - $F/tree/case-studies/index.html` returns nothing.

```
python3 - "$F" <<'EOF'
import re,sys
F=sys.argv[1]
idx=open(F+'/tree/case-studies/index.html',encoding='utf-8').read().split('\n')
for s in ['rv-boat-storage-arizona-sba','rv-boat-storage-california-sba','rv-boat-storage-florida-sba','medical-office-north-carolina-sba']:
    i=next(i for i,l in enumerate(idx) if f'href="/case-studies/{s}/"' in l)
    j=next(j for j in range(i,i+8) if '<p>' in idx[j])
    card=re.search(r'(\d\.\d\d)&times;',idx[j]).group(1)
    page=open(f'{F}/tree/case-studies/{s}/index.html',encoding='utf-8').read()
    tile=re.search(r'stat-num">(\d\.\d\d)<span>x',page).group(1)
    print(f'{s}: case-studies/index.html:{j+1} card says {card}x; case page hero tile says {tile}x')
EOF
```
Output:
```
rv-boat-storage-arizona-sba: case-studies/index.html:1495 card says 1.45x; case page hero tile says 1.52x
rv-boat-storage-california-sba: case-studies/index.html:1187 card says 1.45x; case page hero tile says 1.52x
rv-boat-storage-florida-sba: case-studies/index.html:1484 card says 1.45x; case page hero tile says 1.52x
medical-office-north-carolina-sba: case-studies/index.html:1000 card says 1.50x; case page hero tile says 1.57x
```
I checked every other page that links to the four cases (26 files, including both hubs, four state pages, the SBA practice area and the mesh blocks). None carries a figure for them; only this index does.

### F3 MAJOR: the held ~16% RV IRR conflicts with the page's own inputs (C6 wording)

Where:
- `case-studies/rv-boat-storage-california-sba/index.html:1274-1276`. The page says a stabilized NOI near $0.75M "at a normalized exit rate around 7.5 percent ... implies a gross value near $10.0 million; net of selling costs and the outstanding SBA 504 balance ... the illustrative levered equity IRR lands in the mid-teens, about 16 percent".
- The same ~16% appears in the hero tile (line 892), the verdict (1282), meta, og and JSON-LD.

With the page's own equity ($0.915M), debt service, 10-year balance and stated exit, and **no distributions at all**, the IRR is 19.6%. With distributions it is 29.8%. To get down to 16% with no distributions, selling costs would have to be about 17.6% of the sale price.

Florida (`rv-boat-storage-florida-sba/index.html:1245-1256`) says the injection "earns a growing levered cash flow ... toward a stabilized cash-on-cash", and that the exit is "disciplined against replacement cost". If that cash is distributed, ~16% needs a sale worth no more than the loan balance. A sale at cost gives 22.3%.

Arizona is not strictly contradicted: an exit at cost with nothing distributed gives 6.5%.

```
python3 - <<'EOF'
def pmt(P,a,y): r=a/12;n=12*y; return P*r/(1-(1+r)**-n)
def bal(P,a,y,k): r=a/12; m=pmt(P,a,y); return P*(1+r)**k-m*((1+r)**k-1)/r
def irr(cf):
    lo,hi=-0.99,5.0
    for _ in range(200):
        m=(lo+hi)/2
        if sum(c/(1+m)**t for t,c in enumerate(cf))>0: lo=m
        else: hi=m
    return m
pages={'AZ':(5.00e6,[382e3,488e3,615e3]),'CA':(6.10e6,[466e3,595e3,750e3]),'FL':(5.80e6,[444e3,567e3,713e3])}
for k,(C,noi) in pages.items():
    b,d,e=.5*C,.35*C,.15*C
    ds=12*(pmt(b,.095,25)+pmt(d,.065,25)); b10=bal(b,.095,25,120)+bal(d,.065,25,120)
    cf=[max(0.0,noi[min(y,3)-1]-ds) for y in range(1,11)]   # Y1 shortfall met by the funded reserve; NOI untrended after Y3
    def at(gross,sell=.03,dist=1.0):
        f=[-e]+[dist*c for c in cf]; f[-1]+=gross*(1-sell)-b10; return irr(f)
    print(f'{k}: equity ${e/1e6:.3f}M, DS ${ds/1e3:.0f}k, 10-yr balance ${b10/1e6:.2f}M')
    print(f'   exit worth only the loan balance (net 0), all cash distributed: {irr([-e]+cf)*100:.1f}%')
    for lab,g in (('exit at cost',C),('exit = Y3 NOI / 8.5% cap',noi[2]/.085),('exit = Y3 NOI / 7.5% cap',noi[2]/.075)):
        print(f'   {lab:28s} ${g/1e6:.2f}M, 3% selling: all distributed {at(g)*100:.1f}% | no distributions at all {at(g,dist=0)*100:.1f}%')
EOF
```
Output (CA's "7.5% cap" line is the page's own stated $10.0M exit):
```
AZ: equity $0.750M, DS $404k, 10-yr balance $3.45M
   exit worth only the loan balance (net 0), all cash distributed: 15.8%
   exit at cost                 $5.00M, 3% selling: all distributed 22.3% | no distributions at all 6.5%
   exit = Y3 NOI / 8.5% cap     $7.24M, 3% selling: all distributed 28.0% | no distributions at all 16.9%
   exit = Y3 NOI / 7.5% cap     $8.20M, 3% selling: all distributed 29.8% | no distributions at all 19.6%
CA: equity $0.915M, DS $493k, 10-yr balance $4.21M
   exit worth only the loan balance (net 0), all cash distributed: 15.8%
   exit at cost                 $6.10M, 3% selling: all distributed 22.3% | no distributions at all 6.5%
   exit = Y3 NOI / 8.5% cap     $8.82M, 3% selling: all distributed 28.0% | no distributions at all 16.9%
   exit = Y3 NOI / 7.5% cap     $10.00M, 3% selling: all distributed 29.8% | no distributions at all 19.6%
FL: equity $0.870M, DS $469k, 10-yr balance $4.00M
   exit worth only the loan balance (net 0), all cash distributed: 15.8%
   exit at cost                 $5.80M, 3% selling: all distributed 22.3% | no distributions at all 6.5%
   exit = Y3 NOI / 8.5% cap     $8.39M, 3% selling: all distributed 28.0% | no distributions at all 16.9%
   exit = Y3 NOI / 7.5% cap     $9.51M, 3% selling: all distributed 29.8% | no distributions at all 19.6%
```
Context:
- The problem predates the lane. At base's 50/40/10, the same California exit gives 35.8%.
- The lane discloses it: DECISIONS item 22 says the pages' inputs give "near 30% or above", and the CA script docstring says about 36%.
- Even so, the page now says "Updated October 16, 2026" next to a new $0.915M injection and still prints ~16%. C6's parenthetical "not recomputable from the pages' inputs" understates this: on California the inputs are enough to show that 16% is wrong.
- Severity is major and not blocker only because the figure is pre-existing and disclosed.

### F5 MINOR: the Florida debt-service rows do not add (C6, "arithmetic that no longer adds up")

Where: `case-studies/rv-boat-storage-florida-sba/index.html:1168-1170`. The rows read "Annual debt service: bank ≈ $304k", "Annual debt service: debenture ≈ $164k", "Combined annual debt service ≈ $469k". So 304 + 164 = 468, not 469.

The exact figures (304,046 + 164,480 = 468,527) round to 469 only as a total. Base was consistent (304 + 188 = 492). Repro: `sed -n 1168,1170p $F/tree/case-studies/rv-boat-storage-florida-sba/index.html`, plus the FL line of the rebuild above ("rounded parts sum 468k vs rounded total 469k"). The other three pages add up (262+142=404, 320+173=493, 503+272=775).

## Item 2: dash sweep fidelity and base-vs-tree rewording

### C7 word sequence on the sweep commit (no finding)

```
python3 - <<'EOF'
import subprocess,re,html
R='/Users/michalmohelsky/Downloads/wt-web-fsc-4'; C='c21b055'
git=lambda *a: subprocess.run(['git','-C',R,*a],capture_output=True).stdout
words=lambda b: re.findall(r'[a-z0-9]+',html.unescape(b.decode('utf-8','replace')).lower())
rows=[l.split('\t') for l in git('show','--name-status','--format=',C).decode().splitlines() if l]
served=[(s,p[-1]) for s,*p in rows if not p[-1].startswith(('docs/','src/'))]
diff=[f for s,f in served if s!='A' and words(git('show',f'{C}^:{f}'))!=words(git('show',f'{C}:{f}'))]
print('served files touched by',C,':',len(served),'| added:',sum(s=='A' for s,f in served),'| word sequence differs:',len(diff),diff[:5])
EOF
```
Output: `served files touched by c21b055 : 150 | added: 0 | word sequence differs: 0 []`.

Entities are decoded first. Without decoding, the only differences are the deleted entity names `mdash` and `ndash`.

### F2 MAJOR: the sweep made parentheses that cross sentence breaks (C7; DECISIONS item 24)

DECISIONS item 24 says "a pair in one sentence becomes commas, or parentheses". The splitter in `docs/web-fsc-4/tools/dashes.py` works like this:
- `visible()` strips tags, so `.<sup><a>9</a></sup> On` becomes `.9 On`.
- `SENT_SPLIT = (?<=[.!?])["”)]?\s+(?=[A-Z...])` needs whitespace straight after the full stop, so it never breaks there.

The result: two single em dashes in back-to-back sentences were treated as one pair and turned into one parenthesis spanning two or three sentences.

Example: `case-studies/glamping-utah-usda/index.html:1195`.
- **Base:** "...guarantee to the lender is 70 percent — 80 percent applies ... B&I ceiling.⁹ On a 25-year amortization ..., annual debt service is about $609,000 — the number the projected coverage has to clear."
- **Tree:** "...is 70 percent (80 percent applies ... B&I ceiling.⁹ On a 25-year amortization ..., annual debt service is about $609,000) the number the projected coverage has to clear."

The same defect is on `case-studies/rv-boat-storage-california-sba/index.html:965-974`, a recomputed case. There, "(RVIA's 2025 Go RVing profile ..." opens a parenthesis that closes three sentences later at "reinforce it) Los Angeles and San Jose".

Repro (prints file:line and the span; it skips held pages and spans already present in base):
```
python3 - "$F/base" "$F/tree" <<'EOF'
import os,re,sys,json
from bs4 import BeautifulSoup
B,T=sys.argv[1],sys.argv[2]
hold=[h.rstrip('*') for h in json.load(open(os.path.join(T,'data/site/hold.json')))['pages']]
ABBR=re.compile(r'\b(?:e\.g|i\.e|U\.S|St|No|Inc|Co|vs|Ill|Adm)\.\s')
def blocks(p):
    s=BeautifulSoup(open(p,encoding='utf-8').read(),'lxml')
    for t in s(['script','style']): t.decompose()
    return [re.sub(r'\s+',' ',el.get_text('')).strip() for el in s.find_all(['p','li','td','figcaption','caption','dd','blockquote']) if not el.find(['p','li','td','div'])]
def spans(t):
    st=[];out=[]
    for i,c in enumerate(t):
        if c=='(': st.append(i)
        elif c==')' and st: out.append(t[st.pop():i+1])
    return out
n=0;pages=set()
for dp,dn,fn in sorted(os.walk(T)):
    rel=os.path.relpath(dp,T)
    if rel.split(os.sep)[0] in ('docs','src') or any(rel.startswith(h.rstrip('/')) for h in hold): continue
    for f in sorted(fn):
        if not f.endswith('.html'): continue
        r=os.path.normpath(os.path.join(rel,f)); bp=os.path.join(B,r)
        if not os.path.exists(bp): continue
        btxt=' '.join(blocks(bp))
        for blk in blocks(os.path.join(T,r)):
            for s in spans(blk):
                m=re.search(r'[a-z0-9%)\]][.!?]\d*\s+[A-Z]',ABBR.sub(' ',s[1:-1]))
                if m and s not in btxt and not re.search(r'\d\.\d',m.group(0)):
                    n+=1; pages.add(r); print(f'{r}: {s[:140]}...')
print(f'TOTAL {n} sentence-spanning parentheses on {len(pages)} pages')
EOF
```
The output ends `TOTAL 28 sentence-spanning parentheses on 24 pages`. A 29th, `case-studies/multifamily-arizona-agency/index.html:1132`, is dropped by the decimal filter because ".151" follows "2024", so I confirmed it by hand. Base reads "in-migration — the Phoenix–Mesa–Chandler MSA reached ... 2024.¹⁵¹ Two Arizona-specific factors ... water-gated fringe — which the next section"; the tree turns that into "(the Phoenix-Mesa-Chandler MSA reached ... water-gated fringe) which".

Opening lines in the tree, where `case-studies/` is shortened to `cs/`:

| Page | Line(s) of the opening "(" |
|---|---|
| cs/assisted-living-arizona-hud | 1071 |
| cs/assisted-living-california-hud | 1184 |
| cs/childcare-illinois-sba | 1080 |
| cs/coffee-shop-washington-sba | 969 |
| cs/fitness-minnesota-sba | 1191 |
| cs/funeral-home-wisconsin-sba | 1077 |
| cs/glamping-utah-usda | 1195 |
| cs/hotel-south-carolina-sba | 1188 |
| cs/marina-maryland-sba | 1071 |
| cs/meat-processing-georgia-usda | 1202 |
| cs/meat-processing-north-carolina-usda | 1309 |
| cs/multifamily-arizona-agency | 1132 |
| cs/multifamily-florida-agency | 1186 |
| cs/multifamily-new-york-agency | 970 |
| cs/multifamily-north-carolina-agency | 1079, 1191 |
| cs/qsr-arkansas-sba | 1060 |
| cs/qsr-georgia-sba | 964, 1064, 1178 |
| cs/restaurant-missouri-sba | 1182 |
| cs/rv-boat-storage-california-sba | 965 |
| cs/rv-park-maine-usda | 969, 1189 |
| cs/truck-stop-georgia-sba | 1032 |
| states/georgia | 1084 |
| states/maryland | 1053 |
| states/mississippi | 923 |
| states/nevada | 1102 |

No held page is affected. The word-sequence half of C7 stays true; the "pair in one sentence" rule in DECISIONS item 24 does not.

### F4 MAJOR: 60 em dashes left in served JSON-LD (C7)

Where: `case-studies/index.html:684-743`, the CollectionPage `hasPart` names, for example `"Gas Station Feasibility Study, Texas — An SBA 7(a) Worked Case"`.

`tools/dashes.py:29` defines `EM = r"(?:—|&mdash;|&#8212;|&#x2014;|&#X2014;)"`, which does not include the JSON escape `—`. Every JSON-LD parser reads it as U+2014. The 60 entries include the old em dash names of the four recomputed cases and of every other case. The pages themselves now use the colon form, so these names are stale too.

`scripts/mesh.py:59` also holds `—` and `–` inside a regex, and `/scripts/mesh.py` answers 200 on the draft. That one is code, but it is the same blind spot.

```
python3 - "$F" <<'EOF'
import json,re,sys
t=open(sys.argv[1]+'/tree/case-studies/index.html',encoding='utf-8').read()
blocks=re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)
def walk(o):
    if isinstance(o,dict):
        for v in o.values(): yield from walk(v)
    elif isinstance(o,list):
        for v in o: yield from walk(v)
    elif isinstance(o,str): yield o
names=[s for b in blocks for s in walk(json.loads(b)) if '—' in s]
print('raw "\\u2014" escapes:',t.count('\\u2014'),'| parsed JSON-LD strings containing U+2014:',len(names))
for n in names:
    if re.search('RV & Boat Storage Feasibility Study, (Arizona|California|Florida)|Medical Office',n): print('  ',n)
EOF
```
Output:
```
raw "—" escapes: 60 | parsed JSON-LD strings containing U+2014: 60
   Medical Office & ASC Feasibility Study, North Carolina — An SBA 504 Worked Case
   RV & Boat Storage Feasibility Study, California — An SBA 504 Worked Case
   RV & Boat Storage Feasibility Study, Florida — An SBA 504 Worked Case
   RV & Boat Storage Feasibility Study, Arizona — An SBA 504 Worked Case
```
Base has the same 60 escapes, so the sweep never touched them.

This arguably makes C7 false in substance. I rate it major, not blocker, because readers see it only through structured data.

### F7 MINOR: `.gitignore` U+2014 (C7 as worded)

`.gitignore` holds a literal U+2014: "# Draft page uploads — integrated into the site at their canonical paths". C7 defines "served = everything in the tree except docs/ and src/", so the claim is false as written. In practice:
- `curl -s -o /dev/null -w '%{http_code}' https://6ad1f9a4bba14c3fdb9fa372--splendid-cannoli-80c225.netlify.app/.gitignore` returns 404.
- The charter gives `.gitignore` to WEB-FSC-5. Its last commit is db9d9be, which predates the lane.
- So this is a wording defect in the claim, not a defect on the site.

### Base vs tree: pages whose words changed outside generated regions

Method:
- Remove `<!--chrome:*-->` and `<!--mesh:*-->` regions and the `<!--fsc:byline-article-->` region.
- Unwrap `<a data-fsc-term>`.
- Drop `header.site-header` and `footer.site-footer`. In-page `<nav>` is kept.
- Compare the words of title, meta descriptions and titles, and body.
- The four recomputed cases are excluded; I reviewed them separately, and every changed word there is a financing figure, the tier sentence, the 120.910 source, the disclosure box or the "analytics.loan and" relabel.

```
python3 - "$F" <<'EOF'
import os,re,html,difflib,sys,collections
from bs4 import BeautifulSoup, Comment
F=sys.argv[1]; B,T=F+'/base',F+'/tree'
REG=re.compile(r'<!--(chrome|mesh):([a-z-]+)-->.*?<!--/\1:\2-->|<!--fsc:byline-article.*?<!--/fsc:byline-article-->',re.S)
W=lambda x: re.findall(r'[a-z0-9]+',html.unescape(x).lower())
def body(src):
    s=BeautifulSoup(REG.sub(' ',src),'lxml')
    for a in s.find_all('a',attrs={'data-fsc-term':True}): a.unwrap()
    head=' '.join([s.title.get_text() if s.title else '']+[m['content'] for m in s.find_all('meta') if m.get('content') and (m.get('name') or m.get('property') or '') in ('description','og:description','twitter:description','og:title','twitter:title')])
    for t in s.find_all(['header','footer'],class_=['site-header','site-footer'])+s(['script','style','head']): t.decompose()
    for c in s.find_all(string=lambda x:isinstance(x,Comment)): c.extract()
    return W(head)+['|BODY|']+W(s.get_text(' '))
FOUR=('rv-boat-storage-arizona-sba','rv-boat-storage-california-sba','rv-boat-storage-florida-sba','medical-office-north-carolina-sba')
BOX='representative worked example the site sponsor and project are hypothetical the market evidence comes from the public sources listed below with their dates this page shows how the market analysis is built and how it sets the loan it is not a client engagement'
cat=collections.defaultdict(list)
for dp,dn,fn in os.walk(T):
    rel=os.path.relpath(dp,T)
    if rel.split(os.sep)[0] in ('docs','src'): continue
    for f in fn:
        r=os.path.normpath(os.path.join(rel,f))
        if not f.endswith('.html') or not os.path.exists(os.path.join(B,r)) or any(x in r for x in FOUR): continue
        a,b=body(open(os.path.join(B,r),encoding='utf-8').read()),body(open(os.path.join(T,r),encoding='utf-8').read())
        for t,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
            if t=='equal': continue
            o,n=' '.join(a[i1:i2]),' '.join(b[j1:j2])
            if n==BOX and not o: k='disclosure box'
            elif re.search(r'mmcg|innowave|analytics|loan analytics|consultant com',o) and n in ('industry research','an industry','industry',''): k='relabel to industry research / drop'
            elif o.startswith('worked case'): k='hand list replaced by mesh region'
            elif 'composite of the assisted living' in o: k='removed contradicting sentence (NC assisted living)'
            elif n=='six markets': k='Hawaii heading'
            elif 'truck-stop-oklahoma' in r and not o: k='truck stop Oklahoma title fix'
            else: k='UNEXPLAINED'
            cat[k].append((r,o[:120],n[:120]))
for k,v in cat.items():
    print(f'{k}: {len(v)} edits on {len(set(x[0] for x in v))} pages')
    if k=='UNEXPLAINED':
        for x in v: print('   ',x)
    if k.startswith('relabel'): print('    digits inside any relabel edit:',[x for x in v if re.search(r'\d',x[1]+x[2])])
EOF
```
Output:
```
relabel to industry research / drop: 30 edits on 19 pages
    digits inside any relabel edit: []
UNEXPLAINED: 6 edits on 1 pages
    ('research-notes/sba-feasibility-myth/index.html', '', 'a')
    ('research-notes/sba-feasibility-myth/index.html', 'analytics', 'data site')
    ('research-notes/sba-feasibility-myth/index.html', 'loan analytics', 'that site')
    ('research-notes/sba-feasibility-myth/index.html', 'named', '')
    ('research-notes/sba-feasibility-myth/index.html', '', 'a')
    ('research-notes/sba-feasibility-myth/index.html', 'analytics analytics loan', 'data site')
truck stop Oklahoma title fix: 1 edits on 1 pages
hand list replaced by mesh region: 5 edits on 5 pages
disclosure box: 44 edits on 44 pages
removed contradicting sentence (NC assisted living): 1 edits on 1 pages
Hawaii heading: 1 edits on 1 pages
```
Notes on the explained groups:
- The five "hand list replaced by mesh region" pages are the glamping, marina and rv-park-and-campground hubs and the Florida and New Hampshire state pages. A hand-written Worked cases list was removed and a mesh region now lists the cases. I checked that every `/case-studies/` link the base had is still present in the tree, and none is missing.
- No relabel changed a digit, so no figure or year changed.
- JSON-LD only gained `dateModified` (61 pages at 2026-10-10 plus a few others), the truck stop's revived block, and a WebPage node on `practice-areas/`.

### F6 MINOR: reworded citation on `research-notes/sba-feasibility-myth` (C8, item 2)

Where: tree lines 1218, 1219 and 1284. "Loan Analytics" became "a loan-data site" and "that site"; "Loan Analytics (analytics.loan)" became "a loan-data site"; "from the named firms' own pages" became "from the firms' own pages".

This is neither "industry research" nor a primary source, which is what C8 promises, and it is not in the allowed list. No figure or year changed.

```
python3 - "$F" <<'EOF'
import re,sys
for v in ('base','tree'):
    t=open(f'{sys.argv[1]}/{v}/research-notes/sba-feasibility-myth/index.html',encoding='utf-8').read()
    txt=re.sub(r'\s+',' ',re.sub(r'<[^>]+>','',t))
    for m in re.finditer(r'[^.]*(Loan Analytics|loan-data site|that site further|named firms|the firms\' own)[^.]*\.',txt):
        print(v.upper()+':',m.group(0).strip()[:230])
EOF
```
Output (abridged):
```
BASE: The first is a misquoted regulation: several high-ranking pages, including that of Loan Analytics, reproduce a version of section 120.
BASE: 160 that does not match the current eCFR, ...; Loan Analytics further frames a study as a "de facto requirement" ...
BASE: Public marketing statements ... are quoted or paraphrased from the named firms' own pages: Loan Analytics (analytics.
TREE: ... several high-ranking pages, including that of a loan-data site, reproduce a version of section 120.
TREE: 160 that does not match the current eCFR, ...; that site further frames a study as a "de facto requirement" ...
TREE: Public marketing statements ... are quoted or paraphrased from the firms' own pages: a loan-data site, Peak Business Valuation (peakbusinessvaluation.
```

## Item 3: sister-property and Wert-Berater strings (nothing outside the hold)

Every file under `tree/` except `docs/` and `src/` was scanned: 186 files, including scripts/*.py, data/**/*.json, README.md, sitemap.xml, feed.xml, robots.txt, netlify.toml, .gitignore and `db7ea828330340f8994ca82a16c48c8b.txt`. `.ghtoken` was not opened. Each file was checked three ways:
1. the exact C8 pattern, case-insensitive;
2. after decoding entities twice, URL-decoding, removing zero-width and soft-hyphen characters and deleting every non-alphanumeric character, a search for `mmcg`, `mohelsk`, `unionmetric`, `innowav`, `analyticsloan`, `analyticsdotloan`, `loananalytic`, `wertberat`, `feasibilitystudyconsultant(com|dot)`; this catches "M M C G", `mmcg&#x2d;`, "Wert Berater", "analytics dot loan", "loananalytics" and similar;
3. a lookalike-letter check (Cyrillic м/с) and a check of file and folder names.

```
python3 - "$F/tree" <<'EOF'
import os,re,json,html,sys,urllib.parse
T=sys.argv[1]
hold=[h.rstrip('*') for h in json.load(open(T+'/data/site/hold.json'))['pages']]
P=re.compile(r'm[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er',re.I)
V=['mmcg','mohelsk','unionmetric','innowav','analyticsloan','analyticsdotloan','loananalytic','wertberat','feasibilitystudyconsultantcom','feasibilitystudyconsultantdot']
n=0
for dp,dn,fn in os.walk(T):
    rel=os.path.relpath(dp,T)
    if rel.split(os.sep)[0] in ('docs','src'): continue
    for f in fn+dn:
        if re.search(r'mmcg|mohelsk|union.?metric|innowave|analytics.?loan|loan.?analytic|wert',f,re.I): print('NAME',rel,f)
    for f in fn:
        if f=='.ghtoken': continue
        r=os.path.normpath(os.path.join(rel,f)); n+=1
        tag='[HELD] ' if any(r.startswith(h) for h in hold) else ''
        t=open(os.path.join(dp,f),'rb').read().decode('utf-8','replace')
        for m in P.finditer(t): print('PATTERN',tag+r,t.count('\n',0,m.start())+1,repr(t[m.start()-30:m.end()+20]))
        d=re.sub('[​-‏­⁠﻿]','',urllib.parse.unquote(html.unescape(html.unescape(t))).lower())
        norm=re.sub(r'[^a-z0-9]','',d)
        hits=[v for v in V if v in norm]
        if hits: print('VARIANT',tag+r,hits)
        if re.search(r'[Ѐ-ӿ][mм]?[cс][gɡ]|[mм][Ѐ-ӿ][cс]',d): print('LOOKALIKE',tag+r)
print('files scanned',n)
EOF
```
Result: `files scanned 186`. Every hit is on a held (WEB-FSC-6) page, so none of them is a finding:

| Held page | Line | String |
|---|---|---|
| `asset-classes/gas-station-and-c-store/index.html` | 1409 | "Innowave Studio" |
| `asset-classes/gas-station-and-c-store/index.html` | 1415 | "analytics.loan" |
| `case-studies/rv-boat-storage-texas-sba/index.html` | 1365, 1366 | "analytics.loan" |
| `case-studies/rv-park-texas-usda/index.html` | 1353 | "Loan Analytics / MMCG and Innowave Studio" |
| `case-studies/assisted-living-texas-hud/index.html` | 1215, 1357 | "Janover/MMCG", "Janover Pro and MMCG" |

My first run used a looser `feasibilitystudyconsultant` probe. It also flagged `index.html:791/1639`, which is the generic FAQ phrase "What does a feasibility study consultant do?" and not a domain. The run above excludes it.

Commit metadata: I dumped author, committer and full message (body and trailers) for all 8 commits in `1d48cc2..5e25e47` and applied the same pattern plus the same normalized variants:

```
git -C $R log --format='%H%n%an <%ae>%n%cn <%ce>%n%B%n----' 1d48cc2..5e25e47 | python3 -c "
import sys,re;t=sys.stdin.read()
P=re.compile(r'm[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er',re.I)
n=re.sub(r'[^a-z0-9]','',t.lower())
print('pattern hits',P.findall(t),'variants',[v for v in ['mmcg','mohelsk','unionmetric','innowave','analyticsloan','analyticsdotloan','loananalytic','feasibilitystudyconsultant','wertberat'] if v in n])"
```
Output: `pattern hits [] variants []`. Every commit's author and committer is "Feasibility Study Company <noreply@feasibility-study-company.com>", and the only trailer is "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>".

## Item 4: hand edits to WEB-FSC-6 pages (nothing found)

```
cd $F && python3 - <<'EOF'
import json,os,filecmp,subprocess
hold=json.load(open('tree/data/site/hold.json'))['pages']
files=set()
for root in ('tree','base'):
    for h in hold:
        for dp,dn,fn in os.walk(os.path.join(root,h.rstrip('*'))):
            files|={os.path.relpath(os.path.join(dp,f),root) for f in fn}
print('held files',len(files),'| differ base vs tree:',[f for f in sorted(files) if not (os.path.exists('tree/'+f) and os.path.exists('base/'+f) and filecmp.cmp('tree/'+f,'base/'+f,shallow=False))])
out=subprocess.run(['git','-C','/Users/michalmohelsky/Downloads/wt-web-fsc-4','log','--format=','--name-only','1d48cc2..5e25e47'],capture_output=True,text=True).stdout.split()
print('held paths touched by any lane commit:',[p for p in out if any(p.startswith(h.rstrip('*')) for h in hold)])
EOF
git -C $R log --format='%h %s' --name-status 1d48cc2..5e25e47 -- src scripts/build.py scripts/casemodel.py data/cases data/markets .gitignore
```
Output:
```
held files 14 | differ base vs tree: []
held paths touched by any lane commit: []
```
The second command prints nothing. The hold list in `tree/data/site/hold.json` matches the charter's WEB-FSC-6 list exactly: 14 entries (states/texas, the gas station hub and twelve cases).

## Observations, not counted

- **Medical office tier basis.** Line 1189 rests the 15% on "the operating company is the established physician group (more than two years in operation)". The same page says "a new surgery center does not stabilize on day one. A start-up practice line ramps over two to four years" (line 1265) and has an "ASC ramp / credentialing" Year 1. If the physician-owned ASC entity is the Operating Company, 13 CFR 120.910 puts it at 20%. The page states its assumption, so I do not count this; the owner should confirm.
- **RV storage hub wording.** `asset-classes/rv-and-boat-storage/index.html` (visible FAQ and JSON-LD FAQ) says "a start-up or an Initial Acquisition needs a 10 percent equity injection" in a sentence about SBA generally. Its own table row gives the 504 tiers correctly (10/15/20). It is outside the four pages and not part of the recompute.
- **Draft serves scripts.** The draft serves `/scripts/*.py` (200 for `/scripts/mesh.py`). C3 says only `/docs/*` and `/src/*` 404, so this is consistent with the claims; noted for the owner.

## Files

This file is the only file I leave behind. I ran my helper scripts from a scratch folder `scratchpad/a2/` (copies of the lane's recompute scripts, run with `--check --page` against the tree, plus my own checks). That folder is deleted after this report is written, and every script needed to reproduce a finding is inlined above. Nothing in `tree/`, `base/` or the repo was written.
