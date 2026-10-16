#!/usr/bin/env python3
"""RV and boat storage Florida (SBA 504, ground-up): recompute at the correct borrower-contribution tier.

Page: case-studies/rv-boat-storage-florida-sba/index.html

The rule. 13 CFR 120.910 (unchanged in SOP 50 10 8.1): the 504 borrower contributes at least 10% in standard cases,
at least 15% if the borrower (or Operating Company) has operated two years or less (a New Business) OR the project is
a limited or special purpose property, and at least 20% if both. At 15% the structure is Third Party Lender 50%,
CDC debenture 35%, borrower 15%. The page published 50/40/10 and called the 10% "the SBA minimum"; the 10% start-up
figure in SOP 50 10 8.1 is the 7(a) Start-Up Business rule (sba.json equity.startup_7a), not a 504 rule. A ground-up
storage business is a New Business. RV and boat storage is not on SBA's special purpose example list, and the page
itself argues the format mix (covered-canopy-led, mixed) is the one LESS likely to draw a special-purpose designation,
so the tier is 15% (not 20%). BEFORE = the published 50/40/10; AFTER = 50/35/15.

Case inputs (unchanged, each from the page section named):
  project cost $5.80M, uses table (Financing, "Project cost breakdown");
  bank first mortgage 50% at ~9.5%, 25-yr amortization, debenture at ~6.5%, 25-yr amortization (Financing, "Capital structure & terms");
  NOI Year 1 ~$444k, Year 2 ~$567k, Year 3 ~$713k, occupancy ~58 / ~74 / ~93% (Outcome, "Debt-service coverage ramp");
  Year 3 revenue build 320 x $195, 120 x $115, 60 x $325 per month, 7% vacancy, $63,000 ancillary, $418,000 opex (Outcome, NOI build);
  10-year hold, "Illustrative levered equity IRR" ~16% (stat tile, Outcome prose).
Payments: monthly level amortization, annual debt service = 12 x monthly payment (the convention that reproduces the page).

What moves: debenture $2.32M -> $2.03M, equity $0.58M -> $0.87M, total 504 debt 90% / $5.22M -> 85% / $4.93M,
debenture debt service $188k -> $164k, combined $492k -> $469k, DSCR by year 0.90 / 1.15 / 1.45 -> 0.95 / 1.21 / 1.52,
debt-service break-even occupancy 64% -> 61% (NOI taken proportional to economic occupancy, as the page does).
What does not: the bank loan and its debt service, every NOI line, the unlevered yield (~12%).

Cash on cash. The page publishes no cash-on-cash figure (the sentence names the concept without a number), so none is
written on the page. It is computed below for the log: stabilized (NOI - debt service) / equity.

IRR: RECOMPUTED FROM THE PAGE'S OWN EXIT RULE. The page gives no exit value or cap rate, but it states the rule: "the exit is
disciplined against replacement cost, flagging any income value more than about 15 percent above the cost to rebuild, which
caps terminal value". Stabilized NOI (about $713,000, a 12 percent yield on the $5.80M cost) capitalized at the 6.0 to 8.5
percent cap rates the page cites is far above 1.15x cost, so the cap binds and the terminal value is 1.15 x the cost to rebuild.
Assumptions, every one stated here:
  * cost to rebuild = the $5.80M project cost (the only cost the page gives; land is included), so terminal value = 1.15 x
    $5.80M = $6.67M (EXIT_MULT, REPLACEMENT_COST);
  * selling costs: the page says the result is "net of ... selling costs" but gives no rate, so SELLING_COST = 0 is used. The
    figure is therefore the page's rule with zero selling costs; 3% / 5% / 6% give AFTER 24.54% / 24.21% / 24.05%;
  * net exit proceeds in Year 10 = terminal value less selling costs less the bank and debenture balances outstanding after
    120 monthly payments (BEFORE $4.22M, AFTER $4.00M);
  * equity in at t0 (BEFORE $0.58M, AFTER $0.87M); years 1 to 10 the equity receives NOI minus combined debt service, floored at
    zero in a year where NOI is below debt service because the page says the financed lease-up reserve bridges the opening
    shortfall; NOI is the table's $444k / $567k / $713k and is held flat at $713k from Year 4 ("holding rents to a
    conservative through-cycle path"); 10-year hold, annual end-of-year flows; IRR = largest real root of the NPV equation.
Result: BEFORE (50/40/10) 30.84%, AFTER (50/35/15) 25.01%, so the page says about 25 percent (tile, meta description, Open Graph
description, JSON-LD description, Outcome prose, verdict). The published "about 16 percent" is NOT what the page's own exit rule
gives for its own structure (30.84%), so it was wrong before this recompute as well as stale. Sensitivities (AFTER): terminal
value at 1.00x cost 22.79% (BEFORE 28.51%); the Year 1 shortfall paid by equity instead of the reserve 24.59%; cost to rebuild
taken as the project cost less the $1.35M land, 20.67%. An earlier attempt calibrated the exit cap rate to reproduce 16% and
needed a 21.03% cap (a sale below the loan balance, negative net proceeds), which contradicts the cap rates the page cites;
it was dropped in favor of the page's stated rule.

Modes:
  python3 rv-boat-storage-florida-sba.py            print BEFORE/AFTER and the reproduction test
  python3 rv-boat-storage-florida-sba.py --check    [--page PATH] read the page; exit 1 listing every mismatch, 0 when every AFTER
                                                    figure above appears on the page in its own format and rounding (the IRR included),
                                                    no stale BEFORE figure remains, and no sentence states 10% as this
                                                    project's equity or as the 504 minimum for it.
Check text is the page with comments (including sba: markers) and footnote markers removed, inline tags removed,
block tags turned into spaces, entities decoded, whitespace collapsed and every dash variant mapped to a hyphen. Snippets
never span an existing em dash, and "~~" in a snippet matches a short run of punctuation, so a later punctuation-only sweep
or links wrapped around words in prose do not break the check.
"""
import html
import json
import re
import sys
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
PAGE = ROOT / 'case-studies' / 'rv-boat-storage-florida-sba' / 'index.html'

# ---------------------------------------------------------------- case inputs
TOTAL_COST = 5_800_000                          # Financing, uses table total ($5.80M)
USES = [1.35, 1.18, 1.47, 0.69, 0.15, 0.27, 0.12, 0.33, 0.24]   # Financing, "Project cost breakdown" ($M)
BANK_PCT = 0.50                                 # Financing, "Bank first mortgage (50%)"
BANK_RATE, BANK_YEARS = 0.095, 25               # Financing, "~9.5%, 25-yr amortization"
DEB_RATE, DEB_YEARS = 0.065, 25                 # Financing, "~6.5%, 25-yr amortization"
STACK_BEFORE = {'bank': 0.50, 'deb': 0.40, 'eq': 0.10}   # published 50/40/10
STACK_AFTER = {'bank': 0.50, 'deb': 0.35, 'eq': 0.15}    # 13 CFR 120.910, New Business: 50/35/15
NOI = [444_000, 567_000, 713_000]               # Outcome, "Debt-service coverage ramp": Year 1, 2, 3 NOI
OCC = [58, 74, 93]                              # same table, economic occupancy %
HOLD = 10                                       # stat tile / Outcome prose: 10-year hold
IRR_PUBLISHED = 16                              # stat tile BEFORE: ~16 % levered equity IRR (not what the page's own exit rule gives)
EXIT_MULT = 1.15                                # Outcome prose: income value flagged "more than about 15 percent above the cost to rebuild"
REPLACEMENT_COST = TOTAL_COST                   # the page gives no rebuild cost; the $5.80M project cost is taken (land included)
SELLING_COST = 0.0                              # page: "net of ... selling costs", no rate given; zero is used (see docstring)
# Year 3 revenue build (Outcome, "Stabilized revenue & NOI build")
RENT = [(320, 195), (120, 115), (60, 325)]      # spaces x $/month: covered, open, enclosed
VACANCY, ANCILLARY, OPEX = 80_400, 63_000, 418_000
# Published BEFORE figures the model must reproduce
PUB = {'bank': 2_900_000, 'deb': 2_320_000, 'eq': 580_000, 'debt_pct': 90, 'debt_m': '5.22',
       'ds_bank_k': 304, 'ds_deb_k': 188, 'ds_k': 492, 'dscr': ['0.90', '1.15', '1.45'], 'be_occ': 64}


# ---------------------------------------------------------------- model
def rnd(x, nd=0):
    q = Decimal(1).scaleb(-nd)
    return Decimal(repr(float(x))).quantize(q, rounding=ROUND_HALF_UP)


def annual_ds(principal, rate, years):
    """Annual debt service = 12 x the level monthly payment of a fully amortizing loan."""
    r = rate / 12
    n = years * 12
    return 12 * principal * r / (1 - (1 + r) ** -n)


def balance(principal, rate, years, months_paid):
    r = rate / 12
    n = years * 12
    pmt = principal * r / (1 - (1 + r) ** -n)
    return principal * (1 + r) ** months_paid - pmt * ((1 + r) ** months_paid - 1) / r


def irr(cfs):
    """Largest real root of NPV(r) = 0 on r > -0.5, or None when none exists (scan then bisect)."""
    f = lambda r: sum(c / (1 + r) ** t for t, c in enumerate(cfs))
    grid = [-0.5 + 0.0025 * i for i in range(0, 1800)]
    root = None
    for x0, x1 in zip(grid, grid[1:]):
        if f(x0) == 0:
            root = x0
        elif f(x0) * f(x1) < 0:
            lo, hi = x0, x1
            for _ in range(80):
                mid = (lo + hi) / 2
                if f(lo) * f(mid) <= 0:
                    hi = mid
                else:
                    lo = mid
            root = (lo + hi) / 2
    return root


def model(stack):
    bank = TOTAL_COST * stack['bank']
    deb = TOTAL_COST * stack['deb']
    eq = TOTAL_COST * stack['eq']
    ds_bank = annual_ds(bank, BANK_RATE, BANK_YEARS)
    ds_deb = annual_ds(deb, DEB_RATE, DEB_YEARS)
    ds = ds_bank + ds_deb
    out = {'bank': bank, 'deb': deb, 'eq': eq, 'debt': bank + deb, 'debt_pct': (bank + deb) / TOTAL_COST * 100,
           'ds_bank': ds_bank, 'ds_deb': ds_deb, 'ds': ds,
           'dscr': [n / ds for n in NOI],
           'be_occ': OCC[2] * ds / NOI[2],              # NOI proportional to occupancy (page: constant ~63% margin)
           'coc': [(n - ds) / eq for n in NOI],
           'fcf': [n - ds for n in NOI],
           'bal10': balance(bank, BANK_RATE, BANK_YEARS, HOLD * 12) + balance(deb, DEB_RATE, DEB_YEARS, HOLD * 12)}
    return out


def equity_cfs(m, net_exit, reserve=True):
    """Equity cash flows: -equity at t0, then NOI - debt service for 10 years (NOI flat at Year 3 after Year 3), plus net exit.
    reserve=True (the page): the financed lease-up reserve bridges a year where NOI is below debt service, so the equity
    receives zero that year. reserve=False: the equity pays the shortfall (sensitivity only)."""
    cfs = [-m['eq']]
    for t in range(HOLD):
        cf = NOI[min(t, 2)] - m['ds']
        cfs.append(max(cf, 0.0) if reserve else cf)
    cfs[-1] += net_exit
    return cfs


def net_exit(m, mult=EXIT_MULT, sell=SELLING_COST, cost=REPLACEMENT_COST):
    """Year 10 net proceeds to the equity: terminal value (mult x cost to rebuild) less selling costs less both loan balances."""
    return mult * cost * (1 - sell) - m['bal10']


def page_irr(m, **kw):
    reserve = kw.pop('reserve', True)
    return irr(equity_cfs(m, net_exit(m, **kw), reserve))


IRR_PAGE = int(rnd(page_irr(model(STACK_AFTER)) * 100))   # the IRR the page carries after the recompute (rounded, %)


def fk(x):
    return f"${rnd(x / 1000)}k"


def fM(x):
    return f"${rnd(x / 1e6, 2)}M"


def fmil(x):
    return f"${rnd(x / 1e6, 2)} million"


def fd(x):
    return f"{rnd(x, 2)}"


def after_figures(a):
    """Every AFTER figure the page must carry, in the page's own format."""
    return {
        'debenture $': fM(a['deb']), 'debenture $ (prose)': fmil(a['deb']),
        'equity $': fM(a['eq']), 'equity $ (prose)': fmil(a['eq']),
        'total 504 debt %': f"{rnd(a['debt_pct'])}", 'total 504 debt $': fM(a['debt']),
        'DS bank': fk(a['ds_bank']), 'DS debenture': fk(a['ds_deb']), 'DS combined': fk(a['ds']),
        'DS combined (prose, thousand)': f"${rnd(a['ds'] / 1000):,}" + ',000',
        'DSCR Y1': fd(a['dscr'][0]), 'DSCR Y2': fd(a['dscr'][1]), 'DSCR Y3': fd(a['dscr'][2]),
        'break-even occupancy %': f"{rnd(a['be_occ'])}",
    }


# ---------------------------------------------------------------- report
def report():
    rev = sum(s * r * 12 for s, r in RENT)
    egi = rev - VACANCY + ANCILLARY
    print('INPUT CHECK')
    print(f"  uses sum {sum(USES):.2f}M (page $5.80M); GPR {rev:,} (page $1,148,400); EGI {egi:,} (page $1,131,000); "
          f"NOI {egi - OPEX:,} (page $713,000); opex ratio {OPEX / egi:.3f} (page ~37%); margin {(egi - OPEX) / egi:.3f} (page ~63%)")
    assert abs(sum(USES) - 5.80) < 1e-9 and rev == 1_148_400 and egi == 1_131_000 and egi - OPEX == NOI[2]
    print(f"  NOI proportional to occupancy: {[round(NOI[2] * o / OCC[2] / 1000, 1) for o in OCC]}k vs table {[n // 1000 for n in NOI]}k")
    b, a = model(STACK_BEFORE), model(STACK_AFTER)

    print('\nBEFORE reproduces the published page?')
    tests = [
        ('bank $', fM(b['bank']), '$2.90M'), ('debenture $', fM(b['deb']), '$2.32M'), ('equity $', fM(b['eq']), '$0.58M'),
        ('total debt %', f"{rnd(b['debt_pct'])}", '90'), ('total debt $', fM(b['debt']), '$5.22M'),
        ('DS bank', fk(b['ds_bank']), '$304k'), ('DS debenture', fk(b['ds_deb']), '$188k'), ('DS combined', fk(b['ds']), '$492k'),
        ('DSCR Y1', fd(b['dscr'][0]), '0.90'), ('DSCR Y2', fd(b['dscr'][1]), '1.15'), ('DSCR Y3', fd(b['dscr'][2]), '1.45'),
        ('break-even occupancy %', f"{rnd(b['be_occ'])}", '64'),
    ]
    ok = True
    for name, got, pub in tests:
        flag = 'ok' if got == pub else 'MISMATCH'
        ok &= got == pub
        print(f"  {name:24s} model {got:>8s}   published {pub:>8s}   {flag}")
    if not ok:
        print('BEFORE does not reproduce the page; stopping.')
        return 2

    print('\nBEFORE (50/40/10)  ->  AFTER (50/35/15)')
    rows = [
        ('Bank first mortgage', fM(b['bank']), fM(a['bank'])),
        ('CDC / SBA debenture', fM(b['deb']), fM(a['deb'])),
        ('Borrower equity', f"{fM(b['eq'])} (10%)", f"{fM(a['eq'])} (15%)"),
        ('Total 504 debt', f"{rnd(b['debt_pct'])}% / {fM(b['debt'])}", f"{rnd(a['debt_pct'])}% / {fM(a['debt'])}"),
        ('Debt service bank', fk(b['ds_bank']), fk(a['ds_bank'])),
        ('Debt service debenture', fk(b['ds_deb']), fk(a['ds_deb'])),
        ('Debt service combined', f"{fk(b['ds'])} ({b['ds']:,.0f})", f"{fk(a['ds'])} ({a['ds']:,.0f})"),
        ('DSCR Year 1 (NOI 444k)', fd(b['dscr'][0]), fd(a['dscr'][0])),
        ('DSCR Year 2 (NOI 567k)', fd(b['dscr'][1]), fd(a['dscr'][1])),
        ('DSCR Year 3 (NOI 713k)', fd(b['dscr'][2]), fd(a['dscr'][2])),
        ('Break-even occupancy (DSCR 1.0)', f"{rnd(b['be_occ'])}%", f"{rnd(a['be_occ'])}%"),
        ('Cash flow after DS, Year 3', fk(b['fcf'][2]), fk(a['fcf'][2])),
        ('Stabilized cash-on-cash (not on page)', f"{b['coc'][2] * 100:.1f}%", f"{a['coc'][2] * 100:.1f}%"),
        ('Year 10 loan balance (not on page)', fM(b['bal10']), fM(a['bal10'])),
    ]
    w = max(len(r[0]) for r in rows)
    for name, x, y in rows:
        print(f"  {name:{w}s}  {x:>22s}  ->  {y:>22s}")

    print("\nIRR (page's exit rule: terminal value 1.15 x cost to rebuild, cost to rebuild = $5.80M, selling cost 0%, both loan balances repaid)")
    ib, ia = page_irr(b), page_irr(a)
    print(f"  BEFORE: {ib * 100:5.2f}%  (equity {fM(b['eq'])}, net exit {fM(net_exit(b))} = {EXIT_MULT}x{fM(REPLACEMENT_COST)} less balances {fM(b['bal10'])})"
          f"   published ~{IRR_PUBLISHED}% is not what the rule gives")
    print(f"  AFTER : {ia * 100:5.2f}%  (equity {fM(a['eq'])}, net exit {fM(net_exit(a))} = {EXIT_MULT}x{fM(REPLACEMENT_COST)} less balances {fM(a['bal10'])})"
          f"   page: about {IRR_PAGE} percent")
    print('  Sensitivities, AFTER (BEFORE in brackets):')
    print(f"    terminal value 1.00x cost: {page_irr(a, mult=1.0) * 100:.2f}% ({page_irr(b, mult=1.0) * 100:.2f}%)")
    for sc in (0.03, 0.05, 0.06):
        print(f"    selling cost {sc * 100:.0f}%: {page_irr(a, sell=sc) * 100:.2f}% ({page_irr(b, sell=sc) * 100:.2f}%)")
    print(f"    Year 1 shortfall paid by equity instead of the reserve: {page_irr(a, reserve=False) * 100:.2f}% ({page_irr(b, reserve=False) * 100:.2f}%)")
    print(f"    cost to rebuild = project cost less $1.35M land: {page_irr(a, cost=TOTAL_COST - 1_350_000) * 100:.2f}% ({page_irr(b, cost=TOTAL_COST - 1_350_000) * 100:.2f}%)")
    print(f"    worthless exit (equity gets nothing): {irr(equity_cfs(a, 0.0)) * 100:.2f}% ({irr(equity_cfs(b, 0.0)) * 100:.2f}%)")
    print('  Note: calibrating the exit cap rate to reproduce 16% needed a 21.03% cap (sale below the loan balance); rejected, it contradicts the page.')
    return 0


# ---------------------------------------------------------------- check
DASHES = ''.join(chr(c) for c in (0x2010, 0x2011, 0x2012, 0x2013, 0x2014, 0x2015, 0x2212, 0x2043, 0xFE58, 0xFE63, 0xFF0D))   # hyphen, en, em and look-alikes
INLINE = r'a|span|time|em|strong|b|i|abbr|small|mark|code|cite|u|s'


def norm(t):
    t = html.unescape(t)
    t = re.sub('[' + DASHES + ']', '-', t)
    t = t.replace(' ', ' ')
    t = re.sub(r'\s+', ' ', t)
    t = re.sub(r'\s+([.,;:])', r'\1', t)
    return t.strip()


def page_text(raw):
    t = re.sub(r'<!--.*?-->', '', raw, flags=re.S)                       # comments and sba:/fsc:/mesh: markers
    t = re.sub(r'<(script|style)\b.*?</\1>', ' ', t, flags=re.S | re.I)
    t = re.sub(r'<sup\b[^>]*class="fn"[^>]*>.*?</sup>', '', t, flags=re.S)  # footnote markers
    t = re.sub(r'</?(?:' + INLINE + r')\b[^>]*>', '', t, flags=re.I)        # inline tags: no space
    t = re.sub(r'<[^>]+>', ' ', t)                                          # block tags: space
    return norm(t)


def head_texts(raw):
    """Meta/OG descriptions and the JSON-LD description, normalized."""
    out = {}
    for key, pat in (('meta description', r'<meta name="description" content="([^"]*)"'),
                     ('og:description', r'<meta property="og:description" content="([^"]*)"')):
        m = re.search(pat, raw)
        out[key] = norm(m.group(1)) if m else ''
    desc = ''
    for blk in re.findall(r'<script type="application/ld\+json">(.*?)</script>', raw, flags=re.S):
        try:
            data = json.loads(blk)
        except ValueError:
            continue
        for node in data.get('@graph', [data]):
            if node.get('@type') == 'Article':
                desc = node.get('description', '')
    out['JSON-LD Article description'] = norm(desc)
    return out


GAP = '\x00'   # "~~" in a snippet: a short run of punctuation/space


def rx(snippet):
    parts = [re.escape(norm(p)) for p in snippet.split('~~')]
    return re.compile(r'[\s,;:().\-]{0,6}'.join(parts))


def expected(a):
    f = after_figures(a)
    s = []
    s.append(f"{f['total 504 debt %']}% SBA 504 debt (50% bank + 35% CDC/SBA), {f['total 504 debt $']} of $5.80M")
    s.append(f"{f['DSCR Y3']}x Stabilized DSCR, above the ~1.25x lender floor")
    s.append(f"≈{IRR_PAGE}% Illustrative levered equity IRR, 10-year hold")
    s.append('a bank first mortgage, a CDC/SBA debenture, and a 15 percent equity injection')
    s.append(f"Bank first mortgage (50%) {fM(a['bank'])}")
    s.append(f"CDC / SBA 504 debenture (35%) {f['debenture $']}")
    s.append(f"Borrower equity injection (15%) {f['equity $']}")
    s.append(f"Annual debt service~~bank ≈ {f['DS bank']}")
    s.append(f"Annual debt service~~debenture ≈ {f['DS debenture']}")
    s.append(f"Combined annual debt service ≈ {f['DS combined']}")
    s.append('50/35/15 bank/CDC/equity split')
    s.append(f"a {f['debenture $ (prose)']} CDC/SBA debenture at an illustrative 6.5 percent")
    s.append(f"and a {f['equity $ (prose)']} equity injection, a 50/35/15 split.")
    s.append(f"combined debt service near {f['DS combined (prose, thousand)']} a year")
    s.append('The equity injection is 15%, the 504 minimum for a New Business (two years or less in operation) under 13 CFR 120.910;')
    s.append('the 10% start-up figure in SOP 50 10 8.1 is the 7(a) rule, not a 504 rule.')
    s.append('The 504 minimum is 10% in standard cases, 15% for a New Business or a limited or special purpose property, and 20% for both.')
    for yr, stage, occ, noi, i in (('Year 1', 'Lease-up (reserve-supported)', '~58%', '~$444k', 0), ('Year 2', 'Building', '~74%', '~$567k', 1),
                                   ('Year 3', 'Stabilized', '~93%', '~$713k', 2)):
        s.append(f"{yr} {stage} {occ} {noi} ~{f['DS combined']} {f['DSCR Y' + str(i + 1)]}")
    s.append(f"through a graded lease-up to a stabilized {f['DSCR Y3']}x")
    s.append(f"The stabilized {f['DSCR Y3']}x coverage is the figure the lender and the CDC document")
    s.append(f"coverage tracks that ramp from {f['DSCR Y1']}x to {f['DSCR Y2']}x to {f['DSCR Y3']}x.")
    s.append(f"is crossed near {f['break-even occupancy %']} percent economic occupancy")
    s.append(f"The Year 1 figure of {f['DSCR Y1']}x is intentionally below 1.0")
    s.append(f"the {f['equity $ (prose)']} injection earns a growing levered cash flow")
    s.append(f"stabilized NOI of about $713,000 against {f['DS combined (prose, thousand)']} of debt service")
    s.append(f"a stabilized {f['DSCR Y3']}x DSCR, and a ~{IRR_PAGE}% levered equity IRR")
    s.append(f"an illustrative levered equity IRR of about {IRR_PAGE} percent over a 10-year hold")
    s.append('10% start-up equity injection (a 7(a) rule, not the 504 minimum; see source 14)')
    s.append('with the borrower at 15% as a New Business (13 CFR 120.910). See sources 10 and 14.')
    s.append('13 CFR 120.910, Borrower contributions, eCFR (current as of October 2026), '
             'https://www.ecfr.gov/current/title-13/chapter-I/part-120/subpart-H/section-120.910')
    return s


STALE = [
    r'1\.45x', r'(?<![\d.])1\.45(?![\d])', r'(?<![\d.])0\.90(?![\d])', r'(?<![\d.])1\.15(?![\d])',
    r'\$492', r'492,000', r'\$188k', r'\$2\.32', r'\$0\.58', r'\$5\.22', r'50/40/10', r'canonical',
    r'debenture \(40%\)', r'40% CDC', r'\b64 percent', r'10 percent equity', r'~10% equity injection',
    r'injection holds at', r'rather than escalating',
    r'(?:≈|~)\s?16\s?%', r'about 16 percent',   # the published IRR (false by the page's own exit rule)
]
EQUITY_WORDS = re.compile(r'equity|injection|contribution|borrower|down payment|escalat|minimum|requirement', re.I)
SAFE_WORDS = re.compile(r'start-up|startup|standard', re.I)


def check(page=PAGE):
    raw = Path(page).read_text(encoding='utf-8')
    text = page_text(raw)
    a = model(STACK_AFTER)
    errs = []
    for snip in expected(a):
        if not rx(snip).search(text):
            errs.append("missing on page: " + snip.replace("~~", " ... "))
    heads = head_texts(raw)
    f = after_figures(a)
    for k, v in heads.items():
        if f"a {f['DSCR Y3']}x stabilized DSCR, and a ~{IRR_PAGE}% levered equity IRR" not in v:
            errs.append(f"{k}: does not carry the AFTER stabilized DSCR {f['DSCR Y3']}x and IRR ~{IRR_PAGE}%")
    for pat in STALE:
        for m in re.finditer(pat, text):
            errs.append(f"stale or rejected figure on page ({pat}): ...{text[max(0, m.start() - 50):m.end() + 50]}...")
        for k, v in heads.items():
            if re.search(pat, v):
                errs.append(f"stale or rejected figure in {k} ({pat})")
    # 10% stated as this project's equity or as the 504 minimum
    for src, t in [('page', text)] + list(heads.items()):
        for m in re.finditer(r'(?<![\d.])(?:10 percent|10%|ten percent)', t):
            win = t[max(0, m.start() - 70):m.end() + 70]
            if EQUITY_WORDS.search(win) and not SAFE_WORDS.search(win):
                errs.append(f"10% stated as equity/minimum ({src}): ...{win}...")
    # every IRR statement on the page (and in the head texts) must carry the recomputed value
    irr_pat = re.compile(r'(?:[≈~]\s?(\d+(?:\.\d+)?)\s?%\s*(?:Illustrative )?levered equity IRR)|(?:IRR of about (\d+(?:\.\d+)?) percent)', re.I)
    for src, t in [('page', text)] + list(heads.items()):
        for m in irr_pat.finditer(t):
            val = m.group(1) or m.group(2)
            if val != str(IRR_PAGE):
                errs.append(f"IRR statement ({src}) says {val}, expected {IRR_PAGE}: ...{t[max(0, m.start() - 30):m.end() + 30]}...")
    # source 14 exists and is cited
    if len(re.findall(r'<li id="s14">', raw)) != 1:
        errs.append('source list: expected exactly one <li id="s14">')
    if 'href="#s14"' not in raw:
        errs.append('no footnote marker points at #s14')
    if errs:
        print(f"CHECK FAILED: {len(errs)} mismatch(es)")
        for e in errs:
            print('  - ' + e)
        return 1
    print(f"CHECK OK: {len(expected(a))} AFTER snippets present (IRR {IRR_PAGE}% included), no stale BEFORE figure, no 10% equity/minimum statement")
    return 0


if __name__ == '__main__':
    argv = sys.argv[1:]
    if '--check' in argv:
        # optional: --page PATH checks another copy of the page (used to test the check itself)
        sys.exit(check(argv[argv.index('--page') + 1]) if '--page' in argv else check())
    sys.exit(report())
