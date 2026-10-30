#!/usr/bin/env python3
"""GEO-4 freeze (amendment A2): sha256 of every tranche source and rendered page in the throwaway copy.

    python3 freeze.py <copy> <out FREEZE.txt> /states/florida/ /states/florida/miami/ ...

Write <out> OUTSIDE the copy root (gate 7 scans every file in the copy). Also records the worktree head the copy was archived from and a sha256 over the whole copy's
src/pages/states tree, so a later reviewer can tell whether anything moved.
"""
import hashlib
import os
import subprocess
import sys


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main(copy, out, *urls):
    head = subprocess.run(["git", "-C", os.path.expanduser("~/Downloads/wt-rollout-geo-5"), "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    lines = [f"freeze of {copy}", f"archived from worktree HEAD {head}", ""]
    tree = hashlib.sha256()
    for d, _, fs in sorted(os.walk(os.path.join(copy, "src/pages/states"))):
        for f in sorted(fs):
            p = os.path.join(d, f)
            tree.update(os.path.relpath(p, copy).encode() + b"\0" + sha(p).encode() + b"\n")
    lines.append(f"src/pages/states tree sha256 {tree.hexdigest()}")
    lines.append("")
    for u in urls:
        src = os.path.join(copy, "src/pages", u.strip("/") + ".html")
        page = os.path.join(copy, u.strip("/"), "index.html")
        lines.append(f"{u}\n  source  {sha(src)}  {os.path.relpath(src, copy)}\n  page    {sha(page)}  {os.path.relpath(page, copy)}")
    text = "\n".join(lines).replace(os.path.expanduser("~"), "~")  # records never carry the home path
    open(out, "w").write(text + "\n")
    print(text)


if __name__ == "__main__":
    main(*sys.argv[1:])
