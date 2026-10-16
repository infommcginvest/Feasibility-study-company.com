#!/usr/bin/env python3
"""Readers for the keyed federal sources of the markets register: the Census
Data API (geoinfo roster, ACS, CBP, PEP, 2020 Connecticut towns) and the BEA
API (CAINC1). Imported by scripts/markets_build.py and the assembler; it reads
the raw files under _cache/markets/raw/ and returns plain dicts. Nothing here
fetches.

Census Data API responses are JSON arrays whose first row is the header. ACS
marks a value it cannot publish with a negative sentinel; every sentinel
becomes a null with its meaning as the flag, never a number:
"""
import json
import math
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, '_cache', 'markets', 'raw')

ACS_SENTINELS = {
    '-666666666': 'no-estimate (too few sample observations or not applicable)',
    '-999999999': 'no-estimate (too few sample observations; MOE not computable)',
    '-888888888': 'not-applicable (MOE not appropriate)',
    '-222222222': 'moe-not-computable (too few sample observations)',
    '-333333333': 'median-in-open-ended-interval',
    '-555555555': 'moe-not-applicable (controlled estimate)',
}

CBSA = 'metropolitan statistical area/micropolitan statistical area'


def rows(path):
    """A Census Data API file as a list of dicts; an empty file (HTTP 204, no rows) is []."""
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return []
    data = json.load(open(path, encoding='utf-8'))
    return [dict(zip(data[0], r)) for r in data[1:]]


def src_dir(source, vintage):
    return os.path.join(RAW, source, re.sub(r'[^A-Za-z0-9_.-]', '_', vintage))


# ---------------------------------------------------------------- roster

def roster(vintage='2025'):
    """States, counties, CBSAs with their member counties, places and county
    subdivisions, from the geoinfo files (OMB Bulletin 23-01 delineation)."""
    d = src_dir('census_geoinfo', vintage)
    if not os.path.exists(os.path.join(d, 'state.json')):
        return None
    states = {r['state']: r['NAME'] for r in rows(os.path.join(d, 'state.json'))}
    counties = {r['state'] + r['county']: r['NAME'] for r in rows(os.path.join(d, 'county.json'))}
    cbsas = {}
    for r in rows(os.path.join(d, 'cbsa.json')):
        name = r['NAME']
        cbsas[r[CBSA]] = {'name': name, 'type': 'metro' if name.endswith('Metro Area') else ('micro' if name.endswith('Micro Area') else 'other'),
                          'counties': []}
    for f in sorted(os.listdir(d)):
        m = re.fullmatch(r'cbsa_county_(\d{5})_(\d{2})\.json', f)
        if m:
            for r in rows(os.path.join(d, f)):
                cbsas[m.group(1)]['counties'].append(r['state (or part)'] + r['county'])
    for c in cbsas.values():
        c['counties'] = sorted(set(c['counties']))
    places = {r['state'] + r['place']: r['NAME'] for r in rows(os.path.join(d, 'place.json'))}
    cousubs = {}
    for f in sorted(os.listdir(d)):
        if re.fullmatch(r'cousub_\d{2}\.json', f):
            for r in rows(os.path.join(d, f)):
                cousubs[r['state'] + r['county'] + r['county subdivision']] = r['NAME']
    county_cbsa = {}
    for code, c in cbsas.items():
        for fips in c['counties']:
            county_cbsa[fips] = code
    return {'states': states, 'counties': counties, 'cbsas': cbsas, 'places': places, 'cousubs': cousubs,
            'county_cbsa': county_cbsa, 'dir': d}


def ct_legacy_towns(vintage='2020'):
    """{cousub code (5 digits): legacy county FIPS} from the 2020 Census (dec/pl),
    which still used Connecticut's eight counties."""
    p = os.path.join(src_dir('census_dec2020_ct', vintage), 'ct_cousub_2020.json')
    out = {}
    for r in rows(p):
        if r['county subdivision'] != '00000':
            out[r['county subdivision']] = {'county': '09' + r['county'], 'name': r['NAME'], 'pop2020': int(r['P1_001N'])}
    return out


# ---------------------------------------------------------------- ACS

ACS_VARS = {
    'pop': ['B01003_001'],
    'households': ['B11001_001'],
    'median_hh_income': ['B19013_001'],
    'per_capita_income': ['B19301_001'],
    'aggregate_income': ['B19313_001'],
    'pop65': [f'B01001_{i:03d}' for i in list(range(20, 26)) + list(range(44, 50))],
    'occupied_units': ['B25003_001'],
    'owner_occupied': ['B25003_002'],
    'renter_occupied': ['B25003_003'],
    'median_gross_rent': ['B25064_001'],
    'median_home_value': ['B25077_001'],
    'labor_force': ['B23025_003'],
    'unemployed': ['B23025_005'],
}
ACS_MEDIANS = {'median_hh_income', 'median_gross_rent', 'median_home_value'}


def acs_cell(row, var):
    """(estimate, moe, flag) for one ACS variable in one row."""
    e, m = row.get(var + 'E'), row.get(var + 'M')
    if e is None or e in ACS_SENTINELS or e == '':
        return None, None, ACS_SENTINELS.get(e, 'not-published')
    est = float(e)
    moe, flag = None, None
    if m in ACS_SENTINELS:
        flag = ACS_SENTINELS[m]
    elif m not in (None, ''):
        moe = float(m)
        if moe < 0:
            moe, flag = None, f'moe-sentinel {m}'
    return est, moe, flag


def acs_measures(row):
    """Every register measure for one ACS row: {measure: (estimate, moe, flag)}.
    pop65 sums twelve cells; its MOE is the root sum of squares (Census's
    approximation), flagged as such."""
    out = {}
    for k, vars_ in ACS_VARS.items():
        cells = [acs_cell(row, v) for v in vars_]
        if any(c[0] is None for c in cells):
            out[k] = (None, None, next(c[2] for c in cells if c[0] is None))
        elif len(cells) == 1:
            out[k] = cells[0]
        else:
            moes = [c[1] for c in cells]
            moe = math.sqrt(sum(x * x for x in moes)) if all(x is not None for x in moes) else None
            out[k] = (sum(c[0] for c in cells), moe, 'moe-approximated (root sum of squares of component MOEs)')
    return out


def acs_table(source, vintage, level):
    """{geo key: {measure: (est, moe, flag)}} for one ACS level (us, state, county,
    cbsa, place, cousub). Group a and b files are joined on their geo columns."""
    d = src_dir(source, vintage)
    merged = {}
    files = sorted(f for f in os.listdir(d) if re.fullmatch(rf'{level}(_\d{{2}})?_[ab]\.json', f)) if os.path.isdir(d) else []
    for f in files:
        for r in rows(os.path.join(d, f)):
            key = geo_key(level, r)
            merged.setdefault(key, {}).update(r)
    return {k: acs_measures(r) for k, r in merged.items()}


def geo_key(level, r):
    if level == 'us':
        return 'us'
    if level == 'state':
        return r['state']
    if level == 'county':
        return r['state'] + r['county']
    if level == 'cbsa':
        return r[CBSA]
    if level == 'place':
        return r['state'] + r['place']
    if level == 'cousub':
        return r['state'] + r['county'] + r['county subdivision']
    raise ValueError(level)


# ---------------------------------------------------------------- PEP

def pep_table(vintage='V2023'):
    """{geo key: {year: population}} from pep/charv (July 1 estimates; April 1, 2020 base as '2020-04')."""
    d = src_dir('census_pep_api', vintage)
    out = {}
    for level in ('us', 'state', 'county', 'cbsa'):
        for r in rows(os.path.join(d, f'{level}.json')):
            key = ('cbsa:' if level == 'cbsa' else '') + geo_key(level, r)
            yr = r['YEAR'] if r['MONTH'] == '7' else f'{r["YEAR"]}-0{r["MONTH"]}'
            out.setdefault(key, {})[yr] = int(r['POP'])
    return out


# ---------------------------------------------------------------- CBP

def cbp_table(vintage='2023'):
    """{(level, key, naics): (estab, emp, emp_noise_flag)} from the all-industry
    responses (NAICS2017=*): us_all.json, state_all.json, cbsa_all.json and
    county_<state>.json. Codes are as the API writes them, 2 to 6 digits or one of
    the sector ranges 31-33, 44-45 and 48-49, so parents ('4471', '44-45') sit
    beside their 6-digit children ('447110'); a county code
    999 is the statewide records. Returns (table, levels)."""
    d = src_dir('census_cbp', vintage)
    out, levels = {}, set()
    if not os.path.isdir(d):
        return out, []
    for f in sorted(os.listdir(d)):
        m = re.fullmatch(r'(us|state|cbsa)_all\.json|county_(\d{2})\.json', f)
        if not m:
            continue
        level = m.group(1) or 'county'
        levels.add(level)
        for r in rows(os.path.join(d, f)):
            code = r['NAICS2017']
            if not re.fullmatch(r'\d{2,6}|31-33|44-45|48-49', code):   # three sectors are published only as ranges (D51)
                continue
            out[(level, geo_key(level, r), code)] = (int(r['ESTAB']), int(r['EMP']), r.get('EMP_N'))
    return out, sorted(levels)


# ---------------------------------------------------------------- BEA

def bea_table(vintage='2024'):
    """{(geofips, line): {year: (value, flag)}} from CAINC1 (line 1 personal income,
    thousands of dollars; 2 population; 3 per capita personal income, dollars).
    (D), (NA) and the like, in DataValue or in NoteRef (where BEA pairs them with a
    DataValue of 0), become nulls with the code as the flag."""
    d = src_dir('bea_cainc1_api', vintage)
    out, names = {}, {}
    if not os.path.isdir(d):
        return out, names
    for f in sorted(os.listdir(d)):
        m = re.fullmatch(r'cainc1_(county|state|msa)_line(\d)\.json', f)
        if not m:
            continue
        j = json.load(open(os.path.join(d, f), encoding='utf-8'))
        res = j['BEAAPI'].get('Results') or {}
        if 'Error' in j['BEAAPI'] or 'Error' in res:
            continue
        mult = None
        for r in res.get('Data', []):
            v = r['DataValue'].replace(',', '').strip()
            mult = int(r.get('UNIT_MULT') or 0)
            code = re.search(r'\(([A-Z]+)\)', r.get('NoteRef') or '')
            if code:
                # BEA writes a value it does not publish as DataValue "0" with the code in
                # NoteRef, e.g. "(NA) *" for Connecticut's legacy counties from 2024: a null, never a zero
                val = (None, f'bea-({code.group(1)})')
            else:
                val = (float(v) * (10 ** mult), None) if re.fullmatch(r'-?\d+(\.\d+)?', v) else (None, f'bea-{v}')
            # keyed by the file's level as well: a state's GeoFips (e.g. 32000, Nevada) can equal a CBSA code
            lvl = {'county': 'co', 'state': 'st', 'msa': 'msa'}[m.group(1)]
            out.setdefault((f'{lvl}:{r["GeoFips"]}', m.group(2)), {})[r['TimePeriod']] = val
            names[f'{lvl}:{r["GeoFips"]}'] = r['GeoName']
    return out, names


# ---------------------------------------------------------------- series

ACS_UNITS = {'pop': 'people', 'households': 'households', 'median_hh_income': 'USD', 'per_capita_income': 'USD',
             'aggregate_income': 'USD', 'pop65': 'people', 'occupied_units': 'housing units', 'owner_occupied': 'housing units',
             'renter_occupied': 'housing units', 'median_gross_rent': 'USD', 'median_home_value': 'USD',
             'labor_force': 'people', 'unemployed': 'people'}
ACS_LABELS = {'pop': 'Total population (B01003)', 'households': 'Households (B11001)', 'median_hh_income': 'Median household income, inflation-adjusted dollars (B19013)',
              'per_capita_income': 'Per capita income, inflation-adjusted dollars (B19301; for a set of areas, B19313 aggregate income over B01003 population)',
              'aggregate_income': 'Aggregate household income (B19313)', 'pop65': 'Population 65 and over (B01001, twelve age cells summed)',
              'occupied_units': 'Occupied housing units (B25003)', 'owner_occupied': 'Owner-occupied housing units (B25003)',
              'renter_occupied': 'Renter-occupied housing units (B25003)', 'median_gross_rent': 'Median gross rent, dollars (B25064)',
              'median_home_value': 'Median value, owner-occupied units, dollars (B25077)', 'labor_force': 'Civilian labor force (B23025)',
              'unemployed': 'Unemployed, civilian labor force (B23025)'}


def cell(est, moe=None, flag=None, note=None):
    c = {'v': None if est is None else (int(est) if float(est).is_integer() else round(est, 4))}
    if moe is not None:
        c['moe'] = int(moe) if float(moe).is_integer() else round(moe, 2)
    if flag:
        c['f'] = flag
    if note:
        c['note'] = note
    return c


def sum_cells(parts):
    """Sum additive ACS (est, moe, flag) triples: MOE as the root sum of squares
    (Census's approximation for sums), null if any part is null."""
    if not parts or any(p is None or p[0] is None for p in parts):
        missing = [p[2] if p else 'not-published' for p in parts if p is None or p[0] is None]
        return cell(None, flag='component-null: ' + (missing[0] if missing else 'no components'))
    est = sum(p[0] for p in parts)
    moes = [p[1] for p in parts]
    moe = math.sqrt(sum(m * m for m in moes)) if all(m is not None for m in moes) else None
    return cell(est, moe, note='sum of components; MOE approximated as the root sum of squares' if len(parts) > 1 else None)


def ratio_cell(num, den, flag_prefix=''):
    if num is None or den in (None, 0):
        return {'v': None, 'f': 'no-denominator'}
    return {'v': round(num / den, 6), 'num': num if not float(num).is_integer() else int(num), 'den': den if not float(den).is_integer() else int(den)}


def market_parts(m):
    """How a market composes Census figures: ('cbsa', code), ('counties', [fips]),
    ('places', [geoid]), ('ct-towns', [cousub geoids]) or ('none', reason)."""
    src, r = m.get('composition_source'), m.get('resolved') or {}
    if r.get('unresolved'):
        return 'none', 'composition-unresolved: ' + '; '.join(r['unresolved'])
    if src == 'cbsa-delineation' and r.get('cbsa'):
        return 'cbsa', r['cbsa']
    if src in ('cbsa-union', 'judgement-region', 'single-county', 'page-named-counties') and r.get('counties'):
        return 'counties', r['counties']
    if src == 'sub-county':
        if r.get('places') and not r.get('cousubs'):
            return 'places', r['places']
        if r.get('cousubs') and not r.get('places'):
            return 'ct-towns', r['cousubs']        # county subdivisions (New England towns)
        if r.get('places') or r.get('cousubs'):
            return 'none', 'mixed places and towns: not composed'
        return 'none', 'not-published-at-this-grain: tracts were not fetched'
    if src == 'connecticut-two-schemes':
        if r.get('ct_fit_planning') == 'exact' and r.get('ct_planning_regions'):
            return 'counties', r['ct_planning_regions']        # planning regions are Census county equivalents
        if r.get('ct_fit_legacy') == 'exact' and r.get('ct_legacy_towns'):
            return 'ct-towns', r['ct_legacy_towns']
        return 'none', 'ct-no-exact-scheme'
    return 'none', 'composition-pending: no federal composition for this market'


def _ids(geo):
    st = {s['fips']: s['id'] for s in geo['states'] if s.get('fips')}
    return st


def build_census(geo, nmap):
    """Every keyed Census and BEA series as {series id: series dict}. Returns
    ({}, reasons) entries for sources with no raw files."""
    ros = roster()
    if not ros:
        return {}, {}
    st_id = _ids(geo)
    markets = {f'{m["state"]}/{m["slug"]}': m for m in geo['markets']}
    parts = {mid: market_parts(m) for mid, m in markets.items()}
    out, stats = {}, {}

    # ---- ACS 5-year and 1-year
    for source, vintage, prefix, period in (('census_acs5', '2024 5-year', 'acs5', '2020-2024 (ACS 5-year)'), ('census_acs1', '2024 1-year', 'acs1', '2024 (ACS 1-year)')):
        if not os.path.isdir(src_dir(source, vintage)):
            continue
        t = {lv: acs_table(source, vintage, lv) for lv in ('us', 'state', 'county', 'cbsa', 'place', 'cousub')}
        base = {}
        if 'us' in t['us']:
            base['us'] = t['us']['us']
        base.update({st_id[k]: v for k, v in t['state'].items() if k in st_id})
        base.update({f'co-{k}': v for k, v in t['county'].items() if k in ros['counties']})
        base.update({f'cbsa-{k}': v for k, v in t['cbsa'].items() if k in ros['cbsas']})
        mvals, nulls = {}, {}
        for mid, (how, what) in parts.items():
            if how == 'cbsa':
                if what in t['cbsa']:
                    mvals[mid] = {'single': t['cbsa'][what]}
                else:
                    nulls[mid] = f'not-published: the {period} tables carry no figure for CBSA {what}'
            elif how in ('counties', 'places', 'ct-towns'):
                tab = t['county'] if how == 'counties' else (t['place'] if how == 'places' else t['cousub'])
                comps = [tab.get(x) for x in what]
                if any(c is None for c in comps):
                    nulls[mid] = f'not-published: {sum(c is None for c in comps)} of {len(comps)} components have no {period} figure' + (' (1-year covers areas of 65,000 or more)' if prefix == 'acs1' else '')
                elif len(comps) == 1:
                    mvals[mid] = {'single': comps[0]}
                else:
                    mvals[mid] = {'set': comps, 'ids': what, 'kind': how}
            else:
                nulls[mid] = what
        for meas in ACS_VARS:
            sid = f'{prefix}_{meas}'
            vals = {g: {'all': cell(*row[meas][:2], flag=row[meas][2] if row[meas][0] is None else None,
                                    note=row[meas][2] if row[meas][0] is not None and row[meas][2] else None)} for g, row in base.items()}
            mnull = dict(nulls)
            for mid, mv in mvals.items():
                if 'single' in mv:
                    r = mv['single'][meas]
                    vals[mid] = {'all': cell(r[0], r[1], flag=r[2] if r[0] is None else None, note=r[2] if r[0] is not None and r[2] else None)}
                elif meas in ACS_MEDIANS:
                    comp = {f'{"co" if mv["kind"] == "counties" else ("pl" if mv["kind"] == "places" else "cs")}-{i}': (c[meas][0] if c[meas][0] is not None else None)
                            for i, c in zip(mv['ids'], mv['set'])}
                    vals[mid] = {'all': {'v': None, 'f': 'median-not-aggregated: a median of several areas is not the average of their medians; see components', 'components': comp}}
                elif meas == 'per_capita_income':
                    num = [c['aggregate_income'][0] for c in mv['set']]
                    den = [c['pop'][0] for c in mv['set']]
                    vals[mid] = {'all': ratio_cell(sum(num), sum(den)) if all(x is not None for x in num + den) else {'v': None, 'f': 'component-null'}}
                else:
                    vals[mid] = {'all': sum_cells([c[meas] for c in mv['set']])}
            agg = 'median: published areas only; never aggregated' if meas in ACS_MEDIANS else (
                'ratio of summed numerator and denominator' if meas == 'per_capita_income' else 'sum')
            out[sid] = {'id': sid, 'source': source, 'unit': ACS_UNITS[meas], 'label': ACS_LABELS[meas] + f', {period}',
                        'aggregation': agg, 'vintage': vintage, 'period': period, 'values': vals, 'nulls': mnull}
        # unemployment rate: unemployed / civilian labor force, from the sums
        sid = f'{prefix}_unemployment_rate'
        vals = {}
        for g, row in base.items():
            u, lf = row['unemployed'][0], row['labor_force'][0]
            vals[g] = {'all': ratio_cell(u, lf) if u is not None else {'v': None, 'f': 'component-null'}}
        for mid, mv in mvals.items():
            rows_ = [mv['single']] if 'single' in mv else mv['set']
            u = [r['unemployed'][0] for r in rows_]; lf = [r['labor_force'][0] for r in rows_]
            vals[mid] = {'all': ratio_cell(sum(u), sum(lf)) if all(x is not None for x in u + lf) else {'v': None, 'f': 'component-null'}}
        out[sid] = {'id': sid, 'source': source, 'unit': 'share', 'label': f'Unemployment rate: unemployed over civilian labor force (B23025), {period}',
                    'aggregation': 'ratio of summed numerator and denominator', 'vintage': vintage, 'period': period, 'values': vals, 'nulls': dict(nulls)}
        stats[source] = {'base_geos': len(base), 'markets_with_values': len(mvals), 'markets_null': len(nulls)}

    # ---- PEP Vintage 2023, through the Census Data API (www2.census.gov is closed: D50)
    pep, pv, psrc = (pep_table(), 'V2023', 'census_pep_api') if os.path.isdir(src_dir('census_pep_api', 'V2023')) else ({}, None, None)
    if pep:
        last = max(int(y) for y in next(iter(pep.values())) if y.isdigit())
        base = {}
        if 'us' in pep:
            base['us'] = pep['us']
        base.update({st_id[k]: v for k, v in pep.items() if k in st_id})
        base.update({f'co-{k}': v for k, v in pep.items() if k in ros['counties']})
        base.update({f'cbsa-{k[5:]}': v for k, v in pep.items() if k.startswith('cbsa:') and k[5:] in ros['cbsas']})
        mv, nulls = {}, {}
        for mid, (how, what) in parts.items():
            if how == 'cbsa':
                if 'cbsa:' + what in pep:
                    mv[mid] = pep['cbsa:' + what]
                else:
                    nulls[mid] = f'not-published: PEP {pv} has no row for CBSA {what}'
            elif how == 'counties':
                comps = [pep.get(f) for f in what]
                if any(c is None for c in comps):
                    nulls[mid] = f'not-published: a component county has no PEP {pv} row'
                else:
                    mv[mid] = {y: sum(c[y] for c in comps) for y in comps[0]}
            elif how in ('places', 'ct-towns'):
                nulls[mid] = 'not-published-at-this-grain: the PEP files used cover nation, states, counties and CBSAs'
            else:
                nulls[mid] = what
        allv = {**base, **mv}
        first = 2020
        span = last - first
        lab = f'Vintage {pv[1:]} Population Estimates'
        defs = {f'pep_pop_{last}': ('people', f'Resident population, July 1, {last}', lambda y: y.get(str(last))),
                f'pep_pop_{last - 1}': ('people', f'Resident population, July 1, {last - 1}', lambda y: y.get(str(last - 1))),
                'pep_pop_2023': ('people', 'Resident population, July 1, 2023 (the year of CBP 2023)', lambda y: y.get('2023')),
                f'pep_pop_{first}': ('people', f'Resident population, July 1, {first}', lambda y: y.get(str(first))),
                'pep_change_1y': ('people', f'Population change, July 1, {last - 1} to July 1, {last}', lambda y: y[str(last)] - y[str(last - 1)]),
                f'pep_change_{span}y': ('people', f'Population change, July 1, {first} to July 1, {last}', lambda y: y[str(last)] - y[str(first)])}
        for sid, (unit, l_, fn) in defs.items():
            out[sid] = {'id': sid, 'source': psrc, 'unit': unit, 'label': f'{l_}, {lab}', 'aggregation': 'sum',
                        'vintage': pv, 'period': f'July 1, {first} to July 1, {last}', 'values': {g: {'all': fn(y)} for g, y in allv.items()}, 'nulls': dict(nulls)}
        for sid, (a, b, l_) in {'pep_change_1y_pct': (str(last), str(last - 1), f'Population change, {last - 1} to {last}, share of {last - 1}'),
                                f'pep_change_{span}y_pct': (str(last), str(first), f'Population change, {first} to {last}, share of {first}')}.items():
            out[sid] = {'id': sid, 'source': psrc, 'unit': 'share', 'label': f'{l_}, {lab}',
                        'aggregation': 'ratio of summed numerator and denominator', 'vintage': pv, 'period': f'July 1, {first} to July 1, {last}',
                        'values': {g: {'all': ratio_cell(y[a] - y[b], y[b])} for g, y in allv.items()}, 'nulls': dict(nulls)}
        stats[psrc] = {'vintage': pv, 'base_geos': len(base), 'markets_with_values': len(mv), 'markets_null': len(nulls)}

    # ---- CBP 2023 by asset class, through the Census Data API with every industry code per
    # request, parents included (www2.census.gov is closed: D50)
    cbp, levels = cbp_table()
    cbp_src = 'census_cbp'
    if cbp:
        # Which NAICS edition does the file use? Count the codes that exist in only one
        # edition (charter trap 5: CBP 2023 still carries NAICS 2017 codes such as 447110).
        present = {k[2] for k in cbp}
        only22 = {c for r in nmap['classes'] for c in r['naics2022'] if c not in (r.get('legacy') or {}).get('2017', [])}
        only17 = {c for r in nmap['classes'] for c in (r.get('legacy') or {}).get('2017', []) if c not in r['naics2022']}
        n22, n17 = len(only22 & present), len(only17 & present)
        edition = '2022' if n22 >= n17 else '2017'
        classes = [(r['slug'], r['naics2022'] if edition == '2022' else (r.get('legacy') or {}).get('2017', r['naics2022'])) for r in nmap['classes']]
        all_codes = {c for _, codes in classes for c in codes}
        seen = {(lv, c) for lv in levels for c in all_codes}   # every response lists every industry
        stats['cbp_naics_edition'] = {'edition': edition, 'edition_only_codes_found': {'2022': n22, '2017': n17}}
        geos = {'us': ('us', 'us')}
        geos.update({st_id[k]: ('state', k) for k in st_id})
        geos.update({f'co-{f}': ('county', f) for f in ros['counties']})
        geos.update({f'cbsa-{c}': ('cbsa', c) for c in ros['cbsas']})

        idx = cbp_child_index(cbp)
        def at(level, key, codes):
            if any((level, c) not in seen for c in codes):
                return None, None, 0, []
            e = [cbp.get((level, key, c), (0, 0, None)) for c in codes]
            w, parents = cbp_withheld(cbp, level, key, codes, idx) if idx is not None else (0, [])
            return sum(x[0] for x in e), sum(x[1] for x in e), w, parents

        def put(store_e, store_m, g, slug, a, b, w, parents):
            store_e.setdefault(g, {})
            store_m.setdefault(g, {})
            if w:
                store_e[g][slug] = [a, w]          # [lower bound, up to this many withheld]: flag cbp-cells-withheld
                store_m[g][slug] = [b, w]
            elif a is None:
                store_e[g][slug] = {'v': None, 'f': 'not-fetched'}
                store_m[g][slug] = {'v': None, 'f': 'not-fetched'}
            elif a != 0:                       # a class absent with nothing withheld is zero (absent_class_is_zero)
                store_e[g][slug] = a
                store_m[g][slug] = b
        # A geography with no row at all in its response is not published, never a zero
        # (absent_class_is_zero holds only inside a published geography). The CBP API
        # carries no Puerto Rico metro areas and no row for two counties (D51).
        pub = {(lv, k) for (lv, k, _c) in cbp}
        unpub = {'cbsa': 'not-published: the CBP 2023 API response (cbsa_all.json) has no row for this metro area; it carries no Puerto Rico metro areas',
                 'county': 'not-published: the CBP 2023 API response (county_<state>.json) has no row for this county'}
        est, emp, nulls = {}, {}, {}
        for g, (level, key) in geos.items():
            if (level, key) not in pub:
                nulls[g] = unpub.get(level, 'not-published: no row in the CBP 2023 API response')
                continue
            for slug, codes in classes:
                if codes:
                    put(est, emp, g, slug, *at(level, key, codes))
        for mid, (how, what) in parts.items():
            if how == 'cbsa' and ('cbsa', what) not in pub:
                nulls[mid] = unpub['cbsa']
                continue
            if how == 'counties' and any(('county', f) not in pub for f in what):
                nulls[mid] = unpub['county'] + ' (' + ', '.join(f for f in what if ('county', f) not in pub) + ')'
                continue
            for slug, codes in classes:
                if not codes:
                    continue
                if how == 'cbsa':
                    a, b, w, parents = at('cbsa', what, codes)
                elif how == 'counties':
                    vals = [at('county', f, codes) for f in what]
                    a = None if any(v[0] is None for v in vals) else sum(v[0] for v in vals)
                    b = None if any(v[1] is None for v in vals) else sum(v[1] for v in vals)
                    w = sum(v[2] for v in vals)
                    parents = sorted({p for v in vals for p in v[3]})
                else:
                    nulls[mid] = what if how == 'none' else 'not-published-at-this-grain: CBP covers nation, states, counties and metro areas'
                    break
                put(est, emp, mid, slug, a, b, w, parents)
        if any(k[0] == 'county' and k[1].endswith('999') for k in cbp):
            out['_cbp_statewide'] = {f'{st_id[f]}|{slug}': sum(cbp.get(('county', f + '999', c), (0, 0, None))[0] for c in codes)
                                     for f in st_id for slug, codes in classes if codes}
        pop = out.get('pep_pop_2023', {}).get('values', {})
        per = {}
        for g, cl in est.items():
            p = (pop.get(g) or {}).get('all')
            per[g] = {}
            for s_, v in cl.items():
                val = v[0] if isinstance(v, list) else (v.get('v') if isinstance(v, dict) else v)
                x = round(val * 10000 / p, 2) if (val is not None and p) else None
                per[g][s_] = [x, v[1]] if isinstance(v, list) else ({'v': None, 'f': v.get('f')} if isinstance(v, dict) else x)
        meta = {'source': cbp_src, 'vintage': '2023', 'period': 'week of March 12, 2023',
                'absent_class_is_zero': True,
                'flags': {'cbp-cells-withheld': ('CBP does not publish every 6-digit cell at county and metro level (charter trap 3). A class code with no 6-digit cell at the geography '
                                                 'may hold establishments its published parent industry shows: up_to is the parent\'s establishments less its published 6-digit children, summed over '
                                                 'the class\'s absent codes; the parent of a code in sectors 31-33, 44-45 and 48-49 is the sector range the API publishes. Such a cell is written '
                                                 '[value, up_to]: the value is a lower bound in the series\' own unit; up_to is always a count of ESTABLISHMENTS that may be withheld, in cbp_emp '
                                                 'and cbp_estab_per_10k as well (it does not bound employees or the rate). scripts/markets.py prints only the value, only with allow_flag, '
                                                 'and the page must say "at least".')},
                'up_to_unit': 'establishments',
                'naics_edition_in_file': edition,
                'naics_edition_note': (f'The CBP files carry NAICS {edition} codes ({n17} codes that exist only in NAICS 2017 found, {n22} only in NAICS 2022), '
                                       f'so each class sums its NAICS {edition} code list from naics-map.json.'),
                'classes_note': ('Each class sums its codes of the NAICS edition the file uses (naics-map.json). Classes are not mutually exclusive; never sum across classes. '
                                 'A class absent from a geography that is in values has zero establishments there: CBP lists every industry cell that has an establishment, '
                                 'so absent cells are true zeros and are left out to keep the file small.')}
        out['cbp_estab'] = {'id': 'cbp_estab', 'unit': 'establishments', 'label': 'Establishments, County Business Patterns 2023', 'aggregation': 'sum', **meta,
                            'values': est, 'nulls': dict(nulls)}
        out['cbp_emp'] = {'id': 'cbp_emp', 'unit': 'employees', 'label': 'Paid employees, pay period including March 12, County Business Patterns 2023 (noise-infused; EMP_N per code in the raw files)',
                          'aggregation': 'sum', **meta, 'values': emp, 'nulls': dict(nulls)}
        out['cbp_estab_per_10k'] = {'id': 'cbp_estab_per_10k', 'unit': 'per 10,000 residents', 'label': f'Establishments per 10,000 residents: CBP 2023 establishments over the PEP {pv} estimate for July 1, 2023',
                                    'aggregation': 'ratio of summed numerator and denominator', 'numerator': 'cbp_estab', 'denominator': 'pep_pop_2023', **meta,
                                    'values': per, 'nulls': dict(nulls)}
        stats[cbp_src] = {'codes': len({c for _, c in seen}), 'geos': len(est)}

    # ---- BEA CAINC1, latest year
    bea, names = bea_table()
    if bea:
        year = max(y for v in bea.values() for y in v)
        def b(gf, line):
            v = bea.get((gf, line), {}).get(year)
            return v if v else (None, 'bea-not-in-table')
        geos = {'us': 'st:00000'}
        geos.update({st_id[k]: f'st:{k}000' for k in st_id})
        geos.update({f'co-{f}': f'co:{f}' for f in ros['counties']})
        geos.update({f'cbsa-{c}': f'msa:{c}' for c in ros['cbsas']})
        pi, popb, pc = {}, {}, {}
        for g, gf in geos.items():
            if (gf, '1') not in bea:
                continue
            a, c_ = b(gf, '1'), b(gf, '2')
            pi[g] = {'all': cell(a[0], flag=a[1])}
            popb[g] = {'all': cell(c_[0], flag=c_[1])}
            p3 = b(gf, '3')
            pc[g] = {'all': cell(p3[0], flag=p3[1])}
        nulls = {}
        for mid, (how, what) in parts.items():
            r_ = markets[mid].get('resolved') or {}
            if how == 'ct-towns' and r_.get('ct_fit_legacy') == 'exact' and all((f'co:{c}', '1') in bea for c in r_.get('ct_legacy_counties', [])):
                # BEA publishes Connecticut's legacy counties as well as its planning regions;
                # a legacy-county market takes its legacy county rows (no join across schemes)
                how, what = 'counties', r_['ct_legacy_counties']
            if how == 'cbsa' and (f'msa:{what}', '1') in bea:
                comps = [f'msa:{what}']
            elif how == 'cbsa':
                comps = [f'co:{f}' for f in geo_cbsa_counties(geo, what)]
            elif how == 'counties':
                comps = [f'co:{f}' for f in what]
            else:
                nulls[mid] = what if how == 'none' else 'not-published-at-this-grain: BEA covers nation, states, counties and metro areas'
                continue
            if any((f, '1') not in bea for f in comps):
                nulls[mid] = 'bea-combination-area: a component county is published by BEA only inside a combined area (e.g. Virginia independent cities)'
                continue
            a = [b(f, '1') for f in comps]; c_ = [b(f, '2') for f in comps]
            if any(x[0] is None for x in a + c_):
                nulls[mid] = 'component-null: ' + next(x[1] for x in a + c_ if x[0] is None)
                continue
            pi[mid] = {'all': cell(sum(x[0] for x in a))}
            popb[mid] = {'all': cell(sum(x[0] for x in c_))}
            if len(comps) == 1:
                p3 = b(comps[0], '3')
                pc[mid] = {'all': cell(p3[0], flag=p3[1])}
            else:
                pc[mid] = {'all': ratio_cell(sum(x[0] for x in a), sum(x[0] for x in c_))}
        meta = {'source': 'bea_cainc1_api', 'vintage': year, 'period': f'calendar year {year}'}
        out['bea_personal_income'] = {'id': 'bea_personal_income', 'unit': 'USD', 'label': f'Personal income, {year} (CAINC1 line 1)', 'aggregation': 'sum', **meta, 'values': pi, 'nulls': dict(nulls)}
        out['bea_population'] = {'id': 'bea_population', 'unit': 'people', 'label': f'Population, BEA midyear, {year} (CAINC1 line 2)', 'aggregation': 'sum', **meta, 'values': popb, 'nulls': dict(nulls)}
        out['bea_per_capita_income'] = {'id': 'bea_per_capita_income', 'unit': 'USD', 'label': f'Per capita personal income, {year} (CAINC1 line 3 for a single area; for a set of areas, summed line 1 over summed line 2)',
                                        'aggregation': 'ratio of summed numerator and denominator', **meta, 'values': pc, 'nulls': dict(nulls)}
        stats['bea_cainc1_api'] = {'year': year, 'geos': len(pi)}
    return out, stats


def geo_cbsa_counties(geo, code):
    for r in geo['cbsas']['rows']:
        if r['code'] == code:
            return r['counties']
    return []


# The API publishes three NAICS sectors only as ranges: their 2-digit parent is '31-33',
# '44-45' or '48-49', never '31', '44' or '48' (found by the independent check, D51).
SECTOR_RANGES = {'31': '31-33', '32': '31-33', '33': '31-33', '44': '44-45', '45': '44-45', '48': '48-49', '49': '48-49'}


def cbp_parents(code):
    """The parent codes of a 6-digit code, nearest first: 5, 4 and 3 digits, then the sector as published."""
    return [code[:n] for n in (5, 4, 3)] + [SECTOR_RANGES.get(code[:2], code[:2])]


def cbp_child_index(cbp):
    """{(level, key, parent): sum of published 6-digit establishments under that parent}."""
    idx = {}
    for (lv, k, c), v in cbp.items():
        if len(c) == 6 and c.isdigit():
            for p in cbp_parents(c):
                idx[(lv, k, p)] = idx.get((lv, k, p), 0) + v[0]
    return idx


def cbp_withheld(cbp, level, key, codes, idx=None):
    """Establishments a geography's published 6-digit cells may leave out: for each
    class code with no 6-digit cell at the geography, its nearest published parent
    (5, then 4 or 3 digits, then the sector as the API publishes it) less the sum of that parent's published 6-digit
    children; that gap bounds what the absent cell could hold. CBP withholds
    some detailed cells at county and metro level (charter trap 3), so an absent
    6-digit cell is not a zero when its parent shows more. Returns (count, parents)."""
    total, parents = 0, []
    absent = [c for c in codes if (level, key, c) not in cbp]     # a published 6-digit cell is complete; only an absent one can hide establishments
    for p in sorted({next((q for q in cbp_parents(c) if (level, key, q) in cbp), None) for c in absent} - {None}):
        children = idx.get((level, key, p), 0) if idx is not None else sum(v[0] for (lv, k, c), v in cbp.items() if lv == level and k == key and len(c) == 6 and c.isdigit() and p in cbp_parents(c))
        gap = cbp[(level, key, p)][0] - children
        if gap > 0:
            total += gap
            parents.append(p)
    return total, parents
