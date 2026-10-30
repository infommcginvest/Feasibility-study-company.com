# CASE-NEW-1 step zero

Run 2026-10-29 by the CASE-NEW-1 main thread (Sonnet 5.5). Branch `rollout-case-new-1` in `~/Downloads/wt-rollout-case-new-1`, cut from local `main` at 64d7cc74.

## Probe 1: twin guard (Claude desktop Electron helpers excluded)
- Process arm: 9 Claude Code CLI processes run; `lsof -d cwd` puts each in `~/Downloads/MMCG Analytics Build Up` or `~/.claude/spares/*`, none in the repo, a `wt-rollout-*` or `wt-web-fsc-*` worktree or `fsc-rollout`. `ps` argv grep for the repo, `wt-rollout` and `wt-web-fsc` returns nothing. GEO-5 is paused (`bus/status/geo-5-paused`); the pilot is closed.
- Worktree arm: `wt-rollout-int`, `wt-rollout-geo-5` and `wt-rollout-pilot-1` are clean (0 dirty entries).
Result: PASS.

## Probe 2: repo state
- Local `main` = 64d7cc74 ("INTEGRATOR: GEO-5 records landed; GEO-5 paused after South Dakota (I189)"), 2026-10-28 22:37 +0100.
- Main checkout on `web-fsc-2` at 1d48cc28, unchanged; its only untracked entry is `_bundles/`.
- `bus/status/int`: "integrator free ... GEO-5 holds nothing". `bus/status/int-copies`: slots 1 to 3 free. `wt-rollout-int` at 64d7cc74, clean.
Result: PASS.

## Probe 3: live deploy
- `netlify api getSite` (site 0a67950d-6092-49c3-8277-017897c1b865, read only): published deploy `6ae267122455e19e2b510ea3`, locked, title "rollout geo-5-t3 ee46d2e prod", created 2026-10-28T21:20:18Z. The last recorded deploy (I189) is the same id.
- Byte check, production against the deploy permalink: `/sitemap.xml` 5f8800525eb1372e, `/` 82e7e69b051a59ef, `/states/south-dakota/` 11df61bce164e9a2 (sha256 prefixes) identical on both; sitemap carries 204 `<loc>`.
Result: PASS.

## Probe 4: disk
Boot disk container free 87.1 GB (81.1 GiB) against the 60 GiB floor.
Result: PASS.

## Not recorded / disagreements this lane needs
None found. Note: CASE-3 and CASE-4 lanes left no fact sheets or pre-counts for the CASE-3 cases (their branches hold only step-zero records); the pre-count reads their research files in `~/Downloads/FSC Deep Searches 2/` directly.
