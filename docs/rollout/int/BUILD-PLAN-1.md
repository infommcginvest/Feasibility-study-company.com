# BUILD-PLAN-1: every page still owed on feasibility-study-company.com, in lanes of two to three

Written 2026-10-28 by FSC-PILOT-1, on main a03f562 (deploy 6adf734229718c46d6ff4aa2, 198 sitemap URLs). A plan, not a landing: nothing here starts until the owner or coordinator lifts I92 for the lane in question (the FSC-PILOT-1 charter lifted it for the pilot only). Page counts are re-read from `docs/rollout/int/SITE-REMAINING-1.md` and `data/site/promised.json` against the served files at a03f562, not taken from the charter. Times project from the pilot's own measurements (`PILOT-1-REPORT.md`); where the pilot measured nothing, the plan says so and states its assumption.

## 1. What is owed (re-derived)

`promised.json` by class and served state at a03f562, matching SITE-REMAINING-1 on every line:

| Class | Promised | Live | Unbuilt | Owed work |
|---|---|---|---|---|
| Hub | 40 | 28 (plus gas station and c-store, outside PRO: 29 hub folders) | 12 | 12 new; 22 legacy rebuilds (28 live minus 6 factory-built: hotel, self-storage, private-school, multifamily, quick-service-restaurant, mixed-use) |
| Subtype | 179 | 1 (burger) | 178 | 12 recorded PAGE verdicts (ASSET-2 3, ASSET-3 8, ASSET-4 1); the rest fold as hub sections; ASSET-1 pre-counts beyond hotel not recorded |
| Case | 68 | 46 (legacy, rebuild owed) | 22 | 22 new, 46 rebuilds |
| Practice area | 5 | 4 | 1 (hud-and-agency) | 4 rebuilds, 1 new |
| Framework | 14 | 1 (index) | 13 children | 1 rebuild; 13 new, conditional on A6 (18 counted, 10 research at READY) |
| Note | 4 | 2 | 2 | 2 rebuilds; sba-rural-fee-waiver-vs-usda-bi new; proving-demand new and conditional |
| State | 42 | 42 (plus Texas) | 0 | none |
| Metro | 274 | 18 (plus 4 Texas) | 256 | none: all folded into state sections (SITE-REMAINING-1 section 4) |

Plus the owner's hub adjustment (28 Oct): a retrofit of the 29 live hubs (title, H1, meta, opening paragraph, call to action).

The ten new cases with live pending links (measured on served HTML): self-storage-bardstown-kentucky-usda, retreat-center-kerhonkson-new-york-usda, marina-gig-harbor-washington-sba (two links each); urgent-care-elizabethtown-kentucky-sba, short-term-rental-yucca-valley-california-conventional, self-storage-pataskala-ohio-sba, restaurant-acquisition-broussard-louisiana-sba, hotel-natchitoches-louisiana-eb5, childcare-gonzales-louisiana-sba, assisted-living-elizabethtown-kentucky-bridge (one each).

## 2. What the pilot measured, and the projection rules

| Unit (Sonnet builder, one Opus review, one Sonnet fix pass) | Wall to post-fix gates | Output tokens | Outcome |
|---|---|---|---|
| New hub ported from a lane draft (skilled-nursing) | 50.1 min (build 31.7, review 11.4, fix 7.1) | 178,069 | 14/14, 76 counted |
| New case ported from a lane draft (Gig Harbor, SBA 504) | 80.0 min (38.4, 19.2, 22.4) | 232,078 | 13/14 in tree B: needs the engine and a subject redesign |
| New case ported from a lane draft (Kerhonkson, USDA B&I) | 84.7 min (44.0, 25.2, 15.5) | 260,381 | under the floor: 17 counted; folds |
| Close per freeze (two Sonnet attackers and a Sonnet verifier, in parallel) | see section 9 | see section 9 | |

Projection rules used below:
- **P1, measured.** A hub ported from a lane draft: 50 minutes and 180,000 output tokens per hub to post-fix gates. A case ported from a lane draft: 85 minutes and 260,000 output tokens. Pages of one tranche build in parallel in one copy, so a tranche takes about its slowest page.
- **P2, not measured.** A page with a fact sheet but no page draft: assume the build phase at 1.5 times the pilot's (hub about 66 minutes, case about 105). A page with neither a draft nor a fact sheet adds a Sonnet reader and pre-count step; assume 30 minutes. Measure both on the first such tranche and re-plan.
- **P3, from records.** The integrator lands one tranche at a time. In FSC-RESUME-1, with three lanes feeding it, 19 tranches landed between 25 Oct 14:25Z and 26 Oct 06:09Z (`bus/landed`), one every 50 minutes on average. That is a throughput, not a measured landing duration (no record times a landing), and it caps the whole programme: at most about 29 landings a day.
- **P4, measured fold risk.** Both pilot cases lost half or more of their counted figures to rulings made after their 16 Oct drafts (I64, I71, I77, I86, I106, I144): Gig Harbor 69 to 34, Kerhonkson 36 to 17. A case that folds after a full build wastes about 85 minutes and 260,000 tokens. So every case lane starts with a pre-count under the current rulings (section 6, step C0), and a case is written only if it clears 30 and 20 on that count.
- **P5, copies.** I83 allows three throwaway copies at once, across all lanes. Three lanes means one copy per lane: a lane's tranche (its pages together) lives in one copy.

## 3. Order and the lanes

Owner ruling, 28 Oct (after the pilot): new pages come first. The order is the repair tranche, then the 12 new hubs, then the case pre-count and the CASE-4 engine, then the cases. The 29-hub retrofit moves later and is not top priority. The records force two placements inside that order. The CASE-4 engine runs alongside the last new-hub lane, because A7 lands an engine ahead of page tranches and the cases wait on it. The case pre-count runs before any case is written (P4). The retrofit rides with the hub rebuilds, because each legacy rebuild carries the buyer-intent header in its own source; that leaves the retrofit itself with the 7 factory hubs and whichever legacy hubs have not been rebuilt by then.

skilled-nursing, the pilot hub, landed on 28 Oct through the integrator procedure on the owner's word (`PILOT-1-REPORT.md`, "Landing"), so 11 new hubs remain. Kerhonkson folds as recorded (its slug stays pending, with fallback /case-studies/). Gig Harbor waits for CASE-ENGINE-1 and a hypothetical, transient-heavy subject.

| Wave | Lanes at once | Lanes |
|---|---|---|
| 1 | 3 | INT-REPAIR-1, HUB-NEW-A, HUB-NEW-B |
| 2 | 3 | HUB-NEW-C, CASE-PRECOUNT-1, CASE-ENGINE-1 (when INT-REPAIR-1 closes) |
| 3 | 3 | CASE-NEW-1, CASE-NEW-2, CASE-NEW-3 (the CASE-4 cases, after the engine) |
| 4 | 3 | CASE-REBUILD-1, CASE-REBUILD-2, CASE-REBUILD-3 |
| 5 | 3 | HUB-REBUILD-A, HUB-REBUILD-B, HUB-RETROFIT-1 (later, not top priority) |
| 6 | 3 | HUB-REBUILD-C, METHOD-1 (templates, practice areas, framework), METHOD-2 (notes, then framework children) |
| close | 1 | lane close records (A8), final site-wide gates, integrator close |

## 4. Wave 1: repair and the first new hubs

### INT-REPAIR-1 (integrator; landed pages only)
Pages: /states/texas/houston/ (re-add the register paragraph deleted in close-1 and source 42, I124); /states/pennsylvania/ Philadelphia section (restore the New Jersey, Delaware and Maryland links, I127: all three pages are live); /states/new-york/ New York City pointer (restore only if a page carries the Westchester, Rockland, Putnam side; whether any does is not recorded, so the lane first checks and, if none, records that the pointer stays deleted); /states/delaware/ and /states/west-virginia/ mesh terms (PARK).
Dependencies: none; every target is live. Owner items to settle alongside (cheap, gate nothing): Delaware source 2 URL, O6 history rewrite, Wisconsin statute values.
Projection: not measured (no pilot page was a repair). Assume two landings (GEO edits, mesh terms) at P3: about 2 hours.

### HUB-NEW-A (ASSET-3 and ASSET-4 drafts; 5 hubs, one tranche each)
Order and pages:
1. skilled-nursing: LANDED 28 Oct (the pilot hub, after its I69 fix and a second freeze; see PILOT-1-REPORT.md).
2. independent-living-and-ccrc (draft; hub pre-count 45; active-adult and ccrc-life-plan-communities fold in as the ruling 16 rewrite targets).
3. build-to-rent (draft; target of the ruling 16 rewrite from multifamily/build-to-rent).
4. manufactured-housing (draft; same).
5. meat-and-poultry-processing (draft; the I23 mesh re-key lands with it).
Every landing is a site-wide link flip (every served page carries pending chrome links to the 12 hubs).
Projection (P1, drafts): 4 remaining tranches at about 50 minutes each to post-fix gates, plus close; about 0.72 million output tokens.

### HUB-NEW-B (ASSET-1; 4 hubs)
short-term-rental (draft), event-and-wedding-venue (draft), wellness-and-retreat (draft; no B run in the research, so the lane pre-counts it first and folds it if under 30 and 20), brewery-and-distillery (no page draft; winery-and-tasting-room is a lane-defined subtype draft). The pilot's Kerhonkson case links wellness-and-retreat as its hub.
Projection: three ported (P1, 50 minutes each) and one by P2 (about 66 minutes plus a pre-count); about 0.75 million output tokens.

## 5. Wave 2: the last new hubs, the case pre-count and the engine

### HUB-NEW-C (ASSET-2; 3 hubs, no page drafts)
cold-storage (with its public-refrigerated-warehouse subtype page, pre-count 31, lane-defined and not promised: a promised-entry request first), data-center, industrial-and-warehouse (the 301 from /asset-classes/industrial/ goes into netlify.toml in the same landing, ruling 16). Register extracts exist; page drafts do not.
Projection: P2, about 66 minutes per hub plus the subtype page; about 0.7 million output tokens. Not measured.

### CASE-ENGINE-1 (CASE-4 engine tranche e1, A7)
Scope from the records: the programs CASE-4's cases need (conventional, eb5, bridge, dscr, agency) and returns from `data/returns/` (`v.irr_pct`; CASE-2's rv-boat-storage-arizona-sba keeps one). Added by the pilot, each reproduced in `PILOT-1-REPORT.md`:
- a 504 change-of-ownership path that tests the seller's historical cash flow at 1.15x (SOP 50 10 8.1), with the 504 change-of-ownership conditions as lender conditions;
- an eligibility check, or a determination state, for marinas, campgrounds and other rental businesses under the SOP's transient-revenue test, so the engine cannot print "Every test is met" over an ineligible subject;
- an integrator ruling and a gates.py change: gate 6 applies Appendix 15 (1.25x) to 7(a) purchases only.
Gates: 2, 11, `casemodel.py --check` over every case, and the byte-identical render of every case CASE-4 does not own.
Dependencies: none upstream; every CASE-4 case, the Gig Harbor case and the CASE-2 returns case wait on it.
Projection: not measured (the pilot built no engine change). Assume one working day including the byte-identical proof.

## 6. Waves 2 to 4: cases (68)

### C0, CASE-PRECOUNT-1 (all 68, before any writing; runs in wave 2)
A Sonnet reader per case counts the dated, sourced, case-specific figures under the current rulings (I64, I71, I77, I86, I106, I144), plus at most 10 register figures, against 30 and 20. Pre-counts exist only for CASE-2 (16 Oct, before those rulings). Output: a verdict per case (write, refresh research, or fold), recorded per lane. Projection: not measured; a reader per case at about 15 minutes, three at once: about 6 hours for 68.

### CASE-NEW-1 to 3: the new cases, pending-linked first (22, of which Kerhonkson folds and Gig Harbor waits)
Tranches of up to four cases from one lane (ruling 13), in this order:
1. CASE-2: self-storage-bardstown-kentucky-usda, self-storage-pataskala-ohio-sba, restaurant-acquisition-broussard-louisiana-sba (fact sheets and pre-counts, no page drafts; Broussard is an acquisition and follows Appendix 15).
2. CASE-3: urgent-care-elizabethtown-kentucky-sba, childcare-gonzales-louisiana-sba (no drafts).
3. CASE-1: marina-gig-harbor-washington-sba waits for CASE-ENGINE-1 and a hypothetical, transient-heavy subject (owner, 28 Oct; real-subject file). retreat-center-kerhonkson-new-york-usda FOLDS as recorded (owner, 28 Oct): its slug stays pending with the /case-studies/ fallback, and the /states/new-york/ wording "now being prepared" is corrected by the integrator (close finding B-M2).
4. CASE-4, after CASE-ENGINE-1: assisted-living-elizabethtown-kentucky-bridge, hotel-natchitoches-louisiana-eb5, short-term-rental-yucca-valley-california-conventional.
5. The other 12 new cases: CASE-1 grocery-store-ness-city-kansas-usda, hotel-acquisition-fairlawn-ohio-sba (real-subject file), hotel-hays-kansas-usda, marina-new-baltimore-michigan-sba, marina-shell-knob-missouri-usda (all with page drafts); CASE-2 car-wash-port-charlotte-florida-sba (draft), restaurant-sevierville-tennessee-sba; CASE-3 laundromat-acquisition-huron-county-ohio-sba (real-subject file), medical-office-lebanon-tennessee-sba; CASE-4 industrial-flex-gardner-kansas-conventional, mixed-use-multifamily-euclid-ohio-eb5, multifamily-clarksville-tennessee-dscr (after the engine).
Gate 2 needs the integrator's card region on /case-studies/ (`requests.py` prints `index_entry` and writes nothing): every READY check runs a labelled tree B simulation, and the integrator writes the real card at landing.
Projection: P1 for the 8 with page drafts (the 7 CASE-1 new cases and car-wash-port-charlotte; 85 minutes per four-case tranche), P2 for the 14 without (about 105 minutes per tranche); 22 cases in about 7 tranches; about 5.7 million output tokens at 260,000 per case. Expect folds: the pilot's two drafted cases both failed.

### C0 result (CASE-NEW-1, 29 Oct): PAGE or FOLD for all 68 cases

Counted under the current rulings (I64, I71, I77, I86, I106, I144) with amendment A4 read as pagecheck reads it (a case outranks state, metro and hub pages; another case page that already carries a value takes it). A PAGE needs the reader count and the repo tally to agree on 30 counted and 20 research (ready stage). Counts move when siblings land: rerun the pre-count before each rebuild tranche. The per-figure rows sit outside the repository (they carry real-site identifiers; gate 8). Table: `docs/rollout/case-new-1/PRECOUNT.tsv`.

- **New cases landed (7):** self-storage-bardstown-kentucky-usda (29/19, A4 42/32), restaurant-acquisition-broussard-louisiana-sba (30/20, A4 38/28), urgent-care-elizabethtown-kentucky-sba (26/16, A4 33/23), grocery-store-ness-city-kansas-usda (73/63), car-wash-port-charlotte-florida-sba (58/48), restaurant-sevierville-tennessee-sba (46/36), medical-office-lebanon-tennessee-sba (58/48).
- **New case held (1):** childcare-gonzales-louisiana-sba (57/47).
- **New case waiting on the owner (1):** marina-gig-harbor-washington-sba (75/65).
- **New cases that pass the floor and wait for CASE-ENGINE-1 (3):** hotel-natchitoches-louisiana-eb5 (30/22), industrial-flex-gardner-kansas-conventional (38/28), mixed-use-multifamily-euclid-ohio-eb5 (34/24).
- **New engine cases that also fall short of the floor (3):** assisted-living-elizabethtown-kentucky-bridge (29/19), short-term-rental-yucca-valley-california-conventional (28/18), multifamily-clarksville-tennessee-dscr (27/17).
- **New cases that fold today (floor missed, or the reader and the tally disagree, as for Huron) (6):** self-storage-pataskala-ohio-sba (14/4, A4 20/10), hotel-acquisition-fairlawn-ohio-sba (21/11, A4 21/13), hotel-hays-kansas-usda (24/14, A4 24/15), marina-new-baltimore-michigan-sba (28/18, A4 28/18), marina-shell-knob-missouri-usda (27/17, A4 27/17), laundromat-acquisition-huron-county-ohio-sba (33/23).
- **New case folded by the owner (Kerhonkson) (1):** retreat-center-kerhonkson-new-york-usda (28/18).
- **Legacy rebuilds that pass and need no engine work (25):** fitness-minnesota-sba (37/27), fitness-new-hampshire-sba (71/61), grocery-store-mississippi-usda (31/21), hotel-florida-sba (37/27), hotel-georgia-sba (47/37), hotel-south-carolina-sba (26/17, A4 37/27), marina-maryland-sba (36/27, A4 40/31), rv-park-arizona-usda (26/17, A4 31/21), rv-park-pennsylvania-usda (25/25, A4 31/31), auto-service-new-jersey-sba (47/39, A4 56/47), meat-processing-georgia-usda (38/28), qsr-georgia-sba (53/43), restaurant-missouri-sba (52/42), rv-boat-storage-california-sba (47/37), rv-boat-storage-florida-sba (52/44), self-storage-arizona-sba (70/63), self-storage-indiana-sba (50/40), truck-stop-georgia-sba (62/52), truck-stop-oklahoma-sba (52/42), assisted-living-arizona-hud (47/37), assisted-living-california-hud (50/40), assisted-living-florida-hud (46/36), assisted-living-hawaii-hud (35/25), childcare-illinois-sba (35/25), laundromat-new-mexico-sba (32/22).
- **Legacy rebuilds that pass and wait for the engine (10):** rv-boat-storage-arizona-sba (55/47), behavioral-health-massachusetts-conventional (71/61), hotel-nevada-eb5 (43/33), multifamily-arizona-agency (83/73), multifamily-florida-agency (59/49), multifamily-georgia-agency (81/71), multifamily-new-york-agency (57/57), multifamily-north-carolina-agency (39/39), private-school-connecticut-conventional (34/34), retail-nevada-conventional (46/46).
- **Legacy rebuilds that fall short of the floor today (refresh the research or fold) (11):** glamping-utah-usda (28/18), rv-park-maine-usda (19/11, A4 22/13), coffee-shop-washington-sba (36/26), meat-processing-north-carolina-usda (39/29), qsr-arkansas-sba (28/18), assisted-living-north-carolina-hud (25/15), childcare-iowa-sba (24/14), funeral-home-wisconsin-sba (21/11), medical-office-north-carolina-sba (30/20), pet-boarding-oregon-sba (29/19), urgent-care-florida-sba (31/21).

Format: slug (counted/research as filed by the reader; A4 gives the figures under the A4 reading where the reader stated them). The engine column in PRECOUNT.tsv marks the cases that need CASE-ENGINE-1 (a program outside sba_7a, sba_504, usda_bi, hud_232, or a computed return).

### CASE-REBUILD-1 to 3: the 46 legacy cases
Order inside each lane: the gate 8 reds first (auto-service-new-jersey-sba (real-subject file), multifamily-arizona-agency, multifamily-north-carolina-agency, private-school-connecticut-conventional; I3), the Connecticut case's gates 3, 6, 7 and owner item O3 (I104), coffee-shop-washington-sba (keep the Spokane link, I128), self-storage-indiana-sba (keep the Indianapolis link, I42), the other two real-subject files (marina-maryland-sba, restaurant-missouri-sba), then the rest by the most-linked first.
- CASE-1 (11): fitness-minnesota-sba, fitness-new-hampshire-sba (the bus note: SBA re-total, value collisions, Concord population), glamping-utah-usda, grocery-store-mississippi-usda, hotel-florida-sba, hotel-georgia-sba, hotel-south-carolina-sba, marina-maryland-sba, rv-park-arizona-usda, rv-park-maine-usda, rv-park-pennsylvania-usda.
- CASE-2 (14): auto-service-new-jersey-sba, coffee-shop-washington-sba, meat-processing-georgia-usda, meat-processing-north-carolina-usda, qsr-arkansas-sba, qsr-georgia-sba, restaurant-missouri-sba, rv-boat-storage-arizona-sba (after the engine: it keeps a computed return), rv-boat-storage-california-sba, rv-boat-storage-florida-sba, self-storage-arizona-sba, self-storage-indiana-sba, truck-stop-georgia-sba, truck-stop-oklahoma-sba.
- CASE-3 (12): assisted-living-arizona-hud, assisted-living-california-hud, assisted-living-florida-hud, assisted-living-hawaii-hud, assisted-living-north-carolina-hud, childcare-illinois-sba, childcare-iowa-sba, funeral-home-wisconsin-sba, laundromat-new-mexico-sba, medical-office-north-carolina-sba, pet-boarding-oregon-sba, urgent-care-florida-sba.
- CASE-4 (9, after the engine): behavioral-health-massachusetts-conventional, hotel-nevada-eb5, multifamily-arizona-agency, multifamily-florida-agency, multifamily-georgia-agency, multifamily-new-york-agency, multifamily-north-carolina-agency, private-school-connecticut-conventional, retail-nevada-conventional.
Each rebuild keeps its published date (ruling 12) and clears its legacy gate reds (I3, I4, I125).
Projection: 46 cases in about 12 tranches. 12 have page drafts (CASE-1 9: all its rebuilds but hotel-georgia-sba and rv-park-pennsylvania-usda; CASE-2 3: auto-service-new-jersey, truck-stop-georgia, truck-stop-oklahoma), the other 34 not; at P1 and P2, three lanes, about 12 tranches at 85 to 105 minutes plus close; about 12 million output tokens.

## 7. Waves 5 and 6: hub rebuilds with their subtype PAGE verdicts (22 hubs, 12 subtype pages), and the retrofit

The subtype counts were taken on the 16 to 22 October sites; each is re-counted against the current site before writing (the pilot's hub lost 4 counted figures in review on the same rulings).
- HUB-REBUILD-A (ASSET-3, 8 hubs, 8 subtype pages): assisted-living-and-memory-care with assisted-living (38) and memory-care (43); behavioral-health with psychiatric-hospital (39) and residential-and-inpatient (37); childcare-and-daycare with franchised-branded (49); medical-office-and-asc with ambulatory-surgery-center (34); pet-boarding-and-daycare with franchised-pet-care (34); urgent-care with franchised-platform (33); funeral-home; veterinary-practice. Hub drafts exist for all but childcare-and-daycare.
- HUB-REBUILD-B (ASSET-2, 5 hubs, 2 subtype pages): express-car-wash with express-exterior (47), auto-service-and-collision with quick-lube (41), auto-dealership, rv-and-boat-storage, truck-stop-and-travel-center. No page drafts.
- HUB-REBUILD-C (ASSET-4 then ASSET-1, 9 hubs, 1 subtype page plus ASSET-1 pre-counts): coffee-shop with franchised-drive-thru (51), grocery-store, laundromat, restaurant, retail (all with drafts); then fitness-and-recreation, glamping, marina (draft), rv-park-and-campground, each after an ASSET-1 subtype pre-count (not recorded).
Gate 9: hub and each subtype both ways. Each rebuild keeps its published date and carries the retrofit header.
Projection: hubs at P1 or P2 (50 to 66 minutes); a subtype page is not measured (assume half a hub, 25 to 35 minutes). About 34 pages in about 22 tranches; about 5 million output tokens.

### HUB-RETROFIT-1 (owner adjustment; moved to wave 5 by the owner's 28 Oct ruling; body unchanged)
Pages, two tranches. By wave 5, HUB-REBUILD-A and B will have rebuilt 13 legacy hubs with the new header in their sources, so tranche R2 shrinks to the legacy hubs not yet rebuilt (HUB-REBUILD-C's 9 at most):
- Tranche R1, the 7 hubs with a source in `src/pages/asset-classes/`: hotel, self-storage, private-school, multifamily, quick-service-restaurant, mixed-use, gas-station-and-c-store. Source edits to title, h1, description, hero paragraph and one call to action after the market sections; `updated` back to "DEPLOY" (ruling 12).
- Tranche R2, the 22 legacy hubs, which are served HTML with no source: fitness-and-recreation, glamping, marina, rv-park-and-campground; auto-dealership, auto-service-and-collision, express-car-wash, rv-and-boat-storage, truck-stop-and-travel-center; assisted-living-and-memory-care, behavioral-health, childcare-and-daycare, funeral-home, medical-office-and-asc, pet-boarding-and-daycare, urgent-care, veterinary-practice; coffee-shop, grocery-store, laundromat, restaurant, retail. The integrator owns served HTML (as in I104), so it applies these edits by a recorded script; each later rebuild carries the new header in its source.
Rules each opening must meet: Feasibility Study Company named as the firm that prepares the class's studies for owners, developers and their lenders; deliverable, lender fit, scope and `/#contact` near the top; at least one counted figure on the first screen (ruling 16); no fee, turnaround or service promise (no record states one). Title "<Class> Feasibility Study Company | Feasibility Study Company" and H1 "<Class> Feasibility Study Consultants" (the pilot's form; the review found all 29 landed hubs end "| Feasibility Study Company"). Meta 140 to 160 characters.
Risk the lane must design against: I115's sameness guard forbids a shared hero plan, description frame or CTA move between pages, and gate 4 measures overlap site-wide. Twenty-nine openings written from one template would fail it. Each opening is written from its own hub's figures and argument, the CTA wording varies, and the lane runs gates 4 and 7 site-wide plus the I115 phrase check across all 29 before READY.
Dependencies: none. The 22 legacy hubs keep their legacy gate reds (I3, I4); the retrofit is checked for not adding any.
Projection: not measured. The closest measured unit is the hub fix pass (7.1 minutes for a header and five fixes); with one Opus review per tranche and site-wide gates: R1 about 2.5 hours, R2 about 4.5 hours, two landings.

## 8. Wave 6: METHOD-1 (23 pages) and the research notes

- METHOD-1: the practice, framework and note templates first (src/types.json, I22: the types stay disabled until the templates exist); then the four practice area rebuilds (sba-7a-504, usda-rural-development, eb-5, conventional-institutional) and hud-and-agency (new); then the analytical-framework index rebuild.
- METHOD-2: the notes (sba-feasibility-myth and sba-default-economics rebuilt; sba-rural-fee-waiver-vs-usda-bi new; proving-demand new only if it passes A6), then the 13 framework children, each written only if it reaches 18 counted and 10 research at READY, otherwise folded into the index.
Projection: not measured (the pilot built no METHOD page). Practice areas are 5,000 to 9,000 words, like a hub: assume P2. Framework pages and notes are 2,500 to 5,000 words: assume half a hub. About 10 tranches.

## 9. Totals and the close

The pilot's close (freeze, two Sonnet attackers and a Sonnet verifier in parallel) took 25.6 minutes and 257,456 output tokens for three pages: about 26 minutes per tranche and about 86,000 output tokens per page. No page was READY after its first freeze, so each tranche below carries one rework loop (a fix of about 10 minutes and a second close of about 26).

| Wave | Lanes | Tranches (landings) | Lane wall, by P1 to P3 plus close and one rework loop | Basis |
|---|---|---|---|---|
| 1 | INT-REPAIR-1, HUB-NEW-A, HUB-NEW-B | 2 + 4 + 4 = 10 | about 8 hours (HUB-NEW-A: 4 x (50 + 26 + 36) minutes) | P1 measured for hubs; repair assumed |
| 2 | HUB-NEW-C, CASE-PRECOUNT-1, CASE-ENGINE-1 | 3 + 0 + 1 = 4 | about 8 hours (engine assumed one working day; pre-count about 6 hours) | P2 and P4; engine and pre-count not measured |
| 3 | CASE-NEW-1 to 3 | about 6 (20 cases less the pre-count's folds) | about 8 hours | P1 and P2 |
| 4 | CASE-REBUILD-1 to 3 | about 12 | about 10 hours | P1 and P2 |
| 5 | HUB-REBUILD-A, HUB-REBUILD-B, HUB-RETROFIT-1 | 13 + 2 | about 10 hours | P1 and P2; subtypes and retrofit not measured |
| 6 | HUB-REBUILD-C, METHOD-1, METHOD-2 | 9 + about 10 | about 9 hours | P2; not measured |
| close | integrator | 13 lane close records plus the final pass | | A8 |

- **Lanes alone:** about 53 hours of wall clock with two to three lanes at once.
- **The integrator:** about 66 page and engine landings plus 13 close records. At the 50 minutes per landing that FSC-RESUME-1 sustained (P3), that is about 66 hours, so the integrator, not the writers, sets the pace: about three days of continuous running, more if landings return tranches. Lanes should keep one tranche READY ahead of the integrator, never more (the copy limit, P5).
- **Output tokens, approximate:** hubs 34 x 180,000 (about 6.1 million), cases 68 x 260,000 (about 17.7 million, less what pre-count folds), subtype pages 12 x about 90,000 (about 1.1 million, assumed), METHOD pages 23 x about 150,000 (about 3.5 million, assumed), closes about 86,000 per page across about 140 pages (about 12 million): about 40 million output tokens. Cache reads run about 200 times output in the pilot's transcripts and are not projected.
- **The largest uncertainty is folds, not speed.** The pilot's two drafted cases both failed: one under the floor, one on eligibility and the engine. If the C0 pre-count folds a third of the 22 new cases, as the pilot suggests it may, the case waves shrink and the page count falls with them; the plan re-projects after C0.

## 10. Rules every lane inherits from the pilot

1. Pre-count under the current rulings before writing any case or subtype (P4).
2. Every READY gate run says which tree it ran on: tree A (main plus sources plus `requests.py`) and, for cases, a labelled tree B with the integrator's card simulation. A gate green only on a hand edit that would not land is not green.
3. Never relabel an input to pass a gate (the pilot's Gig Harbor gate 6).
4. One Opus review per page before the freeze: in the pilot it found 8 blockers and 25 majors across three pages that every builder's own 14/14 gate run had missed.
5. Per-agent scratch folders: subagents share the session scratchpad, and one overwrote another's script in the pilot.
6. Report time and tokens from the transcripts, per phase, never from estimates.
7. Print no figure dated only by a builder's or reviewer's own GET (I69): the pilot hub's one blocker at close was about 25 such figures, uncounted but printed. Every builder brief carries I69 beside I86.
8. Integrator hand-offs found by the pilot's close: `/states/new-york/` says the Kerhonkson case is "now being prepared" and "(in preparation)", which gate 7's stale-claim check misses (fix when that case lands or its slug folds); the four `*` lines in `drafts/pilot-1/gig-harbor/dnu-add.txt` go into `private/` before any Gig Harbor tranche; Kerhonkson's $144.6 million also sits in `/states/texas/` (A4: the case keeps it if it ever lands).
