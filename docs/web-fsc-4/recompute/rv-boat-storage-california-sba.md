# Recompute: rv-boat-storage-california-sba (lane WEB-FSC-4)

Page: `case-studies/rv-boat-storage-california-sba/index.html`
Script: `docs/web-fsc-4/recompute/rv-boat-storage-california-sba.py` (run it for the table; `--check` compares it with the page)

## The defect and the rule

The page financed a ground-up RV and boat storage yard 50% bank / 40% CDC debenture / 10% borrower and called the 10% an SBA baseline (and a "standard 10 percent"). Under 13 CFR 120.910 (unchanged in SOP 50 10 8.1; register R31) the 504 borrower contribution is 10% in standard cases, 15% for a New Business (borrower, or the operating company behind an eligible passive company, has operated two years or less) or a limited or special purpose building, and 20% for both. The 10% start-up figure in SOP 50 10 8.1 is the 7(a) Start-Up Business rule (R29). A ground-up storage business is a New Business. RV and boat storage is not on SBA's special purpose examples, and the page itself argues the mixed-format yard is unlikely to draw a special purpose designation, so the tier is 15% and the stack is **50 / 35 / 15**. Nothing on the page argues special purpose, so no stop was needed.

## Model check (BEFORE reproduces the page)

Inputs are all from the page: cost $6.10M (eight uses lines sum to it); bank 9.5% / 25 yr; debenture 6.5% / 25 yr; monthly amortization; NOI Y1 $466k, Y2 $595k, Y3 $750k. BEFORE gives bank $319.8k, debenture $197.7k, total $517.5k, so the page's "about $517k (bank ~$320k + debenture ~$198k)" and DSCR 0.90 / 1.15 / 1.45 are reproduced exactly. The revenue and NOI build (GPR $1.116M, EGI $1.072M, opex $0.322M, NOI $0.750M) is not financing dependent and is unchanged.

## Before and after (every figure that moved)

| Figure | BEFORE (50/40/10) | AFTER (50/35/15) |
|---|---|---|
| Bank first mortgage (50%) | $3.05M | $3.05M (unchanged) |
| CDC / SBA 504 debenture | $2.44M (40%) | $2.135M (35%) |
| Borrower equity injection | $0.61M (10%) | $0.915M (15%) |
| Sources total | $6.10M | $6.10M |
| SBA 504 financing share (stat tile) | 90% | 85% |
| Bank debt service | ~$320k ($319,773) | ~$320k (unchanged) |
| Debenture debt service | ~$198k ($197,701) | ~$173k ($172,988) |
| Annual debt service | about $517k ($517,474) | about $493k ($492,761) |
| DSCR Year 1 (NOI ~$466k) | 0.90 | 0.95 |
| DSCR Year 2 (NOI ~$595k) | 1.15 | 1.21 |
| DSCR Year 3 / stabilized (NOI ~$750k) | 1.45 | 1.52 |
| Cash after debt service Y1 / Y2 / Y3 (log only) | -$51k / $78k / $233k | -$27k / $102k / $257k |
| Stabilized cash-on-cash (log only, not on the page) | 38.1% | 28.1% |
| Loan balance after 10 years (log only) | $4.44M | $4.21M |
| Levered equity IRR (stated exit, 3% selling cost) | 35.8% (page said about 16%) | 29.8%, published as near 30% |

Rounding: at the page's usual two decimals the split would read $2.14M and $0.92M, which sum with the bank loan to $6.11M. The page already uses three decimals where needed ($0.089M, $1.116M), so the two split lines are $2.135M and $0.915M and the table foots to $6.10M.

The page has no cash-on-cash row, no stress-test DSCR, no break-even figure that includes debt service, and no LTV or LTC other than the 90% financing tile, so nothing else moved. The Year-1 shortfall (now $27k, was $51k) is still below the $0.10M lease-up and interest reserve in the budget, so "covered by the funded lease-up and interest reserve" stays true.

## IRR: recomputed from the stated exit (supersedes the earlier hold)

The first version of this log held the IRR at the published about 16% because the page's inputs did not reproduce it. After the adversarial review the ruling is that the page's own stated exit determines the figure, so "about 16 percent" is false by its own derivation and the tile is recomputed (ruling 7).

Stated on the page and used as stated: 10-year hold; stabilized NOI untrended after Year 3 ($750k); sale at a normalized exit rate of about 7.5%, a gross value near $10.0M; net of selling costs and the outstanding 504 balance (loan balances after 120 monthly payments); blended with the graded lease-up (the Year-1 shortfall is paid from the funded lease-up and interest reserve, so the Year-1 distribution is zero; Year 2 onward is NOI less debt service). Equity is the page's own: $0.61M BEFORE, $0.915M AFTER.

One input is not on the page: the selling cost. The script adds exactly one assumption, selling costs of 3% of gross value (`SELL = 0.03`), in the middle of a 0% to 5% band, and states it in its docstring. Nothing else is calibrated.

| Selling cost | 0% | 2% | 3% | 5% | 10% | 30% |
|---|---|---|---|---|---|---|
| BEFORE (50/40/10) | 36.3% | 36.0% | **35.8%** | 35.5% | 34.7% | 30.8% |
| AFTER (50/35/15) | 30.2% | 29.9% | **29.8%** | 29.5% | 28.7% | 25.0% |

At 3%: BEFORE 35.8%, AFTER 29.8%, so the tile, descriptions and verdict read 30% and the prose reads "near 30 percent". Across the 0% to 5% band AFTER spans 29.5% to 30.2%; as integers the 0%, 2% and 3% cases round to 30 and the 5% case (29.48%) rounds to 29, which is why the prose says "near 30 percent" rather than claiming an exact integer at every selling cost.

Why the earlier ~16% was dropped: the present value at 16% of the BEFORE operating distributions alone is about $0.81M, above the $0.61M of equity, so the BEFORE IRR is above 16% for any exit equity of zero or more, whatever the selling cost. Only an exit cap above 17% (17.3% at 3% selling cost) would give 16%, against the page's own 7.5% and its 6.0 to 8.5 percent range. The published figure could not be produced by the page's own derivation, and the stated exit does determine a figure, so keeping it would leave a false sentence.

The twitter description names "levered IRR" without a figure and is unchanged. The `--check` now expects the recomputed IRR text and fails on any remaining 16% IRR (visible text, meta, og, JSON-LD) or on "mid-teens".

## Sentences changed (old, then new)

1. Meta description: "a 1.45x stabilized DSCR, and a ~16% levered equity IRR" -> "a 1.52x stabilized DSCR, and a ~30% levered equity IRR".
2. og:description: "$6.10M cost, 1.45x DSCR, ~16% IRR." -> "$6.10M cost, 1.52x DSCR, ~30% IRR."
3. JSON-LD Article description: "a 1.45x stabilized DSCR, and a ~16% levered equity IRR" -> "a 1.52x stabilized DSCR, and a ~30% levered equity IRR".
4. Stat tile: "90%" / "SBA 504 financing (50% bank + 40% CDC/SBA debenture)" -> "85%" / "SBA 504 financing (50% bank + 35% CDC/SBA debenture)".
5. Stat tile: "1.45x" -> "1.52x" (label unchanged). The IRR tile is item 20.
6. Capital structure caption. Old: "How the $6.10M is financed under a standard SBA 504 stack, and the debt-service load it creates." New: "How the $6.10M is financed under an SBA 504 stack at the 15% New Business contribution, and the debt-service load it creates." (15% is an `equity.sba_504_new_or_special` marker.)
7. Table row: "CDC / SBA 504 debenture (40%)" / "$2.44M" -> "(35%)" / "$2.135M" (the "25-yr, fixed ~6.5%" text is untouched).
8. Table row: "Borrower equity injection (10%)" / "$0.61M" -> "Borrower equity injection (15%)" / "$0.915M" (15% is a marker).
9. Table row: "&asymp; $517k (bank ~$320k + debenture ~$198k)" -> "&asymp; $493k (bank ~$320k + debenture ~$173k)".
10. Table note. Old: "...; 50% bank first / 40% CDC debenture / 10% equity; owner-occupancy 60% for new construction. See sources 13 and 14." New: "...; 50% bank first / 35% CDC debenture / 15% equity, the 504 contribution for a New Business under 13 CFR 120.910; owner-occupancy 60% for new construction. See sources 13, 14, and 18."
11. Financing prose, opening. Old: "The equity injection sits at the 10 percent SBA baseline, and holding it there was a considered call. SBA policy escalates the required injection for projects that are both special-purpose and start-ups, and some lenders tag single-use climate-controlled storage as special-purpose &mdash; but a mixed-format yard, with open, covered, and a modest enclosed component, is less likely to draw that designation, which supports the standard 10 percent here.[14] The $2.44 million CDC debenture sits well inside the program's debenture ceiling..." New: "The equity injection is 15%, the 504 minimum for a New Business (the borrower, or the operating company where the borrower is an eligible passive company, has operated for two years or less) under 13 CFR 120.910, which is the tier a ground-up storage business falls in.[18] The 10 percent start-up figure in SOP 50 10 8.1 is the 7(a) rule, not a 504 rule.[14] The 504 minimum rises to 20% only if the project is also a limited or special-purpose building, so holding the injection at 15 rather than 20 percent was a considered call. Some lenders tag single-use climate-controlled storage as special-purpose, but a mixed-format yard, with open, covered, and a modest enclosed component, is less likely to draw that designation, which supports 15 percent here.[14] The $2.135 million CDC debenture sits well inside the program's debenture ceiling..." (15% and 20% are `sba_504_new_or_special` and `sba_504_new_and_special` markers. The old em dash sat inside a sentence that had to be rewritten, so the new text has none.)
12. Financing prose, debt service: "about $517,000 ... a 504 debenture near $198,000" -> "about $493,000 ... a 504 debenture near $173,000" (bank first near $320,000 unchanged; the existing em dashes are untouched).
13. DSCR caption and note: "about $517k" / "the ~$517k full amortizing annual debt service" -> "about $493k" / "the ~$493k full amortizing annual debt service".
14. DSCR table: Year 1 0.90 -> 0.95; Year 2 1.15 -> 1.21; Year 3 1.45 -> 1.52 (NOI and occupancy columns unchanged).
15. Outcome prose: "The stabilized 1.45x coverage is the figure the lender documents" -> "The stabilized 1.52x coverage ..."; "Year 1 posts 0.90x" -> "Year 1 posts 0.95x".
16. Outcome prose: "the $0.61 million injection earns free cash flow" -> "the $0.915 million injection earns free cash flow".
17. Verdict capsule: "a stabilized 1.45x DSCR" -> "a stabilized 1.52x DSCR". The IRR in the capsule is item 22.
18. Source 14. Old tail: "10% equity injection baseline, higher where a project is both special-purpose and a start-up;" New: "a 10% equity injection for a 7(a) Start-Up Business (the 504 contribution is 10% in standard cases, 15% for a New Business or a limited or special purpose property, and 20% for both, per source 18);" (three markers).
19. New source 18 (appended, nothing renumbered): "13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910". Footnote markers `<sup class="fn"><a href="#s18">18</a></sup>` added in the financing prose.
20. Stat tile IRR: "&asymp;16%" -> "&asymp;30%" (label "Illustrative levered equity IRR, 10-year hold" unchanged).
21. Outcome prose. Old: "...the illustrative levered equity IRR lands in the mid-teens, about 16 percent over a 10-year hold." New: "...the illustrative levered equity IRR lands near 30 percent over a 10-year hold." (the rest of the sentence is unchanged).
22. Verdict capsule: "a ~16% illustrative levered equity IRR" -> "a ~30% illustrative levered equity IRR".
23. The IRR in the meta description, og:description and JSON-LD description (items 1 to 3): "~16%" -> "~30%". The twitter description has no figure.

That is 23 replacements in the original recompute plus 6 for the IRR (items 1 to 3 and 20 to 22 above; the three head strings were edited a second time), 29 in all. The first 23 were: meta, og and JSON-LD (3); two stat tiles (2); capital table caption (1) and three rows (3) and note (1); financing prose (2: tier paragraph, debt-service figures); DSCR caption (1), three DSCR rows (3) and note (1); outcome prose (3: stabilized coverage, Year 1, equity injection); verdict capsule (1); source 14 (1); new source 18 (1).

Not touched: header, nav, footer, the `fsc:` regions, existing `sba:` regions, datePublished and dateModified, breadcrumb, and the other em and en dashes. The `git diff` of this file also shows header, nav and CTA hunks (`data-fsc-pending`, `/#contact`) made by another tool running in the same worktree while this lane ran; they are not part of this recompute.

## Did the conclusion change?

No. The verdict "financially feasible and bankable" stands: coverage improves in every year (0.95 / 1.21 / 1.52), the stabilized 1.52x still clears the roughly 1.20x to 1.25x storage floor, and the 85 percent stress remains better than the old structure's. Only the figures inside the conclusion sentences changed (DSCR 1.45x to 1.52x; IRR about 16% to about 30%, a correction of the earlier figure to what the stated exit gives).

## Could not resolve (open items)

1. **IRR now recomputed** from the stated exit with one added assumption (3% selling costs, not on the page): BEFORE 35.8%, AFTER 29.8%, published as near 30%. The 0% to 5% band spans 29.5% to 30.2% (29.48% at 5% is 29 as an integer), so the page says "near 30 percent". The 3% is the one input an owner or reviewer may want to confirm.
2. The 15% tier assumes the borrower (or its operating company) is a New Business with two years or less of operation. The page does not state the sponsor's operating history; this follows the owner ruling that a ground-up storage business is a New Business.
3. 13 CFR 120.910 applies the percentage to project cost excluding administrative costs. The case has no administrative-cost line, so 15% is applied to the full $6.10M, the same base the page used for 10%.
4. Source 14 still cites 13 CFR 120.160(b) and the SOP for the eligibility facts, as before; only its equity clause was rewritten.
