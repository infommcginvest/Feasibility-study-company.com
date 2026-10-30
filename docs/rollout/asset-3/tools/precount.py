#!/usr/bin/env python3
"""ASSET-3 pre-count (ruling 6, amendment A6): count the dated, sourced, page-specific figures a
fact sheet holds for each page of a hub cluster, the way pagecheck.py will count them.

    python3 docs/rollout/asset-3/tools/precount.py <facts.json> [--root <served tree>] [--json out.json]

A fact sheet (written by a research reader, kept outside the repo) is
    {"hub": "<slug>", "sources": [{"sid", "publisher", "title", "date", "url"}...],
     "figures": [{"fid", "value", "what", "period", "sid", "page": "hub" | "<subtype slug>"}...]}

A figure counts for its page when:
- its value parses as exactly one pagecheck figure (money, %, x, comma thousands, decimals, or a
  number before a counted unit word) and is not a bare year;
- its source has a publisher, title, date and absolute URL;
- no served page outside this lane's own rebuilt hubs carries it by value (pagecheck's rounding rules);
- no other page of the same cluster carries it (a figure belongs to one page; a repeat counts for neither).
"""
import argparse
import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.realpath(__file__))
HUBS = ["assisted-living-and-memory-care", "medical-office-and-asc", "childcare-and-daycare", "behavioral-health",
        "urgent-care", "veterinary-practice", "pet-boarding-and-daycare", "funeral-home", "private-school",
        "skilled-nursing", "independent-living-and-ccrc"]


def load_pagecheck(root):
    path = os.path.join(root, "docs", "web-fsc-6", "tools", "pagecheck.py")
    spec = importlib.util.spec_from_file_location("pagecheck", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = root
    return mod


def site_index(pc, exclude_prefixes):
    idx = pc.NumberIndex()
    for url, path in pc.served_pages().items():
        if any(url.startswith(p) for p in exclude_prefixes):
            continue
        html_text = pc.read(path)
        main = pc.main_soup(pc.strip_regions(html_text, ["sba", "case", "mkt", "mesh"]))
        for raw, key in pc.figures_in(main.get_text(" ")):
            if pc.YEAR.match(pc.norm(raw)):
                continue
            idx.add(key)
    return idx


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("facts")
    ap.add_argument("--root", default=os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE)))))
    ap.add_argument("--json")
    a = ap.parse_args(argv)
    pc = load_pagecheck(a.root)
    facts = json.load(open(a.facts, encoding="utf-8"))
    hub = facts["hub"]
    own = [f"/asset-classes/{h}/" for h in HUBS]
    idx = site_index(pc, own)
    srcs = {s["sid"]: s for s in facts.get("sources", [])}

    parsed = []
    for f in facts["figures"]:
        reason = None
        got = pc.figures_in(str(f.get("value", "")))
        if len(got) != 1:
            reason = f"parses as {len(got)} figures"
        else:
            raw, key = got[0]
            if pc.YEAR.match(pc.norm(raw)):
                reason = "bare year"
        s = srcs.get(f.get("sid"))
        if reason is None and (not s or not all(s.get(k) for k in ("publisher", "title", "date", "url"))
                               or not str(s.get("url", "")).startswith("http")):
            reason = "source lacks one of its four parts"
        if reason is None and idx.has(key):
            reason = "on another served page"
        parsed.append((f, key if reason is None or reason == "on another served page" else None, reason))

    # a value carried by two pages of the cluster counts for neither
    by_page = {}
    for f, key, reason in parsed:
        if key is not None and reason is None:
            by_page.setdefault(f["page"], []).append((f, key))
    pages = sorted(by_page)
    counted = {}
    dup = []
    for p in pages:
        others = pc.NumberIndex()
        for q in pages:
            if q != p:
                for _, k in by_page[q]:
                    others.add(k)
        seen = pc.NumberIndex()
        n = 0
        for f, k in by_page[p]:
            if others.has(k):
                dup.append((p, f["fid"], f["value"]))
                continue
            if seen.has(k):
                continue  # the same figure twice on one page counts once
            seen.add(k)
            n += 1
        counted[p] = n
    refused = [(f["page"], f["fid"], f.get("value"), r) for f, k, r in parsed if r]
    all_pages = sorted({f["page"] for f in facts["figures"]})
    out = {"hub": hub, "counted": {p: counted.get(p, 0) for p in all_pages}, "refused": refused, "cluster_duplicates": dup}
    print(f"pre-count for {hub}: research figures counted per page (READY needs 30 with at least 20 research)")
    for p in all_pages:
        print(f"  {p:45s} {counted.get(p, 0):4d}")
    print(f"refused {len(refused)}, cluster duplicates {len(dup)}")
    for r in refused:
        print("  refused", *r)
    for d in dup:
        print("  cluster duplicate", *d)
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)


if __name__ == "__main__":
    main(sys.argv[1:])
