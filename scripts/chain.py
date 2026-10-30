#!/usr/bin/env python3
"""Run the page chain over the whole tree, in order, each step under a timeout (FACTORY-2).

    python3 scripts/chain.py            build, chrome, byline, regulatory, markets, casemodel, mesh, links --relink, mesh, sitemap
    python3 scripts/chain.py --check    every step's --check (exit 1 on the first failure, after running them all)

The order is ROLLOUT-1's (Measured facts, the chain). Builders run it in a throwaway copy; the integrator runs it at
every landing. A step that fails stops the run (render) or is reported (check).
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STEPS = [["build.py"], ["chrome.py"], ["byline.py"], ["regulatory.py"], ["markets.py"], ["casemodel.py"],
         ["mesh.py"], ["links.py", "--relink"], ["mesh.py"], ["sitemap.py"]]
# mesh.py runs again after --relink: a pending link switched on moves where mesh.py may place a first-mention term
# link in the same sentence, so one more pass makes render and --check agree (geo-1-2)
CHECKS = [["build.py", "--check"], ["chrome.py", "--check"], ["byline.py", "--check"], ["regulatory.py", "--check"],
          ["markets.py", "--check"], ["casemodel.py", "--check"], ["mesh.py", "--check"], ["links.py", "--check"],
          ["sitemap.py", "--check"]]


def run(step, timeout=900):
    try:
        p = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", step[0])] + step[1:], cwd=ROOT,
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"


def main(argv):
    check = "--check" in argv
    bad = 0
    for step in (CHECKS if check else STEPS):
        rc, out = run(step)
        last = out.splitlines()[-1] if out else ""
        print(f"{' '.join(step):22} rc={rc}  {last}")
        if rc != 0:
            bad += 1
            for line in out.splitlines()[:40]:
                print("    " + line)
            if not check:
                return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
