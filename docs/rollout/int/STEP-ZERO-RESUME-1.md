# STEP ZERO, FSC-RESUME-1 (25 October 2026, about 10:30Z)

Block saved verbatim as `docs/rollout/int/input/RESUME-1.md`. The session's own working directory is the owner's analytics folder, not `~/Downloads/wt-rollout-int` as the block's table says; every write of this session goes to the repo, its worktrees and `~/Downloads/fsc-rollout/` by absolute path, so the difference is recorded and not a stop. Host boot 2026-10-23 19:31Z.

## Hashes (sha256)
- `docs/rollout/int/input/RESUME-1.md`: `0aec17c2abdb99fff2bdf2e5553569d718e4196eecab58c45d56a6f758fca8f5`
- `docs/rollout/ROLLOUT-1.md`: `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (equals the rulebook as committed at `fb95856`)
- `docs/rollout/AMENDMENT-1.md`: `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49` (begins `01639b33`, ends `ee49`)

## 1. Local against GitHub
- `git cat-file -e b2fb289`: present. `git merge-base --is-ancestor b2fb289 main`: true.
- Local `main` is `b2fb289c0d46e5dc8b6a4d388d7900df33542391`. Commits on `main` after `b2fb289`: none. No fetch was made; no credential was looked for.

## 2. Branches and worktrees
`git worktree list --porcelain` lists the main checkout (branch `web-fsc-2`), the fourteen roll-out worktrees and `wt-web-fsc-4`, `wt-web-fsc-5`, `wt-web-fsc-6`.

| Branch | Head | Commits not on main | Uncommitted |
|---|---|---|---|
| rollout-int | `b2fb289` | 0 | none |
| rollout-geo-1 | `d85dd9f` (tag t9, landed) | 0 | none |
| rollout-geo-2 | `1198431` (tag t2, landed) | 0 | none |
| rollout-geo-3 | `2c25abf` (tag t9, landed) | 0 | three untracked items, below |
| rollout-geo-4 | `6e9123d` (tag t1, landed) | 0 | none |

GEO-3's untracked items were the 18 October Iowa tranche 10 gate log (`docs/rollout/geo-3/GATES-t10.txt`, built from `393d372` with Iowa and Des Moines) and two screenshot folders (`look/t9/`, six PNGs of Illinois, Indiana and Wisconsin from 22 October; `look/t10/`, four PNGs of Iowa and Des Moines). Screenshots stay out of the repository (I14, I85) and the gate log predates I55 to I77, so all three moved to `~/Downloads/fsc-rollout/drafts/geo-3/worktree-leftovers-2026-10-25/` with a sha256 manifest (verified after the move). The GEO-3 worktree is now clean. Every GEO worktree exists; none needed recreating.

No `index.lock` in the git dir or any worktree git dir; the two zero-byte `stale-index-lock` and `stale-maintenance-lock` files are left as they are.

## 3. Bus and drafts
- `bus/ready`: 26 tags, every one with a matching `bus/landed` entry (the landed list adds int-factory-2, int-factory-2b, int-detroit-link, int-indy-link). Nothing READY is unlanded.
- `bus/returns`: empty. `bus/status`: `int` only (the FSC-NIGHT-1 close of 22 October, 15:55Z). `bus/requests`: 29 notes, all from 16 to 22 October and all answered or recorded in I1 to I101; nothing open for the integrator.
- `drafts/geo-1`: the night's freezes, backups, reviews, briefs (`tools/WRITER-BRIEF`, `FIX-STATE`, `FIX-METRO`) and the Oklahoma City fold draft; no Arkansas or Mississippi tranche started since 18 October.
- `drafts/geo-2`: the 17 October drafts of the other GEO-2 states, Boston and Montgomery County (pre-I55 to I77, the Texas skeleton per D19), the briefs and tools.
- `drafts/geo-3`: per-state folders; `iowa/` holds the 18 October Iowa and Des Moines drafts (pre-I55 to I77, D28) and the leftovers folder above.
- `drafts/geo-4`: the California freezes and reviews, tools and briefs; no Washington draft.
- O2: `~/Downloads/fsc-rollout/tmp/asset-1/look-t1/` is already absent (a full `find` over `~/Downloads/fsc-rollout` for `look-t1` returns only `tmp/asset-3/look-t1/`, which R7(e) does not name and is left alone). ASSET-1's own folders `look-t1-freeze1/` and `look-t1-freeze5/` remain.

## 4. Twin guard
- Process arm: no process on the machine has its working directory in the repo, a worktree or `~/Downloads/fsc-rollout/` (`lsof -d cwd` over every process, and over every Claude Code process by pid). This session's own process is pid 13709.
- Transcript arm: of the session transcripts written in the last six hours, only this one contains `FSC-RESUME-1`; the others name `wt-rollout-int` only inside a quoted memory note about an earlier twin. No peer.
- Git arm: as in 2. No stop.

## 5. Netlify
`getSite` for `0a67950d-6092-49c3-8277-017897c1b865`: custom domain `feasibility-study-company.com`; published deploy `6ada2f2f573648ac6118bcd7` ("rollout geo-3-t9 a208871 prod", published 2026-10-22T15:43:47Z), locked, so auto publishing is stopped. The rollback point is that deploy. CLI logged in.

## 6. Environment and inputs
- Free disk 76 GB on the data volume. python3 3.9 with bs4 4.15.0 and lxml 6.1.3. Node and the Netlify CLI on the PATH; `scripts/qa/shots.mjs` drives the headless Chrome as at every landing since I43.
- The deploy helper `~/Downloads/fsc-rollout/tmp/int/tools/deploy.py` is present.
- Research, found by Research ID on each file's first line (word counts by `wc -w`):

| State | ST- | words | MT- | words |
|---|---|---|---|---|
| Pennsylvania | ST-PENNSYLVANIA | 7,023 | none (block: no MT file) | |
| New Jersey | ST-NEW-JERSEY | 6,032 | MT-NEW-JERSEY | 7,939 |
| Massachusetts | ST-MASSACHUSETTS | 5,568 | MT-MASSACHUSETTS | 7,430 |
| Maryland | ST-MARYLAND | 6,285 | MT-MARYLAND | 5,566 |
| Connecticut | ST-CONNECTICUT | 6,061 | MT-CONNECTICUT | 8,750 |
| West Virginia | ST-WEST-VIRGINIA | 5,565 | MT-WEST-VIRGINIA | 8,661 |
| New Hampshire | ST-NEW-HAMPSHIRE | 5,546 | MT-NEW-HAMPSHIRE | 8,179 |
| Maine | ST-MAINE | 6,961 | MT-MAINE | 7,574 |
| Rhode Island | ST-RHODE-ISLAND | 5,973 | MT-RHODE-ISLAND | 7,541 |
| Delaware | ST-DELAWARE | 5,556 | MT-DELAWARE | 8,305 |
| Washington | ST-WASHINGTON | 5,264 | MT-WASHINGTON | 8,808 |
| Arizona | ST-ARIZONA | 5,803 | MT-ARIZONA | 8,028 |
| Oregon | ST-OREGON | 5,630 | MT-OREGON | 7,877 |
| Utah | ST-UTAH | 5,348 | MT-UTAH | 5,955 |
| Nevada | ST-NEVADA | 5,736 | MT-NEVADA | 8,218 |
| New Mexico | ST-NEW-MEXICO | 5,300 | MT-NEW-MEXICO | 7,645 |
| Idaho | ST-IDAHO | 5,480 | MT-IDAHO | 6,938 |
| Hawaii | ST-HAWAII | 5,344 | MT-HAWAII | 8,179 |
| Montana | ST-MONTANA | 6,316 | MT-MONTANA | 7,385 |
| Iowa | ST-IOWA | 5,137 | MT-IOWA | 7,860 |
| Arkansas | ST-ARKANSAS | 5,807 | MT-ARKANSAS | 7,763 |
| Mississippi | ST-MISSISSIPPI | 6,210 | MT-MISSISSIPPI | 7,451 |

A first scan that matched the ID only at the very start of the file missed nine of these (a byte before the ID on the first line); the full-text search found every one on line 1. MT-PENNSYLVANIA is absent from all 314 files, as the block says.

## Result
No stop. FSC-RESUME-1 proceeds: R7's close pass and the pre-counts of Pennsylvania, Washington and Iowa.
