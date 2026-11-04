# CASE-NEW-1 resume (lane paused by the owner, 2026-10-29)

## Exact state
- Live deploy: 6ae31a7d6a227d282119f142 (t3, corrective), locked, published; 211 URLs. Earlier: t1 6ae303bebaac4163f005af0f, t2 6ae3104e329ef44e1fa3aa2c.
- Main: see the head recorded in `bus/landed/case-new-1-t3` (t3 landing) and the final records commit that follows it. Main checkout still on `web-fsc-2` at 1d48cc28 (never moved). Integrator and copy slots released.
- Landed (7): self-storage-bardstown-kentucky-usda, restaurant-acquisition-broussard-louisiana-sba, urgent-care-elizabethtown-kentucky-sba (t1); grocery-store-ness-city-kansas-usda, car-wash-port-charlotte-florida-sba, restaurant-sevierville-tennessee-sba, medical-office-lebanon-tennessee-sba (t2). t3 fixed the Kansas, Tennessee and Florida state-page text the landings made false.
- LEBANON: owner ruling "keep it live". It is under its floors on the close findings: 22 counted, 12 research (23 and 13 with the surgery count kept). Research refresh pending: dated sources for the Wilson County tax rates and hospital activity, or fold it. Do not extend it with undated figures.
- Held: childcare-gonzales-louisiana-sba (drafts in fsc-rollout/drafts/case-new-1/_held/; 29 counted if the three employer investments are wrapped under I64; owner ruling or a rebuild with more dated local figures).
- Folded or waiting on the owner: retreat-center-kerhonkson-new-york-usda (folded, 28 Oct); marina-gig-harbor-washington-sba (waits for CASE-ENGINE-1 and a hypothetical transient-heavy subject).
- Wait for CASE-ENGINE-1: hotel-natchitoches-louisiana-eb5, industrial-flex-gardner-kansas-conventional, mixed-use-multifamily-euclid-ohio-eb5 (pass the floor); assisted-living-elizabethtown-kentucky-bridge, short-term-rental-yucca-valley-california-conventional, multifamily-clarksville-tennessee-dscr (also short of the floor).
- Fold today (new): self-storage-pataskala-ohio-sba, hotel-acquisition-fairlawn-ohio-sba, hotel-hays-kansas-usda, marina-new-baltimore-michigan-sba, marina-shell-knob-missouri-usda, laundromat-acquisition-huron-county-ohio-sba.
- The 46 legacy rebuilds are not started. PAGE/FOLD list: BUILD-PLAN-1.md ("C0 result"). Rerun the pre-count first: seven landings moved the collisions, and undated figures were found at review.

## Next step (first on resume)
1. Owner: ruling on Gonzales; research refresh for Lebanon (or fold). Then, if wanted, the next new-case tranche only from cases that pass with 36 or more counted figures.
2. Rerun the C0 pre-count for the 46 rebuilds before CASE-REBUILD lanes start (per-figure rows stay outside the repository: gate 8).
3. Pending links still read as published on a few state pages (Louisiana and Kentucky: Gonzales, the Natchitoches hotel and the Elizabethtown assisted living case); they predate the lane.

## Tools and records
tools/check.sh (builder check), tools/addcards.py (the /case-studies/ cards), tools/nashville_edit.py (pattern for a metro edit), WRITER.md and REVIEW-BRIEF.md (lessons from t1 and t2 at the end of WRITER.md), SEARCH-CONSOLE.txt, CLOSE.md, tranches/t1.md and t2.md, GATES-t*-landing.txt. The READY runs were simulations in a throwaway copy (GATES-t*-ready-treeB-simulation.txt).

## Pushing
The public remote `origin` was NOT pushed: three commits on main (a03f5624, 0310699e, b5ad4948) carry the sister firm's domain in author and committer, the GEO-5 D9 owner item. Pushing main or any branch containing them publishes that domain in a public repository. Main and the lane branch were pushed to the private `backup` remote only (see CLOSE.md for the hashes).

## CLOUD-1 (4 Nov 2026)
- Tranche c1 (six new cases from the repository's research): `cloud/case-new-1`, record `tranches/c1.md`, gates `GATES-c1-ready.txt` (13/14). Shipped at the owner's word before the attacker round finished: review the two attacker files and a cold verifier before landing.
- Tranches c2 and c3 (nine more new cases, unreviewed): `cloud/case-new-1-drafts`, `docs/rollout/case-new-1/cloud-1/drafts/` (README there). Folded: pet-boarding-bismarck-north-dakota-sba.
- Pull requests are refused for this session's GitHub integration (403). Compare link: https://github.com/<owner>/Feasibility-study-company.com/compare/main...cloud/case-new-1?expand=1 (`<owner>` is the repository's account, not written out: its name matches the ruling 9 pattern).
