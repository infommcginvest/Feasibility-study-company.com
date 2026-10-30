#!/usr/bin/env python3
"""GEO-3 paraphrase check: section-level 5-word shingle overlap between page sources.

    python3 docs/rollout/geo-3/tools/samecheck.py [--min 0.08] <source.html> [...] -- <compare.html> [...]

The 8-word overlap gate misses a section rewritten clause by clause in the same order. This compares
every <section> (and the front matter hero, FAQ answers and CTA) of each page on the left with every
section of every page on the right (including the left pages themselves, other than the same page) and
prints section pairs whose shared 5-word shingles exceed --min of the smaller section. Read only.
"""
import json
import re
import sys


def tokens(t):
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\[\^[\d,]+\]", " ", t)
    return re.findall(r"[a-z]+", t.lower())


def shingles(tk, n=5):
    return {" ".join(tk[i:i + n]) for i in range(len(tk) - n + 1)}


def parts(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    fm, body = json.loads(m.group(1)), m.group(2)
    out = {"hero": fm.get("hero_sub", ""), "cta": (fm.get("cta") or {}).get("p", "")}
    for i, it in enumerate((fm.get("faq") or {}).get("items", [])):
        out[f"faq{i + 1}"] = it.get("q", "") + " " + it.get("a", "")
    for s in re.finditer(r'<section id="([^"]+)"(.*?)</section>', body, re.S):
        out["#" + s.group(1)] = s.group(2)
    return {k: shingles(tokens(v)) for k, v in out.items() if v}


def main(argv):
    mn = 0.08
    if "--min" in argv:
        i = argv.index("--min")
        mn = float(argv[i + 1])
        del argv[i:i + 2]
    left, right = (argv[:argv.index("--")], argv[argv.index("--") + 1:]) if "--" in argv else (argv, [])
    pages = {p: parts(p) for p in set(left + right)}
    hits = []
    for a in left:
        for b in pages:
            if a == b:
                continue
            for ka, sa in pages[a].items():
                for kb, sb in pages[b].items():
                    if len(sa) < 15 or len(sb) < 15:
                        continue
                    sh = len(sa & sb)
                    r = sh / min(len(sa), len(sb))
                    if r >= mn:
                        hits.append((r, a.split("/")[-1], ka, b.split("/")[-1], kb, sh))
    for r, a, ka, b, kb, sh in sorted(hits, reverse=True):
        print(f"{r * 100:5.1f}%  {a}{ka:28} ~ {b}{kb:28} ({sh} shared 5-grams)")
    print(f"{len(hits)} section pair(s) at or above {mn * 100:.0f}%")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
