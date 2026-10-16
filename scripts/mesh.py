#!/usr/bin/env python3
"""The two-way link mesh and first-mention links for feasibility-study-company.com.

Every case already names its state, its asset-class hub and its practice area
in its own prose. This script writes the reverse edges, so parents list their
children, plus the research-note topic map, into generated regions placed just
before each page's CTA band:

    <!--mesh:NAME--> <section ...> eyebrow, H2, ul.link-cols </section> <!--/mesh:NAME-->

    state page      mesh:state-cases     every case in the state
                    mesh:state-neighbors the neighbouring states that have a page
    hub             mesh:hub-cases       every case of the asset class, and the states they are set in
                    mesh:hub-notes       the research notes that inform the asset class
                    mesh:hub-related     the other asset classes of its family
    practice area   mesh:program-cases   every case under the program, one list per asset family
                    mesh:program-notes   the research notes that inform the program
    case            mesh:case-related    up to 6 sibling cases of the same asset, the research notes for
                                         its asset and program, up to 6 other cases in its state, and the
                                         state, hub and program it sits in
    research note   mesh:note-applied    the hubs, practice areas and cases it informs, and related notes

It then links the first prose mention of each term in data/mesh/terms.json on
every content page (one link per target, at most 15 per page, never in a heading,
the hero, a table, a link, a footnote marker, the sources, a generated region or
JSON-LD, never to the page itself). Those links carry data-fsc-term and are
rewritten from scratch on every run.

Which state, hub and program a case belongs to comes from the case page's own
links (generated links excluded); which hubs and programs a note informs comes
from data/mesh/topics.json. Anchor text is always the target's H1. No list
carries more than 24 links.

    python3 scripts/mesh.py            rewrite every page's mesh and term links
    python3 scripts/mesh.py --check    exit 1 if any page is out of date
    python3 scripts/mesh.py --report   print the edge table as JSON

Pages listed in data/site/hold.json are neither rewritten nor checked, but
they are listed: a held case still appears on its state, hub and program.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import links  # noqa: E402

ROOT = links.ROOT
TOPICS = os.path.join(ROOT, "data", "mesh", "topics.json")
TERMS = os.path.join(ROOT, "data", "mesh", "terms.json")
MAX_LIST = 24
MAX_SIBLINGS = 6
MAX_RELATED = 6
MAX_TERMS = 15
REGION_RX = re.compile(r"[ \t]*<!--mesh:([a-z0-9-]+)(?: \{.*?\})?-->.*?<!--/mesh:\1-->\n\n", re.S)
TERM_RX = re.compile(r'<a href="[^"]*" data-fsc-term="[^"]*">(.*?)</a>', re.S)
EM = re.compile(r"\s*(?:" + chr(0x2014) + "|" + chr(0x2013) + r")\s*")  # an em or en dash, spelled by code point


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def esc(t):
    return html.escape(t, quote=True)


def h1_of(s):
    m = re.search(r"<h1\b[^>]*>(.*?)</h1>", s, re.S)
    if not m:
        return None
    t = links.strip_tags(m.group(1))
    # a held page may still carry a dash in its H1; anchor text never does (ruling 12)
    return EM.sub(": ", t).strip()


def cap(t):
    return t[:1].upper() + t[1:]


# ---------------------------------------------------------------- the model

class Model:
    def __init__(self, site):
        self.site = site
        self.topics = load(TOPICS)
        self.h1 = {}
        self.cases = []
        for rel, url in site.pages:
            s = site.text(rel)
            self.h1[url] = h1_of(s)
        for rel, url in site.pages:
            if url.startswith("/case-studies/") and url != "/case-studies/":
                self.cases.append(self.case(rel, url))
        self.notes = [u for u in self.topics["notes"] if site.page_exists(u)]
        nb = self.topics.get("state_neighbors", {})
        asym = [(a, b) for a, v in nb.items() for b in v if a not in nb.get(b, [])]
        if asym:
            raise SystemExit(f"topics.json state_neighbors is not symmetric: {asym}")
        missing = [u for u in self.topics["notes"] if not site.page_exists(u)]
        if missing:
            raise SystemExit(f"topics.json names notes that do not exist: {missing}")

    def own_links(self, rel, url):
        """Body links the page's author wrote: no generated region, no term link, no breadcrumb."""
        out = []
        for a in links.anchors(self.site, rel, url):
            if a["kind"] != "a" or not a["path"] or not a["in_main"] or a["in_crumb"]:
                continue
            if a["region"] or "data-fsc-term" in a["attrs"]:
                continue
            out.append(a["path"])
        return out

    def pick(self, paths, rx, slug):
        found = [p for p in paths if re.match(rx, p) and self.site.page_exists(p)]
        if not found:
            return None
        named = [p for p in found if p.strip("/").split("/")[-1] in slug]
        return (named or found)[0]

    def case(self, rel, url):
        slug = url.strip("/").split("/")[-1]
        paths = self.own_links(rel, url)
        state = self.pick(paths, r"^/states/[a-z-]+/$", slug)
        hub = self.pick(paths, r"^/asset-classes/[a-z0-9-]+/$", slug)
        program = self.pick(paths, r"^/practice-areas/[a-z0-9-]+/$", slug)
        asset = hub
        if asset is None:
            for key, a in self.topics["assets"].items():
                if a.get("slug_prefix") and slug.startswith(a["slug_prefix"]):
                    asset = key
        return {"url": url, "rel": rel, "slug": slug, "h1": self.h1[url], "state": state,
                "hub": hub, "asset": asset, "program": program}

    def asset_name(self, key):
        return self.topics["assets"].get(key, {}).get("name", key)

    def family(self, key):
        return self.topics["assets"].get(key, {}).get("family", "Other")

    def state_name(self, url):
        return re.sub(r"\s+Feasibility Studies$", "", self.h1.get(url) or "")

    def notes_for_case(self, c):
        out = []
        for n, t in self.topics["notes"].items():
            if c["asset"] in t.get("hubs", []) or (t.get("program_wide") and c["program"] in t.get("programs", [])):
                out.append(n)
        return out

    def note_cases(self, n):
        hubs = set(self.topics["notes"][n].get("hubs", []))
        return [c for c in self.cases if c["asset"] in hubs]

    def related_notes(self, n):
        t = self.topics["notes"][n]
        mine = set(t.get("hubs", [])) | set(t.get("programs", []))
        scored = []
        for m, u in self.topics["notes"].items():
            if m == n:
                continue
            shared = len(mine & (set(u.get("hubs", [])) | set(u.get("programs", []))))
            if shared:
                scored.append((-shared, self.h1[m], m))
        return [m for _, _, m in sorted(scored)[:MAX_RELATED]]


# ---------------------------------------------------------------- rendering

def item(model, url):
    return (url, model.h1[url])


def by_state(model, cs):
    return sorted(cs, key=lambda c: (model.state_name(c["state"]) if c["state"] else "~", c["h1"]))


def section(name, sid, eyebrow, h2, groups, cls):
    out = [f"  <!--mesh:{name}--><section class=\"{cls}\" id=\"{sid}\" aria-labelledby=\"h-{sid}\">",
           "    <div class=\"frame\">",
           "      <div class=\"section-head\">",
           f"        <span class=\"eyebrow\">{esc(eyebrow)}</span>",
           f"        <h2 id=\"h-{sid}\">{esc(h2)}</h2>",
           "      </div>"]
    first = True
    for sub, items in groups:
        if not items:
            continue
        if len(items) > MAX_LIST:
            raise SystemExit(f"mesh:{name}: a list of {len(items)} links (max {MAX_LIST})")
        if sub:
            top = 0 if first else 34
            out.append(f"      <p class=\"lede\" style=\"margin-top:{top}px;margin-bottom:14px\">{esc(sub)}</p>")
        out.append("      <ul class=\"link-cols\">")
        for href, text in items:
            out.append(f"        <li><a href=\"{esc(href)}\">{esc(text)}</a></li>")
        out.append("      </ul>")
        first = False
    out.append("    </div>")
    out.append(f"  </section><!--/mesh:{name}-->")
    return "\n".join(out)


def regions_for(model, url):
    """[(name, sid, eyebrow, h2, groups)] for one page."""
    t = model.topics
    out = []
    sect = links.section(url)
    if sect == "state":
        cs = sorted((c for c in model.cases if c["state"] == url), key=lambda c: (model.asset_name(c["asset"]).lower(), c["h1"]))
        if cs:
            out.append(("state-cases", "worked-cases", "Worked Cases", f"Worked cases in {model.state_name(url)}.",
                        [(None, [item(model, c["url"]) for c in cs])]))
        nb = [n for n in t.get("state_neighbors", {}).get(url, []) if model.site.page_exists(n)]
        if nb:
            out.append(("state-neighbors", "neighbors", "Neighboring Markets", f"States that border {model.state_name(url)}.",
                        [(None, [item(model, n) for n in sorted(nb, key=lambda n: model.h1[n])])]))
    elif sect == "hub":
        cs = by_state(model, [c for c in model.cases if c["asset"] == url])
        name = model.asset_name(url)
        if cs:
            states = sorted({c["state"] for c in cs if c["state"]}, key=lambda u: model.h1[u])
            out.append(("hub-cases", "worked-cases", "Worked Cases", f"{cap(name)} worked cases.",
                        [("The cases" if states else None, [item(model, c["url"]) for c in cs]),
                         ("The states they are set in", [item(model, u) for u in states])]))
        ns = sorted((n for n, v in t["notes"].items() if url in v.get("hubs", [])), key=lambda n: model.h1[n])
        if ns:
            out.append(("hub-notes", "hub-research", "Research", f"Research behind {name} studies.",
                        [(None, [item(model, n) for n in ns])]))
        fam = model.family(url)
        kin = sorted((k for k, a in t["assets"].items() if k != url and a.get("family") == fam and model.site.page_exists(k)),
                     key=lambda k: model.h1[k])
        if kin:
            out.append(("hub-related", "related-assets", "Related", f"Other {fam.lower()} asset classes.",
                        [(None, [item(model, k) for k in kin])]))
    elif sect == "practice":
        cs = [c for c in model.cases if c["program"] == url]
        pname = t["programs"].get(url, {}).get("name", model.h1[url])
        if cs:
            groups = []
            for fam in t["families"] + ["Other"]:
                fc = [c for c in cs if model.family(c["asset"]) == fam]
                if fc:
                    fc = sorted(fc, key=lambda c: (model.asset_name(c["asset"]).lower(), model.state_name(c["state"]) if c["state"] else "~", c["h1"]))
                    groups.append((fam, [item(model, c["url"]) for c in fc]))
            if len(groups) == 1:
                groups = [(None, groups[0][1])]
            out.append(("program-cases", "worked-cases", "Worked Cases", f"{pname} worked cases.", groups))
        ns = sorted((n for n, v in t["notes"].items() if url in v.get("programs", [])), key=lambda n: model.h1[n])
        if ns:
            out.append(("program-notes", "program-research", "Research", f"Research notes for {pname} studies.",
                        [(None, [item(model, n) for n in ns])]))
    elif sect == "case":
        c = next(x for x in model.cases if x["url"] == url)
        sib = by_state(model, [x for x in model.cases if x["asset"] == c["asset"] and x["url"] != url and c["asset"]])[:MAX_SIBLINGS]
        ns = sorted(model.notes_for_case(c), key=lambda n: model.h1[n])
        ctx = [p for p in (c["state"], c["hub"], c["program"]) if p]
        mates = sorted((x for x in model.cases if c["state"] and x["state"] == c["state"] and x["url"] != url and x not in sib),
                       key=lambda x: (model.asset_name(x["asset"]).lower(), x["h1"]))[:MAX_SIBLINGS]
        groups = [(f"Other {model.asset_name(c['asset'])} worked cases", [item(model, x["url"]) for x in sib]),
                  ("Research notes for this case", [item(model, n) for n in ns]),
                  (f"Other worked cases in {model.state_name(c['state'])}" if c["state"] else "", [item(model, x["url"]) for x in mates]),
                  ("Where this case sits", [item(model, p) for p in ctx])]
        if any(g[1] for g in groups):
            out.append(("case-related", "related", "Related", "Related cases and research.", groups))
    elif sect == "note" and url in t["notes"]:
        v = t["notes"][url]
        hubs = [h for h in v.get("hubs", []) if model.site.page_exists(h)]
        progs = [p for p in v.get("programs", []) if model.site.page_exists(p)]
        cs = by_state(model, model.note_cases(url))
        rel = model.related_notes(url)
        groups = [("Asset classes", [item(model, h) for h in sorted(hubs, key=lambda h: model.h1[h])]),
                  ("Practice areas", [item(model, p) for p in progs]),
                  ("Worked cases", [item(model, c["url"]) for c in cs]),
                  ("Related research notes", [item(model, m) for m in rel])]
        if any(g[1] for g in groups):
            out.append(("note-applied", "applied", "Applied In", "Where this research is applied.", groups))
    return out


def place(s, rendered):
    """Remove old mesh regions and insert the new ones before the CTA band."""
    s = REGION_RX.sub("", s)
    # the hand-written Worked Cases sections become generated regions
    s = re.sub(r'[ \t]*<section class="section[^"]*" id="worked-cases" aria-labelledby="h-worked-cases">.*?</section>\n\n', "", s, flags=re.S)
    if not rendered:
        return s
    i = s.find('<section class="cta-band"')
    main_end = s.find("</main>")
    if i < 0 or (main_end >= 0 and i > main_end):
        raise SystemExit("no CTA band to place the mesh before")
    line = s.rfind("\n", 0, i) + 1
    prev = [m.group(1) for m in re.finditer(r'<section class="(section(?: section-alt)?)"', s[:line])]
    alt = bool(prev) and prev[-1] == "section"
    chunks = []
    for name, sid, eyebrow, h2, groups in rendered:
        cls = "section section-alt" if alt else "section"
        chunks.append(section(name, sid, eyebrow, h2, groups, cls) + "\n\n")
        alt = not alt
    return s[:line] + "".join(chunks) + s[line:]


# ---------------------------------------------------------------- first-mention terms

SKIP_TAGS = {"a", "h1", "h2", "h3", "h4", "h5", "h6", "table", "sup", "sub", "code", "pre", "script", "style",
             "button", "label", "figcaption", "nav", "header", "footer", "title", "summary", "aside", "caption",
             "dt", "select", "option", "textarea", "svg"}
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "col", "embed", "param", "track"}
BLOCKS = {"p", "li", "dd", "div", "section", "article", "ul", "ol", "main", "td", "th", "blockquote", "figure", "details", "form"}
TOKEN = re.compile(r"<!--.*?-->|<[^>]+>|[^<]+", re.S)


def term_pattern(term, ignore_case):
    words = [re.escape(html.escape(w, quote=False)) for w in term.split()]
    flags = re.I if ignore_case else 0
    return re.compile(r"(?<![A-Za-z0-9&;-])" + r"\s+".join(words) + r"(?![A-Za-z0-9-])", flags)


def eligible_text(s):
    """(start, end) spans of prose text nodes in <main>, and sba regions that are whole terms."""
    m0 = re.search(r"<main\b", s)
    m1 = s.rfind("</main>")
    if not m0 or m1 < 0:
        return [], []
    stack = []
    texts, sba = [], []
    region = None
    sba_open = None
    for tok in TOKEN.finditer(s, m0.start(), m1):
        t = tok.group(0)
        if t.startswith("<!--"):
            mo = re.match(r"<!--((?:chrome|mesh|fsc):[a-z0-9_.:-]+)", t)
            mc = re.match(r"<!--/((?:chrome|mesh|fsc):[a-z0-9_.:-]+)-->", t)
            so = re.match(r"<!--sba:([a-z0-9_.]+)", t)
            sc = re.match(r"<!--/sba:([a-z0-9_.]+)-->", t)
            if mc and region == mc.group(1):
                region = None
            elif mo and region is None:
                region = mo.group(1)
            elif sc and sba_open and sba_open[0] == sc.group(1):
                sba.append((sba_open[1], tok.end(), sba_open[2], ok_context(stack) and region is None, sba_open[3]))
                sba_open = None
            elif so and sba_open is None:
                sba_open = (so.group(1), tok.start(), tok.end(), "")
            continue
        if t.startswith("</"):
            name = t[2:].strip(" >").lower()
            for k in range(len(stack) - 1, -1, -1):
                if stack[k][0] == name:
                    del stack[k:]
                    break
            continue
        if t.startswith("<"):
            mm = re.match(r"<([a-zA-Z0-9]+)", t)
            if not mm:
                continue
            name = mm.group(1).lower()
            if name in VOID or t.endswith("/>"):
                continue
            stack.append((name, t))
            continue
        if sba_open is not None:
            sba_open = (sba_open[0], sba_open[1], sba_open[2], sba_open[3] + t)
            continue
        if region is None and ok_context(stack):
            texts.append((tok.start(), tok.end()))
    return texts, sba


def ok_context(stack):
    """Prose: the nearest block is a p, li or dd, outside every excluded element."""
    block = None
    for name, tag in stack:
        if name in SKIP_TAGS:
            return False
        cls = re.search(r'class="([^"]*)"', tag)
        cls = cls.group(1) if cls else ""
        idm = re.search(r'id="([^"]*)"', tag)
        ident = idm.group(1) if idm else ""
        if re.search(r"\b(hero|breadcrumb|sources|table-source|capsule|byline|signature|link-cols|cta-band|stat|stats|kpi|data-table-wrap|faq-q)\b", cls):
            return False
        if ident in ("sources",):
            return False
        if name in BLOCKS:
            block = name
    return block in ("p", "li", "dd")


def apply_terms(model, url, s, terms):
    s = TERM_RX.sub(lambda m: m.group(1), s)
    texts, sba = eligible_text(s)
    already = set()
    for a in links.anchors(model.site, url_to_rel(url), url, s):
        if a["kind"] == "a" and a["path"] and a["in_main"] and not a["region"]:
            already.add(a["path"])
    cands = []
    for prio, entry in enumerate(terms):
        target = entry["target"]
        if target == url or target in already or not model.site.page_exists(target):
            continue
        best = None
        for term in entry["terms"]:
            rx = term_pattern(term, entry.get("ignore_case", False))
            for a, b in texts:
                m = rx.search(s, a, b)
                if m and (best is None or m.start() < best[0]):
                    best = (m.start(), m.end())
                    break
            for start, end, inner_start, ok, text in sba:
                if ok and rx.fullmatch(text.strip()) and (best is None or start < best[0]):
                    best = (start, end)
        if best:
            cands.append((prio, best[0], best[1], target, entry["key"]))
    chosen = []
    for prio, a, b, target, key in sorted(cands):
        if len(chosen) >= MAX_TERMS:
            break
        if any(not (b <= x or a >= y) for _, x, y, _, _ in chosen):
            continue
        chosen.append((prio, a, b, target, key))
    for prio, a, b, target, key in sorted(chosen, key=lambda c: -c[1]):
        s = s[:a] + f'<a href="{esc(target)}" data-fsc-term="{esc(key)}">' + s[a:b] + "</a>" + s[b:]
    return s, len(chosen)


def url_to_rel(url):
    return links.url_to_rel(url)


TERM_SECTIONS = {"case", "note", "hub", "state", "practice", "framework"}


def term_page(url):
    return links.section(url) in TERM_SECTIONS or url == "/the-practice/"


# ---------------------------------------------------------------- main

def render_page(model, terms, rel, url, s):
    s = place(s, regions_for(model, url))
    n = 0
    if term_page(url):
        s, n = apply_terms(model, url, s, terms)
    return s, n


def main(argv):
    check = "--check" in argv
    site = links.Site()
    model = Model(site)
    if "--report" in argv:
        print(json.dumps({"cases": model.cases}, indent=1))
        return 0
    terms = load(TERMS)["terms"]
    stale, counts = [], {}
    for rel, url in site.pages:
        if site.held(rel):
            continue
        s = site.text(rel)
        new, n = render_page(model, terms, rel, url, s)
        counts[url] = n
        if new != s:
            stale.append(rel)
            if not check:
                with open(os.path.join(site.root, rel), "w", encoding="utf-8") as fh:
                    fh.write(new)
    label = "out of date" if check else "rewrote"
    for rel in stale:
        print(f"{label}: {rel}")
    held = sum(1 for rel, _ in site.pages if site.held(rel))
    print(f"{len(stale)} page(s) {label}; {held} held; {sum(counts.values())} term link(s) on {sum(1 for v in counts.values() if v)} page(s)")
    return 1 if check and stale else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
