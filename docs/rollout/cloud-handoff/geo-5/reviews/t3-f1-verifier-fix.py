# GEO-5 t3 freeze 1 verifier fix list. Paths are relative to drafts/geo-5/pages.
EDITS = [
    # A1-2 + A1-3 (FAQ 5): one-bedroom label; drop the misattributed sample caution
    ("south-dakota.html",
     "its July 2025 survey had market-rate vacancy at 5.43% and an average rent of $1,002, excluding properties in lease-up [^12]. The two samples differ, so a study for a new building treats them as readings,",
     "its July 2025 survey had market-rate vacancy at 5.43% and an average one-bedroom rent of $1,002, excluding properties in lease-up [^12]. A study for a new building treats them as readings,"),
    # A1-2 + A1-3 (#sioux-falls Apartments)
    ("south-dakota.html",
     "Its July 2025 survey had market-rate vacancy at 5.43% and an average rent of $1,002, excluding properties in lease-up [^12]. The two surveys cover different samples, and the association's own caution about comparing them applies; an apartment study treats them as readings,",
     "Its July 2025 survey had market-rate vacancy at 5.43% and an average one-bedroom rent of $1,002, excluding properties in lease-up [^12]. An apartment study treats them as readings,"),
    # A1-4 + A2-3 (#rapid-city): the MSA composition is uncited and contradicted by the county rows
    ("south-dakota.html",
     "Pennington, Meade and Lawrence counties, the Rapid City metro area as the Labor Market Information Center draws it, all inside South Dakota.",
     "Pennington, Meade and Lawrence counties, all inside South Dakota."),
    ("south-dakota.html",
     "The metro area had 74,312 covered workers in 2025",
     "The Rapid City metro area had 74,312 covered workers in 2025"),
    # A1-5 + A2-5 (#rapid-city): Fall River does not border Pennington
    ("south-dakota.html",
     "for Pennington County, and its neighbors Custer and Fall River [^38].",
     "for Pennington, Custer and Fall River counties [^38]."),
    # A2-1: nothing sources "stands until the annual summary"; NASS's own schedule shows a November 10 release
    ("south-dakota.html",
     "The October 9, 2026 crop forecast stands until NASS's annual summary replaces it, and the sales tax reduction sunsets",
     "The sales tax reduction sunsets"),
    ("south-dakota.html",
     "A study dated between those two events cites the forecast as it stands and states the sales tax rate its first full year assumes. With the project",
     "With the project"),
    ("south-dakota.html",
     " Once NASS publishes its annual summary, that replaces the October forecast in the study.",
     ""),
    # A2-2: the release counts visitors "to and within" the state and gives no origin
    ("south-dakota.html",
     "that share of its sales tax from people who do not live in it is a state",
     "that share of its sales tax is a state"),
    # A2-4: the 504 equity rule is misstated (a new business on special purpose property is 20%; campground is not on SBA's list)
    ("south-dakota.html",
     "standard coverage, and a 504 borrower that is a start-up, or that builds a single-use property such as a hotel or a campground, contributes <!--sba:equity.sba_504_new_or_special.value-->15%<!--/sba:equity.sba_504_new_or_special.value--> equity [^81].",
     "standard coverage [^81]."),
    # A2-6: "written to the program's requirements" follows an SBA paragraph and reads as an SBA requirement (ruling 8)
    ("south-dakota.html",
     "an independent, lender-grade study written to the program's requirements, with every figure traced",
     "an independent, lender-grade study with every figure traced"),
]
