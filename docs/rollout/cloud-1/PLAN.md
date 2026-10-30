# CLOUD-1: plan (30 October 2026)

FSC-CLOUD-1 continues the FSC rollout from a claude.ai cloud session. Goal: as much finished, gated work as possible before 5 November. The records win over the owner's paste where they are more specific; where they disagree this file says which one it follows.

## Step zero (30 Oct)
- `git fetch origin main`: origin/main is `1559002d` (the snapshot of local main `22987c4` plus `docs/rollout/cloud-handoff/`, INT I193). Every track branch is cut from it.
- Read: cloud-handoff/README.md, ROLLOUT-1.md, AMENDMENT-1.md, int/SITE-REMAINING-1.md, int/DECISIONS.md (last entry I193), geo-5/RESUME.md, case-new-1/RESUME.md, int/BUILD-PLAN-1.md (the case PAGE/FOLD list, "C0 result").
- The factory runs here: a throwaway copy (`git archive HEAD`) plus a draft source, `scripts/chain.py` (about 2 minutes, 212 URLs with North Dakota placed) and `scripts/qa/gates.py --stage ready` gave North Dakota 13/14 with gate 13 skipped, on the freeze 1 draft.

## What differs from the Mac, and how each gap is handled
| Mac resource | Here | Handling |
|---|---|---|
| Research folder `FSC Deep Searches 2` | absent | GEO-5: its ST and MT files are in cloud-handoff/geo-5/research. Cases and hubs: figures are re-sourced from the documents themselves (URL, publisher, date, table or page) by Sonnet researchers; the pre-count rows in cloud-handoff/case-new-1/_records/precount name each case figure and its publisher. A figure whose document cannot be fetched is not printed. |
| `fsc-rollout/private/` gate 8 lists | absent | Gate 8 runs on the lists available here: the CASE-NEW-1 `dnu.tsv` files, plus a list each case builder writes for its subject, kept in the session scratchpad, never in the repo. The integrator reruns gate 8 against `private/` at landing. |
| bus, integrator worktree, Netlify | absent by rule | Cloud sessions never land, deploy, or call Netlify, IndexNow or Search Console. Each track ends in a pull request to main that is not merged. |
| Throwaway copies under `fsc-rollout/tmp/` | session scratchpad | Same procedure: `git archive HEAD` of the track branch, sources placed, requests and patches applied, chain, gates. |

## Tracks (one branch and one pull request each)

Priorities (owner amendment 2): track A (states) is parked; track B (new case studies) first; track D (asset-class buyer intent) second; track C (new hubs) only when B and D both wait.

### A. `cloud/geo-5`: GEO-5 states (records: geo-5/RESUME.md, cloud-handoff/geo-5)
Order (GEO-5 D5, with Wyoming moved last by the paste, which the RESUME already allows: it waits for the vote):
1. North Dakota (t4): freeze 1 and both attacker reports exist (`reviews/t4-f1-attacker1.md`, `-attacker2.md`). Next: cold Sonnet verifier on both, fix list, capped Opus review of word-changing edits, copy on the branch, freeze 2, gates.
2. Alaska (t5): the same, after the inbound-link fix (RESUME A2-1: the "Alaska" mesh term lands on "Alaska Native Corporations", so gate 9 fails at landing). The fix is a link-only patch on existing words of live pages, written as `docs/rollout/geo-5/patches/*.py` for the integrator to apply at landing (the D16 Northern Virginia precedent), never a direct edit of an integrator-owned file.
3. District of Columbia (t7) and Vermont (t8): drafted and SEO-finished. Copy, gates, freeze 1, two Opus attackers (numbers; sameness, sourcing and subjects), cold Sonnet verifier, fixes, freeze 2, gates.
4. Wyoming (t6): held until after the vote of 3 November 2026. Then the closing band is refreshed to cite the result, with its source, and Wyoming goes through the same close. Not started before the result is published.
Floors and gates exactly as GEO-5 ran them: A6 READY floors (30 counted, 20 research, at most 10 register), overlap under 15%, 3 inbound links, gates 1 to 14.

### B. `cloud/case-new-1` and its tranche branches: NEW case studies only (owner amendment 3, 30 Oct; supersedes the rebuild plan of the charter and amendment 1)
- No rebuilds. Every case study live on main stays exactly as it is: no edit, rebuild or re-source, and no draft of a live case in any branch or pull request. The rebuild work had not produced a draft when the amendment came (the Track B session was stopped at its step zero).
- The queue is `docs/rollout/case-new-1/CASES-NEW.tsv`: 24 queued cases and the held classes, in the owner's order. Classes with no case (live hubs first: skilled nursing, mixed-use; then the promised hubs whose case links them as pending until track C builds them: event and wedding venue, industrial and warehouse, cold storage, brewery and distillery, wellness and retreat), then classes with one case (funeral home, veterinary practice, coffee shop, laundromat, pet boarding, retail, auto dealership, auto service, behavioral health, private school), then new states for covered classes (the handed-off Gonzales childcare draft first). Towns carry no state-page section and no case today (A4). Programs are the engine's four; independent living, build-to-rent, manufactured housing, short-term rental and data center are held for CASE-ENGINE-1, with the promised engine cases, Gig Harbor and the folded promised cases.
- Tranches of up to six cases, one branch and one pull request each, each from main plus the previous tranche: `cloud/case-new-1` (c1), `cloud/case-new-1-t2` (c2), and on. Each case: a public-document pre-count (fold under 30 and 20), research from documents opened at their URL, the house case format, buyer intent in title, H1, meta, opening and call to action, links both ways with its hub and state page (back-links as link-only patches for the integrator). Full close per tranche. Brief: `docs/rollout/case-new-1/cloud-1/BRIEF-B.md`.
- C0 rerun of 30 Oct (kept for the record; no rebuild uses it): of the 25 no-engine PAGE rebuilds, 21 still cleared 30 and 20 on their reader rows; meat-processing-georgia-usda, hotel-south-carolina-sba, rv-park-arizona-usda and rv-park-pennsylvania-usda fell under.

### C. `cloud/hubs-1`: the 11 hubs still unbuilt (records: int/SITE-REMAINING-1.md section 3, BUILD-PLAN-1 sections 4 and 5)
brewery-and-distillery, build-to-rent, cold-storage, data-center, event-and-wedding-venue, independent-living-and-ccrc, industrial-and-warehouse, manufactured-housing, meat-and-poultry-processing, short-term-rental, wellness-and-retreat (skilled-nursing landed as pilot-1 t1).
1. No hub draft or AH research file is in the cloud, so each hub starts with a Sonnet pre-count from public documents: at least 30 dated, sourced, hub-specific figures not served on any other page, of which at least 20 from documents and at most 10 from the register (CBP establishments and SBA FOIA for the class). Under that count the hub is not written and stays pending (ruling 6; BUILD-PLAN names wellness-and-retreat as the likeliest fold).
2. The hub model is `/asset-classes/skilled-nursing/` (pilot-1): the owner's buyer-intent header ("<Class> Feasibility Study Company | Feasibility Study Company", H1 "<Class> Feasibility Study Consultants", meta 140 to 160 characters, opening and call to action naming the firm, at least one counted figure on the first screen), then hub depth (ruling 3: development cost, operating benchmarks, SBA performance by NAICS, valuation, structure, demand method, supply by state, subtypes as sections, review failures, document checklist, cases). The I115 sameness guard applies: no shared hero plan, description frame or call-to-action move across the eleven.
3. Hubs carry short pointers to cases, never embedded cases. Links both ways: each hub links its cases, related hubs and the practice areas; the inbound side comes from requests (mesh terms, index entries) and, where a live page names the class, link-only patches on existing words for the integrator. Ruling 16 rewrites stay (manufactured-housing and build-to-rent take the multifamily rewrites; independent-living-and-ccrc takes active-adult and ccrc-life-plan-communities). The industrial hub's landing carries the 301 from `/asset-classes/industrial/` (request asset-2-2 form).
4. One tranche per hub (ruling 13), all on one branch.

### D. `cloud/buyer-intent-1`: buyer intent on the existing asset-class pages (owner amendment 1)
Every asset-class hub and asset-class page already on main: the 30 hubs served at `1559002d` (7 with a source under `src/pages/asset-classes/`, among them gas station and c-store, and skilled nursing, whose pilot header is checked and left alone if it already meets the rule; 22 legacy hubs served as HTML with no source) and the 3 subtype pages (burger, ev-charging, interstate-highway).
1. Only the title, H1, meta description, opening paragraph and call to action change, edited in place to target "[subject] feasibility study consultant" and "[subject] feasibility study company" alongside "[subject] feasibility study", so each reads as a firm the visitor can hire. No URL or slug changes; the informational body stays; no new figure; a number touched keeps its citation; no fee, turnaround, guarantee, approval or credential promise (no record states one).
2. Sourced pages: the source's front matter and opening are edited and `updated` goes back to "DEPLOY" (ruling 12). Legacy hubs have no source and the integrator owns served HTML (BUILD-PLAN-1 HUB-RETROFIT-1, I104), so their edits ship as a recorded, idempotent script under `docs/rollout/buyer-intent-1/` that the integrator runs at landing; the gates run on a copy with it applied.
3. Every change, element by element with before and after, goes in `docs/rollout/buyer-intent-1/BUYER-INTENT-1.tsv`. Where a retrofit touches a link, both directions are linked.
4. The I115 sameness guard and gate 4 bind across all 33 openings and against the 11 new hubs of track C: no shared hero plan, description frame or call-to-action move.
5. Close as the other tracks: gates, freeze, two attackers, a cold verifier, one pull request, not merged.

## Network (30 Oct, found during the first review round)
This environment's network policy refuses the source hosts: www.census.gov, data.census.gov, www.bls.gov, does.dc.gov, ora-cfo.dc.gov, www.sba.gov, www.usda.gov, www.ers.usda.gov, www.nass.usda.gov, apps.bea.gov, www.huduser.gov, fred.stlouisfed.org, en.wikipedia.org, www.cbre.com and www.brewersassociation.org all fail (proxy 403 or no resolution). Web search answers, but a search snippet is not the document, so no figure is printed from one. Consequences, until the owner widens Network access in the environment settings:
- Track A goes on: its research rows are in the handoff; reviewers record each source URL they could not open as NOT FETCHED (the integrator can re-open them on the Mac).
- Track D goes on: it reuses each page's own cited figures and fetches nothing.
- Tracks B and C stop before research: every figure must come from a document opened at its URL. Their queue and briefs are prepared; nothing is written from memory or from snippets.
- After amendment 2 (owner set Full access) the hosts still answered 403 at 15:15Z and 15:31Z, both from this container and from a fresh sibling session's container started at 15:29Z; the environment still describes itself as "trusted network access". The setting has not taken effect yet.

## Every new page
Title, H1, meta, opening and call to action target "[subject] feasibility study consultant" and "[subject] feasibility study company" alongside "[subject] feasibility study"; informational depth below. Byline from the author record (Mark Otava). No em or en dashes. No excluded firm, no other property of the owner, no client data or figure from any of the owner's client engagements. Every number cites its document. robots, 403, 429, bot checks and paywalls bind: a closed door is recorded NOT FETCHED, never worked around; nothing is fetched from www2.census.gov.

## Close, per track
1. Render in a throwaway copy of the branch and run `gates.py --stage ready` on the track's pages, plus gates 3, 4, 9, 10 and 12 site-wide; gate 13 screenshots with the pre-installed Chromium on a free port.
2. Freeze: sha256 of every source and input, of each rendered page and of `git archive HEAD`.
3. Two Opus attackers on the frozen copy, working separately (one on numbers, one on sameness, sourcing and subjects), each finding with page, line and reproduction. Then one cold Sonnet verifier whose default verdict on every finding and every tranche claim is REFUTED until it reproduces it. A tally measures how a finding was argued, not how the world is.
4. Fix, re-freeze, rerun the gates the fix touches. Commit page sources only after the review is clean (A2); commits authored Feasibility Study Company <noreply@feasibility-study-company.com>.
5. A merged simulation: one copy with all three tracks' pages, gates 3 and 4 across them, so a figure two tracks share is found before landing (A4: case over hub).
6. One pull request per track to main, with the gate output in the body. Not merged. `docs/rollout/<lane>/RESUME.md` per track for the Mac integrator or a later session.

## Owner items
- O-C1. The snapshot on GitHub main carries gate 8 material the records keep outside the repository (BUILD-PLAN-1 C0: the per-figure rows "sit outside the repository (they carry real-site identifiers; gate 8)"). Exact paths, sizes and sha256 are in the appendix below. Owner ruling (amendment 1): the repository is being made private and the integrator removes these at the next landing; no branch or pull request of this session copies them, and no report quotes them.
- O-C2. Network access (section above): Tracks B and C need the source hosts allowed. The owner set the environment to Full (amendment 2); the policy did not reach this session's running container, so a sibling cloud session (`session_01A2qr3utoM79JaqfPsQasg1`, owner's choice) was started for Track B at 15:29Z; its new container got the same 403 at step zero, and it was stopped there by amendment 3 before any work. It is idle. Until the network setting takes effect, Tracks B and C cannot source a figure.
- O-C3. The first pushes of `cloud/geo-5` and `cloud/case-new-1` (30 Oct, about 15:15Z to 15:30Z) carried the owner's surname, which matches the ruling 9 pattern, in this plan's first line and in the Track B brief. Both branches were rewritten from main without it and force-pushed within minutes; no pull request existed. GitHub may keep the replaced commits reachable by their hashes until it collects them; the owner's switch of the repository to private covers them.

## Appendix: private material on main (amendment 1, item 3)

Paths, sizes in bytes and sha256 at main `1559002d`. Contents are not copied into any branch or pull request and are not quoted in any report. The owner is making the repository private; the integrator removes these at the next landing. Found by name (dnu, PRIVATE, precount rows) and by a case-scoped match of the CASE-NEW-1 subject lists against every file under `docs/rollout/cloud-handoff/case-new-1` and `docs/rollout/case-new-1` (files with two or more matches are listed; files with a single short match, such as gate outputs, read as coincidence and are left to the integrator's own gate 8 run with `private/`).

### A. Gate 8 subject lists (607 lines): 8 files, 31,454 bytes

| Path | Bytes | sha256 |
|---|---|---|
| `docs/rollout/cloud-handoff/case-new-1/car-wash-port-charlotte-florida-sba/dnu.tsv` | 6,769 | `fac48bd899334d146742da94dbeb3167faaaa245bce7fa47f79d6dc73385978c` |
| `docs/rollout/cloud-handoff/case-new-1/childcare-gonzales-louisiana-sba/dnu.tsv` | 1,254 | `b61cb68138b3961371ac12d21b96d08925c4e6c8e27ca328272aaf74d291781f` |
| `docs/rollout/cloud-handoff/case-new-1/grocery-store-ness-city-kansas-usda/dnu.tsv` | 1,332 | `253b07aefe4686e956d0fb9ddba4b4bc3b1ecb5c41ad8ad0e3e3126d765e7c6c` |
| `docs/rollout/cloud-handoff/case-new-1/medical-office-lebanon-tennessee-sba/dnu.tsv` | 1,671 | `6d31b4988e99670f743fac02fef7a07c0def4092ae00c9f2c37bb03486060524` |
| `docs/rollout/cloud-handoff/case-new-1/restaurant-acquisition-broussard-louisiana-sba/dnu.tsv` | 3,996 | `00fb7b0eda9ad55a24af3421922905e9703af6aa10ae791642e3cdfa6c9f5f85` |
| `docs/rollout/cloud-handoff/case-new-1/restaurant-sevierville-tennessee-sba/dnu.tsv` | 10,610 | `c73720eb500162740fb62f5eb9dcec563f2f7ec8d11d91a5d562ef449a948ef5` |
| `docs/rollout/cloud-handoff/case-new-1/self-storage-bardstown-kentucky-usda/dnu.tsv` | 4,023 | `02387054b80d7ee3c2bdcd873838ab714be2a8481ab1022349d639b53c7c10ec` |
| `docs/rollout/cloud-handoff/case-new-1/urgent-care-elizabethtown-kentucky-sba/dnu.tsv` | 1,799 | `0800bd0654ead7fafe1fdcf24130335e9e90ac0df8101c6b13d043ab277bf43d` |

### B1. Pre-count rows, `_records/precount` (per-figure rows; some carry subject listing prices): 68 files, 985,428 bytes

| Path | Bytes | sha256 |
|---|---|---|
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/assisted-living-arizona-hud.tsv` | 12,545 | `99409b19bbfe2609fdef961d9dbe328abd5afb1dc5a46cae50c6692a22e85263` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/assisted-living-california-hud.tsv` | 16,244 | `b0545c14def43ee50df4618a7ec53b337ab9f5c45bad6c04eca32f344db78f03` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/assisted-living-elizabethtown-kentucky-bridge.tsv` | 18,948 | `187412ac0507426ca5421ca06b75f3753e5446dab262890295994c655e3f7bb9` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/assisted-living-florida-hud.tsv` | 16,159 | `13b71d9d56b8c64f2ebf381357dfcb09f82afbbfca5475305ea8b9bc25879a87` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/assisted-living-hawaii-hud.tsv` | 13,292 | `571d0e2e5b27123ddda354d47f248f161189dd55072dbef8b752dbbc12d71b7d` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/assisted-living-north-carolina-hud.tsv` | 12,003 | `939936b28f6b4d3c2430f97ccc4ffae4283789dd80f4aa3d55b7e7859eb1d987` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/auto-service-new-jersey-sba.tsv` | 18,115 | `287abde06a448754dd3f4e59966f5909b286600f9b8204eded89ef9577b7d5a0` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/behavioral-health-massachusetts-conventional.tsv` | 13,327 | `d2e3a2eb474408a3799f0f75d6c1f9657b438e146f156cc376067f01b356c9ef` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/car-wash-port-charlotte-florida-sba.tsv` | 21,899 | `a4bd7dab8ae29a2b2d738a52f060636ac27fe7c4b22c4003c9e0538f2cb9ea1d` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/childcare-gonzales-louisiana-sba.tsv` | 15,564 | `9ae50b6d6ed251c0949ad181108be508ec654c9ea6a95eb880e00a9e8a144997` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/childcare-illinois-sba.tsv` | 13,061 | `befc03bd183f86a8b84e808650a08d07d83536d489ba5866377c13ceb31b9ea2` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/childcare-iowa-sba.tsv` | 10,974 | `79af1cb96d7534b912c541642ed313c443829124ba87ab210732531e4a8003bb` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/coffee-shop-washington-sba.tsv` | 11,971 | `f1c75a09b3bbd347afacf309821a1c2db29bb85c8a9daae1602dbe998824218c` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/fitness-minnesota-sba.tsv` | 14,806 | `df329563cefeb37ff7aecb2e3272ad55f02b8125779bdb44d773d155bcab38ea` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/fitness-new-hampshire-sba.tsv` | 26,509 | `8dec6f3dd9d8e65c362a4fba0e11a3f48e5cd32b15cfc4f54506e4a439836eec` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/funeral-home-wisconsin-sba.tsv` | 8,929 | `1f61d12d1fe44771891bb4fc05d6b13c8884908136db4f987bd06bc083991036` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/glamping-utah-usda.tsv` | 17,702 | `bf1cc7e07620f54a723ce9bfb05c5c82b0e625cf6f21de08e2c1062e886491a4` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/grocery-store-mississippi-usda.tsv` | 14,190 | `5c87ee6393447bff8a418a6906280e25c68bd567458c5a93ac83d821118898e2` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/grocery-store-ness-city-kansas-usda.tsv` | 18,656 | `c1a767133df6957edbe3fb5498c3601e5fffc6c37b00f345486c611d8c77e0cd` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-acquisition-fairlawn-ohio-sba.tsv` | 14,285 | `8fd5fb695a87240cc69edb4deb14bbd4c8cee22d71aed64076344f9c96081a5d` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-florida-sba.tsv` | 17,827 | `1ee7cec33fc5d619ca0d9bf7ce11bc9abb1358fb7f4990aa364291ed96eccba3` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-georgia-sba.tsv` | 20,136 | `813b8db57a7dbe298fc308fa515d21ec50f96c3024f21f09514b5603280f6bb9` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-hays-kansas-usda.tsv` | 10,338 | `b581944b96ae594635e0f0f2b3e1e9503a69f59db233756b776217b89e684a10` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-natchitoches-louisiana-eb5.tsv` | 19,371 | `af215f5b14fe4ab4ce025ac9cfe80db549b086a8ef1032e9790070d3f3c550af` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-nevada-eb5.tsv` | 8,915 | `9955e5a4be9a1bc068ca6e44eda8ab6bdcf95234afe2cb4165bafd7227ae39c6` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/hotel-south-carolina-sba.tsv` | 16,023 | `034c1347c904332ac2342cc9ebf5dc16daffd92e1ab6025f82809ac364f6ee5e` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/industrial-flex-gardner-kansas-conventional.tsv` | 17,639 | `c9f5697ec71c3d3e0b4bd3b2e462b1f0b6581436476e61b155cc542c313bb424` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/laundromat-acquisition-huron-county-ohio-sba.tsv` | 15,908 | `ccbfa65f8ea11029b2712655748429a4ec78786de73c402251a8ec97e6277b7f` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/laundromat-new-mexico-sba.tsv` | 11,731 | `bb63dc8273fdd69a9fbbfc73f7e1484517817b60024ffe6b68fcfdeb54343e07` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/marina-gig-harbor-washington-sba.tsv` | 19,327 | `b73811679f4adc180d36ab02654a1c68d539d8f4fd973014be79897a027554e3` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/marina-maryland-sba.tsv` | 12,820 | `d96c6a64b67bb04b1c1e1ccdbed06b528a6fbcf73ee9b18f77c9ec5f8e400772` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/marina-new-baltimore-michigan-sba.tsv` | 11,615 | `de16c75c55bd358ed8d2728a475be7a0e4785964384575f0609e15bd50785f48` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/marina-shell-knob-missouri-usda.tsv` | 11,865 | `0fb4eaf1eb696dc918af3da4b6100b68a419e503bf8343e23a0f5eaa90fe1e27` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/meat-processing-georgia-usda.tsv` | 11,157 | `b5dbe8ecc7afcc96ee2e474d01484447f1360ee92ea3b5dcb0d78a010a5faa80` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/meat-processing-north-carolina-usda.tsv` | 12,572 | `0dae516b3cdfb381c8143d7beff1b90ae978705f73b4f345ca611bc646abc7e2` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/medical-office-lebanon-tennessee-sba.tsv` | 20,096 | `fa4d4af15b759c2ca4db96a283454c1fe35ae1cfb0132bcfe048a7f6d8ed2a61` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/medical-office-north-carolina-sba.tsv` | 12,153 | `bd0cc18e5d88922ca5ff78090208840da58bd4a7bab454e7387898165c371bc8` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/mixed-use-multifamily-euclid-ohio-eb5.tsv` | 13,575 | `71129223954d5a9980c4be60aa1f93e8309df430757cae112eab2d425d427f7d` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/multifamily-arizona-agency.tsv` | 15,352 | `8f4fe13bb60e73bb7d0b1facdc0e77a3aacad53998806efc38aeedf2807d626c` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/multifamily-clarksville-tennessee-dscr.tsv` | 15,412 | `ab259b8690df8de1f44d76daaf761931b9433e8cafdb7a9cb5f25f30594f7377` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/multifamily-florida-agency.tsv` | 11,797 | `c87e9e6f8e4ced2eeeff95a8fc46e20f76a4dcc53747c815c97fb942ed973dce` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/multifamily-georgia-agency.tsv` | 13,315 | `e5e3588393787af2181c5f1a026ed325483b71a76d896537f0e13332fad78096` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/multifamily-new-york-agency.tsv` | 15,166 | `871f7b26dc0ff167e2d8e466c86b7ab6049bba35739d1f6c212fc03c4c33c3ad` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/multifamily-north-carolina-agency.tsv` | 9,818 | `6fca9929d2aca2746ff939fc35d699a106ba6719e2d16db748017d5e541be90f` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/pet-boarding-oregon-sba.tsv` | 11,520 | `c2fed1f2e714f85854915359fed787df2f6f42425bcbbd35a48a073756d6aae3` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/private-school-connecticut-conventional.tsv` | 9,342 | `94cf4bbcb08f9bd69fa97898491235c422ca5c2358732135b5a671dc7530ca02` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/qsr-arkansas-sba.tsv` | 8,661 | `b8ae920392a90e7cfe509933189f992ab8252babbe9ec12cfff1faebb93eaae5` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/qsr-georgia-sba.tsv` | 15,521 | `e86d36d1a701d041ed305e743b985eaa4255e50d3aa9f6745b625e27586585d2` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/restaurant-acquisition-broussard-louisiana-sba.tsv` | 16,227 | `567a218acb93255a605055b037018843cdcc85dc257f77c692769eaabfa2ec2b` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/restaurant-missouri-sba.tsv` | 13,164 | `a4ccc235e6963d58ff75658b750dca64020fcadd64c1dba1e9834c99514a5b70` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/restaurant-sevierville-tennessee-sba.tsv` | 15,785 | `80c35cd94380ec5e52677603f71ce05512ed177a8b182b766ba03b2cee976437` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/retail-nevada-conventional.tsv` | 10,039 | `b4218b192d9af011603cb3526582057bfa39dc36349bc92100652a34ab145a23` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/retreat-center-kerhonkson-new-york-usda.tsv` | 9,437 | `d80922ab63c2b9f84b18dfa7f20c2b3b4526a94801aa52398ca09525e18f690e` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/rv-boat-storage-arizona-sba.tsv` | 17,850 | `d2e6fcf39dc98d4a5e0794b862fff83fe721c139224f7dab3761c27f34c5de19` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/rv-boat-storage-california-sba.tsv` | 14,330 | `4f6faca9e3d196e2635d0f7743bd8010729421b723e5876003ad26c1a30a033f` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/rv-boat-storage-florida-sba.tsv` | 17,157 | `d50e4400c36856469f599741fb053645555ea74d6b6453cdbebf901c539d414b` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/rv-park-arizona-usda.tsv` | 11,569 | `aaa8eda4c6847fa3c0eef96c1d047426b97371c63022fb7fd1f366c9cb4e97fc` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/rv-park-maine-usda.tsv` | 9,579 | `7438443dfbffe6bff0d89637fcd320d6eec8e24df14f1f0d2a6fc7a97be741d3` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/rv-park-pennsylvania-usda.tsv` | 10,674 | `55f12ec67fa01dc70d9d33b7aebff9788ddaeed50e873cc47248c7602dfc1ea7` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/self-storage-arizona-sba.tsv` | 19,336 | `d1968aca1652e4014b863db5ed3d20e4d332ad41ce4eb2c861ee00ca70e633e1` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/self-storage-bardstown-kentucky-usda.tsv` | 17,264 | `5a42ff23dcb8477d02f3632f2d3149267a61b25eaf6023d1f1a07c7756d46f98` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/self-storage-indiana-sba.tsv` | 14,024 | `07648447cb94c6ed82f927926046d0074e2aa2c045ce93fd28fccbe46b6dbb63` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/self-storage-pataskala-ohio-sba.tsv` | 13,290 | `b30fc97e0921f405c5b931eeae84144413a1d9d9c456bdf4996d8495bf26aea2` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/short-term-rental-yucca-valley-california-conventional.tsv` | 15,673 | `d20e03ec28f2578f5a2c714ebbc3329cf54a86b8c4441a0220f7988db64f8712` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/truck-stop-georgia-sba.tsv` | 18,291 | `9f5e7def794cd144733308f540dc2d73f17f2fa0e2c3b776d4e371ba7be81965` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/truck-stop-oklahoma-sba.tsv` | 16,632 | `14b62aeea7dc9602264dd6f1f320f1f1764dd40675e3401a3d37590d511bbd23` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/urgent-care-elizabethtown-kentucky-sba.tsv` | 14,900 | `bfee098e42bfcf0997f379ee6148509005de09b4fffcefa6f5bb827b47c47156` |
| `docs/rollout/cloud-handoff/case-new-1/_records/precount/urgent-care-florida-sba.tsv` | 12,056 | `434e77cc0c48148549e9128dd35eef22cbcece04aaccf3f93de01cebe7cd9923` |

### B2. Pre-count rows, `_freeze/precount-rows-PRIVATE` (byte-identical set): 68 files, 985,428 bytes

| Path | Bytes | sha256 |
|---|---|---|
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/assisted-living-arizona-hud.tsv` | 12,545 | `99409b19bbfe2609fdef961d9dbe328abd5afb1dc5a46cae50c6692a22e85263` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/assisted-living-california-hud.tsv` | 16,244 | `b0545c14def43ee50df4618a7ec53b337ab9f5c45bad6c04eca32f344db78f03` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/assisted-living-elizabethtown-kentucky-bridge.tsv` | 18,948 | `187412ac0507426ca5421ca06b75f3753e5446dab262890295994c655e3f7bb9` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/assisted-living-florida-hud.tsv` | 16,159 | `13b71d9d56b8c64f2ebf381357dfcb09f82afbbfca5475305ea8b9bc25879a87` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/assisted-living-hawaii-hud.tsv` | 13,292 | `571d0e2e5b27123ddda354d47f248f161189dd55072dbef8b752dbbc12d71b7d` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/assisted-living-north-carolina-hud.tsv` | 12,003 | `939936b28f6b4d3c2430f97ccc4ffae4283789dd80f4aa3d55b7e7859eb1d987` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/auto-service-new-jersey-sba.tsv` | 18,115 | `287abde06a448754dd3f4e59966f5909b286600f9b8204eded89ef9577b7d5a0` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/behavioral-health-massachusetts-conventional.tsv` | 13,327 | `d2e3a2eb474408a3799f0f75d6c1f9657b438e146f156cc376067f01b356c9ef` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/car-wash-port-charlotte-florida-sba.tsv` | 21,899 | `a4bd7dab8ae29a2b2d738a52f060636ac27fe7c4b22c4003c9e0538f2cb9ea1d` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/childcare-gonzales-louisiana-sba.tsv` | 15,564 | `9ae50b6d6ed251c0949ad181108be508ec654c9ea6a95eb880e00a9e8a144997` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/childcare-illinois-sba.tsv` | 13,061 | `befc03bd183f86a8b84e808650a08d07d83536d489ba5866377c13ceb31b9ea2` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/childcare-iowa-sba.tsv` | 10,974 | `79af1cb96d7534b912c541642ed313c443829124ba87ab210732531e4a8003bb` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/coffee-shop-washington-sba.tsv` | 11,971 | `f1c75a09b3bbd347afacf309821a1c2db29bb85c8a9daae1602dbe998824218c` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/fitness-minnesota-sba.tsv` | 14,806 | `df329563cefeb37ff7aecb2e3272ad55f02b8125779bdb44d773d155bcab38ea` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/fitness-new-hampshire-sba.tsv` | 26,509 | `8dec6f3dd9d8e65c362a4fba0e11a3f48e5cd32b15cfc4f54506e4a439836eec` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/funeral-home-wisconsin-sba.tsv` | 8,929 | `1f61d12d1fe44771891bb4fc05d6b13c8884908136db4f987bd06bc083991036` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/glamping-utah-usda.tsv` | 17,702 | `bf1cc7e07620f54a723ce9bfb05c5c82b0e625cf6f21de08e2c1062e886491a4` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/grocery-store-mississippi-usda.tsv` | 14,190 | `5c87ee6393447bff8a418a6906280e25c68bd567458c5a93ac83d821118898e2` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/grocery-store-ness-city-kansas-usda.tsv` | 18,656 | `c1a767133df6957edbe3fb5498c3601e5fffc6c37b00f345486c611d8c77e0cd` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-acquisition-fairlawn-ohio-sba.tsv` | 14,285 | `8fd5fb695a87240cc69edb4deb14bbd4c8cee22d71aed64076344f9c96081a5d` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-florida-sba.tsv` | 17,827 | `1ee7cec33fc5d619ca0d9bf7ce11bc9abb1358fb7f4990aa364291ed96eccba3` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-georgia-sba.tsv` | 20,136 | `813b8db57a7dbe298fc308fa515d21ec50f96c3024f21f09514b5603280f6bb9` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-hays-kansas-usda.tsv` | 10,338 | `b581944b96ae594635e0f0f2b3e1e9503a69f59db233756b776217b89e684a10` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-natchitoches-louisiana-eb5.tsv` | 19,371 | `af215f5b14fe4ab4ce025ac9cfe80db549b086a8ef1032e9790070d3f3c550af` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-nevada-eb5.tsv` | 8,915 | `9955e5a4be9a1bc068ca6e44eda8ab6bdcf95234afe2cb4165bafd7227ae39c6` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/hotel-south-carolina-sba.tsv` | 16,023 | `034c1347c904332ac2342cc9ebf5dc16daffd92e1ab6025f82809ac364f6ee5e` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/industrial-flex-gardner-kansas-conventional.tsv` | 17,639 | `c9f5697ec71c3d3e0b4bd3b2e462b1f0b6581436476e61b155cc542c313bb424` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/laundromat-acquisition-huron-county-ohio-sba.tsv` | 15,908 | `ccbfa65f8ea11029b2712655748429a4ec78786de73c402251a8ec97e6277b7f` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/laundromat-new-mexico-sba.tsv` | 11,731 | `bb63dc8273fdd69a9fbbfc73f7e1484517817b60024ffe6b68fcfdeb54343e07` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/marina-gig-harbor-washington-sba.tsv` | 19,327 | `b73811679f4adc180d36ab02654a1c68d539d8f4fd973014be79897a027554e3` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/marina-maryland-sba.tsv` | 12,820 | `d96c6a64b67bb04b1c1e1ccdbed06b528a6fbcf73ee9b18f77c9ec5f8e400772` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/marina-new-baltimore-michigan-sba.tsv` | 11,615 | `de16c75c55bd358ed8d2728a475be7a0e4785964384575f0609e15bd50785f48` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/marina-shell-knob-missouri-usda.tsv` | 11,865 | `0fb4eaf1eb696dc918af3da4b6100b68a419e503bf8343e23a0f5eaa90fe1e27` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/meat-processing-georgia-usda.tsv` | 11,157 | `b5dbe8ecc7afcc96ee2e474d01484447f1360ee92ea3b5dcb0d78a010a5faa80` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/meat-processing-north-carolina-usda.tsv` | 12,572 | `0dae516b3cdfb381c8143d7beff1b90ae978705f73b4f345ca611bc646abc7e2` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/medical-office-lebanon-tennessee-sba.tsv` | 20,096 | `fa4d4af15b759c2ca4db96a283454c1fe35ae1cfb0132bcfe048a7f6d8ed2a61` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/medical-office-north-carolina-sba.tsv` | 12,153 | `bd0cc18e5d88922ca5ff78090208840da58bd4a7bab454e7387898165c371bc8` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/mixed-use-multifamily-euclid-ohio-eb5.tsv` | 13,575 | `71129223954d5a9980c4be60aa1f93e8309df430757cae112eab2d425d427f7d` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/multifamily-arizona-agency.tsv` | 15,352 | `8f4fe13bb60e73bb7d0b1facdc0e77a3aacad53998806efc38aeedf2807d626c` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/multifamily-clarksville-tennessee-dscr.tsv` | 15,412 | `ab259b8690df8de1f44d76daaf761931b9433e8cafdb7a9cb5f25f30594f7377` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/multifamily-florida-agency.tsv` | 11,797 | `c87e9e6f8e4ced2eeeff95a8fc46e20f76a4dcc53747c815c97fb942ed973dce` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/multifamily-georgia-agency.tsv` | 13,315 | `e5e3588393787af2181c5f1a026ed325483b71a76d896537f0e13332fad78096` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/multifamily-new-york-agency.tsv` | 15,166 | `871f7b26dc0ff167e2d8e466c86b7ab6049bba35739d1f6c212fc03c4c33c3ad` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/multifamily-north-carolina-agency.tsv` | 9,818 | `6fca9929d2aca2746ff939fc35d699a106ba6719e2d16db748017d5e541be90f` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/pet-boarding-oregon-sba.tsv` | 11,520 | `c2fed1f2e714f85854915359fed787df2f6f42425bcbbd35a48a073756d6aae3` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/private-school-connecticut-conventional.tsv` | 9,342 | `94cf4bbcb08f9bd69fa97898491235c422ca5c2358732135b5a671dc7530ca02` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/qsr-arkansas-sba.tsv` | 8,661 | `b8ae920392a90e7cfe509933189f992ab8252babbe9ec12cfff1faebb93eaae5` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/qsr-georgia-sba.tsv` | 15,521 | `e86d36d1a701d041ed305e743b985eaa4255e50d3aa9f6745b625e27586585d2` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/restaurant-acquisition-broussard-louisiana-sba.tsv` | 16,227 | `567a218acb93255a605055b037018843cdcc85dc257f77c692769eaabfa2ec2b` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/restaurant-missouri-sba.tsv` | 13,164 | `a4ccc235e6963d58ff75658b750dca64020fcadd64c1dba1e9834c99514a5b70` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/restaurant-sevierville-tennessee-sba.tsv` | 15,785 | `80c35cd94380ec5e52677603f71ce05512ed177a8b182b766ba03b2cee976437` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/retail-nevada-conventional.tsv` | 10,039 | `b4218b192d9af011603cb3526582057bfa39dc36349bc92100652a34ab145a23` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/retreat-center-kerhonkson-new-york-usda.tsv` | 9,437 | `d80922ab63c2b9f84b18dfa7f20c2b3b4526a94801aa52398ca09525e18f690e` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/rv-boat-storage-arizona-sba.tsv` | 17,850 | `d2e6fcf39dc98d4a5e0794b862fff83fe721c139224f7dab3761c27f34c5de19` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/rv-boat-storage-california-sba.tsv` | 14,330 | `4f6faca9e3d196e2635d0f7743bd8010729421b723e5876003ad26c1a30a033f` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/rv-boat-storage-florida-sba.tsv` | 17,157 | `d50e4400c36856469f599741fb053645555ea74d6b6453cdbebf901c539d414b` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/rv-park-arizona-usda.tsv` | 11,569 | `aaa8eda4c6847fa3c0eef96c1d047426b97371c63022fb7fd1f366c9cb4e97fc` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/rv-park-maine-usda.tsv` | 9,579 | `7438443dfbffe6bff0d89637fcd320d6eec8e24df14f1f0d2a6fc7a97be741d3` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/rv-park-pennsylvania-usda.tsv` | 10,674 | `55f12ec67fa01dc70d9d33b7aebff9788ddaeed50e873cc47248c7602dfc1ea7` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/self-storage-arizona-sba.tsv` | 19,336 | `d1968aca1652e4014b863db5ed3d20e4d332ad41ce4eb2c861ee00ca70e633e1` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/self-storage-bardstown-kentucky-usda.tsv` | 17,264 | `5a42ff23dcb8477d02f3632f2d3149267a61b25eaf6023d1f1a07c7756d46f98` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/self-storage-indiana-sba.tsv` | 14,024 | `07648447cb94c6ed82f927926046d0074e2aa2c045ce93fd28fccbe46b6dbb63` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/self-storage-pataskala-ohio-sba.tsv` | 13,290 | `b30fc97e0921f405c5b931eeae84144413a1d9d9c456bdf4996d8495bf26aea2` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/short-term-rental-yucca-valley-california-conventional.tsv` | 15,673 | `d20e03ec28f2578f5a2c714ebbc3329cf54a86b8c4441a0220f7988db64f8712` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/truck-stop-georgia-sba.tsv` | 18,291 | `9f5e7def794cd144733308f540dc2d73f17f2fa0e2c3b776d4e371ba7be81965` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/truck-stop-oklahoma-sba.tsv` | 16,632 | `14b62aeea7dc9602264dd6f1f320f1f1764dd40675e3401a3d37590d511bbd23` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/urgent-care-elizabethtown-kentucky-sba.tsv` | 14,900 | `bfee098e42bfcf0997f379ee6148509005de09b4fffcefa6f5bb827b47c47156` |
| `docs/rollout/cloud-handoff/case-new-1/_freeze/precount-rows-PRIVATE/urgent-care-florida-sba.tsv` | 12,056 | `434e77cc0c48148549e9128dd35eef22cbcece04aaccf3f93de01cebe7cd9923` |

### C. Similar: notes, reviews and an attack file that repeat their own case's subject identifiers: 14 files, 88,348 bytes

| Path | Bytes | sha256 |
|---|---|---|
| `docs/rollout/cloud-handoff/case-new-1/_freeze/attack-A.md` | 13,147 | `62bd657032640392354fc2688bbf51ac1da4fc723331948b7cf96cc9780d53ef` |
| `docs/rollout/cloud-handoff/case-new-1/_records/tranches/t1-pages/restaurant-acquisition-broussard-louisiana-sba/writer-notes.txt` | 5,710 | `401c0994121eab746b451fc1716aefd277fafc5e163bbfadf59b587b919472a0` |
| `docs/rollout/cloud-handoff/case-new-1/_records/tranches/t1-pages/self-storage-bardstown-kentucky-usda/writer-notes.txt` | 4,384 | `246524b24837e7b0cf9570213bca2fae6797731cc104dcf1db72a669ca42414b` |
| `docs/rollout/cloud-handoff/case-new-1/_records/tranches/t1-pages/urgent-care-elizabethtown-kentucky-sba/writer-notes.txt` | 5,803 | `ba02207b276cce11aa3138f9f5047f8b65ee53566817a5713697f382a01c977f` |
| `docs/rollout/cloud-handoff/case-new-1/_records/tranches/t2/grocery-store-ness-city-kansas-usda/writer-notes.txt` | 6,460 | `981e7e3c7a6a8dbd30f2b9e2086c89b8504bba1f58cb2413faed392da813b57f` |
| `docs/rollout/cloud-handoff/case-new-1/_records/tranches/t2/medical-office-lebanon-tennessee-sba/review.md` | 4,817 | `f3342476c0e4fd40c2b57f74bc2605b763aa1a984c82a76c693e187a75d6a4c2` |
| `docs/rollout/cloud-handoff/case-new-1/_records/tranches/t2/restaurant-sevierville-tennessee-sba/writer-notes.txt` | 7,663 | `8a94814c29a1d63bd83971ef5646ec5ee107b0385897b783be38f52439b8a4ec` |
| `docs/rollout/cloud-handoff/case-new-1/childcare-gonzales-louisiana-sba/writer-notes.txt` | 5,527 | `5a5e89440d96437b46307a28bbb4b19965e8ac6cdbd17450fb3e6c0542682492` |
| `docs/rollout/cloud-handoff/case-new-1/grocery-store-ness-city-kansas-usda/writer-notes.txt` | 6,460 | `981e7e3c7a6a8dbd30f2b9e2086c89b8504bba1f58cb2413faed392da813b57f` |
| `docs/rollout/cloud-handoff/case-new-1/medical-office-lebanon-tennessee-sba/review.md` | 4,817 | `f3342476c0e4fd40c2b57f74bc2605b763aa1a984c82a76c693e187a75d6a4c2` |
| `docs/rollout/cloud-handoff/case-new-1/restaurant-acquisition-broussard-louisiana-sba/writer-notes.txt` | 5,710 | `401c0994121eab746b451fc1716aefd277fafc5e163bbfadf59b587b919472a0` |
| `docs/rollout/cloud-handoff/case-new-1/restaurant-sevierville-tennessee-sba/writer-notes.txt` | 7,663 | `8a94814c29a1d63bd83971ef5646ec5ee107b0385897b783be38f52439b8a4ec` |
| `docs/rollout/cloud-handoff/case-new-1/self-storage-bardstown-kentucky-usda/writer-notes.txt` | 4,384 | `246524b24837e7b0cf9570213bca2fae6797731cc104dcf1db72a669ca42414b` |
| `docs/rollout/cloud-handoff/case-new-1/urgent-care-elizabethtown-kentucky-sba/writer-notes.txt` | 5,803 | `ba02207b276cce11aa3138f9f5047f8b65ee53566817a5713697f382a01c977f` |

