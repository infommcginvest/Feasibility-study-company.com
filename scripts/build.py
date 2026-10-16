#!/usr/bin/env python3
"""Page factory for feasibility-study-company.com (WEB-FSC-6).

Every factory page has one source file, src/pages/<url path>.html (never served; netlify.toml
answers /src/* with 404). The source opens with a JSON front-matter block between two lines
of three hyphens and continues with the body as HTML fragments. build.py renders the source
through src/templates/<type>.html, wrapped in src/templates/base.html, into the served page
<url path>/index.html.

    python3 scripts/build.py                        render every source
    python3 scripts/build.py --page /states/texas/  render one page
    python3 scripts/build.py --check                exit 1 if a served page differs from a
                                                    fresh render outside script-owned regions
    python3 scripts/build.py --list                 list sources, types and served paths

Script-owned regions, <!--NS:NAME {params}-->...<!--/NS:NAME--> with NS in chrome, mesh,
fsc, sba, mkt and case, and the first-mention links mesh.py writes into prose (<a ... data-fsc-term>),
belong to their own scripts (chrome.py, mesh.py, byline.py,
regulatory.py, markets.py, casemodel.py), which check them. build.py writes their markers
and params; on a page that already exists it keeps the content those scripts wrote, and on
a new page it writes their starting content (the chrome partials, the source's sba and mkt
text, and empty fsc and case regions; mesh regions are carried over from the served page to the
start of the CTA line, where mesh.py puts them). Then run, in order: chrome.py (when present),
byline.py, regulatory.py, markets.py (when present), casemodel.py, mesh.py, links.py --relink.

Body shorthand the renderer expands:
    [^3]  [^3,7]        citation of numbered source 3 (and 7), house style per page type
    {{case:NAME}}       <!--case:<slug>.NAME--><!--/case:<slug>.NAME--> (casemodel.py fills it)
    <section id="x" data-h2="..." data-eyebrow="..." data-lede="..." data-layout="split">
        ...</section>   a house section: frame, section head, alternating grey band;
                        with data-layout="split" the part after <!--aside--> becomes the aside
Front matter keys are documented in src/README.md.
"""
import argparse
import html
import json
import os
import re
import string
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "src")
PAGES = os.path.join(SRC, "pages")
TPL = os.path.join(SRC, "templates")
PART = os.path.join(TPL, "partials")
SITE = "https://feasibility-study-company.com"
ORG_ID = SITE + "/#org"
AUTHOR_FILE = os.path.join(ROOT, "data", "authors", "mark-otava.json")

TYPES = ("state", "metro", "hub", "subtype", "case")
REFERENCE = ("state", "metro", "hub", "subtype")
OWNED = ("chrome", "mesh", "fsc", "sba", "mkt", "case")
REGION = re.compile(r"<!--(chrome|mesh|fsc|sba|mkt|case):([a-z0-9_.:-]+)( \{.*?\})?-->(.*?)<!--/\1:\2-->", re.S)
# scripts/mesh.py's own patterns: its regions (with their indentation and the blank line after them), which it
# places at the start of the line holding the CTA band, and the first-mention links it writes into prose
MESH_REGION = re.compile(r"[ \t]*<!--mesh:([a-z0-9-]+)(?: \{.*?\})?-->.*?<!--/mesh:\1-->\n\n", re.S)
TERM_LINK = re.compile(r'<a href="[^"]*" data-fsc-term="[^"]*">(.*?)</a>', re.S)
CITE = re.compile(r"\[\^(\d+(?:\s*,\s*\d+)*)\]")
CASE_SHORT = re.compile(r"\{\{case:([a-z0-9_.]+)\}\}")
SECTION = re.compile(r"<section\s+([^>]*)>(.*?)</section>", re.S)
ATTR = re.compile(r'([a-z][a-z0-9-]*)="([^"]*)"')
DASHES = re.compile(r"–|—|&[mn]dash;|&#821[12];|&#x201[34];", re.I)
FORBIDDEN = re.compile("|".join([
    "m" + "mcg", "moh" + "elsky", "union ?" + "metric", "inno" + "wave", "analytics" + r"\.loan",
    "loan analytic" + "s", "feasibility-study-consulta" + "nt", "wert-?bera" + "ter"]), re.I)


class BuildError(Exception):
    pass


# ------------------------------------------------------------------ helpers

def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def esc(text):
    """Escape a plain-text front-matter value once, whether it was written with & or &amp;."""
    return html.escape(html.unescape(text), quote=True)


def site_config():
    return json.loads(read(os.path.join(SRC, "site.json")))


def author_ref():
    a = json.loads(read(AUTHOR_FILE))
    return {"@type": "Person", "@id": a["person_id"], "name": a["name"]}


def author_inline(ref):
    """The one-line author object scripts/byline.py writes into Article JSON-LD."""
    return json.dumps(ref).replace('{"', '{ "').replace('"}', '" }')


def resolve_date(value, cfg):
    return cfg["deploy_date"] if value == "DEPLOY" else value


def served_path(url):
    return os.path.join(ROOT, url.strip("/"), "index.html")


def source_path(url):
    return os.path.join(PAGES, url.strip("/") + ".html")


def strip_tags(text):
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"<[^>]+>", "", text)
    return re.sub(r"\s+", " ", html.unescape(text)).strip()


# ------------------------------------------------------------------ source files

def parse_source(path):
    raw = read(path)
    if not raw.startswith("---\n"):
        raise BuildError(f"{path}: source must open with a line of three hyphens")
    end = raw.find("\n---\n", 4)
    if end < 0:
        raise BuildError(f"{path}: front matter is not closed by a line of three hyphens")
    try:
        front = json.loads(raw[4:end])
    except ValueError as exc:
        raise BuildError(f"{path}: front matter is not valid JSON: {exc}")
    body = raw[end + 5:]
    for key in ("type", "url", "title", "description", "h1", "breadcrumb", "published", "updated", "sources"):
        if key not in front:
            raise BuildError(f"{path}: front matter lacks '{key}'")
    if front["type"] not in TYPES:
        raise BuildError(f"{path}: unknown type {front['type']}")
    if os.path.normpath(source_path(front["url"])) != os.path.normpath(path):
        raise BuildError(f"{path}: url {front['url']} does not match the file's place under src/pages")
    return front, body


def all_sources():
    out = []
    for d, _dirs, files in os.walk(PAGES):
        for f in sorted(files):
            if f.endswith(".html"):
                out.append(os.path.join(d, f))
    return sorted(out)


# ------------------------------------------------------------------ body expansion

def cite_html(kind, numbers):
    if kind == "case":
        return "".join(f'<a class="cite" href="#s{n}">[{n}]</a>' for n in numbers)
    return "".join(f'<sup class="fn"><a href="#s{n}">{n}</a></sup>' for n in numbers)


def expand_cites(text, kind, nsources, where):
    def sub(m):
        nums = [int(x) for x in re.split(r"\s*,\s*", m.group(1))]
        for n in nums:
            if not 1 <= n <= nsources:
                raise BuildError(f"{where}: citation [^{n}] has no source (the list has {nsources})")
        return cite_html(kind, nums)
    return CITE.sub(sub, text)


def expand_case(text, slug):
    return CASE_SHORT.sub(lambda m: f"<!--case:{slug}.{m.group(1)}--><!--/case:{slug}.{m.group(1)}-->", text)


def expand(text, front, kind, where):
    text = expand_case(text, front.get("case_slug") or front["url"].strip("/").split("/")[-1])
    return expand_cites(text, kind, len(front["sources"]), where)


def section_html(attrs, inner, alt):
    sid = attrs.get("id")
    if not sid or "data-h2" not in attrs:
        raise BuildError(f"section needs id and data-h2: {attrs}")
    cls = "section section-alt" if alt else "section"
    head = []
    if attrs.get("data-eyebrow"):
        head.append(f'        <span class="eyebrow">{attrs["data-eyebrow"]}</span>')
    head.append(f'        <h2 id="h-{sid}">{attrs["data-h2"]}</h2>')
    if attrs.get("data-lede"):
        head.append(f'        <p class="lede">{attrs["data-lede"]}</p>')
    inner = inner.strip("\n")
    banner = f"  <!-- ============ {sid.upper().replace('-', ' ')} ============ -->"
    if attrs.get("data-layout") == "split":
        left, _sep, aside = inner.partition("<!--aside-->")
        return (f"{banner}\n  <section class=\"{cls}\" id=\"{sid}\" aria-labelledby=\"h-{sid}\">\n"
                f"    <div class=\"frame split\">\n      <div>\n" + "\n".join(head) + "\n"
                f"{left.strip(chr(10))}\n      </div>\n{aside.strip(chr(10))}\n    </div>\n  </section>\n")
    return (f"{banner}\n  <section class=\"{cls}\" id=\"{sid}\" aria-labelledby=\"h-{sid}\">\n"
            f"    <div class=\"frame\">\n      <div class=\"section-head\">\n" + "\n".join(head) +
            f"\n      </div>\n{inner}\n    </div>\n  </section>\n")


def render_body(body, front, kind, start_alt):
    body = expand(body, front, kind, front["url"])
    out, pos, alt, ids = [], 0, start_alt, []
    for m in SECTION.finditer(body):
        between = body[pos:m.start()]
        if between.strip():
            raise BuildError(f"{front['url']}: text outside a <section>: {between.strip()[:80]!r}")
        attrs = dict(ATTR.findall(m.group(1)))
        ids.append(attrs.get("id"))
        out.append(section_html(attrs, m.group(2), alt))
        alt = not alt
        pos = m.end()
    if body[pos:].strip():
        raise BuildError(f"{front['url']}: text after the last <section>: {body[pos:].strip()[:80]!r}")
    return "\n" + "\n".join(out), alt, ids


# ------------------------------------------------------------------ fixed blocks

def breadcrumb_html(items):
    lines = []
    for item in items[:-1]:
        lines.append(f'        <li><a href="{esc(item[1])}">{esc(item[0])}</a></li>')
    lines.append(f'        <li aria-current="page">{esc(items[-1][0])}</li>')
    return "\n".join(lines)


def stat_band(front, kind):
    stats = front.get("stats")
    if not stats:
        return ""
    cells = []
    for s in stats:
        label = expand_cites(s["label"], kind, len(front["sources"]), front["url"] + " stats")
        unit = f"<span>{s['unit']}</span>" if s.get("unit") else ""
        cells.append(f'        <div class="stat">\n          <div class="stat-num">{s["num"]}{unit}</div>\n'
                     f'          <div class="stat-label">{label}</div>\n        </div>')
    label = esc(front.get("stats_label") or (front["h1"] + " at a glance"))
    return (f"\n  <!-- ============ STAT BAND ============ -->\n  <section class=\"stat-band\" aria-label=\"{label}\">\n"
            f"    <div class=\"frame\">\n      <div class=\"stat-grid\">\n" + "\n".join(cells) +
            "\n      </div>\n    </div>\n  </section>\n")


def faq_html(front, kind, alt):
    faq = front.get("faq")
    if not faq:
        return "", alt
    items = []
    for it in faq["items"]:
        a = expand(it["a"], front, kind, front["url"] + " faq")
        items.append(f"        <details>\n          <summary>{it['q']}</summary>\n          <p>{a}</p>\n        </details>")
    cls = "section section-alt" if alt else "section"
    eyebrow = f'        <span class="eyebrow">{faq["eyebrow"]}</span>\n' if faq.get("eyebrow") else ""
    out = (f"\n  <!-- ============ FAQ ============ -->\n  <section class=\"{cls}\" id=\"faq\" aria-labelledby=\"h-faq\">\n"
           f"    <div class=\"frame\">\n      <div class=\"section-head\">\n{eyebrow}"
           f"        <h2 id=\"h-faq\">{faq['h2']}</h2>\n      </div>\n      <div class=\"faq-list\">\n" +
           "\n".join(items) + "\n      </div>\n    </div>\n  </section>\n")
    return out, not alt


def sources_html(front):
    lines = []
    for i, s in enumerate(front["sources"], 1):
        for key in ("publisher", "title", "date", "url"):
            if not s.get(key):
                raise BuildError(f"{front['url']}: source {i} lacks '{key}'")
        if not s["url"].startswith(("https://", "http://")):
            raise BuildError(f"{front['url']}: source {i} url is not absolute: {s['url']}")
        note = f" {esc(s['note'])}" if s.get("note") else ""
        lines.append(f'        <li id="s{i}">{esc(s["publisher"])}, <a href="{esc(s["url"])}" rel="noopener">'
                     f'{esc(s["title"])}</a>, {esc(s["date"])}.{note}</li>')
    return "\n".join(lines)


def jsonld(front, cfg, kind):
    url = SITE + front["url"]
    published = resolve_date(front["published"], cfg)
    updated = resolve_date(front["updated"], cfg)
    ref = author_ref()
    graph = [{"@type": "Organization", "@id": ORG_ID, "name": "Feasibility Study Company",
              "url": SITE + "/", "logo": SITE + "/og.png"}]
    if kind == "case":
        graph.append({"@type": "Article", "@id": url + "#article", "headline": strip_tags(front["h1"]),
                      "description": front["description"], "articleSection": "Case Studies", "inLanguage": "en-US",
                      "datePublished": published, "dateModified": updated, "image": SITE + "/og.png",
                      "author": "__AUTHOR__", "publisher": {"@id": ORG_ID}, "mainEntityOfPage": url})
    else:
        svc = dict(front.get("service") or {})
        if svc:
            node = {"@type": "Service", "@id": url + "#service"}
            node.update(svc)
            node["provider"] = {"@id": ORG_ID}
            graph.append(node)
        graph.append({"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": front["title"],
                      "description": front["description"], "inLanguage": "en-US", "datePublished": published,
                      "dateModified": updated, "author": "__AUTHOR__", "publisher": {"@id": ORG_ID}})
    items = []
    for pos, item in enumerate(front["breadcrumb"], 1):
        target = SITE + item[1] if len(item) > 1 else url
        items.append({"@type": "ListItem", "position": pos, "name": item[0], "item": target})
    graph.append({"@type": "BreadcrumbList", "@id": url + "#breadcrumb", "itemListElement": items})
    if front.get("faq"):
        graph.append({"@type": "FAQPage", "@id": url + "#faq", "mainEntity": [
            {"@type": "Question", "name": strip_tags(it["q"]),
             "acceptedAnswer": {"@type": "Answer", "text": strip_tags(re.sub(CITE, "", it["a"]))}}
            for it in front["faq"]["items"]]})
    text = json.dumps({"@context": "https://schema.org", "@graph": graph}, indent=2, ensure_ascii=False)
    text = text.replace('"__AUTHOR__"', author_inline(ref))
    return '<script type="application/ld+json">\n' + text + "\n</script>"


def marker(ns, name, params=None, inner=""):
    head = f"<!--{ns}:{name}" + (" " + json.dumps(params, sort_keys=True) if params else "") + "-->"
    return f"{head}{inner}<!--/{ns}:{name}-->"


# ------------------------------------------------------------------ render

def render(front, body, cfg, old=None):
    kind = front["type"]
    url = SITE + front["url"]
    updated = resolve_date(front["updated"], cfg)
    published = resolve_date(front["published"], cfg)
    body_html, alt, _ids = render_body(body, front, kind, start_alt=False)
    faq, alt = faq_html(front, kind, alt)
    if kind == "case":
        params = {"published": published, "updated": updated}
        if front.get("data_as_of"):
            params["data_as_of"] = front["data_as_of"]
        byline = marker("fsc", "byline-article", params)
    else:
        name = "line-state" if kind in ("state", "metro") else "line-asset"
        byline = marker("fsc", name, {"updated": updated})
    hero_secondary = ""
    if front.get("hero_secondary"):
        hs = front["hero_secondary"]
        hero_secondary = f'\n        <a class="btn btn-outline" href="{esc(hs["href"])}">{hs["text"]}</a>'
    cta = front.get("cta") or {}
    main_values = {
        "eyebrow": front.get("eyebrow", ""),
        "h1": front["h1"],
        "hero_sub": expand(front.get("hero_sub", ""), front, kind, front["url"] + " hero"),
        "hero_secondary": hero_secondary,
        "breadcrumb": breadcrumb_html(front["breadcrumb"]),
        "stat_band": stat_band(front, kind),
        "body": body_html,
        "faq": faq,
        "cta_h2": cta.get("h2", "Start with the market read."),
        "cta_p": cta.get("p", ""),
        "sources_alt": " section-alt" if alt else "",
        "sources_lede": front.get("sources_lede", "Every figure on this page traces to a named, dated source."),
        "byline": byline,
        "sources": sources_html(front),
    }
    main = string.Template(read(os.path.join(TPL, kind + ".html"))).substitute(main_values)
    house = "house-b.css" if kind == "case" else "house-a.css"
    page_css = ""
    if kind == "case":
        page_css = "<style>" + read(os.path.join(PART, "case-components.css")) + "</style>"
    # byline.py keeps the page's one date in the author-ld region too (date_modified mirrors the visible line)
    author_ld = "" if kind == "case" else marker("fsc", "author-ld", {"date_modified": updated, "url": url})
    values = {
        "title": esc(front["title"]),
        "description": esc(front["description"]),
        "og_description": esc(front.get("og_description") or front["description"]),
        "canonical": url,
        "house_css": read(os.path.join(PART, house)),
        "jsonld": jsonld(front, cfg, kind),
        "author_ld": author_ld,
        "page_css": page_css,
        "factory_css": read(os.path.join(PART, "factory.css")),
        "header": read(os.path.join(PART, "header.html")),
        "footer": read(os.path.join(PART, "footer.html")),
        "script": read(os.path.join(PART, "script.html")),
        "main": main.rstrip("\n"),
    }
    out = string.Template(read(os.path.join(TPL, "base.html"))).substitute(values)
    if old:
        out = keep_owned(out, old)
        out = keep_mesh(out, old)
    validate(out, front)
    return out


def keep_mesh(fresh, old):
    """Put the mesh regions of the served page back where scripts/mesh.py places them."""
    regions = "".join(m.group(0) for m in MESH_REGION.finditer(old))
    if not regions:
        return fresh
    i = fresh.find('<section class="cta-band"')
    line = fresh.rfind("\n", 0, i) + 1
    return fresh[:line] + regions + fresh[line:]


def comparable(text):
    """A page with every script-owned region blanked and mesh.py's first-mention links unwrapped."""
    return blank_owned(TERM_LINK.sub(lambda m: m.group(1), text))


def region_key_list(text):
    seen, keys = {}, []
    for m in REGION.finditer(text):
        k = (m.group(1), m.group(2))
        seen[k] = seen.get(k, 0) + 1
        keys.append((k, seen[k], m))
    return keys


def keep_owned(fresh, old):
    """Carry the content other scripts wrote into the served page across a re-render."""
    old_inner = {(k, i): m.group(4) for k, i, m in region_key_list(old)}
    out, pos = [], 0
    for k, i, m in region_key_list(fresh):
        out.append(fresh[pos:m.start()])
        inner = old_inner.get((k, i), m.group(4))
        out.append(f"<!--{k[0]}:{k[1]}{m.group(3) or ''}-->{inner}<!--/{k[0]}:{k[1]}-->")
        pos = m.end()
    out.append(fresh[pos:])
    return "".join(out)


def blank_owned(text):
    return REGION.sub(lambda m: f"<!--{m.group(1)}:{m.group(2)}{m.group(3) or ''}--><!--/{m.group(1)}:{m.group(2)}-->", text)


def validate(out, front):
    where = front["url"]
    outside = blank_owned(out)
    hit = DASHES.search(outside)
    if hit:
        ctx = outside[max(0, hit.start() - 60):hit.end() + 20].replace("\n", " ")
        raise BuildError(f"{where}: em or en dash outside script-owned regions: ...{ctx}...")
    hit = FORBIDDEN.search(out)
    if hit:
        raise BuildError(f"{where}: forbidden name in output: {hit.group(0)!r}")
    if len(re.findall(r"<title>", re.sub(r"<!--.*?-->", "", out, flags=re.S))) != 1:
        raise BuildError(f"{where}: not exactly one <title>")
    if out.count("<h1>") != 1:
        raise BuildError(f"{where}: not exactly one <h1>")
    ids = re.findall(r'\sid="([^"]+)"', re.sub(r"<!--.*?-->", "", outside, flags=re.S))
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        raise BuildError(f"{where}: duplicate element ids {dup}")
    for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', out, re.S):
        json.loads(m.group(1))
    sba = json.loads(read(os.path.join(ROOT, "data", "regulatory", "sba.json")))
    for m in re.finditer(r"<!--sba:([a-z0-9_.]+)", out):
        cur = sba
        for part in m.group(1).split("."):
            if not (isinstance(cur, dict) and part in cur):
                raise BuildError(f"{where}: sba marker path {m.group(1)} is not in data/regulatory/sba.json")
            cur = cur[part]
    left = re.search(r"\[\^\d|\{\{case:", outside)
    if left:
        raise BuildError(f"{where}: unexpanded shorthand near {outside[left.start():left.start() + 30]!r}")


# ------------------------------------------------------------------ commands

def build_one(path, cfg, check):
    front, body = parse_source(path)
    target = served_path(front["url"])
    old = read(target) if os.path.exists(target) else None
    out = render(front, body, cfg, old)
    rel = os.path.relpath(target, ROOT)
    if check:
        if old is None:
            return rel, "missing"
        if comparable(old) != comparable(out):
            return rel, "stale"
        return rel, None
    if out != old:
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(out)
        return rel, "written"
    return rel, None


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--page")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args(argv)
    cfg = site_config()
    paths = all_sources()
    if args.page:
        want = source_path("/" + args.page.strip("/") + "/")
        if want not in paths:
            print(f"no source for {args.page} (looked for {os.path.relpath(want, ROOT)})")
            return 2
        paths = [want]
    if args.list:
        for p in paths:
            front, _ = parse_source(p)
            print(f"{front['type']:8} {front['url']:70} {os.path.relpath(served_path(front['url']), ROOT)}")
        return 0
    bad, done = [], []
    for p in paths:
        try:
            rel, state = build_one(p, cfg, args.check)
        except BuildError as exc:
            print(f"ERROR {exc}")
            bad.append(p)
            continue
        if state:
            (bad if args.check else done).append(f"{state}: {rel}")
    if args.check:
        for b in bad:
            print(b if isinstance(b, str) and ":" in b else f"error: {b}")
        print(f"{len(paths)} page(s) checked, {len(bad)} out of date or failing")
        return 1 if bad else 0
    for d in done:
        print(d)
    print(f"{len(paths)} source(s), {len(done)} page(s) written, {len(bad)} error(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
