# What is still unbuilt for the full expansion of feasibility-study-company.com

Prepared 26 October 2026, at the close of FSC-RESUME-1 (Montana landed at main 0310699), from read only records. Nothing was built, and nothing inside any repository or worktree was created or changed. Counts marked "measured" were taken here from the served page sources or the research folder listing and have no count in a record. Anything not found in a record and not measured is marked not recorded.

Sources, by short name:
- ROLL: docs/rollout/ROLLOUT-1.md and AMENDMENT-1.md
- RES: docs/rollout/int/input/RESUME-1.md
- PARK: docs/rollout/int/PARK-RESUME-1.md
- INT: docs/rollout/int/DECISIONS.md (rulings I1 to I182)
- OWN: docs/rollout/int/OWNER_ITEMS.md
- CLOSE: docs/rollout/int/CLOSE.md (the FSC-NIGHT-1 close)
- PRO: data/site/promised.json (626 promised URLs, read against the served files)
- GEO folds: FOLDED.md and DECISIONS.md under each wt-rollout-geo-N
- ASSET folds: docs/rollout/asset-N/FOLDED.md
- CASE and METHOD blocks: input/BLOCK.md under wt-rollout-case-N and wt-rollout-method-1
- BUS: ~/Downloads/fsc-rollout/bus (landed 49 lane tranches plus 5 integrator items, ready 49, returns empty)
- DRAFTS: ~/Downloads/fsc-rollout/drafts

## 1. Headline position

| Item | Count | Source |
|---|---|---|
| Sitemap URLs live | 198 | INT I185; deploy 6adf734229718c46d6ff4aa2 |
| State pages live | 43 (all 42 lane assigned states, plus Texas from WEB-FSC-6) | INT I185, states landed 42 of 42 |
| State pages unbuilt | 0 (Montana landed 26 Oct) | INT I185 |
| Metro pages live | 22 (18 factory metros plus 4 Texas) | PARK "metros landed 22"; 22 metro folders (measured) |
| Hub pages live | 29 (28 of the 40 promised, plus gas station and c-store, which PRO does not list) | PRO against served files (measured) |
| Subtype pages live | 3 (QSR burger, gas station ev-charging, gas station interstate-highway) | src/pages/asset-classes (measured) |
| Case pages live | 67, of which 0 were built by a CASE lane | folders under case-studies (measured); BUS has no case tranche |
| Practice area, framework, note pages built by METHOD-1 | 0 | BUS has no method-1 tranche; src/types.json says practice, framework and note wait for METHOD-1 templates |
| Pending link targets on served pages | 495 distinct | measured here from data-fsc-pending anchors on 195 served HTML files |
| Lane tranches stopped since 22 October | hub, subtype, case, practice area and METHOD-1 | INT I92; RES R1 lifted the stop for states only |

## 2. Case studies (promised or owed by CASE lane, and live)

| Lane | Promised | Of which new (not yet built) | Of which rebuilds (legacy page live, rebuild not landed) | CASE landed | Source |
|---|---|---|---|---|---|
| CASE-1 | 18 | 7 | 11 | 0 | CASE-1 BLOCK table (18 rows); PRO (7 unbuilt, 11 live) |
| CASE-2 | 19 | 5 | 14 | 0 | CASE-2 BLOCK table (19 rows); PRO |
| CASE-3 | 16 | 4 | 12 | 0 | CASE-3 BLOCK table (16 rows); PRO |
| CASE-4 | 15 | 6 | 9 | 0 | CASE-4 BLOCK table (15 rows); PRO |
| Total | 68 | 22 | 46 | 0 | ROLL says 68 cases, 46 rebuilt, 22 new; PRO agrees |

Live case pages: 67 folders. These are 15 WEB-FSC-6 factory cases (15 sources under src/pages/case-studies), the 46 legacy pages that await a CASE rebuild, and the 6 cases ROLL says stay as they are (Townsend TN, Cape Coral FL, Oak Hill WV, Ossipee NH, the Texas multifamily case and the Michigan veterinary case). The three way split sums to 67 (15 plus 46 plus 6); the 15 and 6 are from ROLL, the 46 from PRO.

The 22 new cases still unbuilt, by lane (PRO):
- CASE-1 (7): grocery-store-ness-city-kansas-usda, hotel-acquisition-fairlawn-ohio-sba, hotel-hays-kansas-usda, marina-gig-harbor-washington-sba, marina-new-baltimore-michigan-sba, marina-shell-knob-missouri-usda, retreat-center-kerhonkson-new-york-usda.
- CASE-2 (5): car-wash-port-charlotte-florida-sba, restaurant-acquisition-broussard-louisiana-sba, restaurant-sevierville-tennessee-sba, self-storage-bardstown-kentucky-usda, self-storage-pataskala-ohio-sba.
- CASE-3 (4): childcare-gonzales-louisiana-sba, laundromat-acquisition-huron-county-ohio-sba, medical-office-lebanon-tennessee-sba, urgent-care-elizabethtown-kentucky-sba.
- CASE-4 (6): assisted-living-elizabethtown-kentucky-bridge, hotel-natchitoches-louisiana-eb5, industrial-flex-gardner-kansas-conventional, mixed-use-multifamily-euclid-ohio-eb5, multifamily-clarksville-tennessee-dscr, short-term-rental-yucca-valley-california-conventional.

Pending links to unbuilt cases already on served pages: 10 distinct case targets (measured). Landed state pages (Kentucky, Louisiana, Washington, Ohio, New York, California) already carry them.

Engine and draft state:
- CASE-4 engine tranche (AMENDMENT A7, rollout/case-4/e<n>): not landed. No tag in the case-4 worktree and no ready file. A draft casemodel.py and fixtures sit in DRAFTS/case-4/engine. CASE-2 and CASE-3 rebuilds that keep a computed return depend on it (A7). CASE-2 keeps data/returns/rv-boat-storage-arizona-sba.json (CASE-2 BLOCK).
- Page drafts, none frozen or tagged: CASE-1 16 page.html drafts, CASE-2 4 (auto-service-new-jersey, car-wash-port-charlotte, truck-stop-georgia, truck-stop-oklahoma), CASE-3 0 (step zero record only), CASE-4 0 pages (15 fact sheets and the engine draft). All measured from DRAFTS.
- CASE-2 pre-counts exist for 19 cases, local figures 40 to 86 each (wt-rollout-case-2 PRECOUNT.md). Pre-counts for CASE-1, CASE-3 and CASE-4: not recorded.
- Never built: CS-Q-COPPERAS-COVE-TEXAS-STORAGE-YARD (ROLL, live client engagement).
- Notes already filed for the cases: bus/requests/case-4/int-1.md (Connecticut private school rebuild), case-1/int-resume-1-nh.md (New Hampshire fitness case: SBA re-total, value collisions with the New Hampshire and Maine pages, Concord population), case-2/int-geo-4-2.md (keep the Spokane link), case-2/int-1.md, case-2/int-asset-4-2.md, case-1/int-1.md.

## 3. Asset class hubs and subtypes (planned against live)

Hubs, from PRO against the served files:

| Lane | Promised hubs | Live | Factory built (landed) | Legacy live, rebuild owed | New, unbuilt |
|---|---|---|---|---|---|
| ASSET-1 | 9 | 5 | hotel | fitness-and-recreation, glamping, marina, rv-park-and-campground (4) | brewery-and-distillery, event-and-wedding-venue, short-term-rental, wellness-and-retreat (4) |
| ASSET-2 | 9 | 6 | self-storage | auto-dealership, auto-service-and-collision, express-car-wash, rv-and-boat-storage, truck-stop-and-travel-center (5) | cold-storage, data-center, industrial-and-warehouse (3) |
| ASSET-3 | 11 | 9 | private-school | assisted-living-and-memory-care, behavioral-health, childcare-and-daycare, funeral-home, medical-office-and-asc, pet-boarding-and-daycare, urgent-care, veterinary-practice (8) | independent-living-and-ccrc, skilled-nursing (2) |
| ASSET-4 | 11 | 8 | mixed-use, multifamily, quick-service-restaurant | coffee-shop, grocery-store, laundromat, restaurant, retail (5) | build-to-rent, manufactured-housing, meat-and-poultry-processing (3) |
| Total | 40 | 28 | 6 | 22 | 12 |

ROLL states 40 hubs, 27 rebuilt and 13 new. PRO gives 28 live and 12 unbuilt. The 13th new hub is not recorded; the count of rebuilt hubs also differs, so treat the ROLL split as superseded by PRO. The gas station and c-store hub (WEB-FSC-6) is built and outside PRO.

Landed hub tranches (BUS and CLOSE): asset-1 t1 hotel, asset-2 t1 self-storage, asset-3 t1 private school, asset-4 t1 multifamily, t2 QSR with burger, t3 mixed-use. All twelve new and 22 legacy hubs wait.

Every one of the 195 served pages carries pending links to the 12 unbuilt hubs in the chrome (measured), so each new hub lands as a site wide link flip.

Hub drafts that exist (unlanded, review state not recorded), measured from DRAFTS:
- ASSET-1: marina, short-term-rental, wellness-and-retreat, event-and-wedding-venue (4 hub drafts) and one brewery subtype draft (winery-and-tasting-room, lane defined).
- ASSET-2: register extracts only for cold-storage, industrial-and-warehouse and others, and a gas station hub draft; no page draft for the other hubs.
- ASSET-3: 9 hub drafts (independent-living-and-ccrc, skilled-nursing, urgent-care, veterinary-practice, funeral-home, medical-office-and-asc, pet-boarding-and-daycare, behavioral-health, assisted-living-and-memory-care) and 7 subtype drafts.
- ASSET-4: 8 hub drafts (restaurant, build-to-rent, manufactured-housing, laundromat, meat-and-poultry-processing, retail, grocery-store, coffee-shop) and the coffee-shop franchised-drive-thru subtype draft. DRAFTS/asset-4 and asset-4/RESUME.md are the resume points.

Subtypes:

| Lane | Promised subtype slugs (PRO) | Live | Verdict PAGE or written in the pre-count, not yet live | Source of the verdict |
|---|---|---|---|---|
| ASSET-1 | 35 | 0 | not recorded except hotel: all 7 hotel subtypes folded into the hotel hub, 0 pages | asset-1 FOLDED.md |
| ASSET-2 | 43 | 0 | 3: express-car-wash/express-exterior (47), auto-service-and-collision/quick-lube (41), cold-storage/public-refrigerated-warehouse (31, lane defined, not promised) | asset-2 FOLDED.md |
| ASSET-3 | 58 | 0 | 8 of 58: assisted-living, memory-care, ambulatory-surgery-center, franchised-branded, psychiatric-hospital, residential-and-inpatient, franchised-platform, franchised-pet-care (56 folded as hub sections) | asset-3 FOLDED.md |
| ASSET-4 | 43 | 1 (burger) | 1: coffee-shop/franchised-drive-thru (51) | asset-4 FOLDED.md |
| Total | 179 | 1 | 12 recorded (3 plus 8 plus 1), ASSET-1 beyond hotel not recorded | |

ROLL says 184 subtype slugs promised plus four folded gas station subtypes; PRO lists 179. The 5 difference is not recorded. The two gas station subtypes live (ev-charging, interstate-highway) are WEB-FSC-6 pages outside PRO.

Folded subtype sections already shipped inside landed hubs: hotel 7 (asset-1 FOLDED), self-storage 6, private school 6 (independent-nais folded after review), mixed-use 5 unpromised sections (asset-4 FOLDED D25). Subtype slugs stay pending links, 178 of them measured on served pages. The pre-counts used 16 October and 21 to 22 October site states; none has been re-counted against the 26 October site except those named in the records.

Hub level strays that rewrite to pending subtypes (ROLL ruling 16, asset-1 FOLDED): limited-service-hotel, select-service-hotel, extended-stay-hotel, boutique-and-resort, plus the meat processing re-key (INT I23, due at the meat hub landing).

## 4. Metro pages: none owed; promised markets folded into state pages

| Lane | Promised metro slugs (PRO) | Live as pages | Promised, folded into a state page section | Source |
|---|---|---|---|---|
| GEO-1 | 69 | 11 | 58 | PRO |
| GEO-2 | 64 | 0 | 64 | PRO |
| GEO-3 | 78 | 2 | 76 | PRO |
| GEO-4 | 63 | 5 | 58 | PRO |
| Total | 274 | 18 | 256 | PRO; the 4 Texas metros live are outside these counts |

None of these 256 promised metro slugs is unbuilt work: every one is already folded into a section of its state page, as its lane's FOLDED.md records (measured by slug match), so the records owe no metro page by promise. Montana's seven markets fold the same way and were never promised. The slug stays a pending link whose fallback is the state page section. No metro page is scheduled in any record.

Folded markets that were never promised, so they have no pending slug (records):
- GEO-1 FOLDED: 6 unpromised sections (D10), 8 West Virginia sections (I151), plus Delaware 6 sections and Mississippi Meridian per the prose.
- GEO-4 FOLDED: Idaho 6 sections (coeur-d-alene, idaho-falls, lewiston, pocatello, sun-valley-ketchum, twin-falls), and a further 5 backtick rows outside PRO.
- Montana: 7 markets, none promised in PRO (PARK).
- GEO-2 and GEO-3 unpromised totals: not recorded.

Folded markets that the records show at or one past the floor on at least one reading. No record uses the words "could stand later"; this list is the near misses their own records give, not a promise.

| Market | Free dated research figures | Record |
|---|---|---|
| Des Moines IA | 21 (9 borderline, 12 strict) | INT I107 |
| Oahu HI | 22 (21 needed), under 21 on six single readings | INT I180 |
| Inland Empire CA | 22 (3 borderline c dated, 19 without) | geo-4 FOLDED |
| Phoenix AZ | 22, 17 once stand ins set aside | INT I129 |
| Montgomery County MD | 20 (1 short of the lane's 21) | geo-1 FOLDED, Maryland |
| Chicago IL | 20 (4 wage floors), folded at the D29 re-count | geo-3 FOLDED |
| Dover DE | 21 or more (22) only if site collisions are ignored, which the rules forbid | geo-1 FOLDED, Delaware |

Texas folded metros (WEB-FSC-6, still pending slugs): McAllen 12, El Paso 9, Lubbock 6, Corpus Christi 10 unique research figures (geo-1 FOLDED, Texas marker pass), against floor 20 (ROLL).

Pending metro targets on served pages absent from PRO (measured here, 23): Kentucky 8, Louisiana 8, Tennessee 7. A5 says on site pending targets count as promised; no record lists them as such. Also pending and absent from PRO: /asset-classes/industrial/ and /infrastructure/deliverable-architecture/ (the retired infrastructure page named in ROLL).

## 5. State pages

| Lane | Promised states (PRO) | Live | Unbuilt |
|---|---|---|---|
| GEO-1 | 11 | 11 | 0 |
| GEO-2 | 11 | 11 | 0 |
| GEO-3 | 10 | 10 | 0 |
| GEO-4 | 10 | 9 | 0 (Montana landed, I185) |

INT I185: states landed 42 of 42; metros landed 22. The research inventory has 43 ST files (ROLL, OWN O5), so no other state has research and no further state is planned. The 7 states without an ST file: not recorded (not in any record).

Montana (GEO-4 t10, new state) landed on 26 October in the resumed session: one page with all seven markets as sections, 53 counted (43 research, 10 register), main 0310699, deploy 6adf734229718c46d6ff4aa2 (INT I183 to I185).

The close (docs/rollout/int/CLOSE-RESUME-1.md) and the resume bundle (RES R8) are written with this inventory; the state programme is complete.

## 6. Practice area, METHOD-1 and other tranche types

Stopped by INT I92 (22 October) and RES R1 (25 October): no hub, subtype, case, practice area or METHOD-1 tranche may start in the resume. Nothing of these types has landed since the stop.

| Type | Planned (METHOD-1 BLOCK, PRO) | Live legacy page | Built by METHOD-1 | Unbuilt |
|---|---|---|---|---|
| Practice areas | 5 (4 rebuilds, 1 new) | 4 (sba-7a-504, usda-rural-development, eb-5, conventional-institutional) | 0 | hud-and-agency (new); 4 rebuilds owed |
| Framework index | 1 rebuild | 1 | 0 | rebuild owed |
| Framework children | 13 promised, "new where each passes, others fold" (BLOCK) | 0 | 0 | 13 (all pending targets on served pages, measured) |
| Research notes | 4 (2 rebuilds, 2 new) | 2 (sba-feasibility-myth, sba-default-economics) | 0 | sba-rural-fee-waiver-vs-usda-bi, proving-demand (conditional slug) |

Total METHOD-1 pages owed: 23 (7 rebuilds, 16 new), of which the 13 children and the proving-demand note are conditional on passing the figure floors for framework pages and notes (A6: 18 counted, 10 research at READY).

METHOD-1 state: only a step zero commit plus uncommitted DECISIONS.md, REQUESTS.md and tools in its worktree; one page draft (conventional-institutional) and three template drafts (practice, framework, note) in DRAFTS/method-1; nine fact sheets. src/types.json says the practice, framework and note types wait for METHOD-1's template files. The integrator side (I22) is done: house partials, byline-framework, and the fee waiver topic left out until that note lands.

Other tranche types the records list: the engine tranche (A7, section 2); close records for 13 lanes (A8, INT I15: the integrator closes when all thirteen close records have landed). Close records landed: not recorded (BUS has none).

Integrator owned pages to keep true at every landing (ROLL, A5): /asset-classes/, /case-studies/ cards, /practice-areas/, /research-notes/, the feed, home and /states/ counts; run the stale claim grep each time.

## 7. Research files with no served page (file names only)

The research folder holds 314 files. Names carry a type prefix on only part of them: ST 9, MT 42, AH 51 (41 A and 10 B), SD 17, CS 9 (8 CS-R and 1 CS-Q), PA 4, and 182 names beginning "EXTRA" with a date. ROLL counts ST 43, MT 42, AH 41, SD 17, CS-R 58, CS-N 15, CS-Q 11, PA 4 by Research ID, so the 182 EXTRA names hide most state, case and B run files. The classification below is by title words in file names only.

| Research type | Files by name | With no served page | Basis |
|---|---|---|---|
| State (ST, plus EXTRA files titled "State Reference" or a state "Feasibility Evidence") | 9 plus 34 = 43 | 0 | all 43 have a state page |
| MT (metro and market, one per state, none for Pennsylvania) | 42 | state level: 0. Market level: all but 22 markets are sections, not pages | PRO, FOLDED |
| AH A run (hub unit economics) | 41 | 12 (the unbuilt hubs) | PRO |
| AH B run (demand, supply, subtypes) | 10 named plus EXTRA "Demand Method, Supply, Subtypes" titled files (exact count not recorded) | B run files for unbuilt hubs: cold-storage, event-and-wedding-venue, independent-living-and-ccrc named, plus EXTRA B runs for short-term-rental, skilled-nursing, brewery, build-to-rent, data-center, industrial, manufactured-housing, meat and poultry (11 in all); wellness has none (BLOCK) | names |
| SD (subtype evidence) | 17 | 15 of 17 hubs have no live subtype page except gas station (2) and QSR (1); the 12 unbuilt hubs have no SD file | names, PRO |
| Case research (CS-prefixed plus EXTRA market evidence titled by town, 15 and 16 October) | 83 by name (9 plus 74) against 84 by ROLL ID count | 22 files for the 22 new cases (each town name found in a file name); 46 more back legacy pages that have not been rebuilt | CASE BLOCKs, names |
| PA (program areas) | 4 | hud-and-agency has no page (PA-HUD-AGENCY) | PRO |
| IW (site plan packs, entitlement case studies) | exact count not recorded (EXTRA titles with IW or entitlement words exist) | not recorded: no record assigns them a page | names |

## 8. Owner items still open

| Item | Status | Source |
|---|---|---|
| O1 publishing refused | resolved 21 Oct | OWN |
| O2 screenshot folder | no action needed, folder already absent | INT I105 |
| O3 Connecticut private school case contradicts its disclosure | wording fixed in close-1; the first person engagement narrative stays until CASE-4 rebuilds it. Open | OWN, RES R7(d), INT I104, I125, PARK |
| O4 fetch dated figures, North Carolina total, pagecheck | close-1 landed 25 Oct (I125); later landings used the I71 aware count. Residual: none listed | OWN, INT I125 |
| O5 states without research | none | OWN |
| O6 45 older commits and 18 tracked files match ruling 9 pattern; history rewrite is the owner's call | open | OWN, PARK |
| Delaware source 2 pairs one publisher's title with another's URL; owner may confirm the URL | open | PARK, INT I168 |
| Wisconsin statute values (7 days, 180 days) from an undated statute | open, for GEO-3 | PARK |
| Register county lists: 28 files differ from the Census CBSA roster; a register lane should re derive them | open, owner item for CLOSE | INT I34 |
| Home page methodology table and FAQ carry 14 uncited figure blocks | open legacy | INT I36 |
| Author record lists credentials (Ph.D., MAI, CCIM) with no verification URLs; Search Console sitemap resubmit | listed as owner items for CLOSE in the integrator block; whether done: not recorded | wt-rollout-int docs/rollout/int/input/BLOCK.md |
| Committed to remote: nothing is pushed from the Mac; the coordinator pushes bundles | open process item | RES R8 |

## 9. Legacy pages needing a rebuild or repair

| Page or item | Problem | Owner of the fix | Source |
|---|---|---|---|
| /states/texas/houston/ | register paragraph deleted in close-1 (no verb left) and source 42 dropped; GEO-1 to re-add | GEO-1 | PARK; DRAFTS/int/RESUME-1-LOG.md line 70 |
| /states/pennsylvania/ Philadelphia section | lost links to New Jersey, Delaware and Maryland; restore when their pages carry their sides. All three pages are now live, so the condition is met | GEO-2 | PARK; geo-2 tranches/t3.md A2-1 |
| /states/new-york/ New York City pointer | pointer to Westchester, Rockland, Putnam deleted; restore when a page carries that side. Whether any page does: not recorded | GEO-2 | geo-2 tranches/t4.md A2-2 |
| /states/delaware/ and /states/west-virginia/ | no mesh term; each holds 3 or more inbound links without one | integrator | PARK |
| /states/texas/ (10,755 words against the 8,000 ceiling) and /states/tennessee/nashville/ (1,433 words) | advisory body word range flags, not a gate | GEO-1 | PARK; INT I7 |
| Pages under their landing floor | none (25 counted and 15 research). Lowest margins at close-1: Detroit 29 (19 research), Raleigh-Durham 26 (17), Nashville 25 (19), Charleston 30 (20); Nashville was repaired from 24 to 25 at the Hawaii landing and sits exactly on the floor | none owed; a later landing gate run is the check | INT I125, I182, PARK |
| Legacy case gate reds (reported, not failed) | gate 4: 10 overlapping pairs before roll out (home against /asset-classes/, QSR AR and GA, fitness MN and NH, others); gate 8 subject identifiers on four legacy cases (auto-service-new-jersey, multifamily-arizona, multifamily-north-carolina, private-school-connecticut); gates 3, 6, 7 red on the Connecticut case (13 counted, missing v3 sections, 13 uncited sources, 38 uncited figure blocks, two subject amounts) and gates 3, 6, 7 on the coffee shop Washington case; gate 7 red on the Michigan veterinary case (17 uncited sources, 38 uncited figure blocks) | CASE-2 and CASE-4 rebuilds | INT I3, I4, I39, I125, I128, PARK |
| CASE-1 note on the New Hampshire fitness case | SBA re-total, value collisions with the New Hampshire and Maine pages, Concord population | CASE-1 | PARK; bus/requests/case-1/int-resume-1-nh.md |
| Coffee shop Washington case | keep the Spokane link when rebuilt | CASE-2 | INT I128; bus/requests/case-2/int-geo-4-2.md |
| Indiana self storage case and Michigan veterinary case | rebuild must keep the Indianapolis and Detroit links (gate 9 required edge) | CASE-2 and the integrator | INT I39, I42 |

Six case research files are built around a real named subject (ROLL measured facts): marina-maryland, auto-service-new-jersey, restaurant-missouri, the Ohio hotel (Fairlawn), the Ohio laundromat (Huron County) and the Gig Harbor marina. Their pages must use hypothetical subjects (ruling 7); three of the six are rebuilds of live legacy pages and three are new cases.

## 10. Proposed build order

Each step cites the dependency the records state.

| Step | Work | One line reason |
|---|---|---|
| 1 | (done) Montana landed 26 Oct (INT I185) | No state remains |
| 2 | Repair tranche on landed pages: Houston register paragraph, Philadelphia links to NJ, DE, MD, New York City pointer if a page carries it, mesh terms for Delaware and West Virginia | Each repair waits only on pages that are now live (PARK, geo-2 t3 A2-1) |
| 3 | Owner decisions: Delaware source 2 URL, O6 history, Wisconsin statute values | Cheap, and they gate nothing but should be settled before the close |
| 4 | CASE-4 engine tranche e1 (credit programs and data/returns support) | A7 lands engine first; CASE-2 and CASE-3 rebuilds with computed returns depend on it |
| 5 | CASE-3 and CASE-1 and CASE-2 and CASE-4 case tranches, new cases with live pending links first (the 10 targets measured), then the four legacy gate 8 cases and the Connecticut and coffee shop cases | Landed state, hub and index pages already link the new cases as pending and gate 9 needs the edges live; legacy reds clear on rebuild (I3, I125) |
| 6 | Hub and subtype tranches, new hubs first (12), starting where drafts exist (ASSET-3 skilled-nursing and independent-living, ASSET-1 four, ASSET-4 build-to-rent, manufactured-housing, meat) | Every served page carries pending links to the 12 hubs, and cases link hubs (A5); meat also triggers the I23 re-key |
| 7 | Hub rebuilds, with the 12 recorded subtype PAGE verdicts alongside their hubs (ASSET-3 8, ASSET-2 3, ASSET-4 1), then ASSET-1 pre-counts (not recorded) | Subtype pages need the hub landed first, and the hotel stray rewrites (ruling 16) already point at hotel sections |
| 8 | METHOD-1 templates, then practice areas (4 rebuilds plus hud-and-agency), the framework index, and the 13 children that pass | Types stay disabled until the templates exist (src/types.json, I22); the 13 children are pending targets on served pages |
| 9 | Research notes (2 rebuilds, 2 new) | Lowest dependency; fee waiver topic already staged (I22) |
| 10 | Metro re-count of the seven near misses only if the owner wants more metro pages | Records show them near the floor but they fold under ruling 6; each needs 3 inbound links at landing (gate 9) |
| 11 | Lane close records (13) and final site wide gates; CLOSE-RESUME-1 and its bundle are done | A8: the integrator closes when all thirteen close records have landed |

## 11. Counts not found in a record (not recorded)

- The 13th new hub in ROLL's "27 rebuilt, 13 new", and the 5 subtype slugs between ROLL's 184 and PRO's 179.
- ASSET-1 subtype pre-counts beyond hotel (brewery, event, short-term-rental, wellness, marina, glamping, fitness, rv park).
- CASE-1, CASE-3 and CASE-4 pre-counts.
- GEO-2 and GEO-3 totals of unpromised sections.
- States without ST research beyond the 43 files, and any state outside the 42 plus Texas that is planned.
- IW research files with no served page, and the exact AH B and SD counts hidden under EXTRA names.
- Whether the Search Console resubmit and author credential verification items were done.
- Lane close records landed (none appear in BUS).
- Whether the New York City pointer targets exist.
