# CASE-NEW-1 c1 freeze 1: attacker 2 (sameness, sourcing, subjects, the owner's rules)

Scope: the six c1 cases in `N/copies/c1/` at freeze 1 (HEAD 752d0af, gates 13/14). I worked separately and edited nothing. Scratch tools and outputs are in `N/reviews-c1/a2-work/`:
- `pagecheck.json` and `pagecheck.txt`: `scripts/qa/pagecheck.py --stage ready --new <six> --figures --overlap 5`, run inside the copy. It gives the counted lists I attack below.
- `audit.py`: for each source entry, finds the research rows with the same URL, then checks publisher, title (verbatim) and date. It also checks every number in a cited block, outside markers, against the cited rows.
- `collide2.py`: scale-aware search (thousand, million) for every counted value on every other case page and on unranked pages, sources lists included.
- `same.py` / `same.json`: 8-word runs, digits dropped and marker text stripped, between each page and every served page.
- `ctx.py`, `figctx.py`, `section.py`: context printers.

Cases: CHE = industrial-warehouse-chesapeake-virginia-sba, EVT = event-venue-jackson-wyoming-sba, BRW = brewery-fargo-north-dakota-sba, CLD = cold-storage-anchorage-alaska-sba, AUT = auto-dealership-sioux-falls-south-dakota-sba, MIX = mixed-use-colorado-springs-colorado-sba. Line numbers refer to `src/pages/case-studies/<slug>.html` unless noted.

## What came out clean (reproduced)

These checks found nothing:
- **Source titles.** Every research-sourced entry's title, publisher and URL equals a research row for that URL (audit.py: 0 TITLE-DIFF on 6 pages). Rule and register entries match the Lebanon exemplar's.
- **Figure support.** Every number in a cited block outside markers is carried by a cited row. The only exceptions are the hand-typed register values in A2-4 to A2-7, and those values do equal the register.
- **Denver and Northern Virginia.** No value from a Denver or Northern Virginia row is printed. Two shared release URLs (BLS QCEW for Virginia and for Colorado) are cited, but only for Hampton Roads and El Paso rows.
- **Banned names and the owner's other properties.** The ruling 9 pattern returns 0 hits in the page, case.json and card of each case. No other property of the owner is named or linked.
- **Dashes.** There are 0 em or en dashes in any encoding in those files.
- **Dates.** Every source has `"published": "DEPLOY"`, `"updated": "DEPLOY"` and `"data_as_of": "2026-11"`.
- **SBA wording.** No page says SBA requires a study. Every page quotes 120.160(b) "may require".
- **Subjects.** All six subjects are generic. The private do-not-use lists give no real hits: the only matches are digits, and "Matan" inside "Matanuska". The Sioux Falls corridor is placed by a nocount, unnamed permit.
- **Competitor census (OWNER RULING clause 2).** All six make the named census a lender condition and carry a County Business Patterns supply table through `mkt:` markers, with source lines and links. They state the fit grade: proxy for CHE, EVT and MIX, exact for BRW and CLD (cold storage), partial for AUT. No page invents or names a competitor.
- **Links.** Every page links its hub, its state and `/practice-areas/sba-7a-504/` in prose, with pending markup where the target is unbuilt.
- **CTA placement.** Every page has a `/#contact` CTA in the opening and another in the dscr section after the determination.
- **Cross-page collisions.** collide2.py finds no counted value that pagecheck missed, scaled or exact, on another case page or on an unranked page.

## BLOCKER

**A2-1. BLOCKER. AUT. A model input typed by hand.**
- **Quote.** FAQ question, L43: "Why does a 10% equity proposal fail?"
- **Reproduction.** The value is the sponsor's proposed equity. It is a model input (`v.equity_proposed_pct` = 10.0% in the engine) typed outside any marker. FAQ items cannot carry `{{case:}}`.
- **Fix.** Use words: "Why does a minimum-equity proposal fail?"

## MAJOR-FACTUAL

**A2-2. MAJOR-FACTUAL. BRW. Three facts counted twice.**
- **Quote.** "the county's real output reached $14,875,063 thousand in chained 2017 dollars in 2024" (L257) and the table cell "14,875,063" (L283). "20,535.575" (L284) and "20,535.575 million dollars for 2023" (L295). "65,268.3" (L286) and "65,268.3 million in chained 2017 dollars" (L295).
- **Reproduction.** pagecheck's research list holds both forms of each value. The $ form and the scale word give different keys, so ruling 5's rescaled-repeat test misses them. Research falls from 34 to 31.
- **Fix.** None on the page. Record the count as 3 fewer. Optionally drop the scale word or the $ so that one form prints.

**A2-3. MAJOR-FACTUAL. MIX. One fact counted twice.**
- **Quote.** "The metro's economic output was $53,092.641 million in 2023" (L322) and the table cell "53,092.641" (L315).
- **Reproduction.** Both forms are in pagecheck's research list. Research falls from 42 to 41.
- **Fix.** As A2-2.

**A2-4. MAJOR-FACTUAL. EVT. Register values typed by hand outside `mkt:` markers, and counted as research.**
- **Quote.** "Teton County has 6.89 establishments per 10,000 residents in the proxy class, against 2.4 for Wyoming as a whole [3]" (L349). Also "The county's median home value is $1,633,900 [^2]" (risks, L444), and "16" in "81 paid employees across those 16 establishments".
- **Reproduction.** audit.py strips `mkt:` regions and the values remain. The register holds `cbp_estab_per_10k` co-56039 = 6.89, wy = 2.4, `cbp_estab` = 16 and `acs5_median_home_value` = 1633900. "6.89" sits in pagecheck's research list. Hand-typed register values bypass `markets.py --check` and BRIEF-REPO's (b).
- **Fix.** Wrap each value in its `mkt:` marker. Counted stays 35, as research 31 and register 4.

**A2-5. MAJOR-FACTUAL. BRW. Register values typed by hand.**
- **Quote.** "at least four establishments and 90 paid employees in the county, and at least five establishments and 101 employees in the metro area [5]" (L329). Also "two 504 loans ... totaling $1,126,000 [26]" (L330).
- **Reproduction.** The register holds `cbp_emp` cbsa-22020 = [101, flag], co-38017 = [90, flag], `sba504_volume` nd = 1,126,000. "101" is counted as research.
- **Fix.** Use `mkt:` markers, with `allow_flag` on the flagged cells. Research falls by 1 and register rises by 1.

**A2-6. MAJOR-FACTUAL. AUT. Register values typed by hand.**
- **Quote.** FAQ, L40: "3.02 against 3.43 per 10,000 residents [^22]".
- **Reproduction.** The register holds `cbp_estab_per_10k` auto-dealership cbsa-43620 = 3.02 and sd = 3.43. Both are in pagecheck's research list. Register is already at its cap of 10, so counted falls from 54 to 52.
- **Fix.** State the comparison in words, or move it out of the FAQ into marked prose.

**A2-7. MAJOR-FACTUAL. MIX. Register values typed by hand.**
- **Quote.** "The county holds 97,958 renter-occupied homes among its 742,999 residents [28] ... The census median gross rent of $1,696" (L365).
- **Reproduction.** These are ACS register values for co-08041: renter-occupied 97958, pop 742999, median gross rent 1696. All three sit in the research list, and their marked table copies then lose to `own.has`.
- **Fix.** Use `mkt:` markers. Research becomes 38 and register 9, so counted is unchanged.

**A2-8. MAJOR-FACTUAL. CLD. A single-project figure counted (I64).**
- **Quote.** "The pipeline project now under discussion would need a peak workforce of about 6,600 workers for construction alone [^16]" (L286, repeated at L424).
- **Reproduction.** Research row ST-ALASKA #35 reads "Peak construction demand for the Alaska LNG Project alone": one named project's attribute. "6,600" is in pagecheck's research list.
- **Fix.** Wrap it in `data-fsc-nocount`. Research falls by 1.

**A2-9. MAJOR-FACTUAL. CHE. A single facility's capacity counted (I64).**
- **Quote.** "a throughput capacity of 5.8 million TEUs once its North Berth work is complete [^15]" (L218).
- **Reproduction.** Research row ST-VIRGINIA #68 is "Capacity, not volume". It is the planned size of one named port after one project. The same paragraph calls its siblings "single projects and capacity statements, not volumes handled", yet this one is counted.
- **Fix.** Wrap it in `data-fsc-nocount`. Research falls by 1.

**A2-10. MAJOR-FACTUAL. CLD. A false statement about two figures.**
- **Quote.** L275: "the gap between them is smaller than the rounding in either".
- **Reproduction.** The two figures are 3.82 million tonnes [8] and more than 3.85 million metric tons [9]. Their gap is at least 0.03 million. The rounding of a two-decimal million figure is 0.005 million, so the gap is about six times the rounding.
- **Fix.** Delete the clause.

**A2-11. MAJOR-FACTUAL. BRW. SBA tiers typed by hand.**
- **Quote.** L382: "it changes the minimum between 15% and 20%".
- **Reproduction.** These are equity tiers outside `sba:` markers. The same page renders them through markers elsewhere.
- **Fix.** Use `<!--sba:equity...-->` markers or words ("between the new-business tier and the special purpose tier").

## MAJOR-NONFACTUAL

The pages pass gate 4: maximum overlap is 10.92%. I115, however, blocks any shared run of 8 or more words outside marker text, and any shared hero plan, description frame or CTA move. The runs below are from `same.json`. Most come from the Lebanon exemplar and are also on landed factory cases (Lebanon, urgent-care Elizabethtown, gas-station Texas, Sevierville, Port Charlotte). Rewriting the six pages in their own words fixes them. The landed pages are reported, not failed.

**A2-12. MAJOR-NONFACTUAL. All six. Shared hero plan.**
- **Quote.** CHE: "An SBA 504 loan at [m] equity covers Year 2 debt service only [m]; the model supports it at [m] equity." BRW and CLD carry the same sentence. EVT reads "... and the model supports it at ...". AUT reads "... the model supports it at [m], at the floor". MIX reads "but at [m] equity Year 2 coverage is only [m]; the model supports the loan at [m] equity".
- **Reproduction.** All six use the same plan: a market figure, a contrast, the proposed coverage shortfall, then the supported equity. Lebanon, Sevierville and Elizabethtown heroes share it.
- **Fix.** Give each hero its own move, for example leading with the binding constraint the case found.

**A2-13. MAJOR-NONFACTUAL. All six. Shared description frame.**
- **Quote.** AUT: "Auto dealership feasibility study case for an SBA 504 loan in Sioux Falls, South Dakota: metro demand, dealer supply counts, a priced build and the coverage test." MIX: "Mixed-use feasibility study case for an SBA 504 loan in Colorado Springs, Colorado: ...". CHE: "Industrial warehouse feasibility study for an SBA 504 loan in Chesapeake, Virginia: ... the supply count and the coverage test." BRW, EVT and CLD end in the same closing slot: "supply count, coverage ...", "supply and coverage", "the supply count and an SBA 504 test".
- **Reproduction.** The frame "[asset] feasibility study case for an SBA [program] [loan] in [town, state]: [list] and coverage" is also used by Lebanon, Sevierville, Elizabethtown and Port Charlotte. I115 rewrote Pennsylvania's description for exactly this.
- **Fix.** A description pass per page.

**A2-14. MAJOR-NONFACTUAL. CHE, BRW, AUT, MIX. Shared opening frame.**
- **Quote.** CHE L195, a 43-word run with Lebanon, Port Charlotte and Elizabethtown: "A study joins a dated market read, a census of competitors, a priced build and a coverage test that shows how much debt a project can carry. This page runs that work on one hypothetical project". BRW L249, AUT L243 and MIX L287 vary one phrase.
- **Reproduction.** same.json.
- **Fix.** Keep only the mandated sentence ("Feasibility Study Company prepares ... for owners, developers and their lenders") and rewrite the rest.

**A2-15. MAJOR-NONFACTUAL. All six. Shared subject-paragraph frame.**
- **Quote.** "Every market figure is public and dated. Every model figure is computed by the case engine from the inputs listed near the end, and each input carries a source or the word assumption. The project belongs to our ... practice, the town sits in ..., and the program rules are laid out on our SBA 7(a) and 504 page."
- **Reproduction.** The run is 38 words. It appears at CHE L196, EVT L246, BRW L250, CLD L238, AUT L244 and MIX L288, and on Lebanon, Port Charlotte, gas-station Texas and Elizabethtown.
- **Fix.** Rewrite per page.

**A2-16. MAJOR-NONFACTUAL. All six. Shared loan and determination frames.**
- **Quote.** These sentences recur:
  - "An SBA 504 project is split three ways ... the rules in force from" (CHE L302, EVT L399, BRW L381, CLD L376, AUT L395).
  - "follows the larger asset class; land, building and site work are the majority of proceeds here, so the model uses a 25-year debenture and a 25-year bank amortization" (CHE, EVT, CLD; 29 words).
  - "As proposed it fails two tests. Restructured it passes the Year 2 test." (EVT L412, BRW L395, CLD L389, AUT L408).
  - "the engine raises the contribution to the tier and then to the share at which Year 2 coverage meets the floor" (CHE, EVT, BRW, CLD, AUT).
  - "The 504 split fixes the bank at half of cost, so extra equity displaces the debenture, the program's longest and cheapest money. The deal clears the floor by a hair in the test year, so a lender should treat it as the upper bound and not a target." (CHE L321, EVT L418, CLD L395; 47 words).
  - MIX shares "as proposed it fails the coverage test, restructured it" and the fee sentence ("the upfront fee is added to project cost and moves with the debenture").
- **Reproduction.** same.json.
- **Fix.** Rewrite per page. The tables already carry the arithmetic.

**A2-17. MAJOR-NONFACTUAL. All six. Shared CTA move.**
- **Quote.** After the determination, at CHE L322, EVT L419 and CLD L396, a 45-word run with Lebanon: "There are three ways to reach such a structure. The sponsor can bring the cash. The sponsor can lease ... which removes land and construction from the budget; this case does not model a lease. Or the sponsor can show ... What does not work is the original request. Contact Feasibility Study Company to test your project against the coverage floor before a lender does. We show the lender the work; we do not predict what the lender will decide." The closing band repeats on all six: "Planning a ...? Test the site against the debt before you sign. Feasibility Study Company builds the market read, the supply count and the coverage test from dated public records for owners, developers and their lenders." CHE, CLD and MIX carry the same 24-word p verbatim (CHE L66, CLD L66, MIX L74).
- **Reproduction.** same.json, and the front matter `cta`.
- **Fix.** Write each CTA from the case's own finding.

**A2-18. MAJOR-NONFACTUAL. All six. Shared sensitivity, inputs and lender-condition frames.**
- **Quote.** These recur:
  - "rows move ... up and down by up to a fifth in every year, and columns move the ... across the range in the headers. The table reads Year 2, the test year, on the restructured loan, and its range runs from" (EVT L431, BRW L414, AUT L428, CLD).
  - "every input and whether a source or an assumption sets it" (all six).
  - "Each condition below closes a gap the public record left open. Several group related items the research reported as not found." (CHE L356, EVT L454, BRW L433, CLD L430, AUT L454).
  - Condition items shared with Lebanon: "the parcel identifier from the county assessor, a written zoning determination", "a state count station and annual average daily traffic for the corridor", "the electric, gas, water and sewer providers for the parcel", "The rural, HUBZone and Opportunity Zone status of the tract were not found and should be checked if any incentive is part of the plan" (AUT, 25 words) and "A funded reserve for the Year 1 shortfall between operating income and debt service, held until the stabilized year is reached" (EVT, AUT; 20 words).
- **Reproduction.** same.json.
- **Fix.** Rewrite per page.

**A2-19. MAJOR-NONFACTUAL. CHE, BRW, CLD, AUT, MIX. FAQ answers not unique (ruling 4).**
- **Quote.** These answer frames recur:
  - "SBA does not require one in every case. The rule says that" (CHE L56, BRW L52, CLD L56, AUT L52, Lebanon, Elizabethtown).
  - "... a lender may ask for one anyway, and a study that builds the supply count and the coverage test puts that work in the lender's hands up front" (CLD, AUT, CHE, MIX).
  - "What could stop the project before any loan question arises? Site facts the research could not find: the parcel's zoning" (CHE L59, BRW L55, AUT L59, MIX L63, and four landed cases).
  - "Why does the restructured loan need so much more equity than the program minimum? Because the minimum is a floor ... cannot carry a loan sized to the minimum, so the engine raises" (CHE, BRW, AUT, MIX).
- **Reproduction.** Front matter `faq`, and same.json.
- **Fix.** Write new answers, and drop the repeated questions where the page has nothing of its own to say.

**A2-20. MAJOR-NONFACTUAL. CHE and CLD. Sibling copying.**
- **Quote.** Two sentences are shared between the pages:
  - CHE L256: "Rows are confirmed by the register's County Business Patterns series, not by any competitor's own site." CLD carries the same 17-word run.
  - CHE L244: "lessors of nonresidential buildings are the nearest industries to industrial property, and no code isolates it". CLD carries the same 16 words. Both paraphrase the `naics-map.json` reason text.
  - Both pages also share "a local wage survey for warehouse and driver".
- **Reproduction.** same.json shows these runs only between the two siblings.
- **Fix.** Rewrite on one of the two pages.

**A2-21. MAJOR-NONFACTUAL. BRW and AUT. Meta description over 160 characters (ruling 16, BRIEF-REPO 140 to 160).**
- **Quote.** BRW L6, 161 characters: "Brewery feasibility study case for a Fargo, North Dakota taproom and production brewery on an SBA 504 loan: jobs, supply count, coverage and the equity it takes." AUT L6, 162 characters.
- **Reproduction.** Python `len` of the front-matter `description`.
- **Fix.** Cut 2 or 3 characters. Do it in the A2-13 rewrite.

**A2-22. MAJOR-NONFACTUAL. AUT. The first screen carries no counted figure (ruling 16).**
- **Quote.** L9: "Sioux Falls added more than 5,000 residents in 2025 [^1] and Minnehaha County's September 2026 unemployment rate was 1.6% [^9]".
- **Reproduction.** Neither 5,000 nor 1.6% is in pagecheck's research list. Both are printed on other case pages, including siblings CLD, EVT and MIX for 1.6%.
- **Fix.** Lead with a counted value. Two candidates: 224,676 residents at the end of 2025 [^1], or 754,686 enplanements.

**A2-23. MAJOR-NONFACTUAL. CHE. The corridor is not named (ruling 7).**
- **Quote.** case.json L458, the glance: "on a southern Chesapeake industrial corridor with highway access [^3]". The site section at L263 and L265 has the same.
- **Reproduction.** The other five name a corridor: US-26/89/191, I-29, the Ted Stevens airport area, 57th Street and Veterans Parkway, and Nevada Avenue. CHE names none.
- **Fix.** Name the corridor, or state that the research names none and make it a lender condition.

**A2-24. MAJOR-NONFACTUAL. MIX. A street name is linked to a state page.**
- **Quote.** The rendered page: "along the <a href="/states/nevada/" data-fsc-term="state-nevada">Nevada</a> Avenue corridor".
- **Reproduction.** The `mesh.py` first-mention term linker made the link. It points a Colorado Springs street at the Nevada state page, and gives Nevada a false contextual inbound link.
- **Fix.** Reword, or have the integrator add a mesh exception for "Nevada Avenue". Then rebuild and rerun gate 9.

## MINOR

**A2-25. MINOR. All six. Buyer-intent phrasing missing from meta and closing CTA.**
- **Quote.** The meta names neither "consultant" nor "company" on CHE, BRW, AUT and MIX. The closing CTA band does not name it on CHE, EVT, BRW, CLD and MIX; only AUT's does.
- **Reproduction.** intent.py output.
- **Fix.** Add the phrase in the A2-13 and A2-17 rewrites.

**A2-26. MINOR. All six. The FAQ claims a reserved query.**
- **Quote.** "Does SBA require a feasibility study for a [warehouse/venue/brewery/cold storage/dealership] loan?"
- **Reproduction.** The question is emitted as FAQPage schema. Ruling 16 gives that query to `/research-notes/sba-feasibility-myth/` alone, and none of the six links that note (0 links).
- **Fix.** Link the note in each answer, or rephrase the question.

**A2-27. MINOR. MIX. A service promise (WRITER: no service promise unless a record states it).**
- **Quote.** L68: "Use the contact form to describe your building, and we will tell you what a study for it would cover."
- **Fix.** Delete "and we will tell you what a study for it would cover".

**A2-28. MINOR. CLD. One fact counted twice.**
- **Quote.** "3.82 million tonnes" [8] and "More than 3.85 million metric tons" [9] (L259).
- **Reproduction.** Both are counted. The page itself presents them as two accounts of one 2025 total.
- **Fix.** Put the second in nocount.

**A2-29. MINOR. CLD. Two counted values that are not market figures.**
- **Quote.** The register zero `co-02020.cbp_estab=0`. Also L380: "a state allocation of $54M to loan guarantees". The second is a program allocation, a rule-type value, and its row is dated by a "page last modified" stamp, so attacker 1 should check its date basis.
- **Fix.** Put both in nocount.

**A2-30. MINOR. CLD. One facility's announced investment is not in nocount (I64).**
- **Quote.** L267: "Planned near-term military investment at JBER: About $2 billion". Also "about 2,700 new personnel and families".
- **Reproduction.** Neither value is counted, but both are one named base's figures.
- **Fix.** Wrap both in `data-fsc-nocount`.

**A2-31. MINOR. BRW. Internal process language on a public page.**
- **Quote.** L308: "the repository's rules forbid naming a business no research row names".
- **Fix.** "the study names no business that no dated public document names".

**A2-32. MINOR. CHE. A statement cited to a source that does not carry it.**
- **Quote.** The glance row cites [3], the QCEW county release, for "on a southern Chesapeake industrial corridor with highway access".
- **Fix.** Drop the citation from the corridor clause. See A2-23.

**A2-33. MINOR. EVT, BRW, CLD, AUT, MIX. Shared card frame.**
- **Quote.** The five cards repeat Lebanon's: "the 504 structure reaches {dscr_y2} in Year 2 only at {equity_pct} equity, with a {debenture} debenture on a {tpc} project".
- **Reproduction.** The card renders inside a `case:` marker, so I115 does not reach it.
- **Fix.** Vary the cards at the integrator's discretion.

## Counted figures after my confirmed findings (A2-2 to A2-9; READY floors 30 counted, 20 research)

| Case | Gate 3 | After confirmed findings | If the minors A2-28 and A2-29 are also upheld |
|---|---|---|---|
| CHE | 36 (28 research, 8 register) | 35 (27, 8) | 35 (27, 8) |
| EVT | 35 (32, 3) | 35 (31, 4) | 35 (31, 4) |
| BRW | 35 (34, 1) | 32 (30, 2) | 32 (30, 2) |
| CLD | 35 (31, 4) | 34 (30, 4) | 31 (28, 3) |
| AUT | 54 (44, 10 of 16) | 52 (42, 10) | 52 (42, 10) |
| MIX | 48 (42, 6) | 47 (38, 9) | 47 (38, 9) |

All six stay at or above both READY floors. BRW and CLD have the least margin.
