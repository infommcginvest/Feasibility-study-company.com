#!/usr/bin/env python3
"""ASSET-1 tranche check on a rendered throwaway copy (before FACTORY-2's scripts/qa exists).

    python3 docs/rollout/asset-1/tools/lanecheck.py --root <copy> --json out.json URL [URL ...]

Wraps docs/web-fsc-6/tools/pagecheck.py (body words, research figures counted outside sba:, case:,
mkt: and mesh: regions, 8-word shingle overlap against every served page, dashes, banned names, the
SBA mandate pattern, missing link targets) with the ROLLOUT-1 ranges and Amendment 1 table:
hub 6,000 to 10,000 body words, subtype 1,800 to 3,000; at READY 30 counted, 20 of them research,
register counted at most 10. Register figures are counted here by (geography, series) pair: a mkt:
value counts when its rendered value appears on no other served page, at most one per pair, at most 10.
Also runs docs/web-fsc-6/tools/sbamandate.py's sentence test on each page.
"""
import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RANGES = {"hub": (6000, 10000), "subtype": (1800, 3000)}
MKT = re.compile(r"<!--mkt:([a-z0-9][a-z0-9/:-]*)\.([a-z0-9_]+)(?:\.([a-z0-9-]+))?( \{.*?\})?-->(.*?)<!--/mkt:", re.S)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--json")
    ap.add_argument("urls", nargs="+")
    a = ap.parse_args()
    root = os.path.abspath(a.root)
    sys.path.insert(0, os.path.join(root, "docs", "web-fsc-6", "tools"))
    import pagecheck as pc
    import sbamandate as sm
    pc.ROOT = root
    hubs = {"/asset-classes/" + h + "/" for h in ("hotel", "rv-park-and-campground", "glamping", "marina",
            "fitness-and-recreation", "short-term-rental", "event-and-wedding-venue", "brewery-and-distillery",
            "wellness-and-retreat")}
    pc.page_type = lambda u: "hub" if u in hubs else ("subtype" if any(u.startswith(h) for h in hubs) else "other")
    pc.siblings = lambda u: [x for x in a.urls if x != u and pc.page_type(x) == pc.page_type(u)]
    pc.RANGES = RANGES
    urls = ["/" + u.strip("/") + "/" for u in a.urls]
    pages = pc.served_pages()
    cache = {u: pc.read(p) for u, p in pages.items()}
    res = pc.check(urls, pages, cache, True, 3)
    others = {}
    for u in pages:
        idx = pc.NumberIndex()
        for _, k in pc.figures_in(pc.overlap_text(cache[u])):
            idx.add(k)
        others[u] = idx
    bad = 0
    for r in res:
        u = r["url"]
        h = cache.get(u, "")
        r["problems"] = [p for p in r["problems"] if not p.startswith("unique sourced figures")]
        pairs = {}
        for geo, sid, cls, _p, val in MKT.findall(h):
            key = pc.figure_key(re.sub(r"<[^>]+>", "", val).strip())
            if key is None:
                continue
            free = not any(idx.has(key) for v, idx in others.items() if v != u)
            pairs.setdefault((geo, sid), []).append(free)
        reg = min(10, sum(1 for v in pairs.values() if any(v)))
        r["register_pairs"] = len(pairs)
        r["register_counted"] = reg
        r["research_counted"] = r.get("figures_unique", 0)
        r["counted"] = r["research_counted"] + reg
        if r["research_counted"] < 20:
            r["problems"].append(f"research figures {r['research_counted']} under 20")
        if r["counted"] < 30:
            r["problems"].append(f"counted figures {r['counted']} under 30")
        mand = sm.flagged(h)
        if mand:
            r["problems"].append("sbamandate: " + mand[0][:120])
        print(f"{u:66} {r['type']:7} words {r.get('words', '-'):>6}  research {r['research_counted']:>3}  register {reg:>2}"
              f"  counted {r['counted']:>3}  overlap {r.get('overlap_max')}% ({r.get('overlap_with')})")
        for p in r["problems"]:
            print("    PROBLEM", p)
        bad += bool(r["problems"])
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    print(f"{len(res)} page(s), {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
