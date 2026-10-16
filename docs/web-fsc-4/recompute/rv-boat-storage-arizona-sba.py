#!/usr/bin/env python3
"""RV and boat storage, Arizona (SBA 504, ground-up): recompute at the 15 percent New Business equity tier.

Page:  case-studies/rv-boat-storage-arizona-sba/index.html
Rule:  13 CFR 120.910 (unchanged in SOP 50 10 8.1). The 504 borrower contribution is at least 10% in standard cases,
       at least 15% if the borrower (or Operating Company) has operated two years or less (a New Business) OR the
       project is a limited or special purpose building, and at least 20% if both. The "10% restored for start-ups"
       in SOP 50 10 8.1 is the 7(a) Start-Up Business rule, not a 504 rule. A ground-up storage business is a New
       Business, and the page itself says a mixed-format yard is unlikely to draw the special purpose designation,
       so the tier is 15% and the stack is Third Party Lender 50% / CDC debenture 35% / borrower 15%.
       The published page financed it 50 / 40 / 10, which is the standard-case tier and does not apply.

Case inputs (all unchanged by the fix; each comment says where on the page it sits):
  total project cost $5.00M and its eight-line uses table ("Project cost breakdown", Financing section);
  bank first mortgage 50% of cost at ~9.5%, 25-year amortization; debenture ~6.5% fixed, 25-year ("Capital structure
  & terms" table); NOI by year ~$382k / ~$488k / ~$615k ("Debt-service coverage ramp" table); Year-3 NOI build
  (rent roll, vacancy 8%, ancillary $44.0k, expenses ~33.5% of EGI, "Stabilized revenue & NOI build" table).
  The page states no cash-on-cash figure, so cash-on-cash is printed here for the log but is not on the page.

Method.
  1. Payments are level monthly amortization: payment = P*r/(1-(1+r)^-n), r = rate/12, n = 12*years; annual debt
     service = 12 * payment. Dollar figures on the page are rounded to $1,000 ("$262k", "$142,000").
  2. DSCR = published NOI (rounded $k) / debt service; the page rounds to two decimals. The script checks that
     dividing by the unrounded debt service and by the $k-rounded debt service give the same two-decimal answer.
  3. BEFORE (50/40/10) must reproduce every published figure (debt service $262k + $162k = $424k; DSCR 0.90, 1.15,
     1.45) or the script exits 2 and does not go on.
  4. IRR. The page states: 10-year hold, "modest" rent growth, a funded replacement reserve, a Year-10 exit "wide of
     the going-in yield on cost" against a market of roughly 6.0-7.5% (Class A) and 7.5-8.5% (Class B), and a levered
     equity IRR "near 16 percent". It gives no growth rate, no exit cap rate, no reserve amount and no sale cost.
     The procedure was to calibrate ONE unstated assumption (the exit cap rate) so BEFORE reproduces 16%, hold it,
     and compute AFTER. That calibration fails the test of a model that can stand on the page: with $0.50M of equity
     and $191k a year of cash after debt service from Year 3, the operating cash flows alone are worth more than the
     equity at a 16% discount rate, so a 16% IRR needs the Year-10 sale to cost the owner money (net sale proceeds
     to equity below zero, an exit price below the remaining debt). No exit cap inside the page's own stated range
     gets near 16% (it gives 30% and up). So the published 16% is NOT reproducible from the page's inputs, and the
     page does not give the facts a recompute needs. Per the hard constraint ("if a fix needs a fact the page does
     not give, leave the original, and report it") the IRR figure on the page is left as published and this script
     prints the evidence, the literal-procedure AFTER figure, a sane-range sensitivity grid, and the unlevered
     (capital-structure-independent) IRR, which does land at about 16% inside the page's own cap range. None of the
     IRR diagnostics is a figure on the page and none is checked by --check.

Usage:
  python3 rv-boat-storage-arizona-sba.py          print the BEFORE / AFTER table and the IRR diagnostics
  python3 rv-boat-storage-arizona-sba.py --check  read the page (--page PATH checks another copy); exit 1 listing every mismatch, 0 when every AFTER
                                                  figure appears on the page in the page's own format and rounding
                                                  and no sentence still states 10% as this project's equity or as
                                                  the 504 minimum for it
--check compares on text with tags stripped, entities decoded, whitespace collapsed, and every dash variant (hyphen,
en dash, em dash, minus, non-breaking hyphen) folded to a plain hyphen, so punctuation-only edits and links wrapped
around ordinary words do not break it. Standard library only; no network; the page is only read.
"""
import html
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

PAGE = Path(__file__).resolve().parents[3] / 'case-studies' / 'rv-boat-storage-arizona-sba' / 'index.html'

# ----------------------------------------------------------------------------------------------------- case inputs
# "Project cost breakdown" table (Financing section), $M
USES = {
    'land': 0.75, 'site_work': 1.05, 'covered_canopy': 1.60, 'enclosed_building': 0.70,
    'security_access': 0.25, 'office_utilities': 0.20, 'soft_costs_contingency': 0.30, 'wc_leaseup_fees': 0.15,
}
COST = 5_000_000                       # "Total project cost $5.00M"; checked against the sum of USES below
BANK_PCT = 0.50                        # "Bank first mortgage (50%)"
BANK_RATE, BANK_YEARS = 0.095, 25      # "~9.5% / 25-year amortization"
DEB_RATE, DEB_YEARS = 0.065, 25        # "~6.5% fixed / 25-year"
NOI = (382_000, 488_000, 615_000)      # "Debt-service coverage ramp": Year 1, Year 2, Year 3 (~$382k, ~$488k, ~$615k)
OCC = ('~62%', '~78%', '~92%')
# "Stabilized revenue & NOI build (Year 3)" table
NOI_BUILD = {'canopy': 320 * 165 * 12, 'open': 120 * 95 * 12, 'enclosed': 60 * 260 * 12,
             'vacancy_pct': 0.08, 'ancillary': 44_000, 'expense_ratio': 0.335}
HOLD_YEARS = 10                        # "10-year hold"
IRR_PUBLISHED = 0.16                   # tile "≈16%", prose "near 16 percent", capsule "~16%"; left as published

# The structure the page published (BEFORE) and the correct 504 tier for a New Business (AFTER)
BEFORE = {'name': 'BEFORE 50/40/10', 'bank': 0.50, 'deb': 0.40, 'eq': 0.10}
AFTER = {'name': 'AFTER 50/35/15', 'bank': 0.50, 'deb': 0.35, 'eq': 0.15}

# Figures the page publishes today (BEFORE); the model must reproduce all of them
PUBLISHED_BEFORE = {
    'bank_ds_k': 262, 'deb_ds_k': 162, 'ds_k': 424,
    'dscr': ('0.90', '1.15', '1.45'),
    'bank_amt': '$2.50M', 'deb_amt': '$2.00M', 'eq_amt': '$0.50M', 'debt_share': 90,
}


# ----------------------------------------------------------------------------------------------------- arithmetic
def pmt_monthly(principal, rate, years):
    r, n = rate / 12.0, years * 12
    return principal * r / (1.0 - (1.0 + r) ** -n)


def balance(principal, rate, years, months_paid):
    r = rate / 12.0
    p = pmt_monthly(principal, rate, years)
    return principal * (1 + r) ** months_paid - p * ((1 + r) ** months_paid - 1) / r


def rhu(x, places=2):
    """Round half up to `places` decimals (the page's rounding), returned as a Decimal."""
    q = Decimal(1).scaleb(-places)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)


def d2(x):
    return str(rhu(x, 2))


def money_m(x):            # $2.50M
    return '$%sM' % rhu(x / 1e6, 2)


def money_million(x):      # $2.50 million
    return '$%s million' % rhu(x / 1e6, 2)


def money_k(x):            # $262k
    return '$%dk' % int(rhu(x / 1e3, 0))


def money_full(x):         # $262,000 (rounded to the nearest $1,000)
    return '${:,}'.format(int(rhu(x / 1e3, 0)) * 1000)


def structure(s):
    bank = s['bank'] * COST
    deb = s['deb'] * COST
    eq = s['eq'] * COST
    bank_ds = 12 * pmt_monthly(bank, BANK_RATE, BANK_YEARS)
    deb_ds = 12 * pmt_monthly(deb, DEB_RATE, DEB_YEARS)
    ds = bank_ds + deb_ds
    ds_k = int(rhu(bank_ds / 1e3, 0)) + int(rhu(deb_ds / 1e3, 0))
    ds_k_total = int(rhu(ds / 1e3, 0))
    out = {
        'name': s['name'], 'bank': bank, 'deb': deb, 'eq': eq, 'bank_ds': bank_ds, 'deb_ds': deb_ds, 'ds': ds,
        'bank_ds_k': int(rhu(bank_ds / 1e3, 0)), 'deb_ds_k': int(rhu(deb_ds / 1e3, 0)), 'ds_k': ds_k,
        'ds_k_total': ds_k_total,
        'debt_share': round((bank + deb) / COST * 100),
        'dscr': [d2(n / ds) for n in NOI],
        'dscr_on_k': [d2(n / (ds_k * 1000.0)) for n in NOI],
        'cash_after_ds': [n - ds for n in NOI],
        'coc': [(n - ds) / eq for n in NOI],
        'bank_bal10': balance(bank, BANK_RATE, BANK_YEARS, 12 * HOLD_YEARS),
        'deb_bal10': balance(deb, DEB_RATE, DEB_YEARS, 12 * HOLD_YEARS),
    }
    return out


def verify_inputs():
    """The case's own arithmetic: uses sum to the cost, the stack sums to 100%, the Year-3 NOI build adds up."""
    problems = []
    if abs(sum(USES.values()) * 1e6 - COST) > 1:
        problems.append('uses do not sum to $5.00M: %s' % sum(USES.values()))
    for s in (BEFORE, AFTER):
        if abs(s['bank'] + s['deb'] + s['eq'] - 1) > 1e-9:
            problems.append('%s stack does not sum to 100%%' % s['name'])
    gpr = NOI_BUILD['canopy'] + NOI_BUILD['open'] + NOI_BUILD['enclosed']
    egi = gpr * (1 - NOI_BUILD['vacancy_pct']) + NOI_BUILD['ancillary']
    noi3 = egi * (1 - NOI_BUILD['expense_ratio'])
    # the page rounds each build line to $0.1k, so compare at that grain
    if round(gpr / 1e3, 1) != 957.6 or round(egi / 1e3, 1) != 925.0 or abs(noi3 - NOI[2]) > 6_000:
        problems.append('NOI build does not reproduce: gpr %.1f egi %.1f noi %.1f' % (gpr / 1e3, egi / 1e3, noi3 / 1e3))
    return problems, gpr, egi, noi3


def verify_before(b):
    """BEFORE must reproduce the published figures."""
    bad = []
    if (b['bank_ds_k'], b['deb_ds_k'], b['ds_k']) != (PUBLISHED_BEFORE['bank_ds_k'], PUBLISHED_BEFORE['deb_ds_k'],
                                                      PUBLISHED_BEFORE['ds_k']):
        bad.append('debt service %s/%s/%s != published' % (b['bank_ds_k'], b['deb_ds_k'], b['ds_k']))
    if tuple(b['dscr']) != PUBLISHED_BEFORE['dscr'] or tuple(b['dscr_on_k']) != PUBLISHED_BEFORE['dscr']:
        bad.append('DSCR %s / %s != published %s' % (b['dscr'], b['dscr_on_k'], PUBLISHED_BEFORE['dscr']))
    if (money_m(b['bank']), money_m(b['deb']), money_m(b['eq']), b['debt_share']) != (
            PUBLISHED_BEFORE['bank_amt'], PUBLISHED_BEFORE['deb_amt'], PUBLISHED_BEFORE['eq_amt'],
            PUBLISHED_BEFORE['debt_share']):
        bad.append('sources != published')
    return bad


# ----------------------------------------------------------------------------------------------------- IRR diagnostics
def npv(rate, cfs):
    return sum(c / (1 + rate) ** t for t, c in enumerate(cfs))


def irr_roots(cfs):
    """All real IRRs between -90% and +500%, found by sign change on a grid and refined by bisection."""
    roots, step = [], 0.0025
    a = -0.90
    fa = npv(a, cfs)
    while a < 5.0:
        b = a + step
        fb = npv(b, cfs)
        if fa == 0:
            roots.append(a)
        elif fa * fb < 0:
            lo, hi = a, b
            for _ in range(80):
                mid = (lo + hi) / 2
                if npv(lo, cfs) * npv(mid, cfs) <= 0:
                    hi = mid
                else:
                    lo = mid
            roots.append((lo + hi) / 2)
        a, fa = b, fb
    return roots


def noi_path(g):
    path = list(NOI)
    for _ in range(4, HOLD_YEARS + 1):
        path.append(path[-1] * (1 + g))
    return path


def levered_cfs(st, g, exit_price, sale_cost=0.0, y1='reserve'):
    """Equity cash flows: -equity at close; NOI less debt service each year; Year 10 adds the sale net of costs and
    the two loan balances. y1='reserve': the Year-1 shortfall is paid from the funded lease-up reserve (page text:
    'covered by the funded lease-up reserve'), so Year-1 cash to equity is zero. y1='outflow': the shortfall is a
    Year-1 equity outflow."""
    path = noi_path(g)
    cfs = [-st['eq']]
    for y, n in enumerate(path):
        cf = n - st['ds']
        if y == 0 and y1 == 'reserve' and cf < 0:
            cf = 0.0
        cfs.append(cf)
    cfs[-1] += exit_price * (1 - sale_cost) - st['bank_bal10'] - st['deb_bal10']
    return cfs


def unlevered_irr(g, cap):
    path = noi_path(g)
    cfs = [-float(COST)] + path[:]
    cfs[-1] += path[-1] * (1 + g) / cap
    r = irr_roots(cfs)
    return r[0] if r else None


def fmt_roots(r):
    return 'none' if not r else ', '.join('%.1f%%' % (x * 100) for x in r)


def irr_diagnostics(b, a):
    lines = []
    lines.append('IRR DIAGNOSTICS (not figures on the page; the page keeps its published ~16%)')
    # 1. What the Year-10 sale must deliver to equity for BEFORE to earn 16%
    lines.append('  1. BEFORE (10%% equity): net Year-10 sale proceeds to equity that make the levered IRR exactly 16%%. '
                 'A negative number means the owner pays to sell. Going-in yield on cost is %.1f%%; the page quotes '
                 'market caps of 6.0-8.5%%.' % (NOI[2] / COST * 100))
    for g in (0.0, 0.02, 0.03):
        cfs0 = levered_cfs(b, g, exit_price=0.0)
        pv_ops = sum(c / (1 + IRR_PUBLISHED) ** t for t, c in enumerate(cfs0[1:], start=1)) \
            + (b['bank_bal10'] + b['deb_bal10']) / (1 + IRR_PUBLISHED) ** HOLD_YEARS      # Years 1-10 cash, no sale
        need_net = (b['eq'] - pv_ops) * (1 + IRR_PUBLISHED) ** HOLD_YEARS
        need_price = need_net + b['bank_bal10'] + b['deb_bal10']
        n11 = noi_path(g)[-1] * (1 + g)
        lines.append('     growth %.0f%%: Years 1-10 cash after debt service is worth $%.0fk at 16%% against $%.0fk of equity; '
                     'net sale proceeds needed $%.0fk = exit price $%.2fM against loan balances $%.2fM (cap %.1f%% on Year-11 NOI)'
                     % (g * 100, pv_ops / 1e3, b['eq'] / 1e3, need_net / 1e3, need_price / 1e6,
                        (b['bank_bal10'] + b['deb_bal10']) / 1e6, n11 / need_price * 100))
        if g == 0.0:
            g0_price = need_price
    # 2. literal procedure: hold that exit price, compute AFTER
    cfs_b = levered_cfs(b, 0.0, g0_price)
    cfs_a = levered_cfs(a, 0.0, g0_price)
    lines.append('  2. Literal procedure (growth 0%%, calibrate the exit, hold it): BEFORE roots %s; AFTER roots %s. The cash flows '
                 'change sign twice, so the IRR is not unique; not usable.' % (
                     fmt_roots(irr_roots(cfs_b)), fmt_roots(irr_roots(cfs_a))))
    # 3. sane-range grid, exit cap inside the page's stated range
    lines.append('  3. Levered equity IRR with the exit cap INSIDE the page\'s stated 6.0-8.5% range '
                 '(growth after Year 3 and sale cost are not on the page; Year-1 shortfall paid from the reserve):')
    lines.append('       growth  exit cap   sale cost   BEFORE (10% equity)   AFTER (15% equity)')
    for g_ in (0.0, 0.02):
        for cap in (0.07, 0.085):
            for sale in (0.0, 0.03):
                n11 = noi_path(g_)[-1] * (1 + g_)
                price = n11 / cap
                rb = irr_roots(levered_cfs(b, g_, price, sale))
                ra = irr_roots(levered_cfs(a, g_, price, sale))
                lines.append('       %4.1f%%   %5.1f%%     %4.1f%%      %-20s  %s' % (
                    g_ * 100, cap * 100, sale * 100, fmt_roots(rb), fmt_roots(ra)))
    # 4. unlevered
    lines.append('  4. Unlevered (project, $5.00M cost, independent of the capital stack) 10-year IRR:')
    for g_ in (0.0, 0.02, 0.03):
        row = []
        for cap in (0.07, 0.075, 0.085):
            row.append('cap %.1f%% -> %.1f%%' % (cap * 100, unlevered_irr(g_, cap) * 100))
        lines.append('       growth %.0f%%: %s' % (g_ * 100, ';  '.join(row)))
    lines.append('     So about 16% is what the PROJECT earns unlevered at a 7.0-8.5% exit and 2-3% growth; the page labels '
                 'it a levered equity IRR. Which one the owner wants on the tile is the open item.')
    return lines


# ----------------------------------------------------------------------------------------------------- report
def expected(a):
    """Every AFTER figure that is on the page, in the page's own format."""
    return {
        'bank_amt': money_m(a['bank']), 'deb_amt': money_m(a['deb']), 'eq_amt': money_m(a['eq']),
        'bank_million': money_million(a['bank']), 'deb_million': money_million(a['deb']),
        'eq_million': money_million(a['eq']),
        'bank_k': money_k(a['bank_ds']), 'deb_k': money_k(a['deb_ds']), 'ds_k': '$%dk' % a['ds_k'],
        'bank_full': money_full(a['bank_ds']), 'deb_full': money_full(a['deb_ds']),
        'ds_full': money_full(a['ds_k'] * 1000),
        'dscr': a['dscr'], 'debt_share': '%d%%' % a['debt_share'],
        'deb_pct': '%d%%' % round(AFTER['deb'] * 100), 'eq_pct': '%d%%' % round(AFTER['eq'] * 100),
    }


def report():
    problems, gpr, egi, noi3 = verify_inputs()
    b, a = structure(BEFORE), structure(AFTER)
    bad = verify_before(b)
    print('Inputs: cost $%.2fM; Year-3 build GPR $%.1fk, EGI $%.1fk, NOI $%.1fk (page ~$615k)' % (
        COST / 1e6, gpr / 1e3, egi / 1e3, noi3 / 1e3))
    for p in problems:
        print('INPUT PROBLEM:', p)
    if bad or problems:
        for x in bad:
            print('BEFORE does not reproduce the page:', x)
        print('Model cannot reproduce the page: not proceeding.')
        return 2
    print('BEFORE reproduces the published figures: debt service $%dk + $%dk = $%dk; DSCR %s (also %s on rounded $k)' % (
        b['bank_ds_k'], b['deb_ds_k'], b['ds_k'], '/'.join(b['dscr']), '/'.join(b['dscr_on_k'])))
    if a['dscr'] != a['dscr_on_k'] or a['ds_k'] != a['ds_k_total']:
        print('WARNING: AFTER rounding conventions disagree', a['dscr'], a['dscr_on_k'], a['ds_k'], a['ds_k_total'])
        return 2
    rows = [
        ('Bank first mortgage (50%)', money_m(b['bank']), money_m(a['bank'])),
        ('CDC / SBA 504 debenture', '%s (40%%)' % money_m(b['deb']), '%s (35%%)' % money_m(a['deb'])),
        ('Borrower equity injection', '%s (10%%)' % money_m(b['eq']), '%s (15%%)' % money_m(a['eq'])),
        ('Sources total', money_m(b['bank'] + b['deb'] + b['eq']), money_m(a['bank'] + a['deb'] + a['eq'])),
        ('Uses total (unchanged)', money_m(COST), money_m(COST)),
        ('SBA 504 debt share (tile)', '%d%%' % b['debt_share'], '%d%%' % a['debt_share']),
        ('Bank debt service /yr', '$%.0f' % b['bank_ds'], '$%.0f' % a['bank_ds']),
        ('Debenture debt service /yr', '$%.0f' % b['deb_ds'], '$%.0f' % a['deb_ds']),
        ('Blended debt service /yr', '$%.0f (page $%dk)' % (b['ds'], b['ds_k']), '$%.0f (page $%dk)' % (a['ds'], a['ds_k'])),
        ('Page line "Annual debt service"', '≈ $%dk ($%dk bank + $%dk debenture)' % (b['ds_k'], b['bank_ds_k'], b['deb_ds_k']),
         '≈ $%dk ($%dk bank + $%dk debenture)' % (a['ds_k'], a['bank_ds_k'], a['deb_ds_k'])),
        ('DSCR Year 1 (NOI ~$382k)', b['dscr'][0], a['dscr'][0]),
        ('DSCR Year 2 (NOI ~$488k)', b['dscr'][1], a['dscr'][1]),
        ('DSCR Year 3 / stabilized (NOI ~$615k)', b['dscr'][2], a['dscr'][2]),
        ('Cash after debt service Y1', '$%.0f' % b['cash_after_ds'][0], '$%.0f' % a['cash_after_ds'][0]),
        ('Cash after debt service Y2', '$%.0f' % b['cash_after_ds'][1], '$%.0f' % a['cash_after_ds'][1]),
        ('Cash after debt service Y3', '$%.0f' % b['cash_after_ds'][2], '$%.0f' % a['cash_after_ds'][2]),
        ('Cash-on-cash Y1 (not on page)', '%.1f%%' % (b['coc'][0] * 100), '%.1f%%' % (a['coc'][0] * 100)),
        ('Cash-on-cash Y2 (not on page)', '%.1f%%' % (b['coc'][1] * 100), '%.1f%%' % (a['coc'][1] * 100)),
        ('Cash-on-cash Y3 (not on page)', '%.1f%%' % (b['coc'][2] * 100), '%.1f%%' % (a['coc'][2] * 100)),
        ('Loan balances after 10 years', '$%.0f' % (b['bank_bal10'] + b['deb_bal10']), '$%.0f' % (a['bank_bal10'] + a['deb_bal10'])),
        ('Levered equity IRR', '~16% (published; not reproducible)', 'left at ~16% on the page (open item)'),
    ]
    w = max(len(r[0]) for r in rows)
    w2 = max(len(r[1]) for r in rows)
    print('\n%-*s  %-*s  %s' % (w, 'Figure', w2, 'BEFORE (10% equity)', 'AFTER (15% equity)'))
    print('-' * (w + w2 + 28))
    for r in rows:
        print('%-*s  %-*s  %s' % (w, r[0], w2, r[1], r[2]))
    print()
    for line in irr_diagnostics(b, a):
        print(line)
    return 0


# ----------------------------------------------------------------------------------------------------- page check
DASHES = re.compile(r'[\u2010-\u2015\u2212\ufe58\ufe63\uff0d]')   # hyphen variants, en dash, em dash, minus, fullwidth
BLOCK_TAGS = re.compile(r'</?(?:p|div|li|ul|ol|tr|td|th|table|thead|tbody|caption|section|aside|nav|header|footer|main|'
                        r'article|h[1-6]|br|blockquote|figure|figcaption|dl|dt|dd)\b[^>]*>', re.I)


def normalize(s):
    s = html.unescape(s)
    s = s.replace(' ', ' ').replace('​', '')
    s = DASHES.sub('-', s)
    return re.sub(r'[ \t\r\f\v]+', ' ', s).strip()


def to_lines(fragment):
    """Visible text of an HTML fragment as a list of normalized lines (one per block element)."""
    f = re.sub(r'<(script|style)\b.*?</\1>', ' ', fragment, flags=re.S | re.I)
    f = re.sub(r'<!--.*?-->', '', f, flags=re.S)                       # drop comment tokens, keep what they wrap
    f = re.sub(r'<sup class="fn">.*?</sup>', '', f, flags=re.S | re.I)  # footnote markers
    f = f.replace('\n', ' ').replace('\r', ' ')                        # source line wraps are not block breaks
    f = BLOCK_TAGS.sub('\n', f)
    f = re.sub(r'<[^>]+>', '', f)                                      # inline tags (a, span, time, em): no space
    lines = [normalize(x) for x in f.split('\n')]
    return [x for x in lines if x]


def one_line(fragment):
    return ' '.join(to_lines(fragment))


def meta_values(src):
    out = {}
    for m in re.finditer(r'<meta\s+([^>]*?)/?>', src, re.I):
        attrs = dict((k.lower(), v) for k, v in re.findall(r'([\w:-]+)\s*=\s*"([^"]*)"', m.group(1)))
        key = attrs.get('name') or attrs.get('property')
        if key and 'content' in attrs:
            out[key] = normalize(attrs['content'])
    return out


def jsonld_blocks(src):
    blocks = []
    for m in re.finditer(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', src, re.S | re.I):
        blocks.append(m.group(1))
    return blocks


def table_rows(src):
    rows = []
    for tr in re.finditer(r'<tr\b[^>]*>(.*?)</tr>', src, re.S | re.I):
        cells = [one_line(c) for c in re.findall(r'<t[dh]\b[^>]*>(.*?)</t[dh]>', tr.group(1), re.S | re.I)]
        if cells:
            rows.append(cells)
    return rows


def sentences(lines):
    out = []
    for ln in lines:
        out.extend(x for x in re.split(r'(?<=[.!?;])\s+(?=[A-Z$~≈(0-9])', ln) if x)
    return out


TEN = re.compile(r'(?<![\d.])10\s?(?:%|percent)(?![\d.])')
EQUITY_CTX = re.compile(r'equity|injection|contribution|minimum|borrower', re.I)
TEN_OK = re.compile(r'7\(a\)|standard|generally|higher for', re.I)


def check():
    a = structure(AFTER)
    ex = expected(a)
    src = PAGE.read_text(encoding='utf-8')
    errors = []

    def need(label, ok):
        if not ok:
            errors.append('MISSING: ' + label)

    def absent(label, text, needle):
        if normalize(needle) in text:
            errors.append('STALE: %s still has %r' % (label, needle))

    body = src[src.index('<body'):]
    body_lines = to_lines(body)
    body_text = ' '.join(body_lines)
    metas = meta_values(src)
    blocks = jsonld_blocks(src)
    jsonld_ok, jsonld_strings = True, []
    for i, blk in enumerate(blocks):
        try:
            data = json.loads(blk)
        except ValueError as e:
            errors.append('JSON-LD block %d does not parse: %s' % (i, e))
            jsonld_ok = False
            continue

        def walk(x):
            if isinstance(x, dict):
                for v in x.values():
                    walk(v)
            elif isinstance(x, list):
                for v in x:
                    walk(v)
            elif isinstance(x, str):
                jsonld_strings.append(normalize(x))
        walk(data)
    alt_text = ' '.join(normalize(x) for x in re.findall(r'\balt="([^"]*)"', src))
    universe = ' '.join([body_text] + list(metas.values()) + jsonld_strings + [alt_text])

    # ---- hero tiles
    nums = [one_line(x) for x in re.findall(r'<div class="stat-num">(.*?)</div>', src, re.S)]
    labels = [one_line(x) for x in re.findall(r'<div class="stat-label">(.*?)</div>', src, re.S)]
    need('four stat tiles', len(nums) == 4 and len(labels) == 4)
    if len(nums) == 4 and len(labels) == 4:
        need('tile 2 number %s' % ex['debt_share'], nums[1] == ex['debt_share'])
        need('tile 2 label "50%% bank + %s CDC of the $5.00M"' % ex['deb_pct'],
             ('50%% bank + %s CDC of the $5.00M' % ex['deb_pct']) in labels[1])
        need('tile 3 number %sx' % ex['dscr'][2], nums[2] == ex['dscr'][2] + 'x')
        need('tile 1 number $5.00M', nums[0] == '$5.00M')
        # Owner ruling of 2026-10-16 (WEB-FSC-6 D27): the IRR now uses the exit at the cap rate the page cites,
        # recomputed by docs/web-fsc-6/recompute/rv-boat-storage-arizona-sba-irr.py, which also checks every IRR place.
        need('tile 4 number ≈28% (owner ruling 2026-10-16, exit at the cited 8.5% cap)', nums[3].replace(' ', '') == '≈28%')

    # ---- capital structure table, DSCR table
    rows = table_rows(src)

    def row_with(prefix):
        for r in rows:
            if r[0].startswith(normalize(prefix)):
                return r
        return None

    spec = [
        ('Bank first mortgage (50%)', ex['bank_amt']),
        ('CDC / SBA 504 debenture (%s)' % ex['deb_pct'], ex['deb_amt']),
        ('Borrower equity injection (%s)' % ex['eq_pct'], ex['eq_amt']),
        ('Total project cost', '$5.00M'),
    ]
    for prefix, val in spec:
        r = row_with(prefix)
        need('table row "%s" = %s' % (prefix, val), bool(r) and r[-1] == val)
    r = row_with('Annual debt service (blended)')
    want = '≈ %s (%s bank + %s debenture)' % (ex['ds_k'], ex['bank_k'], ex['deb_k'])
    need('table row Annual debt service = %s' % want, bool(r) and re.sub(r'\s+', ' ', r[-1]) == want)
    for i, yr in enumerate(('Year 1', 'Year 2', 'Year 3')):
        r = row_with(yr)
        want = ['~$%dk' % (NOI[i] // 1000), '~%s' % ex['ds_k'], ex['dscr'][i]]
        need('DSCR row %s: NOI/debt service/DSCR = %s' % (yr, ' | '.join(want)), bool(r) and r[-4:-3] != [] and
             r[-3:] == want)

    # ---- prose
    prose = [
        'the %s bank note at an illustrative 9.5 percent costs about %s a year' % (ex['bank_million'], ex['bank_full']),
        'the %s CDC debenture at an illustrative 6.5 percent fixed costs about %s' % (ex['deb_million'], ex['deb_full']),
        'blended annual debt service near %s' % ex['ds_full'],
        'stabilized %sx in Year 3' % ex['dscr'][2],
        'DSCR computed as NOI divided by the ~%s blended annual debt service' % ex['ds_k'],
        'The stabilized %sx coverage' % ex['dscr'][2],
        'covers fully amortizing debt service at %sx' % ex['dscr'][1],
        'The Year-1 figure of %sx' % ex['dscr'][0],
        'the %s injection' % ex['eq_million'],
        'a stabilized %sx DSCR that clears' % ex['dscr'][2],
    ]
    for p in prose:
        need('text "%s"' % p, normalize(p) in body_text)

    # ---- meta, og, json-ld descriptions
    need('meta description has "%sx stabilized DSCR"' % ex['dscr'][2],
         '%sx stabilized DSCR' % ex['dscr'][2] in metas.get('description', ''))
    need('og:description has "%sx DSCR"' % ex['dscr'][2], '%sx DSCR' % ex['dscr'][2] in metas.get('og:description', ''))
    need('JSON-LD Article description has "%sx stabilized DSCR"' % ex['dscr'][2],
         any('%sx stabilized DSCR' % ex['dscr'][2] in s for s in jsonld_strings))

    # ---- the tier, stated correctly, with its source
    tier_ok = any(('New Business' in s and '15%' in s.replace(' percent', '%') and '120.910' in s) for s in sentences(body_lines))
    need('a sentence stating the 15% New Business tier under 13 CFR 120.910', tier_ok)
    need('a sentence saying the 10 percent start-up figure is the 7(a) rule',
         any(('start-up' in s and '7(a) rule' in s and '10 percent' in s) for s in sentences(body_lines)))
    need('source id="s20" for 13 CFR 120.910', bool(re.search(r'<li id="s20">13 CFR 120\.910, Borrower contributions', src)))
    need('source text of s20', normalize(
        '13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), '
        'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910') in
        ' '.join(to_lines(src[src.index('id="sources"'):])))
    need('footnote marker pointing at #s20', 'href="#s20"' in src)
    need('sources s1..s20 present once each', all(len(re.findall(r'<li id="s%d">' % n, src)) == 1 for n in range(1, 21)))

    # ---- stale figures (old structure), anywhere in text, meta, JSON-LD, alt
    for needle in ('$424k', '$424,000', '$162k', '$162,000', '$2.00M', '$2.00 million', '$0.50M', '$0.50 million',
                   '1.45x', '1.15x', '0.90x', '50% bank + 40% CDC', 'debenture (40%)', 'injection (10%)',
                   'standard SBA 504 split', 'SBA-minimum 10', 'SBA-minimum'):
        absent('page', universe, needle)

    # ---- no sentence states 10% as this project's equity or as the 504 minimum for it
    for s in sentences(body_lines) + sentences(list(metas.values())) + sentences(jsonld_strings):
        if TEN.search(s) and EQUITY_CTX.search(s) and not TEN_OK.search(s):
            errors.append('STALE TIER: sentence states 10%% as equity or minimum without the 7(a)/standard qualifier: %r'
                          % s[:160])
        if TEN.search(s) and re.search(r'start-?ups?', s, re.I) and not re.search(r'7\(a\)|higher for', s):
            errors.append('STALE TIER: 10%% start-up figure not attributed to 7(a): %r' % s[:160])
        if re.search(r'restored for start-ups', s, re.I) and not re.search(r'7\(a\)', s):
            errors.append('STALE TIER: "restored for start-ups" without 7(a): %r' % s[:160])

    # ---- information only
    irr_places = len(re.findall(r'(?:≈|~|near )\s?28\s?(?:%|percent)', universe))
    print('info: IRR at ~28%% in %d place(s), owner ruling 2026-10-16 (docs/web-fsc-6/recompute/rv-boat-storage-arizona-sba-irr.py)' % irr_places)
    print('info: JSON-LD blocks parsed: %d (%s)' % (len(blocks), 'ok' if jsonld_ok else 'ERROR'))

    if errors:
        print('--check FAILED, %d mismatch(es):' % len(errors))
        for e in errors:
            print('  ' + e)
        return 1
    print('--check OK: every AFTER figure is on the page in the page\'s format and no sentence states the old tier')
    return 0


if __name__ == '__main__':
    args = sys.argv[1:]
    if '--page' in args:                      # test hook: check another copy of the page (for example a swept copy)
        PAGE = Path(args[args.index('--page') + 1])
    if '--check' in args:
        sys.exit(check())
    sys.exit(report())
