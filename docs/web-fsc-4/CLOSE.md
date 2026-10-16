# WEB-FSC-4 CLOSE

Wave 0 on feasibility-study-company.com: zero broken links, the two-way link mesh, one chrome source, 504 case math, disclosure boxes, dashes, dates, index all. Charter: `input/WEB-FSC-4-CHARTER.md`. Decisions: `DECISIONS.md` (43 items). Gate record: `GATES.txt`.

## Head, freezes, deploys

| | |
|---|---|
| Cut from | `main` = `origin/main` = `1d48cc2` (unchanged at issue, at every check during the lane, and before landing) |
| Freeze 1 | `5e25e4783ca950b7274de9a0287245da221b72bc`, archive sha256 `3bb6da2a5ba4...`, draft `6ad1f9a4bba14c3fdb9fa372` |
| Freeze 2 | `9896628866f26d591afec42c0c8b5b8f5df419e3`, archive sha256 `1b513fe087c8...`, draft `6ad20281fa0eff51c6dc288e` |
| Freeze 3 (final) | `f14f6b14d4afa1784477c1d4d5a2c4591cd40d93`, archive sha256 `c97a33e227fd5d54eba11b676293458f8f6448e735b0fa73ee58a6817aca2cb1`, draft `6ad20834bddcf24abc46238a` |
| Landed | `git push . HEAD:main` from the worktree: fast-forward `1d48cc2..f14f6b1` (no other lane had landed; `origin/main` still `1d48cc2`) |
| Production deploy | `6ad2086d3e2479e9245b02a6`, published 2026-10-16T11:20:15Z, from `git archive main` (`f14f6b1`) with `docs/` and `src/` excluded, byte-identical to the freeze 3 draft tree |
| Rollback point | `6acc9381d815c5ea34cbeee7` (commit `1d48cc2`, published 12 October) |

Commits after freeze 3 touch only `docs/web-fsc-4/` (this file and the gate record); the deployed tree never carries `docs/` or `src/`.

## Pages changed, by ruling (146 of the 146 non-held pages; the 14 WEB-FSC-6 pages are byte-identical to `1d48cc2`)

| Ruling | Pages | What |
|---|---|---|
| 1 Pending links | 65 pages with promised links in their body, plus the chrome on all 146 | 1,642 pending anchors to 463 distinct unbuilt targets (1,077 links to a truthful fallback, 564 spans, Ohio held out of the panel): metro 1,285, subtype 185, hub 131, framework 31, state 9, retired-infrastructure 1. Inventory: `docs/web-fsc-4/PENDING.csv`. `links.py --relink` switches each on when its page ships. |
| 2, 6 Chrome | 146 | One header, two mega panels and one footer from `data/site/chrome.json`, rendered by `scripts/chrome.py` into `<!--chrome:header-->` and `<!--chrome:footer-->` (20 header and 9 footer variants before). Inquiries and every "Request a methodology briefing" go to `/#contact` (115 pages had body CTAs to `/inquiries/`); "Published Analyses" is "Worked Cases"; "Infrastructure" is gone; Ohio hidden until its page exists; the seven metros pending to their state's `#metros`. |
| 3 Redirects | `netlify.toml` and 2 pages | 301: `/asset-classes/car-wash/*`, `/gas-station/*`, `/assisted-living/*`, `/independent-living/*`. `/asset-classes/industrial/` pending, not redirected. |
| 4 Mesh | 133 | Generated regions before the CTA band: state-cases, state-neighbors, hub-cases, hub-notes, hub-related, program-cases, program-notes, case-related, note-applied. The three hand-written Worked Cases sections are now generated. |
| 5 First mentions | 132 | 855 first-mention links from `data/mesh/terms.json` (84 terms), at most 15 per page. |
| 7 Case math | 4 + the case index | See below. |
| 8 Truck stop Oklahoma | 1 | The comment that swallowed 709 lines (title, meta, all CSS, JSON-LD) is closed; the page is styled again. |
| 9 Hawaii | 1 | "Four island counties, six markets, distinct demand fingerprints." over six cards. |
| 10 Sister-property citations | 23 | Relabelled to "industry research" or the primary source the page already cites; figures and years unchanged. The four held pages that still carry names are WEB-FSC-6's. |
| 11 Disclosure | 48 | The batch-1 `capsule disclosure` box under the H1 and byline of every older case outside the hold (52 cases now carry it). One contradicting sentence removed (assisted-living-north-carolina-hud). |
| 12 Dashes | 146 pages and 4 other served files | 5,752 dashes plus 60 JSON-escaped ones; words unchanged on every file. |
| 13 Dates | 110 | One date per page in JSON-LD, the visible line and the sitemap. |
| 14 Index all | sitemap, key file | 158 indexable URLs; IndexNow key `db7ea828330340f8994ca82a16c48c8b.txt`; `scripts/indexnow.py`. |
| 15 Source folder | `netlify.toml` | `/src/*` 404, and since freeze 2 `docs/` and `src/` are never deployed. |

## Links and redirects

`scripts/links.py --check`: 0 problems over the 146 non-held pages (19,946 internal anchors), against 2,720 broken anchors (480 distinct targets) at `1d48cc2`. The held pages keep 215 broken anchors until WEB-FSC-6 lands. On the freeze 2 draft every alias answers 301 to its hub, `/asset-classes/industrial/` answers 404, and `/docs/*` and `/src/*` answer 404 in every capitalisation tested (`/Docs/`, `/DOCS/`, `/dOcS/`, `/docs%2F`).

## Mesh, before and after

Contextual inbound links (distinct non-index pages, inside `<main>`, no breadcrumb, no chrome), `1d48cc2` -> freeze 2:

| Section | n | min | median |
|---|---|---|---|
| Hub | 28 | 1 -> 4 | 5.0 -> 14.0 |
| State | 32 | 1 -> 3 | 1.0 -> 8.0 |
| Case | 64 | 0 -> 3 | 0.0 -> 6.0 |
| Note | 19 | 0 -> 8 | 0.0 -> 33.0 |
| Practice area | 4 | 1 -> 9 | 15.5 -> 58.0 |
| Framework | 1 | 3 -> 4 | 3.0 -> 4.0 |

237 child-to-parent and note-topic edges, every one with its reverse except 19 whose parent is a held page (the Texas page and the gas station hub). No two pages carry the same generated link set.

## Chrome

`data/site/chrome.json` is the only place header, panel and footer links live. A lane that ships a page needs no chrome edit: `chrome.py` turns a pending or hidden link on by itself when the target exists. A lane that adds a link edits `chrome.json` and reruns `chrome.py`.

## Case math (ruling 7): 50/40/10 to 50/35/15

Scripts and logs: `docs/web-fsc-4/recompute/<slug>.py` and `.md`. Each reproduces every published before-figure first.

| Case | Equity | Debenture | Debt service | DSCR Y1 / Y2 / Y3 | IRR |
|---|---|---|---|---|---|
| rv-boat-storage-arizona-sba ($5.00M) | $0.50M -> $0.75M | $2.00M -> $1.75M | $424k -> $404k | 0.90/1.15/1.45 -> 0.95/1.21/1.52 | ~16%, held (owner item) |
| rv-boat-storage-california-sba ($6.10M) | $0.61M -> $0.915M | $2.44M -> $2.135M | $517k -> $493k | 0.90/1.15/1.45 -> 0.95/1.21/1.52 | ~16% -> ~30% |
| rv-boat-storage-florida-sba ($5.80M) | $0.58M -> $0.87M | $2.32M -> $2.03M | $492k -> $469k | 0.90/1.15/1.45 -> 0.95/1.21/1.52 | ~16% -> ~25% |
| medical-office-north-carolina-sba ($9.60M) | $0.96M -> $1.44M | $3.84M -> $3.36M | $814k -> $775k | 1.15/1.35/1.50 -> 1.21/1.42/1.57 | 16% -> 12% |

Tier: 13 CFR 120.910, 15% for a New Business (the three storage cases) or a limited or special purpose property (the surgery center, with the established physician group as operating company), stated on each page with the `sba:` markers and the eCFR source. No conclusion changed (all four stay feasible and bankable). IRRs: medical office by one calibrated payout share; California and Florida from the exits their pages state (decision 41); Arizona's exit is not fixed by its page, so its ~16% is held. The case index cards carry the new DSCRs.

## Dashes and fidelity

`docs/web-fsc-4/tools/dashes.py`: 5,752 occurrences on 150 served files (en dash to hyphen 2,441; em dash by rule 2,163; by sentence review 1,148 in 920 sentences), then 60 JSON-escaped em dashes on the case index. 29 pairs joined across a sentence break were repaired one by one after freeze 1. Fidelity: on the sweep commit every word of all 150 files is identical before and after; on the 24 repaired pages (California aside) every word is identical from freeze 1 to freeze 2. 0 dashes remain in served files outside the hold (652 remain on the held pages).

## Dates

Moved: the four recomputed cases only, to 2026-10-16. Every other page keeps its own date; 31 sitemap lastmods went back to the page's own July date because their only 10 October change was the WEB-FSC-1 byline wiring (decision 33). JSON-LD `dateModified`, the visible line and the sitemap agree on every indexable page outside the hold.

## Gates

| # | Gate | Result |
|---|---|---|
| 1 | Pages | GREEN: 160 pages, one title each outside comments, all JSON-LD parses |
| 2 | Links | GREEN: `links.py --check` exit 0 |
| 3 | Redirects | GREEN on drafts `6ad20281fa0eff51c6dc288e` and `6ad20834bddcf24abc46238a` and on production |
| 4 | Mesh | GREEN |
| 5 | Chrome | GREEN: `chrome.py --check` exit 0 |
| 6 | Case math | GREEN: four scripts rerun and `--check` exit 0; 15% row present; no old tier |
| 7 | Dashes | GREEN: 0 left; fidelity holds |
| 8 | Names | GREEN outside the hold; no sister-domain link; commit metadata clean |
| 9 | Credentials | GREEN: the grep returns nothing |
| 10 | Disclosure | GREEN: 52 cases, box directly under H1 and byline |
| 11 | Dates | GREEN: three-way agreement; moved list = the four |
| 12 | Markers | GREEN: byline, regulatory, mesh, links, chrome, sitemap `--check` exit 0 |
| 13 | Look | GREEN: screenshots in `look/`; no page-level horizontal scroll at 390px on any of the 160 pages (freeze 2 draft; freeze 3 changed one card figure) |
| 14 | Index all | GREEN: 158 URLs, key file served on the draft, `indexnow.py --dry-run` 145 URLs |
| 15 | Source folder | GREEN: `/src/anything` 404 |

Commands and full output: `GATES.txt`.

## Attackers and verifier

Freeze 1 went to two Opus attackers and a Sonnet verifier, separately; freeze 2 to a second Sonnet verifier. Every finding was reproduced here before it was resolved.

| Finding | Who | Resolution |
|---|---|---|
| Case index cards kept the old DSCRs of the four recomputed cases | verifier B1, attacker two (blocker) | Fixed (decision 37) |
| 60 em dashes in the case index JSON-LD written as `—` | verifier B2, attacker two (major) | Fixed; tools and gate now cover JSON escapes (decision 38) |
| `/Docs/...` and `/DOCS/...` served the lane records (names included); production has done so since 12 October | verifier M1, attacker one A1 (blocker) | Fixed: `docs/` and `src/` are never deployed (decision 39); production fixed by this deploy |
| 29 parenthesis pairs across a sentence break | attacker two (major) | Fixed, words unchanged (decision 40) |
| California and Florida IRRs contradicted their own stated exits | verifier M2, attacker two (major) | Recomputed (decision 41); Arizona held as an owner item |
| Held Texas RV case still at 50/40/10 | verifier M3 | WEB-FSC-6's page; owner item |
| Rounding, wording, structured data, 320px, served tooling, narrative frame, held-page dates, `.gitignore` dash (not served), claim wording | verifier and attackers (minor) | Ruled on in decisions 42 and 43, or claim wording corrected |
| Freeze 2 re-verification | second verifier (Sonnet) | 12 of 12 items verified, 0 refuted; one new major, the veterinary Michigan card (1.50x on the index, 1.27x on its page, stale since 10 October), fixed in freeze 3 with all 60 card figures rechecked (decision 44); three minors recorded |

Tally. Attackers found 13 (attacker one: 1 blocker, 5 minor; attacker two: 1 blocker, 3 major, 3 minor). Fixed on the site: 5 (the `/Docs/` exposure, the case index cards, the escaped dashes, the cross-sentence pairs, the California and Florida IRRs). The other 8 were ruled on: 3 were claim wording (held pages, `.gitignore`) and the claims were corrected; 2 are structured data and slugs left for the owner; 3 are kept as true (Florida rounding, the myth-note wording, held-page dates). Verifiers: first round 2 blockers and 3 majors, all fixed except M3 (a held page, owner item 5); second round 0 blockers and 1 major (fixed in freeze 3).

## Production checks

On https://feasibility-study-company.com after the deploy (GET only):

```
production checks on https://feasibility-study-company.com
200 /case-studies/rv-boat-storage-arizona-sba/ | H1: RV & Boat Storage Feasibility Study, Arizona: An SBA 504 Worked Case | titles outside comments: 1 | equity row: 15% | IRR tile: 16%
200 /case-studies/rv-boat-storage-california-sba/ | H1: RV & Boat Storage Feasibility Study, California: An SBA 504 Worked Case | titles outside comments: 1 | equity row: 15% | IRR tile: 30%
200 /case-studies/rv-boat-storage-florida-sba/ | H1: RV & Boat Storage Feasibility Study, Florida: An SBA 504 Worked Case | titles outside comments: 1 | equity row: 15% | IRR tile: 25%
200 /case-studies/medical-office-north-carolina-sba/ | H1: Medical Office & ASC Feasibility Study, North Carolina: An SBA 504 Worked Case | titles outside comments: 1 | equity row: 15% | IRR tile: 12%
200 /states/hawaii/ | H1: Hawaii Feasibility Studies | titles outside comments: 1 | Four island counties, six markets, distinct demand fingerprints.
200 /case-studies/truck-stop-oklahoma-sba/ | H1: Truck Stop Feasibility Study, Oklahoma: An SBA 504 Worked Case | titles outside comments: 1
200 /asset-classes/marina/ | H1: Marina & Boat Harbor Feasibility & Market Studies | titles outside comments: 1
200 /asset-classes/hotel/ | H1: Hotel & Hospitality Feasibility & Market Studies | titles outside comments: 1
200 /practice-areas/sba-7a-504/ | H1: SBA Feasibility Studies | titles outside comments: 1
200 /practice-areas/usda-rural-development/ | H1: USDA Feasibility Studies | titles outside comments: 1
301 /asset-classes/car-wash/ -> /asset-classes/express-car-wash/ OK
301 /asset-classes/gas-station/ -> /asset-classes/gas-station-and-c-store/ OK
301 /asset-classes/assisted-living/ -> /asset-classes/assisted-living-and-memory-care/ OK
301 /asset-classes/independent-living/ -> /asset-classes/assisted-living-and-memory-care/ OK
301 /asset-classes/car-wash/x/ -> /asset-classes/express-car-wash/ OK
404 /asset-classes/industrial/ (pending, not redirected)
200 CTA hrefs on /case-studies/hotel-florida-sba/: ['/#contact']
200 CTA hrefs on /states/oregon/: ['/#contact']
200 CTA hrefs on /research-notes/trade-area-is-the-study/: ['#contact', '/#contact']
200 CTA hrefs on /: ['#contact']
405 /api/contact GET: {"ok":false,"error":"Method not allowed."}
404 /docs/web-fsc-4/CLOSE.md
404 /docs/web-fsc-4/DECISIONS.md
404 /Docs/web-fsc-4/DECISIONS.md
404 /DOCS/web-fsc-2/INVENTORY.csv
404 /dOcS/web-fsc-2/CLOSE.md
404 /src/x
200 IndexNow key file: db7ea828330340f8994ca82a16c48c8b
sitemap: 158 URLs live; pages whose live date differs from lastmod or that do not answer 200: none
```

The published deploy read back from the Netlify API: `6ad2086d3e2479e9245b02a6`, state ready.

## IndexNow

`python3 scripts/indexnow.py --since 1d48cc2` at 2026-10-16T11:23:59Z: `IndexNow 202 Accepted: 145 URL(s) submitted` (144 changed indexable pages and `/sitemap.xml`; key `db7ea828330340f8994ca82a16c48c8b`, served at the root). Google reads the sitemap.

## Push and bundle

`git push origin main web-fsc-4` (prompts disabled) failed for credentials: `fatal: could not read Username for 'https://github.com': terminal prompts disabled`. No credential was looked for. `origin/main` is still `1d48cc2`.

**`main` is live but not on GitHub.** Production serves `main`'s tree (`f14f6b1` for every served file; the commits after it touch only `docs/web-fsc-4/`). Netlify builds and publishes GitHub `main` on every push, so nothing may push an older `main` to GitHub before this one, including a WEB-FSC-5 or WEB-FSC-6 branch cut from `1d48cc2` that has not merged this lane: that push would make Netlify rebuild and publish the old site over this one. To publish the history, from the repository with the owner's credentials: `git push origin main web-fsc-4` (a fast-forward from `1d48cc2`).

Bundle of `main` and `web-fsc-4`: `_bundles/web-fsc-4-<final main sha>.bundle` in the repository root (the sha is the one in the five-line report below); `git bundle verify` passes and a clone of it checks out exactly `main`, with an identical `git archive` hash.

## Owner items

1. Resubmit `https://feasibility-study-company.com/sitemap.xml` in Google Search Console (31 lastmods went back to the pages' own July dates; 158 URLs).
2. Arizona RV storage IRR: its page does not fix its exit, so the published ~16% is held; the cap rates it cites imply about 30%. Supply the exit assumption or relabel the tile (decision 41).
3. Medical office: 15% assumes the established physician group is the operating company; if the surgery-center entity is new, 20% applies.
4. Deploying lanes must publish the tree without `docs/` and `src/` (`git archive <ref> | tar -x -C <dir> --exclude=docs --exclude=src`); git builds do it through `netlify.toml`.
5. WEB-FSC-6 (or the second lane to land): empty `data/site/hold.json`, then run `chrome.py`, `mesh.py`, `links.py --relink`, `byline.py` and `sitemap.py` over the whole tree; the held Texas RV case still says 50/40/10 and four held pages still carry sister-property names.
6. Decisions 18 and 43: the "A sponsor came to our feasibility study company" narrative under the hypothetical-case box; `data/authors/mark-otava.json` (served, lists unverified credentials); the framework JSON-LD subpage URLs; the two homepage cards whose pending slugs the framework page does not use; the low-contrast dark-on-red Inquiries button (unchanged from before).
7. The charter copy in `docs/web-fsc-4/input/` names Wert-Berater in plain text, verbatim as issued; this public repository may want a redacted copy.
