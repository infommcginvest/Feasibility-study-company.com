#!/usr/bin/env python3
"""ASSET-1 pre-count helper: does a figure already appear on another served page?

Uses docs/web-fsc-6/tools/pagecheck.py's own figure parser and value index, so a figure that
collides here would not count at the gate either.

    python3 docs/rollout/asset-1/tools/figcheck.py --root <tree> [--exclude /asset-classes/hotel/ ...] figures.txt

figures.txt: one figure per line, written as it will appear on the page ("$187,000", "68.4%",
"1.42x", "4,712", "$3.1 billion"); anything after a TAB is carried through as a label.
Prints FREE or TAKEN <first page it is on> per line, then the count of FREE figures.
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.path.abspath(os.path.join(HERE, "..", "..", "..", "..")))
    ap.add_argument("--exclude", nargs="*", default=[])
    ap.add_argument("file")
    a = ap.parse_args()
    a.root = os.path.abspath(a.root)
    sys.path.insert(0, os.path.join(a.root, "docs", "web-fsc-6", "tools"))
    import pagecheck as pc
    pc.ROOT = a.root
    pages = pc.served_pages()
    where = {}
    for url, path in pages.items():
        if url in a.exclude:
            continue
        idx = pc.NumberIndex()
        for _, k in pc.figures_in(pc.overlap_text(pc.read(path))):
            idx.add(k)
        where[url] = idx
    free = 0
    seen = pc.NumberIndex()
    for line in open(a.file, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip():
            continue
        raw, _, label = line.partition("\t")
        key = pc.figure_key(raw.strip())
        if key is None:
            print(f"UNPARSED\t{raw}\t{label}")
            continue
        hit = next((u for u, idx in where.items() if idx.has(key)), None)
        if hit:
            print(f"TAKEN {hit}\t{raw}\t{label}")
        elif seen.has(key):
            print(f"REPEAT (same figure earlier in this list)\t{raw}\t{label}")
        else:
            print(f"FREE\t{raw}\t{label}")
            free += 1
        seen.add(key)
    print(f"FREE figures: {free}")


if __name__ == "__main__":
    main()
