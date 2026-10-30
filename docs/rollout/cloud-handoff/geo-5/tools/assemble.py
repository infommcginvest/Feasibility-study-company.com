#!/usr/bin/env python3
"""GEO-4: turn a keyed draft (citations [^key] or [^key1, key2], front matter "sources": "KEYED") into a page source.

    python3 assemble.py <keyed.html> <sources.json> <out.html>

Sources are numbered in order of first citation (front matter first, then the body), so every entry is cited;
a key not in sources.json stops the run. The output is the source format of src/README.md.
"""
import json
import re
import sys
from collections import OrderedDict

CITE = re.compile(r"\[\^([a-z0-9_]+(?:\s*,\s*[a-z0-9_]+)*)\]")


def main(keyed, srcfile, out):
    s = open(keyed, encoding="utf-8").read()
    head, body = s.split("\n---\n", 1)
    fm = json.loads(head[4:], object_pairs_hook=OrderedDict)
    pool = json.load(open(srcfile))
    order = []
    fm_text = json.dumps({k: v for k, v in fm.items() if k != "sources"}, ensure_ascii=False)
    for m in CITE.finditer(fm_text + "\n" + body):
        for k in re.split(r"\s*,\s*", m.group(1)):
            if k not in pool:
                sys.exit(f"unknown source key: {k}")
            if k not in order:
                order.append(k)
    num = {k: i + 1 for i, k in enumerate(order)}

    def sub(m):
        return "[^" + ",".join(str(num[k]) for k in re.split(r"\s*,\s*", m.group(1))) + "]"

    def walk(v):
        if isinstance(v, str):
            return CITE.sub(sub, v)
        if isinstance(v, list):
            return [walk(x) for x in v]
        if isinstance(v, dict):
            return OrderedDict((k, walk(x)) for k, x in v.items())
        return v

    fm = walk(fm)
    fm["sources"] = [pool[k] for k in order]
    text = "---\n" + json.dumps(fm, indent=2, ensure_ascii=False) + "\n---\n" + CITE.sub(sub, body)
    open(out, "w", encoding="utf-8").write(text)
    print(f"{out}: {len(order)} sources")
    json.dump(order, open(out + ".keys.json", "w"))


if __name__ == "__main__":
    main(*sys.argv[1:])
