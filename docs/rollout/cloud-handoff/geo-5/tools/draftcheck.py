#!/usr/bin/env python3
"""GEO-5 draft check (from GEO-2's): render draft sources in memory and measure them against the served site.

    python3 draftcheck.py <draft.html> [more drafts] [--figures] [--overlap 5] [--all-drafts]

Drafts live in ~/Downloads/fsc-rollout/drafts/geo-5/pages/<state>.html and
~/Downloads/fsc-rollout/drafts/geo-5/pages/<state>/<metro>.html (the same layout as src/pages/states/).
Nothing is written to the repo. Uses the worktree's build.py to render and pagecheck.py to measure:
- body words (ruling 3 ranges: state 4,500 to 8,000; metro 2,000 to 3,500);
- counted figures: sourced figures outside sba/case/mkt/mesh regions that appear on no other served page
  and on no other GEO-2 draft (the eight GEO-2 state pages being rebuilt are left out of the index);
- overlap: 8-word shingles against every served page and every other GEO-2 draft (< 15%);
- dashes, banned names, SBA-mandate wording, typed credentials, links to pages that do not exist
  (GEO-2 drafts and promised GEO-2 URLs count as existing only when --promised is given).
"""
import argparse
import glob
import json
import os
import re
import sys

TREE = os.path.expanduser("~/Downloads/wt-rollout-geo-5")
DRAFTS = os.path.expanduser("~/Downloads/fsc-rollout/drafts/geo-5/pages")
sys.path.insert(0, os.path.join(TREE, "scripts"))
sys.path.insert(0, os.path.join(TREE, "docs/web-fsc-6/tools"))
import build  # noqa: E402
import pagecheck as pc  # noqa: E402

pc.ROOT = TREE
GEO2 = ["alaska", "colorado", "district-of-columbia", "north-dakota", "south-dakota", "vermont", "virginia", "wyoming"]
RANGES = {"state": (4500, 8000), "metro": (2000, 3500)}


def parse(path):
    raw = open(path, encoding="utf-8").read()
    if not raw.startswith("---\n"):
        raise SystemExit(f"{path}: must open with ---")
    end = raw.find("\n---\n", 4)
    front = json.loads(raw[4:end])
    return front, raw[end + 5:]


def render(path):
    front, body = parse(path)
    cfg = build.site_config()
    return front, build.render(front, body, cfg, None)


def all_draft_paths():
    return sorted(glob.glob(os.path.join(DRAFTS, "*.html")) + glob.glob(os.path.join(DRAFTS, "*", "*.html")))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("drafts", nargs="+")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--overlap", type=int, default=3)
    ap.add_argument("--promised", action="store_true", help="treat GEO-2 draft URLs as existing link targets")
    a = ap.parse_args(argv)

    skip = {f"/states/{s}/" for s in GEO2}
    pages = pc.served_pages()
    cache = {u: pc.read(p) for u, p in pages.items() if u not in skip}
    drafts = {}
    errors = {}
    for p in all_draft_paths():
        try:
            f, h = render(p)
            drafts[f["url"]] = (p, f, h)
        except Exception as e:  # noqa: BLE001
            errors[p] = str(e)
    targets = []
    for d in a.drafts:
        d = os.path.abspath(os.path.expanduser(d))
        if d in errors:
            print(f"{d}: RENDER FAILED: {errors[d]}")
            continue
        hit = [u for u, (p, _, _) in drafts.items() if os.path.abspath(p) == d]
        if not hit:
            try:
                f, h = render(d)
                drafts[f["url"]] = (d, f, h)
                hit = [f["url"]]
            except Exception as e:  # noqa: BLE001
                print(f"{d}: RENDER FAILED: {e}")
                continue
        targets.append(hit[0])

    others_text = {u: pc.overlap_text(h) for u, h in cache.items()}
    for u, (_, _, h) in drafts.items():
        others_text[u] = pc.overlap_text(h)
    nums = {u: [k for _, k in pc.figures_in(t)] for u, t in others_text.items()}
    shing = {u: pc.shingles(t) for u, t in others_text.items()}
    existing = set(pages) | (set(drafts) if a.promised else set())
    bad_total = 0
    for url in targets:
        p, front, h = drafts[url]
        kind = front["type"]
        probs = []
        words = pc.body_words(h)
        lo, hi = RANGES.get(kind, (None, None))
        if lo and words < lo:
            probs.append(f"body words {words} under {lo}")
        if hi and words > hi:
            probs.append(f"body words {words} over {hi}")
        figs = pc.sourced_figures(h)
        elsewhere = pc.NumberIndex()
        for u, ks in nums.items():
            if u != url:
                for k in ks:
                    elsewhere.add(k)
        uniq, own, shared = {}, pc.NumberIndex(), []
        for n, (raw, key) in figs.items():
            if elsewhere.has(key):
                shared.append(raw)
            elif not own.has(key):
                uniq[n] = raw
            own.add(key)
        mkt = len(re.findall(r"<!--mkt:", h))
        if len(uniq) < 20:
            probs.append(f"counted research figures {len(uniq)} under 20 (READY needs 20 research, 30 with register)")
        mine = shing[url]
        ov = []
        for u, s in shing.items():
            if u == url or not mine or not s:
                continue
            sh = len(mine & s)
            if sh:
                ov.append((sh / min(len(mine), len(s)), u, sh))
        ov.sort(reverse=True)
        if ov and ov[0][0] >= 0.15:
            probs.append(f"overlap {ov[0][0]*100:.2f}% with {ov[0][1]}")
        if pc.DASHES.search(h):
            probs.append("dashes present")
        if pc.FORBIDDEN.search(h):
            probs.append("banned name present")
        txt = re.sub(r"<[^>]+>", " ", h)
        if pc.SBA_REQUIRES.search(txt):
            probs.append("SBA-requires wording: " + pc.SBA_REQUIRES.search(txt).group(0)[:90])
        if re.search(r"otava,? *(ph\.?d|ccim|mai)", h, re.I):
            probs.append("credential typed")
        for href in sorted(set(re.findall(r'href="(/[^"#?]*)', h))):
            if href not in existing and href.rstrip("/") + "/" not in existing and not os.path.exists(os.path.join(TREE, href.lstrip("/"))):
                probs.append(f"link to missing page {href}")
        nsrc = len(front.get("sources", []))
        cited = {int(x) for x in re.findall(r"\[\^([\d,\s]+)\]", open(p).read()) for x in x.split(",") if x.strip()} if False else set()
        raw = open(p, encoding="utf-8").read()
        for grp in re.findall(r"\[\^([\d,\s]+)\]", raw):
            for x in grp.split(","):
                if x.strip():
                    cited.add(int(x))
        uncited = [i for i in range(1, nsrc + 1) if i not in cited]
        if uncited:
            probs.append(f"sources never cited: {uncited}")
        bad = [i for i in cited if i < 1 or i > nsrc]
        if bad:
            probs.append(f"citations past the sources list: {bad}")
        print(f"{url:52} {kind:6} words {words:5}  counted {len(uniq):3} (shared {len(shared)}, mkt markers {mkt})  "
              f"overlap {ov[0][0]*100 if ov else 0:.2f}% ({ov[0][1] if ov else '-'})  sources {nsrc}")
        for x in probs:
            print("    PROBLEM", x)
        if a.figures:
            print("    counted:", "; ".join(sorted(uniq.values())))
            print("    shared (do not count):", "; ".join(sorted(shared)))
        for o in ov[:a.overlap]:
            print(f"    overlap {o[0]*100:.2f}% {o[1]} ({o[2]} shingles)")
        bad_total += bool(probs)
    print(f"{len(targets)} draft(s), {bad_total} with problems; {len(errors)} draft(s) failed to render")
    for p, e in errors.items():
        print("  RENDER FAILED", p, e[:200])
    return 1 if bad_total or errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
