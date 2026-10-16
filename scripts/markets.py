#!/usr/bin/env python3
"""Render market figures from the markets register (data/markets/) into pages.

The site is static HTML with no build step, so this script is the template
helper, on the pattern of scripts/regulatory.py. A page states a figure inside
a marker region and the script fills it from data/markets/series/<series>.json:

    <!--mkt:texas/houston.sba7a_loans.gas-station-and-c-store {"fmt": "int"}-->412<!--/mkt:texas/houston.sba7a_loans.gas-station-and-c-store-->

The marker name is <geo>.<series>[.<class>]: a geography id (`us`, a state's
USPS code such as `tx`, or a site market `<state>/<market>`), a series id (the
file name under data/markets/series/), and an asset-class slug (default `all`).
Optional JSON params:
  {"fmt": "int" | "usd" | "usd_m" | "pct" | "pct1" | "num"}   how to print the value
  {"window": "fy2016_2025"}   which period of a windowed series (default: the series' headline)
  {"fy": "2024"}              one approval fiscal year instead of a window
  {"fit": "partial" | "proxy"}  required when the class's NAICS fit is not exact,
                                so a proxy is never printed as if it were exact
  {"allow_flag": true}        print a value that carries a flag (a small denominator, or a class
                              figure that includes approval years before FY2001)
  {"scheme_fit": "approximate"}  required for a Connecticut component whose county
                              composition only approximates the market

The matching source line is its own marker and renders the period, publisher,
title and URL of the series, so value + source line give the site's four-part
citation. A source line must cite a period that a value marker for the same geography
and series on the page shows, and is refused for a geography the register holds no value for:

    <!--mktsrc:texas/houston.sba7a_loans {"window": "fy2016_2025"}-->...<!--/mktsrc:texas/houston.sba7a_loans-->

    python3 scripts/markets.py                       rewrite every region in every page
    python3 scripts/markets.py --check               exit 1 if any region is out of date
    python3 scripts/markets.py --pages <dir|file>    limit to these pages (e.g. the fixture)
    python3 scripts/markets.py audit                 write data/markets/audit.csv

A null value (a series the source does not publish for that geography, or a
composition still pending) stops the script with the null's reason: a page may
not print a figure the register does not hold.
"""
import csv
import html
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'markets')
NAME = r'[a-z0-9][a-z0-9/:-]*\.[a-z0-9_]+(?:\.[a-z0-9-]+)?'
BLOCK = re.compile(r'<!--mkt:(' + NAME + r')( \{.*?\})?-->(.*?)<!--/mkt:\1-->', re.S)
SRC = re.compile(r'<!--mktsrc:([a-z0-9][a-z0-9/:-]*\.[a-z0-9_]+)( \{.*?\})?-->(.*?)<!--/mktsrc:\1-->', re.S)
SKIP_DIRS = {'.git', 'docs', 'node_modules', 'netlify', '_cache', '_bundles'}
HEADLINE_WINDOW = 'fy2016_2025'

_series = {}
_sources = None
_naics = None


class MarkerError(SystemExit):
    pass


def series(sid):
    if sid not in _series:
        p = os.path.join(DATA, 'series', f'{sid}.json')
        if not os.path.exists(p):
            raise MarkerError(f'unknown series in marker: {sid}')
        with open(p, encoding='utf-8') as f:
            _series[sid] = json.load(f)
    return _series[sid]


def sources():
    global _sources
    if _sources is None:
        with open(os.path.join(DATA, 'sources.json'), encoding='utf-8') as f:
            _sources = json.load(f)
    return _sources


def class_fit(slug):
    global _naics
    if _naics is None:
        with open(os.path.join(DATA, 'naics-map.json'), encoding='utf-8') as f:
            _naics = {r['slug']: r for r in json.load(f)['classes']}
    if slug not in _naics:
        raise MarkerError(f'unknown asset class in marker: {slug}')
    return _naics[slug]['fit']


_geo = None


def ct_scheme_fit(geo):
    """'exact' or 'approximate' for a Connecticut component id (<market>:legacy|pr)."""
    global _geo
    if _geo is None:
        with open(os.path.join(DATA, 'geographies.json'), encoding='utf-8') as f:
            _geo = {f'{m["state"]}/{m["slug"]}': m for m in json.load(f)['markets']}
    mid, part = geo.rsplit(':', 1)
    m = _geo.get(mid)
    if not m or not (m['components'].get('ct')) or part not in ('legacy', 'pr'):
        return None
    txt = m['components']['ct'].get('fit_legacy' if part == 'legacy' else 'fit_planning') or ''
    return 'exact' if txt.lower().startswith('exact') else 'approximate'


def split(name):
    geo, rest = name.split('.', 1)
    parts = rest.split('.')
    return geo, parts[0], (parts[1] if len(parts) > 1 else 'all')


def lookup(name, p):
    geo, sid, cls = split(name)
    s = series(sid)
    if geo in s.get('nulls', {}):
        raise MarkerError(f'{name}: the register holds no value here ({s["nulls"][geo]})')
    if geo not in s['values']:
        raise MarkerError(f'{name}: geography {geo} is not in series {sid}')
    if ':' in geo:
        sf = ct_scheme_fit(geo)
        if sf == 'approximate' and p.get('scheme_fit') != 'approximate':
            raise MarkerError(f'{name}: this Connecticut component\'s county composition only approximates the market; '
                              'the marker must say {"scheme_fit": "approximate"} and the page must say so')
    if cls != 'all':
        fit = class_fit(cls)
        if fit == 'none':
            raise MarkerError(f'{name}: class {cls} has NAICS fit "none"; it has no federal figure')
        if fit != 'exact' and p.get('fit') != fit:
            raise MarkerError(f'{name}: class {cls} has NAICS fit "{fit}"; the marker must say {{"fit": "{fit}"}} and the page must say so')
    if cls not in s['values'][geo]:
        raise MarkerError(f'{name}: class {cls} is not in series {sid} for {geo}')
    cell = s['values'][geo][cls]
    if isinstance(cell, dict) and 'by_fy' in cell:
        complete = s.get('class_complete_from_fy')
        if 'fy' in p:
            first, last = s['by_fy_years']
            fy = int(p['fy'])
            if not first <= fy <= last:
                raise MarkerError(f'{name}: FY{fy} is outside {first} to {last}')
            early = cls != 'all' and complete and fy < complete
            val = cell['by_fy'][fy - first]
        else:
            w = p.get('window', HEADLINE_WINDOW)
            if w not in cell:
                raise MarkerError(f'{name}: window {w} is not in series {sid}')
            early = cls != 'all' and complete and w == 'all'
            val = cell[w]
        if early and not p.get('allow_flag'):
            raise MarkerError(f'{name}: a class figure covering approval years before FY{complete} undercounts ({s.get("class_coverage_note", "")}); '
                              'add {"allow_flag": true} only if the page says so')
        return val, None
    if isinstance(cell, dict):
        if 'window' in p or 'fy' in p:
            raise MarkerError(f'{name}: a rate covers its seasoned cohorts only ({s.get("label", "")}); window and fy do not apply')
        if cell.get('v') is None:
            raise MarkerError(f'{name}: null ({cell.get("f")})')
        if cell.get('f') and not p.get('allow_flag'):
            raise MarkerError(f'{name}: value carries a flag ({cell["f"]}); add {{"allow_flag": true}} only if the page states it')
        return cell['v'], cell.get('f')
    return cell, None


def check_fmt(name, unit, fmt):
    if unit == 'share' and fmt not in ('pct', 'pct1', None):
        raise MarkerError(f'{name}: a share prints as pct or pct1, not {fmt}')
    if unit != 'share' and fmt in ('pct', 'pct1'):
        raise MarkerError(f'{name}: {unit} is not a share; pct does not apply')
    if unit == 'USD' and fmt == 'int':
        raise MarkerError(f'{name}: a dollar amount prints as usd or usd_m')


def period_key(sid, p):
    if 'rate' in sid:
        return ('rate',)
    return ('fy', str(int(p['fy']))) if 'fy' in p else ('window', p.get('window', HEADLINE_WINDOW))


def fmt_value(v, fmt):
    if fmt == 'int':
        return f'{int(round(v)):,}'
    if fmt == 'usd':
        return f'${int(round(v)):,}'
    if fmt == 'usd_m':
        return f'${v / 1e6:,.1f} million'
    if fmt == 'pct':
        return f'{v * 100:.0f}%'
    if fmt == 'pct1':
        return f'{v * 100:.1f}%'
    if isinstance(v, float) and not v.is_integer():
        return f'{v:,.2f}'
    return f'{int(v):,}'


def window_label(s, p):
    if 'fy' in p:
        fy = int(p['fy'])
        last = (s.get('by_fy_years') or [None, None])[1]
        return f'approval FY{fy}' + (f' to {s["asof"]} (fiscal year in progress)' if fy == last and s.get('asof') else '')
    w = p.get('window', HEADLINE_WINDOW)
    return s.get('windows', {}).get(w, s.get('label', ''))


def source_line(name, p):
    geo, sid = name.split('.', 1)
    s = series(sid)
    if geo in s.get('nulls', {}):
        raise MarkerError(f'{name}: no source line for a geography the register holds no value for ({s["nulls"][geo]})')
    if geo not in s['values']:
        raise MarkerError(f'{name}: geography {geo} is not in series {sid}')
    src = next((r for r in sources().get('series', []) if r['id'] == sid), None)
    if not src:
        raise MarkerError(f'{name}: sources.json has no series row {sid}')
    if src['status'] != 'FETCHED':
        raise MarkerError(f'{name}: series {sid} is {src["status"]}')
    url = src.get('landing_page') or (src['url'][0] if isinstance(src['url'], list) else src['url'])
    if src['fetch_source'] == 'sba_foia':
        prog = '7(a)' if sid.startswith('sba7a') else '504'
        title = f'{prog} FOIA loan-level data, as of {s["asof"]}'
    else:
        title = src['title']
    period = window_label(s, p) if 'rate' not in sid else s.get('label', '')
    return (f'{html.escape(period)}. {html.escape(src["publisher"])}, {html.escape(title)}. '
            f'<a href="{html.escape(url)}">{html.escape(url)}</a>')


def process(text):
    # every source line must cite a period some value marker on the page uses
    shown = set()
    for m in BLOCK.finditer(text):
        p = json.loads(m.group(2)) if m.group(2) else {}
        geo, sid, _cls = split(m.group(1))
        shown.add((geo, sid, period_key(sid, p)))
    for m in SRC.finditer(text):
        p = json.loads(m.group(2)) if m.group(2) else {}
        geo, sid = m.group(1).split('.', 1)
        if (geo, sid, period_key(sid, p)) not in shown:
            raise MarkerError(f'mktsrc:{m.group(1)} cites {period_key(sid, p)}, which no value marker for {geo}.{sid} on this page shows')

    def sub(m):
        name, params = m.group(1), m.group(2)
        p = json.loads(params) if params else {}
        check_fmt(name, series(split(name)[1]).get('unit'), p.get('fmt'))
        val, _flag = lookup(name, p)
        head = f'<!--mkt:{name}' + (' ' + json.dumps(p, sort_keys=True) if p else '') + '-->'
        return f'{head}{html.escape(fmt_value(val, p.get("fmt")))}<!--/mkt:{name}-->'

    def subsrc(m):
        name, params = m.group(1), m.group(2)
        p = json.loads(params) if params else {}
        head = f'<!--mktsrc:{name}' + (' ' + json.dumps(p, sort_keys=True) if p else '') + '-->'
        return f'{head}{source_line(name, p)}<!--/mktsrc:{name}-->'
    return SRC.sub(subsrc, BLOCK.sub(sub, text))


def pages(targets=None):
    if targets:
        for t in targets:
            t = os.path.join(ROOT, t) if not os.path.isabs(t) else t
            if os.path.isfile(t):
                yield t
            else:
                for d, _, files in os.walk(t):
                    for f in files:
                        if f.endswith('.html'):
                            yield os.path.join(d, f)
        return
    for d, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in files:
            if f.endswith('.html') and not f.startswith('preview-') and not re.match(r'index_\d+\.html', f):
                yield os.path.join(d, f)


# ---------------------------------------------------------------- audit

def audit():
    """For each site market (and each state), count the non-null values specific
    to its own geography: one per (series, class) at the headline window, never
    the by-year breakdown and never a value inherited from the state.
    component_values counts the values held for a market's parts (Connecticut
    coding schemes, the state parts of a cross-state market); they are not
    market totals and do not count toward standalone."""
    with open(os.path.join(DATA, 'geographies.json'), encoding='utf-8') as f:
        geo = json.load(f)
    sdir = os.path.join(DATA, 'series')
    files = sorted(x[:-5] for x in os.listdir(sdir) if x.endswith('.json')) if os.path.isdir(sdir) else []
    src_of = {}
    for r in sources()['sources']:
        for sid in r.get('series') or []:
            src_of[sid] = r['id']
    n_sources = len(sources()['sources'])
    rows = []
    targets = [('state', st['id'], st.get('slug') or '', st.get('name') or st['id'].upper(), None, False) for st in geo['states'] if st.get('site_page')]
    targets += [('market', f'{m["state"]}/{m["slug"]}', m['state'], m['slug'], m['kind'], m.get('review', False)) for m in geo['markets']]
    for level, gid, a, b, kind, review in targets:
        specific = suppressed = 0
        unavailable = {}
        contributing = set()
        for sid in files:
            s = series(sid)
            if gid in s.get('nulls', {}):
                unavailable[sid] = s['nulls'][gid]
                continue
            cl = s['values'].get(gid)
            if not cl:
                continue
            for c, cell in cl.items():
                if isinstance(cell, dict) and 'by_fy' in cell:
                    v = cell.get(HEADLINE_WINDOW)
                    if v is not None:
                        specific += 1; contributing.add(src_of.get(sid, sid))
                elif isinstance(cell, dict):
                    if cell.get('v') is not None:
                        specific += 1; contributing.add(src_of.get(sid, sid))
                    elif cell.get('f', '').startswith('suppressed'):
                        suppressed += 1
                elif cell is not None:
                    specific += 1; contributing.add(src_of.get(sid, sid))
        components = 0
        if level == 'market':
            for sid in files:
                s = series(sid)
                for cid, cl in s['values'].items():
                    if cid.startswith(gid + ':'):
                        for cell in cl.values():
                            v = cell.get(HEADLINE_WINDOW) if isinstance(cell, dict) and 'by_fy' in cell else (cell.get('v') if isinstance(cell, dict) else cell)
                            components += v is not None
        reasons = sorted(set(unavailable.values()))
        standalone = specific >= 25
        rows.append({'level': level, 'geo': gid, 'state': a, 'name': b,
                     'kind': kind or 'state', 'review': 'yes' if review else 'no',
                     'specific_values': specific, 'suppressed_values': suppressed, 'component_values': components,
                     'sources_contributing': len(contributing), 'sources_total': n_sources,
                     'unavailable_series': len(unavailable),
                     'standalone': 'yes' if standalone else 'no',
                     'reason': '' if standalone else ('; '.join(reasons) if reasons else 'fewer than 25 values')})
    p = os.path.join(DATA, 'audit.csv')
    with open(p, 'w', newline='', encoding='utf-8') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)
    mk = [r for r in rows if r['level'] == 'market']
    print(f'audit: {len(mk)} markets, {sum(r["standalone"] == "yes" for r in mk)} standalone; wrote {os.path.relpath(p, ROOT)}')
    return 0


def main(argv):
    if argv and argv[0] == 'audit':
        return audit()
    check = '--check' in argv
    targets = None
    if '--pages' in argv:
        targets = argv[argv.index('--pages') + 1:]
        targets = [t for t in targets if not t.startswith('--')]
    stale, changed = [], []
    for p in pages(targets):
        src = open(p, encoding='utf-8').read()
        if '<!--mkt' not in src:
            continue
        out = process(src)
        if out != src:
            rel = os.path.relpath(p, ROOT)
            if check:
                stale.append(rel)
            else:
                open(p, 'w', encoding='utf-8').write(out); changed.append(rel)
    if check:
        for s in stale:
            print('out of date:', s)
        print(f'{len(stale)} page(s) out of date')
        return 1 if stale else 0
    for c in changed:
        print('rewrote', c)
    print(f'{len(changed)} page(s) rewritten')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
