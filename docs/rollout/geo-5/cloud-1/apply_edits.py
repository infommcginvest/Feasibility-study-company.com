#!/usr/bin/env python3
"""apply_edits.py <fix.py> <pagename> <in> <out> [--extra NAME]: apply EDITS (and optional extra lists) whose first
element equals <pagename>; each old string must occur exactly once at the moment it is applied, else stop."""
import runpy, sys
fix, page, src, dst = sys.argv[1:5]
extra = sys.argv[sys.argv.index("--extra") + 1].split(",") if "--extra" in sys.argv else []
d = runpy.run_path(fix)
edits = list(d["EDITS"])
for name in extra:
    edits += d[name]
s = open(src, encoding="utf-8").read()
n = 0
for e in edits:
    p, old, new = e[0], e[1], e[2]
    if p != page:
        continue
    c = s.count(old)
    if c != 1:
        sys.exit(f"STOP: {c} occurrences of {old[:90]!r}")
    s = s.replace(old, new)
    n += 1
open(dst, "w", encoding="utf-8").write(s)
print(f"{n} edits applied -> {dst}")
