# CHARTER WEB-FSC-6: THE PAGE FACTORY AND THE FIRST TWO CLUSTERS ON FEASIBILITY-STUDY-COMPANY.COM. TEXAS (STATE, EIGHT METROS, ELEVEN CASES) AND GAS STATIONS (HUB, SIX SUBTYPES, FIVE CASES), SHIPPED AND INDEXED

Issued 16 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. It runs at the same time as WEB-FSC-4 and WEB-FSC-5. Deploy pre-authorized: yes. Index all: every page ships indexable.

| | |
|---|---|
| Session | WEB-FSC-6. Main session on Opus: builds the factory and writes the Texas state page. Page-writing subagents on Opus. The final SEO finish (titles, meta descriptions, H1s, first-screen answer, FAQ) of the Texas state page and the eight metro pages on Fable. Research-reading subagents on Sonnet. The two attackers on Opus. Verifier on Sonnet. |
| Repo | `~/Downloads/Feaisbility-Study-Company.com` (spelled as on disk). Remote `origin` is the GitHub repository `Feasibility-study-company.com`. Static HTML, no build step; Netlify publishes the repo root. |
| Worktree | `~/Downloads/wt-web-fsc-6`, branch `web-fsc-6`, cut from local `main`. Never work in the main repo directory. Lanes WEB-FSC-4 and WEB-FSC-5 run at the same time in `~/Downloads/wt-web-fsc-4` and `~/Downloads/wt-web-fsc-5`. |
| Head at issue | `main` = `origin/main` = `1d48cc2`. Expect it may have moved; step zero says what to do. |
| Research input (read only) | `~/Downloads/FSC Deep Searches 2/`. Many files are named "EXTRA <date> - <title>.md"; locate each one by the Research ID on its first line, not by file name. Never copy these files into the repo. |
| Files this lane owns | New `src/` (page sources and templates; WEB-FSC-4 adds the 404 rule that keeps it unserved), `scripts/build.py`, `scripts/casemodel.py`, `data/cases/`, `docs/web-fsc-6/`, and these served pages: everything under `states/texas/`; everything under `asset-classes/gas-station-and-c-store/`; the cases listed in ruling 1. WEB-FSC-4 owns every other page, `netlify.toml`, `sitemap.xml`, `robots.txt` and the shared scripts; WEB-FSC-5 owns `data/markets/`, `scripts/markets*.py` and `.gitignore`. Touch nothing of theirs in this branch. |
| Records | `docs/web-fsc-6/` (committed; production already returns 404 for `/docs/*`) |
| First action | After step zero, save this charter verbatim to `docs/web-fsc-6/input/WEB-FSC-6-CHARTER.md` and commit it. |

## The job in one paragraph

Build the page factory every later lane will use, and prove it on two complete clusters. Texas: the state page rebuilt to at least 6,000 words, eight metro pages, and eleven cases on named towns. Gas stations: the hub rebuilt to 8,000 to 10,000 words, six subtype pages, and five cases on named towns. That is 31 pages: 14 rebuilt at their current URLs and 17 new. The research for all of it is already in the folder. Then ship them, indexed, and switch on every link across the site that has been waiting for these pages.

## The hard constraint

Every figure on these pages traces to a dated source in the research files or in the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. No figure is invented, estimated beyond what its source says, or carried over from any client engagement or from any other property of the owner. A NOT FOUND in the research becomes a lender condition or a stated gap, never a number. Cases are hypothetical, say so in the house disclosure box, and never make a real business the subject. If a page cannot meet the gates on the evidence in hand, it folds into its parent rather than shipping thin.

## Standing scaffolding

Step zero, four probes, before any write:

1. **Repo and head.** `git -C <repo> fetch origin`, then read `main` and `origin/main`. If `origin/main` is ahead of local `main`, stop and report: someone pushed outside this process. If local `main` has moved past `1d48cc2`, cut from it and record the head you cut from.
2. **Twin guard, both arms.** Process arm: list running Claude Code CLI processes whose working directory is inside the repo or any of its worktrees (`lsof -a -d cwd -p <pid>`), excluding this session's own process and excluding the Claude desktop app's Electron helpers (anything running from `/Applications/Claude.app/`). Git arm: `git worktree list --porcelain`, any `index.lock` in the repo's git dir or a worktree git dir, and whether branch `web-fsc-6` or path `~/Downloads/wt-web-fsc-6` already exists. A live session holding this lane's branch or worktree is a stop. WEB-FSC-4 and WEB-FSC-5 in their own worktrees are expected and are not a stop. The zero-byte `stale-index-lock` and `stale-maintenance-lock` files in the git dir are ignored by git; leave them.
3. **Netlify identity.** Confirm site `0a67950d-6092-49c3-8277-017897c1b865` serves `feasibility-study-company.com`; record the current published deploy id as the rollback point.
4. **Environment and inputs.** Free disk of at least 10 GB; python3 with bs4 and lxml (anything else goes in a virtualenv inside the worktree, never system-wide); the Netlify CLI logged in; a headless browser for screenshots; every research file in ruling 1's table found by its Research ID, with its word count logged.

No database is involved, so the database scaffolding (lock_timeout, the one-named-file applier, migration numbers from the live ledger) does not apply. Its equivalent here: every network call and every subprocess carries a timeout, and nothing waits unbounded.

Speed rules:

1. Do not ask the owner questions. Decide, log in `docs/web-fsc-6/DECISIONS.md`, continue.
2. Never end your turn while a subagent, a build, a deploy or a gate is running. Write pages in parallel.
3. Stop only for a step zero stop, a red gate you cannot fix in scope, or free disk under 5 GB.
4. Stage explicit paths only. No `git add -A`. Never open, read or print `.ghtoken` in the repo root. No credential in the repo, a log or a commit.
5. Commit as `git -c user.name="Feasibility Study Company" -c user.email="noreply@feasibility-study-company.com" commit ...`. The repo's configured identity carries the sister firm's domain, and this repo is public.
6. Network: read-only GETs to the production domain and to sources you cite or check (competitor websites, county assessor pages, agency pages); the Netlify CLI for deploys; one IndexNow submission per deploy. Never work around robots.txt, a 403 or a bot check.

## Measured facts (from the repo at `1d48cc2` and the research folder on 16 October)

- **Pages today.** Every page carries the same 24.6 KB inline CSS block and the same header, Markets mega panel and footer. The house skeletons to build templates from: the state page is `states/texas/index.html` (hero, stat band, thesis, monitor, funding, failures, regulatory, metros, assets, FAQ, CTA, sources); the hub is `asset-classes/gas-station-and-c-store/index.html`; the case is `case-studies/cabin-resort-townsend-tennessee-sba/index.html` (batch 1: `capsule disclosure` box under the H1, then At a glance, market conclusion, demand, rental market, competitive supply, revenue build, debt, lender conditions, questions, CTA, sources).
- **Markers.** `fsc:` regions are rendered by `scripts/byline.py` (bylines, reviewed lines, signature, author JSON-LD, style). `sba:` regions are rendered by `scripts/regulatory.py` from `data/regulatory/sba.json`, which holds SOP 50 10 8.1 with its equity tiers, DSCR floors (1.15x standard, 1.25x for Appendix 15 acquisitions on historical EBITDA), the $5,000,000 504 debenture cap, fees and the peg rate, each with a register id. Every SBA rule on a pilot page goes through `sba:` markers.
- **Texas today.** 3,001 body words, 2 tables. The metros H2 says "Seven Texas markets" over eight cards, each card links a metro page that returns 404, and the page links 2 of the state's 10 cases.
- **Gas station hub today.** About 6,200 words in `<main>` and 3 tables. It links 7 subtype pages, all 404. One of them, `truck-stop-travel-center`, would duplicate the existing `/asset-classes/truck-stop-and-travel-center/` hub.
- **Cases today.** The four gas station cases share 56% to 66% of their 8-word shingles with each other, and the H2 skeleton is identical on all four. car-wash-texas-sba (15% equity where 20% applies), rv-boat-storage-texas-sba (10% where 15% applies) and auto-dealership-texas-sba ($5.40M debenture over the $5M cap) break unchanged SBA rules. These rebuilds fix all of that. multifamily-texas-agency has no research file; it stays as it is and remains WEB-FSC-4's page.
- **Research gaps.** MT-TEXAS marks these NOT FOUND for every Texas market: Census building permits for 2025, storage, RV park and senior housing supply, traffic counts, Opportunity Zone, HUBZone and USDA eligibility, and SBA district lender rankings. WEB-FSC-5 supplies permits, CBP supply per capita and FOIA loans by market. The case files carry many NOT FOUND rows (the Lockhart file has 131); each one becomes a lender condition.
- **Research hygiene.** CS-R-RV-PARK-TEXAS-USDA cites the sister firm 12 times. Eight files across the folder cite Wert-Berater. Consulting-firm sources are allowed; Wert-Berater and the owner's other properties are not (ruling 10).
- **Excluded on purpose.** CS-Q-COPPERAS-COVE-TEXAS-STORAGE-YARD is not built: it sits in the same submarket as a live client engagement. Ignore that file.
- **What arrives from the other lanes.** WEB-FSC-4 delivers `scripts/chrome.py`, `scripts/mesh.py`, `scripts/links.py` (with `data-fsc-pending` anchors and `--relink`), `scripts/sitemap.py`, `scripts/indexnow.py` and the `/src/*` 404 rule. WEB-FSC-5 delivers `data/markets/` and `scripts/markets.py` with `mkt:` markers and an `audit` command.

## Already ruled

1. **The 31 pages, and the research each one draws on.**

| Page | URL | Research IDs |
|---|---|---|
| Texas state (rebuild) | `/states/texas/` | ST-TEXAS, MT-TEXAS, PA-USDA, PA-HUD-AGENCY |
| Eight Texas metros (new) | `/states/texas/{houston, dallas-fort-worth, austin, san-antonio, mcallen, el-paso, lubbock, corpus-christi}/` | MT-TEXAS, ST-TEXAS |
| Gas station hub (rebuild) | `/asset-classes/gas-station-and-c-store/` | AH-GAS-STATION-AND-C-STORE-A and -B, SD-GAS-STATION-AND-C-STORE |
| Six gas subtypes (new) | `.../gas-station-and-c-store/{branded-fuel, unbranded-independent, convenience-no-fuel, foodservice-qsr, interstate-highway, ev-charging}/` | SD-GAS-STATION-AND-C-STORE, AH-GAS-STATION-AND-C-STORE-B |
| Gas station, Lockhart TX (rebuild) | `/case-studies/gas-station-texas-sba/` | CS-R-GAS-STATION-TEXAS-SBA |
| Gas station, Lake Wales FL (rebuild) | `/case-studies/gas-station-florida-sba/` | CS-R-GAS-STATION-FLORIDA-SBA |
| Gas station acquisition, Opelika AL (rebuild) | `/case-studies/gas-station-alabama-sba/` | CS-R-GAS-STATION-ALABAMA-SBA |
| Gas station, Cartersville GA (rebuild) | `/case-studies/gas-station-georgia-sba/` | CS-R-GAS-STATION-GEORGIA-SBA |
| Gas station, Versailles OH (new) | `/case-studies/gas-station-versailles-ohio-sba/` | CS-Q-VERSAILLES-OHIO-GAS-STATION |
| Truck stop, Terrell TX (rebuild) | `/case-studies/truck-stop-texas-sba/` | CS-R-TRUCK-STOP-TEXAS-SBA |
| Limited-service hotel, Bastrop TX (rebuild) | `/case-studies/hotel-texas-sba/` | CS-R-HOTEL-TEXAS-SBA |
| RV park, Bastrop TX (rebuild) | `/case-studies/rv-park-texas-usda/` | CS-R-RV-PARK-TEXAS-USDA, PA-USDA |
| Express car wash, Seguin TX (rebuild) | `/case-studies/car-wash-texas-sba/` | CS-R-CAR-WASH-TEXAS-SBA |
| RV and boat storage, Granbury TX (rebuild) | `/case-studies/rv-boat-storage-texas-sba/` | CS-R-RV-BOAT-STORAGE-TEXAS-SBA |
| Franchised auto dealership, Weatherford TX (rebuild) | `/case-studies/auto-dealership-texas-sba/` | CS-R-AUTO-DEALERSHIP-TEXAS-SBA |
| Assisted living and memory care, Boerne TX (rebuild) | `/case-studies/assisted-living-texas-hud/` | CS-R-ASSISTED-LIVING-TEXAS-HUD, PA-HUD-AGENCY |
| Meat and poultry processing, Elgin TX (rebuild) | `/case-studies/meat-processing-texas-usda/` | CS-R-MEAT-PROCESSING-TEXAS-USDA, PA-USDA |
| I-10 travel center, Hankamer TX (new) | `/case-studies/travel-center-hankamer-texas-usda/` | CS-Q-HANKAMER-TEXAS-TRAVEL-CENTER, PA-USDA |
| Lodging and retreat, Johnson City TX (new) | `/case-studies/lodging-retreat-johnson-city-texas-sba/` | CS-Q-JOHNSON-CITY-TEXAS-LODGING |

   The hub's `truck-stop-travel-center` link points at `/asset-classes/truck-stop-and-travel-center/`, and no subtype page is built for it.

2. **The factory.** Page sources live in `src/` and are never served (WEB-FSC-4's `/src/*` rule). One source file per page carries front matter (type, URL, title, meta description, H1, breadcrumb, schema types, byline type, published and updated dates, the numbered sources list) and the body as HTML fragments with markers. One template per page type in `src/templates/` (state, metro, hub, subtype, case), cut from the current house pages so the look does not change. `scripts/build.py` renders each source into its served `index.html`: the house head with the inline CSS byte for byte, chrome regions, byline and regulatory markers, mesh regions, JSON-LD (WebPage or Article, BreadcrumbList, the author `@id`), and the sources list. It has `--check` (served HTML equals a fresh render everywhere outside the script-owned regions, `chrome:`, `mesh:`, `fsc:`, `sba:`, `mkt:` and `case:`, which their own scripts check) and `--page <url>`. CSS the new components need (the sensitivity matrix, the Study at a Glance table) goes in one appended block every factory page shares. Later lanes add pages by adding source files only.
3. **The case model engine.** `scripts/casemodel.py` reads `data/cases/<slug>.json`. Every input carries either its source number on the page or the label "assumption" with its reasoning, built from that case's own research and public data and never from another engagement. The engine computes sources and uses, the loan structure under the program's rules (SBA from `sba.json`: equity tier, DSCR floor, the $5,000,000 debenture cap; USDA B&I and HUD 232 terms from PA-USDA and PA-HUD-AGENCY with their citations), a five-year pro forma, DSCR by year, break-even, a sensitivity matrix (two drivers, five steps each), and the determination: as proposed, and as restructured when the proposed structure fails a floor or a tier. Case pages render every number in their tables from `<!--case:<slug>.<table>-->` regions; `casemodel.py --check` fails on any stale table. The Opelika acquisition follows Appendix 15: the page states the 1.25x historical-EBITDA rule from `sba.json` and labels the seller's trailing two years as illustrative inputs.
4. **Case standard v3, on every case.** The house disclosure box directly under the H1 and byline ("**Representative worked example.** The site, sponsor and project are hypothetical. The market evidence comes from the public sources listed below, with their dates. This page shows how the market analysis is built and how it sets the loan. It is not a client engagement."). A Study at a Glance table. The town, county and corridor named; the subject site described without street number, parcel id, owner or business name. Then: market conclusion first; demand evidence; a competitor census naming each competitor, each row carrying the URL of its own website or the county assessor record that confirms it; utilities, zoning and traffic counts where the research found them, otherwise a lender condition; revenue build; operating expense build; sources and uses; loan structure; five-year pro forma; DSCR by year; break-even; sensitivity matrix; risk factors; lender conditions; FAQ; dated sources. 4,500 to 6,500 body words.
5. **The Texas state page.** At least 6,000 body words from ST-TEXAS, MT-TEXAS and the register. Keep today's sections where they serve and add statewide economy and capital access, rules by asset class, costs and insurance, hazards, statewide supply, and the 2025 to 2026 events a reviewer will ask about. The metros section heading counts eight. Each of the eight metro cards links its page and says in one sentence what sets that market apart. A "Worked cases in Texas" section lists all eleven cases plus multifamily-texas-agency. Program sections link the practice areas.
6. **The eight metro pages.** 2,500 to 3,500 body words each from MT-TEXAS and the register: economic base, growth, corridors (with DOT traffic counts where found), supply by asset class, local rules, active lenders, eligibility (USDA rural, Opportunity Zone, HUBZone where found), the cases located in that metro's region, and what a lender should verify there. Target queries are "feasibility study <metro>", "feasibility study consultant <metro>", "feasibility study company <metro>" and "market study <metro>", with "Texas" where it reads naturally; the title carries "Feasibility Study", the metro and the state, with the house brand suffix. No keyword stuffing.
7. **The gas station hub.** 8,000 to 10,000 body words from AH-GAS-STATION-AND-C-STORE-A and -B, SD-GAS-STATION-AND-C-STORE and the register: development cost per unit, operating benchmarks, SBA loan performance by NAICS, valuation, industry structure, demand method, supply density by state, the subtypes (each linking its page), review failures, a document checklist, and the five cases. The SBA statements stay accurate: 13 CFR 120.160(b) says SBA "may require" a study; nothing on these pages says SBA requires one.
8. **The six subtype pages.** 2,000 to 3,000 body words each, from SD-GAS-STATION-AND-C-STORE and the subtype rows of the B run: how the subtype earns, what it costs, how lenders underwrite it, where it fails review, which cases show it.
9. **Every page is its own.** Prose is written from each page's own facts. Section headings may repeat across siblings; sentences may not. FAQ answers are unique per page. Write from the research's facts, never its sentences.
10. **Sources.** Every figure carries value, period, publisher and title, and URL, in the page's numbered sources list. Consulting-firm sources are allowed. Wert-Berater is never cited or named. The owner's other properties are never cited; a figure sourced only to one of them is re-sourced or dropped. The forbidden pattern, case-insensitive: `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er` (the brackets stop this charter from matching itself).
11. **Federal figures.** If WEB-FSC-5 is on `main` when you integrate, the federal series on the state and metro pages render from its register through `mkt:` markers and override any research value for the same series; log each conflict. If it is not, ship with the research values cited to their federal source as the research gives them, and list those pages in CLOSE for a later marker pass.
12. **Byline** through the author record only (Mark Otava, rendered by `byline.py`). No credential typed by hand.
13. **Index all.** Every page carries `index, follow` and goes into the sitemap with its lastmod.
14. **Integration order.** Write and build in your branch from the start. Integrate only once WEB-FSC-4 is on `main`, because its scripts and its `/src/*` rule are needed. Then merge `main` into `web-fsc-6` and run, in order: `build.py`, `chrome.py`, `byline.py`, `regulatory.py`, `markets.py` (if present), `casemodel.py`, `mesh.py`, `links.py --relink` (this switches every pending link to a pilot page back on, sitewide), `sitemap.py`. Then gates, then deploy.
15. **Checkpoint for the roll-out.** As soon as `build.py` renders the Texas state page and one case that pass gates 1 to 6 and the look gate, commit and print one line to the owner: `WEB-FSC-6 GENERATOR READY <sha>`. Keep working without waiting. The roll-out lanes cut from that commit.

## Delegated (decide, log, keep going)

- Template internals, the source-file format and the CSS additions.
- Section order inside each template, as long as rulings 4 to 8 hold.
- The sensitivity drivers for each asset.
- The target-query list for each page's SEO finish.
- The subagent split. Suggested: the main session builds the factory and writes the Texas state page; one Opus subagent writes the eight metros; one writes the hub and the six subtypes; four write the fifteen cases in groups (gas stations; truck stop, travel center and car wash; hotel, lodging, RV park and RV storage; dealership, assisted living and meat processing); Sonnet subagents pre-read the research and hand each writer a fact sheet with source numbers.

The shape, unless you find a better one: `src/pages/<url path>.html`, each opening with a JSON front-matter block; `src/templates/<type>.html`; `scripts/build.py` on the standard library (string templates), with nothing beyond bs4 and lxml; `data/cases/<slug>.json` inputs; `scripts/casemodel.py` writing its tables into the case regions.

## How the proof could be faked (the gates are written against these)

- Padding to the word targets with boilerplate, or restating tables in prose. Word counts exclude tables, the sources list and the FAQ, and the overlap gate catches boilerplate.
- Meeting the 25-figure gate with trivial or recycled figures. A counted figure is a market figure with its own source and date that appears on no other page of the site. Counts of the page's own sections, and figures repeated from the state page onto a metro page, do not count.
- One template with the place names swapped. The overlap gate runs every page against every sibling (the eight metros, the six subtypes, the fifteen cases) and against the rest of the site, and the verifier reads the eight metros side by side for argument, not words.
- Case numbers typed into prose that the model never computed. Every number in a case table renders from `casemodel.py`; the mutation test changes one input and confirms the tables move and `--check` fails.
- A "verified" competitor census with nothing behind it. Each competitor row carries the URL that confirms it.
- A real business as a case subject, through an address, a parcel id or a name.
- Federal series typed in from the research that disagree with the WEB-FSC-5 register.
- An SBA mandate claim slipping back in through a rewritten paragraph.

## Gates (all green before deploy; commands and outputs in `docs/web-fsc-6/GATES.txt`)

1. **Pages.** 31 pages built: 14 at existing URLs, 17 new. Each has exactly one `<title>` outside comments and JSON-LD that parses, with BreadcrumbList and the author `@id`.
2. **Factory.** `build.py --check` and `casemodel.py --check` exit 0. Mutation tests for both pass (one changed input moves the output and makes `--check` fail) and are reverted without a commit.
3. **Unique figures.** Every page carries at least 25 dated, sourced market figures that appear on no other page of the site. The count per page is recorded.
4. **Overlap.** 8-word shingles of lowercase tokens over `<main>` text minus scripts, styles and the sources list; overlap is shared shingles over the smaller page's shingles. Every page is under 15% against every sibling and against every other page on the site. The matrix is recorded.
5. **Standalone.** Every metro page passes gates 3 and 4 on its own geography's data (the WEB-FSC-5 audit if present). A metro that fails folds into the Texas page as a section and is not built.
6. **Case standard.** Every case has every component in ruling 4 and a body length in range. The equity tiers, DSCR floors and the debenture cap from `sba.json` hold; the Opelika acquisition follows Appendix 15.
7. **Sources.** Every figure carries its four parts. The ruling 10 pattern returns nothing in served files or in the author fields of this lane's commits. The WEB-FSC-2 stale-claim grep returns zero, including any "SBA requires" attached to a feasibility study.
8. **Subjects.** No case subject carries a street number, a parcel id, an owner name or a business name.
9. **Links.** After integration, `links.py --check` and `mesh.py --check` exit 0. Every pilot page has at least 3 inbound contextual links from distinct non-index pages. Every Texas case is linked from the Texas page and from its metro; every gas case from the hub; every subtype from the hub and back. The pending links to pilot pages that `--relink` switched on are counted.
10. **Clean text.** Zero em dashes and en dashes in any encoding across these pages. `grep -riE "otava,? *(ph\.?d|ccim|mai)"` returns nothing.
11. **Markers.** `byline.py --check`, `regulatory.py --check`, `chrome.py --check` and `markets.py --check` (if present) exit 0.
12. **Dates.** JSON-LD `dateModified`, the visible line and sitemap `lastmod` agree on every pilot page. New pages are published on the deploy date; rebuilt pages keep their published date and show Updated on the deploy date.
13. **Look.** Desktop 1440 and mobile 390 screenshots into `docs/web-fsc-6/look/` of Texas, two metros, the hub, two subtypes and three cases. No page-level horizontal scroll at 390; the sensitivity matrix and the pro forma fit or scroll inside their own box.
14. **Index all.** Every pilot page carries `index, follow` and is in the sitemap with its lastmod.

## Close

**Freeze before any verification:** commit, then record the HEAD sha, the sha256 of `git archive HEAD`, and the state behind the pages, not just the pages: the sha256 of every file under `src/` and `data/cases/` and of the `casemodel.py` output, plus the draft deploy id with its check results. Hand the frozen sha to:

- two attackers on Opus, working separately. Attacker one hunts wrong numbers: it re-derives 40 figures from the research files and the case inputs, weighted toward the cases and their DSCR tables. Attacker two hunts sameness and sourcing: false unique-figure counts, near-duplicate prose between siblings, banned sources, a real-business subject, an SBA mandate claim. Each finding comes with page, line and a reproduction.
- one verifier on Sonnet, reading the frozen tree cold, whose default verdict on every CLOSE claim is refuted until it reproduces the claim itself.

Resolve every finding by reproducing it, never by counting how many agents agreed: a tally measures how a finding was argued, not how the world is. Any fix after the freeze means a new freeze and a rerun of the gates the fix touches.

**Land and deploy.** Once WEB-FSC-4 is on `main`, run ruling 14's integration, rerun the gates, refreeze, and fast-forward local `main` to the frozen head from the worktree with `git push . HEAD:main` (if another lane landed meanwhile, merge `main` again, rerun the integration and gates 1, 2, 9 and 11, refreeze and retry). Deploy with the Netlify CLI from `git archive main`, from the archive root so the contact function ships: draft first and its checks, then production. Production checks: HTTP 200 and the expected H1 on all 31 pages; a sample of five formerly pending links elsewhere on the site now resolving to pilot pages; `/src/` and `/docs/web-fsc-6/CLOSE.md` returning 404; sitemap lastmod matching the pages. Run `scripts/indexnow.py` on all 31 URLs, every page whose links `--relink` changed, and the sitemap; record the response. Then try `git push origin main web-fsc-6`. If it fails for credentials, do not look for any. Write a bundle of `main` to `<repo>/_bundles/web-fsc-6-<sha>.bundle`, clone-test it, and state in CLOSE that `main` is live but not on GitHub, so nothing may push an older `main` to GitHub before this one.

Write `docs/web-fsc-6/CLOSE.md`: the head you cut from; the factory (files, how to add a page, how to add a case); the 31 pages with word counts, unique-figure counts and overlap maxima; each case's determination as proposed and as restructured; research figures dropped or re-sourced and why; NOT FOUND items turned into lender conditions, counted by page; whether the WEB-FSC-5 register was used and the pages left for a marker pass; each gate with its command and result; attacker and verifier findings with their resolution; deploy ids, rollback id, production checks and the IndexNow response; the bundle and push state; owner items, including one line telling the owner to resubmit `/sitemap.xml` in Search Console.

End your turn with exactly this five-line report:

WEB-FSC-6 CLOSE
head <sha> | freeze <sha> | archive sha256 <first 12> | generator ready at <sha>
pages <n>/31 | words <total> | min unique figures <n> | max overlap <n>%
deploy <id> | rollback <id> | pushed <yes/no> | gates <green>/14 | verifier blocker <n> major <n>
owner: <one line, or none>
