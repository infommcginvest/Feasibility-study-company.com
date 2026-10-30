#!/usr/bin/env python3
"""Apply a lane's requests for integrator-owned files (FACTORY-2, ROLLOUT-1 ruling 13; format in docs/rollout/int/REQUESTS.md).

    python3 scripts/requests.py docs/rollout/<lane>/requests.json [--check]
    python3 scripts/requests.py --all [--check]        every docs/rollout/*/requests.json in the tree

Every request is idempotent: applying a file twice changes nothing the second time. --check validates the file and
exits 1 when a request is malformed or not applied yet. Kinds:

  promised        add URLs to data/site/promised.json (new metro and subtype slugs a builder chose)
  chrome_link     add an item to a mega panel column of data/site/chrome.json
  mesh_term       add a first-mention term entry to data/mesh/terms.json
  topic_asset     add or rename an asset class in data/mesh/topics.json 'assets'
  topic_program   add a practice area to data/mesh/topics.json 'programs'
  topic_note      add or update a research note's hubs and programs in data/mesh/topics.json 'notes'
  fallback        set the fallback of a promised URL in data/mesh/fallbacks.json 'targets'
  folded          record a promised page folded into a section of its parent ('targets' and 'folded')
  unfolded        remove a folded record when the page ships on its own
  subtype_section name the hub section a pending subtype falls back to (fallbacks.json 'subtype_sections')
  redirect        add a [[redirects]] rule to netlify.toml (301 only; a page path that still exists is refused)
  index_entry     an entry on a section index page the integrator owns; printed for the integrator, who writes it
  page_type       add a page type's settings to src/types.json (METHOD-1, with its src/templates/<type>.html)
"""
import json
import os
import re
import sys
from collections import OrderedDict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = re.compile(r"^/[a-z0-9-]+(?:/[a-z0-9-]+)*/$")
INDEXES = {"/", "/states/", "/asset-classes/", "/case-studies/", "/practice-areas/", "/research-notes/", "/analytical-framework/"}


class RequestError(Exception):
    pass


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return json.load(fh, object_pairs_hook=OrderedDict)


def need(r, *keys):
    for k in keys:
        if k not in r or r[k] in (None, "", []):
            raise RequestError(f"request {r.get('id')}: kind {r.get('kind')} needs '{k}'")


def url_ok(u, what):
    if not isinstance(u, str) or not URL.match(u):
        raise RequestError(f"{what} {u!r} is not a site path like /states/texas/houston/")


class Files:
    """The integrator files a request may touch, loaded once, written once if changed."""

    def __init__(self):
        self.data, self.text, self.dirty = {}, {}, set()

    def json(self, rel):
        if rel not in self.data:
            self.data[rel] = load(rel)
        return self.data[rel]

    def toml(self):
        rel = "netlify.toml"
        if rel not in self.text:
            self.text[rel] = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        return self.text[rel]

    def touch(self, rel):
        self.dirty.add(rel)

    def save(self):
        for rel in sorted(self.dirty):
            path = os.path.join(ROOT, rel)
            if rel in self.text:
                open(path, "w", encoding="utf-8").write(self.text[rel])
            elif rel == "data/site/chrome.json":
                open(path, "w", encoding="utf-8").write(chrome_dump(self.data[rel]) + "\n")
            elif rel == "src/types.json":
                open(path, "w", encoding="utf-8").write(types_dump(self.data[rel]) + "\n")
            elif rel in ("data/mesh/topics.json", "data/mesh/terms.json"):
                open(path, "w", encoding="utf-8").write(json.dumps(self.data[rel], indent=2) + "\n")
            else:
                open(path, "w", encoding="utf-8").write(json.dumps(self.data[rel], indent=1, ensure_ascii=False) + "\n")


def types_dump(d):
    """src/types.json's layout: one type per line."""
    rows = [f"  {json.dumps(k)}: {json.dumps(v, ensure_ascii=False)}" for k, v in d.items()]
    return "{\n" + ",\n".join(rows) + "\n}"


def chrome_dump(x, ind=0):
    """chrome.json's own layout: leaf objects and short scalar lists on one line."""
    sp = "  " * ind
    if isinstance(x, dict):
        if ind > 1 and all(not isinstance(v, (dict, list)) for v in x.values()):
            return json.dumps(x, ensure_ascii=False)
        if ind > 1 and list(x) == ["group"]:
            inner = ",\n".join(f"{sp}  {chrome_dump(v, ind + 1)}" for v in x["group"])
            return '{"group": [\n' + inner + f"\n{sp}]}}"
        return "{\n" + ",\n".join(f"{sp}  {json.dumps(k)}: {chrome_dump(v, ind + 1)}" for k, v in x.items()) + f"\n{sp}}}"
    if isinstance(x, list):
        if all(not isinstance(v, (dict, list)) for v in x) and len(json.dumps(x)) < 100:
            return json.dumps(x, ensure_ascii=False)
        return "[\n" + ",\n".join(f"{sp}  {chrome_dump(v, ind + 1)}" for v in x) + f"\n{sp}]"
    return json.dumps(x, ensure_ascii=False)


def apply_one(f, r, lane, manual):
    kind = r.get("kind")
    if kind == "promised":
        need(r, "urls")
        d = f.json("data/site/promised.json")
        for u in r["urls"]:
            url_ok(u, "promised url")
            if u not in d["pages"]:
                cls = "metro" if u.startswith("/states/") else "subtype" if u.startswith("/asset-classes/") else "other"
                d["pages"][u] = OrderedDict([("lane", lane), ("class", cls)])
                f.touch("data/site/promised.json")
        d["pages"] = OrderedDict(sorted(d["pages"].items()))
    elif kind == "chrome_link":
        need(r, "mega", "col", "label", "href")
        url_ok(r["href"], "href")
        c = f.json("data/site/chrome.json")
        mega = c["mega"].get(r["mega"])
        if mega is None:
            raise RequestError(f"request {r.get('id')}: no mega panel {r['mega']} (assets or markets)")
        cols = [col for col in mega["cols"] if col.get("class") == r["col"] or col.get("title") == r["col"]]
        if len(cols) != 1:
            raise RequestError(f"request {r.get('id')}: column {r['col']!r} not found in mega {r['mega']}")
        items = cols[0]["items"]
        if not any(i.get("href") == r["href"] for i in items):
            item = OrderedDict([("label", r["label"]), ("href", r["href"])])
            if r.get("fallback"):
                item["fallback"] = r["fallback"]
            if r.get("hide_until_live"):
                item["hide_until_live"] = True
            items.append(item)
            f.touch("data/site/chrome.json")
    elif kind == "mesh_term":
        need(r, "key", "target", "terms")
        url_ok(r["target"], "target")
        t = f.json("data/mesh/terms.json")
        entry = OrderedDict([("key", r["key"]), ("target", r["target"]), ("terms", list(r["terms"]))])
        if r.get("ignore_case"):
            entry["ignore_case"] = True
        old = [i for i, e in enumerate(t["terms"]) if e["key"] == r["key"]]
        if old:
            if t["terms"][old[0]] != entry:
                t["terms"][old[0]] = entry
                f.touch("data/mesh/terms.json")
        else:
            t["terms"].append(entry)
            f.touch("data/mesh/terms.json")
    elif kind in ("topic_asset", "topic_program", "topic_note"):
        need(r, "url")
        t = f.json("data/mesh/topics.json")
        if kind == "topic_asset":
            need(r, "name", "family")
            if r["family"] not in t["families"]:
                raise RequestError(f"request {r.get('id')}: family {r['family']!r} is not one of {t['families']}")
            entry = OrderedDict([("name", r["name"]), ("family", r["family"])])
            sect = "assets"
        elif kind == "topic_program":
            need(r, "name")
            entry, sect = OrderedDict([("name", r["name"])]), "programs"
        else:
            entry = OrderedDict([("hubs", list(r.get("hubs", []))), ("programs", list(r.get("programs", [])))])
            if r.get("program_wide"):
                entry["program_wide"] = True
            sect = "notes"
        url_ok(r["url"], "url")
        if t[sect].get(r["url"]) != entry:
            t[sect][r["url"]] = entry
            f.touch("data/mesh/topics.json")
    elif kind in ("fallback", "folded", "unfolded", "subtype_section"):
        fb = f.json("data/mesh/fallbacks.json")
        if kind == "subtype_section":
            need(r, "hub", "section")
            if fb["subtype_sections"].get(r["hub"]) != r["section"]:
                fb["subtype_sections"][r["hub"]] = r["section"]
                f.touch("data/mesh/fallbacks.json")
            return
        need(r, "url")
        url_ok(r["url"], "url")
        if kind == "unfolded":
            if r["url"] in fb["folded"]:
                fb["folded"].remove(r["url"])
                f.touch("data/mesh/fallbacks.json")
            if r["url"] in fb["targets"]:
                del fb["targets"][r["url"]]
                f.touch("data/mesh/fallbacks.json")
            return
        need(r, "target")
        if fb["targets"].get(r["url"]) != r["target"]:
            fb["targets"][r["url"]] = r["target"]
            f.touch("data/mesh/fallbacks.json")
        if kind == "folded" and r["url"] not in fb["folded"]:
            fb["folded"].append(r["url"])
            f.touch("data/mesh/fallbacks.json")
    elif kind == "redirect":
        need(r, "from", "to")
        if int(r.get("status", 301)) != 301:
            raise RequestError(f"request {r.get('id')}: only 301 redirects are taken")
        if os.path.exists(os.path.join(ROOT, r["from"].strip("/"), "index.html")):
            raise RequestError(f"request {r.get('id')}: {r['from']} is a page that exists; a redirect would hide it")
        text = f.toml()
        if f'from = "{r["from"]}"' not in text:
            f.text["netlify.toml"] = text.rstrip("\n") + (
                f'\n\n# {lane} request {r.get("id")}\n[[redirects]]\n  from = "{r["from"]}"\n  to = "{r["to"]}"\n  status = 301\n')
            f.touch("netlify.toml")
    elif kind == "page_type":
        need(r, "type", "settings")
        st = r["settings"]
        if not re.match(r"^[a-z]+$", r["type"]) or r["type"] in ("state", "metro", "hub", "subtype", "case", "base"):
            raise RequestError(f"request {r.get('id')}: type {r['type']!r} is taken or not a lowercase word")
        for k in ("schema", "byline", "mode", "house", "cite", "range", "figures"):
            if k not in st:
                raise RequestError(f"request {r.get('id')}: settings need '{k}'")
        if st["schema"] not in ("article", "webpage") or st["byline"] not in ("byline-article", "line-state", "line-asset") \
                or st["figures"] not in ("reference", "short") or st["cite"] not in ("case", "fn"):
            raise RequestError(f"request {r.get('id')}: settings outside the allowed values (see src/types.json _about)")
        t = f.json("src/types.json")
        entry = OrderedDict((k, st[k]) for k in ("schema", "byline", "mode", "house", "page_css", "cite", "article_section",
                                                 "range", "figures") if k in st)
        if t.get(r["type"]) != entry:
            t[r["type"]] = entry
            f.touch("src/types.json")
    elif kind == "index_entry":
        need(r, "index", "url", "label")
        if r["index"] not in INDEXES:
            raise RequestError(f"request {r.get('id')}: index {r['index']!r} is not one of {sorted(INDEXES)}")
        manual.append(f"{lane} {r.get('id')}: {r['index']} entry for {r['url']}: {r['label']!r}"
                      + (f" ({r['line']})" if r.get("line") else ""))
    else:
        raise RequestError(f"request {r.get('id')}: unknown kind {kind!r}")


def apply_file(path, check):
    spec = json.load(open(path, encoding="utf-8"))
    lane = spec.get("lane")
    if not lane or not isinstance(spec.get("requests"), list):
        raise RequestError(f"{path}: needs 'lane' and a 'requests' list")
    f, manual = Files(), []
    ids = set()
    for r in spec["requests"]:
        if not r.get("id") or r["id"] in ids:
            raise RequestError(f"{path}: every request needs a unique 'id' (got {r.get('id')!r})")
        ids.add(r["id"])
        apply_one(f, r, lane, manual)
    if not check:
        f.save()
    return sorted(f.dirty), manual


def main(argv):
    check = "--check" in argv
    paths = [a for a in argv if not a.startswith("--")]
    if "--all" in argv:
        base = os.path.join(ROOT, "docs", "rollout")
        paths += sorted(os.path.join(base, d, "requests.json") for d in os.listdir(base)
                        if os.path.exists(os.path.join(base, d, "requests.json")))
    if not paths:
        print(__doc__)
        return 2
    bad = 0
    for p in paths:
        try:
            dirty, manual = apply_file(p, check)
        except (RequestError, ValueError, KeyError) as exc:
            print(f"ERROR {p}: {exc}")
            bad += 1
            continue
        verb = "would change" if check else "changed"
        print(f"{p}: {verb} {', '.join(dirty) if dirty else 'nothing'}")
        for m in manual:
            print("  INDEX ENTRY (integrator writes it):", m)
        if check and dirty:
            bad += 1
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
