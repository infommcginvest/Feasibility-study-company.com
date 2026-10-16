# Recompute: rv-boat-storage-florida-sba (WEB-FSC-4)

Page: case-studies/rv-boat-storage-florida-sba/index.html. Script: docs/web-fsc-4/recompute/rv-boat-storage-florida-sba.py
(rerun it for the table below; `--check` reads the page and exits 0 only when every AFTER figure is on it).

## The defect and the tier

The page financed the project 50% bank / 40% CDC debenture / 10% borrower equity and called the 10% the SBA minimum (start-up,
or as restored by SOP 50 10 8.1). For a 504 that is wrong. 13 CFR 120.910 (unchanged in SOP 50 10 8.1): the borrower contributes
at least 10% in standard cases, at least 15% if the borrower or Operating Company has operated two years or less (a New Business) or
the project is a limited or special purpose property, and at least 20% if both. The 10% start-up figure in SOP 50 10 8.1 is the 7(a)
Start-Up Business rule (sba.json equity.startup_7a), not a 504 rule. A ground-up storage business is a New Business. RV and boat
storage is not on SBA's special purpose example list, and the page itself argues the opposite of special purpose (it says the
mixed-format, covered-canopy-led program is less likely to draw that designation than a single-use climate-controlled build), so
the tier is 15%: Third Party Lender 50%, CDC debenture 35%, borrower 15%. No stop-and-report condition arose.

## Before and after (every figure that moved)

BEFORE reproduces the published page exactly (all twelve published figures; see the script's reproduction test).

| Figure | Before (published) | After | Exact after |
|---|---|---|---|
| Borrower equity | 10%, $0.58M | 15%, $0.87M | $870,000 |
| CDC / SBA debenture | 40%, $2.32M | 35%, $2.03M | $2,030,000 |
| Bank first mortgage | 50%, $2.90M | unchanged | $2,900,000 |
| Total 504 debt (tile) | 90%, $5.22M of $5.80M | 85%, $4.93M of $5.80M | $4,930,000 |
| Debt service, bank | about $304k | unchanged | $304,046 |
| Debt service, debenture | about $188k | about $164k | $164,480 |
| Debt service, combined (table and prose) | about $492k, near $492,000 | about $469k, near $469,000 | $468,527 |
| DSCR Year 1 (NOI ~$444k) | 0.90 (prose 0.90x) | 0.95 (0.95x) | 0.9477 |
| DSCR Year 2 (NOI ~$567k) | 1.15 (1.15x) | 1.21 (1.21x) | 1.2102 |
| DSCR Year 3, stabilized (NOI ~$713k) | 1.45 (1.45x) | 1.52 (1.52x) | 1.5218 |
| Debt-service break-even occupancy | near 64 percent | near 61 percent | 61.1 |
| Levered equity IRR (tile, meta, OG, JSON-LD, prose, verdict) | about 16% | left as published, about 16% (not recomputed) | see IRR |
| Cash flow after debt service, Year 3 (not on page) | $221k | $244k | |
| Stabilized cash-on-cash (not on page) | 38.1% | 28.1% | |
| Year 10 loan balances (not on page) | $4.22M | $4.00M | |

Unchanged: project cost $5.80M and every uses line, rates 9.5% and 6.5%, 25-year amortization, every NOI and revenue line, the
about 12 percent unlevered yield, the 1.20 to 1.25x lender floor, the owner-occupancy and 24-month statements, the Small Loan
threshold sentence in source 10 (left exactly as is: "Small Loan threshold reduced from $500,000 to $350,000.").

Rounding note: the table shows about $304k and about $164k beside a combined about $469k. The exact sum is $468,527, which rounds to
$469k; the two rounded components add to $468k. Each figure is the correct rounding of its own exact value.

Cash on cash: the page never states a cash-on-cash number (its sentence names the concept and gives NOI and debt service), so
there was no row to move. None was added: a 28% stabilized cash-on-cash next to a 16% IRR would put the page's existing
IRR inconsistency (below) in plain view.

## IRR: left as published, not recomputed

Decision (coordinator, after this agent's first version): all six IRR sites carry exactly the published text. Tile
`&asymp;16<span>%</span>` ("Illustrative levered equity IRR, 10-year hold"), meta description, Open Graph description and
JSON-LD description (`..., a 1.52x stabilized DSCR, and a ~16% levered equity IRR.`), Outcome prose (`equity IRR of about 16
percent over a 10-year hold.`), verdict (`a stabilized 1.52x DSCR, and a ~16% levered equity IRR, the projections support`).
Only the DSCR beside the IRR moved in the three descriptions and the verdict.

Why. The page does not state enough to compute its 16%: no exit value, no selling cost, no NOI path after Year 3. The brief's
remedy was to calibrate one unstated assumption (the exit cap rate) so BEFORE reproduces 16%. It was run (the script prints it,
labelled REJECTED) with: equity in at t0; years 1 to 10 NOI minus combined debt service, floored at zero where NOI is below debt
service (the page says the financed lease-up reserve bridges the opening shortfall); NOI $444k / $567k / $713k then flat; exit
in Year 10 at Year 3 NOI over the cap rate less the balances outstanding; IRR = largest real root. The cap rate that gives 16.00%
is 21.03%: a $3.39M sale (0.58x project cost) below the $4.22M balance, net proceeds -$0.83M. That is not a gap-filling
assumption but a contradiction of what the page states (dedicated-storage cap rates 6.0 to 8.5%, a 12% unlevered yield on cost,
an exit "disciplined against replacement cost" capped near 1.15x cost). The charter's rule for a fix that needs facts the page
does not give is to leave the original and log it, so the original stays.

Owner item: the published 16% is not consistent with the page's own cash flows, in either structure.

| Exit assumption (page's cash flows, NOI flat after Year 3, reserve bridges Year 1) | BEFORE 50/40/10 | AFTER 50/35/15 |
|---|---|---|
| Worthless exit (equity gets nothing at sale) | 22.31% | 15.81% |
| Sale at 1.00x project cost, no sale cost | 28.51% | 22.79% |
| Sale at 1.15x project cost, no sale cost | 30.84% | 25.01% |
| REJECTED calibration: sale at 21.03% cap (BEFORE set to 16.00%) | 16.00% | 11.45% |
| Same, Year 1 shortfall paid by equity instead of the reserve | 16.00% | 12.44% |
| Same, BEFORE set to 15.5% / 16.5% | 15.50% / 16.50% | 11.04% / 11.87% |

Reading: the published 16% was not produced by any exit the page describes; and because more equity with less debt lowers a
levered IRR, the 16% now sits beside a 15% structure without having been recomputed for it (a restated figure would sit in the
11 to 12% band under the rejected calibration, and at 15.8% or more under a page-consistent exit). Options for the owner: leave the
IRR as is (current), restate it on a model the owner supplies (exit value, selling cost, NOI path), or drop the single IRR
figure as WEB-FSC-2 did for veterinary-michigan. Restating or dropping is one edit across six places and a one-line script change.

## Does the conclusion change?

No. The verdict reads "financially feasible and bankable ... the projections support the SBA 504 credit". Stabilized coverage
rises from 1.45x to 1.52x against the same 1.20 to 1.25x floor, Year 1 stays below 1.0 (0.95x) and is still bridged by the
financed reserve, and break-even moves earlier (61 percent against 64). Only the DSCR figure inside the verdict sentence moved (the IRR figure in it is the published one). Year 2 coverage (1.21x) now sits inside the 1.20 to 1.25x floor band; the page makes no claim about Year 2 against the floor.

## Sentences changed (old, then new)

HTML as in the file, whitespace collapsed. Text I wrote contains no em dash or en dash; existing &mdash; and &ndash; in untouched
parts of these sentences are left for the dash sweep. Regulatory markers (sba:equity.*, sba:sop.short) wrap the tier figures.
24 edit operations, 26 sites. The IRR is not among them (see IRR).

1. meta/OG/JSON-LD description: DSCR (x3 places)
   - old: `a 1.45x stabilized DSCR, and a ~16% levered equity IRR.`
   - new: `a 1.52x stabilized DSCR, and a ~16% levered equity IRR.`

2. tile: 504 debt share
   - old: `<div class="stat-num">90<span>%</span></div> <div class="stat-label">SBA 504 debt (50% bank + 40% CDC/SBA), $5.22M of $5.80M</div>`
   - new: `<div class="stat-num">85<span>%</span></div> <div class="stat-label">SBA 504 debt (50% bank + 35% CDC/SBA), $4.93M of $5.80M</div>`

3. tile: stabilized DSCR
   - old: `<div class="stat-num">1.45<span>x</span></div>`
   - new: `<div class="stat-num">1.52<span>x</span></div>`

4. financing lede: equity tier
   - old: `mortgage, a CDC/SBA debenture, and a 10 percent equity injection &mdash; fits a long-term`
   - new: `mortgage, a CDC/SBA debenture, and a 15 percent equity injection &mdash; fits a long-term`

5. financing lede: footnote 14
   - old: `hold on ground-up, owner-occupied real estate.<sup class="fn"><a href="#s10">10</a></sup>`
   - new: `hold on ground-up, owner-occupied real estate.<sup class="fn"><a href="#s10">10</a></sup><sup class="fn"><a href="#s14">14</a></sup>`

6. capital table: debenture row
   - old: `<tr><td>CDC / SBA 504 debenture (40%)</td><td>$2.32M &mdash; ~6.5%, 25-yr amortization</td></tr>`
   - new: `<tr><td>CDC / SBA 504 debenture (35%)</td><td>$2.03M &mdash; ~6.5%, 25-yr amortization</td></tr>`

7. capital table: equity row
   - old: `<tr><td>Borrower equity injection (10%)</td><td>$0.58M</td></tr>`
   - new: `<tr><td>Borrower equity injection (15%)</td><td>$0.87M</td></tr>`

8. capital table: debenture debt service
   - old: `<tr><td>Annual debt service &mdash; debenture</td><td>&asymp; $188k</td></tr>`
   - new: `<tr><td>Annual debt service &mdash; debenture</td><td>&asymp; $164k</td></tr>`

9. capital table: combined debt service
   - old: `<tr><td>Combined annual debt service</td><td>&asymp; $492k</td></tr>`
   - new: `<tr><td>Combined annual debt service</td><td>&asymp; $469k</td></tr>`

10. capital table source line
   - old: `owner-occupancy 60% for new construction; 50/40/10 bank/CDC/equity split. See source 10.</p>`
   - new: `owner-occupancy 60% for new construction; 50/35/15 bank/CDC/equity split, with the borrower at <!--sba:equity.sba_504_new_or_special-->15%<!--/sba:equity.sba_504_new_or_special--> as a New Business (13 CFR 120.910). See sources 10 and 14.</p>`

11. financing prose: stack and tier
   - old: `illustrative 9.5 percent, a $2.32 million CDC/SBA debenture at an illustrative 6.5 percent, and a $0.58 million equity injection &mdash; the canonical 50/40/10. The injection holds at 10 percent rather than escalating: a single-use climate-controlled facility can draw a special-purpose designation and a higher equity requirement, but a mixed-format, covered-canopy-led site is less likely to, which is one reason the format decision has a capital cost, not just a revenue effect.<sup class="fn"><a href="#s10">10</a></sup> On 25-year amortization the two tranches carry a combined debt service near $492,000 a year`
   - new: `illustrative 9.5 percent, a $2.03 million CDC/SBA debenture at an illustrative 6.5 percent, and a $0.87 million equity injection, a 50/35/15 split. The equity injection is <!--sba:equity.sba_504_new_or_special-->15%<!--/sba:equity.sba_504_new_or_special-->, the 504 minimum for a New Business (two years or less in operation) under 13 CFR 120.910;<sup class="fn"><a href="#s14">14</a></sup> the <!--sba:equity.startup_7a-->10%<!--/sba:equity.startup_7a--> start-up figure in <!--sba:sop.short-->SOP 50 10 8.1<!--/sba:sop.short--> is the 7(a) rule, not a 504 rule. The 504 minimum is <!--sba:equity.sba_504_standard-->10%<!--/sba:equity.sba_504_standard--> in standard cases, <!--sba:equity.sba_504_new_or_special-->15%<!--/sba:equity.sba_504_new_or_special--> for a New Business or a limited or special purpose property, and <!--sba:equity.sba_504_new_and_special-->20%<!--/sba:equity.sba_504_new_and_special--> for both. A single-use climate-controlled facility can draw a special-purpose designation and a higher equity requirement, but a mixed-format, covered-canopy-led site is less likely to, which is one reason the format decision has a capital cost, not just a revenue effect.<sup class="fn"><a href="#s10">10</a></sup> On 25-year amortization the two tranches carry a combined debt service near $469,000 a year`

12. DSCR table: Year 1
   - old: `<td>~$444k</td><td>~$492k</td><td>0.90</td>`
   - new: `<td>~$444k</td><td>~$469k</td><td>0.95</td>`

13. DSCR table: Year 2
   - old: `<td>~$567k</td><td>~$492k</td><td>1.15</td>`
   - new: `<td>~$567k</td><td>~$469k</td><td>1.21</td>`

14. DSCR table: Year 3
   - old: `<td>~$713k</td><td>~$492k</td><td>1.45</td>`
   - new: `<td>~$713k</td><td>~$469k</td><td>1.52</td>`

15. outcome lede: stabilized DSCR
   - old: `graded lease-up to a stabilized 1.45x`
   - new: `graded lease-up to a stabilized 1.52x`

16. outcome prose: stabilized coverage
   - old: `The stabilized 1.45x coverage is the figure`
   - new: `The stabilized 1.52x coverage is the figure`

17. outcome prose: DSCR ramp
   - old: `coverage tracks that ramp from 0.90x to 1.15x to 1.45x.`
   - new: `coverage tracks that ramp from 0.95x to 1.21x to 1.52x.`

18. outcome prose: break-even occupancy
   - old: `is crossed near 64 percent economic occupancy`
   - new: `is crossed near 61 percent economic occupancy`

19. outcome prose: Year 1 DSCR
   - old: `The Year 1 figure of 0.90x is intentionally below 1.0`
   - new: `The Year 1 figure of 0.95x is intentionally below 1.0`

20. outcome prose: equity dollars
   - old: `the $0.58 million injection earns`
   - new: `the $0.87 million injection earns`

21. outcome prose: debt service
   - old: `against $492,000 of debt`
   - new: `against $469,000 of debt`

22. verdict capsule
   - old: `a stabilized 1.45x DSCR, and a ~16% levered equity IRR, the projections support`
   - new: `a stabilized 1.52x DSCR, and a ~16% levered equity IRR, the projections support`

23. source 10: equity tier
   - old: `; ~10% equity injection; owner-occupancy of 60% for new construction;`
   - new: `; 10% start-up equity injection (a 7(a) rule, not the 504 minimum; see source 14); owner-occupancy of 60% for new construction;`

24. sources: add s14
   - old: `</li> </ol><!--fsc:signature-->`
   - new: `</li> <li id="s14">13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910</li> </ol><!--fsc:signature-->`

Source list: new entry s14 (13 CFR 120.910, Borrower contributions, eCFR, text as specified), appended after s13, nothing renumbered;
footnote markers to #s14 added in the Financing lede and after the tier sentence. Source 10 no longer says "~10% equity injection":
it now reads "10% start-up equity injection (a 7(a) rule, not the 504 minimum; see source 14)", with the rest of the entry,
including the Small Loan threshold clause, untouched.

## Not touched

Header, nav, footer, anything between fsc: markers, the content of existing sba: regions (their text is unchanged; the new
sba: regions I added render the values from data/regulatory/sba.json), datePublished and dateModified (JSON-LD and byline), the
breadcrumb, every existing em and en dash.

## Verification

- python3 docs/web-fsc-4/recompute/rv-boat-storage-florida-sba.py : exit 0, BEFORE reproduces all twelve published figures.
- python3 docs/web-fsc-4/recompute/rv-boat-storage-florida-sba.py --check : exit 0 (32 AFTER snippets present, the IRR expected exactly as published, no stale BEFORE
  figure, no 10% stated as this project's equity or as the 504 minimum). Against the original page it exits 1 with 84 mismatches.
  It also passes on copies of the page with every em dash swept to a comma or colon, en dashes to hyphens, and links wrapped around
  words in prose, and fails on partial reverts (equity tier, DSCR cell, IRR, source 10, the tier sentence).
- python3 scripts/regulatory.py --check : exit 0 (0 pages out of date).
- The JSON-LD block (Organization, Article, BreadcrumbList) parses; exactly one title outside comments; href #s14 appears twice, id s14 once.

## Could not resolve

- The IRR (above): the published 16% cannot be derived from the page's inputs, so it is left unchanged. It was not recomputed for the 15% structure. Owner item.
- Cash-on-cash is not stated on the page, so it is not restated.
- "New Business" rests on the page describing a ground-up project for a sponsor with no operating history stated; the page does not give the sponsor's years in business.
