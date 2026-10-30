# FSC-RESUME-1 parked (26 Oct 2026)

The owner asked on 26 October to pause the programme for a couple of days and to finish what was in hand. This record parks FSC-RESUME-1 so a later session can resume it from step zero of this file. The close (CLOSE-RESUME-1.md, the resume bundle of R8 and the close output) is not written: 21 of the 22 lane-assigned states have landed and Montana has not.

## Status at park

states landed 41 of 42; metros landed 22

## Landed in this session (lane, tag, main, deploy, URLs)

| State (pages) | Lane | Tag | Main | Deploy | URLs |
|---|---|---|---|---|---|
| Iowa | GEO-3 | `rollout/geo-3/t10` | `4ab19f1` | `6ade111bb82857c64a50409f` | 188 |
| Pennsylvania | GEO-2 | `rollout/geo-2/t3` | `1aa8ed9` | `6ade123a7a95e6877ddba0ab` | 188 |
| Washington + Seattle + Spokane | GEO-4 | `rollout/geo-4/t2` | `8f4c2c6` | `6ade142ceebdc8bf19e7e024` | 190 |
| Arkansas + Northwest Arkansas | GEO-1 | `rollout/geo-1/t10` | `3d42494` | `6ade1ea3bb5b736c1d328735` | 191 |
| New Jersey | GEO-2 | `rollout/geo-2/t4` | `8abc060` | `6ade1fbc83ef24b45898d5e0` | 191 |
| Arizona | GEO-4 | `rollout/geo-4/t3` | `1252f32` | `6ade2bffd2d46360afd971ae` | 191 |
| Mississippi | GEO-1 | `rollout/geo-1/t11` | `71682d4` | `6ade3ab5f45d3271ca98e9fb` | 191 |
| Massachusetts | GEO-2 | `rollout/geo-2/t5` | `1338b5a` | `6ade42a9945195b6060cc4e2` | 191 |
| Oregon | GEO-4 | `rollout/geo-4/t4` | `8c04c1b` | `6ade45c805f85409fa62b021` | 191 |
| Maryland | GEO-1 | `rollout/geo-1/t12` | `e121211` | `6ade58a39134767c69fc542c` | 191 |
| Utah | GEO-4 | `rollout/geo-4/t5` | `9cf07b4` | `6ade6318911868c25aa5b8b3` | 191 |
| Connecticut | GEO-2 | `rollout/geo-2/t6` | `a224c95` | `6ade674e883f73aa2fae86b4` | 191 |
| West Virginia (new) | GEO-1 | `rollout/geo-1/t13` | `f94f417` | `6ade78e339563b8753dba206` | 192 |
| New Hampshire | GEO-2 | `rollout/geo-2/t7` | `eb44d40` | `6ade844e650baad45cabc680` | 192 |
| Nevada + Las Vegas (new metro) | GEO-4 | `rollout/geo-4/t6` | `99c00b6` | `6ade868aea3c3e54bcaeb25a` | 193 |
| Delaware (new) | GEO-1 | `rollout/geo-1/t14` | `8f2adef` | `6ade99e81d39742792adcfba` | 194 |
| New Mexico | GEO-4 | `rollout/geo-4/t7` | `0b3c3c9` | `6adea5c6696095833692e96c` | 194 |
| Maine | GEO-2 | `rollout/geo-2/t8` | `3c8fa21` | `6adea7d5b93393e4ea6facc9` | 194 |
| Rhode Island (new) | GEO-2 | `rollout/geo-2/t9` | `8ec342d` | `6adec4cb975a49e4fc98d5f0` | 195 |
| Idaho + Treasure Valley (new state, new metro) | GEO-4 | `rollout/geo-4/t8` | `90ede53` | `6adecaadfc49e00551aeb30c` | 197 |
| Hawaii | GEO-4 | `rollout/geo-4/t9` | `c29e330` | `6adeee468b601baae2a5b8b9` | 197 |

New metros this session: Seattle, Spokane, Northwest Arkansas, Las Vegas, Treasure Valley. Every other market was folded into a section of its state page under ruling 6 and the D7 margin; the counts per market are in each lane's FOLDED.md and in I107 to I180. The R7 close pass landed first (tag `rollout/int/close-1`, main `8b822ed`, deploy `6ade0febc265dc0f67515ebf`, I117 to I125).

## What remains

1. Montana (GEO-4 t10, a new state). Its reader and pre-count job is `drafts/int/jobs/precount-montana-t10.md`; its outputs, if the job finished before the park, are in `drafts/geo-4/facts/montana*` and `drafts/geo-4/facts/montana-PRECOUNT.md`. The pre-count finished at the park: every market folds (missoula 10 free, dated research figures, billings 8, bozeman 6, butte, great-falls, helena and kalispell 2 each, against 21), and the state page holds 15 research on its own rows and 44 research, 54 in all, with the sections; under the harshest combination of readings it holds 17 research, under the floor, so it is a thin new state to be written under a watch as Delaware was (I161, I168). Next: the integrator rules on the pre-count (one page or metros, R9 floors for a new state), then writer (Opus), SEO (Fable), gates and freeze 1 (Sonnet, copy slot 3), two attackers and a cold verifier, fixes, freeze 2 and commit, landing with the new state index entries (as I160, I169, I177, I179: the `/states/` list and card, the home page list by population, the chrome item with `hide_until_live`, a mesh term only if gate 9 needs one), deploy with the helper.
2. The close: `docs/rollout/int/CLOSE-RESUME-1.md` (each state with lane, tag, main sha, deploy id and URL count; metros shipped and folded with counts; counted figures and maximum overlap; review findings and resolution; R7 results; open owner items), landed as the last records tranche, then the resume bundle `_bundles/resume-<main sha>.bundle` covering `b2fb289..main` (R8), verified, newest five kept, and the close output block of the owner's FSC-RESUME-1 text.

## Resume step zero

Read `docs/rollout/int/input/RESUME-1.md`, this file, `docs/rollout/int/DECISIONS.md` I102 to the last, and the working log `~/Downloads/fsc-rollout/drafts/int/RESUME-1-LOG.md`. Confirm `git -C ~/Downloads/wt-rollout-int status` is clean and `rollout-int` equals `main`; confirm the copy ledger `~/Downloads/fsc-rollout/bus/status/int-copies` shows three free slots; confirm production serves the last deploy listed above; check `df -g ~` (it stood near 27 GB free at park).

## Open owner items

- O6 (unchanged from before this session).
- The Connecticut private school case keeps its first-person engagement narrative for CASE-4 (I104, I125); legacy gate reds on legacy case pages (gate 4 case pairs, gate 8 subject identifiers on four legacy cases) are reported, not failed (I125, I128).
- Delaware source 2, which carries the lead fact, is the research's own row and pairs one publisher's title with another publisher's URL for the same ruling (I168): the owner may wish to confirm the URL.
- Wisconsin statute values from an undated statute (7 days, 180 days), noted for GEO-3.
- The Houston register paragraph deleted in the close pass, to be re-added by GEO-1 (I124); the Philadelphia section's lost New Jersey, Delaware and Maryland links (I127).
- CASE-1 notes filed on the bus (`bus/requests/case-1/int-resume-1-nh.md`): the New Hampshire fitness case's SBA re-total, value collisions with the New Hampshire and Maine state pages, Concord's population.
- CASE-2 keep-links note (`bus/requests/case-2/int-geo-4-2.md`).
- Delaware and West Virginia have no mesh term (Rhode Island received one at its landing, I177); both hold three or more inbound links without one.
- Pagecheck's advisory body-word range check flags older landed pages (Nashville at 1,433 words, Texas at 10,755), not a gate.
- At the Hawaii landing, the Treasure Valley page's two mentions of a $1.2 billion data center cost (in nocount) were deleted because the value collided with a counted Nashville figure and left Nashville at 24 against its landing floor of 25 (I182); a gate run that treats new pages as new does not see such a collision, so a later landing gate run is the check.
