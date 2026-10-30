# BUYER-INTENT-1 resume (CLOUD-1 Track D, 30 Oct 2026)

- State: closed in the cloud and ready for the integrator. Branch `cloud/buyer-intent-1`, one pull request to main, not merged. Record: `RECORD.md`.
- Freeze 2 is final: 10 sources committed under `src/pages/asset-classes/`, 22 legacy hubs as `legacy/retrofit_legacy.py` plus `legacy/specs/`, every change in `BUYER-INTENT-1.tsv`.
- Landing (Mac integrator): merge, run the legacy script with `--date <landing date>` before the chain, chain, gates (expect `gates/GATES-d-f2.txt`: 12/14 with the legacy hubs' recorded gate 3 and 7 reds unchanged), deploy as usual.
- Open: the mesh anchor item (RECORD.md, "For the integrator", 4) and the MINOR description pair (V-2).
- A later session that edits any of these 33 pages first checks that the retrofit landed (the H1 reads "<Class> Feasibility Study Consultants" on the live page); if the legacy script refuses a page because its served text changed, regenerate that page's spec from the live page.
- Pull request: refused twice by GitHub for this session's integration (403 "Resource not accessible by integration", 30 Oct). The branch is pushed; the integrator lands from it. Compare link: https://github.com/infommcginvest/Feasibility-study-company.com/compare/main...cloud/buyer-intent-1?expand=1 ; description: `docs/rollout/buyer-intent-1/RECORD.md`.
