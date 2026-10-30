#!/usr/bin/env python3
"""GEO-5 D16: Northern Virginia's inbound links from the live neighbours, link-only edits on existing words.

    python3 nova_links.py <tree>

Maryland: "counties in Virginia" (the Washington metro's Virginia counties) links /states/virginia/northern-virginia/.
West Virginia: "Fairfax, Virginia" (where a certified development company is based) links the same page.
Each changed source has its "updated" set back to "DEPLOY" (ruling 12). Idempotent; a missing anchor stops the run.
"""
import re
import sys

URL = "/states/virginia/northern-virginia/"
EDITS = [
    ("src/pages/states/maryland.html", "with the District of Columbia and counties in Virginia and West Virginia",
     f'with the District of Columbia and <a href="{URL}">counties in Virginia</a> and West Virginia'),
    ("src/pages/states/west-virginia.html", "a certified development company based in Fairfax, Virginia,",
     f'a certified development company based in <a href="{URL}">Fairfax, Virginia</a>,'),
]


def main(tree):
    import os
    if not os.path.exists(tree.rstrip("/") + "/src/pages/states/virginia/northern-virginia.html"):
        print("nova_links: no Northern Virginia source in this tree; nothing changed")
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
