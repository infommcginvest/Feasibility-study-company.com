#!/usr/bin/env python3
"""GEO-3 pre-check: how many of a fact sheet's figures are unique on the site, by pagecheck's value rule.

    python3 docs/rollout/geo-3/tools/sheetcheck.py --root <tree> [--exclude <url> ...] <facts-slug.md> [...]

Reads each sheet's figure table rows (`| # | Figure | Value | Period | ...`), extracts the figures in
"<value> <figure description>" with pagecheck's own figure parser, and tests each against every served
page of <tree> except the --exclude URLs (the old version of a page being rebuilt, the page itself).
Prints the unique count per sheet and the colliding values. A writer cannot beat this number on the
site as it stands, so a sheet under 20 here folds before it is drafted. Read only.
"""
import argparse
import importlib.util
import os
import re
import sys


def load_pc(root):
    path = os.path.join(root, "docs", "web-fsc-6", "tools", "pagecheck.py")
    spec = importlib.util.spec_from_file_location("pagecheck_geo3s", path)
    pc = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(path))
    spec.loader.exec_module(pc)
    pc.ROOT = os.path.abspath(root)
    return pc


ROW = re.compile(r"^\|\s*\d+\s*\|([^|]*)\|([^|]*)\|")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--exclude", action="append", default=[])
    ap.add_argument("--show", action="store_true")
    ap.add_argument("sheets", nargs="+")
    a = ap.parse_args(argv)
    pc = load_pc(a.root)
    pages = pc.served_pages()
    excl = {"/" + u.strip("/") + "/" for u in a.exclude}
    idx = pc.NumberIndex()
    for u, p in pages.items():
        if u in excl:
            continue
        for _, k in pc.figures_in(pc.overlap_text(pc.read(p))):
            idx.add(k)
    for sh in a.sheets:
        uniq, coll, own = [], [], pc.NumberIndex()
        for line in open(sh, encoding="utf-8"):
            m = ROW.match(line)
            if not m:
                continue
            desc, val = m.group(1).strip(), m.group(2).strip()
            for raw, key in pc.figures_in(f"{val} {desc}"):
                n = pc.norm(raw)
                if pc.YEAR.match(n) or own.has(key):
                    continue
                own.add(key)
                (coll if idx.has(key) else uniq).append(raw.strip())
        print(f"{os.path.basename(sh):40} unique {len(uniq):3}  colliding {len(coll):3}")
        if a.show:
            print("   unique:", "; ".join(uniq))
            print("   colliding:", "; ".join(coll))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
