#!/usr/bin/env python3
"""GEO-5: add the eight new states' land borders to data/mesh/topics.json state_neighbors (symmetric, idempotent).

    python3 neighbors5.py <tree>

mesh.py lists only neighbours whose page exists, so a state that has not landed shows nowhere. Corner touches are not borders
(Colorado and Arizona). Alaska has no land border with another state.
"""
import json
import sys

B = {
    "colorado": ["wyoming", "nebraska", "kansas", "oklahoma", "new-mexico", "utah"],
    "virginia": ["maryland", "district-of-columbia", "west-virginia", "kentucky", "tennessee", "north-carolina"],
    "south-dakota": ["north-dakota", "minnesota", "iowa", "nebraska", "wyoming", "montana"],
    "north-dakota": ["minnesota", "south-dakota", "montana"],
    "alaska": [],
    "wyoming": ["montana", "south-dakota", "nebraska", "colorado", "utah", "idaho"],
    "district-of-columbia": ["maryland", "virginia"],
    "vermont": ["new-hampshire", "massachusetts", "new-york"],
}


def main(tree):
    p = tree.rstrip("/") + "/data/mesh/topics.json"
    t = json.load(open(p))
    nb = t["state_neighbors"]
    added = 0
    for s, ns in B.items():
        for n in ns:
            for a, b in ((s, n), (n, s)):
                ka, kb = f"/states/{a}/", f"/states/{b}/"
                lst = nb.setdefault(ka, [])
                if kb not in lst:
                    lst.append(kb)
                    lst.sort()
                    added += 1
        nb.setdefault(f"/states/{s}/", [])
    t["state_neighbors"] = dict(sorted(nb.items()))
    json.dump(t, open(p, "w"), indent=2, ensure_ascii=False)
    open(p, "a").write("\n")
    print(f"state_neighbors: {added} directed edges added, {len(nb)} states")


if __name__ == "__main__":
    main(sys.argv[1])
