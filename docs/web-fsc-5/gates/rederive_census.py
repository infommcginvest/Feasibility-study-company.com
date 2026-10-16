#!/usr/bin/env python3
"""Gate 6 (Census, CBP, PEP and BEA half) for WEB-FSC-5: independent re-derivation of the ACS 5-year, ACS 1-year,
BEA, PEP and CBP series of the federal-statistics register from the raw files.

Run:  python3 -I docs/web-fsc-5/gates/rederive_census.py      (standard library only, offline)

Scope after the owner's scope change and the second round (16 Oct 2026)
  Covered:      acs5_* (14 series, fairfield-county included), acs1_* (14), bea_* (3), pep_* (7: pep_pop_2020, _2022,
                _2023, pep_change_1y, _3y and the two _pct series), cbp_* (3: cbp_estab, cbp_emp, cbp_estab_per_10k).
  NOT covered:  the building-permit series (removed from the register) and anything under _cache/markets/held/ (never
                opened).  Nor the pipeline: the script does not import or read scripts/markets*.py or
                docs/web-fsc-5/tools/*.py.

Inputs
  raw    _cache/markets/raw/{census_geoinfo/2025, census_acs5/2024_5-year, census_acs1/2024_1-year, bea_cainc1_api/2024,
         census_pep_api/V2023, census_cbp/2023, census_dec2020_ct/2020}
  checked data/markets/series/{acs5_*,acs1_*,bea_*,pep_*,cbp_*}.json
  rules  data/markets/geographies.json (states[].fips, markets[].composition_source and resolved{...}) and data/markets/
         naics-map.json (legacy["2017"] code lists), plus the rules of DECISIONS.md D39/D40 as restated in the brief:
         a cbsa-delineation market takes its CBSA's own row (ACS, PEP, CBP; BEA publishes no MSA file here, so BEA
         sums the CBSA's member counties); a market of one area takes that area; several areas sum additive counts
         with MOE = root sum of squares; per capita income of a set = summed B19313 / summed B01003; unemployment rate
         = summed B23025_005 / summed B23025_003; a median of several areas is null with its components; a Connecticut
         market with an exact planning-region fit uses its planning regions (county equivalents), one with an exact
         legacy fit (fairfield-county) sums the ACS 5-year cousub rows of its towns (the 2020 county subdivisions of
         legacy county 09001, matched by five-digit town code); places and towns get ACS only.  PEP and CBP markets:
         CBSA row for a cbsa market, the sum of the counties for a county set.  CBP classes sum naics-map.json
         legacy["2017"] codes; a class absent from a geography is zero; a class with codes absent at a geography whose
         nearest published parent (5, 4, 3 or 2 digits) holds more than its published 6-digit children is written
         [lower bound, up_to]; per 10,000 uses pep_pop_2023 at the same geography, rounded to 2 decimals.

What it does
  1. Derives, from the raw files only, the expected cell of EVERY (series, geography[, class]) in the register and the
     expected set of geographies (census route).
  2. Draws a seeded stratified random sample of register values and compares each (sample route; the formal gate).
  3. Checks, for every state, ACS 5-year households (and population, occupied units) and PEP 2023 population against
     the sum of its counties.
  4. Looks for ACS sentinel values in any register value.
  5. Checks BEA: no CBSA id carries a state row; a cbsa market is the sum of its member counties.
  6. Writes docs/web-fsc-5/gates/rederive-census-result.json.
"""
import json
import math
import os
import random
import re
import sys
import time
from collections import Counter, defaultdict

SEED = 20261016
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RAW = os.path.join(ROOT, "_cache", "markets", "raw")
DATA = os.path.join(ROOT, "data", "markets")
OUT = os.path.join(HERE, "rederive-census-result.json")
T0 = time.time()

SENTINELS = (-666666666, -999999999, -888888888, -222222222, -333333333, -555555555)
SENT = frozenset(SENTINELS)
TOL_COUNT = 0          # counts: exact
TOL_DOLLAR = 0.5       # dollars: within 0.5
TOL_SHARE = 1e-6       # shares: within 1e-6
TOL_MOE = 0.0101       # the register rounds MOEs to 2 decimals


def log(msg):
    sys.stderr.write("[%6.1fs] %s\n" % (time.time() - T0, msg))


def jl(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


# ----------------------------------------------------------------------------------------------------------
# series catalogue (read from the register's own labels; the table codes are asserted against this map)
# ----------------------------------------------------------------------------------------------------------
B01001_65 = ["B01001_%03d" % i for i in (20, 21, 22, 23, 24, 25, 44, 45, 46, 47, 48, 49)]
ACS_SPEC = {
    # name: (kind, variables, label table code, unit class)
    "pop": ("add", ["B01003_001"], "B01003", "count"),
    "households": ("add", ["B11001_001"], "B11001", "count"),
    "aggregate_income": ("add", ["B19313_001"], "B19313", "dollar"),
    "labor_force": ("add", ["B23025_003"], "B23025", "count"),
    "unemployed": ("add", ["B23025_005"], "B23025", "count"),
    "occupied_units": ("add", ["B25003_001"], "B25003", "count"),
    "owner_occupied": ("add", ["B25003_002"], "B25003", "count"),
    "renter_occupied": ("add", ["B25003_003"], "B25003", "count"),
    "pop65": ("add", B01001_65, "B01001", "count"),
    "median_gross_rent": ("median", ["B25064_001"], "B25064", "dollar"),
    "median_hh_income": ("median", ["B19013_001"], "B19013", "dollar"),
    "median_home_value": ("median", ["B25077_001"], "B25077", "dollar"),
    "per_capita_income": ("pci", ["B19301_001"], "B19301", "dollar"),
    "unemployment_rate": ("urate", ["B23025_005", "B23025_003"], "B23025", "share"),
}
ACS_VARS = sorted(set(v for s in ACS_SPEC.values() for v in s[1]) | {"B01003_001", "B19313_001"})
BEA_SERIES = {"bea_personal_income": 1, "bea_population": 2, "bea_per_capita_income": 3}


# ----------------------------------------------------------------------------------------------------------
# raw loaders
# ----------------------------------------------------------------------------------------------------------
def num(s):
    if s is None:
        return None
    if isinstance(s, (int, float)):
        return s
    t = s.strip()
    if t == "":
        return None
    try:
        return int(t)
    except ValueError:
        return float(t)


def load_acs(vint_dir, levels):
    """-> {level: {geoid: {var(E|M): value or None}}}.  Geoid = concatenation of the geography columns in header
    order (state+county, state+place, state+county+cousub, cbsa code); the nation is geoid 'us'."""
    out = {}
    for level in levels:
        rows = {}
        parts = ("a", "b")
        for part in parts:
            if level.startswith("cousub_"):
                path = os.path.join(vint_dir, "%s_%s.json" % (level, part))
            else:
                path = os.path.join(vint_dir, "%s_%s.json" % (level, part))
            d = jl(path)
            hdr = d[0]
            gcols = [i for i, h in enumerate(hdr) if h != "NAME" and not re.match(r"^B\d{5}_", h)]
            vcols = [(i, h) for i, h in enumerate(hdr) if re.match(r"^B\d{5}_\d{3}[EM]$", h)]
            for row in d[1:]:
                gid = "us" if level == "us" else "".join(row[i] for i in gcols)
                tgt = rows.setdefault(gid, {})
                tgt["NAME"] = row[0]
                for i, h in vcols:
                    tgt[h] = num(row[i])
        out[level] = rows
    return out


def est(row, var):
    """(E, M, mkind).  E is None for a null or a sentinel.  M is a number, or None with mkind in
    'controlled' (-555555555), 'unavailable' (another sentinel or null)."""
    e = row.get(var + "E")
    m = row.get(var + "M")
    if e is None or e in SENT:
        e = None
    if m is None or m in SENT:
        mk = "controlled" if m == -555555555 else "unavailable"
        m = None
    else:
        mk = "ok"
    return e, m, mk


def load_geoinfo():
    d = os.path.join(RAW, "census_geoinfo", "2025")
    state = jl(os.path.join(d, "state.json"))
    county = jl(os.path.join(d, "county.json"))
    cbsa = jl(os.path.join(d, "cbsa.json"))
    st_fips = {}
    for r in state[1:]:
        st_fips[r[2]] = r[0]
    counties = {}
    for r in county[1:]:
        counties[r[2] + r[3]] = r[0]
    cbsas = {}
    for r in cbsa[1:]:
        cbsas[r[1]] = r[0]
    members = defaultdict(set)
    for f in sorted(os.listdir(d)):
        m = re.match(r"cbsa_county_(\d{5})_(\d{2})\.json$", f)
        if not m:
            continue
        t = jl(os.path.join(d, f))
        for r in t[1:]:
            members[r[1]].add(r[2] + r[3])
    return st_fips, counties, cbsas, dict((k, sorted(v)) for k, v in members.items())


def load_bea():
    d = os.path.join(RAW, "bea_cainc1_api", "2024")
    out = {}
    notes = []
    for level in ("us_state", "county", "msa"):
        pass
    for level in ("county", "state", "msa"):
        for line in (1, 2, 3):
            path = os.path.join(d, "cainc1_%s_line%d.json" % (level, line))
            res = jl(path)["BEAAPI"]["Results"]
            if "Data" not in res:
                out[(level, line)] = None
                notes.append("cainc1_%s_line%d.json carries no Data (BEA API error %s): no %s rows" % (
                    level, line, res.get("Error", {}).get("APIErrorCode"), level.upper()))
                continue
            rows = {}
            for x in res["Data"]:
                if x["TimePeriod"] != "2024":
                    continue
                if x["GeoFips"] in rows:
                    raise SystemExit("duplicate BEA row %s %s" % (level, x["GeoFips"]))
                rows[x["GeoFips"]] = x     # the FULL row: GeoName, Code, CL_UNIT, UNIT_MULT, DataValue, NoteRef ...
            out[(level, line)] = rows
    return out, notes


def bea_value(row):
    """Value in dollars/persons from the full row, or None when the row marks the value not available."""
    if row is None:
        return None
    note = (row.get("NoteRef") or "")
    dv = str(row.get("DataValue", "")).strip().replace(",", "")
    if "(NA)" in note or "(NA)" in dv or "(D)" in dv or dv in ("", "NA"):
        return None
    try:
        x = float(dv)
    except ValueError:
        return None
    mult = int(row.get("UNIT_MULT") or 0)
    x = x * (10 ** mult)
    return int(round(x)) if abs(x - round(x)) < 1e-6 else x


# ----------------------------------------------------------------------------------------------------------
# geography
# ----------------------------------------------------------------------------------------------------------
class Geo:
    def __init__(self, geo, st_fips_by_postal):
        self.geo = geo
        self.states = dict((s["id"], s) for s in geo["states"])
        self.fips_of = dict((sid, s["fips"]) for sid, s in self.states.items() if s.get("fips"))
        self.postal_of_fips = dict((v, k) for k, v in self.fips_of.items())
        self.markets = {}
        for m in geo["markets"]:
            self.markets[m["state"] + "/" + m["slug"]] = m


LEGACY_TOWNS = {}     # market id -> [ACS cousub geoids] for a Connecticut market with an exact legacy-county fit


def market_areas(m):
    """ACS areas of a market: list of (level, geoid) or None when the market has no ACS composition."""
    r = m["resolved"]
    src = m["composition_source"]
    if src == "cbsa-delineation":
        return [("cbsa", r["cbsa"])] if r.get("cbsa") else None
    if src == "connecticut-two-schemes":
        if r.get("ct_fit_planning") == "exact":
            return [("county", c) for c in r["ct_planning_regions"]]
        towns = LEGACY_TOWNS.get(m["state"] + "/" + m["slug"])
        if r.get("ct_fit_legacy") == "exact" and towns:
            return [("cousub", t) for t in towns]
        return None
    areas = [("county", c) for c in r.get("counties", [])]
    areas += [("place", p) for p in r.get("places", [])]
    areas += [("cousub", c) for c in r.get("cousubs", [])]
    return areas or None


def area_id(level, gid):
    return {"county": "co-", "place": "pl-", "cousub": "cs-", "cbsa": "cbsa-"}.get(level, "") + gid


def cousub_state(gid):
    return gid[:2]


# ----------------------------------------------------------------------------------------------------------
# ACS derivation
# ----------------------------------------------------------------------------------------------------------
class AcsDeriver:
    def __init__(self, vname, tables, geo, cbsa_members):
        self.vname = vname
        self.t = tables           # level -> geoid -> row
        self.geo = geo
        self.members = cbsa_members

    def row(self, level, gid):
        return self.t.get(level, {}).get(gid)

    def areas_of(self, g):
        """-> (areas, why).  areas None => the geography has no derivable ACS composition."""
        if g == "us":
            return [("us", "us")], None
        if g in self.geo.fips_of:
            return [("state", self.geo.fips_of[g])], None
        if g.startswith("co-"):
            return [("county", g[3:])], None
        if g.startswith("cbsa-"):
            return [("cbsa", g[5:])], None
        m = self.geo.markets.get(g)
        if m is None:
            return None, "unknown id"
        a = market_areas(m)
        if a is None:
            return None, "no ACS composition (%s)" % m["composition_source"]
        return a, None

    def derive(self, name, g):
        """Expected cell for ACS series `name` (e.g. 'pop') at geography id g.
        -> dict(kind, status, v, moe, mnote, num, den, components) ; status in value | null | unpublished | none"""
        kind, variables, _tbl, unit = ACS_SPEC[name]
        areas, why = self.areas_of(g)
        if areas is None:
            return {"status": "none", "why": why}
        rows = []
        for (lv, gid) in areas:
            r = self.row(lv, gid)
            if r is None:
                return {"status": "unpublished", "why": "%s %s not in the raw file" % (lv, gid), "areas": len(areas)}
            rows.append((lv, gid, r))
        multi = len(rows) > 1
        if kind == "add":
            tot = 0
            msq = 0.0
            m_ok = True
            m_controlled = True
            any_null = False
            for lv, gid, r in rows:
                for var in variables:
                    e, m, mk = est(r, var)
                    if e is None:
                        any_null = True
                        continue
                    tot += e
                    if mk != "ok":
                        m_ok = False
                    if mk != "controlled":
                        m_controlled = False
                    if m is not None:
                        msq += float(m) ** 2
            if any_null:
                return {"status": "null", "kind": kind, "multi": multi, "why": "component estimate null/sentinel"}
            out = {"status": "value", "kind": kind, "multi": multi, "v": tot}
            if m_ok:
                out["moe"] = math.sqrt(msq) if (multi or len(variables) > 1) else float(msq ** 0.5)
            else:
                out["moe"] = None
                out["mnote"] = "controlled" if m_controlled else "unavailable"
            return out
        if kind == "median":
            if multi:
                comps = {}
                for lv, gid, r in rows:
                    e, _m, _mk = est(r, variables[0])
                    comps[area_id(lv, gid)] = e
                return {"status": "value", "kind": kind, "multi": True, "v": None, "components": comps}
            lv, gid, r = rows[0]
            e, m, mk = est(r, variables[0])
            if e is None:
                return {"status": "null", "kind": kind, "multi": False, "why": "estimate null/sentinel"}
            out = {"status": "value", "kind": kind, "multi": False, "v": e, "moe": m}
            if m is None:
                out["mnote"] = "controlled" if mk == "controlled" else "unavailable"
            return out
        if kind == "pci":
            if not multi:
                lv, gid, r = rows[0]
                e, m, mk = est(r, "B19301_001")
                if e is None:
                    return {"status": "null", "kind": kind, "multi": False, "why": "estimate null/sentinel"}
                out = {"status": "value", "kind": kind, "multi": False, "v": e, "moe": m}
                if m is None:
                    out["mnote"] = "controlled" if mk == "controlled" else "unavailable"
                return out
            nsum = dsum = 0
            for lv, gid, r in rows:
                n_, _a, _b = est(r, "B19313_001")
                d_, _c, _d = est(r, "B01003_001")
                if n_ is None or d_ is None:
                    return {"status": "null", "kind": kind, "multi": True, "why": "component estimate null/sentinel"}
                nsum += n_
                dsum += d_
            return {"status": "value", "kind": kind, "multi": True, "num": nsum, "den": dsum,
                    "v": (nsum / float(dsum) if dsum else None)}
        if kind == "urate":
            nsum = dsum = 0
            for lv, gid, r in rows:
                n_, _a, _b = est(r, "B23025_005")
                d_, _c, _d = est(r, "B23025_003")
                if n_ is None or d_ is None:
                    return {"status": "null", "kind": kind, "multi": multi, "why": "component estimate null/sentinel"}
                nsum += n_
                dsum += d_
            return {"status": "value", "kind": kind, "multi": multi, "num": nsum, "den": dsum,
                    "v": (nsum / float(dsum) if dsum else None)}
        raise AssertionError(kind)


def close(a, b, tol):
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) <= tol + 1e-9


def compare_acs(name, exp, cell):
    """-> list of problems (empty = match).  cell is the register cell ({'v',...}) or None when absent."""
    kind, _vars, _t, unit = ACS_SPEC[name]
    tol = TOL_COUNT if unit == "count" else TOL_DOLLAR
    probs = []
    if exp["status"] in ("none", "unpublished"):
        if cell is not None:
            probs.append("register has a value where the raw files give none (%s)" % exp.get("why"))
        return probs
    if cell is None:
        return ["register has no value; raw files give %r" % (exp.get("v"),)]
    if not isinstance(cell, dict):
        return ["register cell is not an object: %r" % (cell,)]
    if exp["status"] == "null":
        if cell.get("v") is not None:
            probs.append("register v=%r, raw files give null (%s)" % (cell.get("v"), exp.get("why")))
        if "f" not in cell:
            probs.append("register null carries no flag")
        return probs
    # status value
    if kind == "median" and exp["multi"]:
        if cell.get("v") is not None:
            probs.append("median of several areas must be null, register v=%r" % cell.get("v"))
        rc = cell.get("components")
        if not isinstance(rc, dict):
            probs.append("median of several areas carries no components")
        else:
            if set(rc) != set(exp["components"]):
                probs.append("components ids differ: register %s vs raw %s" % (sorted(rc)[:6], sorted(exp["components"])[:6]))
            else:
                for k, v in exp["components"].items():
                    if not close(rc[k], v, tol):
                        probs.append("component %s: register %r vs raw %r" % (k, rc[k], v))
        return probs
    if kind in ("pci", "urate") and (kind == "urate" or exp["multi"]):
        for k in ("num", "den"):
            if cell.get(k) != exp[k]:
                probs.append("%s: register %r vs raw %r" % (k, cell.get(k), exp[k]))
        if exp["v"] is None:
            if cell.get("v") is not None:
                probs.append("v: register %r vs raw null (zero denominator)" % cell.get("v"))
        else:
            t = TOL_SHARE if kind == "urate" else TOL_DOLLAR
            if cell.get("v") is None or not close(cell["v"], exp["v"], t):
                probs.append("v: register %r vs raw %r" % (cell.get("v"), exp["v"]))
        if "moe" in cell:
            probs.append("a ratio of summed numerator and denominator carries an moe (%r)" % cell["moe"])
        return probs
    # additive, single-area median, single-area per capita income
    if cell.get("v") is None or not close(cell["v"], exp["v"], tol):
        probs.append("v: register %r vs raw %r" % (cell.get("v"), exp["v"]))
    if exp.get("moe") is not None:
        if cell.get("moe") is None:
            probs.append("moe: register has none, raw gives %.2f" % exp["moe"])
        elif abs(cell["moe"] - exp["moe"]) > TOL_MOE:
            probs.append("moe: register %r vs raw %.2f" % (cell["moe"], exp["moe"]))
    else:
        if cell.get("moe") is not None:
            probs.append("moe: register %r but a component MOE is a sentinel/null in the raw file (%s)" % (cell["moe"], exp.get("mnote")))
    return probs


# ----------------------------------------------------------------------------------------------------------
# BEA derivation
# ----------------------------------------------------------------------------------------------------------
class BeaDeriver:
    def __init__(self, bea, geo, cbsa_members, counties):
        self.b = bea
        self.geo = geo
        self.members = cbsa_members
        self.counties = counties

    def line(self, level, line, fips):
        rows = self.b.get((level, line))
        if rows is None:
            return None
        return bea_value(rows.get(fips))

    def areas(self, g):
        """-> ('us'|'state'|'county'|'set', [county fips], why)"""
        if g == "us":
            return "us", None, None
        if g in self.geo.fips_of:
            return "state", self.geo.fips_of[g], None
        if g.startswith("co-"):
            return "county", [g[3:]], None
        if g.startswith("cbsa-"):
            mem = self.members.get(g[5:])
            if not mem:
                return None, None, "CBSA has no member counties in the geoinfo files"
            return "set", mem, None
        m = self.geo.markets.get(g)
        if m is None:
            return None, None, "unknown id"
        src = m["composition_source"]
        r = m["resolved"]
        if src == "cbsa-delineation":
            mem = self.members.get(r.get("cbsa"))
            return ("set", mem, None) if mem else (None, None, "CBSA has no members")
        if src == "connecticut-two-schemes":
            if r.get("ct_fit_planning") == "exact":
                return "set", list(r["ct_planning_regions"]), None
            if r.get("ct_fit_legacy") == "exact":
                return "set", list(r["ct_legacy_counties"]), None
            return None, None, "no exact Connecticut fit"
        if r.get("places") or r.get("cousubs"):
            return None, None, "not published at this grain (place or town)"
        if not r.get("counties"):
            return None, None, "no composition"
        return "set", list(r["counties"]), None

    def derive(self, sid, g):
        line = BEA_SERIES[sid]
        kind, a, why = self.areas(g)
        if kind is None:
            return {"status": "none", "why": why}
        if kind == "us":
            v = self.line("state", line, "00000")
            return {"status": "value" if v is not None else "null", "v": v, "multi": False}
        if kind == "state":
            v = self.line("state", line, a + "000")
            return {"status": "value" if v is not None else "null", "v": v, "multi": False}
        fl = sorted(set(a))
        single = len(fl) == 1
        vals = {}
        for f in fl:
            if (self.b.get(("county", 1)) or {}).get(f) is None:
                return {"status": "null", "why": "county %s is in no BEA county row (combination area or absent)" % f, "multi": not single}
            x1 = self.line("county", 1, f)
            x2 = self.line("county", 2, f)
            x3 = self.line("county", 3, f)
            if x1 is None or x2 is None or x3 is None:
                return {"status": "null", "why": "county %s is (NA) in the BEA row" % f, "multi": not single}
            vals[f] = (x1, x2, x3)
        if line == 3:
            if single:
                return {"status": "value", "v": vals[fl[0]][2], "multi": False}
            n_ = sum(v[0] for v in vals.values())
            d_ = sum(v[1] for v in vals.values())
            return {"status": "value", "v": (n_ / float(d_) if d_ else None), "num": n_, "den": d_, "multi": True}
        idx = 0 if line == 1 else 1
        return {"status": "value", "v": sum(v[idx] for v in vals.values()), "multi": not single}


def compare_bea(sid, exp, cell):
    line = BEA_SERIES[sid]
    probs = []
    if exp["status"] == "none":
        if cell is not None:
            probs.append("register has a value where the raw files give none (%s)" % exp.get("why"))
        return probs
    if cell is None:
        return ["register has no value; raw files give %r" % (exp.get("v"),)]
    if not isinstance(cell, dict):
        return ["register cell is not an object: %r" % (cell,)]
    if exp["status"] == "null":
        if cell.get("v") is not None:
            probs.append("register v=%r, raw files give null (%s)" % (cell.get("v"), exp.get("why")))
        return probs
    tol = 0 if line in (1, 2) else TOL_DOLLAR
    if cell.get("v") is None or not close(cell["v"], exp["v"], tol):
        probs.append("v: register %r vs raw %r" % (cell.get("v"), exp["v"]))
    if line == 3 and exp.get("multi"):
        for k in ("num", "den"):
            if cell.get(k) != exp.get(k):
                probs.append("%s: register %r vs raw %r" % (k, cell.get(k), exp.get(k)))
    return probs


# ----------------------------------------------------------------------------------------------------------
# helpers on the register
# ----------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------
# round 2: PEP Vintage 2023 (Census Data API), CBP 2023 (Census Data API), Connecticut towns (2020 Census)
# ----------------------------------------------------------------------------------------------------------
def load_pep(states):
    d = os.path.join(RAW, "census_pep_api", "V2023")
    out = {}
    for level in ("us", "state", "county", "cbsa"):
        t = jl(os.path.join(d, level + ".json"))
        hdr = t[0]
        iy, im, ip = hdr.index("YEAR"), hdr.index("MONTH"), hdr.index("POP")
        rows = {}
        for r in t[1:]:
            if r[im] != "7":            # July 1 estimates only (MONTH 4 is the April 2020 base)
                continue
            if level == "us":
                gid = "us"
            elif level == "county":
                gid = r[-2] + r[-1]
            else:
                gid = r[-1]
            rows.setdefault(gid, {})[int(r[iy])] = int(r[ip])
        out[level] = rows
    return out


def load_cbp(states):
    """-> {level: {geoid: {naics code: (ESTAB, EMP)}}} from the all-industry API responses."""
    d = os.path.join(RAW, "census_cbp", "2023")
    out = {"us": {}, "state": {}, "county": {}, "cbsa": {}}

    def read(path, level):
        t = jl(path)
        hdr = t[0]
        ie, im, ic = hdr.index("ESTAB"), hdr.index("EMP"), hdr.index("NAICS2017")
        for r in t[1:]:
            if level == "us":
                gid = "us"
            elif level == "county":
                gid = r[-2] + r[-1]
            else:
                gid = r[-1]
            out[level].setdefault(gid, {})[r[ic]] = (int(r[ie]), int(r[im]))

    read(os.path.join(d, "us_all.json"), "us")
    read(os.path.join(d, "state_all.json"), "state")
    read(os.path.join(d, "cbsa_all.json"), "cbsa")
    for fips in sorted(states):
        path = os.path.join(d, "county_%s.json" % fips)
        if os.path.exists(path):
            read(path, "county")
    return out


SECTOR = {"31": "31-33", "32": "31-33", "33": "31-33", "44": "44-45", "45": "44-45", "48": "48-49", "49": "48-49"}


def naics_parents(code, sector_ranges=True):
    """nearest first: 5, 4, 3 and 2 digits.  The API publishes the 2-digit level of NAICS 31/32/33, 44/45 and 48/49 only as
    the sector ranges '31-33', '44-45', '48-49'.  sector_ranges=True (primary reading) takes the range as the 2-digit parent
    of those codes; False (literal reading) looks for the two-digit string itself, which is never published."""
    return [code[:5], code[:4], code[:3], (SECTOR.get(code[:2], code[:2]) if sector_ranges else code[:2])]


def legacy_towns(geo_markets, dec_path, acs5_cousub):
    """Connecticut markets with an exact legacy-county fit -> their ACS cousub geoids: the 2020 county subdivisions of the
    legacy county, matched to the 2025 ACS cousub rows by the five-digit town code (the placeholder 'County subdivisions
    not defined', code 00000, is not a town and is dropped)."""
    out = {}
    notes = []
    dec = jl(dec_path)
    hdr = dec[0]
    ic, it, ip = hdr.index("county"), hdr.index("county subdivision"), hdr.index("P1_001N")
    for mid, m in geo_markets.items():
        r = m["resolved"]
        if m["composition_source"] != "connecticut-two-schemes" or r.get("ct_fit_legacy") != "exact":
            continue
        towns = []
        for lc in r.get("ct_legacy_counties", []):
            for row in dec[1:]:
                if row[ic] == lc[2:] and row[it] != "00000":
                    towns.append(row[it])
        gids = []
        for t in sorted(set(towns)):
            hit = [g for g in acs5_cousub if g[:2] == "09" and g[5:] == t]
            if len(hit) != 1:
                notes.append("%s: town code %s matches %d ACS cousub rows" % (mid, t, len(hit)))
                continue
            gids.append(hit[0])
        out[mid] = gids
        notes.append("%s: %d towns of legacy county %s in the 2020 Census file (%s), %d matched to one 2025 ACS cousub row each; "
                     "register ct_legacy_towns lists %d" % (mid, len(set(towns)), r.get("ct_legacy_counties"),
                                                           "population %s" % sum(int(row[ip]) for row in dec[1:] if row[ic] == r["ct_legacy_counties"][0][2:]),
                                                           len(gids), len(r.get("ct_legacy_towns", []))))
        if sorted(gids) != sorted(r.get("ct_legacy_towns", [])):
            notes.append("%s: my town list differs from resolved.ct_legacy_towns (mine only %s ; theirs only %s)" % (
                mid, sorted(set(gids) - set(r.get("ct_legacy_towns", [])))[:5], sorted(set(r.get("ct_legacy_towns", [])) - set(gids))[:5]))
    return out, notes


def county_spec(g, G):
    """PEP and CBP composition of a geography id: ('us',), ('state', fips), ('counties', [fips]), ('cbsa', code) or
    (None, why)."""
    if g == "us":
        return ("us", "us")
    if g in G.fips_of:
        return ("state", G.fips_of[g])
    if g.startswith("co-"):
        return ("counties", [g[3:]])
    if g.startswith("cbsa-"):
        return ("cbsa", g[5:])
    m = G.markets.get(g)
    if m is None:
        return (None, "unknown id")
    r = m["resolved"]
    src = m["composition_source"]
    if src == "cbsa-delineation":
        return ("cbsa", r["cbsa"]) if r.get("cbsa") else (None, "no CBSA")
    if src == "connecticut-two-schemes":
        if r.get("ct_fit_planning") == "exact":
            return ("counties", list(r["ct_planning_regions"]))
        return (None, "legacy-county fit: the PEP and CBP files cover the planning regions")
    if r.get("places") or r.get("cousubs"):
        return (None, "not published at this grain (place or town)")
    if not r.get("counties"):
        return (None, "no composition")
    return ("counties", list(r["counties"]))


PEP_SERIES = {
    "pep_pop_2020": ("pop", 2020, None), "pep_pop_2022": ("pop", 2022, None), "pep_pop_2023": ("pop", 2023, None),
    "pep_change_1y": ("change", 2023, 2022), "pep_change_3y": ("change", 2023, 2020),
    "pep_change_1y_pct": ("pct", 2023, 2022), "pep_change_3y_pct": ("pct", 2023, 2020),
}


class PepDeriver:
    def __init__(self, rows, geo):
        self.r = rows
        self.geo = geo

    def pop(self, year, g):
        spec = county_spec(g, self.geo)
        kind = spec[0]
        if kind is None:
            return None, spec[1]
        if kind == "us":
            v = self.r["us"].get("us", {}).get(year)
            return v, "no US row"
        if kind in ("state", "cbsa"):
            v = self.r[kind].get(spec[1], {}).get(year)
            return v, "%s %s not in the raw file" % (kind, spec[1])
        tot = 0
        for c in spec[1]:
            v = self.r["county"].get(c, {}).get(year)
            if v is None:
                return None, "county %s not in the raw file" % c
            tot += v
        return tot, None

    def derive(self, sid, g):
        kind, y2, y1 = PEP_SERIES[sid]
        p2, why = self.pop(y2, g)
        if p2 is None:
            return {"status": "none" if spec_none(g, self.geo) else "unpublished", "why": why}
        if kind == "pop":
            return {"status": "value", "v": p2}
        p1, why = self.pop(y1, g)
        if p1 is None:
            return {"status": "unpublished", "why": why}
        if kind == "change":
            return {"status": "value", "v": p2 - p1}
        return {"status": "value", "num": p2 - p1, "den": p1, "v": ((p2 - p1) / float(p1) if p1 else None)}


def spec_none(g, geo):
    return county_spec(g, geo)[0] is None


def compare_pep(sid, exp, cell):
    kind = PEP_SERIES[sid][0]
    probs = []
    if exp["status"] in ("none", "unpublished"):
        if cell is not None:
            probs.append("register has a value where the raw files give none (%s)" % exp.get("why"))
        return probs
    if cell is None:
        return ["register has no value; raw files give %r" % (exp.get("v"),)]
    if kind == "pct":
        if not isinstance(cell, dict):
            return ["register cell is not an object: %r" % (cell,)]
        for k in ("num", "den"):
            if cell.get(k) != exp[k]:
                probs.append("%s: register %r vs raw %r" % (k, cell.get(k), exp[k]))
        if exp["v"] is None:
            if cell.get("v") is not None:
                probs.append("v: register %r vs raw null (zero denominator)" % cell.get("v"))
        elif cell.get("v") is None or abs(cell["v"] - exp["v"]) > TOL_SHARE + 1e-9:
            probs.append("v: register %r vs raw %r" % (cell.get("v"), exp["v"]))
        return probs
    if isinstance(cell, dict):
        cell = cell.get("v")
    if cell != exp["v"]:
        probs.append("v: register %r vs raw %r" % (cell, exp["v"]))
    return probs


CBP_SERIES = ("cbp_estab", "cbp_emp", "cbp_estab_per_10k")


class CbpDeriver:
    def __init__(self, rows, geo, classes, pep, sector_ranges=True):
        self.r = rows
        self.geo = geo
        self.classes = classes       # slug -> [6-digit codes of NAICS 2017]
        self.pep = pep
        self.sector = sector_ranges
        self._tab = {}
        self.negative_gaps = 0
        self.gap_unit_diff = 0

    def table(self, level, gid):
        """class table of one published geography: slug -> (lower estab, lower emp, up_to estab, up_to emp)"""
        key = (level, gid)
        t = self._tab.get(key)
        if t is not None:
            return t
        rows = self.r[level].get(gid)
        out = {}
        if rows:
            child_e = defaultdict(int)
            child_m = defaultdict(int)
            for code, (e, m) in rows.items():
                if len(code) == 6 and code.isdigit():
                    for p in naics_parents(code, self.sector):
                        child_e[p] += e
                        child_m[p] += m
            for slug, codes in self.classes.items():
                le = lm = 0
                ge = {}
                gm = {}
                for c in codes:
                    cell = rows.get(c)
                    if cell is not None:
                        le += cell[0]
                        lm += cell[1]
                        continue
                    for p in naics_parents(c, self.sector):
                        pc = rows.get(p)
                        if pc is not None:
                            d_e = pc[0] - child_e.get(p, 0)
                            d_m = pc[1] - child_m.get(p, 0)
                            if d_e < 0:
                                self.negative_gaps += 1
                            ge[p] = max(0, d_e)
                            gm[p] = max(0, d_m)
                            break
                ue, um = sum(ge.values()), sum(gm.values())
                if le or ue or lm:
                    out[slug] = (le, lm, ue, um)
        self._tab[key] = out
        return out

    def classes_of(self, g):
        """-> (status, why, {slug: (le, lm, ue, um)})"""
        spec = county_spec(g, self.geo)
        kind = spec[0]
        if kind is None:
            return "none", spec[1], {}
        if kind in ("us", "state", "cbsa"):
            level = kind
            gid = spec[1]
            if gid not in self.r[level]:
                return "unpublished", "%s %s not in the raw file" % (level, gid), {}
            return "value", None, self.table(level, gid)
        acc = {}
        for c in spec[1]:
            for slug, v in self.table("county", c).items():
                a = acc.get(slug)
                acc[slug] = tuple(x + y for x, y in zip(a, v)) if a else v
        return "value", None, acc

    def expected(self, sid, g):
        """-> (status, why, {slug: cell}) with only the classes present (absent = zero)"""
        status, why, tab = self.classes_of(g)
        if status != "value":
            return status, why, {}
        out = {}
        if sid == "cbp_estab_per_10k":
            pop, _w = self.pep.pop(2023, g)
            if pop is None:
                return "unpublished", "no PEP 2023 population at this geography", {}
        for slug, (le, lm, ue, um) in tab.items():
            if not (le or ue):
                continue
            if sid == "cbp_estab":
                lower = le
            elif sid == "cbp_emp":
                lower = lm
            else:
                lower = round(le * 10000.0 / pop, 2)
            out[slug] = [lower, ue] if ue > 0 else lower
        return "value", None, out

    def emp_gap_employees(self, g, slug):
        status, why, tab = self.classes_of(g)
        v = tab.get(slug)
        return v[3] if v else 0


def compare_cbp_cell(sid, reg_cell, exp_cell):
    """both None => absent (zero).  -> list of problems."""
    if reg_cell is None and exp_cell is None:
        return []
    if reg_cell is None:
        return ["register has no cell (zero); raw files give %r" % (exp_cell,)]
    if exp_cell is None:
        return ["register has %r; raw files give no establishment (zero)" % (reg_cell,)]
    tol = 0.006 if sid == "cbp_estab_per_10k" else 0
    rl = isinstance(reg_cell, list)
    el = isinstance(exp_cell, list)
    if rl != el:
        return ["lower-bound form differs: register %r vs raw %r" % (reg_cell, exp_cell)]
    probs = []
    a = reg_cell[0] if rl else reg_cell
    b = exp_cell[0] if el else exp_cell
    if abs(a - b) > tol + 1e-9:
        probs.append("value: register %r vs raw %r" % (a, b))
    if rl and reg_cell[1] != exp_cell[1]:
        probs.append("up_to: register %r vs raw %r" % (reg_cell[1], exp_cell[1]))
    return probs



def scan_sentinels(obj, path, found):
    if isinstance(obj, dict):
        for k, v in obj.items():
            scan_sentinels(v, path + [k], found)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan_sentinels(v, path + [i], found)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        if obj in SENT:
            found.append(path)


def short(cell):
    return cell


def main():
    notes = []
    st_fips_raw, counties, cbsas, members = load_geoinfo()
    geo_json = jl(os.path.join(DATA, "geographies.json"))
    G = Geo(geo_json, st_fips_raw)
    # state FIPS in geographies.json must agree with the raw geoinfo state list
    bad_fips = [(sid, s["fips"]) for sid, s in G.states.items() if s.get("fips") and s["fips"] not in st_fips_raw]
    if bad_fips:
        notes.append("states[].fips not in the raw state list: %s" % bad_fips)

    acs5 = load_acs(os.path.join(RAW, "census_acs5", "2024_5-year"), ["us", "state", "county", "cbsa", "place"])
    acs1 = load_acs(os.path.join(RAW, "census_acs1", "2024_1-year"), ["us", "state", "county", "cbsa", "place"])
    # cousub files only for the states whose markets are built from a town (any state with a cousub in resolved)
    need_cs = set(c[:2] for m in G.markets.values() for c in m["resolved"].get("cousubs", []))
    if any(m["composition_source"] == "connecticut-two-schemes" and m["resolved"].get("ct_fit_legacy") == "exact" for m in G.markets.values()):
        need_cs.add("09")
    need_cs = sorted(need_cs)
    cs5 = load_acs(os.path.join(RAW, "census_acs5", "2024_5-year"), ["cousub_%s" % s for s in need_cs]) if need_cs else {}
    acs5["cousub"] = {}
    for k, rows in cs5.items():
        acs5["cousub"].update(rows)
    acs1["cousub"] = {}
    lt, lt_notes = legacy_towns(G.markets, os.path.join(RAW, "census_dec2020_ct", "2020", "ct_cousub_2020.json"), acs5["cousub"])
    LEGACY_TOWNS.update(lt)
    log("ACS loaded: 5-year %s ; 1-year %s ; cousub states %s" % (
        dict((k, len(v)) for k, v in acs5.items()), dict((k, len(v)) for k, v in acs1.items()), need_cs))
    bea, bea_notes = load_bea()
    notes.extend(bea_notes)
    notes.extend(lt_notes)
    pep_rows = load_pep(G.fips_of.values())
    cbp_rows = load_cbp(G.fips_of.values())
    log("PEP loaded: %s ; CBP loaded: %s" % (dict((k, len(v)) for k, v in pep_rows.items()), dict((k, len(v)) for k, v in cbp_rows.items())))
    log("BEA loaded: %s" % dict((k, (len(v) if v else None)) for k, v in bea.items()))

    # raw-side consistency: CBSA membership vs geographies.json cbsas rows
    reg_cbsa = dict((r["code"], sorted(r["counties"])) for r in geo_json["cbsas"]["rows"])
    diff_cbsa = [c for c in members if reg_cbsa.get(c) != members[c]]
    notes.append("CBSA membership from the 1,002 raw geoinfo cbsa_county files: %d CBSAs, %d differ from geographies.json cbsas rows%s." % (
        len(members), len(diff_cbsa), (": %s" % diff_cbsa[:6]) if diff_cbsa else ""))
    only_in_list = sorted(set(cbsas) - set(members))
    if only_in_list:
        notes.append("CBSAs in cbsa.json with no member file: %s" % only_in_list[:6])

    # the register
    sids_acs5 = sorted("acs5_" + n for n in ACS_SPEC)
    sids_acs1 = sorted("acs1_" + n for n in ACS_SPEC)
    sids_bea = sorted(BEA_SERIES)
    sids_pep = sorted(PEP_SERIES)
    sids_cbp = list(CBP_SERIES)
    sids_all = sids_acs5 + sids_acs1 + sids_bea + sids_pep + sids_cbp
    reg = {}
    for sid in sids_all:
        reg[sid] = jl(os.path.join(DATA, "series", sid + ".json"))
    # PEP labels name the year(s) they difference
    for sid, (kind, y2, y1) in PEP_SERIES.items():
        lab = reg[sid]["label"]
        need = ["July 1, %d" % y2] if kind == "pop" else [str(y1), str(y2)]
        if not all(x in lab for x in need) or "V2023" not in reg[sid].get("vintage", "V2023"):
            notes.append("label of %s does not name %s: %r" % (sid, need, lab))
    naics_map = jl(os.path.join(DATA, "naics-map.json"))
    classes = {}
    fallback = []
    for c in naics_map["classes"]:
        codes = c.get("legacy", {}).get("2017")
        if not codes:
            codes = c["naics2022"]
            fallback.append(c["slug"])
        classes[c["slug"]] = [str(x) for x in codes]
    # label table codes vs the spec
    for name, spec in ACS_SPEC.items():
        for pre in ("acs5_", "acs1_"):
            lab = reg[pre + name]["label"]
            if spec[2] not in lab:
                notes.append("label of %s does not name table %s: %r" % (pre + name, spec[2], lab))
    for sid in sids_bea:
        lab = reg[sid]["label"]
        if "line %d" % BEA_SERIES[sid] not in lab.replace("CAINC1 line", "line").replace("(CAINC1 line", "line") and sid != "bea_per_capita_income":
            notes.append("label of %s: %r" % (sid, lab))

    D5 = AcsDeriver("acs5", acs5, G, members)
    D1 = AcsDeriver("acs1", acs1, G, members)
    DB = BeaDeriver(bea, G, members, counties)
    DP = PepDeriver(pep_rows, G)
    DC = CbpDeriver(cbp_rows, G, classes, DP, sector_ranges=True)
    DC_lit = CbpDeriver(cbp_rows, G, classes, DP, sector_ranges=False)
    cbp_cache = {}
    cbp_cache_lit = {}

    def cbp_exp(sid, g):
        k = (sid, g)
        if k not in cbp_cache:
            cbp_cache[k] = DC.expected(sid, g)
        return cbp_cache[k]

    def cbp_exp_lit(sid, g):
        k = (sid, g)
        if k not in cbp_cache_lit:
            cbp_cache_lit[k] = DC_lit.expected(sid, g)
        return cbp_cache_lit[k]

    sector_explained = Counter()      # CBP cells that differ under the primary reading, split by whether the literal reading explains them
    sector_geos = defaultdict(set)

    def derive_any(sid, g):
        if sid.startswith("acs5_"):
            return D5.derive(sid[5:], g)
        if sid.startswith("acs1_"):
            return D1.derive(sid[5:], g)
        if sid.startswith("pep_"):
            return DP.derive(sid, g)
        if sid.startswith("cbp_"):
            status, why, cells = cbp_exp(sid, g)
            return {"status": status, "why": why, "cells": cells}
        return DB.derive(sid, g)

    def compare_any(sid, exp, cell):
        if sid.startswith("bea_"):
            return compare_bea(sid, exp, cell)
        if sid.startswith("pep_"):
            return compare_pep(sid, exp, cell)
        return compare_acs(sid[5:], exp, cell)

    # geography kinds ------------------------------------------------------------------------------------
    def multi_state_cbsa(code):
        mem = members.get(code, [])
        return len(set(c[:2] for c in mem)) >= 2

    def kind_of(g):
        if g == "us":
            return "us"
        if g in G.fips_of:
            return "state"
        if g.startswith("co-"):
            return "ct-county-equivalent" if g.startswith("co-091") else "county"
        if g.startswith("cbsa-"):
            return "cbsa-cross-state" if multi_state_cbsa(g[5:]) else "cbsa"
        m = G.markets.get(g)
        if m is None:
            return "unknown"
        src = m["composition_source"]
        if src == "connecticut-two-schemes":
            return "ct-market"
        if m["kind"] == "cross-state":
            return "market-cross-state"
        if src == "cbsa-delineation":
            return "market-cbsa-cross-state" if multi_state_cbsa(m["resolved"]["cbsa"]) else "market-cbsa"
        if src == "sub-county" or m["resolved"].get("places") or m["resolved"].get("cousubs"):
            return "market-place"
        a = market_areas(m)
        if a and len(a) > 1:
            return "market-multi-county"
        return "market-single-county"

    # ------------------------------------------------------------------------------------------------------
    # census: every (series, geography[, class]) in the register, plus the expected geography set
    # ------------------------------------------------------------------------------------------------------
    census = {}
    census_detail = []
    coverage = {}
    n_cmp = n_bad = 0
    cand_all = ["us"] + sorted(G.fips_of) + ["co-" + c for c in counties] + ["cbsa-" + c for c in cbsas] + sorted(G.markets)
    for sid in sids_all:
        values = reg[sid]["values"]
        nulls = reg[sid].get("nulls", {})
        c_n = c_bad = 0
        for g in sorted(values):
            if sid.startswith("cbp_"):
                status, why, cells = cbp_exp(sid, g)
                regc = values[g] if isinstance(values[g], dict) else {}
                unknown = sorted(set(regc) - set(classes))
                if status != "value":
                    # the register holds an entry (an empty one reads as zero establishments in every class) for a geography
                    # the raw files do not publish
                    c_n += 1
                    c_bad += 1
                    census_detail.append({"series": sid, "geo": g, "class": "*", "register": "%d classes" % len(regc),
                                          "rederived": status, "problems": ["register holds an entry (%d classes; empty = zero in every class) where the raw "
                                                                            "files carry no row for this geography (%s)" % (len(regc), why)],
                                          "explained_by_sector_range_rule": False})
                    sector_explained[(sid, "NOT explained")] += 1
                    continue
                _st2, _w2, cells_lit = cbp_exp_lit(sid, g)
                for slug in classes:
                    probs = compare_cbp_cell(sid, regc.get(slug), cells.get(slug))
                    c_n += 1
                    if probs:
                        c_bad += 1
                        lit_ok = not compare_cbp_cell(sid, regc.get(slug), cells_lit.get(slug))
                        sector_explained[(sid, "explained by the sector-range parent rule" if lit_ok else "NOT explained")] += 1
                        if lit_ok:
                            sector_geos[sid].add(g)
                        if (not lit_ok) or sum(1 for d_ in census_detail if d_.get("explained_by_sector_range_rule")) < 60:
                            census_detail.append({"series": sid, "geo": g, "class": slug, "register": regc.get(slug),
                                                  "rederived": cells.get(slug), "rederived_literal_2_digit": cells_lit.get(slug),
                                                  "problems": probs, "explained_by_sector_range_rule": lit_ok})
                if unknown:
                    c_n += 1
                    c_bad += 1
                    census_detail.append({"series": sid, "geo": g, "class": unknown, "register": "unknown class keys", "rederived": None,
                                          "problems": ["class keys not in naics-map.json: %s" % unknown]})
                continue
            cell = values[g].get("all") if isinstance(values[g], dict) else None
            exp = derive_any(sid, g)
            probs = compare_any(sid, exp, cell)
            c_n += 1
            if probs:
                c_bad += 1
                if len(census_detail) < 5000:
                    census_detail.append({"series": sid, "geo": g, "class": "all", "register": cell,
                                          "rederived": dict((k, v) for k, v in exp.items() if k not in ("why",)),
                                          "problems": probs})
        # coverage: every geography the raw files can value must be in the register; a MARKET with no value in the raw
        # files must be listed in the series' "nulls" (or carry a flagged null cell); the register may hold no id the raw
        # files cannot value
        expected_vals = set()
        derived_null = []
        for g in cand_all:
            if g.startswith("cbsa-") and sid.startswith("bea_"):
                continue      # BEA publishes no MSA file here: no CBSA id is expected in the BEA series
            exp = derive_any(sid, g)
            if exp["status"] == "value":
                expected_vals.add(g)
            elif g in G.markets and g not in nulls:
                cell_ = (values.get(g) or {}).get("all") if isinstance(values.get(g), dict) else None
                if not (isinstance(cell_, dict) and cell_.get("v") is None and "f" in cell_):
                    derived_null.append(g)
            elif g in G.markets and g in values and exp["status"] in ("none", "unpublished"):
                derived_null.append(g)     # listed as null but also carries a value
        absent_by_design = sorted(g for g in cand_all if g.startswith("co-") and derive_any(sid, g)["status"] != "value" and g not in values)
        missing = sorted(g for g in expected_vals if g not in values) + ["(null not listed) " + g for g in derived_null]
        extra = sorted(g for g in values if g not in expected_vals and derive_any(sid, g)["status"] not in ("null",))
        coverage[sid] = {"expected": len(expected_vals), "register": len(values), "missing": missing, "extra": extra,
                         "counties_absent_because_raw_has_no_value": len(absent_by_design)}
        census[sid] = (c_n, c_bad)
        n_cmp += c_n
        n_bad += c_bad
    log("census: %d compared, %d with problems" % (n_cmp, n_bad))

    # ------------------------------------------------------------------------------------------------------
    # the sample
    # ------------------------------------------------------------------------------------------------------
    rng = random.Random(SEED)

    def pick(seq):
        return seq[min(len(seq) - 1, int(rng.random() * len(seq)))]

    def draw(pool, cnt, whole=False):
        if not pool:
            return []
        if whole and len(pool) <= cnt + 1:
            return list(pool)
        chosen = []
        tries = 0
        while len(chosen) < min(cnt, len(pool)) and tries < 300:
            tries += 1
            g = pick(pool)
            if g not in chosen:
                chosen.append(g)
        return chosen

    STRATA = [("us", 1), ("state", 1), ("county", 2), ("ct-county-equivalent", 1), ("cbsa", 2), ("cbsa-cross-state", 1),
              ("market-cbsa", 2), ("market-cbsa-cross-state", 1), ("market-multi-county", 2), ("market-single-county", 1),
              ("market-place", 1), ("ct-market", 1), ("market-cross-state", 1)]
    sample = []          # (series, geo, stratum, class, round)
    # round 1 (ACS 5-year, ACS 1-year, BEA) -- the draws of the first round, unchanged in design
    for sid in sids_acs5 + sids_acs1 + sids_bea:
        values = reg[sid]["values"]
        pools = defaultdict(list)
        for g in sorted(values):
            pools[kind_of(g)].append(g)
        for stratum, cnt in STRATA:
            for g in draw(pools.get(stratum, []), cnt, whole=(stratum.startswith("cbsa") and sid.startswith("bea_"))):
                sample.append((sid, g, stratum, "all", 1))
    # a multi-area median must be drawn for every vintage: top up
    for sid in [s_ for s_ in sids_acs5 + sids_acs1 if "median" in s_]:
        extra_pool = [g for g in sorted(reg[sid]["values"]) if kind_of(g) in ("market-multi-county", "market-place")]
        for _ in range(2):
            g = pick(extra_pool)
            if (sid, g, kind_of(g), "all", 1) not in sample:
                sample.append((sid, g, kind_of(g), "all", 1))

    # round 2: PEP, CBP and the fairfield-county ACS 5-year values
    STRATA_PEP = [("us", 1), ("state", 2), ("county", 2), ("ct-county-equivalent", 1), ("cbsa", 2), ("cbsa-cross-state", 1),
                  ("market-cbsa", 2), ("market-cbsa-cross-state", 1), ("market-multi-county", 2), ("market-single-county", 1),
                  ("ct-market", 3), ("market-cross-state", 2)]
    STRATA_CBP = [("us", 2), ("state", 3), ("county", 3), ("ct-county-equivalent", 1), ("cbsa", 3), ("cbsa-cross-state", 2),
                  ("market-cbsa", 3), ("market-cbsa-cross-state", 2), ("market-multi-county", 3), ("market-single-county", 2),
                  ("ct-market", 3), ("market-cross-state", 3)]
    for sid in sids_pep:
        pools = defaultdict(list)
        for g in sorted(reg[sid]["values"]):
            pools[kind_of(g)].append(g)
        for stratum, cnt in STRATA_PEP:
            for g in draw(pools.get(stratum, []), cnt):
                sample.append((sid, g, stratum, "all", 2))
    for sid in sids_cbp:
        values = reg[sid]["values"]
        pools = defaultdict(list)
        for g in sorted(values):
            pools[kind_of(g)].append(g)
        for stratum, cnt in STRATA_CBP:
            for g in draw(pools.get(stratum, []), cnt):
                regc = values[g]
                lb = sorted(k for k, v in regc.items() if isinstance(v, list))
                present = sorted(regc)
                r_ = rng.random()
                if r_ < 0.35 and lb:
                    slug = pick(lb)
                elif r_ < 0.80 and present:
                    slug = pick(present)
                else:
                    slug = pick(sorted(classes))
                sample.append((sid, g, stratum, slug, 2))
    for sid in sids_acs5:
        if "connecticut/fairfield-county" in reg[sid]["values"]:
            sample.append((sid, "connecticut/fairfield-county", "ct-market", "all", 2))
    # every register id the raw files cannot value is sampled whole (a small pool: a defect there must not depend on the draw)
    targeted = defaultdict(list)
    for sid in sids_all:
        for g in sorted(reg[sid]["values"]):
            if derive_any(sid, g)["status"] in ("none", "unpublished"):
                targeted[sid].append(g)
                sample.append((sid, g, "register-id-without-raw-data", sorted(classes)[0] if sid.startswith("cbp_") else "all",
                               2 if sid.startswith(("pep_", "cbp_")) else 1))

    samples = []
    mismatch_detail = []
    by_kind = defaultdict(lambda: [0, 0])
    seen = set()
    for sid, g, stratum, slug, rnd in sample:
        if (sid, g, slug) in seen:
            continue
        seen.add((sid, g, slug))
        values = reg[sid]["values"]
        k = kind_of(g)
        if sid.startswith("cbp_"):
            status, why, cells = cbp_exp(sid, g)
            if status != "value":
                slug = "*"
            cell = values[g].get(slug) if status == "value" else values[g]
            exp_cell = cells.get(slug)
            probs = compare_cbp_cell(sid, cell, exp_cell) if status == "value" else ["raw files give no value (%s)" % why]
            rederived = exp_cell
            lit_cell = cbp_exp_lit(sid, g)[2].get(slug)
            lit_probs = compare_cbp_cell(sid, cell, lit_cell) if status == "value" else probs
        else:
            cell = values[g].get("all")
            exp = derive_any(sid, g)
            probs = compare_any(sid, exp, cell)
            rederived = dict((a_, b_) for a_, b_ in exp.items() if a_ not in ("why",))
            lit_probs = probs
            lit_cell = None
        by_kind[k][1] += 1
        if not probs:
            by_kind[k][0] += 1
        else:
            mismatch_detail.append({"series": sid, "geo": g, "class": slug, "register": cell, "rederived": rederived, "problems": probs,
                                    "rederived_literal_2_digit": lit_cell if sid.startswith("cbp_") else None,
                                    "explained_by_sector_range_rule": (not lit_probs) if sid.startswith("cbp_") else False})
        samples.append({"series": sid, "geo": g, "geo_kind": k, "stratum": stratum, "class": slug, "round": rnd,
                        "register": cell, "rederived": rederived, "match": not probs, "match_literal_2_digit_reading": not lit_probs})
    n = len(samples)
    matches = sum(1 for x in samples if x["match"])
    r2 = [x for x in samples if x["round"] == 2]
    r2_matches = sum(1 for x in r2 if x["match"])

    # quotas ---------------------------------------------------------------------------------------------
    ct_markets = [s for s in samples if s["geo_kind"] == "ct-market"]
    ct_county = [s for s in samples if s["geo_kind"] == "ct-county-equivalent" or s["geo"] == "ct"]
    def n_member_counties(g):
        m = G.markets.get(g)
        if m is None:
            return 0
        if m["composition_source"] == "cbsa-delineation":
            return len(members.get(m["resolved"]["cbsa"], []))
        a = market_areas(m)
        return len(a) if a else 0

    multi = [s for s in samples if s["geo"] in G.markets and n_member_counties(s["geo"]) >= 2 and s["geo_kind"] != "market-place"]
    sub = [s for s in samples if s["geo_kind"] == "market-place"]
    cross = [s for s in samples if s["geo_kind"] in ("market-cross-state", "market-cbsa-cross-state")]
    ct_pc = [s for s in samples if s["geo_kind"] == "ct-market" and s["series"].startswith(("pep_", "cbp_"))]
    multi_pc = [s for s in multi if s["series"].startswith(("pep_", "cbp_"))]
    cross_pc = [s for s in cross if s["series"].startswith(("pep_", "cbp_"))]
    medians = [s for s in samples if "median" in s["series"]]
    med_multi_null = [s for s in medians if s["geo_kind"] in ("market-multi-county", "market-place", "market-cross-state")
                      and isinstance(s["register"], dict) and s["register"].get("v") is None and "components" in s["register"]]

    # ------------------------------------------------------------------------------------------------------
    # state sums: ACS 5-year households (and population, occupied units, 1-year households) vs the counties
    # ------------------------------------------------------------------------------------------------------
    state_sums = {"acs5_households": {}, "acs5_pop": {}, "acs5_occupied_units": {}}
    st_bad = []
    for vname, var in (("acs5_households", "B11001_001"), ("acs5_pop", "B01003_001"), ("acs5_occupied_units", "B25003_001")):
        for sid_, fips in sorted(G.fips_of.items()):
            srow = acs5["state"].get(fips)
            s_e = est(srow, var)[0] if srow else None
            tot = 0
            n_co = 0
            for cg, row in acs5["county"].items():
                if cg[:2] == fips:
                    e = est(row, var)[0]
                    if e is None:
                        tot = None
                        break
                    tot += e
                    n_co += 1
            ok = (s_e is not None and tot is not None and s_e == tot)
            # the register's own state value vs the register's own county sum, too
            rv = reg[vname]["values"].get(sid_, {}).get("all", {})
            rv = rv.get("v") if isinstance(rv, dict) else rv
            rsum = 0
            rn = 0
            for g, c in reg[vname]["values"].items():
                if g.startswith("co-" + fips):
                    cv = c["all"].get("v") if isinstance(c["all"], dict) else c["all"]
                    if cv is None:
                        rsum = None
                        break
                    rsum += cv
                    rn += 1
            state_sums[vname][sid_] = {"state_raw": s_e, "sum_of_counties_raw": tot, "counties": n_co, "equal": ok,
                                       "register_state": rv, "register_sum_of_counties": rsum,
                                       "register_equal": (rv is not None and rsum is not None and rv == rsum)}
            if not ok or not state_sums[vname][sid_]["register_equal"]:
                st_bad.append((vname, sid_))
    # PEP Vintage 2023 July 1, 2023 population: state vs sum of its counties (raw, then the register's own rows)
    state_sums["pep_pop_2023"] = {}
    for sid_, fips in sorted(G.fips_of.items()):
        s_p = pep_rows["state"].get(fips, {}).get(2023)
        cs = [pep_rows["county"][c].get(2023) for c in pep_rows["county"] if c[:2] == fips]
        tot = sum(cs) if cs and None not in cs else None
        rv = reg["pep_pop_2023"]["values"].get(sid_, {}).get("all")
        rsum = 0
        for g, c in reg["pep_pop_2023"]["values"].items():
            if g.startswith("co-" + fips):
                rsum += c["all"]
        state_sums["pep_pop_2023"][sid_] = {"state_raw": s_p, "sum_of_counties_raw": tot, "counties": len(cs), "equal": s_p == tot and tot is not None,
                                            "register_state": rv, "register_sum_of_counties": rsum, "register_equal": rv == rsum}
        if not state_sums["pep_pop_2023"][sid_]["equal"] or rv != rsum:
            st_bad.append(("pep_pop_2023", sid_))
    n_states = len(G.fips_of)
    ss_summary = dict((v, "%d/%d states equal (raw), %d/%d (register)" % (
        sum(1 for x in d.values() if x["equal"]), len(d), sum(1 for x in d.values() if x["register_equal"]), len(d)))
        for v, d in state_sums.items())
    state_sums["summary"] = ss_summary
    state_sums["unequal"] = ["%s/%s" % x for x in st_bad]

    # BEA: state vs sum of counties (informational; BEA publishes combination areas)
    bea_state = {}
    for vname, line in (("bea_personal_income", 1), ("bea_population", 2)):
        diffs = []
        for sid_, fips in sorted(G.fips_of.items()):
            sv = DB.line("state", line, fips + "000")
            if sv is None:
                continue
            tot = 0
            for c in counties:
                if c[:2] == fips:
                    x = DB.line("county", line, c)
                    if x is not None:
                        tot += x
            if tot != sv:
                diffs.append("%s: state %s vs counties %s (diff %s)" % (sid_, sv, tot, sv - tot))
        bea_state[vname] = diffs
    state_sums["bea_state_vs_counties"] = bea_state

    # ------------------------------------------------------------------------------------------------------
    # sentinels
    # ------------------------------------------------------------------------------------------------------
    found = []
    for sid in sids_all:
        loc = []
        for g, v in reg[sid]["values"].items():
            scan_sentinels(v, [g], loc)
        for p in loc:
            found.append({"series": sid, "path": p})
    sentinels_found = {"count": len(found), "values_scanned_in": len(sids_all),
                       "sentinels": list(SENTINELS), "found": found[:50]}
    # raw side: sentinels turned into nulls
    raw_sent = {}
    for vint, T in (("acs5", acs5), ("acs1", acs1)):
        c = Counter()
        for lv, rows in T.items():
            for gid, r in rows.items():
                for h, x in r.items():
                    if h != "NAME" and x in SENT:
                        c[("E" if h.endswith("E") else "M", x)] += 1
        raw_sent[vint] = dict(("%s:%s" % k, v) for k, v in sorted(c.items()))
    # E sentinel -> register null: for every single-area cell whose raw E is a sentinel
    e_sent_checked = e_sent_ok = 0
    for sid in sids_acs5 + sids_acs1:
        name = sid[5:]
        if ACS_SPEC[name][0] in ("add", "median", "pci"):
            for g in sorted(reg[sid]["values"]):
                exp = derive_any(sid, g)
                if exp["status"] == "null":
                    e_sent_checked += 1
                    cell = reg[sid]["values"][g]["all"]
                    if isinstance(cell, dict) and cell.get("v") is None:
                        e_sent_ok += 1

    # ------------------------------------------------------------------------------------------------------
    # BEA: no CBSA id carries a state row; a cbsa market is the sum of its member counties
    # ------------------------------------------------------------------------------------------------------
    bea_state_geofips = set(r_["GeoFips"] for r_ in (bea.get(("state", 1)) or {}).values())
    collide = sorted(c for c in cbsas if c in bea_state_geofips)
    bea_chk = {}
    for sid in sids_bea:
        vals = reg[sid]["values"]
        cb_ids = sorted(g for g in vals if g.startswith("cbsa-"))
        state_like = []
        for g in cb_ids:
            for fips in G.fips_of.values():
                if vals[g]["all"] == vals.get(G.postal_of_fips[fips], {}).get("all"):
                    state_like.append(g)
        n_mk = n_ok = 0
        for g, m in G.markets.items():
            if m["composition_source"] == "cbsa-delineation" and g in vals:
                n_mk += 1
                mem = members.get(m["resolved"]["cbsa"], [])
                exp = DB.derive(sid, g)
                if exp["status"] == "value" and not compare_bea(sid, exp, vals[g]["all"]) and len(mem) >= 1:
                    n_ok += 1
        bea_chk[sid] = {"cbsa_ids_in_series": len(cb_ids), "cbsa_ids_equal_to_a_state_row": len(state_like),
                        "cbsa_markets_valued": n_mk, "cbsa_markets_equal_to_member_county_sum": n_ok}

    # CBP: the unit of up_to in cbp_emp (establishments withheld, or employees?)
    emp_unit = Counter()
    for g, cl in reg["cbp_emp"]["values"].items():
        status, why, tab = DC.classes_of(g)
        if status != "value":
            continue
        for slug, cell in cl.items():
            if isinstance(cell, list) and slug in tab:
                le, lm, ue, um = tab[slug]
                emp_unit[("estab_gap" if cell[1] == ue else "other") + ("/=emp_gap" if cell[1] == um else "/!=emp_gap")] += 1

    # ------------------------------------------------------------------------------------------------------
    # notes
    # ------------------------------------------------------------------------------------------------------
    notes.insert(0, "SCOPE (second round, 16 Oct 2026): covered are the 14 acs5_* (fairfield-county included), 14 acs1_*, 3 bea_*, 7 pep_* (Vintage 2023, "
                    "Census Data API) and 3 cbp_* (CBP 2023, Census Data API, NAICS 2017) series. NOT covered: the permit series (removed from the register). "
                    "Nothing under _cache/markets/held/ and none of the pipeline scripts were opened. The PEP check of round one (Vintage 2025 files) is "
                    "replaced by the Vintage 2023 API pull.")
    notes.insert(1, "Method: every expected cell is derived from the raw files by code in this script (ACS Data API JSON by level, geoinfo CBSA member "
                    "lists, BEA CAINC1 full rows keyed by file level, PEP V2023 July 1 rows, CBP all-industry rows with the 2- to 6-digit parent codes, "
                    "the 2020 Census Connecticut county subdivisions) and the market rules of D39/D40; compositions come from geographies.json "
                    "markets[].composition_source and resolved{counties, places, cousubs, cbsa, ct_planning_regions, ct_legacy_counties}; CBP classes "
                    "from naics-map.json legacy['2017'] (%s fall back to naics2022). Tolerances: counts exact, dollars within 0.5, shares within 1e-6, "
                    "CBP per-10,000 within 0.006 (lower bound) with up_to exact, MOE within 0.0101 (the register rounds to 2 decimals)." % (fallback or "no class"))
    notes.insert(2, "CENSUS (every value of every covered series, %s compared): %d with problems. Per series: %s." % (
        format(n_cmp, ","), n_bad, ", ".join("%s %d/%d" % (k, v[0] - v[1], v[0]) for k, v in sorted(census.items()))))
    notes.append("Sample design: seed %d, random.Random(seed).random() only; per series up to 1 us, 1 state, 2 county, 1 Connecticut planning-region county, 2 CBSA, "
                 "1 cross-state CBSA, 2 cbsa-delineation market, 1 cross-state cbsa market, 2 multi-county market, 1 single-county market, 1 place market, "
                 "1 Connecticut planning-region market, 1 kind cross-state market; BEA's CBSA pool (2 ids) is taken whole; plus 2 extra multi-area or place "
                 "markets for each median series." % SEED)
    notes.append("Quota basis: ct counts Connecticut planning-region MARKETS (county-equivalent rows co-091xx, %d, are listed separately); multi_county counts "
                 "markets of two or more counties or planning regions (county-set, cross-state and multi-county cbsa-delineation markets); sub_county counts "
                 "place or town markets (ACS only; FOIA has no sub-county grain); cross_state counts kind cross-state markets and cbsa markets whose CBSA spans states; "
                 "medians counts the median series' sampled cells, of which %d are null multi-area cells carrying their components." % (
                     len(ct_county), len(med_multi_null)))
    cov_bad = dict((k, v) for k, v in coverage.items() if v["missing"] or v["extra"])
    if cov_bad:
        notes.append("COVERAGE differences (expected from the raw files vs keys in the register): " + json.dumps(
            dict((k, {"expected": v["expected"], "register": v["register"], "missing": v["missing"][:12], "n_missing": len(v["missing"]),
                      "extra": v["extra"][:12], "n_extra": len(v["extra"])}) for k, v in cov_bad.items()))[:6000])
    else:
        notes.append("COVERAGE: every geography the raw files can value is in the register or listed as null, and the register holds no other id.")
    notes.append("Raw sentinels in the files (all turned to nulls in the register or to a missing MOE): %s. Register values equal to a sentinel: %d." % (
        json.dumps(raw_sent), len(found)))
    notes.append("E-sentinel / null estimates: %d single-area or set cells derive to null from the raw files; the register has v null in %d of them." % (e_sent_checked, e_sent_ok))
    notes.append("State sums: %s. Unequal: %s." % (json.dumps(ss_summary), state_sums["unequal"] or "none"))
    notes.append("BEA state row vs sum of its counties (information only): %s" % json.dumps(bea_state))
    if census_detail:
        notes.append("First census problems that the sector rule does not explain (up to 12; %d problems in all, the explained ones are in census.problems): %s" % (
            n_bad, json.dumps([d_ for d_ in census_detail if not d_.get("explained_by_sector_range_rule")][:12])[:9000]))
    notes.append("ROUND 2 (PEP, CBP, fairfield-county ACS 5-year): %d sampled values, %d match, %d mismatch. Quotas over this round alone: Connecticut "
                 "planning-region markets in PEP and CBP %d, multi-county PEP and CBP samples %d, cross-state PEP and CBP samples %d." % (
                     len(r2), r2_matches, len(r2) - r2_matches, len(ct_pc), len(multi_pc), len(cross_pc)))
    notes.append("BEA (round 2, item 1): %s. State/region GeoFips that equal a CBSA code (the collision found in round one): %s. BEA rows are keyed by file level "
                 "(state, county; the MSA files are API errors, so no MSA row exists); a cbsa market's BEA figure must equal the sum of its member counties." % (
                     json.dumps(bea_chk), collide))
    notes.append("CBP lower bounds: %d negative parent gaps (parent below the sum of its published 6-digit children) were clamped to 0. In cbp_emp the second "
                 "element of a [value, up_to] cell is the number of establishments that may be withheld, the same as in cbp_estab (not employees): register up_to "
                 "versus my establishment gap / employee gap: %s. The value is a lower bound on paid employees; up_to does not bound employees." % (DC.negative_gaps, json.dumps(dict(emp_unit))))
    expl = sum(v for (sid_, k_), v in sector_explained.items() if k_.startswith("explained"))
    unexpl = sum(v for (sid_, k_), v in sector_explained.items() if k_ == "NOT explained")
    tgt_note = dict((k, v) for k, v in targeted.items() if v)
    n_sample_sector = sum(1 for x in samples if not x["match"] and x["match_literal_2_digit_reading"])
    notes.append("CBP SECTOR-RANGE FINDING. The API publishes the 2-digit level of NAICS 31-33, 44-45 and 48-49 only as the ranges '31-33', '44-45', '48-49'. "
                 "Primary reading (used for the headline numbers): that range IS the 2-digit parent of its codes, so a class code absent at a geography whose "
                 "nearest published parent is the sector range gets that sector's gap (sector establishments less its published 6-digit children) in up_to. "
                 "The register looks for the two-digit string itself ('44', '48'...), which is never published, so it skips the sector range: a class in those "
                 "sectors with no 3-, 4- or 5-digit parent published at a geography is left out as zero with nothing withheld (or carries a smaller up_to), although "
                 "up to the sector gap may be hidden. Effect on the census: %d class cells differ from the primary reading (%s), every one explained by this single "
                 "rule (re-deriving with the literal two-digit lookup reproduces the register cell exactly); %d further problems are not explained by it (the Puerto "
                 "Rico CBSA entries of the next note). Geographies affected by the sector rule: %s. %d of the %d sampled values differ from the primary reading "
                 "because of this rule. Lower-bound values (the sum of published 6-digit cells) agree in every case; only up_to and the presence of an "
                 "otherwise-absent class differ. County sets agree with the sum of their counties' cells (value and up_to) under either reading." % (
                     expl, ", ".join("%s %d" % (k, sum(v for (a_, b_), v in sector_explained.items() if a_ == k and b_.startswith("explained"))) for k in sids_cbp),
                     unexpl, dict((k, len(v)) for k, v in sorted(sector_geos.items())), n_sample_sector, len(samples)))
    notes.append("REGISTER IDS WITHOUT RAW DATA (not caused by the sector rule): %s. The CBP API returned no CBSA row for the ten Puerto Rico metropolitan "
                 "areas (925 of 935 CBSAs are in cbsa_all.json), yet the CBP series hold an empty class dictionary for each (read as zero establishments in "
                 "every class; their PEP population is positive, e.g. cbsa-41980 %s). The Puerto Rico counties do have CBP rows (county_72.json). A county "
                 "that has no rows in its state's file (15005, 48269) is read as zero establishments, which is how CBP lists a county with none." % (
                     json.dumps(dict((k, v) for k, v in tgt_note.items())), reg["pep_pop_2023"]["values"].get("cbsa-41980")))
    notes.append("Absent-means-zero: a class absent from a geography that is in the register's values is checked against the raw files as zero establishments "
                 "with nothing withheld; every class of every valued geography (43 per geography and series) is compared in the census.")
    notes.append("fairfield-county ACS 5-year: towns = 2020 county subdivisions of legacy county 09001 matched by five-digit town code to the 2025 ACS cousub rows; "
                 "the placeholder 'County subdivisions not defined' (00000, population 0) is not a town and is dropped; its ACS 1-year cells are null because the "
                 "1-year files carry no county subdivisions. fairfield PEP and CBP are null (the files cover planning regions), fairfield BEA is null "
                 "(legacy county 09001 is (NA) in the BEA row).")

    result = {
        "seed": SEED,
        "n": n,
        "matches": matches,
        "mismatches": n - matches,
        "by_kind": dict((k, "%d/%d" % (v[0], v[1])) for k, v in sorted(by_kind.items())),
        "quota": {
            "ct": {"need": 5, "have": len(ct_markets), "ct_county_equivalent_samples": len(ct_county), "of_which_pep_cbp": len(ct_pc)},
            "multi_county": {"need": 5, "have": len(multi), "of_which_pep_cbp": len(multi_pc)},
            "sub_county": {"need": 3, "have": len(sub)},
            "cross_state": {"need": 3, "have": len(cross), "of_which_pep_cbp": len(cross_pc)},
            "medians": {"need": 8, "have": len(medians), "null_multi_area_with_components": len(med_multi_null)},
        },
        "mismatch_detail": mismatch_detail,
        "samples": samples,
        "state_sums": state_sums,
        "sentinels_found": sentinels_found,
        "rounds": {"round_1_acs_bea": {"n": n - len(r2), "matches": matches - r2_matches},
                   "round_2_pep_cbp_fairfield": {"n": len(r2), "matches": r2_matches, "mismatches": len(r2) - r2_matches}},
        "census": {"compared": n_cmp, "with_problems": n_bad, "by_series": dict((k, "%d/%d" % (v[0] - v[1], v[0])) for k, v in sorted(census.items())),
                   "problems": [d_ for d_ in census_detail if not d_.get("explained_by_sector_range_rule")][:300]
                   + [d_ for d_ in census_detail if d_.get("explained_by_sector_range_rule")][:20]},
        "notes": notes,
    }
    with open(OUT, "w") as fh:
        json.dump(result, fh, indent=1, default=str)
        fh.write("\n")
    log("wrote %s" % OUT)
    print(json.dumps({"seed": SEED, "n": n, "matches": matches, "mismatches": n - matches,
                      "quota": dict((k, v["have"]) for k, v in result["quota"].items()),
                      "census": [n_cmp, n_bad], "by_kind": result["by_kind"]}))


if __name__ == "__main__":
    main()
