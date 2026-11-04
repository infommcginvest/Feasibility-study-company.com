#!/usr/bin/env python3
"""CLOUD-1 (CASE-NEW-1 tranche c1): slug prefixes for the promised hubs that new cases link before the hub is built.

    python3 topics_slug_prefix.py <tree>

scripts/mesh.py finds a case's asset class from the hub page the case links; when that hub is not built yet it falls
back to the asset's "slug_prefix" in data/mesh/topics.json, as "meat-processing-" already does for the meat hub (INT
I23). Without one the asset is empty and mesh.py stops on the practice-area case lists. This adds the prefix for the
promised hubs that tranches c1 to c3 link; a prefix already set is left alone. Idempotent; an asset missing from
topics.json stops the run. Applied by the integrator at landing, before the chain.
"""
import json
import sys
from collections import OrderedDict

PREFIX = {
    "/asset-classes/industrial-and-warehouse/": "industrial-warehouse-",
    "/asset-classes/event-and-wedding-venue/": "event-venue-",
    "/asset-classes/cold-storage/": "cold-storage-",
    "/asset-classes/brewery-and-distillery/": "brewery-",
    "/asset-classes/wellness-and-retreat/": "wellness-retreat-",
}


def main(tree):
    p = tree.rstrip("/") + "/data/mesh/topics.json"
    raw = open(p, encoding="utf-8").read()
    t = json.loads(raw, object_pairs_hook=OrderedDict)
    changed = 0
    for url, prefix in PREFIX.items():
        if url not in t["assets"]:
            raise SystemExit(f"topics_slug_prefix: {url} is not in topics.json assets")
        if t["assets"][url].get("slug_prefix"):
            continue
        t["assets"][url]["slug_prefix"] = prefix
        changed += 1
    if changed:
        indent = 2 if raw.startswith('{\n  "') else (1 if raw.startswith('{\n "') else None)
        open(p, "w", encoding="utf-8").write(json.dumps(t, ensure_ascii=False, indent=indent) + "\n")
    print(f"topics_slug_prefix: {changed} prefix(es) added")


if __name__ == "__main__":
    main(sys.argv[1])
