#!/usr/bin/env python3
"""Internal links and promised (pending) links for feasibility-study-company.com.

The site is static HTML served from the repository root with no build step. This
script keeps every internal link pointing at a page that exists, without deleting
the links the site promises to pages that are not built yet (metros, asset
subtypes, missing hubs, framework subpages, Ohio).

A promised link keeps its anchor words and carries the real target in
data-fsc-pending. Where a truthful fallback exists the href points to it:

    <a href="/states/texas/#metros" data-fsc-pending="/states/texas/houston/">Houston</a>

Where the fallback would be the page itself, or nothing truthful exists, the
anchor becomes a span with the same text:

    <span data-fsc-pending="/asset-classes/cold-storage/">cold storage</span>

    python3 scripts/links.py             mark every broken link outside generated regions as pending
    python3 scripts/links.py --check     exit 1 on any broken link that is not pending, or any
                                         pending target that now exists
    python3 scripts/links.py --relink    restore every pending link whose page now exists
    python3 scripts/links.py --report    print link and inbound counts as JSON
    python3 scripts/links.py --pending-csv PATH   write the pending inventory

Anchors inside generated regions (chrome:, mesh:, fsc:, sba: and the other
script-owned markers) are left to the script that owns the region; --check still
reads them. Every lane that builds pages runs --relink, then chrome.py and mesh.py.
"""
import csv
import fnmatch
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://feasibility-study-company.com"
HOSTS = ("https://feasibility-study-company.com", "http://feasibility-study-company.com",
         "https://www.feasibility-study-company.com", "http://www.feasibility-study-company.com")

# Top-level folders that are not pages: records, sources, scripts, data, functions.
SKIP_TOP = {"docs", "src", "scripts", "data", "netlify", "node_modules", "_bundles"}
SKIP_FILE = re.compile(r"^(preview-.*|index_\d+)\.html$")

# Pages whose links do not count as contextual inbound links: the homepage and
# section indexes list everything; the 404 page and the NDA tool are utilities.
INDEX_PAGES = {"/", "/case-studies/", "/asset-classes/", "/states/", "/research-notes/",
               "/practice-areas/", "/404.html", "/tools/nda/"}

# Script-owned regions. links.py never rewrites an anchor inside one.
REGION = re.compile(r"<!--((?:chrome|mesh|fsc|sba|terms):[a-z0-9_.:-]+)(?: \{.*?\})?-->(.*?)<!--/\1-->", re.S)

A_TAG = re.compile(r"<a\b([^>]*)>(.*?)</a\s*>", re.S | re.I)
SPAN_PENDING = re.compile(r'<span\b([^>]*\bdata-fsc-pending="[^"]*"[^>]*)>(.*?)</span\s*>', re.S | re.I)
ATTR = re.compile(r'([a-zA-Z_:][-a-zA-Z0-9_:.]*)\s*=\s*("([^"]*)"|\'([^\']*)\')')
ID_ATTR = re.compile(r'\bid\s*=\s*"([^"]+)"')


# ---------------------------------------------------------------- the tree

def served_pages(root=ROOT):
    """Every served HTML file, as (rel_path, url)."""
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir == ".":
            dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_TOP)
        else:
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            if not fn.endswith(".html") or SKIP_FILE.match(fn):
                continue
            rel = fn if rel_dir == "." else rel_dir + "/" + fn
            out.append((rel, rel_to_url(rel)))
    return out


def served_files(root=ROOT):
    """Every served non-HTML file under the root, as URL paths."""
    out = set()
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir == ".":
            dirnames[:] = [d for d in dirnames if not d.startswith(".") and d not in ("docs", "src", "node_modules", "_bundles")]
        else:
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for fn in filenames:
            if fn.endswith(".html") or fn.startswith("."):
                continue
            rel = fn if rel_dir == "." else rel_dir + "/" + fn
            out.add("/" + rel)
    return out


def rel_to_url(rel):
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def url_to_rel(url):
    if url.endswith("/"):
        return url[1:] + "index.html"
    return url[1:]


def redirect_sources(root=ROOT):
    """(from, to, status) rules in netlify.toml."""
    path = os.path.join(root, "netlify.toml")
    rules = []
    if not os.path.exists(path):
        return rules
    text = open(path, encoding="utf-8").read()
    for block in re.split(r"\[\[redirects\]\]", text)[1:]:
        f = re.search(r'from\s*=\s*"([^"]+)"', block)
        t = re.search(r'to\s*=\s*"([^"]+)"', block)
        st = re.search(r"status\s*=\s*(\d+)", block)
        if f and t:
            rules.append((f.group(1), t.group(1), int(st.group(1)) if st else 301))
    return rules


def load_hold(root=ROOT):
    path = os.path.join(root, "data", "site", "hold.json")
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as fh:
        return list(json.load(fh).get("pages", []))


class Site:
    def __init__(self, root=ROOT):
        self.root = root
        self.pages = served_pages(root)
        self.urls = {u for _, u in self.pages}
        self.files = served_files(root)
        self.redirects = redirect_sources(root)
        self.hold = load_hold(root)
        self._ids = {}

    def held(self, rel):
        """True for a page another lane owns while it rebuilds it (data/site/hold.json)."""
        return any(fnmatch.fnmatch(rel, pat) for pat in self.hold)

    def text(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def page_exists(self, path):
        return path in self.urls

    def resolve(self, path):
        """'page', 'file', 'redirect:<to>', 'function', 'noslash' or None."""
        if path in self.urls:
            return "page"
        if path in self.files:
            return "file"
        if not path.endswith("/") and (path + "/") in self.urls:
            return "noslash"
        for f, t, st in self.redirects:
            if f.endswith("/*"):
                base = f[:-2]
                if path == base or path == base + "/" or path.startswith(base + "/"):
                    return ("function" if t.startswith("/.netlify/functions/") else
                            "blocked" if st == 404 else "redirect:" + t)
            elif path == f:
                return "function" if t.startswith("/.netlify/functions/") else (
                    "blocked" if st == 404 else "redirect:" + t)
        return None

    def ids(self, url):
        if url not in self._ids:
            rel = url_to_rel(url)
            try:
                s = mask(self.text(rel))
            except OSError:
                s = ""
            self._ids[url] = set(ID_ATTR.findall(s))
        return self._ids[url]


# ---------------------------------------------------------------- parsing

def mask(s):
    """Blank comments, scripts and styles (same length) so tag searches skip them."""
    def blank(m):
        return re.sub(r"[^\n]", " ", m.group(0))
    s = re.sub(r"<!--.*?-->", blank, s, flags=re.S)
    s = re.sub(r"<script\b.*?</script\s*>", blank, s, flags=re.S | re.I)
    s = re.sub(r"<style\b.*?</style\s*>", blank, s, flags=re.S | re.I)
    return s


def attrs(tag_attrs):
    out = {}
    for m in ATTR.finditer(tag_attrs):
        out[m.group(1).lower()] = html.unescape(m.group(3) if m.group(3) is not None else m.group(4))
    return out


def internal_path(href, base_url):
    """URL path of an internal href (no query, no fragment), the fragment, or (None, None)."""
    if href is None:
        return None, None
    href = href.strip()
    if not href or href.startswith(("mailto:", "tel:", "javascript:", "data:", "sms:")):
        return None, None
    for h in HOSTS:
        if href == h or href.startswith(h + "/") or href.startswith(h + "#") or href.startswith(h + "?"):
            href = href[len(h):] or "/"
            break
    else:
        if re.match(r"^[a-z][a-z0-9+.-]*:", href, re.I) or href.startswith("//"):
            return None, None
    frag = None
    if "#" in href:
        href, frag = href.split("#", 1)
    if "?" in href:
        href = href.split("?", 1)[0]
    if href == "":
        return base_url, frag
    if not href.startswith("/"):
        base_dir = base_url if base_url.endswith("/") else base_url.rsplit("/", 1)[0] + "/"
        parts = (base_dir + href).split("/")
        stack = []
        for p in parts:
            if p == "..":
                if len(stack) > 1:
                    stack.pop()
            elif p != ".":
                stack.append(p)
        href = "/".join(stack)
    return href, frag


def regions(s):
    return [(m.start(), m.end(), m.group(1)) for m in REGION.finditer(s)]


def region_at(spans, pos):
    for a, b, name in spans:
        if a <= pos < b:
            return name
    return None


def landmarks(m):
    """Offsets of <main>...</main> and breadcrumb navs in a masked page."""
    a = re.search(r"<main\b", m)
    b = m.rfind("</main>")
    main = (a.start(), b) if a and b > 0 else (0, 0)
    crumbs = []
    for c in re.finditer(r'<nav\b[^>]*class="[^"]*\bbreadcrumb\b[^"]*"[^>]*>', m):
        e = m.find("</nav>", c.end())
        crumbs.append((c.start(), e if e > 0 else c.end()))
    return main, crumbs


def strip_tags(t):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip()


def anchors(site, rel, url, s=None):
    """Every <a> and pending <span> on a page with its context."""
    s = s if s is not None else site.text(rel)
    m = mask(s)
    spans = regions(s)
    main, crumbs = landmarks(m)
    out = []
    for kind, rx in (("a", A_TAG), ("span", SPAN_PENDING)):
        for t in rx.finditer(m):
            raw = s[t.start():t.end()]
            inner_raw = s[t.start(2):t.end(2)]
            at = attrs(t.group(1))
            href = at.get("href") if kind == "a" else None
            path, frag = internal_path(href, url) if href is not None else (None, None)
            pos = t.start()
            out.append({
                "kind": kind, "start": t.start(), "end": t.end(), "raw": raw,
                "attrs": at, "href": href, "path": path, "frag": frag,
                "pending": at.get("data-fsc-pending"), "text": strip_tags(inner_raw),
                "inner": inner_raw, "region": region_at(spans, pos),
                "in_main": main[0] <= pos < main[1],
                "in_crumb": any(a <= pos < b for a, b in crumbs),
                "line": s.count("\n", 0, pos) + 1,
            })
    out.sort(key=lambda x: x["start"])
    return out


# ---------------------------------------------------------------- classes and fallbacks

def classify(path):
    if path in ("/inquiries/", "/inquiries"):
        return "retired-inquiries"
    if path.startswith("/published-analyses"):
        return "retired-published-analyses"
    if path.startswith("/infrastructure"):
        return "retired-infrastructure"
    if re.match(r"^/states/[a-z0-9-]+/[a-z0-9-]+/?$", path):
        return "metro"
    if re.match(r"^/states/[a-z0-9-]+/?$", path):
        return "state"
    if re.match(r"^/asset-classes/[a-z0-9-]+/[a-z0-9-]+/?$", path):
        return "subtype"
    if re.match(r"^/asset-classes/[a-z0-9-]+/?$", path):
        return "hub"
    if path.startswith("/analytical-framework/"):
        return "framework"
    return "other"


def load_fallbacks(root=ROOT):
    path = os.path.join(root, "data", "mesh", "fallbacks.json")
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def fallback_for(site, path, page_url, fb):
    """The truthful fallback href for a pending target, or None for a span."""
    target = path if path.endswith("/") else path + "/"
    rule = fb.get("targets", {}).get(target)
    href = None
    if rule is not None:
        href = rule or None
    else:
        cls = classify(target)
        if cls == "metro":
            state = "/" + "/".join(target.strip("/").split("/")[:2]) + "/"
            if site.page_exists(state):
                href = state + ("#metros" if "metros" in site.ids(state) else "")
        elif cls == "subtype":
            hub = "/" + "/".join(target.strip("/").split("/")[:2]) + "/"
            sect = fb.get("subtype_sections", {}).get(hub)
            if site.page_exists(hub):
                href = hub + ("#" + sect if sect and sect in site.ids(hub) else "")
    if href is None:
        return None
    hpath, hfrag = internal_path(href, page_url)
    if hpath == page_url:
        return None          # the fallback would be the page itself
    if not site.page_exists(hpath):
        return None
    if hfrag and hfrag not in site.ids(hpath):
        href = hpath
    return href


# ---------------------------------------------------------------- rewriting

def set_attr(tag_open, name, value):
    """Set or replace one attribute on an opening tag string."""
    rx = re.compile(r'\s%s\s*=\s*("[^"]*"|\'[^\']*\')' % re.escape(name))
    val = '%s="%s"' % (name, html.escape(value, quote=True))
    if rx.search(tag_open):
        return rx.sub(" " + val, tag_open, count=1)
    return tag_open[:-1].rstrip() + " " + val + ">"


def drop_attr(tag_open, name):
    return re.sub(r'\s%s\s*=\s*("[^"]*"|\'[^\']*\')' % re.escape(name), "", tag_open, count=1)


def open_tag(raw):
    return raw[: raw.index(">") + 1]


def make_pending(a, fallback):
    """Rewrite one <a> as a pending link (to fallback) or a pending span."""
    real = a["path"] if a["path"].endswith("/") or "." in a["path"].rsplit("/", 1)[-1] else a["path"] + "/"
    if fallback:
        tag = set_attr(open_tag(a["raw"]), "href", fallback)
        tag = set_attr(tag, "data-fsc-pending", real)
        return tag + a["inner"] + "</a>"
    keep = {k: v for k, v in a["attrs"].items() if k in ("class", "id")}
    tag = "<span" + "".join(' %s="%s"' % (k, html.escape(v, quote=True)) for k, v in keep.items())
    tag += ' data-fsc-pending="%s">' % html.escape(real, quote=True)
    return tag + a["inner"] + "</span>"


def relink(a):
    target = a["pending"]
    if a["kind"] == "a":
        tag = drop_attr(set_attr(open_tag(a["raw"]), "href", target), "data-fsc-pending")
        return tag + a["inner"] + "</a>"
    keep = {k: v for k, v in a["attrs"].items() if k in ("class", "id")}
    tag = "<a" + ' href="%s"' % html.escape(target, quote=True)
    tag += "".join(' %s="%s"' % (k, html.escape(v, quote=True)) for k, v in keep.items()) + ">"
    return tag + a["inner"] + "</a>"


def norm_slash(path):
    return path if path.endswith("/") or "." in path.rsplit("/", 1)[-1] else path + "/"


def rewrite_for(a, url, fb):
    """The replacement for a link to a retired or alias path, or None."""
    if a["kind"] != "a" or not a["path"] or a["pending"]:
        return None
    path = norm_slash(a["path"])
    new = fb.get("rewrites", {}).get(path)
    if new is None:
        return None
    npath, nfrag = internal_path(new, url)
    if npath == url and not nfrag:
        real = fb.get("rewrite_self", {}).get(path, path)
        return make_pending(dict(a, path=real), None)
    if url == "/" and new.startswith("/#"):
        new = new[1:]
    return set_attr(open_tag(a["raw"]), "href", new) + a["inner"] + "</a>"


def splice(s, edits):
    for start, end, new in sorted(edits, key=lambda e: -e[0]):
        s = s[:start] + new + s[end:]
    return s


# ---------------------------------------------------------------- modes

def broken(site, a):
    """True when an anchor's internal target does not resolve."""
    if a["kind"] != "a" or a["path"] is None:
        return False
    return site.resolve(a["path"]) is None


def pending_live(site, a):
    if not a["pending"]:
        return False
    p, _ = internal_path(a["pending"], "/")
    return p is not None and site.resolve(p) in ("page", "file", "noslash")


def scan(site):
    rows = []
    for rel, url in site.pages:
        for a in anchors(site, rel, url):
            rows.append((rel, url, a))
    return rows


def apply(site, mode, skip=()):
    fb = load_fallbacks(site.root)
    changed = []
    for rel, url in site.pages:
        if site.held(rel) or rel in skip:
            continue
        s = site.text(rel)
        edits = []
        for a in anchors(site, rel, url, s):
            if a["region"]:
                continue
            rw = rewrite_for(a, url, fb) if mode == "mark" else None
            if rw is not None:
                edits.append((a["start"], a["end"], rw))
            elif mode == "relink" and a["pending"] and pending_live(site, a):
                edits.append((a["start"], a["end"], relink(a)))
            elif mode == "mark" and not a["pending"] and broken(site, a):
                edits.append((a["start"], a["end"], make_pending(a, fallback_for(site, a["path"], url, fb))))
            elif mode == "mark" and a["pending"] and a["kind"] == "a":
                # keep the fallback truthful if the fallback page moved
                p, _ = internal_path(a["href"], url)
                if site.resolve(p) is None:
                    target, _ = internal_path(a["pending"], url)
                    new = fallback_for(site, target, url, fb)
                    a2 = dict(a, path=target)
                    edits.append((a["start"], a["end"], make_pending(a2, new)))
        if edits:
            new_s = splice(s, edits)
            if new_s != s:
                with open(os.path.join(site.root, rel), "w", encoding="utf-8") as fh:
                    fh.write(new_s)
                changed.append((rel, len(edits)))
    return changed


def check(site):
    problems = []
    pend = {}
    fb = load_fallbacks(site.root)
    retired = set(fb.get("rewrites", {}))
    for rel, url, a in scan(site):
        if site.held(rel):
            continue
        if a["pending"]:
            cls = classify(internal_path(a["pending"], url)[0] or "")
            pend[cls] = pend.get(cls, 0) + 1
            if pending_live(site, a):
                problems.append(f"{rel}:{a['line']}: pending target now exists: {a['pending']} ({a['text']!r}); run --relink")
            if a["kind"] == "a" and broken(site, a):
                problems.append(f"{rel}:{a['line']}: pending fallback is broken: {a['href']}")
            continue
        if a["kind"] == "a" and a["path"] and norm_slash(a["path"]) in retired:
            problems.append(f"{rel}:{a['line']}: link to a retired or alias path: {a['href']} ({a['text']!r})")
        elif broken(site, a):
            problems.append(f"{rel}:{a['line']}: broken internal link: {a['href']} ({a['text']!r})")
        elif a["path"] and a["frag"] and site.resolve(a["path"]) == "page" and a["frag"] not in site.ids(a["path"]):
            problems.append(f"{rel}:{a['line']}: missing fragment: {a['href']}")
    return problems, pend


def inbound(site):
    """Distinct contextual source pages per target page."""
    src = {u: set() for u in site.urls}
    for rel, url, a in scan(site):
        if a["kind"] != "a" or not a["path"] or not a["in_main"] or a["in_crumb"]:
            continue
        if url in INDEX_PAGES or a["region"] and a["region"].startswith("chrome:"):
            continue
        p = a["path"]
        if site.resolve(p) == "noslash":
            p += "/"
        if p in src and p != url:
            src[p].add(url)
    return src


def section(url):
    if url in INDEX_PAGES:
        return "index"
    first = url.strip("/").split("/")[0]
    return {"case-studies": "case", "asset-classes": "hub", "states": "state",
            "research-notes": "note", "practice-areas": "practice",
            "analytical-framework": "framework"}.get(first, "other")


def report(site):
    rows = scan(site)
    broken_targets = {}
    for rel, url, a in rows:
        if not a["pending"] and broken(site, a):
            broken_targets.setdefault(a["path"], set()).add(rel)
    by_class = {}
    for p in broken_targets:
        by_class[classify(p)] = by_class.get(classify(p), 0) + 1
    inb = inbound(site)
    stats = {}
    for u, srcs in inb.items():
        stats.setdefault(section(u), []).append(len(srcs))
    def med(v):
        v = sorted(v)
        return v[len(v) // 2] if len(v) % 2 else (v[len(v) // 2 - 1] + v[len(v) // 2]) / 2
    return {
        "pages": len(site.pages),
        "broken_distinct_targets": len(broken_targets),
        "broken_by_class": by_class,
        "pending_anchors": sum(1 for _, _, a in rows if a["pending"]),
        "inbound": {k: {"n": len(v), "min": min(v), "median": med(v)} for k, v in sorted(stats.items())},
        "under_3": sorted(u for u, s in inb.items() if len(s) < 3 and section(u) not in ("index", "other")),
    }


def pending_csv(site, path):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["anchor_text", "page", "real_target", "fallback", "class", "region"])
        for rel, url, a in scan(site):
            if a["pending"]:
                w.writerow([a["text"], url, a["pending"], a["href"] or "(span)",
                            classify(internal_path(a["pending"], url)[0] or ""), a["region"] or ""])


def main(argv):
    site = Site()
    if "--report" in argv:
        print(json.dumps(report(site), indent=1))
        return 0
    if "--pending-csv" in argv:
        pending_csv(site, argv[argv.index("--pending-csv") + 1])
        return 0
    if "--check" in argv:
        problems, pend = check(site)
        for p in problems:
            print(p)
        print(f"pending anchors by class: {json.dumps(pend, sort_keys=True)}")
        held = sum(1 for rel, _ in site.pages if site.held(rel))
        print(f"{len(problems)} problem(s) over {len(site.pages) - held} checked pages ({held} held, data/site/hold.json)")
        return 1 if problems else 0
    mode = "relink" if "--relink" in argv else "mark"
    skip = set(argv[argv.index("--skip") + 1].split(",")) if "--skip" in argv else set()
    changed = apply(site, mode, skip)
    for rel, n in changed:
        print(f"{'relinked' if mode == 'relink' else 'marked'} {n:3d}  {rel}")
    print(f"{len(changed)} page(s) changed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
