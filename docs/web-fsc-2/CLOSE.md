# WEB-FSC-2 close

Closed 10 October 2026. **Deployed to production** (pre-authorized). Not pushed: the remote still has no credentials.

## Repo and cut point

- Repo `~/Downloads/Feaisbility-Study-Company.com`; static HTML, Netlify publishes the repository root (site id 0a67950d-6092-49c3-8277-017897c1b865).
- `web-fsc-1` (56fe9af) was not merged (`main` = `origin/main` = d456950), so `web-fsc-2` was cut from **56fe9af** as the charter directs. Baseline 159 pages, built 160.
- Commits: 9fe5502 input · d097d30 Phase 0 · 2b1cd3b Phase 1 · 3626d3a Phase 3 · 8670d8b, 93a5219, 0a78d71 clusters · d1b3460 inventory and dates · 36c465c verifier fixes · a91093f /docs rule · this records commit.

## Primary documents opened (hashes in `primary/HASHES.txt`)

SOP 50 10 8.1 with Technical Policy Updates .docx (effective 2026-10-01, published 2026-09-25; sha256 279c7eee…); SOP 50 10 8 .docx (bf5cae03…); Information Notices 5000-882227, 5000-880695, 5000-881797, 5000-881796; Policy Notice 5000-879058; Procedural Notice 5000-876777; Federal Register 2026-20080 and 2025-19072; eCFR 13 CFR 120.131, 120.160, 120.861, 120.910, 120.921 (current to 2026-10-07); Federal Reserve H.15 (release of 2026-10-09); SBA's SOP document page and its July 7, 2026 release. No redline exists on SBA's pages; `primary/REDLINE-GENERATED-8-to-8.1TU.diff` is a paragraph diff of the two SOP texts and was used for the Phase 0.5 cross-check (`CROSSCHECK-REGISTER.md`).

## Register (`REGISTER.csv`, 71 rows)

VERIFIED 57 · CONFLICT_RESOLVED 7 · CHANGED 5 · NOT_IN_TEXT 2. Status is relative to the owner's fact sheet (DECISIONS 12).

Conflicts resolved from the text: applicability trigger (both notices quoted; "applications received by SBA on or after October 1, 2026" governs, R05); QoE review standard (lender's approved vendor review, R24; the notice's "reliance letter or secondary review" wording recorded); 7(a) Small $350,000 condition (an internal-valuation threshold, not an eligibility cap, R26); third-party lender change (the amortization cap was removed, the minimum term stays, R35); 85% special use test (85% of the use of total project costs, not value, R25); 504 "51% rule" (both editions say "majority of loan proceeds", no percentage, R34); special purpose list (self-storage, restaurants and day care are not listed; Appendix 15 names storage units and hotels as examples, R44); QoE exemption for owner-occupied special purpose acquisitions confirmed (R23); fee waiver window keyed to loan approval (R52). Dropped: the October 2026 debenture rate and the franchisor "conduct detrimental" screen (R48, R41). Nine SOP 8 to 8.1 changes the diff scan surfaced (9:1 debt-to-worth test, 90% partner-buyout test, 20 to 50% day-one line rule, site-visit scope, 504 "75% of jobs" rule, a CA SBLC cap, three refinance/ESOP deletions) appear on no page and got no row.

## Inventory (`INVENTORY.csv`, 4,022 rows, 143 files, 0 unclassified)

CURRENT 2,095 · STALE_CITATION 1,058 · STALE_RULE 650 · UNVERIFIABLE 185 · HISTORICAL 34. By cluster: A 56 · B 796 · C 665 · D 381 · E 1,457 · F 595 · hub 72. Cluster reports in `clusters/`.

## Pages changed

118 HTML pages plus sitemap, netlify.toml, `data/regulatory/sba.json`, `scripts/regulatory.py`. Rebuilt: the SBA hub. New: `/research-notes/sop-50-10-8-1-what-changed-for-feasibility-studies/` (about 3,000 words, in the research index and sitemap). Updated: the myth note (edition, floors, equity, list, sources; "Reviewed and updated: October 2026"). Every changed page carries dateModified and sitemap lastmod 2026-10-10.

Recomputed case: **veterinary-michigan-sba** (Initial Acquisition under Appendix 15: 10-year amortization on the business portion; debt service 550k to 647k; DSCR Year 2 1.30 to 1.10, Year 3 1.50 to 1.27 against the 1.25:1 floor; verdict now "feasible on projected coverage, with thin headroom"; the page states the ratios are projected because the case has no historical EBITDA). marina-maryland-sba: 504-financed, 1.15x floor governs, tables unchanged, projected-versus-historical statement added. The 34 other SBA cases are start-ups against the unchanged 1.15x Standard 7(a) floor; citations and rule text only.

Rules dropped as unverifiable on pages: lender "15 to 20%+ equity" presented as SBA policy, a "90% Made-in-America guarantee", the SOP pin-cite "Chapter 5 Section E", the franchisor conduct screen, "Restricted Appraisal Reports over $250,000", a 49.9% extended-stay carve-out, several eligibility and procedure claims softened to "confirm with the lender" (clusters B, C, E, F section 3). `HARDCODED.md` lists where values sit outside markers.

## Gates (`GATES.txt`)

1 page count 159 to 160 GREEN · 2 coverage GREEN · 3 stale-claim grep 0 hits, 33 allowed inside `data-historical` wrappers GREEN · 4 data file renders, peg changed to 9.99% in a throwaway run changed both pages and was reverted GREEN · 5 case scripts rerun and match GREEN · 6 names: none in changed files or built changed pages, no sister-domain link anywhere GREEN (30 changed pages had pre-existing market-data citations of the sister firm, now "industry research", DECISIONS 14; 11 unchanged pages keep theirs) · 7 credentials GREEN · 8 links 482 to 480 broken, 0 new; JSON-LD parses; note carries Article, BreadcrumbList, author @id GREEN · 9 screenshots in `look/` GREEN · 10 verifier 0 BLOCKER, 7 MAJOR fixed GREEN.

## Deploy

Push to `origin` failed (no credentials; the token file was not read). Deployed with the Netlify CLI from `git archive a91093f`: draft 6aca50850f1f57b286c9f7c1 (checked), production **6aca50cac15d911dc73c09ca**, live at https://feasibility-study-company.com. Production checks: hub, new note, myth note, gas station, hotel, marina, veterinary case and Florida pages HTTP 200 with "SOP 50 10 8.1"; sitemap lists the new note; `/docs/*` returns 404 (new netlify.toml rule). **Caution for the owner:** the site is linked to GitHub, so the next push to `main` will rebuild from `main` and overwrite this manual deploy unless `web-fsc-1` and `web-fsc-2` are pushed and merged first. Push both branches from this machine and merge `web-fsc-2` (it contains `web-fsc-1`).

## Left for the owner

1. Push and merge `web-fsc-1` and `web-fsc-2` before any other push to `main`.
2. Pre-existing case defects against unchanged SBA rules (not fixed, constraint 5): car-wash-texas equity 15% where a new special purpose 504 project needs 20%; the four RV and boat storage cases and medical-office-north-carolina at 10% where 15% applies; auto-dealership-texas debenture $5.40M above the $5M cap (clusters/E.md section 6).
3. The 11 unchanged pages that still cite the sister firm's abbreviation, and the WEB-FSC-1 items (truck-stop-oklahoma head, credentials record).
4. The citizenship and permanent-resident wording on several pages was softened to "confirm with the lender"; the 8.1 text limits eligibility to U.S. citizens and nationals (Section A, Chapter 1, F). A short register row and a sentence per page would settle it.
5. No FY2027 OneRD B&I fee notice was in the Federal Register as of 2026-10-10 (search of Rural Business-Cooperative Service notices since 2026-07-01); nothing was changed.

## For the next SOP release or quarterly peg change

Edit `data/regulatory/sba.json`, run `python3 scripts/regulatory.py`, and commit the pages it rewrites; `python3 scripts/regulatory.py --check` tells you if anything is stale. The quarterly Optional Peg Rate goes in `rates.peg` (value and quarter) from the Federal Register "Interest Rates" notice SBA publishes at the start of each quarter; prime goes in `rates.prime` from H.15. At a new SOP edition change `sop.*` (name, version, dates, notice numbers), then walk the register: every `value_8_1` that moved needs its data-file key updated and a new row in REGISTER.csv with the new quote, and `history.*` gains the superseded values. Watch for the FY2028 7(a) and 504 fee Information Notices in September 2027 (`fees_fy2027` becomes a new block and the waiver categories and window change), the quarterly peg notices, and the FY2027 OneRD B&I notice for the USDA pages (out of this lane's scope). Values that sit in JSON-LD and meta tags (`HARDCODED.md`) must be edited by hand.
