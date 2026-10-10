# Values edited as text (no data-file marker possible)

The regulatory render helper (`scripts/regulatory.py`) fills `<!--sba:PATH-->` regions in HTML text. It cannot reach JSON-LD strings, HTML attributes (meta descriptions, `content=`), or `<title>`. On the pages below the SOP name and date, and in a few cases a threshold, were edited as plain text and must be edited again at the next SOP release. Grep for `SOP 50 10 8.1` in `application/ld+json` blocks and `<meta` tags to find them.

| Area | Pages | What is hard-coded |
|---|---|---|
| SBA hub | practice-areas/sba-7a-504 | title, meta and og descriptions, Service and DefinedTermSet JSON-LD, FAQPage JSON-LD answers (floors, thresholds, fee waiver) |
| New note | research-notes/sop-50-10-8-1-what-changed-for-feasibility-studies | title, meta, Article JSON-LD description |
| Myth note | research-notes/sba-feasibility-myth | meta and og descriptions, Article JSON-LD description and "about" |
| Practice and framework | practice-areas/index.html, analytical-framework | ItemList, DefinedTerm and FAQ JSON-LD |
| Asset classes (28) | all asset-classes/*/index.html | FAQPage JSON-LD answers; some table cells and source-list sentences (see clusters/B.md and C.md section 3) |
| States (32) | all states/*/index.html | FAQ JSON-LD answers; the "$10 million (with the 7(a) approved first)" and FY2027 fee-waiver sentences |
| SBA cases (36) | case-studies/*-sba*/index.html | JSON-LD descriptions, "Structure per SBA 7(a) conventions" table-source lines, source lists |
| Research notes and homepage | see clusters/F.md section 3 | JSON-LD and source lines |

Everything rendered in visible HTML text on the hub, the new note and the stat blocks comes from `data/regulatory/sba.json` (gate 4).
