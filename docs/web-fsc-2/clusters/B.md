# WEB-FSC-2 cluster B report

Files: 14 asset-class pages (assisted-living-and-memory-care through laundromat). 796 inventory rows. Classes were assigned by statement-keyword rules checked against the page text (STALE_CITATION 314, STALE_RULE 106, UNVERIFIABLE 22, CURRENT 354, HISTORICAL 0 by row; the two deliberate historical wraps, coffee-shop s22 source line and childcare environmental sentence, are listed under changes). Rows repeat because each page carries its SBA text three times (JSON-LD FAQ, visible body, FAQ accordion), and all three were edited together.

## 2. Changes (before / after / register id)

Version and date, all 14 files (R01 to R06): "SOP 50 10 8, effective June 1, 2025" / "SOP 50 10 8 (effective June 1, 2025)" -> "SOP 50 10 8.1 with Technical Policy Updates (effective October 1, 2026)" via sop.name / sop.effective markers in body text (plain text in JSON-LD); bare "SOP 50 10 8" -> sop.short marker or plain "SOP 50 10 8.1". Auto-dealership also lost "; revised September 30, 2025" and "with revisions effective September 30, 2025"; car wash lost "; Procedural Notice effective September 30, 2025"; glamping lost "with technical updates effective March 1, 2026"; childcare lost "technical update May 29, 2025".

Valuation threshold (R21), "$250,000 goodwill / financed amount" -> "Business Purchase Price above $350,000" (valuation.internal_valuation_max marker in body, plain in JSON-LD), buyer-seller "related" -> "closely related":
- auto-service-and-collision: FAQ, body, decision table, comparison cell, source s20.
- coffee-shop: body ("financed amount minus appraised real estate and equipment exceeds $250,000" -> "Business Purchase Price exceeds $350,000"), decision row; source s27 clause wrapped data-historical="SOP 50 10 8" and noted as replaced by the $350,000 threshold.
- express-car-wash: FAQ, body, decision row, source s10.
- funeral-home: FAQ, body, comparison cell, source s21.
- gas-station-and-c-store: FAQ, body, source s23 (four places).
- glamping: FAQ, body, source s16 ("independent going-concern appraisal where intangible portion exceeds $250,000" -> "independent business valuation where the Business Purchase Price exceeds $350,000").
- laundromat: FAQ, body, source s17 ("financed goodwill or intangibles exceed $250,000" -> Business Purchase Price above $350,000).

SBSS (R27): behavioral-health (FAQ, body, table cell, source s19) "raised the minimum SBSS score from 155 to 165 and restored pre-2021 underwriting" -> "SBA has retired the SBSS credit-score screen for 7(a) Small loans, and SOP 50 10 8.1 does not use it" (table "SBSS min raised 155->165" -> "SBSS screen retired"). childcare-and-daycare (FAQ, body, table, source s26) "minimum SBSS score of 165" -> "SBSS score screen has been retired"; also dropped "reinstated tax-transcript verification" (unverifiable) and "lowered the 7(a) Small Loan threshold" -> "7(a) Small Loan ceiling is $350,000" (R26). glamping source s16 "SBSS minimum of 165" -> "SBSS screen retired".

Franchise Directory (R41): "was reinstated / the SBA reinstated / the reinstated Directory" -> "applies / listing required" on childcare, coffee-shop, fitness, hotel.

504 contribution (R31) replacing UNVERIFIABLE "15 to 20 percent or more" style equity:
- express-car-wash (FAQ, body, table, source): "typically 15 percent on 504" -> "15 percent (20 percent if the borrower is also a new business)", 10% injection kept for start-ups and Initial Acquisitions (R13/R29).
- gas-station-and-c-store (FAQ, body, table, source s26): "commonly 15 to 20 percent or more" -> 504 contribution 15 percent, 20 percent if also a new business; table "~1.15x+ DSCR (504)" -> "504 DSCR 1.15x (historical)" (R30).
- glamping (FAQ, body, table, source): "10 percent minimum (effectively higher for startups) / up to 25% for startups" -> 10 percent on 7(a) start-ups included; 504 15 percent (new business or special purpose), 20 percent both; table DSCR "1.25x+" -> "Standard 7(a) 1.15x (1.25x on a change of ownership)" (R28, R09).
- hotel (FAQ, body, table, source s10): "higher equity, 15 percent ... 20 percent if also a startup" -> "a 504 loan also asks a higher borrower contribution ... new business".
- fitness: "10 percent minimum equity injection was restored / for new businesses" -> "applies to start-ups" (R29).
- hotel: "triggers a mandatory third-party feasibility study for virtually all hotel 7(a) and 504 applications" -> "SBA may require a third-party feasibility study under 13 CFR 120.160(b), and lenders commonly do" (R43, UNVERIFIABLE softened).

Transient test (R42), glamping (FAQ, body, FAQ accordion): "more than half of its revenue comes from stays of under 30 days" -> "more than 50 percent of the prior year's revenue comes from transients who stay 30 days or less at a time (a start-up shows this in projections)".

Mixed-purpose maturity (R33), coffee-shop (FAQ, accordion, source s27): "up to 25 years when real estate is involved" -> "up to 25 years when 51 percent or more of proceeds are real estate (not for a change of ownership)".

Special purpose scope (R44), funeral-home (3 places): "Because funeral homes are special-purpose property" -> "Because a funeral home with a crematorium is special-purpose property".

Laundromat table: "~1.25x DSCR" -> "1.25x DSCR on an acquisition (historical)" (R09).

Historical wraps: childcare-and-daycare, sentence "Under SOP 50 10 8, 504 environmental review was streamlined ..." wrapped in span data-historical="SOP 50 10 8"; source s26 mention of it removed. coffee-shop source s22 clause wrapped (above).

## 3. HARDCODED (edited as text, no marker possible)
All 14 files: JSON-LD FAQPage answer (SOP name/date, $350,000, SBSS, 504 contribution and similar). Also plain-text table cells and source-list sentences (the $350,000 or 504 contribution wording is plain where it sits in cells or inline prose): auto-service-and-collision, coffee-shop, express-car-wash, funeral-home, gas-station-and-c-store, glamping, hotel, laundromat (cells/sources), behavioral-health, childcare-and-daycare, fitness-and-recreation (cells/sources).

## 4. Pre-existing names (not changed; the sister-firm names appear in text I did not edit)
assisted-living-and-memory-care 1357; coffee-shop 1391; express-car-wash 1024, 1035, 1375, 1383, 1393; fitness-and-recreation 1376, 1379; gas-station-and-c-store 1414; glamping 706, 709, 987, 1025, 1038, 1316, 1328, 1401, 1408, 1409, 1415, 1419 (post-edit line numbers approximate, +/- 2); hotel 1023, 1364. One name was removed from a changed line (glamping table-source line: the clause naming the firm as underwriting commentary became "Sage underwriting commentary"). No forbidden string appears in any added line.

## 6. Open items
- Environmental, not in register, left untouched: "loans over $250,000 require an environmental questionnaire and Records Search" (gas-station-and-c-store FAQ, JSON-LD, body, source s24); gas station source s24 cites "SOP 50 10 8.1, Chapter 5 Section E and Appendix 7" after a mechanical version change: chapter numbers not verified against 8.1.
- Auto-service-and-collision: "SBA Franchise Directory returned June 1, 2025 (franchisor recertification by July 31, 2025)", "loan capped at the lower of purchase price or appraised value": left, history/unverified. Coffee-shop source s27: "36-month re-appraisal rule", collateral valuation caps (85/75/50%), July 31, 2025 deadline: unverified, left.
- Auto-dealership: "businesses with any non-US-citizen ownership are ineligible"; glamping: "100 percent U.S.-citizen or LPR ownership": no register row, left.
- Childcare: dropped "reinstated tax-transcript verification" and "streamlined 504 environmental review" from the source line (SOP 8 claims, not verifiable).
- Not added: DSCR floors (R08/R09), QoE $3 million (R23), 10-year amortization with 25-year special purpose exemption (R25), seller note 36 months / consulting 24 months (R17/R19) where an acquisition-heavy page (funeral-home, laundromat, gas-station, car wash, coffee-shop, childcare) does not already discuss them; hotel does not state the R42 transient test. Surgical-edit rule applied; the main session may want one added sentence per page.
- Other non-SBA-rule figures left as market statements: hotel "1.15x to 1.25x" lender DSCR, glamping "1.25x-plus" conservative DSCR, USDA B&I terms.
- dateModified / Updated lines untouched.

## 1. Row table (file, original line, class, final register id, resolution)

| file | line | class | register_id | resolution |
|---|---|---|---|---|
| assisted-living-and-memory-care | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 705 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| assisted-living-and-memory-care | 705 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| assisted-living-and-memory-care | 705 | CURRENT | R25 | not an SBA rule statement |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 707 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 948 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| assisted-living-and-memory-care | 949 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1079 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1152 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| assisted-living-and-memory-care | 1152 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1153 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1153 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1153 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1153 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1153 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1161 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1161 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1168 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1168 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1168 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1174 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1174 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1175 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1176 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1196 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1196 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| assisted-living-and-memory-care | 1196 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1222 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1289 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1356 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| assisted-living-and-memory-care | 1359 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1360 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| assisted-living-and-memory-care | 1362 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| auto-dealership | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-dealership | 707 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 707 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1193 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| auto-dealership | 1199 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1199 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1212 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1212 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1212 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1397 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1397 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-dealership | 1397 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 709 | CURRENT | R21 | not an SBA rule statement |
| auto-service-and-collision | 709 | CURRENT | R21 | not an SBA rule statement |
| auto-service-and-collision | 952 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 953 | CURRENT | R37 | not an SBA rule statement |
| auto-service-and-collision | 1144 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 1183 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1183 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1183 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1183 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1183 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1184 | CURRENT | R37 | not an SBA rule statement |
| auto-service-and-collision | 1185 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1190 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1190 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1190 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1195 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1197 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 1197 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1208 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1209 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1213 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| auto-service-and-collision | 1219 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1219 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1220 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 1220 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| auto-service-and-collision | 1247 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1306 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| auto-service-and-collision | 1322 | CURRENT | R21 | not an SBA rule statement |
| auto-service-and-collision | 1322 | CURRENT | R21 | not an SBA rule statement |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1392 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| auto-service-and-collision | 1393 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1393 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1393 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| auto-service-and-collision | 1394 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| auto-service-and-collision | 1394 | CURRENT | R50 | not an SBA rule statement |
| behavioral-health | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 952 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| behavioral-health | 1011 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| behavioral-health | 1155 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1155 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1155 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1155 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1155 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1163 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1163 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1284 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1284 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1284 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1284 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1284 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| behavioral-health | 1354 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| behavioral-health | 1365 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1365 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1365 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| behavioral-health | 1365 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| childcare-and-daycare | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 705 | CURRENT | R08 | not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R27 | not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R31 | not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R31 | not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R26 | not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R26 | not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R26 | 7(a) Small ceiling $350,000 kept (R26) |
| childcare-and-daycare | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 955 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| childcare-and-daycare | 1208 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1211 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| childcare-and-daycare | 1211 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1211 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1211 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1212 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1212 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1215 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| childcare-and-daycare | 1215 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| childcare-and-daycare | 1216 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| childcare-and-daycare | 1219 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1219 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1219 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1227 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1228 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1228 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1228 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1228 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1229 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1231 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1231 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1231 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1232 | STALE_CITATION | R41 | "reinstated" Franchise Directory wording replaced |
| childcare-and-daycare | 1233 | CURRENT | R08 | not an SBA rule statement |
| childcare-and-daycare | 1233 | CURRENT | R26 | not an SBA rule statement |
| childcare-and-daycare | 1242 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1242 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1294 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1294 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1332 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| childcare-and-daycare | 1423 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1424 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| childcare-and-daycare | 1427 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| coffee-shop | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| coffee-shop | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| coffee-shop | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| coffee-shop | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 705 | CURRENT | R34 | not an SBA rule statement |
| coffee-shop | 705 | CURRENT | R25 | not an SBA rule statement |
| coffee-shop | 707 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| coffee-shop | 1195 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| coffee-shop | 1196 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1196 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1196 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1198 | CURRENT | R37 | not an SBA rule statement |
| coffee-shop | 1203 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1203 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1203 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1212 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1212 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1213 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1231 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| coffee-shop | 1231 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| coffee-shop | 1231 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| coffee-shop | 1232 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1232 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1232 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1233 | CURRENT | R37 | not an SBA rule statement |
| coffee-shop | 1258 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| coffee-shop | 1323 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1323 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1323 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1323 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1323 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1323 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| coffee-shop | 1323 | CURRENT | R34 | not an SBA rule statement |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1415 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| coffee-shop | 1416 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| coffee-shop | 1416 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| coffee-shop | 1416 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 703 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 703 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 703 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 704 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 704 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 704 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 706 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| express-car-wash | 706 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| express-car-wash | 706 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| express-car-wash | 925 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 925 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 925 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 925 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1185 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| express-car-wash | 1185 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| express-car-wash | 1185 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| express-car-wash | 1185 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| express-car-wash | 1185 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| express-car-wash | 1186 | CURRENT | R25 | not an SBA rule statement |
| express-car-wash | 1187 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| express-car-wash | 1187 | CURRENT | R50 | not an SBA rule statement |
| express-car-wash | 1191 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1191 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1191 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1201 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 1201 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 1213 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 1214 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 1214 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 1214 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 1214 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| express-car-wash | 1217 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 1241 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1241 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1241 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1256 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1256 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1293 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 1293 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 1293 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 1297 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1297 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1297 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1301 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1378 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| express-car-wash | 1379 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| express-car-wash | 1379 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| express-car-wash | 1379 | CURRENT | R37 | not an SBA rule statement |
| express-car-wash | 1379 | CURRENT | R51 | not an SBA rule statement |
| express-car-wash | 1389 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| express-car-wash | 1389 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 704 | CURRENT | R08 | not an SBA rule statement |
| fitness-and-recreation | 704 | CURRENT | R21 | not an SBA rule statement |
| fitness-and-recreation | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 705 | CURRENT | R31 | not an SBA rule statement |
| fitness-and-recreation | 705 | CURRENT | R31 | not an SBA rule statement |
| fitness-and-recreation | 706 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| fitness-and-recreation | 859 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 950 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1170 | CURRENT | R13 | 10% injection still true (R13/R29) |
| fitness-and-recreation | 1170 | CURRENT | R13 | 10% injection still true (R13/R29) |
| fitness-and-recreation | 1170 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1171 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| fitness-and-recreation | 1171 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| fitness-and-recreation | 1171 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| fitness-and-recreation | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1186 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1186 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1190 | CURRENT | R29 | not an SBA rule statement |
| fitness-and-recreation | 1201 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1201 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1203 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| fitness-and-recreation | 1203 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| fitness-and-recreation | 1203 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| fitness-and-recreation | 1246 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1368 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| fitness-and-recreation | 1369 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| fitness-and-recreation | 1374 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| funeral-home | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| funeral-home | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 705 | CURRENT | R08 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R08 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R31 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R31 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R21 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R21 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R21 | not an SBA rule statement |
| funeral-home | 705 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| funeral-home | 857 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| funeral-home | 1171 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1171 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1172 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| funeral-home | 1172 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| funeral-home | 1172 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| funeral-home | 1173 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| funeral-home | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1185 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| funeral-home | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1187 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1190 | CURRENT | R13 | not an SBA rule statement |
| funeral-home | 1190 | CURRENT | R15 | not an SBA rule statement |
| funeral-home | 1202 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| funeral-home | 1202 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| funeral-home | 1203 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| funeral-home | 1204 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1290 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1377 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| funeral-home | 1380 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| funeral-home | 1380 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| funeral-home | 1380 | CURRENT | R50 | not an SBA rule statement |
| gas-station-and-c-store | 688 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 703 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 703 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 704 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 706 | CURRENT | R21 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 706 | CURRENT | R21 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 859 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 953 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 954 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 954 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1026 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1094 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1186 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1186 | CURRENT | R30 | 1.15x 504 / Standard 7(a) figure current |
| gas-station-and-c-store | 1186 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1186 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1186 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| gas-station-and-c-store | 1186 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| gas-station-and-c-store | 1187 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1187 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1188 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1193 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1193 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1193 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1198 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1199 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1199 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1199 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1200 | CURRENT | R08 | not an SBA rule statement |
| gas-station-and-c-store | 1207 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1208 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1208 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1217 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1217 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1229 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1229 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1230 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1230 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1230 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1231 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1232 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1257 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1316 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1317 | CURRENT | R08 | not an SBA rule statement |
| gas-station-and-c-store | 1317 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| gas-station-and-c-store | 1317 | CURRENT | R21 | not an SBA rule statement |
| gas-station-and-c-store | 1317 | CURRENT | R21 | not an SBA rule statement |
| gas-station-and-c-store | 1317 | CURRENT | R21 | not an SBA rule statement |
| gas-station-and-c-store | 1317 | CURRENT | R35 | not an SBA rule statement |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1321 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| gas-station-and-c-store | 1325 | CURRENT | R44 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 1325 | CURRENT | R21 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 1389 | CURRENT | R37 | not an SBA rule statement |
| gas-station-and-c-store | 1401 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| gas-station-and-c-store | 1409 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1409 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1410 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| gas-station-and-c-store | 1411 | CURRENT | R01 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 1411 | CURRENT | R01 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 1411 | CURRENT | R21 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 1411 | CURRENT | R21 | environmental rule, not in register; left, open item |
| gas-station-and-c-store | 1413 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1413 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1413 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1413 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1413 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| gas-station-and-c-store | 1414 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| gas-station-and-c-store | 1418 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 688 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 704 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 704 | CURRENT | R21 | not an SBA rule statement |
| glamping | 704 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| glamping | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 705 | STALE_RULE | R42 | transient test reworded exactly as R42 |
| glamping | 706 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| glamping | 859 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 955 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1191 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| glamping | 1191 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| glamping | 1191 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| glamping | 1192 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1194 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 1194 | CURRENT | R30 | 1.15x 504 / Standard 7(a) figure current |
| glamping | 1194 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 1194 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1198 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1205 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1206 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1206 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1206 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1206 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1208 | UNVERIFIABLE | R31 | replaced with 504 contribution 15%/20% (R31) |
| glamping | 1217 | CURRENT | R33 | not an SBA rule statement |
| glamping | 1224 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1226 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1228 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 1228 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1251 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| glamping | 1252 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| glamping | 1270 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1316 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1416 | STALE_RULE | R27 | SBSS retired; text now says screen retired |
| glamping | 1417 | CURRENT | R25 | not an SBA rule statement |
| glamping | 1417 | CURRENT | R50 | not an SBA rule statement |
| grocery-store | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| grocery-store | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| grocery-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 705 | CURRENT | R31 | not an SBA rule statement |
| grocery-store | 705 | CURRENT | R31 | not an SBA rule statement |
| grocery-store | 705 | CURRENT | R15 | not an SBA rule statement |
| grocery-store | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 707 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| grocery-store | 859 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| grocery-store | 991 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| grocery-store | 1154 | CURRENT | R13 | 10% injection still true (R13/R29) |
| grocery-store | 1154 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| grocery-store | 1155 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 1155 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 1155 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 1156 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| grocery-store | 1161 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1161 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1171 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1171 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1171 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1172 | CURRENT | R13 | not an SBA rule statement |
| grocery-store | 1172 | CURRENT | R13 | not an SBA rule statement |
| grocery-store | 1172 | CURRENT | R15 | not an SBA rule statement |
| grocery-store | 1272 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1272 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1272 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1272 | CURRENT | R31 | not an SBA rule statement |
| grocery-store | 1272 | CURRENT | R31 | not an SBA rule statement |
| grocery-store | 1272 | CURRENT | R15 | not an SBA rule statement |
| grocery-store | 1272 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| grocery-store | 1272 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 1272 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 1272 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| grocery-store | 1347 | CURRENT | R04 | not an SBA citation (non-SBA source date) |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1353 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| grocery-store | 1354 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 688 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 704 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 705 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 705 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 705 | CURRENT | R30 | 1.15x 504 / Standard 7(a) figure current |
| hotel | 705 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 705 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 705 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 706 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 706 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 948 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1142 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 1143 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 1143 | CURRENT | R30 | 1.15x 504 / Standard 7(a) figure current |
| hotel | 1143 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 1170 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 1170 | CURRENT | R30 | 1.15x 504 / Standard 7(a) figure current |
| hotel | 1170 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 1170 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1172 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1177 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1177 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1184 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 1188 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1190 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1191 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1191 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1191 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1199 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1201 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| hotel | 1287 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1287 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1287 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1287 | UNVERIFIABLE | R43 | softened to 13 CFR 120.160(b) "may require" |
| hotel | 1287 | UNVERIFIABLE | R43 | softened to 13 CFR 120.160(b) "may require" |
| hotel | 1287 | UNVERIFIABLE | R43 | softened to 13 CFR 120.160(b) "may require" |
| hotel | 1287 | UNVERIFIABLE | R43 | softened to 13 CFR 120.160(b) "may require" |
| hotel | 1287 | UNVERIFIABLE | R43 | softened to 13 CFR 120.160(b) "may require" |
| hotel | 1287 | UNVERIFIABLE | R43 | softened to 13 CFR 120.160(b) "may require" |
| hotel | 1290 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 1291 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| hotel | 1291 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 1362 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1363 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| hotel | 1364 | CURRENT | R38 | program limit/test current or not an SBA rule statement |
| hotel | 1364 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| hotel | 1365 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 688 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| laundromat | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 706 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 706 | CURRENT | R08 | not an SBA rule statement |
| laundromat | 706 | CURRENT | R31 | not an SBA rule statement |
| laundromat | 706 | CURRENT | R31 | not an SBA rule statement |
| laundromat | 706 | CURRENT | R43 | not an SBA rule statement |
| laundromat | 965 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| laundromat | 1171 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| laundromat | 1171 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| laundromat | 1171 | CURRENT | R44 | going-concern/special-purpose statement consistent with R21/R44 |
| laundromat | 1172 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1172 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1172 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1173 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1173 | CURRENT | R37 | not an SBA rule statement |
| laundromat | 1174 | CURRENT | R28 | coverage floor not misstated, or not an SBA rule statement |
| laundromat | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1178 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1188 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1188 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1189 | CURRENT | R08 | not an SBA rule statement |
| laundromat | 1189 | CURRENT | R13 | 10% injection still true (R13/R29) |
| laundromat | 1189 | CURRENT | R13 | 10% injection still true (R13/R29) |
| laundromat | 1190 | CURRENT | R13 | 10% injection still true (R13/R29) |
| laundromat | 1202 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1202 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1202 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1302 | STALE_CITATION | R01 | citation changed to SOP 50 10 8.1 with Technical Policy Updates, effective October 1, 2026 |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1381 | STALE_RULE | R21 | $250,000 goodwill/financed amount replaced by $350,000 Business Purchase Price |
| laundromat | 1382 | CURRENT | R32 | 51%/60% occupancy test (R32) or not an SBA rule statement |