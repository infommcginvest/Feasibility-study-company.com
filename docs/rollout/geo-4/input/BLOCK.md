# ROLLOUT GEO-4: THE WEST: TEN STATES AND THEIR METROS

Issued 21 October 2026. Derived by FSC-NIGHT-1 on 21 October 2026 under the owner's block, from the research inventory (the block issued on 16 October was never saved). Run by FSC-NIGHT-1 through subagents inside this lane's own worktree, branch, drafts folder and records, under `~/Downloads/fsc-rollout/drafts/NIGHT-BRIEF.md`. Index all: every page ships indexable. The lane never deploys: the integrator lands, deploys and submits its tranches.

## Your charter is the rulebook; this block is your assignment

The rulebook and its amendment are in the worktree. Check them before anything else:

```
shasum -a 256 docs/rollout/ROLLOUT-1.md
shasum -a 256 docs/rollout/AMENDMENT-1.md
```

The rulebook hash must be `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (the rulebook as committed at `fb95856`) and the amendment's must begin `01639b33` and end `ee49`. If either differs, stop and report the hash you got. Otherwise read all of both files (the rulebook is about 45,000 characters: read it with the Read tool in parts, not through shell output, which truncates) and follow them: step zero, the speed rules, the measured facts, rulings 1 to 17, the gates and the close, as amended. Nothing in this block relaxes them. No GitHub fetch or push tonight (NIGHT-BRIEF). Your lane id is `geo-4`: your branch is `rollout-geo-4`, your worktree `~/Downloads/wt-rollout-geo-4`, your tags `rollout/geo-4/t<n>`, your records `docs/rollout/geo-4/`, your gate 8 list `~/Downloads/fsc-rollout/private/dnu-geo-4.txt`.

The hard constraint, restated so it binds before you have read the rulebook: every figure traces to a dated source in the research files or the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. Nothing is invented, estimated past its source, or carried over from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition or a stated gap, never a number. Cases are hypothetical and never make a real business, listing or address the subject. A page that cannot meet the gates folds into its parent.

| | |
|---|---|
| Lane | GEO-4: 10 state pages and every metro that stands on its own evidence. |
| Models | Main session on Opus: plans, pre-counts, assigns, gates, tags. Research-reading subagents on Sonnet (fact sheets with source numbers, pre-counts, gate 8 identifier lists). Writers on Opus. The final SEO finish of every state and metro page (title, meta description, H1, first-screen answer, FAQ) on Fable. Attackers on Opus, the verifier on Sonnet (ruling 17). |
| Owned paths | `src/pages/states/california.html` and `src/pages/states/california/**`, `src/pages/states/washington.html` and `src/pages/states/washington/**`, `src/pages/states/arizona.html` and `src/pages/states/arizona/**`, `src/pages/states/oregon.html` and `src/pages/states/oregon/**`, `src/pages/states/nevada.html` and `src/pages/states/nevada/**`, `src/pages/states/utah.html` and `src/pages/states/utah/**`, `src/pages/states/new-mexico.html` and `src/pages/states/new-mexico/**`, `src/pages/states/idaho.html` and `src/pages/states/idaho/**`, `src/pages/states/montana.html` and `src/pages/states/montana/**`, `src/pages/states/hawaii.html` and `src/pages/states/hawaii/**`; `docs/rollout/geo-4/`. Nothing else (ruling 1). |
| Page standards | State and metro, ruling 3. Counted figures, ruling 5. Folding, ruling 6. Register use, ruling 10. |

## Pages and research (suggested tranche order, top to bottom: one state with its metros per tranche)

| State | Page | Metros | Research IDs |
|---|---|---|---|
| California | `/states/california/` (rebuild) | promised: central-valley, inland-empire, los-angeles, orange-county, sacramento, san-diego, san-francisco, silicon-valley | ST-CALIFORNIA, MT-CALIFORNIA, the register |
| Washington | `/states/washington/` (rebuild) | promised: bellevue, columbia-basin, everett, seattle, spokane, tri-cities, vancouver, yakima | ST-WASHINGTON, MT-WASHINGTON, the register |
| Arizona | `/states/arizona/` (rebuild) | promised: flagstaff, phoenix, pinal-county, prescott, rural, scottsdale, tucson, yuma | ST-ARIZONA, MT-ARIZONA, the register |
| Oregon | `/states/oregon/` (rebuild) | promised: bend, eastern-oregon, eugene, hillsboro, oregon-coast, portland, prineville, salem | ST-OREGON, MT-OREGON, the register |
| Nevada | `/states/nevada/` (rebuild) | promised: carson-city, elko, fernley, lake-tahoe, las-vegas, laughlin, reno, winnemucca | ST-NEVADA, MT-NEVADA, the register |
| Utah | `/states/utah/` (rebuild) | promised: logan, moab, ogden, park-city, provo-orem, salt-lake-city, st-george, uinta-basin | ST-UTAH, MT-UTAH, the register |
| New Mexico | `/states/new-mexico/` (rebuild) | promised: albuquerque, farmington, las-cruces, los-alamos, permian-basin, rio-rancho, santa-fe, truth-or-consequences | ST-NEW-MEXICO, MT-NEW-MEXICO, the register |
| Idaho | `/states/idaho/` (new) | new: from MT-IDAHO, eight markets; the Treasure Valley (Ada and Canyon counties) is the one named in its opening, and the Kootenai and Bonneville county markets appear in its growth figures; choose the other slugs from the file; pre-count each | ST-IDAHO, MT-IDAHO, the register |
| Montana | `/states/montana/` (new) | new: from MT-MONTANA, seven markets named in its title: billings, missoula, bozeman, great-falls, kalispell (Flathead), helena, butte; pre-count each | ST-MONTANA, MT-MONTANA, the register |
| Hawaii | `/states/hawaii/` (rebuild) | promised: hawaii-island, kapolei, kauai, lahaina, maui, oahu | ST-HAWAII, MT-HAWAII, the register |

Rebuilt states keep their URL and their published date. A promised metro slug is built at exactly that URL or folds into a section of its state page with that slug as its id. New metro slugs follow ruling 3 and the Delegated list. Texas is not in this lane: its state page and four metros are live, and GEO-1 owns the Texas marker pass.

## Lane notes

- **Order.** California first (it carries the most pending metro links across the site), then Washington, Arizona, Oregon, Nevada, Utah, New Mexico, the two new states, and Hawaii last, because its research is the thinnest on supply.
- **Hawaii has six submarkets and little supply data.** Its MT file says the neighbor-island markets lack primary supply figures. Expect folds, and do not stretch: a metro under 30 at the pre-count becomes a section of the Hawaii page.
- **Idaho and Montana are new states.** Pick their metro slugs from their MT files. Idaho's file says the Treasure Valley alone has deep primary data and the other markets stand on population, permits, employers and labor data, so pre-count the Idaho markets honestly and expect folds. Montana's file says no market has asset-class supply metrics in public primary sources, so its markets rest on population, employment and local rules.
- **Arizona's promised `rural` slug** is a pending target that names no place. MT-ARIZONA describes four non-metro blocks. Decide at the pre-count whether `rural` is one page or four sections, and log it.
- **Case towns (A4).** State and metro pages do not use place-level figures for a town that hosts a case. They use county, CBSA or state figures there, and link the case. Case towns in this lane's states:
  - Arizona: Benson (CASE-1), Lake Havasu City (CASE-2), Casa Grande (CASE-2 and CASE-4), Prescott Valley (CASE-3).
  - California: Wildomar (CASE-2), Yucca Valley (CASE-4), Lincoln (CASE-3).
  - Hawaii: Kapolei (CASE-3). `kapolei` is a promised metro slug and a case town, so it either folds into the Oahu material or stands on county and CBSA figures.
  - Nevada: Winnemucca and Fernley (both CASE-4). `winnemucca` and `fernley` are promised metro slugs and case towns: same rule as Kapolei.
  - New Mexico: Carlsbad (CASE-3), inside the `permian-basin` market.
  - Oregon: Redmond (CASE-3), inside the `bend` market.
  - Utah: Hurricane (CASE-1), inside the `st-george` market.
  - Washington: Moses Lake (CASE-2), inside the `columbia-basin` market, and Gig Harbor (CASE-1).
  - Idaho and Montana: no case.
- **Same-name metros elsewhere.** Portland (OR here, ME in GEO-2), Salem (OR here, NH in GEO-2), Vancouver (WA here), Columbia Basin (WA here), Lake Tahoe (it straddles two states: the Nevada page uses its Nevada counties and says so). Each page uses its own counties and says so in its first screen.
- **Sub-county markets and county markets.** Sub-county markets (Kapolei, Lahaina and Hillsboro, for example) are places with ACS only in the register, and some markets are single counties (Pinal County). Pre-count them honestly.
- **Cases.** The state page's "Worked cases in <state>" section and each metro's cases section list the cases located there. Existing case URLs by state:
  - Arizona: `/case-studies/rv-park-arizona-usda/`, `/case-studies/rv-boat-storage-arizona-sba/`, `/case-studies/self-storage-arizona-sba/`, `/case-studies/multifamily-arizona-agency/`, `/case-studies/assisted-living-arizona-hud/`.
  - California: `/case-studies/rv-boat-storage-california-sba/`, `/case-studies/assisted-living-california-hud/`.
  - Hawaii: `/case-studies/assisted-living-hawaii-hud/`.
  - Nevada: `/case-studies/hotel-nevada-eb5/`, `/case-studies/retail-nevada-conventional/`.
  - New Mexico: `/case-studies/laundromat-new-mexico-sba/`.
  - Oregon: `/case-studies/pet-boarding-oregon-sba/`.
  - Utah: `/case-studies/glamping-utah-usda/`.
  - Washington: `/case-studies/coffee-shop-washington-sba/`.

  Cases are rebuilt by CASE-1 to CASE-4 at their current URLs, and new ones arrive at the URLs their blocks list: Yucca Valley CA (`/case-studies/short-term-rental-yucca-valley-california-conventional/`) and Gig Harbor WA (`/case-studies/marina-gig-harbor-washington-sba/`). A new case URL that has not landed yet stays out of your page until it has (the links gate refuses a dead link). Add it in a later tranche, or request a mesh entry so the generated lists pick it up.
- **Requests** (ruling 13): metro cards in the Markets panel come from `data/site/chrome.json`. Ask the integrator for the menu entries your new metros need, and for the Idaho and Montana entries in the state list.

## End your turn with exactly

```
ROLLOUT GEO-4 CLOSE
head <sha> | tranches tagged <n> | landed <n> | returned <n> | last tag <tag>
pages <shipped>/<assigned> | folded <n> | words <total> | min counted figures <n> | max overlap <n>%
gates <green>/14 on the last tranche | open findings blocker <n> major <n>
owner: <one line, or none>
```
