# GEO-5 t2 freeze 1, verifier (cold)

Pages: /states/virginia/ (virginia.html) and /states/virginia/northern-virginia/ (virginia/northern-virginia.html), paths relative to drafts/geo-5/pages.

## Preconditions
- shasum of pages/virginia.html (877d0bf1...) and pages/virginia/northern-virginia.html (6f707577...) equals the copy's src/pages/states files byte for byte. FREEZE-t2-f1.txt carries sha256 values; the shasum equality of drafts and copy is what was checked.
- Headline numbers re-derived with the worktree's scripts/qa/pagecheck.py functions (research_figures, register_figures) on the rendered sources: state 107 research + 10 register = 117; Northern Virginia 37 + 10 = 47. Both equal the gate and both attackers. Body words by draftcheck: 6,852 and 3,186 (inside 4,500 to 8,000 and 2,000 to 3,500). Caution for the integrator: draftcheck.py imports the older docs/web-fsc-6 pagecheck, which does not drop `data-fsc-nocount`, so its "counted" column overstates after a nocount wrap (it still says 37 for Northern Virginia after A1-11). The scripts/qa/pagecheck.py count is the gate's.
- WebFetch reproductions I made: FRED VABPPRIVSA (3,274.12673, "The Federal Reserve Bank of St. Louis seasonally adjusts this series"); REBusinessOnline p=448204 ("is set to break ground", "Site work began in December"); BLS ro3fx9537 (footnote names Currituck only; 164.5 government); BLS ro3fx9538 (footnote adds Clarke, Culpeper, Rappahannock, Warren and four cities); FFXnow April 20 (statewide 173,934 carries no seasonal-adjustment label). No door closed.

## Verdicts, attacker 1

| id | verdict | note |
|---|---|---|
| A1-1 | CONFIRMED, MAJOR-FACTUAL | FRED computes the adjustment itself and prints five decimals; the Census attribution is wrong. Edit deviates from the proposal: the value and the "removes the seasonal swing" sentence go, but source 26 stays as a value-free cite ("FRED adjusts the same series for season itself and posts that version separately [^26]"), and its publisher becomes "FRED, seasonally adjusting U.S. Census Bureau data". Deleting source 26 would renumber [^27] to [^77] in 50 places that cannot be edited uniquely. Research 107 to 106. |
| A1-2 | CONFIRMED, MAJOR-FACTUAL | Payroll footnote names Currituck only; OEWS (source 9) names the three. FHFA and BEA titles say VA-NC with no counties. Both sentences edited; the North Carolina link is kept. |
| A1-3 | CONFIRMED, MAJOR-FACTUAL | 164.5 is the VA-NC metro count, the page defines Hampton Roads as the Virginia side. |
| A1-4 | CONFIRMED, MAJOR-FACTUAL (I60 b) | Both values are in the sentences before, not in this one. |
| A1-5 | CONFIRMED, MAJOR-FACTUAL (I60 b) | Northern Virginia, "therefore differ"; values come in later sentences. |
| A1-6 | CONFIRMED, MAJOR-FACTUAL (I60 b) | 12.3 and 12.5 are not printed on the page. |
| A1-7 | CONFIRMED, MAJOR-FACTUAL (I60 b, I69) | Weldon Cooper values not printed; city value not in the research (MT 210 note holds Albemarle only). |
| A1-8 | CONFIRMED, MINOR | "Industrial space moved the other way": comparison of unprinted-in-sentence values. Verdict only. |
| A1-9 | CONFIRMED, MINOR | FFXnow does not label the statewide 173,934 as not seasonally adjusted. Verdict only. |
| A1-10 | CONFIRMED, MINOR | BLS region also takes in Clarke, Culpeper, Rappahannock, Warren and four cities. Verdict only. |
| A1-11 | CONFIRMED, raised to MAJOR-FACTUAL (I64) | Research row 47 note says "single-property" and PRECOUNT flag 11 says it "must stay out of the count"; the page counts it. Wrapped in nocount at all three uses. Northern Virginia research 37 to 36. |

## Verdicts, attacker 2

| id | verdict | note |
|---|---|---|
| A2-1 | CONFIRMED, BLOCKER | "As a Northern Virginia feasibility study company, we write the study" states a place of business. Fix keeps the keyword (the only "company" form on the page, owner's buyer-intent rule) in a buyer-side sentence with no "we", office, staff or location: "Someone hiring a Northern Virginia feasibility study company needs the study written to the program the capital comes from, and the parcel decides which programs are open." The attacker's version would have dropped the keyword to zero. The Virginia sentence "a Virginia feasibility study company has one job, which Feasibility Study Company does" names no location or staff: MINOR, no edit. |
| A2-2 | CONFIRMED, MAJOR-FACTUAL | p=448204 reports a venture "set to break ground", site work begun in December; no January 2026 groundbreaking. Body sentence, events row, H2 and source 32 date edited. The new sentence does not date the second groundbreaking, only the article (January 13, 2026). |
| A2-3 | CONFIRMED, MAJOR-FACTUAL | Loudoun (north and east boundary) and Prince William (eastern shore) lie on the Potomac. H2 now names the three that lost jobs; the body sentence is deleted. |
| A2-4 | CONFIRMED, MAJOR-FACTUAL | Closing band's "a regional average now describes none of them" is uncited, unperformed arithmetic in words (I59, I181). |
| A2-5 | CONFIRMED, MAJOR-FACTUAL | (a) = A1-6, (b) = A1-7, Northern Virginia = A1-5, (c) summer and academic-calendar claim has no value and no research row (grep of MT-VIRGINIA finds none): sentence, card and H2 edited. |
| A2-6 | REFUTED | "Whether a lender asks for a study ... is the lender's call" is literally true and the SBA "may require" marker sits right before it. No edit. |
| A2-7 | CONFIRMED, MINOR | "counties across the Potomac" and "covered on their own page" go beyond VPM's undefined "Northern Virginia". Verdict only. |
| A2-8 | CONFIRMED, raised to MAJOR-FACTUAL | Source 5 (MEDLISPRI51153, Prince William) prints $599,995; source 6 is Loudoun. Cite [^5] only. The FAQ's [^5,6] prints both counties and is right. |
| A2-9 | CONFIRMED, MAJOR-NONFACTUAL | Run "the deliverable that program asks for and the next steps" shared with colorado.html (reproduced with sameness.py). Edited. |
| A2-10 | (a) CONFIRMED, edited; (b) CONFIRMED as frame-only | (a) "independent lender grade feasibility studies for projects in" shared with colorado.html; "for projects in" to "on projects in". (b) the "first question is which of the five, because the year to March 2026 split them" plan and the cases H2 mirror Denver; no shared 8-word run, so verdict only (integrator assigns the plan under I74). |
| A2-11 | CONFIRMED as frame-only | The firm-first description frame repeats across Wyoming, Denver, DC, VA and NOVA, but it is the frame the writer brief prescribes and no 8-word run is shared. Verdict only. Side note: NOVA says "prepares studies" (no "feasibility") and both omit "their" before SBA. |
| A2-12 | CONFIRMED as frame-only | Engagement-FAQ and cases-lede constructions overlap in plan (Delaware, Colorado, Denver, Wyoming); the longest shared run with Colorado ("would follow the same structure with") is 6 words. Verdict only. |
| A2-13 | CONFIRMED, MINOR | Neighbour links: see below. |
| A2-14 | PARTLY CONFIRMED | Bullet 1 ("Census metropolitan area named for its central city") CONFIRMED and raised to MAJOR-FACTUAL: false for Hampton Roads (named for three cities) and Blacksburg-Christiansburg; edited. Bullet 2 is A1-2 (edited). Bullets 3 (SBA disaster loans follow designated areas) and 5 ("typically where the cash flow has not yet been earned") CONFIRMED as uncited, MINOR, verdict only. Bullet 4 (cases "across the state lines it shares") REFUTED: Maryland, North Carolina, West Virginia and Tennessee all border Virginia; "nearest" is loose, not wrong. Bullet 6 (DC commute) no finding. Bullet 7 is A1-4. |

## Neighbour links into Northern Virginia (three inbound, gate 9 needs three)
- Maryland, #metros: "Washington-Arlington-Alexandria metro with the District of Columbia and counties in Virginia and West Virginia". TRUTHFUL in context. The anchor names a group wider than the target (four counties and Alexandria), but the target states its scope in the first screen and the sentence is about the metro's delineation. Keep.
- West Virginia, #lenders: "a certified development company based in Fairfax, Virginia". TRUTHFUL but loose. The source ([^62], House hearing 2017) says Fairfax, Virginia; the page links to the Fairfax County and Northern Virginia page, which excludes the City of Fairfax and holds no development-company record. It is a place link, not a claim that the target documents the company. Keep; revisit when the DC page lands (a link from DC would let this one go).
Neither is removed by any edit.

## Tally
Confirmed: BLOCKER 1; MAJOR-FACTUAL 13 (A1-1 to A1-7, A1-11, A2-2 to A2-5, A2-8, A2-14 bullet 1); MAJOR-NONFACTUAL 4 confirmed (A2-9 and A2-10a with edits; A2-10b, A2-11, A2-12 frame-only, no edit); MINOR 6 confirmed with no edit (A1-8, A1-9, A1-10, A2-7, A2-13, A2-14 bullets 3 and 5). Refuted: A2-6 whole, A2-14 bullet 4. (Counted by finding id the totals are: attacker 1, 11 confirmed, 0 refuted; attacker 2, 13 confirmed including partials, 1 refuted.)

## Fix file and checks
`t2-f1-verifier-fix.py`: 27 edits (VA 16, NOVA 11); every old text occurs exactly once in its source. One edit beyond the findings: NOVA cta.p ending "and the steps that follow" to "and what comes next", because sameness.py joins cta.p with the description and reports an 8-word run with district-of-columbia.html that exists only through that join; it is harmless to change and leaves the tool clean.

Applied to scratch copies (tmp/geo-5/verify-t2/virginia.html and virginia/northern-virginia.html):
- draftcheck `--figures --promised`: 2 drafts, 0 with problems, 0 failed to render. Words 6,823 and 3,151. No dash characters, no banned names.
- Counted figures (scripts/qa/pagecheck.py functions): state 106 research + 10 register = 116; Northern Virginia 36 + 10 = 46. A6 floors (READY 30 in all with 20 research; landing 25 with 15) hold on both.
- sameness.py, scratch copies against the worktree pages plus the other GEO-5 drafts (the unedited Virginia drafts left out, since they are the same pages): no shared 8-word run except the practice-area link name runs ("explained on the SBA 7(a) and 504 lending page", shared with Montana, Sacramento landed pages and the Colorado draft), the sba marker text, the register labels and the asset hub list names, all exempt. Highest pair overlap 0.72 percent.
