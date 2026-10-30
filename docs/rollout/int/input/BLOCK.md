# ROLLOUT INTEGRATOR: LAND, BUILD, GATE, DEPLOY AND SUBMIT EVERY TRANCHE, ALL NIGHT

Issued 16 October 2026 for the owner. Paste this whole block into a new Claude Code session on the owner's Mac and run it now, end to end, without stopping for questions. Thirteen other roll-out sessions start at the same time. You are the only session that deploys: deploy pre-authorized, by you alone. Index all: every page ships indexable.

## Your charter is the rulebook; this block is your assignment

Before anything else, fetch and check the rulebook:

```
git -C ~/Downloads/Feaisbility-Study-Company.com fetch origin
git -C ~/Downloads/Feaisbility-Study-Company.com show origin/main:docs/rollout/ROLLOUT-1.md > /tmp/ROLLOUT-1-integrator.md
shasum -a 256 /tmp/ROLLOUT-1-integrator.md
```

Fourteen sessions fetch at the same moment: if the fetch fails on a lock, wait a few seconds and retry it, up to five times. The hash must be `6e00a93d5ed9f6e971ccc4724ed744a8849eeab47db4939fd5bbd59a46772034` (the rulebook as committed at `fb95856`). If it differs, stop and report the hash you got. Otherwise read all of that file (it is about 45,000 characters: read it with the Read tool in parts, not through shell output, which truncates) and follow it: step zero, the speed rules, the measured facts, rulings 1 to 17, the gates and the close. Nothing in this block relaxes it. Your lane id is `int`: your branch is `rollout-int`, your worktree `~/Downloads/wt-rollout-int`, your records `docs/rollout/int/`.

The hard constraint, restated so it binds before you have read the rulebook: every figure traces to a dated source in the research files or the WEB-FSC-5 register, or to arithmetic a committed script performs on such figures. Nothing is invented, estimated past its source, or carried over from any client engagement or any other property of the owner. A NOT FOUND becomes a lender condition or a stated gap, never a number. Cases are hypothetical and never make a real business, listing or address the subject. A page that cannot meet the gates folds into its parent.

| | |
|---|---|
| Lane | INTEGRATOR: FACTORY-2, then the landing loop until every builder has closed, then the final site-wide pass. |
| Models | Main session on Opus: owns `main`, the shared files, the chain, the gates and the deploys. Subagents on Sonnet for checks that read many pages. The two final attackers on Opus, the final verifier on Sonnet. |
| Owned paths | Everything ruling 1 does not give a builder: `scripts/**` (except `scripts/casemodel.py` after FACTORY-2, which is CASE-4's), `src/templates/` except METHOD-1's new files, `src/types.json`, `src/site.json`, `src/case-cards.json`, `src/README.md`, `data/site/`, `data/mesh/`, `data/markets/`, `data/regulatory/`, `data/authors/`, `netlify.toml`, `sitemap.xml`, `robots.txt`, `feed.xml`, `index.html`, every section index page, every served HTML file the chain renders, and `docs/rollout/int/`. |
| Netlify | Site `0a67950d-6092-49c3-8277-017897c1b865`, published deploy `6ad23bed0dd08e20da34458c`, locked. That deploy is the rollback point at step zero. |

## Your work, in order

1. **Step zero and the bus.** Run step zero, then:
   - fast-forward local `main` to `origin/main`, cut `rollout-int` and create `~/Downloads/fsc-rollout/` with its folders (rulebook table);
   - write `bus/status/int` with a heartbeat line, refreshed every poll;
   - copy the WEB-FSC-6 gate 8 list into `private/` (ruling 14(c)).
2. **FACTORY-2** (ruling 14, (a) to (h)), within about two hours. Land it on `main` and tag `rollout/factory-2`, then deploy: it changes no page's words, so a draft and its checks are enough unless the chain moved served pages. Write `docs/rollout/int/REQUESTS.md`, with the request format and an example for every request kind.
3. **The landing loop** (ruling 14), every five minutes, one line of output per poll, until every builder has a `bus/status/<lane>-final` whose last tag has landed, or 72 hours have passed.
   - Batch tranches that arrive together.
   - Return what fails with the gate output.
   - Fix what your own files break.
   - Never edit a builder's file to make a tranche pass.
4. **Every landing ends live and submitted.** The steps, in ruling 14's order:
   - pin dates;
   - run the chain and the gates;
   - fast-forward `main`;
   - deploy: draft, its checks, then production, published by id with the lock kept;
   - run the production checks;
   - submit to IndexNow once;
   - write an incremental bundle `origin/main..main` to `<repo>/_bundles/rollout-<sha>.bundle`;
   - write `bus/landed/`.

   The coordinator pushes your bundles to GitHub from outside this Mac. Nothing else may push. Before every landing, `git fetch origin` and confirm `origin/main` is an ancestor of local `main`; a `Coordinator:` commit that is not, you merge.
5. **Your own pages.** Keep these true at every landing:
   - the home page, `/states/`, `/asset-classes/`, `/case-studies/` (cards rendered by `casemodel.py` from the card templates), `/practice-areas/` and `/research-notes/`;
   - the feed;
   - every count the site states about itself (states, metros, cases, asset classes). Run the stale-claim grep on each landing.
6. **The final pass and close** (rulebook, Close): every gate over every page, a freeze, two Opus attackers sampling across all lanes, a Sonnet verifier cold on your CLOSE, a final deploy and submission, then `docs/rollout/int/CLOSE.md`.

## Integrator notes

- **The lock.** Auto publishing stays stopped the whole time. You publish each production deploy by id.
  - If the CLI's `--prod` publishes on its own under the lock, confirm it did and that the lock still holds.
  - If it does not, use `restoreSiteDeploy` for that deploy id.
  - Either way, `getSite` must then show the new deploy published and auto publishing stopped.
- **Sizes.** The sitemap may pass several hundred URLs; keep it one file under 50,000 URLs and 50 MB. The register is about 54 MB against a 60 MB cap, and nothing in this roll-out adds markets to it (ruling 10).
- **Rollback.** If a production check fails, publish the previous good deploy by id at once. Then return the tranche or fix your file, and land again.
- **IndexNow.** One POST per landing, `scripts/indexnow.py --since <previous landed sha>`, with every changed URL and the sitemap. Record each response.
- **Owner items** go in CLOSE:
  - resubmit `/sitemap.xml` in Search Console after the first landing and once more at the end;
  - the author record lists credentials (Ph.D., MAI, CCIM) with no verification URLs;
  - anything a builder lists for the owner.

## End your turn with exactly

```
ROLLOUT INTEGRATOR CLOSE
main <sha> | landings <n> | tranches landed <n>/<tagged> | returned <n>
pages live <n> | new <n> | rebuilt <n> | folded sections <n> | sitemap URLs <n>
deploy <id> | rollback <id> | IndexNow URLs <n> | latest bundle <name>
owner: <one line, or none>
```
