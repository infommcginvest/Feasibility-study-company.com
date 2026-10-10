#!/usr/bin/env python3
"""WEB-FSC-1 one-time wiring: case index cards, Worked cases blocks on the three
asset hubs, case links on the New Hampshire and Florida state pages, sitemap.

Labels and link text come from the owner's front matter (new cases) or from
the existing /case-studies/ index cards (existing cases). Run once; it refuses
to run twice.
"""
import datetime
import html
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from convert import CASES, INPUT, ROOT, SITE, front_matter  # noqa: E402

BUILD_DATE = datetime.date.today().isoformat()
CITE = {
    "rv-park-ossipee-new-hampshire-usda": "RV Park &amp; Campground",
    "cabin-resort-townsend-tennessee-sba": "Glamping &amp; Cabin Resort",
    "glamping-oak-hill-west-virginia-usda": "Glamping &amp; Outdoor Hospitality",
    "dry-stack-cape-coral-florida-sba": "Marina &amp; Dry-Stack",
}
HUBS = {
    "asset-classes/rv-park-and-campground/index.html": (
        "RV park and campground worked cases.",
        ["rv-park-ossipee-new-hampshire-usda", "rv-park-maine-usda", "rv-park-pennsylvania-usda",
         "rv-park-texas-usda", "rv-park-arizona-usda"]),
    "asset-classes/glamping/index.html": (
        "Glamping worked cases.",
        ["cabin-resort-townsend-tennessee-sba", "glamping-oak-hill-west-virginia-usda", "glamping-utah-usda"]),
    "asset-classes/marina/index.html": (
        "Marina worked cases.",
        ["dry-stack-cape-coral-florida-sba", "marina-maryland-sba"]),
}
STATES = {
    "states/new-hampshire/index.html": ("New Hampshire worked case.", ["rv-park-ossipee-new-hampshire-usda"], 'id="assets"'),
    "states/florida/index.html": ("Florida worked case.", ["dry-stack-cape-coral-florida-sba"], 'id="assets"'),
}


def read(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return fh.read()


def write(rel, s):
    with open(os.path.join(ROOT, rel), "w", encoding="utf-8") as fh:
        fh.write(s)


def new_meta():
    out = {}
    for slug, state, program in CASES:
        with open(os.path.join(INPUT, "case-studies", slug + ".md"), encoding="utf-8") as fh:
            meta, _ = front_matter(fh.read())
        out[slug] = (meta, state, program)
    return out


def index_titles(index_html):
    """slug -> link text (already HTML-escaped) from the existing index cards."""
    return dict(re.findall(r'<h3><a href="/case-studies/([^/]+)/">(.*?)</a></h3>', index_html))


def cards(meta):
    out = []
    for slug, (m, state, program) in meta.items():
        out.append(
            '        <article class="card">\n'
            '          <div class="card-top">\n'
            f'            <div class="card-cat">{html.escape(program, quote=False)} &middot; {state}</div>\n'
            f'            <div class="card-cite">{CITE[slug]}</div>\n'
            '          </div>\n'
            '          <div class="card-body">\n'
            f'            <h3><a href="/case-studies/{slug}/">{html.escape(m["title"], quote=False)}</a></h3>\n'
            f'            <p>{html.escape(m["meta_description"], quote=False)}</p>\n'
            '            <span class="card-link">Read the case study &rarr;</span>\n'
            '          </div>\n'
            '        </article>')
    return "\n".join(out)


def block(heading, eyebrow, slugs, titles):
    lis = "\n".join(f'        <li><a href="/case-studies/{s}/">{titles[s]}</a></li>' for s in slugs)
    return ('  <!-- ============ WORKED CASES ============ -->\n'
            '  <section class="section section-alt" id="worked-cases" aria-labelledby="h-worked-cases">\n'
            '    <div class="frame">\n'
            '      <div class="section-head">\n'
            f'        <span class="eyebrow">{eyebrow}</span>\n'
            f'        <h2 id="h-worked-cases">{heading}</h2>\n'
            '      </div>\n'
            '      <ul class="link-cols">\n'
            f'{lis}\n'
            '      </ul>\n'
            '    </div>\n'
            '  </section>\n\n')


def after_section(s, marker):
    start = s.index(marker)
    return s.index("</section>", start) + len("</section>\n\n")


def main():
    idx = read("case-studies/index.html")
    if "rv-park-ossipee-new-hampshire-usda" in idx:
        sys.exit("already wired")
    meta = new_meta()

    # 1. case index: four cards appended to the published grid, same style
    i = idx.rindex("</article>") + len("</article>")
    idx = idx[:i] + "\n" + cards(meta) + idx[i:]
    write("case-studies/index.html", idx)

    titles = index_titles(idx)

    # 2. asset hubs: Worked cases block after the By Market section
    for rel, (heading, slugs) in HUBS.items():
        s = read(rel)
        by_state = 'id="by-state"' if 'id="by-state"' in s else 'id="state"'
        i = after_section(s, by_state)
        s = s[:i] + block(heading, "Worked Cases", slugs, titles) + s[i:]
        write(rel, s)

    # 3. state pages: case link block after the By Asset Class section
    for rel, (heading, slugs, anchor) in STATES.items():
        s = read(rel)
        i = after_section(s, anchor)
        s = s[:i] + block(heading, "Worked Case", slugs, titles) + s[i:]
        write(rel, s)

    # 4. sitemap: four new URLs; lastmod = build date on every page this lane changed
    sm = read("sitemap.xml")
    new_urls = "".join(
        "  <url>\n"
        f"    <loc>{SITE}/case-studies/{slug}/</loc>\n"
        f"    <lastmod>{BUILD_DATE}</lastmod>\n"
        "    <changefreq>monthly</changefreq>\n"
        "    <priority>0.8</priority>\n"
        "  </url>\n" for slug in meta)
    sm = sm.replace("</urlset>", new_urls + "</urlset>")
    changed = subprocess.check_output(["git", "-C", ROOT, "diff", "--name-only", "--", "*.html"]).decode().split()
    n = 0
    for rel in changed:
        loc = f"{SITE}/{rel[:-len('index.html')]}" if rel.endswith("index.html") else None
        if not loc:
            continue
        pat = re.compile(r"(<loc>%s</loc>\s*<lastmod>)[^<]*(</lastmod>)" % re.escape(loc))
        sm, k = pat.subn(r"\g<1>%s\g<2>" % BUILD_DATE, sm)
        n += k
    write("sitemap.xml", sm)
    print(f"cards +4, hubs {len(HUBS)}, states {len(STATES)}, sitemap +4 urls, lastmod set on {n} existing urls")


if __name__ == "__main__":
    main()
