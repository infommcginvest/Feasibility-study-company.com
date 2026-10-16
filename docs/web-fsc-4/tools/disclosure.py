#!/usr/bin/env python3
"""WEB-FSC-4 ruling 11: the disclosure box under the H1 and byline of every older case.

Idempotent. Inserts the batch-1 `capsule disclosure` markup directly after the
byline-article region in the hero, adds the `.hero .disclosure` rule where the
page's CSS lacks it, and removes the one intro sentence that contradicts the box.
Pages listed in data/site/hold.json (WEB-FSC-6) are never touched.

    python3 docs/web-fsc-4/tools/disclosure.py [--only slug,slug] [--skip slug,slug] [--check]
"""
import glob, json, os, re, sys, fnmatch
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
BOX = ('\n      <div class="capsule disclosure">\n'
       '        <p><strong>Representative worked example.</strong> The site, sponsor and project are hypothetical. '
       'The market evidence comes from the public sources listed below, with their dates. This page shows how the '
       'market analysis is built and how it sets the loan. It is not a client engagement.</p>\n'
       '      </div>')
CSS = '<style>\n/* WEB-FSC-4 disclosure box */\n.hero .disclosure { margin-top: 30px; }\n</style>\n'
# Sentences that contradict the box (they say the figures come from real engagements).
CONTRADICT = {
    "assisted-living-north-carolina-hud": [
        "The figures here are a composite of the assisted living and memory care engagements we see in high-growth North Carolina submarkets, not a single named deal.",
    ],
}

def held(rel, pats):
    return any(fnmatch.fnmatch(rel, p) for p in pats)

def main(argv):
    hold = json.load(open(os.path.join(ROOT, "data/site/hold.json")))["pages"]
    only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
    skip = set(argv[argv.index("--skip") + 1].split(",")) if "--skip" in argv else set()
    check = "--check" in argv
    missing, changed = [], []
    for path in sorted(glob.glob(os.path.join(ROOT, "case-studies/*/index.html"))):
        rel = os.path.relpath(path, ROOT)
        slug = rel.split("/")[1]
        if held(rel, hold) or slug in skip or (only and slug not in only):
            continue
        s = open(path, encoding="utf-8").read()
        new = s
        hero = re.search(r'<section class="hero">.*?</section>', new, re.S)
        if 'class="capsule disclosure"' not in hero.group(0):
            end = new.index("<!--/fsc:byline-article-->", hero.start()) + len("<!--/fsc:byline-article-->")
            new = new[:end] + BOX + new[end:]
        if ".hero .disclosure" not in new:
            i = new.index("</head>")
            new = new[:i] + CSS + new[i:]
        for sent in CONTRADICT.get(slug, []):
            flat = re.sub(r"\s+", " ", new)
            if sent in flat:
                # the sentence may wrap across source lines: match on any whitespace
                rx = re.compile(r"\s*" + r"\s+".join(re.escape(w) for w in sent.split()))
                new, n = rx.subn("", new, count=1)
                assert n == 1, (slug, sent)
        hero = re.search(r'<section class="hero">.*?</section>', new, re.S).group(0)
        ok = re.search(r'</h1>\s*<!--fsc:byline-article[^>]*-->.*?<!--/fsc:byline-article-->\s*<div class="capsule disclosure">', hero, re.S)
        if not ok:
            missing.append(rel)
        if new != s:
            changed.append(rel)
            if not check:
                open(path, "w", encoding="utf-8").write(new)
    for r in changed:
        print(("needs box: " if check else "boxed: ") + r)
    for r in missing:
        print("box not directly under H1 and byline: " + r)
    print(f"{len(changed)} page(s) {'out of date' if check else 'changed'}; {len(missing)} misplaced")
    return 1 if (missing or (check and changed)) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
