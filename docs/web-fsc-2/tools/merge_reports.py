#!/usr/bin/env python3
"""Merge the cluster reports' classification tables into INVENTORY.csv.

Each docs/web-fsc-2/clusters/<X>.md has a markdown table whose rows are
| file | line | classification | register_id | resolution |. Rows are matched to
inventory rows by (file, original line) in order; a report row may cover several
inventory rows on the same line when it repeats the (file, line) pair.
"""
import csv, os, re, sys, collections
HERE = os.path.dirname(os.path.abspath(__file__)); D = os.path.join(HERE, '..')
inv = list(csv.DictReader(open(os.path.join(D, 'INVENTORY.csv'), encoding='utf-8')))
by = collections.defaultdict(list)
for r in inv: by[(r['file'], r['line'])].append(r)
CLASSES = {'CURRENT', 'STALE_CITATION', 'STALE_RULE', 'UNVERIFIABLE', 'HISTORICAL'}
applied = 0; unmatched = []
for X in 'ABCDEF':
    p = os.path.join(D, 'clusters', f'{X}.md')
    if not os.path.exists(p): print('missing report', X); continue
    used = collections.Counter()
    for line in open(p, encoding='utf-8'):
        if not line.startswith('|'): continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if len(cells) < 5 or not re.match(r'^\d+$', cells[1]): continue
        f, ln, cls, rid, res = cells[0].strip('`'), cells[1], cells[2].upper().replace(' ', '_'), cells[3].strip('`'), ' | '.join(cells[4:])
        if cls not in CLASSES: continue
        rows = by.get((f, ln))
        if not rows: unmatched.append((X, f, ln)); continue
        i = used[(f, ln)]; used[(f, ln)] += 1
        targets = [rows[i]] if i < len(rows) else []
        if i == 0 and len(rows) > 1:  # first report row for this line also fills the rest until their own rows arrive
            targets = rows
        for r in targets:
            if not r['classification'] or i < len(rows):
                r['classification'] = cls; r['resolution'] = res
                if re.match(r'^R\d+[a-z]?$', rid): r['register_id'] = rid
                applied += 1
with open(os.path.join(D, 'INVENTORY.csv'), 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=list(inv[0].keys())); w.writeheader(); w.writerows(inv)
left = [r for r in inv if not r['classification']]
print('applied', applied, 'unmatched report rows', len(unmatched), unmatched[:5])
print('still unclassified', len(left), collections.Counter(r['cluster'] for r in left))
print('by class', collections.Counter(r['classification'] for r in inv))
