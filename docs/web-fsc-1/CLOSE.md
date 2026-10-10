# WEB-FSC-1 close

Closed 10 October 2026. **Not deployed, not pushed, no PR.** The charter's paste block did not say `Deploy pre-authorized: yes`, so the lane stops at push and PR. The push also failed (see Deploy).

## Repo and cut point

- Repo: `~/Downloads/Feaisbility-Study-Company.com`, remote `origin` on GitHub (repository `Feasibility-study-company.com`). It was the only candidate in an unbounded search of `~`.
- Static HTML with no build step. Netlify publishes the repo root and auto-deploys pushes to `main`.
- Branch `web-fsc-1`, cut from `main` at **`d456950`** (equal to `origin/main` after a fetch).
- Baseline: 155 HTML pages. Built: 159.

## Files changed (177 against `d456950` before the final records commit, which adds DECISIONS.md, GATES.txt and CLOSE.md)

| Area | Files | What |
|---|---|---|
| `case-studies/` | 65 | 4 new case pages, a byline and signature on the 60 existing cases, 4 new cards on the index |
| `asset-classes/` | 28 | Reviewed-by line and author JSON-LD on all 28; Worked Cases block on RV park, glamping and marina |
| `states/` | 32 | Reviewed-by line and author JSON-LD on all 32; case link on New Hampshire and Florida |
| `research-notes/` | 18 | Byline, signature, author JSON-LD |
| `practice-areas/` | 4 | Reviewed-by line, author JSON-LD |
| `analytical-framework/index.html` | 1 | "Written by" byline, signature, author JSON-LD |
| `the-practice/index.html` | 1 | New body from `about.md`; credentials, bio and JSON-LD generated from the author record |
| `index.html` | 1 | "Research directed by" line; counters generated (28, 32, plus a new 64 worked-cases stat) |
| `sitemap.xml` | 1 | 4 new URLs; lastmod 2026-10-10 on 150 URLs |
| `data/authors/mark-otava.json` | 1 | Author record, exactly as byline-spec.md gives it (`verify_url` fields empty) |
| `scripts/byline.py` | 1 | The byline template and display rule; run it after editing the record |
| `docs/web-fsc-1/` | 24 | Charter and input copies, tools, 12 screenshots, these records |

## Commits on `web-fsc-1`

`0043d60` charter and input · `acf6ebf` author record, generator, tools · `488575f` four cases, About, byline, wiring · `7464310` head fix for the new pages, gate runner · `3174ad7` and `77314bc` phone tables · `e86e535` screenshots, 404 list · then a final commit for the records (DECISIONS, GATES, CLOSE).

## Gates

Command (records in `GATES.txt`):

```
git archive HEAD | tar -x -C <dist> && git archive d456950 | tar -x -C <base>
git diff --name-only d456950 HEAD > changed.txt
FSC_CHANGED=changed.txt python3 docs/web-fsc-1/tools/gates.py <dist> <base> .
```

| Gate | Result | Detail |
|---|---|---|
| 1 Build and page count | GREEN | 155 → 159; the 4 added pages are exactly the 4 cases |
| 2 Text fidelity | GREEN | The only differences are component chrome, resolved byline and signature tokens, the CTA trailing ".", About link separators, the stat-band order, and removal of the `[VERIFY]`/`[BIO]` slots. All listed in GATES.txt; classes justified in DECISIONS 31 |
| 3 Credentials | GREEN | `grep -riE "otava,? *(ph\.?d\|ccim\|mai)"` over the working tree and the built tree: 0 hits. Throwaway test with one MAI test link: credential appears in byline, signature, About table and About JSON-LD; reverted, never committed |
| 4 Placeholders | **RED, records only** | Served HTML: 0 hits. 10 hits are the committed input copies and tools under `docs/web-fsc-1/`, which Netlify would publish on merge (DECISIONS 8 and 32) |
| 5 Names | **RED, pre-existing** | 42 published pages already cite the sister-firm abbreviation in their source lists at `d456950`; this lane added 0. Fixing them means rewording existing copy, outside scope (DECISIONS 33) |
| 6 Links | GREEN | Broken internal targets: 482 at baseline, 482 built, 0 new. List in `PREEXISTING-404S.md` |
| 7 Schema | GREEN | Every JSON-LD block on all 150 changed pages parses; the 4 cases carry Article, BreadcrumbList and author `@id` `#mark-otava` |
| 7b Head sanity (added) | GREEN | No changed page has a broken head because of this lane. One pre-existing broken head, see below |
| 8 Disclosure | GREEN | "Representative worked example" box directly under H1 and byline on all 4 cases |
| 9 Look | GREEN | Desktop 1440 and mobile 390 captures of the 4 cases and About in `look/` (plus homepage and RV hub). No page-level horizontal scroll at 390; wide numeric tables scroll inside their own box, as house tables already do |

Sitemap: all 4 new URLs listed, and lastmod is 2026-10-10 on every one of the 150 changed pages.

## Deploy

None. The charter did not pre-authorize a deploy. The push failed too:

- The HTTPS remote has no stored credentials.
- The machine's SSH key is a deploy key for a different repo.
- The only other credential is the token file in the repo root, which this lane did not read.

To publish the branch and open the PR, run from the repo:

```
git push -u origin web-fsc-1
```

then open the GitHub compare page for `main...web-fsc-1` on that repository and create the PR.

**Before merging, decide about `docs/`.** Merging deploys, and Netlify serves the repo root, so everything under `docs/web-fsc-1/` would be public. That includes the input README's note that no public record of the credentials was found. Either drop or move the `docs/` commits before merging, or add a rule that 404s `/docs/*`.

Production checks (HTTP 200, H1, sitemap) were not run, because nothing was deployed.

## Link-path corrections

`/inquiries/` does not exist (404 in production). Corrected to the contact form: `/#contact` on each case's CTA button (4), `#contact` on the About hero and CTA buttons (2). These are all 6 of the input's `/inquiries/` links. Every other input link resolves as written. Tennessee and West Virginia link `/states/` as the input already does.

## Counters

`scripts/byline.py` generates them from the content folders: a count of directories with an `index.html` under `asset-classes/` (28), `states/` (32) and `case-studies/` (64). They are rendered on the homepage and in the About stat band. They match the input's 28, 32 and 64. The homepage had no worked-cases counter, so one was added, and the desktop stat grid went from 4 to 5 columns.

## Pre-existing 404s

482 distinct targets: the metro links, `/states/ohio/`, `/published-analyses/`, `/inquiries/`, `/asset-classes/limited-service-hotel/`, many unbuilt sub-pages, and more. Full table in `PREEXISTING-404S.md`. None were fixed.

## Left for the owner

1. **Broken page in production:** `/case-studies/truck-stop-oklahoma-sba/` renders without its CSS. On line 6, the REBRAND comment swallowed the `<title>` line. Replace `<!-- REBRAND SWAP POINTS: <title>Truck Stop` with the standard comment line (`<!-- REBRAND SWAP POINTS: <title>, meta, og, .wordmark, schema "name", footer -->`) followed by `<title>Truck Stop` on its own line. The repair was refused in this session as outside scope.
2. The 42 pages with the sister-firm abbreviation in their citations (gate 5).
3. `docs/` publication (above).
4. This lane did not verify that the named principal or the role exists. Both now appear on 150 pages.

## Switching on the verified credentials

Fill `verify_url` (an `https://` link to the issuing body's public record), plus `name` and `issuer` for the Ph.D., for each credential in **`data/authors/mark-otava.json`**. Then run `python3 scripts/byline.py` and commit the pages it rewrites. `bio_short` and `same_as` in the same file switch on the About bio and `sameAs`.
