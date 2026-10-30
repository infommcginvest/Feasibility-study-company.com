#!/usr/bin/env python3
"""GEO-3 gates 1 to 14 on a tranche of state and metro pages, in a throwaway copy where the chain has run.

    python3 docs/rollout/geo-3/tools/geo3gates.py --root <copy> --git-dir <worktree> --pages <url,...>
        [--folded <url>=<parent>#<anchor>,...] [--published <url>=<date>,...] [--out GATES-t<n>.txt] [--skip-look]

Adapted from docs/web-fsc-6/tools/gates.py (same checks and wording), with the page set as an argument,
the content gates from lanecheck.py (rollout floors), gate 8 over every list in ~/Downloads/fsc-rollout/private/
(amendment A1 forms), git checks run in --git-dir, and the look gate on a free port (amendment A9).
Gate 6 (case standard) is not applicable: GEO-3 writes no case. Gates that can only be met after landing
(3+ inbound links, sitemap lastmod at the deploy date) report their state and say so.
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
import socket
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PRIVATE = os.path.expanduser("~/Downloads/fsc-rollout/private")
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
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def read(p):
    return open(p, encoding="utf-8", errors="replace").read()


def load(root, rel, name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(root, rel))
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(os.path.join(root, rel)))
    spec.loader.exec_module(m)
    return m


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--git-dir", required=True)
    ap.add_argument("--pages", required=True)
    ap.add_argument("--folded", default="")
    ap.add_argument("--published", default="")
    ap.add_argument("--base", default="main")
    ap.add_argument("--out")
    ap.add_argument("--skip-look", action="store_true")
    ap.add_argument("--look-dir")
    a = ap.parse_args(argv)
    root, gd = os.path.abspath(a.root), os.path.abspath(a.git_dir)
    urls = ["/" + u.strip("/") + "/" for u in a.pages.split(",") if u]
    folded = [x.split("=") for x in a.folded.split(",") if x]
    published = dict(x.split("=") for x in a.published.split(",") if x)
    pc = load(root, "docs/web-fsc-6/tools/pagecheck.py", "pc_g3")
    pc.ROOT = root
    sbam = load(root, "docs/web-fsc-6/tools/sbamandate.py", "sbam_g3")
    served = lambda u: os.path.join(root, u.strip("/"), "index.html")
    src = lambda u: os.path.join(root, "src", "pages", u.strip("/") + ".html")
    deploy = json.load(open(os.path.join(root, "src", "site.json")))["deploy_date"]
    out(f"GEO-3 gates on {root}\npages: {', '.join(urls)}\nfolded: {folded}\ndeploy_date in the copy: {deploy}")

    # 1 pages
    probs = []
    for u in urls:
        if not os.path.exists(served(u)) or not os.path.exists(src(u)):
            probs.append(f"{u}: not built from a source")
            continue
        h = read(served(u))
        t = len(re.findall(r"<title>", re.sub(r"<!--.*?-->", "", h, flags=re.S)))
        if t != 1:
            probs.append(f"{u}: {t} <title>")
        types, ids = set(), set()
        for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
            try:
                d = json.loads(b)
            except ValueError as e:
                probs.append(f"{u}: JSON-LD does not parse: {e}")
                continue
            for nd in d.get("@graph", [d]):
                tt = nd.get("@type")
                types |= set(tt if isinstance(tt, list) else [tt])
                au = nd.get("author")
                if isinstance(au, dict) and au.get("@id"):
                    ids.add(au["@id"])
        if "BreadcrumbList" not in types:
            probs.append(f"{u}: no BreadcrumbList")
        if "https://feasibility-study-company.com/#mark-otava" not in ids:
            probs.append(f"{u}: no author @id")
    for f, parent in folded:
        par, anchor = parent.split("#")
        if os.path.exists(served(f)) or os.path.exists(src(f)):
            probs.append(f"folded {f} still has a page")
        if not os.path.exists(served(par)) or f'id="{anchor}"' not in read(served(par)):
            probs.append(f"folded {f}: no section #{anchor} in {par}")
    gate(1, "pages build from sources; one <title>; JSON-LD parses with BreadcrumbList and author @id; folds have their section",
         "GREEN" if not probs else "RED", f"  {len(urls)} pages, {len(folded)} folded sections\n" + "\n".join("  " + x for x in probs))

    # 2 factory
    rc, o = run([sys.executable, "scripts/build.py", "--check"], root)
    rc2, o2 = run([sys.executable, "scripts/casemodel.py", "--check"], root)
    gate(2, "factory: build.py --check and casemodel.py --check exit 0 (no case in this tranche; casemodel run as a guard)",
         "GREEN" if rc == 0 and rc2 == 0 else "RED", f"  build.py --check rc={rc}: {o.splitlines()[-1] if o else ''}\n  casemodel.py --check rc={rc2}: {o2.splitlines()[-1] if o2 else ''}")

    # 3 4 5 via lanecheck
    rc, o = run([sys.executable, os.path.join(HERE, "lanecheck.py"), "--root", root, "--overlap", "3", "--json",
                 os.path.join(root, ".geo3-lanecheck.json")] + urls, root)
    recs = json.load(open(os.path.join(root, ".geo3-lanecheck.json")))
    bad3 = [r for r in recs if any("figures" in p or p.startswith("body words") for p in r["problems"])]  # ruling 3 ranges too
    bad4 = [r for r in recs if any(p.startswith("overlap") for p in r["problems"])]
    other = [(r["url"], p) for r in recs for p in r["problems"] if "figures" not in p and not p.startswith("overlap") and not p.startswith("body words")]
    table = "\n".join(f"  {r['url']:44} {r['type']:6} words {r.get('words')}  research {r.get('research')}  register {r.get('register_counted')}  "
                      f"counted {r.get('counted')}  overlap max {r.get('overlap_max')}% ({r.get('overlap_with')})" for r in recs)
    gate(3, "counted figures: research at least 20, research plus register (at most 10) at least 30 (amendment A6); body words in the ruling 3 range", "GREEN" if not bad3 else "RED", table + "".join(f"\n  PROBLEM {r['url']}: {p}" for r in bad3 for p in r["problems"]))
    sib = "\n".join(f"  {r['url']:44} sibling max {r.get('overlap_sibling_max')}%; top: {r.get('overlap_top')}" for r in recs)
    gate(4, "overlap under 15% against every page of the copy; sibling matrix", "GREEN" if not bad4 else "RED", sib)
    metros = [r for r in recs if r["type"] == "metro"]
    badm = [r["url"] for r in metros if r in bad3 or r in bad4]
    gate(5, "standalone: every metro passes gates 3 and 4 on its own geography's evidence (folds listed in gate 1)",
         "GREEN" if not badm else "RED", f"  metros {len(metros)}, failing {badm}")
    gate(6, "case standard", "N/A", "  GEO-3 writes no case pages")

    # 7 sources
    probs = []
    for u in urls:
        t = read(src(u))
        fm = json.loads(re.match(r"---\n(.*?)\n---\n", t, re.S).group(1))
        for i, s in enumerate(fm.get("sources", []), 1):
            miss = [k for k in ("publisher", "title", "date", "url") if not str(s.get(k, "")).strip()]
            if miss or not str(s.get("url", "")).startswith("http"):
                probs.append(f"{u} source {i}: missing {miss or 'absolute url'}")
        h = read(served(u))
        for fh in (t, h):
            if pc.FORBIDDEN.search(fh):
                probs.append(f"{u}: forbidden pattern")
        fl = sbam.flagged(h)
        if fl:
            probs.append(f"{u}: sbamandate {fl[:2]}")
    rc, o = run(["git", "log", "--format=%an <%ae>%n%s%n%b", f"{a.base}..HEAD"], gd)
    if pc.FORBIDDEN.search(o):
        probs.append("forbidden pattern in a lane commit author or message")
    authors = set(run(["git", "log", "--format=%an <%ae> | %cn <%ce>", f"{a.base}..HEAD"], gd)[1].splitlines())
    rc, tags = run(["git", "for-each-ref", "refs/tags/rollout/geo-3", "--format=%(contents)"], gd)
    if pc.FORBIDDEN.search(tags):
        probs.append("forbidden pattern in a tag message")
    gate(7, "sources: four parts; ruling 9 pattern absent in sources, served pages, commit authors and messages, tag messages; sbamandate zero",
         "GREEN" if not probs else "RED", f"  lane commit identities: {sorted(authors)}\n" + "\n".join("  " + x for x in probs))

    # 8 subjects
    probs, n_tok = [], 0
    rc, hist = run(["git", "log", "-p", f"{a.base}..HEAD"], gd, timeout=300)
    for lf in sorted(glob.glob(os.path.join(PRIVATE, "*.txt"))):
        for line in read(lf).splitlines():
            if not line.strip():
                continue
            scope, tok = (line.split("\t", 1) if "\t" in line else ("*", line))
            tok = tok.strip()
            if not tok:
                continue
            n_tok += 1
            if scope != "*":
                continue   # a case-scoped line applies to that case's page only; this tranche holds no case
            low = tok.lower()
            for u in urls:
                for fp in (served(u), src(u)):
                    if low in read(fp).lower():
                        probs.append(f"{os.path.basename(lf)} token found in {fp.replace(root, '<copy>')}")
            if low in hist.lower():
                probs.append(f"{os.path.basename(lf)} token found in the lane's git history")
    gate(8, "subjects: no identifier from any list in private/ in the tranche's pages, sources or history",
         "GREEN" if not probs else "RED", f"  {len(glob.glob(os.path.join(PRIVATE, '*.txt')))} lists, {n_tok} tokens\n" + "\n".join("  " + x for x in probs))

    # 9 links
    notes, status = [], "GREEN"
    for script in ("links.py", "mesh.py"):
        rc, o = run([sys.executable, "scripts/" + script, "--check"], root)
        notes.append(f"  {script} --check rc={rc}: {o.splitlines()[-1] if o else ''}")
        status = "RED" if rc else status
    idx = {"/", "/case-studies/", "/asset-classes/", "/states/", "/practice-areas/", "/research-notes/"}
    inb = {u: set() for u in urls}
    for u, p in pc.served_pages().items():
        if u in idx:
            continue
        m = re.search(r"<main.*?</main>", read(p), re.S)
        if not m:
            continue
        body = re.sub(r'<nav class="breadcrumb".*?</nav>', " ", m.group(0), flags=re.S)
        for href in set(re.findall(r'href="(/[^"#?]*)', body)):
            if href in inb and href != u:
                inb[href].add(u)
    miss = []
    for u in urls:
        parts = u.strip("/").split("/")
        if len(parts) == 3:
            st = f"/states/{parts[1]}/"
            if st in urls and f'href="{u}"' not in read(served(st)):
                miss.append(f"{st} does not link {u}")
            body = re.sub(r'<nav class="breadcrumb".*?</nav>', "", read(served(u)), flags=re.S)
            if f'href="{st}"' not in body:
                miss.append(f"{u} does not link {st} in its body")
    status = "RED" if miss else status
    notes.append("  inbound contextual links from distinct non-index pages (3 required after landing):")
    notes += [f"    {u:44} {len(s)}" for u, s in sorted(inb.items())]
    gate(9, "links: links.py and mesh.py --check; required state and metro edges; inbound count (checked again at landing)",
         status, "\n".join(notes) + ("\n  missing edges:\n" + "\n".join("    " + x for x in miss) if miss else ""))

    # 10 clean text
    probs = []
    for u in urls:
        for fp in (served(u), src(u)):
            n = len(pc.DASHES.findall(read(fp)))
            if n:
                probs.append(f"{fp.replace(root, '<copy>')}: {n} dash(es)")
            if re.search(r"otava,? *(ph\.?d|ccim|mai)", read(fp), re.I):
                probs.append(f"{fp}: credential")
    gate(10, "clean text: zero em and en dashes in any encoding; no credential beside the name", "GREEN" if not probs else "RED",
         "\n".join("  " + x for x in probs) or "  0 dashes, credential grep 0")

    # 11 markers
    notes, status = [], "GREEN"
    for script in ("byline.py", "regulatory.py", "chrome.py", "markets.py"):
        rc, o = run([sys.executable, "scripts/" + script, "--check"], root)
        notes.append(f"  {script} --check rc={rc}: {o.splitlines()[-1] if o else ''}")
        status = "RED" if rc else status
    gate(11, "markers: byline, regulatory, chrome and markets --check", status, "\n".join(notes))

    # 12 dates
    probs = []
    sm = read(os.path.join(root, "sitemap.xml"))
    lastmod = dict(re.findall(r"<loc>https://feasibility-study-company.com(/[^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
    for u in urls:
        h = read(served(u))
        mods = set(re.findall(r'"dateModified":\s*"([^"]+)"', h))
        pubs = set(re.findall(r'"datePublished":\s*"([^"]+)"', h))
        vis = set(re.findall(r'(?:Updated|Published) <time datetime="([^"]+)"', h))
        want_pub = published.get(u, deploy)
        if mods != {deploy}:
            probs.append(f"{u}: dateModified {mods}")
        if pubs and pubs != {want_pub}:
            probs.append(f"{u}: datePublished {pubs}, expected {want_pub}")
        if deploy not in vis:
            probs.append(f"{u}: visible dates {vis}")
        if lastmod.get(u) != deploy:
            probs.append(f"{u}: sitemap lastmod {lastmod.get(u)}")
    gate(12, f"dates: JSON-LD dateModified, visible line and sitemap lastmod agree ({deploy} in the copy; the integrator pins DEPLOY at landing); rebuilt pages keep their published date",
         "GREEN" if not probs else "RED", "\n".join("  " + x for x in probs))

    # 13 look
    if a.skip_look:
        gate(13, "look", "PENDING", "  skipped in this run")
    else:
        s = socket.socket()
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
        s.close()
        outdir = a.look_dir or os.path.join(root, ".geo3-look")
        srv = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", root],
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            rc, o = run(["node", os.path.join(HERE, "shots.mjs"), f"http://127.0.0.1:{port}", outdir] + urls, root)
        finally:
            srv.kill()
        shutil.rmtree(os.path.join(outdir, ".profile"), ignore_errors=True)
        recs = [json.loads(l) for l in o.splitlines() if l.startswith("{")]
        bad = [r for r in recs if r["pageOverflow"] or r.get("offenders")]
        uns = [r for r in recs for t in r["wideTables"] if t["scrolls"] not in ("auto", "scroll")]
        ok = rc == 0 and len(recs) == 2 * len(urls) and not bad and not uns
        gate(13, "look: 1440 and 390 screenshots; no page-level horizontal scroll at 390; wide tables scroll in their box",
             "GREEN" if ok else "RED", "\n".join(f"  {r['file']:60} scrollWidth {r['scrollWidth']} / emulated {r.get('emulatedWidth')} (innerWidth {r['innerWidth']}) overflow {r['pageOverflow']} "
                                                 f"inner-scroll tables {len(r['wideTables'])}" + "".join(f"\n    offender {x}" for x in r.get("offenders", [])) for r in recs) + (f"\n{o[-800:]}" if rc else ""))

    # 14 index all
    probs = []
    for u in urls:
        h = read(served(u))
        m = re.search(r'<meta name="robots" content="([^"]+)"', h)
        c = m.group(1) if m else ""
        if "noindex" in c or "nofollow" in c or "index" not in c or "follow" not in c:
            probs.append(f"{u}: robots {c!r}")
        if f"<loc>https://feasibility-study-company.com{u}</loc>" not in sm:
            probs.append(f"{u}: not in sitemap")
    gate(14, "index all: index, follow and in the sitemap with lastmod", "GREEN" if not probs else "RED", "\n".join("  " + x for x in probs))

    green = sum(1 for _, _, s in results if s in ("GREEN", "N/A"))
    out(f"\nSUMMARY: {green}/14 green or not applicable; " + ", ".join(f"{n}:{s}" for n, _, s in results))
    if a.out:
        text = "\n".join(lines) + "\n"
        text = text.replace(os.path.expanduser("~"), "~")
        text = re.sub(r"m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er", "[ruling 9 name withheld]", text, flags=re.I)
        open(a.out, "w").write(text)
    return 0 if green == 14 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
