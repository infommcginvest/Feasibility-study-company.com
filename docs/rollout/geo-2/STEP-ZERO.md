# GEO-2 step zero, 2026-10-16

## Rulebook

- `docs/rollout/ROLLOUT-1.md` sha256 `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (matches the block; read in full with the Read tool, 422 lines, 44,461 bytes).
- `docs/rollout/AMENDMENT-1.md` sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49` (read in full; overrides ROLLOUT-1 where they differ).

## Probe 1: repo and head

- `git fetch origin` succeeded on the first try.
- Local `main` and `origin/main` both at `037450597ff3dda91551ec1fc80afa2219e26fa1` (the integrator had already fast-forwarded).
- Commits on `origin/main` since `2611fc0`: `7ed837f`, `fb95856`, `0374505`, all author `noreply@feasibility-study-company.com`, all subjects starting `Coordinator:`. No stop.
- Worktree cut: `git worktree add -b rollout-geo-2 ~/Downloads/wt-rollout-geo-2 origin/main` at `0374505`.

## Probe 2: twin guard

- Git arm: before the cut, `git worktree list --porcelain` showed the main repo (branch `web-fsc-2`), `wt-rollout-asset-1`, `asset-2`, `case-1`, `case-2`, `int`, and three `wt-web-fsc-*` worktrees. No `rollout-geo-2` branch, no `wt-rollout-geo-2` path, no `index.lock`.
- Process arm: no Claude Code process had a working directory in `wt-rollout-geo-2`.
- Transcript arm (house rule: grep the charter title, not the lane name): two transcripts held `ROLLOUT GEO-2: THE NORTHEAST`. One is this session. The other is the METHOD-1 session, whose own prompt is the METHOD-1 charter and whose grep tool output quoted this block. No live GEO-2 peer.

## Probe 3: production

- `GET https://feasibility-study-company.com/` returned 200, H1 "Independent Feasibility Analysis. Institutional Standards."

## Probe 4: environment and inputs

- Free disk on the data volume: 32 GB (Amendment 1 A3 needs 15 GB).
- python3 with bs4 4.15.0 and lxml.
- node and npx present for the headless browser (`docs/web-fsc-6/tools/shots.mjs`).
- Research folder `~/Downloads/FSC Deep Searches 2/`: 314 files. Located by Research ID in the first 3,000 bytes:

| Research ID | Words |
|---|---|
| ST-NEW-YORK | 5,684 |
| MT-NEW-YORK | 8,019 |
| ST-PENNSYLVANIA | 7,023 |
| MT-PENNSYLVANIA | not present (as the block says) |
| ST-NEW-JERSEY | 6,032 |
| MT-NEW-JERSEY | 7,939 |
| ST-MASSACHUSETTS | 5,568 |
| MT-MASSACHUSETTS | 7,430 |
| ST-MARYLAND | 6,285 |
| MT-MARYLAND | 5,566 |
| ST-CONNECTICUT | 6,061 |
| MT-CONNECTICUT | 8,750 |
| ST-NEW-HAMPSHIRE | 5,546 |
| MT-NEW-HAMPSHIRE | 8,179 |
| ST-MAINE | 6,961 |
| MT-MAINE | 7,574 |
| ST-DELAWARE | 5,556 |
| MT-DELAWARE | 8,305 |
| ST-RHODE-ISLAND | 5,973 |
| MT-RHODE-ISLAND | 7,541 |
| ST-WEST-VIRGINIA | 5,565 |
| MT-WEST-VIRGINIA | 8,661 |

## FSC-NIGHT-1 (22 October 2026, New York tranche)

Run by FSC-NIGHT-1, 21 Oct block, under the owner's geography-first steering of 22 October (integrator I74, I75).

- Brief: `~/Downloads/fsc-rollout/drafts/NIGHT-BRIEF.md` read in full, with integrator rulings I55 to I75 in `wt-rollout-int/docs/rollout/int/DECISIONS.md`, GEO-1's Kentucky record (`tranches/t7.md`) and the Louisiana night reviews (`drafts/geo-1/reviews/t8-*-night*.md`), and GEO-1's FIX-STATE list for the sameness classes those reviews name.
- Branch: `rollout-geo-2` was at `72ba975`. Local `main` `94a1cb6` (120 commits ahead of the lane base, none touching `docs/rollout/geo-2/`) merged with the house identity as `86784a7`. The uncommitted D8 to D14 in DECISIONS.md and the untracked `nocite-reviewed.tsv` and `requests.json` were carried through the merge untouched.
- Throwaway folder: the old copies `1` and `2` were already gone; only their logs and screenshots remained. One copy, `~/Downloads/fsc-rollout/tmp/geo-2/3`, was built from `86784a7`.
- Disk: 175 GB free at the start, 163 GB after the copy (night floor 70 GB).
- Research: ST-NEW-YORK (217 lines) and MT-NEW-YORK (555 lines) read in full; the Saratoga Springs and Kerhonkson case research files located for the A4 check.
- Not done here: no commit of page sources, no tag (A2). STEP-ZERO.md, DECISIONS.md, FOLDED.md and the tranche record stay uncommitted for the integrator.
