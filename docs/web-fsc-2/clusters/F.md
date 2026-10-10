# WEB-FSC-2 cluster F report

Scope: 16 of the cluster's files changed (9 research notes plus index.html, and 7 case studies); the other files in F-files.txt held no SBA rule or citation. The brief's rules applied; (the main session's sba-feasibility-myth page and the research-notes index were not touched; the new SOP 50 10 8.1 note was not touched). `python3 scripts/regulatory.py --check` reports 0 pages out of date.

Class totals over the 595 inventory rows: CURRENT 339, EXCLUDED 67, HISTORICAL 20, STALE_CITATION 114, STALE_RULE 47, UNVERIFIABLE 8. Note: the inventory has one row per match, so one sentence can appear in several rows; the 67 rows for the excluded files are marked EXCLUDED.

Method: rule-bearing sentences were edited by hand; every remaining plain "SOP 50 10 8" citation was converted by script (full name with the sop.name marker at first body mention, sop.short afterwards, the effective date through the sop.effective marker, plain text inside JSON-LD and attributes). Rows whose only trigger was a bare "SOP 50 10 8" in the original text are STALE_CITATION; rows not listed individually below as changes were noise or USDA, HUD and EB-5 text and were left alone.

## 1. Inventory rows

| file | line (original) | classification | register_id | resolution |
|---|---|---|---|---|
| case-studies/assisted-living-arizona-hud/index.html | 1158 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-arizona-hud/index.html | 1184 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-arizona-hud/index.html | 1367 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-arizona-hud/index.html | 1375 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/assisted-living-arizona-hud/index.html | 1375 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/assisted-living-arizona-hud/index.html | 1375 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| case-studies/assisted-living-arizona-hud/index.html | 1375 | STALE_CITATION | R28 | citation changed to 8.1 name/date |
| case-studies/assisted-living-arizona-hud/index.html | 1375 | STALE_CITATION | R21 | citation changed to 8.1 name/date |
| case-studies/assisted-living-arizona-hud/index.html | 1375 | STALE_CITATION | R21 | citation changed to 8.1 name/date |
| case-studies/assisted-living-arizona-hud/index.html | 1376 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-california-hud/index.html | 1173 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-california-hud/index.html | 1336 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-california-hud/index.html | 1370 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/assisted-living-california-hud/index.html | 1370 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/assisted-living-california-hud/index.html | 1370 | STALE_CITATION | R38 | citation changed to 8.1 name/date |
| case-studies/assisted-living-florida-hud/index.html | 1169 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-florida-hud/index.html | 1380 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-florida-hud/index.html | 1391 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-florida-hud/index.html | 1392 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-hawaii-hud/index.html | 1363 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-north-carolina-hud/index.html | 879 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-north-carolina-hud/index.html | 1132 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-north-carolina-hud/index.html | 1163 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-north-carolina-hud/index.html | 1364 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-north-carolina-hud/index.html | 1373 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-texas-hud/index.html | 1155 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/assisted-living-texas-hud/index.html | 1356 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/behavioral-health-massachusetts-conventional/index.html | 1197 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/behavioral-health-massachusetts-conventional/index.html | 1208 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 846 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 915 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1143 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1174 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1174 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1185 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1186 | CURRENT | R29 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1190 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1190 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1283 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1318 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1352 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1383 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1384 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1384 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1384 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1384 | CURRENT | R50 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/glamping-utah-usda/index.html | 1386 | STALE_RULE | R21 | $250,000 intangible test -> $350,000 Business Purchase Price (marker) |
| case-studies/grocery-store-mississippi-usda/index.html | 845 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1148 | CURRENT | R49 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1162 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1162 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1164 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1164 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1174 | CURRENT | R29 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/grocery-store-mississippi-usda/index.html | 1383 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 901 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 912 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 923 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 956 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 967 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 978 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 989 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1000 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1011 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1022 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1022 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1033 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1044 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1055 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1055 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1066 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1088 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1099 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1121 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1121 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1143 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1176 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1187 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1231 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1242 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1253 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1275 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1286 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1297 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1308 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1341 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1352 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1363 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1374 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1385 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1396 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1440 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1484 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/index.html | 1495 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 846 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1089 | CURRENT | R15 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1134 | CURRENT | R15 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1151 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1181 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1181 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1182 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1183 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1183 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1188 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1193 | CURRENT | R29 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1196 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1288 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1334 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1387 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1387 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1396 | CURRENT | R15 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-georgia-usda/index.html | 1397 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 846 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1133 | CURRENT | R15 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1183 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1183 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1184 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1185 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1185 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1197 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1197 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1197 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1199 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1200 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1286 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-north-carolina-usda/index.html | 1419 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 846 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 882 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1159 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1159 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1160 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1161 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1161 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1166 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1172 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1173 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1173 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1178 | CURRENT | R29 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1258 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1344 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1376 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1376 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1377 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/meat-processing-texas-usda/index.html | 1377 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 911 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 1223 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 1422 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 1422 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 1423 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 1423 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-arizona-agency/index.html | 1423 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-florida-agency/index.html | 1135 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-florida-agency/index.html | 1384 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-florida-agency/index.html | 1384 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-florida-agency/index.html | 1384 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-florida-agency/index.html | 1385 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-florida-agency/index.html | 1385 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-georgia-agency/index.html | 1145 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-new-york-agency/index.html | 912 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-new-york-agency/index.html | 1373 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/multifamily-new-york-agency/index.html | 1373 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/multifamily-new-york-agency/index.html | 1373 | STALE_CITATION | R32 | citation changed to 8.1 name/date |
| case-studies/multifamily-new-york-agency/index.html | 1373 | STALE_CITATION | R32 | citation changed to 8.1 name/date |
| case-studies/multifamily-new-york-agency/index.html | 1373 | STALE_CITATION | R32 | citation changed to 8.1 name/date |
| case-studies/multifamily-north-carolina-agency/index.html | 1135 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-north-carolina-agency/index.html | 1136 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-north-carolina-agency/index.html | 1136 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-north-carolina-agency/index.html | 1266 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-north-carolina-agency/index.html | 1376 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-north-carolina-agency/index.html | 1376 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-north-carolina-agency/index.html | 1376 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/multifamily-texas-agency/index.html | 1147 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/private-school-connecticut-conventional/index.html | 916 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/private-school-connecticut-conventional/index.html | 1374 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/private-school-connecticut-conventional/index.html | 1374 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/private-school-connecticut-conventional/index.html | 1374 | CURRENT | R27 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/private-school-connecticut-conventional/index.html | 1374 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/private-school-connecticut-conventional/index.html | 1375 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/private-school-connecticut-conventional/index.html | 1375 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/private-school-connecticut-conventional/index.html | 1375 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| case-studies/private-school-connecticut-conventional/index.html | 1375 | STALE_CITATION | R43 | citation changed to 8.1 name/date |
| case-studies/private-school-connecticut-conventional/index.html | 1381 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/retail-nevada-conventional/index.html | 913 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 913 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R28 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R32 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R32 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1367 | STALE_CITATION | R32 | citation changed to 8.1 name/date |
| case-studies/retail-nevada-conventional/index.html | 1369 | STALE_RULE | R38 | added: when the 7(a) loan is approved first |
| case-studies/rv-park-arizona-usda/index.html | 845 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1135 | CURRENT | R49 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1149 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1155 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1155 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1162 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1162 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1163 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1164 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1165 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1165 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1167 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1167 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1250 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1340 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1340 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1341 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1341 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1341 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1341 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1346 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-arizona-usda/index.html | 1346 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 845 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1132 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1133 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1166 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1166 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1166 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1168 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1168 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1173 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1173 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1178 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1361 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1361 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1374 | CURRENT | R42 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-maine-usda/index.html | 1375 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-ossipee-new-hampshire-usda/index.html | 916 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-ossipee-new-hampshire-usda/index.html | 1059 | CURRENT | R42 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-ossipee-new-hampshire-usda/index.html | 1093 | CURRENT | R49 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 846 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1138 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1169 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1169 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1171 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1181 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1273 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-pennsylvania-usda/index.html | 1372 | STALE_CITATION | R42 | 8.1 cite; transient test worded as R42 |
| case-studies/rv-park-pennsylvania-usda/index.html | 1372 | STALE_CITATION | R42 | 8.1 cite; transient test worded as R42 |
| case-studies/rv-park-pennsylvania-usda/index.html | 1372 | STALE_CITATION | R42 | 8.1 cite; transient test worded as R42 |
| case-studies/rv-park-pennsylvania-usda/index.html | 1372 | STALE_CITATION | R42 | 8.1 cite; transient test worded as R42 |
| case-studies/rv-park-texas-usda/index.html | 845 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1131 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1161 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1161 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1173 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1173 | CURRENT | R13 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1175 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1346 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1347 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| case-studies/rv-park-texas-usda/index.html | 1347 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 736 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 736 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 812 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 822 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 822 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 822 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 822 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 826 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 827 | STALE_RULE | R31 | 8.1 cite; 504 contribution 15/20 vs 10 |
| index.html | 827 | STALE_RULE | R31 | 8.1 cite; 504 contribution 15/20 vs 10 |
| index.html | 827 | STALE_RULE | R31 | 8.1 cite; 504 contribution 15/20 vs 10 |
| index.html | 827 | STALE_RULE | R31 | 8.1 cite; 504 contribution 15/20 vs 10 |
| index.html | 866 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 867 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 867 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 867 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 867 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1140 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1157 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1157 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1157 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| index.html | 1157 | STALE_CITATION | R28 | citation changed to 8.1 name/date |
| index.html | 1157 | STALE_CITATION | R09 | citation changed to 8.1 name/date |
| index.html | 1157 | STALE_CITATION | R44 | citation changed to 8.1 name/date |
| index.html | 1163 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1163 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1239 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1239 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1239 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| index.html | 1264 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1264 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| index.html | 1264 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| index.html | 1523 | CURRENT | R43 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1555 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1567 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1579 | CURRENT | R30 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1658 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1668 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 1668 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 1668 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 1668 | STALE_CITATION | R43 | hook attributed to 13 CFR 120.160(b) |
| index.html | 1671 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1672 | STALE_RULE | R31 | 8.1 cite; 504 contribution via markers |
| index.html | 1672 | STALE_RULE | R31 | 8.1 cite; 504 contribution via markers |
| index.html | 1672 | STALE_RULE | R31 | 8.1 cite; 504 contribution via markers |
| index.html | 1672 | STALE_RULE | R31 | 8.1 cite; 504 contribution via markers |
| index.html | 1709 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1710 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1710 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1710 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| index.html | 1710 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/break-even-occupancy-trap/index.html | 1098 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/break-even-occupancy-trap/index.html | 1098 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/break-even-occupancy-trap/index.html | 1313 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/break-even-occupancy-trap/index.html | 1442 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 807 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 1125 | HISTORICAL | R41 | wrapped as reported under SOP 8; 8.1 confirm-with-lender |
| research-notes/c-store-franchise-category/index.html | 1125 | HISTORICAL | R41 | wrapped as reported under SOP 8; 8.1 confirm-with-lender |
| research-notes/c-store-franchise-category/index.html | 1127 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 1144 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 1407 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 1408 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 1409 | HISTORICAL | R41 | Directory reinstatement wrapped; 8.1 keeps listing |
| research-notes/c-store-franchise-category/index.html | 1409 | HISTORICAL | R41 | Directory reinstatement wrapped; 8.1 keeps listing |
| research-notes/c-store-franchise-category/index.html | 1409 | HISTORICAL | R41 | Directory reinstatement wrapped; 8.1 keeps listing |
| research-notes/c-store-franchise-category/index.html | 1410 | HISTORICAL | R41 | Directory reinstatement wrapped |
| research-notes/c-store-franchise-category/index.html | 1415 | STALE_RULE | R27 | credit score 165 (SBSS) removed; SBSS retired Mar 1, 2026 |
| research-notes/c-store-franchise-category/index.html | 1464 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/c-store-franchise-category/index.html | 1464 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/c-store-franchise-category/index.html | 1464 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| research-notes/c-store-franchise-category/index.html | 1489 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/c-store-franchise-category/index.html | 1500 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/c-store-franchise-category/index.html | 1500 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/c-store-franchise-category/index.html | 1501 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1172 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1321 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1322 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1324 | CURRENT | R49 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1327 | CURRENT | R50 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1375 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/five-usda-components-applied/index.html | 1375 | CURRENT | R50 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/franchise-vs-non-franchise/index.html | 1031 | HISTORICAL | R41 | prior SOP edition named without its number |
| research-notes/franchise-vs-non-franchise/index.html | 1031 | HISTORICAL | R41 | prior SOP edition named without its number |
| research-notes/franchise-vs-non-franchise/index.html | 1040 | HISTORICAL | R41 | wrapped; 8.1 keeps Directory requirement |
| research-notes/franchise-vs-non-franchise/index.html | 1040 | HISTORICAL | R41 | wrapped; 8.1 keeps Directory requirement |
| research-notes/franchise-vs-non-franchise/index.html | 1040 | HISTORICAL | R41 | wrapped; 8.1 keeps Directory requirement |
| research-notes/franchise-vs-non-franchise/index.html | 1058 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/franchise-vs-non-franchise/index.html | 1058 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/franchise-vs-non-franchise/index.html | 1085 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/franchise-vs-non-franchise/index.html | 1110 | HISTORICAL | R41 | wrapped as SOP 8 statement |
| research-notes/franchise-vs-non-franchise/index.html | 1110 | HISTORICAL | R41 | wrapped as SOP 8 statement |
| research-notes/franchise-vs-non-franchise/index.html | 1133 | STALE_RULE | R38 | added: when the 7(a) loan is approved first |
| research-notes/franchise-vs-non-franchise/index.html | 1134 | STALE_RULE | R38 | sequencing qualifier added in the sentence |
| research-notes/franchise-vs-non-franchise/index.html | 1134 | STALE_RULE | R38 | sequencing qualifier added in the sentence |
| research-notes/franchise-vs-non-franchise/index.html | 1135 | CURRENT | R38 | unchanged |
| research-notes/franchise-vs-non-franchise/index.html | 1359 | UNVERIFIABLE | R41 | eligibility claim softened |
| research-notes/franchise-vs-non-franchise/index.html | 1359 | UNVERIFIABLE | R41 | eligibility claim softened |
| research-notes/franchise-vs-non-franchise/index.html | 1413 | CURRENT | R38 | already says sequence 7(a) first |
| research-notes/franchise-vs-non-franchise/index.html | 1415 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/franchise-vs-non-franchise/index.html | 1474 | HISTORICAL | R06 | 8.1 first; earlier editions wrapped |
| research-notes/franchise-vs-non-franchise/index.html | 1474 | HISTORICAL | R06 | 8.1 first; earlier editions wrapped |
| research-notes/franchise-vs-non-franchise/index.html | 1474 | HISTORICAL | R06 | 8.1 first; earlier editions wrapped |
| research-notes/franchise-vs-non-franchise/index.html | 1474 | HISTORICAL | R06 | 8.1 first; earlier editions wrapped |
| research-notes/franchise-vs-non-franchise/index.html | 1521 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 806 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 807 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 994 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1232 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1232 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1232 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1233 | CURRENT | R44 | definition quote aligned to R44 |
| research-notes/hospitality-str-report/index.html | 1244 | STALE_RULE | R31 | 504 contribution wording (new business, not start-up) |
| research-notes/hospitality-str-report/index.html | 1245 | CURRENT | R31 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1247 | CURRENT | R01 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1247 | CURRENT | R01 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1247 | CURRENT | R29 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1258 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1258 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/hospitality-str-report/index.html | 1381 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1381 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1381 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1381 | STALE_CITATION | R21 | citation changed to 8.1 name/date |
| research-notes/hospitality-str-report/index.html | 1390 | UNVERIFIABLE | R43 | "may" attributed to 13 CFR 120.160(b) |
| research-notes/hospitality-str-report/index.html | 1390 | UNVERIFIABLE | R43 | "may" attributed to 13 CFR 120.160(b) |
| research-notes/hospitality-str-report/index.html | 1391 | UNVERIFIABLE | R43 | section-of-SOP claim replaced by confirm-with-lender |
| research-notes/hospitality-str-report/index.html | 1391 | UNVERIFIABLE | R43 | section-of-SOP claim replaced by confirm-with-lender |
| research-notes/index.html | 693 | EXCLUDED |  | excluded file |
| research-notes/index.html | 920 | EXCLUDED |  | excluded file |
| research-notes/index.html | 921 | EXCLUDED |  | excluded file |
| research-notes/office-repurposing/index.html | 1243 | STALE_RULE | R38 | added sequencing qualifier |
| research-notes/office-repurposing/index.html | 1243 | STALE_RULE | R38 | added sequencing qualifier |
| research-notes/office-repurposing/index.html | 1244 | CURRENT | R38 | unchanged |
| research-notes/office-repurposing/index.html | 1373 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1206 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1206 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1206 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1214 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1220 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1220 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1257 | CURRENT | R50 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-default-economics/index.html | 1343 | HISTORICAL | R06 | SOP 8 re-tightening wrapped |
| research-notes/sba-default-economics/index.html | 1343 | HISTORICAL | R06 | SOP 8 re-tightening wrapped |
| research-notes/sba-default-economics/index.html | 1343 | HISTORICAL | R06 | SOP 8 re-tightening wrapped |
| research-notes/sba-default-economics/index.html | 1348 | STALE_RULE | R38 | added sequencing qualifier |
| research-notes/sba-default-economics/index.html | 1348 | STALE_RULE | R38 | added sequencing qualifier |
| research-notes/sba-default-economics/index.html | 1402 | CURRENT | R32 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/sba-feasibility-myth/index.html | 792 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 793 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 793 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 805 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 806 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 806 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 807 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 947 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 950 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 950 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 980 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 999 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1058 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1063 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1063 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1066 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1066 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1067 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1067 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1067 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1068 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1068 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1069 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1073 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1074 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1074 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1075 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1091 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1091 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1093 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1096 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1104 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1113 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1122 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1131 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1148 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1148 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1154 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1154 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1155 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1155 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1158 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1159 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1159 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1160 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1170 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1177 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1188 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1268 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1280 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1281 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1316 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1321 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1326 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1326 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1326 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1327 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1327 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1328 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1332 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1332 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1333 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1339 | EXCLUDED |  | main session already updated |
| research-notes/sba-feasibility-myth/index.html | 1376 | EXCLUDED |  | main session already updated |
| research-notes/special-purpose-property-risk/index.html | 791 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 792 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 793 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 804 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 947 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1001 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1001 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1002 | CURRENT | R04 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1002 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1025 | STALE_RULE | R44 | list wording: no count, same list as 8, non-exhaustive |
| research-notes/special-purpose-property-risk/index.html | 1025 | STALE_RULE | R44 | list wording: no count, same list as 8, non-exhaustive |
| research-notes/special-purpose-property-risk/index.html | 1025 | STALE_RULE | R44 | list wording: no count, same list as 8, non-exhaustive |
| research-notes/special-purpose-property-risk/index.html | 1032 | STALE_RULE | R44 | multipurpose claim removed; not on the list |
| research-notes/special-purpose-property-risk/index.html | 1034 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1140 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1164 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1165 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1264 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1264 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1265 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1266 | STALE_RULE | R31 | equity became 504 borrower contribution; citation to 8.1 |
| research-notes/special-purpose-property-risk/index.html | 1266 | STALE_RULE | R31 | equity became 504 borrower contribution; citation to 8.1 |
| research-notes/special-purpose-property-risk/index.html | 1266 | STALE_RULE | R31 | equity became 504 borrower contribution; citation to 8.1 |
| research-notes/special-purpose-property-risk/index.html | 1267 | CURRENT | R31 | 15%/20% kept (504 contribution) |
| research-notes/special-purpose-property-risk/index.html | 1271 | STALE_CITATION | R21 | QuickRead/SOP 8 cite replaced by 8.1; four appraisals in 36 months |
| research-notes/special-purpose-property-risk/index.html | 1272 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1272 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1288 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1294 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1318 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1318 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1318 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1353 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/special-purpose-property-risk/index.html | 1354 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/special-purpose-property-risk/index.html | 1354 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/trade-area-is-the-study/index.html | 1197 | CURRENT | R01 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/trade-area-is-the-study/index.html | 1197 | CURRENT | R01 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/trade-area-is-the-study/index.html | 1197 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/trade-area-is-the-study/index.html | 1201 | STALE_RULE | R09 | 8.1 name; added 1.25 initial acquisition |
| research-notes/trade-area-is-the-study/index.html | 1201 | STALE_RULE | R09 | 8.1 name; added 1.25 initial acquisition |
| research-notes/trade-area-is-the-study/index.html | 1201 | STALE_RULE | R09 | 8.1 name; added 1.25 initial acquisition |
| research-notes/trade-area-is-the-study/index.html | 1202 | STALE_RULE | R09 | 1.15 and 1.1 kept; acquisition floor added |
| research-notes/trade-area-is-the-study/index.html | 1202 | STALE_RULE | R09 | 1.15 and 1.1 kept; acquisition floor added |
| research-notes/trade-area-is-the-study/index.html | 1203 | CURRENT | R27 | 1.1 for 7(a) Small kept |
| research-notes/trade-area-is-the-study/index.html | 1203 | CURRENT | R27 | 1.1 for 7(a) Small kept |
| research-notes/trade-area-is-the-study/index.html | 1303 | UNVERIFIABLE | R43 | mandatory feasibility claim -> 13 CFR 120.160(b), lenders expect |
| research-notes/trade-area-is-the-study/index.html | 1303 | UNVERIFIABLE | R43 | mandatory feasibility claim -> 13 CFR 120.160(b), lenders expect |
| research-notes/trade-area-is-the-study/index.html | 1374 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/trade-area-is-the-study/index.html | 1374 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/trade-area-is-the-study/index.html | 1374 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| research-notes/underserved-gas-station-markets/index.html | 1292 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/underserved-gas-station-markets/index.html | 1293 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/underserved-gas-station-markets/index.html | 1293 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/underserved-gas-station-markets/index.html | 1354 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/usda-rd-deadline-calendar/index.html | 1088 | CURRENT | R38 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/usda-rd-deadline-calendar/index.html | 1088 | CURRENT | R49 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 793 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 793 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 805 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 805 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 950 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 950 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 989 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 989 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1004 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1004 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1029 | STALE_CITATION | R01 | 8.1 name and date; SOP 8 kept as historical |
| research-notes/why-feasibility-studies-fail-review/index.html | 1029 | STALE_CITATION | R01 | 8.1 name and date; SOP 8 kept as historical |
| research-notes/why-feasibility-studies-fail-review/index.html | 1029 | STALE_CITATION | R01 | 8.1 name and date; SOP 8 kept as historical |
| research-notes/why-feasibility-studies-fail-review/index.html | 1030 | STALE_CITATION | R01 | 8.1 name and date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1030 | STALE_CITATION | R01 | 8.1 name and date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1046 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1053 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1055 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1055 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1055 | CURRENT | R26 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1055 | CURRENT | R26 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1056 | CURRENT | R27 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1182 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1183 | STALE_RULE | R09 | added 1.25x initial acquisition; 8.1 cite |
| research-notes/why-feasibility-studies-fail-review/index.html | 1184 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1199 | STALE_RULE | R09 | 8.1 cite; acquisition 1.25x note |
| research-notes/why-feasibility-studies-fail-review/index.html | 1199 | STALE_RULE | R09 | 8.1 cite; acquisition 1.25x note |
| research-notes/why-feasibility-studies-fail-review/index.html | 1199 | STALE_RULE | R09 | 8.1 cite; acquisition 1.25x note |
| research-notes/why-feasibility-studies-fail-review/index.html | 1200 | CURRENT | R27 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1200 | CURRENT | R26 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1200 | CURRENT | R26 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1201 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1207 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1207 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1235 | CURRENT | R21 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1236 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1236 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1236 | STALE_CITATION | R21 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1277 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1341 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1359 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1359 | CURRENT | R28 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1361 | CURRENT | R33 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1371 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1371 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1371 | STALE_CITATION | R04 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1378 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1378 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1378 | STALE_CITATION | R28 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1388 | CURRENT | R44 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1389 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1389 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1389 | STALE_CITATION | R28 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1390 | CURRENT | R09 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| research-notes/why-feasibility-studies-fail-review/index.html | 1412 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| research-notes/why-feasibility-studies-fail-review/index.html | 1412 | STALE_CITATION | R01 | citation changed to 8.1 name/date |
| the-practice/index.html | 1077 | CURRENT | R01 | already 8.1 |
| the-practice/index.html | 1077 | CURRENT | R01 | already 8.1 |
| the-practice/index.html | 1077 | CURRENT | R43 | already 8.1 |
| the-practice/index.html | 1078 | CURRENT | R39 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| the-practice/index.html | 1144 | CURRENT | R39 | not an SBA rule statement or unchanged (market/USDA/date noise) |
| the-practice/index.html | 1177 | CURRENT | R01 | already 8.1 |
| the-practice/index.html | 1177 | CURRENT | R01 | already 8.1 |
| the-practice/index.html | 1177 | CURRENT | R43 | already 8.1 |

## 2. Changes (before / after / register id)

Every plain "SOP 50 10 8 (effective June 1, 2025)" in a source line, card, table cell or sentence became "SOP 50 10 8.1 with Technical Policy Updates" (first body mention) or "SOP 50 10 8.1" with "effective October 1, 2026" (R01, R04); about 60 such substitutions across the 16 changed files (see `git diff`). Rule changes and other edits:

- special-purpose-property-risk: "technical update effective March 1, 2026 ... specific use" -> 8.1 name/date and the R44 definition wording (no "specific"); "reinstates the full example list of roughly twenty-five special-purpose types" -> "carries a non-exhaustive example list ..., the same list as SOP 50 10 8" (SOP 8 wrapped data-historical) (R44); "treats restaurants, daycares, and mini-storage as multipurpose ... on the theory ..." -> "restaurants, daycares, and self-storage are simply not on it" plus a note that Appendix 15 names "storage units" as a fully secured special purpose acquisition example (R44); "higher equity injection" -> "On a 504 loan ... higher borrower contribution" (R31); "Per QuickRead's analysis of SOP 50 10 8 ... similar special-use businesses" -> "Under SOP 50 10 8.1 ... equivalent special-use property within the last 36 months" (R21, per brief); sources line: QuickRead's SOP 8 analysis wrapped historical; NAICS "classed multipurpose" -> "not on SBA's special-purpose list" (R44); CTA "the independent analysis SBA SOP 50 10 8 expects" -> "may require under 13 CFR 120.160(b)" (R43).
- why-feasibility-studies-fail-review: governing-edition paragraph rewritten to 8.1 (applies_to marker), SOP 8 wrapped historical, SOP 50 10 7.1 reference removed; definition quote to R44 wording; "minimum projected DSCR of 1.15x" -> "minimum DSCR of 1.15x ... (1.25x on historical EBITDA for a 7(a) initial acquisition)" (R28, R09); table note adds the acquisition floor; sources paragraph to 8.1 and "(13 CFR 120.160(b))" added to the discretionary caveat (R43).
- hospitality-str-report: 8.1 name/date; definition quote to R44; two quotations attributed to the SOP (four appraisals in 36 months, separate component values) converted to paraphrase because the register does not carry the verbatim text; the "Restricted Appraisal Reports ... over $250,000" sentence dropped (not in the register); 504 "equity injection" -> "borrower contribution", "start-up" -> "new business" (R31, R55); the feasibility "hook" attributed to 13 CFR 120.160(b), "enumerates" risk patterns -> "lenders commonly read" (R43).
- franchise-vs-non-franchise: "SOP 50 10 7, effective August 1, 2023" -> "the SOP edition effective August 1, 2023" (the old number is forbidden); Directory reinstatement sentence wrapped historical, followed by "8.1 keeps that requirement" (R41); "control as standalone affiliation test" sentence wrapped historical (not in register); "SOP 50 10 8 makes residential facilities ... ineligible" -> eligibility question, confirm 8.1 with the lender (UNVERIFIABLE); "combined $10 million" gains "when the 7(a) loan is approved first" (R38); 504 table row adds CDC closing counsel review of franchise documents (R41); sources line names 8.1 first, earlier editions wrapped.
- c-store-franchise-category: PMPA-as-franchise claim wrapped as "reported under SOP 50 10 8", 8.1 treatment to be confirmed (UNVERIFIABLE); Directory reinstatement wrapped historical, 8.1 still requires listing (R41); "a minimum credit score of 165" removed and "SBA has since retired its SBSS credit-score screen, effective March 1, 2026" added (R27); remaining citations to 8.1.
- trade-area-is-the-study: "mandates a minimum ... 1.15 ... 1.1 to 1" -> 8.1 name/date, same figures, plus "1.25 on historical EBITDA for a 7(a) initial acquisition" (R28, R27, R09); "SOP authorizes the agency to require ... triggers mandatory third-party feasibility for virtually all SBA hotel loans" -> 13 CFR 120.160(b), lenders commonly point to triggers, hotels are on SBA's list, lenders expect (R43, R44).
- sba-default-economics: SOP 8 "re-tightened underwriting" and "post-SOP-50-10-8 cohorts" wrapped historical, 8.1 named; "$5 million 7(a) plus $5 million 504" gains "when the 7(a) loan is approved first" (R38).
- office-repurposing: same R38 qualifier on the combined $10 million.
- index.html: FAQ answer and visible copy "Under SOP 50 10 8, effective June 1, 2025, the SBA's feasibility-study requirement is discretionary" -> "Under 13 CFR 120.160(b) ..." (R43); special-purpose FAQ "SOP 50 10 8 provides ... higher equity-injection requirements" -> 8.1 and "On a 504 loan they carry a 15 percent borrower contribution (20 percent for a new business as well), against 10 percent" (R31, markers in visible copy); stat table cell, sources line, "eff." list item and card cite to 8.1 / October 1, 2026; JSON-LD "SBA SOP 50 10 8" -> 8.1.
- glamping-utah-usda: "independent going-concern appraisal where the intangible portion exceeds $250,000" -> "independent business valuation ... when the Business Purchase Price exceeds $350,000 or the buyer and seller are closely related" (R21, marker).
- retail-nevada-conventional: "combined ... cap raised to $10 million" gains "when the 7(a) loan is approved first" (R38); citations to 8.1.
- rv-park-pennsylvania-usda: transient test reworded to R42 ("more than 50% of the prior year's revenue from transients staying 30 days or less (a start-up shows it in projections)").
- Citation-only: assisted-living (Arizona, California), multifamily-new-york-agency, private-school-connecticut, retail-nevada, glamping, rv-park-pennsylvania and the research notes above.

## 3. HARDCODED (edited as text, not markers)

- index.html: JSON-LD "SBA SOP 50 10 8.1" (line ~736), two FAQ answers (lines ~822, ~827).
- research-notes/why-feasibility-studies-fail-review/index.html: meta description, twitter:description, JSON-LD description and "about" Thing (SOP 50 10 8.1 plain).
- Prose that is not a marker region: the 13 CFR 120.160(b), "when the 7(a) loan is approved first" and 504 table-cell additions.

## 4. Pre-existing names (left, not in changed sentences)

Sister-firm names remain in sentences I did not change in: case-studies/assisted-living-florida-hud (1230), assisted-living-texas-hud (1215), glamping-utah-usda (995, 996, 999, 1164, 1233, 1379), rv-park-arizona-usda (1341), research-notes/c-store-franchise-category (1336, 1495), trade-area-is-the-study (1229), underserved-gas-station-markets (1402), why-feasibility-studies-fail-review (1375); other files with counts: assisted-living-arizona/hawaii/north-carolina, retail-nevada, rv-park-maine, rv-park-texas, break-even-occupancy-trap (one match each, in source or market-data text). Lines are from the pre-edit numbering and shift by a few lines in edited files.

## 5. Recomputations

None (cluster F has no case-math files; the case studies in this cluster are USDA, HUD, agency or conventional).

## 6. Unresolved / for the main session

- Register has no row carrying "four going-concern appraisals within 36 months" or "separate values for land, building, equipment, intangibles"; the brief cites R21 for it. Kept as paraphrase (hospitality, special-purpose, why-fail) and flagged here.
- Statements left because no register row contradicts them but none verifies them: why-feasibility 1236 ("SOP requires independence from loan-production and approval functions"); special-purpose "SOP requires CDCs to address ... limited or special purpose in the credit memorandum"; retail-nevada, private-school, multifamily rows stating that passive/space-leasing and non-profit borrowers are SBA-ineligible (eligibility rules, unchanged by 8.1 as far as the register shows; 51%/60% occupancy is R32).
- Register R44 text lists the 504-chapter examples without "Amusement parks" while sba.json includes it; the research note's list (which names amusement parks) was left as is, with no count stated.
- The first body mention of the SOP on why-feasibility-studies-fail-review is the lede, which got the short form; the full name appears in the governing-edition paragraph.
- Dates (dateModified, Updated, Reviewed lines) untouched, as instructed.
