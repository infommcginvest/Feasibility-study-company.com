# CASE-NEW-1 checklist review (one Sonnet per page; review, then ONE fix pass; no open-ended review)

Page folder: ~/Downloads/fsc-rollout/drafts/case-new-1/<slug>/ (page.html, case.json, card.json, writer-notes.txt, dnu.tsv). Rules: WRITER.md in this folder. Research file: ~/Downloads/FSC Deep Searches 2/ (grep the lines you need; never read it whole). Program rules: data/regulatory/sba.json and ~/Downloads/fsc-rollout/drafts/case-1/PA-USDA-terms.md. Tool: tools/check.sh <slug> (run in zsh). Read only those. No WebFetch except to re-confirm one competitor URL.

## Check each of these classes, and only these (each was a measured pilot failure)
1. Dating (I69, I77, I86, I106): every number printed, counted or not, must trace to a research row whose publication/release/filing date, title edition year or periodic-release period dates it. A figure dated only by the builder's own web check, the researcher's retrieval date, or "current" is deleted (smallest clause that keeps the sentence whole) or stated in words without the number. A nocount wrap does not cure an undated number.
2. Single-property figures (I64, I66): the subject's size, units, acreage, price, listing figures, its loan or financing, and any one named facility's size/price are inside data-fsc-nocount and not counted. Model/assumption figures are not "market" figures.
3. Restated figures: prose that restates a counted figure as if new (same number twice counted once) or rounded repeats presented as different figures.
4. Acquisition label (Appendix 15), where the case is an acquisition: label, seller-history test and change-of-ownership wording correct.
5. Program tests (SBA/USDA): every eligibility, transient-revenue, DSCR floor, equity tier, cap, rate, fee, B&I term stated on the page matches sba.json / PA-USDA, via sba: markers. SBA "may require" a feasibility study (13 CFR 120.160(b)), never "requires".
6. Real subject leak: nothing from dnu.tsv or private lists (run check.sh gate 8); no listing price, exact acreage, street, broker, MLS, parcel; the subject is generic and hypothetical.
7. Pending links counted as live: a link to a page not yet built is a promised page and must not be described as available, and nothing on the page treats its content as existing. Links must be to existing pages or promised/pending ones.
8. Buyer-intent wording: title and H1 name the asset class and "feasibility study"; opening says Feasibility Study Company prepares such studies for owners, developers and their lenders; a CTA near the top and after the determination; no fee, turnaround, guarantee or service promise, and no lender-outcome promise that no record states.
9. Floors after your edits: counted >= 30 and research >= 20 (pagecheck --stage ready), body words 4,500 to 6,500, zero PROBLEM lines.

## Output
Stage 1: write review.md in the page folder: one line per finding (class, location, evidence from the research row id or sba.json path, fix). No prose.
Stage 2 (one fix pass): apply every fix to page.html / case.json / card.json in the page folder (deletions and wraps first; never add a new unsourced figure), then run check.sh until clean. If a fix drops the page below a floor, stop and say so; do not pad.
Reply under 120 words: findings count by class, what was fixed, final pagecheck line, floors met Y/N, anything unresolved. Never write an em dash.
