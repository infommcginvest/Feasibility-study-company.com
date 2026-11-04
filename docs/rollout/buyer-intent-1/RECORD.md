# BUYER-INTENT-1: buyer intent on the 33 existing asset-class pages (CLOUD-1 Track D)

Owner amendment 1 to FSC-CLOUD-1 (30 Oct 2026): retrofit buyer intent onto every asset-class hub and asset-class page already on main, targeting "[subject] feasibility study consultant" and "[subject] feasibility study company" alongside "[subject] feasibility study", so each page reads as a firm the visitor can hire. Branch `cloud/buyer-intent-1`, cut from main `1559002d`. Not landed: the integrator lands it on the Mac.

## What changed, and only that
- Elements: the title, the H1, the meta description, the opening paragraph and the call to action (hero button text, closing band heading, paragraph and button), edited in place. On legacy pages the og and twitter title and description mirrors follow the new title and description; on sourced pages the JSON-LD name and description follow from the front matter. Nothing else: no URL or slug, no body section, table, figure or link target changed; no new figure; every number in a changed element is already on its page with the same value, period and citation. Every element, before and after: `BUYER-INTENT-1.tsv` (334 rows, 33 pages; a newline inside a cell is written `\n`).
- 10 sourced pages (sources under `src/pages/asset-classes/`, front matter and opening edited, `updated` set to "DEPLOY", ruling 12): gas-station-and-c-store, its ev-charging and interstate-highway subtypes, hotel, mixed-use, multifamily, private-school, quick-service-restaurant, its burger subtype, self-storage.
- 1 sourced page left as it is: skilled-nursing (the pilot's header already meets the rule; `updated` not reset).
- 22 legacy hubs (served HTML with no source; the integrator owns served HTML, I104): edited by `legacy/retrofit_legacy.py` from the exact before and after texts in `legacy/specs/*.json`. Assisted living and memory care, auto dealership, auto service and collision, behavioral health, childcare and daycare, coffee shop, express car wash, fitness and recreation, funeral home, glamping, grocery store, laundromat, marina, medical office and ASC, pet boarding and daycare, restaurant, retail, RV and boat storage, RV park and campground, truck stop and travel center, urgent care, veterinary practice.

## For the integrator at landing
1. Merge the branch (sources and records).
2. Run `python3 docs/rollout/buyer-intent-1/legacy/retrofit_legacy.py <tree> --date <landing date>` BEFORE the chain. It checks all 22 pages before writing any; each "before" must occur exactly once, a half-applied or changed page stops the run, a bare `--date` or a date earlier than a page's current date stops it, and a second run changes nothing. It sets each changed page's visible Updated line, its JSON-LD dateModified and so its sitemap lastmod to the landing date (ruling 12; gate 12 green).
3. Chain, gates. Expected: as in `gates/GATES-d-f2.txt` below.
4. Integrator item (mesh, review findings A1-18 and A2-2, confirmed): `scripts/mesh.py` prints each hub's H1 as the anchor of its generated related-hub links, so with the new H1 form ("<Class> Feasibility Study Consultants") 28 pages show that phrase more than three times in visible text (I89), all of it inside generated mesh regions; none did at baseline. Fix on the integrator side: render hub anchors as the class name (strip a trailing " Feasibility Study Consultants" as `state_name` strips " Feasibility Studies", or add a short label per hub), or rule that I89's cap excludes generated regions. Not changed here: scripts and `data/mesh` are integrator-owned.

## Gates (throwaway copies of the branch; `gates.py --stage landing --site-wide` on the 33 URLs, gate 13 at 1440 and 390)
| Run | Copy | Result |
|---|---|---|
| Baseline (main, unchanged) | `GATES-d-base.txt` | 11/14 (gate 13 not run); gates 3 and 7 red |
| Freeze 1 (writers' text) | `GATES-d-f1.txt` | 12/14; gates 3 and 7 red |
| Freeze 2 (after the verifier's fixes) | `GATES-d-f2.txt` | 12/14; gates 3 and 7 red |

- The gate 3, gate 7 and gate 9 detail is identical, line for line, between the baseline and freeze 2: the retrofit adds no red line, removes no counted figure from any page and costs no page an inbound link. The two red gates are the legacy hubs' recorded reds (INT I3, I4; SITE-REMAINING-1 section 9), owed to their rebuilds, among them the RV park hub's counted 0 (its first-screen $10.9 billion also prints on two RV park cases; review A1-14).
- Gate 4: against the baseline, the maximum overlap fell on 23 pages, stayed equal on 10 and rose on none; the highest is 4.54% (fitness and recreation, retail), under 15%.
- Gates 1, 2, 5, 6, 8 (lists available in the cloud), 9, 10, 11, 12, 13 and 14 green.

## Review (freeze 1, `reviews/`)
- Attacker 1 (Opus; figures, claims, the rule): 1 BLOCKER, 3 MAJOR-FACTUAL, 1 MAJOR-NONFACTUAL, 14 MINOR.
- Attacker 2 (Opus; sameness, frames, the script, mirrors, dates): 0 BLOCKER, 0 MAJOR-FACTUAL, 12 MAJOR-NONFACTUAL, 5 MINOR.
- Cold verifier (Sonnet, default REFUTED; `reviews/d-f1-verifier.md`): confirmed BLOCKER 1 (A1-1: an uncited "120-position" in the interstate subtype's opening), MAJOR-FACTUAL 4 (A1-2 to A1-4: openings saying the study values the business where the body says the firm supports the appraisal; A1-10: a truck stop lender claim), MAJOR-NONFACTUAL 14 (shared description, opening and CTA frames, two 8-word runs, the laundromat description's keyword stuffing, the mesh item), MINOR 7; refuted 9 (A1-11, A1-12, A1-13, A1-15, A1-16, A1-17, A2-13, A2-14, A2-16). It also refuted the coordinator's claim that every changed page's overlap fell (23 fell, 9 equal at freeze 1).
- Resolution: the verifier's tested fixes were applied (9 source edits, 76 legacy spec edits; `reviews/d-f1-verifier-fix.py`), and the script's two date gaps (A2-17) were closed. After the fixes: no figure added and every citation kept, no shared 8-word run against any served page, meta 146 to 159 characters on the fixed pages (140 to 160 on all 33), mirrors equal on all 33, keyword forms at most three across the five elements. Freeze 2 hashes: `freeze/FREEZE-d-f2.txt`; gates rerun in full on freeze 2.
- Left open (MINOR, recorded): the car wash and funeral home descriptions share a sentence skeleton (verifier V-2; every rewrite tried reproduced a third page's frame); four 7-word runs that predate the fixes (listed in the verifier file).
