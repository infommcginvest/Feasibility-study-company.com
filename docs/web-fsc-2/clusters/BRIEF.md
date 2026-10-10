# WEB-FSC-2 cluster brief (shared by clusters A to F)

You are fixing SBA statements on feasibility-study-company.com so that every one reflects SOP 50 10 8.1 with Technical Policy Updates (effective October 1, 2026). The site is static HTML served from the repository root; there is no build step. Work only in the files listed for your cluster. Do not touch any other file. Do not use the network. Do not run git commands other than `git diff` on your own files.

## Inputs

- `docs/web-fsc-2/REGISTER.csv`: the verified rules. Columns: id, rule, value_8_1 (the rule now), value_8 (the old SOP 8 value), status, section, paragraph, page, verbatim_quote, primary_url, resolution_note, value_8_cite. Rows with status NOT_IN_TEXT are rules that may NOT be published.
- `data/regulatory/sba.json`: the same values as the site renders them, each with its register id.
- `docs/web-fsc-2/INVENTORY.csv`: every candidate statement (file, url, line, statement, category, match, provisional register_id, classification, resolution, cluster). Filter to your cluster. The line numbers are from before any edit; re-find the text.
- `scripts/regulatory.py`: renders `<!--sba:PATH-->value<!--/sba:PATH-->` regions from sba.json. Run `python3 scripts/regulatory.py` after editing; run `python3 scripts/regulatory.py --check` to confirm nothing is stale.

## Classify every inventory row of your cluster

- CURRENT: still true under 8.1 (for example the 51%/60% occupancy test, the transient test, the 10% start-up injection, a Standard 7(a) 1.15x floor on a start-up, 13 CFR 120.160(b) "may require"). No change.
- STALE_CITATION: only the version or date is wrong ("SOP 50 10 8", "effective June 1, 2025", "under 50 10 8"). Change the citation to the 8.1 name and date; wording otherwise untouched.
- STALE_RULE: the value or rule changed (a 1.15x floor on an acquisition, a $250,000 valuation threshold, SBSS, 504 at 1:1 or 1.0x, $90,000 per job, 120-day financial statements, 24-month seller note seasoning, 12-month seller consulting, 7(a) Small barred from acquisitions, a 75% or 51% 504 equipment test, a combined limit other than $10 million). Replace the value or rule with the register's.
- UNVERIFIABLE: a rule, figure or threshold attributed to SBA that no register row verifies (for example a debenture rate, "equity injection commonly 15 to 20%+" presented as an SBA rule, a fixed-rate spread, a packaging fee cap). Soften to "SBA's 8.1 guidance on this point should be confirmed with the lender" with no figure, or drop the figure if the sentence does not need it. A market observation that is not attributed to SBA (a lender's typical practice, clearly labelled as such) may stay.
- HISTORICAL: a statement about what an earlier SOP said, kept on purpose. Wrap it: add `data-historical="SOP 50 10 8"` (or the edition named) to the enclosing element (table, tr, td, li, p or span). Use this only where the page is deliberately comparing editions.

Many inventory rows are noise (a "jobs" or "occupancy" hit that is not an SBA rule, or a provisional id that is wrong). Classify those CURRENT with resolution "not an SBA rule statement" and fix the register_id to the right row or leave it.

## Editing rules (constraints 1 to 7 of the charter)

1. Primary text governs. Publish a figure only if a REGISTER row with status VERIFIED, CHANGED or CONFLICT_RESOLVED carries it. Never introduce a figure from memory or from another website.
2. Never write the sister-firm names. The four forbidden strings of charter constraint 2 (given to you in your task message, any case) must not appear in any file you touch. If a page you edit already contains one in a sentence you are changing, remove the name from that sentence; if it sits in a sentence you are not otherwise changing, leave it and list it in your report under "pre-existing names".
3. Original prose. Write your own sentences; do not copy from the register's notes or from research documents.
4. Surgical edits. Change only the sentence, table cell, list item, JSON-LD string, meta description or source line that carries an SBA rule, version, date, rate or fee. Do not rewrite surrounding copy, headings or layout. Keep the page's voice.
5. Case math stays honest (cluster E). If a case's numbers rely on a rule 8.1 changed, recompute from the case's own inputs with a short Python script saved to `docs/web-fsc-2/clusters/recompute-<case>.py`; update the affected rows; change the conclusion sentence only if the answer changes; log before and after. A ground-up or start-up case tested against a 1.15x Standard 7(a) floor does not change (that floor is unchanged, register R28). An acquisition case tested against 1.15x on projections DOES change: the floor is 1.25x on historical EBITDA (R09, R11) unless it is an owner-occupied special purpose acquisition the appraised value fully supports.
6. Credentials: never type "Ph.D.", "CCIM" or "MAI" next to the name Mark Otava. Do not edit anything between `<!--fsc:` and `<!--/fsc:` markers (bylines, signatures, author JSON-LD).
7. Historical statements stay historical, wrapped as above.

Dates: do NOT change dateModified, "Updated" or "Reviewed" lines or the sitemap; the main session sets them for every changed file.

Prefer a data-file marker wherever a value sits in plain text and the page format allows it without a layout change, for example:
`<!--sba:dscr.coo_initial_acquisition.value-->1.25x<!--/sba:dscr.coo_initial_acquisition.value-->` or `<!--sba:sop.name-->SOP 50 10 8.1 with Technical Policy Updates<!--/sba:sop.name-->` or `<!--sba:sop.effective {"fmt": "date"}--><time datetime="2026-10-01">October 1, 2026</time><!--/sba:sop.effective-->`. Marker paths are the dotted keys of sba.json (a dict with a "value" key resolves to that value). Inside a JSON-LD string or an HTML attribute (content="..."), you cannot use a marker: edit the text directly and list the file under HARDCODED in your report.

Where a page states the SOP, write the full name at first mention, "SOP 50 10 8.1 with Technical Policy Updates (effective October 1, 2026)", and "SOP 50 10 8.1" after that. Never leave "SOP 50 10 8" standing as the current edition, and never write "50 10 7".

## Asset-class specifics (clusters B and C, and the matching cases in E)

- Special purpose types (car wash, gas station, hotel and lodging, marina, nursing and assisted living, funeral home with crematorium, medical facilities, service centers with pits): state the 8.1 rules from the register where the page discusses SBA: 504 contribution 15% (20% if also a new business) (R31); the 10-year acquisition amortization with the special purpose exemption of up to 25 years when 85% or more of the use of total project costs is real estate (R25); the projection exception for an owner-occupied special purpose acquisition whose price the appraised value fully supports (R11); the going-concern appraisal with four comparable assignments in 36 months (R21).
- Marinas, RV parks, campgrounds, hotels and lodging: the transient test exactly as R42 words it (more than 50% of the prior year's revenue from transients staying 30 days or less; a start-up shows it in projections). Boat slips and docks count as rentable property (R32).
- Acquisition-heavy types (gas station, car wash, restaurant, laundromat, funeral home, veterinary, childcare, auto service): the four Appendix 15 categories and their floors (R08, R09), the 10% injection that cannot be reduced for an Initial Acquisition (R13), the $350,000 internal valuation threshold (R21), the $3 million QoE threshold with its exemptions (R23), the 36-month seller note and 24-month consulting rules (R17, R19).
- Self-storage, restaurants, day care: not on SBA's special purpose list; do not call them "listed". Appendix 15 names storage units as an example of a special purpose acquisition the real estate fully secures (R44). Do not call restaurants or day care "expressly multipurpose"; the SOP does not say that.
- The combined limit is $10 million only when the 7(a) loan is approved first (R38). Jobs: $95,000 per job, $150,000 small manufacturers and energy (R37). FY2027 fees and waivers: R49 to R53. SBSS is gone (R27).

## Report

Write `docs/web-fsc-2/clusters/<X>.md` with:
1. A table of every inventory row of your cluster: file, line (original), classification, register_id (final), resolution (what you did, in a few words).
2. Every change as before / after / register id (quote the old and new text).
3. HARDCODED: files where a value had to be edited as text (JSON-LD, attributes, tables whose format did not allow a marker).
4. Pre-existing names: files and lines where a forbidden name sits in text you did not change.
5. Cluster E only: every recomputation with the script path, inputs, before and after figures, and whether the conclusion sentence changed.
6. Anything you could not resolve, with the reason.

Keep the report factual. Do not write the forbidden strings in it. When done, run `python3 scripts/regulatory.py --check`, then `git diff --stat -- <your files>`, and reply with a 10-line summary: rows classified by class, files changed, recomputations, open items.
