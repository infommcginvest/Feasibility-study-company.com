# ASSET-2 step zero (2026-10-16)

- Rulebook `docs/rollout/ROLLOUT-1.md` as read from `origin/main` after fetch: sha256 `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (matches the block).
- Amendment `docs/rollout/AMENDMENT-1.md` (Coordinator commit `0374505`, arrived on origin/main during step zero): sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49`.

## Probe 1, repo and head
- Local `main` `2611fc0`. `origin/main` `0374505`. `main..origin/main` holds only `7ed837f`, `fb95856`, `0374505`, each authored `noreply@feasibility-study-company.com` with subject `Coordinator:`. No stop.
- Branch `rollout-asset-2` cut from `origin/main` at `0374505` into `~/Downloads/wt-rollout-asset-2`.

## Probe 2, twin guard
- Process arm: no Claude Code CLI process outside /Applications/Claude.app has a cwd inside the repo or a rollout worktree holding asset-2.
- Transcript arm: the charter title line occurs in this session's transcript only.
- Git arm: worktrees before the cut were the main checkout, wt-rollout-asset-1, wt-web-fsc-4, -5, -6. No `index.lock`; only the zero-byte stale-index-lock and stale-maintenance-lock (left alone). Branch `rollout-asset-2` and the worktree path did not exist.

## Probe 3, production
- GET https://feasibility-study-company.com/ returned 200, H1 "Independent Feasibility Analysis. Institutional Standards."

## Probe 4, environment
- Free disk 35 GiB on the data volume (amendment A3 floor 15 GB).
- python3 with bs4 4.15.0 and lxml.
- Research files located by Research ID: see `RESEARCH.md`.

## FSC-NIGHT-1 (21 and 22 October 2026; FSC-NIGHT-1 ran it)
- Charter: `~/Downloads/fsc-rollout/drafts/NIGHT-BRIEF.md` read in full; ROLLOUT-1 and AMENDMENT-1 as in this worktree; integrator REQUESTS.md (requests.json format) and DECISIONS I1 to I58 read.
- 21 Oct: local `main` `4cf7b58` merged into `rollout-asset-2` as `45929f2` (house identity). Free disk 177 GB (floor 70 GB). The self-storage fact sheet and pre-count (`drafts/asset-2/facts/self-storage.counted.json`, FOLDED.md) were present, so no reader job was needed. Parked at about 20:00Z on owner steering (integrator I53) with `drafts/asset-2/RESUME-night.md`.
- 22 Oct, resume after a host reboot (boot 07:16 local): free disk 167 GB; no Claude Code process had its working directory in this worktree or the main repo; no `index.lock` in the repo git dir or this worktree's git dir; worktree clean except the uncommitted `requests.json`. Local `main` `b8df84b` (ASSET-4 t2 landing) merged as `7c57c24` (house identity).
- One throwaway copy at a time: `~/Downloads/fsc-rollout/tmp/asset-2/t1` (deleted on 21 Oct at the park, rebuilt on 22 Oct from `git archive HEAD` at `7c57c24`).
