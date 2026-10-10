#!/usr/bin/env python3
"""Veterinary Michigan (SBA 7(a), practice acquisition plus new-build hospital): Appendix 15 recompute.

Category: Initial Acquisition (the sponsor is a new owner buying an established practice), so under SOP 50 10 8.1
(R08, R09) the floor is 1.25:1 on historical EBITDA over post-transaction debt service (R10); a Business Expansion
(1.15:1, R09) needs an operating business expanding, which this sponsor is not.
Checks:
  R13  injection: 10% of total project cost, cannot be reduced for an Initial Acquisition.
  R25  amortization: not more than 10 years on the business portion; real estate may be a separate loan or blended
       (only the real estate portion may exceed 10 years, up to 25). The Special Purpose Property exemption (25 years
       on the whole loan) needs 85% or more of the use of total project costs in real estate AND an owner-occupied
       Special Purpose Property that cannot be separated from the business; neither holds here (real estate is 60%).
  R11  projections cannot meet the floor unless the acquisition is of an owner-occupied Special Purpose Property whose
       price the appraised value fully supports; a veterinary hospital is not named on SBA's example list (R44) and
       the practice is the acquired item, so the exception is NOT claimed.
Case inputs (unchanged): uses below; 90% SBA 7(a) loan at 10.25% (Prime + 2.75); EBITDA Y1 533k, Y2 715k, Y3 825k;
Year 1 is an interest-only bridge of ~$507k.  The case has no historical EBITDA for the acquired practice.
"""
def const(rate, years):
    r = rate / 12; n = years * 12
    return 12 * r / (1 - (1 + r) ** -n)

uses = {'land': .60, 'site': .45, 'shell': 2.05, 'equip': .85, 'ffe': .30, 'goodwill': .90, 'soft': .20, 'wc': .15}
total = sum(uses.values())
loan = .90 * total
equity = total - loan
re_cost = uses['land'] + uses['site'] + uses['shell'] + uses['soft']          # new-build real estate incl. soft costs
biz_cost = uses['equip'] + uses['ffe'] + uses['goodwill'] + uses['wc']        # business portion
print('total', round(total, 2), 'loan', round(loan, 3), 'equity', round(equity, 3), '(10% =', round(.10 * total, 3), ')')
print('real estate share of project costs', round(re_cost / total * 100, 1), '% (85% needed for the special purpose exemption)')

RATE = .1025
before_ds = loan * const(RATE, 25)
re_loan = .90 * re_cost; biz_loan = .90 * biz_cost
after_ds = re_loan * const(RATE, 25) + biz_loan * const(RATE, 10)
print('BEFORE single 25-year amortization: DS', round(before_ds * 1e3), 'k')
print('AFTER real estate 25-yr', round(re_loan, 3), 'M + business 10-yr', round(biz_loan, 3), 'M: DS', round(after_ds * 1e3), 'k',
      '(RE', round(re_loan * const(RATE, 25) * 1e3), 'k + business', round(biz_loan * const(RATE, 10) * 1e3), 'k)')
io = loan * RATE
ebitda = [533, 715, 825]
print('interest-only year-1 basis', round(io * 1e3), 'k')
print('BEFORE DSCR', [round(ebitda[0] / (io * 1e3), 2), round(ebitda[1] / (before_ds * 1e3), 2), round(ebitda[2] / (before_ds * 1e3), 2)])
print('AFTER  DSCR', [round(ebitda[0] / (io * 1e3), 2), round(ebitda[1] / (after_ds * 1e3), 2), round(ebitda[2] / (after_ds * 1e3), 2)])
print('floor test: stabilized projected', round(ebitda[2] / (after_ds * 1e3), 3), 'vs 1.25 ->', 'clears' if ebitda[2] / (after_ds * 1e3) >= 1.25 else 'fails')
print('EBITDA needed for 1.25x on the new debt service', round(1.25 * after_ds * 1e3), 'k')
# Year-10 loan balance (for the exit net-equity line): 25-yr real estate piece only; business piece is repaid in 10 years
r = RATE / 12
bal_re = re_loan * (1 - (1 + r) ** -(300 - 120)) / (1 - (1 + r) ** -300)
bal_before = loan * (1 - (1 + r) ** -(300 - 120)) / (1 - (1 + r) ** -300)
print('Year-10 balance before', round(bal_before, 2), 'M after', round(bal_re, 2), 'M')
