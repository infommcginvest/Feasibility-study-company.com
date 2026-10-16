#!/usr/bin/env python3
"""Medical office + ASC, North Carolina (SBA 504, ground-up owner-occupied): recompute at the 15% borrower contribution.

Case: a physician group builds a roughly 15,000 sf owner-occupied medical office building with a surgery center (ASC)
inside it, $9.60M all in. The page published a 50/40/10 stack (bank / CDC debenture / borrower) and called the 10% the
504 equity injection. That tier is wrong for this project.

Rule: 13 CFR 120.910 (unchanged in SOP 50 10 8.1; register row R31): the Borrower contributes at least 10% in standard
cases; at least 15% if the Borrower (or the Operating Company when the Borrower is an Eligible Passive Company) has
operated two years or less (a New Business) OR the project is a limited or single purpose building; at least 20% if both.
SBA's limited or special purpose example list (504 chapter, register row R44) names "hospitals, surgery centers,
urgent care centers, and other health or medical facilities", so the surgery center puts this project in the special
purpose tier: 15% minimum. The owner's ruling is 15%, which holds on the reading that the operating company is the
established physician group (more than two years in operation); a New Business operating company would need 20%.
The page never says the group or borrower is newly formed, so the 15% tier is the one stated on the page.
AFTER structure: Third Party Lender 50%, CDC debenture 35%, borrower 15%.

Case inputs (every one is on the page; where is noted at each constant below):
  total project cost $9.60M (seven uses lines); bank 50% = $4.80M at ~9.5%, 25-year amortization; debenture at ~6.5%
  fixed, 25-year; global cash flow available for debt service Y1 ~$0.94M, Y2 ~$1.10M, Y3 ~$1.22M (stabilized);
  10-year hold; exit value ~$9.5M "held flat on value", ~3% selling cost, outstanding balance "near $7.0 million",
  net equity "roughly $2.2 million"; "modest interim distributions".
Only the debenture and the equity change: the bank tranche stays at 50% = $4.80M, so its debt service does not move.

Method.
  1. Payment function: monthly-compounding level payment, annualized (12 x monthly payment). BEFORE reproduces the page:
     bank $503k, debenture $311k, blended $814k; DSCR 1.15 / 1.35 / 1.50; ten-year balance $6.99M (page: near $7.0M);
     net exit equity $2.22M (page: roughly $2.2M). The script refuses to continue if BEFORE does not reproduce them.
  2. DSCR = global cash flow available for debt service / annual debt service, by year (page definition).
  3. IRR. The page states the equity outlay, the hold, the exit value, the selling cost and (via the amortization
     schedule) the exit balance, but NOT the interim distributions beyond calling them "modest", and it states cash
     flow only for Years 1 to 3. Two conventions are therefore needed. Years 4 to 10 global cash flow is held at the
     Year 3 stabilized level ($1.22M), in line with the page's flat-value assumption (this is a modelling convention,
     not a calibrated unknown; the sensitivity block below shows the answer does not depend on it). EXACTLY ONE unstated
     assumption is calibrated: the share p of each year's cash flow after debt service that is distributed to equity.
     p is solved so the BEFORE structure returns the published 16.0% levered IRR (annual end-of-year flows, year-0
     outlay = the equity injection, year-10 flow adds net sale proceeds). p is then held fixed and the AFTER IRR is
     computed with the AFTER equity, debt service and exit balance. The published figure is rounded to a whole percent
     ("about 16 percent"), so the script also shows that any BEFORE IRR between 15.5% and 16.5% leaves the AFTER IRR at
     the same whole percent.
  4. Cash on cash (cash flow after debt service / equity) and the equity multiple are not published on this page; they
     are printed for the record and are NOT part of --check.

Usage:
  python3 medical-office-north-carolina-sba.py            print the BEFORE / AFTER table
  python3 medical-office-north-carolina-sba.py --check    read the page, exit 1 listing every mismatch, 0 when clean
"""
import html
import json
import re
import sys
from pathlib import Path

PAGE = Path(__file__).resolve().parents[3] / 'case-studies' / 'medical-office-north-carolina-sba' / 'index.html'

# ----------------------------------------------------------------------------------------------------------------
# Case inputs, with the place on the page each comes from.
# ----------------------------------------------------------------------------------------------------------------
USES = {                                  # "Project cost breakdown" table (Financing section), $M
    'land': 1.20, 'shell_core': 3.90, 'fitout': 2.40, 'site_work': 0.60,
    'equipment_ffe': 0.75, 'soft_con_contingency': 0.55, 'wc_fees': 0.20,
}
TOTAL_COST = 9.60e6                       # "Total project cost" row, hero tile, lede
BANK_RATE, BANK_YEARS = 0.095, 25         # "Bank term / amortization: 25-year amortization / ~9.5%"
DEB_RATE, DEB_YEARS = 0.065, 25           # "Debenture term / rate: 25-year / ~6.5% fixed"
CASHFLOW = [0.94e6, 1.10e6, 1.22e6]       # "Global debt-service coverage ramp" table, Years 1 to 3 (Y3 = stabilized build)
REVENUE = {'asc': 3.60e6, 'practice': 2.60e6, 'rent': 0.16e6}   # "Stabilized global cash-flow build (Year 3)"
OPEX = 5.14e6                             # same table: operating expenses
HOLD_YEARS = 10                           # "levered equity IRR ... over a 10-year hold"
EXIT_VALUE = 9.5e6                        # "Valuing the stabilized ... enterprise at exit ... about $9.5 million"
SELL_COST = 0.03                          # "net of roughly 3 percent selling cost"
FLOOR = 1.15                              # SBA coverage floor used on the page

# Published BEFORE figures the model must reproduce (page as received).
PUB = {'bank_ds_k': 503, 'deb_ds_k': 311, 'ds_k': 814, 'dscr': ['1.15', '1.35', '1.50'],
       'balance_m': '7.0', 'net_eq_m': '2.2', 'irr_pct': 16.0}

STACKS = {'BEFORE': (0.50, 0.40, 0.10), 'AFTER': (0.50, 0.35, 0.15)}   # bank / debenture / borrower


def pmt(principal, rate, years):
    """Annual debt service: 12 x the monthly level payment, monthly compounding."""
    r = rate / 12.0
    n = years * 12
    return 12.0 * principal * r / (1.0 - (1.0 + r) ** -n)


def balance(principal, rate, years, months):
    """Outstanding principal after `months` monthly payments."""
    r = rate / 12.0
    n = years * 12
    pay = principal * r / (1.0 - (1.0 + r) ** -n)
    return principal * (1.0 + r) ** months - pay * ((1.0 + r) ** months - 1.0) / r


def irr(flows):
    lo, hi = -0.99, 5.0
    f = lambda x: sum(c / (1.0 + x) ** i for i, c in enumerate(flows))
    for _ in range(300):
        mid = (lo + hi) / 2.0
        if f(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def stack(name):
    b, d, e = STACKS[name]
    return {'bank': TOTAL_COST * b, 'deb': TOTAL_COST * d, 'eq': TOTAL_COST * e, 'pcts': (b, d, e)}


def structure(name, payout=None, growth=0.0):
    s = stack(name)
    s['bank_ds'] = pmt(s['bank'], BANK_RATE, BANK_YEARS)
    s['deb_ds'] = pmt(s['deb'], DEB_RATE, DEB_YEARS)
    s['ds'] = s['bank_ds'] + s['deb_ds']
    s['dscr'] = [cf / s['ds'] for cf in CASHFLOW]
    s['cfads'] = [cf - s['ds'] for cf in CASHFLOW]
    s['coc'] = [x / s['eq'] for x in s['cfads']]
    s['balance'] = (balance(s['bank'], BANK_RATE, BANK_YEARS, HOLD_YEARS * 12)
                    + balance(s['deb'], DEB_RATE, DEB_YEARS, HOLD_YEARS * 12))
    s['net_exit_eq'] = EXIT_VALUE * (1.0 - SELL_COST) - s['balance']
    s['financed_pct'] = (s['bank'] + s['deb']) / TOTAL_COST
    if payout is not None:
        cfs = CASHFLOW + [CASHFLOW[-1] * (1.0 + growth) ** k for k in range(1, HOLD_YEARS - 2)]
        flows = [-s['eq']] + [payout * (c - s['ds']) for c in cfs]
        flows[-1] += s['net_exit_eq']
        s['irr'] = irr(flows)
        s['multiple'] = sum(flows[1:]) / s['eq']
    return s


def calibrate(target, growth=0.0):
    """Share of cash flow after debt service distributed, such that BEFORE returns `target`."""
    lo, hi = 0.0, 1.0
    for _ in range(200):
        mid = (lo + hi) / 2.0
        if structure('BEFORE', mid, growth)['irr'] < target:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2.0


def compute():
    p = calibrate(PUB['irr_pct'] / 100.0)
    return p, structure('BEFORE', p), structure('AFTER', p)


# ----------------------------------------------------------------------------------------------------------------
# Formats (the page's own conventions)
# ----------------------------------------------------------------------------------------------------------------
def m2(x):   return '$%.2fM' % (x / 1e6)                      # $1.44M
def mil2(x): return '$%.2f million' % (x / 1e6)               # $1.44 million
def mil1(x): return '$%.1f million' % (x / 1e6)               # $6.6 million
def kc(x):   return '$%s' % format(int(round(x / 1000.0)) * 1000, ',')   # $775,000
def kk(x):   return '$%dk' % int(round(x / 1000.0))           # $775k
def d2(x):   return '%.2f' % x                                # 1.57
def pct0(x): return '%d' % int(round(x * 100.0))              # 12


def reproduce(before):
    got = {
        'bank_ds_k': int(round(before['bank_ds'] / 1000.0)), 'deb_ds_k': int(round(before['deb_ds'] / 1000.0)),
        'ds_k': int(round(before['ds'] / 1000.0)), 'dscr': [d2(x) for x in before['dscr']],
        'balance_m': '%.1f' % (before['balance'] / 1e6), 'net_eq_m': '%.1f' % (before['net_exit_eq'] / 1e6),
        'irr_pct': round(before['irr'] * 100.0, 1),
    }
    bad = [k for k in PUB if got[k] != PUB[k]]
    return got, bad


def report():
    p, b, a = compute()
    # input integrity
    assert abs(sum(USES.values()) * 1e6 - TOTAL_COST) < 1, 'uses do not sum to the total'
    assert abs(sum(REVENUE.values()) - OPEX - CASHFLOW[2]) < 1, 'Year 3 build does not give the Year 3 cash flow'
    got, bad = reproduce(b)
    print('BEFORE reproduces the published figures:', 'YES' if not bad else 'NO %s' % bad)
    if bad:
        print('  model', got, '\n  page ', PUB)
        sys.exit(2)
    print('  bank DS $%dk, debenture DS $%dk, blended $%dk; DSCR %s; ten-year balance $%.2fM; net exit equity $%.2fM'
          % (got['bank_ds_k'], got['deb_ds_k'], got['ds_k'], '/'.join(got['dscr']), b['balance'] / 1e6, b['net_exit_eq'] / 1e6))
    print('IRR calibration: one unstated assumption, share of cash flow after debt service distributed = %.4f' % p)
    print('  (Years 4-10 global cash flow held at the Year 3 level $%.2fM; BEFORE IRR %.2f%% = published ~16%%)'
          % (CASHFLOW[2] / 1e6, b['irr'] * 100))
    print()
    rows = [
        ('Total project cost', m2(TOTAL_COST), m2(TOTAL_COST)),
        ('Bank first mortgage', '%s (%d%%)' % (m2(b['bank']), b['pcts'][0] * 100), '%s (%d%%)' % (m2(a['bank']), a['pcts'][0] * 100)),
        ('CDC debenture', '%s (%d%%)' % (m2(b['deb']), b['pcts'][1] * 100), '%s (%d%%)' % (m2(a['deb']), a['pcts'][1] * 100)),
        ('Borrower equity', '%s (%d%%)' % (m2(b['eq']), b['pcts'][2] * 100), '%s (%d%%)' % (m2(a['eq']), a['pcts'][2] * 100)),
        ('Financed share of cost', '%d%%' % round(b['financed_pct'] * 100), '%d%%' % round(a['financed_pct'] * 100)),
        ('Bank debt service', kc(b['bank_ds']), kc(a['bank_ds'])),
        ('Debenture debt service', kc(b['deb_ds']), kc(a['deb_ds'])),
        ('Blended debt service', '%s (%s)' % (kc(b['ds']), kk(b['ds'])), '%s (%s)' % (kc(a['ds']), kk(a['ds']))),
        ('DSCR Year 1 (cash flow ~$0.94M)', d2(b['dscr'][0]), d2(a['dscr'][0])),
        ('DSCR Year 2 (cash flow ~$1.10M)', d2(b['dscr'][1]), d2(a['dscr'][1])),
        ('DSCR Year 3 / stabilized (~$1.22M)', d2(b['dscr'][2]), d2(a['dscr'][2])),
        ('Ten-year loan balance', mil1(b['balance']), mil1(a['balance'])),
        ('Net equity at exit', mil1(b['net_exit_eq']), mil1(a['net_exit_eq'])),
        ('Levered equity IRR', '%.1f%%' % (b['irr'] * 100), '%.1f%%' % (a['irr'] * 100)),
        ('-- not published on this page (not in --check) --', '', ''),
        ('Cash on cash Y1 / Y2 / Y3 (100% distributed)', ' / '.join('%.1f%%' % (x * 100) for x in b['coc']),
         ' / '.join('%.1f%%' % (x * 100) for x in a['coc'])),
        ('Equity multiple (calibrated payout)', '%.2fx' % b['multiple'], '%.2fx' % a['multiple']),
        ('Cash flow cushion over 1.15x floor, Y3', '$%dk' % round((CASHFLOW[2] - FLOOR * b['ds']) / 1000),
         '$%dk' % round((CASHFLOW[2] - FLOOR * a['ds']) / 1000)),
    ]
    w = max(len(r[0]) for r in rows)
    print('%-*s  %-26s  %s' % (w, 'Figure', 'BEFORE (50/40/10)', 'AFTER (50/35/15)'))
    for r in rows:
        print('%-*s  %-26s  %s' % (w, r[0], r[1], r[2]))
    print()
    print('Sensitivity of the AFTER IRR to the unstated conventions (BEFORE recalibrated to 16.0% each time):')
    for g in (-0.02, 0.0, 0.02, 0.03):
        pg = calibrate(0.16, g)
        print('  Years 4-10 cash flow growth %+.0f%%/yr: payout %.3f, AFTER IRR %.2f%%'
              % (g * 100, pg, structure('AFTER', pg, g)['irr'] * 100))
    for t in (0.155, 0.165):
        pt = calibrate(t)
        print('  BEFORE IRR %.1f%% (published "about 16%%" rounds from 15.5 to 16.5): AFTER IRR %.2f%%'
              % (t * 100, structure('AFTER', pt)['irr'] * 100))
    print()
    print('Rule: 13 CFR 120.910: 10% standard; 15% New Business OR limited/special purpose; 20% both. '
          'Surgery center = special purpose (R44). 15% holds if the operating company is the established group; '
          'a New Business operating company would need 20% (debenture 30%).')
    return p, b, a


# ----------------------------------------------------------------------------------------------------------------
# --check: the page must carry every AFTER figure, in its own format
# ----------------------------------------------------------------------------------------------------------------
DASHES = ''.join(chr(c) for c in (0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015, 0x2212, 0x2043, 0xFE58, 0xFE63, 0xFF0D))
INLINE = r'(?:a|em|strong|b|i|u|span|time|sup|sub|small|abbr|mark|code|cite|s)'


def norm(s):
    s = html.unescape(s)
    s = s.replace(chr(0xA0), ' ').replace(chr(0x2009), ' ').replace(chr(0x202F), ' ')
    s = re.sub('[%s]' % DASHES, '-', s)
    for q, r in ((0x2019, "'"), (0x2018, "'"), (0x201C, '"'), (0x201D, '"')):
        s = s.replace(chr(q), r)
    s = s.replace(chr(0x2248), '~')
    return re.sub(r'\s+', ' ', s).strip()


def page_text(raw):
    """Tags stripped, entities decoded, whitespace collapsed, dashes normalized. Footnote markers and HTML comments
    (including the sba: regulatory markers) are dropped; inline tags join their neighbours, block tags separate."""
    t = re.sub(r'<script\b.*?</script>', ' ', raw, flags=re.S | re.I)
    t = re.sub(r'<style\b.*?</style>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    t = re.sub(r'<sup\s+class="fn">.*?</sup>', '', t, flags=re.S)
    t = re.sub(r'</?%s\b[^>]*>' % INLINE, '', t, flags=re.I)
    t = re.sub(r'<[^>]+>', ' ', t)
    return norm(t)


def meta_contents(raw):
    out = {}
    for tag in re.findall(r'<meta\b[^>]*>', raw, flags=re.I):
        attrs = dict(re.findall(r'([\w:-]+)="([^"]*)"', tag))
        key = attrs.get('name') or attrs.get('property')
        if key and 'content' in attrs:
            out[key] = norm(attrs['content'])
    return out


def jsonld_blocks(raw):
    return re.findall(r'<script\s+type="application/ld\+json">(.*?)</script>', raw, flags=re.S)


def article_description(raw):
    for blk in jsonld_blocks(raw):
        try:
            data = json.loads(blk)
        except ValueError:
            continue
        for node in (data.get('@graph', [data]) if isinstance(data, dict) else data):
            if isinstance(node, dict) and node.get('@type') == 'Article':
                return norm(node.get('description', ''))
    return ''


def expected(p, b, a):
    """(label, source, substring) for every AFTER figure that must appear, in the page's own format."""
    A = a
    ds_c, ds_k = kc(A['ds']), kk(A['ds'])
    dscr = [d2(x) for x in A['dscr']]
    irr_p = pct0(A['irr'])
    fin_p = '%d' % round(A['financed_pct'] * 100)
    bp, dp, ep = ['%d' % round(x * 100) for x in A['pcts']]
    cf = ['~$%.2fM' % (x / 1e6) for x in CASHFLOW]
    E = [
        ('hero tile: financed share and stack', 'text', '%s%% SBA 504 financing (%s%% bank + %s%% CDC debenture)' % (fin_p, bp, dp)),
        ('hero tile: stabilized DSCR', 'text', '%sx Stabilized global DSCR, above the ~1.15x SBA floor' % dscr[2]),
        ('hero tile: IRR', 'text', '~%s%% Illustrative levered equity IRR, 10-year hold' % irr_p),
        ('hero tile: total cost', 'text', '%s Total project cost' % m2(TOTAL_COST)),
        ('capital table: bank', 'text', 'Bank first mortgage (%s%%) %s' % (bp, m2(A['bank']))),
        ('capital table: debenture', 'text', 'CDC / SBA 504 debenture (%s%%) %s' % (dp, m2(A['deb']))),
        ('capital table: equity', 'text', 'Borrower equity injection (%s%%) %s' % (ep, m2(A['eq']))),
        ('capital table: blended debt service', 'text', 'Annual debt service (blended) ~ %s' % ds_k),
        ('financing prose: split', 'text', "The 504's %s/%s/%s split does the work here: a bank first mortgage at %s percent, a fixed-rate CDC "
                                           "debenture at %s percent, and a %s percent equity injection." % (bp, dp, ep, bp, dp, ep)),
        ('financing prose: tranche debt service', 'text', 'the bank tranche at an illustrative 9.5 percent carries about %s a year and the '
                                                           'debenture at roughly 6.5 percent fixed about %s, for blended annual debt service near %s'
                                                           % (kc(A['bank_ds']), kc(A['deb_ds']), ds_c)),
        ('financing lede', 'text', 'a borrower equity injection (%s percent here, as set out below)' % ep),
        ('financing prose: total cost', 'text', 'At %s total the deal' % mil2(TOTAL_COST)),
        ('tier sentence', 'text', TIER_SENTENCE),
        ('coverage prose: stabilized', 'text', 'The stabilized %sx global coverage is the figure the lender documents' % dscr[2]),
        ('coverage prose: ramp', 'text', 'so Year 1 sits at %sx, Year 2 builds to %sx as case volume and payer contracts mature, and Year 3 reaches %sx.'
                                         % tuple(dscr)),
        ('equity prose: injection', 'text', 'the %s injection earns a return' % mil2(A['eq'])),
        ('equity prose: exit balance', 'text', 'an outstanding balance near %s after ten years of amortization' % mil1(A['balance'])),
        ('equity prose: net equity', 'text', 'implies roughly %s of net equity, against the %s injected.' % (mil1(A['net_exit_eq']), mil2(A['eq']))),
        ('equity prose: IRR', 'text', 'levered equity IRR of about %s percent over a 10-year hold.' % irr_p),
        ('verdict', 'text', 'a stabilized %sx global DSCR, and a ~%s%% levered equity IRR' % (dscr[2], irr_p)),
        ('meta description', 'meta:description', 'a %s project cost, a %sx stabilized global DSCR, and a ~%s%% levered equity IRR' % (m2(TOTAL_COST), dscr[2], irr_p)),
        ('og:description', 'meta:og:description', '%s cost, %sx global DSCR, ~%s%% IRR' % (m2(TOTAL_COST), dscr[2], irr_p)),
        ('JSON-LD Article description', 'jsonld', 'a %s project cost, a %sx stabilized global DSCR, and a ~%s%% levered equity IRR' % (m2(TOTAL_COST), dscr[2], irr_p)),
    ]
    return E


TIER_SENTENCE = ('That 15% is the 504 minimum for a limited or special purpose property such as a surgery center '
                 'under 13 CFR 120.910, on the basis that the operating company is the established physician group (more than two '
                 'years in operation); an operating company with two years or less of operations would need 20%.')
SOURCE_14 = ('13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), '
             'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910')

# BEFORE figures that must be gone, as patterns over the normalized text (and meta / JSON-LD descriptions).
STALE = [
    ('blended debt service $814k / $814,000', r'\$814'),
    ('debenture debt service $311,000', r'\$311,000'),
    ('debenture $3.84M', r'\$3\.84'),
    ('equity $0.96M', r'\$0\.96'),
    ('DSCR 1.50x / Year 3 1.50', r'(?<![\d.])1\.50(?![\d])'),
    ('DSCR 1.35', r'(?<![\d.])1\.35(?![\d])'),
    ('IRR 16%', r'(?<![\d.])16(?:\s?%| percent)'),
    ('90% financing', r'(?<![\d.])90\s?%'),
    ('50/40/10 split', r'50/40/10'),
    ('debenture 40%', r'\(40%\)|debenture at 40 percent|\+ 40% CDC'),
    ('balance $7.0 million', r'\$7\.0 million'),
    ('net equity $2.2 million', r'\$2\.2 million'),
]


def stale_equity_sentences(text):
    """Sentences that state 10% as this project's equity or as the 504 minimum for it."""
    bad = []
    for sent in re.split(r'(?<=[.!?;])\s+', text):
        if re.search(r'(?<![\d.])10(?:\s?%| percent)', sent) and re.search(
                r'equity|injection|contribution|minimum|borrower|split|down payment', sent, flags=re.I):
            bad.append(sent[:160])
    return bad


def check():
    if not PAGE.exists():
        print('page not found:', PAGE)
        return 1
    raw = PAGE.read_text(encoding='utf-8')
    p, b, a = compute()
    got, bad = reproduce(b)
    problems = []
    if bad:
        problems.append('model does not reproduce the BEFORE page figures: %s' % bad)
    text = page_text(raw)
    sources = {'text': text, 'jsonld': article_description(raw)}
    for k, v in meta_contents(raw).items():
        sources['meta:' + k] = v
    for label, src, sub in expected(p, b, a):
        if norm(sub) not in sources.get(src, ''):
            problems.append('missing [%s] (%s): %s' % (label, src, norm(sub)))
    # DSCR table rows, whole-row check: global cash flow, debt-service basis, DSCR
    cf = ['~$%.2fM' % (x / 1e6) for x in CASHFLOW]
    for i in range(3):
        row = '%s Fully amortizing ~%s %s' % (cf[i], kk(a['ds']), d2(a['dscr'][i]))
        if norm(row) not in text:
            problems.append('missing [DSCR table year %d row]: %s' % (i + 1, row))
    # stale BEFORE figures anywhere in prose, tables, meta, JSON-LD
    for label, pat in STALE:
        for name, src in sources.items():
            if re.search(pat, src):
                problems.append('stale BEFORE figure [%s] still in %s' % (label, name))
    for sent in stale_equity_sentences(text):
        problems.append('a sentence still states 10%% as the equity / 504 minimum: %s' % sent)
    # source 14 and footnotes
    if norm(SOURCE_14) not in text:
        problems.append('source 14 (13 CFR 120.910 entry) is missing from the sources list')
    ids = set(re.findall(r'<li id="(s\d+)"', raw))
    for ref in sorted(set(re.findall(r'<a href="#(s\d+)">', raw))):
        if ref not in ids:
            problems.append('footnote points at #%s but no source has that id' % ref)
    if 's14' not in ids or not re.search(r'<sup class="fn"><a href="#s14">14</a></sup>', raw):
        problems.append('no footnote marker points at source 14')
    # structured data parses
    for n, blk in enumerate(jsonld_blocks(raw), 1):
        try:
            json.loads(blk)
        except ValueError as e:
            problems.append('JSON-LD block %d does not parse: %s' % (n, e))
    if problems:
        print('CHECK FAILED: %d mismatch(es)' % len(problems))
        for x in problems:
            print('  -', x)
        return 1
    print('CHECK OK: every AFTER figure is on the page in its own format; no stale BEFORE figure; tier sentence and source 14 present')
    return 0


if __name__ == '__main__':
    if '--check' in sys.argv[1:]:
        sys.exit(check())
    report()
