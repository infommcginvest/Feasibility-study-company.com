# ROLLOUT GEO-3: THE MIDWEST: TEN STATES AND THEIR METROS

Issued 16 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. Thirteen other roll-out sessions start at the same time. You never deploy: the integrator lands, deploys and submits your tranches. Index all: every page ships indexable.

## Your charter is the rulebook; this block is your assignment

Before anything else, fetch and check the rulebook:

```
git -C ~/Downloads/Feaisbility-Study-Company.com fetch origin
git -C ~/Downloads/Feaisbility-Study-Company.com show origin/main:docs/rollout/ROLLOUT-1.md > /tmp/ROLLOUT-1-geo-3.md
shasum -a 256 /tmp/ROLLOUT-1-geo-3.md
```

Fourteen sessions fetch at the same moment: if the fetch fails on a lock, wait a few seconds and retry it, up to five times. The hash must be `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (the rulebook as committed at `fb95856`). If it differs, stop and report the hash you got. Otherwise read all of that file (it is about 45,000 characters: read it with the Read tool in parts, not through shell output, which truncates) and follow it: step zero, the speed rules, the measured facts, rulings 1 to 17, the gates and the close. Nothing in this block relaxes it. Your lane id is `geo-3`: your branch is `rollout-geo-3`, your worktree `~/Downloads/wt-rollout-geo-3`, your tags `rollout/geo-3/t<n>`, your records `docs/rollout/geo-3/`, your gate 8 list `~/Downloads/fsc-rollout/private/dnu-geo-3.txt`.

The hard constraint, restated so it binds before you have read the rulebook: every figure traces to a dated source in the research files or the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. Nothing is invented, estimated past its source, or carried over from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition or a stated gap, never a number. Cases are hypothetical and never make a real business, listing or address the subject. A page that cannot meet the gates folds into its parent.

| | |
|---|---|
| Lane | GEO-3: 10 state pages and every metro that stands on its own evidence. |
| Models | Main session on Opus: plans, pre-counts, assigns, gates, tags. Research-reading subagents on Sonnet (fact sheets with source numbers, pre-counts, gate 8 identifier lists). Writers on Opus. The final SEO finish of every state and metro page (title, meta description, H1, first-screen answer, FAQ) on Fable. Attackers on Opus, the verifier on Sonnet (ruling 17). |
| Owned paths | `src/pages/states/illinois.html` and `src/pages/states/illinois/**`, `src/pages/states/ohio.html` and `src/pages/states/ohio/**`, `src/pages/states/michigan.html` and `src/pages/states/michigan/**`, `src/pages/states/indiana.html` and `src/pages/states/indiana/**`, `src/pages/states/minnesota.html` and `src/pages/states/minnesota/**`, `src/pages/states/missouri.html` and `src/pages/states/missouri/**`, `src/pages/states/wisconsin.html` and `src/pages/states/wisconsin/**`, `src/pages/states/iowa.html` and `src/pages/states/iowa/**`, `src/pages/states/kansas.html` and `src/pages/states/kansas/**`, `src/pages/states/nebraska.html` and `src/pages/states/nebraska/**`; `docs/rollout/geo-3/`. Nothing else (ruling 1). |
| Page standards | State and metro, ruling 3. Counted figures, ruling 5. Folding, ruling 6. Register use, ruling 10. |

## Pages and research (suggested tranche order, top to bottom: one state with its metros per tranche)

| State | Page | Metros | Research IDs |
|---|---|---|---|
| Illinois | `/states/illinois/` (rebuild) | promised: bloomington-normal, champaign-urbana, chicago, metro-east, peoria, quad-cities, rockford, springfield | ST-ILLINOIS, MT-ILLINOIS, the register |
| Ohio | `/states/ohio/` (new) | promised: columbus, then the rest from MT-OHIO | ST-OHIO, MT-OHIO, the register |
| Michigan | `/states/michigan/` (rebuild) | promised: ann-arbor, detroit, flint, grand-rapids, kalamazoo, lansing, traverse-city, upper-peninsula | ST-MICHIGAN, MT-MICHIGAN, the register |
| Indiana | `/states/indiana/` (rebuild) | promised: bloomington, carmel, elkhart, fort-wayne, indianapolis, kokomo, northwest-indiana, warsaw | ST-INDIANA, MT-INDIANA, the register |
| Minnesota | `/states/minnesota/` (rebuild) | promised: brainerd, duluth, iron-range, mankato, minneapolis-st-paul, rochester, rosemount, st-cloud | ST-MINNESOTA, MT-MINNESOTA, the register |
| Missouri | `/states/missouri/` (rebuild) | promised: branson, columbia, jefferson-city, kansas-city, springfield, st-joseph, st-louis | ST-MISSOURI, MT-MISSOURI, the register |
| Wisconsin | `/states/wisconsin/` (rebuild) | promised: eau-claire, green-bay, kenosha-racine, madison, milwaukee, wausau, wisconsin-dells | ST-WISCONSIN, MT-WISCONSIN, the register |
| Iowa | `/states/iowa/` (rebuild) | promised: ames, cedar-rapids, council-bluffs, des-moines, iowa-city, quad-cities, sioux-city, waterloo-cedar-falls | ST-IOWA, MT-IOWA, the register |
| Kansas | `/states/kansas/` (new) | new: from MT-KANSAS, about eight; pre-count each | ST-KANSAS, MT-KANSAS, the register |
| Nebraska | `/states/nebraska/` (new) | new: from MT-NEBRASKA, about eight; pre-count each | ST-NEBRASKA, MT-NEBRASKA, the register |

Rebuilt states keep their URL and their published date. A promised metro slug is built at exactly that URL or folds into a section of its state page with that slug as its id. New metro slugs follow ruling 3 and the Delegated list.

## Lane notes

- **Ohio is new and already promised.** Its link is hidden in the site menus until its page exists, and `/states/ohio/columbus/` is promised sitewide. Ship Ohio and Columbus in an early tranche.
- **One market, two states.** The Quad Cities appear under both Illinois and Iowa. Kansas City appears under Missouri, and MT-KANSAS may carry the Kansas side; Council Bluffs sits in the Omaha market that Nebraska's file may also cover. Each such page uses only its own state's counties, says so in its first screen and links the other side. Where one side cannot reach 30 counted figures on its own counties, it folds.
- **Kansas and Nebraska are new states.** Pick their metro slugs from their MT files.
- **Same-name metros elsewhere.** Springfield (IL and MO here, MA in GEO-2), Columbia (MO here, SC in GEO-1), Rochester (MN here, NY in GEO-2), Columbus (OH here, GA in GEO-1), Bloomington (IL and IN, both yours).
- **Cases.** The state page's "Worked cases in <state>" section and each metro's cases section list the cases located there. Cases are rebuilt by CASE-1 to CASE-4 at their current URLs, and new ones arrive at the URLs their blocks list. Link existing case URLs now; a new case URL that has not landed yet stays out of your page until it has (the links gate refuses a dead link). Add it in a later tranche, or request a mesh entry so the generated lists pick it up.
- **Requests** (ruling 13): metro cards in the Markets panel come from `data/site/chrome.json`. Ask the integrator for the menu entries your new metros need.

## End your turn with exactly

```
ROLLOUT GEO-3 CLOSE
head <sha> | tranches tagged <n> | landed <n> | returned <n> | last tag <tag>
pages <shipped>/<assigned> | folded <n> | words <total> | min counted figures <n> | max overlap <n>%
gates <green>/14 on the last tranche | open findings blocker <n> major <n>
owner: <one line, or none>
```
