# ROLLOUT-1: THE RULEBOOK FOR THE FOURTEEN ROLL-OUT SESSIONS ON FEASIBILITY-STUDY-COMPANY.COM

Issued 16 October 2026 by the coordinator for the owner. This file is the full charter for every roll-out session. Each session also gets a short paste block that names its lane, its pages, its research and its owned paths. The block adds an assignment and never relaxes a rule in this file. Where the two seem to disagree, this file wins, unless the block says which numbered ruling it overrides and why.

Deploy pre-authorized: yes, by the integrator only. Index all: every page ships indexable. Run end to end without stopping for questions.

| | |
|---|---|
| Sessions | Thirteen builders and one integrator, all started at the same time. Builders: GEO-1, GEO-2, GEO-3, GEO-4 (states and metros), ASSET-1, ASSET-2, ASSET-3, ASSET-4 (hubs and subtypes), CASE-1, CASE-2, CASE-3, CASE-4 (worked cases), METHOD-1 (practice areas, framework pages, notes). INTEGRATOR lands, builds, gates and deploys. |
| Repo | `~/Downloads/Feaisbility-Study-Company.com` (spelled as on disk). Remote `origin` is the public GitHub repository `Feasibility-study-company.com`. Static HTML, no build step on Netlify; the publish root is the repo root. Never work in the main repo directory. |
| Worktrees | Builder: `~/Downloads/wt-rollout-<lane>` on branch `rollout-<lane>`, lane in lower case (`rollout-geo-1`, `rollout-case-4`, `rollout-method-1`). Integrator: `~/Downloads/wt-rollout-int` on branch `rollout-int`. |
| Shared folder (outside the repo) | `~/Downloads/fsc-rollout/`: `bus/ready/`, `bus/landed/`, `bus/returns/`, `bus/status/`, `bus/requests/<lane>/`, `private/` (gate 8 lists), `drafts/<lane>/`, `tmp/<lane>/` (throwaway build copies). Create what is missing with `mkdir -p`. Nothing in it is ever committed. |
| Research input (read only) | `~/Downloads/FSC Deep Searches 2/`. Locate each file by the Research ID on its first lines, never by file name. Never copy these files, or sentences from them, into the repo. |
| Records | `docs/rollout/<lane>/` in each branch (committed; production returns 404 for `/docs/*`, and the deploy tree never carries `docs/`). |
| First action | After step zero, save your paste block verbatim to `docs/rollout/<lane>/input/BLOCK.md`, record the sha256 of this file as you read it in `docs/rollout/<lane>/STEP-ZERO.md`, and commit both. |

## The job in one paragraph

Ship every page the research in the folder can support, indexed, on top of the factory WEB-FSC-6 built. That means:

- 42 state pages (31 rebuilt, 11 new) and every metro page that stands on its own evidence (249 metro slugs are already promised as pending links across the site, and the 11 new states add their own);
- 40 asset-class hubs (27 rebuilt, 13 new) and every subtype page that stands on its own (184 subtype slugs are already promised);
- 68 worked cases (46 rebuilt on their research files, 22 new);
- five practice areas (four rebuilt, one new);
- the analytical framework pages that stand on their own (13 slugs promised), and the research notes listed for METHOD-1.

Builders write page sources and case inputs in their own branches and hand finished clusters to the integrator as tagged tranches. The integrator merges each tranche, renders it, gates it against the whole site, deploys it and submits it, all night. A page that cannot meet the gates on the evidence in hand folds into its parent as a section, and its slug stays a pending link.

## The hard constraint

Every figure on every page traces to a dated source in the research files or in the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. No figure is invented, estimated beyond what its source says, or carried over from any client engagement or from any other property of the owner. A NOT FOUND in the research becomes a lender condition (cases) or a stated gap (reference pages), never a number. Cases are hypothetical, say so in the house disclosure box, and never make a real business, a real listing or a real address the subject. If a page cannot meet the gates, it folds into its parent rather than shipping thin.

Why the gates are strict: the site is about to grow from 167 URLs to several hundred, on templates, in a financial (YMYL) niche, weeks after Google's September 2026 spam update. Google's scaled content abuse and doorway policies target exactly a set of place-name pages that differ only in the names. What keeps this roll-out on the right side of those policies is that every page carries its own evidence, its own argument and its own numbers. The unique-figure, overlap and standalone gates exist for that reason, and folding a page is a success, not a failure.

## Standing scaffolding

Step zero, four probes, before any write:

1. **Repo and head.** `git -C <repo> fetch origin`. Local `main` sat at `2611fc0` when this was issued. `origin/main` is ahead of it by coordinator commits only (author `noreply@feasibility-study-company.com`, subject starting `Coordinator:`), including the commit that adds this file. Any other commit on `origin/main` that local `main` lacks is a stop: someone pushed outside this process.
   - **Builders** cut from `origin/main`: `git worktree add -b rollout-<lane> ~/Downloads/wt-rollout-<lane> origin/main`. From then on they merge local `main` (the integrator's) and never `origin/main`.
   - **The integrator** fast-forwards local `main` to `origin/main` from its own worktree (`git push . origin/main:main` from `~/Downloads/wt-rollout-int`, which fails safely if not a fast-forward), then cuts `rollout-int` from it. After that, local `main` moves only by the integrator's landings, and `origin/main` moves only when the coordinator pushes a bundle the integrator wrote or a `Coordinator:` commit.
2. **Twin guard, both arms.**
   - Process arm: list running Claude Code CLI processes whose working directory is inside the repo or any of its worktrees (`lsof -a -d cwd -p <pid>`). Exclude this session's own process and the Claude desktop app's Electron helpers (anything running from `/Applications/Claude.app/`).
   - Git arm: `git worktree list --porcelain`; any `index.lock` in the repo's git dir or in a worktree git dir; and whether your branch or worktree path already exists.
   - A live session holding your lane's branch or worktree is a stop. The other thirteen lanes in their own worktrees are expected and are not a stop. The zero-byte `stale-index-lock` and `stale-maintenance-lock` files in the git dir are ignored by git; leave them. An `index.lock` held by another lane's worktree is theirs: wait and retry, never delete it.
3. **Netlify identity.**
   - Integrator: confirm site `0a67950d-6092-49c3-8277-017897c1b865` serves `feasibility-study-company.com`. Record the published deploy id (it should be `6ad23bed0dd08e20da34458c`, locked) as the rollback point, and confirm that auto publishing is stopped.
   - Builders never call Netlify. Their probe 3 is a read-only GET of `https://feasibility-study-company.com/`, recording status and H1.
4. **Environment and inputs.**
   - Free disk of at least 10 GB.
   - python3 with bs4 and lxml. Anything else goes in a virtualenv inside your worktree, never system-wide.
   - A headless browser for screenshots (`docs/web-fsc-6/tools/shots.mjs` shows the way).
   - The Netlify CLI logged in (integrator only).
   - Every research file in your block found by its Research ID, with its word count logged.

No database is involved. Every network call and every subprocess carries a timeout, and nothing waits unbounded.

Speed rules:

1. Do not ask the owner questions. Decide, log in `docs/rollout/<lane>/DECISIONS.md`, continue.
2. Never end your turn while a subagent, a build, a gate, a deploy or a review is running, or while your lane has work left. Write pages in parallel.
3. Stop only for a step zero stop, a red gate you cannot fix in scope, or free disk under 5 GB.
4. Stage explicit paths only. No `git add -A`, no `git add .`.
   - Never open, read or print `.ghtoken` in the repo root.
   - No credential in the repo, a log or a commit.
   - `_bundles/` and `_cache/` are never staged.
5. Commit as `git -c user.name="Feasibility Study Company" -c user.email="noreply@feasibility-study-company.com" commit ...`. The repo's configured identity carries the sister firm's domain, and this repo is public. Annotated tags use the same identity.
6. Network: read-only GETs to the production domain and to sources you cite or check (competitor websites, county assessor pages, agency pages). Never work around robots.txt, a 403, a WAF or a bot check: a closed door is recorded as NOT FETCHED with its reason.
   - The Netlify CLI and IndexNow are for the integrator only.
   - No lane pushes to GitHub. Git on this Mac has no GitHub credential; do not look for one.

## Measured facts (from the repo at `7ed837f` and the research folder on 16 October)

- **The site.** 167 URLs in the sitemap. Production is deploy `6ad23bed0dd08e20da34458c`, published from `main` at `8e3a387` without `docs/`, `src/` or `data/markets/`, and locked: auto publishing is stopped, so a GitHub push publishes nothing. `netlify.toml` (since `7ed837f`) removes all three folders on Git builds too.
- **Pending links.** 468 distinct promised targets carry `data-fsc-pending` anchors across the site:
  - 249 metros in 31 states;
  - 188 subtypes under 28 hubs;
  - 16 hub-level slugs;
  - 13 framework children;
  - Ohio;
  - one retired infrastructure page.

  `scripts/links.py --relink` switches each anchor on, sitewide, the day its page exists. `scripts/chrome.py` does the same in the header, panels and footer.
- **The factory (WEB-FSC-6).**
  - Page sources: `src/pages/<url>.html` (JSON front matter between `---` lines, then `<section>` blocks), in the format specified in `src/README.md`.
  - Templates: `src/templates/` holds base, state, metro, hub, subtype and case.
  - Rendering: `scripts/build.py [--page <url>] [--check] [--list]`. Its `TYPES` are those five only. It refuses dashes in any encoding, a banned name, a second title or h1, a duplicate id, broken JSON-LD, an unknown `sba:` path and unexpanded shorthand.
  - Cases: `scripts/casemodel.py` with `data/cases/<slug>.json`. It supports `sba_7a`, `sba_504`, `usda_bi` and `hud_232` only. It solves the restructure, renders every case table into `case:` regions, refuses a glance or a card that contradicts its own tests, fills the `/case-studies/` cards from `src/case-cards.json`, and computes returns from `data/returns/`.
  - QA tools in `docs/web-fsc-6/tools/`:
    - `pagecheck.py` (body words, unique sourced figures outside script-owned regions, 8-word shingle overlap against every served page);
    - `gates.py`, `sbamandate.py`, `shots.mjs`, `srcedit.py`.
  - The chain, in order: `build.py`, `chrome.py`, `byline.py`, `regulatory.py`, `markets.py`, `casemodel.py`, `mesh.py`, `links.py --relink`, `sitemap.py`.
- **What WEB-FSC-6 shipped.** 23 of 31 pages: Texas, four metros, the gas station hub, two subtypes and 15 cases. Minimum 29 unique figures per page, maximum overlap 7.04%.
  - Folded: McAllen, El Paso, Lubbock and Corpus Christi (12, 7, 8 and 13 unique own-geography figures; drafts in `docs/web-fsc-6/folded/`), and four gas station subtypes.
  - Three review rounds found case "sites" that were real listed properties: the exact asking price sat next to the acreage, road or zoning. Every case now uses a round, labelled land assumption and a generic site. The gate 8 identifier list for those 15 cases lives outside the repo (env `FSC6_DNU`).
- **The register (WEB-FSC-5, `data/markets/`).**
  - Coverage: every state, all 3,222 counties, all 935 CBSAs and the 253 site markets, of which 238 are standalone.
  - Series:
    - Census population estimates, Vintage 2023 only (the API held PEP there; pages that cite Vintage 2025 keep it);
    - ACS 5-year 2020-2024 and 1-year 2024;
    - County Business Patterns 2023 by asset class (43 classes, graded exact, partial or proxy);
    - BEA personal income 2024;
    - SBA 7(a) and 504 FOIA loan files as of 2026-06-30.
  - NOT FETCHED, each with a recorded refusal: building permits, QCEW and HUD Fair Market Rents.
  - How to put a figure on a page: `docs/web-fsc-5/CLOSE.md`, "For the next lanes". `mkt:` markers with geo `us`, a state code, `co-<FIPS>`, `cbsa-<code>` or a market key.
  - Today `pagecheck.py` does not count figures inside `mkt:` regions.
- **Research inventory (314 files).**
  - ST: 43 states, every state with a page plus DE, ID, KS, KY, LA, MT, NE, OH, RI, TN and WV.
  - MT: 42 states (no MT-PENNSYLVANIA).
  - AH: 41 asset classes, mostly an A run (unit economics and capital) and a B run (demand method, supply, subtypes, review patterns).
  - SD: 17 subtype evidence files.
  - CS-R: 58 cases, one per existing case page.
  - CS-N: 15 new cases.
  - CS-Q: 11 named-town cases.
  - PA: CONVENTIONAL, EB5, HUD-AGENCY, USDA.
  - IW-prefixed files.
  - Nine files without a Research ID.
- **Research hygiene.** Some files cite the owner's sister properties or the banned consulting firm. Two files without IDs were written for another of the owner's properties (ruling 2). Six case files are built around a real, named operating business or a street address: CS-R-MARINA-MARYLAND-SBA, CS-R-AUTO-SERVICE-NEW-JERSEY-SBA, CS-R-RESTAURANT-MISSOURI-SBA, CS-N-HOTEL-OHIO-SBA-7A-ACQUISITION, CS-N-LAUNDROMAT-ACQUISITION-OHIO-SBA-7A and CS-Q-GIG-HARBOR-WASHINGTON-MARINA. Their titles carry the name. The pages built from them use a hypothetical subject (ruling 7).
- **Cases with no research file stay as they are:** multifamily-texas-agency, veterinary-michigan-sba and the four batch-1 cases (cabin-resort-townsend-tennessee-sba, dry-stack-cape-coral-florida-sba, glamping-oak-hill-west-virginia-usda, rv-park-ossipee-new-hampshire-usda). CS-Q-COPPERAS-COVE-TEXAS-STORAGE-YARD is never built: it sits in the submarket of a live client engagement.

## Already ruled

1. **Lanes and ownership.** A builder commits only these paths:
   - `src/pages/<path>.html` for the URLs its block assigns;
   - `data/cases/<slug>.json` and `data/returns/<slug>.json` for its cases;
   - `src/case-cards/<slug>.json` for its cases, once FACTORY-2 exists (ruling 14);
   - `docs/rollout/<lane>/`.

   Builders also never commit:
   - served HTML: the integrator renders every page;
   - scripts or templates, with two exceptions. METHOD-1 adds new template files for its page types once FACTORY-2 exists. CASE-4 owns `scripts/casemodel.py` once FACTORY-2 exists and makes every engine change any lane needs.
   - `data/site/`, `data/mesh/`, `data/markets/`, `data/regulatory/`, `data/authors/`, `src/site.json`, `src/case-cards.json`, `src/README.md`, `netlify.toml`, `sitemap.xml`, `robots.txt`, `feed.xml`, `index.html` or any section index page.

   The integrator owns all of those. A builder who needs a change to one of them writes it as a request (ruling 13). A merge conflict on a path the lane does not own means the tranche is returned.

   **The case engine after FACTORY-2.**
   - A CASE lane that needs an engine change writes it to `~/Downloads/fsc-rollout/bus/requests/case-4/<lane>-<n>.md` with the case, the input shape and the test it needs. CASE-4 answers in `bus/requests/<lane>/`.
   - Every CASE-4 engine change leaves the rendered output of every case it does not own byte-identical, including the fifteen WEB-FSC-6 cases. CASE-4 proves this in its tranche record by rendering every case before and after and diffing.
   - The one exception is a fix to a recorded error, which CASE-4 logs with its reproduction and lists in the tranche record.
2. **Research IDs.**
   - **Usable:** files whose Research ID starts `ST-`, `MT-`, `AH-`, `SD-`, `CS-` or `PA-`, plus three files without an ID, used by METHOD-1 and identified by their first heading:
     - "Rural Financing Choices in FY2027";
     - "Proving Demand for SBA Feasibility Studies";
     - "Credit-Risk Evidence Pack: Which SBA 7(a) and 504 Loans Fail".
   - **Also usable:** two more files without an ID, "SBA Feasibility Studies: What the Rules Actually Require" and "SBA and USDA Lending, October 2026: Where the Thought-Leadership White Space Is". METHOD-1 may use them, and any lane may read them for the rules.
   - **Never used for page content:**
     - files with an `IW-` ID, which belong to another property's program;
     - the two 10 October files without an ID (the Polk County RV park pack and the Kane County glamping pack);
     - "Valuation Theory and Professional Standards Behind the SBA Feasibility Study" and "SBA Feasibility Study: SERP Landscape", both written for another of the owner's properties;
     - CS-Q-COPPERAS-COVE-TEXAS-STORAGE-YARD.
3. **Page standards by type.** Body words exclude tables, the sources list, the FAQ, the breadcrumb and generated mesh lists.
   - **State:** 4,500 to 8,000 body words. Write from ST-, MT- and the register.
     - Sections: economy and capital access; rules by asset class; costs and insurance; hazards; statewide supply; the 2025 to 2026 events a reviewer will ask about; the metros (a heading that counts the cards, one card per metro, each card linking the metro page or its folded section, with one sentence on what sets that market apart and without repeating any figure the metro page counts); the program sections linking the practice areas; and "Worked cases in <state>" listing every case in the state.
     - Rebuilt pages keep today's sections where they serve, and their published date.
   - **Metro:** 2,000 to 3,500 body words. Write from the MT- file and the register.
     - Cover: the economic base; growth; corridors (with DOT traffic counts where found); supply by asset class; local rules; active lenders; eligibility (USDA rural, Opportunity Zone and HUBZone where found); the cases located in its region; and what a lender should verify there.
   - **Hub:** 6,000 to 10,000 body words. Write from AH- A and B, the SD- file where one exists, and the register (CBP establishments, SBA FOIA performance for the class).
     - Cover: development cost per unit; operating benchmarks; SBA loan performance by NAICS; valuation; industry structure; demand method; supply density by state; the subtypes (each linking its page or its folded section); review failures; a document checklist; and the cases.
   - **Subtype:** 1,800 to 3,000 body words. Write from the SD- file and the subtype rows of the B run.
     - Cover: how the subtype earns, what it costs, how lenders underwrite it, where it fails review, and which cases show it.
   - **Case:** standard v3 (ruling 7), 4,500 to 6,500 body words.
   - **Practice area:** 5,000 to 9,000 body words.
   - **Framework page and research note:** 2,500 to 5,000 body words.
4. **Every page is its own.**
   - Write prose from each page's own facts. Section headings may repeat across siblings; sentences may not. FAQ answers are unique per page. Write from the research's facts, never its sentences.
   - A parent page (state, hub) summarizes a child (metro, subtype) in a sentence and a link, never by repeating the figures the child counts. Counted figures belong to the most specific page: case over metro over state, subtype over hub.
5. **Counted figures and the gates every page meets.** A counted figure is a market figure with its own value, period and source that appears on no other served page by value. Rounded and rescaled repeats count as the same figure. Counts of the page's own sections, `sba:` values and `case:` values do not count.

   | Page type | Counted figures at READY | Of which from research files | Of which from the register (`mkt:`) | Counted figures at landing |
   |---|---|---|---|---|
   | State, metro, hub, subtype, case, practice area | at least 30 | at least 15 | at most 10, each a different series and geography pair | at least 25 |
   | Framework page, research note | at least 18 | at least 10 | at most 8 | at least 15 |

   The landing floor is checked against the merged site, so a figure another lane's page also carries stops counting for both. The READY margin is what absorbs that.
   - **Overlap:** 8-word shingles of lowercase tokens over `<main>` text minus scripts, styles, generated mesh lists and the sources list, divided by the smaller page's shingles. It must stay under 15% against every page on the merged site.
   - **Standalone:** every metro and subtype passes the figure and overlap gates on its own geography's or its own subtype's evidence.
   - **Links:** after landing, every page has at least 3 inbound contextual links from distinct non-index pages.
6. **Folding.**
   - Pre-count first: before a writer drafts a metro or subtype, a Sonnet reader counts the dated, sourced, page-specific figures the research and the register hold for it.
   - Under 30 at that count means the page is not written as a page. It becomes a section of its parent, with its own id equal to the slug, written in the parent's voice, and the slug stays a pending link.
   - A page that falls below the floor later also folds.
   - Record every fold with its count in `docs/rollout/<lane>/FOLDED.md`. Keep unused drafts in `~/Downloads/fsc-rollout/drafts/<lane>/`, never in the repo. Folding is decided by the count, not by effort spent.
7. **Case standard v3, and subjects.**
   - **Layout.** The house disclosure box sits directly under the H1 and byline: "**Representative worked example.** The site, sponsor and project are hypothetical. The market evidence comes from the public sources listed below, with their dates. This page shows how the market analysis is built and how it sets the loan. It is not a client engagement." Then a Study at a Glance table.
   - **Location.** The town, county and corridor are named. The subject site is described without street number, parcel id, owner, business name, listing or broker.
   - **Sections, in order:**
     - market conclusion first;
     - demand evidence;
     - a competitor census naming each competitor, each row carrying the URL of its own website or the county assessor record that confirms it;
     - utilities, zoning and traffic counts where found, otherwise a lender condition;
     - revenue build;
     - operating expense build;
     - sources and uses;
     - loan structure;
     - five-year pro forma;
     - DSCR by year;
     - break-even;
     - sensitivity matrix (two drivers, five steps each);
     - risk factors;
     - lender conditions;
     - determinations as proposed and as restructured;
     - FAQ;
     - dated sources.
   - **Numbers.** Every number in a case table renders from `casemodel.py`. Inputs carry a source number on the page or the label "assumption" with its reasoning. Land is a round, labelled assumption, never a listing's ask.
   - **Subjects.** Treat every case file as describing a real place until shown otherwise.
     - Before writing a case, list every business name, street address, parcel id, listing id, asking price, per-acre price, acreage, broker and owner name in its research file. Write them to `~/Downloads/fsc-rollout/private/dnu-<lane>.txt`, one per line, never in the repo.
     - The six files named in Measured facts become hypothetical subjects: keep the town and the market evidence, change the flag or brand to a generic description, round the size, and never use the real property's figures as the subject's.
     - An acquisition case whose town holds fewer than three operating businesses of the subject's type (count them in the competitor census) names the county or region instead of the town for the subject. It still names the town for the market evidence.
     - Acquisitions follow SBA Appendix 15 as in the Opelika case: the 1.25x historical rule from `sba.json`, with the seller's two trailing years labelled illustrative inputs.
8. **SBA wording and rules.**
   - SBA rules go through `sba:` markers. 13 CFR 120.160(b) says SBA "may require" a feasibility study; no page says SBA requires one. `docs/web-fsc-6/tools/sbamandate.py` guards this sitewide.
   - The equity tiers, DSCR floors, the debenture cap and the October 2026 rates come from `data/regulatory/sba.json`.
   - USDA B&I and HUD 232 terms come from PA-USDA and PA-HUD-AGENCY with their citations. Conventional, agency, EB-5 and DSCR-loan terms come from PA-CONVENTIONAL, PA-HUD-AGENCY and PA-EB5 with theirs.
9. **Sources and names.**
   - Every figure carries value, period, publisher and title, and URL, in the page's numbered sources list. Consulting-firm sources are allowed.
   - The owner's other properties are never cited or named. A figure sourced only to one of them is re-sourced or dropped. One consulting firm is never cited or named at all; it is the last alternative in the pattern below.
   - The forbidden pattern, case-insensitive: `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er`. The brackets stop this file from matching itself. Never write any of these names unbracketed in any file, commit, tag, log or request.
10. **The register.**
    - Use `mkt:` markers for series the research lacks: CBP establishments by class, SBA 7(a) and 504 counts, volumes and charge-offs by geography and class, ACS, and BEA.
    - Where the research holds a newer vintage of the same series (population at Vintage 2025, for example), the research figure stands and the register's older vintage of that series is not shown for that geography. Never put two vintages of one series on one page.
    - Do not add markets to the register. A new state's metro uses `cbsa-<code>` or `co-<FIPS>` geos, which already cover every CBSA and county.
    - Respect every refusal `markets.py` makes (flags, lower bounds, partial or proxy classes). Rule 5 caps how many register figures count.
11. **Byline and authority.**
    - The byline comes only from the author record (Mark Otava, rendered by `byline.py`). No credential is typed by hand, in prose or in JSON-LD.
    - Every page names its sources with dates. That, the worked arithmetic and the stated gaps are this site's E-E-A-T: no page claims experience it does not show.
12. **Index all, and dates.**
    - Every page carries `index, follow` and goes into the sitemap with its lastmod.
    - New pages: `published` and `updated` are `"DEPLOY"` in the source. Rebuilt pages keep their old published date (read it from the served page's JSON-LD), and `updated` is `"DEPLOY"`.
    - At landing the integrator pins every `"DEPLOY"` in the landed sources to that deploy's date, so a later deploy never re-dates an earlier page.
    - A builder who changes the content of an already-landed page sets its `updated` back to `"DEPLOY"`. JSON-LD `dateModified`, the visible line and the sitemap lastmod agree on every page.
13. **Tranches, the bus, and requests.**
    - **A tranche is one cluster:** a state with its metros; a hub with its subtypes; up to four cases; or up to four METHOD-1 pages. A page source enters `src/pages/` only when its tranche is READY. Until then drafts live in `~/Downloads/fsc-rollout/drafts/<lane>/`, which keeps unfinished text and any unscrubbed identifier out of a public repository.
    - **Readiness check.** Before marking a tranche READY, the builder:
      - merges local `main`;
      - makes a throwaway copy (`git archive HEAD | tar -x -C ~/Downloads/fsc-rollout/tmp/<lane>/<n>`) and applies its requests there;
      - runs the chain there and runs gates 1 to 14 on the tranche's pages against that whole copy;
      - freezes;
      - runs the review in ruling 17;
      - fixes and re-runs what the fixes touch;
      - records `docs/rollout/<lane>/tranches/t<n>.md` (pages, body words, counted figures research and register, overlap maximum with the page it is against, folds, gate results, review findings and their resolution);
      - commits.
    - **Signalling.** Then:
      - an annotated tag `rollout/<lane>/t<n>`;
      - a file `~/Downloads/fsc-rollout/bus/ready/<lane>-t<n>` holding the tag's commit sha and the page list.
    - **Requests** for integrator-owned files go in `docs/rollout/<lane>/requests.json`, in the format the integrator publishes with FACTORY-2: chrome links, mesh terms and topic entries, redirects and fallbacks, index-page entries. Before FACTORY-2, keep the list in prose in the same folder.
    - **Returns.** A returned tranche arrives as `bus/returns/<lane>-t<n>.md` with the failing gate output. The builder fixes it, or moves the failing pages back to drafts, and tags `rollout/<lane>/t<n>r<k>`. A tag only ever holds pages the builder believes pass, because the integrator merges a whole tag.
    - **Finishing.** When a lane has tagged its last tranche, it writes `bus/status/<lane>-final` with the last tag. It keeps watching `bus/returns/` until that tranche shows in `bus/landed/`, then closes.
14. **The integrator.**
    - **FACTORY-2 first,** within about two hours. Land it on `main` and tag `rollout/factory-2`. Builders do not wait for it to research and draft; they merge it before their first throwaway build that needs it. Its contents:
      - **(a) Page types.** `build.py` takes its page types from the templates present in `src/templates/`, with per-type settings (schema type, byline type, reference or article) in a small `src/types.json`, so METHOD-1 can add `practice`, `framework` and `note` templates without touching the script.
      - **(b) Case cards.** `casemodel.py` reads card templates from `src/case-cards/<slug>.json` as well as `src/case-cards.json`. This is the integrator's one and only change to `casemodel.py`; after FACTORY-2 the file belongs to CASE-4.
      - **(c) QA tools.** Copy the WEB-FSC-6 tools to `scripts/qa/` and generalize them.
        - `pagecheck.py` takes any URL list or a tranche manifest, counts register figures inside `mkt:` regions under ruling 5's caps, and reports research and register counts apart.
        - `gates.py` runs gates 1 to 14 on a URL set against the whole tree.
        - Gate 8 reads every list in `~/Downloads/fsc-rollout/private/`.
        - Copy the WEB-FSC-6 gate 8 list there as `dnu-web-fsc-6.txt`. Its path is in that lane's Claude Code memory notes and in its `FSC6_DNU` setting. If it cannot be found, record that gate 8 is not rerun on the fifteen WEB-FSC-6 cases.
      - **(d) Chrome.** `chrome.json` gains the eleven new states (hidden until built) and the thirteen new hubs (pending until built). The fifty states' order stays alphabetical.
      - **(e) Mesh.** `topics.json` gains the new hubs with their families, `state_neighbors` for the new states, and the new practice area.
      - **(f) Rewrites.** `fallbacks.json` gains the permanent rewrites in ruling 16.
      - **(g) Requests.** The `requests.json` format is written to `docs/rollout/int/REQUESTS.md`.
      - **(h) Date pinning.** A date-pinning step is added to the landing script.
    - **Landing loop,** every five minutes, one line of output per poll. Take the oldest READY tag not yet landed (you may batch several READY tags into one landing when they arrive together, and bisect by tranche if the batch fails). For each:
      - merge the tag into `rollout-int`;
      - apply the lane's requests;
      - pin dates;
      - run the chain over the whole tree;
      - run gates 1 to 14 on the tranche's pages and gates 3, 4, 9 and 10 on every page of the site;
      - also confirm that no already-landed page fell below its floor.

      If anything is red, check whether the tranche caused it. If so, reset `rollout-int`, write the return and move on to the next tag. If the integrator's own files caused it, fix them.

      When the run is green, the landing proceeds in this order:
      1. Commit and fast-forward local `main` (`git push . HEAD:main`).
      2. Deploy:
         - build the tree with `git archive main | tar -x -C <dir> --exclude=docs --exclude=src --exclude=data/markets`, and deploy from the archive root so the contact function ships;
         - make a draft deploy and check it, then a production deploy;
         - publish exactly that deploy id with the API (`restoreSiteDeploy`) while keeping the lock;
         - confirm with `getSite` that the published deploy is the new id and that auto publishing is still stopped, and lock the new deploy if it is not.
      3. Run the production checks: HTTP 200 and the expected H1 on every landed page; five formerly pending links now resolving; `/src/`, `/docs/`, `/Docs/` and `/data/markets/` returning 404; sitemap lastmod matching.
      4. Submit to IndexNow: `scripts/indexnow.py --since <previous landed sha>`, one POST per landing.
      5. Write a bundle of `origin/main..main` to `<repo>/_bundles/rollout-<sha>.bundle`. Keep the newest five, verify each, and never stage them.
      6. Write `bus/landed/<lane>-t<n>` with the main sha, deploy id and URL count.
    - **Owned pages.** The integrator updates every index page and the home page as pages land: lists, counts, and the stale-claim grep, so no page states an old number of states, cases or markets.
    - **Coordinator commits.** A `Coordinator:` commit that appears on `origin/main` is merged into the next landing.
    - **When to close.** The integrator closes when every lane has a `bus/status/<lane>-final` whose last tag has landed, or 72 hours after its start, whichever comes first.
15. **Models.**
    - Research-reading subagents (fact sheets with source numbers, pre-counts, the gate 8 identifier lists): Sonnet.
    - Writers: Opus.
    - The SEO finish of every state, metro, hub, practice area and framework page (title, meta description, H1, first-screen answer, FAQ): Fable. Subtypes, cases and notes get theirs from their Opus writer.
    - Attackers: Opus. Verifiers: Sonnet.
16. **One intent, one page.**
    - Every page answers its own query, and no two pages on the site compete for the same one. Title and H1 follow the pattern of the WEB-FSC-6 page of the same type:
      - "Houston Feasibility Study, Texas | Feasibility Study Company";
      - "Interstate Gas Station Feasibility Study | Feasibility Study Company";
      - "Gas Station Feasibility Study, Lockhart TX: SBA 7(a) Worked Case".
    - Format and wording rules:
      - Meta descriptions are 140 to 160 characters, and titles are about 60 characters where possible.
      - The first screen answers the query in two or three sentences carrying at least one counted figure.
      - Target queries are "feasibility study <place>", "<asset> feasibility study", "market study <place>" and "SBA feasibility study <asset>" where each reads naturally, with no stuffing.
      - "Does SBA require a feasibility study" belongs to `/research-notes/sba-feasibility-myth/` alone. `/practice-areas/sba-7a-504/` takes the service query and links to it.
    - These promised slugs duplicate another page's intent and are never built. FACTORY-2 rewrites them permanently in `fallbacks.json`:

      | Promised slug | Rewritten to |
      |---|---|
      | `/asset-classes/multifamily/build-to-rent/` | `/asset-classes/build-to-rent/` |
      | `/asset-classes/multifamily/manufactured-housing/` | `/asset-classes/manufactured-housing/` |
      | `/asset-classes/medical-office-and-asc/urgent-care/` | `/asset-classes/urgent-care/` |
      | `/asset-classes/medical-office-and-asc/veterinary/` | `/asset-classes/veterinary-practice/` |
      | `/asset-classes/rv-park-and-campground/glamping/` | `/asset-classes/glamping/` |
      | `/asset-classes/restaurant/quick-service/` | `/asset-classes/quick-service-restaurant/` |
      | `/asset-classes/quick-service-restaurant/coffee-and-beverage/` | `/asset-classes/coffee-shop/` |
      | `/asset-classes/self-storage/boat-rv/` | `/asset-classes/rv-and-boat-storage/` |
      | `/asset-classes/rv-and-boat-storage/boat-dry-stack/` | `/asset-classes/marina/dry-stack-storage/` |
      | `/asset-classes/limited-service-hotel/` | `/asset-classes/hotel/limited-service/` |
      | `/asset-classes/select-service-hotel/` | `/asset-classes/hotel/select-service/` |
      | `/asset-classes/extended-stay-hotel/` | `/asset-classes/hotel/extended-stay/` |
      | `/asset-classes/boutique-and-resort/` | `/asset-classes/hotel/boutique-and-independent/` |
      | `/asset-classes/active-adult/` | `/asset-classes/independent-living-and-ccrc/` |
      | `/asset-classes/ccrc-life-plan-communities/` | `/asset-classes/independent-living-and-ccrc/` |
      | `/asset-classes/board-and-care/` | `/asset-classes/assisted-living-and-memory-care/` |

      A rewrite target that is itself still pending falls back the way `links.py` already does (a subtype to its hub's section).
    - `/asset-classes/industrial/` gets its 301 to `/asset-classes/industrial-and-warehouse/` in `netlify.toml` in the same landing that ships that hub.
17. **Review before READY.** Each tranche is frozen first: commit, then record the head sha, the sha256 of `git archive HEAD`, and the sha256 of every source and case input in the tranche. The frozen sha goes to:
    - **attacker one on Opus (numbers):** re-derives at least 25 figures from the research files, the register and the case inputs, weighted toward cases and their DSCR tables;
    - **attacker two on Opus (sameness, sourcing, subjects):** hunts false counted figures, near-duplicate prose between siblings and against the site, banned sources, a real-business or real-listing subject, and an SBA mandate claim;
    - **one verifier on Sonnet:** reads the frozen tree cold, and its default verdict on every claim in `t<n>.md` is refuted until it reproduces the claim itself.

    The attackers work separately, and each finding comes with page, line and a reproduction. Resolve every finding by reproducing it, never by counting how many agents agreed: a tally measures how a finding was argued, not how the world is. Any fix after the freeze means a new freeze and a rerun of the gates the fix touches.

## Delegated (decide, log, keep going)

- Tranche order inside a lane. Suggested: largest populations and the most-linked pending slugs first, so the most promised links switch on soonest.
- Section order inside each type, as long as ruling 3 holds.
- The subagent split and how many writers run at once.
- Metro slugs for the eleven new states: lowercase, hyphenated, the market's common name, as the existing states do.
- New subtypes for the thirteen new hubs: define them only where the B run supports a page that passes; otherwise they are sections of the hub.
- Sensitivity drivers for each case.
- The integrator's request format, landing script and tool internals.

The shape, unless you find a better one:

- **Builder:** pre-count, fact sheet, draft, self-check in a throwaway copy, freeze, review, tag.
- **Integrator:** merge, requests, pin, chain, gates, land, deploy, submit, bundle, announce.

## How the proof could be faked (the gates are written against these)

- Padding to word ranges with boilerplate or with tables restated as prose. Word counts exclude tables, sources and FAQ, and the overlap gate catches boilerplate.
- Meeting the figure gate with trivial, recycled or register-stuffed figures. The research minimum and the register cap in ruling 5 stop the last of these, and the count runs against the merged site at landing.
- One template with the place names swapped. Overlap runs against every page on the site, and the verifier reads each tranche's siblings side by side for argument, not words.
- Case numbers typed into prose that the model never computed. Every case table renders from `casemodel.py`, and the mutation test moves an input and confirms `--check` fails.
- A competitor census with nothing behind it. Each row carries its URL.
- A real business, listing or address as a case subject. Gate 8 runs every list in `private/`.
- Federal series typed in from the research that disagree with the register for the same vintage.
- An SBA mandate claim slipping back in through a rewrite.
- A tranche that passes in the builder's copy and breaks something already live. The integrator gates every landing against the whole site.

## Gates (builders run them on each tranche in a throwaway copy; the integrator runs them at every landing; commands and outputs in `docs/rollout/<lane>/GATES-t<n>.txt`)

1. **Pages.** Every page in the tranche builds. Each has exactly one `<title>` outside comments, and JSON-LD that parses, with BreadcrumbList and the author `@id`.
2. **Factory.** `build.py --check` and, where cases are involved, `casemodel.py --check` exit 0. Each CASE lane runs one mutation test on its first tranche and reverts it without a commit. CASE-4 runs one per new program.
3. **Counted figures.** Ruling 5 floors, with research and register counts recorded per page.
4. **Overlap.** Under 15% against every page on the site; the sibling matrix is recorded.
5. **Standalone.** Every metro and subtype passes gates 3 and 4 on its own evidence, or it folds.
6. **Case standard.** Every ruling 7 component, the body length in range, and SBA tiers, floors and caps per `sba.json`. Acquisitions follow Appendix 15.
7. **Sources.** Every figure has its four parts. The ruling 9 pattern returns nothing in sources, served output, tag messages and commit authors. `sbamandate.py` returns zero.
8. **Subjects.** No identifier from any list in `private/` appears in any served file, source or commit message.
9. **Links.** `links.py --check` and `mesh.py --check` exit 0. Each page has at least 3 inbound contextual links from distinct non-index pages after landing. Required edges:
   - state and each metro both ways;
   - hub and each subtype both ways;
   - each case to its hub, its state and its metro where one exists;
   - each hub and each state to their cases.
10. **Clean text.** Zero em and en dashes in any encoding. `grep -riE "otava,? *(ph\.?d|ccim|mai)"` returns nothing.
11. **Markers.** `byline.py --check`, `regulatory.py --check`, `chrome.py --check` and `markets.py --check` exit 0.
12. **Dates.** JSON-LD `dateModified`, the visible line and sitemap lastmod agree. New pages carry their landing date, and rebuilt pages keep their published date.
13. **Look.** Screenshots at desktop 1440 and mobile 390 into `docs/rollout/<lane>/look/t<n>/` of at least one page of each type in the tranche, and all of them for four pages or fewer. No page-level horizontal scroll at 390; wide tables, the pro forma and the sensitivity matrix scroll inside their own box.
14. **Index all.** `index, follow`, and in the sitemap with lastmod (checked at landing).

## Close (every lane)

Write `docs/rollout/<lane>/CLOSE.md`:

- the head you cut from;
- every page with its type, body words, counted figures (research and register), overlap maximum and the page it is against;
- every fold with its count;
- cases with their determinations as proposed and as restructured;
- research figures dropped or re-sourced, and why;
- NOT FOUND items turned into lender conditions or stated gaps, counted by page;
- each tranche with its tag, review findings and their resolution, and its landing (or return);
- owner items, including anything that needs the owner's eyes.

Commit it on your branch and tag `rollout/<lane>/close`. The integrator lands that records-only commit with the next landing, or as the last one.

Builders end their turn with exactly this five-line report:

```
ROLLOUT <LANE> CLOSE
head <sha> | tranches tagged <n> | landed <n> | returned <n> | last tag <tag>
pages <shipped>/<assigned> | folded <n> | words <total> | min counted figures <n> | max overlap <n>%
gates <green>/14 on the last tranche | open findings blocker <n> major <n>
owner: <one line, or none>
```

The integrator closes with one final site-wide pass: every gate over every page, a freeze, two Opus attackers sampling across all lanes (numbers, sameness and subjects), and a Sonnet verifier cold on CLOSE. Then it writes `docs/rollout/int/CLOSE.md`:

- landings with sha, deploy id and URL counts;
- returns and why;
- the pages live by type;
- the final production checks and IndexNow responses;
- bundles;
- owner items, including one line telling the owner to resubmit `/sitemap.xml` in Search Console.

It ends with exactly:

```
ROLLOUT INTEGRATOR CLOSE
main <sha> | landings <n> | tranches landed <n>/<tagged> | returned <n>
pages live <n> | new <n> | rebuilt <n> | folded sections <n> | sitemap URLs <n>
deploy <id> | rollback <id> | IndexNow URLs <n> | latest bundle <name>
owner: <one line, or none>
```
