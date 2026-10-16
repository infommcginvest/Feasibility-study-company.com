# Recompute log: case-studies/medical-office-north-carolina-sba (WEB-FSC-4)

Script: `docs/web-fsc-4/recompute/medical-office-north-carolina-sba.py` (run it for the table; `--check` reads the page and exits 0 or 1).
Page: `case-studies/medical-office-north-carolina-sba/index.html`.

## The defect and the ruling

The page financed the $9.60M ground-up, owner-occupied medical office building with a surgery center (ASC) as 50% bank / 40% CDC debenture / 10% borrower ($0.96M) and called the 10% the 504 equity injection.

13 CFR 120.910 (unchanged in SOP 50 10 8.1; register row R31): the borrower contributes at least 10% in standard cases; at least 15% if the borrower (or the Operating Company) has operated two years or less OR the project is a limited or single purpose building; at least 20% if both. SBA's limited or special purpose example list (register row R44) names "hospitals, surgery centers, urgent care centers, and other health or medical facilities". A surgery center is therefore special purpose and needs at least 15%: Third Party Lender 50%, CDC debenture 35%, borrower 15%.

The owner ruled the case goes to 15%. That holds on the reading that the operating company is the established physician group (more than two years in operation); an operating company with two years or less of operations would need 20% (debenture 30%). The page never says the group or borrower is newly formed, so no tier was left undecided.

## Model check: BEFORE reproduces the page

| Figure | Page published | Model (BEFORE) |
|---|---|---|
| Bank debt service ($4.80M, 9.5%, 25 yr) | about $503,000 | $503,249 |
| Debenture debt service ($3.84M, 6.5%, 25 yr) | about $311,000 | $311,135 |
| Blended debt service | about $814,000 / $814k | $814,385 |
| DSCR Y1 / Y2 / Y3 on $0.94M / $1.10M / $1.22M | 1.15 / 1.35 / 1.50 | 1.154 / 1.351 / 1.498 |
| Ten-year loan balance | near $7.0 million | $6.99M |
| Net exit equity ($9.5M less 3% less balance) | roughly $2.2 million | $2.22M |
| Levered equity IRR | about 16 percent | 16.0% (calibrated, see below) |

Rate convention: monthly compounding, level payment, annualized as 12 x the monthly payment. The Year 3 build ($3.60M + $2.60M + $0.16M revenue less $5.14M operating expenses = $1.22M) and the uses breakdown ($9.60M) are asserted in the script.

## Before / after: every figure that moved

| Figure | BEFORE (50/40/10) | AFTER (50/35/15) |
|---|---|---|
| Total project cost | $9.60M | $9.60M (unchanged) |
| Bank first mortgage | $4.80M (50%) | $4.80M (50%, unchanged) |
| CDC debenture | $3.84M (40%) | $3.36M (35%) |
| Borrower equity | $0.96M (10%) | $1.44M (15%) |
| Financed share of cost (hero tile) | 90% | 85% |
| Bank debt service | $503,000 | $503,000 (unchanged) |
| Debenture debt service | $311,000 | $272,000 |
| Blended debt service | $814,000 / $814k | $775,000 / $775k |
| DSCR Year 1 | 1.15 | 1.21 |
| DSCR Year 2 | 1.35 | 1.42 |
| DSCR Year 3 / stabilized | 1.50 | 1.57 |
| Ten-year loan balance | $7.0 million | $6.6 million |
| Net equity at exit | $2.2 million | $2.6 million |
| Levered equity IRR | 16.0% (published "about 16 percent") | 12.0% (published "about 12 percent") |

Not published on the page (printed by the script for the record, not in `--check`):

| Figure | BEFORE | AFTER |
|---|---|---|
| Cash on cash Y1 / Y2 / Y3 (all cash flow after debt service over equity) | 13.1% / 29.8% / 42.3% | 11.4% / 22.5% / 30.9% |
| Equity multiple (calibrated payout) | 3.38x | 2.59x |
| Year 3 cash-flow cushion over the 1.15x floor | $283k | $328k |

The page has no stress-test DSCRs, break-even figures, LTV/LTC figures, FAQ answers or image alt text, so nothing else is financing-dependent. Global cash flow, revenue lines, operating expenses, the project cost, the exit value ($9.5M), the selling cost (3%), the rates and the amortizations do not depend on the stack and did not change.

## IRR method

The page states the equity outlay, the 10-year hold, the exit value ($9.5M, "held flat on value"), the selling cost (3%) and a rate and amortization for each loan (so the exit balance follows). It does not state the interim distributions beyond "modest", and it gives cash flow only for Years 1 to 3.

1. Years 4 to 10 global cash flow is held at the Year 3 stabilized level ($1.22M), in line with the page's flat-value assumption. This is a modelling convention. The sensitivity below shows the result does not depend on it.
2. Exactly one unstated assumption is calibrated: the share of each year's cash flow after debt service that is distributed to equity. It is solved so the BEFORE structure returns 16.00%. Result: 28.0% (payout 0.2799), which reads as "modest".
3. That share is held fixed. The AFTER IRR is computed with the AFTER equity ($1.44M outlay), AFTER debt service and the AFTER exit balance: 12.0%.
4. Annual end-of-year flows; year-0 outlay is the equity injection; the year-10 flow adds net sale proceeds.

Sensitivity (BEFORE recalibrated to 16.0% each time): Years 4 to 10 cash flow growth of -2%, 0%, +2%, +3% a year gives an AFTER IRR of 12.03%, 12.02%, 12.00%, 12.00%. If the published "about 16 percent" stood for any BEFORE IRR from 15.5% to 16.5%, the AFTER IRR is 11.6% to 12.4%, which still rounds to 12.

## Sentences changed (old text, then new text)

All edits are on the one page. The diff against the page as received is 20 line-diff hunks. No em dash or en dash was added; the page's 49 existing dashes are unchanged (the same count before and after). The header, nav, footer, `fsc:` regions, existing `sba:` regions, `datePublished`, `dateModified` and the breadcrumb were not touched.

1. Meta description. Old: "...a $9.60M project cost, a 1.50x stabilized global DSCR, and a ~16% levered equity IRR." New: "...a $9.60M project cost, a 1.57x stabilized global DSCR, and a ~12% levered equity IRR."
2. og:description. Old: "...$9.60M cost, 1.50x global DSCR, ~16% IRR." New: "...$9.60M cost, 1.57x global DSCR, ~12% IRR."
3. JSON-LD Article description. Old: "...a 1.50x stabilized global DSCR, and a ~16% levered equity IRR." New: "...a 1.57x stabilized global DSCR, and a ~12% levered equity IRR."
4. Hero tile. Old: "90%" / "SBA 504 financing (50% bank + 40% CDC debenture)". New: "85%" / "SBA 504 financing (50% bank + 35% CDC debenture)".
5. Hero tile. Old: "1.50x". New: "1.57x".
6. Hero tile. Old: "&asymp;16%". New: "&asymp;12%".
7. Financing lede (states the old tier). Old: "...a bank first mortgage, a fixed-rate CDC debenture, and a 10 percent equity injection &mdash; which is why an owner-occupied medical building routes here rather than to a leased-fee MOB loan." New: "...a bank first mortgage, a fixed-rate CDC debenture, and a borrower equity injection (15 percent here, as set out below) &mdash; which is why an owner-occupied medical building routes here rather than to a leased-fee MOB loan." (The existing em dash is kept; the program-level clause no longer claims 10 percent, and the case figure points to the sentence that carries the condition.)
8. Capital structure table. Old: "CDC / SBA 504 debenture (40%)" $3.84M; "Borrower equity injection (10%)" $0.96M. New: "CDC / SBA 504 debenture (35%)" $3.36M; "Borrower equity injection (15%)" $1.44M.
9. Capital structure table. Old: "Annual debt service (blended)" "&asymp; $814k". New: "&asymp; $775k".
10. Table source note. Old: "See sources 4, 5, and 6." New: "See sources 4, 5, 6, and 14."
11. Financing prose, split (states the old tier). Old: "The 504's 50/40/10 split does the work here: a bank first mortgage at 50 percent, a fixed-rate CDC debenture at 40 percent, and a 10 percent equity injection." New: "The 504's 50/35/15 split does the work here: a bank first mortgage at 50 percent, a fixed-rate CDC debenture at 35 percent, and a 15 percent equity injection."
12. Financing prose, new sentence stating the tier with its condition (carries `sba:equity.sba_504_new_or_special` and `sba:equity.sba_504_new_and_special` markers, footnotes 5 and 14). New: "That 15% is the 504 minimum for a limited or special purpose property such as a surgery center under 13 CFR 120.910, on the basis that the operating company is the established physician group (more than two years in operation); an operating company with two years or less of operations would need 20%."
13. Financing prose, debt service. Old: "...the debenture at roughly 6.5 percent fixed about $311,000, for blended annual debt service near $814,000 &mdash; the number the projected coverage has to clear." New: "...about $272,000, for blended annual debt service near $775,000 &mdash; the number the projected coverage has to clear." (The $503,000 bank figure is unchanged.)
14. DSCR table. Old: "Fully amortizing ~$814k" with 1.15 / 1.35 / 1.50. New: "Fully amortizing ~$775k" with 1.21 / 1.42 / 1.57.
15. Coverage prose. Old: "The stabilized 1.50x global coverage is the figure the lender documents..." New: "The stabilized 1.57x global coverage is the figure the lender documents..."
16. Coverage prose. Old: "so Year 1 sits at 1.15x, Year 2 builds to 1.35x as case volume and payer contracts mature, and Year 3 reaches 1.50x." New: "so Year 1 sits at 1.21x, Year 2 builds to 1.42x as case volume and payer contracts mature, and Year 3 reaches 1.57x."
17. Equity prose. Old: "the $0.96 million injection earns a return..." New: "the $1.44 million injection earns a return..."
18. Equity prose. Old: "...an outstanding balance near $7.0 million after ten years of amortization &mdash; implies roughly $2.2 million of net equity, against the $0.96 million injected." New: "...an outstanding balance near $6.6 million after ten years of amortization &mdash; implies roughly $2.6 million of net equity, against the $1.44 million injected."
19. Equity prose. Old: "...levered equity IRR of about 16 percent over a 10-year hold." New: "...levered equity IRR of about 12 percent over a 10-year hold."
20. Verdict capsule. Old: "...a stabilized 1.50x global DSCR, and a ~16% levered equity IRR, the projections support the SBA 504 credit." New: "...a stabilized 1.57x global DSCR, and a ~12% levered equity IRR, the projections support the SBA 504 credit."
21. Sources list: new item 14 appended after item 13, nothing renumbered. New: "13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910". Footnote markers to #s14 added in change 12.

## Did the conclusion change?

No. The verdict reads "financially feasible and bankable ... the projections support the SBA 504 credit". At 15% equity the debenture falls from $3.84M to $3.36M while the bank tranche is unchanged, so blended debt service falls from $814k to $775k and every coverage ratio rises: Year 1 1.21x (above the 1.15x floor, where it sat on it before), Year 3 1.57x. The demand, CON and competition findings do not depend on the stack. The levered IRR falls from about 16% to about 12% because the borrower puts in $0.48M more equity, but the page states no IRR hurdle and the verdict does not rest on it, so only the figures in the sentence were updated.

## Not resolved / for the owner

1. The tier rests on the owner's reading that the operating company is the established physician group (more than two years in operation). The page says nothing about the operating company's age. It does speak of "a new surgery center" and, generically, of how "a start-up practice line ramps over two to four years", which describes the ASC ramp and not the borrower. If the operating company is a New Business, 120.910(a)(3) applies: 20% equity, 30% debenture, and this recompute has to be rerun (the script's stack table is the one place to change).
2. The building is mixed: about 60% owner-occupied practice and ASC, about 40% leased to physician tenants. The special purpose classification of the whole building follows the owner's ruling and SBA's example list naming surgery centers; I did not test it further.
3. Footnote 5 (the SOP) is cited beside footnote 14 for the surgery-center example list, which is in the SOP's 504 chapter (register row R44). The existing text of source 5 mentions special-purpose properties but not the example list; I left source 5 alone.
4. Existing sentence, left unchanged because it is not financing-dependent: "At $9.60 million total the deal also sits within the combined 7(a)-plus-504 ceiling that rose to $10 million..." It compares total project cost with a ceiling that applies to the SBA loan amounts, which here are far lower. It is not false as a comparison, but the owner may want it reworded.
5. Cash on cash, equity multiple and break-even figures do not appear on the page, so none were added (no new figures were introduced).
