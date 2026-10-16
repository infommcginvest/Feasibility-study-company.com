#!/usr/bin/env python3
"""RV and boat storage Arizona (SBA 504): levered equity IRR at the exit cap rate the page cites.

Page: case-studies/rv-boat-storage-arizona-sba/index.html   (owner ruling of October 16, 2026, carried by WEB-FSC-6)

THE RULING. The IRR uses the exit at the cap rate the page itself cites, the method WEB-FSC-4 used for California and
Florida (docs/web-fsc-4/DECISIONS.md decision 41; docs/web-fsc-4/recompute/rv-boat-storage-california-sba.py).

INPUTS (all from the page as WEB-FSC-4 left it; docs/web-fsc-4/recompute/rv-boat-storage-arizona-sba.md):
  cost $5.00M; 504 stack for a New Business 50% bank / 35% debenture / 15% equity ($0.75M);
  bank 9.5% / 25 yr; debenture 6.5% fixed / 25 yr; monthly amortization;
  NOI Y1 $382k, Y2 $488k, Y3 $615k (DSCR ramp table); 10-year hold.
  The page cites dedicated RV and boat storage cap rates of about 6.0 to 7.5% (Class A) and 7.5 to 8.5% (Class B)
  (source 18) and says the exit is graded conservatively. The exit here is at 8.5%, the wide end of the range it cites.

METHOD (as California): stabilized NOI untrended after Year 3; the Year 1 shortfall is paid from the funded lease-up
reserve, so the Year 1 distribution is zero; Year 2 onward NOI less debt service; the Year 10 sale at Year 3 NOI over
the exit cap, less selling costs of 3% (the one unstated input, as in California), less both loan balances after 120
monthly payments.

USAGE
  python3 docs/web-fsc-6/recompute/rv-boat-storage-arizona-sba-irr.py           print the IRR and its sensitivity
  python3 docs/web-fsc-6/recompute/rv-boat-storage-arizona-sba-irr.py --check   exit 1 if the page states another IRR
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PAGE = os.path.join(ROOT, "case-studies", "rv-boat-storage-arizona-sba", "index.html")

COST = 5_000_000
SPLIT = {"bank": 0.50, "deb": 0.35, "eq": 0.15}
BANK_RATE, BANK_YEARS = 0.095, 25
DEB_RATE, DEB_YEARS = 0.065, 25
NOI = (382_000, 488_000, 615_000)
HOLD = 10
CAP_RANGE = (0.060, 0.085)      # page source 18: Class A ~6.0-7.5%, Class B ~7.5-8.5%
EXIT_CAP = 0.085                # the wide end of the range the page cites
SELL = 0.03


def const(rate, years):
    r, n = rate / 12, years * 12
    return 12 * r / (1 - (1 + r) ** -n)


def balance(principal, rate, years, months):
    r = rate / 12
    pmt = principal * const(rate, years) / 12
    return principal * (1 + r) ** months - pmt * ((1 + r) ** months - 1) / r


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


def model(exit_cap=EXIT_CAP, sell=SELL):
    bank, deb, eq = (COST * SPLIT[k] for k in ("bank", "deb", "eq"))
    ds = bank * const(BANK_RATE, BANK_YEARS) + deb * const(DEB_RATE, DEB_YEARS)
    bal = balance(bank, BANK_RATE, BANK_YEARS, 12 * HOLD) + balance(deb, DEB_RATE, DEB_YEARS, 12 * HOLD)
    noi = list(NOI) + [NOI[-1]] * (HOLD - len(NOI))
    cfs = [-eq]
    for t, n in enumerate(noi, start=1):
        d = n - ds
        cfs.append(max(d, 0.0) if t == 1 else d)
    gross = NOI[-1] / exit_cap
    cfs[-1] += gross * (1 - sell) - bal
    return {"eq": eq, "ds": ds, "bal": bal, "gross": gross, "cfs": cfs, "irr": irr(cfs)}


def published():
    return int(round(100 * model()["irr"]))


def main(argv):
    m = model()
    if "--check" in argv:
        text = open(PAGE, encoding="utf-8").read()
        want = published()
        found = re.findall(r"(?:&asymp;|~|near |about )(\d+)(?:<span>%</span>|%| percent)(?=[^<]{0,40}(?:IRR|levered|over a 10-year))", text)
        found += re.findall(r'stat-num">&asymp;(\d+)<span>%</span></div>\s*<div class="stat-label">Illustrative levered', text)
        bad = sorted({f for f in found if int(f) != want})
        if bad or not found:
            print(f"page IRR figures {sorted(set(found))}, expected {want}")
            return 1
        print(f"page states {want}% in {len(found)} places; ok")
        return 0
    print(f"equity ${m['eq']:,.0f}; debt service ${m['ds']:,.0f}; balances after {HOLD} years ${m['bal']:,.0f}")
    print(f"exit at {EXIT_CAP:.1%}: gross ${m['gross']:,.0f}, net to equity ${m['gross'] * (1 - SELL) - m['bal']:,.0f}")
    print(f"levered equity IRR {m['irr']:.2%} (published as {published()}%)")
    for cap in (0.060, 0.065, 0.070, 0.075, 0.080, 0.085):
        row = "  ".join(f"sell {s:.0%}: {model(cap, s)['irr']:.1%}" for s in (0.0, 0.03, 0.05))
        print(f"  cap {cap:.1%}  {row}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
