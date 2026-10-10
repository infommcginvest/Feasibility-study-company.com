<!-- Committed copy. Constraint 2 and gate 6 forbid four strings in any committed file, so each occurrence is replaced by a bracketed placeholder. The originals are unchanged in the owner's folder. -->

# CHARTER WEB-FSC-2: REBUILD EVERY SBA STATEMENT ON FEASIBILITY-STUDY-COMPANY.COM TO SOP 50 10 8.1 (TECHNICAL UPDATES, EFFECTIVE 1 OCTOBER 2026)

Issued 10 October 2026 for the owner. This is a heavy lane, so run the fan-out below.

| | |
|---|---|
| Session | WEB-FSC-2, main session on the strongest model; subagents on Sonnet |
| Site | feasibility-study-company.com |
| Repo | The repo WEB-FSC-1 used (read `docs/web-fsc-1/CLOSE.md`). If WEB-FSC-1 has not closed, run its step zero to find the repo. |
| Branch | `web-fsc-2`. Cut from the default branch after WEB-FSC-1 has merged; otherwise cut from the `web-fsc-1` head and record that. |
| Owner input (read only) | `~/Downloads/deep searches/fsc-sop81/` (this charter and SOP-8-1-FACT-SHEET.md) |
| Background research (read only) | `~/Downloads/deep searches/rest 4.md` (8.1 financing spine) and `~/Downloads/deep searches/maqrina batch 2.md` (marina eligibility, primary-verified SOP 8 cites) |
| Records | `docs/web-fsc-2/` (committed) |
| Deploy | Only if the paste block says `Deploy pre-authorized: yes`, and only after every gate is green |
| First action | Copy the owner input into `docs/web-fsc-2/input/` and commit it |

## Speed rules

1. Do not ask the owner questions, except for the one stop in Phase 0. Decide, log the decision in `docs/web-fsc-2/DECISIONS.md`, and keep going.
2. Never end your turn while a build, a fetch, a subagent or a gate is running.
3. Stop only for: the primary SOP text being unobtainable (Phase 0), a red gate you cannot fix in scope, or free disk under 1 GB.
4. Stage explicit paths only. No `git add -A`. No credentials in the repo or in a log.
5. Network: read-only GETs of sba.gov, legacy.sba.gov, federalregister.gov, ecfr.gov, govinfo.gov, federalreserve.gov, and the named secondary sources for cross-checks. Never work around robots.txt, a 403 or a bot check.

## The job in one paragraph

The site cites SOP 50 10 8 (effective 1 June 2025) everywhere. SOP 50 10 8.1 with Technical Updates took effect on 1 October 2026 and changed change-of-ownership underwriting (Appendix 15), DSCR floors, equity rules, valuation thresholds, amortization, 504 coverage and maturity rules, and fees. Build a primary-verified register of the 8.1 rules. Find every SBA statement on the site. Fix each one against the register. Rebuild the SBA practice hub, publish one new research note on what 8.1 changed for feasibility studies, and move the SOP version, dates, rates and fees into one data file, so the next SOP update is a one-file edit.

## Hard constraints

1. **Primary text governs.** No 8.1 rule is published unless the register shows it verified from the primary SOP text, with chapter, paragraph, page and a verbatim quote, or from a primary SBA notice, the Federal Register or eCFR. A rule that cannot be verified is dropped. If dropping it would leave a gap a reader needs, write "SBA's 8.1 guidance on this point should be confirmed with the lender" with no figure.
2. **Never cite [sister-firm-domain]** or any page of a sister firm, even where the research batches list one as a source. No page, file, commit or metadata may contain [sister-firm-abbr], [sister-firm], [sister-firm-name] or [sister-firm-2].
3. **Original prose.** The background research and the [sister-firm] drafts in the owner's folder are for facts, not wording. Do not copy sentences from them.
4. **Surgical edits outside the rebuilt pages.** On every other page, change only the sentences, table cells and citations that carry an SBA rule, version, date, rate or fee. Do not rewrite surrounding copy, layouts or headings.
5. **Case math stays honest.** If a case study's numbers rely on a rule 8.1 changed (for example a change-of-ownership deal underwritten on projections at 1.15x), recompute the affected rows from the case's own inputs with a script. Update the conclusion sentence only if the answer changes. Log every recomputation with the before and after figures.
6. **The WEB-FSC-1 credentials rule stands.** Do not type "Ph.D.", "CCIM" or "MAI" next to Mark Otava's name. Bylines come only from the author record.
7. **Historical statements stay historical.** "What changed" tables may name SOP 50 10 8 and its old values. Wrap each in the historical component or attribute defined in step 1.3, so the gates can tell history from stale claims.
8. **Scope is SBA.** USDA, HUD and EB-5 statements are out of scope. If the Federal Register has published the FY2027 OneRD B&I fee notice, note it in CLOSE.md and change nothing.

## Phase 0: get the primary text and build the register

1. Download from the SBA SOP 50 10 document page:
   - "SOP 50 10 8.1 with Technical Updates" (.docx, effective 1 October 2026);
   - the redline of the August text against the Technical Updates;
   - Information Notices 5000-882227, 5000-880695, 5000-881797 and 5000-881796;
   - Policy Notice 5000-879058;
   - Procedural Notice 5000-876777.

   Also fetch Federal Register notices 2026-20080 and 2025-19072, and eCFR 13 CFR 120.131, 120.160, 120.861, 120.910 and 120.921.
2. **Stop condition.** If the 8.1 .docx cannot be downloaded within these network rules, stop and tell the owner exactly this: "Download 'SOP 50 10 8.1 with Technical Updates' (.docx) and the redline from legacy.sba.gov/document/sop-50-10-lender-development-company-loan-programs into ~/Downloads/deep searches/fsc-sop81/, then rerun." Do not proceed on secondary sources.
3. Convert the .docx to text with pandoc or python-docx, keeping headings and page markers where the file carries them. Commit the text extract to `docs/web-fsc-2/primary/`.
4. Build `docs/web-fsc-2/REGISTER.csv`, one row per rule in SOP-8-1-FACT-SHEET.md plus any other 8.1 rule a page on the site touches. Columns:
   - `id`, `rule`, `value_8_1`, `value_8`;
   - `status`: VERIFIED, CHANGED (the primary text differs from the fact sheet), NOT_IN_TEXT or CONFLICT_RESOLVED;
   - `section`, `paragraph`, `page`, `verbatim_quote`, `primary_url`, `checked_on`.

   Resolve each conflict flagged in the fact sheet from the primary text and record how: the trigger wording, the QoE review standard, the 7(a) Small $350,000 condition, the third-party lender change, the 85% special use threshold, the 504 51% rule and the special purpose list.
5. One subagent cross-checks the register against the redline independently. Any disagreement is resolved by the main session from the primary text and logged.

## Phase 1: central regulatory data, then the inventory

1. Create `src/data/regulatory/sba.json` (adjust the path to the site's data folder) holding:
   - the SOP name and version (`SOP 50 10 8.1 with Technical Updates`), effective date, and the issuance and update notice numbers;
   - the DSCR floors, equity rules, thresholds, amortization rules, 504 jobs ratio, combined limit, peg rate and quarter, FY2027 fee schedule and waiver categories;
   - for each value, its REGISTER `id`, so every figure traces back.
2. Add a small template helper or component so pages render these values from the data file rather than as hard-coded text wherever a page states them. Convert the SBA practice hub, the new research note and every stat block or "regulatory basis" line to use it. On other pages, convert a hard-coded value to the data file wherever the page's format allows it without layout changes. Otherwise edit the text and list the page in `HARDCODED.md`.
3. Add a `historical` wrapper (component or attribute) for "what changed" tables.
4. **Inventory.** Search all content, data, templates and generated page sources for these patterns:
   - versions and dates: `SOP 50 10`, `50 10 8`, `50 10 7`, `June 1, 2025`, `1 June 2025`, `Appendix 15`, `change of ownership`, `change-of-ownership`, `SBSS`, `Peg`;
   - coverage and equity: `DSCR`, `1.15`, `1.25`, `1.10`, `1:1`, `equity injection`, `injection`, `standby`, `earnout`, `quality of earnings`, `QoE`;
   - property and valuation: `special purpose`, `special use`, `limited purpose`, `going-concern`, `$250,000`, `$350,000`;
   - programs and limits: `7(a) Small`, `Express`, `$5 million`, `$5.5`, `$10 million`, `transient`, `30 days`, `occupancy`, `51%`, `60%`;
   - terms, fees and citations: `amortization`, `maturity`, `25 years`, `10 years`, `jobs`, `$90,000`, `$95,000`, `guaranty fee`, `upfront fee`, `120 days`, `13 CFR 120`, `required by SBA`, `SBA requires`.
5. Write `docs/web-fsc-2/INVENTORY.csv` with columns: file, URL, line, exact statement, category, and the matched REGISTER `id`.

## Phase 2: fan out the fixes

Split the inventory by cluster. Give one Sonnet subagent each cluster, with the REGISTER, the data file, constraints 1 to 7 and its file list only:

| Cluster | Pages |
|---|---|
| A | Practice areas and the analytical framework, except the SBA hub rebuilt in Phase 3 |
| B | Asset-class pages, first half alphabetically |
| C | Asset-class pages, second half |
| D | State pages and metro pages |
| E | Case studies with an SBA program (`*-sba*`), including the WEB-FSC-1 cases |
| F | Research notes and any remaining pages in the inventory |

Each subagent:

- classifies every inventory row as CURRENT (no change), STALE_CITATION (version or date only), STALE_RULE (value or rule changed), UNVERIFIABLE (drop or soften under constraint 1) or HISTORICAL (wrap);
- edits only its own files;
- returns `docs/web-fsc-2/clusters/<X>.md`, which lists every change as before, after and REGISTER `id`, plus every case recomputation with its script output.

Asset-class specifics the subagents must handle where the page discusses SBA:

- Special use and special purpose types: state the 8.1 rule from the register, including the 85% special use amortization if verified.
- Marinas, RV parks, campgrounds, hotels and other lodging: the transient test as the register words it.
- Acquisition-heavy types (gas station, car wash, restaurant, laundromat, funeral home, veterinary, childcare, auto service): the Appendix 15 categories, DSCR floors, 10% injection and the QoE and valuation thresholds.

The main session reviews every cluster report, applies or rejects each change and logs it.

## Phase 3: rebuild and add

1. **Rebuild `/practice-areas/sba-7a-504/`.** Same URL. Keep the house template and the market-first voice. Sections:
   - what 8.1 changed, as a three-column historical table: SOP 8, the August 8.1 text and 8.1 with Technical Updates;
   - change-of-ownership categories, DSCR floors and the definition of EBITDA coverage;
   - equity injection and its limited sources;
   - business valuation and QoE thresholds;
   - amortization and maturity, including special use;
   - 7(a) Small and Express;
   - 504 coverage, maturity, third-party lender term and jobs ratio;
   - the $10M combined limit;
   - FY2027 fees and waivers, with the rural county test;
   - personal financial statement age;
   - where a feasibility study fits. 13 CFR 120.160(b) says "may require". Under 8.1, acquisitions close on historical EBITDA, so the market analysis must explain trailing performance, while start-ups and special use deals still depend on projections;
   - FAQ;
   - dated primary sources.

   All values come from the data file.
2. **New research note: `/research-notes/sop-50-10-8-1-what-changed-for-feasibility-studies/`.** About 2,500 words, bylined through the author record. It explains what 8.1 means for the market and feasibility work a lender orders, asset type by asset type, using the register. Include the August text against Technical Updates reversals, because many pages that rank in search still describe the August text. Add it to the research-notes index and the sitemap.
3. **Update `/research-notes/sba-feasibility-myth/`.** Correct its "current edition" section and the 1.15:1 and equity statements against the register. Keep its argument, and set "Reviewed and updated: October 2026".
4. **Dates.** For every changed page, set `dateModified` and sitemap `lastmod` to the build date. Where a page shows a "reviewed" line, update it.

## Gates (all green before any deploy)

1. The build passes, and the page count is the baseline plus 1.
2. **Coverage.** Every INVENTORY row has a classification and a resolution; there are zero unclassified rows. Every published 8.1 figure on the site maps to a REGISTER row with status VERIFIED or CONFLICT_RESOLVED.
3. **Stale-claim grep.** Outside `historical` wrappers, built output contains none of:
   - SOP 50 10 8 presented as current: "SOP 50 10 8," or "SOP 50 10 8 (" followed by "effective June 1, 2025", or "current" within 10 words;
   - `50 10 7`;
   - SBSS described as a current requirement;
   - a 504 DSCR of 1:1 or 1.0x;
   - `$90,000` jobs;
   - a `$250,000` valuation threshold in an SBA context;
   - "required by SBA" or "SBA requires" attached to a feasibility study;
   - a combined limit other than $10 million.

   List every allowed hit inside a historical wrapper.
4. **Data file.** Every value on the SBA hub, in the new note and in the stat blocks renders from `sba.json`. Change the peg rate in a throwaway local build, confirm the pages change, then revert without committing.
5. **Case math.** Every recomputation script reruns, and its output matches the published tables.
6. **Names and sources.** `grep -riE "mmcg|mohelsky|unionmetric"` returns nothing across changed files and built output. No link to [sister-firm-domain] anywhere.
7. **Credentials.** `grep -riE "otava,? *(ph\.?d|ccim|mai)"` across source and built output returns nothing.
8. **Links and schema.** Zero new broken internal links. JSON-LD parses on every changed page. The new note carries Article, BreadcrumbList and the author `@id`.
9. **Look.** Screenshot the SBA hub, the new note, the myth note and three changed asset pages at desktop and mobile widths into `docs/web-fsc-2/look/`. Fix table overflow.
10. **Verifier pass.** One Sonnet subagent reads the REGISTER, the SBA hub and the new note cold, and reports BLOCKER or MAJOR mismatches only. Fix them.

## Deploy

- If `Deploy pre-authorized: yes` and every gate is green, deploy through the repo's normal path, dry run first where the tool supports one. Then fetch the SBA hub, the new note, the myth note and five changed pages from production: confirm HTTP 200, "SOP 50 10 8.1" present, and the sitemap listing the new note.
- Otherwise, push `web-fsc-2`, open a PR and stop.

## Close

Write `docs/web-fsc-2/CLOSE.md` covering:

- the repo and the commit you cut from;
- primary documents opened, with their dates and hashes;
- REGISTER counts by status, and every conflict and how it was resolved;
- inventory counts by classification and cluster;
- pages changed, recomputed cases with before and after figures, rules dropped as unverifiable, and the HARDCODED.md list;
- each gate with its command and result;
- the deploy id or PR link, with production checks;
- one paragraph for the owner: what to edit in `sba.json` at the next SOP release or quarterly peg change, and which notices to watch (the FY2028 fee notices in September 2027, quarterly peg rate notices, the FY2027 OneRD B&I notice).
