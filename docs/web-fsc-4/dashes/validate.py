#!/usr/bin/env python3
"""Validate a dash decisions file against its review file: python3 validate.py review-N.jsonl decisions-N.jsonl"""
import json, sys
OK = {"comma", "colon", "semicolon", "stop", "open", "close"}
rev = {json.loads(l)["key"]: json.loads(l) for l in open(sys.argv[1], encoding="utf-8") if l.strip()}
dec = {}
for i, l in enumerate(open(sys.argv[2], encoding="utf-8")):
    if l.strip():
        r = json.loads(l)
        dec[r["key"]] = r["d"]
bad = []
for k, r in rev.items():
    d = dec.get(k)
    if d is None:
        bad.append(f"missing key {k}")
        continue
    for i in r["decide"]:
        v = d.get(str(i))
        if v not in OK:
            bad.append(f"{k}: dash [{i}] has {v!r}")
    opens = sum(1 for v in d.values() if v == "open"); closes = sum(1 for v in d.values() if v == "close")
    if opens != closes:
        bad.append(f"{k}: {opens} open vs {closes} close")
extra = set(dec) - set(rev)
if extra:
    bad.append(f"{len(extra)} keys not in the review file")
for b in bad[:40]:
    print(b)
print(f"{len(rev)} sentences, {len(bad)} problem(s)")
sys.exit(1 if bad else 0)
