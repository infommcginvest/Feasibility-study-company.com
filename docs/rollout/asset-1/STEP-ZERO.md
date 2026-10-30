# ASSET-1 step zero, 2026-10-16

Rulebook: `docs/rollout/ROLLOUT-1.md` read from `origin/main` at `fb9585661f837755ff95b0d8e3fcf98fc996ee29`.
sha256 as read: `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (matches the block). 44,461 bytes.

1. Repo and head. `fetch origin` succeeded on the first try. Local `main` at `2611fc0`. `main..origin/main` holds two commits, both author `noreply@feasibility-study-company.com` with subject `Coordinator:` (`7ed837f`, `fb95856`). No stop. Branch `rollout-asset-1` cut from `origin/main` at `fb95856` into `~/Downloads/wt-rollout-asset-1`.
2. Twin guard. Process arm: no Claude Code CLI process had a cwd inside the repo or any worktree (only this session, which runs from the estate root). Git arm: worktrees were the main repo (`web-fsc-2`), `wt-web-fsc-4`, `wt-web-fsc-5`, `wt-web-fsc-6`; no `index.lock`; the zero-byte `stale-index-lock` and `stale-maintenance-lock` left alone; neither `rollout-asset-1` nor `~/Downloads/wt-rollout-asset-1` existed. A grep of every transcript written in the last two hours for the block's title line found only this session's own. No stop.
3. Production probe (read-only GET): `https://feasibility-study-company.com/` returned 200, H1 "Independent Feasibility Analysis. Institutional Standards."
4. Environment: 35 GB free on the data volume (above 10 GB). python3 with bs4 and lxml present. node present for `shots.mjs`. No database. Every research file in the block found by its Research ID:

| Research ID | Words |
|---|---|
| AH-HOTEL-A | 5,069 |
| AH-HOTEL-B | 6,348 |
| SD-HOTEL | 10,925 |
| AH-RV-PARK-AND-CAMPGROUND-A | 4,645 |
| AH-RV-PARK-AND-CAMPGROUND-B | 7,106 |
| SD-RV-PARK-AND-CAMPGROUND | 8,562 |
| AH-GLAMPING-A | 5,539 |
| AH-GLAMPING-B | 6,707 |
| SD-GLAMPING | 10,984 |
| AH-MARINA-A | 5,519 |
| AH-MARINA-B | 5,921 |
| AH-FITNESS-AND-RECREATION-A | 6,372 |
| AH-FITNESS-AND-RECREATION-B | 5,693 |
| SD-FITNESS-AND-RECREATION | 7,836 |
| AH-SHORT-TERM-RENTAL-A | 5,228 |
| AH-SHORT-TERM-RENTAL-B | 5,394 |
| AH-EVENT-AND-WEDDING-VENUE-A | 5,072 |
| AH-EVENT-AND-WEDDING-VENUE-B | 6,596 |
| AH-BREWERY-AND-DISTILLERY-A | 5,564 |
| AH-BREWERY-AND-DISTILLERY-B | 7,045 |
| AH-WELLNESS-AND-RETREAT-A | 5,514 |

Word counts by `wc -w`. Files located by the Research ID in their first 3,000 bytes, not by file name (several B runs are named "EXTRA 2026-10-1x ...").

## Amendment 1

`docs/rollout/AMENDMENT-1.md` arrived on local `main` and `origin/main` as Coordinator commit `0374505` (author `noreply@feasibility-study-company.com`) after this lane cut its branch. Merged into `rollout-asset-1`. sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49`. Disk at 35 GB clears its 15 GB floor.

## FSC-NIGHT-1 (21 October 2026)

FSC-NIGHT-1, 21 Oct: the integrator session runs this lane's builder work through a subagent under the owner's FSC-NIGHT-1 block (one session, every lane). The night brief is `~/Downloads/fsc-rollout/drafts/NIGHT-BRIEF.md`, outside the repository.

- Heads. `rollout-asset-1` was at `1afef32` (no tag). Local `main` at `4cf7b58` (INTEGRATOR, geo-1 t6 landing). Merged with the house identity as `6ffbb32` ("ASSET-1: merge local main (FSC-NIGHT-1)"); no conflict. Nothing pushed, nothing tagged.
- Rulebook `docs/rollout/ROLLOUT-1.md` sha256 `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (matches the block). Amendment `docs/rollout/AMENDMENT-1.md` sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49` (matches step zero).
- Disk: 177 GB free on the data volume (`df -g /`), above the night's 70 GB stop.
- Throwaway folder `~/Downloads/fsc-rollout/tmp/asset-1/` held only `t0.log` (the integrator deleted the 16 October copy, its I49).
