#!/usr/bin/env python3
"""WEB-FSC-4 ruling 10: sister-property citations become primary sources or "industry research".

Each entry is (page, old phrase, new phrase). Old phrases match across line
breaks. Figures and years are never part of a change. Every entry must match
exactly once, or the script stops. Idempotent: an entry whose new phrase is
already in place and whose old phrase is gone is skipped.

    python3 docs/web-fsc-4/tools/relabel.py [--only page,page]
"""
import os, re, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# Spelled in pieces so this served file never carries the names it removes.
LA = "Loan " + "Analytics"; AL = "analytics" + ".loan"; MC = "MM" + "CG"; IW = "Inno" + "wave"
FC = "Feasibility-study-" + "consultant.com"
T = [
 ("asset-classes/express-car-wash/index.html", f"churn up 5&ndash;6% YoY ({LA}).", "churn up 5&ndash;6% YoY (industry research)."),
 ("asset-classes/glamping/index.html", f"(industry research, citing Sage/{IW})", "(industry research, citing Sage)"),
 ("asset-classes/multifamily/index.html", f"Zillow, and the {MC} database, Q4 2025", "Zillow, and an industry database, Q4 2025"),
 ("asset-classes/multifamily/index.html", f'<li id="s15">{MC} database (Q1 2026):', '<li id="s15">Industry database (Q1 2026):'),
 ("asset-classes/rv-and-boat-storage/index.html", f"~597 acres per {AL}</span>", "~597 acres per industry research</span>"),
 ("asset-classes/rv-and-boat-storage/index.html", f"StorageCafe (2025), {AL} and industry research (2025&ndash;2026)", "StorageCafe (2025), industry research (2025&ndash;2026)"),
 ("asset-classes/rv-and-boat-storage/index.html", f'<li id="s7">{AL} and industry research (2025&ndash;2026):', '<li id="s7">Industry research (2025&ndash;2026):'),
 ("asset-classes/rv-park-and-campground/index.html", f'<li id="s18">{FC}, RoverPass, RJourney, and RV Podcast', '<li id="s18">Industry research, RoverPass, RJourney, and RV Podcast'),
 ("asset-classes/rv-park-and-campground/index.html", f'<li id="s20">{LA} / industry research and {IW} Studio (2024&ndash;2025):', '<li id="s20">Industry research (2024&ndash;2025):'),
 ("asset-classes/self-storage/index.html", f'<li id="s24">{LA} (2026) and multiple builders:', '<li id="s24">Industry research (2026) and multiple builders:'),
 ("case-studies/assisted-living-florida-hud/index.html", f"labor share per Janover/{MC} and PHI.", "labor share per Janover, industry research and PHI."),
 ("case-studies/assisted-living-florida-hud/index.html", f'<li id="s6">Janover Pro and {MC} (2025):', '<li id="s6">Janover Pro and industry research (2025):'),
 ("case-studies/assisted-living-hawaii-hud/index.html", f'<li id="s6">Janover Pro and {MC} (2025):', '<li id="s6">Janover Pro and industry research (2025):'),
 ("case-studies/assisted-living-north-carolina-hud/index.html", f'<li id="s7">Janover Pro and {MC} (2025):', '<li id="s7">Janover Pro and industry research (2025):'),
 ("case-studies/rv-park-arizona-usda/index.html", f'<li id="s6">{LA} / {MC} and {IW} Studio (2024&ndash;2025):', '<li id="s6">Industry research (2024&ndash;2025):'),
 ("case-studies/rv-park-arizona-usda/index.html", f'<li id="s7">{FC}, RoverPass, and RJourney', '<li id="s7">Industry research, RoverPass, and RJourney'),
 ("case-studies/rv-park-arizona-usda/index.html", f"effective October 1, 2020), via {MC} and Business Finance Depot:", "effective October 1, 2020), via Business Finance Depot:"),
 ("case-studies/rv-park-maine-usda/index.html", f"RoverPass, RJourney, {FC}, Financial Models Lab,", "RoverPass, RJourney, industry research, Financial Models Lab,"),
 ("case-studies/rv-park-maine-usda/index.html", f'<li id="s7">{LA} / {MC} and {IW} Studio (2024&ndash;2025):', '<li id="s7">Industry research (2024&ndash;2025):'),
 ("case-studies/self-storage-arizona-sba/index.html", f'<li id="s10">{LA} (2026) and multiple builders:', '<li id="s10">Industry research (2026) and multiple builders:'),
 ("case-studies/self-storage-indiana-sba/index.html", f'<li id="s8">{LA} (2026) and multiple builders:', '<li id="s8">Industry research (2026) and multiple builders:'),
 ("research-notes/break-even-occupancy-trap/index.html", f"mid-6 percent range through 2025 ({MC}).", "mid-6 percent range through 2025 (industry research)."),
 ("research-notes/c-store-franchise-category/index.html", f"({IW} Studio; CT Acquisitions; Mill Creek Environmental,", "(industry research; CT Acquisitions; Mill Creek Environmental,"),
 ("research-notes/c-store-franchise-category/index.html", f"from the EPA and from {IW} Studio, CT Acquisitions, and Mill Creek Environmental", "from the EPA and from industry research, CT Acquisitions, and Mill Creek Environmental"),
 ("research-notes/effective-rent-vs-asking-rent/index.html", f"at the margin: {MC}'s database showed national asking", "at the margin: an industry database showed national asking"),
 ("research-notes/effective-rent-vs-asking-rent/index.html", f"ALN Apartment Data, and {MC}'s multifamily database (dated inline,", "ALN Apartment Data, and an industry multifamily database (dated inline,"),
 ("research-notes/sba-feasibility-myth/index.html", f"several high-ranking pages, including that of {LA}, reproduce", "several high-ranking pages, including that of a loan-data site, reproduce"),
 ("research-notes/sba-feasibility-myth/index.html", f'the codified text; {LA} further frames a study as a', 'the codified text; that site further frames a study as a'),
 ("research-notes/sba-feasibility-myth/index.html", f"quoted or paraphrased from the named firms' own pages: {LA} ({AL}), Peak Business Valuation", "quoted or paraphrased from the firms' own pages: a loan-data site, Peak Business Valuation"),
 ("research-notes/underserved-gas-station-markets/index.html", f"brokerage sources ({MC}, STAX, Matthews, MSSA, Orbital, IBISWorld)", "brokerage sources (industry research, STAX, Matthews, MSSA, Orbital, IBISWorld)"),
 ("states/pennsylvania/index.html", f"NAGGL; {LA} summary of SBA FY2025 data.", "NAGGL; industry research summary of SBA FY2025 data."),
 ("states/south-carolina/index.html", f"GoSBA / {AL} calendar-year 2025 totals.", "GoSBA / industry research calendar-year 2025 totals."),
 # recompute pages (applied after their recompute agents finished)
 ("case-studies/rv-boat-storage-arizona-sba/index.html", f'<li id="s7">{AL} and industry research (2025&ndash;2026), with Extra Space', '<li id="s7">Industry research (2025&ndash;2026), with Extra Space'),
 ("case-studies/rv-boat-storage-california-sba/index.html", f'<li id="s6">{AL} and industry research (2025&ndash;2026):', '<li id="s6">Industry research (2025&ndash;2026):'),
 ("case-studies/rv-boat-storage-florida-sba/index.html", f'<li id="s5">{AL} and industry research (2025&ndash;2026):', '<li id="s5">Industry research (2025&ndash;2026):'),
]

def rx(phrase):
    return re.compile(r"\s+".join(re.escape(w) for w in phrase.split(" ")))

def main(argv):
    only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
    skip = set(argv[argv.index("--skip") + 1].split(",")) if "--skip" in argv else set()
    done = 0
    for page, old, new in T:
        if (only and page not in only) or page in skip:
            continue
        p = os.path.join(ROOT, page)
        s = open(p, encoding="utf-8").read()
        hits = rx(old).findall(s)
        if not hits:
            if rx(new).search(s):
                continue
            raise SystemExit(f"{page}: phrase not found: {old!r}")
        if len(hits) != 1:
            raise SystemExit(f"{page}: phrase found {len(hits)} times: {old!r}")
        s = rx(old).sub(new.replace("\\", "\\\\"), s, count=1)
        open(p, "w", encoding="utf-8").write(s)
        done += 1
        print(f"relabelled {page}: {new[:70]}")
    print(f"{done} change(s)")

if __name__ == "__main__":
    main(sys.argv[1:])
