# GEO-5 t4 freeze 1, North Dakota: attacker B (gates, links, sameness, buyer intent, claims)

Page: `/states/north-dakota/` (no metro page). Source read: `~/Downloads/fsc-rollout/tmp/geo-5/t4/src/pages/states/north-dakota.html`, byte-identical to `drafts/geo-5/pages/north-dakota.html` (`cmp` silent). Rendered page: `tmp/geo-5/t4/states/north-dakota/index.html`. Line numbers below are the source file's.

## What I ran
- `tools/sameness.py --ours <copy source> --against ~/Downloads/wt-rollout-geo-5/src/pages pages/*.html pages/colorado pages/virginia` (104 files, landed Colorado, Denver, Virginia and Northern Virginia included). Max 0.52% (Nashville). Every shared 8-word run is `sba:` marker text (13 CFR 120.160(b), SOP name), a register row label, or a hub-name list (`truck stop and travel center gas station and c store`, `childcare and daycare assisted living and memory care`). No 8-word finding.
- The same shingler at 7 words (scratchpad script importing `sameness.text_of`), to find near-frames; the hits are used below.
- `tools/frames.py` on ND, SD, Alaska, Vermont, Wyoming, DC drafts and landed Colorado, Denver, Virginia, Northern Virginia; first body paragraph and `#cases` of every GEO-5 draft and of landed Colorado, Virginia, Montana, Idaho, Delaware.
- `tools/draftcheck.py pages/north-dakota.html --figures --promised`: 0 problems.
- `scripts/qa/gates.py --root . --git-dir ~/Downloads/wt-rollout-geo-5 --urls /states/north-dakota/ --stage ready --only 4,9 --skip-look` inside the copy: gates 3, 4, 5, 9 GREEN, 64 counted (56 research, 8 register), max overlap 0.51%; agrees with GATES-t4-f0.txt.
- Keyword cap (I89) on the rendered `<main>`: "North Dakota feasibility study consultant" 2, "North Dakota feasibility study company" 1, "North Dakota feasibility study" 3 (the two above plus none other). Within the cap. Description 155 characters.
- Forbidden service claims: regex scan of front matter (sources dropped) and body for local, on the ground, team, office, visit, fee, price, turnaround, days, weeks, guarantee, approval rate, licen[cs]e, certif, credential, our, we. No hit is a service claim (every hit is a data label, "USDA Rural Development guarantee(s)", or a licensing office the study consults).
- SBA wording (ruling 8): no "SBA requires"; the only rule text is the `sba:` 13 CFR 120.160(b) marker ("may require"). "SBA 7(a) or 504 loans" in `service.description` (line 36) names a financing channel, implies no requirement. Passes.
- Closing band (rendered `section.cta-band`): the only digits are "2026". No figure. Passes.
- Mesh term "North Dakota" (requests.json `geo-5-21`): walked every rendered page in the copy for `href="/states/north-dakota/"` outside header, nav and footer. One term link: `/asset-classes/hotel/` "...Montana 4.69, Alaska 3.95 and [North Dakota] 3.69...", which sits on the state's own name. Montana and Minnesota link it only through their generated "Neighboring Markets" lists. No other GEO-5 draft mentions North Dakota. Passes. Latent, not a finding today: `mesh.py`'s `term_pattern` (lookbehind `(?<![A-Za-z0-9&;-])`) would also match inside "Bank of North Dakota" or "University of North Dakota" on any future page that names them first.
- Gate 9 inbound: the 3 inbound pages are `/asset-classes/hotel/` (prose) and `/states/montana/`, `/states/minnesota/` (generated neighbour lists, which `gates.py` `body_links` counts). Reported for the integrator, not a page finding.
- WebFetch: bnd.nd.gov 2025 annual report release; Yahoo / North Dakota Monitor data center article; Minot Daily News gas record article; fema.gov/assistance/public. No refusal met.

## The five plain claims the writer said rest on general knowledge
1. "The Bank of North Dakota, which the state owns" (line 403, with [^2]; h2s at 397 and 417 "a bank the state owns"). HOLDS. The cited release reads: "Bank of North Dakota is the nation's only state-owned bank." The research row (ST line 48 to 54) does not record it, but the cited source carries it. No finding.
2. Bismarck and Mandan across the Missouri: no source. A2-6.
3. Fargo and Grand Forks on the Red River: no source. A2-7.
4. Williams and McKenzie on the Montana line: no source, and it is the only basis for the Montana link. A2-8.
5. FEMA Public Assistance reimburses public bodies: no source, and incomplete. A2-3.

## Findings

### A2-1 MAJOR-FACTUAL: the Service description says the page is built on the state's oil and gas reports
- Page: front matter `service.description` (line 36, JSON-LD).
- Quote: "built on the state's oil and gas reports, BLS county wage files, airport boarding counts and FEMA declarations."
- Reproduction: the body says the opposite at line 400 ("the department's own site refused the connection when the research for this page was done, so every oil and gas number here is the newspaper's reading of the briefing") and line 409. Every oil and gas figure cites [^1], the Minot Daily News (publisher line 101 marks it "secondary"). The structured data tells search engines the page rests on primary state reports it never opened.
- Fix: delete "the state's oil and gas reports, " (leaves "built on BLS county wage files, airport boarding counts and FEMA declarations.").

### A2-2 MAJOR-FACTUAL: two promises about every study that the page itself contradicts
- Page: `hero_sub` (line 7) and the opening paragraph (line 399).
- Quotes: hero "and every input carries the date of the release it was read from."; overview "Each study is independent and built to a lender's standard, which in practice means that every demand, cost and revenue assumption can be traced to a public source with a date."
- Reproduction: line 512 says construction "comes from the contractor's bid", insurance "comes from the broker's quote for the parcel"; line 443 says the study turns "to its own rent survey of comparable properties"; line 527 "a competitive set survey of its own"; line 552 "a property-by-property survey of competitors". None of these is a public source or a release. Line 421 prints FDIC totals with "no release date". The two sentences also state how every study is built, which no record named in WRITER-BRIEF ("Buyer intent") supports: the records say the firm prepares independent, lender-grade studies and answers an inquiry with the framework, the deliverable and next steps; nothing on dating every input. It reads as a quality guarantee.
- Fix: hero, delete ", and every input carries the date of the release it was read from" (see A2-15 for the whole hero sentence). Overview, delete the sentence "Each study is independent and built to a lender's standard, which in practice means that every demand, cost and revenue assumption can be traced to a public source with a date." and change "This page is that source record" to "This page is a source record".

### A2-3 MAJOR-FACTUAL: Public Assistance described without a source, and wrongly as repaying public bodies "rather than owners"
- Page: `#hazards` line 504; FAQ 6 (line 86).
- Quotes: "The county designations under the three storm declarations are for Public Assistance, which reimburses public bodies for response and repair"; "Owners of damaged commercial property recover through their own insurance and, where SBA opens disaster lending, through SBA."; FAQ 6 "the county designations are for Public Assistance, which repays public bodies rather than owners."
- Reproduction: no source in the pool (lines 99 to 393) and no research row describes who Public Assistance pays (ST lines 123 to 129 only name the program). fema.gov/assistance/public: "An applicant must be a state, territory, tribe, local government or private nonprofit organization." A private nonprofit owner (a nonprofit child care center or senior care community, two of the page's own asset classes) is an eligible applicant, so "rather than owners" is wrong. The SBA disaster-lending sentence has no source either.
- Fix: line 504, delete ", which reimburses public bodies for response and repair" and delete the sentence "Owners of damaged commercial property recover through their own insurance and, where SBA opens disaster lending, through SBA."; FAQ 6, delete ", which repays public bodies rather than owners".

### A2-4 MAJOR-FACTUAL: the Minnesota page does not take up the Minnesota side of Grand Forks
- Page: `#overview` line 404.
- Quote: "Fargo and Grand Forks face Minnesota across the Red River, and federal agencies draw both metro areas across the state line; the Minnesota side of each is left to the Minnesota page."
- Reproduction: `grep -ciE 'grand forks|polk|east grand forks'` on `wt-rollout-geo-5/src/pages/states/minnesota.html` returns 0. Minnesota covers Moorhead (`#other-places`), so the Fargo section's "Moorhead is taken up on the Minnesota page" (line 596) is true, but nothing on the Minnesota page reads Polk County or East Grand Forks.
- Fix: replace "the Minnesota side of each is left to the Minnesota page" with "the Minnesota side of each is left out" (the Minnesota link stays at line 596). The river clause is A2-7.

### A2-5 MAJOR-FACTUAL: EB-5 rule stated without a source and against the site's own EB-5 page
- Page: `#programs` line 651.
- Quote: "An EB-5 offering rests on two things a study must document: the jobs its spending creates, by an accepted model, and the designation of the area the site lies in."
- Reproduction: no source in the pool. The served `/practice-areas/eb-5/` defines a Targeted Employment Area as the area "in which the reduced EB-5 investment threshold applies" and gives the standard minimum ($1,050,000) for a project outside one. Area designation sets the investment amount; it is not a precondition of every offering.
- Fix: delete the sentence (the next two sentences stand alone).

### A2-6 MINOR: "across the Missouri" has no source
- Page: `#costs` line 510; `#bismarck-mandan` h2 line 603; Bismarck-Mandan card line 587 ("The capital and Mandan across the Missouri").
- Quotes: "across the Missouri River from each other"; "two counties across the Missouri"; "across the Missouri".
- Reproduction: `grep -ci missouri` on ST-NORTH-DAKOTA.md, MT-NORTH-DAKOTA.md and the assignment returns 0 (the fact sheet's 4 hits are links to the Missouri state page and a Missouri case). No source in the pool. True, but uncited; nothing on the page turns on it.
- Fix: line 510 delete ", across the Missouri River from each other"; line 603 replace "two counties across the Missouri" with "two counties"; line 587 replace "The capital and Mandan across the Missouri" with "Bismarck and Mandan".

### A2-7 MINOR: the Red River has no source, and it is used to raise a flood point
- Page: line 404 ("face Minnesota across the Red River"); `#hazards` line 505 ("Fargo and Grand Forks sit on the Red River, and their flood exposure is a parcel question"); cards line 586 ("A Red River city"), 588 ("A second Red River county"); `#fargo` h2 line 594 ("all on the North Dakota bank of the river") and line 596 ("cover both banks of the Red River").
- Reproduction: no research row and no source mentions the river (grep "red river" on both research files: 0). The research does carry the two-state metros (MT lines 16 to 18, 95 to 97: "Metro includes Clay County, Minnesota", "Metro includes Polk County, Minnesota"), which is what the state-line point needs. Line 505 then infers flood exposure from an uncited geography on a page whose research holds no flood record.
- Fix: line 404 "face Minnesota across the Red River, and federal agencies" to "border Minnesota, and federal agencies"; line 505 delete "Fargo and Grand Forks sit on the Red River, and their flood exposure is a parcel question this page's record does not answer: " and begin the sentence at "The research did not reach..." (capitalized); line 586 "A Red River city" to "A border city"; line 588 "A second Red River county" to "A second border county"; line 594 delete ", all on the North Dakota bank of the river"; line 596 "cover both banks of the Red River" to "cover both states".

### A2-8 MAJOR-NONFACTUAL: the Montana line is uncited and the Montana link is made for effect
- Page: `#williston` line 631; `#metros` h2 line 584 ("from the Red River to the Montana line").
- Quote: "Both counties lie on the Montana line; nothing from the Montana side is counted here, and the <a href="/states/montana/">Montana</a> page reads that state's markets."
- Reproduction: no research row or source states it (grep "montana" on both research files: 0). No figure on the page could have crossed the line: the research found no two-state series for Williston or Watford City (MT line 180: BLS has no Williston or Dickinson metro page), and the Montana page says nothing about the Bakken, Richland County or North Dakota (`grep -ciE 'williston|bakken|richland|north dakota'` on montana.html: 0 outside the generated neighbour list). WRITER-BRIEF P5: name a neighbour "where a fact makes the border matter; never for effect". The generated neighbour region already links Montana.
- Fix: delete the sentence; line 584 replace ", from the Red River to the Montana line," with "," (or ", from Fargo to Williston,").

### A2-9 MINOR: Stark County and Dickinson placed in the oil field with no source
- Page: line 402 ("A project in Williams, McKenzie or Stark County takes its customers from an oil field that set gas and well-count records"); line 641 ("Dickinson sits in the southern part of the oil field, so the production and rig series in the oil and gas section apply to it as they apply to Williston"); card line 591 ("The southwestern oil county").
- Reproduction: no row places Stark in the field. The cited [^1] (Minot Daily News, fetched) names McKenzie, Williams, Dunn, Mountrail and Divide as the top producing counties; Stark and Dickinson are not named. "apply to it as they apply to Williston" equates the two with no record.
- Fix: line 402 "Williams, McKenzie or Stark County" to "Williams or McKenzie County"; line 641 delete the sentence "Dickinson sits in the southern part of the oil field, so the production and rig series in the oil and gas section apply to it as they apply to Williston."; line 591 "The southwestern oil county" to "The southwestern county".

### A2-10 MINOR: "The reservation spans several Bakken counties" is not in the cited source
- Page: `#bakken` line 412.
- Reproduction: the phrase is a researcher's note (MT line 153, notes column). The Minot Daily News article (fetched) gives 3,040 active wells and one rig on Fort Berthold and names no county for the reservation.
- Fix: delete "The reservation spans several Bakken counties, so a site on or near it reads the reservation's activity and the county series together." 

### A2-11 MINOR: two metro-composition statements with no source
- Page: line 631 ("McKenzie County, whose seat is Watford City and which has no Census metropolitan or micropolitan area of its own"); line 605 ("BEA's and FHFA's Bismarck metropolitan area reaches beyond those two counties").
- Reproduction: no research row gives the delineation of either (MT lines 62, 73, 77 name "Bismarck ND MSA" without its counties; nothing on McKenzie's CBSA status). True to my knowledge, uncited.
- Fix: line 631 delete " and which has no Census metropolitan or micropolitan area of its own"; line 605 replace "BEA's and FHFA's Bismarck metropolitan area reaches beyond those two counties, so the two figures here that describe the wider area say so." with "The two figures here that describe BEA's and FHFA's Bismarck metropolitan area say so."

### A2-12 MINOR: "In this record the deciding body ... is the township"
- Page: `#rules` line 519.
- Reproduction: the cited [^32] article (fetched) reports that annexing the Harwood data center site into city limits was under discussion, so the record holds a city, not only a township, as a deciding body; [^33] concerns a different project (Geronimo Power's Harmony Energy Park).
- Fix: delete "In this record the deciding body for a large load in the countryside is the township." 

### A2-13 MINOR: the Dickinson card says "little else published"
- Page: card line 591 ("with a county payroll and wage and little else published") and h2 line 638 ("a record that stops there").
- Reproduction: the research found little; it does not show little is published. MT lines 166 to 171 hold Stark unemployment rows and a dated $25 million terminal award (2026-10-07); line 173 records items NOT FOUND, not unpublished.
- Fix: line 591 "little else published" to "little else found for this page".

### A2-14 MINOR: USDA eligibility rule stated without a citation
- Page: `#programs` line 649.
- Quote: "eligibility is a parcel test against the agency's map on the application date, and the study runs it before anything else."
- Reproduction: no source in the pool; ruling 8 routes USDA terms through PA-USDA with their citations. The served USDA practice page carries the rural-eligibility point.
- Fix: delete from ": eligibility is" to "anything else" (sentence ends "USDA Rural Development's guarantees turn on where the site is.").

### A2-15 MAJOR-NONFACTUAL: the "two readers" and clients/readers frames are other drafts' openers, and the two framings contradict each other
- Page: `hero_sub` line 7; `#overview` line 399.
- Quotes: hero "for the two readers every study has, the owners and developers who commission it and the bank, SBA or USDA lender who decides on the loan"; overview "a North Dakota feasibility study consultant whose clients are owners and developers and whose readers are the lenders reviewing their loans."
- Reproduction: `grep -rli 'two readers'` over landed sources and GEO-5 drafts: Vermont ("serves two readers: whoever builds or buys the property, and the bank..."), Alaska ("written for two readers at once: the owner or developer ... and the lender"), North Dakota. First paragraphs: South Dakota, the closest sibling, "The clients are owners and developers, and the readers are the SBA lenders, USDA Rural Development and banks"; Wyoming "The client is the owner or developer ..., and the reader is whoever will lend on it". The overview's next moves (assumptions traced to dated public sources, then "This page is that source record") are landed Virginia's plan ("a demand and cost case that a credit officer can trace back to dated public sources. This page lays out those sources"). Inside the page the hero makes owners readers and the overview makes only lenders readers; and "every study has" two readers is untrue of an EB-5 study, which the page offers (line 651).
- Fix: hero, replace "for the two readers every study has, the owners and developers who commission it and the bank, SBA or USDA lender who decides on the loan. The first thing each one settles is whether the project's customers come from that oil field or from a county payroll, and every input carries the date of the release it was read from." with "for owners and developers and for the bank, SBA or USDA lender who decides on the loan."; overview, replace "whose clients are owners and developers and whose readers are the lenders reviewing their loans" with "for owners and developers and the lenders reviewing their loans", plus the A2-2 deletion.

### A2-16 MAJOR-NONFACTUAL: the hero repeats Alaska's hero plan
- Page: `hero_sub` line 7.
- Reproduction: Alaska's hero: resource-production lead fact (North Slope forecast, Pikka first oil), firm statement, then "Each one sets the borough's or census area's own population, payroll and wage record beside that state forecast, with the date of every source." North Dakota: resource-production lead fact (gas record, well count), firm statement, then "whether the project's customers come from that oil field or from a county payroll, and every input carries the date". Same three moves, same oil-against-local-payroll argument, same dating close. Landed Colorado and Virginia also close their heroes on a dated-records clause.
- Fix: the A2-15 hero edit removes the third move.

### A2-17 MAJOR-NONFACTUAL: the closing band's move is landed Virginia's and Denver's, with DC's sentence
- Page: `cta.h2` and `cta.p` lines 95 to 96.
- Quote: "A study commissioned now is written to those releases as they stand on its date".
- Reproduction: 7-word run "a study commissioned now is written to" shared with the DC draft's `cta.p` ("A study commissioned now is written to the October releases"). Landed Virginia: h2 lists recent releases ("September payrolls, third-quarter broker reports ..."), p "A study written against those releases carries their dates into the credit file." Landed Denver: "A study written now reads the market as it stands." ND's h2 lists recent releases including the September payroll count and its p writes the study "to those releases as they stand".
- Fix: in `cta.p` replace "A study commissioned now is written to those releases as they stand on its date, and the first exchange settles" with "The first exchange settles".

### A2-18 MAJOR-NONFACTUAL: FAQ 6 uses the "insurance line" frame I88 keeps for California
- Page: FAQ 6 question, line 85.
- Quote: "Does the insurance line in a feasibility study for a Williston, Fargo or Bismarck site have to answer for the 2024 to 2026 federal declarations?"
- Reproduction: I88: "California keeps ... the 'insurance line of a <State> feasibility study' description frame"; I115 calls it "the frame I88 keeps for California". Landed california.html description: "Price the insurance line of a California feasibility study to that cover."
- Fix: replace the question with "Do the 2024 to 2026 federal declarations reach the property policy for a Williston, Fargo or Bismarck site?"

### A2-19 MAJOR-NONFACTUAL: the `#cases` plan is the Vermont, Alaska and Colorado plan; the lede misdescribes the cases
- Page: `#cases` lines 654 to 656.
- Quotes: "The method carries across state lines even though the inputs do not." ... "A North Dakota version of any of them would replace the wage line with its county's figure from the economy section and the demand line with ..."; lede "Every case on this site was modeled on a project outside North Dakota".
- Reproduction: Alaska "Their structure carries over to Alaska; their inputs do not. Here the payroll line comes from the borough wage..."; Vermont "The case studies include an SBA fitness center ..., a USDA RV park ... A Vermont version of any of them would keep the method and change the inputs: the county wage ... in place of the payroll line"; DC "The case studies include hotels ... A District version of either would keep the case's structure and change three inputs: the payroll series"; landed Colorado "would follow the same structure with this page's inputs in place of theirs: county wages". ND has the same three moves (method carries, inputs do not; "The case studies include" three cases by program; a state version swaps the wage line). The lede's "modeled on a project" is untrue of the hypothetical cases (landed Utah, Maine and Hawaii pages call theirs hypothetical).
- Fix: delete "The method carries across state lines even though the inputs do not." and the sentence beginning "A North Dakota version of any of them"; lede "Every case on this site was modeled on a project outside North Dakota, and no North Dakota case is scheduled." to "No case on this site is set in North Dakota, and none is scheduled." (promised.json holds no North Dakota entry, so "none is scheduled" stands).

### A2-20 MAJOR-NONFACTUAL: FAQ answers repeat the body's argument in the body's words (I115)
- Page: FAQ 1, 2, 4, 7 against the body.
- Reproduction (8-word shingles of each FAQ item against the body; values, publisher names and county lists set aside as I115 allows):
  - FAQ 7 (line 90) against line 623 to 624: "held level while the bedroom towns around it grew" (the trade-area argument) and the whole sentence "BLS's county file lists 30,481 insured jobs in Ward County for March 2026 and an average of $1,234 a week in first-quarter pay [^8]", 27 shared shingles.
  - FAQ 2 (line 70) against line 411: "Rigs and completion crews are a mobile workforce" and "the field after the crews have moved on", the body's argument twice.
  - FAQ 4 (line 78) against line 510: "carries the error into every year of the projection" and the debt service coverage close.
  - FAQ 1 (line 66) against line 399: "the owner or developer commissions the study; the bank ... USDA Rural Development lender asked to finance the project".
  I115: for lanes other than GEO-3 an in-page repeat blocks when it is a sentence frame or argument.
- Fix: FAQ 7, delete "a city that held level while the bedroom towns around it grew" (with its preceding comma) and the sentence "On the payroll side, BLS's county file lists 30,481 insured jobs in Ward County for March 2026 and an average of $1,234 a week in first-quarter pay [^8], the county's dated inputs for a sales or staffing line."; FAQ 2, "No, because it describes the field after the crews have moved on." to "No." and "Rigs and completion crews are a mobile workforce, so a lodging" to "A lodging"; FAQ 4, delete "A statewide average copied into either carries the error into every year of the projection and into the debt service coverage test."; FAQ 1, see A2-21. No counted figure is lost (each value stays in the body).

### A2-21 MAJOR-NONFACTUAL: the engagement FAQ shares South Dakota's and Alaska's construction and goes beyond the records
- Page: FAQ 1, lines 65 to 66.
- Quotes: "what does Feasibility Study Company ask for before starting?"; "The studies Feasibility Study Company prepares are independent and lender-grade, written for"; "the programs work through the lender making the loan, so the coverage test runs with the buydown and without it. A first message with three facts, the project, the county of the site and where the money is expected from, gets back ..."
- Reproduction: 7-word run "with three facts the project the county" shared with the South Dakota draft ("The engagement opens with three facts, the project, the county or market of the site and the capital source, and the reply describes ..."). Alaska's first paragraph: "The studies Feasibility Study Company prepares in Alaska are independent and lender-grade, written for" (ND drops only "in Alaska"); Alaska FAQ 2 "What should a first message to Feasibility Study Company ... say". The question frame "what does Feasibility Study Company ask for before starting" is landed Denver's "What does Feasibility Study Company need to start a Denver project" and landed Virginia's "What does a feasibility consultant need to start a study in Virginia?". Against the records (WRITER-BRIEF, Buyer intent): "the coverage test runs with the buydown and without it" is a practice claim no record states; "ask for before starting" sets a precondition the records do not; the BND programs clause is cited to [^2], which (fetched) says only that the bank "partners with financial institutions", while the program detail is [^16]'s.
- Fix: question to "Who hires a North Dakota feasibility study consultant, and who reads the study?"; answer, replace "The studies Feasibility Study Company prepares are independent and lender-grade, written for" with "Feasibility Study Company writes independent, lender-grade studies for"; delete "; the programs work through the lender making the loan, so the coverage test runs with the buydown and without it" (sentence then ends at "[^2]."); delete the closing sentence "A first message with three facts, ... from there." (the in-body CTA at line 643 and the closing band already say what to send and what comes back).

### A2-22 MINOR: the description says the well count informs every North Dakota study
- Page: `description` line 6.
- Quote: "19,961 producing wells inform North Dakota feasibility studies prepared by Feasibility Study Company for owners, developers and SBA, USDA and bank lenders."
- Reproduction: line 402 says Cass, Burleigh, Grand Forks and Ward projects take customers from payrolls, airports and housing, not the field; the number carries no month (June 2026 is in the body). Figure-first is also landed Colorado's description frame ("12,100 net lost to other states to June 2025. Feasibility Study Company prepares ...").
- Fix: "19,961 producing wells inform North Dakota feasibility studies prepared by" to "June 2026 put 19,961 wells in production; North Dakota feasibility studies by" (or a Fable description pass).

### A2-23 MINOR: FAQ frames close to taken ones
- FAQ 3 "Which airport months belong in a Fargo or Bismarck hotel market study ..." against the taken "Which <X> should a <state> study use?" (SEO-BRIEF, Minnesota, Missouri).
- FAQ 7 "Where does a retail or child care market study in Minot draw its trade area ..." against landed Virginia "Where does a hotel feasibility study in Virginia get its visitor counts?" and Wyoming's draft "Where does a market study for Gillette or Rock Springs get a county job count ...".
- FAQ h2 "Seven questions a North Dakota credit file tends to raise." against landed Colorado "Seven things a sponsor asks ..." and Vermont's draft "Seven Vermont questions, ...".
- Fix: FAQ 3 "Which airport months belong in" to "Are the state's airport months or the airport's own months the input for"; FAQ 7 "Where does a retail or child care market study in Minot draw its trade area" to "Should a retail or child care market study in Minot stop its trade area at the city line"; FAQ h2 "Seven questions a North Dakota credit file tends to raise." to "Questions a North Dakota credit file tends to raise."

### A2-24 MINOR: repeated sentence frames inside the body
- Reproduction (8-word repeats within the body): "a survey-year figure given for scale" (lines 610, 625, 640, and 635's "survey-year figures given for scale"); "is not among the counties of the four" (626, 641); "the city's permit and certificate of occupancy files" (552, 618); "the research for this page did not find" (442, 649). These are frames, not values. Below the I115 blocking line only because they carry no argument; the deposit sentence is the same template four times.
- Fix: line 625 and 640 delete ", a survey-year figure given for scale" (the line 421 explanation covers all county deposit totals: "County deposit totals from the 2025 Summary of Deposits appear in some market sections on the same terms.").

## Checked and passed (no finding)
Title and H1 in the house pattern; description 155 characters; keyword forms within I89; no fee, price, turnaround, office, staff, site visit, licence or credential claim; no "local", "on the ground" or "our team"; no SBA mandate wording, `sba:` markers only; "SBA 7(a) or 504 loans" implies no requirement; in-body CTA placed at the end of the last market section with what to send and the briefing button; closing band carries no figure; no 8-word run shared with any landed page or GEO-5 draft beyond marker text, register labels and hub names; mesh link from the hotel hub sits on the state's name; gates 3, 4, 5 and 9 reproduce GATES-t4-f0; BND "state-owned" carried by [^2]; "no North Dakota case is scheduled" agrees with `data/site/promised.json`.

## Counted figures after my findings
No fix above deletes or wraps a counted figure (the FAQ deletions in A2-20 and A2-21 remove repeats of values the body still prints and counts). North Dakota stays at 64 counted: 56 research, 8 register (gate 3 rerun in the copy), above the READY floor (30, 20 research) and the landing floor (25, 15).

## Tally
BLOCKER 0; MAJOR-FACTUAL 5 (A2-1 to A2-5); MAJOR-NONFACTUAL 8 (A2-8, A2-15 to A2-21); MINOR 11 (A2-6, A2-7, A2-9 to A2-14, A2-22 to A2-24).
