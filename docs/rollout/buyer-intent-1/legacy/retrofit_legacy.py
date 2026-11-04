#!/usr/bin/env python3
"""Track D (CLOUD-1, owner amendment 1): buyer-intent header on the 22 legacy asset-class hubs, exact-text edits.

    python3 retrofit_legacy.py <tree> [--date YYYY-MM-DD]

The 22 legacy hubs are served HTML with no source under src/pages, so the integrator applies these edits (as in I104).
Every spec in specs/ beside this script names one page and its elements (title, meta description, og and twitter
mirrors, H1, hero paragraph, hero button text, CTA band heading, paragraph and button text), each as an exact
"before" and "after". Per page:
- every "before" occurs exactly once: each is replaced by its "after", and because the content changed (ruling 12) the
  page's one date is set to --date (default: src/site.json deploy_date): the line-asset region's "updated" param and its
  visible "Updated <time>", the author-ld region's "date_modified" param and its JSON-LD dateModified, exactly as
  scripts/byline.py renders them, so byline.py --check passes and sitemap.py reads the new date as lastmod;
- no "before" occurs and every "after" does: already applied, the page is left alone (dates included);
- anything else (a "before" missing or repeated, or a page half applied): the run stops with the reasons and writes nothing.
All pages are checked before any is written. Idempotent: a second run changes nothing. No other file is touched.
A bare --date with no value, or a date earlier than a page's current date, stops the run (review finding A2-17).
"""
import datetime
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SPECS = os.path.join(HERE, "specs")
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
LINE = re.compile(r"<!--fsc:line-asset (\{.*?\})-->(.*?)<!--/fsc:line-asset-->", re.S)
AUTHOR = re.compile(r"<!--fsc:author-ld (\{.*?\})-->(.*?)<!--/fsc:author-ld-->", re.S)
VISIBLE = re.compile(r'Updated <time datetime="\d{4}-\d{2}-\d{2}">[^<]*</time>')
LD_DATE = re.compile(r'"dateModified": "\d{4}-\d{2}-\d{2}"')


def fmt_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    return f"{MONTHS[m - 1]} {d}, {y}"


def region(name, params, inner):
    return f"<!--fsc:{name} {json.dumps(params, sort_keys=True)}-->{inner}<!--/fsc:{name}-->"


def set_date(s, date):
    """The page's date in its line-asset and author-ld regions (byline.py's renderings), or raise ValueError."""
    if len(LINE.findall(s)) != 1 or len(AUTHOR.findall(s)) != 1:
        raise ValueError("expected one line-asset and one author-ld region")
    if len(LD_DATE.findall(s)) != 1 or len(VISIBLE.findall(s)) != 1:
        raise ValueError("expected one JSON-LD dateModified and one visible Updated line")
    m = LINE.search(s)
    params = dict(json.loads(m.group(1)), updated=date)
    inner = VISIBLE.sub(f'Updated <time datetime="{date}">{fmt_date(date)}</time>', m.group(2))
    if inner == m.group(2) and json.loads(m.group(1)).get("updated") != date:
        raise ValueError("visible Updated line not inside the line-asset region")
    s = s[:m.start()] + region("line-asset", params, inner) + s[m.end():]
    m = AUTHOR.search(s)
    params = dict(json.loads(m.group(1)), date_modified=date)
    inner, n = LD_DATE.subn(f'"dateModified": "{date}"', m.group(2))
    if n != 1:
        raise ValueError("JSON-LD dateModified not inside the author-ld region")
    return s[:m.start()] + region("author-ld", params, inner) + s[m.end():]


def plan(tree, spec, date):
    """(path, new text or None when already applied, note) for one spec; raise ValueError when it cannot apply."""
    url = spec["url"]
    if spec.get("kind") != "legacy" or not re.fullmatch(r"/asset-classes/[a-z0-9-]+/", url):
        raise ValueError("not a legacy asset-class spec")
    path = os.path.join(tree, url.strip("/"), "index.html")
    if not os.path.exists(path):
        raise ValueError("served page missing")
    s = open(path, encoding="utf-8").read()
    els = spec["elements"]
    before = [s.count(e["before"]) for e in els]
    if all(n == 0 for n in before):
        missing = [e["element"] for e in els if e["after"] not in s]
        if missing:
            raise ValueError(f"no 'before' found, and 'after' absent for {missing}: page changed since the spec")
        return path, None, "already applied"
    if any(n != 1 for n in before):
        raise ValueError("'before' counts " + ", ".join(f"{e['element']}={n}" for e, n in zip(els, before) if n != 1)
                         + " (each must occur exactly once)")
    old = s
    for e in els:
        if s.count(e["before"]) != 1:
            raise ValueError(f"{e['element']}: 'before' no longer unique after the earlier replacements")
        s = s.replace(e["before"], e["after"], 1)
    for mark in ("<!--", "-->", "<title>", "<h1>", '<p class="hero-sub">', '<section class="cta-band"'):
        if s.count(mark) != old.count(mark):
            raise ValueError(f"the edits would change how many {mark!r} the page has")
    m = LINE.search(old)
    current = json.loads(m.group(1)).get("updated") if m else None
    if current and date < current:
        raise ValueError(f"--date {date} is earlier than the page's current date {current}")
    return path, set_date(s, date), f"{len(els)} element(s) replaced; dated {date}"


def main(argv):
    args = [a for a in argv if not a.startswith("--date")]
    date = None
    for i, a in enumerate(argv):
        if a == "--date" and i + 1 < len(argv):
            date = argv[i + 1]
            args.remove(date)
        elif a.startswith("--date="):
            date = a.split("=", 1)[1]
    if "--date" in argv and date is None:
        raise SystemExit("retrofit_legacy: --date needs a value (YYYY-MM-DD)")
    if len(args) != 1:
        raise SystemExit(__doc__.split("\n\n")[1])
    tree = os.path.abspath(args[0])
    if date is None:
        date = json.load(open(os.path.join(tree, "src", "site.json"), encoding="utf-8"))["deploy_date"]
    try:
        datetime.date.fromisoformat(date)
        assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", date)
    except (ValueError, AssertionError):
        raise SystemExit(f"retrofit_legacy: --date {date!r} is not YYYY-MM-DD")
    specs = sorted(glob.glob(os.path.join(SPECS, "*.json")))
    if not specs:
        raise SystemExit(f"retrofit_legacy: no specs in {SPECS}")
    todo, errors = [], []
    for f in specs:
        spec = json.load(open(f, encoding="utf-8"))
        try:
            todo.append((spec["url"],) + plan(tree, spec, date))
        except (ValueError, KeyError) as e:
            errors.append(f"{spec.get('url', os.path.basename(f))}: {e}")
    if errors:
        print("retrofit_legacy: nothing written; " + str(len(errors)) + " page(s) cannot apply:", file=sys.stderr)
        for e in errors:
            print("  " + e, file=sys.stderr)
        return 1
    changed = 0
    for url, path, new, note in todo:
        if new is not None:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new)
            changed += 1
        print(f"{url}: {note}")
    print(f"retrofit_legacy: {changed} page(s) changed, {len(todo) - changed} already applied")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
