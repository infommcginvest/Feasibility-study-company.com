# Track D freeze 1, Attacker 2: sameness, frames, the legacy script, mirrors and dates

Reviewer: Attacker 2 (Opus), working alone. Scope: all 33 asset-class pages in `S/copies/d-f1` (30 hubs, 3 subtypes), against every served page in that copy (states, metros, cases, research notes, practice areas, the skilled nursing pilot header).

S = <scratchpad>. All scratch work is in `S/track-d/a2-work/` (scripts in `py/`, the proposed fixes in `fix/fixes.json`, the script run in `b/`, tests in `t1` to `t6`).

## Counts

| Severity | Count |
|---|---|
| BLOCKER | 0 |
| MAJOR-FACTUAL | 0 |
| MAJOR-NONFACTUAL | 12 |
| MINOR | 5 |

## What holds (reproduced, no finding)

- **Freeze record.** Every hash in `S/freeze/FREEZE-d-f1.txt` (10 sources, script, 22 legacy specs, 11 source specs, 33 rendered pages, 2 gate files) matches the files on disk (`sha256sum -c`, 0 failures).
- **Legacy script (c).** `cp -r S/track-d/scratch-legacy/base a2-work/b`, then `retrofit_legacy.py a2-work/b --date 2026-11-02` twice:
  - run 1: rc 0, "22 page(s) changed"; every "before" counted exactly once on every page (12 elements x 22 pages); the output of each page equals the base page with exactly the spec's 12 replacements plus the four date edits (line-asset `updated`, visible `Updated <time>`, author-ld `date_modified`, JSON-LD `dateModified`), checked byte for byte (`py/verify_script.py`: 22 of 22 match).
  - run 2: rc 0, "0 page(s) changed, 22 already applied"; the tree hash is identical before and after run 2 (idempotent).
  - `diff -rq base b`: exactly the 22 legacy `index.html` files differ; no other file is touched.
  - refusals, each with rc 1 and the tree hash unchanged: a half-applied page (title and H1 only, `t1`): "'before' counts title=0, h1=0"; a duplicated "before" (`t2`): "cta_text=2"; a page edited after apply (`t4`): "page changed since the spec"; bad dates `2026-13-40` and `11/02/2026` (`t3`).
  - dates: after `scripts/sitemap.py` in `b`, each of the 22 pages carries one date (2026-11-02) in the visible line, the JSON-LD dateModified, both region params and the sitemap lastmod; `byline.py --check` and `sitemap.py --check` exit 0; `sitemap.xml` differs from base only in 22 lastmod lines.
  - the frozen copy: each of the 22 frozen legacy pages equals my run (date normalized to 2026-10-29) everywhere outside the generated `mesh:` regions.
- **Dates in the frozen copy.** All 32 changed pages carry 2026-10-29 in the visible line, JSON-LD dateModified (both blocks on source pages) and sitemap lastmod; skilled nursing keeps 2026-10-28 everywhere. Gate 12 green in `GATES-d-f1.txt` agrees.
- **Mirrors (d).** On all 33 pages og:title and twitter:title equal the title, and og:description and twitter:description equal the meta description. On the 11 source pages the JSON-LD WebPage name and description equal the new title and description. The legacy pages carry no WebPage name or description and no headline. No old title or old description survives in any served file (`py/stale.py` over the whole copy; hits only in `docs/`).
- **`updated` (e).** The 10 changed source files set `"updated": "DEPLOY"` and keep `published`; skilled-nursing.html is untouched (byte-identical to the original, `updated` 2026-10-28). Front matter diff: only title, description, h1, hero_sub, cta.h2, cta.p (mixed-use: cta.h2 only) and updated change; every body is identical.
- **8-word runs.** Only one shared run of 8 or more words (digits dropped) between any new element and any other served page, A2-1 (`py/runs.py`, chrome and mesh regions excluded on the compared page).

## Findings

### A2-1 MAJOR-NONFACTUAL: 8-word run in the RV park description
- Page: /asset-classes/rv-park-and-campground/ (meta description, mirrored in og and twitter).
- Text: "Lenders ask how an RV park earns; Feasibility Study Company answers with campground feasibility studies for owners, developers and their lenders."
- Reproduction: `py/runs.py S/copies/d-f1 a2-work 8` returns one run, "feasibility studies for owners developers and their lenders", shared with /asset-classes/skilled-nursing/ (section heading "Skilled nursing feasibility studies for owners, developers and their lenders.") and with four case pages that carry "Feasibility Study Company prepares feasibility studies for owners, developers and their lenders" (grocery-store-ness-city-kansas-usda, medical-office-lebanon-tennessee-sba, restaurant-sevierville-tennessee-sba, self-storage-bardstown-kentucky-usda).
- Fix (description, og:description, twitter:description): replace "for owners, developers and their lenders." with "for park owners, developers and their lenders." (150 characters; deleting "their" instead would leave 139).

### A2-2 MAJOR-NONFACTUAL: the new H1s stuff "feasibility study consultants" into every mesh list (I89)
- Pages: 28 served pages now carry "feasibility study consultant(s)" more than three times in visible text; none did at the baseline. Ten hubs carry it 10 times (behavioral health, childcare, fitness, funeral home, laundromat, medical office, pet boarding, private school, urgent care, veterinary): the H1 plus 9 "Related" links. Also over the cap: auto dealership, auto service, car wash, coffee shop, gas station, glamping, grocery, hotel, marina, mixed-use, QSR, restaurant, retail, RV park, truck stop, and research notes franchise-vs-non-franchise (7), special-purpose-property-risk (5), coverage-constrained-takeout (4).
- Text, e.g. /asset-classes/laundromat/ "Related" list: "Behavioral Health Feasibility Study Consultants", "Childcare and Daycare Feasibility Study Consultants", ... "Veterinary Practice Feasibility Study Consultants" (9 items).
- Reproduction: `py/kw.py S/copies/d-f1 S/track-d/scratch-legacy/base` (main text, chrome excluded, mesh counted apart). `scripts/mesh.py` docstring: "Anchor text is always the target's H1", so every H1 change is copied into 85 other pages (71 cases, 14 research notes) and all 33 hubs (`diff -rq` base against d-f1). I159 excepts linked page names from the 8-word rule only, not from the three-mention cap.
- Fix (outside the five elements, for the integrator): in `scripts/mesh.py`, render a hub anchor as its class name, the way `state_name` already strips " Feasibility Studies" (for example map a trailing " Feasibility Study Consultants" to " Feasibility Studies"), or record a ruling that extends I159 to the I89 count. Without one of the two, the H1 form cannot stay on all 33 hubs.

### A2-3 MAJOR-NONFACTUAL: description frame "[claim]; Feasibility Study Company's <class> studies <verb> <back-reference>"
- Pairs (meta descriptions):
  - car wash / medical office: "Every car wash carries two values; Feasibility Study Company's car wash feasibility studies keep them apart ..." / "Unlike most real estate, a medical practice is valued on cash flow; Feasibility Study Company's medical office and ASC feasibility studies keep that line clear."
  - behavioral health / burger: "... and Feasibility Study Company's behavioral health feasibility studies start there, for operators and lenders." / "..., which is why Feasibility Study Company's burger studies start from the unit's own sales, for franchisees and lenders."
  - funeral home / multifamily: "...: Feasibility Study Company's funeral home feasibility studies test all three for owners and lenders." / "...: Feasibility Study Company's multifamily studies answer both for lenders."
  - The same possessive slot "Feasibility Study Company's <class> studies" sits in 13 of 33 descriptions (also auto service, gas station, interstate, marina, mixed-use, QSR, self-storage), and 24 of 33 close on the audience ("... and (their) lender(s)."), the closing-slot pattern I115 rewrote for Pennsylvania.
  - The medical office description (and auto service, A2-4) does not name who the firm serves, which the owner's rule requires.
- Reproduction: `py/extract.py` on d-f1 (descriptions listed in `a2-work/heads-new.txt`); a scan of every served description finds the possessive "Feasibility Study Company's" in these 13 and in /accessibility/ only.
- Fix (each in description, og:description and twitter:description on legacy pages; front matter on source pages; lengths checked):
  - medical office: replace the whole description with "Practice, surgery center or office building? Feasibility Study Company values each on its own basis in medical office and ASC studies for owners and lenders." (157)
  - burger: replace with "Item 19 averages hide a wide spread, so a Feasibility Study Company burger study swaps the brand average for the unit's own sales, for franchisees and lenders." (159)
  - multifamily: replace "Feasibility Study Company's multifamily studies answer both for lenders." with "lenders read both in a Feasibility Study Company multifamily study." (154)

### A2-4 MAJOR-NONFACTUAL: description frames "Whether ..., Feasibility Study Company's ..." and "Built from/around ..., Feasibility Study Company's ..."
- Pairs:
  - auto service / gas station: "Whether the bays do general repair, collision or quick lube, Feasibility Study Company's auto service feasibility studies tie the ramp to technician supply." / "Whether a site is branded, unbranded or a travel center, Feasibility Study Company's gas station and c-store studies test traffic, tanks and margin for lenders."
  - interstate / marina: "Built from ramp counts and a census of nearby stations, Feasibility Study Company's interstate gas station studies show owners and lenders where a site stands." / "Built around slips, dry stack and the submerged-land lease, Feasibility Study Company's marina feasibility studies serve owners, developers and lenders."
- Reproduction: as A2-3. The source writer's FRAMES-src entry for gas station logs this "concessive 'Whether A, B or C' lead" frame, and FRAMES-legacy logs it for auto service.
- Fix:
  - gas station: replace with "A branded, unbranded or travel center site is tested on traffic, tanks and margin in Feasibility Study Company's gas station and c-store studies for lenders." (157)
  - marina: replace with "Owners, developers and lenders turn to Feasibility Study Company for marina feasibility studies built on slips, dry stack and the submerged-land lease." (151)
  - auto service (audience missing): replace "Feasibility Study Company's auto service feasibility studies tie the ramp to technician supply." with "Feasibility Study Company ties an owner's or lender's auto service study to technician supply." (155)

### A2-5 MAJOR-NONFACTUAL: description frame "<class> feasibility studies from Feasibility Study Company, for <audience>, developers and lenders"
- Pages: glamping "... come first in glamping feasibility studies from Feasibility Study Company, for resort owners, developers and lenders." / grocery "...: grocery store feasibility studies from Feasibility Study Company for independent grocers, developers and lenders." / pet boarding "Dog daycare, boarding and grooming projects get feasibility studies from Feasibility Study Company, built for owners, developers and their lenders."
- Reproduction: `py/cross.py a2-work 5`: "feasibility studies from feasibility study" in all three; 7-word run "feasibility studies from feasibility study company for" glamping / grocery.
- Fix:
  - grocery: replace with "Not a square-footage guess but a margin test: that is how Feasibility Study Company runs grocery store feasibility studies for independent grocers and lenders." (159)
  - pet boarding: replace with "Weekday daycare and holiday boarding earn differently, and Feasibility Study Company models each in pet boarding studies for kennel owners and lenders." (151)

### A2-6 MAJOR-NONFACTUAL: description frame "[what decides credit]; Feasibility Study Company prepares the study for <audience> and lenders", and a shared pseudo-cleft
- Pages: urgent care "To finance an urgent care center or freestanding ED, start with payer mix: Feasibility Study Company prepares the feasibility study for owners and lenders." / truck stop "Diesel gallons, truck traffic and the store mix decide truck stop credit; Feasibility Study Company prepares the study for owners, developers and lenders." / veterinary "What a lender weighs in a veterinary practice is goodwill and DVM labor; Feasibility Study Company prepares feasibility studies for buyers, owners and lenders." (assisted living runs the same two-step: "... Feasibility Study Company writes assisted living and memory care feasibility studies for owners and lenders.")
- Veterinary and QSR also share a pseudo-cleft lead ("What a lender weighs ... is ..." / "... are what Feasibility Study Company's QSR consultants test ..."); both FRAMES logs call their own entry "pseudo-cleft".
- Reproduction: `py/runs.py ... 7`: "feasibility study company prepares feasibility studies for" (truck opening / veterinary description and the case-page house sentence); "feasibility study company prepares the feasibility study" (urgent care description / childcare opening).
- Fix:
  - truck stop: replace with "Diesel gallons, truck traffic and the store mix decide truck stop credit, which is why Feasibility Study Company forecasts them first for owners and lenders." (157)
  - veterinary: replace with "A veterinary practice sells on goodwill and DVM labor, the two things Feasibility Study Company tests first in feasibility studies for buyers and lenders." (154)

### A2-7 MAJOR-NONFACTUAL: one hero plan ends 18 openings, a two-noun imperative contact link
- Pages: 18 of 33 openings end on the /#contact link as a short imperative, 15 of them in one form, "<verb> [us] [about] the <A> and the/its <B>": assisted living "Describe the community and its capital stack to start", auto dealership "Start with the rooftop and the franchise", auto service "Tell us about the shop and its trade area", behavioral health "outline the facility and its payers", childcare "Share the site and the licensing plan", car wash "Bring us the site and the format", fitness "Tell us the format and the trade area", funeral home "Tell us about the firm or the site", glamping "Describe the land and the units", grocery "Send a note on the store and its market", marina "Begin with the harbor and the lease", RV park "Outline the park and its sites", truck stop "Name the corridor and the exit", urgent care "Tell us the trade area and the model", gas station "Get in touch with the address and the store format". EV charging, interstate and veterinary also close on the link.
- Closest pairs: fitness / urgent care ("Tell us the format and the trade area" / "Tell us the trade area and the model"); auto service / funeral home / veterinary / pet boarding ("Tell us about the ..."); assisted living / glamping ("Describe the ..."); RV park / behavioral health ("Outline the park and its sites" / "outline the facility and its payers"); car wash / mixed-use ("Bring us the site and the format" / "Bring the rent roll and the floor plans"); auto dealership / restaurant / coffee shop, and the pilot's CTA heading ("Start with the rooftop and the franchise" / "Start with the concept and the address" / "start with the concept and the corner" / "Start with the payer and the beds."); truck stop / interstate ("Name the corridor and the exit" / "point us to the exit to start"); assisted living / interstate ("... to start").
- Reproduction: link texts in `a2-work/new.json` (opening_html, from `py/extract.py`); FRAMES-legacy itself logs "contact link" as the last move on 15 legacy pages.
- Fix (exact, inside each opening; deletion first):
  - urgent care: replace "Feasibility Study Company prepares urgent care feasibility studies" with "<a href="/#contact">Feasibility Study Company</a> prepares urgent care feasibility studies", and replace "The deliverable suits SBA, USDA, conventional and specialty healthcare, net-lease and health-system lenders. <a href="/#contact">Tell us the trade area and the model</a>." with "It is written for SBA, USDA, conventional and specialty healthcare, net-lease and health-system lenders." (also ends the restaurant pair, A2-10)
  - glamping: replace "Will the resort still cover its debt in the off-season?" with "<a href="/#contact">How does the resort pay its lender in the off-season?</a>" and delete " <a href="/#contact">Describe the land and the units</a>." (also ends the fitness pair "Will the ...?", A2-8)
  - behavioral health: replace "USDA files: <a href="/#contact">outline the facility and its payers</a>." with "USDA files. <a href="/#contact">Which payers will the facility contract with?</a>"
  - car wash: replace "that keep those values apart," with "that <a href="/#contact">keep those values apart</a>," and delete " <a href="/#contact">Bring us the site and the format</a>."
  - funeral home: replace "<a href="/#contact">Tell us about the firm or the site</a>." with "<a href="/#contact">The firm's call history</a>, or a site plan, opens the file."
  - auto dealership: replace "<a href="/#contact">Start with the rooftop and the franchise</a>." with "<a href="/#contact">The rooftop and the franchise</a> frame the rest."
  - fitness: replace "<a href="/#contact">Tell us the format and the trade area</a>." with "<a href="/#contact">Format first, then trade area</a>."
  - by deletion inside the link text: assisted living "Describe the community and its capital stack</a> to start." to "Describe the community</a>."; childcare "Share the site and the licensing plan" to "Share the licensing plan"; grocery "Send a note on the store and its market" to "Send a note on the store"; RV park "Outline the park and its sites" to "Outline the park"; truck stop "Name the corridor and the exit" to "Name the corridor"; gas station "</a> with the address and the store format." to "</a> with the address."
  - veterinary and pet boarding: see A2-9; coffee shop: see A2-8.
  - After these, about ten openings still end on the link; the writers should move it off the last sentence on half of them in their next pass.

### A2-8 MAJOR-NONFACTUAL: shared first-sentence frames in openings
- Pairs:
  - auto service / funeral home: "General repair, collision, quick lube and tire shops share one constraint: ..." / "Funeral homes, crematories and cemeteries share one market and very different economics."
  - RV park / QSR, with hotel: "Debt-fund, CMBS, bank, USDA and SBA lenders put the same question to an RV park: how steady ...?" / "Franchisees, developers and their lenders can put one question to Feasibility Study Company about a quick-service restaurant: can this ...?" / "Owners and developers financing a hotel, and the banks behind them, can hand Feasibility Study Company the site, the flag and the program."
  - glamping / RV park: both open on an off-season question followed straight by "Feasibility Study Company prepares" (7-word run "the off-season? Feasibility Study Company prepares").
  - fitness / glamping: "Will the members stay?" / "Will the resort still cover its debt in the off-season?"
  - coffee shop opening / auto dealership CTA heading: "A coffee shop is an operating business before it is a building" / "A dealership loan is a floor-plan decision before it is a real-estate one."; coffee shop / restaurant also share "start with the concept and the" (A2-7).
- Reproduction: `py/runs.py ... 7` and `py/cross.py a2-work 5` (for example "the off season feasibility study company prepares", "start with the concept and the").
- Fix:
  - funeral home: replace "share one market and very different economics." with "serve the same families on very different economics."
  - RV park: replace "Debt-fund, CMBS, bank, USDA and SBA lenders put the same question to an RV park: how steady is the cash flow through the off-season?" with "Debt-fund, CMBS, bank, USDA and SBA lenders all size an RV park on how steady its cash flow stays between peak seasons."
  - QSR (source hero_sub): replace "Franchisees, developers and their lenders can put one question to Feasibility Study Company about a quick-service restaurant:" with "For franchisees, developers and their lenders, a quick-service restaurant comes down to one question:", and "The feasibility study answers it," with "Feasibility Study Company's feasibility study answers it,"
  - glamping: A2-7.
  - coffee shop: replace "A coffee shop is an operating business before it is a building, so <a href="/#contact">start with the concept and the corner</a>, not the lease." with "A coffee shop earns as an operating business, so <a href="/#contact">the concept and the corner</a> matter more than the lease."

### A2-9 MAJOR-NONFACTUAL: three openings copy the pilot's first move (firm prepares studies for owners, developers and lenders, on a market study of what is nearby)
- Pages: marina "Feasibility Study Company prepares marina, boat harbor and dry-stack feasibility studies for owners, developers and lenders, and each is built on a market study of the boats within reach of the water." / pet boarding "Feasibility Study Company prepares pet boarding and daycare feasibility studies for kennel owners, developers and their lenders, each resting on a market study of the households nearby." / veterinary "Feasibility Study Company prepares veterinary practice and animal hospital feasibility studies for veterinarians buying or building a practice, for developers, and for their lenders; its market study covers the pet households in reach." The pilot: "Feasibility Study Company prepares skilled nursing feasibility studies, with the market study inside, for owners, developers and their lenders: ...". The FRAMES-legacy plans for all three begin "firm + audience + market study".
- Reproduction: openings in `a2-work/heads-new.txt`; pilot header unchanged in d-f1.
- Fix (whole opening; moves only, no figure touched):
  - pet boarding, replace the opening with: <p class="hero-sub">Daycare brings recurring weekday revenue and boarding brings episodic holiday peaks, so a pet boarding and daycare feasibility study models both through the ramp to stabilized occupancy. Feasibility Study Company writes them for kennel owners, developers and their lenders, each resting on a market study of the households nearby. The scope covers kennels, doggy daycare, grooming and integrated pet resorts, a field IBISWorld counted at 169,481 businesses, up from 162,802 in 2024.<sup class="fn"><a href="#s1">1</a></sup> <a href="/#contact">Tell us about the facility</a>, and the study will be framed for a 7(a) or 504 loan, a USDA Business and Industry loan, or specialty, bank or bridge credit.</p>
  - veterinary, replace the opening with: <p class="hero-sub">A practice is a going concern whose value is mostly professional goodwill, so a veterinary feasibility study tests DVM staffing, production and the ramp. Feasibility Study Company prepares veterinary practice and animal hospital feasibility studies for <a href="/#contact">veterinarians buying or building a practice</a>, for developers, and for their lenders; the market study inside counts the pet-owning households a site can draw. The Census Bureau counted 34,296 veterinary practices in 2023,<sup class="fn"><a href="#s1">1</a></sup> and lenders weigh each new one, or each sale, under SBA 7(a) and 504, USDA rural, practice-finance and net-lease programs.</p> (also ends the veterinary closer of A2-7 and the frame of A2-10)
  - marina then stays the only hub opening in the pilot's form.

### A2-10 MAJOR-NONFACTUAL: shared argument sentences in openings
- Pairs:
  - urgent care / veterinary / grocery, "tests A, B and C before it <projects|sets|sizes> <coverage|debt>": "should test payer contracts, credentialing and the visit ramp before it projects coverage" / "the study tests DVM staffing, production and the ramp before it sets coverage" / "the study stress-tests sales, shrink and the wholesaler lien before it sizes debt".
  - urgent care / restaurant, "The deliverable suits <lender list>": "The deliverable suits SBA, USDA, conventional and specialty healthcare, net-lease and health-system lenders." / "The deliverable suits bank, equipment, bridge, SBA and USDA files alike."
- Reproduction: openings in `a2-work/heads-new.txt`.
- Fix: veterinary and urgent care as in A2-9 and A2-7; grocery: replace "the wholesaler lien before it sizes debt for" with "the wholesaler lien, then sizes debt for".

### A2-11 MAJOR-NONFACTUAL: one CTA move across the legacy CTA paragraphs
- Pages: 20 of 22 legacy CTA paragraphs (and the pilot's) are "Send / Share / Tell [us] <list ending in the lender or program>, and Feasibility Study Company will <outline | explain | describe | set out | lay out> the study". Shared wording:
  - auto dealership / car wash: "and the scope of the study follows" (7 words).
  - assisted living / glamping: "and the program you expect to use." (7 words, both closing the paragraph).
  - laundromat / childcare / auto service: "tests the study would run".
  - childcare / medical office / truck stop: "and we will set out the ..." / "and the lender, and we will lay out the study".
  - behavioral health / urgent care: "and the payers you expect".
- Reproduction: `py/runs.py ... 7` and `py/cross.py a2-work 5`.
- Fix (CTA paragraph):
  - car wash: replace ", and the scope of the study follows." with "."
  - glamping: replace "send the acreage, the unit plan and the program you expect to use." with "send the acreage and the unit plan."
  - childcare: replace "ramp tests the study would run." with "ramp tests."
  - auto service: replace "coverage tests the study would run, and name" with "coverage tests, and name"
  - medical office: replace "Send the specialty, the site and the lender, and we will set out the study that fits that structure." with "Send the specialty, the site and the lender."
  - urgent care: replace "the model and the payers you expect, and" with "the model and any signed payer contracts, and"

### A2-12 MAJOR-NONFACTUAL: shared CTA frames on the source pages
- Pairs:
  - hotel / multifamily / self-storage: the same tricolon kept from the old template, "the <X> at|near|competing with your site, the <Y> behind|for your <Z> and the <W> your <lender> <verb>": "the hotels competing with your site, the penetration path for your flag and the coverage your SBA, USDA, bank or CMBS lender will test" / "the lease-up pace at your site, the effective rents behind your unit mix and the permanent loan your construction lender relies on" / "the competitors and pipeline near your site, the street rates behind your lease-up and the coverage test your program applies".
  - gas station / private school: "the methodology briefing shows how" / "a methodology briefing shows how". Eight of ten source CTA paragraphs turn on "a methodology briefing <verb>".
- Reproduction: `cta_text` in `a2-work/heads-new.txt`; the baseline CTA paragraphs (`a2-work/base.json`) already shared the tricolon, and the retrofit kept it in a changed element.
- Fix (front matter cta.p):
  - self-storage: replace "near your site, the street rates behind your lease-up and the coverage test" with "near your site and the coverage test"
  - multifamily: replace "at your site, the effective rents behind your unit mix and the permanent loan your construction lender relies on. Feasibility Study Company builds the study around those three" with "at your site and the permanent loan your construction lender relies on. Feasibility Study Company builds the study around both"
  - gas station: replace ", and the methodology briefing shows how for your site, your format and your capital program." with "."

### A2-13 MINOR: CTA headings close on "loan" on nine pages
- Pages: behavioral health "No payer contract, no loan.", childcare "In childcare, enrollment is the loan.", coffee shop "Can one corner carry the loan?", truck stop "... decide a travel center loan.", hotel "... is what a hotel loan rests on.", multifamily "What repays the construction loan? ...", glamping "Let the off-season set the loan size.", gas station "... should not size the loan.", private school "The admissions funnel carries the loan." The closest pair is coffee shop / private school ("carry the loan" / "carries the loan").
- Reproduction: `cta_heading` in `a2-work/heads-new.txt`.
- Fix: private school, replace "The admissions funnel carries the loan." with "The admissions funnel repays it."

### A2-14 MINOR: button text cannot vary on source pages; legacy buttons share a form
- Pages: all 11 source pages (including the pilot) show "Request a methodology briefing" as the hero and CTA button. It is hard-coded in `src/templates/hub.html` and `subtype.html` (lines 9 and 28), so it cannot change inside the five elements, and it matches every state, metro and case page. On the legacy pages, 7 of 22 buttons take the form "<Verb> your <noun>": "Discuss your community", "Describe your shop", "Send your cafe concept", "Share your wash site", "Size your storage market", "Outline your campground", "Test your restaurant concept".
- Reproduction: `grep -n 'Request a methodology briefing' src/templates/*.html` in /home/user/wt/bi; `hero_buttons` in `a2-work/heads-new.txt`.
- Fix: list the template button for the owner (a front matter button field is a template change, outside this track). Legacy: none required.

### A2-15 MINOR: brand and keyword collide in two descriptions
- Pages: hotel "Every hotel feasibility study Feasibility Study Company writes starts from a named competitive set, ..."; laundromat "Feasibility Study Company is a laundromat feasibility study company for owners, buyers and lenders, testing ...". Both read as stuffing, against "keyword wording must read naturally".
- Reproduction: descriptions in d-f1.
- Fix:
  - hotel (front matter): replace "Every hotel feasibility study Feasibility Study Company writes starts from" with "Each hotel feasibility study by Feasibility Study Company starts from" (153).
  - laundromat (meta, og, twitter): replace with "Feasibility Study Company tests utility cost, turns per day and the lease first in laundromat feasibility studies for owners, buyers and lenders." (145). Optional: this is the only description that carries "<subject> feasibility study company", and the title keeps that form.

### A2-16 MINOR: JSON-LD Service name and description are left in the old wording (not mirrors)
- Pages: all 33. Service.name stays "<Class> Feasibility and Market Studies" or "<Class> Feasibility Studies", and Service.description stays "Independent, lender-grade ...". On EV charging, interstate and burger, Service.name equals the old H1 ("EV Charging and Alternative Fuel Feasibility Studies", "Interstate and Highway Fuel Station Feasibility Studies", "Burger Restaurant Feasibility Studies").
- Reproduction: `py/extract.py` ld field, compared with base titles, descriptions and H1s. None of them ever equaled the title or description, so they are not mirrors under the rule; the pilot leaves its Service block the same way.
- Fix: none required. If wanted, set the three subtype `service.name` values to the new H1.

### A2-17 MINOR: two gaps in retrofit_legacy.py argument handling
- (a) A bare trailing `--date` with no value is ignored, and the run silently dates all 22 pages with `src/site.json` deploy_date. In `t5`, `retrofit_legacy.py t5 --date` gave rc 0 and "dated 2026-10-29".
- (b) No guard against backdating. In `t6`, `--date 2020-01-01` was accepted and wrote "Updated January 1, 2020" on every page. The three dates still agree, so gate 12 passes.
- Fix (`main`): after the parsing loop, add `if "--date" in argv and date is None: raise SystemExit("retrofit_legacy: --date needs a value")`. In `plan`, refuse when `date` is earlier than the page's current line-asset `updated`.
