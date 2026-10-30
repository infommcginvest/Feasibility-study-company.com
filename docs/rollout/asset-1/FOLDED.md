# ASSET-1 folds

Ruling 6 and amendment A6: a subtype is written as a page only when its pre-count reaches 30 dated, sourced figures of its own that no other served page shows, at least 20 of them from research (a subtype carries no register class of its own, D6). Under that, it becomes a section of its hub with `id` equal to the slug, the slug stays a pending link, and the lane's requests carry a `folded` entry so every link to the section stays a pending link to the promised page. Fact sheets and pre-counts are kept outside the repo in `~/Downloads/fsc-rollout/drafts/asset-1/facts/<hub>/`.

## Hotel (`/asset-classes/hotel/`, tranche 1)

Pre-count: Sonnet reader on AH-HOTEL-A, AH-HOTEL-B and SD-HOTEL with `figcheck.py` against the served site on 16 October 2026 (D12; strict dates). Re-check: FSC-NIGHT-1, 21 Oct, every fact-sheet figure keyed by `scripts/qa/pagecheck.py` against the served pages of local `main` at `4cf7b58`, with the year-only and period-only dates D14 accepts added back (D19). FREE counts unique values; figures from named real financings are included, so the counts are an upper bound on what a page of its own could carry.

| Hub | Subtype slug | Promised | FREE at pre-count (16 Oct) | FREE at re-check (21 Oct) | Verdict |
|---|---|---|---|---|---|
| hotel | boutique-and-independent | yes | 1 | 0 | FOLD (section #boutique-and-independent) |
| hotel | extended-stay | yes | 3 | 5 | FOLD (section #extended-stay) |
| hotel | full-service | yes | 4 | 7 | FOLD (section #full-service) |
| hotel | limited-service | yes | 2 | 2 | FOLD (section #limited-service) |
| hotel | resort | yes | 9 | 10 | FOLD (section #resort) |
| hotel | select-service | yes | 7 | 6 | FOLD (section #select-service) |
| hotel | upper-upscale-and-luxury | yes | 8 | 6 | FOLD (section #upper-upscale-and-luxury) |

The four hub-level strays that ruling 16 rewrites to these subtypes (`/asset-classes/limited-service-hotel/`, `/asset-classes/select-service-hotel/`, `/asset-classes/extended-stay-hotel/`, `/asset-classes/boutique-and-resort/`) follow the rewrite to the pending subtype, whose fallback is now its section; requests `asset-1-9` to `asset-1-12` also point the strays' own fallbacks at those sections.
