# WEB-FSC-5 step zero (2026-10-16, 09:20 to 09:40 UTC)

Paths are written relative to the home directory (`~`) on purpose.

## 1. Repo and head

- `git -C ~/Downloads/Feaisbility-Study-Company.com fetch origin`: exit 0.
- `main` = `origin/main` = `1d48cc284330272952083fc91119dd22ee66cb57` (`1d48cc2`); `git rev-list --left-right --count main...origin/main` = `0 0`.
- Local `main` has not moved past `1d48cc2`. Cut point: `1d48cc2`.
- `coreutils timeout` is not installed on this Mac; timeouts are applied with `perl -e 'alarm N; exec @ARGV'`, curl `--max-time` and the Python socket timeout.

## 2. Twin guard

Git arm:
- `git worktree list --porcelain`: the main checkout (branch `web-fsc-2` at 1d48cc2) and `~/Downloads/wt-web-fsc-4` (branch `web-fsc-4` at ebd2f8a). No `wt-web-fsc-6` yet.
- Lock files in the git dir: only the zero-byte `stale-index-lock` and `stale-maintenance-lock` (left alone). No `index.lock` anywhere.
- Branch `web-fsc-5`: absent. Path `~/Downloads/wt-web-fsc-5`: absent.

Process arm:
- Claude Code CLI processes (Electron helpers under `/Applications/Claude.app/` excluded): two besides this session, both with their working directory at the estate root, not inside the repo or a worktree. Sessions run from the estate root, so the cwd arm cannot attribute a process to a lane by itself.
- Second discriminator: a grep of every transcript for the charter title line `CHARTER WEB-FSC-5` found two files: this session's, and the WEB-FSC-6 session's (its own charter quotes the title; its first user message is `CHARTER WEB-FSC-6`). No other session holds this charter.
- Verdict: no live twin. WEB-FSC-4 in its own worktree is expected.

## 3. Hosts (GET with a 30 to 60 s timeout, User-Agent `FSC-MarketsRegister/1.0 (... contact info@feasibility-study-company.com)`)

| Host | Probe | robots.txt | Verdict for this lane |
|---|---|---|---|
| api.census.gov | `/data.json` 200 (5.2 MB) | HTTP 200, a 247-byte WAF "Request Rejected" HTML page, no robots groups | robots allows; **every data request is refused by a key wall**: HTTP 302 to `/data/missing_key.html` with `X-DataWebAPI-KeyError: 1` ("A valid key must be included with each data API request"), confirmed on acs/acs5 2024, pep/charv 2023, cbp 2023, geoinfo 2025 and dec/pl 2020. `CENSUS_API_KEY` is not set. |
| www2.census.gov | `/` 200 | HTTP 200, 398 bytes; opens `User-agent: *`, blank line, `User-agent: RavenCrawler`, `Disallow: /` | **Disallowed for every unnamed agent.** Under RFC 9309 section 2.2 a blank line does not end a group, so `*` and `RavenCrawler` form one group with `Disallow: /`. |
| data.bls.gov | `/cew/data/files/` 403 | HTTP 200, `User-agent: *` / `Disallow: /` | **Disallowed and 403.** The identifying User-Agent BLS asks for did not change the 403. |
| apps.bea.gov | `/regional/zip/` 403 | HTTP 200, `*` group: `Disallow: /` with 15 `Allow` paths (`/api/`, `/regional/bearfacts/`, `/iTable/`, ...) | **`/regional/zip/` disallowed and 403.** `/api/` is allowed but requires a registered UserID (`BEA_API_KEY` not set). |
| www.huduser.gov | `/portal/datasets/fmr.html` 202, empty body | HTTP 202, empty, `x-amzn-waf-action: challenge` | **AWS WAF bot challenge** on every path, robots.txt included. |
| data.sba.gov | `/` 200 | HTTP 200; `*` group disallows only Drupal admin, search and README paths | **Open.** `/dataset/` and `/sites/default/files/` are allowed. |

## 4. Environment

- Free disk: 38 GB on the data volume (charter minimum 15 GB; the charter's "70 GB at issue" no longer holds).
- `CENSUS_API_KEY`: not set. `BEA_API_KEY`: not set.
- Python: `/usr/bin/python3` 3.9.6. The pipeline uses the standard library only, so no virtualenv is created.
