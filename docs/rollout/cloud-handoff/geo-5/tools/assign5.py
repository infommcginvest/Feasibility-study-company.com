#!/usr/bin/env python3
"""GEO-5: write a writer's assignment from a state's fact sheet (yield5.py output) and its market plan.

    python3 assign5.py <state-slug>

Reads facts/<slug>.facts.json and assign/<slug>.plan.json ({"name", "code", "markets": [{"slug", "name", "sections": [MT section
headings]}], "neighbors_live": [...], "neighbors_new": [...]}), and writes assign/<slug>.json:
- countable: fact ids yield5 found dated, read as a figure, market-level, free on the served site and not shared with
  another GEO-5 state (one id per value); grouped by the ST section or the market they belong to;
- context_only: dated facts that may be printed only inside data-fsc-nocount (secondary rows already counted elsewhere on
  the page by value, single-property rows, rule values that read as figures but are taken);
- never: undated rows and rows whose value is research arithmetic (not printed at all, I86, I55).
"""
import json
import os
import sys

D = os.path.expanduser("~/Downloads/fsc-rollout/drafts/geo-5/")
REGISTER = ["acs5_median_hh_income", "acs5_median_gross_rent", "acs5_median_home_value", "acs5_renter_occupied", "acs5_pop65",
            "acs5_labor_force", "bea_per_capita_income", "sba7a_loans", "sba7a_volume", "sba504_loans", "sba504_volume",
            "sba7a_chgoff_rate", "cbp_estab"]


def main(slug):
    facts = json.load(open(D + f"facts/{slug}.facts.json"))["facts"]
    plan = json.load(open(D + f"assign/{slug}.plan.json"))
    sec_to_market = {}
    for m in plan["markets"]:
        for s in m["sections"]:
            sec_to_market[s] = m["slug"]
    countable, context, never = {}, [], []
    for f in facts:
        if f.get("malformed"):
            continue
        where = sec_to_market.get(f["section"], "state") if f["file"] == "MT" else "state"
        row = {"id": f["id"], "value": f["value"], "what": f["what"], "period": f["period"], "published": f["published"],
               "publisher": f["publisher"], "title": f["title"], "url": f["url"], "kind": f["kind"], "section": f["section"]}
        if f.get("countable"):
            countable.setdefault(where, []).append(row)
        elif f["dated"] and f["figure"] and not f.get("countable"):
            row["why"] = ("taken by " + ", ".join(f["taken"])) if f["taken"] else (
                "shared with " + ", ".join(f.get("shared_geo5", [])) if f.get("shared_geo5") else (
                    "single-property or arithmetic" if not f["market"] else "repeat of a value already assigned"))
            if f["market"] or "single-property" in f["note"].lower():
                context.append(row)
            else:
                never.append({"id": f["id"], "why": "research arithmetic (I55)"})
        else:
            never.append({"id": f["id"], "why": "undated (I86)" if not f["dated"] else "no figure read"})
    out = {
        "state": plan["name"], "slug": slug, "url": f"/states/{slug}/", "code": plan["code"],
        "published": "DEPLOY", "updated": "DEPLOY",
        "markets": [{"slug": m["slug"], "name": m["name"], "section_id": m["slug"], "counties": m.get("counties", [])} for m in plan["markets"]],
        "neighbors_live": plan.get("neighbors_live", []), "neighbors_not_live": plan.get("neighbors_new", []),
        "register": {"geo": plan["code"], "series": REGISTER, "max": 10, "note": "one series and geography pair each; values under data/markets/series/<series>.json values.<geo>; no null or flagged value"},
        "countable_total": sum(len(v) for v in countable.values()),
        "countable": countable, "context_only": context, "never": never,
        "cases": [], "case_towns": [],
    }
    json.dump(out, open(D + f"assign/{slug}.json", "w"), indent=1, ensure_ascii=False)
    print(slug, "countable", out["countable_total"], {k: len(v) for k, v in countable.items()}, "context", len(context), "never", len(never))


if __name__ == "__main__":
    main(sys.argv[1])
