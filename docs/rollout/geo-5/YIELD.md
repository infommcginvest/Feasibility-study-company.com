# GEO-5 research yield (before building)

Measured by `drafts/geo-5/tools/yield5.py` against `~/Downloads/wt-rollout-geo-5` (local main `a03f562`, what production serves), using the integrator's `scripts/qa/pagecheck.py` value and rounding rules, with every served page's sources list indexed (I71). Countable = a dated row (the Published cell carries a date), a figure pagecheck reads, market-level (not single-property, not research arithmetic), free on the served site and not shared with another GEO-5 state, one per value. This is the mechanical reading; the pre-count and the review apply I77's kinds and the secondary-row readings on top, so the page's count will be lower.

## Final table (all eight files present, 28 Oct, about 18:45Z)

| State | ST rows | MT rows | Countable (mechanical) | ST | MT | Primary | Secondary | Of the countable: periodic only, no printed date | Of the countable: FRED relays | Primary with a printed date | Undated rows | Taken by the site | Shared with another GEO-5 state |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Colorado | 89 | 184 | 131 | 32 | 99 | 86 | 45 | 0 | 30 | 86 | 0 | 105 | 23 |
| Virginia | 69 | 207 | 152 | 32 | 120 | 91 | 61 | 0 | 44 | 91 | 6 | 107 | 49 |
| South Dakota | 74 | 98 | 54 | 23 | 31 | 21 | 33 | 3 | 17 | 18 | 5 | 72 | 24 |
| North Dakota | 67 | 124 | 77 | 25 | 52 | 43 | 34 | 9 | 18 | 34 | 23 | 64 | 25 |
| Alaska | 99 | 113 | 77 | 35 | 42 | 60 | 17 | 0 | 5 | 60 | 20 | 98 | 18 |
| Wyoming | 77 | 122 | 67 | 32 | 35 | 27 | 40 | 0 | 15 | 27 | 7 | 96 | 33 |
| District of Columbia | 93 | 77 | 53 | 31 | 22 | 48 | 5 | 0 | 0 | 48 | 14 | 82 | 17 |
| Vermont | 94 | 99 | 60 | 35 | 25 | 18 | 42 | 10 | 13 | 8 | 10 | 92 | 22 |

Every state clears the READY research floor of 20 on the mechanical reading; on primary rows with a printed date alone, Vermont (8) and South Dakota (18) do not, so their pre-counts decide on the secondary readings. The tool output is `drafts/geo-5/YIELD-final.txt`.

## Closed doors, by researcher (each file's own `## Doors closed` holds the full list)

- Colorado: Census QuickFacts, CDLE, flydenver.com, fema.gov, DHSEM, Division of Insurance, CHFA, OEDIT, six news and broker hosts, Vail Resorts investor pages (403); forecast and FEMA PDFs unreadable; Matthews and FRED county pages 404. Source titles carrying em dashes were rewritten with commas (flagged for I176).
- Virginia: most *.virginia.gov hosts did not resolve; vedp.org, Census QuickFacts, FEMA, Axios, AJOT, Virginia Business, Cresa, Northmarq, Multi Housing News, Newmark (403); PDFs unreadable; BLS API daily limit.
- South Dakota: census.gov, fema.gov, drgnews.com, rcgov.org, newsfromthestates.com (403); sdvisit.com and dot.sd.gov PDFs unparsed.
- North Dakota: dmr.nd.gov, commerce.nd.gov, nd.gov news, ndlegis.gov, fargond.gov (refused); Census QuickFacts, FEMA and four news hosts (403); Treasury SSBCI 404; an SBA redirect not followed.
- Alaska: Census QuickFacts, Alaska Beacon, a FEMA page, commerce.alaska.gov, kpedd.org, a DOLWD folder (403); matsugov.us refused.
- Wyoming: Census QuickFacts, fema.gov, the WCDA PDF, USDA Rural Development, casperwy.gov (403); wyomingnews.com (451); two news hosts (429); uwyo.edu certificate error; wyoleg.gov and eadiv.state.wy.us refused.
- District of Columbia: Census QuickFacts, CoStar, Northmarq, Axios, GlobeSt, Hotel Investment Today, Avison Young, MultiHousingNews, Greater Greater Washington, fema.gov (403); Savills (429); Marcus and Millichap (sign-in).
- Vermont: fema.gov, Census QuickFacts, vhfa.org, ACCD and vermont.gov pages, Hickok and Boardman, NEREJ, Redfin (403); legislature.vermont.gov and ljfo.vermont.gov (refused).

Every researcher reports the shared web search budget ran out mid-run; none worked around a door, used an archive or fetched www2.census.gov.
