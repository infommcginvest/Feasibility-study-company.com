# Cold verification of the CASE-NEW-1 freeze (t1 + t2, seven landed pages)

Verifier stance: every item REFUTED unless the artifacts prove it. Read only: no page, src or repo file edited. Scratch copies (git archive of 5b5a129b and ce7d9a1c) and a live sitemap download sit in the session scratchpad only. No real-site identifier is quoted below; per-figure private rows were read but not reproduced.

Rules applied (repo ~/Downloads/wt-rollout-int, docs/rollout/int/DECISIONS.md, and the case-new-1 READER-BRIEF): I6 (A4: case rank 3 outranks metro/subtype 2 and state/hub 1; pagecheck `taken()` skips lower-rank pages), I55 (arithmetic the research labels its own is not a source), I64 (size, unit count, acreage or price of one named facility or site), I66 (financing of one named facility), I69/I106 (a fetch date does not date a figure), I77 (dated = publication/release/filing/effective date, edition year in the title, or the reporting period of a periodic document; "a period printed on a web page that is not a periodic document, an undated page saying '2025 data', does not date it"), I86 (undated numbers stay out even when wrapped), AMENDMENT-1 line 70 (pending links are the designed fallback).

## Task 1: SHA-256 of FREEZE-SHA256.txt

`shasum -a 256 -c FREEZE-SHA256.txt` from the freeze folder: 99 lines, 98 OK, 1 FAILED.

- The one failure is the list's own entry (`./FREEZE-SHA256.txt`), recorded as e3b0c442...b855 (the SHA-256 of an empty file, written before the list had content). The file now hashes to 00409b4c...628f. This is a self-reference artefact, not a change to any frozen page, src, gate, PRECOUNT or private row file. Every content file matches.
- Coverage gap to note: seven files in the folder are not in the list (CLOSE-CLAIMS.md, DEPLOYS.txt, attack-A.md, attack-B.md, attackB-gates-rerun.txt, -nohub.txt, -new.txt).
- The seven frozen pages and seven src html files are byte-identical to the repo at 860fcd32 (cmp/shasum) and the seven pages are byte-identical to the live site (curl, sha256 equal).

## Task 2: blockers and majors

Counts are reproduced by `pagecheck.py --root ~/Downloads/wt-rollout-int --stage landing --figures` (tree 860fcd32), and independently on git-archive copies of the landing commits (5b5a129b: Bardstown 34/24/10, Broussard 36/26/10, Urgent care 30/20/10; ce7d9a1c with `--new` set to the four t2 pages: Ness City 50/43/7, Port Charlotte 34/29/5, Sevierville 31/21/10, Lebanon 31/21/10, Broussard still 36/26/10).

### attack-A blockers (4)

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| A-B1 | Lebanon: five 2026 estimated rates ($1.1631, $0.4050, $1.5681, $1.3417, $0.1786) | CONFIRMED | Lebanon research file line 166: period "2026 (estimates)", Lebanon Democrat article, no article date recorded, final city rate NOT FOUND. A newspaper article is not a periodic document; a year label is not a publication, filing or effective date (I77, I86). The page's source 31 also reads only "2026". |
| A-B2 | Lebanon: three tax-year-2025 rates ($1.9089, $0.2973, $0.6855) | CONFIRMED | Line 164: sources are the JECDB "Taxes & Incentives" page and the City "Property Tax" page, both undated web pages; "Tax year 2025" is a period printed on a non-periodic page (I77 last sentence). The pre-count itself excluded the equivalent Elizabethtown tax-year-label figure for the same reason. |
| A-B3 | Sevierville: four GSMNP monthly visit counts as one attraction's figures (I64) | REFUTED | Sevierville research line 129: monthly NPS visitation, document titled "2025 Great Smoky Mountains National Park" (edition year, I77b; periodic monthly data). I64/I66 name size, unit count, acreage, price and financing of a single facility; attendance at a park is a tourism-demand series, not in that list. Precedent in the repo: geo-4 t7 refuted the same shape (an employer's appropriations are not I64). The "Lebanon wrapped its hospital counts" point is a builder's choice, not a rule. |
| A-B4 | Urgent care: $11.4 billion (joint venture dissolved) as a named-employer commitment | REFUTED | Urgent care research line 113: Manufacturing Dive, 23 Mar 2026 (publication date, I77a). The amount is a company joint-venture commitment spanning several plants, not the size, price or financing of one named facility (I64/I66). Not a single-property attribute under the text. |

### attack-A majors (11)

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| A-M1 | Lebanon 6,700 surgeries counted though sibling counts wrapped (I64) | CONFIRMED (different ground) | The I64 ground fails (surgeries are not size/price). But rows at Lebanon research lines 84 and 140 date it only as "2017 data" from the JECDB "Healthcare" page, an undated web page: not dated under I77, so not countable (I86). Outcome of the finding stands; ground is I77. |
| A-M2 | Lebanon $1.1657 date basis weak | REFUTED | Line 165: FY2026-27 rate, "adopted June 2026", budget starting July 1; an effective/adoption date (I77a). Month-level is a date. |
| A-M3 | Lebanon 4,693 residents gained (WorldAtlas relay) | REFUTED | Line 63: period Jul 2024 to Jul 2025, Census estimates, the annual population estimate release period (I77c). Weak (secondary relay) but the rule does not exclude secondary sources. |
| A-M4 | Sevierville $0.87 (twice), "Jun 2026" | REFUTED | Sevierville line 143: FY2026-27 rate, Mountain Press, Jun 2026 (I77a); line 186 ties adoption to Jun 2026. |
| A-M5 | Urgent care $1.3 billion Fort Knox payroll (I64, year inferred) | REFUTED | Line 109: WKYU, 16 Oct 2025 (I77a); the page prints 2024 as the source's "last year". An installation's payroll is not its size/price/financing; the page already wraps the acreage. Hub/state repeats of the value (asset-class hubs, Michigan, Texas) are rank 1 and are ignored under A4 (and are different facts). |
| A-M6 | Urgent care 110,698 and 113,482 (A4 reading) | REFUTED | I6 and the brief's A4 line: a figure held by a state page still counts for the case; pagecheck `taken()` skips lower-rank pages. Both counted figures are on /states/kentucky/ (rank 1) and the case (rank 3) owns them. |
| A-M7 | Bardstown $33.62 an hour (I64, unwrapped) | REFUTED (borderline) | Bardstown line 117: Governor's press release, Jun 6 2022 (I77a). A wage is not in the I64/I66 list. If a reviewer wraps it the page is 33/23, still above 30/20. |
| A-M8 | Bardstown 16.10, 67.0, 67.3 rest on CitizenPortal.ai AI summaries | REFUTED | Lines 135, 137: dated by adoption date Sep 9 2025 and vote Aug 19 2025 (I77a). No counting rule excludes a secondary source. |
| A-M9 | Broussard $288,314,896.36, 4.66, 4.32 mills unverified | REFUTED | Lines 126-127: edition year "2025 Annual Report" in the document title (I77b), periodic annual report. "Search extract; PDF blocked" is a verification quality note, not a counting rule. |
| A-M10 | Broussard $8.29 billion, secondhand, month-only date | REFUTED | Line 143: Starfield & Smith, Sep 2026 (publication month), SBA FY2025 figures (period), disclosed on the page as secondhand. |
| A-M11 | Ness City eight shares (34.53%, 23.13%, 15.45%, 10.56%, 8.24%, 10.39%, 29.57%, 21.05%) are derived arithmetic | REFUTED | Ness City research (tax rows near lines 109-111 and 129-130): each share sits in the same row as, and is attributed to, the Kansas Department of Revenue summary. I55 bites only where the research labels the figure its own computation; the file does not. Not proven. |

### attack-B majors (5)

| # | Finding | Verdict | Evidence |
|---|---|---|---|
| B-M1 | states/kansas: "No published worked case is set in Kansas yet" above a generated list naming Ness City | CONFIRMED | Served html at 860fcd32: section #cases says no case; section #worked-cases (mesh:state-cases) lists the Ness City case. |
| B-M2 | states/tennessee: "One Tennessee case so far", "worked case" singular, above a list of Lebanon and Sevierville | CONFIRMED | #cases text vs #worked-cases list; the Nashville page says Lebanon is a published case. |
| B-M3 | states/florida: "two in named towns, five placed only by region" | CONFIRMED | #cases text counts Cape Coral and Lake Wales as the only named towns; #worked-cases lists Port Charlotte, a named town, among eight cases. |
| B-M4 | states/louisiana: pending link (Gonzales, Natchitoches) reads as live | REFUTED | `data-fsc-pending` falling back to /case-studies/ is the designed mechanism (AMENDMENT-1 line 70; 71 state pages carry such anchors). No ruling requires the prose to say "not yet available". Gonzales is a recorded hold, not a defect of the landing. |
| B-M5 | states/kentucky: pending link (assisted living bridge case) reads as live | REFUTED | Same ground as B-M4. |

Totals: 20 blockers and majors judged (A: 4 blockers + 11 majors; B: 5 majors, 0 blockers). CONFIRMED 6 (A-B1, A-B2, A-M1, B-M1, B-M2, B-M3). REFUTED 14.

### Floors recomputed (pagecheck --figures, tree 860fcd32)

Counted lists agree with the attack's: Urgent care 30 (20 research, 10 register), Lebanon 31 (21, 10), Sevierville 31 (21, 10), Bardstown 34 (24, 10), Broussard 35 on this tree without `--new` (26, 9; 36/26/10 when the earlier-landed page keeps its figure with `--new`, and at its landing), Ness City 50 (43, 7), Port Charlotte 34 (29, 5). Floors 30 counted and 20 research (landing). No counted value is shared between the seven pages.

Figures removed on the CONFIRMED findings: Lebanon only, 9 research figures: $1.1631, $0.4050, $1.5681, $1.3417, $0.1786, $1.9089, $0.2973, $0.6855, 6,700. The register 10 is untouched.

| Page | Landed (counted/research) | After confirmed findings | At or above 30/20? |
|---|---|---|---|
| Lebanon | 31/21 | 22/12 (23/13 if 6,700 is left in) | NO, below both floors. Also below on A-B1 alone (26/16) or A-B2 alone (28/18). |
| Urgent care | 30/20 | 30/20 | Yes, exactly on both floors, no margin |
| Sevierville | 31/21 | 31/21 | Yes (margin 1) |
| Bardstown | 34/24 | 34/24 | Yes |
| Broussard | 36/26 | 36/26 | Yes |
| Ness City | 50/43 | 50/43 | Yes |
| Port Charlotte | 34/29 | 34/29 | Yes |

Figures that stay arguable (challenged, ruled REFUTED, still counted), for a reviewer who wants the exposure: Lebanon $1.1657 and 4,693; Sevierville four GSMNP counts and $0.87; Urgent care $11.4 billion, $1.3 billion, 110,698, 113,482 (and the minor $1,600 tap fee, whose row URL is the dated tariff); Bardstown $33.62, 16.10, 67.0, 67.3; Broussard $288,314,896.36, 4.66, 4.32, $8.29 billion; Ness City the eight shares. Urgent care has zero margin: any one of its five arguable figures removed breaks the floor. Sevierville, with five arguable figures, falls under 30/20 only if two or more go.

Pages below the floors on the confirmed findings: Lebanon only (landed under its floors by 8 counted / 8 research on the strict count; its own 21 research figures hold only 12 that are dated).

## Task 3: the five CLOSE claims

1. Pre-count 68 cases (22 new, 46 legacy); of 22 new: 7 landed, 1 held, 1 waits on owner, 1 folded by owner, 6 engine (3 pass, 3 short), 6 fold today. CONFIRMED. PRECOUNT.tsv (identical to the repo copy): 11+14+12+9 = 46 legacy, 22 new. New: 7 PAGE verdicts landed; Gonzales held; Gig Harbor WAIT-OWNER; Kerhonkson FOLD-OWNER; engine=Y six (Natchitoches, Gardner, Euclid = PAGE-WAIT-ENGINE; Elizabethtown assisted living, Yucca Valley, Clarksville = FOLD(engine)); FOLD six (Pataskala, Fairlawn, Hays, New Baltimore, Shell Knob, Huron County). 7+1+1+1+6+6 = 22. BUILD-PLAN-1 "C0 result" section lists the same groups.
2. Seven pages at landing: 34/24/10, 36/26/10, 30/20/10, 50/43/7, 34/29/5, 31/21/10, 31/21/10. CONFIRMED as counts at landing. GATES-t1/t2-landing.txt gate 3 lines match all seven, and pagecheck on git-archive copies of 5b5a129b and ce7d9a1c reproduces them exactly (Broussard 36/26/10 needs `--new`; on the current tree without it, 35/26/9, a register figure now shared with a t2 page). Whether those counts are rule-clean is a separate matter (Lebanon, above).
3. All 14 gates green at each landing on the merged site, deploys and URL counts, READY runs labelled tree B simulations, no landed page under its floor. REFUTED as worded. What reproduces: both landing gate files read green 14/14; the sitemaps hold 207 URLs at 5b5a129b and 211 at ce7d9a1c; Netlify getDeploy returns 6ae303bebaac4163f005af0f ("rollout case-new-1-t1 prod", created 2026-10-29T08:28Z) and 6ae3104e329ef44e1fa3aa2c ("rollout case-new-1-t2 prod", 09:22Z); the READY gate files carry the tree B simulation only in the file name and the root path. What does not: (a) the gate runs record git dir 445e6bc1 and ef3f0af6, the merge commits; the sitemap at 445e6bc1 held 204 URLs, so they ran on an uncommitted tree that became 5b5a129b/ce7d9a1c, not on the named main; (b) "no landed page under its floor" fails for Lebanon on the confirmed findings (22/12).
4. Live deploy 6ae3104e329ef44e1fa3aa2c; main 860fcd32; main checkout still web-fsc-2 at 1d48cc28. CONFIRMED. `netlify sites:list` shows the published deploy for feasibility-study-company.com is 6ae3104e329ef44e1fa3aa2c; `git rev-parse main` in the integrator tree is 860fcd32b158c4ec1a6235901b9fbe52048da609; `git worktree list` shows the primary checkout (Feaisbility-Study-Company.com) on branch web-fsc-2 at 1d48cc28. The live sitemap equals the repo sitemap (211 URLs, same lastmods) and the seven live pages equal the frozen pages.
5. Seven URLs in the live sitemap, formerly pending links on state/hub pages now live for them. REFUTED as worded. Reproduces: all seven URLs are in the live sitemap with lastmod 2026-10-29. Does not reproduce for four of the seven: before landing, only the three t1 pages had `data-fsc-pending` anchors on served pages (Bardstown 3 pages, Broussard 2, Urgent care 2 at 64d7cc74); Ness City, Port Charlotte, Sevierville and Lebanon had no served-page reference at all (only data/site/promised.json). The link text now live on state/hub pages for those four is new links, not formerly pending ones. No pending anchor to any of the seven remains.

## Notes outside the asked items

- Gate re-runs by attack B (13/13 green without the hub URL; the hub failure is the hub being treated as a case page) were not repeated by me; I reproduced the counts, links-state and live equality only.
- The uncounted-but-printed 5,000 and 65,000 hospital figures on the Lebanon page are wrapped in `data-fsc-nocount` but share the undated "2017 data" basis (I86: a wrap does not cure an undated number).
- I did not touch the .ghtoken or any credential file in the primary checkout; the Netlify reads were two `getDeploy` calls and one site listing (read only).
