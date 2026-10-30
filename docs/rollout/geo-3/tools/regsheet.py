#!/usr/bin/env python3
"""GEO-3 register sheet: which mkt: markers render for a geography, with the value they print.

    python3 docs/rollout/geo-3/tools/regsheet.py <geo> [<geo> ...]      e.g. illinois/chicago il cbsa-48620 co-31055

Read only. Uses scripts/markets.py's own lookup, so a marker listed here renders, and a refusal
is printed with the renderer's reason. Classes are tried with the fit the register records.
"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
import markets  # noqa: E402

ALL = [('acs5_households', 'int'), ('acs5_pop65', 'int'), ('acs5_renter_occupied', 'int'), ('acs5_owner_occupied', 'int'),
       ('acs5_labor_force', 'int'), ('acs5_unemployment_rate', 'pct1'), ('acs5_median_hh_income', 'usd'),
       ('acs5_median_gross_rent', 'usd'), ('acs5_median_home_value', 'usd'), ('acs5_per_capita_income', 'usd'),
       ('acs1_median_hh_income', 'usd'), ('bea_per_capita_income', 'usd'), ('bea_personal_income', 'usd_m'),
       ('sba7a_loans', 'int'), ('sba7a_volume', 'usd_m'), ('sba504_loans', 'int'), ('sba504_volume', 'usd_m'),
       ('sba7a_chgoff_rate', 'pct1'), ('sba504_chgoff_rate', 'pct1')]
CLASSES = ['hotel', 'self-storage', 'restaurant', 'gas-station-and-c-store', 'childcare-and-daycare', 'multifamily',
           'industrial-and-warehouse', 'skilled-nursing', 'assisted-living-and-memory-care', 'medical-office-and-asc',
           'rv-park-and-campground', 'express-car-wash', 'funeral-home', 'veterinary-practice', 'marina', 'grocery-store']


def one(name, p):
    try:
        v, flag = markets.lookup(name, p)
        geo, sid, cls = markets.split(name)
        markets.check_fmt(name, markets.series(sid).get('unit'), p.get('fmt'))
        return markets.fmt_value(v, p['fmt']), flag
    except BaseException as e:  # MarkerError is a SystemExit subclass
        return None, str(e)[:140]


def main(geos):
    for geo in geos:
        print(f'== {geo}')
        for sid, fmt in ALL:
            name = f'{geo}.{sid}'
            v, why = one(name, {'fmt': fmt})
            if v is not None:
                print(f'OK   <!--mkt:{name} {{"fmt": "{fmt}"}}-->{v}<!--/mkt:{name}-->')
            else:
                print(f'NO   {name}: {why}')
        for sid in ('cbp_estab', 'sba7a_loans'):
            for cls in CLASSES:
                fit = markets.class_fit(cls)
                p = {'fmt': 'int'}
                if fit not in ('exact', 'none'):
                    p['fit'] = fit
                name = f'{geo}.{sid}.{cls}'
                v, why = one(name, p)
                if v is not None and v != '0':
                    ps = ', '.join(f'"{k}": "{val}"' for k, val in sorted(p.items()))
                    print(f'OK   <!--mkt:{name} {{{ps}}}-->{v}<!--/mkt:{name}-->')
                elif 'lower bound' in (why or ''):
                    print(f'LB   {name}: lower bound (needs allow_flag and "at least")')
        print('Source line pattern: <!--mktsrc:<geo>.<series>-->x<!--/mktsrc:<geo>.<series>--> (markets.py fills it)')


if __name__ == '__main__':
    main(sys.argv[1:])
