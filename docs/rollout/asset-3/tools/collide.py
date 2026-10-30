#!/usr/bin/env python3
"""ASSET-3 cross-draft figure collisions (decision D6): render every draft in ~/Downloads/fsc-rollout/drafts/asset-3/pages
and list, for each pair of drafts, the cited figures that would count on one of them (not on any served page) but
appear on both by value (pagecheck.py's rounding rules), so a value counts for neither.

    python3 docs/rollout/asset-3/tools/collide.py [--page <url>]
"""
import argparse
import glob
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
spec = importlib.util.spec_from_file_location("selfcheck", os.path.join(HERE, "selfcheck.py"))
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--page")
    a = ap.parse_args(argv)
    pc = sc.load_pagecheck()
    site = {u: p for u, p in pc.served_pages().items() if not any(u.startswith(x) for x in sc.OWN_PREFIXES)}
    idx = pc.NumberIndex()
    for u, p in site.items():
        m = pc.main_soup(pc.strip_regions(pc.read(p), ["sba", "case", "mkt", "mesh"]))
        for raw, key in pc.figures_in(m.get_text(" ")):
            if not pc.YEAR.match(pc.norm(raw)):
                idx.add(key)
    drafts = sorted(glob.glob(os.path.join(sc.DRAFTS, "**", "*.html"), recursive=True))
    cited, alltext = {}, {}
    for d in drafts:
        front, h, log = sc.render(d, False)
        if h is None:
            print("BUILD FAILED", d, log)
            continue
        url = front["url"]
        cited[url] = [(raw, k) for n, (raw, k) in pc.sourced_figures(h).items() if not idx.has(k)]
        m = pc.main_soup(pc.strip_regions(h, ["sba", "case", "mkt", "mesh"]))
        alltext[url] = [(raw, k) for raw, k in pc.figures_in(m.get_text(" ")) if not pc.YEAR.match(pc.norm(raw))]
    urls = sorted(cited)
    for u in urls:
        if a.page and u != a.page:
            continue
        for v in urls:
            if v == u:
                continue
            other = pc.NumberIndex()
            for raw, k in alltext[v]:
                other.add(k)
            hits = [raw for raw, k in cited[u] if other.has(k)]
            if hits:
                print(f"{u}  loses to  {v}: {', '.join(hits)}")
    print("counted (after cross-draft collisions):")
    for u in urls:
        others = pc.NumberIndex()
        for v in urls:
            if v != u:
                for raw, k in alltext[v]:
                    others.add(k)
        print(f"  {u:75} {sum(1 for raw, k in cited[u] if not others.has(k)):4}")


if __name__ == "__main__":
    main(sys.argv[1:])
