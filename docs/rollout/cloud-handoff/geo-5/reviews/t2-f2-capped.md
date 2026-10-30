# GEO-5 t2, capped confirming review (I68) after freeze 1

Scope: the 23 word-adding or word-changing edits of reviews/t2-f1-nondeletion.txt, read in place in the post-fix sources pages/virginia.html (VA) and pages/virginia/northern-virginia.html (NOVA). Each new text occurs exactly once and no old text remains (checked by script). The three nocount wraps and the one pure deletion were not in scope.

## What I opened
- FRED VABPPRIVSA: separate series, units "Units, Seasonally Adjusted", source U.S. Census Bureau, note "The Federal Reserve Bank of St. Louis seasonally adjusts this series".
- BLS ro3fx9537: the area text names Currituck County as the only North Carolina county; government 164.5 thousand, September 2026, preliminary.
- BLS OEWS Virginia Beach release (source 9): the area includes Camden, Currituck and Gates counties, NC.
- REBusinessOnline p=442700 (October 22, 2025): "has broken ground on a 493-bed" development. p=448204 (January 13, 2026): "is set to break ground on Rambler"; "Site work began in December".
- infocville.com March 26, 2026 article (source 56): prints Weldon Cooper estimates for Charlottesville city and Albemarle County.
- Research MT-VIRGINIA rows 1 to 5 (NOVA covered jobs: Fairfax -2.1%, Arlington -4.5%, Alexandria -2.6%, Loudoun +2.8%, Prince William +1.0%), rows 28 and 29 (Loudoun and Prince William listing medians), rows 189 and 190; ST-VIRGINIA rows 27 and 28.
- NOVA source list: [^5] is MEDLISPRI51153 (Prince William), [^6] MEDLISPRI51107 (Loudoun).
- sameness.py, post-fix pages against the worktree pages and the GEO-5 drafts: the only non-register runs left are the SBA SOP marker text, the asset hub list names and the practice-area link name ("explained on the SBA 7(a) and 504 lending page"), all exempt. No run touches any edited text, including the cta.p and description join on NOVA.

No door closed; nothing on www2.census.gov.

## Per edit

| # | page | edit | verdict | reason |
|---|---|---|---|---|
| 1 | VA | A1-1 permits sentence | PASS | 3,274.12673 and the "removes the seasonal swing" sentence are gone. [^26] now cites "FRED adjusts the same series for season itself and posts that version separately", which the VABPPRIVSA page carries (St. Louis Fed note; separate series ID, NSA version at VABPPRIV). No number, no comparison. Grammatical, if stiff. |
| 2 | VA | A1-1 source 26 publisher | PASS | "seasonally adjusting U.S. Census Bureau data" matches the page (source Census, adjustment by the St. Louis Fed). Title unchanged from the research (I176). |
| 3 | VA | A1-2 "each version reaches into North Carolina: ..." | PASS | Source 9 names Camden, Currituck and Gates; source 8 names Currituck. Fixes the finding. Gapped clause is grammatical. |
| 4 | VA | A1-2 "North Carolina counties included [^8,9,45,46]" | FAIL | Fixes the three-county attribution but puts plural "counties" on source 8, which names one county (Currituck), and on FHFA and BEA titles that say only "VA-NC". Fix: "part of North Carolina included ... includes that part" (fix file). |
| 5 | VA | A1-3 "164.5 thousand in the Hampton Roads metro, which reaches into North Carolina [^8]" | PASS | Labels the metro-wide value; true on ro3fx9537. |
| 6 | VA | A1-4 "Both outlets were reporting on the commission's work." | PASS | Comparison in words removed; nothing added. |
| 7 | VA | A1-6 "in their own ways, so each" | PASS | Unprinted vacancy comparison removed. (A1-8, "Industrial space moved the other way", stays as the verifier's verdict-only MINOR, not a new edit.) |
| 8 | VA | A1-7 "prints the Weldon Cooper Center's estimates as well [^56]" | PASS | The article prints Weldon Cooper estimates for both localities; no value, no "differ". |
| 9 | VA | A2-2 Virginia Tech body sentence | PASS | October 2025 groundbreaking ([^31], "has broken ground", October 22, 2025); second "set to break ground" with site work begun in December, reported January 13, 2026 ([^32]). Every word matches. |
| 10 | VA | A2-2 events row | PASS | "breaks ground and a second is reported as set to break ground"; the date cell's "January 2026" is the report date, which the row states as a report. |
| 11 | VA | A2-2 source 32 date | PASS | "site work begun December 2025": article of January 13, 2026 says site work began in December. |
| 12 | VA | A2-5(c) Blacksburg H2 | PASS | No swing or academic-year claim left; "university metro" and "student housing projects near campus" rest on the source titles. |
| 13 | VA | A2-5(c) "A study that reads a single month says which month it read." | PASS | Uncited cause removed; advice only. |
| 14 | VA | A2-5(c) Blacksburg card | PASS | The section reads BLS payroll [^65], a Montgomery County listing median [^66] and REBusinessOnline reports [^31,32]; the card says so. |
| 15 | VA | A2-9 CTA reply sentence | PASS | Run with colorado.html gone. No fee, turnaround or promise added. "the program's deliverable" is softer than the old "asks for"; it does not say SBA requires a study (the "may require" marker stands elsewhere). |
| 16 | VA | A2-14 metros lede "read as a metropolitan area" | PASS | No longer claims each is named for a central city. All eight cards define metro areas; Hampton Roads is read on metro figures plus Virginia-side city figures, so "read as" holds. |
| 17 | NOVA | A1-5 "This page states each broker's number in its own sentence" | PASS | Comparison in words removed. |
| 18 | NOVA | A2-1 keyword sentence | PASS | "Someone hiring a Northern Virginia feasibility study company needs the study written to the program the capital comes from" has no we, office, staff or location; it places the firm nowhere. The keyword form stays (1 use; the "Northern Virginia feasibility stud" stem has 3 uses, within I89). No claim that any program requires a study. |
| 19 | NOVA | A2-3 economy H2 | PASS | Fairfax -2.1%, Arlington -4.5%, Alexandria -2.6% fell; Loudoun +2.8%, Prince William +1.0% rose (research rows 1 to 5; body sentence with [^1]). No Potomac claim left. |
| 20 | NOVA | A2-4 closing band "and two rose." | PASS | Uncited conclusion gone; nothing added. The "three of these five" count words were already there. |
| 21 | NOVA | A2-8 "$599,995 listing median [^5]" | PASS | [^5] is MEDLISPRI51153, Prince William, $599,995 (MT row 29). |
| 22 | NOVA | cta.p "and what comes next" | PASS | Clears the joined run with district-of-columbia.html; no promise added. |
| 23 | NOVA | A2-10(a) "studies on projects in Fairfax" | PASS | Clears the run with colorado.html; grammatical. |

## Totals
22 PASS, 1 FAIL (edit 4). Fix: reviews/t2-f2-capped-fix.py, one edit, old text present once. It adds no figure and no word that a source does not carry.

## Observation outside the fixed regions (not a FAIL, not in EDITS)
Two untouched sentences in the Hampton Roads section say "North Carolina counties included" on a single source each: "For the full metro, ... BLS counted 832.9 thousand ... [^8]" (one county on that table) and "FHFA's index ... read 388.95 ... [^45]" (title says only VA-NC). Research row 103's note says "North Carolina counties", which is where the plural came from. The fix file's closing comment gives the wording if the integrator takes them.
