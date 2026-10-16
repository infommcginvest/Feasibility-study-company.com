#!/usr/bin/env python3
"""WEB-FSC-4 gates 1, 2 and 4 to 12 and the offline half of 14, run on `git archive` trees.

    python3 docs/web-fsc-4/tools/gates.py [HEAD_REF] [BASE_REF]

HEAD_REF (default HEAD) is extracted to a scratch directory and every check runs
there, so untracked files never count. BASE_REF (default 1d48cc2, the cut point)
is extracted beside it for the before/after measures. Prints one block per gate
and a summary line; exits 1 if any gate is red. Gates 3, 13, 15 and the served
half of 14 need the draft deploy and a browser and are recorded separately.
"""
import fnmatch
import html
import importlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
# The ruling 10 set, bracketed so this served file never matches itself.
NAMES = re.compile(r"m[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er", re.I)
CREDS = re.compile(r"otava,? *(ph\.?d|ccim|mai)", re.I)
EMEN = re.compile(r"—|–|&mdash;|&ndash;|&#8212;|&#8211;|&#x2014;|&#x2013;", re.I)
RECOMPUTED = ["rv-boat-storage-arizona-sba", "rv-boat-storage-california-sba", "rv-boat-storage-florida-sba",
              "medical-office-north-carolina-sba"]
RESULTS = []


def run(cmd, cwd, timeout=600):
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, (p.stdout + p.stderr).strip()


def extract(ref, dest):
    os.makedirs(dest, exist_ok=True)
    arch = subprocess.run(["git", "-C", REPO, "archive", ref], capture_output=True, timeout=120, check=True).stdout
    subprocess.run(["tar", "-x", "-C", dest], input=arch, timeout=120, check=True)
    return dest


def gate(n, name, ok, lines):
    RESULTS.append((n, name, ok))
    print(f"\n== Gate {n}: {name}: {'GREEN' if ok else 'RED'}")
    for l in lines:
        print("   " + l)


def load(root, mod):
    sys.path.insert(0, os.path.join(root, "scripts"))
    for m in ("links", "mesh", "chrome", "sitemap"):
        sys.modules.pop(m, None)
    try:
        return importlib.import_module(mod)
    finally:
        sys.path.pop(0)


def visible(raw):
    t = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    t = re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", t, flags=re.S | re.I)
    return html.unescape(re.sub(r"<[^>]+>", " ", t))


def words(t):
    return re.findall(r"[0-9a-zÀ-ɏ]+", t.lower())


def body_words(raw):
    """Visible words of the body outside the chrome, the generated regions and the byline."""
    b = raw[raw.find("<body"):] if "<body" in raw else raw
    b = re.sub(r"<!--(chrome|mesh):([a-z0-9-]+)-->.*?<!--/\1:\2-->", " ", b, flags=re.S)
    b = re.sub(r'<header class="site-header">.*?</header>', " ", b, flags=re.S)
    b = re.sub(r'<footer class="site-footer">.*?</footer>', " ", b, flags=re.S)
    b = re.sub(r"<!--fsc:byline-article.*?<!--/fsc:byline-article-->", " ", b, flags=re.S)
    b = re.sub(r'<section class="section[^"]*" id="worked-cases".*?</section>', " ", b, flags=re.S)
    return words(visible(b))


def main(argv):
    head_ref = argv[0] if argv else "HEAD"
    base_ref = argv[1] if len(argv) > 1 else "1d48cc2"
    tmp = tempfile.mkdtemp(prefix="wfsc4-gates-", dir=os.environ.get("TMPDIR"))
    head = extract(head_ref, os.path.join(tmp, "head"))
    base = extract(base_ref, os.path.join(tmp, "base"))
    sha = subprocess.run(["git", "-C", REPO, "rev-parse", head_ref], capture_output=True, text=True).stdout.strip()
    print(f"gates on {head_ref} = {sha}, base {base_ref}, trees under {tmp}")

    L = load(head, "links")
    site = L.Site(head)
    Lb = L                      # the base tree predates links.py; HEAD's module measures it by root
    bsite = L.Site(base)
    hold = site.hold
    held = lambda rel: any(fnmatch.fnmatch(rel, p) for p in hold)

    # 1 pages
    lines, ok = [], True
    titles_bad, ld_bad = [], []
    for rel, url in site.pages:
        s = site.text(rel)
        nocom = re.sub(r"<!--.*?-->", "", s, flags=re.S)
        if len(re.findall(r"<title>", nocom)) != 1:
            titles_bad.append(rel)
        for m in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', s, re.S):
            try:
                json.loads(m.group(1))
            except ValueError as e:
                ld_bad.append(f"{rel}: {e}")
    ok = len(site.pages) == 160 and not titles_bad and not ld_bad
    lines += [f"served HTML pages: {len(site.pages)} (base {len(bsite.pages)}; must be 160)",
              f"pages without exactly one <title> outside comments: {titles_bad or 'none'}",
              f"JSON-LD blocks that do not parse: {ld_bad or 'none'}"]
    gate(1, "Pages", ok, lines)

    # 2 links
    rc, out = run([sys.executable, "scripts/links.py", "--check"], head)
    b_broken = sum(1 for rel, url, a in Lb.scan(bsite) if Lb.broken(bsite, a))
    held_broken = sum(1 for rel, url, a in L.scan(site) if held(rel) and not a["pending"] and L.broken(site, a))
    gate(2, "Links", rc == 0, ["python3 scripts/links.py --check -> exit %d" % rc] + out.splitlines()[-3:] +
         [f"broken internal anchors at base: {b_broken}", f"broken anchors left on held WEB-FSC-6 pages (theirs to fix): {held_broken}"])

    # 4 mesh
    M = load(head, "mesh")
    model = M.Model(site)
    def mesh_links(url):
        rel = L.url_to_rel(url)
        return {a["path"] for a in L.anchors(site, rel, url) if a["region"] and a["region"].startswith("mesh:") and a["path"]}
    missing, exempt, edges = [], [], 0
    for c in model.cases:
        for p in (c["state"], c["hub"], c["program"]):
            if not p:
                continue
            edges += 1
            if held(L.url_to_rel(p)):
                exempt.append(f"{c['slug']} -> {p}")
            elif c["url"] not in mesh_links(p):
                missing.append(f"{c['slug']} -> {p}")
    for n, v in model.topics["notes"].items():
        for h in v.get("hubs", []) + v.get("programs", []):
            edges += 1
            if held(L.url_to_rel(h)):
                exempt.append(f"{n} -> {h}")
            elif n not in mesh_links(h):
                missing.append(f"{n} -> {h} (note topic)")
    inb, binb = L.inbound(site), Lb.inbound(bsite)
    sect = {}
    for u in site.urls:
        k = L.section(u)
        if k in ("index", "other"):
            continue
        sect.setdefault(k, []).append((len(inb.get(u, ())), len(binb.get(u, ())) if u in binb else 0, u))
    under = sorted(u for k, v in sect.items() for a, b, u in v if a < 3)
    sets = {}
    for rel, url in site.pages:
        if held(rel):
            continue
        g = frozenset(a["path"] for a in L.anchors(site, rel, url) if a["region"] and a["region"].startswith("mesh:") and a["path"])
        if g:
            sets.setdefault(g, []).append(url)
    dups = [v for v in sets.values() if len(v) > 1]
    lines = [f"child-to-parent and note-topic edges: {edges}; missing reverse edge: {missing or 'none'}",
             f"exempt (parent is a held WEB-FSC-6 page, closed when it lands): {len(exempt)}",
             f"pages under 3 contextual inbound links (distinct non-index pages, inside <main>, no breadcrumb, no chrome): {under or 'none'}"]
    for k in ("hub", "state", "case", "note", "practice", "framework"):
        v = sect.get(k, [])
        lines.append(f"  {k:9s} n={len(v):3d}  min {min(b for a, b, u in v):3d} -> {min(a for a, b, u in v):3d}   median {statistics.median(b for a, b, u in v):5.1f} -> {statistics.median(a for a, b, u in v):5.1f}")
    lines.append(f"pages with a generated link set: {sum(len(v) for v in sets.values())}; identical sets: {dups or 'none'}")
    gate(4, "Mesh", not missing and not under and not dups, lines)

    # 5 chrome
    rc, out = run([sys.executable, "scripts/chrome.py", "--check"], head)
    gate(5, "Chrome", rc == 0, ["python3 scripts/chrome.py --check -> exit %d" % rc] + out.splitlines()[-2:])

    # 6 case math
    lines, ok = [], True
    for slug in RECOMPUTED:
        rc1, o1 = run([sys.executable, f"docs/web-fsc-4/recompute/{slug}.py"], head)
        rc2, o2 = run([sys.executable, f"docs/web-fsc-4/recompute/{slug}.py", "--check"], head)
        s = open(os.path.join(head, "case-studies", slug, "index.html"), encoding="utf-8").read()
        t = re.sub(r"\s+", " ", visible(s))
        tier = bool(re.search(r"equity injection \(15%\)", t))
        old = re.search(r"equity injection \(10%\)|\(40%\)|50/40/10|10 percent equity", t)
        ok = ok and rc1 == 0 and rc2 == 0 and tier and not old
        lines.append(f"{slug}: rerun exit {rc1}, --check exit {rc2}, 15% equity row {'present' if tier else 'MISSING'}, old-tier text {'none' if not old else repr(old.group(0))}")
    gate(6, "Case math", ok, lines)

    # 7 dashes and fidelity
    left = []
    D = os.path.join(head, "docs", "web-fsc-4", "tools")
    rc, out = run([sys.executable, os.path.join(D, "dashes.py"), "check"], head)
    held_dashes = 0
    for rel, url in site.pages:
        if held(rel):
            held_dashes += len(EMEN.findall(site.text(rel)))
    # fidelity: the sweep commit alone, word for word
    sweep = subprocess.run(["git", "-C", REPO, "log", "--format=%H", "--grep", "no em or en dash in served files", head_ref],
                           capture_output=True, text=True).stdout.split()
    fid_bad, nsw = [], 0
    if sweep:
        c = sweep[-1]
        files = subprocess.run(["git", "-C", REPO, "diff", "--name-only", c + "^", c], capture_output=True, text=True).stdout.split()
        for f in files:
            if f.startswith("docs/"):
                continue
            a = subprocess.run(["git", "-C", REPO, "show", f"{c}^:{f}"], capture_output=True).stdout.decode("utf-8")
            b = subprocess.run(["git", "-C", REPO, "show", f"{c}:{f}"], capture_output=True).stdout.decode("utf-8")
            nsw += 1
            if words(html.unescape(a)) != words(html.unescape(b)):
                fid_bad.append(f)
    gate(7, "Dashes", rc == 0 and not fid_bad and bool(sweep),
         [f"dashes.py check -> exit {rc}: " + out.splitlines()[-1],
          f"dashes left on held WEB-FSC-6 pages (theirs): {held_dashes}",
          f"fidelity, sweep commit {sweep[-1][:8] if sweep else '?'}: {nsw} served files, every word (text, attributes, JSON-LD) identical before and after: {'yes' if not fid_bad else 'NO ' + str(fid_bad)}"])

    # 8 names
    hits, held_hits, links_out = [], [], []
    for dp, dn, fn in os.walk(head):
        rd = os.path.relpath(dp, head)
        if rd.split(os.sep)[0] in ("docs", "src"):
            continue
        for f in fn:
            rel = os.path.normpath(os.path.join(rd, f)).replace(os.sep, "/")
            try:
                s = open(os.path.join(dp, f), encoding="utf-8").read()
            except (UnicodeDecodeError, OSError):
                continue
            if NAMES.search(s):
                (held_hits if held(rel) else hits).append(rel)
            for m in re.finditer(r'href="([^"]+)"', s):
                if NAMES.search(m.group(1)) and not held(rel):
                    links_out.append(f"{rel}: {m.group(1)}")
    meta = subprocess.run(["git", "-C", REPO, "log", f"{base_ref}..{head_ref}", "--format=%an|%ae|%cn|%ce|%s|%b"],
                          capture_output=True, text=True).stdout
    meta_hits = [l for l in meta.splitlines() if NAMES.search(l)]
    gate(8, "Names", not hits and not links_out and not meta_hits,
         [f"served files outside the hold carrying a ruling-10 name: {hits or 'none'}",
          f"held WEB-FSC-6 pages still carrying one (theirs): {held_hits}",
          f"links to a sister domain: {links_out or 'none'}",
          f"this lane's commits ({base_ref}..{head_ref}) with a name in author, committer or message: {meta_hits or 'none'}"])

    # 9 credentials
    cred = []
    for root in (head, REPO):
        for dp, dn, fn in os.walk(root):
            dn[:] = [d for d in dn if d not in (".git", "node_modules")]
            for f in fn:
                try:
                    s = open(os.path.join(dp, f), encoding="utf-8").read()
                except (UnicodeDecodeError, OSError):
                    continue
                if CREDS.search(s):
                    cred.append(os.path.relpath(os.path.join(dp, f), root))
    gate(9, "Credentials", not cred, ['grep -riE "otava,? *(ph\\.?d|ccim|mai)" over the worktree and the built tree: ' + (", ".join(sorted(set(cred))) or "nothing")])

    # 10 disclosure
    rc, out = run([sys.executable, os.path.join(D, "disclosure.py"), "--check"], head)
    boxed = sum(1 for rel, u in site.pages if rel.startswith("case-studies/") and rel != "case-studies/index.html"
                and not held(rel) and 'class="capsule disclosure"' in site.text(rel))
    gate(10, "Disclosure", rc == 0, [f"disclosure.py --check -> exit {rc}: " + out.splitlines()[-1],
                                     f"cases outside the hold with the box directly under the H1 and byline: {boxed}"])

    # 11 dates
    S = load(head, "sitemap")
    sm = dict(re.findall(r"<loc>https://feasibility-study-company.com([^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>",
                         open(os.path.join(head, "sitemap.xml"), encoding="utf-8").read()))
    bsm = dict(re.findall(r"<loc>https://feasibility-study-company.com([^<]*)</loc>\s*<lastmod>([^<]+)</lastmod>",
                          open(os.path.join(base, "sitemap.xml"), encoding="utf-8").read()))
    disagree, moved = [], []
    for rel, url in site.pages:
        s = site.text(rel)
        if not S.indexable(s):
            continue
        d = S.page_date(s)
        lds = set(re.findall(r'"dateModified"\s*:\s*"([^"]+)"', s))
        vis = None
        b = re.search(r'<!--fsc:(byline-article|line-state|line-asset)[^>]*-->(.*?)<!--/fsc:\1-->', s, re.S)
        if b:
            times = re.findall(r'<time datetime="(\d{4}-\d{2}-\d{2})">', b.group(2))
            if b.group(1) == "byline-article":
                upd = re.search(r'Updated <time datetime="([^"]+)"', b.group(2))
                vis = upd.group(1) if upd else (times[0] if times else None)
            else:
                vis = times[-1] if times else None
        lu = re.search(r"Last updated:?\s*(?:<[^>]+>\s*)*([A-Z][a-z]+ \d{4})", s)
        problems = []
        if sm.get(url) != d:
            problems.append(f"sitemap {sm.get(url)}")
        if lds and lds != {d}:
            problems.append(f"JSON-LD {sorted(lds)}")
        if vis and vis != d:
            problems.append(f"visible {vis}")
        if lu:
            import datetime
            if datetime.date.fromisoformat(d).strftime("%B %Y") != lu.group(1):
                problems.append(f"visible '{lu.group(1)}'")
        if problems and not held(rel):
            disagree.append(f"{url}: date {d}, " + ", ".join(problems))
        # the page's own date at base
        bs = bsite.text(rel) if os.path.exists(os.path.join(base, rel)) else ""
        bd = None
        if re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})"', bs):
            bd = re.search(r'"dateModified"\s*:\s*"(\d{4}-\d{2}-\d{2})"', bs).group(1)
        elif re.search(r'<!--fsc:line-(?:state|asset) (\{.*?\})-->', bs):
            bd = json.loads(re.search(r'<!--fsc:line-(?:state|asset) (\{.*?\})-->', bs).group(1))["updated"]
        else:
            bd = bsm.get(url)
        if bd != d:
            moved.append(f"{url}: {bd} -> {d}")
    want = sorted(f"/case-studies/{s}/" for s in RECOMPUTED)
    got = sorted(m.split(":")[0] for m in moved)
    sm_fixed = sorted(f"{u}: {bsm.get(u)} -> {sm.get(u)}" for u in sm if bsm.get(u) != sm.get(u) and u not in want)
    gate(11, "Dates", not disagree and got == want,
         [f"indexable pages where JSON-LD dateModified, the visible line and sitemap lastmod disagree: {disagree or 'none'}",
          "pages whose own date moved: " + ("; ".join(moved) or "none"),
          f"moved list equals the four recomputed cases: {'yes' if got == want else 'NO'}",
          f"sitemap lastmod corrected to the page's own (unmoved) date: {len(sm_fixed)}"] + ["  " + x for x in sm_fixed])

    # 12 markers
    lines, ok = [], True
    for cmd in (["scripts/byline.py", "--check"], ["scripts/regulatory.py", "--check"], ["scripts/mesh.py", "--check"],
                ["scripts/links.py", "--check"], ["scripts/chrome.py", "--check"], ["scripts/sitemap.py", "--check"]):
        rc, out = run([sys.executable] + cmd, head)
        ok = ok and rc == 0
        lines.append(f"python3 {' '.join(cmd)} -> exit {rc}: {out.splitlines()[-1] if out else ''}")
    gate(12, "Markers", ok, lines)

    # 14 index all (offline half)
    lines, bad = [], []
    for rel, url in site.pages:
        s = site.text(rel)
        rob = re.search(r'<meta name="robots" content="([^"]*)"', s)
        rob = rob.group(1) if rob else ""
        if url in ("/404.html", "/tools/nda/"):
            if "noindex" not in rob or url in sm:
                bad.append(f"{url} should be noindex and out of the sitemap")
        elif "index, follow" not in rob or url not in sm:
            bad.append(f"{url}: robots {rob!r}, in sitemap {url in sm}")
    keys = [f for f in os.listdir(head) if re.fullmatch(r"[0-9a-f]{32}\.txt", f)]
    rc, out = run([sys.executable, "scripts/indexnow.py", "--since", base_ref, "--dry-run"], REPO)
    nurl = sum(1 for l in out.splitlines() if l.startswith("https://"))
    gate(14, "Index all (offline)", not bad and len(keys) == 1 and rc == 0,
         [f"indexable pages without index, follow or missing from the sitemap: {bad or 'none'}",
          f"sitemap URLs: {len(sm)}; IndexNow key file at the root: {keys}",
          f"indexnow.py --since {base_ref} --dry-run -> exit {rc}, {nurl} URL(s)"])

    print("\nSUMMARY: " + " ".join(f"G{n}={'G' if ok else 'R'}" for n, _, ok in RESULTS))
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if all(ok for _, _, ok in RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
