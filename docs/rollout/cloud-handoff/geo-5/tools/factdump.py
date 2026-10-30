#!/usr/bin/env python3
"""Print the California fact sheet by geography with dating, class and site status (collide.json)."""
import json, sys, os
F = os.path.expanduser("~/Downloads/fsc-rollout/drafts/geo-5/facts/")
d = json.load(open(F + "california.json"))
c = json.load(open(F + "california.collide.json"))
st = {}
for g, v in c["by_geo"].items():
    for f in v["figures"]:
        st[f["id"]] = f["status"] + ("" if f.get("lane_alloc") in (None, "kept") else "/" + str(f.get("lane_alloc")))
for k, v in c["not_countable"].items():
    st.setdefault(k, "nc:" + v["status"])
geos = sys.argv[1:] or None
for f in d["facts"]:
    if geos and f["geo"] not in geos:
        continue
    print(f'{f["id"]}|{f["geo"]}|{f["class"]}|{f["dating"]}{"*" if f.get("dating_borderline") else ""}|{st.get(f["id"], "-")}|{f["value"]}|{f["what"]}|{f["period"]}|{f["publisher"]}|{f["title"][:70]}|{f.get("place") or ""}|{f["research_ref"]}|{",".join(f.get("flags", []))}')
