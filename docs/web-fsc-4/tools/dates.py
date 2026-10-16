#!/usr/bin/env python3
"""WEB-FSC-4 ruling 13: the explicit page-date edits. Idempotent.

1. The four cases whose math this lane changed move to the deploy date.
2. The homepage's author JSON-LD gets its date (its sitemap lastmod at 1d48cc2).
3. The five section indexes get JSON-LD dateModified on their CollectionPage node
   (their sitemap lastmod at 1d48cc2).
Every other page keeps the date it already declares; scripts/byline.py renders it
into the visible line and scripts/sitemap.py copies it into lastmod.
"""
import json, os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
DEPLOY_DATE = "2026-10-16"
MOVED = ["case-studies/rv-boat-storage-arizona-sba/index.html", "case-studies/rv-boat-storage-california-sba/index.html",
         "case-studies/rv-boat-storage-florida-sba/index.html", "case-studies/medical-office-north-carolina-sba/index.html"]
HOME = ("index.html", "2026-10-10")
INDEXES = {"states/index.html": "2026-07-08", "asset-classes/index.html": "2026-07-08", "case-studies/index.html": "2026-10-10",
           "research-notes/index.html": "2026-10-10", "practice-areas/index.html": "2026-10-10"}

def rw(rel, fn):
    p = os.path.join(ROOT, rel); s = open(p, encoding="utf-8").read(); new = fn(s)
    if new != s:
        open(p, "w", encoding="utf-8").write(new); print("dated", rel)

for rel in MOVED:
    rw(rel, lambda s: re.sub(r'("dateModified"\s*:\s*)"[0-9-]+"', r'\g<1>"%s"' % DEPLOY_DATE, s))

def home(s):
    m = re.search(r'<!--fsc:author-ld (\{.*?\})-->', s)
    p = json.loads(m.group(1)); p["date_modified"] = HOME[1]
    return s[:m.start(1)] + json.dumps(p, sort_keys=True) + s[m.end(1):]
rw(HOME[0], home)

def index_date(date):
    def fn(s):
        if '"dateModified"' in s:
            return re.sub(r'("dateModified"\s*:\s*)"[0-9-]+"', r'\g<1>"%s"' % date, s)
        m = re.search(r'("@type"\s*:\s*"CollectionPage"\s*,)', s)
        if not m:
            # no page node at all (the practice-areas index): add a WebPage node to the graph
            g = re.search(r'"@graph"\s*:\s*\[\n', s)
            url = re.search(r'<link rel="canonical" href="([^"]+)"', s).group(1)
            node = ('    {\n      "@type": "WebPage",\n      "@id": "%s#webpage",\n      "url": "%s",\n'
                    '      "dateModified": "%s"\n    },\n') % (url, url, date)
            return s[:g.end()] + node + s[g.end():]
        line_start = s.rfind("\n", 0, m.start()) + 1
        indent = re.match(r"[ \t]*", s[line_start:]).group(0)
        return s[:m.end()] + "\n" + indent + '"dateModified": "%s",' % date + s[m.end():]
    return fn
for rel, date in INDEXES.items():
    rw(rel, index_date(date))
