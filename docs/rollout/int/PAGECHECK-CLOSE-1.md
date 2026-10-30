# PAGECHECK-CLOSE-1: the four pagecheck tool fixes (O4)

FSC-RESUME-1, 25 Oct 2026. Tool-fix subagent (Sonnet) for the integrator. Changed: `scripts/qa/pagecheck.py` only. `scripts/qa/gates.py` is unchanged and still runs (smoke below). No page source or served HTML was touched. Nothing is committed: the integrator commits.

Method. Before = `scripts/qa/pagecheck.py` at HEAD c57bf2e. After = the working file. Both ran as gate 3 calls them: `pc.check` over every factory page (63 pages with a source under `src/pages/`), landing stage, the I6 rank rule, no `--new`, over a snapshot of the whole tree taken at 11:58 on 25 Oct (the working tree then held the integrator's uncommitted edits to `case-studies/private-school-connecticut-conventional/index.html`, `src/pages/states/north-carolina.html` and `docs/rollout/int/DECISIONS.md`). The snapshot and every control are under `~/Downloads/fsc-rollout/tmp/int/pagecheck-controls/` (`snapshot/` is a 422 MB throwaway copy that can be deleted). Reproduce: `python3 run_factory.py before snapshot out.json` and `python3 run_factory.py ~/Downloads/wt-rollout-int/scripts/qa snapshot out.json`.

## Result in one table

| | research | register (capped) | counted |
|---|---|---|---|
| Before, 63 factory pages | 3681 | 379 | 4060 |
| After, 63 factory pages | 3608 | 377 | 3985 |

39 pages moved (marked `*` below). No factory page is under its landing floor (25 counted with 15 research) before or after. The smallest margins after the change: Charleston 32 counted (7 over) with 22 research, Raleigh-Durham 32 with 24, Nashville 32 with 26 (counted floor +7 on all three, research floor +7 to +11).

Effect of each fix on its own, against the same snapshot:

| Fix | research | register | pages moved |
|---|---|---|---|
| 1 nocount on `mkt:` regions | 0 | -2 | 1 (mixed-use hub) |
| 2 two-digit rounding | -1 | 0 | 1 (gas-station-and-c-store hub) |
| 3 statute and code numbers | -8 | 0 | 3 (Ohio, Minnesota, Wisconsin) |
| 4 other pages' sources lists | -64 | -2 | 38 |

The fixes overlap: the two register values fix 1 removes from the mixed-use hub (1,665 and 2.12) are also in other pages' sources, so fix 4 removes them too. All four together: research -73, register -2.

## Fix 1: `data-fsc-nocount` honoured on `mkt:` regions

Rule. `register_figures` drops every element carrying `data-fsc-nocount` (comments included) before it reads the `mkt:` regions, so a register value rendered inside such an element, or a region that holds one, is not a register figure. It stays in the page text for the repeat test, so other pages still treat the value as printed (I82). `research_figures` already did this for research blocks.

Control (`C1`, fails before): a page with three `mkt:` values, two wrapped in `<span data-fsc-nocount>`. Before (research 0, register 3), after (0, 1). Unchanged control (`C1u`): two plain `mkt:` values, (0, 2) before and after.

Real effect: the mixed-use hub goes from 40 counted to 38 (34 research, 4 register), the figure the rulings give (I90). Gate 3 on the hub prints `counted 38 (research 34, register 4/4)`.

## Fix 2: two-significant-digit rounding in the repeat test

Rule (also in the module docstring and the `NumberIndex` docstring). A figure written with exactly two significant digits ("$4.8 billion", "about 9,700") is a rounding of a more precise figure of the same kind on another page ("$4.81 billion", "9,692") when both round to the same two digits AND either the same scale word stands on both (thousand, million, billion, trillion, k, m, b, t) or either text marks its value as approximate ("about", "roughly", "nearly", "almost", "some", "around", "more than", "approximately", "~") and the value is 1,000 or more. Plain numbers under 1,000 and percentages never take this path, so 2.5% against 2.54% and 12 counties against 12.4 stay distinct. Three and more digits keep the earlier rule.

That rule alone is not usable, and the counts show why. Two digits agree by chance about once in ninety pairs, and the index holds every figure on about 125 served pages, so the bare rule from the brief marked a third of the site as repeats:

| Variant, measured on the whole factory set (tree at 11:35) | counted figures | change from the other three fixes alone |
|---|---|---|
| Other three fixes only | 3985 | |
| Two-digit rule as briefed (marker or same scale word) | 2557 | -1428 (-36%) |
| Plus two shared content words in the two sentences | 3848 | -137 |
| Plus three shared content words | 3957 | -28 (28 figures on 23 pages), one a true repeat |
| Final rule (below) | 3984 | -1, a true repeat |

The 28 figures at three shared words showed chance matches such as 16,243 Atlanta apartment units under construction against "more than 16,000 dwelling units in the pipeline" in a Texas car-wash case. So a two-digit match counts only with evidence of one fact (`NumberIndex.two_hits`, `rounded_repeats`): the two places must share at least two content words (four letters or more, no stop words, within 110 characters of the figure) AND either share three words of which two are rare on the site (on 5 pages or fewer), or two different figures of one sentence on this page match two different figures of one sentence on the same other page (the pair "9,692 loans for $4.81 billion" against "$4.8 billion across about 9,700 loans", the t1 attacker 1 case). The two-digit test is made against other pages only; a page's own roundings keep the earlier rule.

On the real site the final rule moves one figure: 7,308 (Couche-Tard's U.S. stores) on the gas-station-and-c-store hub, which `/research-notes/c-store-franchise-category/` prints as "more than 7,300 US stores". No other count moves, so the rule costs no landed page anything and catches the pattern the attacker found.

Controls. `C2a` (fails before): a state page with "9,692 7(a) loans for $4.81 billion" and an unrelated 48,210 figure, a case page with "roughly $4.8 billion across about 9,700 loans": before (3, 0), after (1, 0). `C2b` (fails before): one rare-word sentence (7,308 against "more than 7,300") on a state and its metro: (1, 0) to (0, 0). `C2u` (must stay unchanged): 2.5 percent against 2.54 percent, "12 counties" against 12.4, 16,243 apartment units against "more than 16,000" dwelling units, 48.2 thousand against about 48,000, $1.4 million against $1.35 million in unrelated sentences: (4, 0) before and after. The controls pad the tiny site with seven filler pages so the common words are not rare there.

## Fix 3: statute and code section numbers are not figures

Rule. `NOT_FIGURE` also skips a number right after "sec.", "s.", "ss.", "ch.", "U.S.C.", "Stat.", "Statute", "Code", "Ann.", "Act", "Title", "Rule", "HB", "SB", "AB", "LD", "Ordinance", "Order", "Docket", "P.L.", "Article", "Art." or a code reporter (R.C., R.S., G.S., F.S., C.R.S., K.R.S., M.G.L., O.C.G.A., and similar); "section", "§", "chapter", "CFR" and "No." were already there. `STATUTE_SHAPE` skips a bare dotted number of four or five digits (2116.1, 4303.29) or of the shape ddd.ddd (104.001) when no unit or scale word follows; a dotted number followed by "(b)" (already skipped) or by a further dotted or dashed segment (120.160.2) is skipped. Real decimals with a unit or a scale ("566.2 thousand", "17.586 acres", "803.8k", the multiplier 4.865) are untouched. A first draft used any dotted initialism as a prefix and wrongly dropped "$67.9M" after "Newtek Bank, N.A." on the Illinois page; the control now holds that case.

Control (`C3`, fails before): "Ohio Rev. Code 4303.29", "Minn. Stat. 144.551", "Wis. s. 104.001", "Act 152 permits", "HB 407 loans", "Docket 12,345", "Ordinance 2,451", "Fla. Stat. section 2116.1", "13 CFR 120.110", "Rule 120.160(b)", "Order 1,500": before (8, 0), after (0, 0). Unchanged control (`C3u`): 4.865, "566.2 thousand", 17.586 acres, 276.51 (an index reading), 4.5 percent, "N.A. $67.9M", "(e.g. $5 million more)": (7, 0) before and after.

Real effect: eight values leave the count: Ohio 122.175 and 4303.29, Minnesota 144.551, Wisconsin 104.001, 150.31, 66.0304, 66.0615 and 66.1014.

## Fix 4: other pages' numbered sources lists are page content (I71)

Rule. `Site.numbers`, the index of what other pages hold against a page, is built from `index_text` (the page's `<main>` text including `#sources`, bare URLs removed) instead of `overlap_text` (which dropped the sources). Overlap shingles still use `overlap_text`, and `research_figures` still drops the page's own `#sources`, so a page's own sources stay out of its own count.

Control (`C4`, fails before): a state page counts 48,210 and 7,350; a case page prints 48,210 only in its sources annotation: before (2, 0), after (1, 0). Unchanged control (`C4u`): the state page's own sources repeat its own 48,210: (1, 0) before and after.

Real effect: 64 research figures and 2 register figures on 38 pages, the largest being the self-storage hub -8, rv-park-texas -4, Nebraska -4, and the multifamily hub, Kansas and North Carolina -3 each. Caveat for the integrator: the sources lists feed the existing three-digit rounding rule, which has its own chance matches. One example from the sample: Houston's 7,150,233 is now "taken" by "approximately 7.15 million" in the sources of the Massachusetts behavioral-health case, two different populations that agree at three digits. That rule is outside this change (the brief asks only that sources be indexed), so I left it and record it here.

## Controls, all nine

`~/Downloads/fsc-rollout/tmp/int/pagecheck-controls/make_controls.py` builds each synthetic site under `sites/` and runs the before and after tool on it. Result of the final run:

```
PASS  C1 nocount mkt (fails before)                                  before (0, 3) after (0, 1)  (expect (0, 3) -> (0, 1))
PASS  C1u plain mkt values (unchanged)                               before (0, 2) after (0, 2)  (expect (0, 2) -> (0, 2))
PASS  C2a rounded pair (fails before)                                before (3, 0) after (1, 0)  (expect (3, 0) -> (1, 0))
PASS  C2b one sentence, rare words (fails before)                    before (1, 0) after (0, 0)  (expect (1, 0) -> (0, 0))
PASS  C2u small numbers and chance matches (unchanged)               before (4, 0) after (4, 0)  (unchanged)
PASS  C3 statute numbers (fails before)                              before (8, 0) after (0, 0)  (expect (8, 0) -> (0, 0))
PASS  C3u real decimals (unchanged)                                  before (7, 0) after (7, 0)  (expect (7, 0) -> (7, 0))
PASS  C4 value in another page's sources (fails before)              before (2, 0) after (1, 0)  (expect (2, 0) -> (1, 0))
PASS  C4u own sources do not take the page's figure (unchanged)      before (1, 0) after (1, 0)  (expect (1, 0) -> (1, 0))
```

(The result lines show the (research, register) counts of the tested page; every expectation is stated in the script.)

## gates.py still runs

- `python3 scripts/qa/gates.py --help` exits 0 and prints the usage.
- `python3 scripts/qa/gates.py --urls /states/ohio/,/asset-classes/mixed-use/ --only 3 --stage landing --site-wide` exits 0: gate 3 GREEN, mixed-use `counted 38 (research 34, register 4/4)`, Ohio `counted 93 (research 84, register 9/9)`, "61 other factory page(s) at landing floors; under the floor: 0". Output saved at `~/Downloads/fsc-rollout/tmp/int/pagecheck-controls/gates/gate3-two-pages.txt`.

## Every factory page, counted before and after

Counts are (research, register after the cap) as gate 3 computes them. `*` marks a page whose counts moved. Floor: 25 counted and 15 research.

| Page | Type | Research before | Register before | Counted before | Research after | Register after | Counted after | Moved | Floor |
|---|---|---|---|---|---|---|---|---|---|
| `/asset-classes/gas-station-and-c-store/` | hub | 76 | 0 | 76 | 74 | 0 | 74 | * | clear |
| `/asset-classes/gas-station-and-c-store/ev-charging/` | subtype | 33 | 0 | 33 | 33 | 0 | 33 |  | clear |
| `/asset-classes/gas-station-and-c-store/interstate-highway/` | subtype | 32 | 0 | 32 | 32 | 0 | 32 |  | clear |
| `/asset-classes/hotel/` | hub | 98 | 10 | 108 | 97 | 10 | 107 | * | clear |
| `/asset-classes/mixed-use/` | hub | 34 | 6 | 40 | 34 | 4 | 38 | * | clear |
| `/asset-classes/multifamily/` | hub | 125 | 6 | 131 | 122 | 6 | 128 | * | clear |
| `/asset-classes/private-school/` | hub | 122 | 10 | 132 | 122 | 10 | 132 |  | clear |
| `/asset-classes/quick-service-restaurant/` | hub | 104 | 7 | 111 | 102 | 7 | 109 | * | clear |
| `/asset-classes/quick-service-restaurant/burger/` | subtype | 71 | 0 | 71 | 70 | 0 | 70 | * | clear |
| `/asset-classes/self-storage/` | hub | 146 | 10 | 156 | 138 | 10 | 148 | * | clear |
| `/case-studies/assisted-living-texas-hud/` | case | 59 | 0 | 59 | 58 | 0 | 58 | * | clear |
| `/case-studies/auto-dealership-texas-sba/` | case | 50 | 0 | 50 | 49 | 0 | 49 | * | clear |
| `/case-studies/car-wash-texas-sba/` | case | 58 | 0 | 58 | 57 | 0 | 57 | * | clear |
| `/case-studies/gas-station-alabama-sba/` | case | 37 | 0 | 37 | 37 | 0 | 37 |  | clear |
| `/case-studies/gas-station-florida-sba/` | case | 50 | 0 | 50 | 50 | 0 | 50 |  | clear |
| `/case-studies/gas-station-georgia-sba/` | case | 53 | 0 | 53 | 52 | 0 | 52 | * | clear |
| `/case-studies/gas-station-texas-sba/` | case | 41 | 0 | 41 | 41 | 0 | 41 |  | clear |
| `/case-studies/gas-station-versailles-ohio-sba/` | case | 40 | 0 | 40 | 40 | 0 | 40 |  | clear |
| `/case-studies/hotel-texas-sba/` | case | 46 | 0 | 46 | 46 | 0 | 46 |  | clear |
| `/case-studies/lodging-retreat-johnson-city-texas-sba/` | case | 48 | 0 | 48 | 46 | 0 | 46 | * | clear |
| `/case-studies/meat-processing-texas-usda/` | case | 34 | 0 | 34 | 34 | 0 | 34 |  | clear |
| `/case-studies/rv-boat-storage-texas-sba/` | case | 43 | 0 | 43 | 43 | 0 | 43 |  | clear |
| `/case-studies/rv-park-texas-usda/` | case | 44 | 0 | 44 | 40 | 0 | 40 | * | clear |
| `/case-studies/travel-center-hankamer-texas-usda/` | case | 41 | 0 | 41 | 40 | 0 | 40 | * | clear |
| `/case-studies/truck-stop-texas-sba/` | case | 40 | 0 | 40 | 39 | 0 | 39 | * | clear |
| `/states/alabama/` | state | 65 | 10 | 75 | 64 | 10 | 74 | * | clear |
| `/states/alabama/huntsville/` | metro | 26 | 10 | 36 | 24 | 10 | 34 | * | clear |
| `/states/california/` | state | 130 | 10 | 140 | 130 | 10 | 140 |  | clear |
| `/states/california/sacramento/` | metro | 25 | 10 | 35 | 25 | 10 | 35 |  | clear |
| `/states/florida/` | state | 69 | 9 | 78 | 69 | 9 | 78 |  | clear |
| `/states/florida/jacksonville/` | metro | 23 | 10 | 33 | 23 | 10 | 33 |  | clear |
| `/states/florida/miami/` | metro | 27 | 10 | 37 | 27 | 10 | 37 |  | clear |
| `/states/florida/orlando/` | metro | 26 | 10 | 36 | 26 | 10 | 36 |  | clear |
| `/states/florida/tampa/` | metro | 28 | 10 | 38 | 27 | 10 | 37 | * | clear |
| `/states/georgia/` | state | 80 | 10 | 90 | 78 | 10 | 88 | * | clear |
| `/states/georgia/savannah/` | metro | 27 | 10 | 37 | 27 | 10 | 37 |  | clear |
| `/states/illinois/` | state | 68 | 7 | 75 | 68 | 7 | 75 |  | clear |
| `/states/indiana/` | state | 75 | 10 | 85 | 74 | 10 | 84 | * | clear |
| `/states/indiana/indianapolis/` | metro | 45 | 10 | 55 | 44 | 10 | 54 | * | clear |
| `/states/kansas/` | state | 90 | 5 | 95 | 87 | 5 | 92 | * | clear |
| `/states/kentucky/` | state | 63 | 10 | 73 | 62 | 10 | 72 | * | clear |
| `/states/louisiana/` | state | 72 | 8 | 80 | 72 | 8 | 80 |  | clear |
| `/states/michigan/` | state | 84 | 6 | 90 | 83 | 6 | 89 | * | clear |
| `/states/michigan/detroit/` | metro | 25 | 10 | 35 | 25 | 10 | 35 |  | clear |
| `/states/minnesota/` | state | 87 | 10 | 97 | 86 | 10 | 96 | * | clear |
| `/states/missouri/` | state | 47 | 5 | 52 | 47 | 5 | 52 |  | clear |
| `/states/nebraska/` | state | 90 | 7 | 97 | 86 | 7 | 93 | * | clear |
| `/states/new-york/` | state | 60 | 10 | 70 | 60 | 10 | 70 |  | clear |
| `/states/north-carolina/` | state | 62 | 9 | 71 | 59 | 9 | 68 | * | clear |
| `/states/north-carolina/charlotte/` | metro | 24 | 10 | 34 | 23 | 10 | 33 | * | clear |
| `/states/north-carolina/raleigh-durham/` | metro | 26 | 8 | 34 | 24 | 8 | 32 | * | clear |
| `/states/ohio/` | state | 87 | 9 | 96 | 84 | 9 | 93 | * | clear |
| `/states/oklahoma/` | state | 85 | 10 | 95 | 84 | 10 | 94 | * | clear |
| `/states/south-carolina/` | state | 97 | 10 | 107 | 97 | 10 | 107 |  | clear |
| `/states/south-carolina/charleston/` | metro | 22 | 10 | 32 | 22 | 10 | 32 |  | clear |
| `/states/tennessee/` | state | 91 | 8 | 99 | 90 | 8 | 98 | * | clear |
| `/states/tennessee/nashville/` | metro | 27 | 6 | 33 | 26 | 6 | 32 | * | clear |
| `/states/texas/` | state | 60 | 9 | 69 | 59 | 9 | 68 | * | clear |
| `/states/texas/austin/` | metro | 41 | 7 | 48 | 39 | 7 | 46 | * | clear |
| `/states/texas/dallas-fort-worth/` | metro | 39 | 7 | 46 | 38 | 7 | 45 | * | clear |
| `/states/texas/houston/` | metro | 39 | 7 | 46 | 38 | 7 | 45 | * | clear |
| `/states/texas/san-antonio/` | metro | 31 | 7 | 38 | 28 | 7 | 35 | * | clear |
| `/states/wisconsin/` | state | 93 | 6 | 99 | 87 | 6 | 93 | * | clear |

Not done, by design: no page source, served HTML, `gates.py` or other file was changed; the pages that landed before I69 still need the O4 re-audit for fetch-dated figures, and the register-value statute and single-property cases are the lanes' marks.
