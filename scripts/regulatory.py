#!/usr/bin/env python3
"""Render SBA regulatory values from data/regulatory/sba.json into the pages.

The site is static HTML with no build step, so this script is the template
helper. A page states a value inside a marker region and the script fills it:

    <!--sba:dscr.coo_initial_acquisition.value-->1.25x<!--/sba:dscr.coo_initial_acquisition.value-->

The marker name is a dotted path into sba.json. Optional JSON params after the
path format the value:  {"fmt": "date"} renders an ISO date as "October 1,
2026"; {"fmt": "month"} as "October 2026"; {"fmt": "list"} joins a list with
"; "; {"fmt": "table"} renders a list of pairs as <tr><td>a</td><td>b</td></tr>
rows; {"fmt": "rows"} renders a list as <li> items.

    python3 scripts/regulatory.py            rewrite every region in every page
    python3 scripts/regulatory.py --check    exit 1 if any region is out of date

Historical statements (what an earlier SOP said) sit inside an element carrying
data-historical="SOP 50 10 8" (or another edition); the gates skip those
elements when they grep for stale claims. This script does not touch them.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'regulatory', 'sba.json')
BLOCK = re.compile(r'<!--sba:([a-z0-9_.]+)( \{.*?\})?-->(.*?)<!--/sba:\1-->', re.S)
MONTHS = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
SKIP_DIRS = {'.git', 'docs', 'node_modules', 'netlify'}


def lookup(data, path):
    cur = data
    for part in path.split('.'):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            raise KeyError(path)
    if isinstance(cur, dict) and 'value' in cur and path.split('.')[-1] != 'value':
        cur = cur['value']
    return cur


def fmt_date(iso):
    y, m, d = (int(x) for x in iso.split('-'))
    return f'{MONTHS[m - 1]} {d}, {y}'


def render(value, params):
    fmt = (params or {}).get('fmt')
    if fmt == 'date':
        return f'<time datetime="{value}">{fmt_date(value)}</time>'
    if fmt == 'month':
        y, m, _ = value.split('-'); return f'{MONTHS[int(m) - 1]} {y}'
    if fmt == 'list':
        return html.escape('; '.join(value))
    if fmt == 'rows':
        return ''.join(f'<li>{html.escape(v)}</li>' for v in value)
    if fmt == 'table':
        return ''.join('<tr>' + ''.join(f'<td>{html.escape(c)}</td>' for c in row) + '</tr>' for row in value)
    if isinstance(value, list):
        return html.escape(', '.join(map(str, value)))
    return html.escape(str(value))


def process(text, data):
    def sub(m):
        name, params, _inner = m.group(1), m.group(2), m.group(3)
        p = json.loads(params) if params else None
        try:
            val = lookup(data, name)
        except KeyError:
            raise SystemExit(f'unknown sba.json path in marker: {name}')
        head = f'<!--sba:{name}' + (' ' + json.dumps(p, sort_keys=True) if p else '') + '-->'
        return f'{head}{render(val, p)}<!--/sba:{name}-->'
    return BLOCK.sub(sub, text)


def pages():
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith('.html') and not f.startswith('preview-') and not re.match(r'index_\d+\.html', f):
                yield os.path.join(d, f)


def main(argv):
    check = '--check' in argv
    data = json.load(open(DATA, encoding='utf-8'))
    stale = []
    changed = []
    for p in pages():
        src = open(p, encoding='utf-8').read()
        if '<!--sba:' not in src:
            continue
        out = process(src, data)
        if out != src:
            rel = os.path.relpath(p, ROOT)
            if check:
                stale.append(rel)
            else:
                open(p, 'w', encoding='utf-8').write(out); changed.append(rel)
    if check:
        for s in stale: print('out of date:', s)
        print(f'{len(stale)} page(s) out of date')
        return 1 if stale else 0
    for c in changed: print('rewrote', c)
    print(f'{len(changed)} page(s) rewritten')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
