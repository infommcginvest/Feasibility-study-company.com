#!/usr/bin/env python3
"""Fetch the federal series behind the markets register (data/markets/).

Raw files land in _cache/markets/raw/<source>/<vintage>/ (gitignored) and every
file is recorded in _cache/markets/manifest.json with its URL, retrieval time,
HTTP status, bytes and sha256. Nothing here writes to data/markets/; the build
script does that from the raw files.

Every request passes the door gate in get() before any byte is asked for:

  * the host must be one of the six source hosts in HOSTS;
  * the host's robots.txt is read once per run and evaluated as RFC 9309 says
    (a group is one or more user-agent lines, blank lines included, followed by
    its rules; the group naming our product token wins, else the `*` group;
    longest match wins, allow wins a tie; a 4xx robots file allows all, a 5xx
    or network failure disallows all);
  * a 403, an AWS WAF challenge (x-amzn-waf-action) or a Census key wall
    (X-DataWebAPI-KeyError / missing_key.html) is a refusal and is recorded,
    never worked around.

A source whose door is shut is recorded NOT FETCHED with the reason, and the
build carries that status into data/markets/sources.json.

    python3 scripts/markets_fetch.py               fetch every source
    python3 scripts/markets_fetch.py --only sba_7a_foia,sba_504_foia
    python3 scripts/markets_fetch.py --doors       probe and record the doors only
    python3 scripts/markets_fetch.py --refresh     re-pull every source whose expected
                                                   next release has passed, rebuild, and
                                                   print the values that changed

Keys: a Census Data API key is read from the CENSUS_API_KEY environment
variable and a BEA API UserID from BEA_API_KEY. They are sent on the request
only, never written to the manifest, a log or a file; recorded URLs carry
`key=REDACTED`.
"""
import datetime as dt
import hashlib
import html
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, '_cache', 'markets')
RAW = os.path.join(CACHE, 'raw')
MANIFEST = os.path.join(CACHE, 'manifest.json')
SOURCES_JSON = os.path.join(ROOT, 'data', 'markets', 'sources.json')

# The owner may set the User-Agent for a run in MARKETS_UA (the API keys are registered
# to the owner's analytics site); the product token for robots matching follows it.
UA = os.environ.get('MARKETS_UA') or 'FSC-MarketsRegister/1.0 (federal statistics register for feasibility-study-company.com; contact info@feasibility-study-company.com)'
PRODUCT = UA.split('/', 1)[0].split()[0]
HOSTS = {'api.census.gov', 'www2.census.gov', 'data.bls.gov', 'api.bls.gov', 'apps.bea.gov', 'www.huduser.gov', 'data.sba.gov'}
TIMEOUT = 60          # seconds per socket operation
MAX_TRIES = 4
PAUSE = 0.5           # seconds between requests to one host


def now():
    return dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat().replace('+00:00', 'Z')


class Refused(Exception):
    """The door is shut: robots, 403, bot challenge, key wall or a host off the list."""


# ---------------------------------------------------------------- robots (RFC 9309)

def parse_robots(text):
    """Return [(agents, rules)] following the RFC 9309 ABNF: a group starts with
    user-agent lines (blank lines may sit between them) and ends when a
    user-agent line follows a rule."""
    groups, agents, rules, in_rules = [], [], [], False
    for raw in text.splitlines():
        line = raw.split('#', 1)[0].strip()
        if not line or ':' not in line:
            continue
        key, val = line.split(':', 1)
        key, val = key.strip().lower(), val.strip()
        if key == 'user-agent':
            if in_rules:
                groups.append((agents, rules)); agents, rules, in_rules = [], [], False
            agents.append(val.lower())
        elif key in ('allow', 'disallow'):
            if not agents:
                continue          # a rule before any user-agent line belongs to no group
            in_rules = True
            rules.append((key, val))
    if agents:
        groups.append((agents, rules))
    return groups


def _pattern(path):
    anchored = path.endswith('$')
    body = path[:-1] if anchored else path
    rx = ''.join('.*' if ch == '*' else re.escape(ch) for ch in body)
    return re.compile('^' + rx + ('$' if anchored else ''))


def robots_allows(groups, path, product=PRODUCT.lower()):
    """Longest match wins; allow wins a tie; an empty disallow allows."""
    named = [g for g in groups if any(a != '*' and product.startswith(a) for a in g[0])]
    chosen = named or [g for g in groups if '*' in g[0]]
    rules = [r for g in chosen for r in g[1]]
    best = None
    for kind, val in rules:
        if kind == 'disallow' and val == '':
            continue
        if _pattern(val).match(path):
            score = (len(val), kind == 'allow')
            if best is None or score > best[0]:
                best = (score, kind)
    return best is None or best[1] == 'allow'


_DOORS = {}


def door(host, log):
    """Read and evaluate a host's robots.txt once per run."""
    if host in _DOORS:
        return _DOORS[host]
    url = f'https://{host}/robots.txt'
    rec = {'host': host, 'robots_url': url, 'checked_at': now()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            body = r.read()
            rec['status'] = r.status
            hdr = {k.lower(): v for k, v in r.headers.items()}
    except urllib.error.HTTPError as e:
        body = e.read() if hasattr(e, 'read') else b''
        rec['status'] = e.code
        hdr = {k.lower(): v for k, v in (e.headers or {}).items()}
    except Exception as e:          # network failure: RFC 9309 says disallow all
        rec.update(status=None, error=str(e)[:200], verdict='disallow-all (robots unreachable)')
        _DOORS[host] = (rec, None); log.append(rec); return _DOORS[host]
    rec['bytes'] = len(body)
    rec['sha256'] = hashlib.sha256(body).hexdigest()
    if len(body) <= 20000:
        rec['body'] = body.decode('utf-8', 'replace')    # retained as evidence for the verdict
    st = rec['status']
    if hdr.get('x-amzn-waf-action') or (st == 202 and not body):
        rec['verdict'] = 'challenge (AWS WAF bot check on robots.txt)'
        groups = None
    elif 400 <= st < 500:
        rec['verdict'] = 'allow-all (robots.txt 4xx)'
        groups = []
    elif st >= 500:
        rec['verdict'] = 'disallow-all (robots.txt 5xx)'
        groups = None
    else:
        text = body.decode('utf-8', 'replace')
        groups = parse_robots(text)
        rec['groups'] = [{'agents': a, 'rules': [f'{k}: {v}' for k, v in r]} for a, r in groups]
        rec['verdict'] = 'parsed' if groups else 'allow-all (no robots groups in a 200 body)'
    _DOORS[host] = (rec, groups)
    log.append(rec)
    return _DOORS[host]


# Owner rulings that set a robots.txt bar aside, host by host. Empty: the owner's correction of
# 16 Oct withdrew the www2.census.gov reading (D50); www2 is closed under the standing robots rule.
ROBOTS_RULINGS = {}


def ruled_urls():
    return {u for s in SOURCES for u in s.get('urls', []) if urllib.parse.urlsplit(u).hostname in ROBOTS_RULINGS}


def check_door(url, log):
    u = urllib.parse.urlsplit(url)
    if u.scheme != 'https' or u.hostname not in HOSTS:
        raise Refused(f'host {u.hostname} is not one of the source hosts')
    rec, groups = door(u.hostname, log)
    if groups is None:
        raise Refused(f'{u.hostname}: {rec["verdict"]}')
    path = u.path + (('?' + u.query) if u.query else '')
    if not robots_allows(groups, path) and u.hostname in ROBOTS_RULINGS and url in ruled_urls():
        log.append({'host': u.hostname, 'url': url, 'checked_at': now(), 'verdict': 'robots disallows; fetched under ' + ROBOTS_RULINGS[u.hostname]})
        return
    if not robots_allows(groups, path):
        raise Refused(f'{u.hostname} robots.txt disallows {u.path} for user-agent * (RFC 9309 group: '
                      + '; '.join(f"{','.join(a)} -> {len(r)} rule(s)" for a, r in groups if '*' in a) + ')')


# ---------------------------------------------------------------- HTTP

def redact(url):
    return re.sub(r'(key|UserID|api_key|registrationkey)=[^&]+', r'\1=REDACTED', url, flags=re.I)


def get(url, dest=None, log=None, expect_json=False):
    """GET through the door gate. With dest, stream to dest (resuming a .part
    file with a Range request when the server accepts ranges) and return the
    file record; without dest, return the body bytes."""
    log = log if log is not None else []
    check_door(url, log)
    host = urllib.parse.urlsplit(url).hostname
    last = None
    for attempt in range(1, MAX_TRIES + 1):
        time.sleep(PAUSE)
        part = dest + '.part' if dest else None
        have = os.path.getsize(part) if part and os.path.exists(part) else 0
        headers = {'User-Agent': UA}
        if have:
            headers['Range'] = f'bytes={have}-'
        req = urllib.request.Request(url, headers=headers)
        try:
            opener = urllib.request.build_opener(_NoRedirect)
            with opener.open(req, timeout=TIMEOUT) as r:
                hdr = {k.lower(): v for k, v in r.headers.items()}
                _refusal(r.status, hdr, url)
                if dest is None:
                    return r.read()
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                mode = 'ab' if (have and r.status == 206) else 'wb'
                with open(part, mode) as f:
                    while True:
                        chunk = r.read(1 << 20)
                        if not chunk:
                            break
                        f.write(chunk)
                total = int(hdr.get('content-range', '/').split('/')[-1] or 0) if r.status == 206 else int(hdr.get('content-length') or 0)
                size = os.path.getsize(part)
                if total and size != total:
                    raise IOError(f'short read {size} of {total}')
                os.replace(part, dest)
                return {'url': redact(url), 'path': os.path.relpath(dest, ROOT), 'bytes': size,
                        'sha256': sha256(dest), 'retrieved_at': now(), 'http_status': r.status,
                        'last_modified': hdr.get('last-modified'), 'etag': hdr.get('etag')}
        except Refused:
            raise
        except urllib.error.HTTPError as e:
            hdr = {k.lower(): v for k, v in (e.headers or {}).items()}
            _refusal(e.code, hdr, url)
            last = f'HTTP {e.code}'
            if e.code == 416 and part and os.path.exists(part):
                os.remove(part)
            if e.code < 500 and e.code not in (408, 416, 429):
                raise IOError(f'{redact(url)}: HTTP {e.code}')
        except Exception as e:
            last = str(e)[:200]
        time.sleep(min(30, 2 ** attempt))
    raise IOError(f'{redact(url)}: gave up after {MAX_TRIES} tries ({last})')


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Follow a redirect only within the same host; record anything else."""
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        if urllib.parse.urlsplit(newurl).hostname != urllib.parse.urlsplit(req.full_url).hostname:
            raise Refused(f'redirect off host to {newurl}')
        if 'missing_key' in newurl or 'invalid_key' in newurl:
            raise Refused(f'Census Data API key wall: redirected to {newurl} (X-DataWebAPI-KeyError {headers.get("X-DataWebAPI-KeyError")})')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def _refusal(status, hdr, url):
    if hdr.get('x-amzn-waf-action'):
        raise Refused(f'AWS WAF bot challenge (x-amzn-waf-action: {hdr["x-amzn-waf-action"]}, HTTP {status})')
    if hdr.get('x-datawebapi-keyerror'):
        raise Refused(f'Census Data API key wall (X-DataWebAPI-KeyError {hdr["x-datawebapi-keyerror"]})')
    if status == 403:
        raise Refused(f'HTTP 403 from {urllib.parse.urlsplit(url).hostname}')
    if status == 202:
        raise Refused(f'HTTP 202 with no content (bot check) from {urllib.parse.urlsplit(url).hostname}')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


# ---------------------------------------------------------------- source plan
#
# Each source names its publisher, the exact title, the URL(s) and how the
# vintage is found. `plan(src)` returns [(url, relative_dest)] for the run.

def census_key():
    return os.environ.get('CENSUS_API_KEY') or None


def census_api(path, params):
    """Census Data API URL. Spaces go as %20 and '/' stays literal: the API answers
    'unknown/unsupported geography hierarchy' to %2F or '+' (measured 2026-10-16)."""
    q = dict(params)
    if census_key():
        q['key'] = census_key()
    return f'https://api.census.gov/data/{path}?' + '&'.join(f'{k}={urllib.parse.quote(str(v), safe=":,*/()")}' for k, v in q.items())


ACS_VARS_A = ['B01003_001', 'B11001_001', 'B19013_001', 'B19301_001', 'B19313_001', 'B25003_001',
              'B25003_002', 'B25003_003', 'B25064_001', 'B25077_001', 'B23025_003', 'B23025_005']
ACS_VARS_B = [f'B01001_{i:03d}' for i in list(range(20, 26)) + list(range(44, 50))]


def acs_geos(one_year):
    g = [('us', {'for': 'us:1'}), ('state', {'for': 'state:*'}), ('county', {'for': 'county:*', 'in': 'state:*'}),
         ('cbsa', {'for': 'metropolitan statistical area/micropolitan statistical area:*'}),
         ('place', {'for': 'place:*', 'in': 'state:*'})]
    return g


def plan_acs(src):
    out = []
    one = src['id'] == 'census_acs1'
    for tag, vars_ in (('a', ACS_VARS_A), ('b', ACS_VARS_B)):
        get_ = ','.join(['NAME'] + [v + s for v in vars_ for s in ('E', 'M')])
        for geo, params in acs_geos(one):
            out.append((census_api(src['api_path'], {'get': get_, **params}), f'{geo}_{tag}.json'))
        if not one:
            for st in src.get('_states', []):
                out.append((census_api(src['api_path'], {'get': get_, 'for': 'county subdivision:*', 'in': f'state:{st} county:*'}), f'cousub_{st}_{tag}.json'))
    return out


def plan_cbp(src):
    """Every industry code in one request per geography level (NAICS2017=*), so
    parents come with their 6-digit children and absent cells can be bounded;
    counties one state at a time. CBP 2023 in the API uses NAICS 2017 codes."""
    get_ = 'NAME,ESTAB,EMP,EMP_N,NAICS2017'
    p = src['api_path']
    out = [(census_api(p, {'get': get_, 'NAICS2017': '*', 'for': 'us:1'}), 'us_all.json'),
           (census_api(p, {'get': get_, 'NAICS2017': '*', 'for': 'state:*'}), 'state_all.json'),
           (census_api(p, {'get': get_, 'NAICS2017': '*', 'for': 'metropolitan statistical area/micropolitan statistical area:*'}), 'cbsa_all.json')]
    for st in src.get('_states', []):
        out.append((census_api(p, {'get': get_, 'NAICS2017': '*', 'for': 'county:*', 'in': f'state:{st}'}), f'county_{st}.json'))
    return out


def plan_pep(src):
    # total population only: all ages (0000), both sexes (0), all origins (0), total group (001)
    get_ = 'NAME,POP,YEAR,MONTH'
    return [(census_api(src['api_path'], {'get': get_, 'AGE': '0000', 'SEX': '0', 'HISP': '0', 'POPGROUP': '001', **params}), f'{geo}.json')
            for geo, params in (('us', {'for': 'us:1'}), ('state', {'for': 'state:*'}), ('county', {'for': 'county:*', 'in': 'state:*'}),
                                ('cbsa', {'for': 'metropolitan statistical area/micropolitan statistical area:*'}))]


def plan_geoinfo(src):
    """Three phases (the API takes no wildcard CBSA or state in these hierarchies,
    measured 2026-10-16): 1) states, counties, CBSAs, places; 2) per state, its
    CBSA parts (summary level 320) and its county subdivisions; 3) per CBSA part,
    its member counties (summary level 313, explicit CBSA and state)."""
    p = src['api_path']
    out = [(census_api(p, {'get': 'NAME,AREALAND', 'for': 'state:*'}), 'state.json'),
           (census_api(p, {'get': 'NAME,AREALAND', 'for': 'county:*', 'in': 'state:*'}), 'county.json'),
           (census_api(p, {'get': 'NAME', 'for': 'metropolitan statistical area/micropolitan statistical area:*'}), 'cbsa.json'),
           (census_api(p, {'get': 'NAME', 'for': 'place:*', 'in': 'state:*'}), 'place.json')]
    for st in src.get('_states', []):
        out.append((census_api(p, {'get': 'NAME', 'for': 'metropolitan statistical area/micropolitan statistical area (or part):*', 'in': f'state:{st}'}), f'cbsa_parts_{st}.json'))
        out.append((census_api(p, {'get': 'NAME', 'for': 'county subdivision:*', 'in': f'state:{st} county:*'}), f'cousub_{st}.json'))
    for cb, st in src.get('_cbsa_parts', []):
        out.append((census_api(p, {'get': 'NAME', 'for': 'county:*', 'in': f'metropolitan statistical area/micropolitan statistical area:{cb} state (or part):{st}'}), f'cbsa_county_{cb}_{st}.json'))
    return out


def plan_dec_ct(src):
    return [(census_api(src['api_path'], {'get': 'NAME,P1_001N', 'for': 'county subdivision:*', 'in': 'state:09 county:*'}), 'ct_cousub_2020.json')]


def plan_static(src):
    return [(u, os.path.basename(urllib.parse.urlsplit(u).path)) for u in src['urls']]


def plan_bea_api(src):
    k = os.environ.get('BEA_API_KEY')
    if not k:
        return []
    base = 'https://apps.bea.gov/api/data?'
    out = []
    for line in ('1', '2', '3'):
        for geo in ('COUNTY', 'STATE', 'MSA'):
            q = {'UserID': k, 'method': 'GetData', 'datasetname': 'Regional', 'TableName': 'CAINC1',
                 'LineCode': line, 'GeoFips': geo, 'Year': 'LAST5', 'ResultFormat': 'json'}
            out.append((base + urllib.parse.urlencode(q), f'cainc1_{geo.lower()}_line{line}.json'))
    return out


SBA_PAGE = 'https://data.sba.gov/dataset/7a-504-foia'


def discover_sba(log):
    """The FOIA file names carry their as-of date and change every quarter, so
    read them from the dataset page (robots allows /dataset/ and /sites/)."""
    body = get(SBA_PAGE, log=log).decode('utf-8', 'replace')
    urls = sorted(set(html.unescape(m) for m in re.findall(r'href="(https://data\.sba\.gov/sites/default/files/uploaded_resources/[^"]+)"', body)))
    files = [u for u in urls if re.search(r'/FOIA_(7a|504)_FY\d{4}_(FY\d{4}|Present)_asof_\d{6}\.csv$', u)]
    dic = [u for u in urls if re.search(r'foia_data_dictionary\.xlsx$', u, re.I)]
    asof = sorted(set(re.search(r'asof_(\d{6})', u).group(1) for u in files))
    if len(asof) != 1:
        raise IOError(f'SBA FOIA files carry {len(asof)} as-of dates: {asof}')
    a = asof[0]
    vintage = f'20{a[:2]}-{a[2:4]}-{a[4:]}'
    return vintage, files, dic


SOURCES = [
    {'id': 'census_geoinfo', 'publisher': 'U.S. Census Bureau, Geography Division',
     'title': '2025 Geography Information (Census Data API geoinfo): states, counties, CBSAs (OMB Bulletin 23-01 delineation), places, county subdivisions',
     'api_path': '2025/geoinfo', 'vintage': '2025', 'period': 'geography in effect January 1, 2025',
     'cadence': 'annual', 'next_release': '2027-05-31', 'kind': 'geoinfo', 'needs': 'CENSUS_API_KEY'},
    {'id': 'census_pep', 'publisher': 'U.S. Census Bureau, Population Estimates Program',
     'title': 'Vintage 2025 Population Estimates: Annual Estimates of the Resident Population for Counties (co-est2025-alldata.csv)',
     'urls': ['https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/counties/totals/co-est2025-alldata.csv',
              'https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/metro/totals/cbsa-est2025-alldata.csv',
              'https://www2.census.gov/programs-surveys/popest/datasets/2020-2025/state/totals/NST-EST2025-ALLDATA.csv'],
     'vintage': 'V2025', 'period': 'July 1, 2020 to July 1, 2025', 'cadence': 'annual (counties each March)',
     'next_release': '2027-03-31', 'kind': 'static'},
    {'id': 'census_pep_api', 'publisher': 'U.S. Census Bureau, Population Estimates Program',
     'title': 'Vintage 2023 Population Estimates by Age, Sex, Race, and Hispanic Origin (Census Data API pep/charv)',
     'api_path': '2023/pep/charv', 'vintage': 'V2023', 'period': 'July 1, 2020 to July 1, 2023',
     'cadence': 'annual', 'next_release': '2026-12-31', 'kind': 'pep', 'needs': 'CENSUS_API_KEY'},
    {'id': 'census_acs5', 'publisher': 'U.S. Census Bureau, American Community Survey',
     'title': 'American Community Survey 5-Year Estimates, Detailed Tables, 2020-2024 (Census Data API acs/acs5)',
     'api_path': '2024/acs/acs5', 'vintage': '2024 5-year', 'period': '2020-2024',
     'cadence': 'annual (each December)', 'next_release': '2026-12-10', 'kind': 'acs', 'needs': 'CENSUS_API_KEY'},
    {'id': 'census_acs1', 'publisher': 'U.S. Census Bureau, American Community Survey',
     'title': 'American Community Survey 1-Year Estimates, Detailed Tables, 2024 (Census Data API acs/acs1)',
     'api_path': '2024/acs/acs1', 'vintage': '2024 1-year', 'period': '2024',
     'cadence': 'annual (each September)', 'next_release': '2026-09-30', 'kind': 'acs', 'needs': 'CENSUS_API_KEY'},
    {'id': 'census_bps', 'publisher': 'U.S. Census Bureau, Building Permits Survey',
     'title': 'Building Permits Survey, annual county, CBSA and state files (co2025a.txt, cbsa2025a.txt, st2025a.txt) and 2021-2024 annual county files',
     'urls': [f'https://www2.census.gov/econ/bps/County/co{y}a.txt' for y in (2021, 2022, 2023, 2024, 2025)]
             + ['https://www2.census.gov/econ/bps/County/co2022aupdatednotice.txt', 'https://www2.census.gov/econ/bps/State/st2025a.txt'],
     'vintage': '2025 annual', 'period': '2021-2025', 'cadence': 'annual (each May) and monthly',
     'next_release': '2027-05-31', 'kind': 'static'},
    {'id': 'census_cbp', 'publisher': 'U.S. Census Bureau, County Business Patterns',
     'title': '2023 County Business Patterns, all industries (Census Data API cbp, NAICS2017=*)', 'api_path': '2023/cbp',
     'vintage': '2023', 'period': 'week of March 12, 2023', 'cadence': 'annual',
     'next_release': '2026-06-30', 'kind': 'cbp', 'needs': 'CENSUS_API_KEY'},
    {'id': 'census_cbp_bulk', 'publisher': 'U.S. Census Bureau, County Business Patterns',
     'title': '2023 County Business Patterns, complete county, state, metro and U.S. files (cbp23co.zip, cbp23st.zip, cbp23msa.zip, cbp23us.zip)',
     'urls': [f'https://www2.census.gov/programs-surveys/cbp/datasets/2023/cbp23{g}.zip' for g in ('co', 'st', 'msa', 'us')],
     'vintage': '2023', 'period': 'week of March 12, 2023', 'cadence': 'annual', 'next_release': '2026-06-30', 'kind': 'static'},
    {'id': 'census_delineation', 'publisher': 'U.S. Census Bureau (OMB Bulletin 23-01)',
     'title': 'Core based statistical areas (CBSAs), metropolitan divisions, and combined statistical areas (CSAs), July 2023 (list1_2023.xlsx)',
     'urls': ['https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/list1_2023.xlsx'],
     'vintage': 'July 2023', 'period': 'OMB Bulletin 23-01', 'cadence': 'irregular (OMB bulletins)', 'next_release': 'unscheduled', 'kind': 'static'},
    {'id': 'census_dec2020_ct', 'publisher': 'U.S. Census Bureau, 2020 Census',
     'title': '2020 Census Redistricting Data (PL 94-171), Connecticut county subdivisions under the legacy counties (Census Data API dec/pl)',
     'api_path': '2020/dec/pl', 'vintage': '2020', 'period': 'April 1, 2020', 'cadence': 'decennial',
     'next_release': '2031-03-31', 'kind': 'dec_ct', 'needs': 'CENSUS_API_KEY'},
    {'id': 'census_ct_crosswalk', 'publisher': 'U.S. Census Bureau, Geography Division',
     'title': 'Connecticut county to county subdivision crosswalk, legacy counties to planning regions (ct_cou_to_cousub_crosswalk.txt)',
     'urls': ['https://www2.census.gov/geo/docs/reference/ct_change/ct_cou_to_cousub_crosswalk.txt'],
     'vintage': '2022', 'period': 'Connecticut planning regions adopted 2022', 'cadence': 'one-time', 'next_release': 'unscheduled', 'kind': 'static'},
    {'id': 'bls_qcew', 'publisher': 'U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages',
     'title': 'QCEW annual averages, all areas, single file (2025_annual_singlefile.zip)',
     'urls': ['https://data.bls.gov/cew/data/files/2025/csv/2025_annual_singlefile.zip'],
     'vintage': '2025 annual', 'period': '2025', 'cadence': 'quarterly; annual averages each September',
     'next_release': '2027-09-30', 'kind': 'static'},
    {'id': 'bea_cainc1', 'publisher': 'U.S. Bureau of Economic Analysis',
     'title': 'CAINC1 Personal Income Summary: Personal Income, Population, Per Capita Personal Income (county, MSA, state)',
     'urls': ['https://apps.bea.gov/regional/zip/CAINC1.zip'],
     'vintage': '2024', 'period': '2020-2024', 'cadence': 'annual (each November)', 'next_release': '2026-11-15', 'kind': 'static'},
    {'id': 'bea_cainc1_api', 'publisher': 'U.S. Bureau of Economic Analysis',
     'title': 'Regional dataset, table CAINC1, line codes 1 to 3 (BEA API GetData)',
     'vintage': '2024', 'period': 'last five years published', 'cadence': 'annual (each November)',
     'next_release': '2026-11-15', 'kind': 'bea_api', 'needs': 'BEA_API_KEY'},
    {'id': 'bls_qcew_api', 'publisher': 'U.S. Bureau of Labor Statistics, Quarterly Census of Employment and Wages',
     'title': 'QCEW series through the BLS Public Data API v2 (api.bls.gov/publicAPI/v2/timeseries/data/)',
     'urls': ['https://api.bls.gov/publicAPI/v2/timeseries/data/'],
     'vintage': '2025 annual', 'period': '2025', 'cadence': 'quarterly; annual averages each September',
     'next_release': '2027-09-30', 'kind': 'static'},
    {'id': 'hud_fmr', 'publisher': 'U.S. Department of Housing and Urban Development, Office of Policy Development and Research',
     'title': 'FY2027 Fair Market Rents, county-level file (FY27_FMRs.xlsx)',
     'urls': ['https://www.huduser.gov/portal/datasets/fmr/fmr2027/FY27_FMRs.xlsx'],
     'vintage': 'FY2027', 'period': 'October 1, 2026 to September 30, 2027', 'cadence': 'annual (each August/September)',
     'next_release': '2027-09-01', 'kind': 'static'},
    {'id': 'sba_foia', 'publisher': 'U.S. Small Business Administration, Office of Capital Access',
     'title': '7(a) & 504 FOIA (data.sba.gov dataset 7a-504-foia)', 'kind': 'sba',
     'cadence': 'quarterly (about one month after quarter end)'},
]


PROBES = {}
PROBE_URLS = {
    # the smallest data request each API serves; sent once per run without a key
    'CENSUS_API_KEY': 'https://api.census.gov/data/2023/cbp?get=ESTAB&for=us:1&NAICS2017=721110',
    'BEA_API_KEY': 'https://apps.bea.gov/api/data?method=GETDATASETLIST&ResultFormat=JSON',
}


def key_open(name, log):
    """True when the API can be used: the key is set, or a keyless request,
    sent once per run and recorded in PROBES, returned data. Never assumed."""
    if os.environ.get(name):
        return True
    if name in PROBES:
        return PROBES[name]['open']
    url = PROBE_URLS[name]
    rec = {'key': name, 'url': url, 'observed_at': now()}
    try:
        check_door(url, log)
        req = urllib.request.Request(url, headers={'User-Agent': UA})
        opener = urllib.request.build_opener(_NoFollow)
        try:
            with opener.open(req, timeout=TIMEOUT) as r:
                status, hdr, body = r.status, {k.lower(): v for k, v in r.headers.items()}, r.read(4096)
        except urllib.error.HTTPError as e:
            status, hdr, body = e.code, {k.lower(): v for k, v in (e.headers or {}).items()}, (e.read(4096) if hasattr(e, 'read') else b'')
        text = body.decode('utf-8', 'replace')
        rec.update(http_status=status, location=hdr.get('location'), x_datawebapi_keyerror=hdr.get('x-datawebapi-keyerror'),
                   content_type=hdr.get('content-type'), body_start=text[:300])
        if name == 'CENSUS_API_KEY':
            rec['open'] = status == 200 and text.lstrip().startswith('[')
        else:
            rec['open'] = status == 200 and text.lstrip().startswith('{') and '"error"' not in text.lower()
        rec['body_bytes'] = len(body)
    except Refused as e:
        rec.update(open=False, refused=str(e))
    except Exception as e:
        rec.update(open=False, error=str(e)[:200])
    PROBES[name] = rec
    return rec['open']


class _NoFollow(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def plan(src, log):
    k = src['kind']
    if src.get('needs') and not key_open(src['needs'], log):
        pr = PROBES.get(src['needs'], {})
        if pr.get('error'):
            raise Refused(f'{src["needs"]} is not set, and the keyless probe at {pr.get("observed_at")} failed with a network error '
                          f'({pr["error"]}); no key-wall observation was made this run')
        seen = (f'HTTP {pr.get("http_status")}' + (f', Location {pr["location"]}' if pr.get('location') else '')
                + (f', X-DataWebAPI-KeyError {pr["x_datawebapi_keyerror"]}' if pr.get('x_datawebapi_keyerror') else '')
                + (f', body starts {pr["body_start"][:120]!r}' if pr.get('body_start') and not pr.get('location') else '')
                + (', empty body' if pr.get('body_bytes') == 0 else '')
                + (f'; {pr["refused"]}' if pr.get('refused') else ''))
        raise Refused(f'{src["needs"]} is not set, and a keyless request observed at {pr.get("observed_at")} was refused '
                      f'({pr.get("url")} -> {seen}); the probe is recorded under probes in the fetch manifest and copied into each freeze record')
    if k == 'static':
        return src['vintage'], plan_static(src)
    if k == 'acs':
        return src['vintage'], plan_acs(src)
    if k == 'cbp':
        return src['vintage'], plan_cbp(src)
    if k == 'pep':
        return src['vintage'], plan_pep(src)
    if k == 'geoinfo':
        return src['vintage'], plan_geoinfo(src)
    if k == 'dec_ct':
        return src['vintage'], plan_dec_ct(src)
    if k == 'bea_api':
        return src['vintage'], plan_bea_api(src)
    if k == 'sba':
        vintage, files, dic = discover_sba(log)
        src['vintage'] = vintage
        return vintage, [(u, os.path.basename(u)) for u in files + dic]
    raise ValueError(k)


def api_rows(path):
    """A Census Data API response (a JSON array whose first row is the header) as dicts."""
    rows = json.load(open(path))
    return [dict(zip(rows[0], r)) for r in rows[1:]]


def plan_inputs():
    """Parameters the API plans need: the NAICS 2022 codes of the 43 classes
    (naics-map.json), and every state and every CBSA code, read from the
    first-phase geoinfo files (state.json, cbsa.json) once they are fetched."""
    out = {'naics': [], 'cbsas': [], 'states': []}
    nm = os.path.join(ROOT, 'data', 'markets', 'naics-map.json')
    if os.path.exists(nm):
        m = json.load(open(nm))
        out['naics'] = sorted({c for row in m['classes'] for c in row['naics2022']})
    g = next((x for x in SOURCES if x['id'] == 'census_geoinfo'), None)
    gdir = os.path.join(RAW, 'census_geoinfo', re.sub(r'[^A-Za-z0-9_.-]', '_', g['vintage'])) if g else None
    if gdir and os.path.exists(os.path.join(gdir, 'state.json')):
        out['states'] = sorted({r['state'] for r in api_rows(os.path.join(gdir, 'state.json'))})
    if gdir and os.path.exists(os.path.join(gdir, 'cbsa.json')):
        col = 'metropolitan statistical area/micropolitan statistical area'
        out['cbsas'] = sorted({r[col] for r in api_rows(os.path.join(gdir, 'cbsa.json'))})
    out['cbsa_parts'] = []
    for st in out['states']:
        f = os.path.join(gdir, f'cbsa_parts_{st}.json') if gdir else None
        if f and os.path.exists(f):
            col = 'metropolitan statistical area/micropolitan statistical area (or part)'
            out['cbsa_parts'] += [(r[col], st) for r in api_rows(f)]
    out['cbsa_parts'].sort()
    return out


# ---------------------------------------------------------------- run

def load_manifest():
    if os.path.exists(MANIFEST):
        return json.load(open(MANIFEST))
    return {'files': {}, 'sources': {}, 'doors': []}


def save_manifest(m):
    os.makedirs(CACHE, exist_ok=True)
    tmp = MANIFEST + '.tmp'
    json.dump(m, open(tmp, 'w'), indent=1, sort_keys=True)
    os.replace(tmp, MANIFEST)


def fetch_source(src, man, log, force=False):
    sid = src['id']
    rec = {'id': sid, 'attempted_at': now()}
    try:
        files = []
        done = set()
        # geoinfo runs in three phases, each planned from the files of the one
        # before (see plan_geoinfo)
        for phase in range(3 if src['kind'] == 'geoinfo' else 1):
            inputs = plan_inputs()
            src['_naics'], src['_states'], src['_cbsas'] = inputs['naics'], inputs['states'], inputs['cbsas']
            src['_cbsa_parts'] = inputs['cbsa_parts']
            vintage, items = plan(src, log)
            if not items:
                raise Refused('no request planned')
            rec['vintage'] = vintage
            files += fetch_items(sid, vintage, [(u, r) for u, r in items if r not in done], man, log, force)
            done |= {r for _, r in items}
        rec.update(status='FETCHED', files=files)
    except Refused as e:
        rec.update(status='NOT FETCHED', reason=str(e))
    except Exception as e:
        rec.update(status='NOT FETCHED', reason=f'error: {e}')
    man['sources'][sid] = rec
    print(f'{sid}: {rec["status"]}' + (f' ({rec.get("reason")})' if rec.get('reason') else f' ({len(rec["files"])} file(s), vintage {rec["vintage"]})'), flush=True)
    return rec


def fetch_items(sid, vintage, items, man, log, force):
    files = []
    for url, rel in items:
        dest = os.path.join(RAW, sid, re.sub(r'[^A-Za-z0-9_.-]', '_', vintage), rel)
        key = os.path.relpath(dest, ROOT)
        if not force and key in man['files'] and os.path.exists(dest) and man['files'][key]['sha256'] == sha256(dest):
            files.append(key); continue
        check_door(url, log)
        print(f'  GET {redact(url)}', flush=True)
        frec = get(url, dest, log)
        frec['source'] = sid
        man['files'][key] = frec
        files.append(key)
        save_manifest(man)
    return files


def main(argv):
    man = load_manifest()
    log = []
    only = None
    for a in argv:
        if a.startswith('--only'):
            only = set((a.split('=', 1)[1] if '=' in a else argv[argv.index(a) + 1]).split(','))
    if '--doors' in argv:
        for h in sorted(HOSTS):
            door(h, log)
        man['doors'] = log
        save_manifest(man)
        for r in log:
            print(f'{r["host"]}: robots {r.get("status")} -> {r["verdict"]}')
        return 0
    targets = [s for s in SOURCES if not only or s['id'] in only]
    if '--refresh' in argv:
        reg = json.load(open(SOURCES_JSON)) if os.path.exists(SOURCES_JSON) else {'sources': []}
        due = {r['fetch_source'] for r in reg['sources'] if r.get('fetch_source') and (r.get('next_release') or '9999') <= dt.date.today().isoformat()}
        due |= {r['fetch_source'] for r in reg['sources'] if r.get('status') == 'NOT FETCHED' and r.get('fetch_source')}
        targets = [s for s in targets if s['id'] in due]
        print('due:', ', '.join(s['id'] for s in targets) or 'nothing')
    for s in targets:
        fetch_source(s, man, log, force='--refresh' in argv)
    man['doors'] = log or man.get('doors', [])
    if PROBES:
        merged = {r['key']: r for r in man.get('probes', [])}
        merged.update(PROBES)
        man['probes'] = [merged[k] for k in sorted(merged)]
    man['run_at'] = now()
    save_manifest(man)
    if '--refresh' in argv:
        build = [sys.executable, os.path.join(ROOT, 'scripts', 'markets_build.py'), '--diff']
        return subprocess.run(build, timeout=3600).returncode
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
