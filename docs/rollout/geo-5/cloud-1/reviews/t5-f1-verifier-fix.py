# GEO-5 t5 (Alaska) freeze 1 verifier fix list. Paths are relative to drafts/geo-5/pages
# (the page source is src/pages/states/alaska.html in the frozen copy).
# Every edit below is for a finding the verifier CONFIRMED. Each old string occurs exactly once
# in the source. Edits are independent of one another (no old string overlaps another).
#
# NON-DELETION edits (they change or add words, so a capped review should read them):
#   N1 (A2-6)  #population data-h2 rewritten
#   N2 (A2-7)  #capital lede, sentences 2 and 3 reordered/trimmed
#   N3 (A2-12) #events data-h2 rewritten
#   N4 (A2-12) #costs data-h2 clause replaced
#   N5 (A2-12) #assets data-h2 rewritten
#   N6 (A2-13) #oil-and-treasury opening: "two readers" clause reworded
#   N7 (A2-14) 504 equity sentence gains ", and more when it is both" (no figure added)
#   N8 (A2-19) cta.p "that program" -> "the lender's program"
#   N9 (A1-2)  #kodiak paragraph 2 first sentence replaced (dangling reference to the deleted payroll lines)
# Everything else is a pure deletion (the new text is the old text with words removed).
EDITS = [
    # ---- A1-1 (ruling 10, D20): two DOLWD vintages on one page; delete the 1,163 paragraph. Source [^25] stays cited in #kenai-peninsula.
    ("alaska.html",
     "<p>The direction of migration is not new. A year earlier the department had estimated net out-migration of 1,163 for 2023 to 2024, as the Peninsula Clarion reported in January 2025 [^25]; that vintage has since been revised, so the figure describes what the department said then, not the current series.</p>\n",
     ""),

    # ---- A1-2 (I176, strict): source 5 (bls.gov/regions/west/alaska.htm) carries no title the research holds; drop every claim resting on it.
    # (a) #economy paragraph 1: the 365.2 labor force clause
    ("alaska.html",
     ", and a seasonally adjusted civilian labor force of 365.2 thousand [^5]. The Department of Labor",
     ". The Department of Labor"),
    # (b) #economy paragraph 2 (also covers A2-8 first move): the sector lines sentences and the dangling "government line" clause
    ("alaska.html",
     "<p>The sector lines say more about a given project than the total does. In BLS's seasonally adjusted September 2026 figures, all preliminary, construction held 17.7 thousand jobs (-5.3%), government 76.8 thousand (-3.0%) and manufacturing 13.9 thousand (+14.9%), each change measured over twelve months as printed [^5]. The department's Alaska Economic Trends for August 2026 carries an article on the federal jobs Alaska lost in 2025 [^19], and federal employers sit inside the government line.</p>",
     "<p>The department's Alaska Economic Trends for August 2026 carries an article on the federal jobs Alaska lost in 2025 [^19].</p>"),
    # (c) #economy paragraph 3 reads only the deleted lines; delete whole
    ("alaska.html",
     "<p>Each line points at different property types. The government count is the one a project in Juneau, or one leasing to agencies in Anchorage or Fairbanks, cites for its tenant base. The construction count is both a demand signal for builders' supply yards and the labor pool a project's own contractor hires from, so a schedule for a 2027 start is written with it in view. The manufacturing line takes in seafood processing along with other plants, and a processing or industrial study looks past the statewide change to the employer and the borough before using it.</p>\n",
     ""),
    # (d) FAQ 1 last sentence (76.8 thousand government jobs)
    ("alaska.html",
     " BLS counted 76.8 thousand government jobs in Alaska in September 2026, a preliminary figure 3.0% under its count of twelve months earlier [^5].\"",
     "\""),
    # (e) N9 NON-DELETION (A1-2 consequence, A1-13c): #kodiak paragraph 2 pointed at the deleted manufacturing line and made an uncited seafood claim
    ("alaska.html",
     "The statewide manufacturing line in the payroll section takes in seafood processing, but it is not broken out by borough, and a processing, cold-storage or harbor-side project on Kodiak cannot borrow it as a local trend. The study builds its case from",
     "A study for a processing, cold-storage or harbor-side project on Kodiak builds its case from"),

    # ---- A1-6 (I60(b), D21): comparison in words with one value hidden. Source 13 stays cited (460,000).
    ("alaska.html",
     " The airport system's own report, as relayed in October 2026, prints a different cargo figure for 2025 [^13]; a study cites one, with its publisher, and does not present the two as separate years or places.",
     ""),

    # ---- A1-8: "built by separate methods" has no research row
    ("alaska.html",
     "The Census and state figures are separate estimates built by separate methods, and this page uses",
     "The Census and state figures are separate estimates, and this page uses"),

    # ---- A1-9: the Anchorage row left the table with the $1,579 recast
    ("alaska.html",
     "which the table below sets out for Anchorage, Juneau, the Kenai Peninsula and the Mat-Su [^6]",
     "which the table below sets out for Juneau, the Kenai Peninsula and the Mat-Su [^6]"),

    # ---- A2-6 N1 NON-DELETION: #population h2 is landed Colorado's "<State>'s 2025 count: ... on one side ... on the other"
    ("alaska.html",
     "data-h2=\"Alaska's 2025 estimate: a small gain, natural increase on one side and out-migration on the other.\"",
     "data-h2=\"The state demographer's July 1, 2025 estimate, and the Census Bureau's separate one.\""),

    # ---- A2-7 N2 NON-DELETION: #capital lede shares Colorado's skeleton and its tail "the program rules, which are national"
    ("alaska.html",
     "SBA's fiscal 2025 results for its Alaska district, USDA Rural Development's Alaska announcements, FDIC deposit totals, CDFI awards and the totals of the Alaska Industrial Development and Export Authority's loan programs were not found on dated primary pages. An Alaska feasibility study company works from what is dated, set out below, and from the program rules, which are national.",
     "Not found on dated primary pages were SBA's fiscal 2025 results for its Alaska district, USDA Rural Development's Alaska announcements, FDIC deposit totals, CDFI awards and the totals of the Alaska Industrial Development and Export Authority's loan programs. An Alaska feasibility study company works from what is dated, set out below."),

    # ---- A2-8 second move: the BED interpretive sentence is uncited and echoes Wyoming's "churn ... is the point for an operator's budget"
    ("alaska.html",
     " For a start-up borrower the gains and losses are the more useful pair: they show that openings and closings both run in the thousands of jobs within a single quarter, which is the setting a new business's survival assumptions have to fit.",
     ""),

    # ---- A2-9: rules closing sentence is landed Northern Virginia's "confirms the governing jurisdiction ... before reading a single figure"
    ("alaska.html",
     " An Alaska feasibility study therefore names the government whose code governs the parcel before it states any rule.",
     ""),

    # ---- A2-10: cases paragraph is Colorado's frame ("full models in other states", same structure with this page's inputs) plus ND's "inputs do not"
    ("alaska.html",
     " Their structure carries over to Alaska; their inputs do not. Here the payroll line comes from the borough wage in the costs section, the energy line from a utility's written quote, the season from the cruise and airport counts, and the downside case from the state forecast the first section prints.",
     ""),

    # ---- A2-11: FAQ 2 question tail ", and for which programs?" is landed Denver FAQ 7's tail; the answer still names the programs
    ("alaska.html",
     "\"q\": \"What should a first message to Feasibility Study Company about an Alaska project say, and for which programs?\"",
     "\"q\": \"What should a first message to Feasibility Study Company about an Alaska project say?\""),

    # ---- A2-12 N3 / N4 / N5 NON-DELETION: headings that repeat landed or sibling headings
    ("alaska.html",
     "data-h2=\"The dates behind an Alaska credit file, January 2025 to October 2026.\"",
     "data-h2=\"Storm declarations, Pikka's first oil, Alaska LNG and the cruise limits, dated January 2025 to October 2026.\""),
    ("alaska.html",
     "data-h2=\"Labor that BLS prices, natural gas a utility says may run short, and building costs no public index prints.\"",
     "data-h2=\"Labor that BLS prices, natural gas a utility says may run short, and building costs that rest on a contractor's bid.\""),
    ("alaska.html",
     "data-h2=\"The property types Alaska's records on this page bear on.\"",
     "data-h2=\"Asset class pages behind Alaska's visitor, housing and care records.\""),

    # ---- A2-13 (ii): "a study in most states would not" is an uncited comparison with other states (pure deletion)
    ("alaska.html",
     "An Alaska feasibility study consultant starts somewhere a study in most states would not, with the Department of Revenue's oil forecast.",
     "An Alaska feasibility study consultant starts with the Department of Revenue's oil forecast."),
    # ---- A2-13 (i) N6 NON-DELETION: "two readers ... the lender who has to approve" is landed Virginia's / ND's / Vermont's firm sentence
    ("alaska.html",
     "and each one is written for two readers at once: the owner or developer who proposes the project and the lender who has to approve it.",
     "and each is prepared for the owner or developer who proposes the project and for the lender reviewing the request."),

    # ---- A2-14 N7 NON-DELETION (no figure added): SBA 504 equity omits the new-and-special tier (sba.json sba_504_new_and_special)
    ("alaska.html",
     "if the borrower's business is new or its building is special-purpose [^52].",
     "if the borrower's business is new or its building is special-purpose, and more when it is both [^52]."),

    # ---- A2-15: three "most" claims with no research row
    ("alaska.html",
     " In Alaska a lender asks for one most often where the cash flow has not been earned yet: a new lodge sized for the cruise season, a start-up processor, a clinic in a borough without a comparable.",
     ""),
    ("alaska.html",
     "<p>Banks finance most stabilized Alaska property. The department's tables",
     "<p>The department's tables"),
    ("alaska.html",
     "<p>Air and sea traffic are the visitor and freight records Alaska publishes most often, and 2025 and 2026 set records in both. Nearly 460,000",
     "<p>Nearly 460,000"),

    # ---- A2-16: other plain claims with no source
    ("alaska.html",
     "<p>Price is the line that moves first. Alaska North Slope crude",
     "<p>Alaska North Slope crude"),
    ("alaska.html",
     ", with freight and the building season stated as their own lines, since materials reach many Alaska sites by air, by barge or over a long road haul.",
     ", with freight and the building season stated as their own lines."),
    ("alaska.html",
     "and state spending reaches payrolls and contracts in every borough.",
     "and state spending reaches payrolls and contracts."),
    ("alaska.html",
     " A borrower whose bank leans on either guarantee has it named in the term sheet, and the study's sources and uses shows the guaranteed share as the lender structures it.",
     ""),
    ("alaska.html",
     " A loan that leans on either one names it in the term sheet, and the study's sources-and-uses table shows the guaranteed share as the lender structures it.",
     ""),
    ("alaska.html",
     "The cargo airport, the largest payroll and a city government pushing housing permits.",
     "The cargo airport and a city government pushing housing permits."),

    # ---- A2-19 N8 NON-DELETION: the closing band's "that program" has no antecedent
    ("alaska.html",
     "what that program expects to receive, and what comes after.",
     "what the lender's program expects to receive, and what comes after."),

    # ---- A2-20: research-process failures printed as content
    ("alaska.html",
     "were not found, because the borough's site refused the connection, and neither were hotel performance figures",
     "were not found, and neither were hotel performance figures"),
    ("alaska.html",
     "lists the area without an unemployment rate, BLS's Juneau metro page returned an error, and building permits",
     "lists the area without an unemployment rate, and building permits"),
    ("alaska.html",
     "were not found, and the regional development district's site returned an error.",
     "were not found."),
]

# ---------------------------------------------------------------------------------------------
# NOT APPLIED. The verifier could not reproduce these three attacker findings because the source
# hosts are unreachable from the verifier's session (getaddrinfo ENOTFOUND: aksbdc.org, www.bls.gov,
# tax.alaska.gov are outside the session's allowed domains). Verdict REFUTED by default. If the
# coordinator re-checks the attacker's WebFetch reading elsewhere and it holds, these are pure
# deletions that cost one counted figure (A1-3) or none (A1-4, A1-5):
UNREPRODUCED_IF_CONFIRMED_ELSEWHERE = [
    # A1-3 (102.0 million, label "unrestricted mining revenue"): delete the sentence and the table row
    ("alaska.html",
     " Mining adds its own line, with unrestricted mining revenue forecast at 102.0 million dollars for fiscal 2027 [^1].",
     ""),
    ("alaska.html",
     "<tr><td>Unrestricted mining revenue, forecast</td><td>102.0 million dollars</td><td>Fiscal 2027</td><td>[^1]</td></tr>\n",
     ""),
    # A1-4 ("from 2022" not on aksbdc.org/ssbci): FAQ 5 and #capital
    ("alaska.html",
     "part of a 10-year program from 2022, and $83.1M",
     "part of a 10-year program, and $83.1M"),
    ("alaska.html",
     "within a 10-year program from 2022, and the Alaska SSBCI Tribal Consortium",
     "within a 10-year program, and the Alaska SSBCI Tribal Consortium"),
    # A1-5 (BLS county release lists Ketchikan and Kodiak): Ketchikan clause and Kodiak clause
    ("alaska.html",
     "BLS's quarterly county release does not include the borough among its selected areas, and the department's area rental figures",
     "and the department's area rental figures"),
    ("alaska.html",
     "nor were employment and wage rows for the borough or hotel, permit and airport figures.",
     "nor were hotel, permit and airport figures."),
]
