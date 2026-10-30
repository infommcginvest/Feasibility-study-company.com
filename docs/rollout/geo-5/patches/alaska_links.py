#!/usr/bin/env python3
"""CLOUD-1 (GEO-5 t5, finding A2-1): Alaska's third real inbound link, a link-only edit on existing words.

    python3 alaska_links.py <tree>

The "Alaska" mesh term also lands inside "Alaska Native Corporations" on /research-notes/usda-rd-deadline-calendar/,
so only two live pages link /states/alaska/ for a reason (the hotel hub's establishment count and the default
economics note's charge-off rate). The gas station hub's sentence on the NACS store count names Alaska as one of the
eleven states with a published total; that fact makes the link. The hub sits at mesh's 15-term cap, so the link is
written by hand, as GEO-5 D16 did for Northern Virginia. The changed source has its "updated" set back to "DEPLOY"
(ruling 12). Idempotent; a missing anchor stops the run. Applied by the integrator at landing.
"""
import os
import re
import sys

URL = "/states/alaska/"
EDITS = [
    ("src/pages/asset-classes/gas-station-and-c-store.html",
     "publishes totals for the ten largest states and Alaska and",
     f'publishes totals for the ten largest states and <a href="{URL}">Alaska</a> and'),
]


def main(tree):
    if not os.path.exists(tree.rstrip("/") + "/src/pages/states/alaska.html"):
        print("alaska_links: no Alaska source in this tree; nothing changed")
        return
    for rel, old, new in EDITS:
        p = tree.rstrip("/") + "/" + rel
        s = open(p, encoding="utf-8").read()
        if new in s:
            print(rel, "already linked")
            continue
        if s.count(old) != 1:
            raise SystemExit(f"{rel}: anchor text found {s.count(old)} times, expected 1")
        s = s.replace(old, new)
        s, n = re.subn(r'"updated": "\d{4}-\d{2}-\d{2}"', '"updated": "DEPLOY"', s, count=1)
        if n != 1:
            raise SystemExit(f"{rel}: no pinned updated date to reset")
        open(p, "w", encoding="utf-8").write(s)
        print(rel, "linked; updated set to DEPLOY")


if __name__ == "__main__":
    main(sys.argv[1])
