#!/usr/bin/env python3
"""GEO-5: read the research tables (ST-<STATE>.md, MT-<STATE>.md), write a fact sheet per state and measure each file's
counted-figure yield before any page is written.

    python3 yield5.py [STATE ...]        (default: every state with research)

Rows: every markdown table row with the D3 columns (# | Topic | Value | What | Period | Published | Publisher | Title | URL | Kind | Note).
A fact's id is <file id> line <n> (the line of the row in the file), as the inventory's fact sheets cite rows.

Matcher: scripts/qa/pagecheck.py of ~/Downloads/wt-rollout-geo-5 (local main, which is what production serves) imported
unchanged. Index: every served page's overlap text and its numbered sources list (I71). The new pages are state pages (rank 1),
so any served page that holds a value by pagecheck's value and rounding rules takes it.

Classes (a fact counts toward the yield only when all hold):
  dated      the Published cell carries a date (I77 a or b; the reviewer confirms the kind); "undated" never counts (I86)
  figure     pagecheck reads a figure in the value
  market     the Note does not mark it single-property (I64) and the value is not research arithmetic (I55)
  free       no served page holds its first figure, and no other GEO-5 state's research holds it (both would lose it)
Within a state a value counts once. Primary and secondary are reported apart; secondary rows stay in the yield but are flagged.
"""
import importlib.util
import json
import os
import re
import sys
from collections import Counter, defaultdict

HOME = os.path.expanduser("~")
TREE = HOME + "/Downloads/wt-rollout-geo-5"
R = os.environ.get("GEO5_RESEARCH", HOME + "/Downloads/fsc-rollout/drafts/geo-5/research/")
OUT = os.environ.get("GEO5_FACTS", HOME + "/Downloads/fsc-rollout/drafts/geo-5/facts/")
STATES = ["COLORADO", "VIRGINIA", "SOUTH-DAKOTA", "NORTH-DAKOTA", "ALASKA", "WYOMING", "DISTRICT-OF-COLUMBIA", "VERMONT"]


def load_pc():
    spec = importlib.util.spec_from_file_location("pagecheck", TREE + "/scripts/qa/pagecheck.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    m.ROOT = TREE
    return m


def cells(line):
    s = line.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return None
    return [c.strip() for c in s[1:-1].split("|")]


def rows(path):
    fid = None
    out = []
    head = None
    section = ""
    for n, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        if n <= 3 and line.startswith("Research ID:"):
            fid = line.split(":", 1)[1].strip()
        if line.startswith("#"):
            section = line.strip("# \n")
        c = cells(line)
        if c is None:
            continue
        low = [x.lower() for x in c]
        if "value" in low and "url" in low:
            head = low
            continue
        if head is not None and len(c) != len(head) and not any(ch.isdigit() for ch in c[0]):
            head = None  # another table (doors closed, hygiene): not figure rows
            continue
        if head is None or all(set(x) <= set("-: ") for x in c):
            continue
        if len(c) != len(head):
            out.append({"line": n, "malformed": True, "raw": line.strip()[:200], "section": section})
            continue
        d = dict(zip(head, c))
        d["line"] = n
        d["section"] = section
        out.append(d)
    return fid, out


def get(d, *keys):
    for k in keys:
        for h in d:
            if h.startswith(k):
                return d[h]
    return ""


UNDATED = re.compile(r"^\s*(undated|n/?a|none|not dated|unknown|current|-)?\s*$", re.I)
ARITH = re.compile(r"\b(derived|arithmetic|computed|sum of|research calc)", re.I)


def build_index(pc):
    idx = {}
    for u, p in pc.served_pages(TREE).items():
        html = pc.read(p)
        ni = pc.NumberIndex()
        for _, k in pc.figures_in(pc.overlap_text(html)):
            ni.add(k)
        main = pc.main_soup(pc.strip_regions(html, ["mesh"]))
        s = main.find(id="sources")
        if s:
            for _, k in pc.figures_in(s.get_text(" ")):
                ni.add(k)
        idx[u] = ni
    return idx


def main(argv):
    pc = load_pc()
    want = [a.upper() for a in argv] or [s for s in STATES if os.path.exists(R + f"ST-{s}.md") or os.path.exists(R + f"MT-{s}.md")]
    allstates = [s for s in STATES + [w for w in want if w not in STATES] if os.path.exists(R + f"ST-{s}.md") or os.path.exists(R + f"MT-{s}.md")]
    idx = build_index(pc)
    facts = {}
    for st in allstates:
        fs = []
        import glob as _g
        paths = []
        for kind in ("ST", "MT"):
            paths += [(kind, q) for q in sorted(_g.glob(R + f"{kind}-{st}.md") + _g.glob(R + f"{kind}-{st}-[0-9].md"))]
        for kind, p in paths:
            fid, rs = rows(p)
            for d in rs:
                if d.get("malformed"):
                    fs.append({"id": f"{kind}-{st} line {d['line']}", "file": kind, "line": d["line"], "malformed": True, "raw": d["raw"]})
                    continue
                val = get(d, "value")
                figs = pc.figures_in(val)
                f = {
                    "id": f"{fid or kind + '-' + st} line {d['line']}", "file": kind, "line": d["line"], "section": d["section"],
                    "topic": get(d, "topic"), "value": val, "what": get(d, "what"), "period": get(d, "period"),
                    "published": get(d, "published"), "publisher": get(d, "publisher"), "title": get(d, "title"),
                    "url": get(d, "url"), "kind": get(d, "kind").lower(), "note": get(d, "note"),
                    "key": figs[0][1] if figs else None, "raw_fig": figs[0][0] if figs else None,
                }
                f["dated"] = not UNDATED.match(f["published"] or "")
                f["figure"] = bool(figs)
                f["market"] = "single-property" not in f["note"].lower() and not ARITH.search(f["note"] + " " + f["what"])
                f["secondary"] = f["kind"].startswith("second")
                f["taken"] = [u for u, ni in idx.items() if f["key"] is not None and ni.has(f["key"])][:5] if f["figure"] else []
                fs.append(f)
        facts[st] = fs
    # keys held by more than one GEO-5 state
    owners = defaultdict(set)
    for st, fs in facts.items():
        for f in fs:
            if f.get("key") is not None:
                owners[repr(f["key"])].add(st)
    report = []
    for st in want:
        fs = facts.get(st, [])
        seen = set()
        tally = Counter()
        for f in fs:
            if f.get("malformed"):
                tally["malformed"] += 1
                continue
            tally["rows_" + f["file"]] += 1
            f["shared_geo5"] = sorted(owners[repr(f["key"])] - {st}) if f.get("key") is not None else []
            ok = f["dated"] and f["figure"] and f["market"] and not f["taken"] and not f["shared_geo5"]
            k = repr(f["key"])
            f["countable"] = bool(ok and k not in seen)
            if f["countable"]:
                seen.add(k)
                tally["count_" + f["file"]] += 1
                tally["count_secondary" if f["secondary"] else "count_primary"] += 1
            for flag in ("dated", "figure", "market"):
                if not f[flag]:
                    tally["not_" + flag] += 1
            if f["figure"] and f["taken"]:
                tally["taken_by_site"] += 1
            if f.get("shared_geo5"):
                tally["shared_geo5"] += 1
        os.makedirs(OUT, exist_ok=True)
        json.dump({"state": st, "tree": TREE, "facts": fs}, open(OUT + f"{st.lower()}.facts.json", "w"), indent=1, default=repr)
        line = (f"{st}: rows ST {tally['rows_ST']} MT {tally['rows_MT']} | countable {tally['count_ST'] + tally['count_MT']} "
                f"(ST {tally['count_ST']}, MT {tally['count_MT']}; primary {tally['count_primary']}, secondary {tally['count_secondary']}) | "
                f"undated {tally['not_dated']}, no figure {tally['not_figure']}, not market {tally['not_market']}, "
                f"taken by site {tally['taken_by_site']}, shared with GEO-5 {tally['shared_geo5']}, malformed {tally['malformed']}")
        report.append(line)
        print(line)
    return report


if __name__ == "__main__":
    main(sys.argv[1:])
