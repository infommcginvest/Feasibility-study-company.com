#!/usr/bin/env python3
"""WEB-FSC-2 inventory: every SBA statement in the served pages.

Scans the tracked .html files (not docs/) for the charter's patterns. A hit
counts when the pattern is SBA-specific, or when a generic pattern (DSCR,
1.15, occupancy, 25 years ...) sits in a line or table row that names SBA,
the SOP, 7(a), 504 or a CDC. Writes docs/web-fsc-2/INVENTORY.csv with a
provisional REGISTER id per row (the cluster review confirms or changes it).

    python3 docs/web-fsc-2/tools/inventory.py
"""
import csv, html, os, re, subprocess, sys
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'docs', 'web-fsc-2', 'INVENTORY.csv')
files = [f for f in subprocess.check_output(['git', 'ls-files', '*.html'], cwd=ROOT, text=True).split('\n') if f and not f.startswith('docs/')]

SBA_CTX = re.compile(r'\bSBA\b|SOP\s*50\s*10|7\(a\)|\b504\b|\bCDC\b|guarant', re.I)
# (category, regex, sba_specific, provisional register id)
PATTERNS = [
 ('version', re.compile(r'SOP\s*50\s*10(?:\s*8(?:\.1)?|\s*7(?:\.1)?)?', re.I), True, 'R01'),
 ('version', re.compile(r'\b50 10 [78]\b'), True, 'R01'),
 ('version', re.compile(r'June 1, 2025|1 June 2025|Jun(?:e)? 2025', re.I), True, 'R04'),
 ('version', re.compile(r'Appendix 15', re.I), True, 'R08'),
 ('version', re.compile(r'change[- ]of[- ]ownership', re.I), False, 'R08'),
 ('version', re.compile(r'\bSBSS\b'), True, 'R27'),
 ('version', re.compile(r'\bPeg\b'), True, 'R46'),
 ('coverage', re.compile(r'\bDSCR\b|debt[- ]service coverage', re.I), False, 'R28'),
 ('coverage', re.compile(r'\b1\.15\s*(?:x|:1|:1\.0|×)?'), False, 'R28'),
 ('coverage', re.compile(r'\b1\.25\s*(?:x|:1|×)?'), False, 'R09'),
 ('coverage', re.compile(r'\b1\.10\s*(?:x|:1|×)?'), False, 'R27'),
 ('coverage', re.compile(r'\b1:1\b|\b1\.0x\b'), False, 'R30'),
 ('equity', re.compile(r'equity injection', re.I), True, 'R13'),
 ('equity', re.compile(r'\binjection\b', re.I), False, 'R13'),
 ('equity', re.compile(r'\bstandby\b', re.I), True, 'R15'),
 ('equity', re.compile(r'\bearn-?out', re.I), True, 'R18'),
 ('equity', re.compile(r'quality of earnings|\bQoE\b', re.I), True, 'R23'),
 ('property', re.compile(r'special[- ]purpose|special[- ]use|limited[- ]purpose', re.I), False, 'R44'),
 ('property', re.compile(r'going[- ]concern', re.I), False, 'R21'),
 ('property', re.compile(r'\$250,000'), False, 'R21'),
 ('property', re.compile(r'\$350,000'), False, 'R21'),
 ('programs', re.compile(r'7\(a\) Small', re.I), True, 'R26'),
 ('programs', re.compile(r'SBA Express|\bExpress loan', re.I), True, 'R26'),
 ('programs', re.compile(r'\$5 million|\$5\.0 million|\$5,000,000', re.I), False, 'R38'),
 ('programs', re.compile(r'\$5\.5(?: million)?|\$5,500,000', re.I), False, 'R38'),
 ('programs', re.compile(r'\$10 million|\$10,000,000|\$10M\b', re.I), False, 'R38'),
 ('programs', re.compile(r'\btransient', re.I), False, 'R42'),
 ('programs', re.compile(r'30 days', re.I), False, 'R42'),
 ('programs', re.compile(r'owner[- ]occupan|\boccupancy\b', re.I), False, 'R32'),
 ('programs', re.compile(r'\b51\s?%|51 percent', re.I), False, 'R32'),
 ('programs', re.compile(r'\b60\s?%|60 percent', re.I), False, 'R32'),
 ('terms', re.compile(r'amortiz', re.I), False, 'R25'),
 ('terms', re.compile(r'\bmaturity\b', re.I), False, 'R33'),
 ('terms', re.compile(r'25[- ]years?', re.I), False, 'R33'),
 ('terms', re.compile(r'10[- ]years?', re.I), False, 'R25'),
 ('terms', re.compile(r'\bjobs?\b', re.I), False, 'R37'),
 ('terms', re.compile(r'\$90,000'), False, 'R37'),
 ('terms', re.compile(r'\$95,000'), False, 'R37'),
 ('terms', re.compile(r'guarant(?:y|ee) fee|upfront fee|up-front fee', re.I), True, 'R49'),
 ('terms', re.compile(r'120 days', re.I), False, 'R39'),
 ('terms', re.compile(r'13 CFR\s*(?:§\s*)?120(?:\.\d+)?(?:\([a-z]\))?', re.I), True, 'R43'),
 ('terms', re.compile(r'required by (?:the )?SBA|SBA requires|SBA[- ]required|SBA mandates', re.I), True, 'R43'),
]
# refine provisional ids by context
def refine(cat, pid, text):
    t = text.lower()
    if pid == 'R28':
        if re.search(r'change[- ]of[- ]ownership|acquisition|appendix 15', t): return 'R09'
        if re.search(r'\b504\b|cdc|debenture', t) and not re.search(r'7\(a\)', t): return 'R30'
    if pid == 'R30' and not re.search(r'\b504\b|cdc|debenture', t): return 'R28'
    if pid == 'R21' and '$350,000' in text and re.search(r'small|express', t): return 'R26'
    if pid == 'R44' and re.search(r'going[- ]concern|apprais', t): return 'R21'
    if pid == 'R13' and re.search(r'\b504\b|cdc|debenture', t): return 'R31'
    if pid == 'R13' and re.search(r'start-?up|new business', t) and not re.search(r'acqui|change[- ]of', t): return 'R29'
    if pid == 'R25' and not re.search(r'change[- ]of[- ]ownership|acqui|business portion|goodwill', t):
        if re.search(r'\b504\b|debenture', t): return 'R34'
        return 'R33'
    if pid == 'R33' and re.search(r'\b504\b|debenture', t): return 'R34'
    if pid == 'R33' and re.search(r'change[- ]of[- ]ownership|acqui', t): return 'R25'
    if pid == 'R49' and re.search(r'\b504\b|cdc', t): return 'R51'
    if pid == 'R49' and re.search(r'waiv|0%|zero|rural|manufactur', t): return 'R50'
    if pid == 'R43' and re.search(r'120\.131|occupan', t): return 'R32'
    if pid == 'R43' and re.search(r'120\.910|contribution', t): return 'R31'
    if pid == 'R43' and re.search(r'120\.86|job', t): return 'R37'
    if pid == 'R43' and re.search(r'120\.92|third party', t): return 'R35'
    if pid == 'R01' and re.search(r'50 10 7', t): return 'R06'
    return pid

def strip(s):
    s = re.sub(r'<script.*?</script>|<style.*?</style>', ' ', s, flags=re.S)
    s = re.sub(r'<[^>]+>', ' ', s); s = html.unescape(s); return re.sub(r'\s+', ' ', s).strip()

rows = []
for f in files:
    lines = open(os.path.join(ROOT, f), encoding='utf-8', errors='replace').read().split('\n')
    url = '/' + f[:-len('index.html')] if f.endswith('index.html') else '/' + f
    in_style = False
    for i, raw in enumerate(lines, 1):
        if '<style' in raw: in_style = True
        if '</style>' in raw: in_style = False; continue
        if in_style: continue
        text = strip(raw)
        if not text: continue
        # context: this line plus the previous and next line (table rows and list items span lines)
        ctx = strip(' '.join(lines[max(0, i - 2):i + 1]))
        seen = set()
        for cat, rx, specific, pid in PATTERNS:
            for m in rx.finditer(raw):
                frag = strip(raw[max(0, m.start() - 10):m.end() + 10])
                if cat == 'version' and rx.pattern.startswith('change') and not SBA_CTX.search(ctx): continue
                if not specific and not SBA_CTX.search(ctx): continue
                if rx.pattern.startswith(r'\bjobs?') and not re.search(r'\b504\b|per job|\$9[05],000|job opportunit|jobs? (?:created|retained|creation)', ctx, re.I): continue
                if rx.pattern.startswith('30 days') and not re.search(r'transient|stay', ctx, re.I): continue
                if rx.pattern.startswith(r'10[- ]year') and not re.search(r'amortiz|maturity|term|useful life', ctx, re.I): continue
                if rx.pattern.startswith(r'25[- ]year') and not re.search(r'amortiz|maturity|term|debenture|real estate', ctx, re.I): continue
                if rx.pattern.startswith(r'\b60') and not re.search(r'occup|new construction', ctx, re.I): continue
                if rx.pattern.startswith(r'\b51') and not re.search(r'occup|real estate|proceeds|controlling', ctx, re.I): continue
                if rx.pattern.startswith(r'owner') and not re.search(r'owner|51|60|sba|504|7\(a\)', ctx, re.I): continue
                key = (cat, m.group(0).lower())
                if key in seen: continue
                seen.add(key)
                stmt = text if len(text) <= 420 else text[:420] + ' …'
                rows.append(dict(file=f, url=url, line=i, statement=stmt, category=cat, match=m.group(0), register_id=refine(cat, pid, ctx)))
with open(OUT, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['file', 'url', 'line', 'statement', 'category', 'match', 'register_id', 'classification', 'resolution', 'cluster'])
    w.writeheader()
    for r in rows:
        f = r['file']
        if f.startswith('asset-classes/'): r['cluster'] = 'B/C'
        elif f.startswith('states/'): r['cluster'] = 'D'
        elif f.startswith('case-studies/') and '-sba' in f: r['cluster'] = 'E'
        elif f.startswith('practice-areas/sba-7a-504/'): r['cluster'] = 'HUB'
        elif f.startswith('practice-areas/') or f.startswith('analytical-framework/'): r['cluster'] = 'A'
        else: r['cluster'] = 'F'
        r['classification'] = ''; r['resolution'] = ''
        w.writerow(r)
from collections import Counter
print('rows', len(rows), 'files', len({r['file'] for r in rows}))
print('by cluster', dict(Counter(r['cluster'] for r in rows)))
print('by category', dict(Counter(r['category'] for r in rows)))
print('by provisional id', sorted(Counter(r['register_id'] for r in rows).items()))
