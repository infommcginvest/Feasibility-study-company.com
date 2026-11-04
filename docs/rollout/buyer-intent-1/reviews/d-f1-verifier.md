# Track D freeze 1, cold verifier (Sonnet)

S = <scratchpad>. My work folder is `S/track-d/v-work/` (nothing else was written but this file and `d-f1-verifier-fix.py`). The fix script holds `SRC_EDITS` (9 edits on 7 sources) and `SPEC_EDITS` (76 edits on 19 legacy specs); `python3 d-f1-verifier-fix.py <track-d dir> <out dir>` applies both to copies and checks that every `old` occurs exactly once.

## How I reproduced

- Pipeline replica: `cp -r track-d/scratch-legacy/base tree0`, place the 10 sources, run `retrofit_legacy.py --date 2026-10-29`, run `scripts/chain.py`. The result equals `copies/d-f1` file for file (only `docs/rollout/cloud-1/PLAN.md` and `.pyc` files differ). So any later tree built the same way is a true render, not an approximation.
- Frozen inputs: the 10 sources, the script and the 22 legacy specs match the hashes in `freeze/FREEZE-d-f1.txt` (33 of 33). Legacy pages: undoing every spec element on `d-f1` gives the baseline page outside mesh, line-asset and author-ld regions on all 22. Sources: front matter differs from the originals in title, description, h1, hero_sub, cta, updated only; bodies are identical on all 10.
- Text work: my own extractor (`lib.py`), the 8-word check (`runs.py`, `runs_check.py`: lower-case, digit tokens dropped, chrome and mesh regions excluded, own page excluded, against all 212 served pages of `d-f1` and of the fixed tree), pairwise shared-run lists across the 33 heads (`cross.py`).

## Counts

| | Confirmed | Refuted |
|---|---|---|
| Attacker 1 (19) | A1-1 to A1-10, A1-14, A1-18, A1-19 (13) | A1-11, A1-12, A1-13, A1-15, A1-16, A1-17 (6) |
| Attacker 2 (17) | A2-1 to A2-12, A2-15, A2-17 (14; A2-6, A2-8, A2-11, A2-12 in part) | A2-13, A2-14, A2-16 (3) |
| Verifier (new) | V-1 (8-word run), V-2 (residual pair, not fixed) | |

Merged: A1-5 = A2-15 (laundromat; A2-15 adds the hotel description), A1-18 = A2-2 (mesh). Severity after verification: BLOCKER 1 (A1-1); MAJOR-FACTUAL 4 (A1-2, A1-3, A1-4, A1-10); MAJOR-NONFACTUAL 14 (A1-5, mesh, A2-1, A2-3 to A2-12, V-1); MINOR 7 (A1-6, A1-7, A1-8, A1-9, A1-14, A1-19, A2-17).

## Coordinator claims (REVIEW-D.md)

- Gates 3, 7 and 9 detail identical between `GATES-d-f1.txt` and `GATES-d-base.txt`: CONFIRMED. I split both files at the `=== Gate` headers: gates 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12 are byte-identical; only gates 4, 13 (PENDING in base, GREEN in f1 because the base run used `--skip-look`) and the run-summary lines after gate 14 (green 11/14 against 12/14) differ. Gate 3 is red on the same 33 counts; gate 7 is red on the same 83 lines.
- Every changed page's gate 4 maximum lower: REFUTED. Of the 32 changed pages, 23 fell and 9 are equal (behavioral-health 3.85, gas-station-and-c-store 2.87, ev-charging 0.45, interstate-highway 0.45, mixed-use 1.28, private-school 1.70, quick-service-restaurant 1.29, rv-and-boat-storage 3.27, self-storage 2.09); none rose; skilled nursing (unchanged) is equal. Gate 4 stays green. The record should read "no changed page's gate 4 maximum rose; 23 fell, 9 are unchanged".
- Also true as stated: gates 3 and 7 are the red ones (12 of 14 green); the red detail is the legacy hubs' recorded reds.

## Attacker 1

### A1-1 CONFIRMED (BLOCKER by the rule's letter; carried over from the base)
Interstate opening: "a 120-position travel center opens one exit away" has no citation next to it; `ctx` shows 120 only in the megasite table and FAQ, cited [5], [6], [9]. The base hero printed the same clause uncited, but the retrofit rewrote this sentence and the rule is that a touched number keeps its citation. Fix: SRC_EDITS interstate-highway.html, "a megasite travel center" (the body's own word).

### A1-2 CONFIRMED (MAJOR-FACTUAL), A1-3 CONFIRMED (MAJOR-FACTUAL), A1-4 CONFIRMED (MAJOR-FACTUAL)
Marina "Each study values the marina", RV park "each study then values the park", fitness "a valuation of the club". Reproduced from each body's Study Types table: the appraisal answers "What is it worth?" and is a separate document; the feasibility study answers "Does this deal work?" / "Does it pencil for this lender?"; the thesis says the firm prepares "the going-concern appraisal input" (RV park: "support the going-concern appraisal"). The body does give the study a "going-concern income approach", so the repair keeps the going-concern framing and drops the valuation. Fixes: marina "treats the marina as a going concern"; RV park "reads the park as a going concern"; fitness "a model that treats the club as a going concern".

### A1-5 CONFIRMED (MAJOR-NONFACTUAL, with A2-15)
Laundromat: "Feasibility Study Company is a laundromat feasibility study company for owners..." restates the brand as the keyword in one clause; it is the only description carrying the "company" subject form, and the title already has it. Fix (meta and both mirrors, 152 characters): "Do the machines turn enough to cover rent? Feasibility Study Company checks that first in laundromat feasibility studies for owners, buyers and lenders." I did not use A1's "prepares ... studies" or A2's "tests ... first in" versions: each reproduces a frame that the restaurant description already has ("tests both in feasibility studies for owners, franchisees and lenders").

### A1-6 CONFIRMED (MINOR), A1-7 CONFIRMED (MINOR), A1-8 CONFIRMED (MINOR)
Same family as A1-2. Pet CTA "valuation work the study would include": the pet Study Types table gives the study "market study plus the ramp, staffing, a stabilized P&L, and DSCR" and the appraisal the value. Vet CTA heading "What is the practice worth to a lender?" is the appraisal's question verbatim ("What is it worth?"), and "how the study measures each" attaches goodwill to the study. Auto dealership "sets out blue-sky value": the table answers "What is it worth? A value opinion" for the appraisal and "Will it sell and cover its debt?" for the study. Fixes: pet "the demand and ramp work"; vet heading "What does a lender look for in a practice?" and "how the study tests each"; dealership "sets out the blue-sky evidence".

### A1-9 CONFIRMED (MINOR)
Fitness: `#s11` is Market.us and holds only the $40.1 billion; the shake-out is `#s22` (Xponential). The body sentence carries both, rendered as two adjacent `<sup class="fn">` markers. Fix: add the `#s22` marker after the existing one. The number keeps its citation either way.

### A1-10 CONFIRMED (MAJOR-FACTUAL for the claim; the missing period is MINOR)
Truck stop: "chains like it set the bar for every lender reading a travel center file". The body says "Chains dominate, and independents carry the competitive risk" and "the dominant competitive risk in independent underwriting"; nothing says chains set a lender standard. Source [9] and the body date the $13.6 billion to January 2024. Fix: "in January 2024" and "chains like it are the dominant competitive risk in underwriting an independent travel center, whether the lender is a bank, a CMBS or C-PACE lender, a bridge fund, an SBA 7(a) or 504 lender or the USDA Business and Industry program." ([9] kept; 2024 is on the page.)

### A1-11 REFUTED
Medical office "triple-net asking rent set a record at $24.86 a square foot in 2024's second quarter ... rent at that level": the value, period and [7] match the body sentence, and the opening dates the figure itself. Nothing is stated that is false; "that level" points back to the dated record. No fix.

### A1-12 REFUTED, A1-13 REFUTED
Assisted living "Boston ... 93.6 percent" and funeral "15,401 US funeral homes": value and source number match the body's own prose, which prints no period either (the period sits in the table header "Q1 2026" and in source [1] "data updated September 29, 2025"). The brief asks for the same value, period and citation, not that every opening spell the period out. The check that source [1] on the assisted living page does not list Boston is a pre-existing body citation and was not touched. No fix.

### A1-14 CONFIRMED (MINOR, record; no fix inside the five elements)
RV park gate 3 reads "counted 0 (research 0, register 0/0)" in both the base and f1 runs; `$10.9 billion` also prints on `/case-studies/rv-park-arizona-usda/` and `/case-studies/rv-park-pennsylvania-usda/`. The first-screen figure is correct (value, period, [4]); a counted one would need a body change. List with the legacy hubs' recorded gate 3 reds (INT I3, I4).

### A1-15 REFUTED
Titles of 71 to 73 characters (veterinary, RV and boat storage, burger, behavioral health) are the default form that the brief and HUB-RETROFIT-1 name ("<Class> Feasibility Study Company | Feasibility Study Company"; "about 60 characters where possible", "may vary"). The pilot title is 69. No gate or script measures title length (`grep` over `scripts/` and `scripts/qa/`). A trim is optional and would need title, og:title, twitter:title and the JSON-LD name on the four source or legacy pages.

### A1-16 REFUTED
Retail "Feasibility Study Company, retail feasibility study consultants for owners, developers and lenders, tests ...": a grammatical appositive carrying the keyword once, and the only description with this construction. No rule broken.

### A1-17 REFUTED (as a defect of this track; the counts reproduce)
Sentence count base against f1: base 2 or 3, f1 3 to 6; 27 of 32 changed openings run past three sentences. But word length is the pilot's: pilot opening 115 words in 3 sentences, f1 openings 82 to 157 words (median 110). The amendment requires firm, deliverable, lender fit, scope, a `/#contact` link and a counted figure in the opening; HUB-RETROFIT-1 states those rules and no sentence limit. Ruling 16's "two or three sentences" predates the amendment. For the owner or integrator to rule on, not a rewrite of 27 openings. (The A2-7 conversions below also delete 9 closing sentences.)

### A1-18 CONFIRMED (MAJOR-NONFACTUAL, cross-lane; see the integrator item)
Reproduced in the same count as A2-2.

### A1-19 CONFIRMED (MINOR, record accuracy)
Same as the coordinator claim above: 23 fell, 9 equal, 0 rose.

## Attacker 2

### A2-1 CONFIRMED (MAJOR-NONFACTUAL)
RV park description "feasibility studies for owners developers and their lenders" is an 8-word run shared with skilled-nursing and four case pages (my `runs.py` returns it). Fix (meta and mirrors, 150 characters): "campground feasibility studies for park owners, developers and their lenders."

### V-1 NEW, CONFIRMED (MAJOR-NONFACTUAL)
The same run check finds one more 8-word run that A2 reported as absent: assisted living description "assisted living and memory care feasibility studies for" shared with the CTA sentence of the four assisted living case pages ("Feasibility Study Company prepares independent assisted living and memory care feasibility studies for HUD Section 232 ..."). Fix (meta and mirrors, 156 characters): "writes memory care and assisted living feasibility studies for owners and lenders." After all fixes my run check returns 0 hits at 8 words.

### A2-2 CONFIRMED (MAJOR-NONFACTUAL, cross-lane; see the integrator item)
Reproduced: 28 served pages carry "feasibility study consultant(s)" more than three times in visible text on `d-f1`, 0 in the base. 25 are hubs (10 hubs at 10: behavioral health, childcare, fitness, funeral home, laundromat, medical office, pet boarding, private school, urgent care, veterinary) and 3 are research notes (franchise-vs-non-franchise 7, special-purpose-property-risk 5, coverage-constrained-takeout 4). `diff -rq` base against f1: 33 hubs, 71 cases and 14 notes change, because `mesh.py` prints each target's H1 as anchor text. Skilled nursing, unchanged, gains 2.

### A2-3 CONFIRMED (MAJOR-NONFACTUAL)
Reproduced: "Feasibility Study Company's" possessive subject sits in 13 of 33 descriptions and 24 of 33 end on "lender(s)". The three pairs share lead, slot and verb (car wash / medical office: "; FSC's ... feasibility studies keep ..."; funeral / multifamily: ": FSC's ... studies test all three / answer both for lenders"; behavioral / burger: "FSC's ... studies start ..., for X and lenders"), and the medical office description names nobody it serves, which the owner's rule requires (auto service the same). Fixes: medical office, multifamily (source) and burger (source) rewritten; mixed-use rewritten too, because it shares ", and Feasibility Study Company's ... studies [verb] ..." with behavioral health (`cross.py`: "and feasibility study company's" on both). A2's medical office text said the firm "values each" (the A1-2 defect), so I did not use it.

### A2-4 CONFIRMED (MAJOR-NONFACTUAL)
Auto service / gas station ("Whether ..., FSC's ... studies ...") and interstate / marina ("Built from / around ..., FSC's ... studies ... owners and lenders"). Fixes: auto service (also gains an audience) and marina rewritten; gas station and interstate stay.

### A2-5 CONFIRMED (MAJOR-NONFACTUAL)
Glamping, grocery and pet boarding all use "feasibility studies from Feasibility Study Company" (`cross.py` 5-word run, glamping / grocery 6 words with "for"). Fixes: grocery and pet boarding rewritten; glamping stays.

### A2-6 CONFIRMED IN PART (MAJOR-NONFACTUAL)
Truck stop, urgent care and veterinary share "[claim]; or: Feasibility Study Company prepares the (feasibility) study|studies for owners ... and lenders" (the 6-word run "feasibility study company prepares the feasibility" urgent care / childcare and "company prepares feasibility studies for" truck stop opening / veterinary description reproduce). The QSR / veterinary pseudo-cleft pairing is reversed in order (list then "are what" against "What ... is" then list): not a shared frame; refuted. Fixes: truck stop and veterinary descriptions rewritten; urgent care stays. A2's truck stop text "which is why Feasibility Study Company forecasts them first" would copy the burger frame ("which is why"), so I used "rests on ..., which Feasibility Study Company forecasts first".

### A2-7 CONFIRMED (MAJOR-NONFACTUAL)
Reproduced: 18 of 32 changed openings end on the `/#contact` link (position over 0.9 of the paragraph), 15 as "<verb> [us] [about] the A and the/its B". Repeated words: "Tell us" x5 (auto service, fitness, funeral, urgent care, vet), "Describe" x2, "Start with" with the restaurant and coffee openings and the pilot CTA, "Outline" x2. Fix: move the link onto a phrase in the firm sentence (study name, audience or the firm name, varying by page) and delete the closing sentence on 13 openings (auto dealership, auto service, behavioral health, childcare, car wash, fitness, funeral, glamping, interstate, marina, truck stop, urgent care, vet). After the fixes 3 openings still end on the link (EV, grocery, RV park) and 2 more carry text after it (assisted living, gas station), each with a different verb. A2's text for funeral ("The firm's call history, or a site plan, opens the file.") and the shortened link texts were not used: they read as inserted or leave the shape in place.

### A2-8 CONFIRMED IN PART (MAJOR-NONFACTUAL)
Reproduced: auto service / funeral ("... share one constraint" / "... share one market"); RV park / glamping (6-word run "off season feasibility study company prepares"); fitness / glamping ("Will the" openers); coffee shop opening / dealership CTA heading ("is a ... before it is a"); coffee shop / restaurant ("start with the concept and the"); RV park / QSR ("put the same question to" / "can put one question to"). The hotel part ("can hand ... Feasibility Study Company") shares only the modal and the firm name: refuted. Fixes: funeral, RV park, glamping and coffee shop openings. QSR keeps its sentence (the RV park rewrite removes the pair).

### A2-9 CONFIRMED (MAJOR-NONFACTUAL)
Marina, pet boarding and veterinary lead with "Feasibility Study Company prepares [class] feasibility studies for [audience] ..., [each] on a market study of the ...", like the pilot; marina and pet also share "on a market study of the" with urgent care. Fixes: marina keeps its sentences but puts the powerboat sentence first (reorder, nothing rewritten) and "begins with"; pet boarding opens on its daycare and boarding argument; veterinary opens on the goodwill argument.

### A2-10 CONFIRMED (MAJOR-NONFACTUAL)
Urgent care / veterinary / grocery "tests A, B and C before it projects|sets|sizes coverage|debt", and urgent care / restaurant "The deliverable suits". Fixes: grocery "the wholesaler lien, then sizes debt for"; veterinary opening rewritten (A2-9); urgent care "It is written for".

### A2-11 CONFIRMED IN PART (MAJOR-NONFACTUAL)
The shared wordings reproduce: "the scope of the study follows" (dealership / car wash), "the program you expect to use" (assisted living / glamping), "tests the study would run" (childcare, auto service, laundromat), "and we will set out the" (childcare / medical), "and the payers you expect" (behavioral / urgent care), "and the lender and we will" (medical / truck stop). The general claim that 20 of 22 paragraphs follow one move is not a rule breach on its own (a contact CTA asks for the file and says what comes back). Fixes: car wash, glamping, childcare, auto service, medical office, urgent care.

### A2-12 CONFIRMED IN PART (MAJOR-NONFACTUAL)
The tricolon "the X at|near|competing with your site, the Y ... your Z and the W your lender|program ..." sits in hotel, multifamily and self-storage CTAs; gas station and private school share "methodology briefing shows how". The wider claim that 8 of 10 source CTAs mention a briefing is the template button's wording ("Request a methodology briefing" is fixed in `src/templates`) and the base text: no shared run beyond those two words; refuted. Fixes: multifamily and self-storage lose the middle item; gas station loses the second briefing clause.

### A2-13 REFUTED
Nine CTA headings end in "loan" but in nine different constructions; the closest pair shares three words ("carry the loan" / "carries the loan"). No fix.

### A2-14 REFUTED
The source pages' button text is hard-coded in the templates (outside the five elements and this track); the legacy buttons differ from each other (the seven "<Verb> your <noun>" forms share only "your"). No fix; list the template button for the owner.

### A2-15 CONFIRMED (MINOR)
Laundromat as A1-5. Hotel "Every hotel feasibility study Feasibility Study Company writes starts from" runs two noun phrases together. Fix (front matter, 153 characters): "Each hotel feasibility study by Feasibility Study Company starts from a named competitive set, ...".

### A2-16 REFUTED
Reproduced as an observation (Service.name and Service.description keep the old wording; EV, interstate and burger Service.name equal the old H1), but those fields never mirrored the title or description, the rule names only the mirrors, and A2 itself asks for no fix. The mirrors that exist (og, twitter, JSON-LD WebPage name and description on the 11 source pages) all equal the new title and description in `d-f1` and in the fixed tree.

### A2-17 CONFIRMED (MINOR; outside the two lists)
`retrofit_legacy.py <tree> --date` (no value) exits 0 and dates the pages with `site.json` deploy_date; `--date 2020-01-01` is accepted on pages last updated 2026-10-10 and writes "January 1, 2020". Fix in `main` and `plan`: after parsing, `if "--date" in argv and date is None: raise SystemExit(...)`, and refuse a date earlier than the page's current line-asset `updated`. I changed nothing in the script.

## V-2 (new, not fixed)
Car wash and funeral home descriptions share the skeleton "[clause]; or: Feasibility Study Company's [class] feasibility studies [verb] ... for owners ..." that A2 flagged in each of its other pairs (car wash / medical office, funeral / multifamily); neither attacker paired these two. I did not rewrite either: any subject-verb replacement I tried reproduced another description's frame (restaurant "tests both in feasibility studies for owners ...", pet boarding, truck stop), and an untested text would not meet the fix test. Left for the integrator as a MINOR pair; the fix is one description (meta and both mirrors) moved off the possessive subject, rechecked for length and shared runs.

## Integrator item (mesh, A1-18 and A2-2)
Scripts and `data/mesh` are not touched in this track; the integrator-side fix is one sentence: in `scripts/mesh.py` render hub anchors as the class name (strip a trailing " Feasibility Study Consultants" from the target's H1 the way `state_name` strips " Feasibility Studies", or add a short-label field per hub) so generated lists stop printing the keyword phrase, or record a ruling that I89's three-mention cap excludes generated mesh regions.

## Fix test (applied to copies in `v-work/`, built with the chain, not a text comparison)

Built `tree3` = baseline + the 7 fixed sources + the fixed legacy specs through `retrofit_legacy.py --date 2026-10-29` and `scripts/chain.py` (every step rc 0; a second `retrofit_legacy.py` run reports "0 changed, 22 already applied"). 26 pages have at least one changed element against `d-f1`. Checked on the rendered pages:

1. No figure added, every number's citation kept. Every number in every changed element is on the baseline page; the only new numeral is "2024" in the truck stop opening (the date of the Pilot buyout, on the page). No citation moved or dropped (marina's powerboat figure keeps [2] when the sentence moves); fitness gains the [22] marker that the body carries. 
2. No shared run of 8 words: 0 hits for all 33 heads against the 211 other served pages of `d-f1` and against the fixed tree (before the fixes 2: RV park and assisted living descriptions). Own-page body: 0 new 8-word runs. At 7 words, 4 pre-existing shared runs remain (childcare opening / urgent care description "Feasibility Study Company prepares the feasibility study"; car wash / RV and boat storage openings "owners and developers and for their lenders"; grocery / RV and boat storage "their lenders with a market study that"; marina opening / skilled nursing description "feasibility studies for owners developers and lenders"): generic audience or firm wording, below the rule.
3. Meta 140 to 160 characters on all 33 (fixed ones 146 to 159); og and twitter titles and descriptions equal the meta on all 33; on the 4 changed source pages the JSON-LD WebPage name and description equal them too.
4. Keywords: every page keeps "<subject> Feasibility Study Company" in the title and "<subject> Feasibility Study Consultants" in the H1; across the five elements the subject-bearing forms peak at consultants 2, company 2, feasibility study|studies 3 (veterinary, at the cap, up from 1 because its opening and description now name the veterinary feasibility study; laundromat's description moved from the "company" form to "laundromat feasibility studies").
5. No em or en dash and nothing matching the ruling 9 pattern in any changed element, in the fix script, or in this file.

Gates on `tree3` (run without `--site-wide` and `--range`, so only those two summary lines differ): see the last section.

## Gates on the fixed tree (`v-work/gates-tree3.txt`, `--stage landing --skip-look`)

- Gates 1, 2, 4, 5, 6, 8, 9, 10, 11, 12 and 14 green; gate 13 pending (not run); gates 3 and 7 red exactly as in `GATES-d-f1.txt`: the gate 3, gate 7 and gate 9 detail lines are identical to f1 (the fixes add no counted figure, no uncited figure, no link). That is 11 of 14 green because the look gate was skipped, against 12 of 14 in f1.
- Gate 4: no fixed page rises above its baseline maximum; against f1, six pages rise by 0.01 point from re-rounding (auto-dealership 2.38 to 2.39, coffee-shop 4.11 to 4.12, fitness-and-recreation 4.53 to 4.54, grocery-store 4.01 to 4.02, retail 4.53 to 4.54, rv-park-and-campground 2.71 to 2.72); the overall maximum is 4.54 against the 15 percent limit.
- Gate 12 green: the script dates, the JSON-LD and the sitemap agree after the fixes.
