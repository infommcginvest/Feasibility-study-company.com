# CASE-NEW-1 tranche c1: verifier and fixer record (freeze 1 findings)

Frozen copy: N/copies/c1/. Rebuilt and gated copy: N/copies/c1f2/ (gates N/copies/GATES-c1-f2.txt). Fixes were made only in N/cases/<slug>/ (page.html, case.json, card.json); originals are kept in N/cases-orig/<slug>/ and the fix scripts in N/fixes/. Method: each finding was re-opened against the frozen page source, case.json, the engine (`casemodel.py --case`), the research rows and `sba.json`. Default REFUTED until reproduced. No finding was refuted outright; where a finding is partly an accounting note it is marked CONFIRMED (no text change).

## Attacker 1

| Id | Verdict | Reproduction | Fix applied |
|---|---|---|---|
| A1-1 | CONFIRMED BLOCKER | Writer's first-draft `work/out.json` (18,000 sq ft, 8 bays, 21 FTE, 680 vehicles, land $1.4M, 3.0 acres, Prime + 0.5) fails at every equity share; frozen inputs (14,000 sq ft, 6 bays, 18 FTE, 740 vehicles, Prime + 0.25) reach 1.15x at 15.5%. No input gained a source in between; notes.md says the store was resized after the failed draft. | Inputs replaced by the pre-run reasoned store: 18,000 sq ft, 8 bays, land $1.4M, 3.0 acres, 15/19/21/22/22 FTE (staffing set against the register's mid-twenties employees per establishment), vehicles 405/590/680/725/745 (about 13 a week at stabilization, the draft's Year 3 level), bank rate Prime + 0.5. Reran: proposed 10% gives 0.45x; restructured stays at 15.0% (the bank's half of cost alone costs more than Year 2 NOI) and gives 0.48x in Year 2, 0.75x in Year 3. Determination is NEGATIVE (the model does not support the loan at any equity share). Hero, FAQ, market conclusion, loan, dscr, break-even, sensitivity, risks, glance, card and page prose rewritten to the engine result; the page states that inputs were set before the run and not adjusted. |
| A1-2 | CONFIRMED BLOCKER | Rendered inputs table: land 2.0 acres vs "two and a half", barrels 1,800/2,700/3,200/3,500/3,700 vs "1,800 in Year 3 and 2,050 by Year 5", production FTE 4/5/5/5.5/5.5 vs "4 by Year 3", taproom FTE 7/9/10/10/10 vs "nine by Year 3". | The four reasoning strings reworded without numbers; the table text now equals the model values. |
| A1-3 | CONFIRMED | `v.in_*` arrays render the Year 3 element (3,200; 5.0; 10.0). | "reaches ... barrels in Year 3, the stabilized level"; FTE "in Year 3". |
| A1-4 | CONFIRMED | MT-NORTH-DAKOTA rows 33 and 34 call them a September record and a June record. | Research wording used. |
| A1-5 | CONFIRMED | sba.json `terms.sba_504_maturities.note`: with both asset classes the maturity follows the majority of proceeds. | Sentence deleted from the debenture_years reasoning. |
| A1-6 | CONFIRMED | "between 15% and 20%" typed outside sba markers. | Both tiers now in `sba:` markers. |
| A1-7 | CONFIRMED (register values typed; scaled repeats) | 90, 101, 2 loans and $1,126,000 equal register cells; the three rescaled pairs print twice. | The four values wrapped in `mkt:` markers. Rescaled pairs left as printed; true research count is 3 lower than the gate's (see counts). |
| A1-8 | CONFIRMED | 4,143 minus 2,668 is 1,475, not 2,174; rows ST-WYOMING-2 12 and 13 vs ST-WYOMING 33. | Net figure described as the all-establishment net change. |
| A1-9 | CONFIRMED | 6.89, 2.4, 81, 16, $1,633,900 equal register cells, typed outside markers. | `mkt:` markers (proxy fit). |
| A1-10 | CONFIRMED | Chesapeake engine grid (Year 3): margin -10%/+10% gives 0.72x/2.44x; accounts -10%/+10% gives 0.73x/2.42x. | Sentence and its dependent sentence replaced with the engine reading; the risk item no longer claims margin is sharper. |
| A1-11 | CONFIRMED | 3.02/3.43 and 6/12 loans equal register cells. | FAQ numbers removed (words); the page already carries the table via markers. |
| A1-12 | CONFIRMED | 97,958, 742,999, $1,696 equal co-08041 register cells. | `mkt:` markers. |
| A1-13 | CONFIRMED | Table renders 137 and 550. | Markers replace "just over a hundred ... five hundred". |
| A1-14 | CONFIRMED | $1,255,499 / $95,000 = 13.2 jobs against 8 warehouse FTE and 2 drivers. | "light test" claim deleted. |
| A1-15 | CONFIRMED | $450,000 / Year 2 operating cost $2,011,864 = 2.7 months. | "four months" removed from the reasoning. |
| A1-16 | CONFIRMED (count only) | Two accounts of the same 2025 air cargo total. | Second figure in nocount. |
| A1-17 | CONFIRMED MINOR, partly fixed | Typed 25-year terms, uses labels with acres and sq ft, FAQ "10%". | Labels reduced to "Land" and "Building"; 25-year wording turned into words; FAQ question reworded. |
| A1-18 | CONFIRMED | `prop_tests` fail the equity tier in Jackson, Fargo and Anchorage, glances named coverage only. | Determination rows rewritten ("fails the equity tier and the floor test ... meets both"). |
| A1-19 | CONFIRMED | Accounts rise 470, 495, 510; NOI does not turn on account growth ending. | Clause deleted. |
| A1-20 | CONFIRMED | 6.5% debenture is below every sibling; probe shows 6.97% gives 42.6%. | Fixed-rate clause deleted; kept as a labelled round planning rate (not changed, to avoid tuning). |
| A1-21 | CONFIRMED | Row 57 overnight visitors vs row 58 visitors. | Reworded as two separate reports. |
| A1-22 | CONFIRMED | Source is an appraisal firm; 41.6 thousand is statewide. | Reworded. |
| A1-23 | CONFIRMED | MT-COLORADO row 99, single project amounts. | nocount moved onto the amounts. |
| A1-24 | CONFIRMED MINOR, left | True writer arithmetic in assumption text. Colorado Springs "$130 a sq ft" and "14% below" removed; Sioux Falls "$205 a sq ft" (321,594 / 1,572) kept as a labelled reasoning remark. | Partly. |

## Attacker 2

| Id | Verdict | Fix applied |
|---|---|---|
| A2-1 | CONFIRMED BLOCKER (typed "10%" input in FAQ question) | Question reworded without the number. |
| A2-2, A2-3 | CONFIRMED (same fact in $ form and plain form) | No text change; count noted below. |
| A2-4 to A2-7 | CONFIRMED | Markers or words (see A1-7, A1-9, A1-11, A1-12). |
| A2-8, A2-9 | CONFIRMED (Alaska LNG peak workforce 6,600; North Berth 5.8 million TEUs, single-project capacity statements) | `data-fsc-nocount`. |
| A2-10 | CONFIRMED (0.03 million gap against 0.005 rounding) | Clause replaced by "two accounts of the same 2025 total". |
| A2-11 | CONFIRMED | Same fix as A1-6. |
| A2-12 to A2-20 | CONFIRMED (same.py 8-word runs against the copy) | All six heroes, descriptions, opening paragraphs, CTA paragraphs, closing bands, loan and dscr paragraphs, sensitivity paragraphs, FAQ questions and answers, condition frames and section headings rewritten per page. Runs of 8 or more words between any page of the six and any page of the copy fell from 283 to about 120 and from a maximum of 60 words to at most 15; what is left are 8 to 12 word fragments shared with the Lebanon template and landed pages (SBA rule recitals such as "limit for a project that is not a small manufacturer", the mandated "Feasibility Study Company prepares feasibility studies for owners, developers and their lenders", register-sourced sentence stubs). They sit inside rule recitals and could not be cleared without altering the rule wording; reported, not hidden (see v-same.txt). |
| A2-21 | CONFIRMED (161 and 162 characters) | Descriptions rewritten, all six 140 to 160 (156, 154, 150, 153, 157, 152). |
| A2-22 | CONFIRMED | Hero now leads with 224,676 residents (state-page figure, A4). |
| A2-23 | CONFIRMED | Glance says the research names no corridor; corridor becomes a lender condition; no citation on it. |
| A2-24 | CONFIRMED (mesh linked "Nevada Avenue" to the Nevada state page) | Corridor renamed "Tejon Street corridor" (a case assumption), page and glance. |
| A2-25 | CONFIRMED MINOR | Descriptions or closing CTAs now carry "company" or "consultant" in every case. |
| A2-26 | CONFIRMED MINOR | FAQ answers link `/research-notes/sba-feasibility-myth/`; questions reworded. |
| A2-27 | CONFIRMED | "we will tell you what a study for it would cover" removed. |
| A2-28 | CONFIRMED | nocount (see A1-16). |
| A2-29 | CONFIRMED for the $54M allocation (nocount); register zero left as printed |
| A2-30 | CONFIRMED | "About $2 billion" JBER figure in nocount. |
| A2-31 | CONFIRMED | Process wording removed. |
| A2-32 | CONFIRMED | Citation dropped from the corridor clause. |
| A2-33 | CONFIRMED MINOR | All six cards reworded. |

## Final counts (pagecheck --stage ready, copy c1f2)

| Case | Counted | Research | Register | Note |
|---|---|---|---|---|
| industrial-warehouse-chesapeake-virginia-sba | 36 | 28 | 8 | |
| event-venue-jackson-wyoming-sba | 35 | 31 | 4 | |
| brewery-fargo-north-dakota-sba | 35 | 33 | 2 | pagecheck still counts the three rescaled pairs twice; on the ruling 5 reading the research count is 30 |
| cold-storage-anchorage-alaska-sba | 32 | 28 | 4 | |
| auto-dealership-sioux-falls-south-dakota-sba | 52 | 42 | 10 | |
| mixed-use-colorado-springs-colorado-sba | 48 | 39 | 9 | |

All six stay at 30 counted or more with 20 research or more.

## Gates (copy c1f2, `--skip-look`, site-wide)

See the summary line in N/copies/GATES-c1-f2.txt. Gate 9 stays red exactly as at freeze: the hub or state pages that Fargo and Chesapeake (hub) and Anchorage and Jackson (state) link to are not built yet (integrator's inbound-link and card work). Gate 13 is pending only because of `--skip-look`.

## HELD cases

None held. Auto dealership Sioux Falls is NOT held but its determination changed from a pass at 15.5% to a negative result: the model does not support the loan at any equity share (restructured 15.0% equity gives 0.48x in Year 2). The page, glance and card say so.
