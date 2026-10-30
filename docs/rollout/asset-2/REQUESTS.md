# ASSET-2 requests to the integrator (prose until FACTORY-2 publishes the requests.json format)

Each request names the tranche that needs it. Nothing here is a builder edit: every file named is integrator-owned.

R1 (tranche of /asset-classes/industrial-and-warehouse/). Ruling 16: a permanent 301 from `/asset-classes/industrial/` to `/asset-classes/industrial-and-warehouse/` in `netlify.toml`, in the landing that ships the hub.

R2 (tranches of the three new hubs). `data/site/chrome.json` Asset Classes panel: `/asset-classes/industrial-and-warehouse/`, `/asset-classes/cold-storage/` and `/asset-classes/data-center/` switch from pending to live when each lands (FACTORY-2 (d) adds them as pending). The `/asset-classes/` index page lists each new hub when it lands.

R3 (tranche of /asset-classes/cold-storage/). `data/site/promised.json` and the mesh: the lane-defined subtype `/asset-classes/cold-storage/public-refrigerated-warehouse/` ships in the same tranche as its hub; add it to the mesh family of `cold-storage` so generated lists pick it up. No other lane-defined subtype of the three new hubs is promised: they are hub sections.

R4 (tranches with a written subtype). Mesh entries for `/asset-classes/auto-service-and-collision/quick-lube/` and `/asset-classes/express-car-wash/express-exterior/` (promised slugs, now built), so `links.py --relink` switches their pending anchors on sitewide.

R5 (tranche of the gas station register pass). The hub `/asset-classes/gas-station-and-c-store/` changed content (SBA loan performance from the register; the travel-center section shortened so its truck stop figures belong to the truck stop hub; nine uncited sources removed and renumbered): its `updated` is `"DEPLOY"` per ruling 12, so its dateModified moves at that landing.
