#!/usr/bin/env python3
"""GEO-4 writer self-check for one page source draft.

    python3 srccheck.py drafts/geo-5/pages/<state>/<slug>.html

The assignment is read from drafts/geo-5/assign/<state>/<slug>.json. Prints PROBLEM lines and a
summary; exit 1 if any problem. Checks: front matter JSON and required keys; dashes; banned names;
credential after a name; citation numbers in range; every source entry has publisher, title,
date and an absolute url; section ids unique and not reserved; every figure-like number in the
body or front matter is a value of an allowed fact (or inside an sba:/mkt: marker); every block
holding a figure carries a citation; approximate body words against the type's range.
"""
import html as htmllib
import importlib.util
import json
import os
import re
import sys

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
DRAFTS = os.path.dirname(HERE)
WT = os.path.expanduser("~/Downloads/wt-rollout-geo-5")
DASHES = re.compile(r"–|—|&[mn]dash;|&#821[12];|&#x201[34];|%E2%80%9[34]|\\u201[34]", re.I)
FORBIDDEN = re.compile("|".join(["m" + "mcg", "moh" + "elsky", "union ?" + "metric", "inno" + "wave", "analytics" + r"\.loan",
                                 "loan analytic" + "s", "feasibility-study-consulta" + "nt", "wert-?bera" + "ter"]), re.I)
REGION = re.compile(r"<!--(sba|mkt|mktsrc|case):([a-z0-9_./:-]+)( \{.*?\})?-->(.*?)<!--/\1:\2-->", re.S)
# words as the rendered page counts them: body prose plus section eyebrows, headings and ledes, the hero, stats and CTA;
# the range keeps a small margin under ruling 3's caps
RANGES = {"state": (4600, 7800), "metro": (2050, 3400)}


def load_pc():
    spec = importlib.util.spec_from_file_location("pagecheck", os.path.join(WT, "docs/web-fsc-6/tools/pagecheck.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(path):
    pc = load_pc()
    probs = []
    s = open(path, encoding="utf-8").read()
    parts = s.split("\n---\n", 1)
    if not s.startswith("---\n") or len(parts) < 2:
        print("PROBLEM front matter must open with --- and close with a line of ---")
        return 1
    try:
        fm = json.loads(parts[0][4:])
    except json.JSONDecodeError as e:
        print(f"PROBLEM front matter JSON: {e}")
        return 1
    body = parts[1]
    rel = os.path.relpath(path, os.path.join(DRAFTS, "pages"))
    apath = os.path.join(DRAFTS, "assign", os.path.splitext(rel)[0] + ".json")
    asg = json.load(open(apath)) if os.path.exists(apath) else None
    if asg is None:
        probs.append(f"no assignment at {apath}")
    for k in ["type", "url", "title", "description", "h1", "eyebrow", "hero_sub", "breadcrumb", "service", "published",
              "updated", "stats", "faq", "cta", "sources_lede", "sources"]:
        if k not in fm:
            probs.append(f"front matter lacks {k}")
    d = fm.get("description", "")
    if not 140 <= len(d) <= 160:
        probs.append(f"description is {len(d)} characters (140 to 160)")
    if len(fm.get("title", "")) > 76:
        probs.append(f"title is {len(fm['title'])} characters (about 60)")
    if DASHES.search(s):
        probs.append(f"dashes: {len(DASHES.findall(s))}")
    if FORBIDDEN.search(s):
        probs.append("banned name present: " + FORBIDDEN.search(s).group(0))
    if re.search(r"otava,? *(ph\.?d|ccim|mai)", s, re.I):
        probs.append("credential typed after a name")
    srcs = fm.get("sources", [])
    for i, e in enumerate(srcs, 1):
        for f in ("publisher", "title", "date", "url"):
            if not e.get(f):
                probs.append(f"source {i} lacks {f}")
        if not str(e.get("url", "")).startswith(("http://", "https://")):
            probs.append(f"source {i} url not absolute")
    cites = [int(n) for g in re.findall(r"\[\^([\d,\s]+)\]", s) for n in re.split(r"[,\s]+", g) if n]
    bad = sorted({n for n in cites if n < 1 or n > len(srcs)})
    if bad:
        probs.append(f"citations out of range: {bad}")
    unused = sorted(set(range(1, len(srcs) + 1)) - set(cites))
    if unused:
        probs.append(f"sources never cited: {unused}")
    ids = re.findall(r'<section id="([^"]+)"', body)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        probs.append(f"duplicate section ids {dup}")
    for i in ids:
        if i in ("faq", "sources", "main", "worked-cases"):
            probs.append(f"reserved section id {i}")
    if re.search(r"<section(?![^>]*\bid=)", body):
        probs.append("a section without an id")
    # allowed values
    allowed = []
    if asg:
        sheet = json.load(open(os.path.expanduser(asg["fact_sheet"])))
        byid = {f["id"]: f for f in sheet["facts"]}
        for fid in asg.get("facts", []) + asg.get("context_facts", []):
            if fid in byid:
                v = byid[fid]["value"]
                for raw, k in pc.figures_in(v) + pc.figures_in("x " + re.sub(r"(?<![\w.])[-\u2212+](?=\d)", "", v) + " residents"):
                    allowed.append(k)  # a loss recorded as -843 may be written as lost 843
                for raw, k in pc.figures_in(re.sub(r"\$(\d[\d.,]*)-(\d[\d.,]*) (million|billion)", r"$\1 \3 to $\2 \3", v)):
                    allowed.append(k)  # a range recorded as $4.0-4.2 million written out in full
                for tok in re.findall(r"(?<![\w.$])\d[\d,]*(?:\.\d+)?(?![\w%])", v)[:1]:
                    for raw, k in pc.figures_in("x " + tok + " residents"):
                        allowed.append(k)  # a bare count followed by words the counter does not read as a unit
    idx = pc.NumberIndex()
    for k in allowed:
        idx.add(k)
    stripped = REGION.sub(" ", body)
    nocount = re.compile(r"<span data-fsc-nocount>.*?</span>", re.S)  # values the official counter skips (pagecheck.py)
    stripped_n = nocount.sub(" ", stripped)
    fm_text = " ".join([fm.get("hero_sub", ""), fm.get("description", "")] + [f"{x.get('num', '')} {('million' if x.get('unit') == 'M' else 'billion' if x.get('unit') == 'B' else x.get('unit', ''))} {x.get('label', '')}" for x in fm.get("stats", [])]
                       + [q.get("q", "") + " " + q.get("a", "") for q in fm.get("faq", {}).get("items", [])])
    fm_text = nocount.sub(" ", REGION.sub(" ", fm_text))
    unl = []
    for raw, k in pc.figures_in(htmllib.unescape(re.sub(r"<[^>]+>", " ", stripped_n)) + " " + htmllib.unescape(fm_text)):
        if pc.YEAR.match(pc.norm(raw)):
            continue
        if not idx.has(k):
            unl.append(raw)
    if unl and asg:
        probs.append(f"{len(unl)} number(s) not among the assigned facts: {sorted(set(unl))[:40]}")
    soup = BeautifulSoup(stripped, "lxml")
    nocite = 0
    for b in soup.find_all(["p", "li", "tr"]):
        if b.name != "tr" and b.find(["p", "li", "tr"]):
            continue
        t = b.get_text(" ")
        figs = [r for r, k in pc.figures_in(t) if not pc.YEAR.match(pc.norm(r))]
        if figs and "[^" not in t:
            nocite += 1
    if nocite:
        probs.append(f"{nocite} block(s) hold a figure without a citation")
    # approximate body words
    soup = BeautifulSoup(body, "lxml")
    for t in soup.find_all("table"):
        t.decompose()
    attrs = " ".join(m for m in re.findall(r'data-(?:eyebrow|h2|lede)="([^"]*)"', body))
    extra = " ".join([fm.get("h1", ""), fm.get("eyebrow", ""), re.sub(r"\[\^[\d,\s]+\]", " ", fm.get("hero_sub", "")),
                      (fm.get("hero_secondary") or {}).get("text", ""), fm.get("stats_label", ""),
                      " ".join(f"{x.get('num', '')} {x.get('unit', '')} {x.get('label', '')}" for x in fm.get("stats", [])),
                      fm.get("cta", {}).get("h2", ""), fm.get("cta", {}).get("p", ""), "Request a methodology briefing " * 2])
    words = len(pc.tokens(soup.get_text(" ") + " " + htmllib.unescape(attrs) + " " + htmllib.unescape(extra)))
    lo, hi = RANGES.get(fm.get("type"), (0, 10 ** 9))
    if not lo <= words <= hi:
        probs.append(f"body words about {words} (range {lo} to {hi})")
    used = set()
    if asg:
        page_idx = pc.NumberIndex()
        for raw, k in pc.figures_in(htmllib.unescape(re.sub(r"<[^>]+>", " ", stripped)) + " " + htmllib.unescape(fm_text)):
            page_idx.add(k)
        for fid in asg.get("facts", []):
            f = byid.get(fid)
            ks = pc.figures_in(f["value"]) if f else []
            if ks and page_idx.has(ks[0][1]):
                used.add(fid)
    mk = len(re.findall(r"<!--mkt:", body))
    for p in probs:
        print("PROBLEM", p)
    print(f"summary: type {fm.get('type')} words~{words} sources {len(srcs)} assigned facts used {len(used)}"
          + (f"/{len(asg.get('facts', []))} (min_research {asg.get('min_research')})" if asg else "") + f" mkt markers {mk}")
    if asg and len(used) < asg.get("min_research", 0):
        print(f"PROBLEM assigned facts used {len(used)} under min_research {asg.get('min_research')}")
        return 1
    return 1 if probs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
