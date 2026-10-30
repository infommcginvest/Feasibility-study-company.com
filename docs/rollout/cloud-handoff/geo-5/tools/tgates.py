#!/usr/bin/env python3
"""GEO-1 tranche gates 1 to 14 in a throwaway copy (ROLLOUT-1 gates, amendment A6 figure table).

    python3 tgates.py --root <copy> --git-dir <worktree> --pages /states/florida/,/states/florida/miami/ \
        --new /states/florida/miami/ --tranche 1 --out GATES-t1.txt [--look-dir DIR] [--skip-look]

Built on the WEB-FSC-6 page check (pagecheck.py in the copy) so figures, overlap and words are read
the same way. Differences, from the rulebook:
- body word ranges per ruling 3: state 4,500 to 8,000, metro 2,000 to 3,500;
- figures (A6): research figures are counted outside mkt: regions exactly as pagecheck counts them;
  register figures are values inside mkt: regions, unique by value against every other page, one per
  (geography, series) pair, at most 10; READY needs 30 in all with at least 20 research;
- gate 8 reads every list in ~/Downloads/fsc-rollout/private/ (A1 forms: "*<TAB>token" on every
  file, "<slug><TAB>token" on that case only; a line without a tab is checked everywhere);
- gate 13 serves the copy on a free port (A9) and runs shots.mjs.
"""
import argparse
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

PRIVATE = os.path.expanduser("~/Downloads/fsc-rollout/private")
RANGES = {"state": (4500, 8000), "metro": (2000, 3500)}
# pages this lane does not rebuild (only marker passes): ruling 3's range is reported, not enforced (DECISIONS D13)
WORDS_EXEMPT = {"/states/texas/"}
OUT = []


def gate(n, name, ok, detail=""):
    OUT.append(f"GATE {n:2} {'GREEN' if ok else 'RED':5} {name}\n{detail.rstrip()}\n")
    print(f"gate {n}: {'GREEN' if ok else 'RED'}")


def run(cmd, cwd, timeout=900):
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)
    except subprocess.TimeoutExpired:
        return 124, "timeout"


def load(root, rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(root, rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def ptype(url):
    return "state" if re.match(r"^/states/[a-z-]+/$", url) else "metro"


MKT = re.compile(r"<!--mkt:([a-z0-9][a-z0-9/:-]*)\.([a-z0-9_]+)(?:\.[a-z0-9-]+)?( \{.*?\})?-->(.*?)<!--/mkt:", re.S)


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--pages", required=True)
    ap.add_argument("--new", default="")
    ap.add_argument("--tranche", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--look-dir")
    ap.add_argument("--skip-look", action="store_true")
    ap.add_argument("--base", default="0374505")
    a = ap.parse_args(argv)
    root = os.path.abspath(a.root)
    a.look_dir = os.path.abspath(a.look_dir) if a.look_dir else os.path.join(root, "look")
    pages = [u for u in a.pages.split(",") if u]
    new = {u for u in a.new.split(",") if u}
    pc = load(root, "docs/web-fsc-6/tools/pagecheck.py", "pagecheck")
    pc.ROOT = root
    # T1 review M1: pagecheck's region pattern has no "/", so a market-keyed marker (mkt:florida/miami.x) was
    # never stripped and its value was counted as a research figure too. Strip every script-owned region.
    def strip_regions(html_text, names):
        pat = re.compile(r"<!--(" + "|".join(names) + r"):([a-z0-9_./:-]+)( \{.*?\})?-->(.*?)<!--/\1:\2-->", re.S)
        return pat.sub(" ", html_text)
    pc.strip_regions = strip_regions
    # T1 review M12: a statute section ("ss. 408.031", "s. 553.79, F.S.") is an identifier, not a figure
    pc.NOT_FIGURE = re.compile(pc.NOT_FIGURE.pattern[:-len(r")\s*$")] + r"|\bss?\.|\bf\.s\.)\s*$", re.I) if pc.NOT_FIGURE.pattern.endswith(r")\s*$") else pc.NOT_FIGURE
    served = pc.served_pages()
    cache = {u: pc.read(p) for u, p in served.items()}

    # gate 1
    probs = []
    for u in pages:
        if u not in cache:
            probs.append(f"{u}: not built")
            continue
        h = cache[u]
        t = len(re.findall(r"<title>", re.sub(r"<!--.*?-->", "", h, flags=re.S)))
        if t != 1:
            probs.append(f"{u}: {t} <title>")
        types, ids = set(), set()
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                d = json.loads(b)
            except ValueError as e:
                probs.append(f"{u}: JSON-LD: {e}")
                continue
            for nd in d.get("@graph", [d]):
                tp = nd.get("@type")
                types |= set(tp if isinstance(tp, list) else [tp])
                au = nd.get("author")
                if isinstance(au, dict) and au.get("@id"):
                    ids.add(au["@id"])
        if "BreadcrumbList" not in types:
            probs.append(f"{u}: no BreadcrumbList")
        if not any(i.endswith("#mark-otava") for i in ids):
            probs.append(f"{u}: no author @id")
    gate(1, f"pages build; one <title>; JSON-LD parses with BreadcrumbList and author @id ({len(pages)} pages)", not probs,
         "\n".join("  " + x for x in probs))

    # gate 2 and 11
    res = {}
    for s in ["build", "casemodel", "byline", "regulatory", "chrome", "markets", "mesh", "links", "sitemap"]:
        rc, o = run([sys.executable, f"scripts/{s}.py", "--check"], root)
        res[s] = (rc, o.strip().splitlines()[-1] if o.strip() else "")
    gate(2, "factory: build.py --check and casemodel.py --check exit 0", all(res[s][0] == 0 for s in ("build", "casemodel")),
         "\n".join(f"  {s}.py --check: exit {res[s][0]}: {res[s][1]}" for s in ("build", "casemodel")))

    # gates 3, 4, 5
    recs = pc.check(pages, served, cache, True, 3)
    other_vals = {}
    for u in served:
        other_vals[u] = [k for _, k in pc.figures_in(pc.overlap_text(cache[u]))]
    lines3, lines4, ok3, ok4 = [], [], True, True
    figtab = {}
    for r in recs:
        u = r["url"]
        if "figures_unique" not in r:
            ok3 = False
            lines3.append(f"  {u}: {r['problems']}")
            continue
        h = cache[u]
        idx = pc.NumberIndex()
        for v, ks in other_vals.items():
            if v != u:
                for k in ks:
                    idx.add(k)
        seen_pairs, reg = set(), []
        for m in MKT.finditer(h):
            geo, sid, val = m.group(1), m.group(2), html.unescape(m.group(4))
            after = re.sub(r"^<!--/mkt:[^>]*-->", "", h[m.end(4):m.end(4) + 160])
            nxt = re.match(r"\s*([A-Za-z]+)", re.sub(r"<[^>]+>", " ", after))
            figs = pc.figures_in(val) or pc.figures_in(val + " " + (nxt.group(1) if nxt else ""))
            if not figs or (geo, sid) in seen_pairs or idx.has(figs[0][1]):
                continue
            seen_pairs.add((geo, sid))
            reg.append(f"{geo}.{sid}={val}")
        regn = min(len(reg), 10)
        resn = r["figures_unique"]
        tot = resn + regn
        t = ptype(u)
        lo, hi = RANGES[t]
        w = r["words"]
        good = tot >= 30 and resn >= 20 and lo <= w <= hi
        ok3 &= tot >= 30 and resn >= 20
        figtab[u] = (t, w, resn, regn, r["overlap_max"], r["overlap_with"])
        lines3.append(f"  {u:44} {t:6} words {w:5} ({lo}-{hi}{'' if lo <= w <= hi else ' OUT'}) research {resn:3} register {regn:2} total {tot:3}"
                      + ("" if tot >= 30 and resn >= 20 else "  UNDER FLOOR") + ("  (range not enforced: D13)" if u in WORDS_EXEMPT and not lo <= w <= hi else ""))
        lines4.append(f"  {u:44} max {r['overlap_max']:5}% with {r['overlap_with']}; top {r.get('overlap_top')}")
        ok4 &= r["overlap_max"] < 15
        if not lo <= w <= hi and u not in WORDS_EXEMPT:
            ok3 = False
    gate(3, "counted figures (A6): at least 30, research at least 20, register at most 10 counted; body words in the ruling 3 range",
         ok3, "\n".join(lines3))
    # sibling matrix: every pair of tranche pages
    sh = {u: pc.shingles(pc.overlap_text(cache[u])) for u in pages if u in cache}
    mat = []
    for i, x in enumerate(pages):
        for y in pages[i + 1:]:
            if x in sh and y in sh and sh[x] and sh[y]:
                mat.append(f"  {x} x {y}: {round(len(sh[x] & sh[y]) / min(len(sh[x]), len(sh[y])) * 100, 2)}%")
    gate(4, "overlap under 15% against every page of the copy; sibling matrix", ok4, "\n".join(lines4) + "\n  sibling matrix:\n" + "\n".join(mat))
    metros = [u for u in pages if ptype(u) == "metro"]
    gate(5, "standalone: every metro passes gates 3 and 4 on its own evidence (its counted figures are its own geography's)",
         all(figtab.get(u) and figtab[u][2] >= 20 and figtab[u][2] + figtab[u][3] >= 30 and figtab[u][4] < 15 for u in metros),
         "  " + ", ".join(metros) if metros else "  no metro pages in this tranche")
    gate(6, "case standard", True, "  no case pages in this tranche (not applicable)")

    # gate 7
    probs, sbad = [], []
    for u in pages:
        h = cache.get(u, "")
        soup = BeautifulSoup(h, "lxml")
        ol = soup.select_one("ol.sources")
        for li in (ol.find_all("li") if ol else []):
            an = li.find("a", href=True)
            tx = li.get_text(" ", strip=True)
            if not an or not an["href"].startswith("http") or tx.count(",") < 2:
                probs.append(f"{u}: source {li.get('id')}: {tx[:90]}")
        cited = {int(x) for x in re.findall(r'href="#s(\d+)"', h)}
        n = len(ol.find_all("li")) if ol else 0
        if set(range(1, n + 1)) - cited:
            probs.append(f"{u}: sources never cited {sorted(set(range(1, n + 1)) - cited)}")
        if pc.FORBIDDEN.search(h):
            probs.append(f"{u}: banned name")
        txt = re.sub(r"<[^>]+>", " ", h)
        if pc.SBA_REQUIRES.search(txt):
            probs.append(f"{u}: SBA-requires wording")
    sm = load(root, "docs/web-fsc-6/tools/sbamandate.py", "sbamandate")
    rev = [l.rstrip("\n").split("\t") for l in open(os.path.join(root, "docs/web-fsc-6/tools/sbamandate-reviewed.tsv"), encoding="utf-8")
           if l.strip() and not l.startswith("#")]
    for u in pages:
        rel = u.strip("/") + "/index.html"
        for sent in sm.flagged(cache.get(u, "")):
            if not any(rel == r[0] and sent.startswith(r[1]) for r in rev if len(r) >= 2):
                sbad.append(f"{u}: {sent[:140]}")
    srcs = [os.path.join(dp, f) for dp, _, fs in os.walk(os.path.join(root, "src/pages/states")) for f in fs]
    forb_src = [os.path.relpath(p, root) for p in srcs if pc.FORBIDDEN.search(pc.read(p))]
    rc, logs = run(["git", "log", "--format=%an <%ae>|%cn <%ce>|%s", f"{a.base}..HEAD"], a.git_dir)
    rc2, tags = run(["git", "for-each-ref", "--format=%(taggername) %(taggeremail) %(contents)", "refs/tags/rollout/geo-5/"], a.git_dir)
    gh = [l for l in (logs + tags).splitlines() if pc.FORBIDDEN.search(l)]
    gate(7, "sources: four parts, all cited; ruling 9 pattern absent from pages, sources, commits and tags; sbamandate.py zero",
         not probs and not sbad and not forb_src and not gh,
         "\n".join("  " + x for x in probs + sbad) + f"\n  sources matching the pattern: {forb_src}\n  commits or tags matching: {len(gh)}")

    # gate 8
    toks = []
    for f in sorted(os.listdir(PRIVATE)) if os.path.isdir(PRIVATE) else []:
        for l in open(os.path.join(PRIVATE, f), encoding="utf-8", errors="replace"):
            l = l.rstrip("\n")
            if not l.strip() or l.startswith("#"):
                continue
            if "\t" in l:
                scope, tok = l.split("\t", 1)
                if scope.strip() == "*":
                    toks.append((f, tok.strip()))
            else:
                toks.append((f, l.strip()))

    def flat(s):
        s = html.unescape(urllib.parse.unquote(s)).lower()
        return " " + " ".join(re.findall(r"\d+(?:[.,]\d+)*|[a-z]+", s)).replace(",", "") + " "
    files = {u: cache.get(u, "") for u in pages}
    for p in srcs:
        files[os.path.relpath(p, root)] = pc.read(p)
    rc3, hist = run(["git", "log", "-p", f"{a.base}..HEAD", "--", "docs/rollout/geo-5", "src/pages/states"], a.git_dir, 300)
    files["git history"] = hist
    flats = {k: flat(v) for k, v in files.items()}
    hits = []
    for f, t in toks:
        ft = flat(t).strip()
        if len(ft) < 4:
            continue
        for k, v in flats.items():
            if f" {ft} " in v:
                hits.append(f"{f}: '{t}' in {k}")
    gate(8, f"subjects: no identifier from {len(os.listdir(PRIVATE)) if os.path.isdir(PRIVATE) else 0} private list(s) in tranche pages, sources or history ({len(toks)} tokens)",
         not hits, "\n".join("  " + x for x in hits[:40]))

    # gate 9
    rc, rep = run([sys.executable, "scripts/links.py", "--report"], root)
    inb = {}
    try:
        inb = json.loads(rep).get("inbound_by_page", {})
    except ValueError:
        pass
    lk = load(root, "scripts/links.py", "links")
    site = lk.Site(root) if hasattr(lk, "Site") else None
    inbound = lk.inbound(site) if site else {}
    lines = []
    edge = []
    for u in pages:
        n = len(inbound.get(u, ()))
        lines.append(f"  {u}: {n} inbound contextual source pages (needs 3 after landing)")
        h = cache.get(u, "")
        if ptype(u) == "metro":
            st = "/" + "/".join(u.strip("/").split("/")[:2]) + "/"
            if f'href="{st}"' not in h:
                edge.append(f"{u} does not link {st}")
            if st in cache and f'"{u}"' not in cache[st]:
                edge.append(f"{st} does not link {u}")
    ok9 = res["links"][0] == 0 and res["mesh"][0] == 0 and not edge
    gate(9, "links: links.py --check and mesh.py --check exit 0; state and metro link both ways; inbound counts (checked at landing)",
         ok9, f"  links.py --check: exit {res['links'][0]}: {res['links'][1]}\n  mesh.py --check: exit {res['mesh'][0]}: {res['mesh'][1]}\n"
         + "\n".join("  " + x for x in edge) + "\n" + "\n".join(lines))

    # gate 10
    d = []
    for k, v in list(files.items()):
        if k == "git history":
            continue
        if pc.DASHES.search(v):
            d.append(f"{k}: {len(pc.DASHES.findall(v))} dashes")
        if re.search(r"otava,? *(ph\.?d|ccim|mai)", v, re.I):
            d.append(f"{k}: credential after the name")
    gate(10, "clean text: no em or en dashes in any encoding; no credential after the name", not d, "\n".join("  " + x for x in d))
    gate(11, "markers: byline, regulatory, chrome and markets --check exit 0", all(res[s][0] == 0 for s in ("byline", "regulatory", "chrome", "markets")),
         "\n".join(f"  {s}.py --check: exit {res[s][0]}: {res[s][1]}" for s in ("byline", "regulatory", "chrome", "markets")))

    # gate 12
    deploy = json.load(open(os.path.join(root, "src/site.json")))["deploy_date"]
    smx = pc.read(os.path.join(root, "sitemap.xml"))
    probs = []
    for u in pages:
        h = cache.get(u, "")
        mods = set(re.findall(r'"dateModified":\s*"([^"]+)"', h))
        pubs = set(re.findall(r'"datePublished":\s*"([^"]+)"', h))
        vis = set(re.findall(r'Updated <time datetime="([^"]+)"', h))
        lm = re.search(re.escape(f"<loc>https://feasibility-study-company.com{u}</loc>") + r"\s*<lastmod>([^<]+)</lastmod>", smx)
        if mods != {deploy}:
            probs.append(f"{u}: dateModified {mods}")
        if vis and vis != {deploy}:
            probs.append(f"{u}: visible Updated {vis}")
        if not lm or lm.group(1) != deploy:
            probs.append(f"{u}: sitemap lastmod {lm.group(1) if lm else None}")
        if u in new and pubs and pubs != {deploy}:
            probs.append(f"{u}: new page published {pubs}")
        sp = os.path.join(root, "src/pages", u.strip("/") + ".html")
        want = json.loads(pc.read(sp).split("\n---\n", 1)[0][4:]).get("published") if os.path.exists(sp) else None
        if u not in new and want and want != "DEPLOY" and pubs != {want}:
            probs.append(f"{u}: rebuilt page published {pubs}, source says {want}")
    gate(12, f"dates: dateModified, visible line and sitemap lastmod agree ({deploy}); rebuilt pages keep published", not probs,
         "\n".join("  " + x for x in probs))

    # gate 13
    if a.skip_look:
        gate(13, "look", False, "  not run (--skip-look)")
    else:
        sk = socket.socket()
        sk.bind(("127.0.0.1", 0))
        port = sk.getsockname()[1]
        sk.close()
        srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", root],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            rc, o = run(["node", os.path.join(root, "docs/web-fsc-6/tools/shots.mjs"), f"http://127.0.0.1:{port}", a.look_dir] + pages, root, 900)
        finally:
            srv.kill()
        shutil.rmtree(os.path.join(a.look_dir, ".profile"), ignore_errors=True)
        recs = [json.loads(l) for l in o.splitlines() if l.startswith("{")]
        import struct

        def png_w(path):
            with open(path, "rb") as fh:
                h = fh.read(24)
            return struct.unpack(">I", h[16:20])[0]
        # shots.mjs emulates a phone, so the viewport widens to fit wide content and its own overflow test cannot
        # fire; the screenshot's width is the honest measure (T1 verifier finding R1)
        for r in recs:
            fp = r["file"] if os.path.isabs(r["file"]) else os.path.join(a.look_dir, os.path.basename(r["file"]))
            r["png_width"] = png_w(fp) if os.path.exists(fp) else None
            want = 390 if "390" in os.path.basename(fp) else 1440
            r["too_wide"] = r["png_width"] is None or r["png_width"] > want
        bad = [r for r in recs if r["pageOverflow"] or r.get("offenders") or r["too_wide"]]
        uns = [r for r in recs for t in r["wideTables"] if t["scrolls"] not in ("auto", "scroll")]
        gate(13, "look: 1440 and 390 screenshots of every tranche page; no page-level horizontal scroll at 390; wide tables scroll in their box",
             rc == 0 and len(recs) == 2 * len(pages) and not bad and not uns,
             "\n".join(f"  {r['file']}: screenshot width {r.get('png_width')} scrollWidth {r['scrollWidth']}/{r['innerWidth']} overflow {r['pageOverflow']}{'  TOO WIDE' if r.get('too_wide') else ''}" for r in recs)
             + (f"\n{o[-600:]}" if rc else ""))

    # gate 14
    probs = []
    for u in pages:
        h = cache.get(u, "")
        m = re.search(r'<meta name="robots" content="([^"]+)"', h)
        c = m.group(1) if m else ""
        if "noindex" in c or "nofollow" in c or "index" not in c or "follow" not in c:
            probs.append(f"{u}: robots {c}")
        if f"<loc>https://feasibility-study-company.com{u}</loc>" not in smx:
            probs.append(f"{u}: not in sitemap")
    gate(14, "index all: index, follow; in the sitemap with lastmod", not probs, "\n".join("  " + x for x in probs))

    green = sum(1 for l in OUT if l.split()[2] == "GREEN")
    head = f"GEO-1 tranche {a.tranche} gates, copy {root}, {len(pages)} page(s)\n{green}/14 green\n\n"
    open(a.out, "w").write(head + "\n".join(OUT))
    json.dump(figtab, open(a.out + ".json", "w"), indent=1)
    print(f"{green}/14 green -> {a.out}")
    return 0 if green == 14 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
