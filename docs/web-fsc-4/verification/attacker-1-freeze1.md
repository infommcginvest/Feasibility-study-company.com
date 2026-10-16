# WEB-FSC-4, attacker one, freeze 5e25e4783ca950b7274de9a0287245da221b72bc

Worked alone. I did not read attacker-2.md or verifier.md. All checks use my own code, kept in
`scratchpad/atk1/` (beside `freeze/`). Run every script with plain `python3` (bs4 and lxml are in the user
site, so `-I` cannot import them). The scripts read `freeze/tree` and `freeze/base` and write nothing into
either. The lane's scripts ran only on a throwaway copy (`scratchpad/atk1-copy`, removed afterwards). Every
network call was a GET to the draft with `curl -m 20`. I did not probe production. Forbidden names are
written here only in their bracketed regex form.

`D=https://6ad1f9a4bba14c3fdb9fa372--splendid-cannoli-80c225.netlify.app`
`PAT='m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er'`

## Count

- Blocker: 1 (A1)
- Major: 0
- Minor: 5 (A2 to A6)
- Notes that are not findings: N1 to N3

Summary:
- **A1 (blocker; breaks C8 and the purpose of C3; also C7's definition of "served").** The `/docs/*` 404 rule only matches lowercase. `/DOCS/...`, `/Docs/...`, `/dOcs/...` and `/docs%2F...` serve the docs tree byte for byte. Three served docs files carry a ruling-10 name. The `/src/*` rule has the same gap, so WEB-FSC-6's `src/` will be served the same way once it lands.
- **A2 (minor; C11 wording).** "Every indexable page has one date" is false on 11 held indexable pages. The claim does not exclude held pages.
- **A3 (minor; C2 wording).** "`/inquiries/` links are gone" is false sitewide: 56 remain on the 14 held pages, and all of them 404.
- **A4 (minor; C7 wording).** C7 defines "served" as everything except `docs/` and `src/`. That set includes `.gitignore`, which has an em dash on line 16. Netlify does not serve that file (404).
- **A5 (minor).** The JSON-LD ItemList on `/analytical-framework/` (lines 749 to 758) gives 10 URLs that 404 on the draft. The page body marks the same targets as pending spans. Separately, three practice areas point `inDefinedTermSet` at a `#glossary` id that does not exist on the page.
- **A6 (minor; pending typo class).** Two pending targets on the homepage do not match the slugs the framework page promises for the same layers: `demand-modeling` against `demand-analysis`, and `financial-projection-architecture`, which no layer promises. `--relink` will never switch them on.

---

## A1. BLOCKER: the docs tree is served under case variants of `/docs/`; served files carry a ruling-10 name

- **Claims broken:** C8 ("Outside the held pages no served file carries a name matching ..."). C3: `/docs/*` answers 404 only at the lowercase path, so the protection does not work. C7's definition (served = tree minus `docs/` and `src/`) is wrong, because `docs/` is served. DECISIONS 5 rests on the premise "`docs/` is not served (404)", which is false. Charter ruling 15 asks for "a source folder that is never served", which this rule does not give.
- **Files and lines:** `tree/netlify.toml:23` (`from = "/docs/*"`, `force = true`) and `tree/netlify.toml:31` (`from = "/src/*"`). Redirect matching is case-sensitive, while Netlify's static file lookup is not, and it also decodes `%2F`. The name-bearing files are:
  - `tree/docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md`, lines 67 and 115
  - `tree/docs/web-fsc-4/DECISIONS.md`, lines 8, 9 and 11
  - `tree/docs/web-fsc-2/INVENTORY.csv`, line 589
- **Reproduction:**
  ```sh
  for p in /docs/web-fsc-4/DECISIONS.md /DOCS/web-fsc-4/DECISIONS.md /dOcs/web-fsc-4/DECISIONS.md \
           /docs%2Fweb-fsc-4/DECISIONS.md /docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md \
           /Docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md /DOCS/web-fsc-2/INVENTORY.csv; do
    printf '%-46s ' $p; curl -s -m 20 "$D$p" -o probe.bin -w '%{http_code} '
    printf 'name-lines=%s sha=%s\n' "$(grep -ciE "$PAT" probe.bin)" "$(shasum -a 256 probe.bin | cut -c1-12)"; done
  ```
  Output:
  ```
  /docs/web-fsc-4/DECISIONS.md                   404 name-lines=0 sha=e68b0fea74b2
  /DOCS/web-fsc-4/DECISIONS.md                   200 name-lines=3 sha=55082fc3be55
  /dOcs/web-fsc-4/DECISIONS.md                   200 name-lines=3 sha=55082fc3be55
  /docs%2Fweb-fsc-4/DECISIONS.md                 200 name-lines=3 sha=55082fc3be55
  /docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md     404 name-lines=0 sha=e68b0fea74b2
  /Docs/web-fsc-4/input/WEB-FSC-4-CHARTER.md     200 name-lines=2 sha=9142b0965864
  /DOCS/web-fsc-2/INVENTORY.csv                  200 name-lines=1 sha=b7893846f8d5
  ```
  The tree files hash to the same values: DECISIONS.md `55082fc3be55`, the charter `9142b0965864`, INVENTORY.csv `b7893846f8d5`. Every other `docs/` file is reachable the same way. I confirmed `/DOCS/web-fsc-4/PENDING.csv` (200, 183,299 bytes). `docs/` holds 24 files with 7,476 dashes in C7's encodings.
  Variants that do 404: a different case lower in the path (`/docs/WEB-FSC-4/...`), a query string, and `//docs/...`. The bypass is a case change or an encoded slash in the first segment.
- **Scope:** `INVENTORY.csv` was already exposed at base, which has the same rule, so production almost certainly exposes it today. I did not GET production. The two WEB-FSC-4 files are new exposure. No page links to these URLs, and the repository is public, so the practical reach is limited. Still, C8 as written is false on the draft.
- **Severity:** blocker. It makes C8 false and C3's purpose untrue.

## A2. Minor (C11 wording): 11 held indexable pages break "Every indexable page has one date"

- **Claim:** C11, "Every indexable page has one date". Held pages are indexable (they are in `sitemap.xml` with `index, follow`), and C11 does not exclude them, unlike C2, C5, C7, C8 and C10. Gate 11 evidently skipped them.
- **Pages, with JSON-LD `dateModified` against the visible line:**
  - `/states/texas/`: no `dateModified` against "Updated October 10, 2026" (`tree/states/texas/index.html:1423`)
  - `/asset-classes/gas-station-and-c-store/`: no `dateModified` against "Updated October 10, 2026" (line 1384)
  - Nine held cases show JSON-LD `2026-10-10` against "Published July 13, 2026" with no Updated line:
    - auto-dealership-texas-sba
    - car-wash-texas-sba
    - gas-station-alabama-sba (`dateModified` at line 698, byline at line 841)
    - gas-station-florida-sba
    - gas-station-georgia-sba
    - gas-station-texas-sba (Published July 12)
    - hotel-texas-sba
    - rv-boat-storage-texas-sba
    - truck-stop-texas-sba
- **Reproduction:** `python3 scratchpad/atk1/dates_check.py | grep -E 'VISIBLE-DISAGREES|NO-dateModified'`. That prints these 11, plus two lines for `/` and `/analytical-framework/`. Those two are a byline paragraph with no date, which is not a date line, so I am not counting them.
- **Scope:** the defects are WEB-FSC-6's and unchanged from base (the held files are identical). The fix is the claim's scope: add "outside the held pages".

## A3. Minor (C2 wording): 56 `/inquiries/` links remain, all on held pages

- **Claim:** C2, "`/inquiries/` links are gone".
- **Reproduction:** `cd freeze/tree && grep -rho --include='*.html' 'href="[^"]*inquiries[^"]*"' . | grep -v docs | sort | uniq -c` prints `56 href="/inquiries/"`. All of them are on the 14 held pages (`grep -rl` lists exactly those 14). `curl -s -m 20 -o /dev/null -w '%{http_code}' $D/inquiries/` returns `404`.
- **Scope:** outside the hold the claim is true (my link check found 0). The defect is WEB-FSC-6's. Either the sentence needs the scope, or a `/inquiries/ -> /#contact` redirect would cover the held pages until they land.

## A4. Minor (C7 wording): `.gitignore` has an em dash and sits inside C7's definition of "served"

- **File:** `tree/.gitignore:16` (`# Draft page uploads — integrated ...`), unchanged from base.
- **Reproduction:** `grep -n $'—' freeze/tree/.gitignore` prints line 16. `curl -s -m 20 -o /dev/null -w '%{http_code}' $D/.gitignore` returns `404` (Netlify does not serve dotfiles).
- **Impact:** wording only, since no reader can reach it. Combined with A1, C7's definition is wrong in both directions: it includes a file that is not served and excludes `docs/`, which is.

## A5. Minor: JSON-LD on two kinds of page points at targets that do not exist

- **Framework ItemList:** `tree/analytical-framework/index.html`, lines 749 to 758, lists ten `url`s:
  - market-area-definition
  - demand-analysis
  - supply-and-competition
  - absorption-and-lease-up
  - revenue-and-rent
  - operating-expenses
  - coverage-and-stress-testing
  - regulatory-alignment
  - independence-and-evidence
  - common-review-failures

  All ten 404 on the draft, while the same page's body keeps them as `data-fsc-pending` spans (lines 1028 to 1143). The ItemList was already in base.
- **Glossary ids:** `inDefinedTermSet: ".../#glossary"` in `practice-areas/eb-5/`, `practice-areas/sba-7a-504/` and `practice-areas/usda-rural-development/` (lines 785 to 791 in each). None of the three pages has `id="glossary"`; only conventional-institutional does.
- **Reproduction:**
  - `python3 scratchpad/atk1/ext_check.py | grep -v '@id' | grep -E 'MISSING|FRAG'` prints 10 `itemListElement.url MISSING` and 21 `inDefinedTermSet FRAG`.
  - `for s in $(grep -o '"url": "https://feasibility-study-company.com/analytical-framework/[a-z-]*/"' freeze/tree/analytical-framework/index.html | sed 's#.*\.com##; s#"##'); do curl -s -m 20 -o /dev/null -w "%{http_code} $s\n" $D$s; done` prints ten `404`s.
  - `grep -c 'id="glossary"' freeze/tree/practice-areas/*/index.html` gives 1, 0, 0, 0.
- **Scope:** these are not `<a href>`, so C2 stands. Structured data still sends crawlers to 10 404s, which goes against the lane's own pending discipline.

## A6. Minor: two homepage pending targets do not match the framework page's slugs for the same layers

- **Files:**
  - `tree/index.html:1339`: "Demand Before Design" has `data-fsc-pending="/analytical-framework/demand-modeling/"`. The framework page's demand layer promises `/analytical-framework/demand-analysis/` (`tree/analytical-framework/index.html:1041`).
  - `tree/index.html:1351`: "The Projection Regime" has `data-fsc-pending="/analytical-framework/financial-projection-architecture/"`. No layer on the framework page or in its ItemList promises that page.

  Both slugs are inherited from base, which linked them directly.
- **Reproduction:**
  - `grep -n 'data-fsc-pending="/analytical-framework' freeze/tree/index.html freeze/tree/analytical-framework/index.html`
  - `grep -c 'demand-modeling\|financial-projection-architecture' freeze/tree/analytical-framework/index.html` returns 0.
- **Impact:** when the framework subpages ship under the framework page's slugs, `links.py --relink` switches on only exact targets. These two homepage cards would stay on the `#layers` fallback indefinitely. This is the typo-hiding case the brief names, in the form of a stale slug rather than one that exists.

---

## Items with no finding: what I ran and what it returned

### 1. Broken internal links (`scratchpad/atk1/links_check.py`, plus a draft sweep)

- **Method:**
  - Every `<a>` on the 146 non-held pages is resolved against its page URL. Hosts covered: feasibility-study-company.com and the www host, over http and https; root-relative, relative and fragment-only links.
  - Existence is checked case-exactly against the tree's file list. `/docs/` and `/src/` count as absent.
  - Redirect-only targets, missing trailing slashes, `#fragment` ids on the target, pending targets that exist or are redirected, and broken fallback hrefs are all flagged.
  - lxml and html.parser yield identical anchor lists on all 160 pages, and no page has an unbalanced comment.
- **Output:** `pages 160 held 14 {'a': 20088, 'internal': 19946} pending 1641` / `Counter()`. Zero problems: no missing target, no via-301, no missing fragment (5,439 fragment-only links included), no pending target that exists, no broken fallback. The 1,641 pending markers are 1,077 `<a>` plus 564 `<span>`.
- **Control:** `python3 links_check.py ../freeze/base` gives `MISSING: 2505`, so the checker does find broken links.
- **Draft:** all 163 distinct internal targets linked from non-held pages return 200 (`targets.txt` with a curl loop; nothing printed). All 160 pages on the draft are byte-identical to the tree, as are `sitemap.xml`, `robots.txt`, `styles.css` and the key file.
- **C3 aliases on the draft:**
  - `/asset-classes/{car-wash,gas-station,assisted-living,independent-living}` with and without the trailing slash, and with `/foo/` beneath, all return 301 to the stated hubs.
  - `/asset-classes/industrial/` returns 404, and `/docs`, `/docs/`, `/src`, `/src/` and `/src/x.html` return 404.
  - The key file returns 200. A1 still applies.
- **Lane tool gap (not a tree defect):** a mutation test on a copy showed that `links.py --check` catches a missing fragment, a typo target, an alias link and a pending target that exists. It does not flag `href="/states/nevada"` (no slash, resolves only through a Netlify 301). The tree has no such link.

### 2. Missing reverse edges (`mesh_check.py`, `parents_indep.py`, `parent_lists.py`, `topic_consist.py`)

- **Case to parent:**
  - Own-prose links (no mesh region, breadcrumb, chrome or `data-fsc-term`) give 187 edges: 62 state, 61 hub and 64 program, which matches DECISIONS 27.
  - I derived each case's state from its slug and its program from the suffix. Every case links exactly one hub, one program and its state in prose.
  - The only edges with no reverse are those whose parent is held: 14 to Texas or the gas station hub.
  - Every held case's non-held parent (for example Alabama for gas-station-alabama-sba) lists it.
- **Note topics:** of the 50 note-to-hub or note-to-program edges in `topics.json`, the only ones not listed back are the 5 to the held gas station hub (14 + 5 = 19, the lane's exempt count). Every note lists its hubs and programs.
- **Extra cross-checks, all clean:**
  - Each parent's case list contains only its own children, with no misses or duplicates.
  - Each hub's state list equals the states of its cases.
  - `state-neighbors` equals `topics.json`. I hand-checked all 32 rows as true land borders.
  - Each case's "Research notes for this case" list matches the topic map exactly.
  - Each `hub-notes` and `program-notes` entry is backed by `topics.json`.
- **Term-only mentions:** cases that term-link a hub, state or program other than their parent (for example hotel-nevada-eb5 linking California) are mentions, not parent edges, so they are not findings.

### 3. Inbound contextual links (`mesh_check.py`, `inbound_detail.py`, `inbound_strict.py`)

- **Rule:** inside `<main>`, excluding chrome regions and the breadcrumb nav, distinct non-index source pages, not the page itself.

| Kind | n | min | median |
|---|---|---|---|
| framework | 1 | 4 | 4 |
| hub | 28 | 4 | 14 |
| case | 64 | 3 | 6 |
| note | 19 | 8 | 33 |
| practice area | 4 | 9 | 59 (upper middle; the lane gives 58) |
| state | 32 | 3 | 8 |

- **Result:** minimum 3, and no page is under 3. The ten pages at exactly 3 are: auto-dealership-texas-sba (held), auto-service-new-jersey-sba, behavioral-health-massachusetts-conventional, coffee-shop-washington-sba, grocery-store-mississippi-usda, laundromat-new-mexico-sba, pet-boarding-oregon-sba, private-school-connecticut-conventional, veterinary-michigan-sba and `/states/washington/`.
- **Robustness:** the minimum stays at 3, with none under, when held pages are dropped as sources and when pending-fallback anchors are dropped. No inbound link sits in a hidden, `aria-hidden`, `template` or `noscript` ancestor. `<main>` holds no header, footer or nav other than the breadcrumb and the homepage anchor bar.

### 4. Identical generated link sets (`mesh_check.py`)

- 133 pages carry mesh regions. No two share an identical frozenset of mesh links.
- One single region repeats: `hub-notes` on quick-service-restaurant, childcare-and-daycare and fitness-and-recreation, all listing the same one note. The three whole sets differ.
- No mesh link points at its own page, none is duplicated within a page, and no `<ul>` in a mesh region is over 24 links (the maximum is 19).

### 5. Dates (`dates_check.py`, plus checks of each note's second line and the meta tags)

- **Sitemap:** 158 indexable pages and 158 sitemap URLs, the same set, with no duplicates. `/404.html` and `/tools/nda/` are `noindex, follow` and absent. Every indexable page carries `index, follow`.
- **Three-way agreement:** on every non-held indexable page, JSON-LD `dateModified` (exactly one distinct value per page), the visible line and the sitemap `lastmod` agree. That covers byline Published/Updated on cases and notes, the line-region "Updated" on hubs, states and practice areas, "Last updated" on the three legal pages, and every `<time datetime>` checked against its text.
- **Notes:** each note's second visible line ("Reviewed and updated: <Month YYYY>", all 19) agrees with `dateModified` by month. `/analytical-framework/` carries one as well (October 2026, which agrees). `article:modified_time` and `article:published_time` on the 19 notes agree and are unchanged from base.
- **Against base:** JSON-LD `dateModified` moved only on the four recomputed cases (2026-10-10 to 2026-10-16). Truck stop Oklahoma's previously commented-out JSON-LD already said 2026-10-10.
- **Only failures:** the 11 held pages in A2.

## Notes (not findings)

- **N1.** Beyond the four cases, two kinds of date change are visible against base. Both are by design (ruling 13; DECISIONS 33 and 34), but a reader or crawler will see them:
  - 38 case and note pages gained a visible "Updated October 10, 2026" (their JSON-LD already said so). Read-only `git log` shows a substantive WEB-FSC-2 commit on 10 October for each of the 38, so the date is true.
  - 31 sitemap `lastmod` values moved back to July.
- **N2.** For 18 of those 31, read-only `git log` shows the file was created or edited after its stated July date. Examples:
  - assisted-living-hawaii-hud was created in 52dca69 (2026-07-19 15:51) and edited in 996bd18 (2026-07-19 16:22), yet says Published and Modified 2026-07-13.
  - The "Sunbelt wave" cases were created 2026-07-21 (82ce6f1, d456950).

  Ruling 13 says "Today's dates are taken as true", so this is not a claim breach. It is an owner question whether a `lastmod` earlier than the creation commit is acceptable.
- **N3.** The other claims I tested held:
  - C1: 160 pages, one `<title>` outside comments each, every JSON-LD block parses.
  - C5: one header and one footer region per non-held page, identical apart from `aria-current`. The homepage uses `#contact` where other pages use `/#contact`.
  - C9: nothing.
  - C10: 52 non-held cases with the box directly after the H1 and byline.
  - C12: all six `--check` runs exit 0 on a copy.
  - C14: key file content equals its name, served 200.
  - C15: all 14 held directories are byte-identical between base and the tree.
  - C16: title, style and JSON-LD outside comments. Hawaii has six cards and its heading says "six markets".
  - C8's commit arm: author, committer and message of the 8 commits in 1d48cc2..5e25e47 carry no match.
