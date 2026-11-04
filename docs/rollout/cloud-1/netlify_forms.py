#!/usr/bin/env python3
"""CLOUD-1 (owner, 4 Nov 2026): the contact form as a Netlify form.

    python3 netlify_forms.py <tree>

Every served page that carries the inquiry form (id="fsc-contact-form") gets the Netlify Forms attributes
(name="contact", method="POST", data-netlify="true", netlify-honeypot="company_website") and the hidden form-name
field, and its submit script posts the form url-encoded to "/" (Netlify's form endpoint) instead of JSON to
/api/contact. Validation, the honeypot check and the messages stay as they are. Idempotent; a page whose script is not
in the expected shape stops the run before anything is written.
"""
import os
import re
import sys

OPEN = '<form class="contact-form" id="fsc-contact-form" novalidate>'
NEW_OPEN = ('<form class="contact-form" id="fsc-contact-form" name="contact" method="POST" data-netlify="true" '
            'netlify-honeypot="company_website" novalidate>\n<input type="hidden" name="form-name" value="contact">')
FETCH = re.compile(r"fetch\('/api/contact',\{method:'POST',headers:\{'Content-Type':'application/json'\},body:JSON\.stringify\(\{[^}]*\}\)\}\)")
NEW_FETCH = ("fetch('/',{method:'POST',headers:{'Content-Type':'application/x-www-form-urlencoded'},"
             "body:new URLSearchParams(new FormData(f)).toString()})")


def main(tree):
    todo, errors = [], []
    for root, dirs, files in os.walk(tree):
        dirs[:] = [d for d in dirs if d not in ("docs", "src", "data", "scripts", "netlify", ".git", "node_modules")]
        for fn in files:
            if not fn.endswith(".html"):
                continue
            p = os.path.join(root, fn)
            s = open(p, encoding="utf-8").read()
            if 'id="fsc-contact-form"' not in s or 'data-netlify="true"' in s:
                continue
            if s.count(OPEN) != 1 or len(FETCH.findall(s)) != 1:
                errors.append(os.path.relpath(p, tree))
                continue
            todo.append((p, FETCH.sub(NEW_FETCH, s.replace(OPEN, NEW_OPEN))))
    if errors:
        raise SystemExit("netlify_forms: unexpected form or script shape, nothing written: " + ", ".join(errors))
    for p, s in todo:
        open(p, "w", encoding="utf-8").write(s)
    print(f"netlify_forms: {len(todo)} page(s) converted")


if __name__ == "__main__":
    main(sys.argv[1])
