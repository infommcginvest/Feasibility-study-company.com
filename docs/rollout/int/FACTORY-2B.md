# FACTORY-2B (integrator fixes for the lanes' notes, 18 October 2026)

Cut from `main` at `57a5ae3` (FACTORY-2, live as deploy `6ad4160a4c493e9e48468f7e`). Integrator-owned files only; no page's words change, and the chain over the whole tree leaves every served file byte-identical.

| Note | Fix | Files |
|---|---|---|
| geo-3-2, asset-4-1 (first part) | `build.py` renders through `links.py`'s relink step, so render and relink agree before and after a promised page lands (DECISIONS I18). | `scripts/build.py`, `scripts/links.py` |
| geo-3-1 | Already fixed in `scripts/qa/pagecheck.py`; `build.py` checks site-market markers clean (I19). | none |
| asset-3-1 | Screenshot limits raised (I21). | `scripts/qa/shots.mjs`, `scripts/qa/gates.py` |
| geo-2-1 | Public BEA landing page on the three BEA series (I20). | `data/markets/sources.json` |
| method-1-1 | Practice, framework and note types and their house partials; framework byline; promised notes in the mesh (I22). | `src/types.json`, `src/templates/partials/house-*.css`, `scripts/build.py`, `scripts/byline.py`, `scripts/mesh.py`, `data/mesh/topics.json` |
| geo-3-3 | Gate 13 tests overflow against the emulated width (I24). | `scripts/qa/shots.mjs` |
| geo-1-1 | Rescaled stats-band repeats count once; geography counts and `data-fsc-nocount` values are not counted (I25). | `scripts/qa/pagecheck.py` |
| asset-4-1 (second part) | Re-key at the landing that ships the meat processing hub (I23). | later |

Tests, in a throwaway copy of this commit:
- the chain over the whole tree: 0 served files changed; every `--check` exits 0;
- a source linking the promised `/states/michigan/detroit/` and carrying a pending link to `/asset-classes/build-to-rent/`: the chain renders both pending and `build.py --check` passes; after a page appears at `/asset-classes/build-to-rent/`, the next chain renders that link live and `build.py --check` and `links.py --check` pass;
- a framework child at `/analytical-framework/market-area-definition/` on a test template: house partial `871ce15e`, byline and signature in place, its own fragment links intact, every check green, and `/analytical-framework/`'s two pending links to it now live.

Gates: `docs/rollout/int/GATES-factory-2b.txt`.
