# GEO-5 t1 capped confirming review (I68), after freeze 1

Scope: the 27 word-changing edits listed in reviews/t1-f1-nondeletion.txt (numbered here in that file's order), read against the pre-fix sources (work/f1/colorado.html, work/f1/colorado/denver.html) and the post-fix sources (pages/colorado.html, pages/colorado/denver.html). `diff` of pre against post shows only the 34 verifier edits; no other line moved. Pages were not edited.

## What I ran or opened
- `diff` pre against post for both pages.
- WebFetch, no 403, 429, robots or bot stop: CBRE Denver Office Figures Q3 2026 ("Overall net absorption totaled negative 161,000 sq. ft."; "The suburbs recorded more than 320,000 sq. ft. of positive net absorption"; "Downtown posted negative 483,000 sq. ft."); Aviation Industry News, 29 January 2026 ("Denver International Airport (DEN) has announced a new passenger traffic record", no release date named); KUNC, 14 April 2026 ("FEMA has denied Colorado's appeal", no date for the denial; the first request "was denied last December").
- Research rows: ST-COLORADO lines 164 and 165 (publisher "Aviation Industry News (reporting DEN release)"), 127 and 128 (KUNC); MT-COLORADO line 37 (row 27, CBRE) and line 71 (row 61, Matthews, publisher "Matthews Real Estate Investment Services"). SBA register: wt-rollout-geo-5 data/regulatory/sba.json, equity.sba_504_new_or_special note "New Business (two years or less) or Limited or Special Purpose Property", 15%, 20% when both (R31).
- Ruling 8 (ROLLOUT-1 line 211): 13 CFR 120.160(b) says SBA "may require" a feasibility study; no page says SBA requires one.
- Sameness: `tools/sameness.py --ours <post-fix pages> --against wt-rollout-geo-5/src/pages drafts/geo-5/pages` (1,649 lines), then a shingle diff restricted to the 8-word runs that are new after the fixes (post minus pre) and shared with any landed page or other GEO-5 draft. Colorado: 148 new shingles, none shared. Denver: 58 new, the only shared ones are the ACS register label run "2020 to 2024 five year per capita income inflation adjusted dollars", formed where the deleted one-year row closed up (register label, ignored).
- Citation map: every [^n] in both pre-fix and post-fix sources (front matter and body) resolved to its source's publisher and title, then aligned. See the Denver section below.

## Per edit

| # | Page | Edit (new text) | Verdict | Reason |
|---|---|---|---|---|
| 1 | Colorado | "builds its supply count from county assessor records." | PASS | Pure deletion of "and a site survey" (A2-1). No word added; grammatical. |
| 2 | Colorado | source 23 publisher "Aviation Industry News (reporting a Denver International Airport release)" | PASS | Fixes A1-3 (no January 28 date). The article says DEN "has announced" the record and the research row's publisher is "Aviation Industry News (reporting DEN release)", so "a ... release" is carried. Title unchanged (I176). |
| 3 | Colorado FAQ 6 | "FEMA refused aid and then denied the appeal [^9]." | PASS | Fixes A1-6 (no decision date). KUNC: request denied last December, appeal denied; "then" states only that order. No number added. |
| 4 | Colorado events | "KUNC reports FEMA's denial of the appeal for the 2025 fires and flooding" (row dated April 14, 2026) | PASS | The row's date is now KUNC's publication date (14 April 2026, confirmed), which the source carries. Grammatical. |
| 5 | Colorado #costs | "...average weekly wage and each metro section its metro's May 2025 mean hourly wage," | PASS | Fixes A2-3. The six metro sections (Colorado Springs, Fort Collins, Boulder, Greeley, Pueblo, Grand Junction) each print a May 2025 metro mean hourly wage; the resort counties section prints county weekly wages and no hourly wage, and is not a metro section. Gapped clause is grammatical. |
| 6 | Colorado closing band | "In return comes the analytical framework the study would follow, the deliverable required by that program and the steps that follow." | FAIL | (a) Adds a word of compulsion not in the old text: the old "the deliverable that program asks for" becomes "the deliverable required by that program", where "that program" is the capital source and the page names SBA 7(a) and 504 among them. For SBA the deliverable (the study) is one SBA "may require" (13 CFR 120.160(b)); ruling 8 bars saying it is required. The sitewide sbamandate guard does not catch it only because the sentence names neither SBA nor a feasibility study. (b) Not grammatical: a compound subject of three nouns after "In return comes" takes "come". (c) "follow" twice in one sentence. It does clear A2-8 (no shared run). Fix: delete the sentence (below); the paragraph still reads whole and the FAQ already says what the reply names. Simulated: the deletion occurs once and creates no shared 8-word run. |
| 7 | Colorado FAQ 1 | deletion of "The county is asked for first ... [^2]." | PASS | Pure deletion (A2-9). Answer ends cleanly; source 2 still cited elsewhere; no source orphaned. |
| 8 | Colorado lede | "Feasibility Study Company writes independent feasibility studies to lender standard for Colorado projects:" | PASS | Clears the shared run (A2-21). "to lender standard" restates "lender-grade"; no fee, turnaround, office, staff, visit or credential added; grammatical ("them" still finds "projects"). |
| 9 | Colorado SBA | "a 504 borrower in business two years or less, or buying special-purpose property, puts in 15% equity, rising to 20% when it is both [^68]" | PASS | Clears the shared run. "two years or less" is the register's own definition (R31 note), cited to the SOP; values unchanged and still in sba markers; no digit added. "buying" names one case of the rule without claiming it is the only one, so nothing false. |
| 10 | Colorado SBA | "For those tests, see SBA 7(a) and 504 lending." | PASS | Clears the shared run; link text unchanged; grammatical. |
| 11 | Colorado | "The labor force row is a five-year survey estimate of residents" | PASS | Clears the Montana run. The table holds a "Civilian labor force (B23025)" row (line 563), so "row" is accurate. |
| 12 | Denver #office | "net absorption of more than 320,000 square feet outside downtown, and metro net absorption of negative 161,000 square feet [^6]." | PASS | Fixes A1-1: CBRE prints "more than 320,000" and "negative 161,000"; "left" (the arithmetic in words) is gone. Grammatical. |
| 13 | Denver FAQ | "the suburbs absorbing more than 320,000 square feet in that quarter [^6]" | PASS | Verbatim to CBRE's "more than 320,000". |
| 14 | Denver table | "-161,000 sq ft (more than +320,000; -483,000)" | PASS | All three values in CBRE's metro report as printed; terse but readable table cell. |
| 15 | Denver | "Matthews Real Estate Investment Services reads the quarter before." | PASS | Pure deletion of the CoStar clause (A1-2). |
| 16 | Denver source 2 | publisher "Matthews Real Estate Investment Services" | PASS | Equals MT-COLORADO row 61's publisher exactly (I176). |
| 17 | Denver | "calendar 2025 [^7,14]." | PASS | [^14] now resolves to the FRED Arapahoe permits source that [^15] named before. |
| 18 | Denver | "13,365 active listings [^15,16]." | PASS | Same two Realtor.com via FRED sources as the old 16 and 17. |
| 19 | Denver table | 3,599 units [^14] | PASS | Same source as old [^15]. |
| 20 | Denver table | $569,900 [^15] | PASS | Same source as old [^16]. |
| 21 | Denver table | 13,365 listings [^16] | PASS | Same source as old [^17]. |
| 22 | Denver retail prose | $293.2 million, up 95.7% [^17] | PASS | Same CBRE retail source as old [^18]. |
| 23 | Denver table | $20.28 per sq ft (+0.5%) [^17] | PASS | Same as old [^18]. |
| 24 | Denver table | $293.2 million (+95.7%) [^17] | PASS | Same as old [^18]. |
| 25 | Denver SBA | 13 CFR 120.160(b) marker [^18] | PASS | Same source as old [^19]. |
| 26 | Denver SBA | 504 equity marker [^19] | PASS | Same source as old [^20]. |
| 27 | Denver FAQ | deletion of "The county is the first question ... [^4]." | PASS | Pure deletion (A2-9); source 4 still cited elsewhere. |

## Denver renumbering (sources 15 to 20 now 14 to 19)
Every citation in the pre-fix and post-fix Denver sources was resolved to its source (publisher and title) and the two sequences aligned (84 citations before, 82 after). The only differences are the two deleted citations (the one-year income row's [^14] and the FAQ's [^4]) and three citations whose surrounding words changed (edits 12 to 14, still CBRE Denver Office Figures Q3 2026). Every other [^n] points at the same source as before. 19 sources, all cited; the body's first-use sequence is the pre-fix sequence with source 14 removed and later numbers shifted down by one, so the order the page had is kept.

## Tally
27 edits: 26 PASS, 1 FAIL (edit 6). Fix in reviews/t1-f2-capped-fix.py: one deletion of the closing band sentence. No counted figure moves (the sentence holds none), so Colorado stays at 92 and Denver at 54 on the verifier's count.
