# ROLLOUT ASSET-2: FUEL, AUTO, STORAGE AND INDUSTRIAL: NINE HUBS AND THEIR SUBTYPES, PLUS THE GAS STATION REGISTER PASS

Issued 16 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. Thirteen other roll-out sessions start at the same time. You never deploy: the integrator lands, deploys and submits your tranches. Index all: every page ships indexable.

## Your charter is the rulebook; this block is your assignment

Before anything else, fetch and check the rulebook:

```
git -C ~/Downloads/Feaisbility-Study-Company.com fetch origin
git -C ~/Downloads/Feaisbility-Study-Company.com show origin/main:docs/rollout/ROLLOUT-1.md > /tmp/ROLLOUT-1-asset-2.md
shasum -a 256 /tmp/ROLLOUT-1-asset-2.md
```

Fourteen sessions fetch at the same moment: if the fetch fails on a lock, wait a few seconds and retry it, up to five times. The hash must be `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (the rulebook as committed at `fb95856`). If it differs, stop and report the hash you got. Otherwise read all of that file (it is about 45,000 characters: read it with the Read tool in parts, not through shell output, which truncates) and follow it: step zero, the speed rules, the measured facts, rulings 1 to 17, the gates and the close. Nothing in this block relaxes it. Your lane id is `asset-2`: your branch is `rollout-asset-2`, your worktree `~/Downloads/wt-rollout-asset-2`, your tags `rollout/asset-2/t<n>`, your records `docs/rollout/asset-2/`, your gate 8 list `~/Downloads/fsc-rollout/private/dnu-asset-2.txt`.

The hard constraint, restated so it binds before you have read the rulebook: every figure traces to a dated source in the research files or the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. Nothing is invented, estimated past its source, or carried over from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition or a stated gap, never a number. Cases are hypothetical and never make a real business, listing or address the subject. A page that cannot meet the gates folds into its parent.

| | |
|---|---|
| Lane | ASSET-2: 9 hubs and every subtype that stands on its own evidence. |
| Models | Main session on Opus: plans, pre-counts, assigns, gates, tags. Research-reading subagents on Sonnet (fact sheets with source numbers, pre-counts, gate 8 identifier lists). Writers on Opus. The final SEO finish of every hub page on Fable; subtypes get theirs from their Opus writer. Attackers on Opus, the verifier on Sonnet (ruling 17). |
| Owned paths | `src/pages/asset-classes/self-storage.html` and `src/pages/asset-classes/self-storage/**`, `src/pages/asset-classes/truck-stop-and-travel-center.html` and `src/pages/asset-classes/truck-stop-and-travel-center/**`, `src/pages/asset-classes/express-car-wash.html` and `src/pages/asset-classes/express-car-wash/**`, `src/pages/asset-classes/rv-and-boat-storage.html` and `src/pages/asset-classes/rv-and-boat-storage/**`, `src/pages/asset-classes/auto-dealership.html` and `src/pages/asset-classes/auto-dealership/**`, `src/pages/asset-classes/auto-service-and-collision.html` and `src/pages/asset-classes/auto-service-and-collision/**`, `src/pages/asset-classes/industrial-and-warehouse.html` and `src/pages/asset-classes/industrial-and-warehouse/**`, `src/pages/asset-classes/cold-storage.html` and `src/pages/asset-classes/cold-storage/**`, `src/pages/asset-classes/data-center.html` and `src/pages/asset-classes/data-center/**`, and for the register pass `src/pages/asset-classes/gas-station-and-c-store.html` and `src/pages/asset-classes/gas-station-and-c-store/**`; `docs/rollout/asset-2/`. Nothing else (ruling 1). |
| Page standards | Hub and subtype, ruling 3. Counted figures, ruling 5. Folding, ruling 6. One intent, one page, ruling 16. |

## Pages and research (suggested tranche order, top to bottom: one hub with its subtypes per tranche)

| Hub | Subtypes | Research IDs |
|---|---|---|
| `/asset-classes/self-storage/` (rebuild) | promised: climate-controlled, conversion, drive-up, portable-container, third-party-managed, value-add (boat-rv is rewritten to the rv-and-boat-storage hub) | AH-SELF-STORAGE-A, -B, SD-SELF-STORAGE, the register |
| `/asset-classes/truck-stop-and-travel-center/` (rebuild) | promised: foodservice-qsr, fuel-only-fleet-fueling, gaming-truck-stop, independent-truck-stop, interstate-travel-center, net-lease-stnl, truck-parking, truck-service-maintenance | AH-TRUCK-STOP-AND-TRAVEL-CENTER-A, -B, SD-TRUCK-STOP-AND-TRAVEL-CENTER, the register |
| `/asset-classes/express-car-wash/` (rebuild) | promised: conversion, express-exterior, flex-service, full-service, in-bay-automatic, self-service | AH-EXPRESS-CAR-WASH-A, -B, SD-EXPRESS-CAR-WASH, the register |
| `/asset-classes/rv-and-boat-storage/` (rebuild) | promised: climate-controlled, covered-canopy, enclosed-drive-up, open-lot (boat-dry-stack is rewritten to marina/dry-stack-storage) | AH-RV-AND-BOAT-STORAGE-A, -B, SD-RV-AND-BOAT-STORAGE, the register |
| `/asset-classes/auto-dealership/` (rebuild) | promised: buy-here-pay-here, challenged-brand-franchises, franchised-new-car-domestic, franchised-new-car-import-luxury, heavy-truck-and-commercial, independent-used-car, powersports-and-motorcycle, rv-and-marine | AH-AUTO-DEALERSHIP-A, -B, SD-AUTO-DEALERSHIP, the register |
| `/asset-classes/auto-service-and-collision/` (rebuild) | promised: collision-body, dealership-fixed-ops, franchised-service, general-repair, quick-lube, specialty, tire-and-service | AH-AUTO-SERVICE-AND-COLLISION-A (no B run), SD-AUTO-SERVICE-AND-COLLISION, the register |
| `/asset-classes/industrial-and-warehouse/` (new) | new hub: define subtypes only where the B run supports a page that passes (Delegated) | AH-INDUSTRIAL-AND-WAREHOUSE-A, -B, the register |
| `/asset-classes/cold-storage/` (new) | new hub: define subtypes only where the B run supports a page that passes (Delegated) | AH-COLD-STORAGE-A, -B, the register |
| `/asset-classes/data-center/` (new) | new hub: define subtypes only where the B run supports a page that passes (Delegated) | AH-DATA-CENTER-A, -B, the register |

Rebuilt hubs keep their URL and their published date. A promised subtype slug is built at exactly that URL or folds into a section of its hub with that slug as its id. A slug that ruling 16 rewrites is never built.

## Lane notes

- **The gas station register pass.** You own `src/pages/asset-classes/gas-station-and-c-store.html` and `src/pages/asset-classes/gas-station-and-c-store/**` for it. WEB-FSC-6's D15(b) left the hub's SBA loan performance section without NAICS-level figures. Render the register's national and state 7(a) and 504 counts, volumes and charge-offs for the gas-station-and-c-store class through `mkt:` markers, under the register's refusals and flags. Then re-count the four folded subtypes (branded-fuel, unbranded-independent, convenience-no-fuel, foodservice-qsr) under ruling 5; any that reaches 30 at READY ships at its slug. The hub's two live subtypes and the five gas station cases are WEB-FSC-6's finished work.
- **`/asset-classes/industrial/`.** Request its 301 to `/asset-classes/industrial-and-warehouse/` in the tranche that ships that hub (ruling 16).
- **Distinct intents to keep apart.** `truck-stop-and-travel-center/interstate-travel-center` and `gas-station-and-c-store/interstate-highway`; `self-storage/climate-controlled` and `rv-and-boat-storage/climate-controlled`; `cold-storage` and `industrial-and-warehouse`. Each first screen says what this page covers that its neighbor does not.
- **Cases.** Each hub lists its cases, and each subtype names the cases that show it. Cases are rebuilt by CASE-1 to CASE-4 at their current URLs, and new ones arrive at the URLs their blocks list. Link existing case URLs now; a new case URL that has not landed yet stays out of your page until it has. Add it in a later tranche, or request a mesh entry so the generated lists pick it up.
- **The register on hubs.** CBP 2023 establishments by class and state, and SBA 7(a) and 504 counts, volumes and charge-off rates by class, are the hub's supply-density and loan-performance evidence (rulings 3 and 10). Respect each class's grade: a partial or proxy class needs `{"fit": ...}` and a sentence saying what it covers.
- **Requests** (ruling 13): the Asset Classes panel comes from `data/site/chrome.json`. Ask the integrator for any panel entry or mesh family your new hubs need beyond what FACTORY-2 adds.

## End your turn with exactly

```
ROLLOUT ASSET-2 CLOSE
head <sha> | tranches tagged <n> | landed <n> | returned <n> | last tag <tag>
pages <shipped>/<assigned> | folded <n> | words <total> | min counted figures <n> | max overlap <n>%
gates <green>/14 on the last tranche | open findings blocker <n> major <n>
owner: <one line, or none>
```
