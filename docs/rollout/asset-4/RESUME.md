# ASSET-4 resume point (parked by the owner on 20 Oct 2026 until about 22 Oct)

Branch `rollout-asset-4` at local main `60ff2c8` (fast-forwarded on 20 Oct). Tranche 1 (multifamily) has landed. Nothing has been committed for tranche 2 or later. The integrator was paused by the owner at 2026-10-18T15:36Z (`bus/status/int`). There are no returns for this lane in `bus/returns/`.

## Tranche 2 (the quick-service-restaurant hub and burger): frozen, in review

- **Freeze 1, green 14 of 14.** Throwaway copy `~/Downloads/fsc-rollout/tmp/asset-4/t2`, built by `drafts/asset-4/tools/tranche.sh 2`. The hashes are in `drafts/asset-4/t2/FREEZE.txt` and the gate output is in `drafts/asset-4/t2/GATES-t2-freeze1.txt`. The draft tranche record is `drafts/asset-4/t2/t2.md`.
  - Hub: 8,663 body words; 114 counted (107 research, 7 register); overlap 0.89%.
  - Burger: 2,653 body words; 70 counted (70 research); overlap 0.84%.
- **Verifier (Sonnet): closed.** It found blocker 0, major 0, minor 1. The one refuted claim was the wording of the burger stat fix in t2.md, now corrected there and in D16.
- **Attacker one (Opus): five majors, reproduced, not fixed.** Report: `drafts/asset-4/t2/review-a1-r1.md`. Each major has been reproduced against `data/regulatory/sba.json` or the research rows:
  - A1-M1, hub source line 886: the register's 7(a) count is compared with a 722513 tabulation over a different window. The gap comes mostly from FY2016 to FY2019, not from the class definition.
  - A1-M2, hub lines 72, 909, 1041 and burger lines 70, 367: the rule that projections cannot meet the floor is stated without the `dscr.coo_projections` exception (R11) for an owner-occupied special purpose acquisition, and without `valuation.qoe_exempt`.
  - A1-M3, burger lines 366 and 367: "loans numbered from" conflicts with `sop.applies_to` ("applications received by SBA on or after October 1, 2026"). The only research basis for that wording, and for the Franchise Directory carry-forward clause, is a row from a source the rulebook bans. Planned fix: use the sba.json wording, and re-source the Directory rule to the hub's B:Side source or drop the clause.
  - A1-M4, burger lines 62, 317, 326, 327, 388: the Item 7 land and real estate exclusions are stated more firmly than SD rows 64, 67 and 68 support. The 1851 breakdown of Burger King's 2025 Item 7 lists real property and occupancy at $300,000 to $1,500,000.
  - A1-M5, burger line 340: Wendy's is said to have shrunk in 2025, but the 8-K gives a US net gain of 36 in FY2025. It contracted in 2026.
  - The eleven minors (A1-m1 to m11) are listed with their fixes in the report.
- **Attacker two (Opus): report pending.** It was still running at the pause, and `drafts/asset-4/t2/review-a2-r1.md` had not been written. On resume, rerun attacker two on freeze 1 if the report is still absent.
- **Next steps:**
  1. Fix every reproduced finding in the drafts, by exact edits.
  2. Re-run `tranche.sh 2` (freeze 2) and re-review what the fixes touch.
  3. Copy the sources into the worktree, then commit, tag `rollout/asset-4/t2` and write `bus/ready/asset-4-t2`.

## Sweep fixes already applied to later drafts (not yet gated or reviewed)

From the gate 7 and gate 13 patterns seen in tranche 2 (DECISIONS D16). Backups are `drafts/asset-4/<hub>/<hub>.pre-sweep2.html.bak`.

- **mixed-use:** the SOP 50 10 8 sentence reworded so it no longer reads as current (stale-claim scan), and the "708,000 sq ft" stat moved its unit into the label (it pushed the layout to 418 px at 390).
- **retail:** the Byline Bank source date reworded (stale-claim scan), and the 13,331,357 stat shown as 13.33M with the full value in the label.
- **manufactured-housing:** the Coleman-hosted SOP source date and one body sentence reworded (stale-claim scan).
- **No-cite rows:** the rows for the register density unit and the 504 program name on the later hubs wait in `drafts/asset-4/nocite-later.tsv`. Append them after the tranche 2 commit, so the committed list matches the t2 freeze.

## Uncommitted in this worktree (kept on purpose)

These are held back so the tranche 2 commit carries the t2-frozen versions:

- `DECISIONS.md` (D14 to D16)
- `STEP-ZERO.md` (resume probes, 20 Oct)
- `requests.json` (asset-4-7 to asset-4-12)
- `nocite-reviewed.tsv` (the two quick-service-restaurant rows)

## Order after tranche 2 (D15)

mixed-use, build-to-rent, manufactured-housing, meat-and-poultry-processing, retail, laundromat, coffee-shop with franchised-drive-thru, restaurant, grocery-store. A mixed-use pre-check (not a freeze) ran green 12 of 14; its two reds are the ones the sweep above fixes.

## Superseded (FSC-NIGHT-1, 22 Oct)
Tranche 2 was resumed by FSC-NIGHT-1, reviewed in three rounds, fixed, frozen at freeze 4 (green 14/14) and committed with tranches/t2.md (D17 to D21). The next tranche follows D15's order (mixed-use first).

## Tranche 3 (FSC-NIGHT-1, 22 Oct)
The mixed-use hub was reviewed in two full rounds plus a capped confirming review, and frozen at freeze 5 (green 14/14 at READY, gate 9 green at landing). It is committed with tranches/t3.md (D23 to D32) and tagged `rollout/asset-4/t3`. Next in D15's order: build-to-rent.
