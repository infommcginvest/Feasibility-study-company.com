#!/usr/bin/env python3
"""WEB-FSC-4, after freeze 1: repair the 29 dash pairs the sweep joined across a sentence break.

The sentence splitter in dashes.py missed sentence ends hidden behind a footnote
marker (".<sup>9</sup> On") and the abbreviation "J.B.", so two single dashes
in neighbouring sentences were paired and became "(" ... ")". Each half is
decided on its own here. The fix replays the sweep on the pre-sweep text
(c203580) to find exactly which characters each dash became, then edits those
characters in the current file. Words never change.

    python3 docs/web-fsc-4/tools/fix_crosspairs.py [--only slug,...] [--skip slug,...]
"""
import json, os, re, subprocess, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, os.path.join(ROOT, "docs", "web-fsc-4", "tools"))
import dashes  # noqa: E402

C = "case-studies/%s/index.html"; S = "states/%s/index.html"
FIX = {
    (C % "assisted-living-arizona-hud", 22): "comma", (C % "assisted-living-arizona-hud", 23): "comma",
    (C % "assisted-living-california-hud", 29): "comma", (C % "assisted-living-california-hud", 30): "comma",
    (C % "childcare-illinois-sba", 26): "colon", (C % "childcare-illinois-sba", 27): "comma",
    (C % "coffee-shop-washington-sba", 10): "comma", (C % "coffee-shop-washington-sba", 11): "comma",
    (C % "fitness-minnesota-sba", 28): "comma", (C % "fitness-minnesota-sba", 29): "comma",
    (C % "funeral-home-wisconsin-sba", 21): "comma", (C % "funeral-home-wisconsin-sba", 22): "comma",
    (C % "glamping-utah-usda", 32): "colon", (C % "glamping-utah-usda", 33): "comma",
    (C % "hotel-south-carolina-sba", 32): "comma", (C % "hotel-south-carolina-sba", 33): "comma",
    (C % "marina-maryland-sba", 18): "colon", (C % "marina-maryland-sba", 19): "comma",
    (C % "meat-processing-georgia-usda", 31): "comma", (C % "meat-processing-georgia-usda", 32): "comma",
    (C % "meat-processing-north-carolina-usda", 31): "colon", (C % "meat-processing-north-carolina-usda", 32): "colon",
    (C % "multifamily-arizona-agency", 26): "colon", (C % "multifamily-arizona-agency", 29): "comma",
    (C % "multifamily-florida-agency", 29): "comma", (C % "multifamily-florida-agency", 30): "comma",
    (C % "multifamily-new-york-agency", 15): "semicolon", (C % "multifamily-new-york-agency", 16): "comma",
    (C % "multifamily-north-carolina-agency", 27): "comma", (C % "multifamily-north-carolina-agency", 28): "comma",
    (C % "multifamily-north-carolina-agency", 35): "comma", (C % "multifamily-north-carolina-agency", 36): "comma",
    # the real pair is "headquarters (Walmart, Tyson Foods, and J.B. Hunt)"; "J.B." hid it from the splitter
    (C % "qsr-arkansas-sba", 17): "open", (C % "qsr-arkansas-sba", 18): "close", (C % "qsr-arkansas-sba", 19): "comma",
    (C % "qsr-georgia-sba", 11): "colon", (C % "qsr-georgia-sba", 12): "comma",
    (C % "qsr-georgia-sba", 16): "colon", (C % "qsr-georgia-sba", 18): "comma",
    (C % "qsr-georgia-sba", 27): "comma", (C % "qsr-georgia-sba", 28): "comma",
    (C % "restaurant-missouri-sba", 23): "semicolon", (C % "restaurant-missouri-sba", 24): "comma",
    (C % "rv-boat-storage-california-sba", 13): "colon", (C % "rv-boat-storage-california-sba", 14): "colon",
    (C % "rv-park-maine-usda", 12): "comma", (C % "rv-park-maine-usda", 14): "comma",
    (C % "rv-park-maine-usda", 23): "comma", (C % "rv-park-maine-usda", 24): "comma",
    (C % "truck-stop-georgia-sba", 12): "comma", (C % "truck-stop-georgia-sba", 13): "colon",
    (S % "georgia", 21): "colon", (S % "georgia", 23): "comma",
    (S % "maryland", 13): "comma", (S % "maryland", 14): "colon",
    (S % "mississippi", 5): "colon", (S % "mississippi", 6): "comma",
    (S % "nevada", 22): "comma", (S % "nevada", 23): "comma",
}
SWEEP_BASE = "c203580"
MARK = "\x00%d\x00"


def replay(rel, dec):
    """The post-sweep text with each target dash's output wrapped in markers."""
    pre = subprocess.run(["git", "-C", ROOT, "show", f"{SWEEP_BASE}:{rel}"], capture_output=True, check=True).stdout.decode("utf-8")
    ds = [{"file": rel, "n": n, "decision": d} for (f, n), d in dec.items() if f == rel]
    tmp = os.path.join(ROOT, ".fix_crosspairs.tmp")
    with open(tmp, "w", encoding="utf-8") as fh:
        fh.write(pre)
    out, last, n = [], 0, 0
    for m in dashes.DASH.finditer(pre):
        out.append(pre[last:m.start()])
        out.append(m.group(0) if (rel, n) not in FIX else (MARK % n) + m.group(0) + (MARK % n))
        last = m.end(); n += 1
    out.append(pre[last:])
    os.remove(tmp)
    return "".join(out)


def main(argv):
    only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
    skip = set(argv[argv.index("--skip") + 1].split(",")) if "--skip" in argv else set()
    dec = {}
    for l in open(os.path.join(ROOT, "docs", "web-fsc-4", "dashes", "merged.jsonl"), encoding="utf-8"):
        d = json.loads(l); dec[(d["file"], d["n"])] = d["decision"]
    for rel in sorted({f for f, n in FIX}):
        slug = rel.split("/")[1]
        if (only and slug not in only) or slug in skip:
            continue
        cur = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        sweep = subprocess.run(["git", "-C", ROOT, "show", f"c21b055:{rel}"], capture_output=True, check=True).stdout.decode("utf-8")
        for (f, n), new in sorted(FIX.items(), key=lambda x: -x[0][1]):
            if f != rel:
                continue
            old = dec[(f, n)]
            # what the sweep wrote for this dash, and 40 characters of context either side in the sweep output
            marked = replay(rel, dec)
            a = marked.index(MARK % n); b = marked.index(MARK % n, a + 1)
            # rebuild the sweep output position: apply the sweep to the marked text minus this one dash
            plain_before = re.sub("\x00\\d+\x00", "", marked[:a])
            seg = dashes.DASH.match(marked, a + len(MARK % n)).group(0)
            pos_pre = len(plain_before)
            # locate the same dash in the sweep output by replaying the sweep on the pre-sweep text
            pre = re.sub("\x00\\d+\x00", "", marked)
            k = 0; outpos = None; acc = []; last = 0
            for m in dashes.DASH.finditer(pre):
                d = dec[(rel, k)]
                kind = "em" if re.fullmatch(dashes.EM, m.group(2)) else "en"
                r = (m.group(1) + "-" + m.group(3)) if (kind == "en" and d == "hyphen") else dashes.replacement(d, m.group(1), m.group(3), kind)
                chunk = pre[last:m.start()]
                if d in ("comma", "open-comma", "close-comma", "colon", "semicolon", "stop", "close", "close-paren"):
                    if "\n" in m.group(1):
                        r = r.lstrip("\n \t"); chunk = chunk.rstrip(" \t")
                    else:
                        chunk = chunk.rstrip(" \t")
                if d in ("open", "open-paren") and "\n" in m.group(1):
                    r = m.group(1) + "("
                acc.append(chunk)
                if k == n:
                    outpos = (sum(len(x) for x in acc), r)
                acc.append(r); last = m.end(); k += 1
            start, wrote = outpos
            out_text = "".join(acc) + pre[last:]
            assert out_text[start:start + len(wrote)] == wrote
            left = out_text[max(0, start - 40):start]; right = out_text[start + len(wrote):start + len(wrote) + 40]
            # the sweep's output for this dash is unique in the current file by its context
            hits = [m.start() for m in re.finditer(re.escape(left[-24:] + wrote + right[:24]), cur)]
            if len(hits) != 1:
                hits = [m.start() for m in re.finditer(re.escape(left[-14:] + wrote + right[:14]), cur)]
            if len(hits) != 1:
                raise SystemExit(f"{rel} dash {n}: {len(hits)} matches for {left[-24:]!r}+{wrote!r}+{right[:24]!r}")
            p = hits[0] + len(left[-24:]) if (left[-24:] + wrote + right[:24]) in cur else hits[0] + len(left[-14:])
            ws_after = " " if not wrote.endswith(("\n", " ")) and wrote.strip() in ("(",) else ""
            if new == "open":
                rep = " (" if not wrote.startswith("\n") else wrote
            elif new == "close":
                rep = ")" + (" " if (wrote.endswith(" ") or wrote.strip() == "(") else "")
            else:
                mark = {"comma": ",", "colon": ":", "semicolon": ";"}[new]
                if wrote.strip() == "(":          # was an opening parenthesis: "X (Y" -> "X, Y"
                    lead = wrote[:-1]
                    rep = mark + (lead if "\n" in lead else " ")
                elif wrote.startswith(")"):       # was a closing parenthesis: "Y) Z" -> "Y, Z"
                    rep = mark + wrote[1:]
                else:                              # was a colon or comma
                    rep = mark + wrote[1:]
            cur = cur[:p] + rep + cur[p + len(wrote):]
            print(f"{rel} dash {n}: {old} {wrote!r} -> {new} {rep!r}")
        open(os.path.join(ROOT, rel), "w", encoding="utf-8").write(cur)

if __name__ == "__main__":
    main(sys.argv[1:])
