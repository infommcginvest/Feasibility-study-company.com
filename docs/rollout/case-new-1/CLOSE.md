# CASE-NEW-1 close (2026-10-29)

State at close: main 860fcd32 (records only after the t2 landing ce7d9a1c); live deploy 6ae3104e329ef44e1fa3aa2c (t2; t1 was 6ae303bebaac4163f005af0f); 211 URLs. Main checkout still on web-fsc-2 at 1d48cc28. Nothing pushed. Copy slots free, integrator free.

Landed: 7 new cases (t1: Bardstown, Broussard, Elizabethtown urgent care; t2: Ness City, Port Charlotte, Sevierville, Lebanon). Gates 14/14 at each landing on the merged site. Freeze: 99 files hashed (FREEZE-SHA256.txt, outside the repository because the per-figure rows carry real-site identifiers).

## Close round (two Sonnet attackers, one cold Sonnet verifier that defaulted to refuted)
- Verifier result: 20 blockers and majors judged, 6 confirmed, 14 refuted. Confirmed: Lebanon's five 2026 estimated tax rates and three tax-year-2025 rates (dated only by undated pages, I77/I86) and its 6,700 hospital surgeries (undated); stale text on the Kansas, Tennessee and Florida state pages. Refuted: the I64 arguments against Sevierville's park counts and urgent care's two corporate commitments (urgent care stays at exactly 30/20).
- **Lebanon is under its floors on the confirmed findings: 22/12 (23/13 if the 6,700 stays). The page is live. This breaks the lane's own constraint and is reported, not rebuilt: its research holds no further usable local figures.** Options for the owner: retract it (revert the page, card, Nashville edit and sitemap; slug returns to pending), or refresh the Lebanon research with dated sources and rebuild.
- Stale text on live state pages that the two landings made false, to fix in one corrective integrator landing: Kansas (lede says no published case is set in Kansas), Tennessee (heading and lede say one Tennessee case; the other-markets paragraph says no case names a location in Nashville), Florida (heading counts two cases in named towns and five by region; Port Charlotte is a sixth placed in a named town). Not fixed here: a landing needs the same gates and a deploy, and the Lebanon decision belongs in the same corrective landing.
- Verifier also refuted two worded CLOSE claims: gates ran on the merge-commit trees (as recorded), and only the three t1 pages had pending anchors before landing (the four t2 pages had none).
- Held and unchanged: childcare-gonzales-louisiana-sba (29 counted if the three employer investments are wrapped under I64, one under the floor; drafts in fsc-rollout/drafts/case-new-1/_held/).
- Pending links on state pages to Gonzales, the Natchitoches hotel and the Elizabethtown assisted living case remain pending and read as published in a sentence or two; this predates the lane (verifier: refuted as a defect of these landings).

## Process lessons (for the 46 rebuilds)
- Run the READY gates with the repo history clean: real addresses in the lane's own committed notes tripped gate 8; keep per-figure records outside the repository.
- A pre-count that trusts undated pages overstates counts: tax rates and news items dated only by a page or a fetch fell at review or at the close. Treat Sevierville, urgent care and Lebanon style margins (31 or 30) as unsafe; require 36 or more counted before building.
- State and metro pages that say "no published case" go stale at landing: grep for them before the READY run (the gates did not catch Kansas, Tennessee or Florida; gate 9 caught only the Nashville edge).
- card wording must say "does not support" when the restructured structure also fails (casemodel refuses otherwise).

## Tokens
The session reports no output-only figure per tranche (get_usage returns plan percentages and context size). From the subagents' completion notices, total tokens (input plus output, all subagents, Sonnet):
- C0 pre-count, 13 readers: 4,159,732 (about 61,000 per case for 68 cases).
- t1: four builders 1,138,606 (includes the held Gonzales build), four reviews 752,575, one gate 7 fix 97,156; 1,988,337 for the tranche, 662,779 per landed case counting the three landed pages and 497,000 per page built.
- t2: four builders 1,173,631, four reviews 705,636; 1,879,267 for the tranche, 469,817 per landed page.
- Close: two attackers 462,871, one verifier 218,546; 681,417.
- Main thread tokens are not separable from the notices. The pilot's 260,000 output tokens per case is not comparable to these totals (they include input); the per-page build plus review totals were about 480,000 to 640,000 tokens.
