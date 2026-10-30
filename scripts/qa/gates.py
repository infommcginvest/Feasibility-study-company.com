#!/usr/bin/env python3
"""ROLLOUT-1 gates 1 to 14 on a set of pages, against the whole tree (FACTORY-2, generalized from WEB-FSC-6).

    python3 scripts/qa/gates.py --root DIR [--git-dir WORKTREE] (--urls U,U | --manifest FILE | --diff A...B)
                                [--range BASE..HEAD] [--tags T,T] [--stage ready|landing] [--new U,U]
                                [--site-wide] [--only 1,2,3] [--skip-look] [--look-out DIR] [--mutate]
                                [--deploy-date YYYY-MM-DD] [--out FILE]

--root      the tree whose served pages are checked (a throwaway copy, or the integrator's worktree), after the chain ran
--git-dir   the worktree for history, commit authors and tag messages (default: --root)
--diff      derive the page set from `git diff --name-only A...B` in --git-dir (amendment A2): src/pages sources,
            case inputs, returns, card templates and served pages map to their URLs
--range     the commits whose authors, messages and patches gates 7 and 8 scan (default: the --diff range as A..B)
--tags      annotated tags whose messages gate 7 scans
--stage     ready (amendment A6 READY floors) or landing (landing floors; default)
--new       pages new to the site in this landing: in a same-rank figure collision the page already live keeps it
--site-wide also run gates 3, 4, 9, 10 and 12 over every page of the site (ROLLOUT-1 ruling 14, amendment A10)
--mutate    gate 2's mutation test (one per CASE lane's first tranche), in a temporary copy

Gate 8 reads every list in ~/Downloads/fsc-rollout/private/ (or $FSC_PRIVATE): `<case slug><TAB><token>` lines are
checked on that case's page, source and inputs, `*<TAB><token>` lines on every served file and source, and both on the
patches and messages of --range (a case line on the patch hunks of that case's files). A competitor in a census is
never a gate 8 identifier (amendment A1).
"""
import argparse
import datetime
import glob
import html
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import tempfile
import urllib.parse

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagecheck as pc  # noqa: E402
import sbamandate  # noqa: E402

SITE = "https://feasibility-study-company.com"
AUTHOR_ID = SITE + "/#mark-otava"
PRIVATE = os.environ.get("FSC_PRIVATE", os.path.expanduser("~/Downloads/fsc-rollout/private"))
STATES = ["alabama", "alaska", "arizona", "arkansas", "california", "colorado", "connecticut", "delaware", "florida",
          "georgia", "hawaii", "idaho", "illinois", "indiana", "iowa", "kansas", "kentucky", "louisiana", "maine",
          "maryland", "massachusetts", "michigan", "minnesota", "mississippi", "missouri", "montana", "nebraska",
          "nevada", "new-hampshire", "new-jersey", "new-mexico", "new-york", "north-carolina", "north-dakota", "ohio",
          "oklahoma", "oregon", "pennsylvania", "rhode-island", "south-carolina", "south-dakota", "tennessee", "texas",
          "utah", "vermont", "virginia", "washington", "west-virginia", "wisconsin", "wyoming"]

results, lines = [], []
A = None   # parsed args


HOME = os.path.expanduser("~")


def out(s=""):
    s = s.replace(HOME, "~")     # records are public: never print the home directory's absolute path
    print(s)
    lines.append(s)


def gate(n, name, status, detail=""):
    results.append((n, name, status))
    out(f"\n=== Gate {n}: {name}: {status}")
    if detail:
        out(detail.rstrip())


def run(cmd, cwd, timeout=900):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


def git(*args, timeout=300):
    rc, o = run(["git", "-C", A.git_dir] + list(args), A.git_dir, timeout)
    return o if rc == 0 else ""


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def served(url):
    return os.path.join(A.root, url.strip("/"), "index.html") if url != "/" else os.path.join(A.root, "index.html")


def ld_blocks(h):
    return [m.group(1) for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', h, re.S)]


def tail(o, n=1):
    return "\n".join(o.splitlines()[-n:]) if o else ""


def slug_of(url):
    return url.strip("/").split("/")[-1]


# ------------------------------------------------------------------ page set

def urls_from_diff(rng):
    names = git("diff", "--name-only", rng).split()
    urls = set()
    for n in names:
        m = re.match(r"^src/pages/(.+)\.html$", n)
        if m:
            urls.add("/" + m.group(1) + "/")
            continue
        m = re.match(r"^(?:data/cases|data/returns|src/case-cards)/([a-z0-9-]+)\.json$", n)
        if m:
            urls.add(f"/case-studies/{m.group(1)}/")
            continue
        m = re.match(r"^((?:states|asset-classes|case-studies|practice-areas|research-notes|analytical-framework)/.+)/index\.html$", n)
        if m:
            urls.add("/" + m.group(1) + "/")
    return sorted(urls), names


# ------------------------------------------------------------------ gates

def g1(urls):
    probs = []
    for url in urls:
        p = served(url)
        if not os.path.exists(p):
            probs.append(f"{url}: not built")
            continue
        h = read(p)
        titles = len(re.findall(r"<title>", re.sub(r"<!--.*?-->", "", h, flags=re.S)))
        if titles != 1:
            probs.append(f"{url}: {titles} <title> elements")
        types, ids = set(), set()
        for b in ld_blocks(h):
            try:
                d = json.loads(b)
            except ValueError as e:
                probs.append(f"{url}: JSON-LD does not parse: {e}")
                continue
            for nd in d.get("@graph", [d]):
                t = nd.get("@type")
                types |= set(t if isinstance(t, list) else [t])
                a = nd.get("author")
                if isinstance(a, dict) and a.get("@id"):
                    ids.add(a["@id"])
        if "BreadcrumbList" not in types:
            probs.append(f"{url}: no BreadcrumbList")
        if AUTHOR_ID not in ids:
            probs.append(f"{url}: no author @id")
    gate(1, "pages build; one <title>; JSON-LD parses with BreadcrumbList and author @id", "GREEN" if not probs else "RED",
         f"{len(urls)} page(s)\n" + "\n".join("  " + x for x in probs[:60]))


def g2(urls):
    py = sys.executable
    rb, ob = run([py, "scripts/build.py", "--check"], A.root)
    rc, oc = run([py, "scripts/casemodel.py", "--check"], A.root)
    detail = f"build.py --check rc={rb}: {tail(ob)}\ncasemodel.py --check rc={rc}: {tail(oc)}"
    ok = rb == 0 and rc == 0
    if A.mutate:
        cases = [slug_of(u) for u in urls if u.startswith("/case-studies/") and
                 os.path.exists(os.path.join(A.root, "data/cases", slug_of(u) + ".json"))]
        if not cases:
            detail += "\nmutation: no case input in the page set"
        else:
            tmp = tempfile.mkdtemp(prefix="fsc-mut-")
            try:
                for d in ("scripts", "src", "data", "case-studies"):
                    shutil.copytree(os.path.join(A.root, d), os.path.join(tmp, d), ignore=shutil.ignore_patterns("markets"))
                slug = cases[0]
                cp = os.path.join(tmp, "data/cases", slug + ".json")
                spec = json.load(open(cp))
                key = next(k for k, v in spec["inputs"].items() if isinstance(v.get("value"), (int, float))
                           and v["value"] != 0 and not k.startswith(("sba_", "bi_", "hud_")))
                orig = spec["inputs"][key]["value"]
                spec["inputs"][key]["value"] = orig * 1.1
                json.dump(spec, open(cp, "w"), indent=1)
                m1, mo = run([py, "scripts/casemodel.py", "--check", "--only", slug], tmp)
                spec["inputs"][key]["value"] = orig
                json.dump(spec, open(cp, "w"), indent=1)
                m2, _ = run([py, "scripts/casemodel.py", "--check", "--only", slug], tmp)
                ok = ok and m1 != 0 and m2 == 0
                detail += (f"\nmutation ({slug} input {key} x1.1): --check rc={m1} (want non-zero: {tail(mo)}), "
                           f"after revert rc={m2} (want 0); temporary copy removed, nothing committed")
            finally:
                shutil.rmtree(tmp, ignore_errors=True)
    gate(2, "factory: build.py --check and casemodel.py --check exit 0" + ("; mutation test" if A.mutate else ""),
         "GREEN" if ok else "RED", detail)


def g3_4_5(urls, site, recs, wide):
    bad3 = {r["url"]: r for r in recs if any(p.startswith(("counted figures", "research figures")) for p in r["problems"])}
    rows = [f"  {r['url']:62} {r['type']:9} counted {r.get('figures_counted')} (research {r.get('figures_research')}, "
            f"register {r.get('figures_register_counted')}/{r.get('figures_register')})" for r in recs]
    floor_note = ""
    if wide:
        wrecs = pc.check(site, [u for u in pc.factory_urls(A.root) if u not in urls], "landing", A.new_set)
        under = [r for r in wrecs if any(p.startswith(("counted figures", "research figures")) for p in r["problems"])]
        floor_note = (f"\nsite-wide: {len(wrecs)} other factory page(s) at landing floors; under the floor: "
                      f"{len(under)}\n" + "\n".join(f"  UNDER {r['url']}: {[p for p in r['problems'] if 'figures' in p]}"
                                                    for r in under))
        A.under_floor = [r["url"] for r in under]
    gate(3, f"counted figures, amendment A6 {A.stage} floors (research and register apart)",
         "GREEN" if not bad3 and not getattr(A, "under_floor", []) else "RED", "\n".join(rows) + floor_note)
    bad4 = [r for r in recs if r.get("overlap_max", 0) >= 15]
    detail = "\n".join(f"  {r['url']:62} max {r.get('overlap_max')}% ({r.get('overlap_with')})" for r in recs)
    if wide:
        worst = []
        for u, s in site.shing.items():
            for v, t in site.shing.items():
                if u < v and s and t:
                    o = len(s & t) / min(len(s), len(t))
                    if o >= 0.15:
                        worst.append((round(o * 100, 2), u, v))
        A.wide_overlap = [w for w in worst if w[1] in urls or w[2] in urls]
        detail += (f"\nsite-wide pairs at or over 15%: {len(worst)}, of which with a page of this set: {len(A.wide_overlap)} "
                   f"(the others are on pages this landing did not write, reported, not failed)\n" +
                   "\n".join(f"  {o}% {u} ~ {v}" for o, u, v in sorted(worst, reverse=True)[:40]))
    gate(4, "overlap under 15% against every page on the site (8-word shingles)",
         "GREEN" if not bad4 and not (wide and A.wide_overlap) else "RED", detail)
    sub = [r for r in recs if r["type"] in ("metro", "subtype")]
    bad5 = [r["url"] for r in sub if r in bad3.values() or r.get("overlap_max", 0) >= 15]
    gate(5, "standalone: every metro and subtype passes gates 3 and 4 on its own evidence, or it folds",
         "GREEN" if not bad5 else "RED", f"{len(sub)} metro or subtype page(s); failing: {bad5}")


def g6(recs):
    probs, detail = [], []
    cases = [r for r in recs if r["type"] == "case"]
    if not cases:
        gate(6, "case standard v3", "GREEN", "  no case pages in the set")
        return
    sys.path.insert(0, os.path.join(A.root, "scripts"))
    import casemodel as cm
    S = cm.SBA(json.load(open(os.path.join(A.root, "data/regulatory/sba.json"))))
    for r in cases:
        slug = slug_of(r["url"])
        for p in r["problems"]:
            if any(k in p for k in ("missing section", "missing case table", "disclosure", "competitor", "body words", "hero layout")):
                probs.append(f"{slug}: {p}")
        jp = os.path.join(A.root, "data/cases", slug + ".json")
        if not os.path.exists(jp):
            probs.append(f"{slug}: no case input file data/cases/{slug}.json")
            continue
        case = cm.Case(jp, S)
        run_ = case.run()
        t1, rules = run_["restructured"], run_["rules"]
        ok_eq = t1["equity_pct"] + 1e-9 >= rules["equity_req"]
        ok_cap = True
        if case.program == "sba_504":
            ok_cap = t1["debenture"] <= rules["cap"] + 0.5
        elif case.program == "sba_7a":
            ok_cap = t1["loan_total"] <= rules["cap"] + 0.5
        d = case.test_dscr(run_["years"], t1, rules)
        ok_d = d is not None and d >= rules["floor"]
        sb = case.spec.get("sba", {})
        if case.program == "sba_504":
            exp = ("equity.sba_504_new_and_special" if sb.get("business_age") == "new" and sb.get("special_purpose") else
                   "equity.sba_504_new_or_special" if sb.get("business_age") == "new" or sb.get("special_purpose") else
                   "equity.sba_504_standard")
            if rules.get("equity_path") != exp:
                probs.append(f"{slug}: equity path {rules.get('equity_path')} expected {exp}")
        h = read(served(r["url"]))
        if sb.get("purpose") == "acquisition" and case.program in ("sba_7a", "sba_504"):
            if rules.get("test") != "historical" or abs(rules["floor"] - 1.25) > 1e-9:
                probs.append(f"{slug}: acquisition not tested under Appendix 15 (historical EBITDA, 1.25x)")
            if "dscr.coo_initial_acquisition" not in h or "illustrative" not in h.lower():
                probs.append(f"{slug}: acquisition page lacks the 1.25x sba marker or the illustrative label")
        negative = False
        if not ok_d:
            negative = "the market does not support this loan" in h and case.solve_equity_for_floor(
                run_["vals"], run_["uses"], run_["years"], rules, t1["equity_pct"]) is None
        if not (ok_eq and ok_cap and (ok_d or negative)):
            probs.append(f"{slug}: restructured structure fails a rule (equity {ok_eq}, cap {ok_cap}, dscr {ok_d})")
        detail.append(f"  {slug:46} {case.program:8} words {r.get('words'):>5}  equity {t1['equity_pct']*100:5.1f}% "
                      f"(tier {rules['equity_req']*100:.0f}%)  " + ("NEGATIVE  " if negative else "") +
                      (f"test DSCR {d:.3f} " if d is not None else "test DSCR none ") + f"(floor {rules['floor']:.2f})")
    gate(6, "case standard v3: components, body length, SBA tiers, floors and caps (sba.json); acquisitions under Appendix 15",
         "GREEN" if not probs else "RED", "\n".join(detail) + ("\n" + "\n".join("  " + p for p in probs) if probs else ""))


REVIEWED = None


def reviewed(url, sid, num, text):
    global REVIEWED
    if REVIEWED is None:
        REVIEWED = []
        for path in [os.path.join(HERE, "nocite-reviewed.tsv")] + sorted(glob.glob(os.path.join(A.root, "docs/rollout/*/nocite-reviewed.tsv"))):
            for line in open(path, encoding="utf-8"):
                if line.strip() and not line.startswith("#"):
                    parts = line.rstrip("\n").split("\t")
                    if len(parts) >= 4:
                        REVIEWED.append(tuple(parts[:4]))
    return any(u == url and sec == sid and n == num and phrase in text for u, sec, n, phrase in REVIEWED)


def served_files(exts=(".html", ".xml", ".txt", ".json", ".js", ".css", ".toml", ".svg")):
    for d, dirs, files in os.walk(A.root):
        rel = os.path.relpath(d, A.root)
        if rel == ".":
            dirs[:] = [x for x in dirs if x not in (".git", "docs", "src", "node_modules", "_bundles", "_cache") and not x.startswith(".")]
        else:
            dirs[:] = [x for x in dirs if not x.startswith(".")]
        if rel == "data":
            dirs[:] = [x for x in dirs if x != "markets"]
        for f in files:
            if f.endswith(exts) and not f.startswith("."):
                yield os.path.join(d, f)


def source_files():
    for base in ("src", "data/cases", "data/returns"):
        for d, _dirs, files in os.walk(os.path.join(A.root, base)):
            for f in files:
                if f.endswith((".html", ".json", ".md")):
                    yield os.path.join(d, f)


def g7(urls):
    pats = {
        "SOP 50 10 8 as current": re.compile(r"SOP 50 10 8(?!\.1)[,\s(]{1,3}(?:[^.]{0,60}?)(effective June 1, 2025|current)", re.I),
        "50 10 7": re.compile(r"50 10 7(?!\d)"),
        "SBSS as current": re.compile(r"SBSS(?![^.]{0,80}(retire|discontinu|sunset|gone|no longer|former|replaced|was |is gone|ended))", re.I),
        "504 1:1 or 1.0x": re.compile(r"504[^.]{0,80}\b(1:1|1\.0x)\b|\b(1:1|1\.0x)\b[^.]{0,80}504", re.I),
        "$90,000 jobs": re.compile(r"\$90,000[^.]{0,60}job|job[^.]{0,60}\$90,000", re.I),
        "SBA requires + feasibility": pc.SBA_REQUIRES,
    }
    hits, src_probs, nocite = [], [], []
    for url in urls:
        p = served(url)
        if not os.path.exists(p):
            continue
        h = read(p)
        txt = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", " ", re.sub(r"<style.*?</style>", " ", h, flags=re.S), flags=re.S))
        for name, rx in pats.items():
            for m in rx.finditer(txt):
                if name == "504 1:1 or 1.0x" and re.search(r"global", txt[max(0, m.start() - 80):m.end() + 40], re.I):
                    continue
                hits.append(f"{url}: {name}: ...{txt[max(0, m.start() - 50):m.end() + 30].strip()}...")
        soup = BeautifulSoup(h, "lxml")
        ol = soup.select_one("ol.sources")
        for li in (ol.find_all("li") if ol else []):
            a = li.find("a", href=True)
            t = li.get_text(" ", strip=True)
            if not a or not a["href"].startswith("http") or t.count(",") < 2:
                src_probs.append(f"{url}: {li.get('id')}: {t[:90]}")
        if ol is None and pc.url_type(url) != "other":
            src_probs.append(f"{url}: no numbered sources list")
        cited = {int(x) for x in re.findall(r'href="#s(\d+)"', h)}
        n = len(ol.find_all("li")) if ol else 0
        unc = sorted(set(range(1, n + 1)) - cited)
        if unc:
            src_probs.append(f"{url}: sources never cited {unc}")
        main = pc.main_soup(pc.strip_regions(h, ["sba", "case", "mkt", "mesh"]))
        s = main.find(id="sources")
        if s:
            s.decompose()
        for b in main.find_all(["p", "li", "tr"]):
            if b.name != "tr" and b.find(["p", "li", "tr"]):
                continue
            t = b.get_text(" ", strip=True)
            wrap = b.find_parent(class_="data-table-wrap") if b.name == "tr" else None
            note = wrap.find_next_sibling() if wrap is not None else None
            if note is not None and "table-source" in (note.get("class") or []) and (note.select("a.cite") or note.select("sup.fn")):
                continue
            t = re.sub(r"(CFR|SOP 50 10|Handbook|Exit|Exits|Route|FM|US|SH|I-|section|Notice|No\.)\s*[\d.()a-z-]+", " ", t)
            if pc.FIG.search(t) and not (b.select("a.cite") or b.select("sup.fn")) and not b.find_parent("thead"):
                nums = [m.group(1) for m in pc.FIG.finditer(t) if not pc.YEAR.match(pc.norm(m.group(1)))]
                sec = b.find_parent("section")
                sid = sec.get("id") if sec else ""
                left = [x for x in nums if not reviewed(url, sid, x, t)]
                if left:
                    nocite.append(f"{url} #{sid}: {left} in: {t[:110]}")
    rev = []
    for path in [os.path.join(HERE, "sbamandate-reviewed.tsv")] + sorted(glob.glob(os.path.join(A.root, "docs/rollout/*/sbamandate-reviewed.tsv"))):
        rev += [l.rstrip("\n").split("\t") for l in open(path, encoding="utf-8") if l.strip() and not l.startswith("#")]
    mandate = []
    for _url, path in pc.served_pages(A.root).items():
        r = os.path.relpath(path, A.root)
        for sent in sbamandate.flagged(read(path)):
            if not any(len(x) >= 2 and r == x[0] and sent.startswith(x[1]) for x in rev):
                mandate.append(f"{r}: {sent[:160]}")
    forb = [os.path.relpath(f, A.root) for f in list(served_files()) + list(source_files()) if pc.FORBIDDEN.search(read(f))]
    meta = git("log", "--format=%an <%ae>|%cn <%ce>|%s%n%b", A.range) if A.range else ""
    meta_hits = [l for l in meta.splitlines() if pc.FORBIDDEN.search(l)]
    tag_hits = []
    for t in A.tags:
        msg = git("tag", "-l", "--format=%(taggername) %(taggeremail)%0a%(contents)", t)
        if pc.FORBIDDEN.search(msg):
            tag_hits.append(t)
    ok = not hits and not src_probs and not nocite and not mandate and not forb and not meta_hits and not tag_hits
    gate(7, "sources: four parts, every source cited, figures cited; ruling 9 pattern absent from served files, sources, "
            "commits and tags; sbamandate zero; stale-claim patterns zero", "GREEN" if ok else "RED",
         f"stale-claim hits {len(hits)}\n" + "\n".join("  " + x for x in hits[:30]) +
         f"\nsource entries lacking a part or never cited {len(src_probs)}\n" + "\n".join("  " + x for x in src_probs[:30]) +
         f"\nfigure blocks without a citation {len(nocite)}\n" + "\n".join("  " + x for x in nocite[:40]) +
         f"\nSBA mandate sentences (all served pages, unreviewed) {len(mandate)}\n" + "\n".join("  " + x for x in mandate[:20]) +
         f"\nfiles matching the ruling 9 pattern {len(forb)}: {forb[:20]}"
         f"\ncommit authors, committers or messages matching in {A.range or '(no range)'}: {len(meta_hits)}"
         f"\ntag messages matching ({len(A.tags)} tag(s)): {tag_hits}")


def load_lists():
    scoped, star, bad = {}, [], []
    for path in sorted(glob.glob(os.path.join(PRIVATE, "*.txt"))):
        for i, l in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
            l = l.rstrip("\n")
            if not l.strip() or l.startswith("#"):
                continue
            if "\t" not in l:
                bad.append(f"{os.path.basename(path)}:{i}: not in amendment A1 form (<case slug><TAB><token> or *<TAB><token>)")
                continue
            scope, tok = l.split("\t", 1)
            tok = tok.strip()
            if not tok:
                continue
            if scope.strip() == "*":
                star.append(tok)
            else:
                scoped.setdefault(scope.strip(), []).append(tok)
    return scoped, star, bad


def flat(s):
    s = html.unescape(urllib.parse.unquote(s)).lower()
    toks = re.findall(r"\d+(?:[.,]\d+)*|[a-z]+", s)
    return " " + " ".join(t.replace(",", "") if t[0].isdigit() else t for t in toks) + " "


def hit(tok, raw, flatraw):
    if re.search(r"(?<![0-9a-z])" + re.escape(tok.lower()) + r"(?![0-9a-z])", raw):
        return True
    f = flat(tok)
    return f.strip() != "" and f in flatraw


def case_files(slug):
    paths = [os.path.join(A.root, "case-studies", slug, "index.html"),
             os.path.join(A.root, "src/pages/case-studies", slug + ".html"),
             os.path.join(A.root, "data/cases", slug + ".json"),
             os.path.join(A.root, "data/returns", slug + ".json"),
             os.path.join(A.root, "src/case-cards", slug + ".json")]
    return [p for p in paths if os.path.exists(p)]


def g8(urls):
    scoped, star, bad = load_lists()
    probs = list(bad)
    street = re.compile(r"(?<![-\w])\d{2,6}\s+(?:[NSEW]\.?\s+)?(?:[A-Z][a-z]+\s){0,3}(?:St|Street|Rd|Road|Ave|Avenue|Blvd|"
                        r"Boulevard|Hwy|Highway|Dr|Drive|Ln|Lane|Pkwy|Parkway|Way|Ct|Court|Loop)\b\.?")
    parcel = re.compile(r"\b(parcel (?:id|number|no\.?)|APN|prop(?:erty)? id|account (?:no|number)|MLS\s*#|LoopNet ID)\b", re.I)
    for url in urls:
        if pc.url_type(url) != "case" or not os.path.exists(served(url)):
            continue
        slug = slug_of(url)
        soup = BeautifulSoup(read(served(url)), "lxml")
        subj = " ".join(el.get_text(" ") for el in [soup.select_one("section.hero"), soup.find(id="at-a-glance"),
                                                   soup.find(id="market-conclusion")] if el)
        for m in street.finditer(subj):
            probs.append(f"{slug}: street-number pattern in subject text: {m.group(0)}")
        for m in parcel.finditer(subj):
            probs.append(f"{slug}: parcel or listing identifier wording in subject text: ...{subj[max(0, m.start() - 40):m.end() + 40]}...")
    # case-scoped lines on every case that has files in the tree. A hit fails the gate on a case of this set or a
    # factory case (it has a source under src/pages); on a legacy hand-built case awaiting its CASE rebuild it is reported
    legacy = []
    in_set = {slug_of(u) for u in urls if pc.url_type(u) == "case"}
    for slug, toks in sorted(scoped.items()):
        factory = os.path.exists(os.path.join(A.root, "src/pages/case-studies", slug + ".html"))
        for p in case_files(slug):
            raw = read(p).lower()
            fr = flat(raw)
            for tok in toks:
                if hit(tok, raw, fr):
                    msg = f"{slug}: subject identifier present in {os.path.relpath(p, A.root)}: {tok}"
                    (probs if factory or slug in in_set else legacy).append(msg)
    if star:
        for p in list(served_files()) + list(source_files()):
            raw = read(p).lower()
            fr = flat(raw)
            for tok in star:
                if hit(tok, raw, fr):
                    probs.append(f"*: real-subject identifier present in {os.path.relpath(p, A.root)}: {tok}")
    hist = 0
    if A.range:
        msgs = git("log", "--format=%B", A.range)
        patch = git("log", "-p", "--format=COMMIT %H", A.range, timeout=600)
        hist = len(patch)
        lowm, flm = msgs.lower(), flat(msgs)
        for tok in star + [t for v in scoped.values() for t in v]:
            if hit(tok, lowm, flm):
                probs.append(f"history: identifier in a commit message of {A.range}: {tok}")
        cur, buf, chunks = None, [], []
        for line in patch.splitlines():
            if line.startswith("diff --git "):
                if cur is not None:
                    chunks.append((cur, "\n".join(buf)))
                cur, buf = line.split(" b/", 1)[-1], []
            elif line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
                buf.append(line[1:])
        if cur is not None:
            chunks.append((cur, "\n".join(buf)))
        for path, text in chunks:
            low, fl = text.lower(), flat(text)
            m = re.search(r"(?:case-studies/|data/cases/|data/returns/|src/case-cards/|src/pages/case-studies/)([a-z0-9-]+)", path)
            toks = list(star) + (scoped.get(m.group(1), []) if m else [])
            for tok in toks:
                if hit(tok, low, fl):
                    probs.append(f"history: identifier in the patch of {path} in {A.range}: {tok}")
    gate(8, "subjects: no identifier from any list in private/ in a served file, source, input, patch or commit message",
         "GREEN" if not probs else "RED",
         f"lists {len(glob.glob(os.path.join(PRIVATE, '*.txt')))}; case-scoped tokens {sum(len(v) for v in scoped.values())} "
         f"over {len(scoped)} case(s); site-wide tokens {len(star)}; history scanned: {A.range or 'none'} ({hist} bytes)\n" +
         "\n".join("  " + x for x in sorted(set(probs))[:60]) +
         (f"\nlegacy hand-built cases (not in this set, no factory source) carrying a listed value, reported for their "
          f"CASE rebuild: {len(legacy)}\n" + "\n".join("  " + x for x in sorted(set(legacy))[:40]) if legacy else ""))


def body_links(h, url):
    """(href or pending target) paths in <main> outside the breadcrumb, live and pending (amendment A5)."""
    m = re.search(r"<main\b.*?</main>", h, re.S)
    body = re.sub(r'<nav class="breadcrumb".*?</nav>', " ", m.group(0) if m else "", flags=re.S)
    body = re.sub(r"<!--.*?-->", lambda x: x.group(0) if x.group(0).startswith(("<!--mesh", "<!--/mesh")) else " ", body, flags=re.S)
    order = []
    for m in re.finditer(r'<a [^>]*?href="(/[^"#?]*)"([^>]*)>|data-fsc-pending="(/[^"#?]*)"', body):
        if m.group(3):
            order.append(m.group(3))
        elif "data-fsc-pending" not in m.group(2):
            order.append(m.group(1))
    pend = set(re.findall(r'data-fsc-pending="(/[^"#?]*)"', body))
    live = {p for p in order if p not in pend}
    seen = []
    for p in order:
        if p not in seen:
            seen.append(p)
    return seen, live


def best(paths, slug):
    """The linked page whose slug shares the most words with the case slug (ties: link order), or None."""
    words = set(slug.split("-"))
    scored = [(len(set(slug_of(p).split("-")) & words - {"and"}), -i, p) for i, p in enumerate(paths)]
    if not scored:
        return None
    top = max(scored)
    return top[2] if top[0] > 0 else None


def g9(urls, wide):
    notes, status = [], "GREEN"
    for script in ("links.py", "mesh.py"):
        rc, o = run([sys.executable, "scripts/" + script, "--check"], A.root)
        notes.append(f"{script} --check rc={rc}: {tail(o)}")
        if rc != 0:
            status = "RED"
            notes += ["  " + l for l in o.splitlines()[:30]]
    pages = pc.served_pages(A.root)
    idx = {"/", "/case-studies/", "/asset-classes/", "/states/", "/practice-areas/", "/research-notes/", "/404.html", "/tools/nda/"}
    cache = {u: read(p) for u, p in pages.items()}
    links_of = {u: body_links(h, u) for u, h in cache.items()}
    inb = {u: set() for u in pages}
    for u, (_all, live) in links_of.items():
        if u in idx:
            continue
        for p in live:
            if p in inb and p != u:
                inb[p].add(u)
    check = urls if not wide else [u for u in pages if pc.url_type(u) != "other"]
    low = {u: len(inb.get(u, ())) for u in check if u in pages and len(inb.get(u, ())) < 3}
    miss = []

    def has(src, dst):
        return src in links_of and dst in set(links_of[src][0])

    for u in urls:
        t = pc.url_type(u)
        parts = u.strip("/").split("/")
        if t in ("metro", "subtype"):
            parent = "/" + parts[0] + "/" + parts[1] + "/"
            crumb = re.search(r'<nav class="breadcrumb".*?</nav>', cache.get(u, ""), re.S)
            if not has(u, parent) and not (crumb and f'href="{parent}"' in crumb.group(0)):
                miss.append(f"{u} does not link its parent {parent}")
            if parent in pages and not has(parent, u):
                miss.append(f"{parent} does not link {u}")
        if t in ("state", "hub"):
            for v in pages:
                if v.startswith(u) and v != u and v.count("/") == u.count("/") + 1 and not has(u, v):
                    miss.append(f"{u} does not link its child {v}")
        if t == "case" and u in links_of:
            slug = slug_of(u)
            al = links_of[u][0]
            states = [p for p in al if re.match(r"^/states/[a-z-]+/$", p)]
            hubs = [p for p in al if re.match(r"^/asset-classes/[a-z0-9-]+/$", p)]
            metros = [p for p in al if re.match(r"^/states/[a-z-]+/[a-z0-9-]+/$", p)]
            st = best(states, slug)
            hb = best(hubs, slug)
            if st is None and not states:
                miss.append(f"{u} links no state page")
            elif st in pages and not has(st, u):
                miss.append(f"{st} does not link its case {u}")
            if hb is None and not hubs:
                miss.append(f"{u} links no hub page")
            elif hb in pages and not has(hb, u):
                miss.append(f"{hb} does not link its case {u}")
            for mt in metros:
                if st and mt.startswith(st) and mt in pages and not has(mt, u):
                    miss.append(f"{mt} does not link its case {u}")
    if (low and A.stage == "landing") or miss:
        status = "RED"
    gate(9, "links: links.py and mesh.py --check; 3+ inbound contextual links from distinct non-index pages; required "
            "edges (pending links count, amendment A5)", status,
         "\n".join(notes) + f"\npages checked for inbound links: {len(check)}; under 3: {len(low)}\n" +
         "\n".join(f"  {u:62} {n}" for u, n in sorted(low.items())[:80]) +
         ("\nmissing edges:\n" + "\n".join("  " + x for x in miss) if miss else "\nrequired edges: all present"))


def g10(urls, wide):
    probs = []
    for p in list(served_files()) + [f for f in source_files()]:
        n = len(pc.DASHES.findall(read(p)))
        if n:
            probs.append(f"{os.path.relpath(p, A.root)}: {n} dash(es)")
        if pc.CREDENTIAL.search(read(p)):
            probs.append(f"{os.path.relpath(p, A.root)}: credential typed beside the name")
    gate(10, "clean text: zero em and en dashes in any encoding in every served file and source; no credential beside the name",
         "GREEN" if not probs else "RED", "\n".join("  " + x for x in probs[:60]) or "  0 in every served file (data/markets excluded: never deployed) and source")


def g11():
    notes, status = [], "GREEN"
    for script in ("byline.py", "regulatory.py", "chrome.py", "markets.py"):
        rc, o = run([sys.executable, "scripts/" + script, "--check"], A.root)
        notes.append(f"{script} --check rc={rc}: {tail(o)}")
        if rc != 0:
            status = "RED"
    gate(11, "markers: byline, regulatory, chrome and markets --check", status, "\n".join(notes))


def page_dates(h):
    mods = set(re.findall(r'"dateModified":\s*"([^"]+)"', h))
    pubs = set(re.findall(r'"datePublished":\s*"([^"]+)"', h))
    vis_up = set(re.findall(r'Updated <time datetime="([^"]+)"', h))
    vis_pub = set(re.findall(r'Published <time datetime="([^"]+)"', h))
    return mods, pubs, vis_up, vis_pub


def prose_changed(old, new):
    """True when a served page's own text changed, outside script-owned regions and its dates: an edit the
    integrator makes to a page it owns (an index card) moves that page's date legitimately."""
    def norm(h):
        h = pc.strip_regions(h, ["chrome", "mesh", "fsc", "sba", "mkt", "case"])
        return re.sub(r'"date(?:Modified|Published)":\s*"[^"]+"', "", h)
    return norm(old) != norm(new)


def g12(urls, wide, base_ref):
    probs = []
    sm = read(os.path.join(A.root, "sitemap.xml"))
    lastmod = dict(re.findall(r"<loc>" + re.escape(SITE) + r"(/[^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
    pages = pc.served_pages(A.root)
    check = sorted(pages) if wide else urls
    changed = set(A.changed_files or [])
    for url in check:
        p = pages.get(url)
        if not p:
            continue
        h = read(p)
        if 'name="robots" content="noindex' in h:
            continue
        mods, pubs, vis_up, vis_pub = page_dates(h)
        if len(mods) > 1:
            probs.append(f"{url}: dateModified disagrees with itself {mods}")
        mod = next(iter(mods), None)
        if vis_up and mod and vis_up != {mod}:
            probs.append(f"{url}: visible Updated {vis_up} vs dateModified {mod}")
        if lastmod.get(url) is None:
            probs.append(f"{url}: not in the sitemap")
        elif mod and lastmod[url] != mod:
            probs.append(f"{url}: sitemap lastmod {lastmod[url]} vs dateModified {mod}")
        if base_ref:
            rel = os.path.relpath(p, A.root)
            old = git("show", f"{base_ref}:{rel}")
            if old:
                omods, opubs, _, _ = page_dates(old)
                if opubs and pubs and opubs != pubs:
                    probs.append(f"{url}: datePublished moved {opubs} -> {pubs} (a rebuilt page keeps its published date)")
                src = "src/pages" + url.rstrip("/") + ".html"
                own = {src, rel, f"data/cases/{slug_of(url)}.json", f"data/returns/{slug_of(url)}.json"}
                if omods and mods and omods != mods and not (own & changed) and not prose_changed(old, h):
                    probs.append(f"{url}: dateModified moved {omods} -> {mods} although its own content did not change (A10)")
            elif url in urls and A.deploy_date and pubs and pubs != {A.deploy_date}:
                probs.append(f"{url}: new page datePublished {pubs} not the landing date {A.deploy_date}")
    gate(12, "dates: JSON-LD dateModified, the visible line and sitemap lastmod agree; new pages carry the landing date; "
             "rebuilt pages keep their published date; dates move only with content (A10)" + (" (every page)" if wide else ""),
         "GREEN" if not probs else "RED", f"{len(check)} page(s)\n" + "\n".join("  " + x for x in probs[:80]))


def free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def g13(urls):
    if A.skip_look:
        gate(13, "look", "PENDING", "  skipped in this run (--skip-look)")
        return
    by_type = {}
    for u in urls:
        by_type.setdefault(pc.url_type(u), []).append(u)
    look = urls if len(urls) <= 4 else [v[0] for v in by_type.values()]
    outdir = A.look_out or tempfile.mkdtemp(prefix="fsc-look-")
    port = free_port()
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", A.root],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        rc, o = run(["node", os.path.join(HERE, "shots.mjs"), f"http://127.0.0.1:{port}", outdir] + look, A.root, timeout=1800)
    finally:
        srv.kill()
    shutil.rmtree(os.path.join(outdir, ".profile"), ignore_errors=True)
    recs = [json.loads(l) for l in o.splitlines() if l.startswith("{")]
    bad = [r for r in recs if r["pageOverflow"] or r.get("offenders")]
    unscrolled = [r for r in recs for t in r["wideTables"] if t["scrolls"] not in ("auto", "scroll")]
    ok = rc == 0 and len(recs) == 2 * len(look) and not bad and not unscrolled
    gate(13, "look: 1440 and 390 screenshots; no page-level horizontal scroll at 390; wide tables scroll in their box",
         "GREEN" if ok else "RED", f"screenshots in {outdir} (port {port})\n" +
         "\n".join(f"  {r['file']:70} scrollWidth {r['scrollWidth']} / {r['innerWidth']} overflow {r['pageOverflow']} "
                   f"offenders {r.get('offenders')}" for r in recs) + (f"\n{o[-800:]}" if rc else ""))


def g14(urls):
    probs = []
    sm = read(os.path.join(A.root, "sitemap.xml"))
    for url in urls:
        p = served(url)
        if not os.path.exists(p):
            continue
        h = read(p)
        m = re.search(r'<meta name="robots" content="([^"]+)"', h)
        r = m.group(1) if m else ""
        if "index" not in r or "noindex" in r or "follow" not in r or "nofollow" in r:
            probs.append(f"{url}: robots meta {r or None}")
        if not re.search(r"<loc>" + re.escape(SITE + url) + r"</loc>\s*<lastmod>\d{4}-\d\d-\d\d</lastmod>", sm):
            probs.append(f"{url}: not in the sitemap with a lastmod")
    gate(14, "index all: index, follow, and in the sitemap with lastmod", "GREEN" if not probs else "RED",
         "\n".join("  " + x for x in probs) or f"  {len(urls)} page(s) indexable and listed")


def main(argv):
    global A
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=pc.ROOT)
    ap.add_argument("--git-dir")
    ap.add_argument("--urls", default="")
    ap.add_argument("--manifest")
    ap.add_argument("--diff")
    ap.add_argument("--range")
    ap.add_argument("--base-ref", help="ref whose served pages give the previous dates (default: the left side of --diff)")
    ap.add_argument("--tags", default="")
    ap.add_argument("--stage", choices=("ready", "landing"), default="landing")
    ap.add_argument("--new", default="")
    ap.add_argument("--site-wide", action="store_true")
    ap.add_argument("--only")
    ap.add_argument("--skip-look", action="store_true")
    ap.add_argument("--look-out")
    ap.add_argument("--mutate", action="store_true")
    ap.add_argument("--deploy-date")
    ap.add_argument("--out")
    A = ap.parse_args(argv)
    A.root = os.path.abspath(A.root)
    A.git_dir = os.path.abspath(A.git_dir or A.root)
    A.tags = [t for t in A.tags.split(",") if t]
    urls = {("/" + u.strip("/") + "/").replace("//", "/") for u in A.urls.split(",") if u.strip()}
    A.changed_files = []
    if A.manifest:
        urls |= set(pc.manifest_urls(A.manifest))
    if A.diff:
        d_urls, A.changed_files = urls_from_diff(A.diff)
        urls |= set(d_urls)
        if not A.range:
            A.range = A.diff.replace("...", "..")
        if not A.base_ref:
            A.base_ref = A.diff.split("...")[0]
    urls = sorted(urls)
    A.new_set = {"/" + u.strip("/") + "/" for u in A.new.split(",") if u.strip()}
    if not A.deploy_date:
        A.deploy_date = json.load(open(os.path.join(A.root, "src/site.json")))["deploy_date"]
    only = {int(x) for x in A.only.split(",")} if A.only else set(range(1, 15))
    head = git("rev-parse", "HEAD").strip()
    out(f"ROLLOUT-1 gates (scripts/qa/gates.py), run {datetime.datetime.now().isoformat(timespec='seconds')}")
    out(f"root {A.root}; git dir {A.git_dir} at {head}; range {A.range}; stage {A.stage}; site-wide {A.site_wide}")
    out("command: python3 scripts/qa/gates.py " + " ".join(argv))
    out(f"pages ({len(urls)}): " + " ".join(urls))
    site = recs = None
    if only & {3, 4, 5, 6}:
        site = pc.Site(A.root)
        recs = pc.check(site, urls, A.stage, A.new_set)
    if 1 in only: g1(urls)
    if 2 in only: g2(urls)
    if only & {3, 4, 5}: g3_4_5(urls, site, recs, A.site_wide)
    if 6 in only: g6(recs)
    if 7 in only: g7(urls)
    if 8 in only: g8(urls)
    if 9 in only: g9(urls, A.site_wide)
    if 10 in only: g10(urls, A.site_wide)
    if 11 in only: g11()
    if 12 in only: g12(urls, A.site_wide, A.base_ref)
    if 13 in only: g13(urls)
    if 14 in only: g14(urls)
    out("\nSUMMARY")
    for n, name, st in sorted(results):
        out(f"  gate {n:2}: {st:8} {name[:110]}")
    green = sum(1 for r in results if r[2] == "GREEN")
    out(f"  green {green}/{len(results)}")
    if A.out:
        os.makedirs(os.path.dirname(os.path.abspath(A.out)), exist_ok=True)
        open(A.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return 0 if green == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
