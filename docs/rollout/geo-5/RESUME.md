# GEO-5 resume point (30 October 2026, CLOUD-1; parked by the owner)

GEO-5 is parked by owner amendment 2 to FSC-CLOUD-1 (30 Oct): states stop, cases and the asset-class buyer-intent retrofit go first. Nothing is in flight: the three Track A agents still running at the amendment (the District and Vermont verifiers, the North Dakota and Alaska capped review) were stopped before writing. Branch `cloud/geo-5` (pushed, no pull request) holds every record below; no page source is under `src/pages/`, because no state has finished its review (A2). Decisions D29 to D33.

## Where each state stands

| State | Stage reached | Counted at the last gate run (cloud) | Exactly what is left |
|---|---|---|---|
| North Dakota (t4) | Mac freeze 1 and both attacker files (28 Oct). CLOUD-1: cold Sonnet verifier done (`cloud-1/reviews/t4-f1-verifier.md`): 22 confirmed (BLOCKER 0, MAJOR-FACTUAL 6, MAJOR-NONFACTUAL 7, MINOR 9), 12 refuted, A1-1 (the one blocker as filed) among them as not reproduced. Its 43 edits plus the D31 precaution are applied in `cloud-1/candidates/north-dakota.f2-candidate.html` (diff `north-dakota.f1-f2.diff`). | 64 (56 research, 8 register), READY gates 14/14 on the candidate (`cloud-1/gates/GATES-f2-north-dakota.txt`) | 1. Capped Opus review of the NON-DELETION edits listed in the verifier file (not done). 2. A networked check of A1-2 ("for July", 24 rigs) and A1-3 ("in June 2026", 3,040 wells) against the Minot Daily News article, and A1-4's Fargo permit clause (281, "peak month") against its article. 3. Freeze 2, gates, copy the candidate to `src/pages/states/north-dakota.html`, tranche record, commit, land. |
| Alaska (t5) | Mac freeze 1 and both attacker files. CLOUD-1: cold verifier done (`t5-f1-verifier.md`): 20 confirmed (BLOCKER 0, MAJOR-FACTUAL 7, MAJOR-NONFACTUAL 7, MINOR 6), 15 refuted (A1-3, A1-4, A1-5 not reproduced). 34 edits plus the D31 precautions applied, source 5 dropped and citations renumbered (`alaska.f2-candidate.html`). Inbound link fix: `patches/alaska_links.py` (D32). | 66 (61 research, 5 register), READY gates 14/14 with the patch applied | 1. Capped Opus review of the nine NON-DELETION edits and of the renumbering (not done). 2. A networked check of A1-3 (fiscal 2027 mining revenue, one counted figure). 3. Freeze 2, gates, source to `src/pages/states/alaska.html`, record, commit, land with the patch. |
| District of Columbia (t7) | CLOUD-1 freeze 1 (`cloud-1/freeze/FREEZE-district-of-columbia-f1.txt`; source = the handoff draft). Attacker A (`t7-f1-attacker1.md`): BLOCKER 0, MAJOR-FACTUAL 4, MINOR 7. Attacker B (`t7-f1-attacker2.md`): BLOCKER 0, MAJOR-FACTUAL 4, MAJOR-NONFACTUAL 10, MINOR 10, among them mesh links to Maine and Connecticut on "Maine Avenue SW" and "Connecticut Avenue NW". No verifier output. | 56 (48 research, 8 register), READY 14/14 (`GATES-f1-district-of-columbia.txt`, gate 13 in `-g13.txt`); attacker A expects 53 (45) after its fixes | 1. Cold Sonnet verifier on both files (brief: handoff `REVIEW-BRIEF.md` with `cloud-1/reviews/CLOUD-PATHS.md`). 2. Fixes, capped review, freeze 2, gates, record, commit, land. |
| Vermont (t8) | CLOUD-1 freeze 1 (`FREEZE-vermont-f1.txt`). Attacker A: BLOCKER 0, MAJOR-FACTUAL 3, MINOR 9. Attacker B: BLOCKER 0, MAJOR-FACTUAL 4, MAJOR-NONFACTUAL 11, MINOR 8, among them the keyword forms "consultant" and "company" appearing only low on the page, and a mesh link to Connecticut on "Connecticut Public". No verifier output. | 77 (69 research, 8 register), READY 14/14; both attackers expect 77 after their fixes | As the District. |
| Wyoming (t6) | Drafted and SEO-finished (handoff), not frozen. | draftcheck 113 (Mac) | Waits for the vote of 3 November 2026: refresh the closing band to cite the result, then the full close. A session reminder is scheduled for 4 Nov 15:07Z; it does nothing unless the owner reopens the track. |

Order when the track reopens: North Dakota, Alaska, the District, Vermont, then Wyoming after the vote.

## How to resume in a cloud session
1. Network: the attackers and verifiers need the source hosts (D30). Check with one GET to a government host before starting.
2. Build a copy: `docs/rollout/geo-5/cloud-1/mkcopy.sh <copy> <worktree> <candidate>=src/pages/states/<state>.html` (env `PATCHES` for `patches/alaska_links.py`), then from inside the copy `python3 scripts/qa/gates.py --root . --git-dir <worktree> --urls /states/<state>/ --new /states/<state>/ --stage ready --range origin/main..HEAD`. Gate 13 needs a headless Chromium at the path `scripts/qa/shots.mjs` names.
3. Apply a verifier's fix list with `cloud-1/apply_edits.py`; drop an orphaned source with `cloud-1/dropsource.py` (it keeps the front matter's indentation and renumbers every citation).
4. On the Mac: the handoff tools (`docs/rollout/cloud-handoff/geo-5/tools/`) and the landing procedure in the earlier resume point below still apply; take the candidates from `cloud-1/candidates/`.

## Earlier resume point (28 October 2026, kept for the landing procedure)


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
