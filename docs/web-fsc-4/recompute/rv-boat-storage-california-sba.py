#!/usr/bin/env python3
"""RV and boat storage California (SBA 504, ground-up): borrower contribution recompute to 15 percent.

Page: case-studies/rv-boat-storage-california-sba/index.html   (lane WEB-FSC-4, owner ruling)

THE RULE (13 CFR 120.910, unchanged in SOP 50 10 8.1; register row R31, data/regulatory/sba.json equity.sba_504_*):
the 504 borrower contributes at least 10% of project cost in standard cases; at least 15% if the Borrower (or the
Operating Company) has operated for two years or less (a New Business) OR the project is a limited or special purpose
building; at least 20% if both. The page financed this ground-up storage business at 10% and called it an SBA baseline
(or the SOP 50 10 8.1 start-up figure). That 10% start-up figure is the 7(a) Start-Up Business rule (R29), not a 504
rule. A ground-up storage business is a New Business, so the floor is 15%. RV and boat storage is not on SBA's special
purpose example list, and the page itself argues the yard is mixed-format and unlikely to draw a special purpose
designation, so the 20% tier is not claimed. The 504 stack at 15% is Third Party Lender 50% / CDC debenture 35% /
borrower 15%. (120.910 measures the percentage of project cost excluding administrative costs; the case has no
administrative-cost line, so 15% is applied to the full $6.10M, the same base the page used for 10%.)

CASE INPUTS (all from the page, unchanged; the bank loan stays 50% of cost, only the debenture shrinks by 5 points):
  cost $6.10M (uses table); bank 9.5% / 25 yr; debenture fixed 6.5% / 25 yr; monthly amortization;
  NOI Y1 $466k, Y2 $595k, Y3 $750k (DSCR table; Y3 from the NOI build, EGI $1.072M less opex $0.322M);
  hold 10 years, untrended stabilized NOI, exit at a 7.5% cap (financing prose).

REPRODUCTION OF THE PAGE (BEFORE, 50/40/10): bank $3.05M -> $319.8k, debenture $2.44M -> $197.7k, total $517.5k
(page: ~$320k + ~$198k = about $517k); DSCR 466/517.5 = 0.90, 595/517.5 = 1.15, 750/517.5 = 1.45 (page: 0.90, 1.15,
1.45). The model reproduces every published debt-service and coverage figure, with standard monthly amortization.

DOLLAR FORMAT. At 15% the debenture is $2.135M and the equity $0.915M exactly; at the page's two-decimal convention
they would round to $2.14M and $0.92M, which sum to $6.11M against a $6.10M total. The page already uses three
decimals where needed ($0.089M, $1.116M), so the two split lines are printed to three decimals and the table foots.

IRR (levered equity, 10-year hold). The page's stated exit determines the figure, so the IRR is recomputed, not held.
Stated on the page: 10-year hold; stabilized NOI untrended after Year 3 ($750k); sale at a normalized exit rate of about
7.5%, a gross value near $10.0M; net of selling costs and the outstanding 504 balance; blended with the graded lease-up
(Y1 shortfall paid from the funded lease-up and interest reserve, so the Y1 distribution is zero; Y2 onward NOI less debt
service). Not stated on the page: the selling cost. ONE ASSUMPTION IS ADDED: selling costs of 3% of the gross value
(SELL = 0.03), the single unstated input, chosen in the middle of the 0% to 5% band. Equity is the page's own (BEFORE
$0.61M, AFTER $0.915M) and the exit nets the loan balances left after 120 monthly payments. Result at 3%: BEFORE 35.8%,
AFTER 29.8%. Sensitivity: AFTER is 30.2% at 0%, 29.9% at 2%, 29.8% at 3%, 29.5% at 5% (29.48%, which is 29 as an
integer; 0%, 2% and 3% round to 30), so the whole 0% to 5% band lies between 29.5% and 30.2% and the page states it as
"near 30 percent" in the prose and as 30% (the figure at 3%) in the tile and descriptions. The page previously published about 16% (BEFORE structure), which its own stated
exit cannot produce: the present value at 16% of the BEFORE operating distributions alone (about $0.81M) already exceeds
the $0.61M of equity, so the IRR exceeds 16% for ANY non-negative exit equity, and only an exit cap above 17%, against the
page's own 7.5% and 6.0 to 8.5% range, would give 16%. That earlier figure was false by the page's own derivation and is
replaced. Cash-on-cash is not published on the page; it is printed for the log only.

USAGE
  python3 docs/web-fsc-4/recompute/rv-boat-storage-california-sba.py            print BEFORE / AFTER and the IRR analysis
  python3 docs/web-fsc-4/recompute/rv-boat-storage-california-sba.py --check    exit 1 listing every mismatch with the page
                                                                                  (including any remaining 16% IRR)
  (--page PATH reads another copy of the page, used to test the check)
"""
import html
import json
import os
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
PAGE = os.path.join(ROOT, 'case-studies', 'rv-boat-storage-california-sba', 'index.html')

# ---------------------------------------------------------------- case inputs (page location in each comment)
USES = [  # "Project cost breakdown" table, Financing section
    ('Land (~11 acres, inland California)', 1.60e6),
    ('Site work, grading, drainage & paving', 1.35e6),
    ('Canopy structures & enclosed buildings (steel)', 1.85e6),
    ('Security, access control & perimeter', 0.35e6),
    ('Utilities & site lighting', 0.30e6),
    ('Soft costs (A&E, permits, entitlement)', 0.35e6),
    ('Contingency', 0.20e6),
    ('Lease-up & interest reserve', 0.10e6),
]
COST = sum(v for _, v in USES)                  # table total, "Total project cost $6.10M"
BANK_RATE, BANK_YEARS = 0.095, 25               # "Bank first mortgage ... 25-yr amortization, ~9.5%"
DEB_RATE, DEB_YEARS = 0.065, 25                 # "CDC / SBA 504 debenture ... 25-yr, fixed ~6.5%"
NOI = [466e3, 595e3, 750e3]                     # "Debt-service coverage ramp" table, Years 1 to 3
OCC = [62, 78, 92]                              # same table, average occupancy
EXIT_CAP = 0.075                                # financing prose: normalized exit rate around 7.5 percent
HOLD = 10                                       # stat tile and prose: 10-year hold
SELL = 0.03                                     # selling cost, NOT stated on the page: the one added assumption (docstring)
PUBLISHED_IRR_BEFORE = 16                       # what the page said before this fix; false by its own stated exit

BEFORE = {'bank': 0.50, 'deb': 0.40, 'eq': 0.10}    # as published
AFTER = {'bank': 0.50, 'deb': 0.35, 'eq': 0.15}     # 13 CFR 120.910 New Business tier

# What the page published before this lane (used only to prove the model reproduces the page).
PUBLISHED_BEFORE = {'bank_k': 320, 'deb_k': 198, 'ds_k': 517, 'dscr': [0.90, 1.15, 1.45],
                    'bank_m': '3.05', 'deb_m': '2.44', 'eq_m': '0.61'}


# ---------------------------------------------------------------- finance
def const(rate, years):
    """Annual loan constant for monthly amortization: 12 * payment per dollar borrowed."""
    r = rate / 12
    n = years * 12
    return 12 * r / (1 - (1 + r) ** -n)


def balance(principal, rate, years, paid_months):
    r = rate / 12
    pmt = principal * const(rate, years) / 12
    return principal * (1 + r) ** paid_months - pmt * ((1 + r) ** paid_months - 1) / r


def rhu(x, nd):
    """Round half up to nd decimals (Decimal on the repr so 2.135 stays 2.135)."""
    q = Decimal(1).scaleb(-nd)
    return Decimal(repr(round(x, 9))).quantize(q, rounding=ROUND_HALF_UP)


def figures(split):
    f = {}
    f['bank'] = COST * split['bank']
    f['deb'] = COST * split['deb']
    f['eq'] = COST * split['eq']
    f['ltc'] = split['bank'] + split['deb']
    f['bank_ds'] = f['bank'] * const(BANK_RATE, BANK_YEARS)
    f['deb_ds'] = f['deb'] * const(DEB_RATE, DEB_YEARS)
    f['ds'] = f['bank_ds'] + f['deb_ds']
    f['dscr'] = [n / f['ds'] for n in NOI]
    f['cf'] = [n - f['ds'] for n in NOI]
    f['coc'] = f['cf'][2] / f['eq']                      # stabilized cash-on-cash, log only
    f['bal10'] = (balance(f['bank'], BANK_RATE, BANK_YEARS, 12 * HOLD)
                  + balance(f['deb'], DEB_RATE, DEB_YEARS, 12 * HOLD))
    return f


def irr(cfs):
    f = lambda r: sum(c / (1 + r) ** i for i, c in enumerate(cfs))
    lo, hi = -0.95, 10.0
    if f(lo) * f(hi) > 0:
        return None
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def equity_cashflows(fig, exit_cap=EXIT_CAP, sell=SELL):
    noi = NOI + [NOI[-1]] * (HOLD - len(NOI))             # untrended after Year 3
    cfs = [-fig['eq']]
    for t, n in enumerate(noi, start=1):
        d = n - fig['ds']
        if t == 1:
            d = max(d, 0.0)                                # Y1 shortfall paid from the funded lease-up reserve
        cfs.append(d)
    cfs[-1] += NOI[-1] / exit_cap * (1 - sell) - fig['bal10']
    return cfs


def solve(fn, lo, hi, target):
    def g(x):
        v = fn(x)
        return (-1.0 if v is None else v) - target
    flo, fhi = g(lo), g(hi)
    if flo * fhi > 0:
        return None
    for _ in range(200):
        mid = (lo + hi) / 2
        fm = g(mid)
        if flo * fm <= 0:
            hi, fhi = mid, fm
        else:
            lo, flo = mid, fm
    return (lo + hi) / 2


def page_irr():
    """AFTER levered equity IRR on the stated exit at SELL, as the integer percent the page prints."""
    return int(rhu(100 * irr(equity_cashflows(figures(AFTER))), 0))


# ---------------------------------------------------------------- page formats
def k(x):            # "$493k"
    v = rhu(abs(x) / 1e3, 0)
    return '%s$%dk' % ('-' if x < 0 else '', v)


def kk(x):           # "$493,000" (prose rounds to the thousand)
    return '$%s' % format(int(rhu(x / 1e3, 0)) * 1000, ',')


def m(x, nd):        # "$2.135M"
    return '$%sM' % rhu(x / 1e6, nd)


def d2(x):           # "1.52"
    return '%s' % rhu(x, 2)


def expected(after):
    """Every AFTER figure the page must show, in the page's own formats."""
    e = {}
    e['bank_m'] = m(after['bank'], 2)            # $3.05M (unchanged)
    e['deb_m'] = m(after['deb'], 3)              # $2.135M
    e['eq_m'] = m(after['eq'], 3)                # $0.915M
    e['ltc'] = '%d' % rhu(after['ltc'] * 100, 0)  # 85
    e['bank_k'] = k(after['bank_ds'])            # $320k
    e['deb_k'] = k(after['deb_ds'])              # $173k
    e['ds_k'] = k(after['ds'])                   # $493k
    e['bank_kk'] = kk(after['bank_ds'])          # $320,000
    e['deb_kk'] = kk(after['deb_ds'])            # $173,000
    e['ds_kk'] = kk(after['ds'])                 # $493,000
    e['dscr'] = [d2(x) for x in after['dscr']]   # 0.95 1.21 1.52
    return e


# ---------------------------------------------------------------- page text
DASHES = '\u2010\u2011\u2012\u2013\u2014\u2015\u2212\u2043\ufe58\ufe63\uff0d'
INLINE = {'a', 'span', 'sup', 'sub', 'time', 'em', 'strong', 'b', 'i', 'cite', 'abbr', 'small', 'mark', 'code', 'u', 's'}


def norm(s):
    """Decode entities, unify every dash/hyphen variant to '-' (no spaces around it), collapse whitespace."""
    s = html.unescape(s)
    s = re.sub('[' + DASHES + ']', '-', s)
    s = s.replace('\xa0', ' ').replace('\u2009', ' ').replace('\u202f', ' ').replace('\u200b', '')
    s = re.sub(r'\s+', ' ', s)
    s = re.sub(r'\s*-\s*', '-', s)
    return s.strip()


class Visible(HTMLParser):
    """Body text with tags stripped: inline tags add nothing, block tags add a space, footnote markers are dropped.
    Also keeps the text of each block element (cell, paragraph, list item, caption) for the sentence scan."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.out = []
        self.blocks = []
        self.cur = []
        self.skip = []      # stack of tags whose content is dropped
        self.in_body = False

    def flush(self):
        if self.cur:
            self.blocks.append(''.join(self.cur))
            self.cur = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == 'body':
            self.in_body = True
        if tag in ('script', 'style') or (tag == 'sup' and 'fn' in (a.get('class') or '').split()):
            self.skip.append(tag)
            return
        if tag not in INLINE:
            self.out.append(' ')
            self.flush()

    def handle_endtag(self, tag):
        if self.skip and self.skip[-1] == tag:
            self.skip.pop()
            return
        if tag not in INLINE:
            self.out.append(' ')
            self.flush()

    def handle_data(self, data):
        if self.in_body and not self.skip:
            self.out.append(data)
            self.cur.append(data)


def parse_page(src):
    p = Visible()
    p.feed(src)
    p.flush()
    return norm(''.join(p.out)), [norm(b) for b in p.blocks if b.strip()]


def visible_text(src):
    return parse_page(src)[0]


SENTENCE_END = re.compile(r'(?<=[.!?])\s+(?=[A-Z$~(\u2248])')


def meta_values(src):
    vals = {}
    for key, pat in (('description', r'<meta\s+name="description"\s+content="([^"]*)"'),
                     ('og:description', r'<meta\s+property="og:description"\s+content="([^"]*)"')):
        mm = re.search(pat, src)
        vals[key] = norm(mm.group(1)) if mm else ''
    return vals


def jsonld_blocks(src):
    return re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', src, re.S)


# ---------------------------------------------------------------- the check
def run_check(page_path):
    src = open(page_path, encoding='utf-8').read()
    vis, blocks = parse_page(src)
    after = figures(AFTER)
    e = expected(after)
    bad = []

    def need(label, literal, text=None):
        if norm(literal) not in (vis if text is None else text):
            bad.append('MISSING  %s: %r' % (label, literal))

    def forbid(label, literal, text=None):
        if norm(literal) in (vis if text is None else text):
            bad.append('STALE    %s: %r still on the page' % (label, literal))

    def forbid_re(label, pattern, text=None):
        mm = re.search(pattern, vis if text is None else text)
        if mm:
            bad.append('STALE    %s: %r still on the page' % (label, mm.group(0)))

    # stat tiles
    need('stat tile financing share', '%s%% SBA 504 financing (50%% bank + 35%% CDC/SBA debenture)' % e['ltc'])
    need('stat tile DSCR', '%sx Stabilized DSCR (Year 3)' % e['dscr'][2])
    irr_pct = page_irr()
    need('stat tile IRR', '\u2248%d%% Illustrative levered equity IRR, %d-year hold' % (irr_pct, HOLD))
    # capital structure table
    need('table bank', 'Bank first mortgage (50%%) %s' % e['bank_m'])
    need('table debenture', 'CDC / SBA 504 debenture (35%%) %s' % e['deb_m'])
    need('table equity', 'Borrower equity injection (15%%) %s' % e['eq_m'])
    need('table total', 'Total project cost %s' % m(COST, 2))
    need('table debt service', 'Annual debt service (stabilized) \u2248 %s (bank ~%s + debenture ~%s)'
         % (e['ds_k'], e['bank_k'], e['deb_k']))
    need('table-source split', '50% bank first / 35% CDC debenture / 15% equity')
    # prose
    need('prose debenture', 'The %s million CDC debenture' % e['deb_m'].rstrip('M'))
    need('prose blended debt service', 'blended annual debt service is about %s' % e['ds_kk'])
    need('prose bank debt service', 'a bank first near %s' % e['bank_kk'])
    need('prose debenture debt service', 'a 504 debenture near %s' % e['deb_kk'])
    need('prose equity injection', 'the %s million injection earns free cash flow' % e['eq_m'].rstrip('M'))
    # DSCR table and text
    need('DSCR caption', 'full amortizing debt service of about %s' % e['ds_k'])
    need('DSCR source note', 'the ~%s full amortizing annual debt service' % e['ds_k'])
    for i, (stage, noi, occ) in enumerate((('Lease-up', '~$466k', '~62%'), ('Building', '~$595k', '~78%'),
                                           ('Stabilized', '~$750k', '~92%')), start=1):
        need('DSCR table Year %d' % i, 'Year %d %s %s %s %s' % (i, stage, occ, noi, e['dscr'][i - 1]))
    need('prose stabilized coverage', 'The stabilized %sx coverage' % e['dscr'][2])
    need('prose Year 1 coverage', 'Year 1 posts %sx' % e['dscr'][0])
    need('verdict capsule', '%sx DSCR across a graded lease-up' % e['dscr'][2])
    need('verdict capsule IRR', '~%d%% illustrative levered equity IRR' % page_irr())
    need('prose IRR', 'levered equity IRR lands near %d percent over a 10-year hold' % page_irr())
    # head: meta, og, JSON-LD (attributes are not visible text)
    mv = meta_values(src)
    for key in ('description', 'og:description'):
        if '%sx' % e['dscr'][2] not in mv[key]:
            bad.append('MISSING  %s: %sx' % (key, e['dscr'][2]))
        if '~%d%%' % irr_pct not in mv[key]:
            bad.append('MISSING  %s: IRR ~%d%%' % (key, irr_pct))
    ld_blocks = jsonld_blocks(src)
    article = None
    for b in ld_blocks:
        try:
            data = json.loads(b)
        except ValueError as ex:
            bad.append('INVALID  JSON-LD block does not parse: %s' % ex)
            continue
        for node in data.get('@graph', [data]):
            if node.get('@type') == 'Article':
                article = node
    if article is None:
        bad.append('MISSING  JSON-LD Article node')
    else:
        desc = norm(article.get('description', ''))
        if '%sx' % e['dscr'][2] not in desc:
            bad.append('MISSING  JSON-LD Article.description: %sx' % e['dscr'][2])
        if '~%d%%' % irr_pct not in desc:
            bad.append('MISSING  JSON-LD Article.description: IRR ~%d%%' % irr_pct)
    # stale published figures (BEFORE structure and its dependants)
    old = {
        'old debt service $517k': '$517k', 'old debt service $517,000': '$517,000',
        'old debenture debt service $198k': '$198k', 'old debenture debt service $198,000': '$198,000',
        'old debenture $2.44M': '$2.44M', 'old debenture $2.44 million': '$2.44 million',
        'old equity $0.61M': '$0.61M', 'old equity $0.61 million': '$0.61 million',
        'old debenture share (40%)': '(40%)', 'old 40% debenture': '40% CDC',
        'old 10% equity in the stack': '/ 10% equity', 'old financing share 90%': '90% SBA 504',
        'old standard stack caption': 'standard SBA 504 stack',
        'old baseline sentence': '10 percent SBA baseline', 'old standard 10 percent': 'standard 10 percent',
    }
    for label, lit in old.items():
        forbid(label, lit)
    for label, pat in (('old stabilized DSCR 1.45', r'(?<![\d.])1\.45(?!\d)'), ('old Year 1 DSCR 0.90', r'(?<![\d.])0\.90(?!\d)'),
                       ('old Year 2 DSCR 1.15x', r'Year 2 Building ~78% ~\$595k 1\.15(?!\d)')):
        forbid_re(label, pat)
        for key in ('description', 'og:description'):
            forbid_re(label + ' in ' + key, pat, mv[key])
        if article is not None:
            forbid_re(label + ' in JSON-LD description', pat, norm(article.get('description', '')))
    # the earlier ~16% IRR (and 'mid-teens') must not survive anywhere: visible text, meta, og, JSON-LD
    irr16 = r'(?<![\d.])%d(?:\.0)? ?(?:%%|percent)' % PUBLISHED_IRR_BEFORE
    forbid_re('old IRR %d%% in the text' % PUBLISHED_IRR_BEFORE, irr16)
    forbid('old IRR wording', 'mid-teens')
    for key in ('description', 'og:description'):
        forbid_re('old IRR %d%% in %s' % (PUBLISHED_IRR_BEFORE, key), irr16, mv[key])
    if article is not None:
        forbid_re('old IRR %d%% in JSON-LD description' % PUBLISHED_IRR_BEFORE, irr16, norm(article.get('description', '')))
    # tier statements: 15% New Business tier cited to 13 CFR 120.910, with its source entry and footnote
    if not re.search(r'equity injection is 15(?:%| percent), the 504 minimum for a New Business', vis):
        bad.append('MISSING  tier sentence: "equity injection is 15%/15 percent, the 504 minimum for a New Business"')
    if vis.count('13 CFR 120.910') < 2:
        bad.append('MISSING  13 CFR 120.910 must appear in the prose and in the source list')
    if not re.search(r'<li id="s18">13 CFR 120\.910, Borrower contributions', src):
        bad.append('MISSING  source entry s18 for 13 CFR 120.910')
    if 'href="#s18"' not in src:
        bad.append('MISSING  footnote marker pointing at #s18')
    if not re.search(r'start-up figure in SOP 50 10 8\.1 is the 7\(a\) rule', vis):
        bad.append('MISSING  sentence saying the 10 percent start-up figure is the 7(a) rule')
    for fn in sorted(set(re.findall(r'href="#(s\d+)"', src))):
        if 'id="%s"' % fn not in src:
            bad.append('BROKEN   footnote target #%s has no matching id' % fn)
    # no sentence may still state 10% as this project's equity or as the 504 minimum for it
    pct10 = re.compile(r'(?<![\d.])10(?:\.0)? ?(?:%|percent)')
    pct15 = re.compile(r'(?<![\d.])15(?:\.0)? ?(?:%|percent)')
    pct20 = re.compile(r'(?<![\d.])20(?:\.0)? ?(?:%|percent)')
    for block in blocks:
        for sent in SENTENCE_END.split(block):
            if not pct10.search(sent):
                continue
            equityish = re.search(r'equity|injection|contribut|baseline|borrower|504|minimum', sent, re.I)
            exempt = re.search(r'7\(a\)|start-?up business|start-?up figure', sent, re.I) or (pct15.search(sent) and pct20.search(sent))
            if equityish and not exempt:
                bad.append('OLD TIER 10%% stated as equity or the 504 minimum: %s' % sent.strip()[:220])
    return bad


# ---------------------------------------------------------------- report
def report():
    b, a = figures(BEFORE), figures(AFTER)
    pb = PUBLISHED_BEFORE
    ok = (m(b['bank'], 2).lstrip('$').rstrip('M') == pb['bank_m'] and m(b['deb'], 2).lstrip('$').rstrip('M') == pb['deb_m']
          and m(b['eq'], 2).lstrip('$').rstrip('M') == pb['eq_m']
          and int(rhu(b['bank_ds'] / 1e3, 0)) == pb['bank_k'] and int(rhu(b['deb_ds'] / 1e3, 0)) == pb['deb_k']
          and int(rhu(b['ds'] / 1e3, 0)) == pb['ds_k'] and [float(d2(x)) for x in b['dscr']] == pb['dscr'])
    print('uses total', m(COST, 2), '(sum of the eight uses lines)')
    print('BEFORE reproduces the page as published:', 'YES' if ok else 'NO')
    if not ok:
        print('  model cannot reproduce the page; stop')
        return 2
    rows = [
        ('Bank first mortgage (50%)', m(b['bank'], 2), m(a['bank'], 2)),
        ('CDC debenture', '%s (40%%)' % m(b['deb'], 2), '%s (35%%)' % m(a['deb'], 3)),
        ('Borrower equity', '%s (10%%)' % m(b['eq'], 2), '%s (15%%)' % m(a['eq'], 3)),
        ('Sources total', m(b['bank'] + b['deb'] + b['eq'], 2), m(a['bank'] + a['deb'] + a['eq'], 2)),
        ('SBA 504 financing share (tile)', '%d%%' % rhu(b['ltc'] * 100, 0), '%d%%' % rhu(a['ltc'] * 100, 0)),
        ('Bank debt service', k(b['bank_ds']), k(a['bank_ds'])),
        ('Debenture debt service', k(b['deb_ds']), k(a['deb_ds'])),
        ('Annual debt service', k(b['ds']), k(a['ds'])),
        ('DSCR Year 1 (NOI $466k)', d2(b['dscr'][0]), d2(a['dscr'][0])),
        ('DSCR Year 2 (NOI $595k)', d2(b['dscr'][1]), d2(a['dscr'][1])),
        ('DSCR Year 3 (NOI $750k)', d2(b['dscr'][2]), d2(a['dscr'][2])),
        ('Cash after debt service Y1', k(b['cf'][0]), k(a['cf'][0])),
        ('Cash after debt service Y2', k(b['cf'][1]), k(a['cf'][1])),
        ('Cash after debt service Y3', k(b['cf'][2]), k(a['cf'][2])),
        ('Cash-on-cash, stabilized (log only, not on page)', '%s%%' % rhu(b['coc'] * 100, 1), '%s%%' % rhu(a['coc'] * 100, 1)),
        ('Loan balance after 10 years (log only)', m(b['bal10'], 2), m(a['bal10'], 2)),
    ]
    w = max(len(r[0]) for r in rows)
    print('\n%-*s  %-16s %-16s' % (w, 'Figure', 'BEFORE 50/40/10', 'AFTER 50/35/15'))
    for r in rows:
        print('%-*s  %-16s %-16s' % (w, r[0], r[1], r[2]))
    print('\nPage-format AFTER figures the check requires:', json.dumps(expected(a), ensure_ascii=False))

    # ---- IRR analysis
    print('\nIRR (levered equity, %d-year hold, exit at a %.1f%% cap on $%dk = $%.2fM gross, net of selling costs and the 504 balance)'
          % (HOLD, EXIT_CAP * 100, NOI[2] / 1e3, NOI[2] / EXIT_CAP / 1e6))
    print('  selling cost (unstated) :  0%     2%     3%     5%    10%    30%')
    for name, fig in (('BEFORE', b), ('AFTER ', a)):
        print('  %s IRR           ' % name + '  '.join('%5.1f%%' % (100 * irr(equity_cashflows(fig, sell=s)))
                                                       for s in (0, .02, .03, .05, .10, .30)))
    band = [100 * irr(equity_cashflows(a, sell=x / 100.0)) for x in range(0, 6)]
    print('  page figure: selling cost %d%% (added assumption): BEFORE %.1f%%, AFTER %.1f%% -> tile/descriptions %d%%, prose "near %d percent"'
          % (round(SELL * 100), 100 * irr(equity_cashflows(b)), 100 * irr(equity_cashflows(a)), page_irr(), page_irr()))
    print('  AFTER across selling costs 0%% to 5%%: %.1f%% to %.1f%% (all "near %d")' % (min(band), max(band), page_irr()))
    # why the earlier published ~16% was dropped
    ops = equity_cashflows(b, sell=0.0)
    ops[-1] -= NOI[-1] / EXIT_CAP - b['bal10']          # strip the exit equity, keep the operating distributions
    pv_ops = sum(c / 1.16 ** i for i, c in enumerate(ops) if i)
    print('  earlier published ~%d%% (BEFORE): PV at 16%% of BEFORE operating distributions alone $%.3fM > equity $%.3fM, so IRR > 16%% for any exit equity >= 0'
          % (PUBLISHED_IRR_BEFORE, pv_ops / 1e6, b['eq'] / 1e6))
    cap_fit = solve(lambda c: irr(equity_cashflows(b, exit_cap=c)), 0.05, 0.40, PUBLISHED_IRR_BEFORE / 100.0)
    print('  only an exit cap of %s would give %d%% (page says 7.5%%, range 6.0 to 8.5%%): the old figure is replaced'
          % ('none' if cap_fit is None else '%.1f%%' % (100 * cap_fit), PUBLISHED_IRR_BEFORE))
    return 0


def main(argv):
    page = PAGE
    if '--page' in argv:
        page = argv[argv.index('--page') + 1]
    if '--check' in argv:
        bad = run_check(page)
        for line in bad:
            print(line)
        if bad:
            print('%d mismatch(es) in %s' % (len(bad), os.path.relpath(page, ROOT)))
            return 1
        print('OK: every AFTER figure and the 15%% tier statements are on %s' % os.path.relpath(page, ROOT))
        return 0
    return report()


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
