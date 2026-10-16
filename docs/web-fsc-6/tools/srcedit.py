#!/usr/bin/env python3
"""Remove or merge numbered sources on a factory page and renumber every citation that points at them.

    python3 docs/web-fsc-6/tools/srcedit.py <url> --remove 22,69
    python3 docs/web-fsc-6/tools/srcedit.py <url> --merge 34:12,35:12      (cite 12 wherever 34 or 35 was cited, then drop 34 and 35)

Rewrites src/pages/<url>.html (front matter sources, [^n] in body and front matter) and, for a case page,
data/cases/<slug>.json (input "source" lists, rule_sources, and [^n] inside assumption, basis and glance text).
A source can be removed only when nothing cites it after the merge; the tool refuses otherwise.
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
CITE = re.compile(r"\[\^(\d+(?:\s*,\s*\d+)*)\]")


def remap_text(text, mapping):
    def sub(m):
        out = []
        for x in re.split(r"\s*,\s*", m.group(1)):
            n = mapping[int(x)]
            if n not in out:
                out.append(n)
        return "[^" + ",".join(str(n) for n in out) + "]"
    return CITE.sub(sub, text)


def walk_json(obj, fn):
    if isinstance(obj, dict):
        return {k: walk_json(v, fn) for k, v in obj.items()}
    if isinstance(obj, list):
        return [walk_json(v, fn) for v in obj]
    if isinstance(obj, str):
        return fn(obj)
    return obj


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("url")
    ap.add_argument("--remove", default="")
    ap.add_argument("--merge", default="")
    a = ap.parse_args(argv)
    src_path = os.path.join(ROOT, "src", "pages", a.url.strip("/") + ".html")
    raw = open(src_path, encoding="utf-8").read()
    end = raw.index("\n---\n", 4)
    front = json.loads(raw[4:end])
    body = raw[end + 5:]
    n = len(front["sources"])
    merge = {int(x.split(":")[0]): int(x.split(":")[1]) for x in a.merge.split(",") if x}
    drop = {int(x) for x in a.remove.split(",") if x} | set(merge)
    slug = a.url.strip("/").split("/")[-1]
    case_path = os.path.join(ROOT, "data", "cases", slug + ".json")
    case = json.load(open(case_path, encoding="utf-8")) if os.path.exists(case_path) else None
    # citations after merging
    step1 = {i: merge.get(i, i) for i in range(1, n + 1)}
    blob = remap_text(raw, step1) + (remap_text(json.dumps(case), step1) if case else "")
    cited = {int(x) for g in CITE.findall(blob) for x in re.split(r"\s*,\s*", g)}
    if case:
        for inp in case["inputs"].values():
            cited |= {step1[x] for x in (inp.get("source") or [])}
        cited |= {step1[x] if isinstance(x, int) else x for x in case.get("rule_sources", {}).values() if isinstance(x, int)}
        for v in case.get("rule_sources", {}).values():
            if isinstance(v, list):
                cited |= {step1[x] for x in v}
    still = sorted(d for d in drop if d in cited)
    if still:
        raise SystemExit(f"refused: sources still cited after the merge: {still}")
    keep = [i for i in range(1, n + 1) if i not in drop]
    renum = {old: new for new, old in enumerate(keep, 1)}
    final = {i: renum[step1[i]] for i in range(1, n + 1) if step1[i] in renum}
    front["sources"] = [front["sources"][i - 1] for i in keep]
    new_front = walk_json(front, lambda s: remap_text(s, final))
    new_front["sources"] = front["sources"]
    new_body = remap_text(body, final)
    with open(src_path, "w", encoding="utf-8") as fh:
        fh.write("---\n" + json.dumps(new_front, indent=2, ensure_ascii=False) + "\n---\n" + new_body)
    if case:
        for inp in case["inputs"].values():
            if inp.get("source"):
                inp["source"] = sorted({final[x] for x in inp["source"]})
        rs = case.get("rule_sources", {})
        for k, v in list(rs.items()):
            rs[k] = [final[x] for x in v] if isinstance(v, list) else final[v]
        case = walk_json(case, lambda s: remap_text(s, final))
        with open(case_path, "w", encoding="utf-8") as fh:
            json.dump(case, fh, indent=2, ensure_ascii=False)
            fh.write("\n")
    print(f"{a.url}: {n} sources -> {len(keep)}; removed {sorted(drop)}; merged {merge}")


if __name__ == "__main__":
    main(sys.argv[1:])
