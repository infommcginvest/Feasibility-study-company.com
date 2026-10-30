# INTEGRATOR step zero, 16 October 2026

- Rulebook `docs/rollout/ROLLOUT-1.md` as read at `fb95856`: sha256 `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (matches the block).
- Amendment `docs/rollout/AMENDMENT-1.md` at `0374505`: sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49`. `origin/main` moved from `fb95856` to `0374505` during step zero; the only commit in between is the coordinator's (author `noreply@feasibility-study-company.com`, subject `Coordinator:`), and it leaves ROLLOUT-1.md byte-identical.

## Probe 1, repo and head
- Local `main` was `2611fc0`. `main..origin/main`: `7ed837f`, `fb95856`, `0374505`, all coordinator commits. No stop.
- Worktree `~/Downloads/wt-rollout-int` cut on `rollout-int` at `origin/main`; local `main` fast-forwarded with `git push . origin/main:main` from the worktree: `2611fc0..0374505`.

## Probe 2, twin guard
- Process arm: no Claude Code CLI process had its working directory in the repo or any worktree (Electron helpers under /Applications/Claude.app excluded; this session excluded).
- Git arm: worktrees present were the repo (`web-fsc-2`), `wt-web-fsc-4`, `wt-web-fsc-5`, `wt-web-fsc-6`. No `index.lock` anywhere; only the zero-byte `stale-index-lock` and `stale-maintenance-lock`, left alone. No `rollout-int` branch or `wt-rollout-int` path existed. No stop.

## Probe 3, Netlify identity
- `getSite` for `0a67950d-6092-49c3-8277-017897c1b865`: custom domain `feasibility-study-company.com`, published deploy `6ad23bed0dd08e20da34458c`, `locked: true` (auto publishing stopped). Rollback point: `6ad23bed0dd08e20da34458c`.

## Probe 4, environment and inputs
- Free disk 35 GB (amendment A3 floor 15 GB).
- python3 3.9 with bs4 4.15.0 and lxml.
- Headless browser: playwright chromium_headless_shell-1234 (the one `shots.mjs` uses).
- Netlify CLI 26.2.0, logged in (getSite answered).
- Research folder `~/Downloads/FSC Deep Searches 2/`: 314 files. The integrator writes no pages from research; builders log theirs.
- macOS has no `timeout`; every subprocess here runs under a perl `alarm` wrapper.

## Gate 8 list
- WEB-FSC-6's list (its `FSC6_DNU`, 349 lines) found at that session's scratchpad `dnu.txt`, copied to `~/Downloads/fsc-rollout/private/dnu-web-fsc-6.txt` (mode 600), then converted to the amendment A1 forms (see FACTORY-2).

## FSC-NIGHT-1 step zero (21 October 2026, 19:30Z; one session runs every lane, owner block of 21 October)
- Charter read in full: `docs/rollout/ROLLOUT-1.md` on main, sha256 `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (421 lines); `docs/rollout/AMENDMENT-1.md` on main, sha256 `01639b33f8b1f242059d284b85b151ac9fccebd7b97817568d0c9a729e22ee49` (109 lines).
- Probe 1, heads (no fetch: no GitHub credential on this Mac, by the owner's block). Local main `60ff2c86bde2`, origin/main `037450597ff3`, rollout-int `ed20d80d5935`, rollout-geo-1 `0104f5219af8`, rollout-geo-2 `72ba97584b3d`, rollout-geo-3 `393d372b62fc`, rollout-asset-1 `1afef3235da4`, rollout-asset-2 `cffb7e337931`, rollout-asset-3 `56bfc14656dd`, rollout-asset-4 `cdbc632e72dd`, rollout-case-1 `df2cd3f1a6cf`, rollout-case-2 `b6dd38aed165`, rollout-case-4 `05665bd3c77f`, rollout-method-1 `f95ed2bedb6f`. All as the owner measured; no unexplained move.
- Probe 2, twin guard. Process arm: no Claude Code CLI process outside /Applications/Claude.app has its cwd in the repo or any wt-rollout-* worktree. Git arm: 16 worktrees as expected (repo on web-fsc-2, eleven rollout lanes, rollout-int, three web-fsc); no index.lock anywhere; the two zero-byte stale lock files stay.
- Probe 3, Netlify: site `0a67950d-6092-49c3-8277-017897c1b865` serves `feasibility-study-company.com`; published deploy `6ad4e606b27f105d4b2b5345` (published 2026-10-18T15:30:18Z), locked. Tonight's rollback point: `6ad4e606b27f105d4b2b5345`.
- Probe 4: boot disk 174 GB free. Tonight's stop is under 70 GB (owner block, replacing the 5 GB stop); at most three throwaway copies at a time.
- The integrator's uncommitted chain output from 18 October (geo-1 t6 pinned to 2026-10-18) was discarded with `git checkout -- .`; the landing is rerun at tonight's deploy date, 2026-10-21, from the merge `ed20d80`.

## FSC-NIGHT-1 resume after the owner's pause and a host reboot (22 October 2026, 05:34Z)
- Boot 05:16Z; the owner paused the night at 20:41Z on 21 October and typed "continue". Step zero rerun before any write.
- Heads: main and rollout-int `4cf7b58`, origin/main `0374505`; lane branches moved only by tonight's records-free merges of main (geo-1 `2e76fbf`, asset-1 `6ffbb32`, asset-2 `45929f2`) and the two derived-block commits (geo-4 `57506c4`, case-3 `5f410db`). No unexplained move.
- Twin guard: no Claude Code process outside /Applications/Claude.app has its cwd in the repo or a worktree; no index.lock.
- Netlify: published `6ad9168af9a3ecb4ba97c9e8` (geo-1-t6, 2026-10-21T19:46Z), locked. Rollback point unchanged since the night began: `6ad4e606b27f105d4b2b5345`.
- Disk 168 GB free. Throwaway copies: asset-1/t1, asset-4/t2, geo-1/t7 (three).
- bus/landed holds geo-1-t6; nothing READY unlanded; no returns. Resumed from bus/status/int.

## FSC-NIGHT-1 second resume (22 October 2026, 07:47Z; host boot 07:44Z)
- Heads unchanged since the last landing (main and rollout-int `b8df84b`); lane branches moved only by the merges of main recorded in their lanes. No live Claude Code process in any worktree; no index.lock; no gate, chain or deploy process running.
- Netlify: published `6ad9a4815b8c0b9d41defedf` (asset-4-t2), locked. Disk 162 GB free.
- Interrupted and rerun: GEO-1 t7's freeze 6 confirming attacker and verifier (no report written); ASSET-2 t1's round 1 fix pass (drafts partly edited, finished from its backups). ASSET-1 t1 was committed and tagged after the reboot (`rollout/asset-1/t1`, `bcdfdbf`).

## FSC-NIGHT-1 third resume (22 October 2026, 08:31Z; owner pause 07:59Z to 08:31Z; host boot 08:17Z)
- Heads: main and rollout-int `22c329e`, origin/main `0374505`; rollout-asset-3 moved to `fbef73a` (its own merge of main, recorded in the lane), rollout-asset-1 `bcdfdbf` (tag t1, landed). No unexplained move. No live Claude Code process in any worktree; no index.lock; no gate or deploy process.
- Netlify: published `6ad9c104c85d1b403684993c` (asset-1-t1), locked. Disk 179 GB free.
- Resumed from bus/status/int: geo-1 t7 (deletion in the draft, freeze 7 next), asset-2 t1 (Fable re-check 2, then I64 and freeze 3), asset-3 t1 (foreman had merged main and begun records).

## FSC-NIGHT-1 fourth resume (22 October 2026, 10:26Z; owner pause 10:19Z to 10:26Z; no reboot)
- Heads: main and rollout-int `47efc21`; lane branches moved only by their own merges of main (geo-1 `10ab1c9`, asset-3 `ba45c38`, asset-4 `5cda5a3`). No live Claude Code process in a worktree, no index.lock, no gate or deploy process. Netlify published `6ad9dc40e6ddc340fb6f4352` (asset-2-t1), locked. Disk 176 GB free.
- Resumed from bus/status/int: asset-3 t1 (minor deletions partly applied since the pre-r3 backup), geo-1 t8 (review round 2 rerun from the start), asset-4 t3 (gate 9 at landing and the Fable SEO job pending).

## Usage-limit stop, 2026-10-22 ~13:25Z (integrator)
main 8bc8d28 (asset-4 t3 landed, deploy 6ada09e1 locked, 187 URLs). Landings tonight 8. Uncommitted in this worktree: DECISIONS I91 and the asset-4 DECISIONS D33 note.
In flight when stopped (their records are on disk; resume from them):
- geo-2 New York: freeze 2 (tmp/geo-2/t2f1, slot 2). Round 2 attackers are done (1 major plus minors each). Verifier running -> drafts/geo-2/reviews/t2-f2-verifier.md. Next: fix round 2 (last), Fable on the CTA and description queue claim, freeze 3, capped confirming review.
- geo-4 California + Sacramento: freeze 2 (tmp/geo-4/t1, slot 3). Round 2 attackers running -> t1-f2-attacker1.md and t1-f2-attacker2.md. Next: verifier, then fix round 2.
- geo-3 Illinois: foreman building freeze 1 (tmp/geo-3/t9, slot 1). Told to reword "carries the refusal into its own downside case". Next: round 1 review.
- geo-1 Oklahoma: SEO re-check 4 on the description (plan matched New York's), running. Waiting for a copy slot to freeze.
At landing, Sacramento needs two integrator inbound links: rv-boat-storage-california-sba "greater Sacramento", and the express-car-wash Sacramento cell.
