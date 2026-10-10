#!/usr/bin/env python3
"""Set dateModified, article:modified_time, the fsc 'updated' params, 'Reviewed' lines
and sitemap lastmod to the build date on every page changed since the cut point.

    python3 docs/web-fsc-2/tools/stamp_dates.py 2026-10-10 <cut-ref>
"""
import os, re, subprocess, sys, json
DATE, CUT = sys.argv[1], sys.argv[2]
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
y, m, d = DATE.split('-'); month = f'{MONTHS[int(m)-1]} {y}'
changed = set(subprocess.run(['git', 'diff', '--name-only', CUT], cwd=ROOT, capture_output=True, text=True).stdout.split())
changed |= set(subprocess.run(['git', 'ls-files', '--others', '--exclude-standard'], cwd=ROOT, capture_output=True, text=True).stdout.split())
pages = sorted(f for f in changed if f.endswith('.html') and not f.startswith('docs/'))
for f in pages:
    p = os.path.join(ROOT, f); t = open(p, encoding='utf-8').read(); o = t
    t = re.sub(r'"dateModified": "\d{4}-\d{2}-\d{2}"', f'"dateModified": "{DATE}"', t)
    t = re.sub(r'<meta property="article:modified_time" content="\d{4}-\d{2}-\d{2}">', f'<meta property="article:modified_time" content="{DATE}">', t)
    t = re.sub(r'(<!--fsc:line-(?:asset|state|home) \{"updated": ")\d{4}-\d{2}-\d{2}("\})', lambda mm: mm.group(1) + DATE + mm.group(2), t)
    t = re.sub(r'(<strong>Reviewed and updated:</strong>)\s*[A-Z][a-z]+ \d{4}(?=[.,])', lambda mm: f'{mm.group(1)} {month}', t)
    if t != o: open(p, 'w', encoding='utf-8').write(t)
# sitemap
sm = os.path.join(ROOT, 'sitemap.xml'); s = open(sm, encoding='utf-8').read(); n = 0
for f in pages:
    url = 'https://feasibility-study-company.com/' + (f[:-len('index.html')] if f.endswith('index.html') else f)
    s2 = re.sub(r'(<loc>' + re.escape(url) + r'</loc>\s*<lastmod>)\d{4}-\d{2}-\d{2}', lambda mm: mm.group(1) + DATE, s)
    if s2 != s: n += 1; s = s2
open(sm, 'w', encoding='utf-8').write(s)
print('pages stamped', len(pages), 'sitemap entries updated', n)
subprocess.run([sys.executable, 'scripts/byline.py'], cwd=ROOT)
