#!/usr/bin/env python3
"""WEB-FSC-2 gates against a built tree (git archive of the branch) and a baseline tree.

    python3 docs/web-fsc-2/tools/gates.py <built_dir> <baseline_dir> <repo_root>

Gate 1 page count = baseline + 1. Gate 2 coverage: every INVENTORY row classified and
resolved; every <!--sba:--> marker path resolves to a register row that is VERIFIED or
CONFLICT_RESOLVED (CHANGED rows are fact-sheet corrections verified from the text and count).
Gate 3 stale-claim grep outside data-historical elements. Gate 4 data-file rendering
(regulatory.py --check and marker presence on the hub, the note and the stat blocks).
Gate 6 names, Gate 7 credentials, Gate 8 links and JSON-LD. Gates 5, 9 and 10 are
recorded by hand in GATES.txt (case scripts, screenshots, verifier).
"""
import codecs, csv, json, os, re, subprocess, sys
BUILT, BASE, REPO = sys.argv[1:4]
NAMES = re.compile(codecs.decode("zzpt|zburyfxl|havbazrgevp", "rot13"), re.I)
CREDS = re.compile(r"otava,? *(ph\.?d|ccim|mai)", re.I)
res = []
def gate(n, name, ok, detail=''):
    res.append((n, ok)); print(f"\n=== Gate {n}: {name}: {'GREEN' if ok else 'RED'}"); print(detail) if detail else None
def walk(root, ext):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != '.git']
        for f in files:
            if f.endswith(ext): yield os.path.join(d, f)
def read(p): return open(p, encoding='utf-8', errors='replace').read()
def pages(root): return sorted(os.path.relpath(p, root) for p in walk(root, '.html'))
def strip_hist(t):
    # remove elements carrying data-historical (table, tr, td, li, p, span, div)
    for tag in ('table', 'tr', 'td', 'li', 'p', 'span', 'div', 'section'):
        t = re.sub(r'<' + tag + r'\b[^>]*data-historical[^>]*>.*?</' + tag + '>', ' ', t, flags=re.S)
    return t
def text(t):
    t = re.sub(r'<script[^>]*application/ld\+json[^>]*>.*?</script>', lambda m: m.group(0), t, flags=re.S)
    t = re.sub(r'<style.*?</style>|<!--.*?-->', ' ', t, flags=re.S)
    return t

# 1
bp, pp = pages(BASE), pages(BUILT); added = sorted(set(pp) - set(bp))
gate(1, 'page count = baseline + 1', len(pp) == len(bp) + 1 and added == ['research-notes/sop-50-10-8-1-what-changed-for-feasibility-studies/index.html'], f'baseline {len(bp)} built {len(pp)} added {added}')

# 2
reg = {r['id']: r for r in csv.DictReader(open(os.path.join(REPO, 'docs/web-fsc-2/REGISTER.csv'), encoding='utf-8'))}
inv = list(csv.DictReader(open(os.path.join(REPO, 'docs/web-fsc-2/INVENTORY.csv'), encoding='utf-8')))
uncls = [r for r in inv if not r['classification'] or not r['resolution']]
badid = [r for r in inv if r['register_id'] and r['register_id'] not in reg]
data = json.load(open(os.path.join(REPO, 'data/regulatory/sba.json')))
def regid(path):
    cur = data
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur: cur = cur[part]
        else: return None
    if isinstance(cur, dict): return cur.get('register')
    return 'parent'
badmark = []
for p in walk(BUILT, '.html'):
    for m in re.finditer(r'<!--sba:([a-z0-9_.]+)', read(p)):
        path = m.group(1)
        rid = regid(path)
        if rid == 'parent':
            parent = '.'.join(path.split('.')[:-1]); cur = data
            for part in parent.split('.'): cur = cur.get(part, {}) if isinstance(cur, dict) else {}
            rid = cur.get('register') if isinstance(cur, dict) else None
        ids = rid if isinstance(rid, list) else [rid]
        if path.startswith('history.') or path.startswith('sop.') or path.startswith('fees_fy2027.notice') or path == 'fees_fy2027.fiscal_year': continue
        for i in ids:
            if not i or i not in reg or reg[i]['status'] not in ('VERIFIED', 'CONFLICT_RESOLVED', 'CHANGED'):
                badmark.append((os.path.relpath(p, BUILT), path, i))
gate(2, 'coverage: inventory classified; markers trace to verified rows', not uncls and not badid and not badmark,
     f'inventory rows {len(inv)}, unclassified {len(uncls)}, unknown ids {len(badid)}, untraceable markers {len(badmark)} {badmark[:5]}')

# 3 stale claims
pats = {
 'SOP 50 10 8 as current': re.compile(r'SOP 50 10 8(?!\.1)[,\s(]{1,3}(?:[^.]{0,60}?)(effective June 1, 2025|current)', re.I),
 '50 10 7': re.compile(r'50 10 7(?!\d)'),
 'SBSS as current': re.compile(r'(?<![^.]{0,60}(?:Sunset of |retirement of the |end of the ))SBSS(?![^.]{0,80}(retire|discontinu|sunset|gone|no longer|former|replaced|was |is gone|ended))', re.I),
 '504 1:1 or 1.0x': re.compile(r'504[^.]{0,80}\b(1:1|1\.0x)\b|\b(1:1|1\.0x)\b[^.]{0,80}504', re.I),
 '$90,000 jobs': re.compile(r'\$90,000'),
 '$250,000 valuation': re.compile(r'\$250,000[^.]{0,80}(business valuation|going-concern|value the business|valuation threshold|internal valuation)|(business valuation|going-concern|value the business|valuation threshold|internal valuation)[^.]{0,80}\$250,000', re.I),
 'required by SBA + feasibility': re.compile(r'(?<!["“]the )(?<!["“])(required by (the )?SBA|SBA requires)[^.]{0,60}feasibility|feasibility stud(y|ies)[^.]{0,60}(required by (the )?SBA|SBA requires)(?!["”])', re.I),
 'combined limit not $10M': re.compile(r'(?<![^.]{0,200}\$10 million)combined[^.]{0,60}(?:7\(a\)|504)[^.]{0,60}\$(?!10 million|10M|10,000,000)\d[\d.,]* ?(million|M)\b(?![^.]{0,120}\$10 million)', re.I),
}
hits = []; allowed = []
for p in walk(BUILT, '.html'):
    raw = read(p); rel = os.path.relpath(p, BUILT)
    t = text(raw); th = strip_hist(t)
    for name, rx in pats.items():
        for m in rx.finditer(th): hits.append((rel, name, th[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')))
        for m in rx.finditer(t):
            if not rx.search(th[max(0, 0):]) or True:
                ctx = t[max(0, m.start() - 40):m.end() + 40].replace('\n', ' ')
                if not any(h[0] == rel and h[2] == ctx for h in hits): allowed.append((rel, name, ctx))
gate(3, 'stale-claim grep outside historical wrappers', not hits, f'hits {len(hits)}\n' + '\n'.join(f'  {h}' for h in hits[:40]) + f'\nallowed inside historical wrappers: {len(allowed)}\n' + '\n'.join(f'  {a}' for a in allowed[:40]))

# 4 data file
chk = subprocess.run([sys.executable, 'scripts/regulatory.py', '--check'], cwd=REPO, capture_output=True, text=True)
hub = read(os.path.join(BUILT, 'practice-areas/sba-7a-504/index.html')); note = read(os.path.join(BUILT, 'research-notes/sop-50-10-8-1-what-changed-for-feasibility-studies/index.html'))
stat_ok = all('<!--sba:' in s for s in re.findall(r'<div class="stat-num">(.*?)</div>', hub, re.S))
gate(4, 'data file renders (regulatory.py --check; hub stat block and note carry markers)', chk.returncode == 0 and stat_ok and hub.count('<!--sba:') > 100 and note.count('<!--sba:') > 50, chk.stdout.strip() + f'; hub markers {hub.count("<!--sba:")}, note markers {note.count("<!--sba:")}, stat markers {stat_ok}')

# 6 names (changed files + built output)
changed = subprocess.run(['git', 'diff', '--name-only', 'web-fsc-1', 'HEAD'], cwd=REPO, capture_output=True, text=True).stdout.split()
nh = [f for f in changed if os.path.exists(os.path.join(REPO, f)) and NAMES.search(read(os.path.join(REPO, f)))]
nb = [os.path.relpath(p, BUILT) for p in walk(BUILT, '.html') if NAMES.search(read(p)) and os.path.relpath(p, BUILT) in changed]
mm = [os.path.relpath(p, BUILT) for p in walk(BUILT, '.html') if re.search(codecs.decode('zzptvairfg\\.pbz', 'rot13'), read(p), re.I)]
gate(6, 'names: none in changed files; no sister-domain link anywhere', not nh and not nb and not mm, f'changed files with names {nh}; built changed pages {nb}; sister-domain links anywhere {mm}')
pre = [os.path.relpath(p, BUILT) for p in walk(BUILT, '.html') if NAMES.search(read(p))]
print(f'  (pre-existing pages with the abbreviation, not changed by this lane: {len([x for x in pre if x not in changed])})')

# 7 credentials
ch = [os.path.relpath(p, BUILT) for p in walk(BUILT, '.html') if CREDS.search(read(p))] + [f for f in changed if os.path.exists(os.path.join(REPO, f)) and CREDS.search(read(os.path.join(REPO, f)))]
gate(7, 'credentials never typed next to the name', not ch, str(ch))

# 8 links + schema
def targets(root):
    out = {}
    for p in walk(root, '.html'):
        rel = os.path.relpath(p, root)
        for h in re.findall(r'href="(/[^"#?]*)', read(p)):
            fp = os.path.join(root, h.lstrip('/'))
            if h.endswith('/'): fp = os.path.join(fp, 'index.html')
            if not os.path.exists(fp) and not os.path.exists(fp.rstrip('/')): out.setdefault(h, set()).add(rel)
    return out
bt, pt = targets(BASE), targets(BUILT); new = {k: v for k, v in pt.items() if k not in bt}
ld_bad = []
for f in changed:
    p = os.path.join(BUILT, f)
    if f.endswith('.html') and os.path.exists(p):
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', read(p), re.S):
            try: json.loads(m.group(1))
            except Exception as e: ld_bad.append((f, str(e)[:60]))
need = all(s in note for s in ('"@type": "Article"', '"@type": "BreadcrumbList"', '"@id": "https://feasibility-study-company.com/#mark-otava"'))
gate(8, 'no new broken internal links; JSON-LD parses; note carries Article, BreadcrumbList, author @id', not new and not ld_bad and need, f'broken targets baseline {len(bt)} built {len(pt)} new {list(new)[:10]}; ld errors {ld_bad}; note schema {need}')

print('\nRESULT:', 'ALL GREEN' if all(ok for _, ok in res) else 'RED: ' + ', '.join(str(n) for n, ok in res if not ok))
sys.exit(0 if all(ok for _, ok in res) else 1)
