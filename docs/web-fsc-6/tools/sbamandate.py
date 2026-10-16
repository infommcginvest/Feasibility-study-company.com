#!/usr/bin/env python3
"""Sentences on served pages that tie SBA to a required or mandatory feasibility study.

13 CFR 120.160(b): SBA may require a feasibility study. A sentence is flagged when it names SBA (not USDA alone), a
feasibility study, and a word of compulsion, without "may require" or a negation. Used by gate 7 over every served page.
"""
import html
import re

SENT = re.compile(r"[^.!?]*[.!?]")
COMPEL = re.compile(r"\b(requires?|required|mandatory|mandates?|mandated|triggers?|compulsory|must (?:obtain|commission|order|have))\b", re.I)
OK = re.compile(r"may require|does not|doesn't|do not|no rule|not (?:a )?(?:mandatory|required)|\bnever\b|isn't|is not|\boptional\b|"
                r"at (?:its|the lender's|their) discretion|\bmyth\b|lender[s']* (?:may|often|routinely|usually|typically) (?:ask|require|want)", re.I)


def text_of(h):
    h = re.sub(r"<(script|style)\b.*?</\1>", " ", h, flags=re.S | re.I)
    h = re.sub(r"<!--.*?-->", " ", h, flags=re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", h)))


def flagged(h):
    out = []
    for s in SENT.findall(text_of(h)):
        if not s.rstrip().endswith("?") and re.search(r"feasibility stud", s, re.I) and re.search(r"\bSBA\b", s) and COMPEL.search(s) and not OK.search(s):
            out.append(s.strip())
    return out


if __name__ == "__main__":
    import os
    import sys
    root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    n = 0
    for d, ds, fs in os.walk(root):
        ds[:] = [x for x in ds if x not in (".git", "docs", "src", "node_modules", "_bundles", "scripts", "data", "netlify")]
        if "index.html" in fs:
            p = os.path.join(d, "index.html")
            for s in flagged(open(p, encoding="utf-8").read()):
                n += 1
                print(os.path.relpath(p, root), "|", s[:300])
    print(n, "flagged")
    sys.exit(1 if n else 0)
