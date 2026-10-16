#!/usr/bin/env python3
"""Assemble data/markets/geographies.json from the composition drafts
(docs/web-fsc-5/compose/group*.json) and the FOIA county-string inventory.

    python3 docs/web-fsc-5/tools/assemble_geographies.py

Checks, and refuses to write on failure:
  * exactly one row per market slug found on the site (compose/market_extracts.json);
  * every kind is one the charter allows;
  * every FOIA string a row names exists verbatim in the inventory for its state;
  * every Connecticut row carries both schemes;
  * a CBSA row is never marked resolved: its member counties must come from the
    OMB delineation file, which this lane could not fetch.
"""
import csv
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
COMPOSE = os.path.join(ROOT, 'docs', 'web-fsc-5', 'compose')
OUT = os.path.join(ROOT, 'data', 'markets', 'geographies.json')
KINDS = {'cbsa', 'county', 'county-set', 'place', 'tract-set', 'cross-state'}
CT_LEGACY = {'FAIRFIELD', 'HARTFORD', 'LITCHFIELD', 'MIDDLESEX', 'NEW HAVEN', 'NEW LONDON', 'TOLLAND', 'WINDHAM'}


def main():
    extracts = json.load(open(os.path.join(COMPOSE, 'market_extracts.json')))
    want = {(s, m) for s, ms in extracts.items() for m in ms}
    inv = {}
    with open(os.path.join(COMPOSE, 'foia_county_inventory.tsv'), newline='') as f:
        for r in csv.DictReader(f, delimiter='\t'):
            inv.setdefault(r['state'], set()).add(r['project_county'])
    rows, problems = [], []
    for fn in sorted(os.listdir(COMPOSE)):
        if re.fullmatch(r'group\d+\.json', fn):
            rows.extend(json.load(open(os.path.join(COMPOSE, fn)))['markets'])
    seen = {}
    markets = []
    for r in rows:
        key = (r['state'], r['slug'])
        if key in seen:
            problems.append(f'duplicate {key}')
            continue
        seen[key] = True
        if key not in want:
            problems.append(f'not a site market: {key}')
        if r['kind'] not in KINDS:
            problems.append(f'{key}: bad kind {r["kind"]}')
        st = r['state_postal']
        strings, missing = [], []
        for c in r.get('foia_county_strings') or []:
            cst = c.get('state', st)
            for s in c.get('strings') or []:
                if s not in inv.get(cst, set()):
                    problems.append(f'{key}: FOIA string {cst}|{s} not in inventory')
                strings.append({'state': cst, 'string': s})
        ct = None
        note = None
        if r.get('ct') and st != 'CT':
            note = r['ct'].get('description') if isinstance(r['ct'], dict) else str(r['ct'])
            r['ct'] = None
        if r.get('ct'):
            leg = [x for c in r['ct'].get('legacy_counties', []) for x in c.get('foia', [])]
            pr = [x for c in r['ct'].get('planning_regions', []) for x in c.get('foia', [])]
            for s in leg + pr:
                if s not in inv.get('CT', set()):
                    problems.append(f'{key}: CT FOIA string {s} not in inventory')
            if not leg or not pr:
                problems.append(f'{key}: Connecticut row lacks a scheme (legacy {len(leg)}, planning {len(pr)})')
            if set(leg) - CT_LEGACY or set(pr) & CT_LEGACY:
                problems.append(f'{key}: CT strings put in the wrong scheme (legacy {leg}, planning {pr})')
            ct = {'legacy': sorted(set(leg)), 'pr': sorted(set(pr))}
        elif st == 'CT':
            problems.append(f'{key}: Connecticut row without a ct block')
        basis = r.get('basis') or ''
        if ct:
            source = 'connecticut-two-schemes'
        elif r['kind'] in ('place', 'tract-set'):
            source = 'sub-county'
        elif r['kind'] == 'cbsa' or (re.search(r'\bCBSAs?\b', basis) and not re.search(r'page names|named in the page|page text', basis)):
            # member counties rest on CBSA membership, which must come from the OMB
            # delineation file (not fetched); the composer's recalled list is not used
            source = 'cbsa-delineation-pending'
        elif r['kind'] == 'county' and not re.search(r'commonly bounded', basis):
            source = 'single-county'
        elif re.search(r'page names|named in the page|page text|county the state page names', basis):
            source = 'page-named-counties'
        else:
            source = 'judgement-region'
        resolved = source in ('single-county', 'page-named-counties', 'judgement-region') and bool(strings)
        markets.append({
            'state': r['state'], 'slug': r['slug'], 'state_postal': st, 'page_title': r.get('page_title'),
            'kind': r['kind'], 'cbsa': r.get('cbsa'),
            'components': {'counties': r.get('counties') or [], 'places': r.get('places') or [],
                           'cross_state': r.get('cross_state'), 'ct': r.get('ct'), 'tract_note': note},
            'foia': {'resolved': resolved and not ct, 'strings': strings if not ct else [],
                     'ct': ct, 'containing_county_strings': r.get('foia_containing_county_strings') or [],
                     'missing': r.get('foia_missing') or []},
            'ct': bool(ct),
            'composition_source': source,
            'basis': r.get('basis'), 'reason': r.get('reason'), 'review': bool(r.get('review')),
        })
    for k in sorted(want - set(seen)):
        problems.append(f'missing market {k}')
    if problems:
        print('\n'.join(problems))
        print(f'{len(problems)} problem(s); geographies.json NOT written')
        return 1
    postal = {}
    for m in markets:
        postal.setdefault(m['state'], m['state_postal'])
    foia_states = sorted(inv)
    states = []
    for slug, pc in sorted(postal.items()):
        states.append({'id': pc.lower(), 'postal': pc, 'slug': slug, 'name': slug.replace('-', ' ').title(),
                       'site_page': os.path.exists(os.path.join(ROOT, 'states', slug, 'index.html')), 'site_markets': True, 'fips': None})
    for pc in foia_states:
        if pc and pc not in postal.values():
            states.append({'id': pc.lower(), 'postal': pc, 'slug': None, 'name': None, 'site_page': False, 'site_markets': False, 'fips': None})
    out = {
        'about': ('Site markets and their compositions. County is the atomic unit. A CBSA market takes its member counties from the OMB delineation file; '
                  'a judgement composition carries review = true and its basis. State ids are USPS codes in lower case; market ids are <state-slug>/<market-slug>. '
                  'Assembled by docs/web-fsc-5/tools/assemble_geographies.py from the composition drafts in docs/web-fsc-5/compose/.'),
        'id_scheme': {'us': 'the nation', 'state': 'USPS code, lower case (tx)', 'market': '<state-slug>/<market-slug> (texas/houston)',
                      'ct_component': '<market>:legacy or <market>:pr (Connecticut FOIA loans by coding scheme)',
                      'county': 'co-<5-digit FIPS> once a Census county roster is fetched', 'cbsa': 'cbsa-<5-digit code> once the delineation is fetched'},
        'counties': {'status': 'NOT FETCHED', 'reason': 'No federal county roster was reachable: the Census Data API needs a key (DECISIONS D2) and www2.census.gov is closed by robots.txt (D1). County FIPS codes in the market rows are the composer\'s, marked fips_verified false.', 'rows': []},
        'cbsas': {'status': 'NOT FETCHED', 'reason': 'The OMB delineation file (list1_2023.xlsx) is on www2.census.gov (D1) and the geoinfo API needs a key (D2). CBSA codes in the market rows are the composer\'s, marked verified false.', 'rows': []},
        'states': states,
        'markets': sorted(markets, key=lambda m: (m['state'], m['slug'])),
    }
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(out, f, indent=1, ensure_ascii=False)
        f.write('\n')
    kinds = {}
    for m in markets:
        kinds[m['kind']] = kinds.get(m['kind'], 0) + 1
    srcs = {}
    for m in markets:
        srcs[m['composition_source']] = srcs.get(m['composition_source'], 0) + 1
    print('composition sources:', srcs)
    print(f'wrote {os.path.relpath(OUT, ROOT)}: {len(markets)} markets {kinds}; review {sum(m["review"] for m in markets)}; '
          f'FOIA-resolved {sum(m["foia"]["resolved"] for m in markets)}; CT {sum(m["ct"] for m in markets)}; states {len(states)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
