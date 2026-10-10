#!/usr/bin/env python3
"""Marina Maryland (SBA 504, acquisition plus dry-stack expansion): Appendix 15 and 504 test.

Category: Initial Acquisition (the sponsor is a new owner; Business Expansion needs an operating borrower with
two full fiscal years, R09). The loan is a 504, so the governing coverage test is R30: DSC >= 1.15 on a historical
basis (last fiscal year-end or two-year average), projections analyzed where history falls short. Appendix 15 (R08,
R09, R10, R11, R13, R25) governs 7(a) changes of ownership; its tests are run below as the counterfactual the brief
asks for. The case gives NO historical EBITDA, so no historical ratio is computed or invented.
Case inputs (unchanged): cost $12.5M; 50/35/15 stack; bank 9.5% / 25 yr; debenture 6.5% / 25 yr;
NOI Y1 1.11M, Y2 1.31M, Y3 1.46M; stated debt service ~$1.01M.
"""
def const(rate, years):
    r = rate / 12; n = years * 12
    return 12 * r / (1 - (1 + r) ** -n)
uses = {'land_upland': 3.30, 'wet_slip_docks': 3.55, 'dry_stack_bldg': 2.85, 'fuel_dock_env': 0.70,
        'equipment': 0.70, 'soft_dredging_contingency': 0.85, 'wc_closing_fees': 0.55}
total = sum(uses.values())
bank = 6.25e6; deb = 4.375e6; eq = 1.875e6
ds = bank * const(.095, 25) + deb * const(.065, 25)
print('total', total, 'debt service', round(ds), '(case states ~1.01M)')
noi = [1.11e6, 1.31e6, 1.46e6]
print('projected DSCR', [round(n / ds, 2) for n in noi], '(table: 1.10, 1.30, 1.45)')
print('vs 504 floor 1.15 (R30):', ['meets' if n / ds >= 1.15 else 'below' for n in noi])
print('vs Appendix 15 Initial Acquisition 1.25 (R09), projected only:', ['meets' if n / ds >= 1.25 else 'below' for n in noi],
      '- cannot be relied on for the test (R11) unless an owner-occupied Special Purpose Property whose price the appraised value fully supports')
# 10% injection (R13) and 504 contribution (R31)
print('equity', eq / (total * 1e6) * 100, '% of cost; 504 special purpose minimum 15% (20% if also a New Business, R31, R55)')
# 85% test for the Appendix 15 special purpose amortization exemption (R25): real estate share of the USE of total project costs
re_strict = uses['land_upland'] + uses['wet_slip_docks'] + uses['dry_stack_bldg'] + uses['fuel_dock_env']
re_wide = re_strict + uses['soft_dredging_contingency']
print('real estate share (strict)', round(re_strict / total * 100, 1), '%; with soft costs', round(re_wide / total * 100, 1), '%')
print('=> the 85% line is crossed only if soft costs and dredging count as real estate; the case has no goodwill line, so no business-portion loan at 10 years is modeled; 504 maturities (25-yr) govern as financed')
# Business Purchase Price (R22): excludes owner-occupied commercial real estate; here the price is land + docks (real property) so
# the Business Purchase Price is not separately stated in the case; $350,000 / $3 million tests cannot be run.
