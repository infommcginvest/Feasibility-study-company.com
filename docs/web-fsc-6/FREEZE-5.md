# WEB-FSC-6 freeze 5 (landing freeze)

- Content commit: b1491ae292aa94a5eaeec4592394fc77c4f223cc (branch web-fsc-6), which contains main 5f9311f (WEB-FSC-4 and WEB-FSC-5 landed).
- Gate record: docs/web-fsc-6/GATES.txt, run at b1491ae on a clean worktree: 14 of 14 green. This record commit adds only GATES.txt and this file.
- Since freeze 4 (4982fd8): WEB-FSC-5 landed on main during the land step; main merged again (901e93a), the ruling 14 chain rerun over the whole tree including scripts/markets.py (no page changed), and all fourteen gates rerun (D39). The markets register is build input and is excluded from the deploy tree with docs and src (D40).
