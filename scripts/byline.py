#!/usr/bin/env python3
"""Site-wide byline, signature and author JSON-LD for feasibility-study-company.com.

The site is static HTML served from the repository root with no build step, so
this script is the template: it renders every byline, signature block, the About
page credentials table and bio, every author JSON-LD node and the homepage and
About counters from ONE author record, and writes them into the pages between
<!--fsc:NAME--> ... <!--/fsc:NAME--> markers.

    python3 scripts/byline.py           rewrite every managed region
    python3 scripts/byline.py --check   exit 1 if any page is out of date

Edit data/authors/mark-otava.json, run the script, commit the pages it changed.

Display rule (byline-spec.md section 1): a credential renders only when its
verify_url is an https:// link. With none filled, the name renders alone.
"""
import datetime
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTHOR_FILE = os.path.join(ROOT, "data", "authors", "mark-otava.json")
SITE = "https://feasibility-study-company.com"
ORG_ID = SITE + "/#org"
FIRM = "Feasibility Study Company"

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]

STYLE = """<style>
.byline { font-size: 14px; line-height: 1.6; color: var(--grey); margin-top: 26px; }
.byline a { color: var(--ink); font-weight: 600; border-bottom: 1px solid var(--line); }
.byline a:hover { color: var(--red); border-bottom-color: var(--red); }
.byline-reviewed { margin: 0 0 22px; }
.signature { border-top: 2px solid var(--ink); margin-top: 56px; padding-top: 22px; max-width: var(--prose); }
.signature p { margin: 0; }
.signature__name { font-weight: 700; font-size: 17px; }
.signature__name a { color: var(--ink); }
.signature__name a:hover { color: var(--red); }
.signature__role { color: var(--grey); font-size: 14px; margin-top: 2px; }
.signature__note { color: var(--grey); font-size: 14px; margin-top: 12px; line-height: 1.6; }
</style>"""


# ---------------------------------------------------------------- author

def load_author():
    with open(AUTHOR_FILE, encoding="utf-8") as fh:
        return json.load(fh)


def shown_credentials(author):
    """The display rule. Nothing else in the site decides what is shown."""
    return [c for c in author.get("credentials", [])
            if (c.get("verify_url") or "").startswith("https://")]


def display_name(author):
    suffix = ", ".join(c["abbr"] for c in shown_credentials(author))
    return f"{author['name']}, {suffix}" if suffix else author["name"]


def esc(text):
    return html.escape(text, quote=True)


def name_html(author):
    """Name linked to the profile; each shown credential linked to its record."""
    parts = [f'<a href="{esc(author["profile_url"])}">{esc(author["name"])}</a>']
    for c in shown_credentials(author):
        parts.append(f'<a href="{esc(c["verify_url"])}" rel="noopener">{esc(c["abbr"])}</a>')
    return ", ".join(parts)


def person_ref(author):
    return {"@type": "Person", "@id": author["person_id"], "name": author["name"]}


# ---------------------------------------------------------------- dates

def fmt_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"


def fmt_month(iso):
    y, m = (int(x) for x in iso.split("-")[:2])
    return f"{MONTHS[m - 1]} {y}"


def time_tag(iso):
    text = fmt_date(iso) if iso.count("-") == 2 else fmt_month(iso)
    return f'<time datetime="{iso}">{text}</time>'


# ---------------------------------------------------------------- renderers

def r_byline_article(a, p):
    out = f'<p class="byline">Market analysis by {name_html(a)} &middot; Published {time_tag(p["published"])}'
    if p.get("data_as_of"):
        out += f' &middot; Data as of {time_tag(p["data_as_of"])}'
    return out + "</p>"


def r_byline_framework(a, p):
    return f'<p class="byline">Written by {name_html(a)}</p>'


def r_line_asset(a, p):
    return (f'<p class="byline byline-reviewed">Methodology and market data reviewed by '
            f'{name_html(a)} &middot; Updated {time_tag(p["updated"])}</p>')


def r_line_state(a, p):
    return (f'<p class="byline byline-reviewed">Market data reviewed by {name_html(a)} '
            f'&middot; Updated {time_tag(p["updated"])}</p>')


def r_line_home(a, p):
    return f'<p class="byline">Research directed by {name_html(a)}</p>'


def r_signature(a, p):
    return (
        '<aside class="signature" aria-label="Signed by">\n'
        f'  <p class="signature__name"><a href="{esc(a["profile_url"])}">{esc(display_name(a))}</a></p>\n'
        f'  <p class="signature__role">{esc(a["role"])}, {FIRM}</p>\n'
        '  <p class="signature__note">The market conclusion on this page is signed by the principal. '
        'Every figure is sourced and dated in the list above. Worked cases are representative '
        'examples built from public data, not client engagements.</p>\n'
        '</aside>'
    )


def r_about_credentials(a, p):
    rows = shown_credentials(a)
    if not rows:
        return ""
    body = "\n".join(
        f'            <tr><td>{esc(c.get("name") or c["abbr"])}</td><td>{esc(c.get("issuer", ""))}</td>'
        f'<td><a href="{esc(c["verify_url"])}" rel="noopener">{esc(c["verify_url"])}</a></td></tr>'
        for c in rows)
    return (
        '<div class="data-table-wrap">\n'
        '        <table class="data">\n'
        '          <thead><tr><th scope="col">Credential</th><th scope="col">Issuing body</th>'
        '<th scope="col">Verify</th></tr></thead>\n'
        f'          <tbody>\n{body}\n          </tbody>\n'
        '        </table>\n'
        '      </div>'
    )


def r_about_bio(a, p):
    bio = (a.get("bio_short") or "").strip()
    return f"<p>{esc(bio)}</p>" if bio else ""


def credential_node(c):
    node = {"@type": "EducationalOccupationalCredential",
            "credentialCategory": c["abbr"], "url": c["verify_url"]}
    if c.get("name"):
        node["name"] = c["name"]
    if c.get("issuer"):
        node["recognizedBy"] = {"@type": "Organization", "name": c["issuer"]}
    return node


def r_about_ld(a, p):
    url = SITE + "/the-practice/"
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Organization",
                "@id": ORG_ID,
                "name": FIRM,
                "url": SITE + "/",
                "description": "Independent, market-led feasibility studies for SBA, USDA, EB-5 and conventional financing.",
                "founder": {"@id": a["person_id"]},
            },
            {
                "@type": "ProfilePage",
                "@id": url + "#page",
                "url": url,
                "dateModified": p["date_modified"],
                "mainEntity": {"@id": ORG_ID},
            },
            {
                "@type": "Person",
                "@id": a["person_id"],
                "name": a["name"],
                "jobTitle": a["role"],
                "worksFor": {"@id": ORG_ID},
                "knowsAbout": ["trade area analysis", "market feasibility", "absorption",
                               "capture rate", "USDA B&I", "SBA 504"],
                "hasCredential": [credential_node(c) for c in shown_credentials(a)],
                "sameAs": list(a.get("same_as", [])),
            },
            {
                "@type": "BreadcrumbList",
                "@id": url + "#breadcrumb",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE + "/"},
                    {"@type": "ListItem", "position": 2, "name": "The Practice", "item": url},
                ],
            },
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(graph, indent=2, ensure_ascii=False) + "\n</script>"


def r_author_ld(a, p):
    url = p["url"]
    node = {"@context": "https://schema.org", "@type": "WebPage", "@id": url + "#webpage",
            "url": url, "author": person_ref(a), "publisher": {"@id": ORG_ID}}
    return '<script type="application/ld+json">\n' + json.dumps(node, indent=2, ensure_ascii=False) + "\n</script>"


def r_style(a, p):
    return STYLE


RENDER = {
    "byline-article": r_byline_article, "byline-framework": r_byline_framework,
    "line-asset": r_line_asset, "line-state": r_line_state, "line-home": r_line_home,
    "signature": r_signature, "about-credentials": r_about_credentials,
    "about-bio": r_about_bio, "about-ld": r_about_ld, "author-ld": r_author_ld,
    "style": r_style,
}


# ---------------------------------------------------------------- markers

BLOCK = re.compile(r"<!--fsc:([a-z:-]+)( \{.*?\})?-->(.*?)<!--/fsc:\1-->", re.S)


def find_block(s, name):
    for m in BLOCK.finditer(s):
        if m.group(1) == name:
            return m
    return None


def wrap(name, inner, params):
    head = f"<!--fsc:{name}" + (" " + json.dumps(params, sort_keys=True) if params else "") + "-->"
    return f"{head}{inner}<!--/fsc:{name}-->"


def put(s, name, author, params=None, anchor=None):
    """Render region NAME. Reuse params stored in an existing marker; insert at anchor(s) if absent."""
    m = find_block(s, name)
    if m:
        if m.group(2):
            stored = json.loads(m.group(2))
        else:
            stored = params() if callable(params) else (params or {})
        inner = RENDER[name.split(":")[0]](author, stored)
        return s[:m.start()] + wrap(name, inner, stored) + s[m.end():]
    if anchor is None:
        raise ValueError(f"region {name} missing and no anchor given")
    params = params() if callable(params) else (params or {})
    i = anchor(s)
    inner = RENDER[name.split(":")[0]](author, params)
    return s[:i] + wrap(name, inner, params) + s[i:]


def put_count(s, name, value):
    m = find_block(s, name)
    if not m:
        return s
    return s[:m.start()] + wrap(name, str(value), None) + s[m.end():]


# ---------------------------------------------------------------- anchors

def after_h1(s):
    return s.index("</h1>") + len("</h1>")


def before_sources(s):
    return s.index('<ol class="sources">')


def after_sources(s):
    return s.index("</ol>", s.index('<ol class="sources">')) + len("</ol>")


def end_of_section(open_tag):
    def anchor(s):
        start = s.index(open_tag)
        end = s.index("</section>", start)
        return s.rindex("</div>", start, end)
    return anchor


def end_of_article(s):
    end = s.index("</article>")
    return s.rindex("</div>", 0, end)


def before_head_end(s):
    return s.index("</head>")


# ---------------------------------------------------------------- page facts

def ld_value(s, key):
    m = re.search(r'"%s"\s*:\s*"([^"]+)"' % key, s)
    return m.group(1) if m else None


def git_date(rel):
    try:
        out = subprocess.check_output(["git", "-C", ROOT, "log", "-1", "--format=%cs", "--", rel],
                                      stderr=subprocess.DEVNULL).decode().strip()
    except (OSError, subprocess.CalledProcessError):
        out = ""
    return out or datetime.date.today().isoformat()


def page_url(rel):
    return SITE + "/" + rel[: -len("index.html")]


def count_dirs(section):
    base = os.path.join(ROOT, section)
    return sum(1 for d in os.listdir(base)
               if os.path.isfile(os.path.join(base, d, "index.html")))


ARTICLE_AUTHOR = re.compile(
    r'"author"\s*:\s*\{\s*(?:"@id"\s*:\s*"%s"|"@type"\s*:\s*"Person"\s*,\s*"@id"\s*:\s*"[^"]*"\s*,\s*"name"\s*:\s*"[^"]*")\s*\}'
    % re.escape(ORG_ID))


def article_author(s, author):
    ref = json.dumps(person_ref(author)).replace('{"', '{ "').replace('"}', '" }')
    return ARTICLE_AUTHOR.sub('"author": ' + ref, s)


# ---------------------------------------------------------------- page types

def page_type(rel):
    parts = rel.split("/")
    if rel == "index.html":
        return "home"
    if rel == "the-practice/index.html":
        return "about"
    if rel == "analytical-framework/index.html":
        return "framework"
    if len(parts) >= 3 and parts[-1] == "index.html":
        return {"case-studies": "case", "research-notes": "note", "asset-classes": "asset",
                "practice-areas": "practice", "states": "state"}.get(parts[0])
    return None


def render_page(rel, s, author, counts):
    t = page_type(rel)
    if t is None:
        return s
    s = put(s, "style", author, anchor=before_head_end)
    url = page_url(rel)

    if t in ("case", "note"):
        s = put(s, "byline-article", author,
                params=lambda: {"published": ld_value(s, "datePublished")}, anchor=after_h1)
        sig_anchor = end_of_article if t == "note" else after_sources
        s = put(s, "signature", author, anchor=sig_anchor)
        s = article_author(s, author)
    elif t == "framework":
        s = put(s, "byline-framework", author, anchor=after_h1)
        s = put(s, "signature", author, anchor=after_sources)
        s = article_author(s, author)
    elif t in ("asset", "practice", "state"):
        name = "line-state" if t == "state" else "line-asset"
        s = put(s, name, author, params=lambda: {"updated": git_date(rel)}, anchor=before_sources)
        s = put(s, "author-ld", author, params={"url": url}, anchor=before_head_end)
    elif t == "home":
        s = put(s, "line-home", author, anchor=end_of_section('<section class="hero">'))
        s = put(s, "author-ld", author, params={"url": url}, anchor=before_head_end)
    elif t == "about":
        for name in ("about-ld", "about-credentials", "about-bio", "signature"):
            s = put(s, name, author)

    for key, value in counts.items():
        s = put_count(s, "count:" + key, value)
    return s


def main():
    check = "--check" in sys.argv[1:]
    author = load_author()
    counts = {"asset-classes": count_dirs("asset-classes"), "states": count_dirs("states"),
              "cases": count_dirs("case-studies")}
    changed = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in ("docs", "node_modules"))
        for fn in filenames:
            if fn != "index.html":
                continue
            path = os.path.join(dirpath, fn)
            rel = os.path.relpath(path, ROOT).replace(os.sep, "/")
            if page_type(rel) is None:
                continue
            with open(path, encoding="utf-8") as fh:
                old = fh.read()
            new = render_page(rel, old, author, counts)
            if new != old:
                changed.append(rel)
                if not check:
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(new)
    print(f"display name: {display_name(author)}")
    print(f"counts: {counts}")
    print(f"{'out of date' if check else 'updated'}: {len(changed)} page(s)")
    for rel in changed:
        print("  " + rel)
    if check and changed:
        sys.exit(1)


if __name__ == "__main__":
    main()
