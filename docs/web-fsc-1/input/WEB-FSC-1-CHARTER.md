# CHARTER WEB-FSC-1: PUBLISH BATCH 1 ON FEASIBILITY-STUDY-COMPANY.COM (FOUR CASES, NEW ABOUT PAGE, SITE-WIDE BYLINE) AND WIRE THEM IN

Issued 10 October 2026 for the owner.

| | |
|---|---|
| Session | WEB-FSC-1 |
| Site | feasibility-study-company.com |
| Repo | Found in step zero (the git repo that builds feasibility-study-company.com) |
| Branch | `web-fsc-1`, cut from the default branch head. Record the commit you cut from. |
| Owner input | `~/Downloads/deep searches/fsc-pages/` (read only, never written) |
| Records | `docs/web-fsc-1/` in the repo (committed) |
| Deploy | Only if the paste block says `Deploy pre-authorized: yes`, and only after every gate below is green |
| First action | Copy this charter and the owner input folder into `docs/web-fsc-1/input/` and commit them |

## Speed rules

1. Do not ask the owner questions. Decide under this charter, record each decision in `docs/web-fsc-1/DECISIONS.md`, and keep going.
2. Never end your turn while a build, a fetch or a gate is running. Wait for it in the foreground.
3. Stop only for: no repo found or more than one candidate (step zero), a red gate you cannot fix inside scope, or free disk under 1 GB.
4. Stage explicit paths only. Never `git add -A`. No credentials in the repo or in a log.

## Inputs

| File in the owner input | Becomes |
|---|---|
| `case-studies/rv-park-ossipee-new-hampshire-usda.md` | `/case-studies/rv-park-ossipee-new-hampshire-usda/` |
| `case-studies/cabin-resort-townsend-tennessee-sba.md` | `/case-studies/cabin-resort-townsend-tennessee-sba/` |
| `case-studies/glamping-oak-hill-west-virginia-usda.md` | `/case-studies/glamping-oak-hill-west-virginia-usda/` |
| `case-studies/dry-stack-cape-coral-florida-sba.md` | `/case-studies/dry-stack-cape-coral-florida-sba/` |
| `about/about.md` | Replaces the body of `/the-practice/` at the same URL |
| `byline/byline-spec.md` | Author record, byline and signature components, author JSON-LD (spec, not a page) |
| `README.md` | The wiring list. Read it first. |

## Hard constraints

1. **The text is published word for word.** It may differ from the input only by:
   - converting Markdown and front matter into the repo's own content format and components (tables, breadcrumbs, CTA, sources list, related links);
   - resolving `{{byline}}` and `{{signature}}` through the byline components;
   - correcting an internal link path to the route the site actually uses, each one logged in `DECISIONS.md`.

   Never reword a sentence, never change a figure, never add claims.
2. **Credentials.** Do not type "Ph.D.", "CCIM" or "MAI" next to Mark Otava's name anywhere: not in copy, metadata, JSON-LD, alt text or the author record's name field. The credentials render only through the display rule in `byline-spec.md`: a credential shows only when its `verify_url` is a live `https://` link. Ship the author record with the `verify_url` fields empty, exactly as the spec gives them. The owner fills them later, and every page updates from that one file.
3. **About page slots.** The input About page contains `[VERIFY BEFORE PUBLISHING: ...]` and `[BIO: ...]` placeholders. They must never appear on the live site. Build the credentials table from the author record and render only rows with a `verify_url`. If no row qualifies, render no table and keep the sentence above it. Render the bio paragraph from `bio_short`, and omit it while that field is empty. Put the JSON-LD from the HTML comment at the end of `about.md` into real `<script type="application/ld+json">`, with `hasCredential` built only from verified entries.
4. **Disclosure.** Each case keeps its "Representative worked example" box exactly as written, directly under the H1 and byline.
5. **Names.** No page, file, metadata field or commit message may contain any of the five withheld names. [REDACTED IN THIS COPY under constraint 5; the list is in the owner's original, sha256 c1c4623c021401882086999d360161da1a236cb30f05c69a3e32bc50aa923a2b.]
6. **Scope.** Only the following change:
   - the four case pages and their index entries;
   - the About page body at `/the-practice/`;
   - the byline system (author data, byline and signature components, author JSON-LD) on the page types listed in `byline-spec.md` section 2;
   - "Worked cases" blocks on the three asset hubs, and case links on the New Hampshire and Florida state pages;
   - the homepage counters;
   - generated files: sitemap, lastmod, link modules.

   No other copy, layouts, redirects or hosting settings change.

## Step zero: find the repo

1. Look under `~` (skip `~/Library`, caches and `node_modules`) for git repos whose remote, config or site settings reference `feasibility-study-company.com`. Check `git remote -v`, framework config (`astro.config.*`, `next.config.*`, `site` fields), `netlify.toml`, `vercel.json`, `CNAME` and `package.json`.
2. If none is found locally, run `gh repo list` against the owner's accounts and look for it. Clone it into `~/` next to the owner's other site repos.
3. Exactly one match: use it. None, or more than one: stop and report the candidates.
4. Record the framework, the content format used for case studies (open the source of `/case-studies/rv-park-pennsylvania-usda/` and mirror it), the build command, the deploy mechanism and the default branch. Then run a clean baseline build and record its page count.

## The work

1. **Byline system first.** Create the author record (`byline-spec.md` section 1) in the repo's data folder. Build the byline and signature components with the display rule in the template, not by hand. Add the `author` JSON-LD reference (section 4). Apply them to every page type in section 2: homepage line, case studies, research notes, asset-class pages, practice-area pages, analytical framework pages, state and metro pages, and the About page.
2. **Four case pages.** Convert each input into the house case format. Keep every table, the FAQ (as content; no rich-result expectation), the numbered sources with their links, and the related links. Title tag and meta description come from front matter. Canonical is the page's own URL. Schema: Article and BreadcrumbList.
3. **Case index.** Add the four cases to `/case-studies/` in the same style as the existing entries.
4. **Asset hubs.** Add a "Worked cases" block, styled like existing related-content blocks, to:
   - `/asset-classes/rv-park-and-campground/`: Ossipee NH, plus the Maine, Pennsylvania, Texas and Arizona RV park cases
   - `/asset-classes/glamping/`: Townsend TN, Oak Hill WV, plus the Utah glamping case
   - `/asset-classes/marina/`: Cape Coral FL, plus the Maryland marina case
5. **State pages.** Link Ossipee from `/states/new-hampshire/` and Cape Coral from `/states/florida/`. Tennessee and West Virginia have no state page. The two cases link to `/states/` until those pages exist, and you do not create them in this lane.
6. **About page.** Replace the body of `/the-practice/` under constraint 3. Keep its URL, header and footer.
7. **Homepage counters.** Make them match the built site: asset classes, state profiles and worked cases. Generate them from the content collections at build time if the framework allows; otherwise set them to the counted values and log how you counted. The input expects 28, 32 and 64. If your counts differ, use yours and log it.
8. **Sitemap.** Include the four new URLs. Set lastmod to the build date for every page this lane changed.

## Gates (all must be green before any deploy)

1. The build passes, and the page count is the baseline plus 4.
2. **Text fidelity.** For each case and the About page, strip markup from the built HTML and diff it against the input text, minus front matter, tokens and the allowed transformations. Every difference is listed and justified in `DECISIONS.md`.
3. **Credentials.** `grep -riE "otava,? *(ph\.?d|ccim|mai)"` across source and built output returns nothing while the `verify_url` fields are empty. Then, in a throwaway local build only, fill one test `verify_url` and confirm that credential appears in the byline, the signature and the About JSON-LD. Revert the change and do not commit it.
4. **Placeholders.** `grep -r "\[VERIFY\|\[BIO\|{{byline}}\|{{signature}}"` in built output returns nothing.
5. **Names.** A case-insensitive grep for the five withheld names across changed files and built output returns nothing. [Pattern REDACTED IN THIS COPY under constraint 5.]
6. **Links.** Run an internal link check on the built site. Zero new broken links. Separately, list pre-existing broken links (the homepage metro links and some asset links may 404) in `docs/web-fsc-1/PREEXISTING-404S.md` without fixing them.
7. **Schema.** Every JSON-LD block on changed pages parses. The case pages carry Article, BreadcrumbList and an author `@id`.
8. **Disclosure.** All four case pages render the "Representative worked example" box.
9. **Look.** Screenshot each new page and the About page at desktop and mobile widths into `docs/web-fsc-1/look/`. Fix any table overflow or broken layout.

## Deploy

- If `Deploy pre-authorized: yes` is in the paste block and every gate is green, deploy through the repo's normal path. For a PR-based pipeline: push `web-fsc-1`, open a PR, merge it and confirm the production deploy. For a CLI deploy (Netlify or Vercel): deploy from a clean build, dry run first if the tool supports one.
- After the deploy, fetch each new URL and `/the-practice/` from production. Confirm HTTP 200 and the expected H1, and confirm `sitemap.xml` lists the four new URLs.
- Otherwise, push the branch, open the PR and stop.

## Close

Write `docs/web-fsc-1/CLOSE.md` covering:

- the repo and commit you cut from;
- the files changed;
- each gate with its command and result;
- the deploy id or PR link, with production checks;
- link-path corrections;
- counter values and how they were counted;
- the pre-existing 404 list;
- one line telling the owner exactly which file and fields to fill to switch on the verified credentials.
