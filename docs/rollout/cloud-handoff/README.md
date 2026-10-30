# Cloud handoff (30 October 2026)

This folder lets cloud sessions continue the FSC rollout. It is never deployed: netlify.toml removes docs/ from every git build and /docs/* answers 404.

## What is here
- geo-5/: the GEO-5 working drafts from the owner's Mac (pages, research, facts, reviews, freezes, gates, tools, briefs) for the five states not yet landed: North Dakota, Alaska, Wyoming, District of Columbia, Vermont. Start from docs/rollout/geo-5/RESUME.md.
- case-new-1/: the CASE-NEW-1 working drafts (including _held/) and its tools and records. Start from docs/rollout/case-new-1/RESUME.md and BUILD-PLAN-1.md.
- Left out: two writer-notes.txt files under case-new-1 (medical-office-lebanon-tennessee-sba, live copy and t2 record copy) because they name a sister firm's domain. Nothing else was left out; no secrets were found.

## Read first
1. docs/rollout/ROLLOUT-1.md and docs/rollout/AMENDMENT-1.md (the rulebook).
2. docs/rollout/int/SITE-REMAINING-1.md (what is still unbuilt) and docs/rollout/int/DECISIONS.md.
3. The RESUME.md of the lane you continue.

## Standing rules
- Buyer intent on every new page: title, H1, meta, opening and call to action target "[subject] feasibility study consultant" and "[subject] feasibility study company" alongside "[subject] feasibility study"; informational depth below.
- Floors and gates exactly as ROLLOUT-1 and the lane records state. Never cite or name the excluded firms in ROLLOUT-1 and the lane records. Mark Otava is the real byline.
- Cloud sessions build on branches and open pull requests only. They never deploy, never call Netlify or IndexNow, never push to main. Landing (merge, render, gates, deploy, Search Console and IndexNow) stays with the integrator on the owner's Mac.
- Commits are authored Feasibility Study Company <noreply@feasibility-study-company.com>. No em dashes.

## History
GitHub main jumped from 0374505 to one snapshot commit holding the exact tree of local main 22987c41 plus this folder (owner ruling, 30 Oct, resolving GEO-5 D9). The full local history is kept on the owner's Mac under tag archive/local-main-2026-10-30.
