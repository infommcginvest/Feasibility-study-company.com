# GEO-5 t2, capped confirming review (I68) after the freeze 1 fixes. Paths are relative to drafts/geo-5/pages.
# One FAIL. The old text occurs exactly once in the post-fix source. No dash characters, no new figure.

VA = "virginia.html"

EDITS = [
    # Verifier edit 4 (A1-2): "North Carolina counties included [^8,9,45,46]" puts plural counties on source 8,
    # whose BLS payroll table names one North Carolina county (Currituck), and on FHFA and BEA titles that say
    # only "VA-NC". "part of North Carolina" is true for all four sources; "them" follows the noun.
    (VA,
     "publish the metro with North Carolina counties included [^8,9,45,46], so every metro-wide figure below includes them and every city figure does not.",
     "publish the metro with part of North Carolina included [^8,9,45,46], so every metro-wide figure below includes that part and every city figure does not."),
]

# Not a FAIL of any edit (outside the fixed regions, left for the integrator): two untouched sentences in the
# same section repeat the plural on single sources, "For the full metro, North Carolina counties included, BLS
# counted ... [^8]" and "FHFA's index for the Virginia Beach-Norfolk-Newport News metro, North Carolina counties
# included, read 388.95 ... [^45]". If the integrator takes them, "North Carolina counties included" becomes
# "its North Carolina part included" in each; neither is in EDITS above.
