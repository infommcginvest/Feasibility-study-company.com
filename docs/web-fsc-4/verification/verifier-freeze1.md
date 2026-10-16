# WEB-FSC-4 verifier report (freeze 5e25e4783ca950b7274de9a0287245da221b72bc)

Method: default verdict REFUTED; each claim re-derived with my own Python (bs4/lxml, stdlib), grep, git (read-only) and curl GET on the draft. Lane scripts were run only with `--check` on a copy (`verifier-run/tree`); afterwards `diff -rq` of the copy against `tree/` showed no writes. The draft was compared byte for byte with the tree: 183 files (every non-dotfile, non-`docs/` file in the tree, including all 160 pages) fetched by GET and SHA-256 equal, 0 differences. So the draft is the frozen tree.

Held set: `data/site/hold.json` resolves to 14 pages (states/texas, gas-station hub, 4 gas-station cases, truck-stop-texas, hotel-texas, rv-park-texas, car-wash-texas, rv-boat-storage-texas, auto-dealership-texas, assisted-living-texas, meat-processing-texas). "Outside the hold" = 146 pages.

## Verdicts (one line each)

- C1 VERIFIED
- C2 VERIFIED
- C3 VERIFIED as worded (but a case-variant bypass exists: defect M1)
- C4 VERIFIED (strict-reading note in m7)
- C5 VERIFIED
- C6 PARTLY: the four pages verified; the same DSCRs are stale on /case-studies/index.html (blocker B1); the RV IRR carve-out is true (major M2)
- C7 REFUTED (60 em dashes remain as JSON `—` in JSON-LD; one literal U+2014 in `.gitignore`): blocker B2
- C8 VERIFIED
- C9 VERIFIED
- C10 VERIFIED (narrative contradiction in m1)
- C11 VERIFIED for every page outside the hold; two held pages lack a JSON-LD dateModified (m3)
- C13 VERIFIED by my own measurement (iframe at 390px in the Browser pane, all 160 draft pages); screenshots exist; not a device-emulated UA
- C12 VERIFIED
- C14 VERIFIED
- C15 VERIFIED
- C16 VERIFIED

Defects: 2 blockers, 3 majors, 7 minors.

---

## C1 VERIFIED
```
python3 (bs4+lxml) over tree/**/*.html excluding docs/:
pages 160            (find base -name '*.html' = 160; diff of the two sorted path lists: "same page set")
bad_title []         (regex <title after stripping <!--...-->  == 1 AND bs4 find_all('title') == 1 AND non-empty, all 160)
pages with <title in a comment 158   (the pre-existing "REBRAND SWAP POINTS: <title>" comment; correctly not counted)
ld blocks (comments stripped) 223  bad []   (json.loads on every block, regex and bs4)
```

## C2 VERIFIED
Own checker (resolve every `<a href>` on the 146 non-held pages against the tree; also fragments against `id=`):
```
internal links checked (non-held src): 19946
broken (target missing): 0
broken fragments: 0
```
Pending markup: `data-fsc-pending` appears 1641 times, all on non-held pages: 1077 `<a>` + 564 `<span>`; 463 distinct targets; 0 pending targets that exist as a page; 0 `<a>` whose href equals its pending target; 0 other tags. PENDING.csv has 1642 rows = 1641 + one summary row ("every page with the Markets panel", Ohio, hide_until_live). Fallbacks spot-checked: `/states/texas/#metros` has Houston, Dallas, Austin cards; `#thesis`, `#rejected`, `#layers`, `#study-types`, `#coverage` all exist.
`/inquiries`: base had 133 pages with `href="/inquiries..."`; tree has it only on the 14 held pages (+ docs). Homepage has `<section id="contact">`; the homepage chrome uses `#contact`, other pages `/#contact`.
Draft GET of every distinct internal link path (186): 159 x 200, 27 x 404; all 27 are linked only from held pages (checked: 0 sources outside the hold without a pending marker).
Also checked 478 local `img/script/link/form` references: 0 missing.

## C3 VERIFIED as worded (see M1)
```
D=https://6ad1f9a4bba14c3fdb9fa372--splendid-cannoli-80c225.netlify.app ; curl -s -m 20 -o /dev/null -w "%{http_code} %{redirect_url}"
/asset-classes/car-wash/ , /car-wash , /car-wash/x         301 -> /asset-classes/express-car-wash/
/asset-classes/gas-station/ , /gas-station/anything/deep   301 -> /asset-classes/gas-station-and-c-store/
/asset-classes/assisted-living/                             301 -> /asset-classes/assisted-living-and-memory-care/
/asset-classes/independent-living/ , /independent-living    301 -> /asset-classes/assisted-living-and-memory-care/
/asset-classes/industrial/ , /industrial                    404  (not redirected)
/docs , /docs/ , /docs/web-fsc-4/DECISIONS.md , /src , /src/x.html   404
```
No static dir shadows the four redirects (`ls asset-classes`). Redirect targets return 200.

## C4 VERIFIED
Own code (bs4): "own parents" of each case = the three links in its "Where this case sits" block (52 non-held cases carry it; the 12 held cases do not).
```
reverse link missing: 1 -> ('multifamily-texas-agency', '/states/texas/')   parent is HELD (exempt)
held cases -> open parents (hub, practice area): all have the reverse link; held -> held parents exempt
```
Inbound (links inside `<main>`, not in header/footer, not in `.breadcrumb`, source not an index page, not self), distinct source pages. Computed four ways (all sources; without pending-marked links; non-held sources only; both):
```
all four modes: min inbound = framework 3-4, hub 3-4, case 3, state 3, note 8, practice 9; pages under 3: 0 in every mode
lowest (strict): case auto-service-new-jersey 3, hub auto-dealership 3, state washington 3, framework 3
```
Identical generated sets: 133 pages carry `<!--mesh:..-->` regions; union-of-hrefs per page: duplicates none. (Per marker kind, `hub-notes` is identical on three hubs: m4.)

## C5 VERIFIED
```
non-held pages 146: each has exactly one <!--chrome:header--> and one <!--chrome:footer--> region, no raw <header class="site-header"> outside it
held pages carrying chrome markers: 0 (untouched)
distinct header texts after dropping aria-current: 5 (142 identical; 4 state pages differ only by one pending item becoming a <span>, correct); footer: 1 distinct
chrome links broken: 0 (hrefs and fragments); 1018 pending-marked chrome anchors
all 73 chrome.json items present in a rendered page's regions except Ohio (hide_until_live)
```
`python3 scripts/chrome.py --check` exit 0 (C12).

## C6 PARTLY
The four pages (own recompute, then page-by-page text and token diff base to tree):
```
independent amortization (monthly, 9.5%/25y bank, 6.5%/25y debenture, 50/35/15):
 AZ  bank 262,109 + deb 141,794 = 403,903 -> $262k+$142k=$404k  DSCR 0.95/1.21/1.52 (NOI 382/488/615k)
 CA  319,773 + 172,988 = 492,761 -> $320k+$173k=$493k           0.95/1.21/1.52 (466/595/750k)
 FL  304,046 + 164,480 = 468,527 -> shown "$304k, $164k, $469k"   0.95/1.21/1.52 (444/567/713k)
 NC  503,249 + 272,244 = 775,493 -> $775k                        1.21/1.42/1.57 (0.94/1.10/1.22M)
 old 50/40/10 reproduces the base figures (AZ 0.90/1.15/1.45 on $424k, NC 1.15/1.35/1.50 on $814k)
```
Uses tables sum to the totals; sources = bank+deb+equity = cost (5.00, 6.10, 5.80, 9.60M); hero tile "85%" and "$4.93M of $5.80M" (FL) correct; FL "DSCR 1.0 crossed near 61 percent occupancy" = 469/7.66 = 61.2, correct; CA "NOI $0.75M / 7.5% = $10.0M" correct; NC exit balance $6.6M and net equity $2.6M correct (9.5M x 0.97 - 6.62M = 2.59M). Meta, og, twitter, JSON-LD descriptions, tiles, tables, prose all show 1.52x/1.57x. New source `13 CFR 120.910` present once per page, footnote refs resolve, sources numbered 1..N. Every sentence containing 10%/ten percent in the four pages is either the 7(a) start-up rule, the standard-case tier, or a source description; none states 10% as their equity or minimum. NC IRR 16% -> 12%: my own calibration (28% payout share reproduces 16.00% on 50/40/10, same as the lane's 0.2799) gives 12.02% on 50/35/15.
`python3 docs/web-fsc-4/recompute/<case>.py --check` on the copy: all four exit 0.

What fails: the same figures are stale elsewhere (B1). What the claim says about IRR is true (M2): with each page's own inputs the RV IRR is 22-30% (15% equity) or 27-35% (10%), not ~16%.
```
case-studies/index.html (cards still carry the old numbers):
 rv-boat-storage-arizona-sba   "... and a 1.45× DSCR."            (page: 1.52x)
 rv-boat-storage-california-sba "... and a 1.45× stabilized DSCR." (page: 1.52x)
 rv-boat-storage-florida-sba   "... and a 1.45× DSCR."            (page: 1.52x)
 medical-office-north-carolina-sba "... and a 1.50× global DSCR."  (page: 1.57x)
```

## C7 REFUTED
Scan of all 186 files in the tree outside `docs/`, `src/` and the held pages (U+2014/2013/2015/2012, `&mdash;` `&ndash;` `&#8212;` `&#8211;` `&#x2014;` `&#x2013;` with leading zeros, bare entities, `—`, `–`, `%E2%80%94`):
```
non-held files with dash tokens: {'.gitignore': 1 (literal U+2014 in a comment),
                                  'case-studies/index.html': 60 (JSON escape —),
                                  'scripts/mesh.py': 2 (regex source text, not a dash character)}
held dash tokens (excluded): 652
parsed JSON-LD of case-studies/index.html: 60 ItemList "name" strings contain U+2014, e.g.
  "Gas Station Feasibility Study, Texas — An SBA 7(a) Worked Case", "Limited-Service Hotel Feasibility Study, Florida — SBA 504"
```
Charter ruling 12 explicitly covers "JSON-LD", so these are in scope. `—` is the JSON encoding of an em dash; any parser or crawler reads the dash. The listed encodings do not name this form, which is why the lane's gate missed it; base had the same 60. `.gitignore` is not served by Netlify (draft: 404) but it is a tree file outside `docs/`/`src/`, so inside the claim's own definition of "served".

Second sentence of C7 (fidelity) VERIFIED: `git diff --name-only c203580 c21b055` = 153 files (150 readable: 146 html, README.md, one xml, netlify.toml, styles.css; 3 new docs files skipped). For each, tokens `\w+` of old vs new after removing dash tokens are identical: 0 files differ.

## C8 VERIFIED
```
regex (exact, case-insens): mmcg|mohelsky|union ?metric|innowave|analytics\.loan|loan analytics|feasibility-study-consultant|wert-?berater
  over 186 served files outside docs/src and non-held (bytes, utf-8 ignore, filenames too): 0 hits
  broad variants (m m c g, mohel, unionmetrics, inno-wave, loan-analytic, consultant.com, wertbera...): 0 hits
  held pages still carrying a name: gas-station-and-c-store hub, rv-boat-storage-texas, rv-park-texas, assisted-living-texas (live in production today)
hosts referenced in non-held served files: 102 distinct, none a sister domain
git log --format=raw 1d48cc2..5e25e47 | grep -ciE <regex> = 0 ; authors/committers: "Feasibility Study Company <noreply@feasibility-study-company.com>" only
```
Relabels: 23 non-held base files carried a name (13 MMCG, 6 Innowave, 11 Loan Analytics, 8 analytics.loan, 3 feasibility-study-consultant). Spot-read 25: now "industry research" / "an industry database" / "a loan-data site"; in commit c203580 the numeric tokens of the 20 non-case files are identical before and after (0 files with a changed number or year).

## C9 VERIFIED
```
cd tree && grep -riE "otava,? *(ph\.?d|ccim|mai)" .   -> no output, exit 1 (whole tree incl. docs)
rendered pages: no "Ph.D", "CCIM" or "MAI" next to Otava (only an unrelated "Gerard McDonough, MAI" citation on 2 marina pages)
```
Note m6: `data/authors/mark-otava.json` (served, unchanged from base) lists Ph.D., MAI, CCIM with empty verify_url; `byline.py` shows a credential only when verified, so none render.

## C10 VERIFIED
bs4 on all 52 non-held case pages: exactly one `h1`; its next tag siblings are `p.byline` then `div.capsule.disclosure`; one disclosure per page; text starts "Representative worked example. The site, sponsor and project are hypothetical."; 48 carry the standard sentence 2, 4 (rv-park-ossipee, dry-stack-cape-coral, glamping-oak-hill, cabin-resort-townsend) carry the base batch-1 variant ("The market evidence is real, public and dated October 2026"); unchanged from base.

## C11 VERIFIED (outside the hold)
```
indexable pages 158; sitemap 158 entries, unique, none without lastmod; 2 noindex pages not in it
JSON-LD dateModified vs byline marker vs visible Updated vs sitemap lastmod: 0 disagreements outside the hold
base->tree sitemap lastmod changes: 35 = 31 corrected to the page's own unchanged date (visible+JSON-LD date in base already 2026-07-xx) + the four cases to 2026-10-16
pages whose date moved (JSON-LD/visible vs base): the four cases (2026-10-10 -> 2026-10-16); 7 further pages merely gained a dateModified equal to their base sitemap lastmod
```
Held exceptions: `/states/texas/` and `/asset-classes/gas-station-and-c-store/` have no JSON-LD dateModified; 12 held cases have no "Updated" in the byline marker (m3).

## C12 VERIFIED
```
cd verifier-run/tree; for s in byline regulatory mesh links chrome sitemap; python3 scripts/$s.py --check
scripts/byline.py --check exit 0 (out of date: 0)    scripts/regulatory.py --check exit 0
scripts/mesh.py --check exit 0 (855 term links on 132 pages)   scripts/links.py --check exit 0 (0 problems over 146 pages)
scripts/chrome.py --check exit 0 (0 out of date)     scripts/sitemap.py --check exit 0 (up to date)
```

## C13 VERIFIED by my own measurement; screenshots present
Browser pane, draft origin, same-origin iframe of width 390px per page, `documentElement.scrollWidth`/`body.scrollWidth` vs `clientWidth`, pages = sitemap (158) + /404.html + /tools/nda/:
```
n=160, clientWidth 390 on all 160, max scrollWidth 390, pages with overflow: 0
control (detector can fire): same pages at 320px -> /states/washington/ overflows (sw 328); at 280/240px most pages overflow
every page has <meta name="viewport" content="width=device-width, initial-scale=1">
```
Caveat: iframe width, not a device-emulated UA or touch. `docs/web-fsc-4/look/`: 32 PNGs = 8 subjects x desktop (1440 wide) + mobile (390 wide) (+ "-section" crops, markets panel has none): hawaii, hub-mesh-marina, markets-panel, note-trade-area, older-case-disclosure-hotel-florida, practice-area-mesh-sba, recomputed-medical-office-nc, truck-stop-oklahoma = charter item 13's list. Viewed the NC mobile, Hawaii section, markets panel desktop and Oklahoma mobile images: they show what their names say.

## C14 VERIFIED
```
meta robots: 158 x "index, follow, max-image-preview:large, max-snippet:-1"; 2 x "noindex, follow" (/404.html, /tools/nda/)
all 158 in sitemap.xml with lastmod; canonical == sitemap URL on every page; no noindex page in the sitemap
db7ea828330340f8994ca82a16c48c8b.txt: content "db7ea828330340f8994ca82a16c48c8b" (equals its name); draft GET 200 text/plain
```

## C15 VERIFIED
`cmp base/<p>/index.html tree/<p>/index.html` for all 14 held pages: IDENTICAL x14. `git diff --name-only 1d48cc2 5e25e47 -- <the 14 held paths>`: empty.

## C16 VERIFIED
```
truck-stop-oklahoma-sba base: whole head inside one 29,096-char comment -> live <title> none, <style> 1 (740 chars), ld+json 0
                       tree: live <title> "Truck Stop Feasibility Study in Oklahoma: SBA 504 Worked Case | Feasibility Study Company",
                             3 <style> (25,346 chars), 1 ld+json (Organization, Article, BreadcrumbList) parses; head children match truck-stop-georgia-sba
states/hawaii #metros: base h2 "Four island counties, distinct demand fingerprints."  tree h2 "Four island counties, six markets, distinct demand fingerprints."
   6 cards: Honolulu/Oahu, Kapolei/Ewa, Maui County, West Maui/Lahaina, Hawaii Island, Kauai
```

---

## Defects

### Blockers (2)
- **B1. False figures on /case-studies/index.html.** Four cards keep the pre-fix DSCR (1.45x for the Arizona, California and Florida RV storage cases; 1.50x for the North Carolina medical office), while the case pages now say 1.52x and 1.57x. Found by grepping every other page for links to the four slugs: `case-studies/index.html` card text at line 1000 (north-carolina medical office, `1.50&times; global DSCR`), 1187 (california, `1.45&times; stabilized DSCR`), 1484 (florida, `1.45&times; DSCR`), 1495 (arizona, `1.45&times; DSCR`). Not touched by the lane (the card text is the same in base). Fix: 1.57&times; at line 1000 and 1.52&times; at 1187, 1484 and 1495. (Line 1440 is the held Texas RV card; 1.45x is right for that page as it stands.)
- **B2. C7 is false: 60 em dashes remain in JSON-LD** of `/case-studies/index.html` (`—` escapes in the ItemList `name` of each case) and one literal U+2014 in `.gitignore` (not deployed). Ruling 12 names JSON-LD explicitly. The sweep/gate looked only for literal characters and entities. Fix: replace `—` with `:` (matching the pages' titles) in that block; add `\\u2014|\\u2013` to the dash gate.

### Majors (3)
- **M1. `/docs/*` 404 rule is bypassed by case.** On the draft `GET /Docs/web-fsc-4/DECISIONS.md`, `/DOCS/...`, `/Docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md`, `/Docs/web-fsc-4/PENDING.csv`, `/Docs/web-fsc-1/CLOSE.md`, `/Docs/web-fsc-2/tools/gates.py` all return 200 (`/docs/...` and `/%64ocs/...` return 404). Those files contain the sister-property and Wert-Berater names (DECISIONS.md, the charter, web-fsc-2/INVENTORY.csv), the owner's local folder `~/MMCG Analytics Build Up`, the GitHub org `infommcginvest` and the Netlify site id. DECISIONS.md item 5 states "`docs/` is not served (404)", which is wrong for these URLs. The rule is pre-existing, the new `docs/web-fsc-4/` content is this lane's. Fix: exclude `docs/` from the publish root, or add the case variants and `force`; same for `/src/*`.
- **M2. The three RV storage pages publish "about 16 percent" levered IRR that their own inputs do not produce.** My calculation with each page's NOI, debt service, 10-year hold and market caps (7.5%, 8.5%, 12.3% yield on cost; 0% or 3% sale cost): 22-30% on the new 50/35/15 stack (27-35% on the old). The California prose gives the full derivation (NOI $0.75M at 7.5% = $10.0M, net of selling costs and the 504 balance, "about 16 percent"), which computes to about 29%. The lane's `recompute/*.md` discloses this and leaves it as an owner item, and C6 says so; but the figure is financing-dependent and sits in the hero tile, meta, og and JSON-LD of three pages. The NC 12% is derived by calibrating an unstated 28% payout share so the old structure returns 16% (I reproduced 0.2799 and 12.02%); with 100% distribution it is 27%.
- **M3. Held sibling contradicts the corrected pages.** `case-studies/rv-boat-storage-texas-sba` (held, WEB-FSC-6) still says "10 percent SBA baseline" and "50% bank + 40% CDC" for a ground-up storage business, and it is linked from the "Other RV and boat storage worked cases" block on the three corrected pages (and `/case-studies/` still shows it at 1.45x). After merge a reader moves between 15% ("the 10% contribution of a standard case does not apply") and 10% in one click.

### Minors (7)
- **m1.** 48 of 52 non-held case pages narrate "A sponsor came to our feasibility study company ..." directly under a box saying "The site, sponsor and project are hypothetical ... It is not a client engagement." disclosure.py removed only one such sentence (assisted-living-north-carolina-hud). Owner call.
- **m2.** Florida table: bank "≈ $304k", debenture "≈ $164k", combined "≈ $469k" (components sum to 468; unrounded 468.5).
- **m3.** Held exceptions to C11: `/states/texas/` and `/asset-classes/gas-station-and-c-store/` have no JSON-LD dateModified; the 12 held cases show "Published" only while JSON-LD/sitemap say 2026-10-10 or 2026-07-13 (ruling 13 asks for "Updated" where the two differ).
- **m4.** `hub-notes` mesh block is identical (one link, franchise-vs-non-franchise) on the QSR, childcare and fitness hubs; page-level sets differ, so C4 holds.
- **m5.** `/states/washington/` overflows horizontally by about 8px at 320px width (claim covers 390 only).
- **m6.** Internal tooling is served publicly: `scripts/*.py`, `data/site/hold.json` (lane names, workflow notes), `data/mesh/*.json`, `README.md`, `netlify/functions/contact.js`, and `data/authors/mark-otava.json` listing Ph.D./MAI/CCIM abbreviations with empty verification (unchanged from base, not rendered). `netlify.toml` and dotfiles are not served.
- **m7.** Strict reading of C4: 42 prose cross-links from case bodies to hubs/states/practice areas other than the case's own (e.g. retail-nevada -> grocery-store hub) have no reverse link. The claim says "its" state/hub/practice area, which I read as the three in "Where this case sits"; those all have reverse links.

### Not counted (owned by WEB-FSC-6, live in production today, unchanged by this lane)
The 14 held pages keep `/inquiries/` links (404), 652 dashes, 215 broken anchors, and four of them carry sister-property names.
