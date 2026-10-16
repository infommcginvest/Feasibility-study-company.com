# Recompute log: rv-boat-storage-arizona-sba (WEB-FSC-4)

Page: `case-studies/rv-boat-storage-arizona-sba/index.html`. Script: `docs/web-fsc-4/recompute/rv-boat-storage-arizona-sba.py` (run it with no argument for the before/after table and the IRR diagnostics; `--check` reads the page).

## The rule

13 CFR 120.910 (unchanged in SOP 50 10 8.1): the 504 borrower contribution is at least 10% in standard cases, at least 15% if the borrower (or Operating Company) has operated two years or less (a New Business) or the project is a limited or special purpose building, and at least 20% if both. The 10% start-up figure in SOP 50 10 8.1 is the 7(a) Start-Up Business rule. A ground-up storage business is a New Business, and the page itself says the yard is unlikely to draw the special purpose designation, so the tier is 15% and the stack is 50% Third Party Lender / 35% CDC debenture / 15% borrower. The page had 50 / 40 / 10.

## Does BEFORE reproduce the page?

Yes, for everything except the IRR. Bank $2.50M at 9.5% over 25 years (monthly amortization) gives $262,109 a year; debenture $2.00M at 6.5% over 25 years gives $162,050; blended $424,159, which the page rounds to $262k + $162k = $424k. DSCR on the published NOI (~$382k, ~$488k, ~$615k) is 0.90, 1.15, 1.45, the same on unrounded and on $k-rounded debt service. The Year-3 NOI build (rent roll $957.6k, vacancy 8%, ancillary $44.0k, EGI $925.0k, expenses 33.5%) gives NOI $615.1k against the page's ~$615k. Uses sum to $5.00M.

## Figures that moved

| Figure | Page before | Page after |
|---|---|---|
| CDC debenture | $2.00M (40%) | $1.75M (35%) |
| Borrower equity | $0.50M (10%) | $0.75M (15%) |
| Bank first mortgage | $2.50M (50%) | $2.50M (50%), unchanged |
| Sources total / uses total | $5.00M / $5.00M | $5.00M / $5.00M |
| SBA 504 debt share (hero tile, bank + CDC) | 90% | 85% |
| Debenture debt service | $162k ($162,050; "about $162,000") | $142k ($141,794; "about $142,000") |
| Bank debt service | $262k | $262k, unchanged |
| Blended annual debt service | $424k ($424,159) | $404k ($403,903) |
| DSCR Year 1 (NOI ~$382k) | 0.90 | 0.95 |
| DSCR Year 2 (NOI ~$488k) | 1.15 | 1.21 |
| DSCR Year 3, stabilized (NOI ~$615k) | 1.45 | 1.52 |
| Cash after debt service, Year 1 / 2 / 3 (log only, not on the page) | -$42,159 / $63,841 / $190,841 | -$21,903 / $84,097 / $211,097 |
| Cash-on-cash, Year 1 / 2 / 3 (log only, not on the page) | -8.4% / 12.8% / 38.2% | -2.9% / 11.2% / 28.1% |
| Loan balances after 10 years (log only) | $3,641,963 | $3,448,184 |
| Levered equity IRR | ~16% (not reproducible, see below) | left at ~16% on the page (open item 1) |

Not on the page and therefore not changed: equity multiple, LTV (no appraised value is given), stress-test DSCRs, break-even DSCR figures (the page says only "within 24 months", which still holds: Year-2 DSCR is 1.21). The page has no FAQ block, no JSON-LD FAQ and no image alt text.

## Sentences changed (old, then new)

Descriptions (meta, Open Graph, JSON-LD Article): "a 1.45x stabilized DSCR" became "a 1.52x stabilized DSCR" in the meta description and in the JSON-LD description; "$5.00M cost, 1.45x DSCR, ~16% IRR" became "$5.00M cost, 1.52x DSCR, ~16% IRR" in og:description. The twitter description has no figure.

Hero tile 2: "90%" / "SBA 504 debt (em dash) 50% bank + 40% CDC of the $5.00M" became "85%" / "SBA 504 debt (em dash) 50% bank + 35% CDC of the $5.00M" (the existing dash is untouched). Hero tile 3: "1.45x" became "1.52x".

Capital structure table caption: "How the $5.00M is financed under a standard SBA 504 split, and the debt-service load it creates." became "How the $5.00M is financed under the SBA 504 split for a New Business, and the debt-service load it creates."

Capital structure rows: "CDC / SBA 504 debenture (40%) ... $2.00M" became "(35%) ... $1.75M"; "Borrower equity injection (10%) ... $0.50M" became "Borrower equity injection (15%), footnote 20, $0.75M"; "Annual debt service (blended) ≈ $424k ($262k bank + $162k debenture)" became "≈ $404k ($262k bank + $142k debenture)".

Capital structure source note: "...: bank first mortgage, CDC debenture, borrower equity; owner-occupancy 60% for new construction; rates illustrative. See sources 14 and 15." became "...: bank first mortgage, CDC debenture, borrower equity at the New Business tier of 13 CFR 120.910; owner-occupancy 60% for new construction; rates illustrative. See sources 14, 15 and 20."

Financing paragraph, old: "The equity injection sits at the SBA-minimum 10 percent, which SOP 50 10 8.1 (effective October 1, 2026) restored for start-ups and changes of ownership. That 10 percent is defensible here precisely because a mixed-format storage yard is unlikely to draw the special-purpose designation that raises the required injection to 15 or 20 percent; single-use climate-controlled product is the format that draws heightened scrutiny, and this program is deliberately mixed.[14] On a 25-year amortization, the $2.50 million bank note at an illustrative 9.5 percent costs about $262,000 a year, and the $2.00 million CDC debenture at an illustrative 6.5 percent fixed costs about $162,000, for a blended annual debt service near $424,000 (em dash) the number the projected coverage must clear."

Financing paragraph, new: "The equity injection sits at 15% of total project cost, the 504 minimum for a New Business (a borrower, or Operating Company, with two years or less in operation) under 13 CFR 120.910.[20] This ground-up storage business is a New Business, so the 10% contribution of a standard case does not apply; the 10 percent start-up figure in SOP 50 10 8.1 (effective October 1, 2026) is the 7(a) rule, not a 504 rule. The injection stays at 15 percent, and does not rise further, because a mixed-format storage yard is unlikely to draw the limited or special purpose designation; together with New Business status that designation would make the minimum 20%. Single-use climate-controlled product is the format that draws heightened scrutiny, and this program is deliberately mixed.[14] On a 25-year amortization, the $2.50 million bank note at an illustrative 9.5 percent costs about $262,000 a year, and the $1.75 million CDC debenture at an illustrative 6.5 percent fixed costs about $142,000, for a blended annual debt service near $404,000 (em dash) the number the projected coverage must clear." The 15%, 10% and 20% tiers use the page's `<!--sba:equity.sba_504_new_or_special-->`, `sba_504_standard` and `sba_504_new_and_special` markers; the existing `sop.short` and `sop.effective` regions are carried over with their content unchanged.

Outcome lede: "a stabilized 1.45x in Year 3" became "a stabilized 1.52x in Year 3".

DSCR ramp rows: debt service "~$424k" became "~$404k" in all three rows; DSCR 0.90 became 0.95, 1.15 became 1.21, 1.45 became 1.52. Its source note: "DSCR computed as NOI divided by the ~$424k blended annual debt service" became "...~$404k...".

Outcome prose: "The stabilized 1.45x coverage is the figure" became "The stabilized 1.52x coverage is the figure"; "covers fully amortizing debt service at 1.15x. The Year-1 figure of 0.90x is intentionally below 1.0" became "...at 1.21x. The Year-1 figure of 0.95x is intentionally below 1.0".

Equity paragraph, old: "On the equity side, the $0.50 million injection is the SBA-minimum 10 percent, and the levered return is graded by..." New: "On the equity side, the $0.75 million injection is the 15 percent minimum the 504 program requires of a New Business under 13 CFR 120.910,[20] and the levered return is graded by..." The rest of that paragraph, including "levered equity IRR near 16 percent over a 10-year hold", is unchanged.

Verdict capsule: "a stabilized 1.45x DSCR that clears the storage lending floor with headroom" became "a stabilized 1.52x DSCR that ...". The "~16% levered equity IRR" in the capsule is unchanged.

Source 14, old: "...; 10% equity injection restored for start-ups and changes of ownership, higher for special-purpose; owner-occupancy of 51% (existing) or 60% (new construction); ..." New: "...; 10% equity injection restored for 7(a) start-ups and changes of ownership (the 7(a) rule, not the 504 tier; see source 20); owner-occupancy of 51% (existing) or 60% (new construction); ...". The clause "higher for special-purpose" was dropped from this entry because the entry's SOP 7(a) context is not where the 15% and 20% 504 tiers come from; they now sit in the Financing paragraph with source 20.

Source 20 added at the end of the list, plain text like its neighbours: "13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910". Footnote markers `<sup class="fn"><a href="#s20">20</a></sup>` point at it from the Financing paragraph, the equity row of the capital table and the equity paragraph. Nothing else was renumbered.

Left as written: source 15 ("equity generally 10%, higher for start-ups and special-purpose property"), which is true as a general statement and does not give 10% as this project's equity.

Edit count on the page: 24 replacements (3 description attributes, 3 hero-tile cells, 1 caption, 3 capital-table rows, 1 capital-table note, 2 in the Financing paragraph, 1 outcome lede, 3 DSCR rows, 1 DSCR note, 2 outcome-prose sentences, 1 equity paragraph, 1 capsule, 1 source-14 entry, 1 new source-20 entry). Nothing touched: header, nav, footer, anything inside `fsc:` markers, the content of existing `sba:` regions, `datePublished`/`dateModified`, the breadcrumb, existing em and en dashes. No em or en dash appears in text I wrote.

## Does the conclusion change?

No. The verdict stays "financially feasible and bankable". The answer moves in the favourable direction on coverage (stabilized DSCR 1.45x to 1.52x, headroom over the ~1.20 to 1.25x floor grows; Year 2 now reaches 1.21x; the Year-1 shortfall falls from about $42k to about $22k and is still covered by the funded lease-up reserve; coverage still passes 1.0 inside 24 months). The equity check rises from $0.50M to $0.75M, which the page now states truthfully.

## The IRR (open item 1: not recomputed, left as published)

What the page gives: a 10-year hold, "modest" rent growth, a funded canopy-and-paving replacement reserve, a Year-10 exit "wide of the going-in yield on cost" against a market of about 6.0 to 7.5% (Class A) and 7.5 to 8.5% (Class B), and "a levered equity IRR near 16 percent". It gives no growth rate, no exit cap, no reserve amount, no sale cost.

The procedure was to calibrate one unstated assumption (the exit cap) until BEFORE gives 16%, hold it, and run AFTER. It does not give a model the page can stand on:

1. With $0.50M of equity and $64k, then $191k a year of cash after debt service, the cash flows of Years 1 to 10 alone are worth $663k at a 16% discount rate (NOI flat after Year 3), more than the $500k invested. A 16% levered IRR therefore needs the Year-10 sale to cost the owner money: net sale proceeds to equity of about -$721k, an exit price of $2.92M against loan balances of $3.64M, a cap of 21.1% on Year-11 NOI. With 2% and 3% growth the required net proceeds are -$1.22M and -$1.48M. That cap is far outside the page's own 6.0 to 8.5% and above the 12.3% going-in yield on cost.
2. Run literally anyway (growth 0%, exit price held), BEFORE has two IRR roots (-21.7% and 16.0%) and AFTER has -39.0% and 11.5%. The cash flows change sign twice, so the figure is not unique. Not usable on a page.
3. With the exit cap inside the page's range (7.0% to 8.5%, growth 0% or 2%, sale cost 0% or 3%, Year-1 shortfall paid from the reserve) the levered IRR is 34% to 41% BEFORE and 28% to 34% AFTER. These depend on assumptions the page does not give, and they are not near 16%.
4. The unlevered project IRR ($5.00M cost, independent of the capital stack) is 14.9% / 16.4% / 17.2% at a 7.0% exit and 0% / 2% / 3% growth, and 13.5% / 15.0% / 15.8% at 8.5%. So about 16% is what the project earns before financing, inside the page's own cap range. It is the figure the tile resembles, and it does not move when the stack moves.

The hard constraint says that if a fix needs a fact the page does not give, leave the original and report it. The IRR in all six places (hero tile, meta, og, JSON-LD, prose, capsule) is therefore unchanged at about 16%. The script prints all four diagnostics; `--check` does not check any IRR value.

The owner has two honest ways to close this: (a) supply the growth rate, exit cap, reserve and sale cost, and accept a levered IRR in the 30s; or (b) relabel the tile as an unlevered project IRR of about 16% (which the page's own cap range supports at 2 to 3% growth), which is independent of the 10/15% question. I did not choose, because either needs a fact or a judgment the page does not contain.

## Other items for the owner

2. The same paragraph says the exit capitalization is "held wide of the going-in yield on cost". Yield on cost is $615k / $5.00M = 12.3%, and the cap rates the sentence cites are 6.0 to 8.5%, so the sentence does not hold as written. Not financing-dependent; left unchanged.
3. "Working capital, lease-up reserve & fees" is $0.15M inside the $5.00M project cost that the 504 stack funds. My understanding is that 504 proceeds cannot fund working capital or an operating reserve. I did not verify this against the SOP text and did not change the uses table.
4. `git diff` of this page against HEAD also shows header, footer, nav and CTA link changes (pending spans, `/#contact`, chrome links). They were made by another tool running at the same time, not by me.
