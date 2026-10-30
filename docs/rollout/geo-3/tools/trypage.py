#!/usr/bin/env python3
"""GEO-3 writer self-check: render draft sources into a throwaway copy and run lanecheck on them.

    python3 docs/rollout/geo-3/tools/trypage.py --root <copy> <draft.html> [<draft.html> ...] [--figures]

<copy> is a throwaway tree (git archive of the lane branch) under ~/Downloads/fsc-rollout/tmp/geo-3/.
Each draft is copied to <copy>/src/pages/<url>.html (from its front matter url), rendered with
build.py --page, then regulatory.py and markets.py --pages fill its markers. A lock file serializes
renders, because several writers share one copy. Then lanecheck runs on the drafts' URLs plus every
other state or metro page already rendered from this lane's drafts in the copy (the sibling matrix).
Never run this against the worktree.
"""
import fcntl
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def front(path):
    t = open(path, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    if not m:
        sys.exit(f"{path}: no front matter")
    return json.loads(m.group(1))


def run(cmd, cwd):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=900)
    out = (p.stdout + p.stderr).strip()
    return p.returncode, out


def main(argv):
    figs = "--figures" in argv
    argv = [a for a in argv if a != "--figures"]
    if argv[0] != "--root":
        sys.exit(__doc__)
    root = os.path.abspath(os.path.expanduser(argv[1]))
    if "fsc-rollout/tmp/geo-3" not in root:
        sys.exit("refusing: --root must be a throwaway copy under ~/Downloads/fsc-rollout/tmp/geo-3/")
    drafts = argv[2:]
    urls = []
    with open(os.path.join(root, ".geo3-render.lock"), "w") as lk:
        fcntl.flock(lk, fcntl.LOCK_EX)
        for d in drafts:
            fm = front(d)
            url = fm["url"]
            dest = os.path.join(root, "src", "pages", url.strip("/") + ".html")
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(d, dest)
            rc, out = run([sys.executable, "scripts/build.py", "--page", url], root)
            print(f"build {url}: exit {rc}")
            if rc:
                print(out[-3000:])
                continue
            served = os.path.join(root, url.strip("/"), "index.html")
            rc, out = run([sys.executable, "scripts/regulatory.py"], root)
            if rc:
                print("regulatory:", out[-2000:])
            rc, out = run([sys.executable, "scripts/markets.py", "--pages", served], root)
            if rc:
                print("markets:", out[-2000:])
            urls.append(url)
        fcntl.flock(lk, fcntl.LOCK_UN)
    if not urls:
        return 1
    # siblings: every lane page already rendered in the copy from src/pages/states/<state>/
    sib = set(urls)
    for u in list(urls):
        st = u.strip("/").split("/")[1]
        base = os.path.join(root, "src", "pages", "states", st)
        if os.path.exists(base + ".html"):
            sib.add(f"/states/{st}/")
        if os.path.isdir(base):
            for f in os.listdir(base):
                if f.endswith(".html"):
                    sib.add(f"/states/{st}/{f[:-5]}/")
    cmd = [sys.executable, os.path.join(HERE, "lanecheck.py"), "--root", root] + (["--figures"] if figs else []) + sorted(sib)
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    print(p.stdout[-20000:], p.stderr[-2000:])
    return p.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
