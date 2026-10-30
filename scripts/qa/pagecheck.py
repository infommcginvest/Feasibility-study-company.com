#!/usr/bin/env python3
"""Page checks for the roll-out (FACTORY-2, generalized from WEB-FSC-6's pagecheck): body words, counted
figures (research and register apart), shingle overlap, clean text and the case components.

    python3 scripts/qa/pagecheck.py [--root DIR] URL [URL ...]
    python3 scripts/qa/pagecheck.py --manifest FILE        one URL per line (# comments allowed), or a tranche
                                                           record's JSON list
    python3 scripts/qa/pagecheck.py --factory              every page with a source under src/pages
    options:
      --stage ready|landing   which floors of amendment A6 apply (default landing)
      --new URL,URL           the tranche's pages: in a collision between two pages of the same rank, the page
                              already on the site keeps the figure and the new page loses it (amendment A4)
      --json OUT  --figures (list counted figures)  --overlap N (the N highest overlaps)

Definitions (ROLLOUT-1 rulings 3 and 5, amendments A4 and A6):
- Body words: words in <main> outside tables, the sources section, the FAQ section, the breadcrumb, mesh
  regions, scripts and styles.
- Overlap: 8-word shingles of lowercase tokens over <main> text minus scripts, styles, mesh regions and the
  sources section; overlap = shared shingles / the smaller page's shingle count, against every served page.
- A figure is a number with a unit ($, %, x, thousands separators, decimals, a scale word, or a counted unit
  word). A research figure sits in a block (p, li, tr, stat) that carries a citation, outside sba:, case:, mkt:
  and mesh: regions. A register figure is the value inside a mkt: region; it counts once per distinct
  (geography, series) pair, and at most register_cap of them count (src/types.json).
- A figure counts when no other served page carries it by value (rounded and rescaled repeats are the same
  figure), except that it belongs to the more specific page: case over metro or subtype over state or hub
  (amendment A4). Between two pages of the same rank, with --new, the page already on the site keeps it;
  otherwise neither counts it.

FSC-RESUME-1 tool fixes (integrator owner item O4; docs/rollout/int/PAGECHECK-CLOSE-1.md has the counts):
- nocount on mkt: regions. A register value that sits inside an element carrying data-fsc-nocount (or whose
  region holds such an element) is not a register figure. The value stays on the page for the repeat test: other
  pages still treat it as printed (I82).
- Two-significant-digit rounding. A figure written with exactly two significant digits ("$4.8 billion", "about
  9,700") is a rounding of a more precise figure of the same kind ("$4.81 billion", "9,692") on another page when
  both round to the same two digits AND either (a) the same scale word stands on both (thousand, million,
  billion, trillion, k, m, b, t), or (b) either text marks its value as approximate ("about", "roughly",
  "nearly", "almost", "some", "around", "more than", "approximately", "~") and the value is 1,000 or more.
  Plain numbers under 1,000 and percentages never take this path (2.5% against 2.54%, 12 against 12.4 stay
  distinct). Two digits agree by chance about once in ninety pairs: with that test alone 35% of all counted
  figures on the site were "repeats". So a two-digit match counts only with evidence of one fact (NumberIndex,
  rounded_repeats): the two places share content words and either share three with two of them rare on the
  site, or two different figures of one sentence here match two different figures of one sentence on the same
  other page. Three and more digits keep the earlier rule (the coarser written precision decides).
- Code and statute numbers are not figures: a number right after "section", "sec.", "s.", "ss.", "chapter",
  "CFR", "U.S.C.", "Stat.", "Code", "Act", "Title", "Rule", "HB", "SB", "AB", "LD", "Ordinance", "Order",
  "Docket", "Article" or a code reporter (R.C., G.S., C.R.S., ...); a bare dotted number of four or five digits
  or of the shape ddd.ddd with no unit or scale word after it (2116.1, 4303.29, 104.001); a dotted number
  followed by "(b)" or by a further dotted segment (120.160(b), 120.160.2).
- Other pages' numbered sources lists count as page content (I71) when the repeat test indexes them: a value a
  served page prints only in its sources (publisher, title, annotation; URLs excluded) is taken. A page's own
  sources list stays out of its own counted figures.
"""
import argparse
import json
import math
import os
import re
import sys

from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEFAULT_TYPES = {   # METHOD-1's planned types, used until src/types.json carries them (ROLLOUT-1 ruling 3)
    "practice": {"range": [5000, 9000], "figures": "reference"},
    "framework": {"range": [2500, 5000], "figures": "short"},
    "note": {"range": [2500, 5000], "figures": "short"},
}
DEFAULT_FIGURES = {
    "reference": {"ready_counted": 30, "ready_research": 20, "register_cap": 10, "landing_counted": 25, "landing_research": 15},
    "short": {"ready_counted": 18, "ready_research": 10, "register_cap": 8, "landing_counted": 15, "landing_research": 8},
}
RANK = {"state": 1, "hub": 1, "metro": 2, "subtype": 2, "case": 3}   # amendment A4: case over metro over state, subtype over hub
CASE_SECTIONS = ["at-a-glance", "market-conclusion", "demand", "competitors", "site", "revenue", "opex", "sources-uses",
                 "loan", "pro-forma", "dscr", "break-even", "sensitivity", "risks", "lender-conditions", "faq", "sources"]
CASE_TABLES = ["glance", "revenue", "opex", "uses", "sources", "loan", "proforma", "dscr", "determination", "verdict",
               "breakeven", "sensitivity"]
DISCLOSURE = ("Representative worked example. The site, sponsor and project are hypothetical. The market evidence comes "
              "from the public sources listed below, with their dates. This page shows how the market analysis is built "
              "and how it sets the loan. It is not a client engagement.")
# En and em dash in any encoding, built from code points so this file carries none.
DASHES = re.compile("|".join([chr(0x2013), chr(0x2014), "&[mn]dash;", "&#821[12];", "&#x201[34];", "%E2%80%9[34]",
                              "\\\\u201" + "[34]"]), re.I)
FORBIDDEN = re.compile("|".join(["m" + "mcg", "moh" + "elsky", "union ?" + "metric", "inno" + "wave", "analytics" + r"\.loan",
                                 "loan analytic" + "s", "feasibility-study-consulta" + "nt", "wert-?bera" + "ter"]), re.I)
SBA_REQUIRES = re.compile(r"(?<![\"“]the )(required by (the )?SBA|SBA requires|SBA mandates|SBA-required)[^.]{0,80}feasibility|"
                          r"feasibility stud(y|ies)[^.]{0,80}(required by (the )?SBA|SBA requires|SBA mandates|SBA-required)", re.I)
CREDENTIAL = re.compile(r"otava,? *(ph\.?d|ccim|mai)", re.I)
UNITS = (r"acres?|sites?|keys|rooms|units|beds|residents|people|jobs|employees|workers|households|gallons|vehicles|cars|trucks|"
         r"stores|stations|locations|outlets|dealers|dealerships|square feet|sq ft|sf|miles|parcels|permits|homes|spaces|"
         r"pads|pumps|dispensers|positions|fueling positions|chargers|ports|head|pounds|lbs|students|visitors|visits|passengers|"
         r"listings|loans|establishments|firms|businesses|properties|hotels|campgrounds|facilities|plants|counties|trips|"
         r"vehicles per day|aadt|cents")
FIG = re.compile(r"(?<![\w.$])(\$\s?\d[\d,]*(?:\.\d+)?(?:\s?(?:million|billion|thousand|trillion|[mbkt]\b))?"
                 r"|\d[\d,]*(?:\.\d+)?\s?(?:%|percent\b|x\b)"
                 r"|\d[\d,]*(?:\.\d+)?\s(?:million|billion|trillion)\b"
                 r"|\d[\d,]*\.\d+\s?[MB]\b"
                 r"|\d{1,3}(?:,\d{3})+(?:\.\d+)?"
                 r"|\d+\.\d+"
                 r"|\d{2,}(?=\s(?:" + UNITS + r")\b))", re.I)
YEAR = re.compile(r"^(19|20)\d\d$")
GEO_COUNT = re.compile(r"\s(?:counties|parishes|boroughs)\b", re.I)
NOT_FIGURE = re.compile(r"(?:§|\bcfr|\bsection|\bsections|\bsec\.|\bs\.|\bss\.|\bpart|\bsop|\bchapter|\bch\.|\bform|\bexit|"
                        r"\bexits|\binterstate|\bi-|\bus|\bu\.s\.|\bsh|\bfm|\bhighway|\broute|\bsr|\bloop|\bspur|\bno\.|±|"
                        r"\+/-|margin of error|\bml|\bmortgagee letter|\bfr|\bpub\. ?l\.|\bnaics|"
                        # FSC-RESUME-1 (O4): statute and code citations
                        r"\busc|\bstats?\.|\bstatutes?|\bcode|\bann\.|\bact|\btitle|\brules?|\bhb|\bsb|\bab|\bld|"
                        r"\bordinance|\border|\bdocket|\bp\.l\.|\barticle|\bart\.|"
                        r"\b(?:u\.s\.c|r\.c|r\.s|g\.s|f\.s|c\.r\.s|c\.g\.s|k\.r\.s|m\.g\.l|m\.c\.l|o\.c\.g\.a|o\.r\.s|a\.r\.s|"
                        r"r\.c\.w|t\.c\.a|v\.a\.m\.s)\.?)\s*$", re.I)
CTX_STOP = set("""that this with from have were been which their there than then also into about over under more most some such
only other these those them they will would could should while where when what whose after before between during against
among within without through across around each both either very much many does done being year years percent million
billion thousand first second third four five seven eight nine twelve three two one its our your for and the are was has
had not but may can per""".split())
CTX_WINDOW = 110   # characters each side of a figure whose content words give its context
CTX_MIN, CTX_STRONG, RARE_DF, PAIR_SPAN = 2, 3, 5, 220   # content words two places share for a two-digit match; shared words
# (two of them on at most RARE_DF pages) that stand alone; characters within which two figures belong to one sentence
STATUTE_SHAPE = re.compile(r"^\d{4,5}\.\d+$|^\d{3}\.\d{3}$")   # 2116.1, 4303.29, 104.001: no comma, no unit (checked below)
UNIT_AFTER = re.compile(r"\s?(?:thousand|million|billion|trillion|k|m|b|mw|mwh|kw|mills?|days|years|months|" + UNITS + r")\b", re.I)
APPROX = re.compile(r"(?:\babout|\broughly|\bnearly|\balmost|\bsome|\baround|\bmore than|\bapproximately|\bapprox\.?|~|≈|"
                    r"\bclose to|\ban estimated)\s*$", re.I)
SCALE = {"t": 1e12, "trillion": 1e12, "b": 1e9, "billion": 1e9, "m": 1e6, "million": 1e6, "k": 1e3, "thousand": 1e3}
MKT = re.compile(r"<!--mkt:([a-z0-9][a-z0-9/:-]*)\.([a-z0-9_]+)(?:\.([a-z0-9-]+))?( \{.*?\})?-->(.*?)<!--/mkt:[^>]*-->", re.S)
SKIP_TOP = {".git", "docs", "src", "node_modules", "netlify", "_bundles", "_cache", "scripts", "data"}


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def served_pages(root):
    out = {}
    for d, dirs, files in os.walk(root):
        rel = os.path.relpath(d, root)
        if rel == ".":
            dirs[:] = [x for x in dirs if x not in SKIP_TOP and not x.startswith(".")]
        else:
            dirs[:] = [x for x in dirs if not x.startswith(".")]
        if "index.html" in files:
            url = "/" if rel == "." else "/" + rel.replace(os.sep, "/") + "/"
            out[url] = os.path.join(d, "index.html")
    return out


def load_types(root):
    path = os.path.join(root, "src", "types.json")
    t = json.load(open(path, encoding="utf-8")) if os.path.exists(path) else {}
    figures = dict(DEFAULT_FIGURES, **t.get("_figures", {}))
    types = dict(DEFAULT_TYPES)
    types.update({k: v for k, v in t.items() if not k.startswith("_") and isinstance(v, dict)})
    return types, figures


def source_type(root, url):
    p = os.path.join(root, "src", "pages", url.strip("/") + ".html")
    if not os.path.exists(p):
        return None
    raw = read(p)
    end = raw.find("\n---\n", 4)
    try:
        return json.loads(raw[4:end]).get("type")
    except ValueError:
        return None


def url_type(url):
    parts = url.strip("/").split("/")
    if parts[0] == "states":
        return {2: "state", 3: "metro"}.get(len(parts), "other")
    if parts[0] == "asset-classes":
        return {2: "hub", 3: "subtype"}.get(len(parts), "other")
    if parts[0] == "case-studies" and len(parts) == 2:
        return "case"
    if parts[0] == "practice-areas" and len(parts) == 2:
        return "practice"
    if parts[0] == "analytical-framework" and len(parts) == 2:
        return "framework"
    if parts[0] == "research-notes" and len(parts) == 2:
        return "note"
    return "other"


def page_type(root, url):
    return source_type(root, url) or url_type(url)


def strip_regions(html_text, names):
    pat = re.compile(r"<!--(" + "|".join(names) + r"):([a-z0-9_.:/-]+)( \{.*?\})?-->(.*?)<!--/\1:\2-->", re.S)
    return pat.sub(" ", html_text)


def main_soup(html_text):
    soup = BeautifulSoup(html_text, "lxml")
    main = soup.find("main") or soup.body or soup
    for t in main.find_all(["script", "style"]):
        t.decompose()
    return main


def tokens(text):
    return re.findall(r"[a-z0-9]+(?:[.,'][a-z0-9]+)*", text.lower())


def overlap_text(html_text):
    main = main_soup(strip_regions(html_text, ["mesh"]))
    s = main.find(id="sources")
    if s:
        s.decompose()
    return main.get_text(" ")


def index_text(html_text):
    """Text of <main> for the repeat test: overlap_text plus the numbered sources list (I71), minus bare URLs."""
    main = main_soup(strip_regions(html_text, ["mesh"]))
    return re.sub(r"https?://\S+", " ", main.get_text(" "))


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
    f = fig.lower().replace(" ", "").replace(" ", "").replace("percent", "%").rstrip(".,")
    for word, short in (("trillion", "t"), ("billion", "b"), ("million", "m"), ("thousand", "k")):
        if f.endswith(word):
            f = f[: -len(word)] + short
    return f


def figure_key(raw):
    """(kind, value, significant digits, scaled, scale factor, approximate, context words, position, block) for a
    figure as written, or None; the last four are filled in by figures_in and research_figures."""
    f = raw.lower().replace(" ", " ").strip().rstrip(".,")
    kind = "plain"
    if f.startswith("$"):
        kind, f = "money", f[1:].strip()
    if f.endswith("%") or f.endswith("percent"):
        kind, f = "pct", f.replace("percent", "").rstrip("% ")
    elif re.search(r"\d\s?x$", f):
        kind, f = "ratio", f[:-1].strip()
    scale = 1.0
    m = re.match(r"^([\d,]*\.?\d+)\s?([a-z]+)?$", f)
    if not m:
        return None
    num, word = m.group(1).replace(",", ""), m.group(2)
    if word:
        if word not in SCALE:
            return None
        scale = SCALE[word]
    digits = num.replace(".", "").lstrip("0").rstrip("0")
    try:
        val = float(num) * scale
    except ValueError:
        return None
    return kind, val, max(len(digits), 1), scale >= 1e6, scale, False, frozenset(), 0, None


def round_sig(v, k):
    return 0.0 if v == 0 else float(f"{v:.{k}g}")


def context_words(text, a, b):
    """Content words (four letters or more, no stop words) in the whole words within CTX_WINDOW characters of a figure."""
    before, after = text[max(0, a - CTX_WINDOW):a], text[b:b + CTX_WINDOW]
    if a > CTX_WINDOW:
        before = before.split(" ", 1)[-1]
    if len(text) - b > CTX_WINDOW:
        after = after.rsplit(" ", 1)[0]
    return frozenset(w for w in re.findall(r"[a-z]{4,}", (before + " " + after).lower()) if w not in CTX_STOP)


def figures_in(text):
    text = re.sub(r"\s+", " ", text)
    out = []
    for m in FIG.finditer(text):
        if NOT_FIGURE.search(text[max(0, m.start(1) - 24):m.start(1)]):
            continue
        after = text[m.end(1):]
        if re.match(r"\(", after[:1]) and re.match(r"^\d+\.\d+$", m.group(1)):
            continue  # 120.160(b)
        if STATUTE_SHAPE.match(m.group(1)) and not UNIT_AFTER.match(after):
            continue  # 2116.1, 104.001: a section number in the dotted shape, no unit (O4)
        if re.match(r"\.\d", after[:2]) or (re.match(r"^\d+\.\d+$", m.group(1)) and re.match(r"-\d", after[:2])):
            continue  # 120.160.2, 120.160-1: a further section segment (O4)
        if GEO_COUNT.match(after[:12]):
            continue  # "32 counties": a geography count, not a market figure (geo-1-1)
        k = figure_key(m.group(1))
        if k:
            approx = bool(APPROX.search(text[max(0, m.start(1) - 16):m.start(1)]))
            ctx = context_words(text, m.start(1), m.end(1))
            out.append((m.group(1), k[:5] + (approx, ctx, m.start(1), None)))
    return out


class NumberIndex:
    """Figures on other pages, matched by value and by rounding.

    A key is (kind, value, significant digits, scaled, scale factor, approximate, context words, position, block).
    Rounding rules:
    - Three or more digits (has): the coarser written precision decides (a figure written with k digits, k >= 3,
      matches a more precise figure that rounds to it at k digits).
    - Two digits (FSC-RESUME-1, O4; two_hits): a figure written with exactly two significant digits is a rounding
      of a more precise figure of the same kind that rounds to the same two digits when the same scale word
      stands on both ("$4.8 billion" and "$4.81 billion"), or when either is marked approximate and the value is
      1,000 or more ("about 9,700" and "9,692"). Two digits agree by chance about once in ninety pairs, which on a
      site of 120 pages swallows a third of all counted figures, so check() accepts a two-digit match only with
      evidence of one fact: the two places share at least CTX_MIN content words AND either share CTX_STRONG
      words of which two are rare on the site (on RARE_DF pages or fewer: "couche", "tard"), or two different
      figures of one sentence here match two different figures of one sentence on the same other page (the pair
      "9,692 loans for $4.81 billion" against "$4.8 billion across about 9,700 loans").
      Plain numbers under 1,000 and percentages never take this path."""

    def __init__(self):
        self.exact, self.short, self.long = set(), {}, {}
        self.two_fine, self.two_coarse = {}, {}

    def add(self, key, src=None):
        kind, v, d, scaled = key[:4]
        sc, apx, ctx = key[4], key[5], key[6]
        self.exact.add((kind, round(v, 6)))
        self.short.setdefault((kind, d, scaled), set()).add(round_sig(v, d))
        for k in range(3, d):
            self.long.setdefault((kind, k, scaled), set()).add(round_sig(v, k))
        if src is not None:
            if d >= 3:
                self.two_fine.setdefault((kind, round_sig(v, 2)), []).append((sc, apx, ctx, src, key[7], v))
            elif d == 2:
                self.two_coarse.setdefault((kind, round_sig(v, 2)), []).append((sc, apx, ctx, src, key[7], v))

    def two_hits(self, key):
        """{source page: [(content words shared, position there, value there)]} for a figure's two-digit matches."""
        kind, v, d, scaled = key[:4]
        sc, apx, ctx = key[4], key[5], key[6]
        out = {}
        if d < 2:
            return out
        pool = (self.two_fine if d == 2 else self.two_coarse).get((kind, round_sig(v, 2)))
        for sc2, apx2, ctx2, src, pos2, v2 in pool or ():
            shared = ctx & ctx2
            if len(shared) < CTX_MIN:
                continue
            if (sc > 1 and sc2 == sc) or ((apx or apx2) and v >= 1000):
                out.setdefault(src, []).append((shared, pos2, v2))
        return out

    def has(self, key):
        kind, v, d, scaled = key[:4]
        if (kind, round(v, 6)) in self.exact:
            return True
        if d >= 3:
            r = round_sig(v, d)
            if r in self.long.get((kind, d, True), ()):
                return True
            if (scaled or d >= 4) and r in self.long.get((kind, d, False), ()):
                return True
        for k in range(3, d):
            r = round_sig(v, k)
            if r in self.short.get((kind, k, True), ()):
                return True
            if (scaled or k >= 4) and r in self.short.get((kind, k, False), ()):
                return True
        return False


def research_figures(html_text):
    """{norm: (raw, key)} figures in cited blocks outside sba, case, mkt and mesh regions and the sources list."""
    main = main_soup(strip_regions(html_text, ["sba", "case", "mkt", "mesh"]))
    s = main.find(id="sources")
    if s:
        s.decompose()
    for t in main.select("[data-fsc-nocount]"):
        t.decompose()   # a value the page marks as context, not a market figure: a code ratio, a fee, a national count (geo-1-1)
    figs, band = {}, set()
    for bid, b in enumerate(main.find_all(["p", "li", "tr"]) + main.select("div.stat")):
        if b.name != "tr" and b.find(["p", "li", "tr"]):
            continue
        if not (b.select("a.cite") or b.select("sup.fn")):
            continue
        for raw, key in figures_in(b.get_text(" ")):
            n = norm(raw)
            if YEAR.match(n):
                continue
            if n not in figs and b.name == "div":
                band.add(n)
            figs.setdefault(n, (raw.strip(), key[:8] + (bid,)))
    # a stats-band value whose unit sits outside the number ("31.2" over "msf") is a rescaled repeat of the body
    # figure with the same digits and a scale word ("31.2 million"): it counts once (ruling 5; geo-1-1)
    scaled = {numeral(r) for n, (r, k) in figs.items() if n not in band and k[3]}
    for n in band:
        raw, key = figs[n]
        if not key[3] and numeral(raw) in scaled:
            del figs[n]
    return figs


def numeral(raw):
    m = re.search(r"\d[\d,]*(?:\.\d+)?", raw)
    return m.group(0).replace(",", "") if m else raw


def register_figures(html_text):
    """[(pair, raw, key)] for every mkt: value in <main> outside the sources list; pair = (geo, series)."""
    m = re.search(r"<main\b.*?</main>", html_text, re.S)
    body = m.group(0) if m else html_text
    i = body.find('id="sources"')
    if i > 0:
        body = body[:i]
    if "data-fsc-nocount" in body:
        # a register value the page marks as context (a code ratio, a fee, a single property) is printed but not
        # counted: drop every element carrying data-fsc-nocount, comments and all (O4; the mixed-use hub, I90)
        soup = BeautifulSoup(body, "lxml")
        for t in soup.select("[data-fsc-nocount]"):
            t.decompose()
        body = str(soup)
    out = []
    for r in MKT.finditer(body):
        text = re.sub(r"<[^>]+>", " ", r.group(5))
        figs = figures_in(text) or [(t, figure_key(t)) for t in re.findall(r"\d[\d,]*(?:\.\d+)?", text) if figure_key(t)]
        if figs:
            raw, key = figs[0]
            out.append(((r.group(1), r.group(2)), raw.strip(), key))
    return out


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
        kids = list(hero.select_one(".frame").find_all(recursive=False))
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


class Site:
    """Every served page of a tree, with the figure index the counted-figure gate needs."""

    def __init__(self, root):
        self.root = root
        self.pages = served_pages(root)
        self.cache = {u: read(p) for u, p in self.pages.items()}
        self.types, self.figure_rules = load_types(root)
        self.ptype = {u: page_type(root, u) for u in self.pages}
        # figures other pages hold against a page include their sources lists (I71, O4); a page's own sources stay out
        # of its own counted figures (research_figures drops them)
        self.numbers = {u: [k for _, k in figures_in(index_text(self.cache[u]))] for u in self.pages}
        self.shing = {u: shingles(overlap_text(self.cache[u])) for u in self.pages}
        self.df = {}   # pages carrying each content word, for the rare-word test of a two-digit match (NumberIndex)
        for u in self.pages:
            for w in set(re.findall(r"[a-z]{4,}", re.sub(r"\s+", " ", index_text(self.cache[u])).lower())):
                self.df[w] = self.df.get(w, 0) + 1

    def rules(self, t):
        conf = self.types.get(t)
        if not conf:
            return None, None
        return conf.get("range"), self.figure_rules.get(conf.get("figures", "reference"))

    def taken(self, url, new):
        """A NumberIndex of the figures other pages hold against this page (amendment A4 applied)."""
        idx = NumberIndex()
        mine = RANK.get(self.ptype[url])
        for u, nums in self.numbers.items():
            if u == url:
                continue
            theirs = RANK.get(self.ptype[u])
            if mine is not None and theirs is not None:
                if theirs < mine:
                    continue                  # the less specific page never takes a figure from this one
                if theirs == mine and new and url not in new and u in new:
                    continue                  # same rank: the page already on the site keeps it
            for k in nums:
                idx.add(k, u)
        return idx


def rounded_repeats(cand, hits, df):
    """Ids of the candidate figures that are two-digit roundings of a fact another page prints (see NumberIndex):
    a hit whose shared words number CTX_STRONG with two of them rare on the site (df: pages per word), or two
    figures of one block, within PAIR_SPAN characters of each other and of different rounded values, that hit two
    figures of different values within PAIR_SPAN characters of each other on the same other page."""
    def stands_alone(shared):
        return len(shared) >= CTX_STRONG and sum(1 for w in shared if df.get(w, 0) <= RARE_DF) >= 2
    out = {cid for cid, hs in hits.items() if any(stands_alone(sh) for lst in hs.values() for sh, _, _ in lst)}
    blocks = {}
    for cid, key in cand:
        if cid in hits and key[8] is not None:
            blocks.setdefault(key[8], []).append((cid, key[7], round_sig(key[1], 2)))
    for items in blocks.values():
        for i, (c1, p1, r1) in enumerate(items):
            for c2, p2, r2 in items[i + 1:]:
                if abs(p1 - p2) > PAIR_SPAN or r1 == r2:
                    continue
                for src in set(hits[c1]) & set(hits[c2]):
                    if any(v1 != v2 and abs(g1 - g2) <= PAIR_SPAN for _, g1, v1 in hits[c1][src] for _, g2, v2 in hits[c2][src]):
                        out |= {c1, c2}
    return out


def check(site, urls, stage="landing", new=None, show_figs=False, show_overlap=0):
    new = set(new or ())
    results = []
    for url in urls:
        t = site.ptype.get(url) or url_type(url)
        rec = {"url": url, "type": t, "problems": []}
        if url not in site.pages:
            rec["problems"].append("not built")
            results.append(rec)
            continue
        h = site.cache[url]
        rng, fr = site.rules(t)
        rec["words"] = body_words(h)
        if rng:
            lo, hi = rng
            if lo and rec["words"] < lo:
                rec["problems"].append(f"body words {rec['words']} under {lo}")
            if hi and rec["words"] > hi:
                rec["problems"].append(f"body words {rec['words']} over {hi}")
        taken = site.taken(url, new)
        own = NumberIndex()
        rfig = research_figures(h)
        mfig = register_figures(h)
        # two-digit roundings (O4): a figure not otherwise taken whose two-digit match is backed by evidence of one
        # fact (see NumberIndex and rounded_repeats)
        cand = [(("r", n), key) for n, (_raw, key) in rfig.items()] + [(("m", i), key) for i, (_p, _r, key) in enumerate(mfig)]
        hits = {cid: h2 for cid, key in cand if not taken.has(key) for h2 in [taken.two_hits(key)] if h2}
        rounded = rounded_repeats(cand, hits, site.df)
        research = {}
        for n, (raw, key) in rfig.items():
            if not taken.has(key) and ("r", n) not in rounded and not own.has(key):
                research[n] = raw
            own.add(key)
        register, pairs = {}, set()
        for i, (pair, raw, key) in enumerate(mfig):
            if pair in pairs or taken.has(key) or ("m", i) in rounded or own.has(key):
                own.add(key)
                continue
            pairs.add(pair)
            register[f"{pair[0]}.{pair[1]}"] = raw
            own.add(key)
        cap = fr["register_cap"] if fr else 10
        rec["figures_research"] = len(research)
        rec["figures_register"] = len(register)
        rec["figures_register_counted"] = min(len(register), cap)
        rec["figures_counted"] = rec["figures_research"] + rec["figures_register_counted"]
        if show_figs:
            rec["research_list"] = sorted(research.values())
            rec["register_list"] = sorted(f"{k}={v}" for k, v in register.items())
        if fr:
            need_c, need_r = fr[f"{stage}_counted"], fr[f"{stage}_research"]
            if rec["figures_counted"] < need_c:
                rec["problems"].append(f"counted figures {rec['figures_counted']} under {need_c} ({stage})")
            if rec["figures_research"] < need_r:
                rec["problems"].append(f"research figures {rec['figures_research']} under {need_r} ({stage})")
        mine = site.shing[url]
        ov = []
        for u, s in site.shing.items():
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
        if ov and ov[0][0] >= 0.15:
            rec["problems"].append(f"overlap {rec['overlap_max']}% with {ov[0][1]}")
        if DASHES.search(h):
            rec["problems"].append(f"dashes: {len(DASHES.findall(h))}")
        if FORBIDDEN.search(h):
            rec["problems"].append("forbidden name present")
        txt = re.sub(r"<[^>]+>", " ", h)
        if SBA_REQUIRES.search(txt):
            rec["problems"].append("SBA-requires claim: " + SBA_REQUIRES.search(txt).group(0)[:100])
        if CREDENTIAL.search(h):
            rec["problems"].append("credential typed next to the name")
        if t == "case":
            rec["problems"] += case_checks(url, h)
        results.append(rec)
    return results


def manifest_urls(path):
    text = read(path)
    try:
        data = json.loads(text)
        items = data if isinstance(data, list) else data.get("pages", [])
        return ["/" + (u["url"] if isinstance(u, dict) else u).strip("/") + "/" for u in items]
    except ValueError:
        return ["/" + l.split("#")[0].strip().strip("/") + "/" for l in text.splitlines() if l.split("#")[0].strip()]


def factory_urls(root):
    out = []
    base = os.path.join(root, "src", "pages")
    for d, _dirs, files in os.walk(base):
        for f in files:
            if f.endswith(".html"):
                rel = os.path.relpath(os.path.join(d, f), base)[:-5]
                out.append("/" + rel.replace(os.sep, "/") + "/")
    return sorted(out)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("urls", nargs="*")
    ap.add_argument("--root", default=ROOT)
    ap.add_argument("--manifest")
    ap.add_argument("--factory", action="store_true")
    ap.add_argument("--stage", choices=("ready", "landing"), default="landing")
    ap.add_argument("--new", default="")
    ap.add_argument("--json")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--overlap", type=int, default=0)
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    urls = ["/" + u.strip("/") + "/" if u.strip("/") else "/" for u in a.urls]
    if a.manifest:
        urls += manifest_urls(a.manifest)
    if a.factory:
        urls += factory_urls(root)
    new = {"/" + u.strip("/") + "/" for u in a.new.split(",") if u.strip()}
    site = Site(root)
    res = check(site, urls, a.stage, new, a.figures, a.overlap)
    for r in res:
        print(f"{r['url']:62} {r['type']:9} words {r.get('words', '-'):>6}  counted {r.get('figures_counted', '-'):>4} "
              f"(research {r.get('figures_research', '-')}, register {r.get('figures_register_counted', '-')}/{r.get('figures_register', '-')})  "
              f"overlap {r.get('overlap_max', '-')}% ({r.get('overlap_with')})")
        for p in r["problems"]:
            print("    PROBLEM", p)
        if a.figures:
            print("    research:", "; ".join(r.get("research_list", [])))
            print("    register:", "; ".join(r.get("register_list", [])))
        for o in r.get("overlap_top", []):
            print("    overlap", o)
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    bad = sum(1 for r in res if r["problems"])
    print(f"{len(res)} page(s), {bad} with problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
