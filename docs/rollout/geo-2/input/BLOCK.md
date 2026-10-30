# ROLLOUT GEO-2: THE NORTHEAST: ELEVEN STATES AND THEIR METROS

Issued 16 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. Thirteen other roll-out sessions start at the same time. You never deploy: the integrator lands, deploys and submits your tranches. Index all: every page ships indexable.

## Your charter is the rulebook; this block is your assignment

Before anything else, fetch and check the rulebook:

```
git -C ~/Downloads/Feaisbility-Study-Company.com fetch origin
git -C ~/Downloads/Feaisbility-Study-Company.com show origin/main:docs/rollout/ROLLOUT-1.md > /tmp/ROLLOUT-1-geo-2.md
shasum -a 256 /tmp/ROLLOUT-1-geo-2.md
```

Fourteen sessions fetch at the same moment: if the fetch fails on a lock, wait a few seconds and retry it, up to five times. The hash must be `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (the rulebook as committed at `fb95856`). If it differs, stop and report the hash you got. Otherwise read all of that file (it is about 45,000 characters: read it with the Read tool in parts, not through shell output, which truncates) and follow it: step zero, the speed rules, the measured facts, rulings 1 to 17, the gates and the close. Nothing in this block relaxes it. Your lane id is `geo-2`: your branch is `rollout-geo-2`, your worktree `~/Downloads/wt-rollout-geo-2`, your tags `rollout/geo-2/t<n>`, your records `docs/rollout/geo-2/`, your gate 8 list `~/Downloads/fsc-rollout/private/dnu-geo-2.txt`.

The hard constraint, restated so it binds before you have read the rulebook: every figure traces to a dated source in the research files or the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. Nothing is invented, estimated past its source, or carried over from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition or a stated gap, never a number. Cases are hypothetical and never make a real business, listing or address the subject. A page that cannot meet the gates folds into its parent.

| | |
|---|---|
| Lane | GEO-2: 11 state pages and every metro that stands on its own evidence. |
| Models | Main session on Opus: plans, pre-counts, assigns, gates, tags. Research-reading subagents on Sonnet (fact sheets with source numbers, pre-counts, gate 8 identifier lists). Writers on Opus. The final SEO finish of every state and metro page (title, meta description, H1, first-screen answer, FAQ) on Fable. Attackers on Opus, the verifier on Sonnet (ruling 17). |
| Owned paths | `src/pages/states/new-york.html` and `src/pages/states/new-york/**`, `src/pages/states/pennsylvania.html` and `src/pages/states/pennsylvania/**`, `src/pages/states/new-jersey.html` and `src/pages/states/new-jersey/**`, `src/pages/states/massachusetts.html` and `src/pages/states/massachusetts/**`, `src/pages/states/maryland.html` and `src/pages/states/maryland/**`, `src/pages/states/connecticut.html` and `src/pages/states/connecticut/**`, `src/pages/states/new-hampshire.html` and `src/pages/states/new-hampshire/**`, `src/pages/states/maine.html` and `src/pages/states/maine/**`, `src/pages/states/delaware.html` and `src/pages/states/delaware/**`, `src/pages/states/rhode-island.html` and `src/pages/states/rhode-island/**`, `src/pages/states/west-virginia.html` and `src/pages/states/west-virginia/**`; `docs/rollout/geo-2/`. Nothing else (ruling 1). |
| Page standards | State and metro, ruling 3. Counted figures, ruling 5. Folding, ruling 6. Register use, ruling 10. |

## Pages and research (suggested tranche order, top to bottom: one state with its metros per tranche)

| State | Page | Metros | Research IDs |
|---|---|---|---|
| New York | `/states/new-york/` (rebuild) | promised: albany, binghamton, buffalo, hudson-valley, long-island, new-york-city, rochester, syracuse | ST-NEW-YORK, MT-NEW-YORK, the register |
| Pennsylvania | `/states/pennsylvania/` (rebuild) | promised: erie, harrisburg, lancaster, lehigh-valley, philadelphia, pittsburgh, scranton-wilkes-barre, state-college | ST-PENNSYLVANIA (no MT file), the register |
| New Jersey | `/states/new-jersey/` (rebuild) | promised: atlantic-city, bergen-county, camden, jersey-city, middlesex-county, monmouth-ocean, morris-county, newark | ST-NEW-JERSEY, MT-NEW-JERSEY, the register |
| Massachusetts | `/states/massachusetts/` (rebuild) | promised: berkshires, boston, cambridge, cape-cod, lowell, new-bedford, springfield, worcester | ST-MASSACHUSETTS, MT-MASSACHUSETTS, the register |
| Maryland | `/states/maryland/` (rebuild) | promised: baltimore, bwi-corridor, eastern-shore, frederick, montgomery-county, prince-georges-county, southern-maryland, western-maryland | ST-MARYLAND, MT-MARYLAND, the register |
| Connecticut | `/states/connecticut/` (rebuild) | promised: bridgeport, fairfield-county, hartford, litchfield-hills, new-haven, new-london, quiet-corner, waterbury | ST-CONNECTICUT, MT-CONNECTICUT, the register |
| New Hampshire | `/states/new-hampshire/` (rebuild) | promised: concord, lakes-and-mountains, manchester, nashua, north-country, portsmouth, salem, upper-valley | ST-NEW-HAMPSHIRE, MT-NEW-HAMPSHIRE, the register |
| Maine | `/states/maine/` (rebuild) | promised: aroostook, bangor, bar-harbor, bath, lewiston-auburn, midcoast, portland, york-county | ST-MAINE, MT-MAINE, the register |
| Delaware | `/states/delaware/` (new) | new: from MT-DELAWARE, about eight; pre-count each | ST-DELAWARE, MT-DELAWARE, the register |
| Rhode Island | `/states/rhode-island/` (new) | new: from MT-RHODE-ISLAND, about eight; pre-count each | ST-RHODE-ISLAND, MT-RHODE-ISLAND, the register |
| West Virginia | `/states/west-virginia/` (new) | new: from MT-WEST-VIRGINIA, about eight; pre-count each | ST-WEST-VIRGINIA, MT-WEST-VIRGINIA, the register |

Rebuilt states keep their URL and their published date. A promised metro slug is built at exactly that URL or folds into a section of its state page with that slug as its id. New metro slugs follow ruling 3 and the Delegated list.

## Lane notes

- **Pennsylvania has no MT file.** Its eight promised metros pre-count on ST-PENNSYLVANIA and the register alone. Expect folds, and do not stretch: a metro under 30 at the pre-count becomes a section of the Pennsylvania page.
- **Connecticut.** Its markets are planning regions in the register, with FOIA as two scheme components (`{"scheme_fit": ...}`, docs/web-fsc-5/CLOSE.md). `fairfield-county` carries ACS from its towns only and is not standalone in the register, so it needs its own research figures.
- **Sub-county markets** (Cambridge, for example) are places with ACS only in the register. Pre-count them honestly.
- **Delaware, Rhode Island and West Virginia are new states.** Pick their metro slugs from their MT files.
- **Same-name metros elsewhere.** Springfield (MA here; IL and MO in GEO-3), Rochester (NY here, MN in GEO-3), Portland (ME here, OR in GEO-4), Salem (NH here, OR in GEO-4), Albany (NY here, GA in GEO-1). Each page uses its own counties and says so in its first screen.
- **Cases.** The state page's "Worked cases in <state>" section and each metro's cases section list the cases located there. Cases are rebuilt by CASE-1 to CASE-4 at their current URLs, and new ones arrive at the URLs their blocks list. Link existing case URLs now; a new case URL that has not landed yet stays out of your page until it has (the links gate refuses a dead link). Add it in a later tranche, or request a mesh entry so the generated lists pick it up.
- **Requests** (ruling 13): metro cards in the Markets panel come from `data/site/chrome.json`. Ask the integrator for the menu entries your new metros need.

## End your turn with exactly

```
ROLLOUT GEO-2 CLOSE
head <sha> | tranches tagged <n> | landed <n> | returned <n> | last tag <tag>
pages <shipped>/<assigned> | folded <n> | words <total> | min counted figures <n> | max overlap <n>%
gates <green>/14 on the last tranche | open findings blocker <n> major <n>
owner: <one line, or none>
```
