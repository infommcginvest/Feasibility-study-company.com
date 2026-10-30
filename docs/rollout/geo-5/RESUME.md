# GEO-5 resume point (28 October 2026, about 21:30Z)

GEO-5 is paused after South Dakota, before North Dakota. Nothing is in flight: no subagent, copy build, gate run, landing or deploy is running. The integrator (`~/Downloads/wt-rollout-int`) is free and equal to local main; `bus/status/int` says so.

## Where the site stands
- Local main `ee46d2e` (INT I188). Live deploy `6ae267122455e19e2b510ea3` (published, locked), 204 sitemap URLs. Bundles in `<repo>/_bundles/`, newest `rollout-ee46d2e9.bundle` (verified; not pushed: the coordinator pushes). `origin/main` is still `0374505`.
- Landed by GEO-5: geo-5 t1 Colorado and Denver (INT I186; deploy `6ae252b0...`), geo-5 t2 Virginia and Northern Virginia (I187; `6ae2629a...`), geo-5 t3 South Dakota (I188; `6ae26712...`). FSC-PILOT-1 landed pilot-1 t1 (skilled nursing hub) between t1 and t2 (its own I186).
- Each new URL was checked on the deployed site after its landing: 200, its H1, `index, follow`, in the live sitemap with lastmod 2026-10-28; no landed page under its floor at any landing (gate 3 site-wide, gate 9: none under 3 inbound).

## The five states not landed
Every page source is drafted and SEO-finished in `~/Downloads/fsc-rollout/drafts/geo-5/pages/<state>.html`; research in the inventory (D22) and in `drafts/geo-5/research/`; pre-counts in `drafts/geo-5/facts/`. Requests for all five are already on main (geo-5-11 to 23: chrome items hidden until live, `/states/` index lines, mesh terms "North Dakota", "Alaska", "District of Columbia", which link nothing until their pages exist).

| State | Stage | Counted at the last gate run | Next step |
|---|---|---|---|
| North Dakota (t4) | Freeze 1 done (`FREEZE-t4-f1.txt`; gates 14/14 at READY and 3, 9 green at landing on main `24aa91e`). Both attackers finished: `reviews/t4-f1-attacker1.md` (1 blocker: a "two-year" moratorium the article does not state; 3 factual majors; 6 minors) and `t4-f1-attacker2.md` (0 blockers; 5 factual majors, among them "rather than owners" for FEMA Public Assistance, which also funds private nonprofits, and the Montana link earned by no fact; 8 non-factual majors; 11 minors). | 64 (56 research, 8 register) | Cold Sonnet verifier on both findings files (`REVIEW-BRIEF.md`), apply its fix list, capped review of word-changing edits, rebuild the copy on current main (`mkcopy5.sh`), freeze 2, tranche record, commit, tag `rollout/geo-5/t4`, land. |
| Alaska (t5) | Freeze 1 done (`FREEZE-t5-f1.txt`). Both attackers finished: `reviews/t5-f1-attacker1.md` (0 blockers; 9 factual majors, among them an uncited explanation of the two September job readings, a superseded DOLWD vintage beside the current one (ruling 10), "Alaska Economy at a Glance" not being the BLS page's title (I176), a cargo comparison in words) and `t5-f1-attacker2.md` (0 blockers; 4 factual majors; 11 non-factual majors; 7 minors). | 71 (66 research, 5 register); attacker one expects 65 or 66 after its fixes | First fix the inbound links (A2-1): the "Alaska" mesh term lands on "Alaska Native Corporations" on `/research-notes/usda-rd-deadline-calendar/`, so only two real inbound links exist and gate 9 fails at landing. Either a term exclusion in `scripts/mesh.py` (an integrator change: no other page's output may move) or one link added by hand to a live page that mentions the state (the gas station hub and research note mention it but sit at mesh's 15-term cap). Then the verifier, fixes, capped review, freeze 2, land. |
| District of Columbia (t7) | Drafted and SEO-finished; not frozen. Pre-count 46 research (40 or more after any single family removed; 15 on the harshest stack). | draftcheck 50 | Claim a slot, build the copy, gates (gate 9 relies on the "District of Columbia" term plus Maryland and Virginia), freeze 1, two attackers, verifier, fixes, freeze 2, land. Its Washington metro section must keep printing no Virginia county figure. |
| Wyoming (t6) | Drafted and SEO-finished; not frozen. Pre-count after its supplement 99 research (45 without secondary and borderline). | draftcheck 113 (92 research by the writer's count) | As the District. Refresh the closing band after the Proposition 1 vote of November 3, 2026 (it stays true either way, but reads better with the result). |
| Vermont (t8) | Drafted and SEO-finished; not frozen. Pre-count after its supplement 72 research (21 on the harshest stack). | draftcheck 72 | As the District. |

D5's order holds for what is left: North Dakota, Alaska, Wyoming, the District of Columbia, Vermont.

## How to resume
1. Step zero again (twin guard both arms, main head, live deploy against `6ae26712...`, disk against 60 GiB). Check that no other session holds `wt-rollout-int` and that `bus/status/int` says it is free; mark it before each landing and free it after (D25, D26: FSC-PILOT-1 landed in the same worktree once without notice).
2. Merge local main into `rollout-geo-5` before any freeze 2.
3. The tools are in `~/Downloads/fsc-rollout/drafts/geo-5/tools/` (`mkcopy5.sh`, `land5.py`, `neighbors5.py`, `yield5.py`, `assign_pc.py`, `inventory5.py`, `draftcheck.py`, `sameness.py`, `to`); the briefs are `RESEARCH-BRIEF.md`, `PRECOUNT-BRIEF.md`, `WRITER-BRIEF.md`, `SEO-BRIEF.md`, `REVIEW-BRIEF.md` in the same folder. The deploy helper is `~/Downloads/fsc-rollout/tmp/int/tools/deploy.py`, run as `python3` plus its absolute path and nothing in front (I51), with `--since` the previous landed main.
4. Home-list positions used so far: Colorado after Wisconsin, Virginia after Michigan, South Dakota after Nebraska; place each new state near its population (`land5.py --after-home`).
5. After the last landing: the close round (freeze and hash research, pages and gate outputs with the deploy ids; two Sonnet attackers, A on figures, dates, floors and research hygiene, B on gates, links and buyer-intent claims; one cold Sonnet verifier re-deriving every CLOSE figure), `CLOSE.md`, and the resume bundle as RES R8 did.

## Owner items
- D9: three FSC-RESUME-1 commits on main (`b5ad494`, `0310699`, `a03f562`) are authored with the sister firm's domain; decide before the coordinator pushes.
- INT DECISIONS carries two I186 entries (GEO-5 t1 and pilot-1 t1), side by side.
- Wyoming's closing band ties the property tax line to the November 3 vote.

## Search Console (request indexing by hand)
- https://feasibility-study-company.com/states/colorado/
- https://feasibility-study-company.com/states/colorado/denver/
- https://feasibility-study-company.com/states/virginia/
- https://feasibility-study-company.com/states/virginia/northern-virginia/
- https://feasibility-study-company.com/states/south-dakota/
