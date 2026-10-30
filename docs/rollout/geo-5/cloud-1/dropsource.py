#!/usr/bin/env python3
"""dropsource.py <src.html> <n> [<n> ...]: remove uncited source entries (1-based numbers) from the front matter
and renumber every [^a,b] citation above them. Refuses when a number to drop is still cited."""
import json, re, sys
path, drops = sys.argv[1], sorted({int(x) for x in sys.argv[2:]})
s = open(path, encoding="utf-8").read()
m = re.match(r"---\n(.*?)\n---\n", s, re.S)
fm, body = json.loads(m.group(1)), s[m.end():]
text_wo_sources = json.dumps({k: v for k, v in fm.items() if k != "sources"}, ensure_ascii=False) + body
cited = {int(x) for g in re.findall(r"\[\^([\d,\s]+)\]", text_wo_sources) for x in re.split(r"[,\s]+", g) if x}
bad = [d for d in drops if d in cited]
if bad:
    sys.exit(f"STOP: still cited: {bad}")
def renum(mo):
    nums = [int(x) for x in re.split(r"[,\s]+", mo.group(1)) if x]
    out = [k - sum(1 for d in drops if d < k) for k in nums]
    return "[^" + ",".join(str(k) for k in out) + "]"
fm["sources"] = [e for i, e in enumerate(fm["sources"], 1) if i not in drops]
for k in list(fm):
    if k != "sources":
        fm[k] = json.loads(re.sub(r"\[\^([\d,\s]+)\]", renum, json.dumps(fm[k], ensure_ascii=False)))
body = re.sub(r"\[\^([\d,\s]+)\]", renum, body)
raw = m.group(1)
mi = re.match(r"\{\n( +)\"", raw)
indent = len(mi.group(1)) if mi else None
out = "---\n" + json.dumps(fm, ensure_ascii=False, indent=indent) + "\n---\n" + body
open(path, "w", encoding="utf-8").write(out)
print(f"dropped {drops}; {len(fm['sources'])} sources remain")
