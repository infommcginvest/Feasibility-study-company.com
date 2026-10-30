# GEO-5 pre-count brief (Sonnet reader, one state)

ROLLOUT-1 ruling 6 and amendment A6: before a page is written, a reader counts the dated, sourced, page-specific figures the research and the register hold for it. You do that for ONE new state and each of its markets, and you decide which markets could stand as their own metro page. You write two files and nothing else.

## Inputs (read only)
- Rules: `~/Downloads/wt-rollout-geo-5/docs/rollout/ROLLOUT-1.md` rulings 4 to 6, `AMENDMENT-1.md` A4 and A6; integrator rulings in `~/Downloads/wt-rollout-geo-5/docs/rollout/int/DECISIONS.md`: I55, I59, I60, I62, I64, I66, I69, I71, I77, I82, I86, I87, I91, I109, I131, I142, I154, I176 (search for `**I<n>.`), and the precedent reading of a new state with folded markets: I183 and `~/Downloads/fsc-rollout/drafts/geo-4/facts/montana-PRECOUNT.md` (its method and sensitivity tables; do not copy its numbers).
- The research: `~/Downloads/fsc-rollout/drafts/geo-5/research/ST-<STATE>.md` and `MT-<STATE>.md`.
- The mechanical fact sheet: `~/Downloads/fsc-rollout/drafts/geo-5/facts/<slug>.facts.json` (from `tools/yield5.py`). Each fact carries `dated`, `figure`, `market`, `taken` (served pages that already print its first figure, body or sources list, by the integrator's pagecheck value and rounding rules), `shared_geo5` (another new state's research holds it) and `countable`. Trust `taken` and `shared_geo5`; YOU judge everything else row by row.
- The register: `~/Downloads/wt-rollout-geo-5/data/markets/series/<series>.json` `values.<geo>` (state code; `co-<FIPS>`; `cbsa-<code>`, codes in `data/markets/geographies.json`). Up to 10 register figures per page, each a different series and geography pair, no null or flagged value, never PEP population where the page has a Vintage 2025 population.

## What you decide for every row
1. **Dated (I77)?** (a) a publication, release, filing or effective date in the Published cell; (b) an edition year in the title; (c) the reporting period of a periodic document (a monthly or quarterly release, an annual statistical release) that the period identifies. Mark which. A row whose Published cell says "periodic (no date printed)" or similar and whose URL is an API or a live data page (FRED, BLS data tool, OpenFEMA, FDIC API) is BORDERLINE: count it in the main reading only when the publisher's series is a recognised periodic release (BLS CES/LAUS/QCEW, BEA, FHFA HPI, Census building permits), and list it in a borderline column. A period printed on an undated non-periodic page does not date a row. A retrieval date never dates a row.
2. **Countable?** Not countable: rule values (statutory rates, fees, thresholds), code or bill numbers, single-property values (one building, site, project, firm: I64, I66; a portfolio or market total still counts), research arithmetic (I55), counts of a list the page would name in full (I91), and any row whose `taken` or `shared_geo5` is non-empty. A value counts once per page (rounded or rescaled repeats of the same series, period and publisher are the same fact, I82).
3. **Secondary rows** (news relays, FRED relays, aggregators): count them in the main reading when the row names the original publisher and a date; list them so the sensitivity can remove them.
4. **Where it belongs.** MT rows belong to their market section; ST rows to the state. A metro-wide figure that equals a state figure goes to the metro (ruling 4).

## Markets: page or section
For each market: free research figures (main reading), and the register figures available for its geography (count the pairs, at most 10). A market stands as its own metro page only if it has **at least 21 free research figures** (the GEO-1 D7 margin over A6's 20) AND research plus at most 10 register reach 30, AND it still holds 20 research once secondary and borderline rows are removed one family at a time (the Oahu rule, I180: a page that rests on secondary rows for half its count folds). Otherwise it folds into the state page as a section with its slug as id. Propose each market's slug (lowercase, hyphenated, the market's common name, as `src/pages/states/*/` already does).

Then the state page: its own rows plus every folded market's free rows. A new state ships only with 20 research and 30 in all at READY (R9); report the state's count with all markets folded, and again with any standing metro taken out.

## Spot check (do it)
Open (WebFetch) the URL of 12 countable rows chosen across topics and markets, weighted to secondary and borderline rows, and confirm the page prints that value for that period. Record each result (confirmed / not on page / door closed). Never work around a closed door (403, 429, robots, bot check, paywall, login): record it. Never fetch www2.census.gov. If a row's value is not on its page, mark it not countable and say so.

## Output (write exactly these two files)
- `~/Downloads/fsc-rollout/drafts/geo-5/facts/<slug>-PRECOUNT.md`: method (5 lines); a verdict table (page | facts | countable | free research main reading (a/b/c) | register | total at READY | verdict); per-market sensitivity (without secondary; without borderline; without both); the state's harshest stack; the spot-check table; flags for the writer (conflicts inside the research, rows that look wrong, titles changed from the source, e.g. dashes replaced).
- `~/Downloads/fsc-rollout/drafts/geo-5/facts/<slug>.precount.json`: `{"state": ..., "markets": [{"slug", "name", "section": "<MT heading as in the file>", "counties": [...], "verdict": "page"|"section", "free_ids": [...]}], "state_free_ids": [...], "register_pairs": [{"geo", "series", "value"}], "borderline_ids": [...], "secondary_ids": [...], "dropped": [{"id", "why"}]}`. Ids exactly as the fact sheet writes them (`ST-<STATE> line <n>`).

## Rules
- Write only those two files. No git, no subagents, nothing inside any repository or worktree.
- No em or en dashes. Never write anything matching `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er`.
- Every command carries a time limit: `~/Downloads/fsc-rollout/drafts/geo-5/tools/to <seconds> <cmd>`.

## Reply (under 200 words)
The verdict table rows, the state's count (main reading and harshest stack), spot-check tally, and anything blocking.
