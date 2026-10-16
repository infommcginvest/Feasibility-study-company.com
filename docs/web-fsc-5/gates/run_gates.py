#!/usr/bin/env python3
"""Run the WEB-FSC-5 gates and write docs/web-fsc-5/GATES.txt.

    python3 docs/web-fsc-5/gates/run_gates.py

Each gate prints the command it ran or the check it made, the output, and
GREEN or RED with the reason. Gate 6 (independent re-derivation) is run by
docs/web-fsc-5/gates/rederive.py, which does not import the pipeline; this
runner only reads its result file. Gate 8 copies data/markets/series/sba7a_loans.json
to _cache/, mutates the register file in place, runs --check, restores the file
byte for byte from the copy, and asks git to confirm the file is unchanged.
"""
import csv
import glob
import json
import os
import re
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
DATA = os.path.join(ROOT, 'data', 'markets')
OUT = os.path.join(ROOT, 'docs', 'web-fsc-5', 'GATES.txt')
ALLOWED = [r'^data/markets/', r'^scripts/markets[^/]*\.py$', r'^\.gitignore$', r'^docs/web-fsc-5/']
NAMES = r'm[m]cg|moh[e]lsky|union ?[m]etric|inno[w]ave|analytics[.]loan|loan analytic[s]|feasibility-study-consulta[n]t|wert-?bera[t]er'
LOG = []


def sh(cmd, cwd=ROOT, timeout=900):
    r = subprocess.run(cmd, cwd=cwd, shell=True, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout + r.stderr).rstrip()


def say(*a):
    LOG.append(' '.join(str(x) for x in a))


def gate(n, title, fn):
    say(f'\n=== GATE {n}: {title}')
    try:
        ok, why = fn()
    except Exception as e:
        ok, why = False, f'gate raised {type(e).__name__}: {e}'
    say(f'--> GATE {n} {"GREEN" if ok else "RED"}: {why}')
    return ok


def jl(p):
    return json.load(open(p, encoding='utf-8'))


def g1():
    rc, out = sh('git diff --name-only main...HEAD')
    say('$ git diff --name-only main...HEAD'); say(out)
    bad = [p for p in out.splitlines() if p and not any(re.search(a, p) for a in ALLOWED)]
    rc2, ws = sh('git status --porcelain')
    stray = [l for l in ws.splitlines() if l.strip() and not any(re.search(a, l[3:]) for a in ALLOWED)]
    say('$ git status --porcelain (paths outside the lane)'); say('\n'.join(stray) or '(none)')
    return (not bad and not stray), (f'{len(out.splitlines())} changed path(s), all inside the lane' if not bad and not stray else f'outside the lane: {bad + stray}')


def g2():
    geo = jl(os.path.join(DATA, 'geographies.json'))
    sj = jl(os.path.join(DATA, 'sources.json'))
    src = sj['sources'] + sj['series']
    need = ['id', 'publisher', 'title', 'url', 'vintage', 'period', 'retrieved', 'sha256', 'cadence', 'next_release', 'status']
    files = sorted(f[:-5] for f in os.listdir(os.path.join(DATA, 'series')) if f.endswith('.json'))
    rowless = [f for f in files if f not in {r['id'] for r in sj['series']}]
    say(f'series files {len(files)}; series rows {len(sj["series"])}; series files without a row: {rowless or "none"}')
    markets = len(geo['markets'])
    anchor = re.compile(r'href="(?:https://feasibility-study-company\.com)?/states/([a-z0-9-]+)/([a-z0-9-]+)/?(?:#[^"]*)?"')
    site = set()
    rc, files = sh("git ls-files -- '*.html'")
    for f in files.splitlines():
        if f.startswith(('docs/', 'netlify/')):
            continue
        site |= set(anchor.findall(open(os.path.join(ROOT, f), encoding='utf-8', errors='replace').read()))
    reg = {(m['state'], m['slug']) for m in geo['markets']}
    say(f'market anchors on the site\'s pages (git ls-files *.html outside docs/ and netlify/, measured now): {len(site)}; markets in geographies.json: {markets}; '
        f'anchors without a row: {sorted(site - reg) or "none"}; rows without an anchor: {sorted(reg - site) or "none"}')
    say(f'states: {len(geo["states"])}; counties: {geo["counties"]["status"]} ({len(geo["counties"]["rows"])} rows); CBSAs: {geo["cbsas"]["status"]} ({len(geo["cbsas"]["rows"])} rows)')
    missing_fields = []
    for r in src:
        for k in need:
            if k not in r:
                missing_fields.append(f'{r["id"]}.{k} absent')
            elif r[k] in (None, '', [], {}) and not (r['status'] == 'NOT FETCHED' and k in ('retrieved', 'sha256')):
                missing_fields.append(f'{r["id"]}.{k} empty')
    by = {}
    for r in sj['sources']:
        by.setdefault(r['status'], []).append(r['id'])
    for st, ids in sorted(by.items()):
        say(f'{st}: {len(ids)}: {", ".join(ids)}')
    for r in sj['sources']:
        if r['status'] != 'FETCHED':
            say(f'  {r["id"]}: {r.get("reason")}')
    say('sources.json field check: ' + ('every row has every field (retrieved and sha256 are empty only for NOT FETCHED rows)' if not missing_fields else '; '.join(missing_fields)))
    ok = markets == 253 and site == reg and not missing_fields and not rowless and geo['counties']['rows'] and geo['cbsas']['rows']
    why = []
    if markets != 253:
        why.append(f'{markets}/253 markets')
    if not geo['counties']['rows'] or not geo['cbsas']['rows']:
        why.append('no county or CBSA roster: both NOT FETCHED (Census API key wall D2, www2 robots D1)')
    if missing_fields:
        why.append('sources.json fields missing')
    return bool(ok), ('; '.join(why) if why else 'all geographies and source fields present')


def g3():
    rec = jl(os.path.join(DATA, 'reconciliation.json'))
    bad = [r for r in rec['us_by_program_fy'] if not r['match']]
    say(f'FOIA us by program and FY: {len(rec["us_by_program_fy"])} cells, {len(bad)} mismatches')
    for prog, v in rec['states_vs_us'].items():
        say(f'FOIA {prog}: sum of states {v["sum_of_states_loans"]:,} vs us {v["us_loans"]:,}; difference {v["difference"]} ({v["explained_by"]})')
    rd = os.path.join(ROOT, 'docs', 'web-fsc-5', 'gates', 'rederive-result.json')
    if os.path.exists(rd):
        r = jl(rd)
        say(f'independent FOIA totals by program and FY (rederive.py): {r.get("foia_totals", {}).get("summary")}')
    src = jl(os.path.join(DATA, 'sources.json'))['sources']
    census = [r['id'] for r in src if r['id'].startswith(('census_', 'bls_', 'bea_', 'hud_')) and r['status'] == 'FETCHED']
    say(f'additive federal series fetched for a county-to-state-to-nation reconciliation: {census or "none"}')
    unexplained = [p for p, v in rec['states_vs_us'].items() if not v.get('explained')]
    ok = not bad and rec['all_match'] and not unexplained
    return ok, ('FOIA register equals the raw files by program and FY; state sums differ from us only by rows without a ProjectState; '
                'no Census, BLS or BEA additive series was fetched, so there is no county sum to reconcile') if ok else 'mismatch'


def g4():
    sm = jl(os.path.join(DATA, 'foia-status-map.json'))
    sc = jl(os.path.join(DATA, 'foia-status-counts.json'))
    unclassified = []
    for prog, files in sc['counts'].items():
        for f, d in files.items():
            if f == '_evidence':
                continue
            for st in d:
                if st not in sm['programs'][prog]:
                    unclassified.append((prog, f, st))
            say(f'{prog} {f}: ' + ', '.join(f'{k}={v:,}' for k, v in sorted(d.items())))
    s = jl(os.path.join(DATA, 'series', 'sba7a_chgoff_n.json'))
    s5 = jl(os.path.join(DATA, 'series', 'sba504_chgoff_n.json'))
    first, last = s['by_fy_years']
    rec = jl(os.path.join(DATA, 'reconciliation.json'))
    zero_fy = []
    raw_ch = jl(os.path.join(ROOT, 'docs', 'web-fsc-5', 'gates', 'rederive-result.json')).get('foia_chgoff_by_program_fy', {}) if os.path.exists(os.path.join(ROOT, 'docs', 'web-fsc-5', 'gates', 'rederive-result.json')) else {}
    for prog, ser in (('7a', s), ('504', s5)):
        arr = ser['values']['us']['all']['by_fy']
        for i, v in enumerate(arr):
            fy = first + i
            raw = raw_ch.get(prog, {}).get(str(fy))
            if raw is not None and raw > 0 and v == 0:
                zero_fy.append((prog, fy))
        say(f'{prog} charge-offs by approval FY (register): ' + ', '.join(f'{first + i}:{v}' for i, v in enumerate(arr)))
        if raw_ch.get(prog):
            say(f'{prog} charge-offs by approval FY (raw, independent): ' + ', '.join(f'{k}:{v}' for k, v in sorted(raw_ch[prog].items())))
    ok = not unclassified and not zero_fy and bool(raw_ch)
    return ok, ('every status classified; charge-offs non-zero in every program and FY where the raw files have them' if ok else
                f'unclassified {unclassified}; zero where raw has charge-offs {zero_fy}; independent counts present: {bool(raw_ch)}')


def g5():
    nm = jl(os.path.join(DATA, 'naics-map.json'))
    ev = jl(os.path.join(DATA, 'naics-evidence.json'))
    rows = nm['classes']
    no_fit = [r['slug'] for r in rows if r.get('fit') not in ('exact', 'partial', 'proxy', 'none')]
    say(f'classes: {len(rows)}; without a fit grade: {no_fit or "none"}')
    for r in rows:
        e = ev['classes'][r['slug']]
        say(f'  {r["slug"]}: fit {r["fit"]}; 2022 {",".join(r["naics2022"]) or "-"}; FOIA loans {e["foia_loans_total"]:,}; by edition set {e["foia_loans_by_edition_set"]}')
    src = {x['id']: x for x in jl(os.path.join(DATA, 'sources.json'))['sources']}
    cbp_ok = src['census_cbp']['status'] == 'FETCHED' or src['census_cbp_bulk']['status'] == 'FETCHED'
    say(f'CBP establishment counts nationally per class: {"available" if cbp_ok else "NOT FETCHED (census_cbp: " + str(src["census_cbp"]["reason"]) + ")"}')
    ok = len(rows) == 43 and not no_fit and cbp_ok
    return ok, ('every class graded; FOIA loans reported by code and edition' + ('' if cbp_ok else '; RED because CBP was NOT FETCHED, so no class can show a non-zero national CBP count'))


def g6():
    p = os.path.join(ROOT, 'docs', 'web-fsc-5', 'gates', 'rederive-result.json')
    if not os.path.exists(p):
        return False, 'rederive-result.json absent'
    r = jl(p)
    say(f'sampled {r["n"]} values; matches {r["matches"]}; mismatches {r["mismatches"]}')
    for k, v in r['by_kind'].items():
        say(f'  {k}: {v}')
    for x in r.get('mismatch_detail', []):
        say(f'  MISMATCH {x}')
    quota = r.get('quota', {})
    short = {k: v for k, v in quota.items() if v['have'] < v['need']}
    say(f'quota: {quota}')
    ok = r['n'] >= 40 and r['mismatches'] == 0 and not short
    return ok, ('40+ values re-derived independently, all match, every quota met' if ok else f'mismatches {r["mismatches"]}; quotas short {short}')


def g7():
    bad = []
    n_rates = n_sums = 0
    for f in sorted(glob.glob(os.path.join(DATA, 'series', '*.json'))):
        s = jl(f)
        agg = s.get('aggregation')
        if agg not in ('sum', 'ratio of summed numerator and denominator'):
            bad.append(f'{os.path.basename(f)}: aggregation {agg!r}')
        if 'median' in (s.get('label', '') + s['id']).lower():
            bad.append(f'{os.path.basename(f)}: a median series is aggregated')
        for g, cl in s['values'].items():
            for c, cell in cl.items():
                if isinstance(cell, dict) and 'num' in cell:
                    n_rates += 1
                    if cell['v'] is not None and abs(cell['v'] - cell['num'] / cell['den']) > 1e-6:
                        bad.append(f'{s["id"]} {g} {c}: rate {cell["v"]} != num/den')
                elif isinstance(cell, dict) and 'by_fy' in cell:
                    n_sums += 1
    # the small-sample flag follows the disbursed-loan count for both rates (attacker finding F1)
    flag_checked = 0
    for prog in ('sba7a', 'sba504'):
        cnt = jl(os.path.join(DATA, 'series', f'{prog}_chgoff_rate.json'))['values']
        amt = jl(os.path.join(DATA, 'series', f'{prog}_chgoff_amt_rate.json'))['values']
        for g, cl in cnt.items():
            for c, cell in cl.items():
                a = amt[g][c]
                small = 0 < cell['den'] < 30
                for which, x in (('count', cell), ('amount', a)):
                    flag_checked += 1
                    if small != str(x.get('f', '')).startswith('small-denominator'):
                        bad.append(f'{prog} {g} {c}: {which} rate flag {x.get("f")!r} but {cell["den"]} disbursed loans')
    say(f'rate cells checked for the small-sample flag on the disbursed-loan count: {flag_checked:,}')
    # every market value equals the sum of its component county strings (class all, all years)
    geo = jl(os.path.join(DATA, 'geographies.json'))
    cs = jl(os.path.join(DATA, 'foia-county-strings.json'))['values']
    s7 = jl(os.path.join(DATA, 'series', 'sba7a_loans.json'))
    checked = 0
    for m in geo['markets']:
        mid = f'{m["state"]}/{m["slug"]}'
        if mid in s7['values']:
            want = sum(cs.get(f'{x["state"]}|{x["string"]}', {}).get('7a', [0])[0] for x in m['foia']['strings'])
            got = s7['values'][mid]['all']['all']
            checked += 1
            if want != got:
                bad.append(f'{mid}: sba7a_loans {got} != sum of its county strings {want}')
    say(f'series walked: rate cells {n_rates:,} (each re-divided), additive cells {n_sums:,}; markets checked as sums of their county strings: {checked}')
    say('no series in the register is a median (no ACS or HUD series was fetched)')
    for b in bad[:50]:
        say('  ' + b)
    return not bad, ('every aggregate is a sum or a ratio of sums; no median is aggregated' if not bad else f'{len(bad)} problem(s)')


def g8():
    fx = os.path.join(ROOT, 'docs', 'web-fsc-5', 'fixture')
    rc0, out0 = sh('python3 scripts/markets.py --check --pages docs/web-fsc-5/fixture/index.html')
    say('$ python3 scripts/markets.py --check --pages docs/web-fsc-5/fixture/index.html'); say(out0); say(f'exit {rc0}')
    # mutate a copy of one series value the fixture renders, in place, then revert from the copy
    target = os.path.join(DATA, 'series', 'sba7a_loans.json')
    keep = os.path.join(ROOT, '_cache', 'markets', 'gate8-sba7a_loans.json.orig')
    shutil.copyfile(target, keep)
    try:
        s = jl(target)
        s['values']['tx']['all']['fy2016_2025'] += 1
        json.dump(s, open(target, 'w'), separators=(',', ':'), sort_keys=True)
        rc1, out1 = sh('python3 scripts/markets.py --check --pages docs/web-fsc-5/fixture/index.html')
        say('mutation: data/markets/series/sba7a_loans.json values.tx.all.fy2016_2025 += 1')
        say('$ python3 scripts/markets.py --check --pages docs/web-fsc-5/fixture/index.html'); say(out1); say(f'exit {rc1}')
    finally:
        shutil.copyfile(keep, target)
        os.remove(keep)
    rc2, out2 = sh('python3 scripts/markets.py --check --pages docs/web-fsc-5/fixture/index.html')
    say('revert, then $ python3 scripts/markets.py --check --pages docs/web-fsc-5/fixture/index.html'); say(out2); say(f'exit {rc2}')
    rc3, out3 = sh('git diff --quiet -- data/markets/series/sba7a_loans.json && echo unchanged-vs-index')
    say(f'register file after revert: {out3 or "DIFFERS"}')
    html_ = open(os.path.join(fx, 'index.html'), encoding='utf-8').read()
    houston = re.findall(r'<!--mkt:texas/houston\.', html_)
    ct = re.findall(r'<!--mkt:connecticut/[a-z-]+(?::legacy|:pr)?\.', html_)
    rc4, out4 = sh('python3 scripts/markets.py --pages docs/web-fsc-5/fixture/houston-negative.html')
    say('$ python3 scripts/markets.py --pages docs/web-fsc-5/fixture/houston-negative.html'); say(out4); say(f'exit {rc4}')
    say(f'fixture markers: Houston {len(houston)}, Connecticut {len(ct)}')
    mutation_ok = rc0 == 0 and rc1 == 1 and rc2 == 0
    ok = mutation_ok and len(houston) > 0 and len(ct) > 0
    why = 'mutation test passes (0, 1, 0)' if mutation_ok else f'mutation test failed ({rc0}, {rc1}, {rc2})'
    if not houston:
        why += '; RED for Houston: the register holds no Houston value (CBSA composition pending the delineation file), and the renderer refuses the Houston marker with that reason'
    return ok, why


def g9():
    rows = list(csv.DictReader(open(os.path.join(DATA, 'audit.csv'), encoding='utf-8')))
    tx = [r for r in rows if r['geo'] == 'tx' or r['geo'].startswith('texas/')]
    for r in tx:
        say(f'  {r["geo"]}: specific {r["specific_values"]}, suppressed {r["suppressed_values"]}, standalone {r["standalone"]}' + (f', reason: {r["reason"]}' if r['reason'] else ''))
    mk = [r for r in tx if r['level'] == 'market']
    stated = all(r['standalone'] == 'yes' or r['reason'] for r in mk)
    ok = len(mk) == 8 and any(r['geo'] == 'tx' for r in tx) and stated
    return ok, (f'Texas and its eight markets listed; {sum(r["standalone"] == "yes" for r in mk)} of 8 standalone; every non-standalone market carries its reason' if ok else 'Texas rows missing or a reason absent')


def g10():
    paths = 'data/markets scripts/markets.py scripts/markets_build.py scripts/markets_fetch.py docs/web-fsc-5 .gitignore'
    rc, out = sh(f"grep -rniE '{NAMES}' {paths}")
    say(f"$ grep -rniE '<pattern>' {paths}"); say(out or '(no match)')
    rc2, authors = sh("git log --format='%an <%ae> | %cn <%ce>' main..HEAD")
    hits = [l for l in authors.splitlines() if re.search(NAMES, l, re.I)]
    say('$ git log --format="%an <%ae> | %cn <%ce>" main..HEAD'); say('\n'.join(sorted(set(authors.splitlines()))))
    return (not out and not hits), ('no match in lane files or commit identities' if not out and not hits else f'matches: {out[:300]} {hits}')


def g11():
    total = 0
    big = []
    for d, _, fs in os.walk(DATA):
        for f in fs:
            p = os.path.join(d, f)
            sz = os.path.getsize(p)
            total += sz
            if sz > 25e6:
                big.append((os.path.relpath(p, ROOT), sz))
    rc, out = sh('git ls-files _cache _bundles')
    say(f'data/markets total {total:,} bytes = {total / 1e6:.2f} MB = {total / 1048576:.2f} MiB; files over 25 MB: {big or "none"}; tracked under _cache or _bundles: {out or "none"}')
    largest = sorted(((os.path.getsize(os.path.join(d, f)), os.path.relpath(os.path.join(d, f), ROOT)) for d, _, fs in os.walk(DATA) for f in fs), reverse=True)[:5]
    say('largest: ' + '; '.join(f'{p} {s / 1e6:.2f} MB' for s, p in largest))
    return total < 60e6 and not big and not out, f'{total / 1e6:.2f} MB ({total / 1048576:.2f} MiB), largest file {largest[0][0] / 1e6:.2f} MB, nothing under _cache tracked'


def main():
    rc, head = sh('git rev-parse HEAD')
    say(f'WEB-FSC-5 gates at HEAD {head}')
    say('runner: python3 docs/web-fsc-5/gates/run_gates.py (from the worktree root). Gates 1, 8 and 10 run shell commands, printed with "$"; '
        'the other gates are checks inside this script over the committed files, and each prints what it measured. The gate record is committed after this run, '
        'so the commit that holds GATES.txt is one record-only commit after the HEAD above.')
    results = [gate(1, 'no served file changed', g1), gate(2, 'coverage', g2), gate(3, 'reconciliation', g3),
               gate(4, 'FOIA status', g4), gate(5, 'NAICS', g5), gate(6, 'independent re-derivation', g6),
               gate(7, 'no synthesized medians, no averaged rates', g7), gate(8, 'render and mutation', g8),
               gate(9, 'Texas', g9), gate(10, 'names and identity', g10), gate(11, 'size', g11)]
    say(f'\nGATES GREEN {sum(results)}/11: ' + ' '.join(f'{i + 1}:{"G" if r else "R"}' for i, r in enumerate(results)))
    open(OUT, 'w', encoding='utf-8').write('\n'.join(LOG) + '\n')
    print('\n'.join(LOG))
    return 0


if __name__ == '__main__':
    sys.exit(main())
