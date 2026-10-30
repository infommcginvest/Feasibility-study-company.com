# C0 pre-count reader brief (CASE-NEW-1)

You pre-count cases. Read only; write only precount/<slug>.tsv files in this folder. No prose output beyond one line per case: `<slug> counted=N research=N register=N verdict engine=Y/N`.

Repo (read only): ~/Downloads/wt-rollout-case-new-1. Research inventory: ~/Downloads/FSC Deep Searches 2/ (find a case's file with `ls` and grep on its town or the CS-R / CS-N / EXTRA name; MANIFEST.tsv column 4 gives a path for some). Earlier fact sheets and 16 Oct pre-counts (stale: made before the rulings below) sit at the path in MANIFEST.tsv column 3 (facts.tsv, precount.txt, or a .md). Use them only as a map to the research rows; re-judge every figure under the rulings. Read a research file with line ranges or grep; never print a whole large file. Do not read other lanes' transcripts.

## Counting rules (all must hold for a figure to count)
- Market figure with its own value, period and source (ruling 5). A counted figure appears on no other served page by value; rounded and rescaled repeats are the same figure. Counts of the page's own sections, `sba:` and `case:` values do not count.
- Dated, sourced, case-specific. Dated = the research ties it to a publication/release/filing/effective date, an edition year in the document title, or the reporting period of a periodic document that identifies it (I77). A date found only by our own or the researcher's fetch/retrieval does not date it (I69, I106). A page saying "2025 data" with no periodic document does not date it. "Current" or undated: not countable (I86).
- Single-property attributes (the subject's size, units, acreage, price, listing figures, its loan or financing, I64, I66) do not count. A portfolio or market total still counts.
- The subject's own listing figures, program rules (SBA/USDA/HUD rule values), NOT FOUND rows, analyst assumptions and a research file's own summary counts do not count.
- Two rows with the same value count once.
- Register figures: at most 10, and only ones you can name (data/ file and key, or a state/metro page already served). If you cannot name them, 0.
- Floors: 30 counted in total and 20 from research (ready stage). Verdict PAGE if counted>=30 and research>=20 with the figures all dated; otherwise FOLD (say what is short in the notes column).
- Engine: engine=Y if the program is not one of sba_7a, sba_504, usda_bi, hud_232 (eb5, bridge, conventional, dscr, agency) or the case needs a computed return; otherwise N.
- Real-subject research files get hypothetical subjects only; count market figures, not the subject's.
- Never name or cite Wert-Berater or the owner's sister properties. No em dashes in anything you write.

## Output per case: precount/<slug>.tsv, tab separated, header row:
fig_id  value_token  figure_short  class(research|register)  date_basis(I77a|I77b|I77c|none)  source_publisher  research_ref(file:line or row id)  counts(Y|N)  why_not
List every candidate figure (counted or excluded with the reason), value_token being the number exactly as it would print (e.g. 14,161 or 4.4%). Last line of the file: `#SUMMARY slug counted=N research=N register=N verdict=PAGE|FOLD engine=Y|N notes=...` (notes under 20 words).
