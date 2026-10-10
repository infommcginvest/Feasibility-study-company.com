#!/usr/bin/env python3
"""WEB-FSC-1 gates 1-8 against a built tree.

The site has no build step: Netlify publishes the repository root as committed.
The "build" is therefore `git archive <ref>` into a directory, which is exactly
the tree Netlify serves. Usage:

    python3 gates.py <built_dir> <baseline_dir> <repo_root>

Writes nothing; prints a report and exits 1 if any gate is red.
"""
import codecs
import difflib
import html
import json
import os
import re
import sys
import urllib.parse

BUILT, BASE, REPO = sys.argv[1:4]
INPUT = os.path.join(REPO, "docs", "web-fsc-1", "input")
CASES = ["rv-park-ossipee-new-hampshire-usda", "cabin-resort-townsend-tennessee-sba",
         "glamping-oak-hill-west-virginia-usda", "dry-stack-cape-coral-florida-sba"]
# constraint 5 pattern, rot13-encoded so this file does not itself carry the names
NAMES = re.compile(codecs.decode("zzpt|zburyfxl|havbazrgevp|znvqra ynar", "rot13"), re.I)
CREDS = re.compile(r"otava,? *(ph\.?d|ccim|mai)", re.I)
PLACEHOLDERS = re.compile(r"\[VERIFY|\[BIO|\{\{byline\}\}|\{\{signature\}\}")
results = []


def gate(n, name, ok, detail=""):
    results.append((n, name, ok))
    print(f"\n=== Gate {n}: {name}: {'GREEN' if ok else 'RED'}")
    if detail:
        print(detail)


def walk(root, exts=None):
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != ".git"]
        for f in files:
            if exts is None or f.endswith(exts):
                yield os.path.join(d, f)


def read(p):
    with open(p, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def pages(root):
    return sorted(os.path.relpath(p, root) for p in walk(root, (".html",)))


# ---- 1. page count
base_pages, built_pages = pages(BASE), pages(BUILT)
added = sorted(set(built_pages) - set(base_pages))
gate(1, "page count = baseline + 4", len(built_pages) == len(base_pages) + 4
     and added == sorted(f"case-studies/{c}/index.html" for c in CASES),
     f"baseline {len(base_pages)}, built {len(built_pages)}, added {added}")


# ---- 2. text fidelity
def md_words(path):
    text = read(path)
    text = text[text.index("\n---\n", 4) + 5:]
    text = re.sub(r"<!--.*?-->", " ", text, flags=re.S)
    out = []
    for line in text.split("\n"):
        s = line.strip()
        if s in ("{{byline}}", "{{signature}}") or re.match(r"^\|[-| ]+\|$", s):
            continue
        s = re.sub(r"^#+ ", "", s)
        s = re.sub(r"^> ", "", s)
        s = re.sub(r"^\d+\. ", "", s)
        s = re.sub(r"^- ", "", s)
        s = s.replace("|", " ")
        s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
        s = s.replace("**", "")
        out.append(s)
    return " ".join(out).split()


def html_words(path):
    s = read(path)
    s = s[s.index('<main id="main">'):s.index("</main>")]
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = re.sub(r"</?(a|strong|em|time|span|sup)\b[^>]*>", "", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return html.unescape(s).split()


fid_lines, fid_ok = [], True
targets = [(os.path.join(INPUT, "case-studies", c + ".md"), os.path.join(BUILT, "case-studies", c, "index.html")) for c in CASES]
targets.append((os.path.join(INPUT, "about", "about.md"), os.path.join(BUILT, "the-practice", "index.html")))
for md, built in targets:
    a, b = md_words(md), html_words(built)
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    diffs = [op for op in sm.get_opcodes() if op[0] != "equal"]
    fid_lines.append(f"-- {os.path.relpath(built, BUILT)}: {len(a)} input words, {len(b)} built words, {len(diffs)} difference(s)")
    for tag, i1, i2, j1, j2 in diffs:
        fid_lines.append(f"   {tag:7} input: {' '.join(a[i1:i2])[:300]!r}")
        fid_lines.append(f"           built: {' '.join(b[j1:j2])[:300]!r}")
# Every difference is listed; DECISIONS.md section "Text fidelity" justifies each class.
gate(2, "text fidelity (differences listed for DECISIONS.md)", fid_ok, "\n".join(fid_lines))


# ---- 3. credentials grep (source = repo working tree, built = archive)
hits = [p for root in (REPO, BUILT) for p in walk(root) if CREDS.search(read(p))]
gate(3, "credentials grep returns nothing", not hits, "\n".join(hits))

# ---- 4. placeholders in built output
hits = [os.path.relpath(p, BUILT) for p in walk(BUILT) if PLACEHOLDERS.search(read(p))]
gate(4, "placeholders absent from built output", not hits, "\n".join(hits))

# ---- 5. names: changed files and built output; pre-existing hits reported separately
base_hits = {os.path.relpath(p, BASE) for p in walk(BASE) if NAMES.search(read(p))}
built_hits = {os.path.relpath(p, BUILT) for p in walk(BUILT) if NAMES.search(read(p))}
new_hits = []
for rel in sorted(built_hits):
    now = len(NAMES.findall(read(os.path.join(BUILT, rel))))
    before = len(NAMES.findall(read(os.path.join(BASE, rel)))) if rel in base_hits else 0
    if now > before:
        new_hits.append(f"{rel}: {before} -> {now}")
gate(5, "names grep across changed files and built output returns nothing", not built_hits,
     f"files with hits in built output: {len(built_hits)}; at baseline: {len(base_hits)}; "
     f"hits ADDED by this lane: {len(new_hits)}\n" + "\n".join(new_hits)
     + "\npre-existing files: " + ", ".join(sorted(built_hits)))


# ---- 6. internal links
def targets_of(root, rel):
    s = read(os.path.join(root, rel))
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    for href in re.findall(r'href="([^"]+)"', s):
        yield html.unescape(href)


def resolve(root, rel, href):
    """-> None if fine, else the broken target (path#frag)."""
    u = urllib.parse.urlparse(href)
    if u.scheme in ("http", "https", "mailto", "tel") and u.netloc not in ("feasibility-study-company.com", "www.feasibility-study-company.com"):
        return None
    path = u.path
    if not path:
        page = rel
    else:
        if not path.startswith("/"):
            path = "/" + os.path.normpath(os.path.join(os.path.dirname(rel), path))
        if path == "/api/contact":
            return None
        cand = path.lstrip("/")
        if cand == "" or cand.endswith("/"):
            cand += "index.html"
        if not os.path.isfile(os.path.join(root, cand)):
            if os.path.isfile(os.path.join(root, cand, "index.html")):
                cand = os.path.join(cand, "index.html")
            else:
                return path
        page = cand
    if u.fragment and page.endswith(".html"):
        ids = set(re.findall(r'\sid="([^"]+)"', read(os.path.join(root, page))))
        if u.fragment not in ids:
            return f"{path or '/' + rel}#{u.fragment}"
    return None


def broken(root):
    out = {}
    for rel in pages(root):
        for href in targets_of(root, rel):
            t = resolve(root, rel, href)
            if t:
                out.setdefault(t, set()).add(rel)
    return out


b_base, b_built = broken(BASE), broken(BUILT)
new_targets = sorted(set(b_built) - set(b_base))
# a pre-existing broken target newly linked from a page this lane created is also reported
new_pages = set(added) | {"the-practice/index.html"}
new_refs = sorted(f"{t} <- {sorted(set(b_built[t]) & new_pages)}" for t in b_built
                  if t in b_base and set(b_built[t]) & new_pages)
detail = (f"broken targets at baseline: {len(b_base)}; built: {len(b_built)}; NEW broken targets: {len(new_targets)}\n"
          + "\n".join(f"  NEW {t} <- {sorted(b_built[t])[:5]}" for t in new_targets)
          + "\npre-existing broken targets also linked from the new or replaced pages (house header/footer):\n  "
          + "\n  ".join(new_refs))
gate(6, "zero new broken internal links", not new_targets, detail)
with open(os.path.join(os.environ.get("FSC_OUT", "."), "preexisting-404s.json"), "w") as fh:
    json.dump({t: sorted(v) for t, v in sorted(b_base.items())}, fh, indent=1)

# ---- 7. JSON-LD on changed pages
changed = [l.strip() for l in open(os.environ["FSC_CHANGED"]) if l.strip().endswith(".html")]
bad, missing = [], []
for rel in changed:
    s = read(os.path.join(BUILT, rel))
    nodes = []
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
        try:
            d = json.loads(blk)
        except ValueError as e:
            bad.append(f"{rel}: {e}")
            continue
        nodes += d.get("@graph", [d])
    if rel.startswith("case-studies/") and rel != "case-studies/index.html":
        types = {n.get("@type") if isinstance(n.get("@type"), str) else "+".join(n["@type"]) for n in nodes}
        art = [n for n in nodes if n.get("@type") == "Article"]
        if "Article" not in types or "BreadcrumbList" not in types or not art or \
                art[0].get("author", {}).get("@id") != "https://feasibility-study-company.com/#mark-otava":
            missing.append(rel)
gate(7, "JSON-LD parses on changed pages; cases carry Article, BreadcrumbList, author @id",
     not bad and not missing, f"changed pages checked: {len(changed)}\n" + "\n".join(bad + [f"missing: {m}" for m in missing]))

# ---- 7b. head sanity: each changed page parses to exactly one <title> and its CSS is live (added after
# the first look pass caught a title regex that swallowed the head on the new pages)
from html.parser import HTMLParser


class Head(HTMLParser):
    def __init__(self):
        super().__init__()
        self.titles, self.styles, self.in_title, self.text = 0, 0, False, ""

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.titles += 1
            self.in_title = True
        if tag == "style":
            self.styles += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.text += data


def head_ok(path):
    h = Head()
    h.feed(read(path))
    return h.titles == 1 and h.styles >= 1 and h.text.strip(), f"titles={h.titles} styles={h.styles}"


insane, pre_broken = [], []
for rel in changed:
    ok, info = head_ok(os.path.join(BUILT, rel))
    if ok:
        continue
    base = os.path.join(BASE, rel)
    if os.path.isfile(base) and not head_ok(base)[0]:
        pre_broken.append(f"{rel}: {info} (already broken at baseline)")
    else:
        insane.append(f"{rel}: {info}")
gate("7b", "head sanity on changed pages: none broken by this lane", not insane,
     "\n".join(insane + ["pre-existing: " + p for p in pre_broken]))

# ---- 8. disclosure box
miss = [c for c in CASES if 'class="capsule disclosure"' not in read(os.path.join(BUILT, "case-studies", c, "index.html"))
        or "<strong>Representative worked example.</strong>" not in read(os.path.join(BUILT, "case-studies", c, "index.html"))]
gate(8, "disclosure box on all four cases", not miss, "\n".join(miss))

print("\n=== SUMMARY")
for n, name, ok in results:
    print(f"Gate {n}: {'GREEN' if ok else 'RED'}  {name}")
sys.exit(0 if all(ok for _, _, ok in results) else 1)
