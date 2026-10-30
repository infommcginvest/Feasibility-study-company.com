#!/usr/bin/env python3
"""GEO-4 cross-lane sameness guard (integrator I74): 8-word shingle overlap of page SOURCES (body prose plus the
front matter's hero, FAQ and CTA; sources lists left out) between our drafts and a comparison set of landed sources
and in-flight drafts. Prints the overlap per pair (shared shingles over the smaller page's) and every shared run.

    python3 sameness.py --ours a.html b.html --against <files or dirs...>
"""
import argparse
import html
import json
import os
import re

TOK = re.compile(r"[a-z0-9]+(?:['.][a-z0-9]+)*")


def text_of(path):
    s = open(path, encoding="utf-8").read()
    if not s.startswith("---\n"):
        body, fm = s, {}
    else:
        head, body = s.split("\n---\n", 1)
        try:
            fm = json.loads(head[4:])
        except Exception:
            fm = {}
    body = re.sub(r"<!--.*?-->", " ", body, flags=re.S)
    attrs = " ".join(re.findall(r'data-(?:h2|lede)="([^"]*)"', body))
    body = re.sub(r"<[^>]+>", " ", body)
    extra = [fm.get("hero_sub", ""), (fm.get("cta") or {}).get("h2", ""), (fm.get("cta") or {}).get("p", ""),
             fm.get("description", ""), fm.get("sources_lede", "")]
    for q in (fm.get("faq") or {}).get("items", []):
        extra += [q.get("q", ""), q.get("a", "")]
    t = html.unescape(body + " " + attrs + " " + " ".join(extra))
    t = re.sub(r"\[\^[\d,\s]+\]", " ", t).lower()
    return TOK.findall(t)


def shingles(toks, n=8):
    return {" ".join(toks[i:i + n]) for i in range(len(toks) - n + 1)}


def files(args):
    out = []
    for a in args:
        if os.path.isdir(a):
            for d, _, fs in os.walk(a):
                out += [os.path.join(d, f) for f in fs if f.endswith(".html")]
        elif a.endswith(".html"):
            out.append(a)
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ours", nargs="+", required=True)
    ap.add_argument("--against", nargs="+", required=True)
    a = ap.parse_args()
    home = os.path.expanduser("~")
    ours = {p: shingles(text_of(p)) for p in a.ours}
    others = [p for p in files(a.against) if os.path.abspath(p) not in {os.path.abspath(x) for x in a.ours}]
    print(f"comparison set: {len(others)} files")
    worst = []
    for p, sp in ours.items():
        for q in others:
            sq = shingles(text_of(q))
            if not sp or not sq:
                continue
            common = sp & sq
            ov = len(common) / min(len(sp), len(sq))
            worst.append((ov, p, q, common))
    worst.sort(reverse=True)
    for ov, p, q, common in worst[:25]:
        print(f"{ov * 100:6.2f}%  {os.path.basename(p):24} vs {q.replace(home, '~')}  shared {len(common)}")
    print("\nshared 8-word runs:")
    for ov, p, q, common in worst:
        for c in sorted(common):
            print(f"  {os.path.basename(p)} | {q.replace(home, '~')} | {c}")


if __name__ == "__main__":
    main()
