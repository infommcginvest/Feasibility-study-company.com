#!/usr/bin/env python3
"""WEB-FSC-6 page checks: body words, unique sourced figures, shingle overlap, clean text, case components.

    python3 docs/web-fsc-6/tools/pagecheck.py /states/texas/houston/ [more urls]
    python3 docs/web-fsc-6/tools/pagecheck.py --pilot            all 31 pilot pages
    python3 docs/web-fsc-6/tools/pagecheck.py --pilot --json out.json
    options: --figures (list counted figures), --overlap N (show the N highest overlaps)

Definitions (the gates in the charter):
- Body words: words in <main> outside tables, the sources section, the FAQ section, the
  breadcrumb, mesh regions, scripts and styles.
- Overlap: 8-word shingles of lowercase tokens over <main> text minus scripts, styles and the
  sources section; overlap = shared shingles / the smaller page's shingle count. Every other
  served page of the site is compared.
- Unique figures: a number with a unit ($, %, x, thousands separators, decimals, or a counted
  unit word) inside a block (p, li, tr, stat, details) that carries a citation, outside sba:,
  case: and mkt: regions, that appears nowhere in the text of any other served page.
"""
import argparse
import json
import os
import re
import sys

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

TEXAS_METROS = ["houston", "dallas-fort-worth", "austin", "san-antonio", "mcallen", "el-paso", "lubbock", "corpus-christi"]
GAS_SUBTYPES = ["branded-fuel", "unbranded-independent", "convenience-no-fuel", "foodservice-qsr", "interstate-highway", "ev-charging"]
CASES = ["gas-station-texas-sba", "gas-station-florida-sba", "gas-station-alabama-sba", "gas-station-georgia-sba",
         "gas-station-versailles-ohio-sba", "truck-stop-texas-sba", "hotel-texas-sba", "rv-park-texas-usda",
         "car-wash-texas-sba", "rv-boat-storage-texas-sba", "auto-dealership-texas-sba", "assisted-living-texas-hud",
         "meat-processing-texas-usda", "travel-center-hankamer-texas-usda", "lodging-retreat-johnson-city-texas-sba"]
PILOT = (["/states/texas/"] + [f"/states/texas/{m}/" for m in TEXAS_METROS] + ["/asset-classes/gas-station-and-c-store/"]
         + [f"/asset-classes/gas-station-and-c-store/{s}/" for s in GAS_SUBTYPES] + [f"/case-studies/{c}/" for c in CASES])
REBUILT = {"/states/texas/", "/asset-classes/gas-station-and-c-store/"} | {f"/case-studies/{c}/" for c in CASES
           if c not in ("gas-station-versailles-ohio-sba", "travel-center-hankamer-texas-usda", "lodging-retreat-johnson-city-texas-sba")}
RANGES = {"state": (6000, None), "metro": (2500, 3500), "hub": (8000, 10000), "subtype": (2000, 3000), "case": (4500, 6500)}
CASE_SECTIONS = ["at-a-glance", "market-conclusion", "demand", "competitors", "site", "revenue", "opex", "sources-uses",
                 "loan", "pro-forma", "dscr", "break-even", "sensitivity", "risks", "lender-conditions", "faq", "sources"]
CASE_TABLES = ["glance", "revenue", "opex", "uses", "sources", "loan", "proforma", "dscr", "determination", "verdict",
               "breakeven", "sensitivity"]
DISCLOSURE = ("Representative worked example. The site, sponsor and project are hypothetical. The market evidence comes "
              "from the public sources listed below, with their dates. This page shows how the market analysis is built "
              "and how it sets the loan. It is not a client engagement.")
DASHES = re.compile(r"–|—|&[mn]dash;|&#821[12];|&#x201[34];", re.I)
FORBIDDEN = re.compile("|".join(["m" + "mcg", "moh" + "elsky", "union ?" + "metric", "inno" + "wave", "analytics" + r"\.loan",
                                 "loan analytic" + "s", "feasibility-study-consulta" + "nt", "wert-?bera" + "ter"]), re.I)
SBA_REQUIRES = re.compile(r"(?<![\"“]the )(required by (the )?SBA|SBA requires|SBA mandates|SBA-required)[^.]{0,80}feasibility|"
                          r"feasibility stud(y|ies)[^.]{0,80}(required by (the )?SBA|SBA requires|SBA mandates|SBA-required)", re.I)
UNITS = (r"acres?|sites?|keys|rooms|units|beds|residents|people|jobs|employees|workers|households|gallons|vehicles|cars|trucks|"
         r"stores|stations|locations|outlets|dealers|dealerships|square feet|sq ft|sf|miles|parcels|permits|homes|spaces|"
         r"pads|pumps|dispensers|positions|fueling positions|chargers|ports|head|pounds|lbs|students|visitors|visits|passengers|"
         r"listings|loans|establishments|firms|businesses|properties|hotels|campgrounds|facilities|plants|counties|trips|"
         r"vehicles per day|aadt|cents")
FIG = re.compile(r"(?<![\w.$])(\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand|trillion|[mbkt]\b))?"
                 r"|\d[\d,]*(?:\.\d+)?\s?(?:%|percent\b|x\b)"
                 r"|\d{1,3}(?:,\d{3})+(?:\.\d+)?"
                 r"|\d+\.\d+"
                 r"|\d{2,}(?=\s(?:" + UNITS + r")\b))", re.I)
YEAR = re.compile(r"^(19|20)\d\d$")


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def served_pages():
    out = {}
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", "docs", "src", "node_modules", "netlify", "_bundles")]
        if "index.html" in files:
            rel = os.path.relpath(d, ROOT)
            url = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
            out[url] = os.path.join(d, "index.html")
    return out


def strip_regions(html_text, names):
    pat = re.compile(r"<!--(" + "|".join(names) + r"):([a-z0-9_.:-]+)( \{.*?\})?-->(.*?)<!--/\1:\2-->", re.S)
    return pat.sub(" ", html_text)


def main_soup(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    main = soup.find("main")
    if main is None:
        main = soup.body or soup
    for t in main.find_all(["script", "style"]):
        t.decompose()
    return main


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:[.,'][a-z0-9]+)*", text.lower())


def overlap_text(html_text):
    main = main_soup(html_text)
    s = main.find(id="sources")
    if s:
        s.decompose()
    return main.get_text(" ")


def body_words(html_text):
    main = main_soup(strip_regions(html_text, ["mesh"]))
    for sel in ["#sources", "#faq"]:
        el = main.select_one(sel)
        if el:
            el.decompose()
    for t in main.find_all("table"):
        t.decompose()
    for t in main.select("nav.breadcrumb"):
        t.decompose()
    return len(tokens(main.get_text(" ")))


def shingles(text, n=8):
    tk = tokens(text)
    return {" ".join(tk[i:i + n]) for i in range(len(tk) - n + 1)}


def norm(fig):
    f = fig.lower().replace(" ", "").replace("percent", "%")
    return f.rstrip(".,")


def all_numbers(text):
    return {norm(m.group(1)) for m in FIG.finditer(text)}


def sourced_figures(html_text):
    main = main_soup(strip_regions(html_text, ["sba", "case", "mkt", "mesh"]))
    s = main.find(id="sources")
    if s:
        s.decompose()
    figs = {}
    blocks = main.find_all(["p", "li", "tr"]) + main.select("div.stat")
    for b in blocks:
        if b.name != "tr" and b.find(["p", "li", "tr"]):
            continue
        if not (b.select("a.cite") or b.select("sup.fn")):
            continue
        for m in FIG.finditer(b.get_text(" ")):
            raw = m.group(1)
            n = norm(raw)
            if YEAR.match(n):
                continue
            figs.setdefault(n, raw.strip())
    return figs


def page_type(url):
    if url == "/states/texas/":
        return "state"
    if url.startswith("/states/texas/"):
        return "metro"
    if url == "/asset-classes/gas-station-and-c-store/":
        return "hub"
    if url.startswith("/asset-classes/gas-station-and-c-store/"):
        return "subtype"
    if url.startswith("/case-studies/"):
        return "case"
    return "other"


def siblings(url):
    t = page_type(url)
    if t == "metro":
        return [f"/states/texas/{m}/" for m in TEXAS_METROS]
    if t == "subtype":
        return [f"/asset-classes/gas-station-and-c-store/{s}/" for s in GAS_SUBTYPES]
    if t == "case":
        return [f"/case-studies/{c}/" for c in CASES]
    return []


def case_checks(url, html_text):
    problems = []
    soup = BeautifulSoup(html_text, "lxml")
    ids = {t.get("id") for t in soup.find_all(id=True)}
    for sid in CASE_SECTIONS:
        if sid not in ids:
            problems.append(f"missing section #{sid}")
    slug = url.strip("/").split("/")[-1]
    for t in CASE_TABLES:
        if f"<!--case:{slug}.{t}-->" not in html_text:
            problems.append(f"missing case table {t}")
    hero = soup.select_one("section.hero")
    disc = hero.select_one(".capsule.disclosure") if hero else None
    if not disc or re.sub(r"\s+", " ", disc.get_text(" ")).strip() != DISCLOSURE:
        problems.append("disclosure box missing or altered")
    else:
        kids = [c for c in hero.select_one(".frame").find_all(recursive=False)]
        names = [(c.name, " ".join(c.get("class", []))) for c in kids]
        try:
            i_h1 = [n for n, _ in names].index("h1")
            if "disclosure" not in names[i_h1 + 2][1] and "disclosure" not in names[i_h1 + 1][1]:
                problems.append("disclosure box is not directly under the H1 and byline")
        except (ValueError, IndexError):
            problems.append("hero layout unexpected")
    comp = soup.find(id="competitors")
    if comp:
        rows = comp.select("table tbody tr")
        bad = [r for r in rows if not r.find("a", href=re.compile(r"^https?://"))]
        if not rows:
            problems.append("competitor census has no table rows")
        if bad:
            problems.append(f"{len(bad)} competitor row(s) without a confirming URL")
    return problems


def check(urls, pages, cache, show_figs=False, show_overlap=0):
    other_numbers = {}
    for u, p in pages.items():
        other_numbers[u] = all_numbers(overlap_text(cache[u]) if u in cache else "")
    shing = {u: shingles(overlap_text(cache[u])) for u in pages}
    results = []
    for url in urls:
        rec = {"url": url, "type": page_type(url), "problems": []}
        if url not in pages:
            rec["problems"].append("not built")
            results.append(rec)
            continue
        h = cache[url]
        rec["words"] = body_words(h)
        lo, hi = RANGES.get(rec["type"], (None, None))
        if lo and rec["words"] < lo:
            rec["problems"].append(f"body words {rec['words']} under {lo}")
        if hi and rec["words"] > hi:
            rec["problems"].append(f"body words {rec['words']} over {hi}")
        figs = sourced_figures(h)
        elsewhere = set()
        for u, nums in other_numbers.items():
            if u != url:
                elsewhere |= nums
        uniq = {k: v for k, v in figs.items() if k not in elsewhere}
        rec["figures_sourced"] = len(figs)
        rec["figures_unique"] = len(uniq)
        if show_figs:
            rec["unique_list"] = sorted(uniq.values())
        if len(uniq) < 25:
            rec["problems"].append(f"unique sourced figures {len(uniq)} under 25")
        mine = shing[url]
        ov = []
        for u, s in shing.items():
            if u == url or not mine or not s:
                continue
            shared = len(mine & s)
            if shared:
                ov.append((shared / min(len(mine), len(s)), u, shared))
        ov.sort(reverse=True)
        rec["overlap_max"] = round(ov[0][0] * 100, 2) if ov else 0.0
        rec["overlap_with"] = ov[0][1] if ov else None
        if show_overlap:
            rec["overlap_top"] = [(round(a * 100, 2), b, c) for a, b, c in ov[:show_overlap]]
        sib = set(siblings(url))
        rec["overlap_sibling_max"] = max([round(a * 100, 2) for a, b, _ in ov if b in sib] or [0.0])
        if ov and ov[0][0] >= 0.15:
            rec["problems"].append(f"overlap {rec['overlap_max']}% with {ov[0][1]}")
        if DASHES.search(h):
            rec["problems"].append(f"dashes: {len(DASHES.findall(h))}")
        if FORBIDDEN.search(h):
            rec["problems"].append("forbidden name present")
        txt = re.sub(r"<[^>]+>", " ", h)
        if SBA_REQUIRES.search(txt):
            rec["problems"].append("SBA-requires claim: " + SBA_REQUIRES.search(txt).group(0)[:100])
        if re.search(r"otava,? *(ph\.?d|ccim|mai)", h, re.I):
            rec["problems"].append("credential typed next to the name")
        for href in set(re.findall(r'href="(/[^"#?]*)', h)):
            target = os.path.join(ROOT, href.lstrip("/"))
            if href.endswith("/"):
                target = os.path.join(target, "index.html")
            if not os.path.exists(target) and not os.path.exists(target.rstrip("/")):
                rec["problems"].append(f"link to missing page {href}")
        if rec["type"] == "case":
            rec["problems"] += case_checks(url, h)
        results.append(rec)
    return results


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--pilot", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--overlap", type=int, default=0)
    a = ap.parse_args(argv)
    urls = PILOT if a.pilot else ["/" + u.strip("/") + "/" for u in a.urls]
    pages = served_pages()
    cache = {u: read(p) for u, p in pages.items()}
    res = check(urls, pages, cache, a.figures, a.overlap)
    for r in res:
        line = f"{r['url']:62} {r['type']:7} words {r.get('words', '-'):>6}  uniq figs {r.get('figures_unique', '-'):>4}  overlap {r.get('overlap_max', '-')}% ({r.get('overlap_with')})"
        print(line)
        for p in r["problems"]:
            print("    PROBLEM", p)
        if a.figures and r.get("unique_list"):
            print("    figures:", "; ".join(r["unique_list"]))
        if a.overlap and r.get("overlap_top"):
            for o in r["overlap_top"]:
                print("    overlap", o)
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    bad = sum(1 for r in res if r["problems"])
    print(f"{len(res)} page(s), {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
