# Track D freeze 1, Attacker 1 (figures, claims and the rule)

Reviewed: all 33 pages in `S/copies/d-f1` against `S/track-d/scratch-legacy/base`, the 10 edited sources against `/home/user/wt/bi/src/pages/asset-classes/`, the specs, the TSV, BRIEF.md, ROLLOUT-1 rulings 5, 8, 9, 12, 16 and DECISIONS I74, I89, I104, I115, I159. Worked separately from any other reviewer. Scratch scripts and outputs are in `S/track-d/a1-work/` (extract.py, figcheck.py, ctx.py, kw2.py, regions.py, pagecheck-f1.txt).

Counts: BLOCKER 1, MAJOR-FACTUAL 3, MAJOR-NONFACTUAL 1, MINOR 14.

## What held (reproduced, no finding)
- (a) Every new opening carries a figure that already prints in the stat band or body with the same value and the same source number, and each cited source entry is the publisher of that figure (32 changed openings checked figure by figure with figcheck.py and ctx.py; skilled nursing is unchanged). Period gaps are A1-12, A1-13 and A1-10 below.
- Ruling 16 counted figure: `pagecheck.py --figures` run on the frozen copy (its counts equal gate 3 for all 33 pages). The first-screen figure is a counted figure on 32 pages; the exception is A1-14.
- (b) No number in any changed element is new to its page (every digit string found in the base page; spelled quantities checked by hand).
- (d) No fee, price, turnaround, delivery time, guarantee, approval rate, office, local staff, site visit, licence, credential or lender-outcome promise in any title, H1, description, opening, CTA or button.
- (e) No "SBA requires" wording anywhere in the changed elements; the `sba:` markers are byte-identical base to freeze on all 33 pages; the only SBA statements (gas station Phase I, multifamily ineligibility, EV "no rule found") repeat the body with its citation.
- (f) Meta descriptions run 145 to 160 characters. Every page carries "<subject> Feasibility Study Company" in the title and "<subject> Feasibility Study Consultants" in the H1; the subject forms with "consultant(s)" and "company" appear at most twice in visible prose. Those "<subject> feasibility study" counts that run past three (7 to 11 on 22 legacy hubs) are pre-existing "By Market" link labels (I159 kind), with the opening adding one prose mention; no finding.
- (g) regions.py classifies every changed line on all 33 pages: only title, description, og and twitter mirrors, H1, hero-sub, hero buttons, CTA band, the JSON-LD mirrors of the sourced pages, and generated regions (author-ld, line-asset, mesh) changed. The ten sources change only title, description, h1, hero_sub, updated and the cta block. Skilled nursing changed only in its mesh.
- (h) Every href in every hero and CTA band resolves (`/#contact` exists on the home page; every `#sN`, `#monitor`, `#cases` and other anchor exists on its page; the five hub links exist).
- Gates: diffing GATES-d-base against GATES-d-f1 confirms that gate 3, 7 and 9 detail is identical. The gate 4 claim is only partly right (A1-19).
- No em or en dash and no ruling 9 pattern in any changed element.

## Findings

### A1-1 BLOCKER: uncited number on the first screen
- Page: /asset-classes/gas-station-and-c-store/interstate-highway/ (opening, `hero_sub`)
- Text: "the study shows where the subject sits against that, and what happens when a 120-position travel center opens one exit away."
- Reproduction: ctx.py on the body shows 120 only in the megasite table and FAQ, cited [5], [6] and [9] (Greenwood, Oak Creek, Rockingham County). In the opening the number carries no citation; the [1] [2] in that sentence belong to the Murphy USA figures. The base hero already had the clause, but the retrofit rewrote this sentence and the rule says a touched number keeps its citation.
- Fix (deletion): "what happens when a 120-position travel center opens one exit away" becomes "what happens when a megasite opens one exit away" ("megasite" is the body's own word).

### A1-2 MAJOR-FACTUAL: the opening says the study values the marina
- Page: /asset-classes/marina/ (opening)
- Text: "Each study values the marina as a going concern and tests slip and rack occupancy, the submerged-land lease and storm exposure."
- Reproduction: the body's FAQ says the market study and the feasibility study are not appraisals: "Neither is an appraisal, which is an independent going-concern opinion of value." The thesis says the firm prepares "the going-concern appraisal input". SBA routing requires an appraisal by a Certified General appraiser. So the opening claims a deliverable the page denies, and it implies a licensed valuation.
- Fix: "Each study values the marina" becomes "Each study treats the marina".

### A1-3 MAJOR-FACTUAL: the opening says the study values the park
- Page: /asset-classes/rv-park-and-campground/ (opening)
- Text: "each study then values the park as a going concern, sizes the ramp for a new or expanded park and tests coverage."
- Reproduction: the body says "We prepare the market study and the feasibility study, and support the going-concern appraisal", and leaves value to "Specialist appraisers". The study supports a valuation; it does not make one.
- Fix: "each study then values the park as a going concern" becomes "each study then reads the park as a going concern".

### A1-4 MAJOR-FACTUAL: the opening promises a valuation of the club
- Page: /asset-classes/fitness-and-recreation/ (opening)
- Text: "pairing a trade-area market study with a valuation of the club as a going concern rather than as a building."
- Reproduction: the body says "We prepare the market study, the feasibility study, and the going-concern appraisal input a fitness file needs". It also says that for a change of ownership "the lender will also require a going-concern business valuation and appraisal", which is a separate document.
- Fix: "with a valuation of the club as a going concern" becomes "with a read of the club as a going concern".

### A1-5 MAJOR-NONFACTUAL: keyword stuffed in the meta description
- Page: /asset-classes/laundromat/ (description and its og and twitter mirrors)
- Text: "Feasibility Study Company is a laundromat feasibility study company for owners, buyers and lenders, testing utility cost, turns per day and the lease first."
- Reproduction: the brand name is restated as the keyword in one clause ("X is a ... feasibility study company"). The rule asks for natural wording, never stuffed. The title already carries "Laundromat Feasibility Study Company".
- Fix (the description and both mirrors, 154 characters): "Feasibility Study Company prepares laundromat feasibility studies for owners, buyers and lenders, testing utility cost, turns per day and the lease first."

### A1-6 MINOR: the CTA offers "valuation work"
- Page: /asset-classes/pet-boarding-and-daycare/ (CTA paragraph)
- Text: "Feasibility Study Company will describe the demand, ramp and valuation work the study would include."
- Reproduction: the body gives the firm "the going-concern appraisal input". It says an acquisition needs "an independent business valuation ... as is a going-concern appraisal". Valuation is not part of the study.
- Fix (deletion): "the demand, ramp and valuation work" becomes "the demand and ramp work".

### A1-7 MINOR: the CTA frames the study as a valuation of the practice
- Page: /asset-classes/veterinary-practice/ (CTA heading and paragraph)
- Text: "What is the practice worth to a lender?" and "Feasibility Study Company will walk through how the study measures each".
- Reproduction: the body's thesis gives the firm "the going-concern appraisal input". The capital table puts the going-concern valuation with SBA 7(a) acquisitions as a separate deliverable.
- Fix: the heading becomes "What does a lender look for in a practice?" and "how the study measures each" becomes "how the study tests each".

### A1-8 MINOR: "sets out blue-sky value"
- Page: /asset-classes/auto-dealership/ (opening)
- Text: "Each one sets out blue-sky value, the floor-plan lien and service absorption in terms a credit committee can check."
- Reproduction: the body says "We prepare the market study, the feasibility study, and the appraisal input a dealership file needs". The blue-sky figures on the page are the Haig and Kerrigan multiples [3] [4]. The study reports them; it does not set a value.
- Fix: "sets out blue-sky value" becomes "sets out the blue-sky evidence".

### A1-9 MINOR: the "shook out" clause loses its citation
- Page: /asset-classes/fitness-and-recreation/ (opening)
- Text: "boutique studios grew into a $40.1 billion global market by 2024 and then shook out.[11]"
- Reproduction: the body sentence carries [11] [22]. Source [11] (Market.us) holds only the $40.1 billion; the shakeout (the Xponential brand cut and settlements) is in [22]. The value and period are correct.
- Fix: after the existing `<sup class="fn"><a href="#s11">11</a></sup>`, add ` <sup class="fn"><a href="#s22">22</a></sup>` as the body does. Or delete " and then shook out".

### A1-10 MINOR: unsupported lender claim and missing period
- Page: /asset-classes/truck-stop-and-travel-center/ (opening)
- Text: "Berkshire Hathaway's total cost to own Pilot came to roughly $13.6 billion,[9] and chains like it set the bar for every lender reading a travel center file,"
- Reproduction: the body supports "Chains dominate, and independents carry the competitive risk" and "A new Love's, Pilot, or TA within a few exits can devastate an independent". Nothing says chains set a lender standard. The $13.6 billion has no period on the first screen; the body and [9] give January 2024.
- Fix: "came to roughly $13.6 billion" becomes "came to roughly $13.6 billion in January 2024", and "set the bar for every lender reading a travel center file" becomes "are the competition every lender reading a travel center file weighs".

### A1-11 MINOR: a 2024 record is treated as the current rent level
- Page: /asset-classes/medical-office-and-asc/ (opening)
- Text: "triple-net asking rent set a record at $24.86 a square foot in 2024's second quarter,[7] and the study tests whether your tenants can carry rent at that level."
- Reproduction: the value, period and source [7] are correct. The same body sentence adds "reached $25.40 by the first quarter of 2026" [7] [8], so "that level" is a superseded benchmark.
- Fix: "carry rent at that level" becomes "carry market rent".

### A1-12 MINOR: the figure has no period
- Page: /asset-classes/assisted-living-and-memory-care/ (opening)
- Text: "Boston senior housing runs at 93.6 percent while parts of the Sun Belt are still absorbing legacy oversupply.[1]"
- Reproduction: the value and the [1] match the body, but the first screen gives no period. The body table header is "Occupancy (Q1 2026)", from the NIC MAP Q1 2026 release. Also, the source [1] entry lists the 89.5, 91 and 87.9 percent figures but not Boston. This is a pre-existing body citation and cannot be verified offline.
- Fix: "runs at 93.6 percent" becomes "ran at 93.6 percent in the first quarter of 2026".

### A1-13 MINOR: the figure has no period
- Page: /asset-classes/funeral-home/ (opening)
- Text: "The NFDA tally stands at 15,401 US funeral homes,[1]"
- Reproduction: the value and [1] are correct; source [1] is "data updated September 29, 2025", and the first screen gives no date.
- Fix: "The NFDA tally stands at" becomes "The NFDA tally, updated September 29, 2025, stands at".

### A1-14 MINOR (record): the first screen has no counted figure
- Page: /asset-classes/rv-park-and-campground/
- Text: "in a sector that earned $10.9 billion of US revenue in 2025.[4]"
- Reproduction: pagecheck-f1.txt gives "counted 0 (research 0)" for this page (gate 3 agrees). The same $10.9 billion prints on /case-studies/rv-park-arizona-usda/ and /case-studies/rv-park-pennsylvania-usda/, which outrank the hub. Ruling 16's counted figure cannot be met without a body change. The value, period and citation are correct.
- Fix: none in scope; list it with the legacy hubs' recorded gate 3 reds (INT I3 and I4).

### A1-15 MINOR: titles well over about 60 characters
- Pages: /asset-classes/behavioral-health/ (71), /asset-classes/quick-service-restaurant/burger/ (71), /asset-classes/rv-and-boat-storage/ (73), /asset-classes/veterinary-practice/ (73)
- Text: e.g. "Veterinary Practice Feasibility Study Company | Feasibility Study Company"
- Reproduction: measured on the rendered titles. The gas station hub, the interstate subtype and the QSR hub already drop the suffix to stay near 50.
- Fix (deletion; mirror og:title and twitter:title the same way): drop " | Feasibility Study Company". This gives "Behavioral Health Feasibility Study Company" (43), "Burger Restaurant Feasibility Study Company" (43), "RV and Boat Storage Feasibility Study Company" (45) and "Veterinary Practice Feasibility Study Company" (45).

### A1-16 MINOR: the keyword is set as an appositive in the description
- Page: /asset-classes/retail/ (description and its og and twitter mirrors)
- Text: "Feasibility Study Company, retail feasibility study consultants for owners, developers and lenders, tests tenancy, co-tenancy and lease-up before the loan."
- Reproduction: a plural keyword appositive sits between a singular subject and its verb, so the line reads as inserted.
- Fix (158 characters): "As retail feasibility study consultants, Feasibility Study Company tests tenancy, co-tenancy and lease-up before the loan, for owners, developers and lenders."

### A1-17 MINOR: openings longer than ruling 16's two or three sentences
- Pages: 27 of the 32 changed openings run 4 to 6 sentences: mixed-use 6; 5 on auto-dealership, behavioral-health, fitness, funeral-home, EV charging, glamping, grocery, hotel, marina, multifamily, private-school, QSR, self-storage and urgent-care; 4 on the rest. The base openings ran 2 or 3.
- Reproduction: sentence count of each rendered hero-sub, base against freeze (a1-work, inline script). Ruling 16: "The first screen answers the query in two or three sentences carrying at least one counted figure." The amendment's added moves (firm, deliverable, lenders, contact link) explain the growth.
- Fix: the integrator decides whether amendment 1 supersedes the sentence count. If it does not, merge the lender-list sentence into the firm sentence on each page (deletion-led).

### A1-18 MINOR (cross-lane, I89): the generic keyword repeats in the generated mesh
- Pages: behavioral-health, childcare-and-daycare, fitness-and-recreation, funeral-home, laundromat, medical-office-and-asc, pet-boarding-and-daycare, private-school, urgent-care and veterinary-practice.
- Text: the related-hubs mesh now prints "... Feasibility Study Consultants" 9 times (it takes each linked hub's new H1). With the page's own H1 that makes 10 visible instances of the generic phrase; the base showed 0.
- Reproduction: kw2.py, column Dmesh (f1 9, base 0).
- Fix: outside the five elements; the integrator's mesh label choice (for example a short hub name as the link text). Record it for Attacker 2's site-wide count.

### A1-19 MINOR (record accuracy): the coordinator's gate 4 claim
- Claim: "every changed page's gate 4 maximum fell".
- Reproduction: diffing GATES-d-base.txt against GATES-d-f1.txt shows unchanged maxima on 9 changed pages: behavioral-health 3.85%, gas-station-and-c-store 2.87%, ev-charging 0.45%, interstate-highway 0.45%, mixed-use 1.28%, private-school 1.7%, quick-service-restaurant 1.29%, rv-and-boat-storage 3.27% and self-storage 2.09%. None rose, and gate 4 stays GREEN.
- Fix: the record should read "no changed page's gate 4 maximum rose; 23 fell, 9 are unchanged".
