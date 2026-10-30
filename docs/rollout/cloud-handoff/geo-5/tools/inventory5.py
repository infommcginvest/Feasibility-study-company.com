#!/usr/bin/env python3
"""GEO-5: write the eight states' research into the research inventory (~/Downloads/FSC Deep Searches 2/) in its own format.

    python3 inventory5.py [--write]

Reads the GEO-5 working files (drafts/geo-5/research/ST-<STATE>.md, ST-<STATE>-2.md where present, MT-<STATE>.md: the
11-column tables of D3) and writes, per state, one ST and one MT file in the inventory's shape, as ST-MONTANA and MT-MONTANA
have it: line 1 the bare Research ID; a dated H1; a method note; a TL;DR; numbered sections, each a table with the columns
| Item | Value | Period | Source (publisher, title, date) | URL | Primary or secondary |; "Not found"; numbered "Sources"; and the
working file's "Doors closed" and "Hygiene" notes. A supplement file's rows join its state's ST file as further sections.
Every value, period, title, date and URL is carried over unchanged; nothing is summarised or rewritten.

Also writes drafts/geo-5/research/INVENTORY-MAP.tsv: old id (file line) -> new file and line, so every fact-sheet,
pre-count and review reference to a working file resolves in the inventory. Without --write it only reports.
"""
import os
import re
import sys

HOME = os.path.expanduser("~")
SRC = HOME + "/Downloads/fsc-rollout/drafts/geo-5/research/"
INV = HOME + "/Downloads/FSC Deep Searches 2/"
STATES = {"COLORADO": "Colorado", "VIRGINIA": "Virginia", "SOUTH-DAKOTA": "South Dakota", "NORTH-DAKOTA": "North Dakota",
          "ALASKA": "Alaska", "WYOMING": "Wyoming", "DISTRICT-OF-COLUMBIA": "District of Columbia", "VERMONT": "Vermont"}
HEAD = "| Item | Value | Period | Source (publisher, title, date) | URL | Primary or secondary |"
SEP = "|---|---|---|---|---|---|"


def cells(line):
    s = line.strip()
    return [c.strip() for c in s[1:-1].split("|")] if s.startswith("|") and s.endswith("|") else None


def parse(path):
    """-> (sections, notfound, tail): sections = [(heading, [(old_line, row dict)])]; tail = other '##' blocks kept verbatim."""
    sections, notfound, tail = [], [], []
    head, cur, mode = None, None, "body"
    for n, line in enumerate(open(path, encoding="utf-8"), 1):
        line = line.rstrip("\n")
        if line.startswith("## "):
            title = line[3:].strip()
            if re.match(r"(?i)(doors closed|hygiene)", title):
                mode = "tail"
                tail.append([title, []])
                continue
            mode = "body"
            cur = (title, [])
            sections.append(cur)
            head = None
            continue
        if mode == "tail":
            tail[-1][1].append(line)
            continue
        if line.startswith("NOT FOUND"):
            notfound.append((cur[0] if cur else "", line.split(":", 1)[1].strip() if ":" in line else line))
            continue
        c = cells(line)
        if c is None or cur is None:
            continue
        low = [x.lower() for x in c]
        if "value" in low and "url" in low:
            head = low
            continue
        if head is None or all(set(x) <= set("-: ") for x in c) or len(c) != len(head):
            continue
        cur[1].append((n, dict(zip(head, c))))
    return sections, notfound, tail


def get(d, k):
    for h, v in d.items():
        if h.startswith(k):
            return v
    return ""


def row6(d):
    item = get(d, "what") or get(d, "topic")
    pub, title, date = get(d, "publisher"), get(d, "title"), get(d, "published")
    src = f'{pub}, "{title}"' + (f", {date}" if date and date.lower() != "undated" else ", undated")
    kind = get(d, "kind").capitalize() or "Primary"
    note = get(d, "note")
    if note:
        kind += f" ({note})"
    return "| " + " | ".join(x.replace("|", "/") for x in (item, get(d, "value"), get(d, "period"), src, get(d, "url"), kind)) + " |"


def build(kind, st, name, parts):
    """parts: [(working file id, path)] -> (text, map [(old id, old line, new line)])."""
    out, amap, srcs = [], [], []
    rid = f"{kind}-{st}"
    if kind == "ST":
        h1 = f"# {name} State Reference Page: Evidence for Commercial Project Feasibility (as of 28 October 2026)"
    else:
        h1 = f"# {name} Market Evidence Pack: Growth, Employment, Supply and Local Rules by Market (as of 28 October 2026)"
    out += [rid, "", h1, ""]
    out.append("**Method note.** Researched for GEO-5 (feasibility-study-company.com) on 28 October 2026 from public web sources, "
               "one figure per row, each row with the publisher's title as the researcher recorded it, its publication or release "
               "date and the URL the researcher read it on. The last column's parentheses carry the researcher's note: secondary "
               "rows name the original publisher there, and rows resting on a search-result excerpt say snippet. Rows marked "
               "undated have no publication date and are context only. Values are as the sources print them; a row the "
               "researcher marked derived says so. The GEO-5 pre-counts (drafts/geo-5/facts/) record which rows count. Working files: "
               + ", ".join(f"`{w}`" for w, _ in parts) + " (GEO-5 drafts folder); the row map is INVENTORY-MAP.tsv there.")
    out.append("")
    allsecs, allnf, alltail = [], [], []
    for wid, path in parts:
        secs, nf, tail = parse(path)
        tag = " (supplement of 28 October 2026)" if wid.endswith("-2") else ""
        allsecs += [(t + tag, rows, wid) for t, rows in secs if rows]
        allnf += [(t + tag, x) for t, x in nf]
        alltail += tail
    out.append("## TL;DR")
    for i, (t, rows, _) in enumerate(allsecs, 1):
        out.append(f"- Section {i}, {t}: {len(rows)} dated or labelled rows.")
    out.append("")
    for i, (t, rows, wid) in enumerate(allsecs, 1):
        out += [f"## {i}. {t}", "", HEAD, SEP]
        for old, d in rows:
            out.append(row6(d))
            amap.append((wid, old, len(out)))
            s = (get(d, "publisher"), get(d, "title"), get(d, "published"), get(d, "url"))
            if s not in srcs:
                srcs.append(s)
        out.append("")
    out += ["## What changed since January 2025", "",
            "The dated events and releases of 2025 and 2026 sit in the sections above with their own dates; this pack adds no summary of them.", "",
            "## Not found", ""]
    out += [f"- {t}: {x}" for t, x in allnf] or ["- None recorded."]
    out += ["", "## Sources", ""]
    out += [f'{i}. {p}, "{t}"' + (f", {d}" if d and d.lower() != "undated" else "") + f". {u}" for i, (p, t, d, u) in enumerate(srcs, 1)]
    for t, lines in alltail:
        out += ["", f"## {t}"] + [l for l in lines]
    return "\n".join(out).rstrip() + "\n", amap


def main(write):
    maps = []
    for st, name in STATES.items():
        for kind in ("ST", "MT"):
            parts = [(f"{kind}-{st}", SRC + f"{kind}-{st}.md")]
            if kind == "ST" and os.path.exists(SRC + f"ST-{st}-2.md"):
                parts.append((f"ST-{st}-2", SRC + f"ST-{st}-2.md"))
            text, amap = build(kind, st, name, parts)
            title = (f"{name} State Reference Page Commercial Project Feasibility Evidence, October 2026" if kind == "ST"
                     else f"{name} Market Evidence Pack Growth, Employment, Supply and Local Rules, October 2026")
            fn = f"{kind}-{st} - {title}.md"
            bad = re.findall(r"[–—]", text)
            print(f"{fn}: {len(text.splitlines())} lines, {len(amap)} rows, dashes {len(bad)}")
            if write:
                if os.path.exists(INV + fn):
                    raise SystemExit(f"refusing to overwrite {fn}")
                open(INV + fn, "w", encoding="utf-8").write(text)
            maps += [(w, o, fn, n) for w, o, n in amap]
    if write:
        with open(SRC + "INVENTORY-MAP.tsv", "w", encoding="utf-8") as f:
            f.write("working_id\tworking_line\tinventory_file\tinventory_line\n")
            for w, o, fn, n in maps:
                f.write(f"{w}\t{o}\t{fn}\t{n}\n")
    print("rows mapped", len(maps))


if __name__ == "__main__":
    main("--write" in sys.argv)
