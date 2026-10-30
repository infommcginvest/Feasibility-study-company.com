#!/usr/bin/env python3
"""ASSET-3 draft self-check: render draft page sources in a small sandbox and measure them the way the
gates will (pagecheck.py's definitions), without a full copy of the tree.

    python3 docs/rollout/asset-3/tools/selfcheck.py <draft.html> [more drafts] [--figures] [--keep]

For each draft: build errors, body words against its type's range, counted research figures (cited,
parseable, not on any served page outside this lane's own rebuilt hubs, not on another draft in
~/Downloads/fsc-rollout/drafts/asset-3/pages/), distinct register pairs (mkt markers), and the highest
8-word shingle overlap against every served page and every other draft.

The sandbox holds copies of scripts/ and src/templates/ and a read-only symlink to data/; only the
draft's own served file is written, inside the sandbox, which is deleted afterwards (unless --keep).
"""
import argparse
import glob
import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.realpath(__file__))
WT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(HERE))))
DRAFTS = os.path.expanduser("~/Downloads/fsc-rollout/drafts/asset-3/pages")
SANDBOX_PARENT = os.path.expanduser("~/Downloads/fsc-rollout/tmp/asset-3/sc")
HUBS = ["assisted-living-and-memory-care", "medical-office-and-asc", "childcare-and-daycare", "behavioral-health",
        "urgent-care", "veterinary-practice", "pet-boarding-and-daycare", "funeral-home", "private-school",
        "skilled-nursing", "independent-living-and-ccrc"]
OWN_PREFIXES = [f"/asset-classes/{h}/" for h in HUBS]
RANGES = {"hub": (6000, 10000), "subtype": (1800, 3000)}
TARGET = {"hub": 40, "subtype": 30}
MKT = re.compile(r"<!--mkt:([a-z0-9/:-]+)\.([a-z0-9_]+)(?:\.[a-z0-9-]+)?( \{.*?\})?-->")


def load_pagecheck():
    spec = importlib.util.spec_from_file_location("pagecheck", os.path.join(WT, "docs", "web-fsc-6", "tools", "pagecheck.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.ROOT = WT
    return mod


def front_of(path):
    text = open(path, encoding="utf-8").read()
    parts = text.split("\n---\n", 1)
    head = parts[0]
    if head.startswith("---\n"):
        head = head[4:]
    return json.loads(head)


def render(draft, keep):
    os.makedirs(SANDBOX_PARENT, exist_ok=True)
    sb = tempfile.mkdtemp(prefix="sc-", dir=SANDBOX_PARENT)
    shutil.copytree(os.path.join(WT, "scripts"), os.path.join(sb, "scripts"))
    # everything under src/ except the page sources (templates, types.json, site.json, case cards, ...)
    shutil.copytree(os.path.join(WT, "src"), os.path.join(sb, "src"), ignore=lambda d, names: ["pages"] if d == os.path.join(WT, "src") else [])
    os.symlink(os.path.join(WT, "data"), os.path.join(sb, "data"))
    front = front_of(draft)
    url = front["url"]
    rel = url.strip("/")
    dst = os.path.join(sb, "src", "pages", rel + ".html")
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy(draft, dst)
    served_old = os.path.join(WT, rel, "index.html")
    out_path = os.path.join(sb, rel, "index.html")
    if os.path.exists(served_old):  # a rebuild keeps the served page's chrome and mesh regions
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        shutil.copy(served_old, out_path)
    log = []
    ok = True
    for cmd in (["scripts/build.py", "--page", url], ["scripts/regulatory.py"],
                ["scripts/markets.py", "--pages", os.path.join(rel, "index.html")]):
        try:
            r = subprocess.run([sys.executable] + cmd, cwd=sb, capture_output=True, text=True, timeout=300)
        except subprocess.TimeoutExpired:
            log.append(f"{cmd[0]}: timeout")
            ok = False
            break
        if r.returncode != 0:
            log.append(f"{cmd[0]} exit {r.returncode}: {(r.stdout + r.stderr).strip()[-1500:]}")
            ok = False
            break
    html_text = open(out_path, encoding="utf-8").read() if ok and os.path.exists(out_path) else None
    if not keep:
        shutil.rmtree(sb, ignore_errors=True)
    else:
        log.append(f"sandbox kept at {sb}")
    return front, html_text, log


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("drafts", nargs="+")
    ap.add_argument("--figures", action="store_true")
    ap.add_argument("--keep", action="store_true")
    a = ap.parse_args(argv)
    pc = load_pagecheck()

    site = {u: p for u, p in pc.served_pages().items() if not any(u.startswith(x) for x in OWN_PREFIXES)}
    idx = pc.NumberIndex()
    site_sh = {}
    for u, p in site.items():
        t = pc.read(p)
        main = pc.main_soup(pc.strip_regions(t, ["sba", "case", "mkt", "mesh"]))
        for raw, key in pc.figures_in(main.get_text(" ")):
            if not pc.YEAR.match(pc.norm(raw)):
                idx.add(key)
        site_sh[u] = pc.shingles(pc.overlap_text(pc.strip_regions(t, ["mesh"])))

    targets = [os.path.abspath(d) for d in a.drafts]
    others = [os.path.abspath(p) for p in glob.glob(os.path.join(DRAFTS, "**", "*.html"), recursive=True)]
    rendered = {}
    for d in sorted(set(targets) | set(others)):
        front, html_text, log = render(d, a.keep and d in targets)
        rendered[d] = (front, html_text, log)

    fail = 0
    for d in targets:
        front, html_text, log = rendered[d]
        kind = front.get("type")
        print(f"== {front.get('url')}  ({os.path.basename(d)}, type {kind})")
        if html_text is None:
            print("  BUILD FAILED"); [print("  " + x) for x in log]; fail = 1
            continue
        for x in log:
            print("  " + x)
        if "<!--mkt" in open(d, encoding="utf-8").read().split("\n---\n", 1)[0]:
            print("  FRONT MATTER HOLDS A mkt: MARKER (markets.py cannot parse it there): move it to the body"); fail = 1
        words = pc.body_words(html_text)
        lo, hi = RANGES.get(kind, (0, 10 ** 9))
        cl = pc.NumberIndex()
        cl_sh = {}
        for o, (of, oh, _) in rendered.items():
            if o == d or oh is None:
                continue
            m = pc.main_soup(pc.strip_regions(oh, ["sba", "case", "mkt", "mesh"]))
            for raw, key in pc.figures_in(m.get_text(" ")):
                if not pc.YEAR.match(pc.norm(raw)):
                    cl.add(key)
            cl_sh[of.get("url")] = pc.shingles(pc.overlap_text(pc.strip_regions(oh, ["mesh"])))
        figs = pc.sourced_figures(html_text)
        counted, lost_site, lost_cluster = [], [], []
        for n, (raw, key) in figs.items():
            if idx.has(key):
                lost_site.append(raw)
            elif cl.has(key):
                lost_cluster.append(raw)
            else:
                counted.append(raw)
        pairs = sorted({(g, s) for g, s, _ in MKT.findall(html_text)})
        mine = pc.shingles(pc.overlap_text(pc.strip_regions(html_text, ["mesh"])))
        worst = (0.0, "")
        for u, sh in list(site_sh.items()) + list(cl_sh.items()):
            if not sh or not mine:
                continue
            ov = len(mine & sh) / min(len(mine), len(sh))
            if ov > worst[0]:
                worst = (ov, u)
        need = TARGET.get(kind, 30)
        wflag = "OK" if lo <= words <= hi else "OUT OF RANGE"
        fflag = "OK" if len(counted) >= need else f"SHORT (target {need})"
        oflag = "OK" if worst[0] < 0.10 else ("HIGH" if worst[0] < 0.15 else "FAIL")
        print(f"  body words {words} [{lo} to {hi}] {wflag}")
        print(f"  counted research figures {len(counted)} {fflag}; lost to other served pages {len(lost_site)}; "
              f"lost to sibling drafts {len(lost_cluster)}")
        print(f"  register pairs (geo, series) {len(pairs)}: {', '.join(g + '.' + s for g, s in pairs)}")
        print(f"  highest overlap {worst[0] * 100:.2f}% against {worst[1]} {oflag}")
        if a.figures:
            print("  counted: " + " | ".join(counted))
            print("  lost to site: " + " | ".join(lost_site))
            print("  lost to siblings: " + " | ".join(lost_cluster))
        if wflag != "OK" or fflag != "OK" or oflag == "FAIL":
            fail = 1
    return fail


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
