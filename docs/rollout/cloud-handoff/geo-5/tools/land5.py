#!/usr/bin/env python3
"""GEO-5 landing edits the integrator owns, as the Montana landing made them (INT I185, commit 0310699).

    python3 land5.py <tree> <state-slug> "<State name>" "<index line>" --after-home "<State already on the home list>"

In <tree> (the integrator's worktree after the merge):
- /states/ (served-only page): a "State Practice" card appended after the last card, and a list item in the alphabetical
  list of state links (the line before the first state that sorts after it);
- the home page: a list item in the state row after --after-home (the row is ordered by size, not alphabetically), and
  the state count in <!--fsc:count:states--> on the home page and /the-practice/ raised by one;
- data/mesh/topics.json state_neighbors via neighbors5.py (idempotent).
The index_entry request supplies the card's line; chrome items, promised URLs and mesh terms come from scripts/requests.py.
Idempotent: a state already present is left alone. Prints every change.
"""
import argparse
import os
import re
import subprocess
import sys

CARD = """        <article class="card">
          <div class="card-top">
            <div class="card-cat">State Practice</div>
          </div>
          <div class="card-body">
            <h3><a href="/states/{slug}/">{name}</a></h3>
            <p>
              {line}
            </p>
            <a class="card-link" href="/states/{slug}/">Read the {name} practice &rarr;</a>
          </div>
        </article>
"""


def edit_states_index(tree, slug, name, line):
    p = os.path.join(tree, "states/index.html")
    s = open(p, encoding="utf-8").read()
    if f'Read the {name} practice' not in s:
        last = s.rfind("        </article>\n")
        if last < 0:
            raise SystemExit("states/index.html: no card to append after")
        at = last + len("        </article>\n")
        s = s[:at] + CARD.format(slug=slug, name=name, line=line) + s[at:]
        print(f"states/index.html: card for {name}")
    item = f'        <li><a href="/states/{slug}/">{name}</a></li>\n'
    if item not in s:
        rows = list(re.finditer(r'        <li><a href="/states/([a-z-]+)/">([^<]+)</a></li>\n', s))
        if not rows:
            raise SystemExit("states/index.html: no plain state list found")
        after = [m for m in rows if m.group(2) > name]
        at = after[0].start() if after else rows[-1].end()
        s = s[:at] + item + s[at:]
        print(f"states/index.html: list item for {name}")
    open(p, "w", encoding="utf-8").write(s)


def edit_home(tree, slug, name, after_home):
    p = os.path.join(tree, "index.html")
    s = open(p, encoding="utf-8").read()
    item = f'        <li><a href="/states/{slug}/">{name}</a></li>\n'
    if item not in s:
        anchor = f'        <li><a href="/states/{after_home.lower().replace(" ", "-")}/">{after_home}</a></li>\n'
        if s.count(anchor) != 1:
            raise SystemExit(f"index.html: anchor for {after_home} found {s.count(anchor)} times")
        s = s.replace(anchor, anchor + item)
        print(f"index.html: home list item for {name} after {after_home}")
        for q in (p, os.path.join(tree, "the-practice/index.html")):
            t = s if q == p else open(q, encoding="utf-8").read()
            t, n = re.subn(r"(<!--fsc:count:states-->)(\d+)(<!--/fsc:count:states-->)",
                           lambda m: f"{m.group(1)}{int(m.group(2)) + 1}{m.group(3)}", t)
            if n != 1:
                raise SystemExit(f"{q}: states count marker found {n} times")
            if q == p:
                s = t
            else:
                open(q, "w", encoding="utf-8").write(t)
            print(f"{os.path.relpath(q, tree)}: states count raised by one")
    open(p, "w", encoding="utf-8").write(s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tree")
    ap.add_argument("slug")
    ap.add_argument("name")
    ap.add_argument("line")
    ap.add_argument("--after-home", required=True)
    a = ap.parse_args()
    edit_states_index(a.tree, a.slug, a.name, a.line)
    edit_home(a.tree, a.slug, a.name, a.after_home)
    here = os.path.dirname(os.path.abspath(__file__))
    subprocess.run([sys.executable, os.path.join(here, "neighbors5.py"), a.tree], check=True, timeout=120)


if __name__ == "__main__":
    main()
