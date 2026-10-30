#!/usr/bin/env python3
"""GEO-5: writer assignments from a pre-count (facts/<slug>.precount.json) and the fact sheet (facts/<slug>.facts.json).

    python3 assign_pc.py <state-slug> <code> "<State name>" [--neighbors-live a,b] [--neighbors-new c,d]

Writes assign/<slug>.json (the state page, with every folded market as a section) and assign/<slug>/<metro>.json for each
market whose verdict is "page". Each lists the countable facts in full (only the pre-count's free ids), the register pairs
the pre-count found for its geography, and, for the state, the standing metros it links but never repeats figures from.
"""
import argparse
import json
import os

D = os.path.expanduser("~/Downloads/fsc-rollout/drafts/geo-5/")


def rowmap(slug):
    return {f["id"]: f for f in json.load(open(D + f"facts/{slug}.facts.json"))["facts"] if not f.get("malformed")}


def facts_for(ids, rm, pc):
    out = []
    bl, sec = set(pc.get("borderline_ids", [])), set(pc.get("secondary_ids", []))
    for i in ids:
        f = rm.get(i)
        if not f:
            out.append({"id": i, "missing_from_sheet": True})
            continue
        out.append({"id": i, "value": f["value"], "what": f["what"], "period": f["period"], "published": f["published"],
                    "publisher": f["publisher"], "title": f["title"], "url": f["url"], "kind": f["kind"], "note": f["note"],
                    "section": f["section"], "borderline": i in bl, "secondary": i in sec})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("code")
    ap.add_argument("name")
    ap.add_argument("--neighbors-live", default="")
    ap.add_argument("--neighbors-new", default="")
    a = ap.parse_args()
    pc = json.load(open(D + f"facts/{a.slug}.precount.json"))
    rm = rowmap(a.slug)
    regs = pc.get("register_pairs", [])
    pages = [m for m in pc["markets"] if m["verdict"] == "page"]
    folded = [m for m in pc["markets"] if m["verdict"] != "page"]
    live = [f"/states/{s}/" for s in a.neighbors_live.split(",") if s]
    new = [f"/states/{s}/" for s in a.neighbors_new.split(",") if s]
    state = {
        "state": a.name, "slug": a.slug, "url": f"/states/{a.slug}/", "type": "state", "code": a.code,
        "published": "DEPLOY", "updated": "DEPLOY",
        "standing_metros": [{"slug": m["slug"], "name": m["name"], "url": f"/states/{a.slug}/{m['slug']}/",
                             "rule": "link it from the metros section and from text; never print a figure it counts"} for m in pages],
        "folded_markets": [{"slug": m["slug"], "name": m["name"], "section_id": m["slug"], "counties": m.get("counties", []),
                            "facts": facts_for(m["free_ids"], rm, pc)} for m in folded],
        "state_facts": facts_for(pc["state_free_ids"], rm, pc),
        "register": {"pairs_available": [r for r in regs if r["geo"] == a.code], "max": 10,
                     "rule": "at most 10, each a different series; never two vintages of one series (acs1 and acs5 of the same measure are one series for this rule); no PEP population"},
        "neighbors_live": live, "neighbors_not_live": new, "cases": [], "case_towns": [],
    }
    state["countable_total"] = len(state["state_facts"]) + sum(len(m["facts"]) for m in state["folded_markets"])
    os.makedirs(D + f"assign/{a.slug}", exist_ok=True)
    json.dump(state, open(D + f"assign/{a.slug}.json", "w"), indent=1, ensure_ascii=False)
    print(a.slug, "state countable", state["countable_total"], "folded", [m["slug"] for m in folded], "standing", [m["slug"] for m in pages])
    for m in pages:
        geos = sorted({r["geo"] for r in regs if r["geo"] != a.code})
        metro = {
            "state": a.name, "metro": m["name"], "slug": m["slug"], "url": f"/states/{a.slug}/{m['slug']}/", "type": "metro",
            "parent": f"/states/{a.slug}/", "published": "DEPLOY", "updated": "DEPLOY", "counties": m.get("counties", []),
            "facts": facts_for(m["free_ids"], rm, pc),
            "register": {"pairs_available": [r for r in regs if r["geo"] != a.code], "geos": geos, "max": 10,
                         "rule": "the metro's own CBSA or county keys only; at most 10, each a different series"},
            "siblings_folded": [{"slug": f["slug"], "name": f["name"], "href": f"/states/{a.slug}/#{f['slug']}"} for f in folded],
            "cases": [], "case_towns": [],
        }
        json.dump(metro, open(D + f"assign/{a.slug}/{m['slug']}.json", "w"), indent=1, ensure_ascii=False)
        print(" metro", m["slug"], "countable", len(metro["facts"]))


if __name__ == "__main__":
    main()
