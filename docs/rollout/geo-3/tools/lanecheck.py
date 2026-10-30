#!/usr/bin/env python3
"""GEO-3 content gates on a rendered tree: body words, counted figures (research and register),
overlap, clean text, links. Wraps the WEB-FSC-6 pagecheck definitions so the counts match the
house tool; adds the rollout's state and metro ranges, the register count and the promised-link rule.

    python3 docs/rollout/geo-3/tools/lanecheck.py --root <tree> [--figures] [--overlap N] [--json out] <url> ...

<tree> is a throwaway copy with the chain already run. Read only.

- Research figures: pagecheck's unique sourced figures (outside sba:, case:, mkt:, mesh: regions),
  compared by value against every other served page in <tree>.
- Register figures: distinct (geography, series) pairs among the page's mkt: markers whose rendered
  value appears on no other served page; capped at 10 (ruling 5, amendment A6).
- Floors at READY (amendment A6): counted = research + min(register, 10) >= 30, research >= 20.
- Ranges (ruling 3): state 4,500 to 8,000 body words; metro 2,000 to 3,500.
- Links: a root-relative link must resolve in <tree>, or be a promised URL (data/site/promised.json when
  present, else any URL some served page already carries as a data-fsc-pending target).
"""
import argparse
import importlib.util
import json
import os
import re
import sys

RANGES = {"state": (4500, 8000), "metro": (2000, 3500)}
MKT = re.compile(r"<!--mkt:([a-z0-9][a-z0-9/:-]*)\.([a-z0-9_]+)(?:\.[a-z0-9-]+)?( \{.*?\})?-->(.*?)<!--/mkt:", re.S)


def load_pc(root):
    path = os.path.join(root, "docs", "web-fsc-6", "tools", "pagecheck.py")
    spec = importlib.util.spec_from_file_location("pagecheck_geo3", path)
    pc = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(pc)
    pc.ROOT = os.path.abspath(root)

    def strip_regions(html_text, names):
        # pagecheck's own pattern leaves out "/", so a market geo (illinois/chicago) was not stripped
        pat = re.compile(r"<!--(" + "|".join(names) + r"):([a-z0-9_.:/-]+)( \{.*?\})?-->(.*?)<!--/\1:\2-->", re.S)
        return pat.sub(" ", html_text)
    pc.strip_regions = strip_regions
    return pc


def ptype(url):
    parts = url.strip("/").split("/")
    if parts[0] == "states" and len(parts) == 2:
        return "state"
    if parts[0] == "states" and len(parts) == 3:
        return "metro"
    return "other"


def promised(root, cache):
    p = os.path.join(root, "data", "site", "promised.json")
    out = set()
    if os.path.exists(p):
        d = json.load(open(p, encoding="utf-8"))
        items = d if isinstance(d, list) else [u for v in d.values() if isinstance(v, list) for u in v]
        out |= {x if isinstance(x, str) else x.get("url", "") for x in items}
    for h in cache.values():
        out |= set(re.findall(r'data-fsc-pending="(/[^"#?]*)"', h))
    return out


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--overlap", type=int, default=3)
    ap.add_argument("--json")
    ap.add_argument("urls", nargs="+")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    pc = load_pc(root)
    urls = ["/" + u.strip("/") + "/" for u in a.urls]
    pages = pc.served_pages()
    cache = {u: pc.read(p) for u, p in pages.items()}
    prom = promised(root, cache)
    pc.page_type = ptype
    pc.siblings = lambda url: [u for u in urls if ptype(u) == ptype(url) and u != url]
    pc.RANGES = RANGES
    res = pc.check(urls, pages, cache, True, a.overlap)
    # numbers in every page's main text, for the register uniqueness test
    nums = {u: [k for _, k in pc.figures_in(pc.overlap_text(cache[u]))] for u in pages}
    bad = 0
    report = []
    for r in res:
        url = r["url"]
        probs = [p for p in r["problems"] if not p.startswith("unique sourced figures") and not p.startswith("link to missing page")]
        if url in cache:
            h = cache[url]
            for href in sorted(set(re.findall(r'href="(/[^"#?]*)', h))):
                target = os.path.join(root, href.lstrip("/"))
                if href.endswith("/"):
                    target = os.path.join(target, "index.html")
                if not os.path.exists(target) and not os.path.exists(target.rstrip("/")) and href not in prom:
                    probs.append(f"link to a page that neither exists nor is promised: {href}")
            elsewhere = pc.NumberIndex()
            for u, ks in nums.items():
                if u != url:
                    for k in ks:
                        elsewhere.add(k)
            reg = {}
            for geo, sid, _p, val in MKT.findall(h):
                txt = re.sub(r"<[^>]+>", " ", val)
                keys = [k for _, k in pc.figures_in(txt)]
                if keys and not any(elsewhere.has(k) for k in keys):
                    reg.setdefault((geo, sid), txt.strip())
            r["register_pairs"] = len(reg)
            r["register_counted"] = min(len(reg), 10)
            r["research"] = r.get("figures_unique", 0)
            r["counted"] = r["research"] + r["register_counted"]
            if r["research"] < 20:
                probs.append(f"research figures {r['research']} under 20")
            if r["counted"] < 30:
                probs.append(f"counted figures {r['counted']} under 30")
        r["problems"] = probs
        bad += bool(probs)
        line = (f"{url:52} {r['type']:6} words {r.get('words', '-'):>6}  research {r.get('research', '-'):>3}  "
                f"register {r.get('register_counted', '-'):>2}  counted {r.get('counted', '-'):>3}  "
                f"overlap {r.get('overlap_max', '-')}% ({r.get('overlap_with')})  sibling max {r.get('overlap_sibling_max', '-')}%")
        print(line)
        for p in probs:
            print("    PROBLEM", p)
        if a.figures and r.get("unique_list"):
            print("    research figures:", "; ".join(r["unique_list"]))
        for o in r.get("overlap_top", []):
            print("    overlap", o)
        report.append(r)
    if a.json:
        json.dump(report, open(a.json, "w"), indent=1)
    print(f"{len(res)} page(s), {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
