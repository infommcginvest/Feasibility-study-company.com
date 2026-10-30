# DERIVATION: GEO-4 and CASE-3 blocks (FSC-NIGHT-1, 21 October 2026)

Derived by FSC-NIGHT-1 on 21 October 2026 under the owner's block, from the research inventory. Nothing in the repositories was edited. Outputs are in `~/Downloads/fsc-rollout/drafts/int/derive/`: `INVENTORY.tsv`, `GEO-4-BLOCK.md`, `CASE-3-BLOCK.md`, `promised-add.json` and this file.

## Method

1. Enumerated every file in `~/Downloads/FSC Deep Searches 2/` first (`ls`, no filter), then read only the first 15 lines of each to get the Research ID and the first heading. The Research ID is either a `RESEARCH ID:` line or a bare ID on the first line; file names were not used (138 files carry an ID that does not match their name, for example ST- files named "EXTRA 2026-10-12").
2. Read the ten saved blocks plus the METHOD-1 block from their worktrees (`wt-rollout-geo-1`, `-geo-2`, `-geo-3`, `-asset-1` to `-asset-4`, `-case-1`, `-case-2`, `-case-4`, `-method-1`) and matched every ST- and CS- ID against them with a whole-token match. No asset or method block names any ST- or CS- ID. No CS- ID is named by two blocks. Every ID a saved block names exists in the folder.
3. Read ROLLOUT-1 (Measured facts, rulings 2, 3, 7, 13, 16), AMENDMENT-1 (A1, A4, A5, A6), `data/site/promised.json`, `case-studies/` and `states/` of the integrator worktree, and the WEB-FSC-6 CLOSE for the fifteen live cases.
4. Pending metro slugs for the eight existing GEO-4 states were read from the `data-fsc-pending` anchors on the live site sources (promised.json holds none for them, since the lane was missing); Idaho and Montana have none and take their candidates from their MT files' opening lines only.

## Counts

- Files: 314 (all `.md`). With a Research ID: 270. Without: 44 (34 carry an IW- number in their title, 2 are the 10 October packs ruling 2 names, 8 others).
- By prefix: ST 43, MT 42, CS-R 58, CS-N 15, CS-Q 11 (these match ROLLOUT-1 Measured facts), AH 80, SD 17, PA 4. No Research ID appears twice.
- ST 43 = 32 in saved blocks (GEO-1 11, GEO-2 11, GEO-3 10) + Texas (live page) + 10 for GEO-4.
- MT 42 follows its ST (no MT-PENNSYLVANIA): GEO-1 11, GEO-2 10, GEO-3 10, GEO-4 10, Texas live 1.
- CS 84 = 52 in the CASE-1, CASE-2 and CASE-4 blocks (18, 19, 15) + 15 live WEB-FSC-6 cases + 1 excluded + 16 for CASE-3.
- Check against ROLLOUT-1: 68 cases = 46 rebuilt + 22 new. 52 + 16 = 68. The 12 CS-R files behind live WEB-FSC-6 cases are not rebuilt (58 - 12 = 46 rebuilt); the 3 CS-Q files behind live cases and the excluded one are not new (26 - 4 = 22 new).

## GEO-4: ten states

Arizona, California, Hawaii, Idaho, Montana, Nevada, New Mexico, Oregon, Utah, Washington: the ST- files with no page in the saved blocks, less Texas. Eight rebuild existing state pages (31 rebuilt in all: GEO-1 8, GEO-2 8, GEO-3 7, GEO-4 8); Idaho and Montana are new (11 new in all: 3, 3, 3, 2), which matches ROLLOUT-1 (31 rebuilt, 11 new). Metros: the 62 promised slugs are the ones already pending on the site (Arizona 8, California 8, Hawaii 6, Nevada 8, New Mexico 8, Oregon 8, Utah 8, Washington 8); the MT files' headline counts agree (eight, eight, six, eight, eight, eight, eight, eight). Montana's seven markets come from its MT title. Idaho's eight are not named in the first 15 lines beyond the Treasure Valley and two growth counties, so the block leaves the rest to the lane's pre-count.

## CASE-3: sixteen cases

Twelve rebuilds (existing case URLs: five HUD 232 assisted living, two childcare, one funeral home, one laundromat, one medical office, one pet boarding, one urgent care) and four new cases (childcare Gonzales LA, urgent care Elizabethtown KY, medical office Lebanon TN, laundromat acquisition Willard OH). Program and town come from the first heading and TL;DR of each file; no address, price or listing id is copied. New slugs follow the house pattern of the other blocks (`<asset>-<town>-<state>-<program>`, as in `hotel-hays-kansas-usda`); the rebuilds keep their existing `<asset>-<state>-<program>` URL. Four tranches of four; ordering puts large states first and keeps sibling assets apart.


## Ambiguous or decided by me

1. **The fifteen live WEB-FSC-6 case files are not in CASE-3.** They have no case in the CASE-1, CASE-2 or CASE-4 blocks, so a literal reading of the task would give CASE-3 31 cases. They are already live (their `data/cases/*.json` exist in the integrator tree; the WEB-FSC-6 CLOSE lists the fifteen pages), the GEO-1 block calls them finished work not to be touched, and the CASE-4 block requires their render to stay byte-identical. 68 minus the 52 in the three blocks is 16, which is exactly what remains. If the owner wants any of the fifteen rebuilt on the v3 engine, they would be added to CASE-3 as a fifth tranche onward.
2. **CS-Q-COPPERAS-COVE-TEXAS-STORAGE-YARD** is excluded as instructed (live client engagement in its submarket). It is not counted among the sixteen.
3. **Real-subject file in CASE-3.** CS-N-LAUNDROMAT-ACQUISITION-OHIO-SBA-7A is one of the six real-subject files. The five others sit in CASE-1 (hotel acquisition Fairlawn, marina Maryland, marina Gig Harbor) and CASE-2 (auto service, restaurant Branson). I named the subject by county in the slug (`laundromat-acquisition-huron-county-ohio-sba`) because Willard's confirmed operating laundromats are fewer than three (ruling 7). A town-named slug is the alternative; the lane may change it before its first request and tell the integrator.
4. **Other files that may be real-subject.** The Port Washington funeral home file is built around a named, closed business at a street address, and the Redmond pet boarding file and the Wendell assisted living file centre on a specific listed property. Ruling 7 already makes the gate 8 reader list identifiers for every case; I flagged only the funeral home in the block because it names a business, and left the decision on `*` lines to the reader.
5. **Same-name and same-place collisions (A4).** Winter Haven FL hosts CASE-3's assisted living case and CASE-4's multifamily case; Elizabethtown KY hosts CASE-3's urgent care case and CASE-4's assisted living bridge case; Haines City, Winter Haven and the WEB-FSC-6 Lake Wales case share Polk County. Same rank, so the first to land keeps a repeated figure. Noted in the block.
6. **Promised metros that are case towns.** `kapolei` (HI), `winnemucca` and `fernley` (NV) are promised metro slugs and case towns; A4 says state and metro pages avoid place-level figures for such towns, so those pages may fold or stand on county figures. Noted in the GEO-4 block.
7. **`/states/arizona/rural/`** is a pending target that names no place. Left as a promised slug with an instruction to decide and log at the pre-count.
8. **Idaho and Montana metro slugs** were not available beyond the first 15 lines of their MT files (reading bodies was out of scope). Montana's seven come from its title; `kalispell` is my short slug for "Kalispell/Flathead". Idaho lists only the Treasure Valley by name.
9. **Texas.** ST-TEXAS and MT-TEXAS are marked "live page". MT-TEXAS also feeds the GEO-1 marker pass and the four folded Texas metros (McAllen, El Paso, Lubbock, Corpus Christi), which GEO-1 owns.
10. **Charter section.** The saved blocks tell the lane to `git fetch origin` and hash the fetched rulebook. NIGHT-BRIEF forbids GitHub, so the derived blocks hash the copies in the worktree instead (same expected hash) and add the amendment's hash. Everything else in the structure is copied. The issued line states the derivation.
11. **promised-add.json** holds 88 URLs, none of them already in promised.json: 10 state pages, 62 promised metros (already pending on the site, but not in the file), and 16 cases. Idaho and Montana metro slugs are left out until the lane chooses them (new metro slugs arrive by request, I12).
12. **Titles.** In INVENTORY.tsv the six real-subject files carry a withheld title (their titles name the business), and a few titles are cut at 80 characters.
13. **Entries without a Research ID** are marked "not a state/case file" in the inventory; they are not ST or CS files, so none of them could hold a state or case.

## Every ST- file and where it went

| Research ID | Where it went |
|---|---|
| ST-ALABAMA | GEO-1 /states/alabama/ |
| ST-ARIZONA | GEO-4 /states/arizona/ |
| ST-ARKANSAS | GEO-1 /states/arkansas/ |
| ST-CALIFORNIA | GEO-4 /states/california/ |
| ST-CONNECTICUT | GEO-2 /states/connecticut/ |
| ST-DELAWARE | GEO-2 /states/delaware/ |
| ST-FLORIDA | GEO-1 /states/florida/ |
| ST-GEORGIA | GEO-1 /states/georgia/ |
| ST-HAWAII | GEO-4 /states/hawaii/ |
| ST-IDAHO | GEO-4 /states/idaho/ |
| ST-ILLINOIS | GEO-3 /states/illinois/ |
| ST-INDIANA | GEO-3 /states/indiana/ |
| ST-IOWA | GEO-3 /states/iowa/ |
| ST-KANSAS | GEO-3 /states/kansas/ |
| ST-KENTUCKY | GEO-1 /states/kentucky/ |
| ST-LOUISIANA | GEO-1 /states/louisiana/ |
| ST-MAINE | GEO-2 /states/maine/ |
| ST-MARYLAND | GEO-2 /states/maryland/ |
| ST-MASSACHUSETTS | GEO-2 /states/massachusetts/ |
| ST-MICHIGAN | GEO-3 /states/michigan/ |
| ST-MINNESOTA | GEO-3 /states/minnesota/ |
| ST-MISSISSIPPI | GEO-1 /states/mississippi/ |
| ST-MISSOURI | GEO-3 /states/missouri/ |
| ST-MONTANA | GEO-4 /states/montana/ |
| ST-NEBRASKA | GEO-3 /states/nebraska/ |
| ST-NEVADA | GEO-4 /states/nevada/ |
| ST-NEW-HAMPSHIRE | GEO-2 /states/new-hampshire/ |
| ST-NEW-JERSEY | GEO-2 /states/new-jersey/ |
| ST-NEW-MEXICO | GEO-4 /states/new-mexico/ |
| ST-NEW-YORK | GEO-2 /states/new-york/ |
| ST-NORTH-CAROLINA | GEO-1 /states/north-carolina/ |
| ST-OHIO | GEO-3 /states/ohio/ |
| ST-OKLAHOMA | GEO-1 /states/oklahoma/ |
| ST-OREGON | GEO-4 /states/oregon/ |
| ST-PENNSYLVANIA | GEO-2 /states/pennsylvania/ |
| ST-RHODE-ISLAND | GEO-2 /states/rhode-island/ |
| ST-SOUTH-CAROLINA | GEO-1 /states/south-carolina/ |
| ST-TENNESSEE | GEO-1 /states/tennessee/ |
| ST-TEXAS | live page /states/texas/ (state page) |
| ST-UTAH | GEO-4 /states/utah/ |
| ST-WASHINGTON | GEO-4 /states/washington/ |
| ST-WEST-VIRGINIA | GEO-2 /states/west-virginia/ |
| ST-WISCONSIN | GEO-3 /states/wisconsin/ |

## Every MT- file (for completeness)

| Research ID | Where it went |
|---|---|
| MT-ALABAMA | GEO-1 /states/alabama/ (metros) |
| MT-ARIZONA | GEO-4 /states/arizona/ (metros) |
| MT-ARKANSAS | GEO-1 /states/arkansas/ (metros) |
| MT-CALIFORNIA | GEO-4 /states/california/ (metros) |
| MT-CONNECTICUT | GEO-2 /states/connecticut/ (metros) |
| MT-DELAWARE | GEO-2 /states/delaware/ (metros) |
| MT-FLORIDA | GEO-1 /states/florida/ (metros) |
| MT-GEORGIA | GEO-1 /states/georgia/ (metros) |
| MT-HAWAII | GEO-4 /states/hawaii/ (metros) |
| MT-IDAHO | GEO-4 /states/idaho/ (metros) |
| MT-ILLINOIS | GEO-3 /states/illinois/ (metros) |
| MT-INDIANA | GEO-3 /states/indiana/ (metros) |
| MT-IOWA | GEO-3 /states/iowa/ (metros) |
| MT-KANSAS | GEO-3 /states/kansas/ (metros) |
| MT-KENTUCKY | GEO-1 /states/kentucky/ (metros) |
| MT-LOUISIANA | GEO-1 /states/louisiana/ (metros) |
| MT-MAINE | GEO-2 /states/maine/ (metros) |
| MT-MARYLAND | GEO-2 /states/maryland/ (metros) |
| MT-MASSACHUSETTS | GEO-2 /states/massachusetts/ (metros) |
| MT-MICHIGAN | GEO-3 /states/michigan/ (metros) |
| MT-MINNESOTA | GEO-3 /states/minnesota/ (metros) |
| MT-MISSISSIPPI | GEO-1 /states/mississippi/ (metros) |
| MT-MISSOURI | GEO-3 /states/missouri/ (metros) |
| MT-MONTANA | GEO-4 /states/montana/ (metros) |
| MT-NEBRASKA | GEO-3 /states/nebraska/ (metros) |
| MT-NEVADA | GEO-4 /states/nevada/ (metros) |
| MT-NEW-HAMPSHIRE | GEO-2 /states/new-hampshire/ (metros) |
| MT-NEW-JERSEY | GEO-2 /states/new-jersey/ (metros) |
| MT-NEW-MEXICO | GEO-4 /states/new-mexico/ (metros) |
| MT-NEW-YORK | GEO-2 /states/new-york/ (metros) |
| MT-NORTH-CAROLINA | GEO-1 /states/north-carolina/ (metros) |
| MT-OHIO | GEO-3 /states/ohio/ (metros) |
| MT-OKLAHOMA | GEO-1 /states/oklahoma/ (metros) |
| MT-OREGON | GEO-4 /states/oregon/ (metros) |
| MT-RHODE-ISLAND | GEO-2 /states/rhode-island/ (metros) |
| MT-SOUTH-CAROLINA | GEO-1 /states/south-carolina/ (metros) |
| MT-TENNESSEE | GEO-1 /states/tennessee/ (metros) |
| MT-TEXAS | live page /states/texas/ (metros: 4 live, 4 folded; GEO-1 marker pass) |
| MT-UTAH | GEO-4 /states/utah/ (metros) |
| MT-WASHINGTON | GEO-4 /states/washington/ (metros) |
| MT-WEST-VIRGINIA | GEO-2 /states/west-virginia/ (metros) |
| MT-WISCONSIN | GEO-3 /states/wisconsin/ (metros) |

## Every CS- file and where it went

| Research ID | Where it went |
|---|---|
| CS-R-ASSISTED-LIVING-ARIZONA-HUD | CASE-3 /case-studies/assisted-living-arizona-hud/ (rebuild) |
| CS-R-ASSISTED-LIVING-CALIFORNIA-HUD | CASE-3 /case-studies/assisted-living-california-hud/ (rebuild) |
| CS-R-ASSISTED-LIVING-FLORIDA-HUD | CASE-3 /case-studies/assisted-living-florida-hud/ (rebuild) |
| CS-R-ASSISTED-LIVING-HAWAII-HUD | CASE-3 /case-studies/assisted-living-hawaii-hud/ (rebuild) |
| CS-R-ASSISTED-LIVING-NORTH-CAROLINA-HUD | CASE-3 /case-studies/assisted-living-north-carolina-hud/ (rebuild) |
| CS-R-ASSISTED-LIVING-TEXAS-HUD | live page /case-studies/assisted-living-texas-hud/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-AUTO-DEALERSHIP-TEXAS-SBA | live page /case-studies/auto-dealership-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-AUTO-SERVICE-NEW-JERSEY-SBA | CASE-2 /case-studies/auto-service-new-jersey-sba/ (real-subject file, ruling 7) |
| CS-R-BEHAVIORAL-HEALTH-MASSACHUSETTS-CONVENTIONAL | CASE-4 /case-studies/behavioral-health-massachusetts-conventional/ |
| CS-R-CAR-WASH-TEXAS-SBA | live page /case-studies/car-wash-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-CHILDCARE-ILLINOIS-SBA | CASE-3 /case-studies/childcare-illinois-sba/ (rebuild) |
| CS-R-CHILDCARE-IOWA-SBA | CASE-3 /case-studies/childcare-iowa-sba/ (rebuild) |
| CS-R-COFFEE-SHOP-WASHINGTON-SBA | CASE-2 /case-studies/coffee-shop-washington-sba/ |
| CS-R-FITNESS-MINNESOTA-SBA | CASE-1 /case-studies/fitness-minnesota-sba/ |
| CS-R-FITNESS-NEW-HAMPSHIRE-SBA | CASE-1 /case-studies/fitness-new-hampshire-sba/ |
| CS-R-FUNERAL-HOME-WISCONSIN-SBA | CASE-3 /case-studies/funeral-home-wisconsin-sba/ (rebuild) |
| CS-R-GAS-STATION-ALABAMA-SBA | live page /case-studies/gas-station-alabama-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-GAS-STATION-FLORIDA-SBA | live page /case-studies/gas-station-florida-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-GAS-STATION-GEORGIA-SBA | live page /case-studies/gas-station-georgia-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-GAS-STATION-TEXAS-SBA | live page /case-studies/gas-station-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-GLAMPING-UTAH-USDA | CASE-1 /case-studies/glamping-utah-usda/ |
| CS-R-GROCERY-STORE-MISSISSIPPI-USDA | CASE-1 /case-studies/grocery-store-mississippi-usda/ |
| CS-R-HOTEL-FLORIDA-SBA | CASE-1 /case-studies/hotel-florida-sba/ |
| CS-R-HOTEL-GEORGIA-SBA | CASE-1 /case-studies/hotel-georgia-sba/ |
| CS-R-HOTEL-NEVADA-EB5 | CASE-4 /case-studies/hotel-nevada-eb5/ |
| CS-R-HOTEL-SOUTH-CAROLINA-SBA | CASE-1 /case-studies/hotel-south-carolina-sba/ |
| CS-R-HOTEL-TEXAS-SBA | live page /case-studies/hotel-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-LAUNDROMAT-NEW-MEXICO-SBA | CASE-3 /case-studies/laundromat-new-mexico-sba/ (rebuild) |
| CS-R-MARINA-MARYLAND-SBA | CASE-1 /case-studies/marina-maryland-sba/ (real-subject file, ruling 7) |
| CS-R-MEAT-PROCESSING-GEORGIA-USDA | CASE-2 /case-studies/meat-processing-georgia-usda/ |
| CS-R-MEAT-PROCESSING-NORTH-CAROLINA-USDA | CASE-2 /case-studies/meat-processing-north-carolina-usda/ |
| CS-R-MEAT-PROCESSING-TEXAS-USDA | live page /case-studies/meat-processing-texas-usda/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-MEDICAL-OFFICE-NORTH-CAROLINA-SBA | CASE-3 /case-studies/medical-office-north-carolina-sba/ (rebuild) |
| CS-R-MULTIFAMILY-ARIZONA-AGENCY | CASE-4 /case-studies/multifamily-arizona-agency/ |
| CS-R-MULTIFAMILY-FLORIDA-AGENCY | CASE-4 /case-studies/multifamily-florida-agency/ |
| CS-R-MULTIFAMILY-GEORGIA-AGENCY | CASE-4 /case-studies/multifamily-georgia-agency/ |
| CS-R-MULTIFAMILY-NEW-YORK-AGENCY | CASE-4 /case-studies/multifamily-new-york-agency/ |
| CS-R-MULTIFAMILY-NORTH-CAROLINA-AGENCY | CASE-4 /case-studies/multifamily-north-carolina-agency/ |
| CS-R-PET-BOARDING-OREGON-SBA | CASE-3 /case-studies/pet-boarding-oregon-sba/ (rebuild) |
| CS-R-PRIVATE-SCHOOL-CONNECTICUT-CONVENTIONAL | CASE-4 /case-studies/private-school-connecticut-conventional/ |
| CS-R-QSR-ARKANSAS-SBA | CASE-2 /case-studies/qsr-arkansas-sba/ |
| CS-R-QSR-GEORGIA-SBA | CASE-2 /case-studies/qsr-georgia-sba/ |
| CS-R-RESTAURANT-MISSOURI-SBA | CASE-2 /case-studies/restaurant-missouri-sba/ (real-subject file, ruling 7) |
| CS-R-RETAIL-NEVADA-CONVENTIONAL | CASE-4 /case-studies/retail-nevada-conventional/ |
| CS-R-RV-BOAT-STORAGE-ARIZONA-SBA | CASE-2 /case-studies/rv-boat-storage-arizona-sba/ |
| CS-R-RV-BOAT-STORAGE-CALIFORNIA-SBA | CASE-2 /case-studies/rv-boat-storage-california-sba/ |
| CS-R-RV-BOAT-STORAGE-FLORIDA-SBA | CASE-2 /case-studies/rv-boat-storage-florida-sba/ |
| CS-R-RV-BOAT-STORAGE-TEXAS-SBA | live page /case-studies/rv-boat-storage-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-RV-PARK-ARIZONA-USDA | CASE-1 /case-studies/rv-park-arizona-usda/ |
| CS-R-RV-PARK-MAINE-USDA | CASE-1 /case-studies/rv-park-maine-usda/ |
| CS-R-RV-PARK-PENNSYLVANIA-USDA | CASE-1 /case-studies/rv-park-pennsylvania-usda/ |
| CS-R-RV-PARK-TEXAS-USDA | live page /case-studies/rv-park-texas-usda/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-SELF-STORAGE-ARIZONA-SBA | CASE-2 /case-studies/self-storage-arizona-sba/ |
| CS-R-SELF-STORAGE-INDIANA-SBA | CASE-2 /case-studies/self-storage-indiana-sba/ |
| CS-R-TRUCK-STOP-GEORGIA-SBA | CASE-2 /case-studies/truck-stop-georgia-sba/ |
| CS-R-TRUCK-STOP-OKLAHOMA-SBA | CASE-2 /case-studies/truck-stop-oklahoma-sba/ |
| CS-R-TRUCK-STOP-TEXAS-SBA | live page /case-studies/truck-stop-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-R-URGENT-CARE-FLORIDA-SBA | CASE-3 /case-studies/urgent-care-florida-sba/ (rebuild) |
| CS-N-ASSISTED-LIVING-KENTUCKY-BANK-BRIDGE | CASE-4 /case-studies/assisted-living-elizabethtown-kentucky-bridge/ |
| CS-N-CHILDCARE-LOUISIANA-SBA-7A | CASE-3 /case-studies/childcare-gonzales-louisiana-sba/ (new) |
| CS-N-HOTEL-KANSAS-USDA-BI | CASE-1 /case-studies/hotel-hays-kansas-usda/ |
| CS-N-HOTEL-LOUISIANA-EB5-RURAL-TEA | CASE-4 /case-studies/hotel-natchitoches-louisiana-eb5/ |
| CS-N-HOTEL-OHIO-SBA-7A-ACQUISITION | CASE-1 /case-studies/hotel-acquisition-fairlawn-ohio-sba/ (real-subject file, ruling 7) |
| CS-N-INDUSTRIAL-FLEX-KANSAS-CONVENTIONAL | CASE-4 /case-studies/industrial-flex-gardner-kansas-conventional/ |
| CS-N-LAUNDROMAT-ACQUISITION-OHIO-SBA-7A | CASE-3 /case-studies/laundromat-acquisition-huron-county-ohio-sba/ (new) (real-subject file, ruling 7) |
| CS-N-MEDICAL-OFFICE-ASC-TENNESSEE-SBA-504 | CASE-3 /case-studies/medical-office-lebanon-tennessee-sba/ (new) |
| CS-N-MULTIFAMILY-MIXED-USE-OHIO-EB5 | CASE-4 /case-studies/mixed-use-multifamily-euclid-ohio-eb5/ |
| CS-N-MULTIFAMILY-TENNESSEE-DSCR | CASE-4 /case-studies/multifamily-clarksville-tennessee-dscr/ |
| CS-N-RESTAURANT-ACQUISITION-LOUISIANA-SBA-7A | CASE-2 /case-studies/restaurant-acquisition-broussard-louisiana-sba/ |
| CS-N-RESTAURANT-NEW-BUILD-TENNESSEE-SBA-7A | CASE-2 /case-studies/restaurant-sevierville-tennessee-sba/ |
| CS-N-SELF-STORAGE-KENTUCKY-USDA | CASE-2 /case-studies/self-storage-bardstown-kentucky-usda/ |
| CS-N-SELF-STORAGE-OHIO-SBA-504 | CASE-2 /case-studies/self-storage-pataskala-ohio-sba/ |
| CS-N-URGENT-CARE-KENTUCKY-SBA-7A | CASE-3 /case-studies/urgent-care-elizabethtown-kentucky-sba/ (new) |
| CS-Q-COPPERAS-COVE-TEXAS-STORAGE-YARD | excluded: sits in the submarket of a live client engagement (ROLLOUT-1, never built) |
| CS-Q-GIG-HARBOR-WASHINGTON-MARINA | CASE-1 /case-studies/marina-gig-harbor-washington-sba/ (real-subject file, ruling 7) |
| CS-Q-HANKAMER-TEXAS-TRAVEL-CENTER | live page /case-studies/travel-center-hankamer-texas-usda/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-Q-JOHNSON-CITY-TEXAS-LODGING | live page /case-studies/lodging-retreat-johnson-city-texas-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-Q-KERHONKSON-NEW-YORK-RETREAT | CASE-1 /case-studies/retreat-center-kerhonkson-new-york-usda/ |
| CS-Q-NESS-CITY-KANSAS-GROCERY | CASE-1 /case-studies/grocery-store-ness-city-kansas-usda/ |
| CS-Q-NEW-BALTIMORE-MICHIGAN-MARINA | CASE-1 /case-studies/marina-new-baltimore-michigan-sba/ |
| CS-Q-PORT-CHARLOTTE-FLORIDA-CAR-WASH | CASE-2 /case-studies/car-wash-port-charlotte-florida-sba/ |
| CS-Q-SHELL-KNOB-MISSOURI-MARINA | CASE-1 /case-studies/marina-shell-knob-missouri-usda/ |
| CS-Q-VERSAILLES-OHIO-GAS-STATION | live page /case-studies/gas-station-versailles-ohio-sba/ (WEB-FSC-6 finished case, not rebuilt) |
| CS-Q-YUCCA-VALLEY-CALIFORNIA-STR | CASE-4 /case-studies/short-term-rental-yucca-valley-california-conventional/ |
