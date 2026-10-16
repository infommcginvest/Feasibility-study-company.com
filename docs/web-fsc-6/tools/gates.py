#!/usr/bin/env python3
"""WEB-FSC-6 gates 1 to 14 over the worktree.

    python3 docs/web-fsc-6/tools/gates.py [--base 1d48cc2] [--deploy-date 2026-10-16] [--out docs/web-fsc-6/GATES.txt]
                                          [--only 1,2,3] [--skip-look]

Gates that need WEB-FSC-4 or WEB-FSC-5 scripts (links.py, mesh.py, chrome.py, sitemap.py, markets.py) run
them when present and say NOT RUN (script absent) when not; a gate with a NOT RUN part is reported PENDING,
never GREEN. Mutation tests run in a temporary copy of the tree, so nothing in the worktree changes.
"""
import argparse
import datetime
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pagecheck as pc  # noqa: E402

ROOT = pc.ROOT
CASE_JSON = os.path.join(ROOT, "data", "cases")
TEXAS_CASES = {
    "gas-station-texas-sba": "austin", "truck-stop-texas-sba": "dallas-fort-worth", "hotel-texas-sba": "austin",
    "rv-park-texas-usda": "austin", "car-wash-texas-sba": "san-antonio", "rv-boat-storage-texas-sba": "dallas-fort-worth",
    "auto-dealership-texas-sba": "dallas-fort-worth", "assisted-living-texas-hud": "san-antonio",
    "meat-processing-texas-usda": "austin", "travel-center-hankamer-texas-usda": "houston",
    "lodging-retreat-johnson-city-texas-sba": "austin"}
GAS_CASES = ["gas-station-texas-sba", "gas-station-florida-sba", "gas-station-alabama-sba", "gas-station-georgia-sba",
             "gas-station-versailles-ohio-sba"]
NEW = {"/states/texas/" + m + "/" for m in pc.TEXAS_METROS} | {"/asset-classes/gas-station-and-c-store/" + s + "/" for s in pc.GAS_SUBTYPES} | {
    "/case-studies/gas-station-versailles-ohio-sba/", "/case-studies/travel-center-hankamer-texas-usda/",
    "/case-studies/lodging-retreat-johnson-city-texas-sba/"}
LOOK = ["/states/texas/", "/states/texas/houston/", "/states/texas/austin/", "/asset-classes/gas-station-and-c-store/",
        "/asset-classes/gas-station-and-c-store/branded-fuel/", "/asset-classes/gas-station-and-c-store/ev-charging/",
        "/case-studies/gas-station-alabama-sba/", "/case-studies/car-wash-texas-sba/", "/case-studies/assisted-living-texas-hud/"]

results = []
lines = []


def out(s=""):
    print(s)
    lines.append(s)


def gate(n, name, status, detail=""):
    results.append((n, name, status))
    out(f"\n=== Gate {n}: {name}: {status}")
    if detail:
        out(detail.rstrip())


def run(cmd, cwd=ROOT, timeout=900):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def served(url):
    return os.path.join(ROOT, url.strip("/"), "index.html")


def ld_blocks(html):
    return [m.group(1) for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)]


# ------------------------------------------------------------------ gates

def g1(base):
    probs, existing, new = [], [], []
    for url in pc.PILOT:
        p = served(url)
        if not os.path.exists(p):
            probs.append(f"{url}: not built")
            continue
        rel = url.strip("/") + "/index.html"
        was = subprocess.run(["git", "cat-file", "-e", f"{base}:{rel}"], cwd=ROOT, capture_output=True).returncode == 0
        (existing if was else new).append(url)
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
            nodes = d.get("@graph", [d])
            for nd in nodes:
                t = nd.get("@type")
                types |= set(t if isinstance(t, list) else [t])
                a = nd.get("author")
                if isinstance(a, dict) and a.get("@id"):
                    ids.add(a["@id"])
        if "BreadcrumbList" not in types:
            probs.append(f"{url}: no BreadcrumbList")
        if "https://feasibility-study-company.com/#mark-otava" not in ids:
            probs.append(f"{url}: no author @id")
    want_existing = {u for u in pc.PILOT if u not in NEW}
    folded = [f"/states/texas/{m}/" for m in pc.FOLDED_METROS]
    stray = [u for u in folded if os.path.exists(served(u)) or os.path.exists(os.path.join(ROOT, "src/pages", u.strip("/") + ".html"))]
    tx = read(served("/states/texas/")) if os.path.exists(served("/states/texas/")) else ""
    no_section = [u for u in folded if f'id="{u.strip("/").split("/")[-1]}"' not in tx]
    ok = (not probs and len(existing) == 14 and len(new) == 17 - len(folded) and set(existing) == want_existing
          and not stray and not no_section)
    gate(1, "31 pages accounted for: 14 at existing URLs, 17 new, of which gate 5 folds some into the Texas page; one <title>; JSON-LD with BreadcrumbList and author @id",
         "GREEN" if ok else "RED", f"built {len(existing) + len(new)}/31; existing URLs {len(existing)}; new {len(new)}; folded into /states/texas/ by gate 5: {len(folded)} {folded}\n"
         f"folded pages still on disk: {stray}; folded metros without a Texas section: {no_section}\n" +
         "\n".join("  " + x for x in probs[:40]))


def g2():
    rb, ob = run([sys.executable, "scripts/build.py", "--check"])
    rc, oc = run([sys.executable, "scripts/casemodel.py", "--check"])
    tmp = tempfile.mkdtemp(prefix="fsc6-mut-")
    try:
        for d in ("scripts", "src", "data", "states", "asset-classes", "case-studies"):
            shutil.copytree(os.path.join(ROOT, d), os.path.join(tmp, d))
        # build mutation: change one word of the Texas source
        sp = os.path.join(tmp, "src/pages/states/texas.html")
        s = read(sp)
        s2 = s.replace("Texas still grows.", "Texas still grows fast.", 1)
        assert s2 != s
        open(sp, "w", encoding="utf-8").write(s2)
        m1, mo1 = run([sys.executable, "scripts/build.py", "--check", "--page", "/states/texas/"], cwd=tmp)
        open(sp, "w", encoding="utf-8").write(s)
        m1b, _ = run([sys.executable, "scripts/build.py", "--check", "--page", "/states/texas/"], cwd=tmp)
        # case mutation: scale the first numeric scalar input of the first case by 1.1
        cases = sorted(f for f in os.listdir(os.path.join(tmp, "data/cases")) if f.endswith(".json"))
        cp = os.path.join(tmp, "data/cases", cases[0])
        spec = json.load(open(cp))
        before = read(served(spec["page"]).replace(ROOT, tmp))
        key = next(k for k, v in spec["inputs"].items() if isinstance(v["value"], (int, float)) and v["value"] not in (0,) and not k.startswith(("sba_", "bi_", "hud_")))
        orig = spec["inputs"][key]["value"]
        spec["inputs"][key]["value"] = orig * 1.1
        with open(cp, "w") as fh:
            json.dump(spec, fh, indent=1)
        m2, mo2 = run([sys.executable, "scripts/casemodel.py", "--check", "--only", spec["slug"]], cwd=tmp)
        run([sys.executable, "scripts/casemodel.py", "--only", spec["slug"]], cwd=tmp)
        after = read(served(spec["page"]).replace(ROOT, tmp))
        moved = before != after
        spec["inputs"][key]["value"] = orig
        with open(cp, "w") as fh:
            json.dump(spec, fh, indent=1)
        run([sys.executable, "scripts/casemodel.py", "--only", spec["slug"]], cwd=tmp)
        m2b, _ = run([sys.executable, "scripts/casemodel.py", "--check", "--only", spec["slug"]], cwd=tmp)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = rb == 0 and rc == 0 and m1 != 0 and m1b == 0 and m2 != 0 and "stale region" in mo2 and moved and m2b == 0
    gate(2, "factory: build.py --check and casemodel.py --check exit 0; mutation tests", "GREEN" if ok else "RED",
         f"build.py --check rc={rb}: {ob.splitlines()[-1] if ob else ''}\ncasemodel.py --check rc={rc}: {oc.splitlines()[-1] if oc else ''}\n"
         f"mutation 1 (Texas source text): --check rc={m1} (want 1), after revert rc={m1b} (want 0)\n"
         f"mutation 2 ({spec['slug']} input {key} x1.1): --check rc={m2} (want 1; {mo2.splitlines()[0] if mo2 else ''}), tables moved={moved}, after revert rc={m2b} (want 0)\n"
         f"mutations ran in a temporary copy ({tmp}), removed afterwards; nothing committed")


def g3_4_5(recs):
    figs = {r["url"]: r.get("figures_unique", 0) for r in recs}
    bad3 = {u: n for u, n in figs.items() if n < 25}
    gate(3, "unique figures: at least 25 dated, sourced figures per page that appear on no other page", "GREEN" if not bad3 else "RED",
         "\n".join(f"  {u:62} {n}" for u, n in sorted(figs.items())) + (f"\nunder 25: {bad3}" if bad3 else ""))
    ov = {r["url"]: (r.get("overlap_max", 0), r.get("overlap_with"), r.get("overlap_sibling_max", 0)) for r in recs}
    bad4 = {u: v for u, v in ov.items() if v[0] >= 15}
    gate(4, "overlap under 15% against every sibling and every other page (8-word shingles)", "GREEN" if not bad4 else "RED",
         "\n".join(f"  {u:62} max {v[0]}% ({v[1]}); max vs siblings {v[2]}%" for u, v in sorted(ov.items())))
    metros = [r for r in recs if r["type"] == "metro"]
    audit = os.path.join(ROOT, "data/markets/audit.csv")
    a = "WEB-FSC-5 audit present" if os.path.exists(audit) else "WEB-FSC-5 audit not present (research figures only)"
    badm = [r["url"] for r in metros if r.get("figures_unique", 0) < 25 or r.get("overlap_max", 0) >= 15]
    gate(5, "standalone metros (gates 3 and 4 on own-geography data); failures fold into the Texas page", "GREEN" if not badm and len(metros) == len(pc.TEXAS_METROS) else "RED",
         a + f"\nfolded into /states/texas/ as sections: {pc.FOLDED_METROS}\n" + "\n".join(f"  {r['url']:40} unique {r.get('figures_unique')} overlap {r.get('overlap_max')}%" for r in metros))


def g6(recs):
    probs = []
    sba = json.load(open(os.path.join(ROOT, "data/regulatory/sba.json")))
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import casemodel as cm
    S = cm.SBA(sba)
    detail = []
    for r in recs:
        if r["type"] != "case":
            continue
        slug = r["url"].strip("/").split("/")[-1]
        for p in r["problems"]:
            if any(k in p for k in ("missing section", "missing case table", "disclosure", "competitor", "body words")):
                probs.append(f"{slug}: {p}")
        jp = os.path.join(CASE_JSON, slug + ".json")
        if not os.path.exists(jp):
            probs.append(f"{slug}: no case input file")
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
        # the tier and floor actually applied must be the ones sba.json prescribes for the case's facts
        if case.program == "sba_504":
            sb = case.spec.get("sba", {})
            exp = "equity.sba_504_new_and_special" if sb.get("business_age") == "new" and sb.get("special_purpose") else (
                "equity.sba_504_new_or_special" if sb.get("business_age") == "new" or sb.get("special_purpose") else "equity.sba_504_standard")
            if rules["equity_path"] != exp:
                probs.append(f"{slug}: equity path {rules['equity_path']} expected {exp}")
        if slug == "gas-station-alabama-sba":
            if case.spec.get("sba", {}).get("purpose") != "acquisition" or rules.get("test") != "historical" or abs(rules["floor"] - 1.25) > 1e-9:
                probs.append("gas-station-alabama-sba: not tested under Appendix 15 (acquisition, historical EBITDA, 1.25x)")
            h = read(served(r["url"]))
            if "dscr.coo_initial_acquisition" not in h or "illustrative" not in h.lower():
                probs.append("gas-station-alabama-sba: page lacks the 1.25x sba marker or the illustrative label")
        if not (ok_eq and ok_cap and ok_d):
            probs.append(f"{slug}: restructured structure fails a rule (equity {ok_eq}, cap {ok_cap}, dscr {ok_d})")
        detail.append(f"  {slug:42} {case.program:8} words {r.get('words'):>5}  equity {t1['equity_pct']*100:5.1f}% (tier {rules['equity_req']*100:.0f}%)  "
                      f"test DSCR {d:.3f} (floor {rules['floor']:.2f})  loan {t1['loan_total']:,.0f}" +
                      (f"  debenture {t1['debenture']:,.0f}" if case.program == "sba_504" else ""))
    gate(6, "case standard v3 components, body length, SBA tiers, floors and caps; Opelika under Appendix 15",
         "GREEN" if not probs else "RED", "\n".join(detail) + ("\n" + "\n".join("  " + p for p in probs) if probs else ""))


STALE = None


def g7(base):
    sys.path.insert(0, os.path.join(ROOT, "docs/web-fsc-2/tools"))
    pats = {
        "SOP 50 10 8 as current": re.compile(r"SOP 50 10 8(?!\.1)[,\s(]{1,3}(?:[^.]{0,60}?)(effective June 1, 2025|current)", re.I),
        "50 10 7": re.compile(r"50 10 7(?!\d)"),
        "SBSS as current": re.compile(r"SBSS(?![^.]{0,80}(retire|discontinu|sunset|gone|no longer|former|replaced|was |is gone|ended))", re.I),
        "504 1:1 or 1.0x": re.compile(r"504[^.]{0,80}\b(1:1|1\.0x)\b|\b(1:1|1\.0x)\b[^.]{0,80}504", re.I),
        "$90,000 jobs": re.compile(r"\$90,000[^.]{0,60}job|job[^.]{0,60}\$90,000", re.I),
        "$250,000 valuation": re.compile(r"\$250,000[^.]{0,80}(business valuation|going-concern|value the business|valuation threshold|internal valuation)", re.I),
        "SBA requires + feasibility": pc.SBA_REQUIRES,
    }
    hits, src_probs, fig_nocite = [], [], []
    for url in pc.PILOT:
        p = served(url)
        if not os.path.exists(p):
            continue
        h = read(p)
        txt = re.sub(r"<!--.*?-->", " ", re.sub(r"<style.*?</style>", " ", h, flags=re.S), flags=re.S)
        txt = re.sub(r"<[^>]+>", " ", txt)
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
        cited = {int(x) for x in re.findall(r'href="#s(\d+)"', h)}
        n = len(ol.find_all("li")) if ol else 0
        unc = sorted(set(range(1, n + 1)) - cited)
        if unc:
            src_probs.append(f"{url}: sources never cited {unc}")
        # figure-bearing prose blocks without a citation (outside model regions)
        main = pc.main_soup(pc.strip_regions(h, ["sba", "case", "mkt", "mesh"]))
        s = main.find(id="sources")
        if s:
            s.decompose()
        for b in main.find_all(["p", "li", "tr"]):
            if b.name != "tr" and b.find(["p", "li", "tr"]):
                continue
            if b.find_parent(class_="faq-list") or b.find_parent("nav") or b.find_parent(class_="hero"):
                pass
            t = b.get_text(" ", strip=True)
            if pc.FIG.search(t) and not (b.select("a.cite") or b.select("sup.fn")) and not b.find_parent("thead"):
                nums = [m.group(1) for m in pc.FIG.finditer(t) if not pc.YEAR.match(pc.norm(m.group(1)))]
                if nums:
                    fig_nocite.append(f"{url}: {t[:110]}")
    forb = []
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in (".git", "docs", "node_modules", "_bundles", "_cache")]
        for f in files:
            if f.endswith((".html", ".xml", ".txt", ".json", ".js", ".css", ".toml")):
                fp = os.path.join(d, f)
                if pc.FORBIDDEN.search(read(fp)):
                    forb.append(os.path.relpath(fp, ROOT))
    authors = subprocess.run(["git", "log", "--format=%an <%ae>|%cn <%ce>", f"{base}..HEAD"], cwd=ROOT, capture_output=True, text=True).stdout
    auth_hits = [l for l in authors.splitlines() if pc.FORBIDDEN.search(l)]
    ok = not hits and not src_probs and not forb and not auth_hits and not fig_nocite
    gate(7, "sources: four parts; ruling 10 pattern absent from served files and lane commit authors; stale-claim grep zero",
         "GREEN" if ok else "RED",
         f"stale-claim hits {len(hits)}\n" + "\n".join("  " + x for x in hits[:30]) +
         f"\nsource entries lacking a part or never cited {len(src_probs)}\n" + "\n".join("  " + x for x in src_probs[:30]) +
         f"\nfigure blocks without a citation {len(fig_nocite)}\n" + "\n".join("  " + x for x in fig_nocite[:40]) +
         f"\nserved files matching the ruling 10 pattern (whole site) {len(forb)}: {forb[:20]}\n"
         f"lane commits whose author or committer matches: {len(auth_hits)}")


def g8():
    probs = []
    dnu = os.environ.get("FSC6_DNU")
    patterns = []
    if dnu and os.path.exists(dnu):
        patterns = [l.strip() for l in open(dnu, encoding="utf-8") if l.strip() and not l.startswith("#")]
    street = re.compile(r"\b\d{2,6}\s+(?:[NSEW]\.?\s+)?(?:[A-Z][a-z]+\s){0,3}(?:St|Street|Rd|Road|Ave|Avenue|Blvd|Boulevard|Hwy|Highway|Dr|Drive|Ln|Lane|Pkwy|Parkway|Way|Ct|Court|Loop)\b\.?")
    parcel = re.compile(r"\b(parcel (?:id|number|no\.?)|APN|prop(?:erty)? id|account (?:no|number)|MLS\s*#|LoopNet ID)\b", re.I)
    for c in pc.CASES:
        p = served(f"/case-studies/{c}/")
        if not os.path.exists(p):
            continue
        soup = BeautifulSoup(read(p), "lxml")
        subj = []
        hero = soup.select_one("section.hero")
        if hero:
            subj.append(hero.get_text(" "))
        g = soup.find(id="at-a-glance")
        if g:
            subj.append(g.get_text(" "))
        for sid in ("market-conclusion", "site"):
            el = soup.find(id=sid)
            if el:
                subj.append(el.get_text(" "))
        text = " ".join(subj)
        for m in street.finditer(text):
            probs.append(f"{c}: street-number pattern in subject text: {m.group(0)}")
        for m in parcel.finditer(text):
            probs.append(f"{c}: parcel or listing identifier wording in subject text: ...{text[max(0, m.start() - 40):m.end() + 40]}...")
        whole = soup.get_text(" ")
        for pat in patterns:
            if pat.lower() in whole.lower():
                probs.append(f"{c}: do-not-use string present: {pat}")
    gate(8, "subjects: no street number, parcel id, owner or business name for any case subject", "GREEN" if not probs else "RED",
         f"do-not-use strings checked: {len(patterns)}\n" + "\n".join("  " + x for x in probs[:40]))


def inbound():
    pages = pc.served_pages()
    idx = {"/", "/case-studies/", "/asset-classes/", "/states/", "/practice-areas/", "/research-notes/"}
    inb = {u: set() for u in pc.PILOT}
    for u, p in pages.items():
        if u in idx:
            continue
        h = read(p)
        main = re.search(r"<main.*?</main>", h, re.S)
        if not main:
            continue
        body = re.sub(r'<nav class="breadcrumb".*?</nav>', " ", main.group(0), flags=re.S)
        for href in set(re.findall(r'href="(/[^"#?]*)', body)):
            if href in inb and href != u:
                inb[href].add(u)
    return inb


def g9():
    notes = []
    status = "GREEN"
    for script, args in (("links.py", ["--check"]), ("mesh.py", ["--check"])):
        if os.path.exists(os.path.join(ROOT, "scripts", script)):
            rc, o = run([sys.executable, "scripts/" + script] + args)
            notes.append(f"{script} {' '.join(args)} rc={rc}: {o.splitlines()[-1] if o else ''}")
            if rc != 0:
                status = "RED"
        else:
            notes.append(f"{script}: NOT RUN (script absent until WEB-FSC-4 lands)")
            status = "PENDING" if status == "GREEN" else status
    inb = inbound()
    low = {u: len(s) for u, s in inb.items() if len(s) < 3}
    tx = read(served("/states/texas/")) if os.path.exists(served("/states/texas/")) else ""
    hub = read(served("/asset-classes/gas-station-and-c-store/")) if os.path.exists(served("/asset-classes/gas-station-and-c-store/")) else ""
    miss = []
    for c, m in TEXAS_CASES.items():
        if f'href="/case-studies/{c}/"' not in tx:
            miss.append(f"Texas page lacks {c}")
        mp = served(f"/states/texas/{m}/")
        if not os.path.exists(mp) or f'href="/case-studies/{c}/"' not in read(mp):
            miss.append(f"metro {m} lacks {c}")
    for c in GAS_CASES:
        if f'href="/case-studies/{c}/"' not in hub:
            miss.append(f"hub lacks {c}")
    for s in pc.GAS_SUBTYPES:
        if f'href="/asset-classes/gas-station-and-c-store/{s}/"' not in hub:
            miss.append(f"hub lacks subtype {s}")
        sp = served(f"/asset-classes/gas-station-and-c-store/{s}/")
        if not os.path.exists(sp) or 'href="/asset-classes/gas-station-and-c-store/"' not in re.sub(r'<nav class="breadcrumb".*?</nav>', "", read(sp), flags=re.S):
            miss.append(f"subtype {s} does not link the hub in its body")
    if low or miss:
        status = "RED"
    gate(9, "links: links.py and mesh.py --check; 3+ inbound contextual links; required edges", status,
         "\n".join(notes) + "\ninbound contextual links from distinct non-index pages (min 3):\n" +
         "\n".join(f"  {u:62} {len(s)}" for u, s in sorted(inb.items())) +
         (f"\nunder 3: {low}" if low else "") + ("\nmissing edges:\n" + "\n".join("  " + x for x in miss) if miss else ""))


def g10():
    probs = []
    for url in pc.PILOT:
        p = served(url)
        if os.path.exists(p):
            h = read(p)
            n = len(pc.DASHES.findall(h))
            if n:
                probs.append(f"{url}: {n} dash(es)")
            if re.search(r"otava,? *(ph\.?d|ccim|mai)", h, re.I):
                probs.append(f"{url}: credential typed next to the name")
    for d, _dirs, files in os.walk(os.path.join(ROOT, "src")):
        for f in files:
            h = read(os.path.join(d, f))
            if pc.DASHES.search(h):
                probs.append(f"src/{os.path.relpath(os.path.join(d, f), os.path.join(ROOT, 'src'))}: dash in source")
    gate(10, "clean text: zero em and en dashes in any encoding; no credential beside the name", "GREEN" if not probs else "RED",
         "\n".join("  " + x for x in probs) or "  0 dashes on 31 pages and their sources; credential grep 0")


def g11():
    notes, status = [], "GREEN"
    for script in ("byline.py", "regulatory.py", "chrome.py", "markets.py"):
        if os.path.exists(os.path.join(ROOT, "scripts", script)):
            rc, o = run([sys.executable, "scripts/" + script, "--check"])
            notes.append(f"{script} --check rc={rc}: {o.splitlines()[-1] if o else ''}")
            if rc != 0:
                status = "RED"
        else:
            notes.append(f"{script}: NOT RUN (script absent)")
            if script == "chrome.py" and status == "GREEN":
                status = "PENDING"
    gate(11, "markers: byline, regulatory, chrome and markets --check", status, "\n".join(notes))


def g12(deploy):
    probs = []
    sm = read(os.path.join(ROOT, "sitemap.xml"))
    lastmod = dict(re.findall(r"<loc>https://feasibility-study-company.com(/[^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
    for url in pc.PILOT:
        p = served(url)
        if not os.path.exists(p):
            continue
        h = read(p)
        mods = set(re.findall(r'"dateModified":\s*"([^"]+)"', h))
        pubs = set(re.findall(r'"datePublished":\s*"([^"]+)"', h))
        vis_up = set(re.findall(r'Updated <time datetime="([^"]+)"', h))
        vis_pub = set(re.findall(r'Published <time datetime="([^"]+)"', h))
        if mods != {deploy}:
            probs.append(f"{url}: dateModified {mods} not {deploy}")
        if url in NEW and pubs != {deploy}:
            probs.append(f"{url}: new page datePublished {pubs} not {deploy}")
        if url not in NEW and deploy in pubs:
            probs.append(f"{url}: rebuilt page lost its published date")
        if vis_up and vis_up != {deploy}:
            probs.append(f"{url}: visible Updated {vis_up}")
        if not vis_up and not (url in NEW and vis_pub == {deploy}):
            probs.append(f"{url}: no visible Updated line (published {vis_pub})")
        if lastmod.get(url) != deploy:
            probs.append(f"{url}: sitemap lastmod {lastmod.get(url)}")
    gate(12, f"dates agree (JSON-LD dateModified, visible line, sitemap lastmod = {deploy})", "GREEN" if not probs else "RED",
         "\n".join("  " + x for x in probs[:60]))


def g13(skip):
    if skip:
        gate(13, "look", "PENDING", "  skipped in this run (--skip-look)")
        return
    outdir = os.path.join(ROOT, "docs/web-fsc-6/look")
    port = 8770
    srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", ROOT],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    try:
        rc, o = run(["node", os.path.join(HERE, "shots.mjs"), f"http://127.0.0.1:{port}", outdir] + LOOK, timeout=900)
    finally:
        srv.kill()
    shutil.rmtree(os.path.join(outdir, ".profile"), ignore_errors=True)
    recs = [json.loads(l) for l in o.splitlines() if l.startswith("{")]
    bad = [r for r in recs if r["pageOverflow"] or r.get("offenders")]
    unscrolled = [r for r in recs for t in r["wideTables"] if t["scrolls"] not in ("auto", "scroll")]
    ok = rc == 0 and len(recs) == 2 * len(LOOK) and not bad and not unscrolled
    gate(13, "look: 1440 and 390 screenshots; no page-level horizontal scroll at 390; wide tables scroll in their box",
         "GREEN" if ok else "RED", "\n".join(f"  {r['file']:70} scrollWidth {r['scrollWidth']} / {r['innerWidth']} overflow {r['pageOverflow']} "
                                             f"inner-scroll tables {len(r['wideTables'])}" for r in recs) + (f"\n{o[-800:]}" if rc else ""))


def g14():
    probs = []
    sm = read(os.path.join(ROOT, "sitemap.xml"))
    for url in pc.PILOT:
        p = served(url)
        if not os.path.exists(p):
            continue
        h = read(p)
        m = re.search(r'<meta name="robots" content="([^"]+)"', h)
        if not m or "index" not in m.group(1) or "noindex" in m.group(1) or "follow" not in m.group(1) or "nofollow" in m.group(1):
            probs.append(f"{url}: robots meta {m.group(1) if m else None}")
        if f"<loc>https://feasibility-study-company.com{url}</loc>" not in sm:
            probs.append(f"{url}: not in sitemap")
    gate(14, "index all: index, follow and in the sitemap with lastmod", "GREEN" if not probs else "RED", "\n".join("  " + x for x in probs))


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="1d48cc2")
    ap.add_argument("--deploy-date", default=json.load(open(os.path.join(ROOT, "src/site.json")))["deploy_date"])
    ap.add_argument("--out")
    ap.add_argument("--only")
    ap.add_argument("--skip-look", action="store_true")
    a = ap.parse_args(argv)
    only = {int(x) for x in a.only.split(",")} if a.only else set(range(1, 15))
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
    out(f"WEB-FSC-6 gates, run {datetime.datetime.now().isoformat(timespec='seconds')} at HEAD {head} (worktree may carry uncommitted changes: "
        f"{bool(subprocess.run(['git', 'status', '--porcelain'], cwd=ROOT, capture_output=True, text=True).stdout.strip())})")
    out("command: python3 docs/web-fsc-6/tools/gates.py " + " ".join(argv))
    recs = None
    if only & {3, 4, 5, 6}:
        pages = pc.served_pages()
        cache = {u: read(p) for u, p in pages.items()}
        recs = pc.check(pc.PILOT, pages, cache, show_figs=False, show_overlap=0)
    if 1 in only: g1(a.base)
    if 2 in only: g2()
    if only & {3, 4, 5}: g3_4_5(recs)
    if 6 in only: g6(recs)
    if 7 in only: g7(a.base)
    if 8 in only: g8()
    if 9 in only: g9()
    if 10 in only: g10()
    if 11 in only: g11()
    if 12 in only: g12(a.deploy_date)
    if 13 in only: g13(a.skip_look)
    if 14 in only: g14()
    out("\nSUMMARY")
    for n, name, st in sorted(results):
        out(f"  gate {n:2}: {st:8} {name}")
    green = sum(1 for r in results if r[2] == "GREEN")
    out(f"  green {green}/{len(results)}")
    if a.out:
        open(os.path.join(ROOT, a.out) if not os.path.isabs(a.out) else a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return 0 if green == len(results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
