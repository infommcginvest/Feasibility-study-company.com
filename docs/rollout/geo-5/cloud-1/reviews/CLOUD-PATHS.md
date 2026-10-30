# Path map for GEO-5 reviews run in the cloud session (CLOUD-1)

The GEO-5 review brief was written for the owner's Mac. Read its Mac paths as these cloud paths:

| Brief says | Read here |
|---|---|
| `~/Downloads/fsc-rollout/drafts/geo-5/` (research, facts, assign, pages, reviews, tools, briefs, FREEZE and GATES files from the Mac) | `/home/user/wt/geo-5/docs/rollout/cloud-handoff/geo-5/` (READ ONLY) |
| `~/Downloads/wt-rollout-geo-5` (the live site, local main) | `/home/user/wt/geo-5` (READ ONLY; branch cloud/geo-5 = GitHub main 1559002d, which equals the owner's local main 22987c4, plus one plan file) |
| the frozen copy `~/Downloads/fsc-rollout/tmp/geo-5/<t>/` | `<scratchpad>/copies/f1-<state>/` (READ ONLY) |
| the freeze record | `<scratchpad>/freeze/geo-5/FREEZE-<state>-f1.txt` |
| gate output at READY (DC and Vermont, cloud run) | `<scratchpad>/copies/GATES-f1-<state>.txt` and `-g13.txt` |
| where you write your findings / verifier files | `<scratchpad>/reviews/geo-5/` |
| `drafts/geo-4/tools/SEO-BRIEF.md` (taken frames) | not in the cloud; use `/home/user/wt/geo-5/docs/rollout/cloud-handoff/geo-5/SEO-BRIEF.md` and the landed state pages under `/home/user/wt/geo-5/src/pages/states/` |
| `tools/to <seconds> <cmd>` | `timeout <seconds> <cmd>` |
| a gate rerun | from inside the copy: `FSC_PRIVATE=<scratchpad>/private timeout 900 python3 scripts/qa/gates.py --root . --git-dir /home/user/wt/geo-5 --urls /states/<state>/ --stage ready --only <n> --skip-look` |

Facts that differ from the brief:
- The ND and Alaska frozen sources are byte-identical to the Mac's freeze 1 (sha256 in the FREEZE files), now rendered on the current site (main 1559002d, 211 URLs, which adds the seven CASE-NEW-1 cases and South Dakota since the Mac freeze).
- Never write inside `/home/user/wt/*` or `/home/user/feasibility-study-company.com`. Never run git commands that change anything. Write only your one findings file (verifier: the two files it names) into the reviews folder above.
- Network: WebFetch and WebSearch only, read-only. A 403, 429, robots refusal, bot check or paywall is recorded NOT FETCHED with its reason and never worked around. Never fetch anything on www2.census.gov.
- No em or en dashes in anything you write.
