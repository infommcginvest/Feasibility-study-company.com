# WEB-FSC-1 decisions

Each decision taken under the charter without asking the owner, in the order it came up. "Charter" means `docs/web-fsc-1/input/WEB-FSC-1-CHARTER.md`.

## Step zero

1. **Repo.** One candidate after an unbounded search of `~` (all `.git` directories outside `~/Library` and `~/.Trash`, checking remotes and `CNAME`, `netlify.toml`, `robots.txt`, `astro.config.mjs`, `package.json`): `~/Downloads/Feaisbility-Study-Company.com`, remote `origin` on GitHub (repository `Feasibility-study-company.com`). `gh` is not installed, so the GitHub listing in step zero 2 was not needed and not run.
2. **Framework.** None. The site is hand-written static HTML with inline CSS on every page. Netlify publishes the repository root (`publish = "."`), there is no build command, and every push to `main` deploys automatically (repo README). Default branch `main`. Case-study format: one `index.html` per case under `case-studies/<slug>/`, mirrored from `/case-studies/rv-park-pennsylvania-usda/`.
3. **Cut point.** Branch `web-fsc-1` was cut from `main` at `d456950`, equal to `origin/main` after a fetch.
4. **What "build" means here.** With no build step, the built site is exactly the committed tree Netlify serves. Gates run against `git archive <ref>` exported to a scratch directory. Baseline (`d456950`): 155 HTML pages. Built: 159 (155 + 4).

## Records and names

5. **The charter copy is redacted.** Constraint 5 lists the five forbidden names, and its gate repeats them as a grep pattern. Copying the charter verbatim would put those names in a committed file. The committed copy replaces those two lines with a note. The owner's original is unchanged, sha256 `c1c4623c…a2b`.
6. **The byline-spec copy is redacted in one sentence.** Its example of the credentialed display name would put credential abbreviations next to the principal's name in a committed file, which constraint 2 forbids. The fix was folded into the first commit before anything was pushed. Original sha256 `5407cfb3…b45`. The four case files and `about.md` are byte-identical to the owner input.
7. **Commit identity.** The repo's local git config uses an email on the sister-firm domain. Constraint 5 bars that name from commit metadata, so this lane's commits use `Feasibility Study Company <info@feasibility-study-company.com>` via `-c` flags. The repo config itself is unchanged.
8. **`docs/` is publicly served after merge.** Netlify serves the repository root, and `/README.md` already returns 200 in production. So `docs/web-fsc-1/` (records, owner input, screenshots, tools) would be public at `/docs/web-fsc-1/…` once merged, including the input README's note that no public record of the credentials was found. The charter puts the records there and forbids hosting changes, so they stay. The owner decides before merging. Options: drop or move the `docs/` commits, or add a Netlify rule that 404s `/docs/*`. This is also why gate 4 is red (decision 30).

## Byline system

9. **How it is built.** There is no template engine, so `scripts/byline.py` is the template. It reads `data/authors/mark-otava.json`, applies the display rule (a credential shows only when `verify_url` starts with `https://`), and writes every byline, signature, the About credentials table and bio, the author JSON-LD and the counters between `<!--fsc:NAME-->…<!--/fsc:NAME-->` markers. Running it again with no change is a no-op, and `--check` exits 1 when pages are stale. It is not wired into Netlify, because that would mean adding a build command, a hosting-setting change the charter forbids. After editing the record, the owner runs the script and commits.
10. **Credential order.** The suffix follows the order of the record's `credentials` array, as in the spec's pseudo-code: Ph.D., MAI, CCIM. The spec's prose example lists CCIM before MAI. Reordering the array changes the order everywhere.
11. **Placements** (spec section 2):
    - Homepage: the "Research directed by" line sits at the end of the hero, under the independence charter box.
    - Case studies and research notes: the byline goes directly after the H1. Existing cases get the signature after the sources list, because they have no related-links block. The new cases get it after their Related line. Research notes get it at the end of the article body.
    - Analytical framework: "Written by" after the H1, and a signature after its sources list (it is the methodology page).
    - Asset-class, practice-area and state pages: the reviewed-by line goes directly above the `<ol class="sources">` list.
    - About: the "Who stands behind the research" section.
    - Not bylined: the hub index pages (`/asset-classes/`, `/states/`, `/case-studies/`, `/research-notes/`, `/practice-areas/`) and the legal pages. They are not in the spec's table. No metro pages exist.
12. **Dates in bylines.**
    - Existing cases and notes: "Published" comes from each page's JSON-LD `datePublished`. Their data-as-of date is unknown, so that segment is omitted rather than invented. The new cases use `data_as_of` from front matter, shown as "October 2026".
    - Asset, practice and state pages: they carry no `dateModified`, so "Updated" is the date of the file's last content commit before this lane, frozen into the marker on first render. Adding a byline is not a content update, so it does not move that date.
13. **Author JSON-LD.** On Article pages (cases, notes, framework) `author` now references the Person `@id`, and `publisher` stays `#org`. Asset, practice and state pages and the homepage use `Service` or `WebSite` nodes, which cannot carry `author`. Those pages get one extra JSON-LD block with a `WebPage` node (`<url>#webpage`, the id three state pages already use) that carries the author reference. The full Person node, with `hasCredential` built only from verified entries, lives on the About page alone.
14. **CSS.** Every page inlines its own CSS, so the byline and signature styles go into each bylined page as one managed `<style>` block.

## Four case pages

15. **Shell.** The new cases use the Pennsylvania RV park case's head, CSS, header, mega-menu, footer and script verbatim, with title, description, canonical, og and twitter fields from front matter. The title tag is the front-matter `title` exactly, with no brand suffix, as the charter says. The JSON-LD has Organization, Article (headline = H1) and BreadcrumbList.
16. **Components.**
    - Each `##` section becomes a house `section` with alternating backgrounds.
    - Tables become `data-table-wrap` / `table.data`, and lists go inside `.prose`.
    - The disclosure blockquote becomes a `capsule disclosure` box directly under the H1 and byline. The intro paragraph becomes the hero sub-line.
    - The FAQ becomes the house `faq-list` (`details`/`summary`) with no FAQPage schema.
    - The "Planning…?" section becomes the house `cta-band`.
    - Sources become `ol.sources` with `id="sN"`, each URL kept as visible link text.
    - The Related line stays a paragraph after the sources.
    - Bare `[n]` citations link to `#sN`, and their text is unchanged.
17. **Labels added (component chrome, not claims).** The hero eyebrow reads "Case Study · {state} · {front-matter breadcrumb 3} · {program}". The breadcrumb uses the front-matter `breadcrumbs`, with item 3 linking to the front-matter `asset_class`.
18. **Tennessee and West Virginia.** No state pages exist. The input's Related lines already link `/states/`, and the front-matter `state` values are not used in any link. No state pages were created.
19. **Mobile tables.** At 390 px no page scrolls sideways. On phones, figures stay whole and the widest numeric tables scroll inside their own box, as house tables already do on the homepage and the marina hub. Breaking figures mid-number ("$116,9 / 36") was tried and rejected as unreadable.

## Link-path corrections (the only text-level link changes)

20. **`/inquiries/` does not exist** (404 in production). The site's inquiry route is the contact form: `/#contact` on the homepage, `#contact` on pages that carry the contact band.
    - Each case page, CTA button "Request a methodology briefing": `/inquiries/` → `/#contact` (4 corrections, one per case).
    - About hero button "Request a methodology briefing": `/inquiries/` → `#contact`.
    - About CTA button "Request a methodology briefing": `/inquiries/` → `#contact`.
    - Total: 6, matching the 6 `/inquiries/` links in the input. Every other input link resolves as written.
21. **House chrome is not corrected.** The header, mega-menu and footer were copied verbatim, including their pre-existing broken targets (`/inquiries/` in the case header, the metro links, `/published-analyses/`, `/asset-classes/limited-service-hotel/`). Fixing the chrome on four pages only would fork the template. The list is in `PREEXISTING-404S.md`.

## About page

22. **Kept.** The URL, header, footer and the contact band (it sits after `</main>`, beside the footer) stay as they were. The `<main>` content is replaced, and the title, description, og and twitter fields come from front matter.
23. **Hero.** The lede becomes the hero sub-line. The three " · "-separated links become three hero buttons, so the two "·" separators are dropped (text-fidelity class D).
24. **Stat band.** The four-column figure table becomes the house stat band. 28, 32 and 64 are generated counters, so they stay true as the site grows. Today they equal the input. The 4 is static.
25. **Credentials and bio.** The `[VERIFY BEFORE PUBLISHING …]` table is replaced by a generated region that renders only rows with a verified URL. Today there are none, so no table renders. The sentence above it and the sentence after it are kept. The `[BIO: …]` paragraph is replaced by a region that renders `bio_short`, which is empty today, so it renders nothing.
26. **JSON-LD.** The graph from the HTML comment at the end of `about.md` is rendered by the generator, with `hasCredential` built from verified entries only. A BreadcrumbList node was added because front matter lists it. The old page's FAQPage and AboutPage nodes are gone with the old body.

## Wiring

27. **Case index.** Four cards were appended to the published grid in the existing style. Card title = front-matter `title`, card text = front-matter `meta_description`, card category = program · state, and the cite label is in the existing cards' style.
28. **Hubs and state pages.**
    - Each of the three hubs gets a "Worked Cases" `link-cols` block after its By Market block, styled like that block. Link text for existing cases is the title from their index card.
    - New Hampshire and Florida each get a one-link block after their By Asset Class block.
    - Other Florida cases (gas station, hotel, multifamily and others) are not linked from the Florida page. That is a pre-existing gap outside this lane's scope.
29. **Homepage counters.** Asset classes (25 → 28) and state profiles (12 → 32) are now generated by `scripts/byline.py`, counting directories with an `index.html` under `asset-classes/`, `states/` and `case-studies/`. The homepage had no worked-cases counter, so a fifth stat, "Worked Cases Published" (64), was added and the homepage stat grid changed from 4 to 5 columns on desktop. The mobile grid is unchanged. Counts match the input's 28, 32 and 64.
30. **Sitemap.** Four new `<url>` entries were added. lastmod was set to 2026-10-10 on the 146 existing URLs whose page this lane changed, and on the 4 new ones (150 total).

## Gates

31. **Gate 2 differences, by class** (every one is listed in GATES.txt):
    - **A.** Inserted component chrome: hero eyebrow, breadcrumb.
    - **B.** Resolved tokens: byline text and signature text.
    - **C.** CTA conversion: the paragraph's trailing link becomes a button, and the "." after the link is dropped (one per page).
    - **D.** About only: hero link separators "·" dropped; stat table reordered from row-wise (numbers, then labels) into stat cards (number + label); the `[VERIFY …]` table and `[BIO: …]` slot removed, as constraint 3 requires.
    - No word or figure of the input differs otherwise.
32. **Gate 4 is red only because of the records.** Served HTML has 0 placeholder hits. The 10 hits are the committed input copies and tools under `docs/web-fsc-1/`, which Netlify would publish (decision 8).
33. **Gate 5 is red only because of pre-existing pages.** 42 published pages already contain the sister-firm abbreviation in their source citations at baseline `d456950`. This lane added 0 occurrences. Removing them means rewording existing citations, which is outside scope and would change attributions. The owner decides.
34. **Gate 7b was added during the look pass.** That pass caught a converter bug: a `<title>` mention inside the REBRAND comment swallowed the real title and the inline CSS on the new pages. It was fixed in `7464310`, and gate 7b now checks every changed page's head.
35. **Pre-existing broken head: `/case-studies/truck-stop-oklahoma-sba/`.** At baseline and in production, its REBRAND comment swallowed the `<title>` line, so the head CSS and the header are commented out. The byline style marker now closes that comment earlier: the page still renders without its CSS, but the header now shows. A one-line markup repair was attempted and refused by the session's permission policy as outside scope, so it is left for the owner (see CLOSE.md).
36. **Gate 3 live test.** In a throwaway copy outside the repo, the MAI `verify_url` was set to a test https link and the generator re-run. "MAI" then appeared in the byline (linked), the signature, the About credentials table and the About Person `hasCredential`, and the Person `name` field stayed the bare name. The copy was deleted, and nothing from it was committed.
37. **Identity not verified.** This lane did not verify that the named principal or the role exists. The site will state both on 150 pages. The credentials and bio stay empty until the owner fills them.
