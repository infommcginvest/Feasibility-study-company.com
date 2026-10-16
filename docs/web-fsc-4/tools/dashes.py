#!/usr/bin/env python3
"""WEB-FSC-4 ruling 12: no em dash or en dash anywhere served.

An en dash becomes a hyphen. An em dash becomes the punctuation the sentence
needs; in titles and headings "X — Y" becomes "X: Y". Words never change.

    python3 docs/web-fsc-4/tools/dashes.py scan OUT.jsonl     every occurrence, its zone, its sentence,
                                                              and the decision the rules can make
    python3 docs/web-fsc-4/tools/dashes.py review OUT.jsonl   the unique sentences the rules cannot settle
    python3 docs/web-fsc-4/tools/dashes.py apply DECISIONS.jsonl [--only page,page]
    python3 docs/web-fsc-4/tools/dashes.py check [BASE_REF]   zero dashes in every listed encoding, and the
                                                              fidelity check against BASE_REF

Decisions: comma, colon, semicolon, stop (full stop; the next word is
capitalised), open / close (a parenthesis pair), hyphen (a range, a compound,
a placeholder cell, or a comment), drop (an attribution dash before a name).
Pages listed in data/site/hold.json are never touched.
"""
import fnmatch
import hashlib
import html
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
EM = r"(?:—|&mdash;|&#8212;|&#x2014;|&#X2014;)"
EN = r"(?:–|&ndash;|&#8211;|&#x2013;|&#X2013;)"
DASH = re.compile(r"([ \t]*\n?[ \t]*)(" + EM + "|" + EN + r")([ \t]*\n?[ \t]*)")
SERVED_EXT = (".html", ".xml", ".css", ".js", ".json", ".md", ".txt", ".svg", ".py", ".toml")
SKIP_TOP = {"docs", "src", "node_modules", "_bundles"}
BLOCK_TAGS = ("p", "li", "td", "th", "dt", "dd", "h1", "h2", "h3", "h4", "h5", "h6", "figcaption",
              "blockquote", "caption", "title", "summary", "label", "button", "span", "div", "a", "strong", "em", "sup")
HEAD_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "title")
TITLE_META = ("og:title", "twitter:title")


def hold():
    with open(os.path.join(ROOT, "data", "site", "hold.json"), encoding="utf-8") as fh:
        return json.load(fh)["pages"]


def served(root=ROOT):
    pats = hold()
    out = []
    for dirpath, dirnames, filenames in os.walk(root):
        rel_dir = os.path.relpath(dirpath, root).replace(os.sep, "/")
        if rel_dir == ".":
            dirnames[:] = sorted(d for d in dirnames if not d.startswith(".") and d not in SKIP_TOP)
        else:
            dirnames[:] = sorted(d for d in dirnames if not d.startswith("."))
        for fn in sorted(filenames):
            rel = fn if rel_dir == "." else rel_dir + "/" + fn
            if not fn.endswith(SERVED_EXT) or fn.startswith("."):
                continue
            if re.match(r"^(preview-.*|index_\d+)\.html$", fn) or (rel_dir == "." and fn.endswith(".md") and fn != "README.md"):
                continue
            if any(fnmatch.fnmatch(rel, p) for p in pats):
                continue
            out.append(rel)
    return out


# ---------------------------------------------------------------- zones

def spans(s, rx):
    return [(m.start(), m.end()) for m in re.finditer(rx, s, re.S | re.I)]


def inside(pos, sp):
    return any(a <= pos < b for a, b in sp)


def zone(s, pos, cache):
    if "c" not in cache:
        cache["c"] = spans(s, r"<!--.*?-->")
        cache["ld"] = spans(s, r'<script type="application/ld\+json">.*?</script>')
        cache["js"] = spans(s, r"<script\b(?![^>]*ld\+json).*?</script>")
        cache["css"] = spans(s, r"<style\b.*?</style>")
        cache["tag"] = spans(s, r"<[a-zA-Z][^<>]*>")
    if inside(pos, cache["c"]):
        return "comment"
    if inside(pos, cache["css"]):
        return "style"
    if inside(pos, cache["js"]):
        return "script"
    if inside(pos, cache["ld"]):
        return "ldjson"
    for a, b in cache["tag"]:
        if a <= pos < b:
            tag = s[a:b]
            if tag.startswith("<meta") and any(f'"{k}"' in tag for k in TITLE_META):
                return "meta-title"
            return "attr"
    return "text"


def enclosing(s, pos):
    """The innermost open block-ish tag before pos."""
    best = None
    for t in HEAD_TAGS + ("p", "li", "td", "th", "dt", "dd", "figcaption", "blockquote", "caption", "summary"):
        i = s.rfind("<" + t, 0, pos)
        while i >= 0 and not re.match(r"<%s[\s>]" % t, s[i:i + len(t) + 2]):
            i = s.rfind("<" + t, 0, i)
        if i < 0:
            continue
        j = s.find("</" + t + ">", i)
        if j >= pos and (best is None or i > best[1]):
            best = (t, i, j)
    return best


def ld_key(s, pos):
    """The JSON key whose string value contains pos."""
    i = s.rfind('":', 0, pos)
    k = s.rfind('"', 0, i)
    return s[k + 1:i] if i > 0 and k >= 0 else ""


# ---------------------------------------------------------------- sentences

MARK = "⟦"  # the dash under decision is shown as ⟦—⟧, other dashes as —


def visible(raw):
    t = re.sub(r"<!--.*?-->", "", raw, flags=re.S)
    t = re.sub(r"<[^>]+>", "", t)
    t = html.unescape(t)
    return re.sub(r"\s+", " ", t)


def block_text(s, pos, z):
    """Visible text of the block that holds pos, with that dash marked."""
    if z == "ldjson" or z == "attr" or z == "meta-title":
        q1 = s.rfind('"', 0, pos)
        q2 = s.find('"', pos)
        raw = s[q1 + 1:pos] + MARK + s[pos:q2]
    else:
        enc = enclosing(s, pos)
        if enc:
            t, a, b = enc
            a = s.index(">", a) + 1
        else:
            a = max(s.rfind(">", 0, pos) + 1, pos - 400)
            b = s.find("<", pos)
            b = pos + 400 if b < 0 else b
        raw = s[a:pos] + MARK + s[pos:b]
    t = visible(raw)
    t = re.sub(r"\s*" + EM + r"\s*", " — ", t)
    t = re.sub(MARK + r"\s*(—|–)", MARK, t)
    return t.strip()


SENT_SPLIT = re.compile(r"(?<=[.!?])[\"”)]?\s+(?=[A-Z“\"(\d])")


def sentence(block):
    parts = SENT_SPLIT.split(block)
    for p in parts:
        if MARK in p:
            return p.strip()
    return block


# ---------------------------------------------------------------- rules

def auto(item):
    """The decision the rules can make, or None for review."""
    k, z, sent = item["kind"], item["zone"], item["sentence"]
    if k == "en":
        return "hyphen"
    if z in ("comment", "style", "script") or item["file"].endswith((".css", ".js", ".py", ".toml")):
        return "hyphen"
    if item["tag"] in HEAD_TAGS or z == "meta-title" or (z == "ldjson" and item["ldkey"] in ("name", "headline", "alternativeHeadline")) or item["file"].endswith(".xml") and item["xmltag"] == "title":
        n = sent.count("—") + 1
        return "colon" if n == 1 else None
    stripped = sent.replace(MARK, "").strip()
    if stripped == "":
        return "hyphen"          # a placeholder cell: the dash is the whole content
    left = sent.split(MARK)[0].strip()
    right = sent.split(MARK)[1].strip() if MARK in sent else ""
    if left == "" and right:
        return "drop"            # a dash opening a line: an attribution
    dashes = sent.count("—") + 1
    if dashes == 2:
        before = sent.split(MARK)[0]
        after = sent.split(MARK)[1]
        if "—" in after and "—" not in before:
            inner = after.split("—")[0]
            return "open-paren" if "," in inner or ";" in inner else "open-comma"
        if "—" in before and "—" not in after:
            inner = before.split("—")[-1]
            return "close-paren" if "," in inner or ";" in inner else "close-comma"
    if dashes == 1 and item["label"]:
        return "colon"
    return None


def scan(root=ROOT):
    items = []
    for rel in served(root):
        s = open(os.path.join(root, rel), encoding="utf-8").read()
        cache = {}
        n = 0
        for m in DASH.finditer(s):
            pos = m.start(2)
            kind = "em" if re.fullmatch(EM, m.group(2)) else "en"
            z = zone(s, pos, cache)
            enc = enclosing(s, pos) if z == "text" else None
            tag = enc[0] if enc else ""
            if z in ("comment", "style", "script"):
                sent = ""
            else:
                sent = sentence(block_text(s, pos, z))
            pre = s[max(0, m.start() - 40):m.start()]
            label = bool(re.search(r"</(strong|b|dt)>\s*$", pre)) or bool(re.search(r"<(li|td|dt)[^>]*>\s*(<[^>]+>\s*)*[^<]{1,48}$", s[max(0, m.start() - 120):m.start()]) and len(sent.split(MARK)[0].split()) <= 5)
            xmltag = ""
            if rel.endswith(".xml"):
                o = s.rfind("<", 0, pos)
                xmltag = re.match(r"<(\w+)", s[o:]).group(1) if re.match(r"<(\w+)", s[o:]) else ""
            it = {"id": f"{rel}#{n}", "file": rel, "n": n, "kind": kind, "zone": z, "tag": tag,
                  "ldkey": ld_key(s, pos) if z == "ldjson" else "", "xmltag": xmltag, "label": label,
                  "spaced": bool(m.group(1)) or bool(m.group(3)), "sentence": sent}
            base = sent.replace(MARK, "\u2014") if sent else ""
            it["idx"] = sent.split(MARK)[0].count("\u2014") if MARK in sent else 0
            it["key"] = hashlib.sha1((base + "|" + kind).encode()).hexdigest()[:12] if sent else ""
            it["auto"] = auto(it)
            items.append(it)
            n += 1
    return items


# ---------------------------------------------------------------- apply

def capitalise_next(s, i):
    """Uppercase the first letter at or after i, skipping tags and spaces."""
    j = i
    while j < len(s):
        if s[j] == "<":
            j = s.find(">", j) + 1
            continue
        if s[j].isspace():
            j += 1
            continue
        if s[j] == "&":
            semi = s.find(";", j)
            if 0 < semi - j < 10:
                j = semi + 1
                continue
        if s[j].isalpha() and s[j].islower():
            return s[:j] + s[j].upper() + s[j + 1:]
        return s
    return s


def replacement(decision, pre_ws, post_ws, ctx):
    nl = "\n" in post_ws
    tail = post_ws if nl else " "
    lead = pre_ws if "\n" in pre_ws else ""
    if decision == "hyphen":
        return pre_ws + "-" + post_ws if ctx != "en" else "-"
    if decision in ("comma", "open-comma", "close-comma"):
        return "," + (lead or "") + tail if not lead else "," + tail
    if decision == "colon":
        return ":" + tail
    if decision == "semicolon":
        return ";" + tail
    if decision == "stop":
        return "." + tail
    if decision in ("open", "open-paren"):
        return (lead or " ") + "("
    if decision in ("close", "close-paren"):
        return ")" + tail
    if decision == "drop":
        return lead
    raise ValueError(decision)


def apply(decisions, only=None, root=ROOT):
    by_file = {}
    for d in decisions:
        by_file.setdefault(d["file"], {})[d["n"]] = d["decision"]
    changed = 0
    for rel in served(root):
        if only and rel not in only:
            continue
        p = os.path.join(root, rel)
        s = open(p, encoding="utf-8").read()
        dec = by_file.get(rel, {})
        out, last, n, caps = [], 0, 0, []
        for m in DASH.finditer(s):
            kind = "em" if re.fullmatch(EM, m.group(2)) else "en"
            d = dec.get(n)
            if d is None:
                raise SystemExit(f"{rel}: no decision for dash #{n}")
            if kind == "en" and d == "hyphen":
                # a range or compound keeps its own spacing: 5-6, Dallas-Fort Worth
                r = m.group(1) + "-" + m.group(3)
            else:
                r = replacement(d, m.group(1), m.group(3), kind)
            out.append(s[last:m.start()])
            # punctuation attaches to the previous word
            if d in ("comma", "open-comma", "close-comma", "colon", "semicolon", "stop", "close", "close-paren"):
                out[-1] = out[-1].rstrip(" \t") if "\n" not in m.group(1) else out[-1]
                if "\n" in m.group(1):
                    r = r.lstrip("\n \t")
                    out[-1] = out[-1].rstrip(" \t")
            if d in ("open", "open-paren") and "\n" in m.group(1):
                r = m.group(1) + "("
            out.append(r)
            if d == "stop":
                caps.append(sum(len(x) for x in out))
            last = m.end()
            n += 1
        out.append(s[last:])
        new = "".join(out)
        for i in reversed(caps):
            new = capitalise_next(new, i)
        if new != s:
            open(p, "w", encoding="utf-8").write(new)
            changed += 1
    return changed


# ---------------------------------------------------------------- check

def words(raw):
    t = visible(re.sub(r"<script\b.*?</script>|<style\b.*?</style>", " ", raw, flags=re.S | re.I))
    return re.findall(r"[0-9A-Za-zÀ-ɏ]+", t.lower())


def check(base):
    bad = []
    pats = hold()
    for rel in served():
        s = open(os.path.join(ROOT, rel), encoding="utf-8").read()
        for m in re.finditer(EM + "|" + EN, s):
            bad.append(f"{rel}:{s.count(chr(10), 0, m.start()) + 1}: {m.group(0)!r}")
    return bad


def main(argv):
    cmd = argv[0]
    if cmd == "scan":
        items = scan()
        with open(argv[1], "w", encoding="utf-8") as fh:
            for it in items:
                fh.write(json.dumps(it, ensure_ascii=False) + "\n")
        from collections import Counter
        c = Counter((it["kind"], it["auto"] or "REVIEW") for it in items)
        for k, v in sorted(c.items()):
            print(k, v)
        keys = {it["key"] for it in items if it["auto"] is None}
        print("occurrences", len(items), "review occurrences", sum(1 for it in items if it["auto"] is None), "unique review sentences", len(keys))
    elif cmd == "review":
        items = [json.loads(l) for l in open(argv[1], encoding="utf-8")]
        groups = {}
        for it in items:
            if it["auto"] is None:
                g = groups.setdefault(it["key"], {"key": it["key"], "file": it["file"], "zone": it["zone"],
                                                  "tag": it["tag"], "sentence": it["sentence"].replace(MARK, "\u2014"), "idx": set()})
                g["idx"].add(it["idx"])
        with open(argv[2], "w", encoding="utf-8") as fh:
            for g in groups.values():
                parts = g["sentence"].split("\u2014")
                shown = parts[0]
                for i, part in enumerate(parts[1:]):
                    shown += ("[%d]" % (i + 1)) + part
                g = {"key": g["key"], "file": g["file"], "zone": g["zone"], "tag": g["tag"], "dashes": len(parts) - 1,
                     "decide": sorted(i + 1 for i in g["idx"]), "sentence": shown}
                fh.write(json.dumps(g, ensure_ascii=False) + "\n")
        print(len(groups), "unique sentences to review")
    elif cmd == "merge":
        # scan + reviewed decisions -> one decision per occurrence
        items = [json.loads(l) for l in open(argv[1], encoding="utf-8")]
        rev = {}
        for path in argv[3:]:
            for l in open(path, encoding="utf-8"):
                if l.strip():
                    r = json.loads(l)
                    rev[r["key"]] = r["d"]
        out, missing = [], []
        for it in items:
            d = it["auto"]
            if d is None:
                ds = rev.get(it["key"])
                d = ds.get(str(it["idx"] + 1)) if isinstance(ds, dict) else None
                if d is None:
                    missing.append(it["id"])
                    continue
            out.append({"file": it["file"], "n": it["n"], "decision": d})
        with open(argv[2], "w", encoding="utf-8") as fh:
            for o in out:
                fh.write(json.dumps(o) + "\n")
        print(len(out), "decisions;", len(missing), "missing")
        for m in missing[:20]:
            print("  missing", m)
        return 1 if missing else 0
    elif cmd == "apply":
        decisions = [json.loads(l) for l in open(argv[1], encoding="utf-8")]
        only = set(argv[argv.index("--only") + 1].split(",")) if "--only" in argv else None
        print(apply(decisions, only), "file(s) changed")
    elif cmd == "check":
        bad = check(argv[1] if len(argv) > 1 else None)
        for b in bad[:50]:
            print(b)
        print(f"{len(bad)} dash(es) left in served files outside data/site/hold.json")
        return 1 if bad else 0
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
