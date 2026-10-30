# GEO-5 t1 freeze 1, verifier (cold)

Pages: /states/colorado/ and /states/colorado/denver/. Sources in drafts/geo-5/pages hash-equal to the frozen copy's src/pages/states files and to FREEZE-t1-f1.txt (16c81ff9..., f98aaaa9...). Fix list: reviews/t1-f1-verifier-fix.py (34 edits, applied in order to scratch copies in tmp/geo-5/verify-t1/scratch; every old text occurs exactly once in the original and at its turn).

## Headline numbers re-derived
`pagecheck.py --root . --stage ready --figures` in the frozen copy: Colorado 6,960 words, 94 counted (85 research, 9 register); Denver 3,359 words, 55 counted (46 research, 9 register). Both attackers' figures CONFIRMED, equal to GATES-t1-f0. Gates 7, 9, 10 green per attacker B's rerun (not rerun by me).

## Documents I opened (WebFetch, no 403/429/robots stop)
CBRE Denver Office Q3 2026; Matthews Denver multifamily Q2 2026; Aviation Industry News DEN article; Cushman and Wakefield Denver Office Q3 2026; KUNC 14 Apr 2026; KJCT tourism article; SnowBrains tourism article.

## Verdicts, attacker A (A1)
- A1-1 CONFIRMED MAJOR-FACTUAL. CBRE prints "The suburbs recorded more than 320,000 sq. ft. of positive net absorption" and "Overall net absorption totaled negative 161,000"; the page prints exact 320,000 and says the suburbs "left" the metro at -161,000 (I59 arithmetic in words; 320,000 less 483,000 is not -161,000). Edits: prose, FAQ 1, table.
- A1-2 CONFIRMED MAJOR-FACTUAL. Matthews multifamily page: no CoStar, no chart credit. Edits: prose and source 2 publisher only (the industrial report, source 11, does carry the CoStar credit per attacker A and is left alone).
- A1-3 CONFIRMED MAJOR-FACTUAL. Aviation Industry News is dated 29 Jan 2026 and names no 28 January release; ST line 164 note is a 403 original. Edits: sentence, events row, source 23 publisher.
- A1-4 CONFIRMED MAJOR-FACTUAL (rule). SnowBrains carries $14.2 billion and 48.5% for the Denver metro; ROLLOUT-1 line 166 gives counted figures to the most specific page and the pre-count (line 53) flagged ST 155. Edit: nocount wrap. Colorado 94 to 92.
- A1-5 CONFIRMED MINOR (KJCT carries no release date, SnowBrains does). No edit (minor).
- A1-6 CONFIRMED, severity raised to MAJOR-FACTUAL. KUNC says only "FEMA has denied Colorado's appeal", published 14 Apr 2026, no decision date; the page asserts a decision date its source does not carry (same class as A1-3). Edits: FAQ 6, #hazards, events row.
- A1-7 CONFIRMED, severity raised to MAJOR-FACTUAL (rule). assign/colorado.json: "acs1 and acs5 of the same measure are one series for this rule"; the page prints B19013 in both. Edits: delete the one-year row and source 14; sources 15 to 20 renumbered to 14 to 19 (first-use order holds, all 19 cited). Denver register 9 to 8 counted.
- A1-8 CONFIRMED MINOR (Cushman: "approximately 439,100 sf"; the value itself is carried). No edit.
- A1-9 CONFIRMED, raised to MAJOR-FACTUAL: I60(b) names a comparison in words without both values as a cut (I181 lists one among its factual majors). Edit: delete the sentence.
- A1-10 REFUTED. Values carry; the pre-count held them as doubtful, not as an I64 breach, and the Denver page does not print them. A judgment call, no rule broken.
- A1-11 REFUTED as a defect (the finding itself says FEMA R8-26-NR-025 prints both place names).

## Verdicts, attacker B (A2)
- A2-1 CONFIRMED BLOCKER. "a site survey" builds the supply count; WRITER-BRIEF line 20 forbids a site visit claim and no record states one; the phrase appears on no landed page. Edit: delete.
- A2-2 CONFIRMED MAJOR-FACTUAL (same as A1-7).
- A2-3 CONFIRMED MAJOR-FACTUAL. grep: six metro sections print a mean hourly wage, the resort counties section does not. Edit: "and each metro section its metro's".
- A2-4 CONFIRMED MAJOR-NONFACTUAL, frame only (landed Nebraska hero is domestic against international migration, same Vintage 2025 year). No shared 8-word run. Verdict only.
- A2-5 CONFIRMED MAJOR-NONFACTUAL, frame only; "Each is built on county records" is also a method claim no record states. No 8-word run. Verdict only.
- A2-6 CONFIRMED, frame only (California "Eight California markets: Sacramento on its own page, and seven..."). Verdict only.
- A2-7 CONFIRMED, frame only (Idaho "holds no Idaho site", Wyoming, Vermont ledes; Denver h2 is the Northern Virginia draft's). No shared 8-word run. Verdict only.
- A2-8 CONFIRMED for Colorado: sameness shows 8-word runs with the Virginia draft ("the reply sets out the analytical framework the", "the deliverable that program asks for and the next steps..."). Edit: reword. Denver's "needs three things" is plan only (no run). Verdict only for Denver.
- A2-9 CONFIRMED. Question frames track the Northern Virginia and Virginia drafts (frame only), and each answer's last sentence says the county is "asked for first"/"the first question" after listing the project first. Edit: delete both closing sentences (every figure stays in the body with its citation; counts unchanged). Questions: verdict only.
- A2-10 CONFIRMED, frame only (District CTA: releases dated October, then "A study commissioned now"). Verdict only.
- A2-11 CONFIRMED, frame only (District description: firm statement plus one appended figure). Verdict only.
- A2-12 CONFIRMED but MINOR, not major: the border sentence and Nebraska link carry no fact and "may draw customers from across it" is uncited. No edit (minor).
- A2-13 CONFIRMED MINOR (same kind for Utah). No edit.
- A2-14 CONFIRMED MINOR (E-470 toll claim, no research row). A2-15 CONFIRMED MINOR (Aurora counties). A2-16 CONFIRMED MINOR (water and sewer patchwork). A2-17 CONFIRMED MINOR (USDA resort town clause). A2-20 CONFIRMED MINOR (coverage test clause). No edits (minors).
- A2-18 REFUTED. "need one document that their lender's credit officer will accept" states the owner's need, not the firm's approval rate.
- A2-19 CONFIRMED (same as A1-9).
- A2-21 CONFIRMED, three prose runs with other pages: Colorado/Denver/Northern Virginia "prepares independent lender grade feasibility studies for"; "a new business or a special purpose property" (five landed pages); "tests are explained on the sba 7 a and 504 lending page" (Sacramento, Virginia draft). Also found by me: "table is a five year survey estimate of" (Montana). Four edits.
- A2-22 REFUTED. Ohio's taken frame is a hero clause; Colorado's is a mid-body clause with no shared run.
- A2-23 CONFIRMED MINOR (description restates the 12,100 fact; I89 judgment). No edit.
- A2-24 CONFIRMED MINOR (parent and child FAQ 5 frames). No edit.
- A2-25 CONFIRMED (same as A1-4).

## Tallies
Attacker A: BLOCKER 0; MAJOR-FACTUAL claimed 4, confirmed 4; MINOR claimed 7, confirmed 5 (A1-6, A1-7, A1-9 raised to major), refuted 2.
Attacker B: BLOCKER 1/1 confirmed; MAJOR-FACTUAL 2/2; MAJOR-NONFACTUAL 9 claimed, 8 confirmed, 1 (A2-12) confirmed as MINOR; MINOR 13 claimed, 11 confirmed, 2 refuted.
Distinct after merging duplicates: BLOCKER 1 (A2-1); MAJOR-FACTUAL 8 (A1-1, A1-2, A1-3, A1-4, A1-6, A1-7, A1-9, A2-3); MAJOR-NONFACTUAL 8, of which 1 also carries a shared prose run (A2-8) and 1 a contradiction (A2-9); refuted 4 (A1-10, A1-11, A2-18, A2-22).

## After the 34 edits (scratch copies)
- `draftcheck.py --figures --promised`: 2 drafts, 0 with problems, 0 failed to render. Words Colorado 6,948, Denver 3,320 (ranges hold). Note draftcheck's own "counted" (91 and 46) uses the older web-fsc-6 pagecheck that ignores nocount, so it does not move; the gate's pagecheck (scripts/qa) on the same renders drops $14.2 billion and 48.5% from Colorado and the one-year income value from Denver: Colorado 92 (83 research, 9 register), Denver 54 (46 research, 8 register). Floors (30 in all, 20 research; landing 25, 15) hold.
- `sameness.py --ours ... --against wt-rollout-geo-5/src/pages drafts/geo-5/pages`: the only 8-word runs left against any landed page or other GEO-5 draft are register labels (ACS table names and codes), sba marker text (13 CFR 120.160(b), SOP 50 10 8.1) and the generated asset-class list. The tool also compares the scratch copies with the unedited originals in drafts/geo-5/pages/colorado*, which is why it prints 98 percent against them; excluded.
- Sources: Colorado 70 and Denver 19, every source cited, first-use order intact. No em or en dash in either page.
