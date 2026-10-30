# GEO-1 requests to the integrator

Ruling 13: the lane does not edit integrator-owned files. Until FACTORY-2 publishes `docs/rollout/int/REQUESTS.md` and the `requests.json` format, the requests are listed here in prose; the lane converts them to `requests.json` once the format exists. Each tranche record says which of these it needs at its landing.

## R1. Fallbacks for folded metros (`data/mesh/fallbacks.json` "targets")

Each promised or lane-chosen metro slug that folds into its state page needs its pending links to point at the section with the slug as its id, as WEB-FSC-6 did for McAllen, El Paso, Lubbock and Corpus Christi. The section exists on the state page from that state's tranche on; request the entries with that tranche.

| Pending target | Fallback |
|---|---|
| `/states/alabama/auburn/` | `/states/alabama/#auburn` |
| `/states/alabama/birmingham/` | `/states/alabama/#birmingham` |
| `/states/alabama/black-belt/` | `/states/alabama/#black-belt` |
| `/states/alabama/gulf-shores/` | `/states/alabama/#gulf-shores` |
| `/states/alabama/mobile/` | `/states/alabama/#mobile` |
| `/states/alabama/montgomery/` | `/states/alabama/#montgomery` |
| `/states/alabama/tuscaloosa/` | `/states/alabama/#tuscaloosa` |
| `/states/arkansas/fort-smith/` | `/states/arkansas/#fort-smith` |
| `/states/arkansas/hot-springs/` | `/states/arkansas/#hot-springs` |
| `/states/arkansas/jonesboro/` | `/states/arkansas/#jonesboro` |
| `/states/arkansas/little-rock/` | `/states/arkansas/#little-rock` |
| `/states/arkansas/mississippi-county/` | `/states/arkansas/#mississippi-county` |
| `/states/arkansas/pine-bluff/` | `/states/arkansas/#pine-bluff` |
| `/states/arkansas/south-arkansas/` | `/states/arkansas/#south-arkansas` |
| `/states/florida/fort-myers/` | `/states/florida/#fort-myers` |
| `/states/florida/gainesville/` | `/states/florida/#gainesville` |
| `/states/florida/lakeland/` | `/states/florida/#lakeland` |
| `/states/florida/ocala/` | `/states/florida/#ocala` |
| `/states/florida/pensacola/` | `/states/florida/#pensacola` |
| `/states/florida/sarasota/` | `/states/florida/#sarasota` |
| `/states/florida/tallahassee/` | `/states/florida/#tallahassee` |
| `/states/florida/the-villages/` | `/states/florida/#the-villages` |
| `/states/georgia/albany/` | `/states/georgia/#albany` |
| `/states/georgia/athens/` | `/states/georgia/#athens` |
| `/states/georgia/atlanta/` | `/states/georgia/#atlanta` |
| `/states/georgia/augusta/` | `/states/georgia/#augusta` |
| `/states/georgia/columbus/` | `/states/georgia/#columbus` |
| `/states/georgia/macon/` | `/states/georgia/#macon` |
| `/states/georgia/valdosta/` | `/states/georgia/#valdosta` |
| `/states/georgia/warner-robins/` | `/states/georgia/#warner-robins` |
| `/states/kentucky/bowling-green/` | `/states/kentucky/#bowling-green` |
| `/states/kentucky/elizabethtown/` | `/states/kentucky/#elizabethtown` |
| `/states/kentucky/lexington/` | `/states/kentucky/#lexington` |
| `/states/kentucky/louisville/` | `/states/kentucky/#louisville` |
| `/states/kentucky/northern-kentucky/` | `/states/kentucky/#northern-kentucky` |
| `/states/kentucky/owensboro/` | `/states/kentucky/#owensboro` |
| `/states/kentucky/paducah/` | `/states/kentucky/#paducah` |
| `/states/kentucky/pikeville/` | `/states/kentucky/#pikeville` |
| `/states/louisiana/alexandria/` | `/states/louisiana/#alexandria` |
| `/states/louisiana/baton-rouge/` | `/states/louisiana/#baton-rouge` |
| `/states/louisiana/houma-thibodaux/` | `/states/louisiana/#houma-thibodaux` |
| `/states/louisiana/lafayette/` | `/states/louisiana/#lafayette` |
| `/states/louisiana/lake-charles/` | `/states/louisiana/#lake-charles` |
| `/states/louisiana/monroe/` | `/states/louisiana/#monroe` |
| `/states/louisiana/new-orleans/` | `/states/louisiana/#new-orleans` |
| `/states/louisiana/shreveport/` | `/states/louisiana/#shreveport` |
| `/states/mississippi/delta/` | `/states/mississippi/#delta` |
| `/states/mississippi/desoto-county/` | `/states/mississippi/#desoto-county` |
| `/states/mississippi/golden-triangle/` | `/states/mississippi/#golden-triangle` |
| `/states/mississippi/gulf-coast/` | `/states/mississippi/#gulf-coast` |
| `/states/mississippi/hattiesburg/` | `/states/mississippi/#hattiesburg` |
| `/states/mississippi/jackson/` | `/states/mississippi/#jackson` |
| `/states/mississippi/meridian/` | `/states/mississippi/#meridian` |
| `/states/mississippi/oxford/` | `/states/mississippi/#oxford` |
| `/states/mississippi/tupelo/` | `/states/mississippi/#tupelo` |
| `/states/north-carolina/asheville/` | `/states/north-carolina/#asheville` |
| `/states/north-carolina/fayetteville/` | `/states/north-carolina/#fayetteville` |
| `/states/north-carolina/greensboro/` | `/states/north-carolina/#greensboro` |
| `/states/north-carolina/greenville/` | `/states/north-carolina/#greenville` |
| `/states/north-carolina/hickory/` | `/states/north-carolina/#hickory` |
| `/states/north-carolina/wilmington/` | `/states/north-carolina/#wilmington` |
| `/states/oklahoma/durant/` | `/states/oklahoma/#durant` |
| `/states/oklahoma/edmond/` | `/states/oklahoma/#edmond` |
| `/states/oklahoma/lawton/` | `/states/oklahoma/#lawton` |
| `/states/oklahoma/norman/` | `/states/oklahoma/#norman` |
| `/states/oklahoma/pryor/` | `/states/oklahoma/#pryor` |
| `/states/oklahoma/stillwater/` | `/states/oklahoma/#stillwater` |
| `/states/oklahoma/tulsa/` | `/states/oklahoma/#tulsa` |
| `/states/south-carolina/columbia/` | `/states/south-carolina/#columbia` |
| `/states/south-carolina/florence/` | `/states/south-carolina/#florence` |
| `/states/south-carolina/greenville/` | `/states/south-carolina/#greenville` |
| `/states/south-carolina/hilton-head/` | `/states/south-carolina/#hilton-head` |
| `/states/south-carolina/i-95-corridor/` | `/states/south-carolina/#i-95-corridor` |
| `/states/south-carolina/myrtle-beach/` | `/states/south-carolina/#myrtle-beach` |
| `/states/south-carolina/spartanburg/` | `/states/south-carolina/#spartanburg` |
| `/states/tennessee/chattanooga/` | `/states/tennessee/#chattanooga` |
| `/states/tennessee/clarksville/` | `/states/tennessee/#clarksville` |
| `/states/tennessee/jackson/` | `/states/tennessee/#jackson` |
| `/states/tennessee/knoxville/` | `/states/tennessee/#knoxville` |
| `/states/tennessee/memphis/` | `/states/tennessee/#memphis` |
| `/states/tennessee/pigeon-forge-gatlinburg/` | `/states/tennessee/#pigeon-forge-gatlinburg` |
| `/states/tennessee/tri-cities/` | `/states/tennessee/#tri-cities` |

## R2. Promised URLs (`data/site/promised.json`, amendment A5)

Metro pages this lane builds at slugs that were not promised before: `/states/tennessee/nashville/`. The new states themselves (`/states/tennessee/`, `/states/kentucky/`, `/states/louisiana/`) are in the block. The other metros of Tennessee, Kentucky and Louisiana are sections, not promised pages; no promised entry is needed for them.

## R3. Markets panel (`data/site/chrome.json`)

The "Major Metros" column of the Markets panel lists Miami, Atlanta and Charlotte with fallbacks today. Requested at each landing that ships the page:

- Miami: the entry already exists (`/states/florida/miami/`); it goes live when the page lands.
- Charlotte: the entry already exists; it goes live when the page lands.
- Atlanta: folds into `/states/georgia/#atlanta` (R1); please point the entry's fallback there instead of `#metros`.
- Add, if the column has room in the integrator's design: Tampa, Orlando, Raleigh-Durham and Nashville. Their pages: `/states/florida/orlando/`, `/states/florida/tampa/`, `/states/north-carolina/raleigh-durham/`, `/states/tennessee/nashville/`.
- "By State": Tennessee, Kentucky and Louisiana are hidden until built (FACTORY-2 (d)); they go live with their tranches.

## R4. State neighbours (`data/mesh/topics.json`)

FACTORY-2 (e) adds `state_neighbors` for the new states. The lane checks them in its throwaway copy at each tranche and reports any missing pair here.

## R5. Metro pages the lane ships (for the integrator's index pages)

- `/states/alabama/huntsville/`
- `/states/arkansas/northwest-arkansas/`
- `/states/florida/jacksonville/`
- `/states/florida/miami/`
- `/states/florida/orlando/`
- `/states/florida/tampa/`
- `/states/georgia/savannah/`
- `/states/north-carolina/charlotte/`
- `/states/north-carolina/raleigh-durham/`
- `/states/oklahoma/oklahoma-city/`
- `/states/south-carolina/charleston/`
- `/states/tennessee/nashville/`
