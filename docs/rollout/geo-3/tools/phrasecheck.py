#!/usr/bin/env python3
"""GEO-3 phrase census: word runs a page shares with other pages, and runs repeated between its own sections.

    python3 docs/rollout/geo-3/tools/phrasecheck.py [--n 6] <source.html> [...] -- <compare> [...]

samecheck.py measures a section's share of 5-word shingles, which a long section dilutes; a reviewer
still sees a stock clause carried from page to page ("a credit officer can check", a table cell copied
with the state renamed). This lists every run of at least --n words (lowercase letters only, digits and
markup dropped) that a left page shares with any compare file or with another section of itself, merged
into maximal runs, with the sections it sits in. A compare file is a page source (JSON front matter) or a
served page (its <main> text, mesh lists and the sources list removed). Runs made mostly of stopwords are
skipped. Read only.
"""
import json
import os
import re
import sys

STOP = set("a an and are as at be by for from has have in into is it its of on or that the this to was were with which "
           "not no can will should than then there their they them more most any each one two who what when where how "
           "our we you your about over under after before but also only so if".split())


DEFAULT_LEDE = "Every figure on this page traces to a named, dated source."


def toks(t):
    # text rendered from sba: and mkt: markers is register wording, identical on every page by design (D22)
    t = re.sub(r"<!--(sba|mkt):([^ >]+?)(?: [^>]*)?-->.*?<!--/\1:\2-->", " ", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", " ", t, flags=re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"\[\^[\d,]+\]", " ", t)
    return re.findall(r"[a-z]+", t.lower())


def parts(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", t, re.S)
    if m:
        fm, body = json.loads(m.group(1)), m.group(2)
        # sources_lede, description and stat labels are prose too (Missouri t6 attacker two: a 14-word sources_lede run
        # with live Texas passed this census); the build's default sources_lede sentence renders on every page that omits one
        lede = (fm.get("sources_lede") or "").replace(DEFAULT_LEDE, " ")
        out = {"hero": fm.get("hero_sub", ""), "cta": (fm.get("cta") or {}).get("p", ""), "description": fm.get("description", ""),
               "sources_lede": lede, "stats": " | ".join(s.get("label", "") for s in fm.get("stats") or [])}
        for i, it in enumerate((fm.get("faq") or {}).get("items", [])):
            out[f"faq{i + 1}"] = it.get("q", "") + " " + it.get("a", "")
        for s in re.finditer(r'<section id="([^"]+)"([^>]*)>(.*?)</section>', body, re.S):
            # headings (data-eyebrow, data-h2) may repeat across siblings (ruling 4); the lede is prose
            lede = re.search(r'data-lede="([^"]*)"', s.group(2))
            out["#" + s.group(1)] = (lede.group(1) if lede else "") + " " + s.group(3)
    else:
        mm = re.search(r"<main\b.*?</main>", t, re.S)
        h = mm.group(0) if mm else t
        h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S)
        h = re.sub(r"<!--mesh:.*?<!--/mesh:[^>]*-->", " ", h, flags=re.S)
        h = re.sub(r'<ol class="sources".*?</ol>', " ", h, flags=re.S).replace(DEFAULT_LEDE, " ")
        out = {"main": h}
    return {k: toks(v) for k, v in out.items() if v}


def grams(tk, n):
    g = {}
    for i in range(len(tk) - n + 1):
        w = tuple(tk[i:i + n])
        if sum(x in STOP for x in w) >= n - 1:
            continue
        g.setdefault(w, i)
    return g


def runs(tk, hit_starts, n):
    """Merge hit n-gram start positions into maximal word runs."""
    out, cur = [], None
    for i in sorted(hit_starts):
        if cur and i <= cur[1]:
            cur[1] = i + n
        else:
            if cur:
                out.append(cur)
            cur = [i, i + n]
    if cur:
        out.append(cur)
    return [" ".join(tk[a:b]) for a, b in out]


def label(p):
    parts_ = p.split(os.sep)
    return "/".join(parts_[-2:]) if parts_[-1] == "index.html" else parts_[-1]


def main(argv):
    n = 6
    if "--n" in argv:
        i = argv.index("--n")
        n = int(argv[i + 1])
        del argv[i:i + 2]
    left, right = (argv[:argv.index("--")], argv[argv.index("--") + 1:]) if "--" in argv else (argv, [])
    right = [p for p in right if os.path.abspath(p) not in {os.path.abspath(x) for x in left}]
    index = {}
    for p in right:
        try:
            pp = parts(p)
        except Exception as exc:
            print(f"skip {p}: {exc}", file=sys.stderr)
            continue
        for k, tk in pp.items():
            for w in grams(tk, n):
                index.setdefault(w, set()).add(f"{label(p)}{'' if k == 'main' else k}")
    total = 0
    for p in left:
        pp = parts(p)
        own = {}
        for k, tk in pp.items():
            for w in grams(tk, n):
                own.setdefault(w, set()).add(k)
        print(f"### {label(p)}")
        for k, tk in pp.items():
            g = grams(tk, n)
            ext = {i for w, i in g.items() if w in index}
            intra = {i for w, i in g.items() if len(own[w]) > 1}
            for kind, starts in (("shared", ext), ("repeated in page", intra)):
                for r in runs(tk, starts, n):
                    w = tuple(r.split()[:n])
                    where = sorted(index.get(w, set())) if kind == "shared" else sorted(own[w] - {k})
                    print(f"  {k:24} {kind:16} \"{r}\"  <- {', '.join(where[:6])}{' ...' if len(where) > 6 else ''}")
                    total += 1
    print(f"{total} run(s) of {n}+ words")
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
