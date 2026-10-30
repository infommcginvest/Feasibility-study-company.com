# FSC-PILOT-1 step zero

Run 2026-10-28 16:50Z to 16:55Z by the FSC-PILOT-1 main thread. Pilot branch `rollout-pilot-1` in `~/Downloads/wt-rollout-pilot-1`, cut from local `main` at `a03f562`. Drafts only: nothing lands, merges, tags, deploys or pushes. No database is involved.

Records read, sha256 as read:

| File | sha256 |
|---|---|
| docs/rollout/ROLLOUT-1.md | 6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034 |
| docs/rollout/AMENDMENT-1.md | 01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49 |
| docs/rollout/int/DECISIONS.md (I1 to I185) | 41bc62e09f68a7d506b118de006d64d2b0e1aac2761df478b1d5def71b03e3a1 |
| docs/rollout/int/SITE-REMAINING-1.md | 4a9cf2b1e77a5ad78dbe274c6982bef385f77e88993be496ae1fdc47c9d72c36 |
| data/site/promised.json | 9720d70f61a0dd00881849ffc6e05e37d3d3760602aec030d38703f14222f085 |

## Probe 1: twin guard (both arms; Claude desktop Electron helpers excluded)

- Process arm: seven Claude Code CLI processes run (pids 28668, 41084, 42815, 43016, 43198, 45851, 89028). `lsof -d cwd` puts every one in one project folder outside Downloads (named for the owner's other property, so ruling 9 keeps its name out of this file), none inside the repo or a worktree. A full `lsof` for paths under the repo, `wt-rollout-*`, `wt-web-fsc-*` and `fsc-rollout` finds one holder only: pid 39621, `com.apple.Virtualization.VirtualMachine` (the desktop app's VM service, started 16:59 CET), not a Claude session. No process carries an FSC path in its argv.
- Transcript arm: of every transcript written in the last 12 hours, one other session's tool calls (command, file_path or path) touch the repo, its worktrees or `fsc-rollout`: `c37e964f`, last written 2026-10-28 09:22 CET, before the Claude app started at 09:25:33 CET. No process now runs from it. The other hits in recent transcripts are memory-index text, not tool calls.
- Montana integration session: `6429060b` (cwd `wt-rollout-int`), last written 2026-10-26 16:53 CET, no live process. Closed.
- Git arm: no `index.lock` in the repo's git dir or any worktree git dir. `rollout-pilot-1` and `~/Downloads/wt-rollout-pilot-1` did not exist before this run.

Result: PASS.

## Probe 2: repo state

- Local `main` = `a03f5624e2b42e7b055ca0693eea1428a83ed147` (2026-10-26 16:42:32 +0100, "INTEGRATOR: FSC-RESUME-1 close (CLOSE-RESUME-1) and the site inventory (SITE-REMAINING-1)"). Not moved.
- Main checkout on `web-fsc-2` at `1d48cc284330272952083fc91119dd22ee66cb57`, re-read after the worktree add: unchanged. Its only untracked entry is `_bundles/`.
- Integrator: `wt-rollout-int` sits at `a03f562` on `rollout-int`, clean, with no live process. No lane holds the integrator. `bus/status/int` still reads "States landed 41 of 42 ... Montana remains" (written 26 Oct 07:09, before I185); stale, superseded by `bus/landed/geo-4-t10` and I185. The pilot does not need it.
- Copy slots (I83 ledger `bus/status/int-copies`): all three were free. This pilot claimed all three at 16:54Z for its three drafts and releases them at close.

Result: PASS.

## Probe 3: live deploy

The recorded deploy is `6adf734229718c46d6ff4aa2` (`bus/landed/geo-4-t10`, I185). Builders never call Netlify (ROLLOUT-1 probe 3), so this was checked by read-only GETs: production and the deploy permalink `6adf734229718c46d6ff4aa2--splendid-cannoli-80c225.netlify.app` return byte-identical `/sitemap.xml` (sha256 prefix 494f97d6842e7f1d), `/` (f801ed7f9be349e9) and `/states/montana/` (c29f10970b9da074). Production `/` returns 200 with H1 "Independent Feasibility Analysis. Institutional Standards."; the sitemap holds 198 `<loc>`. Limit: byte identity with the permalink is strong evidence, not the API's published-deploy field, which this pilot may not read.

Result: PASS.

## Probe 4: disk

Boot disk container free 94.1 GB (94,111,903,744 bytes, 87.6 GiB) against the 60 GiB floor. The three throwaway copies cost 426 MB each.

Result: PASS.

## Measured for step 1 (pick)

- Pending links to unbuilt cases on served HTML in `main`: 10 distinct targets, matching the charter. Two links each: self-storage-bardstown-kentucky-usda, retreat-center-kerhonkson-new-york-usda, marina-gig-harbor-washington-sba. One each: urgent-care-elizabethtown-kentucky-sba, short-term-rental-yucca-valley-california-conventional, self-storage-pataskala-ohio-sba, restaurant-acquisition-broussard-louisiana-sba, hotel-natchitoches-louisiana-eb5, childcare-gonzales-louisiana-sba, assisted-living-elizabethtown-kentucky-bridge.
- Of the ten, only two have a page draft: CASE-1's retreat-center-kerhonkson-new-york-usda (`usda_bi`) and marina-gig-harbor-washington-sba (`sba_504`), each with case.json, facts.md, dnu.txt and page.html (16 Oct). Bardstown, Pataskala and Broussard have facts and pre-counts only; the CASE-3 and CASE-4 drafts folder holds no page. The three CASE-4 targets (bridge, eb5, conventional) need programs the engine on `main` lacks (it supports sba_7a, sba_504, usda_bi, hud_232), so they depend on the CASE-4 engine tranche.
- Hub drafts for skilled-nursing and independent-living-and-ccrc (ASSET-3, 17 Oct). Pre-count: skilled-nursing hub 87, independent-living-and-ccrc hub 45. Both have A and B research runs (asset-3 STEP-ZERO). Review state of either draft: not recorded, so the pilot reviews from scratch.

## Rulings this pilot runs under, and where the charter departs from the rulebook

- The charter lifts I92 for this pilot only.
- Models: the charter sets Sonnet builders and one Opus review per page, Sonnet attackers and a Sonnet verifier. ROLLOUT-1 ruling 15 sets Opus writers, Fable for the hub's SEO finish and Opus attackers. The charter is the owner's direct instruction for this pilot and its subject is measuring a page under that shape, so the pilot follows the charter and records the departure. The main thread runs on Opus 5.5 (`claude-opus-5-5`), not Sonnet as the charter asks: the session model was set before the charter arrived, and that is reported as a departure, not hidden.
- Owner adjustment received mid-run (28 Oct): every asset class hub is a buyer-intent page (title, H1, meta and opening say Feasibility Study Company prepares the studies for owners, developers and their lenders; scope, deliverable, lender fit and how to start near the top; a call to action repeated after the market sections; no fee, turnaround or service promise unless a record states one). This overrides ruling 16's hub title pattern for hubs only. Floors and gates are unchanged.
- Research input: ROLLOUT-1 says write from `~/Downloads/FSC Deep Searches 2/`, but the charter allows only the repo, its `wt-rollout-*` worktrees and `~/Downloads/fsc-rollout`, "nothing else in Downloads". The pilot keeps the charter's fence. Builders and attackers work from the lanes' fact sheets in `fsc-rollout/drafts/` (each figure carries research ID, line, period and source id; each source its publisher, title and URL) and check figures against the cited public source by read-only GET where it answers. No figure is re-derived from a research file itself, and every report says so.
- Drafts only: page sources and case inputs stay in `~/Downloads/fsc-rollout/drafts/pilot-1/` and the throwaway copies. Only records are committed, on `rollout-pilot-1` (A2: a source is committed only after its review is clean, and a commit travels to the public repository in a bundle).
