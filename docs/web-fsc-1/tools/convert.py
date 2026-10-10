#!/usr/bin/env python3
"""WEB-FSC-1 one-time converter: owner Markdown -> house HTML pages.

Reads docs/web-fsc-1/input/ and writes:
  case-studies/<slug>/index.html for the four batch-1 cases (shell: the
  Pennsylvania RV park case), and the body of the-practice/index.html.

Text is carried word for word. The only transformations are the ones the
charter allows (house components, {{byline}}/{{signature}} -> byline markers,
logged internal link corrections). scripts/byline.py then fills the markers.
"""
import html
import json
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
INPUT = os.path.join(ROOT, "docs", "web-fsc-1", "input")
SITE = "https://feasibility-study-company.com"
BASE_COMMIT = "d456950"  # default-branch head this lane was cut from

CASES = [
    ("rv-park-ossipee-new-hampshire-usda", "New Hampshire", "USDA B&I"),
    ("cabin-resort-townsend-tennessee-sba", "Tennessee", "SBA 504"),
    ("glamping-oak-hill-west-virginia-usda", "West Virginia", "USDA B&I"),
    ("dry-stack-cape-coral-florida-sba", "Florida", "SBA 504"),
]

# Internal link corrections (each one logged in DECISIONS.md).
CASE_LINKS = {"/inquiries/": "/#contact"}
ABOUT_LINKS = {"/inquiries/": "#contact"}

PAGE_CSS = """<style>
/* WEB-FSC-1 batch-1 page components */
.hero .disclosure { margin-top: 30px; }
.prose ol, .prose ul { padding-left: 1.4em; margin-bottom: 1.15em; }
.prose li { margin-bottom: .6em; }
.prose a, .related a { color: var(--red); }
.prose a:hover, .related a:hover { text-decoration: underline; text-underline-offset: 3px; }
.prose + .data-table-wrap { margin-top: 28px; }
.data-table-wrap + .prose { margin-top: 36px; }
a.cite { color: var(--red); white-space: nowrap; }
table.data td { min-width: 7em; }
.related { max-width: 860px; margin-top: 40px; font-size: 15px; line-height: 1.7; }
@media (max-width: 680px) {
  table.data { font-size: 13px; }
  table.data th, table.data td { padding: 9px 8px; min-width: 0; }
  table.data td:first-child { min-width: 8.5em; }
  table.data thead th { font-size: 11px; letter-spacing: 0.02em; }
}
</style>"""


# ---------------------------------------------------------------- parsing

def front_matter(text):
    assert text.startswith("---\n")
    end = text.index("\n---\n", 4)
    meta = {}
    key = None
    for line in text[4:end].split("\n"):
        if re.match(r"^[a-z_0-9]+:", line):
            key, _, val = line.partition(":")
            val = val.strip()
            if val.startswith('"'):
                val = val[1:val.index('"', 1)]
            else:
                val = re.sub(r"\s+#.*$", "", val)
            meta[key] = val
        elif key and line.startswith("  "):
            meta[key] = (meta[key] + " " + line.strip()).strip()
    return meta, text[end + 5:]


def blocks(body):
    """Split Markdown into typed blocks. Single-line list items; pipe tables."""
    out = []
    for chunk in re.split(r"\n\s*\n", body.strip()):
        lines = chunk.split("\n")
        first = lines[0]
        if first.startswith("<!--"):
            continue
        if first.startswith("## "):
            out.append(("h2", first[3:].strip()))
            rest = "\n".join(lines[1:]).strip()
            if rest:
                out.extend(blocks(rest))
        elif first.startswith("# "):
            out.append(("h1", first[2:].strip()))
        elif first.startswith("|"):
            out.append(("table", lines))
        elif re.match(r"^\d+\. ", first):
            out.append(("ol", [re.sub(r"^\d+\. ", "", l) for l in lines]))
        elif first.startswith("- "):
            out.append(("ul", [l[2:] for l in lines]))
        elif first.startswith("> "):
            out.append(("quote", " ".join(l[2:] for l in lines)))
        elif first.strip() in ("{{byline}}", "{{signature}}"):
            out.append(("token", first.strip()))
        else:
            out.append(("p", " ".join(lines)))
    return out


def slugify(text):
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s


# ---------------------------------------------------------------- inline

def inline(text, links):
    """Escape, then bold, links and [n] citations. Words are never altered."""
    out = []
    pos = 0
    for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", text):
        out.append(_plain(text[pos:m.start()]))
        href = links.get(m.group(2), m.group(2))
        out.append(f'<a href="{html.escape(href)}">{_plain(m.group(1))}</a>')
        pos = m.end()
    out.append(_plain(text[pos:]))
    return "".join(out)


def _plain(text):
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"\[(\d+)\]", r'<a class="cite" href="#s\1">[\1]</a>', t)
    return t


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def table_html(lines, links, indent="      "):
    head = cells(lines[0])
    rows = [cells(l) for l in lines[2:]]
    th = "".join(f'<th scope="col">{inline(c, links)}</th>' for c in head)
    body = "\n".join(
        f"{indent}      <tr>" + "".join(f"<td>{inline(c, links)}</td>" for c in r) + "</tr>"
        for r in rows)
    return (f'{indent}<div class="data-table-wrap">\n'
            f'{indent}  <table class="data">\n'
            f'{indent}    <thead><tr>{th}</tr></thead>\n'
            f'{indent}    <tbody>\n{body}\n'
            f'{indent}    </tbody>\n'
            f'{indent}  </table>\n'
            f'{indent}</div>')


def flow_html(items, links, indent="      "):
    """Paragraphs and lists grouped into .prose runs; tables full width."""
    out, prose = [], []

    def flush():
        if prose:
            out.append(f'{indent}<div class="prose">\n' + "\n".join(prose) + f"\n{indent}</div>")
            prose.clear()

    for kind, val in items:
        if kind == "p":
            prose.append(f"{indent}  <p>{inline(val, links)}</p>")
        elif kind in ("ol", "ul"):
            lis = "\n".join(f"{indent}    <li>{inline(v, links)}</li>" for v in val)
            prose.append(f"{indent}  <{kind}>\n{lis}\n{indent}  </{kind}>")
        elif kind == "table":
            flush()
            out.append(table_html(val, links, indent))
        elif kind == "raw":
            flush()
            out.append(val)
        else:
            raise ValueError(f"unexpected block {kind}: {val!r}")
    flush()
    return "\n".join(out)


def faq_html(items, links, indent="      "):
    qs = []
    for kind, val in items:
        m = re.match(r"^\*\*(.+?)\*\*\s+(.*)$", val) if kind == "p" else None
        if not m:
            raise ValueError(f"FAQ item not in **Q** A form: {val!r}")
        qs.append(f"{indent}  <details>\n{indent}    <summary>{inline(m.group(1), links)}</summary>\n"
                  f"{indent}    <p>{inline(m.group(2), links)}</p>\n{indent}  </details>")
    return f'{indent}<div class="faq-list">\n' + "\n".join(qs) + f"\n{indent}</div>"


def sources_html(items, indent="      "):
    (kind, val), = items
    assert kind == "ol"
    lis = []
    for n, item in enumerate(val, 1):
        m = re.match(r"^(.*?)\s(https?://\S+)$", item)
        if m:
            text = html.escape(m.group(1), quote=False)
            url = m.group(2)
            lis.append(f'{indent}  <li id="s{n}">{text} <a href="{html.escape(url)}" rel="noopener">{html.escape(url, quote=False)}</a></li>')
        else:
            lis.append(f'{indent}  <li id="s{n}">{html.escape(item, quote=False)}</li>')
    return f'{indent}<ol class="sources">\n' + "\n".join(lis) + f"\n{indent}</ol>"


CTA_TAIL = re.compile(r"^(.*?)\s*\[(Request a methodology briefing)\]\(([^)]+)\)\.?$")


def section(slug, heading, inner, alt, extra_head=""):
    cls = "section section-alt" if alt else "section"
    return (f'  <section class="{cls}" id="{slug}" aria-labelledby="h-{slug}">\n'
            f'    <div class="frame">\n'
            f'      <div class="section-head">\n'
            f'        <h2 id="h-{slug}">{html.escape(heading, quote=False)}</h2>{extra_head}\n'
            f'      </div>\n'
            f'{inner}\n'
            f'    </div>\n'
            f'  </section>')


def cta_band(heading, para, links):
    m = CTA_TAIL.match(para)
    assert m, para
    slug = slugify(heading)
    href = links.get(m.group(3), m.group(3))
    return (f'  <section class="cta-band" aria-labelledby="h-{slug}">\n'
            f'    <div class="frame">\n'
            f'      <h2 id="h-{slug}">{html.escape(heading, quote=False)}</h2>\n'
            f'      <p>{inline(m.group(1), links)}</p>\n'
            f'      <a class="btn" href="{html.escape(href)}">{m.group(2)}</a>\n'
            f'    </div>\n'
            f'  </section>')


def split_sections(bl):
    """-> (pre-H2 blocks, [(heading, blocks)])"""
    pre, secs = [], []
    for b in bl:
        if b[0] == "h2":
            secs.append((b[1], []))
        elif secs:
            secs[-1][1].append(b)
        else:
            pre.append(b)
    return pre, secs


def marker(name, params=None):
    head = f"<!--fsc:{name}" + (" " + json.dumps(params, sort_keys=True) if params else "") + "-->"
    return f"{head}<!--/fsc:{name}-->"


# ---------------------------------------------------------------- head

def set_head(shell, meta, url, og_type=None):
    title = html.escape(meta["title"], quote=False)
    desc = html.escape(meta["meta_description"], quote=True)
    t_attr = html.escape(meta["title"], quote=True)
    s, n = re.subn(r"^<title>.*?</title>$", lambda m: f"<title>{title}</title>", shell, count=1, flags=re.M)
    assert n == 1, "title"
    reps = [
        (r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{desc}">'),
        (r'<link rel="canonical" href="[^"]*">', f'<link rel="canonical" href="{url}">'),
        (r'<meta property="og:title" content="[^"]*">', f'<meta property="og:title" content="{t_attr}">'),
        (r'<meta property="og:description" content="[^"]*">', f'<meta property="og:description" content="{desc}">'),
        (r'<meta property="og:url" content="[^"]*">', f'<meta property="og:url" content="{url}">'),
        (r'<meta name="twitter:title" content="[^"]*">', f'<meta name="twitter:title" content="{t_attr}">'),
        (r'<meta name="twitter:description" content="[^"]*">', f'<meta name="twitter:description" content="{desc}">'),
    ]
    if og_type:
        reps.append((r'<meta property="og:type" content="[^"]*">', f'<meta property="og:type" content="{og_type}">'))
    for pat, rep in reps:
        s, n = re.subn(pat, lambda m: rep, s, count=1)
        assert n == 1, pat
    return s


def replace_ld(s, new_block):
    s, n = re.subn(r'<script type="application/ld\+json">.*?</script>', lambda m: new_block, s, count=1, flags=re.S)
    assert n == 1
    return s


def add_css(s):
    i = s.index("</head>")
    return s[:i] + PAGE_CSS + "\n" + s[i:]


def replace_main(s, main_inner):
    a = s.index('<main id="main">') + len('<main id="main">')
    b = s.index("</main>")
    return s[:a] + "\n\n" + main_inner + "\n\n" + s[b:]


# ---------------------------------------------------------------- cases

def case_ld(meta, url, crumbs):
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {"@type": "Organization", "@id": SITE + "/#org", "name": "Feasibility Study Company",
             "url": SITE + "/", "logo": SITE + "/og.png"},
            {"@type": "Article", "@id": url + "#article", "headline": meta["h1"],
             "description": meta["meta_description"], "articleSection": "Case Studies",
             "inLanguage": "en-US", "datePublished": meta["date_published"],
             "dateModified": meta["date_modified"], "image": SITE + "/og.png",
             "author": {"@type": "Person", "@id": SITE + "/#mark-otava", "name": "Mark Otava"},
             "publisher": {"@id": SITE + "/#org"}, "mainEntityOfPage": url},
            {"@type": "BreadcrumbList", "@id": url + "#breadcrumb",
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + h}
                                 for i, (n, h) in enumerate(crumbs)]},
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(graph, indent=2, ensure_ascii=False) + "\n</script>"


def breadcrumb_nav(crumbs):
    lis = []
    for i, (name, href) in enumerate(crumbs):
        n = html.escape(name, quote=False)
        if i == len(crumbs) - 1:
            lis.append(f'        <li aria-current="page">{n}</li>')
        else:
            lis.append(f'        <li><a href="{href}">{n}</a></li>')
    return ('  <nav class="breadcrumb" aria-label="Breadcrumb">\n    <div class="frame">\n      <ol>\n'
            + "\n".join(lis) + "\n      </ol>\n    </div>\n  </nav>")


def build_case(slug, state, program, shell):
    with open(os.path.join(INPUT, "case-studies", slug + ".md"), encoding="utf-8") as fh:
        meta, body = front_matter(fh.read())
    assert meta["slug"] == f"/case-studies/{slug}/"
    url = SITE + meta["slug"]
    names = [x.strip() for x in meta["breadcrumbs"].strip("[]").split(",")]
    crumbs = list(zip(names, ["/", "/case-studies/", meta["asset_class"], meta["slug"]]))
    links = CASE_LINKS

    bl = blocks(body)
    pre, secs = split_sections(bl)
    assert pre[0] == ("h1", meta["h1"]), pre[0]
    assert pre[1] == ("token", "{{byline}}")
    assert pre[2][0] == "quote" and pre[2][1].startswith("**Representative worked example.**")
    intro = [b for b in pre[3:]]
    assert all(k == "p" for k, _ in intro)

    eyebrow = " &middot; ".join(html.escape(x, quote=False) for x in ("Case Study", state, names[2], program))
    hero = ['  <!-- ============ HERO ============ -->',
            '  <section class="hero">', '    <div class="frame">',
            f'      <p class="hero-eyebrow">{eyebrow}</p>',
            f'      <h1>{html.escape(meta["h1"], quote=False)}</h1>',
            "      " + marker("byline-article", {"published": meta["date_published"], "data_as_of": meta["data_as_of"]}),
            '      <div class="capsule disclosure">',
            f'        <p>{inline(pre[2][1], links)}</p>',
            '      </div>']
    for _, p in intro:
        hero.append(f'      <p class="hero-sub">{inline(p, links)}</p>')
    hero += ['    </div>', '  </section>']

    parts = ["\n".join(hero), "  <!-- ============ BREADCRUMB ============ -->", breadcrumb_nav(crumbs)]
    alt = False
    tail = None
    for heading, items in secs:
        sl = slugify(heading)
        if heading.startswith("Questions"):
            parts.append(section(sl, heading, faq_html(items, links), alt))
        elif heading == "Data sources and dates":
            src = [b for b in items if b[0] == "ol"]
            rest = [b for b in items if b[0] != "ol"]
            assert rest[0][0] == "p" and rest[0][1].startswith("**Related:**"), rest
            assert rest[1] == ("token", "{{signature}}") and len(rest) == 2
            inner = (sources_html(src) + "\n"
                     f'      <p class="related">{inline(rest[0][1], links)}</p>\n'
                     "      " + marker("signature"))
            parts.append(section("sources", heading, inner, alt))
        elif len(items) == 1 and items[0][0] == "p" and CTA_TAIL.match(items[0][1]):
            parts.append(cta_band(heading, items[0][1], links))
            continue
        else:
            parts.append(section(sl, heading, flow_html(items, links), alt))
        alt = not alt

    s = set_head(shell, meta, url, og_type="article")
    s = replace_ld(s, case_ld(meta, url, crumbs))
    s = add_css(s)
    s = replace_main(s, "\n\n".join(parts))
    out = os.path.join(ROOT, "case-studies", slug, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(s)
    return out


# ---------------------------------------------------------------- about

COUNT_KEYS = ["asset-classes", "states", "cases", None]


def build_about():
    path = os.path.join(ROOT, "the-practice", "index.html")
    # always start from the pre-lane page so a rerun never converts a converted page
    shell = subprocess.check_output(["git", "-C", ROOT, "show", BASE_COMMIT + ":the-practice/index.html"]).decode("utf-8")
    with open(os.path.join(INPUT, "about", "about.md"), encoding="utf-8") as fh:
        meta, body = front_matter(fh.read())
    links = ABOUT_LINKS
    bl = blocks(body)
    pre, secs = split_sections(bl)
    assert pre[0] == ("h1", meta["h1"])
    assert pre[1][0] == "p" and pre[2][0] == "p" and pre[3][0] == "table" and len(pre) == 4

    # hero: lede + the three links as hero buttons
    btns = re.findall(r"\[([^\]]+)\]\(([^)]+)\)", pre[2][1])
    assert len(btns) == 3 and re.sub(r"\[[^\]]+\]\([^)]+\)", "", pre[2][1]).replace("·", "").strip() == ""
    btn_html = []
    for i, (text, href) in enumerate(btns):
        cls = "btn" if i == 0 else "btn btn-outline"
        btn_html.append(f'        <a class="{cls}" href="{html.escape(links.get(href, href))}">{html.escape(text, quote=False)}</a>')
    hero = "\n".join([
        '  <!-- ============ HERO ============ -->',
        '  <section class="hero">', '    <div class="frame">',
        '      <p class="hero-eyebrow">The Practice</p>',
        f'      <h1>{html.escape(meta["h1"], quote=False)}</h1>',
        f'      <p class="hero-sub">{inline(pre[1][1], links)}</p>',
        '      <div class="hero-actions">', *btn_html, '      </div>',
        '    </div>', '  </section>'])

    # stat band from the 4-column figure table; the first three are generated counters
    nums, labels = cells(pre[3][1][0]), cells(pre[3][1][2])
    stats = []
    for key, num, label in zip(COUNT_KEYS, nums, labels):
        n = f"<!--fsc:count:{key}-->{num}<!--/fsc:count:{key}-->" if key else num
        stats.append('        <div class="stat">\n'
                     f'          <div class="stat-num">{n}</div>\n'
                     f'          <div class="stat-label">{inline(label, links)}</div>\n'
                     '        </div>')
    band = ('  <section class="stat-band" aria-label="The practice at a glance">\n    <div class="frame">\n'
            '      <div class="stat-grid">\n' + "\n".join(stats) + "\n      </div>\n    </div>\n  </section>")

    crumbs = [("Home", "/"), ("The Practice", "/the-practice/")]
    parts = [hero, "  <!-- ============ BREADCRUMB ============ -->", breadcrumb_nav(crumbs), band]
    alt = False
    for heading, items in secs:
        sl = slugify(heading)
        if heading.startswith("Questions"):
            parts.append(section(sl, heading, faq_html(items, links), alt))
        elif heading == "Sources":
            src = [b for b in items if b[0] == "ol"]
            assert items[-1] == ("token", "{{signature}}") and len(items) == 2
            parts.append(section("sources", heading, sources_html(src) + "\n      " + marker("signature"), alt))
        elif heading == "Who stands behind the research":
            out = []
            for kind, val in items:
                if kind == "table":
                    assert "[VERIFY BEFORE PUBLISHING" in val[2]
                    out.append(("raw", "      " + marker("about-credentials")))
                elif kind == "p" and val.startswith("[BIO:"):
                    out.append(("raw", "      " + marker("about-bio")))
                else:
                    out.append((kind, val))
            parts.append(section(sl, heading, flow_html(out, links), alt))
        elif len(items) == 1 and items[0][0] == "p" and CTA_TAIL.match(items[0][1]):
            parts.append(cta_band(heading, items[0][1], links))
            continue
        else:
            parts.append(section(sl, heading, flow_html(items, links), alt))
        alt = not alt

    # the contact band sits after </main> and is kept with the header and footer

    s = set_head(shell, meta, SITE + "/the-practice/")
    s = replace_ld(s, marker("about-ld", {"date_modified": meta["date_modified"]}))
    s = add_css(s)
    s = replace_main(s, "\n\n".join(parts))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(s)
    return path


def main():
    with open(os.path.join(ROOT, "case-studies", "rv-park-pennsylvania-usda", "index.html"), encoding="utf-8") as fh:
        shell = fh.read()
    for slug, state, program in CASES:
        print(build_case(slug, state, program, shell))
    print(build_about())


if __name__ == "__main__":
    main()
