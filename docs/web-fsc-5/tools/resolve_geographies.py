#!/usr/bin/env python3
"""Resolve the market compositions against the federal roster (geoinfo 2025,
OMB Bulletin 23-01), called by assemble_geographies.py once the Census files
are in _cache. Nothing here is typed: state codes, county FIPS, CBSA membership
and place GEOIDs all come from the fetched roster, and every match is by name
within a state, with failures listed, never guessed.

  * postal_to_fips: the USPS codes SBA writes are matched to Census state codes by
    comparing each state's set of county names (no hand table).
  * foia_fips: each FOIA (state, ProjectCounty) string is joined to a 2025 county
    FIPS by normalised name; strings of counties that no longer exist (renamed or
    split) stay unmatched and are listed.
  * markets: a cbsa row takes the federal membership of its CBSA (code checked
    against the roster and its title); a row composed from CBSA membership by a
    composer is compared with the federal union and used as federal when equal,
    else kept as a judgement region with the difference recorded; county rows map
    their names to FIPS; place rows map to place GEOIDs; Connecticut rows keep
    planning-region FIPS and, for the legacy scheme, the towns of each legacy county
    from the 2020 Census (dec/pl, Census Data API), matched to the 2025 roster by town code.
"""
import collections
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import markets_census as mc  # noqa: E402

SUFFIX = re.compile(r'\b(county|parish|borough|census area|city and borough|municipality|municipio|planning region)$', re.I)
ABBREV = {'CT': 'CONNECTICUT', 'VLY': 'VALLEY', 'NW': 'NORTHWEST'}
# Composition corrections whose basis is a named CBSA plus named counties (attacker finding F3).
UNION_OVERRIDES = {
    ('mississippi', 'hattiesburg'): {'cbsa_title_contains': 'Hattiesburg', 'plus_names': ['Jones County', 'Lauderdale County'],
                                     'note': 'the row\'s basis is "Hattiesburg CBSA counties plus Jones and Lauderdale"; the CBSA part now comes from the federal membership, which adds Covington County (attacker finding F3)'},
}


def ascii_upper(s):
    return unicodedata.normalize('NFKD', s).encode('ascii', 'ignore').decode().upper()


def norm_census(name):
    """'Travis County, Texas' -> 'TRAVIS'; 'Fairfax city, Virginia' -> 'FAIRFAXCITY'."""
    base = name.rsplit(',', 1)[0].strip()
    independent_city = base.endswith(' city')
    base = SUFFIX.sub('', base).strip()
    k = ascii_upper(base)
    k = re.sub(r'\bSAINTE\b', 'STE', k)
    k = re.sub(r'\bSAINT\b|\bST\.', 'ST', k)
    k = re.sub(r'[^A-Z]', '', k)
    return k + ('CITY' if independent_city and not k.endswith('CITY') else '')


def norm_foia(s):
    k = ascii_upper(s)
    k = ' '.join(ABBREV.get(w, w) for w in k.split())
    k = re.sub(r'\bSAINTE\b', 'STE', k)
    k = re.sub(r'\bSAINT\b|\bST\.', 'ST', k)
    return re.sub(r'[^A-Z]', '', k)


def postal_to_fips(ros, foia_by_state):
    by_state = collections.defaultdict(set)
    for fips, name in ros['counties'].items():
        by_state[fips[:2]].add(norm_census(name))
    out, report = {}, {}
    for postal, strings in foia_by_state.items():
        if not postal:
            continue
        keys = {norm_foia(s) for s in strings if s}
        scores = sorted(((len(keys & names) / max(1, len(keys)), st) for st, names in by_state.items()), reverse=True)
        best, second = scores[0], scores[1] if len(scores) > 1 else (0, None)
        if best[0] >= 0.5 and best[0] - second[0] >= 0.3:
            out[postal] = best[1]
        report[postal] = {'best': best[1], 'share': round(best[0], 3), 'second': second[1], 'second_share': round(second[0], 3),
                          'assigned': postal in out}
    return out, report


def foia_fips(ros, foia_by_state, p2f):
    idx = collections.defaultdict(dict)
    for fips, name in ros['counties'].items():
        idx[fips[:2]].setdefault(norm_census(name), []).append(fips)
    join, unmatched = {}, []
    for postal, strings in foia_by_state.items():
        st = p2f.get(postal)
        for s in strings:
            k = norm_foia(s)
            hits = idx.get(st, {}).get(k, []) if st else []
            if not hits and st:
                hits = idx[st].get(k + 'CITY', [])   # Virginia independent cities written without CITY (BRISTOL, SALEM)
            if len(hits) == 1:
                join[(postal, s)] = hits[0]
            elif s:
                unmatched.append((postal, s, 'ambiguous' if hits else 'no 2025 county of that name'))
    return join, unmatched


def names_to_fips(ros, st_fips, names):
    idx = {}
    for fips, name in ros['counties'].items():
        if fips[:2] == st_fips:
            idx.setdefault(norm_census(name), []).append(fips)
    out, missing = [], []
    for n in names:
        hits = idx.get(norm_census(n + ', x'), [])
        if len(hits) == 1:
            out.append(hits[0])
        else:
            missing.append(n)
    return out, missing


def place_ids(ros, st_fips, names):
    """Census places by exact name; a New England town that is a county
    subdivision, not a place (Salem town, New Hampshire), falls back to the
    county subdivisions. Returns ([('place'|'cousub', geoid)], missing)."""
    idx = collections.defaultdict(list)
    for gid, name in ros['places'].items():
        if gid[:2] == st_fips:
            idx[ascii_upper(name.rsplit(',', 1)[0])].append(('place', gid))
    cidx = collections.defaultdict(list)
    for gid, name in ros['cousubs'].items():
        if gid[:2] == st_fips:
            cidx[ascii_upper(name.split(',')[0])].append(('cousub', gid))
    out, missing = [], []
    for n in names:
        hits = idx.get(ascii_upper(n), []) or cidx.get(ascii_upper(n), [])
        if len(hits) == 1:
            out.append(hits[0])
        else:
            missing.append(n)
    return out, missing


def resolve(geo, foia_by_state):
    ros = mc.roster()
    if not ros:
        return None
    p2f, preport = postal_to_fips(ros, foia_by_state)
    f2p = {v: k for k, v in p2f.items()}
    join, unmatched = foia_fips(ros, foia_by_state, p2f)
    strings_of = collections.defaultdict(list)
    for (postal, s), fips in join.items():
        strings_of[fips].append({'state': postal, 'string': s})
    # legacy county -> towns, from the 2020 Census (dec/pl, Census Data API): its five-digit town codes
    # are unchanged under the planning regions, so they match the 2025 roster's town GEOIDs by their last five digits
    towns2020 = mc.ct_legacy_towns()
    by_code = collections.defaultdict(list)
    for g in ros['cousubs']:
        if g.startswith('09'):
            by_code[g[-5:]].append(g)
    xwalk = collections.defaultdict(list)
    for code, v in towns2020.items():
        if len(by_code.get(code, [])) == 1:
            xwalk[v['county']].append(by_code[code][0])
    problems = []

    for st in geo['states']:
        st['fips'] = p2f.get(st['postal'])
    for m in geo['markets']:
        key = (m['state'], m['slug'])
        st_fips = p2f.get(m['state_postal'])
        res = {'counties': [], 'places': [], 'cbsa': None, 'ct_legacy_towns': [], 'unresolved': [], 'notes': []}
        src = m['composition_source']
        comp = m['components']
        if src == 'connecticut-two-schemes':
            pr = [c['code'] for c in comp['ct']['planning_regions'] if c['code'] in ros['counties']]
            legacy = [c['code'] for c in comp['ct']['legacy_counties']]
            res['ct_planning_regions'] = pr
            res['ct_legacy_counties'] = legacy
            res['ct_legacy_towns'] = sorted({g for c in legacy for g in xwalk.get(c, []) if g in ros['cousubs']})
            res['ct_fit_planning'] = 'exact' if comp['ct'].get('fit_planning', '').lower().startswith('exact') else 'approximate'
            res['ct_fit_legacy'] = 'exact' if comp['ct'].get('fit_legacy', '').lower().startswith('exact') else 'approximate'
            if len(pr) != len(comp['ct']['planning_regions']):
                res['unresolved'].append('a planning-region code is not in the 2025 roster')
        elif src == 'sub-county':
            if m['kind'] == 'place':
                gids, missing = place_ids(ros, st_fips, [p['name'] for p in comp['places']])
                res['places'] = [g for k, g in gids if k == 'place']
                res['cousubs'] = [g for k, g in gids if k == 'cousub']
                res['unresolved'] = [f'place or town not in the 2025 roster: {x}' for x in missing]
            else:
                res['unresolved'].append('tract-set: tracts were not fetched')
            fips, missing = names_to_fips(ros, st_fips, [c['name'] for c in comp['counties']])
            res['containing_counties'] = fips
        elif m['kind'] == 'cbsa':
            code = (m.get('cbsa') or {}).get('code')
            fed = ros['cbsas'].get(code)
            title = (m.get('cbsa') or {}).get('title', '')
            first_city = re.split(r'[-,]', title)[0].strip().lower()
            if not (fed and first_city and first_city in fed['name'].lower()):
                # a recalled code from an older delineation: find the 2023 CBSA by first city and state abbreviations
                abbrs = title.rsplit(',', 1)[-1].strip() if ',' in title else ''
                cands = [c for c, v in ros['cbsas'].items() if first_city and first_city in v['name'].lower() and abbrs and abbrs in v['name']]
                if len(cands) == 1:
                    res['notes'].append(f'the composer recalled code {code}; the 2023 delineation gives {cands[0]} "{ros["cbsas"][cands[0]]["name"]}" for that title')
                    code = cands[0]
                    fed = ros['cbsas'][code]
            if fed and first_city and first_city in fed['name'].lower():
                res['cbsa'] = code
                res['counties'] = fed['counties']
                res['notes'].append(f'CBSA {code} "{fed["name"]}", federal membership ({len(fed["counties"])} counties)')
                recalled = set(names_to_fips(ros, st_fips, [c['name'] for c in comp['counties'] if c.get('state') in (None, m['state_postal'])])[0])
                fed_here = {f for f in fed['counties'] if f[:2] == st_fips}
                if recalled and recalled != fed_here:
                    res['notes'].append('the composer recalled ' + ', '.join(sorted(ros['counties'][f].split(',')[0] for f in recalled - fed_here) or ['nothing extra'])
                                        + ' beyond, and missed ' + ', '.join(sorted(ros['counties'][f].split(',')[0] for f in fed_here - recalled) or ['nothing']))
                m['composition_source'] = 'cbsa-delineation'
            else:
                res['unresolved'].append(f'CBSA code {code} with title "{title}" is not in the 2025 roster under that title')
        else:
            names_by_state = collections.defaultdict(list)
            for c in comp['counties']:
                names_by_state[c.get('state') or m['state_postal']].append(c['name'])
            fips_all = []
            for postal, names in names_by_state.items():
                fips, missing = names_to_fips(ros, p2f.get(postal), names)
                fips_all += fips
                res['unresolved'] += [f'county not in the 2025 roster: {n} ({postal})' for n in missing]
            if key in UNION_OVERRIDES:
                ov = UNION_OVERRIDES[key]
                cb = next((c for c, v in ros['cbsas'].items() if ov['cbsa_title_contains'] in v['name'] and v['counties'] and v['counties'][0][:2] == st_fips), None)
                if cb is None:
                    res['unresolved'].append(f'no CBSA titled {ov["cbsa_title_contains"]} with members in this state in the roster')
                else:
                    plus, _ = names_to_fips(ros, st_fips, ov['plus_names'])
                    fips_all = sorted(set(ros['cbsas'][cb]['counties']) | set(plus))
                    res['notes'].append(ov['note'])
                m['composition_source'] = 'judgement-region'
            elif src == 'cbsa-delineation-pending':
                touched = sorted({ros['county_cbsa'][f] for f in fips_all if f in ros['county_cbsa']})
                states_here = {p2f.get(p) for p in names_by_state}
                union = sorted({f for cb in touched for f in ros['cbsas'][cb]['counties'] if f[:2] in states_here})
                if set(union) == set(fips_all) and fips_all:
                    m['composition_source'] = 'cbsa-union'
                    res['notes'].append('equals the federal union of CBSAs ' + ', '.join(f'{c} {ros["cbsas"][c]["name"]}' for c in touched))
                else:
                    m['composition_source'] = 'judgement-region'
                    m['review'] = True
                    extra = sorted(set(fips_all) - set(union))
                    missing = sorted(set(union) - set(fips_all))
                    res['notes'].append('kept as the composer listed it; against the federal union of the CBSAs it touches ('
                                        + ', '.join(f'{c} {ros["cbsas"][c]["name"]}' for c in touched) + ') it adds '
                                        + (', '.join(ros['counties'][f] for f in extra) or 'nothing') + ' and leaves out '
                                        + (', '.join(ros['counties'][f] for f in missing) or 'nothing'))
            res['counties'] = sorted(set(fips_all))
        # FOIA strings for every resolved county-based market
        if res['counties'] and m['composition_source'] in ('cbsa-delineation', 'cbsa-union', 'judgement-region', 'single-county', 'page-named-counties'):
            strings = [s for f in res['counties'] for s in strings_of.get(f, [])]
            old = {(x['state'], x['string']) for x in m['foia']['strings']}
            new = {(x['state'], x['string']) for x in strings}
            if m['foia']['strings'] and old != new:
                res['notes'].append('FOIA strings re-derived from the county FIPS join differ from the composer\'s: '
                                    f'added {sorted(new - old)}, dropped {sorted(old - new)}')
            m['foia']['strings'] = sorted(strings, key=lambda x: (x['state'], x['string']))
            m['foia']['resolved'] = True
        # The composer's text and flags predate the roster (D51): say where the membership
        # now comes from, and mark each recalled code against the 2025 roster.
        stale = '; counties unverified pending the delineation file'
        if res['cbsa'] and (m.get('basis') or '').endswith(stale):
            m['basis'] = m['basis'][:-len(stale)] + '; membership from the Census Data API geoinfo roster (2025)'
        if m.get('cbsa'):
            m['cbsa']['verified'] = bool(res['cbsa']) and res['cbsa'] == m['cbsa'].get('code')
        for c in comp.get('counties') or []:
            c['fips_verified'] = c.get('fips') in ros['counties'] and ros['counties'][c['fips']].split(',')[0].lower() == (c.get('name') or '').lower()
        m['resolved'] = res
        if res['unresolved']:
            problems.append((f'{m["state"]}/{m["slug"]}', res['unresolved']))

    geo['counties'] = {'status': 'FETCHED', 'source': 'census_geoinfo 2025', 'rows': [
        {'id': f'co-{f}', 'fips': f, 'name': n, 'state': f2p.get(f[:2]), 'cbsa': ros['county_cbsa'].get(f),
         'foia_strings': [x['string'] for x in strings_of.get(f, [])]} for f, n in sorted(ros['counties'].items())]}
    geo['cbsas'] = {'status': 'FETCHED', 'source': 'census_geoinfo 2025 (OMB Bulletin 23-01), summary levels 310, 320 and 313', 'rows': [
        {'id': f'cbsa-{c}', 'code': c, 'name': v['name'], 'type': v['type'], 'counties': v['counties']} for c, v in sorted(ros['cbsas'].items())]}
    geo['foia_county_join'] = {'about': 'FOIA (ProjectState, ProjectCounty) strings joined to 2025 county FIPS by normalised name within the state. '
                                        'Unmatched strings are counties that were renamed, split or merged, Connecticut\'s legacy counties (the 2025 roster uses planning regions), and blanks.',
                               'postal_to_state_fips': preport, 'matched': len(join),
                               'unmatched': [{'state': p, 'string': s, 'why': w} for p, s, w in sorted(unmatched)]}
    return problems
