# ROLLOUT GEO-1: THE SOUTH: ELEVEN STATES AND THEIR METROS, PLUS THE TEXAS MARKER PASS

Issued 16 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. Thirteen other roll-out sessions start at the same time. You never deploy: the integrator lands, deploys and submits your tranches. Index all: every page ships indexable.

## Your charter is the rulebook; this block is your assignment

Before anything else, fetch and check the rulebook:

```
git -C ~/Downloads/Feaisbility-Study-Company.com fetch origin
git -C ~/Downloads/Feaisbility-Study-Company.com show origin/main:docs/rollout/ROLLOUT-1.md > /tmp/ROLLOUT-1-geo-1.md
shasum -a 256 /tmp/ROLLOUT-1-geo-1.md
```

Fourteen sessions fetch at the same moment: if the fetch fails on a lock, wait a few seconds and retry it, up to five times. The hash must be `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (the rulebook as committed at `fb95856`). If it differs, stop and report the hash you got. Otherwise read all of that file (it is about 45,000 characters: read it with the Read tool in parts, not through shell output, which truncates) and follow it: step zero, the speed rules, the measured facts, rulings 1 to 17, the gates and the close. Nothing in this block relaxes it. Your lane id is `geo-1`: your branch is `rollout-geo-1`, your worktree `~/Downloads/wt-rollout-geo-1`, your tags `rollout/geo-1/t<n>`, your records `docs/rollout/geo-1/`, your gate 8 list `~/Downloads/fsc-rollout/private/dnu-geo-1.txt`.

The hard constraint, restated so it binds before you have read the rulebook: every figure traces to a dated source in the research files or the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. Nothing is invented, estimated past its source, or carried over from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition or a stated gap, never a number. Cases are hypothetical and never make a real business, listing or address the subject. A page that cannot meet the gates folds into its parent.

| | |
|---|---|
| Lane | GEO-1: 11 state pages and every metro that stands on its own evidence. |
| Models | Main session on Opus: plans, pre-counts, assigns, gates, tags. Research-reading subagents on Sonnet (fact sheets with source numbers, pre-counts, gate 8 identifier lists). Writers on Opus. The final SEO finish of every state and metro page (title, meta description, H1, first-screen answer, FAQ) on Fable. Attackers on Opus, the verifier on Sonnet (ruling 17). |
| Owned paths | `src/pages/states/florida.html` and `src/pages/states/florida/**`, `src/pages/states/georgia.html` and `src/pages/states/georgia/**`, `src/pages/states/north-carolina.html` and `src/pages/states/north-carolina/**`, `src/pages/states/tennessee.html` and `src/pages/states/tennessee/**`, `src/pages/states/south-carolina.html` and `src/pages/states/south-carolina/**`, `src/pages/states/alabama.html` and `src/pages/states/alabama/**`, `src/pages/states/kentucky.html` and `src/pages/states/kentucky/**`, `src/pages/states/louisiana.html` and `src/pages/states/louisiana/**`, `src/pages/states/oklahoma.html` and `src/pages/states/oklahoma/**`, `src/pages/states/arkansas.html` and `src/pages/states/arkansas/**`, `src/pages/states/mississippi.html` and `src/pages/states/mississippi/**`, and for the marker pass `src/pages/states/texas.html` and `src/pages/states/texas/**`; `docs/rollout/geo-1/`. Nothing else (ruling 1). |
| Page standards | State and metro, ruling 3. Counted figures, ruling 5. Folding, ruling 6. Register use, ruling 10. |

## Pages and research (suggested tranche order, top to bottom: one state with its metros per tranche)

| State | Page | Metros | Research IDs |
|---|---|---|---|
| Florida | `/states/florida/` (rebuild) | promised: fort-myers, gainesville, jacksonville, lakeland, miami, orlando, tampa, the-villages | ST-FLORIDA, MT-FLORIDA, the register |
| Georgia | `/states/georgia/` (rebuild) | promised: albany, athens, atlanta, augusta, columbus, macon, savannah, valdosta | ST-GEORGIA, MT-GEORGIA, the register |
| North Carolina | `/states/north-carolina/` (rebuild) | promised: asheville, charlotte, fayetteville, greensboro, greenville, hickory, raleigh-durham, wilmington | ST-NORTH-CAROLINA, MT-NORTH-CAROLINA, the register |
| Tennessee | `/states/tennessee/` (new) | new: from MT-TENNESSEE, about eight; pre-count each | ST-TENNESSEE, MT-TENNESSEE, the register |
| South Carolina | `/states/south-carolina/` (rebuild) | promised: charleston, columbia, florence, greenville, hilton-head, i-95-corridor, myrtle-beach, spartanburg | ST-SOUTH-CAROLINA, MT-SOUTH-CAROLINA, the register |
| Alabama | `/states/alabama/` (rebuild) | promised: auburn, birmingham, black-belt, gulf-shores, huntsville, mobile, montgomery, tuscaloosa | ST-ALABAMA, MT-ALABAMA, the register |
| Kentucky | `/states/kentucky/` (new) | new: from MT-KENTUCKY, about eight; pre-count each | ST-KENTUCKY, MT-KENTUCKY, the register |
| Louisiana | `/states/louisiana/` (new) | new: from MT-LOUISIANA, about eight; pre-count each | ST-LOUISIANA, MT-LOUISIANA, the register |
| Oklahoma | `/states/oklahoma/` (rebuild) | promised: durant, edmond, lawton, norman, oklahoma-city, pryor, stillwater, tulsa | ST-OKLAHOMA, MT-OKLAHOMA, the register |
| Arkansas | `/states/arkansas/` (rebuild) | promised: fort-smith, hot-springs, jonesboro, little-rock, mississippi-county, northwest-arkansas, pine-bluff, south-arkansas | ST-ARKANSAS, MT-ARKANSAS, the register |
| Mississippi | `/states/mississippi/` (rebuild) | promised: delta, desoto-county, golden-triangle, gulf-coast, hattiesburg, jackson, oxford, tupelo | ST-MISSISSIPPI, MT-MISSISSIPPI, the register |

Rebuilt states keep their URL and their published date. A promised metro slug is built at exactly that URL or folds into a section of its state page with that slug as its id. New metro slugs follow ruling 3 and the Delegated list.

## Lane notes

- **The Texas marker pass (do it in your first tranche; it is small).** You own `src/pages/states/texas.html` and `src/pages/states/texas/**` for it. WEB-FSC-6 left this pass open (its CLOSE, "WEB-FSC-5 register", and its D15 and D39):
  - render through `mkt:` markers the register series the Texas pages lack (CBP establishments by class, SBA 7(a) and 504 by market, ACS, BEA);
  - replace the Texas page's FY2025 7(a) count and volume, now cited to a loan broker's tabulation, with the register's loan-level values, and log the conflict;
  - keep Vintage 2025 population wherever the pages cite it (ruling 10);
  - then re-count McAllen, El Paso, Lubbock and Corpus Christi under ruling 5, starting from the drafts in `docs/web-fsc-6/folded/`. A metro that reaches 30 counted figures at READY ships as its own page, and its section on the Texas page becomes a card. One that does not stays a section. The fifteen Texas and gas station cases are WEB-FSC-6's finished work: do not touch them.
- **Kentucky, Louisiana and Tennessee are new states.** Pick their metro slugs from MT-KENTUCKY, MT-LOUISIANA and MT-TENNESSEE (rulings 3 and Delegated). Their neighbors in the mesh come from FACTORY-2; check them in your throwaway copy.
- **Same-name metros elsewhere.** Columbia (SC here, MO in GEO-3), Greenville (NC and SC, both yours), Columbus (GA here, OH in GEO-3). Each page uses its own counties and says so in its first screen.
- **Cases.** The state page's "Worked cases in <state>" section and each metro's cases section list the cases located there. Cases are rebuilt by CASE-1 to CASE-4 at their current URLs, and new ones arrive at the URLs their blocks list. Link existing case URLs now; a new case URL that has not landed yet stays out of your page until it has (the links gate refuses a dead link). Add it in a later tranche, or request a mesh entry so the generated lists pick it up.
- **Requests** (ruling 13): metro cards in the Markets panel come from `data/site/chrome.json`. Ask the integrator for the menu entries your new metros need.

## End your turn with exactly

```
ROLLOUT GEO-1 CLOSE
head <sha> | tranches tagged <n> | landed <n> | returned <n> | last tag <tag>
pages <shipped>/<assigned> | folded <n> | words <total> | min counted figures <n> | max overlap <n>%
gates <green>/14 on the last tranche | open findings blocker <n> major <n>
owner: <one line, or none>
```
