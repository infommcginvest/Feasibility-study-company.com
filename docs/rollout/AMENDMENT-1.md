# ROLLOUT-1 AMENDMENT 1

Issued 16 October 2026 by the coordinator, after an independent review of ROLLOUT-1 against the repo at `fb95856`. Every session reads this as soon as the owner points to it. It overrides ROLLOUT-1 where they differ, and changes nothing else. Record its sha256 in `docs/rollout/<lane>/STEP-ZERO.md` beside the rulebook's.

## A1. Gate 8 lists hold the subject only (replaces the list rule in ruling 7 and gate 8)

The competitor census names real competitors, so a list that bans every business name in a research file would turn every case red. A gate 8 list holds only the identifiers of the case's subject: the business name, street address, parcel id, listing id, asking price, per-acre price, exact acreage, broker and owner of the property or business the research file is built around.

Each line is `<case slug><TAB><token>`, checked on that case's page, source and inputs only.

A line of `*<TAB><token>` is checked on every served file and source. Use it only for the name and street address of a real subject: the six files named in Measured facts, and any other file whose subject turns out to be a real operating business or a listed property.

The WEB-FSC-6 list keeps its own format. The integrator converts it to these two forms when it copies it into `private/`.

A competitor named in a census with its URL is never a gate 8 identifier. It must also not be the subject wearing a new name.

## A2. Review before commit, history scanned (amends rulings 13, 14 and 17)

A page source is committed only after its review is clean, because a commit carries its contents into the bundle and from there to the public GitHub repository.

**The freeze** is the tranche's files in the throwaway copy, not a commit: record the sha256 of every source and case input, and of the copy's rendered pages. Attackers and the verifier read that copy. Fix the findings there, re-freeze, re-review what the fixes touch, and only then copy the sources into the worktree, commit and tag.

**At landing the integrator:**
- derives the tranche's page set from `git diff --name-only main...<tag>`, not from the builder's list, and runs every gate on all of those pages;
- scans `git log -p main..<tag>` against every gate 8 list, so an identifier anywhere in the tranche's history returns the tranche;
- lands a lane's tags in the order they were made.

**A returned tranche whose history carries an identifier:**
- the builder rebuilds its branch so that no commit carries it (reset to the last landed point and recommit the clean files);
- deletes the old tag;
- tags again.

Nothing has been pushed from a builder branch, so this rewrites only local history.

## A3. Disk (amends step zero probe 4 and speed rule 3)

The repo tree is about 211 MB, so each worktree and each throwaway copy costs about that much. Step zero needs at least 15 GB free. The stop is still under 5 GB.

- **Builders** keep at most two throwaway copies at a time. Delete each one as soon as its gate output and hashes are recorded. Delete everything under `~/Downloads/fsc-rollout/tmp/<lane>/` at close.
- **The integrator** deletes each deploy tree once its production checks are recorded.

These folders are yours to delete. Nothing else on the machine is.

## A4. A figure belongs to the most specific page, at landing too (amends ruling 14's floor check)

When a tranche repeats a counted figure of an already-landed page, the integrator applies ruling 4: the figure belongs to the more specific page (case over metro over state, subtype over hub).

**The specific page lands.** The landed parent no longer counts that figure. If that takes the parent under its floor, the integrator writes a return to the parent's lane naming the figure, and the parent's lane replaces it in its next tranche. The parent stays live meanwhile.

**Between two pages of the same rank,** the one that landed first keeps the figure, and the newcomer is returned.

**To avoid the collision,** state and metro pages do not use place-level figures for a town that hosts a case. They use county, CBSA or state figures there, and link the case. The case towns are:
- the towns in the four CASE blocks;
- the WEB-FSC-6 case towns (Lockhart, Lake Wales, Opelika, Cartersville, Versailles OH, Terrell, Bastrop, Seguin, Granbury, Weatherford, Boerne, Elgin, Hankamer, Johnson City);
- the six cases kept as they are (Townsend TN, Cape Coral FL, Oak Hill WV, Ossipee NH, and the Texas multifamily and Michigan veterinary cases).

## A5. Links to pages other lanes will build (amends gate 9 and the README's link rule)

A case links its state, metro and hub even when another lane has not landed that page yet.

**FACTORY-2 adds `data/site/promised.json`,** listing every URL any block assigns:
- the states;
- the promised metro and subtype slugs;
- the new hubs;
- every case URL;
- the METHOD-1 pages.

New metro and subtype slugs that builders choose are added from their requests.

**The chain renders promised links as pending.** A link to a promised URL that does not exist yet becomes a pending link with its class fallback (a state to `/states/`, a metro to its state's `#metros`, a subtype to its hub, a hub to `/asset-classes/`, a case to `/case-studies/`). `links.py --relink` switches it on the day the page lands.

**Gate 9's required edges count while pending.** At the target's landing the integrator checks that each one is live. A link to a URL that is neither existing nor promised is still a broken link.

## A6. The figure table, made explicit (replaces the table in ruling 5 and the threshold in ruling 6)

| Page type | Counted at READY | Research at READY | Register counted | Counted at landing | Research at landing |
|---|---|---|---|---|---|
| State, metro, hub, subtype, case, practice area | at least 30 | at least 20 | at most 10 | at least 25 | at least 15 |
| Framework page, research note | at least 18 | at least 10 | at most 8 | at least 15 | at least 8 |

The pre-count applies the same caps: research figures plus at most 10 register figures (8 for framework pages and notes) must reach the READY total, and research alone must reach its READY minimum. A metro that clears 30 only on the register does not get written.

## A7. Engine-only tranches (amends ruling 1 and ruling 13's tranche definition)

CASE-4 may tag engine changes on their own as `rollout/case-4/e<n>`, with no pages. The integrator lands an engine tranche as soon as it is READY, ahead of page tranches. Its gates are:
- gate 2;
- gate 11;
- `casemodel.py --check` over every case;
- the byte-identical render of every case CASE-4 does not own, proven in the tranche record.

CASE-4's first engine tranche should come early and should make every value a factory case needs renderable, including returns from `data/returns/` (`v.irr_pct` and its kin). The CASE-2 and CASE-3 rebuilds that keep a computed return depend on it. CASE-2 and CASE-3 work on their other cases until it lands.

## A8. Close records land (amends ruling 13's Finishing and ruling 14's When to close)

When a builder has committed its CLOSE and tagged `rollout/<lane>/close`, it writes `bus/ready/<lane>-close` with that tag's sha. The integrator lands close records like tranches (records only: gates 7, 8 and 10 on the diff). It closes only when all thirteen close records have landed, or 72 hours after its start.

## A9. Tools in parallel (amends ruling 14(c) and the gates)

Fourteen lanes run gates at once on one machine.

- **No fixed port.** Never use the fixed port 8770 that `docs/web-fsc-6/tools/gates.py` uses for screenshots. Pick a free port per run (bind to port 0, or 8800 plus a lane offset plus the tranche number), and serve only your own throwaway copy.
- **The integrator's tools.** In `scripts/qa/`, choose the port that way and take `--root` (the tree to check) and `--git-dir` (the worktree for history, commit-author and tag checks) separately.
- **Before FACTORY-2.** Builders run the content gates on the throwaway copy and the git-based checks (commit authors, tag messages, the history scan) in their worktree.

## A10. Pin the WEB-FSC-6 dates first (amends ruling 12 and FACTORY-2 (h))

All 23 WEB-FSC-6 sources carry `"updated": "DEPLOY"`, and nine also carry `"published": "DEPLOY"`. `src/site.json` says `2026-10-16`. Before any landing changes `deploy_date`, FACTORY-2 pins those 23 sources to `2026-10-16`, the date they went live, so no later deploy re-dates them.

From then on, gate 12 runs on every page of the site at every landing. A page's dates move only when its own content changed in that landing.
