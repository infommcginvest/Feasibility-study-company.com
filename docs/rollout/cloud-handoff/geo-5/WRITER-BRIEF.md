# GEO-5 writer brief (one new state page; its markets are sections of it)

You write ONE new state page source for feasibility-study-company.com. The state has no page today. The page does two jobs, in this order: (1) it reads as a firm the visitor can hire for a feasibility study in that state, and (2) below that, it is a reference page for lenders and sponsors built on dated public evidence. The site is in a financial (YMYL) niche weeks after Google's spam update: every page must carry its own evidence, its own argument and its own numbers, or it is a doorway page. A page that cannot reach its floor is reported, never padded.

## Read first (Read tool, in parts where long)
1. `~/Downloads/wt-rollout-geo-5/src/README.md`: the source format. Follow it exactly.
2. The model, for FORMAT and DEPTH only (never copy its sentences, plan or argument): `~/Downloads/wt-rollout-geo-5/src/pages/states/montana.html`, a new state whose seven markets are sections. Read its front matter, then skim the body section by section.
3. Your assignment `~/Downloads/fsc-rollout/drafts/geo-5/assign/<state>.json`: the countable fact ids, the markets and their section ids, the register keys you may use, the neighbours, the frames already taken.
4. Your fact sheet `~/Downloads/fsc-rollout/drafts/geo-5/facts/<state>.facts.json` and the research files `~/Downloads/fsc-rollout/drafts/geo-5/research/ST-<STATE>.md` and `MT-<STATE>.md`, for context and argument. Write from the facts, never from the research's sentences.
5. Integrator rulings on sameness and frames: `~/Downloads/wt-rollout-geo-5/docs/rollout/int/DECISIONS.md` entries I81, I84, I88 and I89, and `~/Downloads/fsc-rollout/drafts/geo-4/tools/SEO-BRIEF.md` (the "Frames already taken" list).

## Where to write
Write the keyed draft to `~/Downloads/fsc-rollout/drafts/geo-5/work/<state>.keyed.html` and its sources pool to `work/<state>.sources.json`, then assemble: `python3 ~/Downloads/fsc-rollout/drafts/geo-5/tools/assemble.py work/<state>.keyed.html work/<state>.sources.json pages/<state>.html`. Citations in the keyed draft are `[^key]` with keys you define in the pool (lowercase letters, digits, underscore); each pool entry is `{"publisher", "title", "date", "url"}` with the title verbatim from the research (I176). NEVER write inside any git worktree or repository. Never run git. Never spawn subagents.

## Buyer intent (owner's standing rule, 28 Oct 2026)
- Targets: "<State> feasibility study consultant", "<State> feasibility study company" and "<State> feasibility study". Use each naturally, once or twice in visible text; no stuffing (I89: three mentions of a keyword form at most in visible text).
- Title: "<State> Feasibility Study Consultants | Feasibility Study Company" (the house state pattern). H1: "<State> Feasibility Studies" or "<State> Feasibility Study Consultants".
- The description and `hero_sub` say that Feasibility Study Company prepares feasibility studies in <State> for owners, developers and their SBA, USDA and bank lenders, and carry at least one counted figure with its citation (hero) or one counted figure (description). The opening paragraph of the first body section says the same in its own words and then turns to the evidence.
- Calls to action: the template already puts "Request a methodology briefing" in the hero and a CTA band at the end (front matter `cta.h2`, `cta.p`). Add ONE more inside the body, at the end of the `metros` section after the last market card or at the end of the last market section: a short paragraph that tells the visitor what to send (the project, the site's county or market, the capital source) and links `<a class="btn" href="/#contact">Request a methodology briefing</a>`.
- What the firm may be said to do comes only from records: it prepares independent, lender-grade feasibility studies for SBA 7(a) and 504, USDA Rural Development, EB-5 and conventional financing; an inquiry is answered with the analytical framework, the deliverable the program requires, and next steps. NO fee, price, turnaround, delivery time, guarantee, approval rate, office, local staff, site visit, licence or credential claim: no record states one. Never say "local", "on the ground", "our team in <State>".

## Page standard (ruling 3; body words exclude tables, sources, FAQ, breadcrumb)
- 4,500 to 8,000 body words. Sections: economy and capital access; rules by asset class; costs and insurance; hazards; statewide supply; the 2025 to 2026 events a reviewer will ask about; `metros` (a heading that COUNTS the markets in words, one `metro-grid` card per market linking `#<slug>`, one sentence on what sets it apart, with NO figure); one section per market with `id` equal to its slug (the assignment gives them) written in the state page's voice; the program sections linking the practice areas (`/practice-areas/sba-7a-504/`, `/practice-areas/usda-rural-development/`, `/practice-areas/conventional-institutional/`, `/practice-areas/eb-5/`); `cases` ("Worked cases in <State>": the case library has none in the state; say so in your own words, not Montana's, Idaho's or Delaware's frame, and link `/case-studies/`); `assets` (the asset classes the page's rules touch, linking their hubs where a hub page exists in the tree).
- Order the sections by THIS state's own story (I74, I84): open on its own lead fact, not on a sentence about the study, not with another state's hero plan.
- Front matter: `type` "state"; `url` "/states/<slug>/"; `published` and `updated` both "DEPLOY"; `service.areaServed` `{"@type": "State", "name": "<State>"}` (the District of Columbia: `{"@type": "AdministrativeArea", "name": "District of Columbia"}`); `stats` three or four counted figures, each value six visible characters or fewer, each label with its citation; FAQ five to seven questions a lender or sponsor in THIS state would ask, each answered from this page's own figures with citations.

## Figures (rulings 4, 5, 9, 10; A4, A6; I55, I59, I60, I62, I64, I77, I86)
- F1. Use ONLY fact ids your assignment lists as countable, plus register markers. Copy each value exactly as the fact sheet gives it. Target at least 35 counted research figures; the floor at READY is 20 research and 30 in all, and landing is 15 and 25.
- F2. A fact the assignment lists as `context_only` (secondary, single-property, rule value) may be printed only inside `<span data-fsc-nocount>...</span>` with its citation, and only if it is dated. An undated number is never printed (I86).
- F3. No arithmetic of your own: no sums, differences, shares, growth rates, "more than twice", "the largest", "fits within" unless the source says it. Give both cited figures and let them stand.
- F4. NOT FOUND items become stated gaps ("a study has to source X from Y"), never numbers.
- F5. Register figures: at most 10 `mkt:` markers, each a different series and geography pair, in ONE table in the capital or economy section (format in `src/README.md` and the Montana source). Geos: the state code your assignment gives, or `co-<FIPS>` / `cbsa-<code>` keys it lists. Values: `~/Downloads/wt-rollout-geo-5/data/markets/series/<series>.json` under `values.<geo>`; never use a null or flagged value. Never show the register's Census population estimates where the page prints a Vintage 2025 population (one vintage per series per page). SBA FOIA series need `{"window": "fy2021_2025"}` or `"fy2016_2025"` on the `mktsrc` line.
- F6. SBA rules only through `sba:` markers (README). 13 CFR 120.160(b) says SBA "may require" a feasibility study; never write that SBA requires one.
- F7. A two-state market uses only this state's counties and says so.

## Prose
- P1. Write the argument from this state's facts: its demand base, weak spot, rules, hazard, lending channel. No paragraph that would fit another state with the names swapped. No 8-word run shared with any served page or with another GEO-5 draft in `~/Downloads/fsc-rollout/drafts/geo-5/pages/`.
- P2. No em or en dashes in any form (no `&mdash;`, `&ndash;`, U+2013, U+2014). Use `&amp;` for "&" in text.
- P3. Never write anything matching `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er` (case-insensitive), in any file.
- P4. Byline and credentials come from the template. Never type a credential.
- P5. Links: contextual links only to pages that exist in `~/Downloads/wt-rollout-geo-5` (check with `ls`), to your own sections, and to the neighbouring live state pages your assignment lists (name each neighbour where a fact makes the border matter; never for effect). No external links in the body.
- P6. American English, plain and exact. No hype, no rhetorical questions in body prose.

## Check your draft
`python3 ~/Downloads/fsc-rollout/drafts/geo-5/tools/draftcheck.py ~/Downloads/fsc-rollout/drafts/geo-5/pages/<state>.html --figures`
Fix every PROBLEM and rerun until clean. A figure reported as shared does not count: replace it with another assigned fact.

## Reply (short)
Draft path; body words; counted research figures; register markers; max overlap and against which page; any assigned fact you could not use and why; anything in the research that looked wrong or conflicting.

## Metro pages (a market that stood on its own pre-count)
- Your assignment is `assign/<state>/<metro>.json`; write `work/<state>/<metro>.keyed.html` and `work/<state>/<metro>.sources.json`, assemble to `pages/<state>/<metro>.html`.
- Model for FORMAT and DEPTH only: `~/Downloads/wt-rollout-geo-5/src/pages/states/texas/houston.html` (and one factory metro such as `src/pages/states/north-carolina/charlotte.html`). Never copy their sentences or plan.
- 2,000 to 3,500 body words. Cover: the economic base; growth; corridors (traffic counts only where your facts have them); supply by asset class; local rules; active lenders; eligibility (USDA rural, Opportunity Zone, HUBZone only where your facts hold them); "Worked cases" (none in this metro: say so in your own words and link `/case-studies/`); and what a lender should verify there (an `<ol class="failures">` list, as Houston's `#verify`).
- Front matter `type` "metro"; title "<Metro> Feasibility Study, <State> | Feasibility Study Company"; H1 "<Metro> Feasibility Studies"; `service.areaServed` `{"@type": "AdministrativeArea", "name": "<Metro>"}`; breadcrumb Home, Markets (`/states/`), <State> (`/states/<state>/`), <Metro>. The first screen names the counties the page covers (your assignment lists them) and says the page uses only those counties.
- Buyer intent as for the state, in the metro's terms: "<Metro> feasibility study consultant", "<Metro> feasibility study company", "<Metro> feasibility study"; the hero says Feasibility Study Company prepares feasibility studies in <Metro> for owners, developers and their SBA, USDA and bank lenders; one in-body CTA at the end of the supply or lenders section. Same limits: no fee, turnaround, office, local staff or credential claim.
- Links: the parent state page (`/states/<state>/`) at least twice in text, two or more folded sibling sections of the state page (`/states/<state>/#<slug>`, listed in your assignment), relevant hub pages that exist, a practice area.
- Figures: only your assignment's `facts` and its register pairs (the metro's own keys). The state page never repeats a figure you count, and you never use a state page fact.

## State pages with a standing metro
The state assignment lists `standing_metros`. Their card in `#metros` links the metro page (`/states/<state>/<metro>/`), not a section, and the state page links the metro page at least twice in text. Never print a figure the metro page counts; the state's own and folded-section facts are yours.
