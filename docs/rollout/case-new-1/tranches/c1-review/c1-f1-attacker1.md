# CASE-NEW-1 tranche c1, freeze 1: Attacker 1 (numbers)

Scope: the six frozen pages in `N/copies/c1/` (freeze record FREEZE-c1-f1, gates 13/14). Read only; scratch work in `N/reviews-c1/a1-work/`.

## What I ran

- `python3 scripts/casemodel.py --case <slug>` inside the copy for all six (outputs `a1-work/model-<slug>.txt`); `casemodel.py --check`: 28 cases, 0 problems.
- `scripts/qa/pagecheck.py --stage ready --figures` on the six URLs (`a1-work/figures.txt`): the counted list per page.
- My own checks (`a1-work/nums.py`, `srccheck.py`, `citecheck.py`, `orphan.py`, `mktcheck.py`, `probe.py`):
  - every block that prints a number outside `case:`, `sba:` and `mkt:` markers, listed per case;
  - every number in a cited block matched against the research rows (`geo-5/facts/*.facts.json`) whose URL is one of that block's cited sources;
  - every sources entry matched by URL against the research rows (publisher, verbatim title, publication date);
  - every `mkt:` marker looked up in `data/markets/series/*.json` through `scripts/markets.py`'s own `lookup`;
  - engine probes with inputs overridden.

## Re-derivation summary

**Research figures.** Every counted research figure on all six pages traces to a research row with the same value, period, publisher, verbatim title, publication date and URL. The only mismatches are the findings below. Some examples, at least four per case:

- **Chesapeake**
  - 832.9 thousand jobs: MT-VIRGINIA line 127, Sep 2026 preliminary, BLS metro table, listed Oct 2026.
  - 105,954 covered jobs: line 136, Mar 2026, BLS QCEW Q1 2026, 2026-09-02.
  - $487,250 median listing price: line 146, FRED relaying Realtor.com, 2026-10-01.
  - 4,892,594 ORF passengers: line 162, AviationPros, 2026-01-15.
  - 10.62 cents per kWh and 138,044,772 MWh: ST lines 79 and 78, EIA, 2025-11-10.
  - 8.88 million residents: ST line 10, Cooper Center, 2026-02-24.
  - 127,459.149 million GDP: line 149, FRED, 2024-12-04.
- **Jackson**
  - 3,800,648 Grand Teton visits: MT-WYOMING line 129, NPS, 2026-03-13.
  - 598,923 enplanements and 83,388 in July: lines 128 and 127, News&Guide, 2026-09-02.
  - 23.333 thousand residents: line 122, FRED, 2026-03-27.
  - 4,762,988 Yellowstone visits: ST line 116, NPS, 2026-03-17.
  - 4,143, 2,668 and 2,174 jobs: ST-WYOMING-2 lines 12 and 13 and ST line 33, BLS BED, 2026-07-31.
  - $10,095,202.90 lodging tax: line 137, Buckrail, 2024-02-01.
- **Fargo**
  - 126,659 covered jobs and $1,376 weekly wage: MT-NORTH-DAKOTA rows 9 and 10, BLS, 2026-09-04.
  - 590,542 boardings: row 32, Inforum, 2026-01-23.
  - 14,875,063 real GDP: row 11, FRED, 2026-02-05.
  - 447.3 and 448.7 thousand jobs: ST rows 5 and 6, BLS, 2026-10-20.
  - $10.7 billion and 4.69%: ST rows 17 and 19, Bank of North Dakota, 2026-06-29.
- **Anchorage**
  - 289,221 residents: MT-ALASKA line 12, DOLWD.
  - 3.82 million tonnes: line 45, Alaska Business, 2026-01-30.
  - 145,080 jobs and $1,579 weekly wage: lines 22 and 23, BLS, 2026-09-04.
  - 30,293, 23,914 and 6,379 jobs: ST lines 48 to 50, BLS BED, 2026-08-19. The arithmetic holds.
  - 738,737 residents, +1,649, 3,389 and 1,740: ST lines 11 to 14, 2026-01-28. The arithmetic holds.
- **Sioux Falls**
  - 224,676 residents: MT-SOUTH-DAKOTA row 1, SDPB, 2026-01-14.
  - $1,327,437,573 and 5,615: rows 2 and 3, City permit statistics.
  - 754,686 enplanements and 46,696,248 lbs: rows 31 and 32, airport 2025 statistics, a periodic document.
  - 6.62% of 14,409 units, 954 vacant: row 23, 2026-03-16.
  - $66,768 and $41,028: ST-2 row 39, DLR 2025 QCEW report.
  - 470,500 jobs: ST row 7.
- **Colorado Springs**
  - 94.4%, $1,457, 1,319 and 369: MT-COLORADO rows 88 to 91, CBRE, 2026-08-11.
  - $17.67, down 4.3%, Class A $21.14: row 86.
  - 301,647 and $1,437: rows 75 and 76, BLS, 2026-09-04.
  - 25.6 million visitors and $3.1 billion: rows 96 and 97, Visit Colorado Springs, 2026-05-28.
  - 6,012,561 residents, -12,100, 15,356 and 3,256: ST rows 1 to 6, DOLA, 2026-01-27.
  - $18,085,922, 185 loans and $97,762: ST rows 70, 71 and 73, Colorado Enterprise Fund, 2025-12-03.

**Dating.** No printed figure rests on a fetch date. Every source maps to a research row with a publication or release date, an edition year or a periodic release's period. Secondary rows are labelled as relays.

**Single-property figures.** These sit in nocount: Chesapeake $450 million and the rail expansion; Sioux Falls "more than $42 million"; Anchorage Port MacKenzie. The Chesapeake port capacity and the Anchorage LNG workforce are counted, which matches how the GEO-5 readers graded them.

**Register.** All 82 `mkt:` markers equal the register for their geography, series and class, including the flags, the `allow_flag` lower bounds and the proxy or partial fit.

**Model.** The glance, uses, sources, loan, pro forma, DSCR, determination, verdict, break-even and sensitivity tables all render from the engine (build.py --check 0 out of date). Engine results:

| Case | Proposed | Restructured | Y2 / Y3 DSCR | Break-even cushion | Sensitivity range |
|---|---|---|---|---|---|
| Chesapeake | 10% equity, Y2 0.75x, fails coverage | 42.2% | 1.15x / 1.57x | 6.8% | -0.81x to 4.30x |
| Jackson | 10%, fails the 15% tier and coverage (0.74x) | 42.2% | 1.15x / 1.73x | 29.9% | 0.48x to 1.93x |
| Fargo | 10%, fails the 20% tier and coverage (0.76x) | 40.7% | 1.15x / 1.29x | 5.2% | -0.42x to 2.98x |
| Anchorage | 15%, fails the 20% tier and coverage (0.81x) | 40.5% | 1.15x / 1.74x | 21.1% | 0.29x to 1.79x |
| Sioux Falls | 10%, fails the 15% tier and coverage (1.08x) | 15.5% | 1.15x / 1.50x | 10.6% | -0.13x to 2.65x |
| Colorado Springs | 10%, fails coverage (0.91x) | 28.7% | 1.15x / 1.15x | 20.7% | 0.84x to 1.45x |

The prose determinations match the engine except where the findings below say otherwise. Land is a round, labelled assumption in all six cases (the Fargo label text contradicts its own value: A1-2).

## Findings

### A1-1 BLOCKER: Sioux Falls, tuned inputs

**Case:** auto-dealership-sioux-falls-south-dakota-sba

**Quoted text:**
- Page: "the model supports it at 15.5% , at the floor".
- Inputs: `"bldg_sf": 14000`, `"bays": 6`, `"fte": [12, 16, 18, 19, 19]`, `"used_units": [440, 640, 740, 790, 810]`, `"tpl_rate": 0.0725`.
- `used_units` reasoning: "The ramp is an assumption: the store sells to customers who today buy from the dealer establishments the competitor section counts for the metro area [^22], so the model builds slowly and stabilizes in Year 3."

**Reproduction:**
- I compared the writer's first-draft engine output (`cases/<slug>/work/out.json`, 14:10) with the frozen model.
- What changed between the two:

  | Input or result | First draft | Frozen |
  |---|---|---|
  | Building | 18,000 sq ft | 14,000 sq ft |
  | Bays | 8 | 6 |
  | Year 3 staff | 21 FTE | 18 FTE |
  | Land | $1,400,000 | $1,200,000 |
  | Site | 3.0 acres | 2.5 acres |
  | Used vehicles, Year 3 | 680 | 740 |
  | Total project cost | $7,015,396 | $5,841,819 |
  | Year 2 DSCR at 10% equity | 0.31x | 1.08x |

- The draft failed at every equity share. The bank's fixed half of cost alone needed more than the draft's Year 2 NOI of $169,901.
- notes.md says the first draft "failed at every equity share, so the building, staffing and ramp were reduced to a self-consistent store".
- No input gained a source between the two drafts. Volume rose 9% while the building fell 22%, the bays 25% and the staff 14%. That is the opposite direction a reasoned resize would take.
- The bank rate is Prime plus 0.25 for a start-up. The other five cases use Prime plus 0.5.
- The result lands half a point above the 15% tier, at a Year 2 DSCR of 1.151x.
- The page does not disclose the resize.
- Verdict: the inputs were reverse-engineered, not reasoned.
- Probe: the frozen store with volume scaled back to the draft's 680 in Year 3. The engine then restructures at 40.3% equity, Year 2 1.15x.

**Smallest fix:** Restore the first draft's volume ramp (680 in Year 3), or the whole first-draft store. Let the engine set the determination and write the page to it; a negative determination is acceptable house practice. Set the bank rate to Prime plus 0.5, or give a reason for 0.25.

### A1-2 BLOCKER: Fargo, the inputs table states values that contradict the engine

**Case:** brewery-fargo-north-dakota-sba

**Quoted text** (rendered Model Inputs table):

| Input | Value the engine uses | What the reasoning text says |
|---|---|---|
| Land | 2.0 | "A round hypothetical site of about two and a half acres" |
| Barrels | 1,800 / 2,700 / 3,200 / 3,500 / 3,700 | "The study ramps a newcomer to 1,800 barrels in Year 3 and 2,050 by Year 5" |
| Production staff | 4.0 / 5.0 / 5.0 / 5.5 / 5.5 | "at 4 full-time equivalents by Year 3" |
| Taproom staff | 7.0 / 9.0 / 10.0 / 10.0 / 10.0 | "needs about nine by Year 3" |

**Reproduction:** I read the rendered `case-studies/brewery-fargo-north-dakota-sba/index.html` against `data/cases/<slug>.json`. In each row the reasoning text contradicts the value beside it, and the engine computes on the values. `case.tpl.json` already held these values, so the reasoning was never synced to them. Note that the land label is also not the round figure the model uses.

**Smallest fix:** Delete the numbers from the four reasoning strings:
- "A round hypothetical site: room for ...".
- "The study ramps a newcomer to its stabilized volume by Year 3, a modest ramp ...".
- "The study staffs a production hall of this size at a planning level."
- "A taproom open most evenings and weekend afternoons."

### A1-3 MAJOR-FACTUAL: Fargo, prose misreads Year 3 values as opening or five-year values

**Case:** brewery-fargo-north-dakota-sba

**Quoted text:**
- "The model opens at {{case:v.in_barrels}} barrels over the five years, with Year 3 at the stabilized level." This renders as "opens at 3,200 barrels".
- "Payroll is the largest line: {{case:v.in_prod_fte}} production and {{case:v.in_tap_fte}} taproom full-time equivalents over the five years". This renders as 5.0 and 10.0.

**Reproduction:** The `in_` values render the Year 3 element of each array. Year 1 is 1,800 barrels, 4.0 production FTE and 7.0 taproom FTE.

**Smallest fix:**
- "The model reaches {{case:v.in_barrels}} barrels in Year 3, the stabilized level."
- Replace "over the five years" with "in Year 3".

### A1-4 MAJOR-FACTUAL: Fargo, airport records misstated

**Case:** brewery-fargo-north-dakota-sba

**Quoted text:** "In June 2026 it set a monthly record of 50,959 [^22] and in September 2026 another of 49,464 [^10]."

**Reproduction:** MT-NORTH-DAKOTA row 34 calls 50,959 a "June record" (prior June record 47,898). Row 33 calls 49,464 a "September record" (prior September record 46,258). A September count below June's cannot be another monthly record.

**Smallest fix:** "In June 2026 it set a June record of 50,959 [^22] and in September 2026 a September record of 49,464 [^10]." This uses the research's words.

### A1-5 MAJOR-FACTUAL: Fargo, a program rule typed by hand that contradicts sba.json

**Case:** brewery-fargo-north-dakota-sba

**Quoted text** (debenture_years reasoning, rendered in the inputs table): "A mixed project of real estate and equipment would carry a 25-year real-estate part and a 10-year equipment part, which the single-term model blends."

**Reproduction:** `data/regulatory/sba.json` `terms.sba_504_maturities` note: "with both, the maturity follows the asset category that is the majority of loan proceeds". Per the engine's uses, real estate is 61.9% of cost.

**Smallest fix:** Delete the sentence.

### A1-6 MAJOR-NONFACTUAL: Fargo, SBA tiers typed outside sba markers

**Case:** brewery-fargo-north-dakota-sba

**Quoted text:** "and it changes the minimum between 15% and 20%."

**Reproduction:** These are the tiers `equity.sba_504_new_or_special` and `new_and_special`, typed without markers.

**Smallest fix:** Wrap them in their `sba:` markers, or delete "between 15% and 20%".

### A1-7 MAJOR-NONFACTUAL: Fargo, the counted figures are inflated

**Case:** brewery-fargo-north-dakota-sba

**Quoted text:**
- "$14,875,063 thousand" (prose) and the table row "14,875,063".
- "20,535.575 million dollars" and "20,535.575".
- "65,268.3 million" and "65,268.3".
- "at least five establishments and 101 employees in the metro area [^5]".
- Also typed: "90 paid employees" and "totaling $1,126,000 [^26]".

**Reproduction:**
- pagecheck `--figures` lists each of the three rescaled pairs as two research figures. Ruling 5 says a rescaled repeat is the same figure.
- 101 is the register value `cbsa-22020.cbp_emp.brewery-and-distillery`, typed outside its marker and counted as research.
- The research count is therefore 30, not 34.

**Smallest fix:**
- Wrap 90, 101 and $1,126,000 in their `mkt:` markers (with `allow_flag` as in the table), or delete them.
- Record the true count. No other text change is needed.

### A1-8 MAJOR-FACTUAL: Jackson, arithmetic implied by the sentence is wrong

**Case:** event-venue-jackson-wyoming-sba

**Quoted text:** "Private-sector openings created 4,143 jobs in the fourth quarter of 2025 while closings removed 2,668, a net private-sector gain of 2,174 jobs [^23]."

**Reproduction:**
- 4,143 is the gross job gains at opening establishments (ST-WYOMING-2 line 12).
- 2,668 is the losses at closing establishments (line 13).
- +2,174 is the private-sector net change over all establishments, including expansions and contractions (ST-WYOMING line 33).
- 4,143 - 2,668 = 1,475, so the sentence implies arithmetic that does not hold.

**Smallest fix:** Replace ", a net private-sector gain of 2,174 jobs" with "; the private-sector net job change for the quarter, which also counts expanding and contracting establishments, was +2,174".

### A1-9 MAJOR-NONFACTUAL: Jackson, register values typed outside markers, one counted as research

**Case:** event-venue-jackson-wyoming-sba

**Quoted text:**
- "Teton County has 6.89 establishments per 10,000 residents in the proxy class, against 2.4 for Wyoming as a whole [^3]."
- "The class holds 81 paid employees across those 16 establishments [^3]."
- Risks: "The county's median home value is $1,633,900 [^2]".

**Reproduction:**
- The values equal the register: co-56039 per-10k 6.89, wy 2.40, cbp_emp 81, cbp_estab 16, acs5_median_home_value 1,633,900.
- They sit outside markers, so markets.py --check cannot guard them.
- pagecheck counts 6.89 as a research figure.

**Smallest fix:** Wrap each in its `mkt:` marker (event-and-wedding-venue with `{"fit": "proxy"}`). The table already carries these markers.

### A1-10 MAJOR-FACTUAL: Chesapeake, the sensitivity reading contradicts the engine

**Case:** industrial-warehouse-chesapeake-virginia-sba

**Quoted text:** "Gross margin is the sharper driver: a small change in the margin moves gross profit on every dollar of sales, while a change in accounts moves it only on the dollars those accounts bring."

**Reproduction:**
- The engine applies both steps as multipliers (`casemodel.py` sensitivity: input x (1 + step)).
- In the engine grid (Year 3), margin -10% / +10% gives 0.72x / 2.44x. Accounts -10% / +10% gives 0.73x / 2.42x. Per step the two drivers are equal.
- Across the matrix, accounts span -0.11x to 3.27x against 0.72x to 2.44x for margin.

**Smallest fix:** Delete this sentence and the next ("The operator's pricing power ... than the building does."), which rests on it.

### A1-11 MAJOR-NONFACTUAL: Sioux Falls, register values typed in an FAQ answer and counted as research

**Case:** auto-dealership-sioux-falls-south-dakota-sba

**Quoted text:**
- FAQ1: "3.02 against 3.43 per 10,000 residents [^22]".
- Body: "Six 504 loans and twelve 7(a) loans in ten years".

**Reproduction:**
- These are `cbsa-43620` and `sd` `cbp_estab_per_10k.auto-dealership`, and the `sd` sba504_loans and sba7a_loans values (6 and 12).
- pagecheck lists 3.02 and 3.43 among the 44 research figures.

**Smallest fix:** Use the `mkt:` markers with `{"fit": "partial"}`, or say "slightly fewer per resident" without the numbers.

### A1-12 MAJOR-NONFACTUAL: Colorado Springs, register values typed in prose and counted as research

**Case:** mixed-use-colorado-springs-colorado-sba

**Quoted text:** "The county holds 97,958 renter-occupied homes among its 742,999 residents [^28] ... The census median gross rent of $1,696".

**Reproduction:**
- The values equal the register for co-08041: acs5_renter_occupied, acs5_pop and acs5_median_gross_rent.
- They are outside markers, and pagecheck counts all three as research figures.

**Smallest fix:** Wrap each in its `mkt:` marker, as in the table above it.

### A1-13 MAJOR-FACTUAL: Colorado Springs, a register count misstated in words

**Case:** mixed-use-colorado-springs-colorado-sba

**Quoted text:** "the county holds just over a hundred establishments and a little over five hundred paid employees, and the metro area adds only a handful beyond the county line [^29]."

**Reproduction:** The table above it renders co-08041.cbp_estab.mixed-use as 137 and cbp_emp as 550. 137 is not "just over a hundred".

**Smallest fix:** Replace the words with the two `mkt:` markers (137, 550), or delete "just over a hundred establishments and".

### A1-14 MAJOR-FACTUAL: Anchorage, the jobs-standard arithmetic is not what the model shows

**Case:** cold-storage-anchorage-alaska-sba

**Quoted text:** "a small warehouse crew and drivers are the jobs the subject creates, and the debenture is small enough on the restructured loan to make that a light test."

**Reproduction:**
- Restructured debenture $1,255,499 / [SBA:$95,000] = 13.2 jobs.
- The model staffs 8 warehouse FTE and 2 drivers in Year 3, plus a $300,000 management payroll.
- That is about the requirement, not a light test.

**Smallest fix:** Delete everything after "[^23];" in that sentence.

### A1-15 MAJOR-FACTUAL: Anchorage, the working-capital reasoning misstates the engine

**Case:** cold-storage-anchorage-alaska-sba

**Quoted text** (inputs table): "Roughly four months of Year 2 operating cost to carry payroll and power while customers move in."

**Reproduction:** $450,000 against the engine's Year 2 operating cost of $2,011,864 is 2.7 months.

**Smallest fix:** "An allowance to carry payroll and power while customers move in."

### A1-16 MINOR: Anchorage, one measure counted twice

**Case:** cold-storage-anchorage-alaska-sba

**Quoted text:** "3.82 million tonnes ... [^8]" and "more than 3.85 million metric tons ... [^9]". Both are 2025 Anchorage air cargo.

**Reproduction:** The Alaska pre-count dropped MT 46 as "duplicate of MT 45". pagecheck counts both.

**Smallest fix:** No text change. Count one.

### A1-17 MINOR: model numbers typed by hand (all equal the engine today; the Lebanon TN exemplar does the same)

**Cases:** Chesapeake, Jackson, Anchorage, Colorado Springs, Sioux Falls

**Quoted text:**
- "the model uses a 25-year debenture and a 25-year bank amortization" (Chesapeake, Jackson, Anchorage, Colorado Springs).
- "assumed at 25 years" (Sioux Falls).
- "two drivers at" (Anchorage).
- FAQ question "Why does a 10% equity proposal fail?" (Sioux Falls).
- Glance "about 9,600 sq ft" (Colorado Springs).
- Uses labels "Land, about 4.5 acres", "Building, 60,000 sq ft" (Chesapeake) and "Building, 14,000 sq ft" (Sioux Falls).

**Reproduction:** Each equals the case input or a sum of inputs.

**Smallest fix:** Use `{{case:v.in_...}}` placeholders, or words without the number.

### A1-18 MINOR: glance determinations incomplete

**Cases:** Jackson, Fargo, Anchorage

**Quoted text:**
- Jackson and Fargo: "As proposed ({equity_proposed_pct} equity): fails the {floor} test, ..."
- Anchorage: "As proposed (...): see the coverage test. As restructured (...): see the coverage test".

**Reproduction:** The engine's `prop_tests` report the equity tier failing in all three, but the Jackson and Fargo glances name only coverage. The Anchorage glance states no determination.

**Smallest fix:** Use "fails the equity tier and the {floor} test" (as the Sioux Falls glance does). For Anchorage, use the same wording plus "meets it" for the restructured structure.

### A1-19 MINOR: Chesapeake, NOI wording

**Case:** industrial-warehouse-chesapeake-virginia-sba

**Quoted text:** "a deliberate choice that shows how thin the operator's margin is once growth in accounts ends."

**Reproduction:** Accounts rise 470, 495, 510 in Years 3 to 5, and NOI goes $891,688, $840,997, $870,815. Account growth never ends in the model.

**Smallest fix:** Delete the clause after "inflation".

### A1-20 MINOR: Chesapeake, the debenture rate reasoning

**Case:** industrial-warehouse-chesapeake-virginia-sba

**Quoted text:** "a little below the bank rate above because the debenture is sold at a fixed rate".

**Reproduction:**
- A fixed-rate sale does not imply a lower rate.
- 6.5% is below every sibling (6.75% to 7.0%).
- Probe: at 6.97% the engine restructures at 42.6% instead of 42.2%.

**Smallest fix:** Delete the clause and keep "a round planning rate".

### A1-21 MINOR: Jackson, two different measures compared

**Case:** event-venue-jackson-wyoming-sba

**Quoted text:** "Overnight visitors numbered 8.8 million in 2025 [^14], against 8.7 million visitors in 2024 [^15]."

**Reproduction:** ST-WYOMING row 57 is overnight visitors; row 58 is visitors.

**Smallest fix:** Replace "against 8.7 million visitors in 2024" with "; a separate report counted 8.7 million visitors in 2024".

### A1-22 MINOR: Fargo, attribution wording

**Case:** brewery-fargo-north-dakota-sba

**Quoted text:**
- "A broker survey puts metro apartment vacancy at 6.2%". The source is Appraisal Services, not a broker (MT-NORTH-DAKOTA row 29).
- other_pct reasoning: "The metro's leisure and hospitality workforce is large, 41.6 thousand statewide [^13]". This is a statewide series.

**Smallest fix:**
- "An appraisal firm's quarterly survey puts ...".
- "Statewide leisure and hospitality employment is 41.6 thousand [^13]".

### A1-23 MINOR: Colorado Springs, nocount on the wrong words

**Case:** mixed-use-colorado-springs-colorado-sba

**Quoted text:** "more than $8 million in hazard mitigation money for floodplain restoration on <span data-fsc-nocount>Cottonwood Creek</span> and more than $2.9 million for <span data-fsc-nocount>Monument Creek</span>".

**Reproduction:** MT-COLORADO row 99 marks these as single-project. The wrap covers the names, not the amounts.

**Smallest fix:** Move both spans onto "more than $8 million" and "more than $2.9 million".

### A1-24 MINOR: writer arithmetic in the inputs table (true, but not engine-computed)

**Cases:** Sioux Falls, Colorado Springs

**Quoted text:**
- Sioux Falls: "about $205 a sq ft before land".
- Colorado Springs: "about $130 a square foot of building" and "$1,250 sits about 14% below it".

**Reproduction:** 321,594 / 1,572 = 204.6; 1,250,000 / 9,600 = 130.2; 1 - 1,250 / 1,457 = 14.2%.

**Smallest fix:** Delete the derived numbers, or leave them as labelled reasoning if the integrator accepts writer arithmetic inside an assumption.

## Counts by severity

| Case | BLOCKER | MAJOR-FACTUAL | MAJOR-NONFACTUAL | MINOR |
|---|---|---|---|---|
| Chesapeake | 0 | 1 | 0 | 3 |
| Jackson | 0 | 1 | 1 | 3 |
| Fargo | 1 | 3 | 2 | 2 |
| Anchorage | 0 | 2 | 0 | 3 |
| Sioux Falls | 1 | 0 | 1 | 2 |
| Colorado Springs | 0 | 1 | 1 | 3 |

## Counted figures after my confirmed findings (gate figure, then mine)

I give the conservative reading: a value moved into a marker counts as register only where the gate already counted that pair.

| Case | Gate | After my findings | Why it changed |
|---|---|---|---|
| Chesapeake | 36 (28 research, 8 register) | 36 (28, 8) | No change. |
| Jackson | 35 (32, 3) | 34 (31, 3) | 6.89 is register, not research. If its marker pair counts: 35 (31, 4). |
| Fargo | 35 (34, 1) | 31 (30, 1) | Three rescaled repeats; 101 is register. If 101's pair counts: 32 (30, 2). One above the floor. |
| Anchorage | 35 (31, 4) | 34 (30, 4) | 3.85 million is a duplicate. |
| Sioux Falls | 54 (44, 10) | 52 (42, 10) | 3.02 and 3.43 are register; register is at the cap. The A1-1 fix does not change the count. |
| Colorado Springs | 48 (42, 6) | 45 (39, 6) | Three register values. Up to 48 (39, 9) if their pairs count. |

All six stay at or above 30 counted and 20 research at READY. Fargo has the least room.
