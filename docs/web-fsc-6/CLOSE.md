# WEB-FSC-6 close

Lane: the page factory and the first two clusters (Texas and gas stations) on feasibility-study-company.com. Branch `web-fsc-6`, worktree `~/Downloads/wt-web-fsc-6`.

## Heads

- Cut from: `1d48cc2` (local `main` = `origin/main` at step zero, STEP-ZERO.md).
- Generator ready: `f8d22c4` (CHECKPOINT.md; the Texas page and the Lockhart case passed gates 1 to 6 and the look gate).
- Integrated with `main` twice: `53ad912` (WEB-FSC-4 landed; ruling 14 chain run with the hold list emptied) and `5f9311f` (WEB-FSC-5 landed during the land step; merged again, chain and all gates rerun, D39).
- Freezes: 1 `2f1e5b9`, 2 `9459513`, 3 `034c3bb`, 4 `4982fd8`, 5 (landing) `8e3a387` = content `b1491ae` plus the gate record.
- Landed: `git push . HEAD:main` fast-forwarded local `main` `5f9311f..8e3a387`. The records-only commit holding this file follows on `main`.
- Deployed tree: `git archive main` at `8e3a387` without docs/, src/ and data/markets/ (D40); archive sha256 `ce400d5687811316bc8cf7bcd81d8b83790b87ffd3eef533a0f918623b6586b0`.

## The factory

- `src/pages/**.html`: one source per page, JSON front matter (type, url, title, description, h1, breadcrumb, published, updated, sources, faq, stats) and a body of `<section id data-h2 data-eyebrow>` blocks with `[^n]` citations. `src/README.md` is the format spec.
- `src/templates/` (base, state, metro, hub, subtype, case) and `src/templates/partials/` (house CSS byte-identical to the merged pages, case components, factory CSS, interim chrome that chrome.py replaces).
- `scripts/build.py`: renders every source to its served `index.html`, keeps every script-owned region (chrome, mesh, fsc, sba, mkt, case), writes links to folded sections as pending links (D30), and refuses a page with a dash in any encoding, a banned name, a second title or h1, a duplicate id, broken JSON-LD, an unknown `sba:` path or unexpanded shorthand. `--check` compares every page with a fresh render.
- `scripts/casemodel.py` with `data/cases/<slug>.json`: the case engine (SBA 7(a), SBA 504, USDA B&I, HUD 232). Inputs each carry a source on the page or a labelled assumption; it solves the restructure, renders every table and inline value into `case:` regions, refuses a glance or card that contradicts the computed tests, fills the `/case-studies/` cards from `src/case-cards.json`, and computes the Arizona RV and boat storage IRR from `data/returns/` (D27). `--check` fails on any stale region.
- To add a page: write `src/pages/<url>.html` in the format above, run `python3 scripts/build.py --page <url>`, then the ruling 14 chain (chrome.py, byline.py, regulatory.py, markets.py, casemodel.py, mesh.py, links.py --relink, sitemap.py) and `docs/web-fsc-6/tools/pagecheck.py <url>`.
- To add a case: write `data/cases/<slug>.json` (program, inputs with source or assumption, uses, revenue, cost of sales, opex, glance, breakeven and sensitivity specs) and `src/pages/case-studies/<slug>.html` with `{case:...}` regions, add a card template to `src/case-cards.json`, then build.py --page, `casemodel.py --only <slug>`, the chain, and pagecheck.

## The 31 pages

Body words exclude tables, sources, FAQ, breadcrumb and generated mesh lists. Unique figures are dated, cited figures that appear on no other served page by value (rounded and rescaled repeats count as the same figure, D29, D38). Overlap is 8-word shingles over the smaller page; the tool counts WEB-FSC-4's generated mesh lists inside `<main>`, so the written-text figure is given beside it (D36). Totals: 23 pages built, 118,584 body words, minimum 29 unique figures (interstate-highway), maximum overlap 7.04% (3.68% on written text). The fourth column of the last field counts the research gaps a reference page states as gaps, and each case's lender conditions (where NOT FOUND items became conditions).

| Page | Type | Body words | Unique figures | Max overlap (tool) | with | Written text only | Research gaps or lender conditions |
|---|---|---|---|---|---|---|---|
| /states/texas/ | state | 10,820 | 71 | 2.45% | /case-studies/multifamily-texas-agency/ | 0.74% | 18 stated gaps |
| /states/texas/houston/ | metro | 3,160 | 35 | 0.07% | /states/texas/san-antonio/ | 0.07% | 6 stated gaps |
| /states/texas/dallas-fort-worth/ | metro | 3,279 | 34 | 0.26% | /asset-classes/gas-station-and-c-store/ev-charging/ | 0.26% | 3 stated gaps |
| /states/texas/austin/ | metro | 2,932 | 37 | 0.05% | /states/texas/houston/ | 0.05% | 0 stated gaps |
| /states/texas/san-antonio/ | metro | 2,946 | 31 | 0.07% | /states/texas/houston/ | 0.07% | 2 stated gaps |
| /asset-classes/gas-station-and-c-store/ | hub | 9,730 | 81 | 5.27% | /practice-areas/sba-7a-504/ | 2.87% | 3 stated gaps |
| /asset-classes/gas-station-and-c-store/interstate-highway/ | subtype | 2,907 | 29 | 0.32% | /asset-classes/gas-station-and-c-store/ev-charging/ | 0.32% | 0 stated gaps |
| /asset-classes/gas-station-and-c-store/ev-charging/ | subtype | 2,545 | 31 | 0.32% | /asset-classes/gas-station-and-c-store/interstate-highway/ | 0.32% | 0 stated gaps |
| /case-studies/gas-station-texas-sba/ | case | 5,733 | 38 | 5.25% | /case-studies/gas-station-versailles-ohio-sba/ | 2.94% | 12 lender conditions |
| /case-studies/gas-station-florida-sba/ | case | 4,896 | 44 | 5.22% | /case-studies/hotel-florida-sba/ | 2.68% | 11 lender conditions |
| /case-studies/gas-station-alabama-sba/ | case | 5,732 | 35 | 5.64% | /practice-areas/sba-7a-504/ | 2.13% | 22 lender conditions |
| /case-studies/gas-station-georgia-sba/ | case | 5,515 | 45 | 4.71% | /case-studies/gas-station-texas-sba/ | 2.55% | 21 lender conditions |
| /case-studies/gas-station-versailles-ohio-sba/ | case | 5,077 | 34 | 5.25% | /case-studies/gas-station-texas-sba/ | 2.94% | 10 lender conditions |
| /case-studies/truck-stop-texas-sba/ | case | 5,354 | 37 | 4.22% | /case-studies/truck-stop-oklahoma-sba/ | 2.42% | 22 lender conditions |
| /case-studies/hotel-texas-sba/ | case | 5,912 | 40 | 7.04% | /case-studies/lodging-retreat-johnson-city-texas-sba/ | 3.67% | 12 lender conditions |
| /case-studies/rv-park-texas-usda/ | case | 5,415 | 30 | 5.69% | /case-studies/rv-park-ossipee-new-hampshire-usda/ | 2.52% | 12 lender conditions |
| /case-studies/car-wash-texas-sba/ | case | 5,263 | 52 | 5.13% | /case-studies/rv-boat-storage-texas-sba/ | 3.68% | 12 lender conditions |
| /case-studies/rv-boat-storage-texas-sba/ | case | 4,837 | 36 | 5.13% | /case-studies/car-wash-texas-sba/ | 3.68% | 11 lender conditions |
| /case-studies/auto-dealership-texas-sba/ | case | 5,777 | 43 | 4.15% | /case-studies/car-wash-texas-sba/ | 2.5% | 18 lender conditions |
| /case-studies/assisted-living-texas-hud/ | case | 5,284 | 49 | 4.28% | /case-studies/assisted-living-hawaii-hud/ | 1.57% | 19 lender conditions |
| /case-studies/meat-processing-texas-usda/ | case | 5,165 | 30 | 4.18% | /case-studies/rv-park-texas-usda/ | 2.57% | 20 lender conditions |
| /case-studies/travel-center-hankamer-texas-usda/ | case | 5,269 | 32 | 4.17% | /case-studies/meat-processing-texas-usda/ | 2.57% | 13 lender conditions |
| /case-studies/lodging-retreat-johnson-city-texas-sba/ | case | 5,036 | 42 | 7.04% | /case-studies/hotel-texas-sba/ | 3.67% | 13 lender conditions |
| /states/texas/mcallen/ | folded | section /states/texas/#mcallen | counted with the parent | | | | pending link to the slug (D30) |
| /states/texas/el-paso/ | folded | section /states/texas/#el-paso | counted with the parent | | | | pending link to the slug (D30) |
| /states/texas/lubbock/ | folded | section /states/texas/#lubbock | counted with the parent | | | | pending link to the slug (D30) |
| /states/texas/corpus-christi/ | folded | section /states/texas/#corpus-christi | counted with the parent | | | | pending link to the slug (D30) |
| /asset-classes/gas-station-and-c-store/branded-fuel/ | folded | section /asset-classes/gas-station-and-c-store/#branded-fuel | counted with the parent | | | | pending link to the slug (D30) |
| /asset-classes/gas-station-and-c-store/unbranded-independent/ | folded | section /asset-classes/gas-station-and-c-store/#unbranded-independent | counted with the parent | | | | pending link to the slug (D30) |
| /asset-classes/gas-station-and-c-store/convenience-no-fuel/ | folded | section /asset-classes/gas-station-and-c-store/#convenience-no-fuel | counted with the parent | | | | pending link to the slug (D30) |
| /asset-classes/gas-station-and-c-store/foodservice-qsr/ | folded | section /asset-classes/gas-station-and-c-store/#foodservice-qsr | counted with the parent | | | | pending link to the slug (D30) |

Four metros (McAllen, El Paso, Lubbock, Corpus Christi; D16) and four gas station subtypes (branded fuel, unbranded independent, convenience without fuel, foodservice and QSR; D21) could not reach 25 unique figures of their own and ship as sections of their parents with their own ids; their slugs stay promised as pending links with the section as fallback (D30).

## Cases: as proposed and as restructured

| Case | Program | Project cost | As proposed | As restructured | Test | Result |
|---|---|---|---|---|---|---|
| assisted-living-texas-hud | hud_232 | $31,068,599 | 10.0% equity, 0.71x: fails coverage | 52.8% equity, $14,664,379 of debt, 1.45x | Year 3 against 1.45x | meets every test |
| auto-dealership-texas-sba | sba_504 | $17,134,459 | 10.0% equity, 1.01x: fails equity tier, size limit, coverage | 20.8% equity, $13,570,492 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| car-wash-texas-sba | sba_504 | $5,342,093 | 15.0% equity, 1.27x: fails equity tier | 20.0% equity, $4,273,675 of debt, 1.34x | Year 2 against 1.15x | meets every test |
| gas-station-alabama-sba | sba_7a | $1,253,024 | 10.0% equity, 1.18x: fails coverage | 14.8% equity, $1,067,576 of debt, 1.25x | seller last year (Appendix 15) against 1.25x | meets every test |
| gas-station-florida-sba | sba_7a | $4,062,749 | 10.0% equity, 0.29x: fails coverage | 76.7% equity, $946,620 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| gas-station-georgia-sba | sba_7a | $4,867,551 | 10.0% equity, 0.60x: fails coverage | 52.3% equity, $2,321,822 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| gas-station-texas-sba | sba_7a | $5,638,517 | 15.0% equity, 0.62x: fails coverage | 53.2% equity, $2,638,826 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| gas-station-versailles-ohio-sba | sba_7a | $3,017,672 | 10.0% equity, 0.62x: fails coverage | 50.9% equity, $1,481,677 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| hotel-texas-sba | sba_504 | $13,887,569 | 15.0% equity, 0.82x: fails equity tier, coverage | 39.1% equity, $8,457,529 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| lodging-retreat-johnson-city-texas-sba | sba_7a | $5,010,422 | 10.0% equity, 0.49x: fails coverage | 60.6% equity, $1,974,106 of debt, 1.15x | Year 2 against 1.15x | meets every test |
| meat-processing-texas-usda | usda_bi | $14,665,957 | 20.0% equity, 1.08x: fails equity tier, coverage | 30.3% equity, $10,222,172 of debt, 1.25x | Year 3 against 1.25x | meets every test |
| rv-boat-storage-texas-sba | sba_504 | $3,125,470 | 10.0% equity, 0.04x: fails equity tier, coverage | 15.0% equity, $2,656,649 of debt, 0.04x | Year 2 against 1.15x | fails; the market does not support this loan |
| rv-park-texas-usda | usda_bi | $3,814,615 | 20.0% equity, 1.11x: fails equity tier, coverage | 28.7% equity, $2,719,820 of debt, 1.25x | Year 3 against 1.25x | meets every test |
| travel-center-hankamer-texas-usda | usda_bi | $7,703,799 | 15.0% equity, 1.04x: fails equity tier, coverage | 28.7% equity, $5,492,808 of debt, 1.25x | Year 3 against 1.25x | meets every test |
| truck-stop-texas-sba | sba_504 | $15,945,118 | 15.0% equity, 0.68x: fails equity tier, size limit, coverage | 20.0% equity, $12,756,094 of debt, 0.72x | Year 2 against 1.15x | fails; the market does not support this loan |

Terrell and Granbury are negative determinations on their own evidence (D20). The Arizona RV and boat storage case (WEB-FSC-4's page, owner ruling) now states a levered IRR of about 28%, computed by casemodel.py from the case's own inputs at the 8.5% exit its page cites (D27); the earlier about 16% cannot be computed from those inputs.

## Research figures dropped or re-sourced

- Folded pages (D16, D21): figures that only a folded metro or subtype carried live in the parent's section.
- Subject listings (D18, D26, D35, D38): every subject listing's ask, per-acre price, acreage, address, ids and broker came off the case pages and their sources; land is a round labelled assumption inside other research land data or, where none exists, a stated planning assumption. Gate 8 checks 170 identifiers and 140 per-case values kept outside the repository.
- Figures a fetch added that the research never held were struck (D19), including Terrell's 6.95% debenture rate (now the October 8, 2026 effective 6.97%, D23).
- Re-sourced: SOP 50 10 8 and 7.1 rules to SOP 50 10 8.1 (D22); the dealership's February 2026 coupon to the October 2026 effective rate (D23); Boerne's 0.25% premium to HUD's 0.77% Section 232 rate table (D24); Bastrop County's tax rate to FY2026-27 on three pages (D31); the B&I equity rule to 7 CFR 5001.105(d) at 25% (D31); Florida's PMPA rule from an S3 copy to the SOP 50 10 8.1 entry (D32).
- Dropped: Yelp search-result sources (dealership), a redirected Austin source and its claim, a mixed-vintage Bastrop County growth figure, the Lockhart 7-Eleven offer that only the subject listing source supported, the Elgin park sources (D32, D35).

## NOT FOUND items as lender conditions

Counted per page in the table above (lender conditions on cases, stated gaps on reference pages). The largest: Terrell and Opelika (22 conditions each), Cartersville (21), the meat plant (20), Boerne (19); the Texas page states 18 research gaps.

## WEB-FSC-5 register

Not used for page figures. WEB-FSC-5 landed during the land step (D39); the chain ran markets.py (no page carries `mkt:` markers yet) and gate 11 includes `markets.py --check`. Pages left for a ruling 11 marker pass: `/states/texas/` (with its four folded metro sections), `/states/texas/houston/`, `/states/texas/dallas-fort-worth/`, `/states/texas/austin/`, `/states/texas/san-antonio/`, for Census population, ACS, CBP, BEA and SBA 7(a) and 504 FOIA series. Two facts for that pass: the register's population estimates are Vintage 2023 while the pages cite Vintage 2025, and figures rendered through `mkt:` markers do not count toward gate 3. The register is build input and is not deployed (D40).

## Gates

Command: `FSC6_DNU=<identifier list outside the repo> python3 docs/web-fsc-6/tools/gates.py --out docs/web-fsc-6/GATES.txt`, run at `b1491ae` on a clean worktree. GATES.txt holds each gate's checks and output.

| Gate | Result | What it checks |
|---|---|---|
| 1 | GREEN | 31 pages accounted for: 14 at existing URLs, 17 new, of which gate 5 folds some into the Texas page; one <title>; JSON-LD with BreadcrumbList and author @id |
| 2 | GREEN | factory: build.py --check and casemodel.py --check exit 0; mutation tests |
| 3 | GREEN | unique figures: at least 25 dated, sourced figures per page that appear on no other page |
| 4 | GREEN | overlap under 15% against every sibling and every other page (8-word shingles) |
| 5 | GREEN | standalone metros (gates 3 and 4 on own-geography data); failures fold into the Texas page |
| 6 | GREEN | case standard v3 components, body length, SBA tiers, floors and caps; Opelika under Appendix 15 |
| 7 | GREEN | sources: four parts; ruling 10 pattern absent from served files and lane commit authors; stale-claim grep zero |
| 8 | GREEN | subjects: no street number, parcel id, owner or business name for any case subject |
| 9 | GREEN | links: links.py and mesh.py --check; 3+ inbound contextual links; required edges |
| 10 | GREEN | clean text: zero em and en dashes in any encoding; no credential beside the name |
| 11 | GREEN | markers: byline, regulatory, chrome and markets --check |
| 12 | GREEN | dates agree (JSON-LD dateModified, visible line, sitemap lastmod = 2026-10-16) |
| 13 | GREEN | look: 1440 and 390 screenshots; no page-level horizontal scroll at 390; wide tables scroll in their box |
| 14 | GREEN | index all: index, follow and in the sitemap with lastmod |

## Attack and verification

Every finding was reproduced before it was fixed; nothing was resolved by counting agreement.

| Round | Freeze | Reviewer | Blocker | Major | Minor | Resolution |
|---|---|---|---|---|---|---|
| 1 | 1 | attacker one (numbers) | 1 | 5 | 10 | fixed (D23 to D25, D31); engine refuses glance contradictions |
| 1 | 1 | attacker two (sameness, sourcing) | 4 | 11 | 12 | fixed (D26 to D34); tightened figure, identifier and dash gates |
| 1 | 1 | verifier | 2 | 0 | 1 | fixed (encoded dash URL, subject URL, undated sources) |
| 2 | 2 | attacker three (case subjects) | 2 | 2 | 10 | fixed (D35); gate 8 list covers all fifteen cases |
| 2 | 2 | verifier | 1 | 2 | 0 | fixed (D37): served-file dashes, SBA mandate wording on older pages |
| 3 | 3 | attacker three | 0 | 0 | 4 | two generalized, two accepted (D35, D38) |
| 3 | 3 | verifier | 0 | 1 | 2 | fixed and reproduced on freeze 4 (D38); .gitignore dash not served |

Open at close: 0 blockers, 0 majors. Accepted minors: Cartersville keeps a generic unsewered-lot budget; the Bastrop hotel's land rests on its one corridor comparable; Lockhart's land total sits 6% under the old listing's ask with a different acreage; figures a writer derived from cited figures still count in gate 3 (honest minimum about 26 by the verifier's hand count).

## Deploy

- Drafts: `6ad2064ab5927d22435b3caa` (freeze 1), `6ad220c5dcfd658f6f037e0a` (freeze 2), `6ad236858d41a3fff00d9698` (freeze 3), `6ad23bb096ae000c504b30ab` (main `8e3a387`, checked before production).
- Production: `6ad23bed0dd08e20da34458c`, from the same tree, published 2026-10-16 15:00 UTC, then locked (auto publishing stopped, as the coordinator asked; the site stays locked).
- Rollback: `6ad211a47a07ab112446c83f` (commit `53ad912`), the deploy published before this one.
- Production checks (read-only GETs): all 23 pages and nine other changed pages HTTP 200, byte-identical to `main`, expected H1; the eight folded sections present in their parents and their slugs 404; `/src/`, `/docs/web-fsc-6/CLOSE.md`, `/Docs/...`, `/DOCS/...` and `/data/markets/...` 404; five formerly pending links resolve (Houston, Dallas-Fort Worth and Austin in the site menus; the Versailles and Hankamer cards on `/case-studies/`); sitemap lastmod 2026-10-16 on the changed pages; `/api/contact` answers (the function shipped).
- IndexNow: `scripts/indexnow.py --since 53ad912`, one POST, 168 URLs (every page changed since the live commit plus the sitemap): HTTP 200 OK.

## Push and bundle

- Origin: `infommcginvest/Feasibility-study-company.com`. GitHub's `main` is `53ad912`; `web-fsc-6` is not on GitHub.
- `git push origin main web-fsc-6` with prompts disabled failed for credentials: git on this Mac has no stored GitHub credential (the keychain helper returns none, so git stops at the username). No credential was looked for. The account infommcginvest owns the repository, so adding it as a collaborator is not the fix; git needs a sign-in.
- Bundle: `{repo}/_bundles/web-fsc-6-8e3a387.bundle` (refs `main` and `web-fsc-6` at `8e3a387`, 243,984,464 bytes, sha256 `727320748fa621fc9a165d73eedf01862701365f2ea6f697e9af96524ecd1f29`); `git bundle verify` passes, and a clone of it checks out `8e3a387` whose `git archive` matches the deployed archive's sha256. `_bundles/` is not ignored by .gitignore: never stage it.
- `main` is live but not on GitHub, so nothing may push an older `main` to GitHub before this one.

## Owner items

- Resubmit `/sitemap.xml` in Search Console.
- Push: sign git in on this Mac for github.com as infommcginvest (for example a fine-grained token at https://github.com/settings/personal-access-tokens/new with Repository access: Only select repositories, Feasibility-study-company.com; Repository permissions: Contents, Read and write; then run `git -C ~/Downloads/wt-web-fsc-6 push origin main` once in Terminal and enter the username and the token, which the macOS keychain keeps). Then type "added": main and web-fsc-6 are pushed fast-forward only with prompts disabled.
- Auto publishing is locked on deploy `6ad23bed0dd08e20da34458c`; a GitHub build will not replace the live site until the owner unlocks it.
- netlify.toml (WEB-FSC-4's) removes docs and src on git builds but not data/markets; add it before any git build is published (D40).
- The ruling 11 marker pass on the Texas page and the four metros (see WEB-FSC-5 register above).
- `.gitignore` line 16 (WEB-FSC-5's) holds a literal em dash; it is not served (HTTP 404).
- `/scripts/` and the case inputs under `/data/` are served from the publish root as before this lane; they carry no dashes, no banned names and no subject identifiers.
