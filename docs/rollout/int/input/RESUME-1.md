# FSC-RESUME-1: FINISH THE STATE PROGRAMME ON FEASIBILITY-STUDY-COMPANY.COM

Issued 25 October 2026 by the coordinator for the owner. This block adds an assignment to the roll-out rulebook and changes only the rulings it names in section R. Everything else in `docs/rollout/ROLLOUT-1.md`, `docs/rollout/AMENDMENT-1.md`, `docs/rollout/int/DECISIONS.md` (I1 to I101) and each GEO lane's `DECISIONS.md` and `input/BLOCK.md` stands. Read all of them before step zero.

| | |
|---|---|
| Session | One Claude Code session on the owner's Mac, Opus 5.5, opened in `~/Downloads/wt-rollout-int`. It is the integrator, and it drives the builder work of GEO-1 to GEO-4 itself through subagents. It opens no other Claude Code session. |
| Repo | `~/Downloads/Feaisbility-Study-Company.com` (spelled as on disk), worktrees as in ROLLOUT-1. Shared folder `~/Downloads/fsc-rollout/`. Research `~/Downloads/FSC Deep Searches 2/`, located by Research ID only. |
| Deploy pre-authorized | Yes, production included, by the integrator only, with the deploy helper in `~/Downloads/fsc-rollout/tmp/int/tools/` run as `python3` plus its absolute path and nothing in front (I51). Index all. |
| Pace | Run end to end. Do not ask the owner questions: decide, log, continue. Never end the turn to wait for "continue" while any state, subagent, build, gate, deploy or review is open. |

## Where things stand (measured from GitHub on 25 October)

- **Latest commit.** `b2fb289` (22 Oct, 17:46 +0200, "INTEGRATOR: FSC-NIGHT-1 close (I92)") is the head of the private GitHub repository `feasibility-study-company-site` on the owner's account, pushed 23 Oct at 01:08Z. It is 164 commits ahead of the public repository `Feasibility-study-company.com`, whose head `0374505` is the 16 October amendment commit. The private repository is now the canonical remote. The public one is frozen and receives nothing.
- **Production.** main `a208871` on deploy `6ada2f2f573648ac6118bcd7` (locked), 188 URLs, prodcheck 188/188, problems 0. This is the rollback point.
- **Factory pages live.** 21 states (20 of the 42 lane-assigned states plus Texas), 17 metros, 7 hubs, 3 subtypes, 15 cases. No tranche is in flight. The factory stopped under I92 after Illinois.
- **Open owner items.** O2, O3, O4 and O6 in `docs/rollout/int/OWNER_ITEMS.md`. R7 below settles O2, O3 and O4.

## The job

Land the 22 remaining lane-assigned states with every metro that stands on its own evidence, in I74 population order within each lane, on the metros, research IDs and lane notes already set in each lane's `input/BLOCK.md`.

| Lane | Remaining states, in order |
|---|---|
| GEO-2 (Northeast) | Pennsylvania, New Jersey, Massachusetts, Maryland, Connecticut, West Virginia (new), New Hampshire, Maine, Rhode Island (new), Delaware (new) |
| GEO-4 (West) | Washington, Arizona, Oregon, Utah, Nevada, New Mexico, Idaho (new), Hawaii, Montana (new) |
| GEO-3 (Midwest) | Iowa |
| GEO-1 (South) | Arkansas, Mississippi |

Lane notes that bite here: Pennsylvania has no MT file and pre-counts on ST-PENNSYLVANIA and the register alone; Connecticut's markets are planning regions and `fairfield-county` is not standalone in the register; Arizona's `rural` slug is decided at the pre-count; Hawaii, Idaho and Montana are thin on supply and will fold markets; the Quad Cities and Council Bluffs follow the one-market-two-states rule; the A4 case-town rule applies in every state.

## Step zero (replaces ROLLOUT-1 probes 1 and 3 for this session; probes 2 and 4 stand)

1. **Local versus GitHub.** In the repo: `git cat-file -e b2fb289` succeeds and `git merge-base --is-ancestor b2fb289 main` is true. Record local `main` and every commit on it after `b2fb289` (expected: none). Commits after `b2fb289` by the house identity are carried and listed. Local `main` without `b2fb289`, or a later commit by any other identity, is a stop. Git on this Mac has no GitHub credential: do not look for one, and do not fetch.
2. **Branches and worktrees.** `git worktree list --porcelain`. For `rollout-int` and `rollout-geo-1` to `rollout-geo-4`, record the head, commits not on `main`, and uncommitted changes. Unlanded or uncommitted work is inventoried in the step zero record, then either finished in its tranche or moved to `drafts/<lane>/`. Nothing is discarded without a record. A missing GEO worktree is recreated from local `main` with the ROLLOUT-1 command.
3. **Bus and drafts.** List `bus/ready`, `bus/returns`, `bus/landed`, `bus/status`, `bus/requests` and `drafts/geo-*`, and record anything not landed.
4. **Twin guard,** both arms, as ROLLOUT-1 probe 2. A live Claude Code process in the repo or any worktree other than this session is a stop.
5. **Netlify.** Site `0a67950d-6092-49c3-8277-017897c1b865` serves `feasibility-study-company.com`; the published deploy is `6ada2f2f573648ac6118bcd7`, locked, auto publishing stopped. Any other published deploy is a stop.
6. **Environment and inputs.** Free disk at least 15 GB; python3 with bs4 and lxml; the headless browser; the Netlify CLI logged in; the deploy helper present at its absolute path; the ST- file for each of the 22 states and every MT- file their blocks name, found by Research ID and word-counted.
7. **Record.** Save this block verbatim to `docs/rollout/int/input/RESUME-1.md`. Record the sha256 of it, of ROLLOUT-1.md and of AMENDMENT-1.md, with the probe results, in `docs/rollout/int/STEP-ZERO-RESUME-1.md`. Commit both with the house identity.

## R. Rulings this block makes (log them in `docs/rollout/int/DECISIONS.md` as I102 onward)

- **R1. Geography resumes.** I92's stop is lifted for states only. I74, I75 and I76 govern again for the 22 states above. No hub, subtype, case, practice-area or METHOD-1 tranche starts in this session.
- **R2. One session, four lanes.** This session drives GEO-1 to GEO-4 in their own worktrees and branches. Builder commits are made in the lane's worktree with the house identity and touch only that lane's owned paths; records go in `docs/rollout/<lane>/`; tranche numbers continue from each lane's last. Lane ownership of integrator files (ruling 1) is unchanged: the lanes write requests, the integrator applies them.
- **R3. Concurrency.** At most three states in flight, five subagents at once and three throwaway copies (I75, I83). States in flight together sit in different regions and never border each other (I74). Open with Pennsylvania (GEO-2), Washington (GEO-4) and Iowa (GEO-3); Arkansas then Mississippi take the third slot after Iowa. When GEO-1 and GEO-3 are empty, Maryland, West Virginia and Delaware transfer from GEO-2 to GEO-1 (recorded in both lanes' DECISIONS and owned-paths lists) and take the third slot, still under the no-border rule. If no queued state clears the no-border rule, the slot waits for the next landing.
- **R4. Review economy, now standing.** Per state: freeze 1 and one round of two Opus attackers and one cold Sonnet verifier (ruling 17, A2). Fix blockers and factual majors. A fix made only of deletions, nocount wrapping or verbatim source restoration is confirmed by the integrator diff check (I79, I94); any other fix gets one capped confirming review (I68). No third round anywhere. Non-factual majors and minors are recorded in the tranche record. The I74 cross-lane sameness guard runs before READY against every landed page and every draft in flight, and the I81, I84 and I88 rulings on shared construction apply.
- **R5. Models.** Sonnet 5.5 for research readers, fact sheets, pre-counts, verifiers, gate runs, tool fixes and every line of code. Opus 5.5 for writers and attackers. Fable for the first-screen SEO finish of state and metro pages only (title, meta description, H1, first screen, FAQ), under ruling 16 and the I81 and I89 caps.
- **R6. Landing.** One tranche at a time, taken as soon as it is READY, with no fixed polling interval and one status line per change: "states landed N of 42; metros landed N". Everything else in ruling 14 and A2 is unchanged: merge, requests, date pinning, chain, gates 1 to 14 on the tranche's diff-derived page set and gates 3, 4, 9 and 10 site-wide, the floor check of landed pages (A4), commit and fast-forward `main`, draft then production deploy with the helper, lock, production checks, IndexNow, bundle, `bus/landed`. Each landing updates `/states/`, the home page counts and the stale-claim grep.
- **R7. Close pass first.** The integrator runs it while the first three states pre-count, and lands it as one tranche tagged `rollout/int/close-1`:
  - (a) **O4, North Carolina.** Delete the SBA Ledger FY2025 combined total from `/states/north-carolina/` (I87).
  - (b) **O4, fetch-dated figures.** A Sonnet reader per factory page landed before I69 (the 18 October landings, Alabama, the quick-service restaurant hub and its burger subtype, the hotel hub, Kentucky) lists every figure dated only by a fetch or retrieval date. Each is fixed by deletion or nocount (I79) and confirmed by the diff check. A page that falls under its landing floor stays live and is listed for its lane's next pass.
  - (c) **O4, pagecheck.** In `scripts/qa/pagecheck.py`: honour `data-fsc-nocount` on `mkt:` regions; fix the two-digit rounding in the repeat test; stop counting statute section numbers as figures; count values that sit only in another page's sources list (I71). Rerun it on every landed page and record the counts before and after.
  - (d) **O3, Connecticut.** Bring `/case-studies/private-school-connecticut-conventional/` into line with its own disclosure by deleting, or minimally rewording, the three passages that claim an engagement (the "standing analyses" and "the firm's analysis" source wording, and "surveyed for the engagement" in the competitor table). Its full rebuild stays with CASE-4.
  - (e) **O2.** Delete `~/Downloads/fsc-rollout/tmp/asset-1/look-t1/` (A3: the roll-out's tmp folders are its own to delete).
  - (f) **O6** stays as recorded. The repository is private, and history is not rewritten.
- **R8. Remote.** Nothing is pushed from the Mac. At close the integrator writes `_bundles/resume-<main sha>.bundle` covering `b2fb289..main`, verifies it, keeps the newest five bundles, and reports the path. The coordinator pushes it to the private repository.
- **R9. Stops and thin states.** The only stops are ROLLOUT-1's (a step zero stop, a red gate the session cannot fix in scope, free disk under 5 GB) and a message from the owner. Metros under the pre-count floor fold into their state (ruling 6, A6). A rebuilt state that cannot reach its landing floor stays live as it is and is recorded; a new state that cannot reach it is not shipped and is recorded. Nothing ships thin.

## Close

When all 22 states have landed or been recorded under R9, write `docs/rollout/int/CLOSE-RESUME-1.md`: each state with its lane, tag, main sha, deploy id and URL count; metros shipped and folded with their counts; counted figures (research and register) and maximum overlap with the page it is against; review findings and their resolution; the R7 results; and the owner items still open. Land it as the last records tranche, write the bundle, and end the turn with exactly:

```
FSC-RESUME-1 CLOSE
main <sha> | deploy <id> | URLs <n> | bundle <path>
states landed <n>/22 | metros landed <n> | metros folded <n> | states recorded under R9 <n>
close pass: NC total deleted <y/n> | fetch-dated figures fixed <n> | pagecheck fixes <n>/4 | CT case aligned <y/n>
gates 14/14 site-wide at last landing <y/n> | open owner items <list>
```
