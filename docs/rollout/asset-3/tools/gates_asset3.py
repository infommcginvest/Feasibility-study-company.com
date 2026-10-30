#!/usr/bin/env python3
"""ASSET-3 gates 1 to 14 for one tranche, run on a throwaway copy of the merged tree (ROLLOUT-1 gates,
amendments A6 and A9). Written because FACTORY-2's scripts/qa/gates.py had not landed; it measures with
pagecheck.py's own definitions.

    python3 docs/rollout/asset-3/tools/gates_asset3.py --root <throwaway copy> --git-dir <worktree>
            --manifest <tranche manifest.json> [--out GATES-t<n>.txt] [--look-dir <dir>] [--skip-look]

The manifest:
    {"tranche": 1, "hub": "private-school", "rebuilt": true, "published": "2026-07-12",
     "pages": ["/asset-classes/private-school/", "/asset-classes/private-school/independent-nais/"],
     "folded": ["catholic-parochial", ...], "cases": ["/case-studies/..."], "base": "<sha the lane cut from>"}
"""
import argparse
import datetime
import glob
import html
import importlib.util
import json
import os
import re
import shutil
import socket
import subprocess
import sys
import urllib.parse

from bs4 import BeautifulSoup

HERE = os.path.dirname(os.path.realpath(__file__))
PRIVATE = os.path.expanduser("~/Downloads/fsc-rollout/private")
INDEX_PAGES = {"/", "/case-studies/", "/asset-classes/", "/states/", "/practice-areas/", "/research-notes/",
               "/analytical-framework/"}
FLOORS = {"total": 30, "research": 20, "register_cap": 10}
results, lines = [], []


def out(s=""):
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


def load_pc(root):
    spec = importlib.util.spec_from_file_location("pagecheck", os.path.join(root, "docs/web-fsc-6/tools/pagecheck.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = root
    return mod


MKT = re.compile(r"<!--mkt:([a-z0-9/:-]+)\.([a-z0-9_]+)(?:\.[a-z0-9-]+)?( \{.*?\})?-->")


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--out")
    ap.add_argument("--look-dir")
    ap.add_argument("--skip-look", action="store_true")
    a = ap.parse_args(argv)
    root, gd = os.path.abspath(a.root), os.path.abspath(a.git_dir)
    man = json.load(open(a.manifest))
    pc = load_pc(root)
    pages = man["pages"]
    hub_url = f"/asset-classes/{man['hub']}/"
    deploy = json.load(open(os.path.join(root, "src/site.json")))["deploy_date"]

    def served(u):
        return os.path.join(root, u.strip("/"), "index.html")

    def read(p):
        return open(p, encoding="utf-8", errors="replace").read()

    out(f"ASSET-3 gates, tranche {man['tranche']} ({man['hub']}), run {datetime.datetime.now().isoformat(timespec='seconds')}")
    out(f"root (throwaway copy): {os.path.basename(root)}; git dir: worktree rollout-asset-3 at "
        f"{run(['git', 'rev-parse', '--short', 'HEAD'], gd)[1]}; deploy_date {deploy}")
    out("pages: " + ", ".join(pages))

    # ---- gate 1
    probs = []
    for u in pages:
        p = served(u)
        if not os.path.exists(p):
            probs.append(f"{u}: not built")
            continue
        h = read(p)
        if len(re.findall(r"<title>", re.sub(r"<!--.*?-->", "", h, flags=re.S))) != 1:
            probs.append(f"{u}: not exactly one <title>")
        types, ids = set(), set()
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                d = json.loads(b)
            except ValueError as e:
                probs.append(f"{u}: JSON-LD does not parse: {e}")
                continue
            for nd in d.get("@graph", [d]):
                t = nd.get("@type")
                types |= set(t if isinstance(t, list) else [t])
                au = nd.get("author")
                if isinstance(au, dict) and au.get("@id"):
                    ids.add(au["@id"])
        if "BreadcrumbList" not in types:
            probs.append(f"{u}: no BreadcrumbList")
        if not any(i.endswith("#mark-otava") for i in ids):
            probs.append(f"{u}: no author @id")
    gate(1, "pages build; one <title>; JSON-LD parses with BreadcrumbList and author @id",
         "GREEN" if not probs else "RED", "\n".join("  " + x for x in probs) or f"  {len(pages)} pages checked")

    # ---- gate 2
    rb, ob = run([sys.executable, "scripts/build.py", "--check"], root)
    gate(2, "factory: build.py --check exits 0 (no case in this tranche, so no casemodel mutation is owed)",
         "GREEN" if rb == 0 else "RED", f"  build.py --check rc={rb}: {ob.splitlines()[-1] if ob else ''}")

    # ---- gates 3, 4, 5
    allp = pc.served_pages()
    cache = {u: read(p) for u, p in allp.items()}
    figs_by = {}
    shingles = {}
    for u, h in cache.items():
        m = pc.main_soup(pc.strip_regions(h, ["sba", "case", "mkt", "mesh"]))
        figs_by[u] = [k for raw, k in pc.figures_in(m.get_text(" ")) if not pc.YEAR.match(pc.norm(raw))]
        shingles[u] = pc.shingles(pc.overlap_text(pc.strip_regions(h, ["mesh"])))
    rec = {}
    for u in pages:
        h = cache.get(u)
        if h is None:
            continue
        idx = pc.NumberIndex()
        for v, ks in figs_by.items():
            if v != u:
                for k in ks:
                    idx.add(k)
        research = [raw for n, (raw, k) in pc.sourced_figures(h).items() if not idx.has(k)]
        pairs = sorted({(g, s) for g, s, _ in MKT.findall(h)})
        reg = min(len(pairs), FLOORS["register_cap"])
        mine = shingles[u]
        worst, wu, sib = 0.0, "", {}
        for v, sh in shingles.items():
            if v == u or not sh or not mine:
                continue
            ov = len(mine & sh) / min(len(mine), len(sh))
            if v in pages:
                sib[v] = ov
            if ov > worst:
                worst, wu = ov, v
        rec[u] = {"words": pc.body_words(h), "research": len(research), "register": reg, "pairs": len(pairs),
                  "total": len(research) + reg, "overlap": worst * 100, "against": wu, "sib": sib}
    bad3 = [u for u, r in rec.items() if r["total"] < FLOORS["total"] or r["research"] < FLOORS["research"]]
    gate(3, "counted figures at READY: at least 30, of which at least 20 research, register counted at most 10 (A6)",
         "GREEN" if not bad3 and len(rec) == len(pages) else "RED",
         "\n".join(f"  {u:70} research {r['research']:3}  register {r['register']:2} (pairs {r['pairs']})  total {r['total']:3}  body words {r['words']}"
                   for u, r in rec.items()) + (f"\n  under the floor: {bad3}" if bad3 else ""))
    bad4 = [u for u, r in rec.items() if r["overlap"] >= 15]
    matrix = []
    for u, r in rec.items():
        matrix.append(f"  {u:70} max {r['overlap']:.2f}% ({r['against']})")
        for v, ov in sorted(r["sib"].items()):
            matrix.append(f"      vs sibling {v}: {ov * 100:.2f}%")
    gate(4, "overlap under 15% against every page on the site; sibling matrix", "GREEN" if not bad4 else "RED", "\n".join(matrix))
    subs = [u for u in pages if u != hub_url]
    hub_html = cache.get(hub_url, "")
    nosec = [s for s in man.get("folded", []) if f'id="{s}"' not in hub_html]
    stray = [s for s in man.get("folded", []) if os.path.exists(served(f"{hub_url}{s}/"))
             or os.path.exists(os.path.join(root, "src/pages", hub_url.strip("/"), s + ".html"))]
    rng = []
    for u, r in rec.items():
        lo, hi = (6000, 10000) if u == hub_url else (1800, 3000)
        if not lo <= r["words"] <= hi:
            rng.append(f"{u}: {r['words']} body words outside {lo} to {hi}")
    bad5 = [u for u in subs if u in bad3 or u in bad4]
    gate(5, "standalone subtypes pass gates 3 and 4 on their own evidence; folds carry a section id in the hub; word ranges (ruling 3)",
         "GREEN" if not (bad5 or nosec or stray or rng) else "RED",
         f"  subtype pages {len(subs)}: {subs}\n  folded sections in the hub {len(man.get('folded', []))}: {man.get('folded', [])}\n"
         f"  folded without a section: {nosec}; folded with a page on disk: {stray}\n" + "\n".join("  " + x for x in rng))

    # ---- gate 6
    gate(6, "case standard", "GREEN", "  not applicable: the tranche holds no case page (ASSET-3 builds hubs and subtypes only)")

    # ---- gate 7
    sys.path.insert(0, os.path.join(root, "docs/web-fsc-6/tools"))
    import sbamandate
    p7 = []
    for u in pages:
        h = cache.get(u, "")
        soup = BeautifulSoup(h, "lxml")
        ol = soup.select_one("ol.sources")
        lis = ol.find_all("li") if ol else []
        for li in lis:
            a_ = li.find("a", href=True)
            if not a_ or not a_["href"].startswith("http") or li.get_text(" ", strip=True).count(",") < 2:
                p7.append(f"{u}: source {li.get('id')} lacks a part")
        cited = {int(x) for x in re.findall(r'href="#s(\d+)"', h)}
        unc = sorted(set(range(1, len(lis) + 1)) - cited)
        if unc:
            p7.append(f"{u}: sources never cited {unc}")
        for sent in sbamandate.flagged(h):
            p7.append(f"{u}: SBA mandate wording: {sent[:140]}")
        if pc.FORBIDDEN.search(h):
            p7.append(f"{u}: ruling 9 pattern in served page")
        if "/Users/" in h:
            p7.append(f"{u}: absolute path in served page")
        src = os.path.join(root, "src/pages", u.strip("/") + ".html")
        if os.path.exists(src) and (pc.FORBIDDEN.search(read(src)) or "/Users/" in read(src)):
            p7.append(f"{u}: ruling 9 pattern or absolute path in source")
    mandate_site = []
    for v, h in cache.items():
        for sent in sbamandate.flagged(h):
            mandate_site.append(v)
    base = man.get("base", "0374505")
    log = run(["git", "log", "--format=%an <%ae>|%cn <%ce>|%s%n%b", f"{base}..HEAD"], gd)[1]
    tags = run(["git", "for-each-ref", "--format=%(contents)", "refs/tags/rollout/asset-3/"], gd)[1]
    for t, what in ((log, "lane commit authors or messages"), (tags, "lane tag messages")):
        if pc.FORBIDDEN.search(t):
            p7.append(f"ruling 9 pattern in {what}")
    gate(7, "sources have four parts and are all cited; sbamandate zero; ruling 9 pattern absent from pages, sources, commits and tags",
         "GREEN" if not p7 else "RED",
         "\n".join("  " + x for x in p7) or "  clean" +
         f"\n  SBA mandate sentences anywhere on the copy: {len(mandate_site)} (pages: {sorted(set(mandate_site))[:10]})")

    # ---- gate 8
    toks_all, per = [], {}
    lists = sorted(glob.glob(os.path.join(PRIVATE, "*.txt")))
    for f in lists:
        for l in open(f, encoding="utf-8", errors="replace"):
            l = l.rstrip("\n")
            if not l.strip() or l.startswith("#"):
                continue
            if "\t" in l:
                k, t = l.split("\t", 1)
                (toks_all if k == "*" else per.setdefault(k, [])).append(t.strip())
            else:
                toks_all.append(l.strip())

    def flat(s):
        s = html.unescape(urllib.parse.unquote(s)).lower()
        tk = re.findall(r"\d+(?:[.,]\d+)*|[a-z]+", s)
        return " " + " ".join(t.replace(",", "") if t[0].isdigit() else t for t in tk) + " "
    p8 = []
    texts = {}
    for u in pages:
        texts[u] = cache.get(u, "")
        src = os.path.join(root, "src/pages", u.strip("/") + ".html")
        if os.path.exists(src):
            texts[u + " (source)"] = read(src)
    texts["lane git history"] = run(["git", "log", "-p", f"{base}..HEAD", "--", "docs/rollout/asset-3", "src/pages/asset-classes"], gd)[1]
    for name, t in texts.items():
        ft, low = flat(t), t.lower()
        for tok in toks_all:
            if len(tok) < 4:
                continue
            if re.search(r"(?<![0-9a-z])" + re.escape(tok.lower()) + r"(?![0-9a-z])", low) or (len(flat(tok).split()) > 1 and flat(tok) in ft):
                p8.append(f"{name}: global identifier present: {tok}")
    gate(8, "subjects: no identifier from any list in private/ (A1: '*' lines everywhere; case lines only on their case, and this tranche has no case)",
         "GREEN" if not p8 else "RED",
         f"  lists read {len(lists)}: {[os.path.basename(x) for x in lists]}; global tokens {len(toks_all)}; per-case tokens {sum(len(v) for v in per.values())} (none apply: no case here)\n" +
         "\n".join("  " + x for x in p8[:40]))

    # ---- gate 9
    notes, st9 = [], "GREEN"
    for script in ("links.py", "mesh.py"):
        rc, o = run([sys.executable, "scripts/" + script, "--check"], root)
        notes.append(f"  {script} --check rc={rc}: {o.splitlines()[-1] if o else ''}")
        if rc != 0:
            st9 = "RED"
    inb = {u: set() for u in pages}
    for v, h in cache.items():
        if v in INDEX_PAGES:
            continue
        mm = re.search(r"<main.*?</main>", h, re.S)
        if not mm:
            continue
        body = re.sub(r'<nav class="breadcrumb".*?</nav>', " ", mm.group(0), flags=re.S)
        for href in set(re.findall(r'href="(/[^"#?]*)', body)) | set(re.findall(r'data-fsc-pending="(/[^"#?]*)', body)):
            if href in inb and href != v:
                inb[href].add(v)
    miss = []
    for s in subs:
        if f'href="{s}"' not in hub_html:
            miss.append(f"hub lacks a link to {s}")
        sh = re.sub(r'<nav class="breadcrumb".*?</nav>', "", cache.get(s, ""), flags=re.S)
        if f'href="{hub_url}"' not in sh and f'href="{hub_url}#' not in sh:
            miss.append(f"{s} does not link the hub in its body")
    for c in man.get("cases", []):
        if f'href="{c}"' not in hub_html:
            miss.append(f"hub lacks case {c}")
    low = {u: len(s) for u, s in inb.items() if len(s) < 3}
    if miss:
        st9 = "RED"
    gate(9, "links: links.py and mesh.py --check; required edges hub and subtype both ways, hub to its cases; inbound contextual links (3 needed after landing)",
         st9, "\n".join(notes) + "\n" + "\n".join(f"  inbound {u:66} {len(s)}  {sorted(s)[:6]}" for u, s in inb.items()) +
         (f"\n  under 3 in the copy (checked again at landing, where other lanes' links and relinks count): {low}" if low else "") +
         ("\n  missing edges:\n" + "\n".join("    " + x for x in miss) if miss else ""))

    # ---- gate 10
    p10 = []
    for u in pages:
        for t, what in ((cache.get(u, ""), "served"), (read(os.path.join(root, "src/pages", u.strip("/") + ".html")) if os.path.exists(os.path.join(root, "src/pages", u.strip("/") + ".html")) else "", "source")):
            n = len(pc.DASHES.findall(t))
            if n:
                p10.append(f"{u}: {n} dash(es) in {what}")
            if re.search(r"otava,? *(ph\.?d|ccim|mai)", t, re.I):
                p10.append(f"{u}: credential beside the name in {what}")
    gate(10, "clean text: zero em and en dashes in any encoding; no credential beside the name", "GREEN" if not p10 else "RED",
         "\n".join("  " + x for x in p10) or "  clean")

    # ---- gate 11
    notes, st = [], "GREEN"
    for script in ("byline.py", "regulatory.py", "chrome.py", "markets.py"):
        rc, o = run([sys.executable, "scripts/" + script, "--check"], root)
        notes.append(f"  {script} --check rc={rc}: {o.splitlines()[-1] if o else ''}")
        if rc != 0:
            st = "RED"
    gate(11, "markers: byline, regulatory, chrome and markets --check", st, "\n".join(notes))

    # ---- gate 12
    p12 = []
    sm = read(os.path.join(root, "sitemap.xml"))
    lastmod = dict(re.findall(r"<loc>https://feasibility-study-company.com(/[^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
    for u in pages:
        h = cache.get(u, "")
        mods = set(re.findall(r'"dateModified":\s*"([^"]+)"', h))
        pubs = set(re.findall(r'"datePublished":\s*"([^"]+)"', h))
        vis = set(re.findall(r'Updated <time datetime="([^"]+)"', h))
        want_pub = man["published"] if (u == hub_url and man.get("rebuilt")) else deploy
        if mods != {deploy}:
            p12.append(f"{u}: dateModified {mods}")
        if pubs and pubs != {want_pub}:
            p12.append(f"{u}: datePublished {pubs}, want {want_pub}")
        if vis and vis != {deploy}:
            p12.append(f"{u}: visible Updated {vis}")
        if lastmod.get(u) != deploy:
            p12.append(f"{u}: sitemap lastmod {lastmod.get(u)}")
    gate(12, f"dates: dateModified, visible line and sitemap lastmod agree ({deploy} in this copy; the integrator pins DEPLOY at landing); rebuilt hub keeps its published date",
         "GREEN" if not p12 else "RED", "\n".join("  " + x for x in p12) or "  agree")

    # ---- gate 13
    if a.skip_look or not a.look_dir:
        gate(13, "look", "PENDING", "  skipped")
    else:
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        tmpout = os.path.join(os.path.dirname(root), f"shots-tmp-{man['tranche']}")
        srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", root],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            rc, o = run(["node", os.path.join(root, "docs/web-fsc-6/tools/shots.mjs"), f"http://127.0.0.1:{port}", tmpout] + pages, root, 900)
        finally:
            srv.kill()
        shutil.rmtree(os.path.join(tmpout, ".profile"), ignore_errors=True)
        os.makedirs(a.look_dir, exist_ok=True)
        for f in glob.glob(os.path.join(tmpout, "*.png")):
            shutil.copy(f, a.look_dir)
        shutil.rmtree(tmpout, ignore_errors=True)
        recs = [json.loads(l) for l in o.splitlines() if l.startswith("{")]
        bad = [r for r in recs if r.get("pageOverflow") or r.get("offenders")]
        unscrolled = [r for r in recs for t in r.get("wideTables", []) if t.get("scrolls") not in ("auto", "scroll")]
        ok = rc == 0 and len(recs) == 2 * len(pages) and not bad and not unscrolled
        gate(13, "look: 1440 and 390 screenshots of every page; no page-level horizontal scroll at 390; wide tables scroll in their box",
             "GREEN" if ok else "RED", f"  http.server on free port {port}\n" + "\n".join(
                 f"  {r['file']:60} scrollWidth {r['scrollWidth']} / {r['innerWidth']} overflow {r['pageOverflow']} inner-scroll tables {len(r['wideTables'])}"
                 for r in recs) + (f"\n{o[-800:]}" if rc else ""))

    # ---- gate 14
    p14 = []
    for u in pages:
        h = cache.get(u, "")
        m = re.search(r'<meta name="robots" content="([^"]+)"', h)
        if not m or "noindex" in m.group(1) or "nofollow" in m.group(1) or "index" not in m.group(1):
            p14.append(f"{u}: robots {m.group(1) if m else None}")
        if f"<loc>https://feasibility-study-company.com{u}</loc>" not in sm:
            p14.append(f"{u}: not in sitemap")
    gate(14, "index all: index, follow and in the sitemap with lastmod", "GREEN" if not p14 else "RED", "\n".join("  " + x for x in p14) or "  all indexable")

    out("\nSUMMARY")
    for n, name, st in sorted(results):
        out(f"  gate {n:2}: {st:8} {name[:100]}")
    green = sum(1 for r in results if r[2] == "GREEN")
    out(f"  green {green}/14")
    out("\nPER PAGE (json)")
    out(json.dumps({u: {k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k != "sib"} for u, r in rec.items()}))
    if a.out:
        open(a.out, "w", encoding="utf-8").write("\n".join(lines) + "\n")
    return 0 if green == 14 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
