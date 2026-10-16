# WEB-FSC-5 decisions

Each decision was taken without stopping, as speed rule 1 asks. Owner-facing items are marked **OWNER**.

## Doors (which hosts this lane may read)

**D1. www2.census.gov is closed by its robots.txt. OWNER.** The file opens with `User-agent: *`, a blank line, `User-agent: RavenCrawler`, then `Disallow: /`. RFC 9309 section 2.2 lets blank lines sit inside a group (`group = startgroupline *(startgroupline / emptyline) *(rule / emptyline)`), so `*` and `RavenCrawler` are one group and every unnamed agent is barred from the whole host. Google's reference parser reads it the same way: a new group starts only when a user-agent line follows a rule. The file is almost certainly an authoring slip, but the charter says never work around robots.txt, and the owner's 2026-09-22 and 2026-09-23 rulings that set robots aside applied to internal gathers, not to a lane whose output is served publicly. So PEP Vintage 2025, the Building Permits Survey, the CBP bulk files and the OMB delineation file (all on www2 only) are NOT FETCHED. Disclosure: the charter's step-zero host probe sent one GET to `https://www2.census.gov/` (HTTP 200, the directory page) before robots.txt had been read. Under this reading that path is disallowed too. No other www2 path was requested. The fetcher's evaluator was tested against the live robots bodies of all six hosts (12 of 12 cases), and against a control parser that splits groups on blank lines, which wrongly returns ALLOW for www2. **Reopen:** an owner ruling that www2.census.gov is fetchable; then `python3 scripts/markets_fetch.py --refresh` would fetch those files, but their parsers still have to be written against the real files.

**D2. The Census Data API is closed by a key wall. OWNER.** Every data request (acs/acs5 2024, acs/acs1 2024, cbp 2023, pep/charv 2023, geoinfo 2025, dec/pl 2020) returns HTTP 302 to `/data/missing_key.html` with `X-DataWebAPI-KeyError: 1`. The page says a valid key must be included with each data API request. The charter assumed keyless access with a daily limit; that is no longer true. `CENSUS_API_KEY` is not set, and creating an account is not something this lane does. Since freeze 1 the fetcher no longer assumes the wall: it sends one keyless data request per run (the 2023 CBP national count for one NAICS code) and records the response in the manifest's `probes`. At 10:38:34Z it got HTTP 302 to `missing_key.html` with `X-DataWebAPI-KeyError: 1`. If a keyless request ever returns data, the Census sources are fetched without a key. **Reopen:** the owner requests a free key at api.census.gov and puts it in `CENSUS_API_KEY` for the run. The fetcher sends it on the request only and redacts it from every recorded URL.

**D3. BLS QCEW is closed.** data.bls.gov robots.txt is `User-agent: *` / `Disallow: /` (the body is kept in `evidence/step0/`). NOT FETCHED. Disclosure: the charter's step-zero host probe sent one GET to `/cew/data/files/` before robots.txt had been read. It returned 403 to a User-Agent naming the product and a contact address on feasibility-study-company.com, as BLS asks. That 403 was seen in the session but its response was not kept, and no further request went to a disallowed BLS path.

**D4. BEA is closed.** apps.bea.gov robots.txt disallows `/regional/zip/` (CAINC1.zip). The step-zero host probe had already sent one GET to `/regional/zip/` before robots.txt was read; it returned 403, which was seen but not kept. robots allows `/api/`, but GetData needs a registered UserID (`BEA_API_KEY` not set). A keyless request to the API is now sent once per run and recorded in the manifest's `probes`; at 10:38:37Z it returned HTTP 200 with an empty body. robots also allows `/regional/bearfacts/`, but BEARFACTS is an interactive fact-sheet app whose data come from the app's own `/data/...` calls, one area at a time and largely POST. That is not a published file, and this lane makes read-only GETs of published files. NOT FETCHED. **Reopen:** a BEA API UserID in `BEA_API_KEY`; the fetch plan for CAINC1 lines 1 to 3 (county, state and MSA) is already written.

**D5. HUD Fair Market Rents are closed.** www.huduser.gov answered robots.txt (headers kept in `evidence/step0/`) and the FMR dataset page at step zero with HTTP 202, an empty body and `x-amzn-waf-action: challenge`. That is a bot check, not worked around. NOT FETCHED.

**D6. api.census.gov robots.txt** comes back as HTTP 200 with a 247-byte WAF "Request Rejected" HTML page. It has no robots groups, so it evaluates as allow-all. This is moot while the key wall stands (D2).

**D7. data.sba.gov moved to Drupal 11.** The CKAN API (`/api/3/action/...`) and the old dataset slug are gone (404). The files are read from the dataset page `https://data.sba.gov/dataset/7a-504-foia` (robots allows `/dataset/` except `/dataset/search?`). The fetcher discovers them there every run, because their names carry the as-of date (`asof_260630`) and change every quarter. The run fetched six CSVs and the data dictionary as of 30 June 2026 (last modified 21 July 2026).

**D8. User-Agent:** `FSC-MarketsRegister/1.0 (federal statistics register for feasibility-study-company.com; contact info@feasibility-study-company.com)`. `info@` is the contact address the site already publishes (126 mentions); the commit identity's `noreply@` is not a contact.

**D9. No third-party Python.** The pipeline uses the standard library only (urllib, csv, zipfile with ElementTree for xlsx, json, hashlib), so there is no virtualenv and nothing installs system-wide. Every network call carries a 60 s socket timeout and at most 4 tries, and large files resume from a `.part` file with an HTTP Range request.

## Inputs read from the site

**D10. 253 market slugs.** A Python regex over all 160 HTML pages at the cut point found 253 distinct `/states/<state>/<market>/` anchors in 33 states: 8 in most, Hawaii 6, Missouri 7, Wisconsin 7, Ohio 1 (`columbus`, linked from the home page only; there is no Ohio state page). An earlier shell pipeline (`git grep -o | sed | sort -u`) returned 252, dropping `iowa/waterloo-cedar-falls`. The Python enumeration was checked per state against every `states/<state>/` reference, so the 252 was the instrument's fault, not the site's.

**D11. 43 asset classes.** The 28 built hubs plus the 15 unbuilt hub paths the charter lists. The site also links three more unbuilt hub paths: `/asset-classes/assisted-living/` and `/asset-classes/industrial/` (from two practice-area pages) and `/asset-classes/independent-living/` (from the assisted-living hub). Each is the short name of a class already in the 43 (`assisted-living-and-memory-care`, `industrial-and-warehouse`, `independent-living-and-ccrc`). They are recorded as aliases in `naics-map.json`, not as extra classes.

## The SBA FOIA register

**D12. Status classification** (`data/markets/foia-status-map.json`). The values come from SBA's data dictionary. Every distinct status value in each file was enumerated; the build fails on an unlisted value and on any charge-off evidence (a ChargeOffDate, or GrossChargeOffAmount above zero) under a status that is not charged off. 7(a) writes paid-in-full as `P I F` (with spaces), while the dictionary writes `PIF`; both are listed. The files as of 30 June 2026 carry one charged-off code, `CHGOFF`, in both programs. The split the charter warned about is not present, and the build re-checks for it on every run. Disbursed: paid in full, `CHGOFF`, `EXEMPT` (disbursed, active, status withheld under FOIA Exemption 4) and 504 `CLOSED`. `CLOSED` counts as disbursed because 337 of its 339 rows carry a FirstDisbursementDate. Not disbursed, so never in a denominator: `CANCLD`, 7(a) `COMMIT` and 504 `NOT FUNDED`; none of those rows has a FirstDisbursementDate. Measured counts are regenerated in `foia-status-counts.json` rather than typed (one hand-typed evidence count was wrong and was removed for that reason).

**D13. Definitions.** `loans` = approvals net of cancellations, which keeps undisbursed live approvals. `volume` = GrossApproval of those loans (504: the SBA/CDC debenture amount, not the project). `disbursed`, `chgoff_n` (by approval cohort) and `chgoff_amt` (GrossChargeOffAmount). The charge-off rate covers seasoned cohorts only: approval FY2011 to FY2020 pooled, each at least five full fiscal years old at the 30 June 2026 as-of date. It is computed as summed charge-offs over summed disbursed loans, never as an average of rates, with a flag when fewer than 30 loans were disbursed. The same applies by amount. Windows: all, FY2016-2025 (the headline), FY2021-2025, FY2025 and FY2026 to date, plus a by-year array. FOIA lists every approval, so a zero is a true zero, not a suppression. The full text is in `sources.json` under `definitions`.

**D14. NAICS editions are mixed in the files.** A 2022 code (457110) appears on loans approved in FY1995, and 447110 on loans approved in FY2026, so SBA re-codes old loans. A loan therefore belongs to a class when its code is in ANY edition list for that class, never only the edition of its approval year. The 43-class map was drafted offline by the mapping subagent from the FOIA code inventory: 22 exact, 13 partial, 8 proxy, 0 none. The census.gov concordance files are outside the six hosts, so the edition lists rest on the drafter's knowledge and are not checked against a concordance. `naics-evidence.json` measures FOIA loans by class, code and edition on every build, so a class losing loans to a code change shows up there. One invalid code in the draft (722300, a single loan with a blank description) was dropped. The three extra linked hub paths are recorded as aliases (D11). Classes overlap by design (hotel and its four service-level subtypes all use 721110), and the series say never to sum across classes.

**D15. Connecticut in FOIA: two schemes in one file.** SBA's ProjectCounty for CT holds both the eight legacy counties (FAIRFIELD, HARTFORD, ...) and the nine planning regions (CAPITOL, WESTERN CT, NW HILLS, ...). The planning-region codes appear on loans approved as early as FY2000, so SBA re-coded loans rather than switching at a date (`foia-geocoding.json` has the split by FY). The schemes do not nest, so no CT market has a FOIA total; its own id is null with that reason. It has two exact components instead: `<market>:legacy` (loans coded to the legacy counties of its legacy composition) and `<market>:pr` (loans coded to the planning regions of its planning-region composition). Each CT row records both compositions and how well each fits. The two components are never added together.

**D16. Which compositions carry figures now.** Each market row has a `composition_source`. single-county (40), page-named-counties (19) and judgement-region (29, `review` true) are summed from their FOIA county strings now: 88 markets. cbsa-delineation-pending (137) covers every market whose counties rest on CBSA, CSA or micropolitan membership: kind cbsa, the "union of CBSAs" county-sets, the quad-cities rows defined as CBSA 19340, and seven county-sets the assembler's text rule missed and attacker one found (D27). Those counties must come from the OMB delineation file, which this lane could not fetch (D1, D2). The composers' recalled county lists are kept in the row, marked unverified, but no figure is built from them. That holds even where the recall is probably right, because a CBSA's membership is a federal fact this lane cannot check. sub-county (20 places and tract-sets) get no FOIA figure, because the FOIA project location is a county. connecticut-two-schemes covers 8 markets (D15). So the eight Texas markets, all single CBSAs, carry no figures, and gate 9 states that reason for each.

**D17. Composition calls that depart from the charter's slug reading.** bar-harbor is Hancock County, because the page text names it (`review` true). park-city (Summit County) and hillsboro (Washington County, Oregon) are counties because their headings name the county. The charter reads them as a town and a city, so the assembler forces `review` true on both. moab is a five-county parks region taken from the page text (`review` true). council-bluffs is a place, Council Bluffs city, because the page treats it as a distinct sub-economy inside the Omaha CBSA (`review` true). edmond is a place lying in Oklahoma and Logan counties (`review` true). provo-orem, st-george, logan and madison are single counties their headings name, which matches the charter, so `review` is false. The owner reviews every `review` row; CLOSE lists them.

**D18. Cross-state markets** carry the whole region and one component per state part (`<market>:nm`, `<market>:tx`). permian-basin (New Mexico page) is resolved as a judgement region: Lea and Eddy, which the page names, plus 17 Texas counties as commonly bounded. metro-east is the two Illinois counties the page names. Both quad-cities rows rest on CBSA 19340 and are pending.

**D19. Geography ids.** `us`; a state's USPS code in lower case (`tx`); a market `<state-slug>/<market-slug>`; components `<market>:<part>`. County FIPS (`co-…`) and CBSA (`cbsa-…`) ids are reserved for when a Census roster is fetched. No federal source of FIPS codes was reachable, so FIPS codes appear only as the composers' unverified annotations. FOIA figures are keyed by state and market, and the FOIA county strings are kept in `foia-county-strings.json` for the later FIPS join.

**D20. Size.** A first build was 53 MB, against the 60 MB cap and with no Census series yet. Series files now carry the page-facing metrics only (loans, volume, cancelled, disbursed, charge-off count and amount, the two rates). approved, approved_vol, undisbursed and disbursed_vol stay internal to the reconciliation. Bundles cover site markets and the 33 site states. At freeze 2: 30.72 MB (29.30 MiB), largest file 1.92 MB (the gate measures both units; an earlier "29.63 MB" was MiB).

**D21. Audit counting unit.** One value per (series, class) at the headline window, excluding by-year values. Component values (CT schemes, cross-state parts) are counted in their own column and do not make a market standalone. With FOIA as the only source, every summed market clears 25 easily, because 2 programs x 8 series x 44 classes gives about 700 values. The `sources_contributing` column shows they all rest on one source. The standalone count should be re-read once Census series arrive.

**D22. No parser was written for a source whose file this lane could not see.** The fetch plans for the Census API (ACS 5-year and 1-year, CBP, PEP Vintage 2023, geoinfo, the 2020 Connecticut county subdivisions) and the BEA API are written and gated on `CENSUS_API_KEY` and `BEA_API_KEY`. Building series from them needs parsers written and checked against real responses; guessing at suppression sentinels is the failure trap 3 describes. `markets_fetch.py --refresh` treats every NOT FETCHED source as due, so the first keyed run fetches them.

## After the freeze 1 review (verifier and two attackers on e7cc263)

**D23. Exact-duplicate rows are counted as published.** The 7(a) files carry 1,918 rows identical in every field to an earlier row of the same file; 531 are not cancelled ($250,499,334 gross approval). The 504 files carry 69 such rows, 3 not cancelled ($777,000). The files have no loan identifier (LocationID is the lender), so a listing error cannot be told from twin loans, and the register counts every row. The live duplicates are 0.03% of 7(a) loans and 0.05% of volume. The counts are measured on every build into `reconciliation.json` under `raw_file_properties`. Found by the gate-6 checker and confirmed by recount.

**D24. Other raw properties kept as published:** one 7(a) FY1995 paid-in-full row with GrossApproval of minus $120,000, 180 7(a) and 2 504 charge-offs with a zero amount, and 58 7(a) charge-offs with no ChargeOffDate. These are also in `raw_file_properties`. ProjectState `TQ` (8 7(a) rows, FY1991-95) is not a USPS code; it stays a geography as SBA writes it, with a note in `geographies.json`.

**D25. Class figures before FY2001 undercount (attacker two, A2-1 and A2-2, reproduced).** Before FY2001 SBA left NaicsCode blank on whole industries. In the register's own by-year cells, 7(a) hotel loans are 0, 0, 0, 0, 0, 5, 11 for FY1991 to FY1997, and restaurants about 0 to FY1997, while childcare and car washes are fully coded. FY1998 to FY2000 restaurants are nearly all coded 722110, quick-service brands included. Blank-code rows: 7(a) 203,850 (176,915 net of cancellations), 504 21,922 (18,655 net), measured by FY in `naics-evidence.json`. No imputation, which the charter forbids. Instead the series carry `class_complete_from_fy` = 2001, and `scripts/markets.py` refuses a class figure for the window "all" or an approval year before FY2001 unless the marker sets `allow_flag` and the page says so. "all" (every loan), the FY2016-2025 headline and the seasoned charge-off rates (FY2011-2020) are unaffected.

**D26. NAICS map revisions (attacker two, A2-3 to A2-7).** auto-dealership adds RV dealers (441210), boat dealers (441222) and the motorcycle and other-vehicle chain (441221/441229 to 2007, 441228 2012-2017, 441227 2022), and is graded partial, because heavy-truck dealers sit in 423110 with all motor vehicle wholesalers. auto-service-and-collision adds tire dealers (441320, renamed 441340 in 2022). quick-service-restaurant adds snack and nonalcoholic beverage bars (722213, then 722515), because the hub covers coffee and beverage quick service. fitness-and-recreation adds 611620 (martial arts and other instruction) and is graded partial. assisted-living-and-memory-care and ccrc-life-plan-communities are regraded partial. Grades are now 18 exact, 17 partial, 8 proxy. `naics-evidence.json` now reports the number of distinct codes in no class (1,313), not program-and-code pairs.

**D27. Composition corrections (attacker one, F2 to F4 and F7, each read against the row's own text).** Seven summed markets took their county lists from recalled CBSA, CSA or micropolitan membership. The assembler's rule read only the basis field, while these rows said it in the reason: michigan/flint, minnesota/mankato, mississippi/hattiesburg, missouri/branson, missouri/jefferson-city, north-carolina/greensboro, washington/yakima. They are now cbsa-delineation-pending by an explicit, reasoned override. All 37 summed rows whose text mentions a metro were read; the other 30 name their counties on the page, or are judgement regions that only mention a metro for context. F3 (hattiesburg omits Covington County) is moot while pending and is recorded on the row. F4: wisconsin/wausau claims the ten-county North Central Wisconsin planning region but listed Price County, which is not in it, in place of Juneau; it is corrected to match its stated basis. F7: an approximate Connecticut component now needs `{"scheme_fit": "approximate"}` on its marker, and waterbury's legacy fit note now names Bristol (Hartford County). maine/bangor (pending) beside maine/bath (summed) is consistent with the rule: bangor is kind cbsa, while the page names Sagadahoc County for bath.

**D28. Renderer and flag fixes (attacker one, F1, F5 and F6).** F1: the small-sample flag on the charge-off rate by amount compared a dollar denominator with 30 and never fired (6,890 cells). Both rates now flag on the disbursed-loan count, and gate 7 checks every rate cell. F5: the rate series rows in `sources.json` now give their period as the FY2011-2020 cohorts, and a rate marker with `window` or `fy` is refused. F6: a source line must cite a period that a value marker for the same geography and series on the page shows; a source line for a null geography is refused; a share must print as pct and a dollar amount as usd.

**D29. Fetch plan fix (verifier, major).** The fetcher would not have fetched CBSA membership even with a key: it read state codes from a file that does not exist, and its CBSA list was always empty. geoinfo now runs first and in two phases. It fetches the state and CBSA lists, then one summary-level-313 request per CBSA (its member counties) and one county-subdivision request per state, planned from those lists. ACS county subdivisions use the same state list. Tested offline by planning from fake first-phase files (8 geoinfo requests for 2 states and 2 CBSAs, 14 ACS 5-year, and CBP at 4 requests per NAICS 2022 code: 412 with the 103 codes of the revised map). Never run against the live API, which needs a key; the first keyed run is the real test.

**D30. Evidence the verifier could not find.** The fetcher now keeps each robots.txt body in the manifest. `docs/web-fsc-5/evidence/step0/` holds the six robots bodies and their response headers from step zero (cookies stripped), and an extract of the Census API catalogue (249 rows): no county Building Permits Survey dataset; latest vintages acs5 2024, acs1 2024, cbp 2023, pep/charv 2023, geoinfo 2025. The key probes are recorded per run (D2, D4). GATES.txt now names its runner and says which gates run shell commands.

**D31. permian-basin is a judgement region.** Its New Mexico part is page-named but its 17 Texas counties are not, so its `composition_source` is set to judgement-region by override.

## After the freeze 2 re-check (all 12 items resolved, no regression, 10 minors)

**D32. Minors fixed for freeze 3.**
- A keyless probe that fails at the network is now reported as a failed probe, not as a key wall.
- Format guards follow D28 exactly: a share prints with pct or pct1, a dollar amount with usd or usd_m, a count with int or num, and a marker must name its fmt.
- The composition-pending reason is read from the manifest's census_geoinfo and census_delineation records, no longer hard-coded.
- `negative_gross_approval_rows` is an integer.
- The class coverage note now names every year from FY2001 on where blank NAICS codes exceed 1% of rows. That is 504 FY2013 (2.7%) and FY2014 (1.6%), with FY2012 at about 1.0%; there, by-year class values undercount by about that share. The windows from FY2016 are unaffected.
- The freeze record now carries the manifest's door and probe records (robots bodies included), and the refusal text says so, so the key-wall and robots evidence is tracked.
- D1 now discloses the step-zero GET of www2.census.gov `/`.
- D29's CBP request count is corrected to 412.
- CLOSE's gate-7 sentence now gives the flag split.
- The first fetch run's log (09:37Z, untracked) printed `GET` lines for robots-disallowed URLs before the code checked the door: the log line came first. `get()` checked the door before any request in that version too, so no request was sent. The order was fixed before freeze 1.

**D33. A freeze superseded before review.** The freeze taken at `35433de` was dropped within minutes and its record deleted, because CLOSE's size figures in it were stale. The fuller composition-pending reasons (D32) had grown data/markets from 30.72 MB to 31.63 MB. No reviewer saw it. The final freeze carries the corrected figures.

## The owner's 16 Oct correction: keyed fetches

**D34. Keys.** The owner wrote that free Census, BLS and BEA API keys were registered on 19 Aug, and named where to look. The credentials file named in the correction exists in the owner's analytics estate. Its path is not written here, because this repo is public and gate 10 bars the sister firm's name. It defines `CENSUS_API_KEY` (40 characters), `BLS_API_KEY` (32) and `BEA_API_KEY` (36). Only the variable names and lengths were ever displayed. The configuration folder the correction names holds only a data.gov key, which the correction does not name and which was not used. The keys are loaded into the environment of the fetch run only. The fetcher sends them on the request and redacts `key=`, `UserID=` and `registrationkey=` from every recorded URL and message. No key value is in the repo, a log, a manifest or a commit.

**D35. API doors, read first as the correction asks.**
- `api.census.gov/robots.txt` has no robots groups (a 200 WAF page), so the API is open.
- `apps.bea.gov/robots.txt` explicitly allows `/api/`, so it is open.
- `api.bls.gov/robots.txt` is `User-agent: *` / `Disallow: /`, so the BLS API path is closed by its own host's robots. Under the correction's rule ("an API path open by robots is fine"), QCEW stays NOT FETCHED and no request, not even a key probe, went to the BLS API.
- The new source row `bls_qcew_api` records the refusal.

**D36. User agent.** The correction sets the user agent for this run. The fetcher reads it from `MARKETS_UA` at run time, and the robots product token follows it. The value is not written in this repo (gate 10). One stream per host: the fetcher is sequential, with a pause between requests.

**D37. Census Data API behaviour measured on 2026-10-16.**
- Spaces must be sent as `%20` and `/` left literal. `+` or `%2F` gets "unknown/unsupported geography hierarchy".
- geoinfo takes no wildcard CBSA or state in the CBSA hierarchies: summary level 313 needs an explicit CBSA and state. A wildcard across all CBSAs returned 503.
- The roster is therefore fetched in three phases: (1) states, counties, CBSAs and places; (2) per state, its CBSA parts (summary level 320) and county subdivisions; (3) per CBSA part, its member counties (summary level 313), about 1,000 requests at about 4 seconds each.
- PEP `pep/charv` needs `AGE=0000`, `SEX=0`, `HISP=0`, `POPGROUP=001` to return totals; without them it returns thousands of rows a county.
- An empty CBP response means no establishment in that code at that geography.

**D38. "Land as in item 7".** When the correction arrived, no 16 Oct rulings list could be found, in any session transcript since 15 Oct or in the FSC repo and its worktrees. The owner's rulings of 16 October then arrived in this session (D42) and set the landing path: merge main, rerun gates 1, 10 and 11, freeze, fast-forward, push or bundle. A series NOT FETCHED for a recorded refusal does not block landing; every other gate must be green.

**D39. Resolution against the federal roster** (`docs/web-fsc-5/tools/resolve_geographies.py`; all from fetched files, nothing typed):
- SBA's USPS state codes are matched to Census state codes by the overlap of their county-name sets.
- FOIA (state, ProjectCounty) strings join to 2025 county FIPS by normalised name. Strings of renamed or split counties and Connecticut's legacy counties stay unmatched and are listed in `geographies.json`.
- A cbsa market takes the federal membership of its CBSA. Its code is checked against the roster and the first city of its title, and the composer's recalled list is compared, with the difference noted.
- A composition that rests on CBSA membership but is not one CBSA (the "union of CBSAs" rows, the seven of D27, and quad-cities) becomes cbsa-union when the composer's counties equal the federal union of the CBSAs they touch, within the market's own states. Otherwise it is kept as the composer listed it, as a judgement region with `review` true and the difference written on the row.
- mississippi/hattiesburg takes the federal Hattiesburg CBSA plus Jones and Lauderdale, which is its stated basis.
- County names map to FIPS within the state. Places map to GEOIDs by exact name. Tract-sets stay unresolved, because tracts were not fetched.
- Connecticut keeps its planning-region FIPS, and for the legacy scheme, the 2020 towns of each legacy county, taken from the 2020 Census.

**D40. Census and BEA aggregation.**
- A cbsa market uses the CBSA's own published figures, medians included.
- A market of several counties, places or Connecticut towns sums its additive counts. ACS MOEs are combined as the root sum of squares, which Census gives as an approximation, and noted.
- Per capita income for a set is aggregate income (B19313) over population (B01003), and the unemployment rate is unemployed over civilian labor force, both from the sums.
- A median for a set is null with its component values: never averaged, never population-weighted.
- PEP Vintage 2023 covers July 2020 to July 2023 only, so the five-year change the charter asks for cannot be built within one vintage. The series give the 1-year change and the change since July 2020, labelled as such.
- CBP establishments per 10,000 residents use PEP's July 1, 2023 population, the same year as CBP 2023.
- BEA single areas carry BEA's published per capita figure (line 3). A set is summed line 1 over summed line 2, and is null where a member county is published only inside a BEA combined area.
- A place market has ACS figures only; PEP, CBP and BEA were not pulled at that grain.
- fairfield-county (legacy) has ACS figures summed from its 2020 towns. Its PEP and CBP figures are null.

**D41. Source rows for API pulls.** A source answered by more than ten responses records the API base URL, the number of responses, and the sha256 of its sorted file hashes, not one hash per response. Every response's own hash stays in the fetch manifest, which each freeze record copies.

## The owner's rulings of 16 October

**D42. The rulings, as applied.**
- Item 1: www2.census.gov is fetchable for the files the plan needs, one at a time, with the descriptive User-Agent. The fetcher's `ROBOTS_RULINGS` exempts that host for exactly the URLs listed in its source plan; every other www2 path is still refused. Fetched:
  - PEP Vintage 2025: `co-est2025-alldata.csv`, `cbsa-est2025-alldata.csv`, `NST-EST2025-ALLDATA.csv`.
  - Building Permits Survey: county files `co2021a.txt` to `co2025a.txt`, the 2022 re-upload notice, and `st2025a.txt`.
  - CBP 2023 complete files: `cbp23co/st/msa/us.zip`.
  - The OMB delineation file `list1_2023.xlsx`.
  - The Connecticut county-to-town crosswalk.
  - Three directory listings were read to confirm the latest vintages: CBP's newest year on www2 is 2023, the delineation's is July 2023, and the PEP and BPS folders hold the 2025 files.
- Item 2: the keys were already found (D34).
- Item 3: Census Data API and BEA API as in D35. The BLS Public Data API stays closed: `api.bls.gov/robots.txt` is `Disallow: /` for every agent, and the item 1 robots ruling covers www2.census.gov only. QCEW is NOT FETCHED with that recorded refusal, beside HUD (bot challenge). Neither blocks landing (item 4).
- Item 5: main had moved to `53ad912` (WEB-FSC-4). It was merged into web-fsc-5 cleanly (`e334cfb`); against main the lane still changes only its own paths.

**D43. CBP comes from the complete files, not the API.** At about 7 requests a minute the 412-request API pull would have taken an hour. The complete files, which the charter prefers, hold every industry for every county, state, metro and the nation in four downloads, including the statewide records the reconciliation needs. The API pull was stopped after 180 responses; they stay in the cache unused, and the source row says so.

**D44. CBP 2023 uses NAICS 2017 codes (charter trap 5, found by gate 5).** The 2023 complete files carry 447110, 447190 and 445120, not 457110, 457120 and 445131. The first build summed the NAICS 2022 lists and returned no gas-station establishments nationally, with no error. The build now counts which edition's distinctive codes a CBP file carries (54 codes only in NAICS 2017, 0 only in NAICS 2022), sums each class over that edition's list, and records the edition in the series. National gas stations and c-stores: 146,166 = 96,002 (447110) + 13,172 (447190) + 36,992 (445120).

**D45. CBP withholds detailed cells below the state (charter trap 3).**
- In Andrews County, Texas, the gasoline-station subsector shows 8 establishments, but its published 6-digit cells sum to 6. Two are withheld, not zero.
- For every geography and class, the build takes each class code that has no 6-digit cell there, finds its nearest published parent (5, 4, 3 or 2 digits), and takes that parent's count less its published 6-digit children. If any such gap exists, the class value is written `[value, up_to]`: a lower bound with up to that many establishments withheld.
- A published 6-digit cell is complete, so only absent codes are bounded. The renderer refuses a lower bound unless the marker sets allow_flag and the page says "at least".
- About 62% of county class cells and 41% of CBSA cells are lower bounds, mostly in multi-code classes. The Texas markets have 0 to 8 of their 43 classes bounded, and Houston and Dallas-Fort Worth none.
- Absent with no gap means zero, and such classes are left out of the file.

**D46. Building permits.** Units authorized come from the county files' estimates with imputation (not the reported-only groups), by structure type and total, for 2025 and for 2021 to 2025.
- A county missing from a year's file has no permit-issuing place in the BPS universe: it is null, never zero.
- A set sums its covered counties and flags partial coverage.
- A state's 2025 value is the published state-file row (the state file is in thousands of dollars for value; only units are used).
- The county files switch Connecticut from legacy counties (2021 and 2022) to planning regions (2023 to 2025), so no five-year Connecticut county total is built; it is null with that reason.

**D47. Census reconciliation (gate 3).** State against the sum of its counties:
- ACS and PEP: every state is equal.
- BEA: equal except Virginia and Hawaii, whose combined areas BEA publishes only as combinations.
- Permits: 28 of the 30 fully covered states are equal; Michigan (135 units) and Maine (114) are named as state-file units the county file does not place.
- CBP: the state may exceed its counties only by its statewide records plus the bound on withheld county cells. That holds in every state for gas stations and self-storage, and in 49 of 52 for hotels. California (2), Massachusetts (1) and New Jersey (1) are named residuals: every county there publishes 721110 and there is no statewide row, yet the state file counts one or two more.
- Differences are named with their measured amounts, never forced to zero.

**D48. Size.** With 225 summed markets, the first keyed build was 82 MB, against the 60 MB cap. The fixes:
- FOIA keeps three windows (all years, FY2016-2025, FY2021-2025); a single year is the by-year element of a count series, and the dollar series carry no by-year array.
- CBP leaves out zero classes and writes lower bounds as two-element lists; per-10,000 figures are rounded to 2 decimals.
- Bundles hold headline values only, without CBP employment and per-10,000.
- State parts are made only for markets of kind cross-state.

Result: 55.7 MB, largest file under 5 MB. A wave that adds many markets will need the FOIA series split by program or by state.

**D49. Gate 6 for the keyed data.** The FOIA check (`rederive.py`) and a new Census, CBP, permits and BEA check (`rederive_census.py`) were written by an independent subagent session against the raw files. Neither imports the pipeline.



## D50. Misread of the 16 Oct rulings (owner correction, 16 Oct)

**What happened.** I read the owner's rulings of 16 October as making www2.census.gov fetchable for named files. The owner then corrected that reading: www2.census.gov is CLOSED under the standing robots rule (its robots.txt bars every unnamed agent), and there is no owner exception for named files. I had already fetched 16 files from it, one at a time, between 12:17 and 12:18 UTC, and read eight www2 directory listings to find them (not saved).

**What is held.** The 16 files were moved, not deleted, to `_cache/markets/held/www2/` inside the lane's worktree. That folder is gitignored, and nothing is loaded from it or published. The manifest marks each file held, with its new path and a hash re-checked after the move (all unchanged). The fetcher's www2 exemption (`ROBOTS_RULINGS`) is empty again, so a refresh refuses every www2 path. The step-zero copy of www2's robots.txt in `evidence/step0/` is the robots file itself, not a data file, and stays.

| held file (under `_cache/markets/held/www2/`) | bytes | sha256 | retrieved (UTC) |
|---|---|---|---|
| `census_bps/2025_annual/co2021a.txt` | 372,012 | `ce2c9aa7b7c036ddbc99d6dc398ddf71e4a0ad0fc2782db883b559ca264f14b6` | 2026-10-16T12:18:02Z |
| `census_bps/2025_annual/co2022a.txt` | 374,937 | `0a88c16861ede81b04f8785e1c626e772510f33f1de9452f7592d86d308e2b5c` | 2026-10-16T12:18:04Z |
| `census_bps/2025_annual/co2022aupdatednotice.txt` | 190 | `bc83046236dd0647eb2b4edf7133348de67c0fd81f49b2a3dcd1b38e25df0142` | 2026-10-16T12:18:12Z |
| `census_bps/2025_annual/co2023a.txt` | 374,707 | `fab11d759e905ff61838b8dfa41c0f2082e150cad07a20c65ddd620a007aa158` | 2026-10-16T12:18:06Z |
| `census_bps/2025_annual/co2024a.txt` | 375,214 | `a64c2dd19be96c469763c10d637575a584ef16a6878f451bba80c847bcafc8c6` | 2026-10-16T12:18:08Z |
| `census_bps/2025_annual/co2025a.txt` | 375,314 | `5d523b1ff172c886ee7f2bc770c82c8c5470b5aaaec5f63441a18c621c80b30e` | 2026-10-16T12:18:11Z |
| `census_bps/2025_annual/st2025a.txt` | 10,744 | `eab29258ada8389b9f469c566eb6eb074cf128aa94c471e89f818a20a4d83afb` | 2026-10-16T12:18:14Z |
| `census_cbp_bulk/2023/cbp23co.zip` | 12,919,520 | `e9539e96ceb91608ad44ab1cfc651d7c1ff9b88bddfe7a8ff64134ccde6e9603` | 2026-10-16T12:18:18Z |
| `census_cbp_bulk/2023/cbp23msa.zip` | 7,070,587 | `b7c3afe15351e525bd1c1498a06018946b8f5fc9f70b87e2fc6f6df8c84800a1` | 2026-10-16T12:18:25Z |
| `census_cbp_bulk/2023/cbp23st.zip` | 11,115,845 | `9fc306ecc4f9633092e2432c2db2acdf53798da0480e6f6beeb953d583b41ede` | 2026-10-16T12:18:22Z |
| `census_cbp_bulk/2023/cbp23us.zip` | 750,265 | `3f9018f807f1ffd7bcbb00690f9792573bc2bc6bb4cfab9df14ca7ab3eac0862` | 2026-10-16T12:18:27Z |
| `census_ct_crosswalk/2022/ct_cou_to_cousub_crosswalk.txt` | 22,091 | `13ad002564e30e6dcd1df112fdaa985f2cd0cdb908f7f3017cd2723db294cff8` | 2026-10-16T12:18:31Z |
| `census_delineation/July_2023/list1_2023.xlsx` | 143,798 | `952c4b1e78acbb54e6ec9412434b7602fedacbf021736351a63c181bdb753629` | 2026-10-16T12:18:30Z |
| `census_pep/V2025/NST-EST2025-ALLDATA.csv` | 53,555 | `92188e29cb0a67dcf95afa7d6c47359409782f086478b70ea4128eb70e223ca9` | 2026-10-16T12:17:59Z |
| `census_pep/V2025/cbsa-est2025-alldata.csv` | 827,252 | `bf6fad83753456413d047d1acebeb434bd067eba9d6d0be62b3f737ad1301852` | 2026-10-16T12:17:58Z |
| `census_pep/V2025/co-est2025-alldata.csv` | 2,071,735 | `4f5a499d851e2cb48fd7a5405e5a9235453a8a66933657aacd10df0e264f35d5` | 2026-10-16T12:17:55Z |

**What was removed** from the register, the bundles and the code:
- the PEP Vintage 2025 series;
- every building-permits series;
- the CBP series built from the complete files;
- fairfield-county's Census figures built from the Connecticut crosswalk.

The delineation file had never been used: CBSA membership came from the Census Data API roster. The readers for these files are gone from `scripts/markets_census.py`.

**What replaced it**, from open sources only:
- **Population:** Census population estimates now come from the Vintage 2023 pull through the Census Data API (keyed). Series: July 1 2023, 2022 and 2020, the 1-year change, and the change since 2020. Vintage 2023 holds no five-year span, so no five-year change is built.
- **CBP 2023:** now through the Census Data API with every industry code in one request per level (nation, states, metros, and counties one state at a time): 55 responses, accepting what the API serves. That is NAICS 2017 codes, as D44 found in the complete files. Parents come with their children, so the withheld-cell lower bounds of D45 stand. The API publishes no county-999 statewide rows, so the CBP reconciliation now checks that no state falls below the sum of its counties, and names each difference with the withheld bound.
- **CBSA to county:** unchanged. It was always the Census Data API geoinfo roster (OMB Bulletin 23-01 membership, part by part); the OMB bulletin and NBER's crosswalk are not on this lane's hosts, and were not needed.
- **fairfield-county towns:** now from the 2020 Census (dec/pl, Census Data API), matched to the 2025 roster by five-digit town code (23 towns).
- **Building permits:** no open source exists (the Census Data API carries no county permits), so permits are NOT FETCHED with that reason.

**Superseded by this decision:**
- **D42:** item 1 is withdrawn; items 2 to 5 stand.
- **D43:** CBP now comes from the API, not the complete files. The partial per-code API pull was moved to `census_cbp/2023-superseded-per-code/` and is unused.
- **D46:** the permits series are removed.
- **D47:** the permits rows and the CBP statewide-record check are gone; the CBP check is replaced as above.
- **D48:** the sizes changed; GATES.txt has the final size.

**Independent check:** one round on the affected series (PEP, CBP, BEA after the collision fix below, fairfield-county ACS), as the owner asked; see GATES.txt gate 6.

**History:** the commit that held the www2-built series (`7cff37f`) and the merge after it (`e334cfb`) are kept, not deleted, on a local branch `held-web-fsc-5-www2`. That branch is never pushed or bundled. Branch web-fsc-5 is rebuilt from `d2dabc6`, plus a fresh merge of main and one commit of the www2-free lane, so no www2-built file is in the history that lands.

**BEA collision (found by the independent check, fixed).** BEA's state GeoFips (`SS000`) collided with two CBSA codes ending in 000: 32000 (Marion, NC) and 45000 (Susanville, CA). Those micropolitan areas carried Nevada's and South Carolina's state figures. BEA rows are now keyed by their file's level. The BEA API answered the MSA request with error 101, so no CBSA carries a BEA row of its own, and a CBSA market sums its member counties.

## D51. The independent check's round on the affected series: findings and fixes (16 October)

**The round** (as D50 asked, one round): seed 20261016, 797 sampled values (271 new: PEP Vintage 2023, CBP 2023, fairfield-county ACS 5-year), 765 matched, 32 did not, all in CBP. Its full sweep of the register compared 698,318 values and found 43,236 problems, all in CBP. The result is kept as `gates/rederive-census-result.round2.json`. ACS, BEA (after the D50 collision fix) and PEP matched in full, and the FOIA check, rerun on the same register, matched 352 of 352 with 0 problems in 4,416,192 values.

**Finding 1, Puerto Rico metro areas (30 sampled values).** The CBP API's metro response has no row for the ten Puerto Rico CBSAs (10380, 11640, 17620, 17640, 25020, 29720, 32420, 38660, 41980, 46580). The register gave them empty class lists, which the renderer reads as zero establishments. Fixed: a geography with no row at all in its CBP response is a null with that reason, never a zero. That covers the ten CBSAs and two counties with no row (15005 Kalawao, Hawaii; 48269 King, Texas). No site market uses any of them, and the Texas state row is published.

**Finding 2, sector ranges (2 sampled values; 43,206 cells in the sweep, 14,402 per CBP series across 3,315 geographies).** The API publishes the two-digit level of NAICS 31-33, 44-45 and 48-49 only as those ranges. The reader dropped the range codes, and the withheld-cell bound of D45 looked for the strings `31`, `44` and `48`, which never appear. A class code with no 3-, 4- or 5-digit parent at a geography therefore got no bound. Fixed: the reader keeps the three ranges, and the sector parent of a code in them is its range. Lower bounds do not change; some `up_to` amounts grow, and some classes that read as zero are now lower bounds of zero.

**Note, no mismatch:** in `cbp_emp` and `cbp_estab_per_10k` the `up_to` of a `[value, up_to]` cell counts establishments that may be withheld, not employees or a rate. Kept that way, because the renderer prints only the lower bound. The flag text now says so, and each CBP series carries `up_to_unit: establishments`.

**After the fixes:** the checker's script, unchanged (`gates/rederive_census.py`, sha256 `f764764ba797e90bde678bd200c498849d5d12026b0a1806664f41fc75c8f33d`), was run once on the rebuilt register. It finds 767 of 767 sampled values equal (the 30 Puerto Rico values are now nulls, so they are not drawn), and 0 problems in 698,030 values. Gate 6 reads that run. Following the owner's "one round, then fix and stop", no further round was sent.

**Also corrected before landing (my reading, not a checker finding).** No composition changed. A diff of `geographies.json` shows only these fields moved: `basis` on 91 rows, `cbsa.verified` on 115, and `fips_verified` on 896 composer county entries.
- 91 rows had kept the composer's basis "counties unverified pending the delineation file". They now say their membership comes from the Census Data API geoinfo roster.
- Each recalled CBSA code and county entry carries `verified` / `fips_verified` measured against the 2025 roster.
- The seven F2 rows no longer say only the OMB delineation file can confirm them. They name the roster check that writes their difference in `resolved.notes`.
- The owner's review table in CLOSE-TABLES.md lists the counties the register uses, not the composer's list.
- Gate 3's message no longer names permits.
