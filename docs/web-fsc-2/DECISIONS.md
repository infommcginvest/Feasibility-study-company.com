# WEB-FSC-2 decisions

Logged as made. Numbered in order.

1. **Cut point.** `web-fsc-1` (56fe9af) is not merged: `main` and `origin/main` both sit at d456950. The charter says to cut from the `web-fsc-1` head in that case, so `web-fsc-2` is cut from 56fe9af. The byline system, author record and the four batch-1 cases are therefore in scope for the inventory.
2. **Redacted input copies.** The charter's constraint 2 and the fact sheet both name the sister firm's domain in order to forbid it, and gate 6 greps every changed file for those strings. A verbatim copy would fail its own gate. The committed copies replace each forbidden token with a bracketed placeholder and say so in a leading comment. The owner's originals in `~/Downloads/deep searches/fsc-sop81/` are untouched.
3. **Token file.** `.ghtoken` in the repo root is ignored by `.gitignore` and is not tracked. It was not read, per the WEB-FSC-1 rule.
4. **No live peer.** A grep of every session transcript for `WEB-FSC-2` matched only this session before work began.
