# GEO-5 t2 freeze 1, verifier fix list. Paths are relative to drafts/geo-5/pages.
# Each old text occurs exactly once in its file (checked by apply). No dash characters, no new figure.
# Finding ids in comments: A1-n from attacker1, A2-n from attacker2.

VA = "virginia.html"
NV = "virginia/northern-virginia.html"

EDITS = [
    # A1-1: FRED's own seasonal adjustment printed to five decimals under a Census attribution.
    # Source 26 is kept (as the FRED-adjusted version, no value printed) so no later citation renumbers.
    (VA,
     "before seasonal adjustment [^25], and 3,274.12673 units for the same month on the seasonally adjusted series [^26]. A single month is a thin base for a housing study. The adjusted figure removes the seasonal swing, and neither is a full-year total, which a study takes",
     "before seasonal adjustment [^25]. FRED adjusts the same series for season itself and posts that version separately [^26]. A single month is a thin base for a housing study, and neither version is a full-year total, which a study takes"),
    (VA,
     '"publisher": "Federal Reserve Bank of St. Louis (FRED), relaying the U.S. Census Bureau",\n      "title": "New Private Housing Units Authorized by Building Permits for Virginia",\n      "date": "last updated October 27, 2026 (September 2026, seasonally adjusted)"',
     '"publisher": "Federal Reserve Bank of St. Louis (FRED), seasonally adjusting U.S. Census Bureau data",\n      "title": "New Private Housing Units Authorized by Building Permits for Virginia",\n      "date": "last updated October 27, 2026 (September 2026, seasonally adjusted)"'),

    # A1-2 (and A2-14, second bullet): the three-county list is the OEWS definition only.
    (VA,
     'and both versions take in Camden, Currituck and Gates counties in <a href="/states/north-carolina/">North Carolina</a> [^9].',
     'and each version reaches into <a href="/states/north-carolina/">North Carolina</a>: the occupational survey names Camden, Currituck and Gates counties [^9] and the payroll table Currituck County [^8].'),
    (VA,
     "BLS, FHFA and BEA publish the metro with Camden, Currituck and Gates counties in North Carolina included [^9], so every",
     "BLS, FHFA and BEA publish the metro with North Carolina counties included [^8,9,45,46], so every"),

    # A1-3: Hampton Roads metro-wide count printed without its North Carolina label.
    (VA,
     "and 164.5 thousand in Hampton Roads [^8]",
     "and 164.5 thousand in the Hampton Roads metro, which reaches into North Carolina [^8]"),

    # A1-4 (and A2-14, last bullet): comparison in words, values in other sentences (I60 b).
    (VA,
     "Both outlets were reporting on the commission's work, and they print different amounts.",
     "Both outlets were reporting on the commission's work."),

    # A1-6 / A2-5(a): Richmond vacancy rates compared, neither printed.
    (VA,
     "in their own ways and report different vacancy rates for the quarter, so each",
     "in their own ways, so each"),

    # A1-7 / A2-5(b): Weldon Cooper estimates compared, not printed.
    (VA,
     "the Weldon Cooper Center's estimates, which differ for both [^56]",
     "the Weldon Cooper Center's estimates as well [^56]"),

    # A2-2: REBusinessOnline 448204 (January 13, 2026) says the venture "is set to break ground" and that site work began
    # in December; it does not report a January 2026 groundbreaking. A2-5(c): H2 swing claim has no source. One H2 edit covers both.
    (VA,
     "Two developments near Virginia Tech broke ground, one in October 2025 and one in January 2026, as REBusinessOnline reported [^31,32].",
     "REBusinessOnline reported one development near Virginia Tech breaking ground in October 2025 [^31] and, on January 13, 2026, a second set to break ground, with site work begun in December [^32]."),
    (VA,
     "Two student housing developments near Virginia Tech break ground",
     "One student housing development near Virginia Tech breaks ground and a second is reported as set to break ground"),
    (VA,
     '"date": "January 13, 2026 (groundbreaking January 2026)"',
     '"date": "January 13, 2026 (site work begun December 2025)"'),
    (VA,
     "Blacksburg-Christiansburg: a university payroll that swings with the academic year, and student housing in the ground.",
     "Blacksburg-Christiansburg: a university metro's payroll and student housing projects near campus."),

    # A2-5(c): uncited cause (summer months, academic calendar); no summer value is printed or in the research.
    (VA,
     "The summer months in the same series run lower, which follows the academic calendar of the universities in the metro, so a study that reads a single month says which month it read.",
     "A study that reads a single month says which month it read."),
    (VA,
     "Virginia Tech's metro, where the monthly payroll follows the academic calendar.",
     "Virginia Tech's metro, read on a payroll count, a county price series and student housing reports."),

    # A2-9: 10-word run shared with pages/colorado.html.
    (VA,
     "The reply sets out the analytical framework, the deliverable that program asks for and the next steps.",
     "The reply states the approach the study takes, the program's deliverable and what comes next."),

    # A2-14 (first bullet): "named for its central city" is false for Hampton Roads and Blacksburg-Christiansburg.
    (VA,
     "Each of the eight is a Census metropolitan area named for its central city;",
     "Each of the eight is read as a metropolitan area;"),

    # ---- Northern Virginia ----
    # A1-5 / A2-5 (NOVA): broker figures compared in words, values in later sentences.
    (NV,
     "Their figures for the same quarter therefore differ, and this page states",
     "This page states"),

    # A1-11 (I64): Alexandria +377,800 sf is one occupier's 386,600 sf move (research row 47 note "single-property").
    (NV,
     "and net absorption of +377,800 square feet in Alexandria that it attributes",
     "and net absorption of <span data-fsc-nocount>+377,800</span> square feet in Alexandria that it attributes"),
    (NV,
     "and +377,800 in Alexandria, a city figure it attributes",
     "and <span data-fsc-nocount>+377,800</span> in Alexandria, a city figure it attributes"),
    (NV,
     "<td>+377,800 sf</td>",
     "<td><span data-fsc-nocount>+377,800 sf</span></td>"),

    # A2-1 BLOCKER: "As a Northern Virginia feasibility study company, we" says the firm sits in Northern Virginia.
    # The keyword stays (owner's buyer-intent rule) in a sentence about the buyer, with no we, office, staff or location.
    (NV,
     "As a Northern Virginia feasibility study company, we write the study to the program the capital comes from, and the parcel decides which programs are open.",
     "Someone hiring a Northern Virginia feasibility study company needs the study written to the program the capital comes from, and the parcel decides which programs are open."),

    # A2-3: Loudoun (north and east boundary) and Prince William (eastern shore) both lie on the Potomac.
    (NV,
     "The Potomac jurisdictions shed covered jobs over the twelve months to March 2026; Loudoun and Prince William gained.",
     "Fairfax, Arlington and Alexandria shed covered jobs over the twelve months to March 2026; Loudoun and Prince William gained."),
    (NV,
     "The three jurisdictions on or near the Potomac lost ground; the two counties farther out gained it. ",
     ""),

    # A2-4: closing band draws a conclusion no source states.
    (NV,
     "and two rose, so a regional average now describes none of them.",
     "and two rose."),

    # A2-8: Prince William's $599,995 is printed by source 5 only; source 6 is Loudoun.
    (NV,
     "its $599,995 listing median [^5,6] describe the county",
     "its $599,995 listing median [^5] describe the county"),

    # Tool artifact: cta.p ends "and the steps that follow" and the description starts "Feasibility Study Company prepares",
    # which sameness.py joins into an 8-word run with district-of-columbia.html (same ending, same description start).
    (NV,
     "the deliverable the program calls for and the steps that follow.",
     "the deliverable the program calls for and what comes next."),

    # A2-10(a): 8-word run shared with pages/colorado.html.
    (NV,
     "Feasibility Study Company writes independent, lender-grade feasibility studies for projects in Fairfax",
     "Feasibility Study Company writes independent, lender-grade feasibility studies on projects in Fairfax"),
]
