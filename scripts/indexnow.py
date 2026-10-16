#!/usr/bin/env python3
"""Submit changed URLs to IndexNow (Bing, Yandex and the other IndexNow engines).

Google does not take IndexNow; it reads /sitemap.xml. The key is the file
<key>.txt at the repository root, served at https://feasibility-study-company.com/<key>.txt.

    python3 scripts/indexnow.py --since REF [--dry-run]
        every indexable page whose file changed between REF and HEAD, plus the sitemap
    python3 scripts/indexnow.py --urls FILE [--dry-run]
        the URLs in FILE, one per line

Run once per deploy, after the production deploy, by the lane that deployed:
REF is the commit that was live before the deploy. One POST per run, 30 second
timeout; the response status is printed (200 or 202 is success).
"""
import glob
import json
import os
import re
import subprocess
import sys
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import links  # noqa: E402
import sitemap  # noqa: E402

ROOT = links.ROOT
HOST = "feasibility-study-company.com"
ENDPOINT = "https://api.indexnow.org/indexnow"


def key():
    found = [os.path.basename(p)[:-4] for p in glob.glob(os.path.join(ROOT, "*.txt"))
             if re.fullmatch(r"[0-9a-f]{32}\.txt", os.path.basename(p))]
    if len(found) != 1:
        raise SystemExit(f"expected one IndexNow key file at the root, found {found}")
    k = found[0]
    with open(os.path.join(ROOT, k + ".txt"), encoding="utf-8") as fh:
        if fh.read().strip() != k:
            raise SystemExit("the key file does not contain its own key")
    return k


def changed_since(ref):
    out = subprocess.run(["git", "-C", ROOT, "diff", "--name-only", ref, "HEAD"],
                         capture_output=True, text=True, timeout=60, check=True).stdout.split()
    site = links.Site()
    by_rel = dict(site.pages)
    urls = []
    for rel in out:
        if rel in by_rel and sitemap.indexable(site.text(rel)):
            urls.append(links.SITE + by_rel[rel])
    urls.append(links.SITE + "/sitemap.xml")
    return sorted(set(urls))


def main(argv):
    if "--since" in argv:
        urls = changed_since(argv[argv.index("--since") + 1])
    elif "--urls" in argv:
        with open(argv[argv.index("--urls") + 1], encoding="utf-8") as fh:
            urls = [l.strip() for l in fh if l.strip()]
    else:
        print(__doc__)
        return 2
    k = key()
    body = {"host": HOST, "key": k, "keyLocation": f"https://{HOST}/{k}.txt", "urlList": urls}
    if "--dry-run" in argv:
        print(json.dumps({**body, "urlList": f"{len(urls)} URL(s)"}, indent=1))
        for u in urls:
            print(u)
        return 0
    req = urllib.request.Request(ENDPOINT, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"IndexNow {r.status} {r.reason}: {len(urls)} URL(s) submitted")
            return 0 if r.status in (200, 202) else 1
    except urllib.error.HTTPError as e:
        print(f"IndexNow {e.code} {e.reason}: {e.read()[:300]!r}")
        return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
