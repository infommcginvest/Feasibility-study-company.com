#!/usr/bin/env python3
"""Build the markets register (data/markets/) from the raw files that
scripts/markets_fetch.py left in _cache/markets/.

    python3 scripts/markets_build.py          build from the raw files
    python3 scripts/markets_build.py --diff   build, then print every value that
                                              changed against the previous register

Inputs that are authored, not fetched (committed under data/markets/):
  geographies.json       site markets and their compositions
  naics-map.json         the 43 asset classes and their NAICS codes by edition
  foia-status-map.json   every SBA FOIA LoanStatus value, classified

Outputs (data/markets/):
  sources.json             one row per series: publisher, title, URL, vintage, period,
                           retrieval date, raw sha256, cadence, next release, status
  series/<id>.json         values keyed by geography id
  geo/<state>/<market>.json and geo/states/<id>.json   bundles per market and state
  foia-status-counts.json  measured status counts and the evidence behind each category
  foia-geocoding.json      FOIA match rates by state and method
  foia-county-strings.json FOIA totals by (state, ProjectCounty string), for the FIPS join
  naics-evidence.json      FOIA loans by class, NAICS code and NAICS edition
  reconciliation.json      register totals against the raw files

Geography ids: `us`; a state is its USPS code in lower case (`tx`); a site
market is `<state-slug>/<market-slug>` (`texas/houston`). County FIPS and CBSA
ids (`co-48453`, `cbsa-12420`) join the scheme when a Census roster is fetched.

A value is a number, or an object {"v": number|null, "moe": number, "f": flag}.
A null always carries a flag saying why. Nothing here averages a rate or a
median: a market's count is the sum of its loans, and a rate is a sum of
numerators over a sum of denominators.
"""
import csv
import datetime as dt
import hashlib
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, 'data', 'markets')
CACHE = os.path.join(ROOT, '_cache', 'markets')
MANIFEST = os.path.join(CACHE, 'manifest.json')

FY_FIRST = 1991
SEASONED = (2011, 2020)       # approval cohorts pooled for a charge-off rate
WINDOWS = {                   # id: (first FY, last FY, label)
    'all': (FY_FIRST, None, 'all approval fiscal years in the files'),
    'fy2016_2025': (2016, 2025, 'approval FY2016 to FY2025 (ten full fiscal years)'),
    'fy2021_2025': (2021, 2025, 'approval FY2021 to FY2025 (five full fiscal years)'),
    'fy2025': (2025, 2025, 'approval FY2025 (October 2024 to September 2025)'),
    'fy2026ytd': (2026, 2026, 'approval FY2026 to the files\' as-of date'),
}
HEADLINE_WINDOW = 'fy2016_2025'
SMALL_DENOMINATOR = 30


def jload(p):
    with open(p, encoding='utf-8') as f:
        return json.load(f)


def jdump(obj, p, compact=False):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        if compact:
            json.dump(obj, f, separators=(',', ':'), sort_keys=True, ensure_ascii=False)
        else:
            json.dump(obj, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write('\n')
    os.replace(tmp, p)


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


class BuildError(Exception):
    pass


# ---------------------------------------------------------------- FOIA

FOIA_FILE = re.compile(r'FOIA_(7a|504)_FY(\d{4})_(FY\d{4}|Present)_asof_(\d{6})\.csv$')
METRICS = ('approved', 'approved_vol', 'cancelled', 'undisbursed', 'loans', 'volume',
           'disbursed', 'disbursed_vol', 'chgoff_n', 'chgoff_amt')
# Series files written for pages; the other metrics stay internal (reconciliation)
# to keep data/markets/ well under its 60 MB cap.
PUBLISHED = ('loans', 'volume', 'cancelled', 'disbursed', 'chgoff_n', 'chgoff_amt')


def money(s):
    s = (s or '').strip().replace(',', '').replace('$', '')
    return float(s) if s else 0.0


def norm_county(s):
    return re.sub(r'\s+', ' ', (s or '').strip().upper())


def naics_index(nmap):
    """code -> sorted tuple of class slugs, over every NAICS edition listed."""
    idx = defaultdict(set)
    for row in nmap['classes']:
        for code in row.get('naics2022', []):
            idx[code].add(row['slug'])
        for codes in (row.get('legacy') or {}).values():
            for code in codes:
                idx[code].add(row['slug'])
    return {c: tuple(sorted(s)) for c, s in idx.items()}


def read_foia(files, smap, nidx):
    """One pass over the FOIA CSVs. Returns the fine aggregate keyed by
    (program, state, county string, FY, class tuple) plus the evidence tables."""
    agg = defaultdict(lambda: [0.0] * len(METRICS))
    status_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
    code_tally = defaultdict(lambda: [0, 9999, 0, 0.0])          # (program, code) -> n, fy_min, fy_max, volume
    raw_totals = defaultdict(lambda: [0, 0.0, 0, 0.0])            # (program, fy) -> rows, gross, cancelled rows, cancelled gross
    county_blank = defaultdict(int)
    unknown = []
    rows_by_file = {}
    for path in files:
        m = FOIA_FILE.search(path)
        prog = m.group(1)
        pmap = smap['programs'][prog]
        n = 0
        with open(path, newline='', encoding='utf-8', errors='strict') as fh:
            for row in csv.DictReader(fh):
                n += 1
                st = row['LoanStatus']
                if st not in pmap:
                    unknown.append((os.path.basename(path), st))
                    continue
                cat = pmap[st]['category']
                cinfo = smap['categories'][cat]
                fy = int(row['ApprovalFY'])
                gross = money(row['GrossApproval'])
                coamt = money(row['GrossChargeOffAmount'])
                codate = (row['ChargeOffDate'] or '').strip()
                disb = bool((row['FirstDisbursementDate'] or '').strip())
                sc = status_counts[prog][os.path.basename(path)][st]
                status_counts[prog][os.path.basename(path)][st] = sc + 1
                ev = status_counts[prog]['_evidence']
                ev[f'{st}|first_disbursement_date'] += disb
                ev[f'{st}|charge_off_date'] += bool(codate)
                ev[f'{st}|charge_off_amount_gt0'] += coamt > 0
                ev[f'{st}|rows'] += 1
                if not cinfo['charged_off'] and (codate or coamt > 0):
                    raise BuildError(f'{os.path.basename(path)}: status {st!r} ({cat}) carries charge-off evidence; '
                                     'a new charged-off code may have appeared. Classify it in foia-status-map.json.')
                state = row['ProjectState'].strip().upper()
                county = norm_county(row['ProjectCounty'])
                if not county:
                    county_blank[(prog, state)] += 1
                code = (row['NaicsCode'] or '').strip()
                classes = nidx.get(code, ())
                t = code_tally[(prog, code)]
                t[0] += 1; t[1] = min(t[1], fy); t[2] = max(t[2], fy); t[3] += gross
                rt = raw_totals[(prog, fy)]
                rt[0] += 1; rt[1] += gross
                a = agg[(prog, state, county, fy, classes)]
                a[0] += 1; a[1] += gross
                if cinfo['cancelled']:
                    a[2] += 1; rt[2] += 1; rt[3] += gross
                else:
                    a[4] += 1; a[5] += gross
                    if cinfo['disbursed']:
                        a[6] += 1; a[7] += gross
                    else:
                        a[3] += 1
                if cinfo['charged_off']:
                    a[8] += 1; a[9] += coamt
        rows_by_file[os.path.basename(path)] = n
    if unknown:
        seen = sorted(set(unknown))
        raise BuildError(f'unclassified LoanStatus value(s): {seen}. Classify every value in foia-status-map.json.')
    return agg, status_counts, code_tally, raw_totals, county_blank, rows_by_file


def windows_of(fy):
    out = []
    for w, (a, b, _) in WINDOWS.items():
        if fy >= a and (b is None or fy <= b):
            out.append(w)
    return out


def rollup(agg, geo_of, fy_last, classes_all):
    """Sum the fine aggregate into {geo: {program: {class: {window|fy: [metrics]}}}}.
    geo_of(program, state, county) -> list of geo ids the loan belongs to."""
    out = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: [0.0] * len(METRICS)))))
    for (prog, state, county, fy, classes), vals in agg.items():
        geos = geo_of(prog, state, county)
        if not geos:
            continue
        keys = [str(fy)] + windows_of(fy)
        for g in geos:
            for c in ('all',) + classes:
                cell = out[g][prog][c]
                for k in keys:
                    t = cell[k]
                    for i, v in enumerate(vals):
                        t[i] += v
    return out


def foia_series(roll, geos, classes_all, fy_last, prog_ids):
    """Turn the rollup into series dicts. Every listed geo and class gets an
    explicit value in every window (zero when no loan), because the FOIA files
    list every approval and a missing cell is a true zero, not a suppression."""
    fys = [str(y) for y in range(FY_FIRST, fy_last + 1)]
    series = {}
    zero = [0.0] * len(METRICS)
    for prog in prog_ids:
        p = 'sba7a' if prog == '7a' else 'sba504'
        sdict = {m: {} for m in METRICS}
        rate_n, rate_a = {}, {}
        for g in geos:
            for c in ['all'] + classes_all:
                cell = roll.get(g, {}).get(prog, {}).get(c, {})
                for i, m in enumerate(METRICS):
                    win = {w: _num(cell.get(w, zero)[i]) for w in WINDOWS}
                    win['by_fy'] = [_num(cell.get(y, zero)[i]) for y in fys]
                    sdict[m].setdefault(g, {})[c] = win
                num = sum(cell.get(str(y), zero)[8] for y in range(SEASONED[0], SEASONED[1] + 1))
                den = sum(cell.get(str(y), zero)[6] for y in range(SEASONED[0], SEASONED[1] + 1))
                numa = sum(cell.get(str(y), zero)[9] for y in range(SEASONED[0], SEASONED[1] + 1))
                dena = sum(cell.get(str(y), zero)[7] for y in range(SEASONED[0], SEASONED[1] + 1))
                rate_n.setdefault(g, {})[c] = _rate(num, den)
                rate_a.setdefault(g, {})[c] = _rate(numa, dena)
        for m in PUBLISHED:
            series[f'{p}_{m}'] = sdict[m]
        series[f'{p}_chgoff_rate'] = rate_n
        series[f'{p}_chgoff_amt_rate'] = rate_a
    return series


def _num(x):
    return int(x) if float(x).is_integer() else round(x, 2)


def _rate(num, den):
    if den == 0:
        return {'v': None, 'num': _num(num), 'den': _num(den), 'f': 'no-disbursed-loans-in-seasoned-cohorts'}
    v = {'v': round(num / den, 6), 'num': _num(num), 'den': _num(den)}
    if den < SMALL_DENOMINATOR:
        v['f'] = f'small-denominator (<{SMALL_DENOMINATOR} disbursed loans)'
    return v


# ---------------------------------------------------------------- geographies

def market_id(m):
    return f'{m["state"]}/{m["slug"]}'


def market_foia_plan(m):
    """How a market gets FOIA values: ('sum', {(STATE, COUNTY)}), ('ct', schemes)
    or ('null', flag). Driven by the row's composition_source (geographies.json)."""
    src = m.get('composition_source')
    comp = m.get('foia') or {}
    if src == 'cbsa-delineation-pending':
        return 'null', ('composition-pending: the member counties of this market rest on CBSA membership, which must come from the OMB '
                        'delineation file; it was NOT FETCHED (census_delineation: www2.census.gov robots.txt; census_geoinfo: Census Data API key wall)')
    if src == 'sub-county':
        return 'null', 'not-published-at-this-grain: the SBA FOIA files carry a project county, not a place or tract'
    if src == 'connecticut-two-schemes':
        ct = comp.get('ct') or {}
        return 'ct', {'legacy': {('CT', norm_county(x)) for x in ct.get('legacy', [])}, 'pr': {('CT', norm_county(x)) for x in ct.get('pr', [])}}
    if src not in ('single-county', 'page-named-counties', 'judgement-region'):
        raise BuildError(f'{market_id(m)}: unknown composition_source {src!r}')
    keys = {(s['state'].strip().upper(), norm_county(s['string'])) for s in comp.get('strings', [])}
    if not comp.get('resolved') or not keys:
        return 'null', 'no-component-county-strings'
    return 'sum', keys


def load_geographies():
    g = jload(os.path.join(DATA, 'geographies.json'))
    ids = [market_id(m) for m in g['markets']]
    if len(ids) != len(set(ids)):
        dup = sorted({i for i in ids if ids.count(i) > 1})
        raise BuildError(f'duplicate market ids in geographies.json: {dup}')
    return g


# ---------------------------------------------------------------- sources

def manifest():
    return jload(MANIFEST) if os.path.exists(MANIFEST) else {'files': {}, 'sources': {}}


def fetch_module():
    sys.path.insert(0, os.path.join(ROOT, 'scripts'))
    import markets_fetch
    return markets_fetch


def sources_rows(man, built):
    mf = fetch_module()
    rows = []
    for s in mf.SOURCES:
        rec = man['sources'].get(s['id'], {})
        files = [man['files'][k] for k in rec.get('files', []) if k in man['files']]
        if s['kind'] == 'sba' and rec.get('vintage'):
            asof = dt.date.fromisoformat(rec['vintage'])
            fy = asof.year + (1 if asof.month >= 10 else 0)
            s = dict(s, period=f'approval FY{FY_FIRST} to FY{fy}, loan status as of {asof.isoformat()}',
                     next_release=sba_next_release(asof).isoformat())
        row = {
            'id': s['id'],
            'fetch_source': s['id'],
            'publisher': s['publisher'],
            'title': s['title'],
            'url': [f['url'] for f in files] if files else (s.get('urls') or [f'https://api.census.gov/data/{s["api_path"]}' if s.get('api_path') else (mf.SBA_PAGE if s['kind'] == 'sba' else 'https://apps.bea.gov/api/data')]),
            'vintage': rec.get('vintage') or s.get('vintage'),
            'period': s.get('period'),
            'retrieved': max((f['retrieved_at'] for f in files), default=None),
            'sha256': {os.path.basename(f['path']): f['sha256'] for f in files} or None,
            'cadence': s['cadence'],
            'next_release': s.get('next_release'),
            'status': rec.get('status', 'NOT FETCHED'),
            'reason': rec.get('reason'),
            'series': built.get(s['id'], []),
        }
        rows.append(row)
    return rows


# ---------------------------------------------------------------- main build

def build(diff=False):
    man = manifest()
    smap = jload(os.path.join(DATA, 'foia-status-map.json'))
    nmap = jload(os.path.join(DATA, 'naics-map.json'))
    geo = load_geographies()
    nidx = naics_index(nmap)
    classes_all = [r['slug'] for r in nmap['classes']]
    old = snapshot_values() if diff else None
    built = defaultdict(list)
    report = {}

    sba = man['sources'].get('sba_foia', {})
    if sba.get('status') == 'FETCHED':
        files = sorted(os.path.join(ROOT, k) for k in sba['files'] if FOIA_FILE.search(k))
        for f in files:
            k = os.path.relpath(f, ROOT)
            if sha256(f) != man['files'][k]['sha256']:
                raise BuildError(f'{k} does not match the sha256 in the manifest')
        asof = sorted({FOIA_FILE.search(f).group(4) for f in files})
        if len(asof) != 1:
            raise BuildError(f'FOIA files carry {len(asof)} as-of dates')
        asof = asof[0]
        asof_date = dt.date(2000 + int(asof[:2]), int(asof[2:4]), int(asof[4:]))
        fy_last = asof_date.year + (1 if asof_date.month >= 10 else 0)
        agg, status_counts, code_tally, raw_totals, county_blank, rows_by_file = read_foia(files, smap, nidx)

        states = sorted({k[1] for k in agg if k[1]})
        plans = {market_id(m): market_foia_plan(m) for m in geo['markets']}
        member = defaultdict(list)            # (STATE, COUNTY) -> market ids
        component_ids = []
        for mid, (how, keys) in plans.items():
            if how == 'sum':
                for k in keys:
                    member[k].append(mid)
                if len({st for st, _ in keys}) > 1:
                    # a cross-state market also gets one component per state part
                    for st in sorted({st for st, _ in keys}):
                        cid = f'{mid}:{st.lower()}'
                        component_ids.append(cid)
                        for k in keys:
                            if k[0] == st:
                                member[k].append(cid)
            elif how == 'ct':
                # Connecticut: each scheme is an exact set of loans, but neither is
                # the market total, so the market id itself stays null.
                for scheme, ks in keys.items():
                    component_ids.append(f'{mid}:{scheme}')
                    for k in ks:
                        member[k].append(f'{mid}:{scheme}')

        def geo_of(prog, state, county):
            out = ['us']
            if state:
                out.append(state.lower())
            out.extend(member.get((state, county), ()))
            return out

        roll = rollup(agg, geo_of, fy_last, classes_all)
        geo_ids = ['us'] + [s.lower() for s in states] + [mid for mid, (how, _) in plans.items() if how == 'sum'] + component_ids
        series = foia_series(roll, geo_ids, classes_all, fy_last, ('7a', '504'))
        nulls = {mid: flag for mid, (how, flag) in plans.items() if how == 'null'}
        for mid, (how, _) in plans.items():
            if how == 'ct':
                nulls[mid] = ('ct-split-coding: SBA codes Connecticut project counties in two schemes (the eight legacy counties and the nine 2022 planning regions) '
                              f'that do not nest, so no market total exists; the exact components are {mid}:legacy (loans coded to the market\'s legacy counties) '
                              f'and {mid}:pr (loans coded to its planning regions)')
        meta = foia_meta(asof_date, fy_last)
        for sid, values in series.items():
            prog = 'sba_7a_foia' if sid.startswith('sba7a') else 'sba_504_foia'
            out = {'id': sid, 'source': 'sba_foia', 'program': prog, **meta[sid.split('_', 1)[1]],
                   'windows': {w: lab for w, (_, _, lab) in WINDOWS.items()},
                   'by_fy_years': [FY_FIRST, fy_last], 'asof': asof_date.isoformat(),
                   'classes_note': 'Classes are not mutually exclusive (a loan coded 721110 counts under every hotel class); never sum across classes. "all" is every loan.',
                   'values': values, 'nulls': nulls}
            jdump(out, os.path.join(DATA, 'series', f'{sid}.json'), compact=True)
            built['sba_foia'].append(sid)
        report['foia'] = foia_reports(agg, status_counts, code_tally, raw_totals, county_blank, rows_by_file,
                                      roll, plans, nmap, geo, fy_last, asof_date)
    else:
        report['foia'] = None

    for s in sources_rows(man, built):
        report.setdefault('sources', []).append(s)
    jdump({'about': ('sources: one row per fetch source, status FETCHED or NOT FETCHED with the reason; series lists the series files built from it. '
                     'series: one row per series file with the citation fields of the exact raw files behind it (publisher, title, URL, vintage, period, '
                     'retrieval date, sha256, cadence, next release). The SBA FOIA definitions, including the seasoned charge-off cohorts, are in definitions.'),
           'definitions': foia_definitions(), 'sources': report['sources'], 'series': series_rows(report['sources'], man)},
          os.path.join(DATA, 'sources.json'))
    write_bundles(geo)
    if diff:
        print_diff(old, snapshot_values())
    return report


def sba_next_release(asof):
    """SBA: 'updated quarterly ... typically available one month after the
    quarter has ended'. The next as-of date is the next quarter end; its files
    are expected about one month later."""
    m = asof.month + 3
    y = asof.year + (m - 1) // 12
    m = (m - 1) % 12 + 1
    qend = dt.date(y, m, [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    nm = qend.month % 12 + 1
    ny = qend.year + (1 if qend.month == 12 else 0)
    return dt.date(ny, nm, 28) if nm == 2 else dt.date(ny, nm, 30 if nm in (4, 6, 9, 11) else 31)


def series_rows(srcrows, man):
    """One sources.json row per series file, carrying the citation fields of
    the exact raw files it is built from."""
    out = []
    for r in srcrows:
        for sid in r.get('series') or []:
            row = {k: r[k] for k in ('publisher', 'vintage', 'period', 'retrieved', 'cadence', 'next_release', 'status')}
            row['id'] = sid
            row['fetch_source'] = r['id']
            if r['id'] == 'sba_foia':
                prog = '7a' if sid.startswith('sba7a') else '504'
                files = {k: v for k, v in (r['sha256'] or {}).items() if f'_{prog}_' in k}
                row['title'] = (f'{"7(a)" if prog == "7a" else "504"} FOIA loan-level data as of {r["vintage"]} ('
                                + ', '.join(sorted(files)) + '); data.sba.gov dataset "7(a) & 504 FOIA"')
                row['url'] = [u for u in r['url'] if f'_{prog}_' in u]
                row['landing_page'] = 'https://data.sba.gov/dataset/7a-504-foia'
                row['sha256'] = files
                row['definition'] = foia_definitions().get(sid.split('_', 1)[1])
            else:
                row['title'], row['url'], row['sha256'] = r['title'], r['url'], r['sha256']
            out.append(row)
    return out


def foia_definitions():
    return {
        'loans': 'Approvals net of cancellations: every loan in the FOIA files whose LoanStatus is not cancelled (CANCLD). Undisbursed loans (7(a) COMMIT, 504 NOT FUNDED) are included because they are live approvals.',
        'volume': 'Sum of GrossApproval over the same loans. 7(a): total loan amount; 504: SBA/CDC (debenture) loan amount, not the whole project.',
        'approved': 'Every approval row in the files, including loans later cancelled.',
        'disbursed': 'Loans with a disbursed status: paid in full, charged off, active (EXEMPT), and 504 CLOSED. The denominator of the charge-off rate.',
        'chgoff_n': 'Loans with status CHGOFF, by approval fiscal year (a cohort count, not charge-offs dated in that year).',
        'chgoff_amt': 'Sum of GrossChargeOffAmount over CHGOFF loans (7(a): guaranteed and unguaranteed portion; 504: SBA/CDC balance).',
        'chgoff_rate': f'Seasoned cohorts only: approval FY{SEASONED[0]} to FY{SEASONED[1]} pooled, each at least five full fiscal years old at the as-of date. Rate = sum of charged-off loans / sum of disbursed loans over those cohorts. Cancelled and undisbursed loans never enter the denominator. A denominator under {SMALL_DENOMINATOR} is flagged.',
        'chgoff_amt_rate': f'Same cohorts: sum of GrossChargeOffAmount / sum of GrossApproval of disbursed loans.',
        'class': 'A loan belongs to every class whose NAICS code list (any edition, see naics-map.json) contains its NaicsCode. Loans with a blank NaicsCode belong to no class but count in "all".',
        'geography': 'us = every row in the files (all states and territories). A state is the loan\'s ProjectState. A site market sums the loans whose (ProjectState, ProjectCounty) strings are listed in its composition (geographies.json).',
    }


def foia_meta(asof, fy_last):
    t = {
        'approved': ('loans', 'Approved loans, including later cancellations'),
        'approved_vol': ('USD', 'Gross approval of all approved loans'),
        'cancelled': ('loans', 'Cancelled loans'),
        'undisbursed': ('loans', 'Approved, not cancelled, not yet disbursed'),
        'loans': ('loans', 'Loans approved, net of cancellations'),
        'volume': ('USD', 'Gross approval, net of cancellations'),
        'disbursed': ('loans', 'Disbursed loans'),
        'disbursed_vol': ('USD', 'Gross approval of disbursed loans'),
        'chgoff_n': ('loans', 'Charged-off loans by approval cohort'),
        'chgoff_amt': ('USD', 'Gross charge-off amount by approval cohort'),
        'chgoff_rate': ('share', f'Charge-off rate by count, seasoned cohorts FY{SEASONED[0]} to FY{SEASONED[1]}'),
        'chgoff_amt_rate': ('share', f'Charge-off rate by amount, seasoned cohorts FY{SEASONED[0]} to FY{SEASONED[1]}'),
    }
    return {k: {'unit': u, 'label': lab, 'aggregation': 'ratio of summed numerator and denominator' if 'rate' in k else 'sum'} for k, (u, lab) in t.items()}


def foia_reports(agg, status_counts, code_tally, raw_totals, county_blank, rows_by_file, roll, plans, nmap, geo, fy_last, asof):
    # status counts with evidence
    sc = {}
    for prog, files in status_counts.items():
        sc[prog] = {}
        for f, d in files.items():
            sc[prog][f] = dict(sorted(d.items()))
    jdump({'about': 'Measured from the raw FOIA files on every build. _evidence counts, per status, the rows with a FirstDisbursementDate, a ChargeOffDate and a GrossChargeOffAmount above zero.',
           'asof': asof.isoformat(), 'rows_by_file': rows_by_file, 'counts': sc}, os.path.join(DATA, 'foia-status-counts.json'))

    # geocoding: by program and state, rows with a ProjectCounty string vs blank
    totals = defaultdict(int)
    for (prog, state, county, fy, classes), v in agg.items():
        totals[(prog, state)] += int(v[0])
    in_market = defaultdict(int)
    keyset = {}
    for mid, (how, keys) in plans.items():
        if how == 'sum':
            for k in keys:
                keyset[k] = True
        elif how == 'ct':
            for ks in keys.values():
                for k in ks:
                    keyset[k] = True
    for (prog, state, county, fy, classes), v in agg.items():
        if (state, county) in keyset:
            in_market[(prog, state)] += int(v[0])
    rows = []
    for (prog, state), n in sorted(totals.items()):
        blank = county_blank.get((prog, state), 0)
        rows.append({'program': prog, 'state': state, 'rows': n, 'project_county_present': n - blank,
                     'unmatched_blank_county': blank, 'match_rate_project_county': round((n - blank) / n, 6) if n else None,
                     'in_a_site_market_composition': in_market.get((prog, state), 0)})
    ct = defaultdict(lambda: defaultdict(int))
    legacy = {'FAIRFIELD', 'HARTFORD', 'LITCHFIELD', 'MIDDLESEX', 'NEW HAVEN', 'NEW LONDON', 'TOLLAND', 'WINDHAM'}
    for (prog, state, county, fy, classes), v in agg.items():
        if state == 'CT':
            scheme = 'legacy_county' if county in legacy else ('blank' if not county else 'planning_region')
            ct[f'{prog}|FY{fy}'][scheme] += int(v[0])
    jdump({'about': 'FOIA geocoding. Method project_county: the loan carries a ProjectCounty string under its ProjectState. The ZIP method (BorrZip to ZCTA to county) is not available: the ZCTA-to-county relationship file is on www2.census.gov (robots, D1). A blank ProjectCounty is reported unmatched, never dropped: it still counts in its state and in us. County strings are not yet joined to FIPS (no county roster fetched); foia-county-strings.json carries them for that join.',
           'methods': {'project_county': 'ProjectState + ProjectCounty string as written by SBA', 'zip_zcta': 'NOT AVAILABLE (census relationship file not fetched)'},
           'by_state': rows,
           'connecticut_scheme_by_fy': {k: dict(v) for k, v in sorted(ct.items())}},
          os.path.join(DATA, 'foia-geocoding.json'))

    # county strings
    cs = defaultdict(lambda: defaultdict(lambda: [0, 0.0, 0, 0.0, 9999, 0]))
    for (prog, state, county, fy, classes), v in agg.items():
        t = cs[f'{state}|{county}'][prog]
        t[0] += int(v[4]); t[1] += v[5]; t[2] += int(v[8]); t[3] += v[9]; t[4] = min(t[4], fy); t[5] = max(t[5], fy)
    jdump({'about': 'FOIA totals by (ProjectState, ProjectCounty) string as SBA writes it, all approval years: loans (net of cancellations), volume, charge-offs, charge-off amount, first and last approval FY. Keyed "STATE|COUNTY STRING". For the join to county FIPS once a Census county roster is fetched.',
           'fields': ['loans', 'volume', 'chgoff_n', 'chgoff_amt', 'fy_min', 'fy_max'],
           'values': {k: {p: [t[0], round(t[1], 2), t[2], round(t[3], 2), t[4], t[5]] for p, t in v.items()} for k, v in sorted(cs.items())}},
          os.path.join(DATA, 'foia-county-strings.json'), compact=True)

    # naics evidence
    editions = {}
    for row in nmap['classes']:
        for code in row.get('naics2022', []):
            editions.setdefault((row['slug'], code), set()).add('2022')
        for ed, codes in (row.get('legacy') or {}).items():
            for code in codes:
                editions.setdefault((row['slug'], code), set()).add(ed)
    ev = {}
    for row in nmap['classes']:
        slug = row['slug']
        codes = sorted({c for (s, c) in editions if s == slug})
        by_code = {}
        by_edition = defaultdict(int)
        for c in codes:
            for prog in ('7a', '504'):
                t = code_tally.get((prog, c))
                if t:
                    d = by_code.setdefault(c, {'editions': sorted(editions[(slug, c)])})
                    d[prog] = {'loans_all_statuses': t[0], 'fy_min': t[1], 'fy_max': t[2]}
                    by_edition['+'.join(sorted(editions[(slug, c)]))] += t[0]
        ev[slug] = {'fit': row.get('fit'), 'codes_in_map': codes, 'foia_by_code': by_code,
                    'foia_loans_by_edition_set': dict(by_edition),
                    'foia_loans_total': sum(v.get('7a', {}).get('loans_all_statuses', 0) + v.get('504', {}).get('loans_all_statuses', 0) for v in by_code.values())}
    unmapped = sorted(((p, c), t[0]) for (p, c), t in code_tally.items() if c and not any(c in r for r in [set(x['codes_in_map']) for x in ev.values()]))
    blank = {p: code_tally[(p, '')][0] for p in ('7a', '504') if (p, '') in code_tally}
    jdump({'about': 'FOIA loans (all statuses) by asset class, NAICS code and the NAICS editions the map lists the code under. A code can sit in several editions; foia_loans_by_edition_set groups by that set. Loans with a blank NaicsCode belong to no class.',
           'classes': ev, 'blank_naics_loans': blank, 'codes_in_no_class': len(unmapped)},
          os.path.join(DATA, 'naics-evidence.json'))

    # reconciliation: us by FY against the raw recount kept during the read
    rec = []
    for (prog, fy), (n, gross, cn, cgross) in sorted(raw_totals.items()):
        cell = roll['us'][prog]['all'][str(fy)]
        rec.append({'program': prog, 'fy': fy, 'raw_rows': n, 'raw_gross': round(gross, 2),
                    'raw_cancelled': cn, 'register_approved': int(cell[0]), 'register_loans': int(cell[4]),
                    'register_volume': round(cell[5], 2),
                    'match': int(cell[0]) == n and int(cell[4]) == n - cn and abs(cell[5] - (gross - cgross)) < 0.01})
    st_sum = defaultdict(lambda: [0, 0.0])
    for g, progs in roll.items():
        if g != 'us' and re.fullmatch(r'[a-z]{2}', g):
            for prog, cl in progs.items():
                st_sum[prog][0] += int(cl['all']['all'][4]); st_sum[prog][1] += cl['all']['all'][5]
    blank_state = defaultdict(int)
    for (prog, state, county, fy, classes), v in agg.items():
        if not state:
            blank_state[prog] += int(v[4])
    states_vs_us = {}
    for prog, v in st_sum.items():
        us_n = int(roll['us'][prog]['all']['all'][4])
        states_vs_us[prog] = {'sum_of_states_loans': v[0], 'us_loans': us_n, 'difference': us_n - v[0],
                              'loans_with_blank_project_state': blank_state[prog],
                              'explained_by': 'loans with a blank ProjectState, which count in us only',
                              'explained': us_n - v[0] == blank_state[prog]}
    jdump({'about': 'Register totals against the raw files. The raw recount is taken row by row during the read; the independent re-derivation in docs/web-fsc-5/gates/ does not import this script.',
           'us_by_program_fy': rec, 'states_vs_us': states_vs_us, 'all_match': all(r['match'] for r in rec)},
          os.path.join(DATA, 'reconciliation.json'))
    if not all(r['match'] for r in rec) or not all(v['explained'] for v in states_vs_us.values()):
        raise BuildError('FOIA reconciliation failed: see data/markets/reconciliation.json')
    return {'states_vs_us': states_vs_us}


# ---------------------------------------------------------------- bundles

def write_bundles(geo):
    series_dir = os.path.join(DATA, 'series')
    sfiles = sorted(f for f in os.listdir(series_dir) if f.endswith('.json')) if os.path.isdir(series_dir) else []
    loaded = {f[:-5]: jload(os.path.join(series_dir, f)) for f in sfiles}
    bdir = os.path.join(DATA, 'geo')
    want = set()
    for m in geo['markets']:
        mid = market_id(m)
        b = {'id': mid, 'market': m, 'series': {}}
        for sid, s in loaded.items():
            if mid in s['values']:
                v = s['values'][mid]
                b['series'][sid] = {c: {w: x for w, x in cv.items() if w != 'by_fy'} if isinstance(cv, dict) and 'by_fy' in cv else cv for c, cv in v.items()}
            elif mid in s.get('nulls', {}):
                b['series'][sid] = {'v': None, 'f': s['nulls'][mid]}
            for cid in [k for k in s['values'] if k.startswith(mid + ':')]:
                if cid in s['values']:
                    v = s['values'][cid]
                    b.setdefault('components', {}).setdefault(cid, {})[sid] = {c: {w: x for w, x in cv.items() if w != 'by_fy'} if isinstance(cv, dict) and 'by_fy' in cv else cv for c, cv in v.items()}
        p = os.path.join(bdir, m['state'], f'{m["slug"]}.json')
        jdump(b, p, compact=True)
        want.add(os.path.relpath(p, bdir))
    for st in geo['states']:
        if not st.get('site_markets'):
            continue
        sid = st['id']
        b = {'id': sid, 'state': st, 'series': {}}
        for k, s in loaded.items():
            if sid in s['values']:
                v = s['values'][sid]
                b['series'][k] = {c: {w: x for w, x in cv.items() if w != 'by_fy'} if isinstance(cv, dict) and 'by_fy' in cv else cv for c, cv in v.items()}
        p = os.path.join(bdir, 'states', f'{sid}.json')
        jdump(b, p, compact=True)
        want.add(os.path.relpath(p, bdir))
    for d, _, fs in os.walk(bdir):
        for f in fs:
            rel = os.path.relpath(os.path.join(d, f), bdir)
            if rel not in want:
                os.remove(os.path.join(d, f))


# ---------------------------------------------------------------- diff

def snapshot_values():
    out = {}
    sdir = os.path.join(DATA, 'series')
    if not os.path.isdir(sdir):
        return out
    for f in sorted(os.listdir(sdir)):
        if not f.endswith('.json'):
            continue
        s = jload(os.path.join(sdir, f))
        for g, cl in s['values'].items():
            for c, wv in cl.items():
                if isinstance(wv, dict) and 'by_fy' not in wv:
                    out[(f[:-5], g, c)] = wv.get('v')
                    continue
                for w, v in wv.items():
                    if w != 'by_fy':
                        out[(f[:-5], g, c, w)] = v
    return out


def print_diff(old, new):
    keys = sorted(set(old or {}) | set(new), key=str)
    changed = [(k, (old or {}).get(k), new.get(k)) for k in keys if (old or {}).get(k) != new.get(k)]
    for k, a, b in changed[:2000]:
        print('changed', '.'.join(map(str, k)), a, '->', b)
    print(f'{len(changed)} value(s) changed')


def main(argv):
    try:
        build(diff='--diff' in argv)
    except BuildError as e:
        print('BUILD FAILED:', e, file=sys.stderr)
        return 1
    print('build complete')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
