#!/usr/bin/env python3
"""The integrator's landing steps (FACTORY-2, ROLLOUT-1 ruling 14). Run from the integrator's worktree.

    python3 scripts/land.py pin --date YYYY-MM-DD --since REF
        set src/site.json deploy_date, and pin every "DEPLOY" date in the page sources this landing changed
        (REF..HEAD plus the working tree) to that date, so a later deploy never re-dates an earlier page (ruling 12,
        amendment A10). A "DEPLOY" left in a source this landing did not change stops the run.
    python3 scripts/land.py tree --ref main --out DIR
        the deploy tree: git archive REF | tar -x -C DIR --exclude=docs --exclude=src --exclude=data/markets
    python3 scripts/land.py prodcheck --base URL --urls FILE [--relinked FILE] [--tree DIR]
        production checks: 200 and the expected H1 on every landed page, formerly pending links now resolving,
        /src/, /docs/, /Docs/ and /data/markets/ answering 404, and the served sitemap's lastmod matching the tree
    python3 scripts/land.py bundle
        an incremental bundle origin/main..main at <repo>/_bundles/rollout-<sha>.bundle, verified; the newest five
        rollout bundles are kept
    python3 scripts/land.py landed --name <lane>-t<n> --deploy ID --urls N [--tag TAG]
        write ~/Downloads/fsc-rollout/bus/landed/<name> with main's sha, the deploy id and the URL count
"""
import argparse
import datetime
import glob
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUS = os.path.expanduser("~/Downloads/fsc-rollout/bus")
UA = "Mozilla/5.0 (compatible; FSC-integrator-prodcheck/1.0)"


def sh(*cmd, timeout=600, cwd=ROOT, check=True):
    p = subprocess.run(list(cmd), cwd=cwd, capture_output=True, text=True, timeout=timeout)
    if check and p.returncode != 0:
        raise SystemExit(f"{' '.join(cmd)} failed: {p.stderr.strip()[:400]}")
    return p.stdout


def repo_dir():
    common = sh("git", "rev-parse", "--git-common-dir").strip()
    return os.path.dirname(os.path.abspath(os.path.join(ROOT, common)))


# ------------------------------------------------------------------ pin

FRONT_DATE = re.compile(r'("(?:published|updated)"\s*:\s*)"DEPLOY"')


def cmd_pin(a):
    datetime.date.fromisoformat(a.date)
    site = os.path.join(ROOT, "src", "site.json")
    cfg = json.load(open(site, encoding="utf-8"))
    if cfg.get("deploy_date") != a.date:
        text = open(site, encoding="utf-8").read()
        text = re.sub(r'("deploy_date"\s*:\s*)"[^"]*"', r'\1"%s"' % a.date, text, count=1)
        open(site, "w", encoding="utf-8").write(text)
    changed = set(sh("git", "diff", "--name-only", a.since).split())
    changed |= set(sh("git", "ls-files", "--others", "--exclude-standard", "src/pages").split())
    pinned, stray = [], []
    for d, _dirs, files in os.walk(os.path.join(ROOT, "src", "pages")):
        for f in files:
            if not f.endswith(".html"):
                continue
            p = os.path.join(d, f)
            rel = os.path.relpath(p, ROOT)
            s = open(p, encoding="utf-8").read()
            end = s.find("\n---\n", 4)
            fm = s[:end]
            if '"DEPLOY"' not in fm:
                continue
            if rel not in changed:
                stray.append(rel)
                continue
            open(p, "w", encoding="utf-8").write(FRONT_DATE.sub(r'\1"%s"' % a.date, fm) + s[end:])
            pinned.append(rel)
    for r in pinned:
        print("pinned", r)
    print(f"deploy_date {a.date}; {len(pinned)} source(s) pinned")
    if stray:
        print("ERROR: \"DEPLOY\" in sources this landing did not change:\n  " + "\n  ".join(stray))
        return 1
    return 0


# ------------------------------------------------------------------ tree

def cmd_tree(a):
    out = os.path.abspath(a.out)
    os.makedirs(out, exist_ok=True)
    if os.listdir(out):
        raise SystemExit(f"{out} is not empty")
    arch = subprocess.Popen(["git", "archive", a.ref], cwd=ROOT, stdout=subprocess.PIPE)
    tar = subprocess.run(["tar", "-x", "-C", out, "--exclude=docs", "--exclude=src", "--exclude=data/markets"],
                         stdin=arch.stdout, timeout=600)
    arch.stdout.close()
    if arch.wait(timeout=600) != 0 or tar.returncode != 0:
        raise SystemExit("git archive | tar failed")
    for must in ("index.html", "netlify.toml", "sitemap.xml", "netlify/functions"):
        if not os.path.exists(os.path.join(out, must)):
            raise SystemExit(f"deploy tree lacks {must}")
    for never in ("docs", "src", "data/markets", ".ghtoken", "_bundles"):
        if os.path.exists(os.path.join(out, never)):
            raise SystemExit(f"deploy tree carries {never}")
    n = sum(1 for _ in glob.iglob(os.path.join(out, "**", "index.html"), recursive=True))
    print(f"deploy tree {out} from {a.ref}: {n} index.html file(s)")
    return 0


# ------------------------------------------------------------------ prodcheck

def get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Cache-Control": "no-cache"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", "replace"), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace"), url


def h1_of(s):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", m.group(1)))).strip() if m else None


def cmd_prodcheck(a):
    base = a.base.rstrip("/")
    tree = a.tree or ROOT
    urls = [l.strip() for l in open(a.urls, encoding="utf-8") if l.strip() and not l.startswith("#")]
    bad, ok = [], 0
    for u in urls:
        local = os.path.join(tree, u.strip("/"), "index.html") if u != "/" else os.path.join(tree, "index.html")
        want = h1_of(open(local, encoding="utf-8").read()) if os.path.exists(local) else None
        for attempt in range(3):
            st, body, final = get(base + u)
            if st == 200 and h1_of(body) == want:
                break
            time.sleep(3)
        if st != 200 or h1_of(body) != want:
            bad.append(f"{u}: status {st}, H1 {h1_of(body)!r} (want {want!r})")
        else:
            ok += 1
    rel_ok = 0
    if a.relinked:
        for u in [l.strip() for l in open(a.relinked, encoding="utf-8") if l.strip()][:5]:
            st, _, _ = get(base + u)
            if st == 200:
                rel_ok += 1
            else:
                bad.append(f"formerly pending {u}: status {st}")
    for p in ("/src/", "/docs/", "/Docs/", "/data/markets/", "/src/README.md", "/docs/rollout/ROLLOUT-1.md"):
        st, _, _ = get(base + p)
        if st != 404:
            bad.append(f"{p}: status {st}, want 404")
    st, sm, _ = get(base + "/sitemap.xml")
    local_sm = open(os.path.join(tree, "sitemap.xml"), encoding="utf-8").read()
    if st != 200 or sm.strip() != local_sm.strip():
        served = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", sm))
        local = dict(re.findall(r"<loc>([^<]+)</loc>\s*<lastmod>([^<]+)</lastmod>", local_sm))
        diff = [k for k in set(served) | set(local) if served.get(k) != local.get(k)]
        bad.append(f"sitemap: status {st}; {len(diff)} loc/lastmod difference(s) from the tree: {sorted(diff)[:5]}")
    print(f"pages 200 with expected H1: {ok}/{len(urls)}; formerly pending now 200: {rel_ok}; "
          f"sitemap URLs {local_sm.count('<url>')}; problems {len(bad)}")
    for b in bad:
        print("  PROBLEM", b)
    return 1 if bad else 0


# ------------------------------------------------------------------ bundle

def cmd_bundle(a):
    repo = repo_dir()
    sha = sh("git", "rev-parse", "--short", "main").strip()
    base = sh("git", "rev-parse", "origin/main").strip()
    if subprocess.run(["git", "merge-base", "--is-ancestor", base, "main"], cwd=ROOT, timeout=60).returncode != 0:
        raise SystemExit("origin/main is not an ancestor of main: merge the coordinator's commits first")
    count = sh("git", "rev-list", "--count", "origin/main..main").strip()
    if count == "0":
        print("main equals origin/main: no bundle")
        return 0
    d = os.path.join(repo, "_bundles")
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, f"rollout-{sha}.bundle")
    sh("git", "bundle", "create", path, "origin/main..main")
    v = subprocess.run(["git", "bundle", "verify", path], cwd=repo, capture_output=True, text=True, timeout=300)
    if v.returncode != 0:
        raise SystemExit(f"bundle does not verify: {v.stderr.strip()[:300]}")
    mine = sorted(glob.glob(os.path.join(d, "rollout-*.bundle")), key=os.path.getmtime)
    for old in mine[:-5]:
        os.remove(old)
    print(f"bundle {os.path.relpath(path, repo)}: {count} commit(s) origin/main..main, verified; kept {min(len(mine), 5)}")
    return 0


# ------------------------------------------------------------------ landed

def cmd_landed(a):
    sha = sh("git", "rev-parse", "main").strip()
    os.makedirs(os.path.join(BUS, "landed"), exist_ok=True)
    text = (f"landed {datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')}\n"
            f"main {sha}\ndeploy {a.deploy}\nurls {a.urls}\n" + (f"tag {a.tag}\n" if a.tag else ""))
    open(os.path.join(BUS, "landed", a.name), "w", encoding="utf-8").write(text)
    print(text, end="")
    return 0


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pin")
    p.add_argument("--date", required=True)
    p.add_argument("--since", required=True)
    p = sub.add_parser("tree")
    p.add_argument("--ref", default="main")
    p.add_argument("--out", required=True)
    p = sub.add_parser("prodcheck")
    p.add_argument("--base", default="https://feasibility-study-company.com")
    p.add_argument("--urls", required=True)
    p.add_argument("--relinked")
    p.add_argument("--tree")
    sub.add_parser("bundle")
    p = sub.add_parser("landed")
    p.add_argument("--name", required=True)
    p.add_argument("--deploy", required=True)
    p.add_argument("--urls", required=True)
    p.add_argument("--tag")
    a = ap.parse_args(argv)
    return {"pin": cmd_pin, "tree": cmd_tree, "prodcheck": cmd_prodcheck, "bundle": cmd_bundle, "landed": cmd_landed}[a.cmd](a)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
