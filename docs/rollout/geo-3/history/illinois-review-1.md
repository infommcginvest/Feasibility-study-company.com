# GEO-3 tranche t1: Illinois

Status: FROZEN for review (amendment A2: sources are committed only after the review is clean).

## Freeze
- Throwaway copy: ~/Downloads/fsc-rollout/tmp/geo-3/t1, from `git archive HEAD` of rollout-geo-3 at 03c96b2, with the two sources copied into src/pages, this lane's Illinois requests applied to data/mesh/fallbacks.json (7 folded URLs), and the chain run over the whole copy.
- sha256 of each source and rendered page: see the freeze block at the end of docs/rollout/geo-3/GATES-t1.txt.

## Pages
| URL | Type | Published | Body words | Research | Register counted | Counted | Overlap max (page) |
|---|---|---|---|---|---|---|---|
| /states/illinois/ | state, rebuilt | 2026-07-08 | 7,610 | 93 | 9 | 102 | 0.77% (/states/texas/) |
| /states/illinois/chicago/ | metro, new | DEPLOY | 3,179 | 29 | 10 | 39 | 0.28% (/states/illinois/) |

Register geographies: Illinois page `il`; Chicago page Illinois counties only (co-17031 Cook, co-17043 DuPage, co-17097 Lake, co-17197 Will), decision D10.

## Folds (sections of /states/illinois/, each with id equal to the slug)
peoria (folded after drafting: 13 unique research figures), rockford, springfield, champaign-urbana, bloomington-normal, quad-cities (Henry, Mercer, Rock Island only), metro-east (Madison, St. Clair only). Counts in FOLDED.md.

## Gates
14 of 14 green or not applicable (gate 6, case standard, does not apply). Commands and output: docs/rollout/geo-3/GATES-t1.txt. Screenshots: docs/rollout/geo-3/look/t1/. Gate 9's inbound count for Chicago (1 contextual link today, from the Illinois page) is checked again at landing; the Indiana and Wisconsin pages in later tranches link it.

## Requests (docs/rollout/geo-3/requests.json, state illinois)
- data/mesh/fallbacks.json: add the 7 folded URLs to "folded" with targets /states/illinois/#<slug>.

## Review (ruling 17)
Pending: attacker one (numbers), attacker two (sameness, sourcing, subjects), verifier.

## Review round 1 (ruling 17), on the freeze in history/illinois-GATES-review-1.txt

Attacker one (Opus, numbers): about 150 figures re-derived across both pages (105 on the state page including all seven folded sections, 45 on Chicago including all 10 register markers); every value matched its research row or register series. Findings: 1 MAJOR, 13 MINOR.
Attacker two (Opus, sameness, sourcing, subjects): 2 MAJOR, 17 MINOR. No banned name, no SBA mandate claim, no real subject, no Yorkville figure.
Verifier (Sonnet, cold): 13 of 14 claims reproduced; 1 MAJOR, 2 MINOR.

Resolution, each reproduced against the research or the copy before fixing:
- MAJOR (all three reviewers): Chicago's headline population (9,434,123, the 2020 base 9,449,351, the -0.16% change) and the 5,324 permits are CBSA-wide, Indiana counties included, and the first screen did not say so. Fixed: all four removed; the hero names the nine Illinois counties the page covers and sends the Indiana counties to the Indiana page; the stat tile is the city's 2,731,585. Research figures 29 to 25 (still over 20).
- MAJOR (attacker two): the Illinois #sba section followed the Texas section paragraph by paragraph. Fixed: rewritten in its own order from Illinois facts. Because the same pattern ran through the other state drafts (SBA, assets, cases, neighbors, CTA), the lane added tools/samecheck.py (section-level 5-word shingles) and every state page now passes it at under 20% per section pair.
- MINOR fixed: EDGE versus EDGE plus REV job counts; the Growth Corp 504 award dated FY2023 and in past tense, SomerCor's award without a district attribution; "-0.8% since April 2020"; the Springfield medical district wording; 42,284 vehicles cited to the April 2026 source only; the uncited Air Mobility Drive sentence and the Mahomet Aquifer clause removed; paired citations added (DCFS and Briskman, BNBCalc, myenterprisezone.com, FAIR Plan); undated source entries dated "undated web page, as read in research of 12 October 2026"; titles rebuilt from URLs marked "(descriptive title)"; Lake County qualified as Illinois; the $250 fee's term left to verification; the $150.96 comparison stripped of an invented period; the 17.4% versus 17.39% conflict stated; the Lincoln Institute date corrected; statewide facts on the Chicago page cut to pointers; Texas-shaped sentences, the FAQ frame, the supply section's order and the CTA rewritten; the folded sections' closing sentences varied and the FEMA denial stated once.
- MINOR not changed, with reason: the SBA values in the Illinois SBA paragraph render from sba: markers, and ruling 8 makes data/regulatory/sba.json their authority; the "Consultants" title follows the WEB-FSC-6 Texas pattern (an owner item in CLOSE.md).
