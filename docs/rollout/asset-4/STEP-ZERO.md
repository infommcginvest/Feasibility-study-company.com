# ASSET-4 step zero

Run 2026-10-16 19:23Z by the ASSET-4 session (Opus).

- Rulebook `docs/rollout/ROLLOUT-1.md` at `fb95856`: sha256 `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (matches the block).
- Amendment `docs/rollout/AMENDMENT-1.md` at `0374505`: sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49`.

## Probe 1, repo and head
- local main `2611fc0`; origin/main `0374505`. main..origin/main holds three commits, all author noreply@feasibility-study-company.com with subject `Coordinator:` (7ed837f, fb95856, 0374505). No stop.
- Cut `rollout-asset-4` from origin/main `0374505` into `~/Downloads/wt-rollout-asset-4`.

## Probe 2, twin guard
- Process arm: no Claude Code process had a cwd inside the repo or any rollout worktree except asset-1's lane (expected).
- Charter-title grep over every transcript: only this session carries the ASSET-4 block.
- Git arm: worktrees main repo (web-fsc-2), wt-rollout-asset-1, wt-web-fsc-4/5/6. No index.lock (only the zero-byte stale-* files). `rollout-asset-4` branch and worktree did not exist. No stop.

## Probe 3, production
- GET https://feasibility-study-company.com/ : HTTP 200, H1 "Independent Feasibility Analysis. Institutional Standards."

## Probe 4, environment and inputs
- Free disk 32 GB (amendment A3 floor 15 GB). python3 with bs4 4.15.0 and lxml. node v24.18.0 for screenshots.

| Research ID | Words |
|---|---|
| AH-MULTIFAMILY-A | 4592 |
| AH-MULTIFAMILY-B | 5759 |
| SD-MULTIFAMILY | 6877 |
| AH-QUICK-SERVICE-RESTAURANT-A | 7184 |
| AH-QUICK-SERVICE-RESTAURANT-B | 6621 |
| SD-QUICK-SERVICE-RESTAURANT | 12433 |
| AH-COFFEE-SHOP-A | 5247 |
| AH-COFFEE-SHOP-B | 6258 |
| SD-COFFEE-SHOP | 7048 |
| AH-RESTAURANT-A | 5421 |
| AH-RESTAURANT-B | 6199 |
| AH-RETAIL-A | 6244 |
| AH-RETAIL-B | 5706 |
| AH-GROCERY-STORE-A | 5719 |
| AH-GROCERY-STORE-B | 6400 |
| AH-LAUNDROMAT-A | 6206 |
| AH-LAUNDROMAT-B | 5517 |
| AH-BUILD-TO-RENT-A | 5530 |
| AH-BUILD-TO-RENT-B | 5816 |
| AH-MANUFACTURED-HOUSING-A | 5471 |
| AH-MANUFACTURED-HOUSING-B | 6364 |
| AH-MIXED-USE-A | 5032 |
| AH-MIXED-USE-B | 6160 |
| AH-MEAT-AND-POULTRY-PROCESSING-A | 5608 |
| AH-MEAT-AND-POULTRY-PROCESSING-B | 5519 |

## Resume, 2026-10-20 (new account; the previous session stopped on 17 Oct when its credit ran out)

- Rulebook and amendment on origin/main: sha256 `6e00a93d...72034` and `01639b33...e22ee49`, unchanged. origin/main `0374505`, local main `60ff2c8`; `main..origin/main` is empty, so nothing was pushed outside this process.
- Twin guard, process arm: no Claude Code CLI process has a cwd inside the repo or a rollout worktree besides this session. Transcript grep for the lane: one other transcript names `wt-rollout-asset-4`, a SITE-BACKUP-1 session listing worktrees, which is not an ASSET-4 peer.
- Twin guard, git arm: 16 worktrees, `rollout-asset-4` held only by `~/Downloads/wt-rollout-asset-4`; no `index.lock` (only the zero-byte stale-* files).
- Production: GET https://feasibility-study-company.com/ returns HTTP 200, H1 "Independent Feasibility Analysis. Institutional Standards."
- Free disk 244 GB; python3 bs4 4.15.0 with lxml; node v24.18.0.
- The bus: no returns for asset-4; `bus/status/int` says the integrator was PAUSED by the owner at 2026-10-18T15:36Z (main `60ff2c8`). READY tranches wait in `bus/ready/` until it resumes.

## FSC-NIGHT-1, 22 Oct (tranche 3, the mixed-use hub)

FSC-NIGHT-1 ran this step (the owner's FSC-NIGHT-1 block, 21 to 22 Oct), as the lane's writer and foreman.

- Rulebook and amendment unchanged: sha256 `6e00a93d...72034` and `01639b33...e22ee49`.
- Branch: `rollout-asset-4` held `23f482e` (t2 commit), and tranche 2 has landed (`bus/landed/asset-4-t2`, main `b8df84b`). Local main stood at `47efc21` (asset-2 t1 landing), which was merged into the branch with the house identity as `5cda5a3`. No returns for asset-4 in `bus/returns/`.
- Host: booted 10:17 local on 22 Oct; 176 GB free on `/`. Git: 18 worktrees, `rollout-asset-4` held only by `~/Downloads/wt-rollout-asset-4`; no `index.lock` (only the zero-byte stale-* files).
- Throwaway copies: the tranche 2 copy `tmp/asset-4/t2` was deleted before tranche 3 began; tranche 3 keeps one copy, `tmp/asset-4/t3`.
- The later no-cite rows waiting in `drafts/asset-4/nocite-later.tsv` (seven rows: the register density unit on five hubs and the 504 program name on two) were appended to `nocite-reviewed.tsv` after the t2 commit, as RESUME.md said.
