# Batch 1: four market-led case studies, the About page and the site-wide byline

Built October 10, 2026 from four market deep searches. All figures are sourced and dated on each page.

## Files

| File | Target URL | Words (approx.) |
|---|---|---|
| case-studies/rv-park-ossipee-new-hampshire-usda.md | /case-studies/rv-park-ossipee-new-hampshire-usda/ | 2,900 |
| case-studies/cabin-resort-townsend-tennessee-sba.md | /case-studies/cabin-resort-townsend-tennessee-sba/ | 2,750 |
| case-studies/glamping-oak-hill-west-virginia-usda.md | /case-studies/glamping-oak-hill-west-virginia-usda/ | 2,650 |
| case-studies/dry-stack-cape-coral-florida-sba.md | /case-studies/dry-stack-cape-coral-florida-sba/ | 2,850 |
| about/about.md | /the-practice/ (replaces the current page) | 1,750 |
| byline/byline-spec.md | Template and data change, not a page | |

Each file carries front matter: title tag, meta description, slug, H1, asset-class, state and program links, dates and schema types. `{{byline}}` and `{{signature}}` are template tokens resolved from the author record (see byline-spec.md).

## Wiring to do when the files go into the repo

1. **Asset-class hubs link their cases.** The RV park page currently links none of its four RV park cases, and the marina page links none of its marina cases. Add a "Worked cases" block to:
   - /asset-classes/rv-park-and-campground/: Ossipee NH, plus the Maine, Pennsylvania, Texas and Arizona cases
   - /asset-classes/glamping/: Townsend TN, Oak Hill WV, plus the Utah case
   - /asset-classes/marina/: Cape Coral FL, plus the Maryland case
2. **State pages.** New Hampshire and Florida exist; add each new case to them. Tennessee and West Virginia have no state page yet. Until those pages exist, the new cases link to /states/ instead.
3. **Case index.** Add all four to /case-studies/ and to sitemap.xml with lastmod 2026-10-10. The sitemap's lastmod dates are frozen in July.
4. **Homepage counters.** The homepage says "12 State Practice Profiles" and "25 Asset Classes". The site has 32 state pages and 28 asset classes, and will have 64 worked cases after this batch. The About page uses 28, 32 and 64. Set the homepage to match, ideally generated at build time.
5. **Byline.** Implement the author record and display rule in byline-spec.md on every page type listed there.

## Before the credentials go live

Both About-page research briefs searched the Appraisal Institute, CCIM, appraiser-registry and dissertation trails for Mark Otava and found no public record. The About page and the byline template therefore keep the Ph.D., CCIM and MAI as slots that display only when each has a working public verification link. Fill the links in the author record and the credentials appear everywhere at once.

## Quality checks run

- No mention of the sister firms or the original research subjects.
- Every financial figure was recomputed by script and cross-checked against the tables.
- Sources that were themselves competitor pages were dropped. Figures the briefs flagged as unverified, such as a 2025 Fayette County spending figure, are not used.
