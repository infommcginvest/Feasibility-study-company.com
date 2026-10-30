# GEO-5 t3 freeze 1, attacker two (gates, links, sameness, buyer intent, claims)

Page: /states/south-dakota/ (no metro page). Source `src/pages/states/south-dakota.html` in the frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/t3/` (sha256 68eb5362..., equal to `drafts/geo-5/pages/south-dakota.html` and to FREEZE-t3-f1.txt; rendered page 56012101..., equal to the record). Line numbers below are the source's.

Comparison set: the nine other GEO-5 drafts in `drafts/geo-5/pages/` (Alaska, Colorado, Denver, District of Columbia, North Dakota, Vermont, Virginia, Northern Virginia, Wyoming), every landed source under `~/Downloads/wt-rollout-geo-5/src/pages/`, and the taken-frames list in `drafts/geo-4/tools/SEO-BRIEF.md`.

## What I ran

- `tools/sameness.py --ours pages/south-dakota.html --against <the nine drafts> ~/Downloads/wt-rollout-geo-5/src`: max 0.67% (Denver). After removing `sba:` marker text, register row labels and asset-class hub names, no shared 8-word prose run remains with any page.
- A second pass of my own (scratchpad `norm.py`) with place names replaced by one token and digits dropped (I115's reading), to catch frames that differ only by the state's name. Its hits are in A2-8 to A2-13.
- `tools/frames.py` over all ten GEO-5 sources; landed descriptions and CTA h2s scanned for the same openers.
- Gates rerun from inside the copy: `gates.py --root . --git-dir ~/Downloads/wt-rollout-geo-5 --urls /states/south-dakota/ --new /states/south-dakota/ --stage ready --only 3,4,7,9 --skip-look` gave GREEN 5/5, the same as GATES-t3-f0.txt: counted 107 (research 98, register 9/9), overlap max 0.51% against /states/tennessee/nashville/, SBA mandate sentences 0, figure blocks without a citation 0, required edges all present. The gate outputs agree with the copy.
- `scripts/qa/sbamandate.py` `flagged()` on the rendered page: []. I also listed every sentence that has a compulsion word and "stud" without the guard's other conditions (A2-6).
- I scanned the rendered visible text for fee, price, turnaround, weeks, guarantee, approval, office, staff, local, on the ground, our team, licence, certified, credential and site visit. No service claim of any of these kinds is made. The hits are data ("state and local taxes", "office building", "impact fee schedule", "price index") or method ("a study here buys the hotel or storage data").
- Keyword counts in visible text (I89). "South Dakota feasibility study consultant": 2 (hero, #capital), plus the title, which is not page text. "South Dakota feasibility study company": 1 (#capital). The bare form "South Dakota feasibility study": 3, all inside those two longer forms. H1 "South Dakota Feasibility Studies". All within the cap.
- Links in the rendered page. /states/minnesota/ and /states/iowa/ each appear once in prose (#metros, #rules) and once in the generated neighbour block. /states/nebraska/ and /states/montana/ appear only in the generated neighbour block and the mega menu. North Dakota and Wyoming have 0 mentions and 0 links. Four pages link in: Iowa, Minnesota, Montana and Nebraska.
- WebFetch: ESMIS Crop Production publication page; the Department of Tourism release; the LMIC Rapid City MSA and Sioux Falls MSA QCEW tables. The NASS PDF came back as binary and no local PDF tool exists, so I did not use it.

## Findings

### A2-1 MAJOR-FACTUAL: the closing band and FAQ 2 say the October forecast stands until NASS's annual summary
- Page: front matter `cta.h2` (line 93), `cta.p` (line 94), FAQ 2 answer (line 68).
- Text: "The October 9, 2026 crop forecast stands until NASS's annual summary replaces it, and the sales tax reduction sunsets on June 30, 2027 unless the Legislature acts." / "A study dated between those two events cites the forecast as it stands and states the sales tax rate its first full year assumes." / FAQ 2: "Once NASS publishes its annual summary, that replaces the October forecast in the study."
- Reproduction: the ESMIS Crop Production page (https://esmis.nal.usda.gov/publication/crop-production) lists two upcoming releases, "Nov 10 2026 12:00 PM" and "Dec 10 2026 12:00 PM", after the latest one of Oct 09 2026. The October forecast is replaced on November 10, 2026, 13 days after today, not by the January annual summary. So a study dated in late November or December would not "cite the forecast as it stands". No research row (ST, ST-2 or MT) states what replaces the October release; grep for "annual summary" and "November" in the three files returns nothing relevant. The claim is uncited, and the band cannot carry a citation (I181). The body's own sentence at line 612 ("The October figure is a forecast, and NASS revises it; a study dated after January cites the annual summary that replaces it.") is true as written and stays.
- Smallest fix (deletions):
  - `cta.h2`: delete "The October 9, 2026 crop forecast stands until NASS's annual summary replaces it, and " and capitalise "the" to "The". It reads: "The sales tax reduction sunsets on June 30, 2027 unless the Legislature acts."
  - `cta.p`: delete "A study dated between those two events cites the forecast as it stands and states the sales tax rate its first full year assumes. "
  - FAQ 2: delete " Once NASS publishes its annual summary, that replaces the October forecast in the study."
  - After these deletions the band names one date. If the integrator wants to keep two dates, the second date needs a research row first (for example, the ESMIS schedule). That is not my edit.
- The rest of the band checks out. It carries no figure, only dates, and no citation. The sunset date is ST-SOUTH-DAKOTA line 87 (DOR, April 3, 2023), whose note reads "Rate returns to 4.5% after the sunset unless the Legislature acts; no 2026 action confirmed on an opened page". The band drops the body's hedge (line 653, "no 2026 action on the sunset was confirmed on an opened page") and states the sunset as settled on a 2023 source. I record that as part of this finding, not as a separate one.

### A2-2 MAJOR-FACTUAL: the tourism tax share is said to come from people who do not live in the state
- Page: #brief, line 590.
- Text: "A state that collects that share of its sales tax from people who do not live in it is a state where hotels, campgrounds, restaurants and fuel stops are underwritten against a calendar"
- Reproduction: WebFetch of the cited release (sdvisit.com, January 21, 2026) gives "14.97 million visitors traveled to and within South Dakota in 2025". It also gives "representing 16.5% of all state sales tax collections". The release counts travel within the state, which includes residents, and never says the 16.5% comes from non-residents. ST-SOUTH-DAKOTA lines 50 and 55 say the same: "Visitors to and within South Dakota", "Tourism share of total state sales tax collections". The page's own stats tile (line 47) also says "Visitors to and within South Dakota".
- Smallest fix: delete " from people who do not live in it".

### A2-3 MAJOR-FACTUAL: the Rapid City metro area is said to be Pennington, Meade and Lawrence counties "as the Labor Market Information Center draws it"
- Page: #rapid-city, line 757.
- Text: "The Black Hills market here is Pennington, Meade and Lawrence counties, the Rapid City metro area as the Labor Market Information Center draws it, all inside South Dakota."
- Reproduction: WebFetch of https://dlr.sd.gov/lmic/qcew2025_9_rcmsa_est_work_pay.aspx (source 63) shows the table title "Rapid City MSA Covered Workers and Pay 2025" with no county list, and a total of 74,312 workers. Compare the Sioux Falls MSA page, which does name its counties. The research row (ST-2 line 124) says only "In-state MSA". The research's own county rows contradict the claim. Lawrence County is 13,694 workers and Pennington alone is 62,445 (ST-2 line 126, same LMIC report), so an MSA total of 74,312 cannot contain all three counties. I give that comparison only as reproduction; the page must not print it. Lawrence County is the Spearfish micropolitan area, not part of the Rapid City MSA. The clause is uncited and contradicted. It also carries over to the metro-wide figures printed after it (74,312 and $59,377, FHFA, BEA), which a reader would take to cover Lawrence County.
- Smallest fix: delete ", the Rapid City metro area as the Labor Market Information Center draws it". The sentence becomes: "The Black Hills market here is Pennington, Meade and Lawrence counties, all inside South Dakota."

### A2-4 MAJOR-FACTUAL: the SBA 504 equity rule is misstated
- Page: #capital, line 801.
- Text: "and a 504 borrower that is a start-up, or that builds a single-use property such as a hotel or a campground, contributes <!--sba:equity.sba_504_new_or_special.value-->15%<!--/sba:...--> equity [^81]"
- Reproduction: `data/regulatory/sba.json` in the copy gives `equity.sba_504_new_or_special` = 15% ("New Business (two years or less) or Limited or Special Purpose Property") and `equity.sba_504_new_and_special` = 20%. The page's "or" sentence assigns 15% to a start-up that builds a hotel, the commonest South Dakota case on this page, and that borrower is at 20%. The register calls it "Limited or Special Purpose Property", not "single-use". The rule covers acquisitions as well as builds, so "that builds" narrows it wrongly. SBA's example list (`valuation.special_purpose_list`, 25 items) names "Hotels, motels, and other lodging facilities" but not campgrounds. Calling a campground SBA's example is therefore the page's own extension, with no source.
- Smallest fix: delete ", and a 504 borrower that is a start-up, or that builds a single-use property such as a hotel or a campground, contributes <!--sba:equity.sba_504_new_or_special.value-->15%<!--/sba:equity.sba_504_new_or_special.value--> equity". Keep " [^81]" after "1.15x standard coverage". The next sentence ("For a seasonal South Dakota business that coverage test ...") still has its antecedent. `sba:` values are outside the count (pagecheck line 21), so the count is unchanged.

### A2-5 MAJOR-FACTUAL: Fall River County is called Pennington County's neighbour
- Page: #rapid-city, line 767.
- Text: "Straight-line winds in December 2025 brought DR-4903-SD for Pennington County, and its neighbors Custer and Fall River [^38]."
- Reproduction: ST line 120 (DR-4903-SD) lists "Custer, Fall River and Pennington counties" and says nothing about adjacency. Fall River County lies south of Custer County and does not border Pennington County. The adjacency claim is the page's own, and it is wrong. The #hazards line 675 lists the three counties correctly.
- Smallest fix: delete ", and its neighbors Custer and Fall River".

### A2-6 MINOR (SBA wording, ruling 8): the clause the integrator removed from FAQ 7 survives in #capital, and the reworded FAQ 7 checks out
- The FAQ 7 rewording is true and says nothing about what SBA requires. Diff of `work/south-dakota.pre-g7.html` against the frozen source: the only change is "each written to that program's requirements" becoming "each written for the program that will read it". The new clause asserts only what the records allow: studies for SBA 7(a) and 504, USDA Rural Development, EB-5 and conventional financing, written for the program. It contains no compulsion word, and the guard returns [] for the page. The question's "the study a USDA Rural Development or SBA lender asks for" is conditional on a lender asking, and the guard skips questions in any case. "which deliverable that program expects" is softer than the records' own "the deliverable the program requires". One residual inaccuracy is in A2-7.
- The same construction survives at line 805: "Whatever the source, Feasibility Study Company's role as a South Dakota feasibility study company is the same: an independent, lender-grade study written to the program's requirements, with every figure traced to a dated source like those above." It follows a paragraph about SBA, USDA, state programs and banks. It passes `sbamandate.flagged()` only because "SBA" is not in that sentence; my near-miss listing printed it beside the 120.160(b) marker sentence. The integrator judged this exact clause unfit in FAQ 7, so the page is inconsistent with its own fix. "with every figure traced to a dated source" is also a blanket quality promise that no record states.
- The closing band's "the deliverable that program wants from the study" (line 94) has no program named in the band to refer to.
- Smallest fix: see A2-11, which deletes this clause for a sameness reason as well.

### A2-7 MINOR: FAQ 7 says 504 loans come from SBA lenders
- Page: FAQ 7 answer, line 88.
- Text: "independent, lender-grade feasibility studies for 7(a) and 504 loans from SBA lenders"
- Reproduction: 504 loans are made through Certified Development Companies alongside a third-party lender. The page's own in-body CTA (line 732) avoids the claim ("an SBA-backed loan"). The records state "SBA 7(a) and 504" with no channel.
- Smallest fix: delete " from SBA lenders" ("for 7(a) and 504 loans, for USDA ...").

### A2-8 MAJOR-NONFACTUAL: the hero opens on the firm sentence, which breaks I81(1) and repeats the District of Columbia's order
- Page: `hero_sub`, line 9.
- Text: "Feasibility Study Company prepares feasibility studies in South Dakota for the owners and developers behind a project and for the SBA lenders, USDA programs and banks that will read them. The lead fact on this page is a tax share: tourism generated 16.5% ... The second is a forecast, ..."
- Reproduction: I81(1) says every later hero "opens on its own lead fact, never on a sentence about the study". SEO-BRIEF (geo-5) asks for the lead fact and the firm statement "in an order no sibling uses". frames.py shows the District of Columbia hero also opens on the firm sentence ("Feasibility Study Company prepares feasibility studies in Washington, DC, written for the owners and developers who commission them and read by the SBA, USDA and bank lenders..."). The other eight GEO-5 heroes open on a fact or a geography. "The lead fact on this page is a tax share:" labels the lead fact rather than opening on it. The pre-SEO hero (`work/south-dakota.before-seo.html`) opened on the tourism fact. The hero also repeats #brief's plan (firm sentence, then "The first is visitors", then "The second is the crop").
- Smallest fix: a pure reorder plus a deletion. Move sentence 1 to the end and delete "The lead fact on this page is a tax share: ", capitalising "tourism". No figure or citation changes.

### A2-9 MAJOR-NONFACTUAL: the description frame is taken, and the description names SBA and USDA as clients
- Page: `description`, line 6 (158 characters).
- Text: "Where tourism raised 16.5% of 2025 sales tax, Feasibility Study Company prepares South Dakota feasibility studies for owners, developers, SBA, USDA and banks."
- Reproduction:
  - The "Where <condition>, ..." opener is on the landed Northwest Arkansas description: "Where a Bentonville sewer basin is full, a Northwest Arkansas feasibility study budgets the new fee; ...". Landed Spokane's description opens "Where does a Spokane feasibility study ...".
  - With the state name normalised, the second half is a 12-token run shared with Colorado's description: "Feasibility Study Company prepares Colorado feasibility studies for owners, developers, SBA, USDA or bank lenders." Vermont's description has the same frame: "...: Feasibility Study Company prepares Vermont feasibility studies for owners, developers and the SBA, USDA or bank lender."
  - The owner's rule wording is "their SBA, USDA and bank lenders". "for ... SBA, USDA and banks" names the agencies as the firm's clients.
  - "16.5% of 2025 sales tax" drops "state". The source says "all state sales tax collections".
- Smallest fix: a description-only Fable pass (I115 practice), keeping 16.5% as its one counted figure and "state sales tax".

### A2-10 MAJOR-NONFACTUAL: the #brief opening uses North Dakota's and Wyoming's clients-and-readers construction
- Page: #brief, line 589.
- Text: "Feasibility Study Company prepares feasibility studies for South Dakota projects. The clients are owners and developers, and the readers are the SBA lenders, USDA Rural Development and banks that finance them."
- Reproduction:
  - North Dakota's first body sentence: "Feasibility Study Company works as a North Dakota feasibility study consultant whose clients are owners and developers and whose readers are the lenders reviewing their loans."
  - Wyoming's: "The client is the owner or developer behind the project, and the reader is whoever will lend on it".
  - North Dakota is the closest sibling, and the client/reader split is a chosen construction, not the owner's mandated sentence. Wyoming's #lead then enumerates ("The first direction is southeast."), as #brief does ("The first is visitors." / "The second is the crop.").
- Smallest fix: merge into one sentence without the client/reader split, for example "Feasibility Study Company prepares feasibility studies for South Dakota projects, for the owners and developers behind them and the SBA lenders, USDA Rural Development and banks that finance them." The integrator may prefer to leave this to the I84 rule (the page that lands second rewords).

### A2-11 MAJOR-NONFACTUAL: the #capital closing repeats Virginia's closing move
- Page: #capital, lines 804 and 805.
- Text: "...is covered on the EB-5 page; no South Dakota regional center figure was in the record." followed by "Whatever the source, Feasibility Study Company's role as a South Dakota feasibility study company is the same: an independent, lender-grade study written to the program's requirements, with every figure traced to a dated source like those above."
- Reproduction: Virginia's #capital ends "...are on the EB-5 page. No Virginia regional center or project figure was in the research. Whichever lender or investor is involved, a Virginia feasibility study company has one job, which Feasibility Study Company does for each of these programs: a study independent of sponsor and lender, written to the program's requirements and traceable, figure by figure, to dated sources like those on this page." The two endings match in plan and in clauses:
  - the EB-5 page pointer, then "no <State> regional center figure";
  - "whatever source / whichever lender" leading to the same role;
  - "written to the program's requirements";
  - "dated source(s) like those".
- Smallest fix: delete " written to the program's requirements, with every figure traced to a dated source like those above" and keep the full stop. This also closes A2-6 and keeps the page's only "South Dakota feasibility study company" mention.

### A2-12 MAJOR-NONFACTUAL: four FAQ question frames are shared with Wyoming, Vermont and Alaska
- Page: front matter `faq.items`, lines 63, 67, 79 and 83.
- Shared frames:
  - FAQ 1: "How does a feasibility consultant treat the Sturgis rally in ...?" Wyoming FAQ 2: "How does a feasibility consultant price Wyoming property tax with Proposition 1 on the ballot?"
  - FAQ 2: "What crop figures does a market study for a South Dakota grain elevator or farm-service project cite in late 2026?" Wyoming FAQ 4: "What wage figures does an SBA feasibility study for a repair shop or field-services yard in Casper cite?" Alaska FAQ 7: "Which airport records does an SBA feasibility study for an Anchorage hotel or warehouse cite?"
  - FAQ 5: "Is there a current apartment vacancy survey that a Sioux Falls multifamily study can cite?" Wyoming FAQ 6: "Is there a hotel occupancy rate for Wyoming or Jackson that a lodging feasibility study can quote?"
  - FAQ 6: "How much did South Dakota Housing award in December 2025, and what does a tax credit feasibility study do with it?" Vermont FAQ 5: "How much flood recovery money has Vermont awarded, and why does an apartment study read it as supply?"
- Reproduction: frames.py output for all ten drafts. None of the shared frames is South Dakota's opening story. I84 gives the frame to the page that lands first. Answers are not shared (no 8-word run).
- Smallest fix: question-only rewording, in an SEO pass, for whichever page lands second. Recorded under I84; this finding does not block on its own.

### A2-13 MAJOR-NONFACTUAL: the closing band's move is Alaska's and Wyoming's
- Page: `cta`, lines 93 and 94.
- Reproduction:
  - Alaska's CTA: "Alaska's revenue forecast is rewritten every spring and fall, and a study is read against the edition it names." That is the forecast-edition move of SD's first clause.
  - Wyoming's CTA: "Wyoming votes on Proposition 1 on November 3, 2026, and a study's property tax line is priced on one side of that date or the other." That is the dated-tax-event move of SD's second clause and its "states the sales tax rate its first full year assumes".
  - SD's band joins the two.
- Fix: A2-1's deletions remove the Alaska half. The Wyoming half remains; under I84 it is a plan note for whichever of the two pages lands second.

### A2-14 MAJOR-NONFACTUAL: the #cases sentences repeat the District of Columbia, Wyoming and Virginia
- Page: #cases, line 810.
- Text: "..., the two kinds of project South Dakota's visitor and farm records bear on most, and an SBA hotel. Each rests on its own state's figures, and a South Dakota study would run the same sequence on the records above."
- Reproduction:
  - District of Columbia: "the two property types most of this page's District records bear on".
  - Wyoming: "Both are built on another state's records; a Wyoming study would take the same steps with the county figures above."
  - Virginia: "Each shows the sequence a Virginia feasibility study would follow with Virginia's own records in place of its state's".
  - North Dakota: "the kinds of project the oil field, the highway work and the Flex PACE program on this page bear on".
  - Smaller point: the linked "USDA meat processing plant" case is titled "Poultry Processing Feasibility Study in Georgia: USDA B&I Worked Case".
- Smallest fix: delete ", the two kinds of project South Dakota's visitor and farm records bear on most," and delete " Each rests on its own state's figures, and a South Dakota study would run the same sequence on the records above."

### A2-15 MINOR: the USDA eligibility rule is stated with no source
- Page: #capital, line 802, and FAQ 7, line 88.
- Text: "Outside the Sioux Falls and Rapid City areas, many South Dakota sites are candidates for USDA Rural Development, whose map decides, one parcel at a time, whether a site can carry a B&amp;I guarantee or Community Facilities money." / FAQ 7: "Outside Sioux Falls and Rapid City the USDA map is checked one parcel at a time before the program is named,"
- Reproduction: ST line 80 is "NOT FOUND: ... USDA Rural Development South Dakota FY2025 totals". No research row holds a USDA eligibility rule or a map, and the sentence carries no citation. Community Facilities and B&I use different population limits, so "outside Sioux Falls and Rapid City" is not one rule for both.
- Smallest fix:
  - #capital: delete the first sentence, starting at "Outside" and ending at "money.".
  - FAQ 7: delete "Outside Sioux Falls and Rapid City the USDA map is checked one parcel at a time before the program is named, and " and capitalise "a state award" to "A state award".

### A2-16 MINOR: the Sioux Falls metro is described as Minnehaha, Lincoln and Rock County, but McCook and Turner are left out
- Page: #metros, line 730; FAQ 4, line 76; #sioux-falls, line 740.
- Text: "Five of the six sit wholly inside South Dakota. Sioux Falls does not: the Labor Market Information Center draws its Sioux Falls metropolitan area to include Rock County, Minnesota [^9]"
- Reproduction: WebFetch of source 9 quotes "including Lincoln, Minnehaha, McCook and Turner counties of South Dakota and Rock County of Minnesota". ST-2 line 104 says the same. The Rock County label is true. But the card and the lede define the Sioux Falls market as Minnehaha and Lincoln, which do sit wholly inside the state. The metro-wide figures also take in McCook and Turner, and the page never names them.
- Fix (optional): none required for truth. If the integrator wants the label complete, that is a wording addition, not mine to propose.

### A2-17 MINOR: the neighbour links
- Minnesota is earned. Rock County, Minnesota is inside the LMIC Sioux Falls MSA, and a counted figure rests on it; WebFetch confirmed it, as above.
- The Iowa link (line 668) rests on KOTA's report that Summit's new route "affects counties in Iowa". The research note (ST line 147) reads "Page prints 12 Iowa counties affected by the new route". That is a fact about Iowa, not one that makes the South Dakota and Iowa border matter for a project here, so the link is weakly earned. The fact that would earn it, Union County's place in the Sioux City metro, is not in the research.
- Nebraska and Montana are not named in prose; they appear only in the generated neighbour block and the menu. North Dakota and Wyoming are neither named nor linked anywhere on the rendered page.
- The generated block's heading, "States that border South Dakota.", lists four of the six. That is the template (`neighbors5.py`), not this source.
- Fix (optional): none required.

### A2-18 MINOR: South Dakota has no landing requests
- Reproduction: `~/Downloads/wt-rollout-geo-5/docs/rollout/geo-5/requests.json` holds `chrome_link` and `index_entry` requests for Colorado and Virginia (geo-5-2 to geo-5-8) and none for South Dakota. In the copy, `states/index.html` and `index.html` carry 0 mentions of "South Dakota", and the mega menu omits it. I177's landing added these for a new state. Gate 9 is green on the four neighbour pages alone.
- Fix: an integrator request at landing; no page edit.

### A2-19 MINOR: plain claims with no source
- Line 793: "Pierre is the state capital, and state government is a large employer there, but no Pierre-only government count was found." No row supports "a large employer". Fix: delete ", and state government is a large employer there, but no Pierre-only government count was found" so the sentence ends "Pierre is the state capital."
- Line 755, #rapid-city h2: "rally money that moved south". DOR reports a statewide decrease and an increase for the southern hills vendors (ST-2 line 129; line 763). It does not report money moving between the two. Fix: delete "rally money that moved south, ".
- Line 623: "Health care and public employment carry a large part of the state's payroll". This is a share stated in words with no total in the sentence (I60). It belongs to attacker one; I record it.

### A2-20 MINOR: the engagement list is said three times
- The three items (project, county or market, capital source) appear in FAQ 7 (line 88), the in-body CTA (line 732) and the band (line 94). The in-body CTA is the brief's mandated move. I record the band's restatement under I89's judgment reading.
- Fix: none required.

### A2-21 MINOR: a run of BLS sector labels shared with Vermont
- Line 623 and Vermont's #economy, with digits dropped: "thousand jobs in education and health services, thousand in government" (10 words).
- These are BLS supersector names, the label category I115 allows.
- Fix: none required.

## Counted figures after my confirmed findings
No finding deletes or wraps a counted figure. The A2-4 deletion removes an `sba:` value, which pagecheck does not count. The A2-1, A2-3, A2-5, A2-11, A2-14, A2-15 and A2-19 deletions carry no counted value and orphan no source. The page holds 107 counted figures (98 research, 9 register), over the READY floors (30 and 20) and the landing floors (25 and 15).

Severity tally: BLOCKER 0; MAJOR-FACTUAL 5 (A2-1 to A2-5); MAJOR-NONFACTUAL 7 (A2-8 to A2-14); MINOR 9 (A2-6, A2-7, A2-15 to A2-21).
