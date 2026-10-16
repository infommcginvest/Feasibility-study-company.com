# WEB-FSC-4 verifier report, freeze 2 (9896628866f26d591afec42c0c8b5b8f5df419e3)

Method: default verdict REFUTED; each item re-derived with my own Python 3 (bs4 + lxml, stdlib), grep, read-only git and `curl -m 20` GET on the draft. I wrote nothing into `tree/`, `base/`, the repository or the draft. Lane scripts were run only with `--check`, on a throwaway copy of the tree (copy and tree compared afterwards: no writes). My working files live outside `freeze2/` (`scratchpad/verifier2-work/`); this file is the only thing I put in `freeze2/`.

`D=https://6ad20281fa0eff51c6dc288e--splendid-cannoli-80c225.netlify.app`
`PAT='m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er'` (case-insensitive; names only in bracketed form here)

## Ground truth I established first

```
git archive 9896628 | tar -x -C arch ; diff -rq arch tree            -> identical ("TREE == git archive 9896628")
git archive 1d48cc2 | tar -x -C arch_base ; diff -rq arch_base base   -> identical (base is production today)
served set = tree minus docs/, src/, dotfiles = 184 files (160 pages); held = 14 pages (data/site/hold.json), so 146 non-held pages, 170 non-held served files
GET of all 184 served files on the draft: 183 x 200, 1 x 404 (netlify.toml, a config file Netlify does not serve)
cmp tree vs draft bytes on the 183: 0 differences  -> the draft IS the frozen tree (minus docs/ and src/, as stated)
```

## One line per item

- A1 VERIFIED
- A2 VERIFIED
- A3 VERIFIED (draft only; see N4 on what a draft cannot prove)
- A4 VERIFIED
- A5 VERIFIED (two disclosure notes in N2 and N3)
- C2 VERIFIED
- C3 VERIFIED (on the draft; the git-build path is untestable here, N4)
- C6 VERIFIED (caveats: NC 12% is a calibration, N3; Arizona ~16% stays as a disclosed owner item)
- C7 VERIFIED
- C8 VERIFIED
- C11 VERIFIED
- C15 VERIFIED

New defects: 0 blockers, 1 major (N1), 3 minors (N2 to N4). Carried and disclosed items are listed separately and not counted.

---

## A1 VERIFIED: the four case cards on `/case-studies/`, and no other stale figure of the four cases

Cards in `tree/case-studies/index.html` against each case page's hero tile (bs4):

```
rv-boat-storage-arizona-sba         page tile 1.52  index card (line 1495) "a 1.52× DSCR"
rv-boat-storage-california-sba      page tile 1.52  index card (line 1187) "a 1.52× stabilized DSCR"
rv-boat-storage-florida-sba         page tile 1.52  index card (line 1484) "a 1.52× DSCR"
medical-office-north-carolina-sba   page tile 1.57  index card (line 1000) "a 1.57× global DSCR"
```
`git diff 1d48cc2 9896628 -- case-studies/index.html | grep DSCR` shows exactly those four -/+ pairs (1.50->1.57, 1.45->1.52 x3). The held Texas RV card (line 1440) still reads 1.45x and its page tile is `1.45`, so it is right for that page.

"No other page": (a) for every one of the 146 non-held pages other than the four, every block (li, p, article, div, tr, td, section) around a link to one of the four slugs that holds a number: only `case-studies/index.html`, 4 blocks, all correct now. (b) Every sentence on every other non-held page that names RV, boat storage, medical office, MOB or ASC together with DSCR, IRR, equity, debt service, coverage or a `d.dd x` figure: 55 sentences, all about other assets or generic (hotel and RV-park cards, the lender matrix, an external source's "1.88x at stabilization" in rv-and-boat-storage source note s11, which is a third party figure). (c) every `1.45` or `1.50` followed by x, ×, `&times;` or "times" in all 184 served files: 259 hits in 36 files; I printed the 300 characters before each and filtered for RV, boat, storage, medical office, MOB, ASC: the only hits in such a context are the self-storage and marina cases (their own pages, 50/35/15 or 504 cases not in the four), the held Texas RV page and its card on `/case-studies/` (1.45x, right for that page); every other hit is a lender floor or another asset. None quotes an old figure of the four cases. (d) The ItemList JSON-LD on `/case-studies/` carries names and URLs only, no figures. (e) `feed.xml` has no items. Result: no old figure of the four cases survives outside the four pages and the held Texas RV page.

## A2 VERIFIED: no em or en dash in any form in served non-held files

Detector (mine): literal U+2014, U+2013 (and, as extras, U+2012, U+2015, U+2212, U+2E3A, U+2E3B, U+FE58, U+FE63, U+FF0D); `&mdash;`, `&ndash;`; `&#0*8212;`, `&#0*8211;`; `&#x0*2014;`, `&#x0*2013;` (any case); `\\+[uU]\{?0*2014|2013`; CSS `\2014`, `\2013`; `%E2%80%94`, `%E2%80%93`; `fromCharCode(8212|8211|0x2014|0x2013)`; `\x97`, `\x96`. Run on every served file as text (binary `og.png` checked for the UTF-8 byte pairs; I also viewed it: no dash in the image).

```
tree:  served files 184 held 14 | files with hits outside hold: 0 | held pages: 14 files, 652 hits (WEB-FSC-6's, exempt)
draft bytes (the 184 files I fetched): files with hits outside hold: 0 | held: 14 files, 652 hits
independent grep -nIiE '\xe2\x80\x94|\xe2\x80\x93|&mdash;|&ndash;|&#0*8212;|&#0*8211;|&#x0*2014;|&#x0*2013;|\\u2014|\\u2013|%e2%80%9[34]|\\2014|\\2013' over the 170 non-held served files: no output
controls: freeze 1 tree -> case-studies/index.html 60 x — and scripts/mesh.py 2 hits (exactly the first-round blocker);
          base -> 5,277 matching lines. The detector finds them, and finds none in freeze 2.
grep -o '\\u2014' case-studies/index.html: base 60, freeze 1 60, freeze 2 0
```
The 60 JSON-LD names are now colons: `RV & Boat Storage Feasibility Study, California: An SBA 504 Worked Case` etc., equal to each page's H1. `scripts/mesh.py` now builds its dash pattern from `chr(0x2014)`/`chr(0x2013)`.
Outside C7's definition: `.gitignore` line 16 still has a literal U+2014 (dotfile; `/.gitignore` is 404 on the draft; WEB-FSC-5's). `&minus;` (U+2212, a minus sign, not a dash) appears on 46 non-held pages; unchanged by the sweep and not in C7's list.

## A3 VERIFIED: `/docs`, `/src` in every capitalisation and encoding answer 404; no ruling-10 name outside the held pages

```
20 prefixes (docs Docs DOCS dOcS dOcs doCs docS DocS dOCS DOcs doCS DOCs docs%2F Docs%2F DOCS%2F dOcS%2F docs%2f %64ocs %44ocs docs%2e)
 x 3 files (docs/web-fsc-4/DECISIONS.md, docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md, docs/web-fsc-2/INVENTORY.csv) = 60 GETs: 60 x 404, 0 matches of PAT in any body
 (404 body is the site's 404.html, 13,957 bytes)
more: /docs /docs/ /Docs /DOCS/ /src /Src /SRC /sRc/ /docs/web-fsc-4/PENDING.csv /DOCS/web-fsc-4/PENDING.csv /Docs/web-fsc-1/CLOSE.md
      /DOCS/web-fsc-2/tools/gates.py /SRC/x.html /docs/index.html /docs/web-fsc-4/DECISIONS.md?x=1 //docs/web-fsc-4/DECISIONS.md /docs/web-fsc-4/DECISIONS.md/ /DOCS/WEB-FSC-4/DECISIONS.MD /docs\web-fsc-4\DECISIONS.md : all 404
      (/./docs/... and /docs/../docs/... with --path-as-is: 404; /%2e%2e/docs/... : 400)
```
First-round bypass repro (`/DOCS/web-fsc-4/DECISIONS.md` was 200 with 3 name lines): now 404.

Names: all 184 served files fetched over HTTP from the draft (sitemap's 158 URLs, `/README.md`, `/scripts/*.py`, `/data/**/*.json`, `netlify/functions/contact.js`, css, key file) searched with PAT: 0 hits outside the held pages. In the tree the 170 non-held served files: 0. External hostnames linked from non-held served files (distinct list read): no sister domain. Held pages with a name, live on the draft and on production today, WEB-FSC-6's, untouched: `asset-classes/gas-station-and-c-store` (2 lines), `case-studies/assisted-living-texas-hud` (2), `case-studies/rv-boat-storage-texas-sba` (2), `case-studies/rv-park-texas-usda` (1).

## A4 VERIFIED: the 29 cross-sentence parenthesis pairs are gone, words unchanged

My detector (not the lane's, not attacker two's): per block of visible text (bs4, `get_text('')` so `.<sup>9</sup> On` is `.9 On`; `<sup>` footnote markers replaced by a sentinel), match each "(" with its ")" by stack, flag a pair when the inside holds `[A-Za-z0-9%)\]"'][.!?](footnote)*["')]?\s+[A-Z"(\d$]` after masking a list of abbreviations (e.g., i.e., U.S., Inc., Dec., Comm., Stat., Ch., Ord., Vol., Rt., state abbreviations, J.B., G.L.) and single initials.

```
freeze 1: pages 25, pairs 29      <- reproduces attacker two's "29 on 25 pages" exactly (control)
freeze 2: pages 0,  pairs 0
(raw output of the detector before masking statute citations: 8 freeze-2 candidates, all "P.L. 119-21", "H.R. 2398/S. 1163", "H.B. 1, signed ..." - abbreviation dots, not sentence breaks)
a second, looser detector (any [.!?] then up to 6 non-space characters then space then capital): 60 freeze-2 spans, read one by one: all decimals ("3.71, R"), "e.g.,", "incl.", "p. 142", "Dec. 206", "Sault Ste. Marie"; none is a sentence break
unbalanced parentheses in any visible block: freeze 1: 0, freeze 2: 0
qsr-arkansas-sba: freeze 2 reads "headquarters (Walmart, Tyson Foods, and J.B. Hunt) and roughly 1,300 supplier offices"; base had "&mdash; ... &mdash;"
```
I read the freeze-2 text of all 29 sites; each is now a comma, colon or sentence break that parses (e.g. glamping-utah: "...is about $609,000, the number the projected coverage has to clear.").

Word sequence, freeze 1 -> freeze 2, all 146 non-held pages (tokens `\w+` of visible text, and again of the whole file with JSON-LD escapes and entities decoded, meta content and attributes included):
```
visible word sequence differs on 3 pages: case-studies/index.html, rv-boat-storage-california-sba, rv-boat-storage-florida-sba
whole-file word sequence differs on the same 3 pages and no other
so the other 24 of the 25 pair pages are word-identical; the California page differs only in its IRR sentences (below)
held pages freeze 1 vs freeze 2: byte-identical
difflib on the 3: index: four DSCR numbers (50->57, 45->52 x3); California: six IRR sites "16"/"in the mid teens about 16" -> "30"/"near 30"; Florida: six sites 16 -> 25. Nothing else.
git: sweep commit c21b055 vs parent: 150 files changed outside docs, word sequence identical in 150.
     9896628 vs 5e25e47: 29 files, 24 identical, 5 differ (the 3 pages above, netlify.toml (config comment + build command), scripts/mesh.py (dash regex spelled by code point)).
```

## A5 VERIFIED: California about 30 percent, Florida about 25 percent

Rebuild (own code, `pmt`, `bal` closed forms, bisection IRR). Inputs read from the pages: California cost $6.10M, NOI Y1 466k, Y2 595k, Y3 750k; Florida cost $5.80M, NOI 444k, 567k, 713k; 50/35/15; bank 9.5% and debenture 6.5%, both 25-year monthly amortization; 10-year hold; balance after 120 payments.

```
CA: bank 3.050M deb 2.135M eq 0.915M; DS 492.8k; balance at yr 10 4.207M; exit = 0.75M / 0.075 = 10.00M
FL: bank 2.900M deb 2.030M eq 0.870M; DS 468.5k; balance at yr 10 4.000M; terminal value = 1.15 x 5.80M = 6.670M

Y1 shortfall met from the funded reserve (distribution floored at 0), NOI flat after Y3, annual cash flows:
  CA sell 0%: 30.2%   3%: 29.8%   5%: 29.5%
  FL sell 0%: 25.0%   3%: 24.5%   5%: 24.2%
Y1 shortfall treated as an equity outflow, annual cash flows:
  CA 0%: 29.8%  3%: 29.4%  5%: 29.1%      FL 0%: 24.6%  3%: 24.1%  5%: 23.8%
NOI growing 2-3% a year after Y3 (0-5% selling cost):  CA 30.3% to 31.5%     FL 25.4% to 26.9%
monthly cash flows, effective annual:                  CA 30.4% to 31.1%     FL 25.2% to 26.0%
no interim distributions at all (not the pages' words):  CA 19.6-20.3%        FL 11.0-11.9%
old 50/40/10 structure on the same exits: CA 34.6-35.1%, FL 29.1-29.6%  (so "about 16" was never the answer, before or after)
```
My CA 30.2/29.8/29.5 and FL 25.0/24.5 reproduce the lane's recompute scripts and DECISIONS item 41 to the decimal. "About 30" and "about 25" lie inside every plausible reading (29.1-31.5 and 23.8-26.9).

Sites, parsed on the draft bytes (all six on each page agree; "twitter:description" carries no figure):
```
California: tile "&asymp;30%"; meta description "~30% levered equity IRR"; og:description "~30% IRR"; JSON-LD Article.description "~30% levered equity IRR";
            outcome sentence "lands near 30 percent over a 10-year hold"; verdict "~30% illustrative levered equity IRR"
Florida:    tile "&asymp;25%"; meta "~25% levered equity IRR"; og "~25% levered equity IRR"; JSON-LD "~25% levered equity IRR";
            outcome "about 25 percent over a 10-year hold"; verdict "~25% levered equity IRR"
regex for a 16 as percent, ~16, "about 16", "mid-teens", "teens", "sixteen" on both pages (tree and draft): 0 hits
the 1.52x / 85% / $4.93M / $0.915M / $2.135M figures on both pages match my rebuild
```

---

## B. Re-verification of C2, C3, C6, C7, C8, C11, C15 on freeze 2

### C2 VERIFIED
Own checker over the 146 non-held pages: every `<a href>` (root-relative, relative, fragment-only, and absolute on feasibility-study-company.com or www) resolved case-exactly against the served file list, fragments against `id=`/`name=`:
```
internal <a href> checked 19,946 | missing target 0 | missing trailing slash 0 | missing fragment 0 | links to a redirect-only alias 0
data-fsc-pending 1,641 (1,077 <a> + 564 <span>), 463 distinct targets; pending targets that exist as a page: 0; <a> whose href equals its pending target: 0
/inquiries anchors on non-held pages: 0 (base had 468 on 119 pages); /#contact anchors on 146 pages (559); homepage uses href="#contact" (4) and has id="contact"
control: same checker on base: 2,505 broken links
draft: all 160 distinct internal link targets: 160 x 200; all 463 distinct pending targets: 463 x 404
```
(The 56 `/inquiries/` hrefs on the 14 held pages remain, as the claim scopes.)

### C3 VERIFIED (on the draft)
```
/asset-classes/car-wash/ , car-wash (no slash), car-wash/x/y        301 -> /asset-classes/express-car-wash/
/asset-classes/gas-station/ , gas-station/anything                  301 -> /asset-classes/gas-station-and-c-store/
/asset-classes/assisted-living/ , assisted-living                    301 -> /asset-classes/assisted-living-and-memory-care/
/asset-classes/independent-living/ , independent-living, /z         301 -> /asset-classes/assisted-living-and-memory-care/
/asset-classes/industrial/ and /asset-classes/industrial            404 (not redirected)
the three targets: 200
/docs, /src and all 60+ capitalisation/encoding variants of A3: 404
```
`netlify.toml` (tree) keeps `/docs/*` and `/src/*` 404 rules and adds `[build] command = "rm -rf docs src"`; the draft shows the CLI-filtered path works (no docs/ file is reachable in any form). See N4 for what this cannot prove.

### C6 VERIFIED (caveats N3 and the disclosed Arizona item)
- Own rebuild of all four pages' financing (50/35/15; 9.5% / 6.5%; 25-yr monthly):
```
AZ  cost 5.00M: bank 2.500 deb 1.750 eq 0.750 | DS 262.1k + 141.8k = 403.9k | DSCR 0.95/1.21/1.52 | all on page ("$404k", "$262k bank + $142k debenture")
CA  cost 6.10M: bank 3.050 deb 2.135 eq 0.915 | DS 319.8k + 173.0k = 492.8k | DSCR 0.95/1.21/1.52 | page "$493k (bank ~$320k + debenture ~$173k)"
FL  cost 5.80M: bank 2.900 deb 2.030 eq 0.870 | DS 304.0k + 164.5k = 468.5k | DSCR 0.95/1.21/1.52 | page "$304k / $164k / $469k"
NC  cost 9.60M: bank 4.800 deb 3.360 eq 1.440 | DS 503.2k + 272.2k = 775.5k | DSCR 1.21/1.42/1.57 | page "$775k", 1.21 1.42 1.57
```
Sources equal uses on each page; hero tiles show 85% (FL "$4.93M of $5.80M", correct); Florida debt-service break-even "near 61 percent" = 469/713 x 93% = 61.2% (correct); NC exit "about $9.5 million, net of roughly 3 percent selling cost and a balance near $6.6 million ... roughly $2.6 million of net equity" = 9.5 x 0.97 - 6.621 = 2.594M (correct).
- Lane scripts on a copy: `rv-boat-storage-arizona-sba.py --check` exit 0, `-california-` exit 0, `-florida-` exit 0, `medical-office-north-carolina-sba.py --check` exit 0.
- Every sentence on the four pages containing "10%", "10 percent", "40%", "90%", "50/40/10": all say the 10% is the 7(a) start-up rule or the 504 standard-case tier, never these cases' equity or minimum. Meta, og, JSON-LD, tiles and prose carry 1.52x / 1.57x and the new IRRs; grep of the four pages for `1.45`, `1.50x`, `0.90`, `1.35x`: 0 hits on each; `~16` / `&asymp;16` / "16 percent": 0 on CA, FL and NC, 6 on AZ.
- IRRs: California 16 -> ~30 and Florida 16 -> ~25 verified in A5. Medical office 16 -> 12: reproduced (12.02%) only through the lane's calibration (N3). Arizona keeps ~16% in six places (tile, meta, og, JSON-LD, prose, verdict), as C6 says (carried item, below).

### C7 VERIFIED
First half: A2. Second half ("the dash sweep changed punctuation only ... word sequence identical"): the sweep commit c21b055 against its parent c203580, all 150 changed non-docs files (html, feed.xml, styles.css, README.md, netlify.toml), tokens `\w+` of the whole file after decoding entities and JSON `\uXXXX`: 150 identical, 0 differ. The follow-up commit's word changes are the three non-dash edits in A4 plus `netlify.toml` and `scripts/mesh.py` (config and regex only).

### C8 VERIFIED
```
served non-held files matching PAT: tree 0, draft bytes 0 (the 4 held pages above are the only hits on the draft)
sister-domain links from non-held served files: none (all distinct external hosts read)
git log 1d48cc2..9896628 (9 commits, which covers the claim's 1d48cc2..5e25e47): author, committer, name, email and the full message: 0 matches of PAT; all nine commits by "Feasibility Study Company <noreply@feasibility-study-company.com>"; no ref or branch name matches
citations: the 23 non-held base pages that carried a name, sentence-diffed against freeze 2: every edit replaces the name with "industry research", "an industry database" or the primary source (e.g. "Janover Pro and industry research (2025)", "Industry research (2026) and multiple builders"), or drops it
           ("citing Sage/<name>" -> "citing Sage"); the multiset of numbers is identical in every edited sentence (0 changes of a figure or a year)
the one reword outside that pattern, research-notes/sba-feasibility-myth ("a loan-data site", "that site"), is ruled on in DECISIONS 42; numbers unchanged.
```

### C11 VERIFIED
Own parser: sitemap `<lastmod>` by URL; every `dateModified` anywhere in every JSON-LD block (after `json.loads`); visible "Updated"/"Last updated" dates (day or month precision); "Published" dates.
```
indexable pages 158 (non-held 144) = sitemap 158 URLs, both directions; 2 noindex pages absent from the sitemap; draft sitemap == tree sitemap
non-held indexable pages: all 144 have a JSON-LD dateModified, one value per page, equal to the sitemap lastmod; visible Updated equals lastmod on all 104 that show one;
  Published-only pages: visible Published == lastmod on all; visible Published == JSON-LD datePublished on all; datePublished never after lastmod
disagreements: 0     (same parser on base: 29)
11 pages have no visible date line (home, indexes, framework, About, legal): JSON-LD and sitemap agree
base -> freeze 2, own-date values where both versions carry one: 4 differ, exactly the four recomputed cases (dateModified 2026-10-10 -> 2026-10-16, tile, byline and sitemap all 10-16)
sitemap lastmod moved on 32 pages: the 4 above plus 28 where the page's own dateModified in base was already July (10-10 -> 07-10/11/12/13), i.e. the sitemap now follows the page
```
(Visible "Updated" lines were added on 42 pages whose JSON-LD already said 2026-10-10 or July; no own date value moved. Held pages excluded, as the claim says.)

### C15 VERIFIED
```
cmp base/<p>/index.html tree/<p>/index.html for the 14 held pages: 14 identical, 0 differ (diff -rq of each held page directory: nothing)
base == git archive 1d48cc2 (shown above), and git diff --name-only 1d48cc2 9896628 -- <the 14 paths>: empty
```

---

## Regression checks run beyond the brief (all clean)
- C1: 160 pages, exactly one `<title>` outside comments on each; 223 JSON-LD blocks, all parse.
- `scripts/{byline,regulatory,mesh,links,chrome,sitemap}.py --check` on a copy: all exit 0 ("0 problem(s) over 146 checked pages", "0 page(s) out of date").
- Punctuation damage scan over non-held visible text (",,", ":,", "(,", ", )", ",.", ":.", "::", ";,", "()"): 0 in base and in freeze 2. Placeholder hyphen in empty table cells is the only new `-` pattern.

## New defects

### N1 (major): `/case-studies/` card for the veterinary Michigan case shows 1.50x; the case page says 1.27x
`tree/case-studies/index.html:1022`: "A small-animal hospital: ... and a 1.50&times; DSCR." The page `case-studies/veterinary-michigan-sba/` carries 1.27x in the hero tile ("Stabilized projected DSCR, against the 1.25x acquisition floor"), the meta description, the JSON-LD description and the DSCR table (Y3 $825k / $647k) and says it "clears the 1.25x ... floor only narrowly". Not caused by this lane (the same card line is in base; both files are non-held), but it is the same class as first-round B1, a false and favourable figure on a public index page, and the lane's search for stale cards looked only near the four recomputed cases. Found by comparing every case card's DSCR on `/case-studies/` and the homepage (52 cards with a figure) with the target page's tile, meta and JSON-LD:
```
case cards with a DSCR/IRR figure checked (all non-held pages): 52 | mismatches: 1 -> ('case-studies/index.html', 'veterinary-michigan-sba', 'DSCR card', '1.50', ['1.27'])
```
Fix: 1.27&times; at line 1022 (the page's other 51 card figures agree).

### N2 (minor): Florida "about 25 percent" rests on two readings the page does not state
The lane's 25.0% is the 0% selling-cost result; the page says "net of ... selling costs" (3% gives 24.5%, 5% gives 24.2%), and it takes "cost to rebuild" as the whole $5.80M cost including the $1.35M land (the previous sentence on the page does speak of "the $5.80 million cost"). If the replacement cost excludes land: 1.15 x $4.45M = $5.12M terminal value, IRR 20.7% (0%) / 20.1% (3%); at 1.00 x the $5.80M cost: 22.8% / 22.3%. DECISIONS 41 records 24.5%, 22.8% and 20.7%; the page does not. "About 25" is the top of the 20-25 band. Within the page's own wording it is correct; a reader of "cost to rebuild" as improvements-only gets about 20.

### N3 (minor): the medical office 12% is a calibration, not a derivation from the page
Reproduced: calibrating the share of cash flow after debt service that is distributed (0.2799) so that the old 50/40/10 structure returns exactly 16.00%, the same share on 50/35/15 gives 12.02%. The 28% share is on neither the page nor in the claim; the page says only "modest interim distributions". Same anchor, constant-dollar distributions: 11.28%. 100% distribution: 34.4% old, 27.0% new; none: 8.8% old, 6.1% new. So "about 12" is relative to the old unverified 16, not fixed by the page's inputs (the exit equity of about $2.6M is). Disclosed in `recompute/medical-office-north-carolina-sba.md`; not on the page.

### N4 (minor): C3's protection of `docs/` now rests on deploy procedure, which a draft cannot show
`docs/` is no longer shielded by a file rule: any deploy of the raw tree (for example `netlify deploy --dir .` from the repo root) publishes `docs/` again and the case-variant URLs serve DECISIONS.md, the charter and INVENTORY.csv (the three files that contain ruling-10 names). Protection depends on (a) CLI deploys using `git archive | tar -x --exclude=docs --exclude=src` and (b) git builds running `[build] command = "rm -rf docs src"`; the draft proves only (a), I could not exercise (b), and per the brief I did not GET production, so I cannot say whether production still serves `/DOCS/web-fsc-2/INVENTORY.csv` until freeze 2 ships (the first round showed it did on the draft of 5e25e47). The `/docs/*` and `/src/*` 404 rules stay as a second line but are case-sensitive. DECISIONS 39 already tells later lanes to deploy the filtered tree; consider a deploy gate (assert `docs/` absent from the publish dir) rather than a convention.

## Carried and disclosed (not new, not counted)
- Arizona IRR stays "~16%" in six places (DECISIONS 41, owner item). My rebuild at 50/35/15 with Y1 funded from reserve: exit cap 7.5% 32%, 8.5% 30%, 10% 27%, 12.3% (the going-in yield on cost) 23%, 14% (value below cost) 20%. The page's "exit capitalization held wide of the going-in yield" does not give a number, so the lane's ruling "not fixed by the page" stands, but no reading consistent with the page gets to 16, and Arizona is now the outlier beside 30 (CA) and 25 (FL) for the same product.
- Held Texas RV case still says "10 percent SBA baseline" and "50% bank + 40% CDC", is linked from the three corrected RV pages (1 link on the California page) and carries 1.45x on `/case-studies/` (DECISIONS 43).
- Held pages: 56 `/inquiries/` links, 652 dashes, 4 pages with ruling-10 names (WEB-FSC-6's).
- Framework JSON-LD ItemList: 10 URLs, all 404 on the draft; `#glossary` referenced by three practice areas that have no such id (8 `inDefinedTermSet` hits each, 0 ids); two homepage pending slugs differ from the framework page's; `/states/washington/` at 320px; `.gitignore` U+2014 (dotfile, 404); `README.md`, `scripts/*`, `data/site/hold.json` served (DECISIONS 43).
- Observation, consistent with C11: pages the lane edited editorially (the four index cards, 24 punctuation fixes, 23 citation relabels) keep their old own dates and sitemap lastmod; only the four recomputed cases moved.

## Counts
Items: 12 (A1-A5, C2, C3, C6, C7, C8, C11, C15). VERIFIED 12, PARTLY 0, REFUTED 0.
New defects: blocker 0, major 1 (N1), minor 3 (N2, N3, N4).
