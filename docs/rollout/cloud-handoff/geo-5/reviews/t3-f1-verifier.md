# GEO-5 t3 freeze 1, verifier (cold, Sonnet): /states/south-dakota/

Source sha256 68eb5362... equals FREEZE-t3-f1.txt and the copy's src/pages/states/south-dakota.html. Headline numbers re-derived with pagecheck.py --figures in the copy: 6,722 body words, 107 counted (research 98, register 9/9): CONFIRMED. draftcheck on the draft: 97 counted (3 shared, 9 markers), overlap max 0.51% (Nashville). Baseline sameness: no non-exempt shared 8-word prose run (all runs are register labels, sba marker text or SOP name).

Sources opened by me (WebFetch, none refused): LMIC October 2026 occupational demand; SiouxFalls.Business ?p=174122 and ?p=185065; LMIC Rapid City MSA QCEW table; SD Tourism release; SDHDA awards release; ESMIS Crop Production page. Research and data/regulatory/sba.json read in the copy.

## Attacker one

- A1-1 REFUTED. The source says openings are "employment growth and the need for replacement workers due to separations", and separations include occupational transfers and labor force exits. The page names the same three parts and prints no component value and no arithmetic.
- A1-2 CONFIRMED MAJOR-FACTUAL. Source: "A one-bedroom averages $1,002". Page says "an average rent". Edited (two places).
- A1-3 CONFIRMED MAJOR-FACTUAL. The only caution in ?p=185065 is "somewhat hard to compare with one year ago, when 20,000 units reported", about January 2025, not the July 2025 survey set beside it. Edited (two places).
- A1-4 CONFIRMED MAJOR-FACTUAL (same as A2-3). The LMIC table names no counties; Pennington 62,445 + Meade 9,178 + Lawrence 13,694 exceeds the MSA's 74,312. Edited.
- A1-5 CONFIRMED MAJOR-FACTUAL (same as A2-5). Research row says only "Custer, Fall River and Pennington counties"; adjacency is uncited and Fall River does not border Pennington. Edited.
- A1-6 CONFIRMED MINOR. The release ties $406.1 million of state and local tax revenue to "16.5% of all state sales tax collections"; the page's compression follows the Department's framing and the research label. Verdict only.
- A1-7 CONFIRMED MINOR ("counted two ways" with one vintage left). Verdict only.
- A1-8 CONFIRMED MINOR (source 21 "Vintage 2024" is the researcher's inference). Verdict only.
- A1-9 CONFIRMED MINOR ("including" is an inference; the release lists $4.19 million among amounts the developments received). Verdict only.
- A1-10 CONFIRMED MINOR (the "small sample" note is the researcher's, not FRED's). Verdict only.
- A1-11 CONFIRMED MINOR (FHFA and BEA figures carry no boundary label). Verdict only.
- A1-12 CONFIRMED MINOR, record only.

## Attacker two

- A2-1 CONFIRMED MAJOR-FACTUAL. ESMIS lists upcoming releases Nov 10 2026 and Dec 10 2026; no research row says the October forecast stands until an annual summary. The band cannot cite. Three deletions (h2, cta.p first sentence, FAQ 2 last sentence). Body line "a study dated after January cites the annual summary" stays (true as written).
- A2-2 CONFIRMED MAJOR-FACTUAL. The release counts visitors "to and within" the state and gives no origin. Deletion.
- A2-3 CONFIRMED (see A1-4).
- A2-4 CONFIRMED MAJOR-FACTUAL. sba.json: sba_504_new_or_special 15% ("New Business ... or Limited or Special Purpose Property"), sba_504_new_and_special 20%; the special_purpose_list has hotels but no campgrounds. The sentence mis-states the rule. Clause deleted (marker outside the count).
- A2-5 CONFIRMED (see A1-5).
- A2-6 CONFIRMED MINOR as to FAQ 7 (its rewording is clean). The #capital clause "written to the program's requirements" CONFIRMED to read as an SBA requirement (ruling 8): edited. The remaining "every figure traced to a dated source like those above" is left (no edit in scope); the band's "that program" has no antecedent after the A2-1 deletions: MINOR, verdict only.
- A2-7 CONFIRMED MINOR (504 loans "from SBA lenders"). Verdict only.
- A2-8 CONFIRMED MAJOR-NONFACTUAL (hero opens on the firm sentence; frame only). Verdict only.
- A2-9 CONFIRMED MAJOR-NONFACTUAL (description frame shared with Colorado and Vermont descriptions; frame only; no 8-word run). Verdict only.
- A2-10 CONFIRMED MAJOR-NONFACTUAL (client/reader split as in North Dakota; frame only). Verdict only.
- A2-11 CONFIRMED MAJOR-NONFACTUAL (closing move as in Virginia; frame only, no 8-word run). Verdict only beyond the A2-6 clause already removed.
- A2-12 CONFIRMED MAJOR-NONFACTUAL (question frames with Wyoming, Vermont, Alaska). Verdict only.
- A2-13 CONFIRMED MAJOR-NONFACTUAL (band move; the Alaska half is gone with A2-1). Verdict only.
- A2-14 CONFIRMED MAJOR-NONFACTUAL (#cases frame). Verdict only.
- A2-15 CONFIRMED MINOR (USDA map rule uncited; no research row). Verdict only.
- A2-16 CONFIRMED MINOR (McCook and Turner unnamed). Verdict only.
- A2-17 CONFIRMED MINOR (Iowa link weakly earned). Verdict only.
- A2-18 CONFIRMED MINOR (no landing requests). Verdict only.
- A2-19 CONFIRMED MINOR (three claims with no source). Verdict only.
- A2-20, A2-21 CONFIRMED MINOR. Verdict only.

## Tally

Confirmed: BLOCKER 0; MAJOR-FACTUAL 7 distinct (A1-2, A1-3, A1-4=A2-3, A1-5=A2-5, A2-1, A2-2, A2-4); MAJOR-NONFACTUAL 7 (A2-8 to A2-14, no edit); MINOR 18 (incl. record-only A1-12). Refuted: A1-1 (1).
Shared 8-word prose runs confirmed: 0 (none exist before or after).

## Edits: 11 (file t3-f1-verifier-fix.py), each old text occurs once

After applying to ~/Downloads/fsc-rollout/tmp/geo-5/verify-t3/south-dakota.html: draftcheck --figures --promised: 97 counted (3 shared, 9 markers), 6,618 words, overlap max 0.51%, 0 problems. sameness: 937 shared-run lines, identical to the baseline (all register labels, sba marker text, SOP name), 0 non-exempt prose runs. pagecheck counts: no counted value removed (107 = research 98 + register 9 expected unchanged).
