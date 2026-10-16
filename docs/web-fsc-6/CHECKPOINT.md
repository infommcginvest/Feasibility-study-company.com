# WEB-FSC-6 generator-ready checkpoint (ruling 15)

Recorded 2026-10-16. The factory renders the Texas state page and the first case (gas station, Lockhart, Texas, SBA 7(a)),
and both pass gates 1 to 6 and the look gate. Evidence was taken on a clean `git archive` of the committed tree
(no uncommitted writer files present), so nothing in progress elsewhere in the worktree affected it.

| Gate | Texas state page | Lockhart case |
|---|---|---|
| 1 one title; JSON-LD parses; BreadcrumbList; author @id | yes | yes |
| 2 build.py --check / casemodel.py --check | rc 0 | rc 0 (case) |
| 2 mutation tests (archive copy, reverted, nothing committed) | source text changed: --check rc 1, revert rc 0 | input land x1.1: --check rc 1 ("stale region v.loan_total_proposed"), tables moved, revert rc 0 |
| 3 unique dated sourced figures (min 25) | 70 | 59 |
| 4 max 8-word shingle overlap (under 15%) | 0.86% | 1.57% |
| 5 standalone metros | n/a (no metro in the pair) | n/a |
| 6 case standard v3 | n/a | all 17 sections, all 12 model tables, disclosure under H1 and byline, every competitor row with a confirming URL, 5,470 body words; Year 2 DSCR 1.152 against the 1.15x floor at 54.4% equity (tier 10%), loan under the $5,000,000 limit |
| byline.py / regulatory.py --check | rc 0 | rc 0 |
| look: 1440 and 390, page-level overflow | none at either width | none at either width; wide tables scroll in their own box |

Engine fix found by the mutation test: a proposed 7(a) loan above $5,000,000 had no FY2027 fee tier and stopped the
engine; it is now charged on the top tier's terms, fails the size test and is restructured under the limit.

How a roll-out lane adds a page or a case: src/README.md.
