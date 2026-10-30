# CASE-NEW-1 case writer brief (Sonnet)

You write ONE worked case for feasibility-study-company.com at case standard v3: a page source and its case-model input. The lane owner gates, reviews and commits; you never touch a git repository or commit anything.

## Machine scope

- Read: your research file (path in ~/Downloads/fsc-rollout/drafts/case-new-1/research-paths.tsv), the reader outputs in your case folder (facts.tsv, precount.txt, dnu.tsv), PA-USDA (same tsv) when your case is USDA B&I, and anything under ~/Downloads/wt-rollout-case-new-1/ (READ ONLY: the factory, exemplar cases, sba.json, the rulebook docs/rollout/ROLLOUT-1.md and docs/rollout/AMENDMENT-1.md).
- Write: only inside ~/Downloads/fsc-rollout/drafts/case-new-1/<slug>/. The workbench copy ~/Downloads/fsc-rollout/tmp/case-2/wb/ is changed only by the check script below; never edit files there yourself, and never touch another case's files.
- Network: only read-only GETs (WebFetch) to confirm a competitor's OWN website or its county assessor record for the competitor census, when the research gives no such URL (a brand's store-locator page for that exact store counts as its own website). Record the date you confirmed it in the source entry. A 403, a bot check, a robots refusal or a dead page means that row gets no URL: drop the row or say in prose that the competitor is unconfirmed; never work around a closed door. No other fetching. Do not search the home folder, other folders or transcripts.
- Save page.html early and re-save after each section (a session limit can end you mid-work; a saved partial survives).

## What you produce (in your case folder)

1. `case.json`: the case-model input (format: ~/Downloads/wt-rollout-case-new-1/src/README.md, "Case input file").
2. `page.html`: the page source (format: same README, "Source file format"), type "case".
3. `card.txt`: one JSON string (with quotes) holding the card template for /case-studies/, in the style of ~/Downloads/wt-rollout-case-new-1/src/case-cards.json (model placeholders like {dscr_y2}, no citations, no market figures, must not contradict the determination).
4. `writer-notes.txt`: determination as proposed and as restructured (from the engine), body words, unique figures from pagecheck, lender conditions count, every NOT FOUND turned into a lender condition, every research figure you dropped or re-sourced and why, any engine limitation you hit.

## Study first (read, do not copy)

- ~/Downloads/wt-rollout-case-new-1/src/README.md (whole file).
- Exemplars, source and input: src/pages/case-studies/truck-stop-texas-sba.html with data/cases/truck-stop-texas-sba.json (SBA 504, a negative determination); gas-station-alabama-sba (SBA 7(a) acquisition under Appendix 15); meat-processing-texas-usda (USDA B&I); car-wash-texas-sba (504). See how the hero, glance, `{{case:...}}` tables and values, `sba:` markers, citations `[^n]`, competitor table with URLs, inputs with source or assumption, FAQ and sources are written.
- scripts/casemodel.py (how it sizes, tests and restructures; `python3 scripts/casemodel.py --case <slug>` in the workbench prints values once your files are in it).
- data/regulatory/sba.json (tiers, floors, caps, rates, fees).

## The hard constraint

Every figure traces to a dated source in your research file (or PA-USDA for USDA terms, sba.json for SBA rules), or to arithmetic casemodel.py performs. Nothing invented, nothing estimated past what its source says, nothing from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition, never a number. Model inputs with no source carry the label "assumption" and their reasoning (and may cite research figures in that reasoning).

## Subject rules (gate 8)

- The case is hypothetical. The town, county and corridor are named; the subject site is generic: no street number, parcel id, block and lot, owner, business name, listing id, broker, or the listed property's ask, per-acre price, exact acreage or exact building size.
- dnu.tsv in your folder lists the identifiers the research file carries for real candidate sites and businesses. None of those tokens may appear in page.html or case.json, not even in a source title or URL. If a source URL is a listing page of the subject, drop that source.
- Land is a round, labelled assumption ("about 3 acres", "$600,000, assumption: ..."), never a listing's ask; give the reasoning from other land evidence in the file if any.
- Real-address files (Audubon NJ, Branson MO): keep the town and corridor, use a generic site, use none of the real property's figures.
- Competitors named in the census with their own URL are fine; never make the subject a competitor wearing a new name.

## Page standard (rulings 3, 5, 7, 8, 9, 12, 16 of the rulebook; read them)

- Body words 4,500 to 6,500 (excludes tables, sources, FAQ, breadcrumb). Aim for about 5,200.
- House disclosure box under the H1 and byline (the template does it for type "case"; check the exemplar).
- Sections, in this order and with these ids: at-a-glance (`{{case:glance}}`), market-conclusion, demand, competitors (a table, one row per competitor, each row with an `<a href="https://...">` to that competitor's own website or the county assessor record), site (utilities, zoning, traffic counts where found, otherwise said to be lender conditions), revenue, opex, sources-uses, loan, pro-forma, dscr (the determination as proposed and as restructured), break-even, sensitivity (two drivers, five steps each), inputs (the model inputs table), risks, lender-conditions. FAQ and sources render from front matter. Table ids: `{{case:glance}}`, `inputs`, `revenue`, `opex`, `uses`, `sources`, `loan`, `proforma`, `dscr`, `determination`, `verdict`, `breakeven`, `sensitivity`, all present.
- Every number in a case table, and every model number in prose, renders from casemodel.py through `{{case:...}}`. Never type a model number by hand.
- Counted figures: at least 30 dated, sourced market figures with their own value that appear on no other served page, at least 20 of them from the research file. Aim for 38 or more, because sibling cases in this lane and other lanes' pages may share some at landing. Figures inside `case:`, `sba:` and `mkt:` regions do not count. National asset-class benchmarks are often shared with sibling cases: prefer local figures (town, county, corridor, competitors, local rents and prices, local traffic, local pipeline). Every block (p, li, table row) that states a figure carries a citation `[^n]`; a table can instead have a `<p class="table-source">` note directly under it that cites.
- Sources list: every entry has publisher, title, date and an absolute URL; every entry is cited somewhere; numbering is list order from 1.
- SBA: rules go through `sba:` markers with their current value inside (README lists paths). 13 CFR 120.160(b): SBA MAY require a feasibility study. Never write that SBA requires, mandates or triggers one. Equity tiers, DSCR floors, the debenture cap and rates come from sba.json through the engine.
- USDA B&I terms come from PA-USDA with its citations.
- Title and H1 follow WEB-FSC-6: title like "Truck Stop Feasibility Study, Jackson GA: SBA 504 Worked Case" (about 60 characters), H1 descriptive like the exemplar. Meta description 140 to 160 characters. The hero_sub (first screen) answers the query in two or three sentences with at least one counted figure.
- Dates: rebuilt pages keep `"published": "2026-07-13"` and `"updated": "DEPLOY"`; new pages carry `"DEPLOY"` for both. `"data_as_of": "2026-10"`.
- Every page is its own: write your own sentences from the research facts, never the research file's sentences (8-word shingle overlap is measured against every page on the site; stay far under 15%). Section headings may follow the exemplar pattern; prose, FAQ answers and the market argument must be specific to this town and asset.
- Banned: em dashes and en dashes in any encoding (use commas, colons, parentheses, "to" for ranges); this pattern, case-insensitive, anywhere: `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er` (brackets stop this brief matching itself); typed credentials next to the author name; Yelp or search-result pages as sources.
- A negative determination is a finding, not a failure (the Terrell and Granbury cases show it). Let the engine decide; write the page to its result.
- Links in prose: plain `<a href="/path/">`. Link the case's hub, state, metro (where given below) and practice area. Your brief lists the targets; a target that does not exist yet is a promised page and is fine (pagecheck will print "link to missing page" for it; ignore that line for the listed targets only).

## Self-check loop

After writing case.json and page.html, run:

    zsh ~/Downloads/fsc-rollout/../../../../wt-rollout-case-new-1/docs/rollout/case-new-1/tools/check.sh <slug>

It copies your two files into the workbench, builds the page, runs casemodel for your case, then pagecheck (body words, unique figures with --figures list, overlap top 5, case components), and checks your page against dnu.tsv. Fix and rerun until: build and casemodel clean, casemodel --check clean, pagecheck shows no PROBLEM except "link to missing page" for listed promised targets, unique figures 30 or more (aim 38), body words 4,500 to 6,500, gate 8 zero hits, zero dashes, zero banned names. If the script reports the lock is busy, wait and rerun.

If the engine cannot express something the case needs, do not fake it: write the nearest honest structure, and describe the needed engine change in writer-notes.txt (case, input shape, test).

## Reply

When done, reply with: the last pagecheck line and its PROBLEM lines, the casemodel determination (as proposed and as restructured), the gate 8 line, body words, unique figures, and anything the lane owner must decide. Under 300 words.

## Scratch files

If you write any helper script or scratch file, put it ONLY under ~/Downloads/fsc-rollout/tmp/case-2/scratch/<slug>/ (mkdir -p). Never use a shared scratchpad or a generic file name another agent might also use, and never run a script you did not write.

## CASE-NEW-1 overrides (these win over anything above)

- Check script: `zsh ~/Downloads/wt-rollout-case-new-1/docs/rollout/case-new-1/tools/check.sh <slug>` (your folder is ~/Downloads/fsc-rollout/drafts/case-new-1/<slug>/; create it). It copies your page.html, case.json and card.json into the shared worktree, builds, runs casemodel, `scripts/qa/pagecheck.py --stage ready`, sbamandate and your gate 8 list. Run it as often as you like; it costs no tokens.
- Replace card.txt with `card.json`: `{"slug": "<slug>", "card": "<template>", "category": "SBA 7(a) · State", "asset": "<Hub name>", "title": "<card title>"}` (see docs/rollout/int/REQUESTS.md, "Case cards"). The card has no market figures.
- Research: read your case's section in the MANIFEST (docs/rollout/case-new-1/MANIFEST.tsv column 3 is the old fact sheet, a map only; its counts predate the rulings). The research file is in ~/Downloads/FSC Deep Searches 2/ (ls and grep on the town). Your pre-count rows are docs/rollout/case-new-1/precount/<slug>.tsv: figures with counts=Y are your starting set; re-check the date basis of each against the research before you print it.
- Rulings that bind every figure you print, counted or not: I64/I66 (one property's size, units, acreage, price, loan or financing is not a market figure: cite it, inside `data-fsc-nocount`, never count it), I69/I77/I86/I106 (a figure is dated only if the research ties it to a publication, release, filing or effective date, an edition year in the document title, or the period of a periodic release; a date found only by a fetch, yours or the researcher's, does not date it, and an undated number is deleted or stated without the number), I71 (a value in another served page's sources list is on that page), A4 (figures held by a state, metro or hub page still count for the case; another case page that already carries a value takes it). Check the other case pages for a value you plan to count (grep -rl in case-studies/*/index.html).
- Buyer intent (owner, 28 Oct): the case page reads as the work of a firm the visitor can hire. Title and H1 name the asset class and "feasibility study", for example "[Asset] Feasibility Study Case: [Town, State], [Program]" (title about 60 characters). The opening paragraph says Feasibility Study Company prepares such studies for owners, developers and their lenders. A call to action (a plain link to /contact/ or the site's contact route as the exemplar pages do; check the base template) sits near the top and again after the determination. No fee, turnaround, guarantee or service promise unless a record states it. Do not promise a lender outcome.
- Acquisition (Broussard only): follow Appendix 15 (docs/rollout/ROLLOUT-1.md) for the acquisition label, the seller-history test and change-of-ownership rules, as the gas-station-alabama-sba exemplar does.
- SBA and USDA program tests (eligibility, transient revenue, DSCR floors, equity tiers, caps, the debenture) come only from `sba:` markers / data/regulatory/sba.json, or PA-USDA terms for USDA B&I (docs in ~/Downloads/fsc-rollout/drafts/case-1/PA-USDA-terms.md). Do not state a program rule from memory.
- Links: only link pages that exist or are in data/site/promised.json or chrome.json as pending; a pending link is not a live link. Never name or link the owner's other properties or any firm besides the competitors in your census.
- Do not use WebFetch for anything except the competitor-website confirmation described above. No Opus, no nested agents.
- Reply under 200 words: last pagecheck line, PROBLEM lines, determination, gate 8 line, body words, unique figures (research/register), and anything the lane owner must decide. Do not paste the page.

## Lessons from t1 (the READY gates found these; avoid them)
- Gate 7: every block (p, li, table row, FAQ answer) that prints a number carries a citation [^n] or sits under a table-source note. That includes percentages in sensitivity text, risks and FAQ answers. Where the number is a model/assumption value, say it in words ("one step", "a fifth") or use a {{case:...}} placeholder (not in FAQ answers).
- A rate printed with a unit like "per 10,000 residents" needs its citation in the same row.
- Gate 8 scans the repo history: real addresses, business names or listing ids never go in any file that is committed (page, case.json, card, notes). Notes files stay in your drafts folder.
- Competitor rows need an own-website or assessor URL you or the research confirmed; unconfirmed competitors are named in prose only.
- Do not cite a program rule (guaranty share, fee, term) from memory: it comes from sba.json via markers or PA-USDA.
- The floors are exact: 30 counted and 20 research. Aim for 36 or more counted so a review that deletes an undated figure does not sink the page. A named employer's announced investment, a single facility's size or acreage, are I64 single-property figures (cited, wrapped, not counted).
- Your scratch dir is ~/Downloads/fsc-rollout/tmp/case-new-1/scratch/<slug>/ (not case-2).
