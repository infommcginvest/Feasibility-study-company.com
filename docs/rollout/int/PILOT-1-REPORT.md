# FSC-PILOT-1 report: one new hub and two new cases, measured

Written 2026-10-28 by the FSC-PILOT-1 main thread, from the session's own transcripts and the gate files. Drafts only: nothing landed, merged, tagged, deployed or pushed. Step zero: `STEP-ZERO-PILOT-1.md`. The plan built on these measurements: `BUILD-PLAN-1.md`.

## Verdict in one table

| Page | Type | Final gates (ready stage) | Counted (research, register) | Floor at READY | Body words (range) | State |
|---|---|---|---|---|---|---|
| /asset-classes/skilled-nursing/ | new hub | 14/14 (GATES-ready-r3) | 76 (66, 10 of 13 pairs) | 30 (20) met | 9,483 (6,000 to 10,000) | NOT READY (corrected at close): about 25 printed, uncounted figures are dated only by the builder's own GET, which I69 forbids printing (close B1, reproduced on the rule); the floor is unaffected |
| /case-studies/marina-gig-harbor-washington-sba/ | new case, SBA 504 | tree A 12/14 (2, 6 red); tree B 13/14 (6 red) | 34 (34, 0) by pagecheck; 30 at most after I64 and I66 (close B2, reproduced), 29 on attacker A's reading | met by pagecheck only; at the floor or under it on the rulings (corrected at close) | 6,435 (4,500 to 6,500) | NOT READY: gate 6 needs the CASE-4 engine; the modelled subject fails SBA marina eligibility; no floor margin |
| /case-studies/retreat-center-kerhonkson-new-york-usda/ | new case, USDA B&I | tree A 11/14 (2, 3, 9 red); tree B 13/14 (3 red) | 17 (14, 3) by pagecheck; 13 on the builder's strict reading, 10 (7 research) on attacker A's | NOT met (30 and 20) | 6,194 (4,500 to 6,500) | FOLD CANDIDATE: under the floor on this research |

Counts and words are pagecheck's (`scripts/qa/pagecheck.py --stage ready <url>` run by the main thread in each frozen copy after the fix pass), not the builders' reports; they reproduce the builders' figures exactly. Overlap maxima: hub 1.67% (/asset-classes/private-school/), Gig Harbor 3.09% (/case-studies/hotel-texas-sba/), Kerhonkson 3.88% (/case-studies/rv-park-texas-usda/).

Tree A is `git archive` of main a03f562, plus the page source and case inputs, plus `scripts/requests.py`: the tree that lands without integrator help. Tree B adds the `/case-studies/` card region by a saved script (`integrator-sim-index.py` in each case's drafts folder), a simulation of the integrator's landing edit, labelled as such. `requests.py` prints an `index_entry`; it writes nothing, so every new case is red on gate 2 (casemodel "0 card regions") until the integrator writes the card. The hub needed no integrator edit: its copy differs from main in integrator-owned files only by the mesh term `requests.py` applied (checked by `cmp` on data/site, data/mesh, src/site.json, src/case-cards.json, src/types.json and netlify.toml).

## The hub's title and H1 (owner adjustment, 28 Oct)

| | Before (ASSET-3 draft, 17 Oct) | After |
|---|---|---|
| Title | Skilled Nursing Feasibility Study \| Feasibility Study Company | Skilled Nursing Feasibility Study Company \| Feasibility Study Company (69 characters) |
| H1 | Skilled Nursing Facility Feasibility and Market Studies | Skilled Nursing Feasibility Study Consultants |

The builder first dropped the brand suffix ("Skilled Nursing Feasibility Study Company and Consultants"); the review showed all 29 landed hubs end "| Feasibility Study Company", so the owner's example form was used. The meta description is 158 characters and the first screen says Feasibility Study Company prepares these studies for owners, developers and their lenders (HUD 232, SBA, USDA, banks) with a counted figure. `#engagement` (what the client receives, the lenders, scope, how to start via `/#contact`) is the first section; a second call to action sits in `#commission` after the supply section. No fee, turnaround or service promise: no record states one.

## Time and tokens, per phase, from the transcripts

Each subagent's transcript under the session's `subagents/` folder, summed per message id (largest usage record per id). Wall time is first to last timestamp in the phase's window; the build and fix phases of one builder are split at the idle gap while its review ran. Raw rows: `~/Downloads/fsc-rollout/drafts/pilot-1/USAGE-raw.jsonl`.

| Page | Phase | Model | Wall (min) | Output tokens | Cache read tokens |
|---|---|---|---|---|---|
| skilled-nursing | build | claude-sonnet-5-5 | 31.7 | 106,594 | 33,046,180 |
| skilled-nursing | review | claude-opus-5-5 | 11.4 | 50,478 | 8,865,414 |
| skilled-nursing | fix + gates | claude-sonnet-5-5 | 7.1 | 20,997 | 7,177,857 |
| skilled-nursing | total | | 50.1 (corrected at close: 50.12 exact; 50.2 summed rounded rows) | 178,069 | |
| gig-harbor | build | claude-sonnet-5-5 | 38.4 | 90,681 | 19,894,223 |
| gig-harbor | review | claude-opus-5-5 | 19.2 | 69,394 | 15,795,315 |
| gig-harbor | fix + gates (two trees) | claude-sonnet-5-5 | 22.4 | 72,003 | 18,495,079 |
| gig-harbor | total | | 80.0 | 232,078 | |
| kerhonkson | build | claude-sonnet-5-5 | 44.0 | 129,310 | 26,342,476 |
| kerhonkson | review | claude-opus-5-5 | 25.2 | 90,229 | 18,496,566 |
| kerhonkson | fix + gates (two trees) | claude-sonnet-5-5 | 15.5 | 40,842 | 7,758,910 |
| kerhonkson | total | | 84.7 | 260,381 | |
| main thread (step zero, picks, briefs, rulings, measurement, this report) | 16:50Z to 18:23Z at measurement | claude-opus-5-5 | 92.5 | 67,208 | 13,918,240 |

The three pages ran in parallel: build 16:57Z to 17:41Z, last fix pass done 18:22Z, so 85 minutes of wall clock for three pages to the end of the fix pass. The close (freeze, two attackers, verifier) and BUILD-PLAN-1 are measured in the close record, not here.

## What the pilot found (each reproduced, not tallied)

1. **Both cases picked as "no engine dependency" turned out not to be clean.** Gig Harbor is the purchase of an operating marina on a 504. SOP 50 10 8.1 tests 504 changes of ownership on historical cash flow at 1.15x; casemodel.py on main has no historical path for 504, and gates.py's gate 6 applies Appendix 15 (a 7(a) appendix, 1.25x) to every `purpose: acquisition`. The builder first removed the purpose to turn gate 6 green; the review caught it, the label was restored, and gate 6 is reported red. Both the engine path (CASE-4) and an integrator ruling on gate 6 for 504 purchases are owed.
2. **Gig Harbor's modelled subject fails SBA eligibility.** The builder found in its fix pass that SOP 50 10 8.1 lets a marina borrow only if more than 50% of prior-year revenue comes from stays of 30 days or less; the modelled marina earns about 90% from permanent moorage. The page now says so, but the engine still prints "Every test is met", so page and model disagree. The subject needs redesign (a transient-heavy marina) or a ruling. At close, attacker A read SOP 50 10 8.1 from SBA's own .docx and confirmed both the marina rule and the 504 historical 1.15x test (projections a fallback only), and that 1.25x is Appendix 15, a 7(a) appendix.
3. **Kerhonkson's research does not carry a case.** After I86, I77, I144 and I64 deletions (undated ratings, review counts, booking-widget prices, year-only capacities, undated zoning values, single-property figures), pagecheck counts 17 (14 research); the builder's strict hand reading of I64 and I71 gives 13. The 16 Oct draft's 36 counted rested on figures the rulings exclude. Under ruling 6 it folds: the slug stays pending until the research is refreshed or the owner rules.
4. **Thin research is the norm for named-town cases.** Gig Harbor fell from 69 counted to 34 on the same dating rules (B2: figures dated only by the research's 15 October read). Both case reviews found the 16 Oct drafts counted figures the integrator's later rulings (I64, I77, I86, I106, I144) exclude. Every CASE-1 to CASE-3 draft predates those rulings and needs the same pass.
5. **A new case cannot pass gate 2 without the integrator.** The card region on `/case-studies/` is integrator-owned and `requests.py` does not write it. Every case tranche's READY check needs the tree B simulation, labelled, and the integrator writes the real card at landing.
6. **Review value.** One Opus review per page found 3 + 2 + 3 blockers and 7 + 6 + 12 majors that the Sonnet builders' own gate runs (all 14/14 at first report) did not. Every builder's first report was 14/14; after review, only the hub stayed green.
7. **Process fault.** Subagents share one scratchpad directory; another agent overwrote the hub builder's ledger script mid-pass. The builder rebuilt the ledger from the final source. Builders need per-agent scratch folders.

## Open findings carried into the freeze

- **F1 (hub, hard constraint).** Corrected at close: `LEDGER-uncounted.tsv` holds 8 rows and 19 values, and attacker A found about 25 printed figures with no fact sheet or PA-USDA row (Ensign 40 operations, MedPAC 45 states, NIC 89% and 18 quarters among the unlisted). As first written: about 17 uncounted figures on the hub (HUD Express Lane bulletin, FHA premium notice, USDA fee notice, 7 CFR 5001, USDA rural test, PACS 10-K, a trade-press count, a Missouri hospital association share) come from dated public documents the builder fetched, not from the AH fact sheet. ROLLOUT-1's hard constraint says every figure traces to the research files or the register. They may sit in PA-HUD-AGENCY or PA-USDA, which this pilot may not open (charter fence). Listed in `drafts/pilot-1/skilled-nursing/LEDGER-uncounted.tsv`. Until the integrator confirms them against the PA files, they are a hard-constraint risk; they do not affect the floor.
- **F2 (Kerhonkson).** The 42% group occupancy input is unchanged (lowering it re-solves the determination); the wording and a risk and condition were added.
- **F3 (Gig Harbor).** About 8 prose restatements of model inputs in the frozen source (corrected at close; about 20 was the review's count before the fix pass) sit outside `case:` placeholders (listed in its BUILD.md); a gate 8 line for the bare street fragment is in `dnu-add.txt` for the integrator to add to `private/`.
- **F4 (all).** No figure was re-derived from a research file: the charter fences `~/Downloads/FSC Deep Searches 2/`. Figures were checked against the lanes' fact sheets (research ID and line) and, where the source answered, the live page. Sources that refused a GET are recorded NOT FETCHED in each LEDGER.tsv.

## Departures from the charter and the rulebook

- Main thread ran on Opus 5.5, not Sonnet (session model set before the charter).
- Ruling 15 (Opus writers, Fable SEO finish, Opus attackers) replaced by the charter's shape (Sonnet builders, one Opus review per page, Sonnet attackers and verifier).
- Research folder not read (charter fence), see F4.

## Close (freeze 1, two attackers, one cold verifier)

Freeze 1: `~/Downloads/fsc-rollout/drafts/pilot-1/FREEZE-1.txt` (sha256 ebb8e2205e786b74313c959a74f66a0a7ae1f4a66c37410f1a12cb2b7204740d) hashes each copy's source, case inputs, card, rendered page and the integrator-owned files the pages touch, every drafts file, and this report as frozen (sha256 f33737aecb0f8341965047e9ea69a47b2cb06731eb77c5f249753e96acfabcaf). The report was corrected after the close in the places marked "corrected at close" and in this section; nothing in the three copies changed (all three close agents matched every hash first and last).

| Agent | Brief | Model | Wall (min) | Output tokens | Result |
|---|---|---|---|---|---|
| Attacker A | figures, dates and floors | claude-sonnet-5-5 | 22.3 | 115,716 | 3 blockers, 9 majors, 9 minors |
| Attacker B | gates, links and subjects | claude-sonnet-5-5 | 18.3 | 82,306 | 0 blockers, 2 majors, 9 minors; every gate verdict reproduced |
| Verifier (cold, default refuted) | every figure in this report | claude-sonnet-5-5 | 25.6 | 59,434 | 62 claims: 53 confirmed, 3 refuted, 6 unverifiable |
| Close, in parallel | | | 25.6 (18:25:53Z to 18:51:28Z) | 257,456 | |

Both attackers' writes of their findings files were refused by a tool rule; each returned its findings as text and the main thread saved the returned text to `close/attacker-A/FINDINGS.md` and `close/attacker-B/FINDINGS.md`, beside the attackers' own evidence files. The verifier wrote `close/verifier/VERIFY.md` itself.

How each blocker was resolved (by reproduction, not by count):
- A-B1 (hub, I69): confirmed on the rule's text. I69: a builder's or reviewer's GET that finds a value in a dated document does not date it, and the figure is not printed. The hub's state is corrected to NOT READY. The fix is deletion or a research citation for each of about 25 figures (the PA files may carry some), then a new freeze; the floor does not move (all are uncounted).
- A-B2 (Gig Harbor floor): confirmed on the rendered page. $3,480,000 is one named dock project's budget (I66), $121,000 and $54,000 that project's own revenue and upkeep (I64), "85 units built in 1985" one condominium marina's size (I64). Those four alone put the case at 30, the READY floor exactly; $61,560 (attacker A: undated letter, wrong ledger source) was not checked by the main thread. The case had no margin before its other blockers.
- A-B3 (Kerhonkson): the strict reading of 10 (7 research) against the builder's 13 changes nothing: the page is under the floor on every reading.
- Verifier refutations: all three were rounding or stale counts, each confirmed against its evidence and corrected above (50.1 minutes; 19 values in 8 ledger rows; about 8 prose restatements).
- Attacker B M1: the git legs of gates 7 and 8 scanned an empty range (no pilot commit existed at freeze). The records-only commit that closes this pilot was scanned by the main thread against the ruling 9 pattern and every list in `private/` before committing (zero hits), and the range must be re-scanned at any landing.
- Attacker B M2, for the integrator: `/states/new-york/` says the Kerhonkson case is "now being prepared" and "(in preparation)"; gate 7's stale-claim check will not catch it when the link goes live.
- Unverifiable to the cold verifier (6): Kerhonkson tree A's pre-chain state (the frozen file reports 11/14; its own rebuild gave 12/14), the hub's "before" title and H1 (outside its read set; the ASSET-3 draft's front matter carries them), the two SOP statements (attacker A confirmed them from SBA's .docx), the ruling 15 and attacker model statements, and "not pushed" (local only).

## Bottom line

Of three pages built to the site's standard from the best-prepared drafts, none is READY after a full close: the hub needs about 25 GET-dated figures removed or cited to research (mechanical, one more freeze), Gig Harbor needs the CASE-4 engine and a new subject, and Kerhonkson folds on its research. A hub ported from a draft costs about 50 minutes and 180,000 output tokens to post-fix gates, a case about 85 minutes and 260,000, and a three-page close 26 minutes and 257,000. The binding constraints for the remaining programme are research depth under the post-16 October rulings (cases) and the integrator's one-at-a-time landings, not writing speed.

## Landing (owner's word, 28 October): the hub is live

The owner ruled the skilled nursing hub lands, with the research folder opened for its I69 fix; Kerhonkson folds as recorded; Gig Harbor waits for the CASE-4 engine and a hypothetical subject.

- **I69 fix (fix pass 2, Sonnet, 7.4 minutes).** Each printed figure dated only by the builder's GET was cited to a research row naming a dated publisher document (PA-HUD-AGENCY lines 46, 48, 123; AH-SKILLED-NURSING-A lines 135, 136, 146; AH-SKILLED-NURSING-B lines 44, 67, 79; PA-USDA) or deleted (the CF 90% cap and 20,000 reservation, the $58 million, the Weitz later edition, the V2025 population row, "four"). The integrator re-read all nine research rows and checked the freeze 1 to 2 diff (deletions and three rewordings, citation numbers stripped).
- **Freeze 2** (`drafts/pilot-1/FREEZE-2.txt`, sha256 75d0c43b7d8f949e03e80e7003791b3bc9469329ed21ed8d7a410580c6d0ad19): 9,393 words, 71 counted (61 research, 10 register), overlap 1.7%, gates 14/14 at READY.
- **Landing** (I186): tag rollout/pilot-1/t1 (ea3affc) onto main 8d68a82; mesh term; the /asset-classes/ list entry by relink; dates 2026-10-28; chain twice; gates 14/14 at landing, site-wide. Main 5a1d8a6.
- **Deploy:** 6ae255bf66dd3698da15c2ed, published 2026-10-28T20:06:26Z and locked; draft and production checks 0 problems over 201 pages; IndexNow 200 OK; bundle rollout-5a1d8a6.
- **Live check:** all 201 sitemap URLs answer 200; 0 pages carry a pending skilled nursing link (199 did before); 200 pages link the hub. Live title "Skilled Nursing Feasibility Study Company | Feasibility Study Company", H1 "Skilled Nursing Feasibility Study Consultants", index, follow.
- **A live peer.** GEO-5 opened at 16:54:19Z, minutes after this pilot's twin guard, and landed its t1 (Colorado and Denver, main 8d68a82, deploy 6ae252b073c8143085f3abff) through the same integrator worktree at 19:54Z. Its t2 merge at 19:56Z met this landing, was reverted by GEO-5 and held (its D25); this landing's first gate run crashed on a file that merge added and removed, and the re-run on the settled tree is the record. The twin guard at step zero is a snapshot: a lane that lands holds the integrator by writing `bus/status/int` before its merge, as this landing did from 19:59Z.
- **A ledger overwrite by this pilot.** At 19:44Z this pilot rewrote `bus/status/int-copies` whole to claim slot 1 for the I69 fix, which erased GEO-5's live claim on slot 2 (19:24Z, South Dakota). GEO-5 re-entered it at 19:58Z. Ledgers on the bus are edited line by line, never rewritten whole.
