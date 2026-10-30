# Owner items (integrator; FSC-NIGHT-1 and later)

## O1. Production publishing refused by the permission classifier (21 October 2026, about 19:39Z)

The FSC-NIGHT-1 block authorises production deploys for every green landing, but in this session Claude Code's auto-mode permission classifier refused the deploy helper's production step. The session does not work around a refusal. Until the owner decides, each landing stops after its draft deploy and draft checks: gated 14/14, committed and fast-forwarded on local `main`, a draft deploy of that `main` checked. `bus/landed/` is not written for it, because a landing counts only with its production deploy id. Production stays on deploy `6ad4e606b27f105d4b2b5345` (locked), the rollback point.

Landings waiting for the owner's publish decision:
- geo-1-t6 (Alabama, Huntsville): main `4cf7b58`, draft `6ad914414334be22e2cb686e` checked 183/183 pages, 0 problems.
- Resolved 2026-10-21T19:48Z: on the owner's instruction (20:00Z message) the deploy helper ran from `--step prod` by its absolute path and went through: geo-1-t6 published as deploy `6ad9168af9a3ecb4ba97c9e8` (locked), production checks 183/183 pages, 0 problems, IndexNow 200 (184 URLs since `60ff2c8`), bundle `rollout-4cf7b58.bundle`. Landings publish all night from here.

## O2. A screenshot folder left in place (21 October 2026, about 20:20Z)
ASSET-1's builder was refused by its permission check when it tried to delete an older screenshot folder, `~/Downloads/fsc-rollout/tmp/asset-1/look-t1/`, from before tonight's freeze. The integrator does not delete it on the builder's behalf. It holds only public page images and costs little disk, so it can be removed at close or by the owner.

## O3. A served legacy case contradicts its disclosure (22 October 2026, about 09:20Z)
`/case-studies/private-school-connecticut-conventional/` (hand-built before the roll-out) says it "is not a client engagement" while its sources cite "our standing ... analyses" and "the firm's ... analysis" and its competitor table says the set was "surveyed for the engagement". It is CASE-4's to rebuild (told in `bus/requests/case-4/int-1.md`). Until then the page is live as it was; the owner may want it held from the sitemap sooner.

## O4. Pages that landed before I69 may carry figures dated only by our own fetch (22 October 2026, about 09:55Z)
I69 (a figure is dated only when the research file itself ties it to a dated document) was ruled at 09:20Z on 22 October. Louisiana's review (GEO-1 t8) found values on landed pages dated the same way (the Alabama page labels the LendingTree SBA page "undated", correctly). Tonight's earlier landings (Alabama, the QSR hub and burger, the hotel hub, Kentucky) and the 18 October landings were reviewed before the ruling. The integrator's close pass re-audits every landed factory page for figures whose date comes only from a fetch or a retrieval date, and returns those to their lanes; pages stay live meanwhile. `pagecheck.py` also counts statute section numbers (for example 2116.1) as figures, counts register (`mkt:`) values that sit inside a `data-fsc-nocount` span (found on the mixed-use hub, 22 October), and misses values that sit only in other pages' sources lists (I71); those tool fixes belong to the same close pass.

Added under I87 (13:00Z): landed /states/north-carolina/ prints SBA Ledger's FY2025 combined total (1,906) against the register's 1,561 for the same cut-off, a re-total the rulebook's fake-proof test forbids printing; fix by deletion in the integrator's close pass or the re-audit.

## O5. Planned states without an ST- research file (owner steering, 22 October about 11:00Z)
None. All 42 lane-assigned states have an ST- file (ST 43 in the inventory = the 42 plus Texas; DERIVATION.md in the GEO-4 and CASE-3 blocks lists each). No state is held for research.

## O6. Older commits on main match the ruling 9 pattern (22 October 2026, about 12:30Z; information, integrator verified)

Local main holds 45 older commits (2026-07-21 to 2026-10-10, newest 1d48cc2) whose author and committer identity matches the ruling 9 pattern; one subject does too. None is from tonight: gate 7 scans each landing's range only, and every landing tonight is green. The bundles in _bundles/ carry that history. Rewriting history would change every sha, tag and bundle since July, so the integrator does not do it; whether to rewrite it before any push is the owner's decision. Also (I85): 18 tracked files on main match the pattern on raw bytes. Eight are text records from before tonight: web-fsc-2 INVENTORY.csv and seven web-fsc-4 and web-fsc-6 records, 10 and 16 October. Ten are screenshots: eight from before tonight, plus two from tonight's geo-1 t7 landing whose match is 4 bytes inside compressed image data. None of them is served.
