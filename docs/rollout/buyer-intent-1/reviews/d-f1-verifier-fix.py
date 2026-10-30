#!/usr/bin/env python3
"""Verifier fixes for Track D freeze 1 (CLOUD-1, buyer intent on the 33 asset-class pages).

Two lists, applied by the coordinator in order:

  SRC_EDITS  = [(path under track-d/src, old, new), ...]
      old is exact raw text of the source file (front matter JSON, so quotes inside strings are written \\"),
      and occurs exactly once in the file at the moment the edit is applied (edits apply in list order).
  SPEC_EDITS = [(spec file in track-d/legacy/specs, element name, old, new), ...]
      old is an exact substring of that element's "after" and occurs exactly once in it at the moment the edit
      is applied (edits apply in list order); the description edits come with their og_ and twitter_ mirrors.

Run `python3 d-f1-verifier-fix.py <track-d dir> <out dir>` to apply both lists to copies of track-d/src and
track-d/legacy/specs written under <out dir> (the originals are never touched).
"""
import json
import os
import shutil
import sys

# ---------------------------------------------------------------------------------------------------------------
# Source pages (raw text of the front matter; \" is a JSON-escaped quote)
# ---------------------------------------------------------------------------------------------------------------
SRC_EDITS = [
    # A1-1: the 120-position clause carries no citation in the opening; use the body's own word. A2-7: the contact
    # link moves from a closing "point us to the exit to start" onto the study name.
    ("pages/asset-classes/gas-station-and-c-store/interstate-highway.html",
     r'prepares an interstate gas station feasibility study for an owner',
     r'prepares an <a href=\"/#contact\">interstate gas station feasibility study</a> for an owner'),
    ("pages/asset-classes/gas-station-and-c-store/interstate-highway.html",
     r'what happens when a 120-position travel center opens one exit away. SBA 7(a) and 504 lenders, CDCs and USDA review the same evidence; <a href=\"/#contact\">point us to the exit</a> to start.',
     r'what happens when a megasite travel center opens one exit away. SBA 7(a) and 504 lenders, CDCs and USDA review the same evidence.'),
    # A2-15: "study Feasibility Study Company writes" runs two noun phrases together.
    ("pages/asset-classes/hotel.html",
     r'Every hotel feasibility study Feasibility Study Company writes starts from',
     r'Each hotel feasibility study by Feasibility Study Company starts from'),
    # A2-3 (funeral / multifamily frame), A2-12 (shared three-item CTA tricolon)
    ("pages/asset-classes/multifamily.html",
     r"Feasibility Study Company's multifamily studies answer both for lenders.",
     r'lenders read both in a Feasibility Study Company multifamily study.'),
    ("pages/asset-classes/multifamily.html",
     r'the lease-up pace at your site, the effective rents behind your unit mix and the permanent loan your construction lender relies on. Feasibility Study Company builds the study around those three in',
     r'the lease-up pace at your site and the permanent loan your construction lender relies on. Feasibility Study Company builds the study around both in'),
    ("pages/asset-classes/self-storage.html",
     r'near your site, the street rates behind your lease-up and the coverage test your program applies.',
     r'near your site and the coverage test your program applies.'),
    # A2-12: second "methodology briefing shows how" CTA clause
    ("pages/asset-classes/gas-station-and-c-store.html",
     r'lender applies, and the methodology briefing shows how for your site, your format and your capital program.',
     r'lender applies.'),
    # A2-3 residual: "and Feasibility Study Company's ... studies" shared with behavioral health
    ("pages/asset-classes/mixed-use.html",
     r"Mixed-use buildings earn from more than one market, and Feasibility Study Company's feasibility studies test each income for owners, developers and lenders.",
     r'Mixed-use buildings earn from more than one market, which a Feasibility Study Company feasibility study tests use by use for owners, developers and lenders.'),
    # A2-3: behavioral health / burger frame ("..., FSC's ... studies start ..., for ... and lenders")
    ("pages/asset-classes/quick-service-restaurant/burger.html",
     r"Item 19 averages hide a wide spread, which is why Feasibility Study Company's burger studies start from the unit's own sales, for franchisees and lenders.",
     r"Item 19 averages hide a wide spread: a Feasibility Study Company burger study swaps the brand average for the unit's own sales, for franchisees and lenders."),
]

# ---------------------------------------------------------------------------------------------------------------
# Legacy hubs (spec elements: old is a substring of the element's "after")
# ---------------------------------------------------------------------------------------------------------------
LINK = '<a href="/#contact">'
SUP22 = '<sup class="fn"><a href="#s22">22</a></sup>'


def desc3(spec, old, new):
    """The description and its og and twitter mirrors."""
    return [(spec, "description", old, new), (spec, "og_description", old, new), (spec, "twitter_description", old, new)]


SPEC_EDITS = []

# V-1 (verifier): the description's "assisted living and memory care feasibility studies for" is an 8-word run shared
# with four case pages' CTA sentence.
SPEC_EDITS += desc3("asset-classes-assisted-living-and-memory-care.json",
                    "writes assisted living and memory care feasibility studies for owners and lenders.",
                    "writes memory care and assisted living feasibility studies for owners and lenders.")

# A1-8 (blue-sky "value" is the appraisal's), A2-7 (closing imperative to a link on the study name)
SPEC_EDITS += [
    ("asset-classes-auto-dealership.json", "opening",
     "so Feasibility Study Company builds its auto dealership feasibility studies around fixed operations",
     "so Feasibility Study Company builds its " + LINK + "auto dealership feasibility studies</a> around fixed operations"),
    ("asset-classes-auto-dealership.json", "opening",
     "Each one sets out blue-sky value, the floor-plan lien",
     "Each one sets out the blue-sky evidence, the floor-plan lien"),
    ("asset-classes-auto-dealership.json", "opening",
     " " + LINK + "Start with the rooftop and the franchise</a>.",
     ""),
]

# A2-4 / A2-3 (frame shared with the gas station description; no audience named), A2-7, A2-11
SPEC_EDITS += desc3("asset-classes-auto-service-and-collision.json",
                    "Whether the bays do general repair, collision or quick lube, Feasibility Study Company's auto service feasibility studies tie the ramp to technician supply.",
                    "Bay count means little without technicians; Feasibility Study Company ties auto service feasibility studies to staffing, for shop owners and lenders.")
SPEC_EDITS += [
    ("asset-classes-auto-service-and-collision.json", "opening",
     "for shop owners, developers and their lenders, and the market study",
     "for " + LINK + "shop owners</a>, developers and their lenders, and the market study"),
    ("asset-classes-auto-service-and-collision.json", "opening",
     " " + LINK + "Tell us about the shop and its trade area</a>.",
     ""),
    ("asset-classes-auto-service-and-collision.json", "cta_text",
     "coverage tests the study would run, and name the lender",
     "coverage tests, and name the lender"),
]

# A2-7
SPEC_EDITS += [
    ("asset-classes-behavioral-health.json", "opening",
     "for operators and developers and the lenders who fund them",
     "for " + LINK + "operators and developers</a> and the lenders who fund them"),
    ("asset-classes-behavioral-health.json", "opening",
     "files: " + LINK + "outline the facility and its payers</a>.",
     "files."),
]

# A2-7 (closing imperative), A2-11
SPEC_EDITS += [
    ("asset-classes-childcare-and-daycare.json", "opening",
     "within it for center owners, developers and the lenders they work with",
     "within it for " + LINK + "center owners</a>, developers and the lenders they work with"),
    ("asset-classes-childcare-and-daycare.json", "opening",
     " " + LINK + "Share the site and the licensing plan</a>.",
     ""),
    ("asset-classes-childcare-and-daycare.json", "cta_text",
     "ramp tests the study would run.",
     "ramp tests."),
]

# A2-8 (first-sentence frame shared with the restaurant opening and the dealership CTA heading)
SPEC_EDITS += [
    ("asset-classes-coffee-shop.json", "opening",
     "A coffee shop is an operating business before it is a building, so " + LINK + "start with the concept and the corner</a>, not the lease.",
     "A coffee shop earns as an operating business, so " + LINK + "the concept and the corner</a> matter more than the lease."),
]

# A2-7 (closing imperative), A2-11
SPEC_EDITS += [
    ("asset-classes-express-car-wash.json", "opening",
     "Feasibility Study Company prepares car wash feasibility studies that keep those values apart",
     "Feasibility Study Company prepares " + LINK + "car wash feasibility studies</a> that keep those values apart"),
    ("asset-classes-express-car-wash.json", "opening",
     " " + LINK + "Bring us the site and the format</a>.",
     ""),
    ("asset-classes-express-car-wash.json", "cta_text",
     ", and the scope of the study follows.",
     "."),
]

# A1-4 (a valuation is the appraisal's), A1-9 (the shake-out is source 22's), A2-7
SPEC_EDITS += [
    ("asset-classes-fitness-and-recreation.json", "opening",
     "pairing a trade-area market study with a valuation of the club as a going concern rather than as a building",
     "pairing a " + LINK + "trade-area market study</a> with a model that treats the club as a going concern rather than as a building"),
    ("asset-classes-fitness-and-recreation.json", "opening",
     'and then shook out.<sup class="fn"><a href="#s11">11</a></sup>',
     'and then shook out.<sup class="fn"><a href="#s11">11</a></sup>' + SUP22),
    ("asset-classes-fitness-and-recreation.json", "opening",
     " " + LINK + "Tell us the format and the trade area</a>.",
     ""),
]

# A2-8 (first-sentence frame shared with auto service), A2-7
SPEC_EDITS += [
    ("asset-classes-funeral-home.json", "opening",
     "share one market and very different economics.",
     "draw on one market and run on very different economics."),
    ("asset-classes-funeral-home.json", "opening",
     "prepares their feasibility studies, each grounded",
     "prepares their " + LINK + "feasibility studies</a>, each grounded"),
    ("asset-classes-funeral-home.json", "opening",
     " " + LINK + "Tell us about the firm or the site</a>.",
     ""),
]

# A2-8 ("Will the" opener shared with fitness; "off-season? Feasibility Study Company prepares" shared with RV park),
# A2-7, A2-11
SPEC_EDITS += [
    ("asset-classes-glamping.json", "opening",
     "Will the resort still cover its debt in the off-season? Feasibility Study Company prepares",
     "The off-season is where a glamping resort has to cover its debt. Feasibility Study Company prepares"),
    ("asset-classes-glamping.json", "opening",
     "feasibility studies for owners and developers, and for lenders using SBA",
     "feasibility studies for " + LINK + "owners and developers</a>, and for lenders using SBA"),
    ("asset-classes-glamping.json", "opening",
     " " + LINK + "Describe the land and the units</a>.",
     ""),
    ("asset-classes-glamping.json", "cta_text",
     "send the acreage, the unit plan and the program you expect to use.",
     "send the acreage and the unit plan."),
]

# A2-5 (three descriptions on "feasibility studies from Feasibility Study Company"), A2-10
SPEC_EDITS += desc3("asset-classes-grocery-store.json",
                    "grocery store feasibility studies from Feasibility Study Company for independent grocers, developers and lenders.",
                    "that is how Feasibility Study Company runs grocery store feasibility studies for independent grocers and lenders.")
SPEC_EDITS += [
    ("asset-classes-grocery-store.json", "opening",
     "the wholesaler lien before it sizes debt for bank",
     "the wholesaler lien, then sizes debt for bank"),
]

# A1-5 / A2-15 (the brand restated as the keyword in one clause)
SPEC_EDITS += desc3("asset-classes-laundromat.json",
                    "Feasibility Study Company is a laundromat feasibility study company for owners, buyers and lenders, testing utility cost, turns per day and the lease first.",
                    "Do the machines turn enough to cover rent? Feasibility Study Company checks that first in laundromat feasibility studies for owners, buyers and lenders.")

# A1-2 (the study does not value), A2-4 (frame shared with the interstate description), A2-9 (the pilot's first move)
SPEC_EDITS += desc3("asset-classes-marina.json",
                    "Built around slips, dry stack and the submerged-land lease, Feasibility Study Company's marina feasibility studies serve owners, developers and lenders.",
                    "Owners, developers and lenders turn to Feasibility Study Company for marina feasibility studies built on slips, dry stack and the submerged-land lease.")
SPEC_EDITS += [
    ("asset-classes-marina.json", "opening",
     ' Every boat sold needs a place to sit: new powerboat unit sales were 231,576 in 2024,<sup class="fn"><a href="#s2">2</a></sup> on top of the installed fleet, while permittable waterfront barely grows. Each study values the marina as a going concern',
     " Each study treats the marina as a going concern"),
    ("asset-classes-marina.json", "opening",
     '<p class="hero-sub">Feasibility Study Company prepares marina',
     '<p class="hero-sub">Every boat sold needs a place to sit: new powerboat unit sales were 231,576 in 2024,<sup class="fn"><a href="#s2">2</a></sup> on top of the installed fleet, while permittable waterfront barely grows. Feasibility Study Company prepares marina'),
    ("asset-classes-marina.json", "opening",
     "prepares marina, boat harbor and dry-stack feasibility studies for owners, developers and lenders, and each is built on a market study of the boats within reach of the water",
     "prepares " + LINK + "marina, boat harbor and dry-stack feasibility studies</a> for owners, developers and lenders, and each begins with a market study of the boats within reach of the water"),
    ("asset-classes-marina.json", "opening",
     " " + LINK + "Begin with the harbor and the lease</a>.",
     ""),
]

# A2-3 (frame shared with the car wash description; no audience named), A2-11
SPEC_EDITS += desc3("asset-classes-medical-office-and-asc.json",
                    "Unlike most real estate, a medical practice is valued on cash flow; Feasibility Study Company's medical office and ASC feasibility studies keep that line clear.",
                    "A practice is valued on cash flow, a medical office building on its leases; Feasibility Study Company models each basis for physician owners and lenders.")
SPEC_EDITS += [
    ("asset-classes-medical-office-and-asc.json", "cta_text",
     "Send the specialty, the site and the lender, and we will set out the study that fits that structure.",
     "Send the specialty, the site and the lender."),
]

# A2-5 (description), A2-9 (the pilot's first move), A1-6 (valuation is the appraisal's)
SPEC_EDITS += desc3("asset-classes-pet-boarding-and-daycare.json",
                    "Dog daycare, boarding and grooming projects get feasibility studies from Feasibility Study Company, built for owners, developers and their lenders.",
                    "Daycare and boarding earn differently; Feasibility Study Company projects both in its pet boarding feasibility studies for kennel owners and lenders.")
SPEC_EDITS += [
    ("asset-classes-pet-boarding-and-daycare.json", "opening",
     '<p class="hero-sub">Feasibility Study Company prepares pet boarding and daycare feasibility studies for kennel owners, developers and their lenders, each resting on a market study of the households nearby. The scope',
     '<p class="hero-sub">Daycare brings recurring weekday revenue and boarding brings episodic holiday peaks, so each pet boarding and daycare feasibility study models both through the ramp to stabilized occupancy. Feasibility Study Company writes them for kennel owners, developers and their lenders, each starting from a market study of the households nearby. The scope'),
    ("asset-classes-pet-boarding-and-daycare.json", "opening",
     " Daycare brings recurring weekday revenue and boarding brings episodic holiday peaks, so the study models both through the ramp to stabilized occupancy. " + LINK + "Tell us about the facility</a>",
     " " + LINK + "Tell us about the facility</a>"),
    ("asset-classes-pet-boarding-and-daycare.json", "cta_text",
     "describe the demand, ramp and valuation work the study would include.",
     "describe the demand and ramp work the study would include."),
]

# A1-3 (the study does not value the park), A2-1 (8-word run in the description), A2-8
SPEC_EDITS += desc3("asset-classes-rv-park-and-campground.json",
                    "campground feasibility studies for owners, developers and their lenders.",
                    "campground feasibility studies for park owners, developers and their lenders.")
SPEC_EDITS += [
    ("asset-classes-rv-park-and-campground.json", "opening",
     "Debt-fund, CMBS, bank, USDA and SBA lenders put the same question to an RV park: how steady is the cash flow through the off-season?",
     "Debt-fund, CMBS, bank, USDA and SBA lenders all size an RV park on how steady its cash flow stays between peak seasons."),
    ("asset-classes-rv-park-and-campground.json", "opening",
     "each study then values the park as a going concern",
     "each study then reads the park as a going concern"),
]

# A2-6 (description frame shared with urgent care and veterinary), A1-10 (unsupported lender claim, no period)
SPEC_EDITS += desc3("asset-classes-truck-stop-and-travel-center.json",
                    "Diesel gallons, truck traffic and the store mix decide truck stop credit; Feasibility Study Company prepares the study for owners, developers and lenders.",
                    "Truck stop credit rests on diesel gallons, truck traffic and the store mix, which Feasibility Study Company forecasts first for owners, developers and lenders.")
SPEC_EDITS += [
    ("asset-classes-truck-stop-and-travel-center.json", "opening",
     'came to roughly $13.6 billion,<sup class="fn"><a href="#s9">9</a></sup> and chains like it set the bar for every lender reading a travel center file, from banks, CMBS and C-PACE lenders and bridge funds to SBA 7(a) and 504 lenders and the USDA Business and Industry program.',
     'came to roughly $13.6 billion in January 2024,<sup class="fn"><a href="#s9">9</a></sup> and chains like it are the dominant competitive risk in underwriting an independent travel center, whether the lender is a bank, a CMBS or C-PACE lender, a bridge fund, an SBA 7(a) or 504 lender or the USDA Business and Industry program.'),
    ("asset-classes-truck-stop-and-travel-center.json", "opening",
     "Feasibility Study Company prepares feasibility studies for truck stops and travel centers, serving",
     "Feasibility Study Company prepares " + LINK + "feasibility studies for truck stops and travel centers</a>, serving"),
    ("asset-classes-truck-stop-and-travel-center.json", "opening",
     " " + LINK + "Name the corridor and the exit</a>.",
     ""),
]

# A2-7, A2-10 ("The deliverable suits" shared with the restaurant opening), A2-11
SPEC_EDITS += [
    ("asset-classes-urgent-care.json", "opening",
     "Feasibility Study Company prepares urgent care feasibility studies",
     LINK + "Feasibility Study Company</a> prepares urgent care feasibility studies"),
    ("asset-classes-urgent-care.json", "opening",
     "The deliverable suits SBA, USDA, conventional and specialty healthcare, net-lease and health-system lenders. " + LINK + "Tell us the trade area and the model</a>.",
     "It is written for SBA, USDA, conventional and specialty healthcare, net-lease and health-system lenders."),
    ("asset-classes-urgent-care.json", "cta_text",
     "send the address, the model and the payers you expect, and we will describe",
     "send the address, the model and any signed payer contracts, and we will describe"),
]

# A2-6 (description frame), A2-9 (the pilot's first move), A2-10, A2-7, A1-7 (the practice's worth is the appraisal's)
SPEC_EDITS += desc3("asset-classes-veterinary-practice.json",
                    "What a lender weighs in a veterinary practice is goodwill and DVM labor; Feasibility Study Company prepares feasibility studies for buyers, owners and lenders.",
                    "Goodwill and DVM labor are the first two things tested in a Feasibility Study Company veterinary feasibility study for buyers, owners and lenders.")
SPEC_EDITS += [
    ("asset-classes-veterinary-practice.json", "opening",
     '<p class="hero-sub">Feasibility Study Company prepares veterinary practice and animal hospital feasibility studies for veterinarians buying or building a practice, for developers',
     '<p class="hero-sub">A practice is a going concern whose value is mostly professional goodwill, so a veterinary feasibility study tests DVM staffing, production and the ramp. Feasibility Study Company prepares veterinary practice and animal hospital feasibility studies for ' + LINK + 'veterinarians buying or building a practice</a>, for developers'),
    ("asset-classes-veterinary-practice.json", "opening",
     " A practice is a going concern whose value is mostly professional goodwill, so the study tests DVM staffing, production and the ramp before it sets coverage. " + LINK + "Tell us about the practice</a>.",
     ""),
    ("asset-classes-veterinary-practice.json", "cta_heading",
     "What is the practice worth to a lender?",
     "What does a lender look for in a practice?"),
    ("asset-classes-veterinary-practice.json", "cta_text",
     "how the study measures each",
     "how the study tests each"),
]


# ---------------------------------------------------------------------------------------------------------------
def apply_all(track_d, out):
    """Apply both lists to copies under out/src and out/specs; return a list of problems."""
    problems = []
    src_out = os.path.join(out, "src")
    spec_out = os.path.join(out, "specs")
    for d in (src_out, spec_out):
        if os.path.exists(d):
            shutil.rmtree(d)
    shutil.copytree(os.path.join(track_d, "src"), src_out)
    shutil.copytree(os.path.join(track_d, "legacy", "specs"), spec_out)
    for rel, old, new in SRC_EDITS:
        p = os.path.join(src_out, rel)
        s = open(p, encoding="utf-8").read()
        if s.count(old) != 1:
            problems.append(f"SRC {rel}: old occurs {s.count(old)} times: {old[:70]!r}")
            continue
        open(p, "w", encoding="utf-8").write(s.replace(old, new, 1))
    for name, element, old, new in SPEC_EDITS:
        p = os.path.join(spec_out, name)
        d = json.load(open(p, encoding="utf-8"))
        els = [e for e in d["elements"] if e["element"] == element]
        if len(els) != 1:
            problems.append(f"SPEC {name}: element {element} found {len(els)} times")
            continue
        e = els[0]
        if e["after"].count(old) != 1:
            problems.append(f"SPEC {name} {element}: old occurs {e['after'].count(old)} times: {old[:70]!r}")
            continue
        e["after"] = e["after"].replace(old, new, 1)
        with open(p, "w", encoding="utf-8") as fh:
            json.dump(d, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
    return problems


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    probs = apply_all(sys.argv[1], sys.argv[2])
    for p in probs:
        print("PROBLEM:", p)
    print(f"{len(SRC_EDITS)} source edit(s), {len(SPEC_EDITS)} spec edit(s), {len(probs)} problem(s)")
    sys.exit(1 if probs else 0)
