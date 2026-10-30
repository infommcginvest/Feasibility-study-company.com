# GEO-5 t4 freeze 1 verifier fix list for /states/north-dakota/. Paths are relative to drafts/geo-5/pages.
# 43 edits, each old string occurs exactly once in src/pages/states/north-dakota.html (sha256 16ba0e93...b020f0), no two overlap.
# Run against the frozen source: body words 7,178 -> 6,715; counted figures 64 (research 56, register 8/8) -> 64 (56, 8/8), no counted value removed or added;
# gate 4 overlap max 0.5% (Nashville) unchanged; no new 7-word or 8-word run shared with any landed page or GEO-5 draft; no source left uncited (49 of 49 cited).
# Edits marked NON-DELETION change or add words (a pure deletion, nocount wrap or restoration is not marked).
EDITS = [
    # A2-1: the Service description says the page is built on the state's oil and gas reports; the body says they could not be opened
    ("north-dakota.html",
     "built on the state's oil and gas reports, BLS county wage files",
     "built on BLS county wage files"),
    # A2-2 + A2-15 + A2-16 (hero): NON-DELETION. Drops the universal dating promise, the "two readers" frame and the third hero move
    ("north-dakota.html",
     "for the two readers every study has, the owners and developers who commission it and the bank, SBA or USDA lender who decides on the loan. The first thing each one settles is whether the project's customers come from that oil field or from a county payroll, and every input carries the date of the release it was read from.",
     "for owners or developers and for the bank, SBA or USDA lender who decides on the loan."),
    # A2-15 (overview, sentence 1): NON-DELETION. The clients/readers split is South Dakota's frame and contradicts the hero's "readers"
    ("north-dakota.html",
     "consultant whose clients are owners and developers and whose readers are the lenders reviewing their loans.",
     "consultant for owners and developers and the lenders reviewing their loans."),
    # A2-2 (overview): NON-DELETION (one word, "that" to "a"). "Every assumption traced to a dated public source" is contradicted by the page's own bid, quote and survey lines
    ("north-dakota.html",
     "built to a lender's standard, which in practice means that every demand, cost and revenue assumption can be traced to a public source with a date. This page is that source record for North Dakota",
     "built to a lender's standard. This page is a source record for North Dakota"),
    # A2-9 (overview): NON-DELETION. Stark County is placed in the oil field with no record
    ("north-dakota.html",
     "A project in Williams, McKenzie or Stark County takes its customers",
     "A project in Williams or McKenzie County takes its customers"),
    # A2-4 + A2-7 (overview): NON-DELETION. The Minnesota page does not take up Grand Forks; the Red River is uncited
    ("north-dakota.html",
     "Fargo and Grand Forks face Minnesota across the Red River, and federal agencies draw both metro areas across the state line; the Minnesota side of each is left to the <a href=\"/states/minnesota/\">Minnesota</a> page.",
     "Fargo and Grand Forks face Minnesota, and federal agencies draw both metro areas across the state line; the Minnesota side of each is left out."),
    # A1-6a (#bakken h2): NON-DELETION (one "and"). "rose" compares two rig counts that are not in the heading
    ("north-dakota.html",
     "a gas record, a well-count record and a rig count that rose into August.",
     "a gas record and a well-count record."),
    # A1-6a + A2-9 (#bakken last paragraph): NON-DELETION. Rig-count comparison does not occur here; Stark County in the oil economy has no record
    ("north-dakota.html",
     "The county side of the oil economy is in the <a href=\"#williston\">Williston</a> and <a href=\"#dickinson\">Dickinson</a> sections: covered jobs and wages for Williams, McKenzie and Stark counties from the first-quarter 2026 file",
     "The county side of the oil economy is in the <a href=\"#williston\">Williston</a> section: covered jobs and wages for Williams and McKenzie counties from the first-quarter 2026 file"),
    # A2-3 (#hazards): who Public Assistance pays is uncited and wrong for private nonprofits; the SBA disaster-lending sentence has no source
    ("north-dakota.html",
     "for Public Assistance, which reimburses public bodies for response and repair; the research shows no Individual Assistance designation for them. Owners of damaged commercial property recover through their own insurance and, where SBA opens disaster lending, through SBA. A study",
     "for Public Assistance; the research shows no Individual Assistance designation for them. A study"),
    # A2-7 (#hazards): NON-DELETION (capital F). The Red River is uncited
    ("north-dakota.html",
     "Fargo and Grand Forks sit on the Red River, and their flood exposure is a parcel question this page's record does not answer: the research did not reach",
     "Flood exposure is a parcel question this page's record does not answer: the research did not reach"),
    # A2-3 (FAQ 6)
    ("north-dakota.html",
     ", which repays public bodies rather than owners.",
     "."),
    # A2-6 (#costs): the Missouri River is uncited
    ("north-dakota.html",
     "Mandan's Morton County $1,126, across the Missouri River from each other; McKenzie County",
     "Mandan's Morton County $1,126; McKenzie County"),
    # A1-6e (#economy): a conclusion across six county values, none printed in the sentence (I60b)
    ("north-dakota.html",
     " The table makes one point plainly: a wage assumption copied from the statewide average is wrong almost everywhere a project is likely to sit.",
     ""),
    # A1-4 (#supply): NON-DELETION, restoration of the article's own label (MT-NORTH-DAKOTA line 78: "article labels series metro-level")
    ("north-dakota.html",
     "<span data-fsc-nocount>71</span> in Bismarck in August 2025, the peak there [^38]",
     "<span data-fsc-nocount>71</span> in the Bismarck metro area in August 2025, the peak there [^38]"),
    # A2-14 (#programs): the USDA eligibility rule is uncited and differs from the served USDA page (population test against the current designation)
    ("north-dakota.html",
     "USDA Rural Development's guarantees turn on where the site is: eligibility is a parcel test against the agency's map on the application date, and the study runs it before anything else.",
     "USDA Rural Development's guarantees turn on where the site is."),
    # A2-5 (#programs): EB-5 rule stated without a source and against the served EB-5 page (the EB-5 question is employment; the area sets the minimum)
    ("north-dakota.html",
     "An EB-5 offering rests on two things a study must document: the jobs its spending creates, by an accepted model, and the designation of the area the site lies in. ",
     ""),
    # A2-19 (#cases lede): NON-DELETION. The served case pages call their sites, sponsors and projects hypothetical, not "modeled on a project"
    ("north-dakota.html",
     "Every case on this site was modeled on a project outside North Dakota, and no North Dakota case is scheduled.",
     "No case on this site is set in North Dakota, and none is scheduled."),
    # A2-19 (#cases): the "method carries, inputs do not" move and the "a North Dakota version would replace the wage line" move are Vermont's, Alaska's and DC's plan
    ("north-dakota.html",
     "The method carries across state lines even though the inputs do not. The <a href=\"/case-studies/\">case studies</a> include",
     "The <a href=\"/case-studies/\">case studies</a> include"),
    ("north-dakota.html",
     " A North Dakota version of any of them would replace the wage line with its county's figure from the economy section and the demand line with the rig, airport or household series for its market.",
     ""),
    # A2-17 (closing band): NON-DELETION (capital T). 7-word run shared with the DC draft
    ("north-dakota.html",
     "A study commissioned now is written to those releases as they stand on its date, and the first exchange settles the analytical framework",
     "The first exchange settles the analytical framework"),
    # A2-7 (#metros cards)
    ("north-dakota.html",
     "A Red River city whose airport",
     "A city whose airport"),
    # A1-6d + A2-6 (#metros card): "far apart" is a comparison with no values; the Missouri is uncited
    ("north-dakota.html",
     "The capital and Mandan across the Missouri, two counties whose wage files sit far apart.",
     "The capital and Mandan."),
    # A2-7 (#metros cards)
    ("north-dakota.html",
     "A second Red River county, read",
     "A second county, read"),
    # A2-9 + A2-13 (#metros card): Stark County in the oil field has no record; "little else published" is not shown (the research holds Stark rows beyond payroll and wage)
    ("north-dakota.html",
     "The southwestern oil county, with a county payroll and wage and little else published.",
     "The southwestern county, with a county payroll and wage."),
    # A2-8 + A2-7 (#metros h2)
    ("north-dakota.html",
     "Six North Dakota markets, from the Red River to the Montana line, each with a section below.",
     "Six North Dakota markets, each with a section below."),
    # A2-7 (#fargo h2 and first paragraph)
    ("north-dakota.html",
     "and September listings, all on the North Dakota bank of the river.",
     "and September listings."),
    # A2-7 (#fargo): NON-DELETION
    ("north-dakota.html",
     "the brokers' Fargo-Moorhead reports cover both banks of the Red River; none",
     "the brokers' Fargo-Moorhead reports cover both states; none"),
    # A1-6c (#fargo): comparison in words, values not in the sentence
    ("north-dakota.html",
     " A listing count higher in September than in May is a signal that a study of homes for sale or rent checks against closed sales before it prices units.",
     ""),
    # A2-6 (#bismarck-mandan h2)
    ("north-dakota.html",
     "Bismarck and Mandan: two counties across the Missouri, airport records",
     "Bismarck and Mandan: two counties, airport records"),
    # A1-8 + A2-11 (#bismarck-mandan first paragraph): the Bismarck metro composition is uncited
    ("north-dakota.html",
     " BEA's and FHFA's Bismarck metropolitan area reaches beyond those two counties, so the two figures here that describe the wider area say so.",
     ""),
    # A1-6b (#minot): comparison in words, values not in the sentence
    ("north-dakota.html",
     " Three readings, each below the one before, are a reason to test asking prices against recorded sales before a for-sale or rental study relies on either.",
     ""),
    # A2-11 + A2-8 (#williston first paragraph): McKenzie's metro status and the Montana line are uncited; the Montana link is not earned by a fact (the neighbour list still links Montana)
    ("north-dakota.html",
     ", whose seat is Watford City and which has no Census metropolitan or micropolitan area of its own. Both counties lie on the Montana line; nothing from the Montana side is counted here, and the <a href=\"/states/montana/\">Montana</a> page reads that state's markets.",
     ", whose seat is Watford City."),
    # A1-6a (#williston): NON-DELETION. "rose" compares two rig counts that are not in the sentence
    ("north-dakota.html",
     "and rig counts that rose between July 13 and August 19, 2026 [^1]",
     "and the rig counts of July 13 and August 19, 2026 [^1]"),
    # A2-9 (#dickinson): Dickinson's place in the oil field and "the series apply to it as they apply to Williston" have no record
    ("north-dakota.html",
     "Dickinson sits in the southern part of the oil field, so the production and rig series in the <a href=\"#bakken\">oil and gas section</a> apply to it as they apply to Williston. ",
     ""),
    # A2-20 (FAQ 2): NON-DELETION (capital letters). Sentences repeated from #bakken
    ("north-dakota.html",
     "No, because it describes the field after the crews have moved on. The Department",
     "No. The Department"),
    ("north-dakota.html",
     "Rigs and completion crews are a mobile workforce, so a lodging, RV park or workforce rental study ties",
     "A lodging, RV park or workforce rental study ties"),
    # A2-20 (FAQ 4): argument repeated from #costs
    ("north-dakota.html",
     " A statewide average copied into either carries the error into every year of the projection and into the debt service coverage test.",
     ""),
    # A2-20 (FAQ 7): argument and a whole sentence repeated from #minot
    ("north-dakota.html",
     ", a city that held level while the bedroom towns around it grew. The new households",
     ". The new households"),
    ("north-dakota.html",
     " On the payroll side, BLS's county file lists 30,481 insured jobs in Ward County for March 2026 and an average of $1,234 a week in first-quarter pay [^8], the county's dated inputs for a sales or staffing line.",
     ""),
    # A2-21 (FAQ 1): NON-DELETION. Question and answer frames shared with South Dakota (7-word run) and Alaska (7-word run); the closing three-facts sentence repeats the in-body CTA
    ("north-dakota.html",
     "Who hires a North Dakota feasibility study consultant, who reads the study, and what does Feasibility Study Company ask for before starting?",
     "Who hires a North Dakota feasibility study consultant, and who reads the study?"),
    ("north-dakota.html",
     "The studies Feasibility Study Company prepares are independent and lender-grade, written for a bank's credit committee",
     "Each study is independent, lender-grade work written for a bank's credit committee"),
    ("north-dakota.html",
     "; the programs work through the lender making the loan, so the coverage test runs with the buydown and without it. A first message with three facts, the project, the county of the site and where the money is expected from, gets back the analytical framework, the deliverable that program wants and the order of work from there.",
     "."),
    # A1-10 (stats band): the unit letter doubles the label's first word ("3.58B" above "Billion cubic feet")
    ("north-dakota.html",
     "\"num\": \"3.58\",\n      \"unit\": \"B\",\n",
     "\"num\": \"3.58\",\n"),
]
