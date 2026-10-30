#!/usr/bin/env python3
"""ASSET-2: recompute every figure a page states as calculated, and check the page prints it.

    python3 docs/rollout/asset-2/recompute/recompute.py <site root>

Reads docs/rollout/asset-2/recompute/<slug>.tsv (printed_value, formula, inputs, sources). Each input is a
value the page prints with its cited source; the formula is the arithmetic the page describes. A row passes when
the formula's result rounds to the printed value at the printed precision, and the printed value and every input
appear in the served page. Exit 1 on any failure.
"""
import csv, glob, os, re, sys, html

ROOT = sys.argv[1] if len(sys.argv) > 1 else '.'
HERE = os.path.dirname(os.path.abspath(__file__))
PAGES = {}  # slug -> served path, from the manifest
for line in open(os.path.join(HERE, 'pages.tsv'), encoding='utf-8'):
    if line.strip() and not line.startswith('#'):
        slug, url = line.rstrip('\n').split('\t')
        PAGES[slug] = os.path.join(ROOT, url.strip('/'), 'index.html')


def num(s):
    s = s.strip().lower().replace(',', '').replace('$', '').replace('%', '').replace('x', '')
    mult = 1
    for w, m in (('billion', 1e9), ('million', 1e6), ('thousand', 1e3), ('b', 1e9), ('m', 1e6), ('k', 1e3)):
        if s.endswith(w):
            s, mult = s[: -len(w)].strip(), m
            break
    return float(s) * mult


def decimals(s):
    m = re.search(r'\.(\d+)', s.replace(',', ''))
    return len(m.group(1)) if m else 0


def text(p):
    t = open(p, encoding='utf-8').read()
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', html.unescape(t))


fails = rows = 0
for f in sorted(glob.glob(os.path.join(HERE, '*.tsv'))):
    slug = os.path.basename(f)[:-4]
    if slug == 'pages':
        continue
    page = text(PAGES[slug])
    for r in csv.reader(open(f, encoding='utf-8'), delimiter='\t'):
        if not r or r[0].startswith('#') or r[0] == 'printed_value':
            continue
        rows += 1
        printed, formula, inputs = r[0], r[1], r[2]
        env, missing = {}, []
        for kv in inputs.split(';'):
            if kv.strip():
                k, v = kv.split('=', 1)
                env[k.strip()] = num(v)
                if v.strip() not in page:
                    missing.append(v.strip())
        got = eval(formula, {'__builtins__': {}, 'round': round, 'min': min, 'max': max}, env)
        want = num(printed)
        scale = 1
        for w, m in (('billion', 1e9), ('million', 1e6), ('thousand', 1e3)):
            if w in printed.lower():
                scale = m
        if '%' in printed and abs(got) < 5 and abs(want) >= 1:
            got *= 100
        ok_val = round(got / scale, decimals(printed)) == round(want / scale, decimals(printed))
        ok_page = printed.strip() in page
        if not (ok_val and ok_page and not missing):
            fails += 1
            print(f'FAIL {slug}: printed {printed!r} computed {got:.6g} value_ok={ok_val} on_page={ok_page} '
                  f'inputs_missing={missing} ({formula})')
print(f'{rows} calculated figures checked, {fails} failing')
sys.exit(1 if fails else 0)
