#!/usr/bin/env python3
"""Site chrome for feasibility-study-company.com: header, mega panels, footer.

The site is static HTML with no build step. This script is the template for the
chrome: it renders the header (with the Asset Classes and Markets mega panels),
the footer and the panel script from ONE file, data/site/chrome.json, into

    <!--chrome:header--> ... <!--/chrome:header-->
    <!--chrome:footer--> ... <!--/chrome:footer-->

on every served page. A page without the markers gets them the first time: the
script wraps its <header class="site-header"> and its <footer class="site-footer">
(and the panel script that follows it).

    python3 scripts/chrome.py            rewrite every page's chrome
    python3 scripts/chrome.py --check    exit 1 if any page is out of date or a
                                         chrome link points at a missing page

Each chrome link decides its own state from the tree: the real target when its
page exists; otherwise the pending fallback of scripts/links.py (a link to the
fallback with data-fsc-pending, or a span when the fallback would be the page
itself), or nothing at all for an item marked hide_until_live. When a page ships,
rerun this script and its links switch on. Never edit chrome by hand: edit
data/site/chrome.json and rerun. Pages listed in data/site/hold.json are skipped.
"""
import html
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import links  # noqa: E402

ROOT = links.ROOT
CHROME = os.path.join(ROOT, "data", "site", "chrome.json")

HEADER_REGION = re.compile(r"<!--chrome:header-->.*?<!--/chrome:header-->", re.S)
FOOTER_REGION = re.compile(r"<!--chrome:footer-->.*?<!--/chrome:footer-->", re.S)
RAW_HEADER = re.compile(r'<header class="site-header">.*?</header>', re.S)
RAW_FOOTER = re.compile(r'<footer class="site-footer">.*?</footer>(\s*<script id="mega-markets-script">.*?</script>)?', re.S)

SCRIPT = """<script id="mega-markets-script">
(function(){
  document.querySelectorAll('.has-mega').forEach(function(wrap){
  var btn=wrap.querySelector('.mega-trigger'), panel=wrap.querySelector('.mega-panel');
  if(!btn||!panel) return;
  function open(){panel.classList.add('is-open');btn.setAttribute('aria-expanded','true');}
  function close(){panel.classList.remove('is-open');btn.setAttribute('aria-expanded','false');}
  btn.addEventListener('click',function(e){e.stopPropagation();panel.classList.contains('is-open')?close():open();});
  document.addEventListener('click',function(e){if(!wrap.contains(e.target))close();});
  document.addEventListener('keydown',function(e){if(e.key==='Escape')close();});
  wrap.addEventListener('focusout',function(e){if(!wrap.contains(e.relatedTarget))close();});
  });
})();
</script>"""


def esc(text):
    return html.escape(text, quote=True).replace("→", "&rarr;").replace("©", "&copy;")


class Ctx:
    def __init__(self, site, url):
        self.site = site
        self.url = url
        self.fb = links.load_fallbacks(site.root)

    def local(self, href):
        """'/#contact' is '#contact' on the homepage itself."""
        if self.url == "/" and href.startswith("/#"):
            return href[1:]
        return href

    def link(self, item, attrs="", role=False):
        """One chrome link, resolved against the tree. Returns '' when hidden."""
        label = esc(item["label"])
        href = item["href"]
        path, frag = links.internal_path(href, self.url)
        menu = ' role="menuitem"' if role else ""
        live = path is None or self.site.resolve(path) in ("page", "file", "function")
        if live:
            cur = ""
            if not frag and (path == self.url or (item.get("current_prefix") and self.url.startswith(item["current_prefix"]))):
                cur = ' aria-current="page"'
            return f'<a href="{esc(self.local(href))}"{attrs}{menu}{cur}>{label}</a>'
        if item.get("hide_until_live"):
            return ""
        fallback = item.get("fallback")
        if fallback:
            fpath, ffrag = links.internal_path(fallback, self.url)
            if fpath == self.url or not self.site.page_exists(fpath):
                fallback = None
            elif ffrag and ffrag not in self.site.ids(fpath):
                fallback = fpath
        if fallback is None:
            fallback = links.fallback_for(self.site, path, self.url, self.fb)
        if fallback:
            return (f'<a href="{esc(fallback)}"{attrs}{menu} data-fsc-pending="{esc(href)}">{label}</a>')
        return f'<span data-fsc-pending="{esc(href)}">{label}</span>'


def render_mega(ctx, m):
    style = f' style="{esc(m["style"])}"' if m.get("style") else ""
    out = ['      <div class="has-mega">',
           f'        <button class="mega-trigger" aria-expanded="false" aria-controls="{m["id"]}" aria-haspopup="true">{esc(m["trigger"])}</button>',
           f'        <div class="mega-panel" id="{m["id"]}" role="menu" aria-label="{esc(m["trigger"])}"{style}>']
    for col in m["cols"]:
        cls = f'mega-col {col["class"]}'.strip()
        ls = f' style="{esc(col["list_style"])}"' if col.get("list_style") else ""
        out.append(f'          <div class="{cls}">')
        out.append(f'            <h5>{esc(col["title"])}</h5>')
        out.append(f'            <ul class="mega-list"{ls}>')
        for item in col["items"]:
            a = ctx.link(item, role=True)
            if a:
                out.append(f'              <li>{a}</li>')
        out.append('            </ul>')
        out.append('          </div>')
    foot = m["foot"]
    out.append('          <div class="mega-foot">')
    out.append(f'            {ctx.link(foot)}')
    out.append(f'            <span>{esc(foot["note"])}</span>')
    out.append('          </div>')
    out.append('        </div>')
    out.append('      </div>')
    return out


def render_header(ctx, c):
    w = c["wordmark"]
    out = ['<header class="site-header">',
           '  <div class="frame header-row">',
           '    <div class="wordmark">',
           f'      <a href="{esc(w["href"])}">',
           f'        <span class="mark" aria-hidden="true">{esc(w["mark"])}</span>',
           '        <span class="wordmark-text">',
           f'          <span class="wordmark-name">{esc(w["name"])}</span>',
           f'          <span class="wordmark-tag">{esc(w["tag"])}</span>',
           '        </span>',
           '      </a>',
           '    </div>',
           '    <nav class="site-nav" aria-label="Primary">']
    for item in c["nav"]:
        if "mega" in item:
            out.extend(render_mega(ctx, c["mega"][item["mega"]]))
            continue
        attrs = f' class="{esc(item["class"])}"' if item.get("class") else ""
        a = ctx.link(item, attrs=attrs)
        if a:
            out.append(f'      {a}')
    out.append('    </nav>')
    out.append('  </div>')
    out.append('</header>')
    return "<!--chrome:header-->" + "\n".join(out) + "<!--/chrome:header-->"


def render_footer(ctx, c):
    f = c["footer"]
    out = ['<footer class="site-footer">',
           '  <div class="frame">',
           '    <div class="footer-grid">',
           '      <div class="footer-brand">',
           '        <span class="mark" aria-hidden="true">F</span>',
           f'        <p>{esc(f["brand"])}</p>',
           '      </div>']
    for col in f["cols"]:
        out.append('      <div class="footer-col">')
        out.append(f'        <h4>{esc(col["title"])}</h4>')
        out.append('        <ul>')
        for item in col["items"]:
            if "group" in item:
                parts = [ctx.link(i) for i in item["group"]]
                parts = [p for p in parts if p]
                if parts:
                    out.append('          <li>' + " &middot; ".join(parts) + '</li>')
                continue
            a = ctx.link(item)
            if a:
                out.append(f'          <li>{a}</li>')
        out.append('        </ul>')
        out.append('      </div>')
    out.append('    </div>')
    out.append('    <div class="footer-legal">')
    for line in f["legal"]:
        out.append(f'      <span>{esc(line)}</span>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</footer>')
    return "<!--chrome:footer-->" + "\n".join(out) + "\n" + SCRIPT + "<!--/chrome:footer-->"


def render_page(site, c, rel, url, s):
    ctx = Ctx(site, url)
    head = render_header(ctx, c)
    foot = render_footer(ctx, c)
    if HEADER_REGION.search(s):
        s = HEADER_REGION.sub(lambda m: head, s, count=1)
    elif RAW_HEADER.search(s):
        s = RAW_HEADER.sub(lambda m: head, s, count=1)
    else:
        raise SystemExit(f"{rel}: no header to replace")
    if FOOTER_REGION.search(s):
        s = FOOTER_REGION.sub(lambda m: foot, s, count=1)
    elif RAW_FOOTER.search(s):
        s = RAW_FOOTER.sub(lambda m: foot, s, count=1)
    else:
        raise SystemExit(f"{rel}: no footer to replace")
    # a panel script left outside the region would run twice
    outside = FOOTER_REGION.sub("", s)
    if '<script id="mega-markets-script">' in outside:
        raise SystemExit(f"{rel}: a mega-markets script sits outside the footer region")
    return s


def main(argv):
    check = "--check" in argv
    skip = set()
    if "--skip" in argv:
        skip = set(argv[argv.index("--skip") + 1].split(","))
    site = links.Site()
    with open(CHROME, encoding="utf-8") as fh:
        c = json.load(fh)
    stale, held, bad = [], [], []
    for rel, url in site.pages:
        if site.held(rel) or rel in skip:
            held.append(rel)
            continue
        s = site.text(rel)
        new = render_page(site, c, rel, url, s)
        if new != s:
            stale.append(rel)
            if not check:
                with open(os.path.join(site.root, rel), "w", encoding="utf-8") as fh:
                    fh.write(new)
                s = new
        # every chrome link on the page must resolve (pending links resolve to their fallback)
        for a in links.anchors(site, rel, url, s):
            if a["region"] and a["region"].startswith("chrome:") and links.broken(site, a):
                bad.append(f"{rel}:{a['line']}: chrome link to a missing page: {a['href']}")
            if a["region"] and a["region"].startswith("chrome:") and a["pending"] and links.pending_live(site, a):
                bad.append(f"{rel}:{a['line']}: chrome pending target now exists: {a['pending']}")
        if "<!--chrome:header-->" not in s or "<!--chrome:footer-->" not in s:
            bad.append(f"{rel}: chrome regions missing")
    for b in bad:
        print(b)
    label = "out of date" if check else "rewrote"
    for rel in stale:
        print(f"{label}: {rel}")
    print(f"{len(stale)} page(s) {label}; {len(held)} held; {len(site.pages) - len(held)} checked; {len(bad)} problem(s)")
    if check and (stale or bad):
        return 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
