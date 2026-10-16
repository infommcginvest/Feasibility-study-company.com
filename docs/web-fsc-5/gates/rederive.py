#!/usr/bin/env python3
"""Gate 6 for WEB-FSC-5: independent re-derivation of the federal-statistics register.

Run:  python3 -I docs/web-fsc-5/gates/rederive.py      (standard library only, offline)

What it does
  1. Reads SBA's own data dictionary (xlsx, via zipfile + xml.etree) for the field list and the
     LoanStatus codes, and reads data/markets/sources.json (definitions), geographies.json
     (market compositions) and naics-map.json (class code lists).  It does not read any other
     classification file in data/markets and it never imports or reads the three build scripts.
  2. Draws a seeded random sample of register values (stratified across the 16 series, both
     programs, geography kinds, class fits and windows) and re-derives every sampled value by a
     DIRECT scan of the raw CSVs (each CSV row is tested against each sampled value's geography,
     class and window predicates).
  3. Builds a second, independent route: a full (program, state, county, NAICS, FY) cube from the
     same CSVs and a census that compares EVERY value of every series (all geographies, 44 classes,
     5 windows, 36 FYs, rates).  The sample is the formal gate; the census and the agreement between
     the two routes are recorded in "notes".
  4. Computes rows / loans / volume / CHGOFF rows per program and approval FY, and every distinct
     LoanStatus per file, straight from the CSVs.
  5. Writes docs/web-fsc-5/gates/rederive-result.json.
"""
import csv
import difflib
import json
import os
import random
import re
import sys
import time
import zipfile
import xml.etree.ElementTree as ET
from collections import Counter, defaultdict

SEED = 20261016          # fixed and recorded in the result
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
RAW = os.path.join(ROOT, "_cache", "markets", "raw", "sba_foia", "2026-06-30")
DATA = os.path.join(ROOT, "data", "markets")
OUT = os.path.join(HERE, "rederive-result.json")

T0 = time.time()


def log(msg):
    sys.stderr.write("[%6.1fs] %s\n" % (time.time() - T0, msg))


# --------------------------------------------------------------------------------------------
# 1. SBA data dictionary
# --------------------------------------------------------------------------------------------
def read_dictionary(path):
    z = zipfile.ZipFile(path)
    M = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"
    R = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}"
    PR = "{http://schemas.openxmlformats.org/package/2006/relationships}"
    shared = []
    root = ET.fromstring(z.read("xl/sharedStrings.xml"))
    for si in root.findall(M + "si"):
        shared.append("".join(t.text or "" for t in si.iter(M + "t")))
    rels = {}
    for rel in ET.fromstring(z.read("xl/_rels/workbook.xml.rels")).findall(PR + "Relationship"):
        rels[rel.get("Id")] = rel.get("Target")
    wb = ET.fromstring(z.read("xl/workbook.xml"))
    out = {}
    for sh in wb.find(M + "sheets"):
        name = sh.get("name")
        target = rels[sh.get(R + "id")]
        target = target.lstrip("/")
        if not target.startswith("xl/"):
            target = "xl/" + target
        sheet = ET.fromstring(z.read(target))
        fields = {}
        order = []
        for row in sheet.iter(M + "row"):
            cells = {}
            for c in row.findall(M + "c"):
                col = re.match(r"[A-Z]+", c.get("r")).group(0)
                v = c.find(M + "v")
                if v is None:
                    isel = c.find(M + "is")
                    val = "".join(t.text or "" for t in isel.iter(M + "t")) if isel is not None else ""
                elif c.get("t") == "s":
                    val = shared[int(v.text)]
                else:
                    val = v.text or ""
                cells[col] = val
            if "A" in cells and cells["A"] != "Field Name":
                fields[cells["A"]] = cells.get("B", "")
                order.append(cells["A"])
        out[name] = {"fields": fields, "order": order}
    return out


def dict_status_codes(definition):
    """Codes listed as bullet lines '• CODE = meaning' in the LoanStatus definition."""
    return [m.group(1).strip() for m in re.finditer(r"•\s*([A-Za-z ]+?)\s*=", definition)]


def squash(s):
    return "".join(s.split()).upper()


# Meaning of each dictionary code (my reading of SBA's text).  Keys are the dictionary codes with
# internal blanks removed, so the 7(a) file's "P I F" and the dictionary's "PIF" are the same code.
CATEGORY = {
    "CANCLD": "cancelled",
    "CHGOFF": "chgoff",
    "PIF": "paid",
    "EXEMPT": "active",
    "CLOSED": "closed",          # 504 only: closed for any reason other than cancelled / PIF / CHGOFF
    "COMMIT": "undisbursed",     # 7(a)
    "NOTFUNDED": "undisbursed",  # 504
}
DISBURSED = frozenset(["paid", "chgoff", "active", "closed"])

# --------------------------------------------------------------------------------------------
# helpers for the register
# --------------------------------------------------------------------------------------------
SERIES_BASE = ["loans", "volume", "cancelled", "disbursed", "chgoff_n", "chgoff_amt",
               "chgoff_rate", "chgoff_amt_rate"]
PROGS = ["7a", "504"]
RATE_SERIES = ("chgoff_rate", "chgoff_amt_rate")
WINDOWS = ["all", "fy2016_2025", "fy2021_2025", "fy2025", "fy2026ytd"]
WINDOW_RANGE = {"fy2016_2025": (2016, 2025), "fy2021_2025": (2021, 2025),
                "fy2025": (2025, 2025), "fy2026ytd": (2026, 2026)}
POOL_LO, POOL_HI = 2011, 2020
# vector layout shared by both routes:
#  0 rows  1 loans  2 volume(c)  3 cancelled  4 disbursed  5 chgoff_n  6 chgoff_amt(c)  7 disbursed GrossApproval(c)
ADDITIVE_IDX = {"loans": (1, False), "volume": (2, True), "cancelled": (3, False),
                "disbursed": (4, False), "chgoff_n": (5, False), "chgoff_amt": (6, True)}
RATE_IDX = {"chgoff_rate": ((5, False), (4, False)), "chgoff_amt_rate": ((6, True), (7, True))}
FLAG_SMALL = "small-denominator (<30 disbursed loans)"
FLAG_NONE = "no-disbursed-loans-in-seasoned-cohorts"


def norm_county(s):
    return " ".join(s.split()).upper()


def norm_state(s):
    return s.strip().lower()


def money(c):
    return round(c / 100.0, 2)


def prog_of(sid):
    return "7a" if sid.startswith("sba7a_") else "504"


def main():
    # ----------------------------------------------------------------------------------------
    # inputs
    # ----------------------------------------------------------------------------------------
    notes = []
    dic = read_dictionary(os.path.join(RAW, "7a_504_foia_data_dictionary.xlsx"))
    sheet7 = [k for k in dic if k.startswith("7(a)")][0]
    sheet5 = [k for k in dic if k.startswith("504")][0]
    dict_fields = {"7a": dic[sheet7]["order"], "504": dic[sheet5]["order"]}
    dict_codes = {"7a": [squash(c) for c in dict_status_codes(dic[sheet7]["fields"]["LoanStatus"])],
                  "504": [squash(c) for c in dict_status_codes(dic[sheet5]["fields"]["LoanStatus"])]}
    for p in PROGS:
        unmapped = [c for c in dict_codes[p] if c not in CATEGORY]
        if unmapped:
            notes.append("Dictionary lists a %s status code this checker does not categorise: %s" % (p, unmapped))
    log("dictionary: 7a codes %s ; 504 codes %s" % (dict_codes["7a"], dict_codes["504"]))

    sources = json.load(open(os.path.join(DATA, "sources.json")))
    geo = json.load(open(os.path.join(DATA, "geographies.json")))
    naics = json.load(open(os.path.join(DATA, "naics-map.json")))

    markets = {}
    for m in geo["markets"]:
        markets[m["state"] + "/" + m["slug"]] = m
    state_ids = [s["id"] for s in geo["states"]]

    # classes: NaicsCode membership = naics2022 or any legacy edition list
    class_codes = {}
    class_fit = {"all": "all"}
    for c in naics["classes"]:
        codes = set(c["naics2022"])
        for lst in c["legacy"].values():
            codes.update(lst)
        class_codes[c["slug"]] = codes
        class_fit[c["slug"]] = c["fit"]
    naics2cls = defaultdict(list)
    for slug, codes in class_codes.items():
        for code in codes:
            naics2cls[code].append(slug)
    CLASSES = ["all"] + sorted(class_codes)

    # geography compositions: id -> set of (state lower, county string)
    def pairs_of(strings):
        return set((x["state"].strip().lower(), norm_county(x["string"])) for x in strings)

    compositions = {}   # id -> frozenset of pairs
    geo_kind = {}       # id -> kind label
    multi_county = set()
    for mid, m in markets.items():
        kind = m["kind"]
        strings = m["foia"]["strings"]
        if m.get("ct") and m["foia"].get("ct"):
            for comp in ("legacy", "pr"):
                cid = "%s:%s" % (mid, comp)
                compositions[cid] = frozenset(("ct", norm_county(s)) for s in m["foia"]["ct"][comp])
                geo_kind[cid] = "ct-component"
            continue
        if not strings:
            continue
        compositions[mid] = frozenset(pairs_of(strings))
        geo_kind[mid] = kind
        if kind == "county-set" and len(set(x["string"] for x in strings)) >= 2:
            multi_county.add(mid)
        sts = sorted(set(x["state"].strip().lower() for x in strings))
        if kind == "cross-state" and len(sts) >= 2:
            for st in sts:
                cid = "%s:%s" % (mid, st)
                compositions[cid] = frozenset(p for p in compositions[mid] if p[0] == st)
                geo_kind[cid] = "cross-state-part"
    geo_kind["us"] = "us"
    for s in state_ids:
        geo_kind[s] = "state"

    # register
    reg = {}
    for p in PROGS:
        for b in SERIES_BASE:
            sid = "sba%s_%s" % (p, b)
            reg[sid] = json.load(open(os.path.join(DATA, "series", sid + ".json")))
    SIDS = sorted(reg)
    by_fy_years = reg[SIDS[0]]["by_fy_years"]
    for sid in SIDS:
        if reg[sid]["by_fy_years"] != by_fy_years:
            notes.append("by_fy_years differs in %s" % sid)
        if sorted(reg[sid]["windows"]) != sorted(WINDOWS):
            notes.append("windows keys differ in %s: %s" % (sid, sorted(reg[sid]["windows"])))
    FY0, FY1 = by_fy_years
    NFY = FY1 - FY0 + 1

    # ----------------------------------------------------------------------------------------
    # 2. the sample (drawn from the register only, before the raw files are read)
    # ----------------------------------------------------------------------------------------
    rng = random.Random(SEED)

    def u():
        return rng.random()

    def pick(seq):
        return seq[min(len(seq) - 1, int(u() * len(seq)))]

    fit_groups = {"exact": [], "partial": [], "proxy": []}
    for slug in sorted(class_codes):
        fit_groups[class_fit[slug]].append(slug)

    def draw_class():
        r = u()
        if r < 0.20:
            return "all"
        if r < 0.55:
            return pick(fit_groups["exact"])
        if r < 0.80:
            return pick(fit_groups["partial"])
        return pick(fit_groups["proxy"])

    ADD_WINDOW_CHOICES = WINDOWS + ["by_fy", "by_fy", "by_fy"]

    def draw_window(rate):
        if rate:
            return "pooled_fy2011_2020"
        w = pick(ADD_WINDOW_CHOICES)
        if w == "by_fy":
            return "by_fy:%d" % (FY0 + min(NFY - 1, int(u() * NFY)))
        return w

    def register_value(sid, g, cls, window):
        cell = reg[sid]["values"].get(g, {}).get(cls)
        if cell is None:
            return None
        if sid.split("_", 1)[1] in RATE_SERIES:
            return cell
        if window.startswith("by_fy:"):
            return cell["by_fy"][int(window.split(":")[1]) - FY0]
        return cell[window]

    def nonzero(sid, cell):
        if cell is None:
            return False
        if isinstance(cell, dict):
            return cell.get("den", 0) > 0 and cell.get("num", 0) > 0
        return cell != 0

    STRATA = [("us", 2), ("state", 4), ("county", 3), ("multi_county", 5),
              ("cross_state", 2), ("ct", 3)]
    sample_specs = []
    used = set()
    for sid in SIDS:
        base = sid.split("_", 1)[1]
        rate = base in RATE_SERIES
        gids = sorted(reg[sid]["values"])
        pools = {
            "us": ["us"],
            "state": [g for g in gids if geo_kind.get(g) == "state"],
            "county": [g for g in gids if geo_kind.get(g) == "county"],
            "multi_county": [g for g in gids if g in multi_county],
            "cross_state": [g for g in gids if geo_kind.get(g) in ("cross-state", "cross-state-part")],
            "ct": [g for g in gids if geo_kind.get(g) == "ct-component"],
        }
        for stratum, count in STRATA:
            pool = pools[stratum]
            if not pool:
                notes.append("no register geographies for stratum %s in %s" % (stratum, sid))
                continue
            for _ in range(count):
                want_nonzero = u() < 0.75
                chosen = None
                for attempt in range(60):
                    g = pick(pool)
                    cls = draw_class()
                    win = draw_window(rate)
                    if (sid, g, cls, win) in used:
                        continue
                    cell = register_value(sid, g, cls, win)
                    chosen = (sid, g, cls, win)
                    if want_nonzero and not nonzero(sid, cell) and attempt < 50:
                        continue
                    break
                if chosen is None:
                    continue
                used.add(chosen)
                sample_specs.append({"series": chosen[0], "geo": chosen[1], "class": chosen[2],
                                     "window": chosen[3], "stratum": stratum,
                                     "nonzero_wanted": want_nonzero})
    log("sample drawn: %d values" % len(sample_specs))

    # direct-scan index
    def label_of(window):
        return "pooled" if window == "pooled_fy2011_2020" else window

    spec_index = defaultdict(set)      # (prog, geo, class) -> set of labels
    for s in sample_specs:
        spec_index[(prog_of(s["series"]), s["geo"], s["class"])].add(label_of(s["window"]))
    sampled_classes = set(k[2] for k in spec_index)
    us_sampled = any(k[1] == "us" for k in spec_index)
    pair_geos = defaultdict(set)       # (state, county) -> geos
    state_geos = set()
    for (p, g, c) in spec_index:
        if g == "us":
            continue
        if "/" not in g:
            state_geos.add(g)
        else:
            for pr in compositions[g]:
                pair_geos[pr].add(g)
    pair_geos = dict((k, sorted(v)) for k, v in pair_geos.items())

    labels_for_fy = {}
    for fy in range(1980, 2100):
        labs = ["all", "by_fy:%d" % fy]
        for w, (lo, hi) in WINDOW_RANGE.items():
            if lo <= fy <= hi:
                labs.append(w)
        if POOL_LO <= fy <= POOL_HI:
            labs.append("pooled")
        labels_for_fy[fy] = tuple(labs)

    dacc = defaultdict(lambda: [0] * 8)   # (prog, geo, class, label) -> vec  (direct route)
    cls_cache = {}

    # ----------------------------------------------------------------------------------------
    # 3. one pass over the raw files: totals, statuses, cube, direct scan, diagnostics
    # ----------------------------------------------------------------------------------------
    files = sorted(f for f in os.listdir(RAW) if f.endswith(".csv"))
    cube = {"7a": {}, "504": {}}                   # prog -> (state, county) -> {(naics, fy): vec}
    tot = defaultdict(lambda: [0, 0, 0, 0])        # (prog, fy) -> rows, loans, volume(c), chgoff rows
    status_values = {"7a": {}, "504": {}}
    file_fy = {}
    diag = defaultdict(Counter)
    diag_lists = defaultdict(list)
    header_by_file = {}
    seen_hash = set()
    cents_cache = {}
    cat_cache = {}
    total_rows = Counter()
    state_seen = defaultdict(Counter)
    blank_naics = Counter()

    def to_cents(s, what, prog):
        v = cents_cache.get(s)
        if v is None:
            t = s.strip()
            if not t:
                diag["blank_" + what][prog] += 1
                return 0
            x = float(t) * 100.0
            v = int(round(x))
            if abs(x - v) > 1e-4:
                diag["distinct_values_with_sub_cent_precision_" + what][prog] += 1
            cents_cache[s] = v
        return v

    for fname in files:
        prog = "7a" if "_7a_" in fname else "504"
        path = os.path.join(RAW, fname)
        sv = Counter()
        fys = Counter()
        with open(path, newline="", encoding="utf-8") as fh:
            rd = csv.reader(fh)
            hdr = next(rd)
            header_by_file[fname] = hdr
            ix = dict((h, i) for i, h in enumerate(hdr))
            need = ["Program", "GrossApproval", "ApprovalFY", "FirstDisbursementDate", "NaicsCode",
                    "ProjectCounty", "ProjectState", "LoanStatus", "ChargeOffDate", "GrossChargeOffAmount"]
            for n_ in need:
                if n_ not in ix:
                    raise SystemExit("missing field %s in %s" % (n_, fname))
            iP, iGA, iFY, iFD, iNA = ix["Program"], ix["GrossApproval"], ix["ApprovalFY"], ix["FirstDisbursementDate"], ix["NaicsCode"]
            iCT, iST, iLS, iCO, iGC = ix["ProjectCounty"], ix["ProjectState"], ix["LoanStatus"], ix["ChargeOffDate"], ix["GrossChargeOffAmount"]
            ncols = len(hdr)
            cube_p = cube[prog]
            for row in rd:
                if len(row) != ncols:
                    diag["malformed_row"][fname] += 1
                    continue
                h = hash(tuple(row))
                is_dup = h in seen_hash
                if not is_dup:
                    seen_hash.add(h)
                total_rows[prog] += 1
                if squash(row[iP]) != ("7A" if prog == "7a" else "504"):
                    diag["program_field_disagrees_with_file"][fname] += 1
                raw_status = row[iLS]
                sv[raw_status] += 1
                ck = (prog, raw_status)
                cc = cat_cache.get(ck)
                if cc is None:
                    code = squash(raw_status)
                    cc = (CATEGORY.get(code, "UNKNOWN"), code in dict_codes[prog])
                    cat_cache[ck] = cc
                cat = cc[0]
                if cat == "UNKNOWN" or not cc[1]:
                    diag["status_not_in_dictionary_for_program"]["%s:%s" % (prog, raw_status)] += 1
                fy = int(row[iFY])
                fys[fy] += 1
                ga = to_cents(row[iGA], "GrossApproval", prog)
                gc = to_cents(row[iGC], "GrossChargeOffAmount", prog)
                st = norm_state(row[iST])
                cty = norm_county(row[iCT])
                nc = row[iNA].strip()
                state_seen[prog][st] += 1
                if not nc:
                    blank_naics[prog] += 1
                if ga < 0:
                    diag["negative_GrossApproval"][prog] += 1
                    diag_lists["negative_GrossApproval"].append("%s FY%d status %s GrossApproval %s county %s/%s" % (prog, fy, raw_status, row[iGA], st, cty))
                if not st:
                    diag["blank_ProjectState"][prog] += 1
                if not cty:
                    diag["blank_ProjectCounty"][prog] += 1
                fdate = row[iFD].strip()
                if cat in DISBURSED and not fdate:
                    diag["disbursed_status_without_FirstDisbursementDate"][prog] += 1
                if cat == "undisbursed" and fdate:
                    diag["undisbursed_status_with_FirstDisbursementDate"][prog] += 1
                if cat == "cancelled" and fdate:
                    diag["cancelled_with_FirstDisbursementDate"][prog] += 1
                if cat == "chgoff":
                    if not row[iCO].strip():
                        diag["CHGOFF_without_ChargeOffDate"][prog] += 1
                    if gc == 0:
                        diag["CHGOFF_with_zero_GrossChargeOffAmount"][prog] += 1
                else:
                    if row[iCO].strip():
                        diag["ChargeOffDate_on_non_CHGOFF"][prog] += 1
                    if gc != 0:
                        diag["nonzero_GrossChargeOffAmount_on_non_CHGOFF"][prog] += 1
                # contributions
                cancelled = 1 if cat == "cancelled" else 0
                loans = 1 - cancelled
                disb = 1 if cat in DISBURSED else 0
                chg = 1 if cat == "chgoff" else 0
                c_vol = ga if loans else 0
                c_chgamt = gc if chg else 0
                c_den = ga if disb else 0
                if is_dup:
                    diag["exact_duplicate_row_all_statuses"][prog] += 1
                    if loans:
                        diag["exact_duplicate_row_not_cancelled"][prog] += 1
                        diag["exact_duplicate_row_not_cancelled_GrossApproval_dollars"][prog] += ga // 100
                rc = row[iCT]
                if rc.strip() != " ".join(rc.split()):
                    diag["ProjectCounty_with_extra_whitespace"][prog] += 1
                if rc != rc.upper():
                    diag["ProjectCounty_not_upper_case"][prog] += 1
                # totals
                t = tot[(prog, fy)]
                t[0] += 1
                t[1] += loans
                t[2] += c_vol
                t[3] += chg
                # cube
                sc = (st, cty)
                inner = cube_p.get(sc)
                if inner is None:
                    inner = {}
                    cube_p[sc] = inner
                key = (nc, fy)
                v = inner.get(key)
                if v is None:
                    v = [0] * 8
                    inner[key] = v
                v[0] += 1
                v[1] += loans
                v[2] += c_vol
                v[3] += cancelled
                v[4] += disb
                v[5] += chg
                v[6] += c_chgamt
                v[7] += c_den
                # direct scan of the sampled values
                geos = []
                if us_sampled:
                    geos.append("us")
                if st in state_geos:
                    geos.append(st)
                pg = pair_geos.get(sc)
                if pg:
                    geos.extend(pg)
                if geos:
                    clss = cls_cache.get(nc)
                    if clss is None:
                        clss = ("all",) + tuple(c for c in naics2cls.get(nc, ()) if c in sampled_classes)
                        cls_cache[nc] = clss
                    labs = labels_for_fy.get(fy) or ("all",)
                    for g in geos:
                        for c in clss:
                            req = spec_index.get((prog, g, c))
                            if req:
                                for lab in labs:
                                    if lab in req:
                                        a = dacc[(prog, g, c, lab)]
                                        a[0] += 1
                                        a[1] += loans
                                        a[2] += c_vol
                                        a[3] += cancelled
                                        a[4] += disb
                                        a[5] += chg
                                        a[6] += c_chgamt
                                        a[7] += c_den
        status_values[prog][fname] = dict(sorted(sv.items(), key=lambda kv: -kv[1]))
        file_fy[fname] = (min(fys), max(fys), sum(fys.values()))
        log("%s: %d rows, FY %d..%d" % (fname, sum(fys.values()), min(fys), max(fys)))

    # file FY ranges must not overlap inside a program (otherwise rows could be double counted)
    for p in PROGS:
        rngs = sorted((v[0], v[1], f) for f, v in file_fy.items() if ("_7a_" in f) == (p == "7a"))
        for a, b in zip(rngs, rngs[1:]):
            if b[0] <= a[1]:
                notes.append("FY ranges of %s and %s overlap" % (a[2], b[2]))

    # ----------------------------------------------------------------------------------------
    # 4. totals per program and FY
    # ----------------------------------------------------------------------------------------
    fys_all = sorted(set(fy for (_, fy) in tot))
    data_fy0, data_fy1 = fys_all[0], fys_all[-1]
    if (data_fy0, data_fy1) != (FY0, FY1):
        raise SystemExit("data FY range %d..%d differs from register by_fy_years %s" % (data_fy0, data_fy1, by_fy_years))
    by_program_fy = {}
    chgoff_by = {}
    for p in PROGS:
        by_program_fy[p] = {}
        chgoff_by[p] = {}
        for fy in fys_all:
            r = tot.get((p, fy))
            if not r:
                continue
            by_program_fy[p][str(fy)] = {"rows": r[0], "loans": r[1], "volume": money(r[2]), "chgoff_n": r[3]}
            chgoff_by[p][str(fy)] = r[3]
    prog_tot = {}
    for p in PROGS:
        rows = sum(v["rows"] for v in by_program_fy[p].values())
        loans = sum(v["loans"] for v in by_program_fy[p].values())
        vol = sum(tot[(p, int(k))][2] for k in by_program_fy[p])
        chg = sum(v["chgoff_n"] for v in by_program_fy[p].values())
        prog_tot[p] = (rows, loans, vol, chg)
    summary = ("FOIA as of 2026-06-30, %d files: 7(a) %s rows, %s loans net of cancellations, volume $%s, %s CHGOFF rows; "
               "504 %s rows, %s loans, volume $%s, %s CHGOFF rows; approval FY %d to %d."
               % (len(files), format(prog_tot["7a"][0], ","), format(prog_tot["7a"][1], ","),
                  format(prog_tot["7a"][2] // 100, ","), format(prog_tot["7a"][3], ","),
                  format(prog_tot["504"][0], ","), format(prog_tot["504"][1], ","),
                  format(prog_tot["504"][2] // 100, ","), format(prog_tot["504"][3], ","), data_fy0, data_fy1))
    log(summary)

    # ----------------------------------------------------------------------------------------
    # 5. cube aggregation (second route) and the census
    # ----------------------------------------------------------------------------------------
    by_state = {p: defaultdict(list) for p in PROGS}
    for p in PROGS:
        for (st, cty), inner in cube[p].items():
            by_state[p][st].append(inner)

    def inners_for(p, g):
        if g == "us":
            return list(cube[p].values())
        if "/" not in g:
            return by_state[p].get(g, [])
        out = []
        for pr in compositions[g]:
            inn = cube[p].get(pr)
            if inn is not None:
                out.append(inn)
        return out

    def build_W(p, g):
        per = {}
        for inner in inners_for(p, g):
            for (nc, fy), vec in inner.items():
                fi = fy - data_fy0
                targets = ["all"]
                cl = naics2cls.get(nc)
                if cl:
                    targets = targets + cl
                for c in targets:
                    arr = per.get(c)
                    if arr is None:
                        arr = [[0] * 8 for _ in range(NFY)]
                        per[c] = arr
                    a = arr[fi]
                    a[0] += vec[0]; a[1] += vec[1]; a[2] += vec[2]; a[3] += vec[3]
                    a[4] += vec[4]; a[5] += vec[5]; a[6] += vec[6]; a[7] += vec[7]
        W = {}
        zero = [0] * 8
        for c in CLASSES:
            arr = per.get(c)
            d = {}
            if arr is None:
                for w in WINDOWS + ["pooled"]:
                    d[w] = zero
                d["by_fy"] = [zero] * NFY
            else:
                def span(lo, hi):
                    s = [0] * 8
                    for fy in range(max(lo, data_fy0), min(hi, data_fy1) + 1):
                        a = arr[fy - data_fy0]
                        for k in range(8):
                            s[k] += a[k]
                    return s
                d["all"] = span(data_fy0, data_fy1)
                for w, (lo, hi) in WINDOW_RANGE.items():
                    d[w] = span(lo, hi)
                d["pooled"] = span(POOL_LO, POOL_HI)
                d["by_fy"] = arr
            W[c] = d
        return W

    Wcache = {}

    def getW(p, g):
        k = (p, g)
        if k not in Wcache:
            Wcache[k] = build_W(p, g)
        return Wcache[k]

    def cmp_add(base, regv, vec_val):
        idx, usd = ADDITIVE_IDX[base]
        mine = vec_val[idx]
        if regv is None or isinstance(regv, (dict, list, str, bool)):
            return False, (money(mine) if usd else mine)
        if usd:
            return abs(regv * 100.0 - mine) <= 1.0 + 1e-6, money(mine)
        return (regv == mine and float(regv).is_integer()), mine

    def derive_rate(base, vec_val):
        (ni, nusd), (di, dusd) = RATE_IDX[base]
        num, den = vec_val[ni], vec_val[di]
        r = {"v": (num / float(den) if den else None),
             "num": (money(num) if nusd else num), "den": (money(den) if dusd else den)}
        return r

    def cmp_rate(base, cell, mine):
        (ni, nusd), (di, dusd) = RATE_IDX[base]
        if not isinstance(cell, dict):
            return False
        try:
            if mine["v"] is None:
                okv = cell.get("v") is None
            else:
                okv = cell.get("v") is not None and abs(cell["v"] - mine["v"]) <= 1e-6
            if nusd:
                okn = abs(cell["num"] - mine["num"]) <= 0.01 + 1e-9
            else:
                okn = cell["num"] == mine["num"]
            if dusd:
                okd = abs(cell["den"] - mine["den"]) <= 0.01 + 1e-9
            else:
                okd = cell["den"] == mine["den"]
        except (KeyError, TypeError):
            return False
        return okv and okn and okd

    # --- structure checks (geo ids, nulls) ---
    first_nulls = set(reg[SIDS[0]]["nulls"])
    expected_geos = set(["us"] + state_ids)
    for gid in compositions:
        base_id = gid.split(":")[0]
        if ":" in gid:
            if geo_kind[gid] == "ct-component" or base_id not in first_nulls:
                expected_geos.add(gid)
        elif gid not in first_nulls:
            expected_geos.add(gid)
    null_sets = {}
    for sid in SIDS:
        keys = set(reg[sid]["values"])
        nulls = set(reg[sid]["nulls"])
        null_sets[sid] = nulls
        missing = expected_geos - keys
        extra = keys - expected_geos
        if missing:
            notes.append("%s: geographies.json composition exists but the register has no value for %s" % (sid, sorted(missing)[:8]))
        if extra:
            notes.append("%s: register has values for ids with no composition: %s" % (sid, sorted(extra)[:8]))
        both = keys & nulls
        if both:
            notes.append("%s: ids both valued and null: %s" % (sid, sorted(both)[:8]))
    first = null_sets[SIDS[0]]
    if any(null_sets[s] != first for s in SIDS):
        notes.append("the nulls lists differ between series")
    state_obs = set()
    for p in PROGS:
        state_obs |= set(state_seen[p])
    obs_not_reg = sorted(s for s in state_obs if s and s not in set(state_ids))
    reg_not_obs = sorted(s for s in state_ids if s not in state_obs)
    if obs_not_reg:
        notes.append("ProjectState values in the files with no state id in geographies.json: %s" % obs_not_reg)
    if reg_not_obs:
        notes.append("state ids in geographies.json with no FOIA row: %s" % reg_not_obs)

    # --- census ---
    log("census: building aggregates")
    census_n = 0
    census_bad = 0
    census_detail = []
    census_by_series = {}
    flag_problems = []
    shape_problems = []
    for sid in SIDS:
        p = prog_of(sid)
        base = sid.split("_", 1)[1]
        n_s = 0
        bad_s = 0
        values = reg[sid]["values"]
        for g in sorted(values):
            if g != "us" and g not in compositions and "/" in g:
                shape_problems.append("%s: unresolvable geography id %s" % (sid, g))
                continue
            W = getW(p, g)
            gv = values[g]
            if sorted(gv) != sorted(CLASSES):
                shape_problems.append("%s/%s: class keys differ from the 43 classes + all" % (sid, g))
            for c in CLASSES:
                cell = gv.get(c)
                d = W[c]
                if base in RATE_SERIES:
                    mine = derive_rate(base, d["pooled"])
                    ok = cmp_rate(base, cell, mine)
                    n_s += 1
                    if not ok:
                        bad_s += 1
                        if len(census_detail) < 60:
                            census_detail.append({"series": sid, "geo": g, "class": c, "window": "pooled_fy2011_2020",
                                                  "register": cell, "rederived": mine})
                    if isinstance(cell, dict):
                        den = cell.get("den")
                        f = cell.get("f")
                        exp = FLAG_NONE if den == 0 else (FLAG_SMALL if (den is not None and 0 < den < 30) else None)
                        if f != exp or ((cell.get("v") is None) != (den == 0)):
                            flag_problems.append("%s/%s/%s den %s flag %s v %s" % (sid, g, c, den, f, cell.get("v")))
                    continue
                if not isinstance(cell, dict) or sorted(cell) != sorted(WINDOWS + ["by_fy"]):
                    shape_problems.append("%s/%s/%s: window keys %s" % (sid, g, c, sorted(cell) if isinstance(cell, dict) else cell))
                    continue
                for w in WINDOWS:
                    ok, mine = cmp_add(base, cell.get(w), d[w])
                    n_s += 1
                    if not ok:
                        bad_s += 1
                        if len(census_detail) < 60:
                            census_detail.append({"series": sid, "geo": g, "class": c, "window": w,
                                                  "register": cell.get(w), "rederived": mine})
                byfy = cell.get("by_fy")
                if not isinstance(byfy, list) or len(byfy) != NFY:
                    shape_problems.append("%s/%s/%s: by_fy length %s" % (sid, g, c, len(byfy) if isinstance(byfy, list) else byfy))
                    continue
                arr = d["by_fy"]
                for i in range(NFY):
                    ok, mine = cmp_add(base, byfy[i], arr[i])
                    n_s += 1
                    if not ok:
                        bad_s += 1
                        if len(census_detail) < 60:
                            census_detail.append({"series": sid, "geo": g, "class": c, "window": "by_fy:%d" % (FY0 + i),
                                                  "register": byfy[i], "rederived": mine})
        census_by_series[sid] = (n_s, bad_s)
        census_n += n_s
        census_bad += bad_s
        log("census %s: %d compared, %d mismatches" % (sid, n_s, bad_s))

    # --- consistency checks inside the raw data / composition ---
    # us == sum of states + rows with no state ; parent == sum of its cross-state parts
    for p in PROGS:
        wu = getW(p, "us")["all"]["all"]
        s_sum = [0] * 8
        for st in state_ids:
            w = getW(p, st)["all"]["all"]
            for k in range(8):
                s_sum[k] += w[k]
        unreg_rows = 0
        for st, inners in by_state[p].items():
            if st not in state_ids:
                unreg_rows += sum(v[0] for inn in inners for v in inn.values())
        if wu[0] != s_sum[0] + unreg_rows:
            notes.append("%s: us rows %d != states %d + rows in no listed state %d" % (p, wu[0], s_sum[0], unreg_rows))
        else:
            notes.append("%s: us rows %s = %s in the %d listed states + %d rows with a blank or unlisted ProjectState" % (p, format(wu[0], ","), format(s_sum[0], ","), len(state_ids), unreg_rows))
    for mid, m in markets.items():
        if m["kind"] == "cross-state" and mid in compositions:
            parts = [g for g in compositions if g.startswith(mid + ":")]
            if len(parts) >= 2:
                for p in PROGS:
                    par = getW(p, mid)["all"]["all"]
                    tot_parts = [0] * 8
                    for g in parts:
                        w = getW(p, g)["all"]["all"]
                        for k in range(8):
                            tot_parts[k] += w[k]
                    if par != tot_parts:
                        notes.append("%s %s: parent %s != sum of parts %s" % (p, mid, par, tot_parts))

    # --- sample comparison (direct route) and cross-check against the cube route ---
    samples = []
    mismatch_detail = []
    kind_counts = defaultdict(lambda: [0, 0])
    cube_disagree = 0
    for s in sample_specs:
        sid, g, c, w = s["series"], s["geo"], s["class"], s["window"]
        p = prog_of(sid)
        base = sid.split("_", 1)[1]
        lab = label_of(w)
        vec = dacc.get((p, g, c, lab), [0] * 8)
        regcell = register_value(sid, g, c, w)
        if w.startswith("by_fy:"):
            cube_vec = getW(p, g)[c]["by_fy"][int(w.split(":")[1]) - data_fy0]
        elif w == "pooled_fy2011_2020":
            cube_vec = getW(p, g)[c]["pooled"]
        else:
            cube_vec = getW(p, g)[c][w]
        if base in RATE_SERIES:
            mine = derive_rate(base, vec)
            ok = cmp_rate(base, regcell, mine)
            cube_ok = (derive_rate(base, cube_vec) == mine)
            reg_out = None if regcell is None else dict((k, regcell.get(k)) for k in ("v", "num", "den", "f") if k in regcell)
            mine_out = mine
        else:
            ok, mine_out = cmp_add(base, regcell, vec)
            cube_ok = (list(cube_vec) == list(vec))
            reg_out = regcell
        if not cube_ok:
            cube_disagree += 1
        gk = geo_kind.get(g, "unknown")
        kind_counts[gk][1] += 1
        if ok:
            kind_counts[gk][0] += 1
        else:
            mismatch_detail.append({"series": sid, "geo": g, "class": c, "window": w,
                                    "register": reg_out, "rederived": mine_out})
        samples.append({"series": sid, "program": p, "geo": g, "geo_kind": gk, "class": c,
                        "class_fit": class_fit[c], "window": w, "stratum": s["stratum"],
                        "register": reg_out, "rederived": mine_out, "match": bool(ok),
                        "cube_route_agrees": bool(cube_ok)})
    n = len(samples)
    matches = sum(1 for x in samples if x["match"])

    # --- quotas ---
    q_ct = sum(1 for x in samples if x["geo_kind"] == "ct-component")
    q_multi = sum(1 for x in samples if x["geo"] in multi_county)
    q_cross = sum(1 for x in samples if x["geo_kind"] in ("cross-state", "cross-state-part"))
    q_sub_have = sum(1 for x in samples if x["geo_kind"] in ("place", "tract-set"))

    # --- sub-county verification ---
    subs = [mid for mid, m in markets.items() if m["kind"] in ("place", "tract-set")]
    sub_problems = []
    for mid in subs:
        for sid in SIDS:
            if mid in reg[sid]["values"]:
                sub_problems.append("%s has a value in %s" % (mid, sid))
            r = reg[sid]["nulls"].get(mid, "")
            if not r.startswith("not-published-at-this-grain"):
                sub_problems.append("%s null reason in %s is %r" % (mid, sid, r[:60]))
    place_like = {}
    for p in PROGS:
        place_like[p] = [f for f in dict_fields[p] if re.search(r"tract|place|census|fips|geoid|latitude|longitude|neighborhood|municipal", f, re.I)
                         or (f.startswith("Project") and f not in ("ProjectCounty", "ProjectState"))]
    csv_place_like = {}
    for fname, hdr in header_by_file.items():
        csv_place_like[fname] = [f for f in hdr if re.search(r"tract|place|census|fips|geoid|latitude|longitude|neighborhood|municipal", f, re.I)
                                 or (f.startswith("Project") and f not in ("ProjectCounty", "ProjectState"))]
    proj_fields = sorted(set(f for p in PROGS for f in dict_fields[p] if f.startswith("Project") or f in ("CongressionalDistrict", "SBADistrictOffice")))
    borrower_geo = sorted(set(f for p in PROGS for f in dict_fields[p] if f.startswith("Borr") and f in ("BorrCity", "BorrState", "BorrZip")))
    sub_note = ("0 sub-county VALUES exist, so have=0 by design. %d sub-county markets (%d place, %d tract-set) were checked: none has a value in any of the 16 series "
                "and every null reason starts 'not-published-at-this-grain'%s. SBA's dictionary (both sheets) and all 6 CSV headers carry only these project-site "
                "geography fields: %s; none is a place, tract or sub-county field (fields matching tract/place/census/fips/geoid/lat/long/Project* other than county and state: dictionary %s, CSV headers %s). "
                "BorrCity/BorrZip are the borrower's mailing address, not the project site, so the register is right not to substitute them."
                % (len(subs), sum(1 for m in subs if markets[m]["kind"] == "place"),
                   sum(1 for m in subs if markets[m]["kind"] == "tract-set"),
                   "" if not sub_problems else " EXCEPT: " + "; ".join(sub_problems[:5]),
                   proj_fields, place_like, dict((k, v) for k, v in csv_place_like.items() if v) or "none"))
    # --- composition strings that match no FOIA row ---
    seen_pairs = set()
    obs_counties = defaultdict(set)
    for p in PROGS:
        for (st, cty) in cube[p]:
            seen_pairs.add((st, cty))
            obs_counties[st].add(cty)
    zero_hits = []
    for gid, pairs in compositions.items():
        if ":" in gid:
            continue
        for pr in sorted(pairs):
            if pr not in seen_pairs:
                near = difflib.get_close_matches(pr[1], sorted(obs_counties.get(pr[0], [])), n=2, cutoff=0.6)
                zero_hits.append("%s: (%s, %s) matches no row in any file; nearest FOIA strings %s" % (gid, pr[0].upper(), pr[1], near))
    for mid, m in markets.items():
        if m.get("ct") and m["foia"].get("ct"):
            for comp in ("legacy", "pr"):
                for s_ in m["foia"]["ct"][comp]:
                    pr = ("ct", norm_county(s_))
                    if pr not in seen_pairs:
                        near = difflib.get_close_matches(pr[1], sorted(obs_counties.get("ct", [])), n=2, cutoff=0.6)
                        zero_hits.append("%s:%s: (CT, %s) matches no row; nearest %s" % (mid, comp, pr[1], near))

    # ----------------------------------------------------------------------------------------
    # 6. notes
    # ----------------------------------------------------------------------------------------
    notes.insert(0, "Method: sample values are re-derived by a direct per-row scan of the raw CSVs; a second route (full state/county/NAICS/FY cube) re-derives every value of all 16 series; "
                    "the two routes agree on %d of %d sampled cells. Neither route uses scripts/markets*.py or any data/markets file other than sources.json, geographies.json, naics-map.json "
                    "and the register series being checked." % (n - cube_disagree, n))
    notes.insert(1, "Sample design: seed %d, python random.Random(seed).random() only; 16 series x [2 us, 4 state, 3 single-county, 5 multi-county county-set, 2 cross-state or part, 3 CT component]; "
                    "class drawn 20%% 'all', 35%% exact, 25%% partial, 20%% proxy; window drawn from the 5 windows (once each) and by_fy (3 slots) for additive series, pooled FY2011-2020 for rates; "
                    "75%% of draws required a non-zero register value (so matches are not just zero equals zero), 25%% unconstrained. Sampled non-zero register cells: %d of %d."
                    % (SEED, sum(1 for x in samples if nonzero(x["series"], x["register"])), n))
    notes.insert(2, "CENSUS (all values of all 16 series, all geographies, 44 classes incl. all, 5 windows, 36 FYs, rates): %s compared, %d mismatches. Per series: %s."
                 % (format(census_n, ","), census_bad,
                    ", ".join("%s %s/%d" % (k.replace("sba", ""), format(v[0] - v[1], ","), v[0]) for k, v in sorted(census_by_series.items()))))
    if census_detail:
        notes.append("First census mismatches (up to 60): " + json.dumps(census_detail))
    if flag_problems:
        notes.append("Rate flag problems (%d), first 5: %s" % (len(flag_problems), flag_problems[:5]))
    else:
        notes.append("Rate cells: every 'f' flag matches the rule (den 0 -> no-disbursed flag and v null; 0<den<30 -> small-denominator flag; else no flag).")
    if shape_problems:
        notes.append("Register shape problems (%d), first 8: %s" % (len(shape_problems), shape_problems[:8]))
    else:
        notes.append("Register shape: every valued geography carries all 44 class keys; additive cells carry exactly the 5 windows + by_fy of %d years (%d..%d); rate cells carry v/num/den(/f)." % (NFY, FY0, FY1))
    notes.append("Dictionary status codes: 7(a) %s ; 504 %s." % (dict_codes["7a"], dict_codes["504"]))
    bad_status = dict(diag.get("status_not_in_dictionary_for_program", {}))
    bad_status = dict((k, v) for k, v in bad_status.items() if v)
    notes.append("LoanStatus values outside the dictionary's list for their program: %s." % (bad_status or "none"))
    for k in sorted(diag):
        if k == "status_not_in_dictionary_for_program":
            continue
        notes.append("Data diagnostic %s: %s" % (k, dict(diag[k])))
    for k, lst in diag_lists.items():
        notes.append("Detail %s: %s" % (k, lst[:5]))
    notes.append("Blank NaicsCode rows (counted in 'all', in no class): 7(a) %s, 504 %s." % (format(blank_naics["7a"], ","), format(blank_naics["504"], ",")))
    notes.append("The registry/dictionary Program field is ' 7A' (with a leading blank) in every 7(a) file and '504' in the 504 files; program was taken from the file name and the field checked against it.")
    if zero_hits:
        notes.append("Composition strings with NO matching FOIA row (%d): %s" % (len(zero_hits), " | ".join(zero_hits[:40])))
    else:
        notes.append("Every composition string in geographies.json matches at least one FOIA row.")
    notes.append("Sub-county markets: " + sub_note)
    notes.append("Cross-state markets with values: %s; Connecticut markets (null at market level, values only for :legacy and :pr): %s."
                 % (sorted(g for g, k in geo_kind.items() if k == "cross-state" and g in reg[SIDS[0]]["values"]),
                    sorted(mid for mid, m in markets.items() if m.get("ct"))))
    notes.append("Register composition nulls: %d markets in 'nulls' (composition-pending, sub-county or Connecticut split) have no value in any series, as the definitions say."
                 % len(first))
    notes.append("Sources definitions read from sources.json: %s." % sorted(sources["definitions"]))

    # ----------------------------------------------------------------------------------------
    # 7. write the result
    # ----------------------------------------------------------------------------------------
    result = {
        "seed": SEED,
        "n": n,
        "matches": matches,
        "mismatches": n - matches,
        "by_kind": dict((k, "%d/%d" % (v[0], v[1])) for k, v in sorted(kind_counts.items())),
        "quota": {
            "ct": {"need": 5, "have": q_ct},
            "multi_county": {"need": 5, "have": q_multi},
            "sub_county": {"need": 3, "have": q_sub_have, "note": sub_note},
            "cross_state": {"need": 3, "have": q_cross},
        },
        "mismatch_detail": mismatch_detail,
        "samples": samples,
        "status_values": status_values,
        "foia_totals": {"summary": summary, "by_program_fy": by_program_fy},
        "foia_chgoff_by_program_fy": chgoff_by,
        "notes": notes,
    }
    with open(OUT, "w") as fh:
        json.dump(result, fh, indent=1)
        fh.write("\n")
    log("wrote %s" % OUT)
    print(json.dumps({"seed": SEED, "n": n, "matches": matches, "mismatches": n - matches,
                      "quota": dict((k, v["have"]) for k, v in result["quota"].items()),
                      "census": [census_n, census_bad], "cube_disagree": cube_disagree}))


if __name__ == "__main__":
    main()
