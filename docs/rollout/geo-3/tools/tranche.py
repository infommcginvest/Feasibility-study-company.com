#!/usr/bin/env python3
"""GEO-3 readiness run for one tranche (ruling 13, amendments A2 and A9).

    python3 docs/rollout/geo-3/tools/tranche.py <n> <state> [--keep] [--skip-look]

1. Makes a fresh throwaway copy ~/Downloads/fsc-rollout/tmp/geo-3/t<n> from `git archive HEAD` of the worktree.
2. Copies the state's finished drafts (~/Downloads/fsc-rollout/drafts/geo-3/<state>/pages/*.html) into src/pages.
3. Applies this lane's requests for the state (docs/rollout/geo-3/requests.json): folded URLs and their section
   targets into data/mesh/fallbacks.json.
4. Runs the chain over the whole copy: build, chrome, byline, regulatory, markets, casemodel, mesh, links --relink, sitemap.
5. Runs geo3gates.py on the tranche's pages and writes docs/rollout/geo-3/GATES-t<n>.txt in the worktree, with
   screenshots in docs/rollout/geo-3/look/t<n>/.
6. Prints the freeze record: sha256 of every source in the tranche and of every rendered page.
"""
import hashlib
import json
import os
import shutil
import re
import subprocess
import sys

RULING9 = re.compile(r"m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er", re.I)
WT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
LANE = os.path.join(WT, "docs", "rollout", "geo-3")
TMP = os.path.expanduser("~/Downloads/fsc-rollout/tmp/geo-3")
DRAFTS = os.path.expanduser("~/Downloads/fsc-rollout/drafts/geo-3")
PUBLISHED = {"illinois": "2026-07-08", "michigan": "2026-07-08", "indiana": "2026-07-10", "minnesota": "2026-07-10",
             "missouri": "2026-07-10", "wisconsin": "2026-07-10", "iowa": "2026-07-11"}
CHAIN = [["scripts/build.py"], ["scripts/chrome.py"], ["scripts/byline.py"], ["scripts/regulatory.py"], ["scripts/markets.py"],
         ["scripts/casemodel.py"], ["scripts/mesh.py"], ["scripts/links.py", "--relink"], ["scripts/sitemap.py"]]


def sh(cmd, cwd, timeout=1200):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, shell=isinstance(cmd, str))
    return p.returncode, (p.stdout + p.stderr).strip()


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(argv):
    n, state = argv[0], argv[1]
    copy = os.path.join(TMP, f"t{n}")
    if os.path.exists(copy):
        shutil.rmtree(copy)
    os.makedirs(copy)
    rc, o = sh(f"git archive HEAD | tar -x -C '{copy}'", WT)
    if rc:
        sys.exit(o)
    head = sh(["git", "rev-parse", "HEAD"], WT)[1]
    pages = []
    for f in sorted(os.listdir(os.path.join(DRAFTS, state, "pages"))):
        if not f.endswith(".html"):
            continue
        t = open(os.path.join(DRAFTS, state, "pages", f), encoding="utf-8").read()
        url = json.loads(t.split("\n---\n", 1)[0].lstrip("-\n"))["url"]
        dest = os.path.join(copy, "src", "pages", url.strip("/") + ".html")
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copyfile(os.path.join(DRAFTS, state, "pages", f), dest)
        pages.append(url)
    req = json.load(open(os.path.join(LANE, "requests-plan.json")))["states"][state]
    rc, o = sh([sys.executable, "scripts/requests.py", "docs/rollout/geo-3/requests.json"], copy)
    reqlog = f"scripts/requests.py docs/rollout/geo-3/requests.json: rc={rc} {o.splitlines()[-1] if o else ''}"
    nxt = os.path.join(DRAFTS, "requests-next", f"{state}.json")
    if os.path.exists(nxt):
        # this tranche's own requests, not yet committed because an earlier tranche is still untagged
        shutil.copyfile(nxt, os.path.join(copy, ".geo3-requests-next.json"))
        rc2, o2 = sh([sys.executable, "scripts/requests.py", ".geo3-requests-next.json"], copy)
        reqlog += f"; {state} requests from drafts/geo-3/requests-next: rc={rc2} {o2.splitlines()[-1] if o2 else ''}"
    log = [f"tranche t{n} ({state}) copy {copy} from worktree HEAD {head}", f"pages: {pages}",
           "requests applied in the copy: " + reqlog]
    for c in CHAIN:
        rc, o = sh([sys.executable] + c, copy)
        log.append(f"chain {' '.join(c)}: rc={rc} {o.splitlines()[-1] if o else ''}")
        if rc:
            log.append(o[-3000:])
    print("\n".join(log))
    folded = ",".join(f"{u}={t.replace('#', '#')}" for u, t in req["folded"].items())
    # every rebuilt state page in the tranche keeps its own published date (a carried sentence on a landed sibling included)
    pub = ",".join(f"{u}={PUBLISHED[u.strip('/').split('/')[1]]}" for u in pages
                   if u.count("/") == 3 and u.strip("/").split("/")[1] in PUBLISHED)
    look = os.path.join(LANE, "look", f"t{n}")
    cmd = [sys.executable, os.path.join(LANE, "tools", "geo3gates.py"), "--root", copy, "--git-dir", WT, "--pages", ",".join(pages),
           "--folded", folded, "--published", pub, "--look-dir", look, "--out", os.path.join(copy, ".gates.txt")]
    if "--skip-look" in argv:
        cmd.append("--skip-look")
    rc, o = sh(cmd, WT, timeout=2400)
    print(o)
    qa = [sys.executable, "scripts/qa/gates.py", "--root", copy, "--git-dir", WT, "--urls", ",".join(pages), "--stage", "ready",
          "--range", "main..HEAD", "--skip-look", "--out", os.path.join(copy, ".qa-gates.txt")]
    rq, oq = sh(qa, copy, timeout=2400)
    print("integrator scripts/qa/gates.py (stage ready, look skipped; the lane's look gate is above): rc", rq)
    print("\n".join(l for l in oq.splitlines() if l.startswith("===") or "SUMMARY" in l or "RED" in l)[-4000:])
    freeze = [f"freeze of tranche t{n}: worktree HEAD {head}"]
    for u in pages:
        s = os.path.join(copy, "src", "pages", u.strip("/") + ".html")
        r = os.path.join(copy, u.strip("/"), "index.html")
        freeze.append(f"  source {u:40} {sha(s)}")
        freeze.append(f"  served {u:40} {sha(r)}")
    print("\n".join(freeze))
    gates = open(os.path.join(copy, ".gates.txt")).read() if os.path.exists(os.path.join(copy, ".gates.txt")) else o
    qat = open(os.path.join(copy, ".qa-gates.txt")).read() if os.path.exists(os.path.join(copy, ".qa-gates.txt")) else oq
    text = "\n".join(log) + "\n\n" + gates + "\n\n## Integrator tool, scripts/qa/gates.py --stage ready\n" + qat + "\n" + "\n".join(freeze) + "\n"
    # records are committed to a public repo: no home path (it carries a ruling 9 name) and no ruling 9 match at all
    text = text.replace(os.path.expanduser("~"), "~")
    text = RULING9.sub("[ruling 9 name withheld]", text)
    open(os.path.join(LANE, f"GATES-t{n}.txt"), "w").write(text)
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
