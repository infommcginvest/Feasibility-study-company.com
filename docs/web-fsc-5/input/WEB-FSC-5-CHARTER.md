# CHARTER WEB-FSC-5: WAVE 1 ON FEASIBILITY-STUDY-COMPANY.COM. THE MARKETS DATA PIPELINE: ONE REGISTER OF FEDERAL SERIES FOR EVERY STATE, COUNTY, CBSA AND SITE MARKET, MAPPED TO ASSET CLASSES, WITH A RENDER SCRIPT

Issued 15 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. It runs at the same time as WEB-FSC-4 and WEB-FSC-6. No deploy: this lane changes no served page. Land the moment gates are green: WEB-FSC-6 renders its Texas figures from this register if it is on `main` by then.

| | |
|---|---|
| Session | WEB-FSC-5. Main session on Opus. Fetch, mapping and composition subagents on Sonnet. The two attackers on Opus. Verifier on Sonnet. |
| Repo | `~/Downloads/Feaisbility-Study-Company.com` (spelled as on disk). Remote `origin` is the GitHub repository `Feasibility-study-company.com`. Static HTML, no build step; Netlify publishes the repo root. |
| Worktree | `~/Downloads/wt-web-fsc-5`, branch `web-fsc-5`, cut from local `main`. Never work in the main repo directory. Lanes WEB-FSC-4 and WEB-FSC-6 run at the same time in `~/Downloads/wt-web-fsc-4` and `~/Downloads/wt-web-fsc-6`. |
| Head at issue | `main` = `origin/main` = `1d48cc2`. Expect it may have moved; step zero says what to do. |
| Files this lane may change | `data/markets/**`, `scripts/markets*.py`, `.gitignore` (add `/_cache/` and `/_bundles/`), `docs/web-fsc-5/**`. Nothing else. WEB-FSC-4 owns most served pages, `netlify.toml`, `sitemap.xml` and the other scripts; WEB-FSC-6 owns `src/`, `scripts/build.py`, `scripts/casemodel.py`, `data/cases/` and the Texas and gas station pages. The three branches cannot conflict. |
| Raw downloads | `<worktree>/_cache/markets/`, gitignored, never committed. Python dependencies go in a virtualenv under `_cache/`, never system-wide. |
| Records | `docs/web-fsc-5/` (committed; production already returns 404 for `/docs/*`) |
| First action | After step zero, save this charter verbatim to `docs/web-fsc-5/input/WEB-FSC-5-CHARTER.md` and commit it. |

## Why this lane exists

Waves 2 to 4 add about 600 pages: 253 metro pages, rebuilt state pages and 191 subtype pages. Their figures must not come from deep searches, because each research run returns different years and definitions, and that is how a 750-page site becomes internally inconsistent. This lane pulls the federal series once, for every geography, on one definition per series, and renders them into pages the way `scripts/regulatory.py` renders `data/regulatory/sba.json`. Prose does not refresh; this register does, on a schedule.

## The hard constraint

Every value in the register is a published federal value, or arithmetic on published federal values done by a script whose method is recorded, and it is retrievable from a recorded URL for a recorded vintage and period. Nothing is typed by hand, estimated, imputed, interpolated, or carried over from any other property of the owner: not the sister firm's analytics platform, not its repos, not the SBA files already on this Mac outside this repo. Fetch fresh from the federal host. A value the source suppresses or does not publish is null with a flag, never zero. No served page changes in this lane.

## Standing scaffolding

Step zero, four probes, before any write:

1. **Repo and head.** `git -C <repo> fetch origin`, then read `main` and `origin/main`. If `origin/main` is ahead of local `main`, stop and report: someone pushed outside this process. If local `main` has moved past `1d48cc2`, cut from it and record the head you cut from.
2. **Twin guard, both arms.** Process arm: list running Claude Code CLI processes whose working directory is inside the repo or any of its worktrees (`lsof -a -d cwd -p <pid>`), excluding this session's own process and excluding the Claude desktop app's Electron helpers (anything running from `/Applications/Claude.app/`). Git arm: `git worktree list --porcelain`, any `index.lock` in the repo's git dir or a worktree git dir, and whether branch `web-fsc-5` or path `~/Downloads/wt-web-fsc-5` already exists. A live session holding this lane's branch or worktree is a stop. WEB-FSC-4 and WEB-FSC-6 in their own worktrees are expected and are not a stop. The zero-byte `stale-index-lock` and `stale-maintenance-lock` files in the git dir are ignored by git; leave them.
3. **Hosts.** GET each source host with a timeout and record the result: `api.census.gov`, `www2.census.gov`, `data.bls.gov`, `apps.bea.gov`, `[www.huduser.gov](https://www.huduser.gov)`, `data.sba.gov`. A host that refuses is recorded; carry on with the others and close with that series NOT FETCHED and the reason. Never work around robots.txt, a 403 or a bot check. BLS asks automated clients to identify themselves in the User-Agent with a product name and a contact address; do that with an address on feasibility-study-company.com, and if BLS still refuses, record it.
4. **Environment.** Free disk of at least 15 GB (70 GB free at issue; raw files can reach several GB). No Census API key is required; if `CENSUS_API_KEY` is set in the environment, use it and never write it anywhere.

No database is involved, so the database scaffolding (lock_timeout, the one-named-file applier, migration numbers from the live ledger) does not apply. Its equivalent here: every fetch and every subprocess carries a timeout, downloads resume rather than restart, and nothing waits unbounded.

Speed rules:

1. Do not ask the owner questions. Decide, log in `docs/web-fsc-5/DECISIONS.md`, continue.
2. Never end your turn while a subagent, a download, a build or a gate is running.
3. Stop only for a step zero stop, a red gate you cannot fix in scope, or free disk under 8 GB.
4. Stage explicit paths only. No `git add -A`. Never open, read or print `.ghtoken` in the repo root. No credential or key in the repo, a log or a commit.
5. Commit as `git -c user.name="Feasibility Study Company" -c user.email="noreply@feasibility-study-company.com" commit ...`. The repo's configured identity carries the sister firm's domain, and this repo is public.
6. Network: read-only GETs to the hosts in probe 3. Fetch every series for all geographies at once, by bulk file wherever the agency publishes one.

## Measured facts (from the repo at `1d48cc2` on 15 October)

- **Render precedent.** `scripts/regulatory.py` (112 lines) fills `<!--sba:dotted.path {"fmt": ...}-->value<!--/sba:dotted.path-->` regions from `data/regulatory/sba.json`, where each value carries a `register` id. `--check` exits 1 when a page is out of date. It skips `docs/`, `netlify/`, `preview-*.html` and `index_N.html`. Copy this pattern under the `mkt:` namespace.
- **The site's markets are not CBSAs.** The metro research for every state marks Census building permits, storage supply and SBA loan counts as NOT FOUND in nearly every market, so permits, CBP supply per capita and FOIA loans by market are the series the next lanes need most; do not let them slip to NOT FETCHED without a recorded refusal. The pages already promise 253 market slugs under `/states/<state>/<market>/` in 33 states: 8 per state for most, Hawaii 6, Missouri and Wisconsin 7, and Ohio 1 (`columbus`, with no Ohio state page yet). Extract the full list from the anchors at your cut point. Their kinds, read from the slugs:
  - CBSA-like metros: houston, phoenix, atlanta, inland-empire, berkshires, the-villages.
  - Cities inside a larger CBSA: scottsdale, carmel, edmond, norman, cambridge, bellevue, hillsboro.
  - Single counties: pinal-county, fairfield-county, bergen-county, middlesex-county, morris-county, york-county, desoto-county, mississippi-county, prince-georges-county, montgomery-county.
  - Multi-county regions with no federal definition: black-belt, quiet-corner, lakes-and-mountains, upper-peninsula, eastern-shore, iron-range, delta, golden-triangle, midcoast, north-country, central-valley, columbia-basin, eastern-oregon, oregon-coast, uinta-basin, i-95-corridor, southern-maryland, western-maryland, litchfield-hills.
  - Towns inside a larger county: kapolei, lahaina, bar-harbor, park-city, moab.
  - Cross-state: quad-cities appears under both illinois and iowa; metro-east is the Illinois side of St. Louis; council-bluffs sits in the Omaha CBSA; permian-basin is listed under new-mexico while most of the basin lies in Texas.
  - Arizona has one called `rural`.
- **Texas, the wave 2 pilot:** austin, corpus-christi, dallas-fort-worth, el-paso, houston, lubbock, mcallen, san-antonio. Each maps to a single CBSA; the page calls mcallen "McAllen / Rio Grande Valley", which is the McAllen-Edinburg-Mission metro.
- **Asset classes.** The 28 hubs in `asset-classes/`, plus 15 hub paths the site links but has not built: limited-service-hotel, select-service-hotel, extended-stay-hotel, boutique-and-resort, industrial-and-warehouse, cold-storage, event-and-wedding-venue, skilled-nursing, build-to-rent, mixed-use, brewery-and-distillery, independent-living-and-ccrc, active-adult, board-and-care, ccrc-life-plan-communities. That makes 43 classes. The 191 subtype pages get no NAICS row of their own; they inherit their class.
- `data/regulatory/sba.json` is served publicly at its path, and `data/markets/` will be too. That is acceptable: it is federal data.

## Traps already known (each makes the numbers wrong while every script exits 0)

1. **Medians do not aggregate.** A multi-county region's median household income is not the average, or the population-weighted average, of its counties' medians. Report component values or use a source that publishes the region; never synthesize a median.
2. **Rates aggregate from numerators and denominators**, never by averaging rates.
3. **Suppressed is not zero.** QCEW disclosure suppression and ACS cells with no estimate are null with a flag. A suppressed value read as zero turns a market with ten employers into a market with none.
4. **CBP statewide records** (county code 999) belong to the state, not to any county. County sums will not equal the state total; reconcile by naming the difference, not by forcing equality.
5. **NAICS vintages.** CBP and QCEW use NAICS 2022 for recent years, while SBA FOIA loans carry the code of their approval era. Gas stations moved from 447110 and 447190 to 457110 and 457120 in 2022, and other retail codes merged too. Map every vintage present in each file, or one source loses an asset class without an error.
6. **Connecticut.** From 2022, Census data uses nine planning regions as county equivalents in place of eight counties, and some series still publish the old counties. Never join across the two. Record which each series uses and how each Connecticut market is composed in each.
7. **ZIP is not ZCTA.** PO box and business-only ZIPs have no ZCTA. The FOIA files also carry project county and state fields; confirm the field names from the headers rather than from this charter. Report the geocoding match rate by state and by method. An unmatched loan is reported unmatched, never dropped silently.
8. **FOIA status vocabularies** differ between the 7(a) and 504 files, and SBA split the charged-off status into more than one code in a 2026 release. An earlier analysis of these files elsewhere returned zero charge-offs and silently excluded 136,181 cancelled loans because of exactly this. Enumerate every distinct status value in each file, classify each in a table you commit, and fail the build on any unclassified value. Cancelled loans never disbursed and stay out of denominators.
9. **Vintages.** Within one series every geography carries the same vintage and period. Pair counts with the population of the same year (Census population estimates for totals, ACS for characteristics).

## Already ruled

1. **County is the atomic unit** (FIPS, with Connecticut as in trap 6). States, CBSAs (the current OMB delineation file, from Census) and site markets are compositions of counties. Sub-county markets use Census places or tract sets and carry only the series published at that grain.
2. **Site markets live in `data/markets/geographies.json`**: slug, state, kind (cbsa, county, county-set, place, tract-set, cross-state), component FIPS or place GEOIDs, the basis for the composition (the CBSA code; or the counties the state page names; or the region as commonly bounded, with a one-line reason), and a `review` flag on any composition that rests on judgement. Every one of the 253 slugs gets a row, Ohio's columbus included, and the file takes new markets as later waves add them.
3. **Series**, each at the latest vintage published at run time, for every county, CBSA, state and site market where the source publishes it:
   - Census population estimates: total population, and change over 1 and 5 years.
   - ACS 5-year (plus ACS 1-year where published for the geography, labelled as such): households, median household income, per capita income, population 65 and over, owner and renter occupied units, median gross rent, median home value, labor force and unemployment.
   - Census Building Permits Survey: units authorized by structure type, latest year and 5-year total.
   - County Business Patterns: establishments (and employment where published) for each asset class's NAICS codes, plus establishments per 10,000 residents against the same-year population.
   - QCEW: annual average employment and average weekly wage, total covered and by asset-class NAICS where disclosed.
   - BEA: personal income and per capita personal income.
   - HUD Fair Market Rents for the current fiscal year by bedroom count, at the HUD FMR area, mapped to counties.
   - SBA 7(a) and 504 FOIA: loan counts, gross approval volume, charge-off counts and gross charge-off amounts, by geography, asset class (through NAICS) and approval fiscal year. A charge-off rate appears only for cohorts you define as seasoned, with the definition recorded in `sources.json`.
4. **Every series has a row in `data/markets/sources.json`**: id, publisher, exact table or file title, URL, vintage, period, retrieval date, the sha256 of the raw file, cadence and expected next release. So a rendered figure can always print the four-part citation the site uses: value, period, publisher and title, URL.
5. **`data/markets/naics-map.json`** maps each of the 43 classes to its NAICS 2022 codes and its legacy codes by vintage, with a fit grade (exact, partial, proxy, none) and a one-line reason. Proxy and none are never rendered as if exact. Expect glamping, RV and boat storage, coffee shop, urgent care, behavioral health, event venue and build-to-rent to come out partial or proxy.
6. **The render script `scripts/markets.py` follows `regulatory.py`:** `<!--mkt:<geo>.<series>[.<class>] {"fmt": ...}-->value<!--/mkt:...-->`, plus a renderer for the matching source line, with `--check`. It is proven on a fixture page under `docs/web-fsc-5/fixture/` (not served). This lane writes no marker into a served page; the Texas pilot (WEB-FSC-6) is the first consumer.
7. **`scripts/markets.py audit`** writes `data/markets/audit.csv`: for each site market, the count of non-null values specific to its own geography (not inherited from its state), the suppressed count, and `standalone` = yes when at least 25 such values exist. This is publication gate 3 for waves 2 to 4: a market below it folds into its state page.
8. **Refresh.** `python3 scripts/markets_fetch.py --refresh` re-pulls every series whose expected next release has passed, rebuilds, and prints which values changed. Putting it on a schedule is the owner's later call.
9. **Size.** Committed `data/markets/` stays under 60 MB with no single file over 25 MB. Raw files never enter git.

## Delegated (decide, log, keep going)

- Exact ACS tables and variables, file formats, and API versus bulk file per source. Prefer the bulk files Census, BLS and BEA publish; the keyless Census API has a daily limit.
- The composition of each judgement-based region, with its reason and `review` flag.
- The charge-off cohort definition and seasoning window.
- The folder layout under `data/markets/`.

The shape, unless you find a better one:

- `scripts/markets_fetch.py`: raw files into `_cache/markets/raw/<source>/<vintage>/`, and a manifest with URL, timestamp and sha256 per file.
- `scripts/markets_build.py`: raw files to `data/markets/series/<series-id>.json` (values keyed by geography id, each with value, margin of error where published, and flag), then per-market bundles under `data/markets/geo/`.
- `scripts/markets.py`: render, `--check` and `audit`.
- `data/markets/`: `sources.json`, `geographies.json`, `naics-map.json`, `foia-status-map.json`, `series/`, `geo/`, `audit.csv`.

## How the proof could be faked (the gates are written against these)

- Spot-checking values against the register the pipeline itself wrote. That is circular. Verification re-derives values from the raw file or the agency's own published table through code that does not import the pipeline.
- A render test on a fixture whose values already equal what the page shows. The render gate mutates a register value, confirms the fixture changes and `--check` fails, then reverts.
- A run that quietly skipped a source that refused. The gate counts series by status (FETCHED, or NOT FETCHED with its reason), and every NOT FETCHED appears in CLOSE.
- Composing a region from whatever counties make its numbers look right. Every composition carries its basis, and every `review` row goes to the owner.

## Gates (all green before landing; commands and outputs in `docs/web-fsc-5/GATES.txt`)

1. **No served file changed.** `git diff --name-only main...HEAD` lists only the paths this lane may change.
2. **Coverage.** Every county, CBSA, state and the 253 site markets are in `geographies.json`. Every `sources.json` row has every field. Series counted by status.
3. **Reconciliation.** For additive series, county sums against the source's own state and national totals, with every difference explained (statewide records, suppression, Connecticut). For FOIA, loan counts and volumes by program and fiscal year in the register equal the raw files' totals after the documented exclusions.
4. **FOIA status.** Every distinct status value in each file is classified. Charge-offs are non-zero in every program and fiscal year where the raw file has charge-offs.
5. **NAICS.** Every class has a row with a fit grade. For each class, CBP establishment counts are non-zero nationally, and FOIA loan counts are reported for every NAICS vintage present in the file.
6. **Independent re-derivation.** 40 values sampled at random across series and geography kinds, including at least 5 Connecticut values, 5 multi-county regions, 3 sub-county markets and 3 cross-state markets, re-derived from raw files or agency tables by code that does not import the pipeline. All match.
7. **No synthesized medians, no averaged rates.** A check walks every aggregated value and fails on any median or rate built by averaging.
8. **Render.** The fixture renders Houston and one Connecticut market from markers. The mutation test passes: `markets.py --check` exits 0 on the fixture, 1 after the mutation, and 0 again after the revert.
9. **Texas.** The audit lists Texas and all eight Texas markets with their counts; all eight are standalone, or the reason is stated.
10. **Names and identity.** The case-insensitive pattern `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er` returns nothing in this lane's files or in the author fields of its commits (the brackets stop this charter from matching itself).
11. **Size.** Committed `data/markets/` under 60 MB, no file over 25 MB, nothing under `_cache/` tracked.

## Close

**Freeze before any verification:** commit, then record the HEAD sha, the sha256 of `git archive HEAD`, and the state of the data, not just the files: the raw manifest (every URL, timestamp and sha256) and the sha256 of every file under `data/markets/`. Hand the frozen sha to:

- two attackers on Opus, working separately. Attacker one hunts wrong values with its own sample, weighted toward the nine traps. Attacker two hunts the FOIA and NAICS mapping: dropped loans, misclassified statuses, and any class that lost loans to a vintage change. Each finding comes with the geography, series, expected and found values, and a reproduction.
- one verifier on Sonnet, reading the frozen tree cold, whose default verdict on every CLOSE claim is refuted until it reproduces the claim itself.

Resolve every finding by reproducing it, never by counting how many agents agreed: a tally measures how a finding was argued, not how the world is. Any fix after the freeze means a new freeze and a rerun of the gates the fix touches.

**Land.** Fast-forward local `main` to the frozen head from the worktree with `git push . HEAD:main`. If that is not a fast-forward because WEB-FSC-4 landed first, merge `main` into `web-fsc-5`, rerun gates 1, 10 and 11, refreeze and retry. No deploy: nothing served changed. Then try `git push origin main web-fsc-5`. If it fails for credentials, do not look for any. Write a bundle of `main` to `<repo>/_bundles/web-fsc-5-<sha>.bundle`, clone-test it, and record that in CLOSE.

Write `docs/web-fsc-5/CLOSE.md`: the head you cut from; every series with vintage, period, status and row counts; the market compositions, with the `review` list for the owner; the NAICS map with fit grades; the FOIA status table and match rates; reconciliation results; the Texas audit and the national standalone count; each gate with its command and result; attacker and verifier findings with their resolution; land and push state; and one paragraph for the next lanes on how to put a market figure on a page, how to run the refresh, and which releases come next.

End your turn with exactly this five-line report:

WEB-FSC-5 CLOSE
head <sha> | freeze <sha> | archive sha256 <first 12> | data manifest sha256 <first 12>
series fetched <n>/<n> | markets defined <n>/253 | standalone <n> | review rows <n>
gates <green>/11 | attackers <found>/<fixed> | verifier blocker <n> major <n>
owner: <one line, or none>
