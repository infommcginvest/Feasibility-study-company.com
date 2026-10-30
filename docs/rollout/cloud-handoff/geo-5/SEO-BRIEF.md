# GEO-5 SEO finish brief (Fable; state and metro pages)

You finish the search-facing fields of the page sources a writer has drafted. You edit only those files, only the fields named here; you never touch the body sections, the sources list, or any other file. No git, no subagents, nothing written inside any repository or worktree.

## Read first
- Each draft (paths in your task) and its assignment (`~/Downloads/fsc-rollout/drafts/geo-5/assign/<state>.json` or `assign/<state>/<metro>.json`).
- `~/Downloads/fsc-rollout/drafts/geo-5/WRITER-BRIEF.md`, sections "Buyer intent" and "Metro pages": the owner's standing rule of 28 Oct 2026 and the limits on service claims.
- The house models (front matter only): `~/Downloads/wt-rollout-geo-5/src/pages/states/montana.html` (state) and `.../states/texas/houston.html` (metro).
- `~/Downloads/fsc-rollout/drafts/geo-4/tools/SEO-BRIEF.md`, the lists of frames already taken (titles, descriptions, heroes, FAQ questions) on landed pages. Add to them every frame used by the other GEO-5 drafts in `~/Downloads/fsc-rollout/drafts/geo-5/pages/`.

## Fields you own (front matter JSON)
- `title`: state "<State> Feasibility Study Consultants | Feasibility Study Company"; metro "<Metro> Feasibility Study, <State> | Feasibility Study Company". About 60 characters; the house pattern wins over length.
- `h1`: "<State> Feasibility Studies" or "<State> Feasibility Study Consultants"; metro "<Metro> Feasibility Studies".
- `description`: 140 to 160 characters (count them and report the count), plain text. It says Feasibility Study Company prepares feasibility studies in the place for owners, developers and their SBA, USDA and bank lenders, and carries exactly one counted figure from the page, written as the body writes it. No frame another landed page or GEO-5 draft uses.
- `hero_sub`: two or three sentences. The page's own lead fact with its citation `[^n]` exactly as the body has it, and the firm statement (who we prepare studies for), in an order no sibling uses. A metro names the counties it covers. Never a sentence about "a <place> feasibility study" as the subject with a dating verb (I81).
- `cta`: `h2` and `p` of the closing band: a reason to send the project now drawn from this page's own facts, no promise. The in-body CTA the writer placed stays as it is unless it carries a forbidden claim.
- `faq`: 5 to 7 questions people search about hiring a feasibility consultant or a market study in this place ("<place> feasibility study consultant", "market study <place>", "SBA feasibility study <asset> in <place>" where natural), at least one about engaging the firm (what to send, which programs: answered only from the records named in the writer brief). Each answer is specific to this place, cites figures `[^n]` already on the page, and repeats no other page's question frame or answer. No question about whether SBA requires a feasibility study.

## Hard limits
- Figures: only those already in the body with the same citation; never round or restate one. Three visible mentions at most of each keyword form (I89; the description does not count).
- No fee, price, turnaround, delivery time, guarantee, approval rate, office, local staff, site visit, licence or credential: no record states one. Never "local", "on the ground", "our team in".
- No em or en dashes in any form. Never write anything matching `m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er`.
- Titles and H1s unique across the site.

## Finish
Write each file back with Edit. Run `python3 ~/Downloads/fsc-rollout/drafts/geo-5/tools/draftcheck.py <path> --figures --promised` and fix every PROBLEM in your fields (a missing link to a sibling GEO-5 draft not yet in `pages/` is expected). Save a copy of each draft as it was before your edits to `~/Downloads/fsc-rollout/drafts/geo-5/work/<name>.before-seo.html` FIRST. Reply per page in four lines: title; description with its character count; hero_sub; FAQ questions.
