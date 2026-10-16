#!/usr/bin/env python3
"""Case model engine for the worked cases on feasibility-study-company.com (WEB-FSC-6).

Each case has one input file, data/cases/<slug>.json. Every input carries its basis: the
number of a source in the case page's numbered sources list, or the label "assumption"
with its reasoning. The engine computes sources and uses, the loan structure under the
program's rules, a five-year pro forma, DSCR by year, break-even, a two-driver sensitivity
matrix and the determination (as proposed, and as restructured when the proposed structure
fails a floor, a tier or a cap). SBA rules come from data/regulatory/sba.json; USDA B&I and
HUD 232 terms come from the case inputs, each cited to its program source on the page.

The case page carries <!--case:<slug>.<name>--> regions (build.py writes them from
{{case:<name>}} in the page source); this script fills them.

    python3 scripts/casemodel.py                 write every case region into the served pages
    python3 scripts/casemodel.py --check         exit 1 if any case region is stale or unknown
    python3 scripts/casemodel.py --case <slug>   print one case's computed model as JSON
    python3 scripts/casemodel.py --only <slug>   write (or with --check, check) one case only
    python3 scripts/casemodel.py --dump <dir>    write every computed model as <dir>/<slug>.json

Tables: glance, inputs, revenue, opex, uses, sources, loan, proforma, dscr, determination,
verdict, breakeven, sensitivity. Inline values: v.<name>, listed by --case under "values".
Input file keys are documented in src/README.md.
"""
import argparse
import ast
import copy
import html
import json
import math
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CASES = os.path.join(ROOT, "data", "cases")
SBA_FILE = os.path.join(ROOT, "data", "regulatory", "sba.json")
CARDS = os.path.join(ROOT, "src", "case-cards.json")
RETURNS = os.path.join(ROOT, "data", "returns")
INDEX = os.path.join(ROOT, "case-studies", "index.html")
REGION = re.compile(r"<!--case:([a-z0-9-]+)\.([a-z0-9_.]+)-->(.*?)<!--/case:\1\.\2-->", re.S)
CITE = re.compile(r"\[\^(\d+(?:\s*,\s*\d+)*)\]")
YEARS = 5


class ModelError(Exception):
    pass


# ------------------------------------------------------------------ number parsing and format

def pct(text):
    m = re.search(r"(-?\d+(?:\.\d+)?)\s*%", str(text))
    if not m:
        raise ModelError(f"no percentage in {text!r}")
    return float(m.group(1)) / 100.0


def ratio(text):
    m = re.search(r"(\d+(?:\.\d+)?)\s*x", str(text))
    if not m:
        raise ModelError(f"no ratio in {text!r}")
    return float(m.group(1))


def money(text):
    t = str(text).replace(",", "")
    m = re.search(r"\$\s*(\d+(?:\.\d+)?)\s*(million|billion)?", t)
    if not m:
        raise ModelError(f"no dollar amount in {text!r}")
    v = float(m.group(1))
    return v * {"million": 1e6, "billion": 1e9}.get(m.group(2) or "", 1)


def fmt_money(v):
    if v is None:
        return "n/a"
    r = int(round(v))
    return f"(${-r:,})" if r < 0 else f"${r:,}"


def fmt_pct(v, nd=1):
    return "n/a" if v is None else f"{v * 100:.{nd}f}%"


def fmt_x(v):
    """Coverage ratios display truncated to two decimals, so a shown 1.15x always meets a 1.15x floor."""
    return "n/a" if v is None else f"{math.floor(v * 100 + 1e-9) / 100:.2f}x"


def fmt_num(v, nd=0):
    if v is None:
        return "n/a"
    return f"{v:,.{nd}f}"


def fmt_value(v, f):
    if isinstance(v, list):
        return " / ".join(fmt_value(x, f) for x in v)
    if f == "$":
        return fmt_money(v)
    if f == "$2":
        return f"${v:,.2f}"
    if f == "%":
        return fmt_pct(v)
    if f == "%2":
        return fmt_pct(v, 2)
    if f == "x":
        return fmt_x(v)
    if f == "cpg":
        return f"{v * 100:.1f} cents"
    if f == "n1":
        return fmt_num(v, 1)
    if f == "n2":
        return fmt_num(v, 2)
    if f == "yr":
        return f"{v:g} years"
    return fmt_num(v)


def esc(t):
    return html.escape(str(t), quote=False)


# ------------------------------------------------------------------ SBA rules from sba.json

class SBA:
    def __init__(self, data):
        self.d = data

    def node(self, path):
        cur = self.d
        for part in path.split("."):
            cur = cur[part]
        return cur

    def val(self, path):
        n = self.node(path)
        return n["value"] if isinstance(n, dict) and "value" in n else n

    def rule(self, path, parse):
        return parse(self.val(path))

    def fee_7a(self, loan, guaranteed):
        """Upfront guaranty fee, FY2027 schedule (fees_fy2027.upfront_7a). A proposed loan above the
        program limit has no tier of its own; it is charged on the top tier's terms, and the structure
        then fails the size test and is restructured under the limit."""
        tiers = []
        for label, text in self.val("fees_fy2027.upfront_7a"):
            if "maturity" in label:
                continue
            nums = [float(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", label)]
            lo, hi = (0.0, nums[0]) if "or less" in label else (nums[0], nums[1])
            tiers.append((lo, hi, text))
        tiers.sort()
        pick = next((t for t in tiers if t[0] <= round(loan) <= t[1]), None)
        if pick is None and tiers and round(loan) > tiers[-1][1]:
            pick = tiers[-1]
        if pick is None:
            raise ModelError(f"no FY2027 7(a) fee tier for a loan of {loan:,.0f}")
        text = pick[2]
        rates = [float(x) / 100 for x in re.findall(r"(\d+(?:\.\d+)?)%", text)]
        split = re.search(r"up to \$([\d,]+)", text)
        if split and len(rates) == 2:
            cut = float(split.group(1).replace(",", ""))
            return rates[0] * min(guaranteed, cut) + rates[1] * max(0.0, guaranteed - cut)
        return rates[0] * guaranteed

    def spread_7a(self, loan):
        for label, text in self.val("rates.spreads_7a"):
            nums = [float(x.replace(",", "")) for x in re.findall(r"\$([\d,]+)", label)]
            if "or less" in label:
                lo, hi = 0.0, nums[0]
            elif "and over" in label:
                lo, hi = nums[0], float("inf")
            else:
                lo, hi = nums[0], nums[1]
            if lo <= round(loan) <= hi:
                return pct(text)
        raise ModelError("no 7(a) spread tier")


# ------------------------------------------------------------------ safe expressions

ALLOWED_CALLS = {"min": min, "max": max, "round": round}


def evaluate(expr, names, where):
    try:
        tree = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise ModelError(f"{where}: bad expression {expr!r}: {exc}")

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return float(n.value)
        if isinstance(n, ast.Name):
            if n.id not in names:
                raise ModelError(f"{where}: unknown name {n.id!r} in {expr!r}")
            v = names[n.id]
            if isinstance(v, list):
                return float(v[names["y"]])
            return float(v)
        if isinstance(n, ast.Subscript):
            base = names.get(n.value.id) if isinstance(n.value, ast.Name) else None
            if not isinstance(base, list):
                raise ModelError(f"{where}: subscript on a non-list in {expr!r}")
            idx = n.slice.value if isinstance(n.slice, ast.Index) else n.slice
            return float(base[int(ev(idx))])
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            ops = {ast.Add: lambda: a + b, ast.Sub: lambda: a - b, ast.Mult: lambda: a * b,
                   ast.Div: lambda: a / b, ast.Pow: lambda: a ** b}
            if type(n.op) not in ops:
                raise ModelError(f"{where}: operator not allowed in {expr!r}")
            return ops[type(n.op)]()
        if isinstance(n, ast.UnaryOp) and isinstance(n.op, (ast.USub, ast.UAdd)):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id in ALLOWED_CALLS:
            return float(ALLOWED_CALLS[n.func.id](*[ev(a) for a in n.args]))
        raise ModelError(f"{where}: construct not allowed in {expr!r}")
    return ev(tree)


# ------------------------------------------------------------------ finance math

def payment(principal, rate, years):
    if principal <= 0:
        return 0.0
    if years <= 0:
        raise ModelError("amortization of zero years")
    r = rate / 12.0
    n = years * 12
    if r == 0:
        return principal / years
    return principal * r / (1 - (1 + r) ** -n) * 12


def principal_for(annual_payment, rate, years):
    r = rate / 12.0
    n = years * 12
    if r == 0:
        return annual_payment * years
    return annual_payment / 12 / r * (1 - (1 + r) ** -n)


# ------------------------------------------------------------------ the model

class Case:
    def __init__(self, path, sba):
        self.path = path
        self.spec = json.load(open(path, encoding="utf-8"))
        self.slug = self.spec["slug"]
        if os.path.splitext(os.path.basename(path))[0] != self.slug:
            raise ModelError(f"{path}: slug does not match file name")
        self.sba = sba
        self.program = self.spec["program"]
        if self.program not in ("sba_7a", "sba_504", "usda_bi", "hud_232"):
            raise ModelError(f"{self.slug}: unknown program {self.program}")
        self.check_inputs()

    # -- inputs
    def check_inputs(self):
        if self.program != "hud_232" and any("per_loan" in u for u in self.spec["uses"]):
            raise ModelError(f"{self.slug}: per_loan uses are supported for hud_232 only")
        for name, inp in self.spec["inputs"].items():
            if not re.match(r"^[a-z][a-z0-9_]*$", name):
                raise ModelError(f"{self.slug}: bad input name {name}")
            has_src = bool(inp.get("source"))
            has_ass = bool(inp.get("assumption"))
            if has_src == has_ass:
                raise ModelError(f"{self.slug}: input {name} needs exactly one of source or assumption")
            v = inp.get("value")
            if isinstance(v, list):
                if len(v) != YEARS:
                    raise ModelError(f"{self.slug}: input {name} lists {len(v)} values, not {YEARS}")
            elif not isinstance(v, (int, float)):
                raise ModelError(f"{self.slug}: input {name} value is not a number or a list")

    def inputs(self, overrides=None):
        vals = {k: copy.deepcopy(v["value"]) for k, v in self.spec["inputs"].items()}
        for k, m in (overrides or {}).items():
            v = vals[k]
            vals[k] = [x * m for x in v] if isinstance(v, list) else v * m
        return vals

    # -- uses
    def uses(self, vals):
        out = []
        for u in self.spec["uses"]:
            if "per_loan" in u:
                continue  # sized on the loan actually made; see finance()
            amt = evaluate(u["expr"], dict(vals, y=0), f"{self.slug} use {u['key']}")
            out.append({"key": u["key"], "label": u["label"], "amount": amt, "class": u.get("class", "other"),
                        "basis": u.get("basis", "")})
        return out

    # -- operations
    def operate(self, vals, tpc):
        years = []
        for y in range(YEARS):
            names = dict(vals, y=y, tpc=tpc)
            rev = []
            for line in self.spec["revenue"]:
                v = evaluate(line["expr"], names, f"{self.slug} revenue {line['key']}")
                names["rev_" + line["key"]] = v
                rev.append(v)
            names["rev_total"] = sum(rev)
            cos = []
            for line in self.spec.get("cost_of_sales", []):
                v = evaluate(line["expr"], names, f"{self.slug} cost of sales {line['key']}")
                names["cos_" + line["key"]] = v
                cos.append(v)
            names["cos_total"] = sum(cos)
            names["gp_total"] = names["rev_total"] - names["cos_total"]
            opx = []
            for line in self.spec["opex"]:
                v = evaluate(line["expr"], names, f"{self.slug} opex {line['key']}")
                names["opex_" + line["key"]] = v
                opx.append(v)
            noi = names["gp_total"] - sum(opx)
            years.append({"revenue": rev, "rev_total": names["rev_total"], "cos": cos, "cos_total": names["cos_total"],
                          "gp_total": names["gp_total"], "opex": opx, "opex_total": sum(opx), "noi": noi})
        return years

    # -- program rules
    def rules(self):
        s, p, sb = self.sba, self.program, self.spec.get("sba", {})
        r = {}
        if p == "sba_7a":
            purpose = sb.get("purpose")
            if purpose == "startup":
                r["equity_path"] = "equity.startup_7a"
                r["floor_path"] = "dscr.standard_7a"
                r["test"] = "projected"
                r["test_year"] = int(self.spec.get("dscr_test_year", 2))
            elif purpose == "acquisition":
                r["equity_path"] = "equity.coo_initial_acquisition"
                r["floor_path"] = "dscr.coo_initial_acquisition"
                r["test"] = "historical"
            else:
                raise ModelError(f"{self.slug}: sba.purpose must be startup or acquisition for 7(a)")
            r["equity_req"] = s.rule(r["equity_path"], pct)
            r["floor"] = s.rule(r["floor_path"], ratio)
            r["cap"] = s.rule("limits.max_7a", money)
            r["cap_path"] = "limits.max_7a"
        elif p == "sba_504":
            new = sb.get("business_age") == "new"
            special = bool(sb.get("special_purpose"))
            r["equity_path"] = ("equity.sba_504_new_and_special" if new and special else
                                "equity.sba_504_new_or_special" if new or special else "equity.sba_504_standard")
            r["equity_req"] = s.rule(r["equity_path"], pct)
            r["floor_path"] = "dscr.sba_504"
            r["floor"] = s.rule("dscr.sba_504", ratio)
            r["cap_path"] = "limits.max_504_manufacturer" if sb.get("manufacturer") else "limits.max_504"
            r["cap"] = s.rule(r["cap_path"], money)
            r["test"] = "projected"
            r["test_year"] = int(self.spec.get("dscr_test_year", 2))
        elif p == "usda_bi":
            v = self.inputs()
            r["equity_req"] = v["bi_equity_min_pct"]
            r["floor"] = v["bi_dscr_floor"]
            r["cap"] = v.get("bi_loan_cap")
            r["test"] = "projected"
            r["test_year"] = int(self.spec.get("dscr_test_year", 3))
        elif p == "hud_232":
            v = self.inputs()
            r["equity_req"] = 1 - v["hud_max_ltc"]
            r["floor"] = v["hud_dscr_floor"]
            r["cap"] = None
            r["test"] = "projected"
            r["test_year"] = int(self.spec.get("dscr_test_year", 3))
        return r

    # -- financing for a given equity share
    def finance(self, vals, uses, equity_pct, rules, debenture_cap=True):
        base = sum(u["amount"] for u in uses)
        re_share = sum(u["amount"] for u in uses if u["class"] == "real_estate") / base if base else 0
        p = self.program
        t = {"tranches": [], "fees": [], "equity_pct": equity_pct}
        if p == "sba_7a":
            g = vals["sba_guaranty_pct"]
            fee = 0.0
            for _ in range(60):
                tpc = base + fee
                loan = tpc * (1 - equity_pct)
                waived = self.spec.get("sba", {}).get("rural_fee_waiver") and loan <= self.sba.rule("fees_fy2027.waiver_7a_max_loan", money)
                new_fee = 0.0 if waived else self.sba.fee_7a(loan, loan * g)
                if abs(new_fee - fee) < 0.005:
                    fee = new_fee
                    break
                fee = new_fee
            tpc = base + fee
            loan = tpc * (1 - equity_pct)
            if "rate_7a" in vals:
                rate = vals["rate_7a"]
                rate_basis = "input"
            else:
                rate = self.sba.rule("rates.prime", pct) + self.sba.spread_7a(loan)
                rate_basis = "prime_plus_max"
            purpose = self.spec["sba"]["purpose"]
            re_years = self.sba.val("terms.real_estate_max_years")
            if purpose == "acquisition":
                sp = self.spec["sba"].get("special_purpose") and re_share >= self.sba.rule("terms.coo_special_purpose_threshold", pct)
                if sp:
                    parts = [("Whole loan", loan, int(self.sba.val("terms.coo_special_purpose_max_years")), "terms.coo_special_purpose_max_years")]
                else:
                    re_part = loan * re_share
                    parts = [("Real estate portion", re_part, int(re_years), "terms.real_estate_max_years"),
                             ("Business portion", loan - re_part, int(self.sba.val("terms.coo_amortization_years")), "terms.coo_amortization_years")]
            else:
                if re_share >= 0.51:
                    parts = [("Whole loan", loan, int(re_years), "terms.mixed_purpose_7a")]
                else:
                    yrs = re_share * int(re_years) + (1 - re_share) * int(vals.get("non_re_years", 10))
                    parts = [("Whole loan (blended)", loan, round(yrs), "terms.mixed_purpose_7a")]
            for label, amt, yrs, path in parts:
                if amt > 0:
                    t["tranches"].append({"label": f"SBA 7(a) loan, {label.lower()}", "lender": "Bank (SBA 7(a), {:.0f}% guaranteed)".format(g * 100),
                                          "amount": amt, "rate": rate, "years": yrs, "rule_path": path,
                                          "ds": payment(amt, rate, yrs)})
            t["rate_basis"] = rate_basis
            t["fees"].append({"label": "SBA upfront guaranty fee (added to project cost)", "amount": fee, "rule_path": "fees_fy2027.upfront_7a"})
            t["loan_total"] = loan
            t["cap_amount"] = loan
        elif p == "sba_504":
            fee_rate = 0.0 if self.spec.get("sba", {}).get("rural_fee_waiver") else self.sba.rule("fees_fy2027.upfront_504", pct)
            fee = 0.0
            for _ in range(60):
                tpc = base + fee
                eq = tpc * equity_pct
                tpl = tpc * 0.5
                deb = tpc - tpl - eq
                if debenture_cap and deb > rules["cap"]:
                    deb = rules["cap"]
                    tpl = tpc - eq - deb
                new_fee = deb * fee_rate
                if abs(new_fee - fee) < 0.005:
                    fee = new_fee
                    break
                fee = new_fee
            tpc = base + fee
            eq = tpc * equity_pct
            tpl = tpc * 0.5
            deb = tpc - tpl - eq
            if debenture_cap and deb > rules["cap"]:
                deb = rules["cap"]
                tpl = tpc - eq - deb
            t["tranches"].append({"label": "Third-party first lien", "lender": "Bank", "amount": tpl,
                                  "rate": vals["tpl_rate"], "years": int(vals["tpl_amort_years"]), "rule_path": "equity.sba_504_split",
                                  "ds": payment(tpl, vals["tpl_rate"], int(vals["tpl_amort_years"]))})
            t["tranches"].append({"label": "SBA 504 debenture", "lender": "CDC (SBA-guaranteed debenture)", "amount": deb,
                                  "rate": vals["debenture_rate"], "years": int(vals["debenture_years"]), "rule_path": "terms.sba_504_maturities",
                                  "ds": payment(deb, vals["debenture_rate"], int(vals["debenture_years"]))})
            t["fees"].append({"label": "SBA 504 upfront fee on the debenture (added to project cost)", "amount": fee, "rule_path": "fees_fy2027.upfront_504"})
            t["loan_total"] = tpl + deb
            t["debenture"] = deb
            t["tpl"] = tpl
            t["cap_amount"] = tpc - tpc * 0.5 - eq
        elif p == "usda_bi":
            g, fr = vals["bi_guarantee_pct"], vals["bi_fee_pct"]
            fee = 0.0
            for _ in range(60):
                tpc = base + fee
                loan = tpc * (1 - equity_pct)
                new_fee = loan * g * fr
                if abs(new_fee - fee) < 0.005:
                    fee = new_fee
                    break
                fee = new_fee
            tpc = base + fee
            loan = tpc * (1 - equity_pct)
            yrs = int(vals["bi_amort_years"])
            t["tranches"].append({"label": "USDA B&I guaranteed loan", "lender": "Bank ({:.0f}% USDA guarantee)".format(g * 100),
                                  "amount": loan, "rate": vals["bi_rate"], "years": yrs, "rule_path": None,
                                  "ds": payment(loan, vals["bi_rate"], yrs)})
            t["fees"].append({"label": "USDA guarantee fee (added to project cost)", "amount": fee, "rule_path": None})
            t["loan_total"] = loan
            t["cap_amount"] = loan
        elif p == "hud_232":
            fee = vals.get("hud_upfront_fees", 0.0)
            # uses marked per_loan are a share of the loan made: loan = (1 - e) * (base + fee + k * loan)
            per = [(u, evaluate(u["per_loan"], dict(vals, y=0), f"{self.slug} use {u['key']}")) for u in self.spec["uses"] if "per_loan" in u]
            k = sum(x for _, x in per)
            loan = (1 - equity_pct) * (base + fee) / (1 - (1 - equity_pct) * k)
            tpc = base + fee + k * loan
            for u, x in per:
                t["fees"].append({"label": u["label"], "amount": x * loan, "rule_path": None, "basis": u.get("basis", "")})
            yrs = int(vals["hud_amort_years"])
            ds = payment(loan, vals["hud_rate"], yrs) + loan * vals["hud_mip_annual"]
            t["tranches"].append({"label": "HUD 232 insured mortgage", "lender": "HUD-approved lender (FHA-insured)",
                                  "amount": loan, "rate": vals["hud_rate"], "years": yrs, "rule_path": None, "ds": ds,
                                  "mip": vals["hud_mip_annual"]})
            if fee:
                t["fees"].append({"label": "HUD financing and MIP fees (added to project cost)", "amount": fee, "rule_path": None})
            t["loan_total"] = loan
            t["cap_amount"] = loan
        t["tpc"] = tpc
        t["equity"] = tpc - t["loan_total"]
        t["ds"] = sum(x["ds"] for x in t["tranches"])
        return t

    # -- tests
    def dscr_series(self, years, ds):
        return [y["noi"] / ds if ds else None for y in years]

    def historical_dscr(self, ds):
        h = self.spec["historical"]
        vals = [x["value"] for x in h["ebitda"]]
        basis = h.get("use", "last")
        e = vals[-1] if basis == "last" else sum(vals[-2:]) / 2
        return e / ds if ds else None, e

    def test_dscr(self, years, t, rules):
        if rules["test"] == "historical":
            d, _ = self.historical_dscr(t["ds"])
            return d
        return self.dscr_series(years, t["ds"])[rules["test_year"] - 1]

    def evaluate_structure(self, vals, uses, years, t, rules, debenture_cap=True):
        tests = []
        tests.append({"key": "equity", "ok": t["equity_pct"] + 1e-9 >= rules["equity_req"]})
        if self.program == "sba_504":
            raw_deb = t["cap_amount"]
            tests.append({"key": "cap", "ok": raw_deb <= rules["cap"] + 0.5 if not debenture_cap else t["debenture"] <= rules["cap"] + 0.5,
                          "value": raw_deb})
        elif rules.get("cap"):
            tests.append({"key": "cap", "ok": t["loan_total"] <= rules["cap"] + 0.5, "value": t["loan_total"]})
        d = self.test_dscr(years, t, rules)
        tests.append({"key": "dscr", "ok": d is not None and d >= rules["floor"], "value": d})
        return tests

    def solve_equity_for_floor(self, vals, uses, years, rules, lo):
        """Smallest equity share (at or above lo) whose test DSCR meets the floor."""
        def ok(e):
            t = self.finance(vals, uses, e, rules)
            d = self.test_dscr(self.operate(vals, t["tpc"]), t, rules)
            return d is not None and d >= rules["floor"]
        if ok(lo):
            return lo
        hi = 0.999
        if not ok(hi):
            return None
        for _ in range(60):
            mid = (lo + hi) / 2
            if ok(mid):
                hi = mid
            else:
                lo = mid
        return math.ceil(hi * 1000) / 1000.0

    # -- run
    def run(self, overrides=None, structure_equity=None):
        vals = self.inputs(overrides)
        uses = self.uses(vals)
        rules = self.rules()
        base = sum(u["amount"] for u in uses)
        prop = self.spec["proposed"]
        prop_eq = prop["equity_pct"]
        t0 = self.finance(vals, uses, prop_eq, rules, debenture_cap=False)
        years = self.operate(vals, t0["tpc"])
        prop_tests = self.evaluate_structure(vals, uses, years, t0, rules, debenture_cap=False)
        if structure_equity is not None:
            r_eq = structure_equity
        else:
            r_eq = max(prop_eq, rules["equity_req"])
            if self.program == "sba_7a":
                t = self.finance(vals, uses, r_eq, rules)
                if t["loan_total"] > rules["cap"]:
                    r_eq = 1 - rules["cap"] / t["tpc"]
            solved = self.solve_equity_for_floor(vals, uses, years, rules, r_eq)
            r_eq = solved if solved is not None else r_eq
        t1 = self.finance(vals, uses, r_eq, rules)
        years1 = self.operate(vals, t1["tpc"])
        res_tests = self.evaluate_structure(vals, uses, years1, t1, rules)
        return {"vals": vals, "uses": uses, "base": base, "rules": rules, "proposed": t0, "restructured": t1,
                "years": years1, "years_proposed": years, "prop_tests": prop_tests, "res_tests": res_tests,
                "restructured_needed": not all(x["ok"] for x in prop_tests)}

    # -- break-even and sensitivity on the restructured structure
    def breakeven(self, base_run):
        spec = self.spec["breakeven"]
        name = spec["input"]
        year = int(spec.get("year", self.spec.get("stabilized_year", 3)))
        eq = base_run["restructured"]["equity_pct"]
        ds = base_run["restructured"]["ds"]
        floor = base_run["rules"]["floor"]

        def noi_at(m):
            r = self.run({name: m}, structure_equity=eq)
            return r["years"][year - 1]["noi"]

        def solve(target):
            lo, hi = 0.0, 3.0
            if noi_at(hi) < target:
                return None
            for _ in range(60):
                mid = (lo + hi) / 2
                if noi_at(mid) >= target:
                    hi = mid
                else:
                    lo = mid
            return hi
        m1 = solve(ds)
        mf = solve(ds * floor)
        v = self.spec["inputs"][name]["value"]
        base_v = v[year - 1] if isinstance(v, list) else v
        return {"input": name, "label": spec.get("label", self.spec["inputs"][name].get("label", name)),
                "fmt": self.spec["inputs"][name].get("fmt", "n"), "year": year, "base": base_v,
                "m_breakeven": m1, "m_floor": mf, "floor": floor, "ds": ds}

    def sensitivity(self, base_run):
        spec = self.spec["sensitivity"]
        year = int(spec.get("year", self.spec.get("stabilized_year", 3)))
        eq = base_run["restructured"]["equity_pct"]
        rows, cols = spec["rows"], spec["cols"]
        grid = []
        for rs in rows["steps"]:
            line = []
            for cs in cols["steps"]:
                r = self.run({rows["input"]: 1 + rs, cols["input"]: 1 + cs}, structure_equity=eq)
                line.append(r["years"][year - 1]["noi"] / r["restructured"]["ds"])
            grid.append(line)
        return {"year": year, "rows": rows, "cols": cols, "grid": grid, "floor": base_run["rules"]["floor"]}


# ------------------------------------------------------------------ rendering

class Renderer:
    def __init__(self, case, nsources):
        self.c = case
        self.n = nsources
        self.run = case.run()
        self.be = case.breakeven(self.run)
        self.sens = case.sensitivity(self.run)
        self.values = self.make_values()

    def cites(self, text):
        def sub(m):
            nums = [int(x) for x in re.split(r"\s*,\s*", m.group(1))]
            for k in nums:
                if not 1 <= k <= self.n:
                    raise ModelError(f"{self.c.slug}: citation [^{k}] has no source on the page ({self.n} sources)")
            return "".join(f'<a class="cite" href="#s{k}">[{k}]</a>' for k in nums)
        return CITE.sub(sub, text)

    def src(self, nums):
        nums = nums if isinstance(nums, list) else [nums]
        return self.cites("[^" + ",".join(str(x) for x in nums) + "]")

    def rule_cite(self, kind):
        rs = self.c.spec.get("rule_sources", {})
        if kind not in rs:
            raise ModelError(f"{self.c.slug}: rule_sources lacks '{kind}'")
        return self.src(rs[kind])

    def input_basis(self, name):
        inp = self.c.spec["inputs"][name]
        if inp.get("source"):
            return "Source " + self.src(inp["source"])
        return "Assumption: " + self.cites(esc(inp["assumption"]))

    def fmt_in(self, name, year=None):
        inp = self.c.spec["inputs"][name]
        v = inp["value"]
        if isinstance(v, list) and year is not None:
            v = v[year - 1]
        return fmt_value(v, inp.get("fmt", "n"))

    # -- values for prose
    def make_values(self):
        r, c = self.run, self.c
        t0, t1 = r["proposed"], r["restructured"]
        v = {"tpc": fmt_money(t1["tpc"]), "tpc_proposed": fmt_money(t0["tpc"]), "uses_base": fmt_money(r["base"]),
             "equity_req_pct": fmt_pct(r["rules"]["equity_req"]), "floor": fmt_x(r["rules"]["floor"]),
             "equity_proposed_pct": fmt_pct(t0["equity_pct"]), "equity_proposed": fmt_money(t0["equity"]),
             "equity_pct": fmt_pct(t1["equity_pct"]), "equity": fmt_money(t1["equity"]),
             "loan_total": fmt_money(t1["loan_total"]), "loan_total_proposed": fmt_money(t0["loan_total"]),
             "ds": fmt_money(t1["ds"]), "ds_proposed": fmt_money(t0["ds"]),
             "rate": fmt_pct(t1["tranches"][0]["rate"], 2),
             "breakeven_pct": fmt_pct(self.be["m_breakeven"]) if self.be["m_breakeven"] else "n/a",
             "breakeven_floor_pct": fmt_pct(self.be["m_floor"]) if self.be["m_floor"] else "n/a",
             "breakeven_value": fmt_value(self.be["base"] * self.be["m_breakeven"], self.be["fmt"]) if self.be["m_breakeven"] else "n/a",
             "breakeven_floor_value": fmt_value(self.be["base"] * self.be["m_floor"], self.be["fmt"]) if self.be["m_floor"] else "n/a",
             "cushion_pct": fmt_pct(1 - self.be["m_breakeven"]) if self.be["m_breakeven"] else "n/a",
             "test_year": str(r["rules"].get("test_year", "")),
             "verdict_proposed": "meets" if not r["restructured_needed"] else "fails"}
        if c.program == "sba_504":
            v.update({"debenture": fmt_money(t1["debenture"]), "tpl": fmt_money(t1["tpl"]),
                      "debenture_proposed": fmt_money(t0["debenture"]), "tpl_proposed": fmt_money(t0["tpl"]),
                      "cap": fmt_money(r["rules"]["cap"]),
                      "debenture_position": "at the program limit" if t1["debenture"] >= r["rules"]["cap"] - 1 else "under the program limit",
                      "tpl_share": fmt_pct(t1["tpl"] / t1["tpc"])})
        elif r["rules"].get("cap"):
            v["cap"] = fmt_money(r["rules"]["cap"])
        for i, y in enumerate(r["years"], 1):
            v[f"rev_y{i}"] = fmt_money(y["rev_total"])
            v[f"noi_y{i}"] = fmt_money(y["noi"])
            v[f"opex_y{i}"] = fmt_money(y["opex_total"])
            v[f"gp_y{i}"] = fmt_money(y["gp_total"])
            v[f"dscr_y{i}"] = fmt_x(y["noi"] / t1["ds"])
            v[f"noi_margin_y{i}"] = fmt_pct(y["noi"] / y["rev_total"]) if y["rev_total"] else "n/a"
        for i, y in enumerate(r["years_proposed"], 1):
            v[f"dscr_y{i}_proposed"] = fmt_x(y["noi"] / t0["ds"])
        if c.spec.get("historical"):
            d1, e = c.historical_dscr(t1["ds"])
            d0, _ = c.historical_dscr(t0["ds"])
            v.update({"hist_ebitda": fmt_money(e), "hist_dscr": fmt_x(d1), "hist_dscr_proposed": fmt_x(d0)})
        if "hud_max_ltv" in r["vals"]:
            ltv = r["vals"]["hud_max_ltv"]
            v["value_needed"] = fmt_money(t1["loan_total"] / ltv)
            v["value_needed_pct"] = fmt_pct(t1["loan_total"] / ltv / t1["tpc"])
            v["value_needed_proposed"] = fmt_money(t0["loan_total"] / ltv)
            v["value_needed_pct_proposed"] = fmt_pct(t0["loan_total"] / ltv / t0["tpc"])
        units = c.spec.get("units")
        if units:
            v["tpc_per_unit"] = fmt_money(t1["tpc"] / units["count"])
            v["units"] = fmt_num(units["count"])
        for name in c.spec["inputs"]:
            v["in_" + name] = self.fmt_in(name, c.spec.get("stabilized_year", 3))
        v["sens_min"] = fmt_x(min(min(row) for row in self.sens["grid"]))
        v["sens_max"] = fmt_x(max(max(row) for row in self.sens["grid"]))
        return v

    # -- table helpers
    @staticmethod
    def table(head, rows, cls="data", foot=None):
        th = "".join(f'<th scope="col">{h}</th>' for h in head)
        body = []
        for row in rows:
            rc = ""
            if isinstance(row, dict):
                rc = f' class="{row["cls"]}"'
                row = row["cells"]
            body.append(f"<tr{rc}>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>")
        out = (f'<div class="data-table-wrap">\n        <table class="{cls}">\n          <thead><tr>{th}</tr></thead>\n'
               f"          <tbody>\n            " + "\n            ".join(body) + "\n          </tbody>\n        </table>\n      </div>")
        if foot:
            out += f'\n      <p class="table-source">{foot}</p>'
        return out

    def check_glance(self):
        """The glance rows are typed text; refuse any that contradict the computed tests or the break-even."""
        passes = all(x["ok"] for x in self.run["res_tests"])
        det = " ".join(t for l, t in self.c.spec["glance"] if l.lower().startswith("determination"))
        if not det:
            raise ModelError(f"{self.c.slug}: glance has no Determination row")
        says_pass = re.search(r"\bmeets (all|every|it\b)", det, re.I) or re.search(r"(^|[.;] *)Meets:", det)
        says_fail = re.search(r"does not support|still fails", det, re.I)
        if not passes and (says_pass or not says_fail):
            raise ModelError(f"{self.c.slug}: the restructured structure fails a test but the glance Determination does not say so")
        if passes and says_fail:
            raise ModelError(f"{self.c.slug}: the restructured structure passes but the glance Determination says it fails")
        m = self.be["m_breakeven"]
        if m is None or m > 1:
            for label, text in self.c.spec["glance"]:
                if re.search(r"\{cushion_pct\}|cushion|below (the )?(plan|underwritten)|covered down to|\bmargin\b", text, re.I):
                    raise ModelError(f"{self.c.slug}: glance row '{label}' reads as a cushion, but break-even is above plan or not reached")

    def card(self, text):
        """The case's card summary on /case-studies/, filled from the model; no citations, no contradiction."""
        passes = all(x["ok"] for x in self.run["res_tests"])
        says_fail = re.search(r"does not support", text, re.I)
        if passes == bool(says_fail):
            raise ModelError(f"{self.c.slug}: card wording contradicts the determination")
        if CITE.search(text):
            raise ModelError(f"{self.c.slug}: card carries a citation")
        return esc(re.sub(r"\{([a-z0-9_]+)\}", lambda m: self.values[m.group(1)], text))

    def t_glance(self):
        self.check_glance()
        rows = []
        for label, text in self.c.spec["glance"]:
            filled = re.sub(r"\{([a-z0-9_]+)\}", lambda m: self.values[m.group(1)], text)
            rows.append([esc(label), self.cites(filled)])
        return self.table(["Item", "Finding"], rows, "data glance")

    def t_inputs(self):
        rows = []
        for name, inp in self.c.spec["inputs"].items():
            rows.append([esc(inp.get("label", name)), self.fmt_in(name), self.input_basis(name)])
        return self.table(["Input", "Value", "Basis"], rows, "data")

    def _lines(self, key, spec_key, years, cls):
        rows = []
        for i, line in enumerate(self.c.spec.get(spec_key, [])):
            vals = [years[y][key][i] for y in (0, 2, 4)]
            rows.append([esc(line["label"]), self.cites(esc(line.get("basis", ""))) if line.get("basis") else ""] + [fmt_money(x) for x in vals])
        return rows

    def t_revenue(self):
        ys = self.run["years"]
        rows = self._lines("revenue", "revenue", ys, "")
        rows.append({"cls": "total", "cells": ["Total revenue", ""] + [fmt_money(ys[y]["rev_total"]) for y in (0, 2, 4)]})
        if self.c.spec.get("cost_of_sales"):
            rows += self._lines("cos", "cost_of_sales", ys, "")
            rows.append({"cls": "total", "cells": ["Gross profit", ""] + [fmt_money(ys[y]["gp_total"]) for y in (0, 2, 4)]})
        return self.table(["Line", "Basis", "Year 1", "Year 3", "Year 5"], rows, "data num wide")

    def t_opex(self):
        ys = self.run["years"]
        rows = self._lines("opex", "opex", ys, "")
        rows.append({"cls": "total", "cells": ["Total operating expenses", ""] + [fmt_money(ys[y]["opex_total"]) for y in (0, 2, 4)]})
        rows.append({"cls": "total", "cells": ["Net operating income", ""] + [fmt_money(ys[y]["noi"]) for y in (0, 2, 4)]})
        return self.table(["Line", "Basis", "Year 1", "Year 3", "Year 5"], rows, "data num wide")

    def t_uses(self):
        t1 = self.run["restructured"]
        rows = []
        for u in self.run["uses"]:
            basis = self.cites(esc(u["basis"])) if u["basis"] else ""
            rows.append([esc(u["label"]), basis, fmt_money(u["amount"]), fmt_pct(u["amount"] / t1["tpc"])])
        for f in t1["fees"]:
            if f["amount"] or f["rule_path"]:
                if "basis" in f:
                    basis = self.cites(esc(f["basis"])) if f["basis"] else ""
                else:
                    basis = self.rule_cite("fees") if f["rule_path"] else self.rule_cite("program")
                rows.append([esc(f["label"]), basis, fmt_money(f["amount"]), fmt_pct(f["amount"] / t1["tpc"])])
        rows.append({"cls": "total", "cells": ["Total project cost", "", fmt_money(t1["tpc"]), "100.0%"]})
        return self.table(["Use of funds", "Basis", "Amount", "Share"], rows, "data num wide")

    def t_sources(self):
        t0, t1 = self.run["proposed"], self.run["restructured"]
        rows = []
        for a, b in zip(t0["tranches"], t1["tranches"]):
            rows.append([esc(b["label"]), fmt_money(a["amount"]), fmt_pct(a["amount"] / t0["tpc"]),
                         fmt_money(b["amount"]), fmt_pct(b["amount"] / t1["tpc"])])
        rows.append(["Sponsor equity", fmt_money(t0["equity"]), fmt_pct(t0["equity"] / t0["tpc"]),
                     fmt_money(t1["equity"]), fmt_pct(t1["equity"] / t1["tpc"])])
        rows.append({"cls": "total", "cells": ["Total sources", fmt_money(t0["tpc"]), "100.0%", fmt_money(t1["tpc"]), "100.0%"]})
        return self.table(["Source of funds", "As proposed", "Share", "As restructured", "Share"], rows, "data num wide")

    def rule_text(self, path):
        sba = self.c.sba
        if path is None:
            return self.rule_cite("program")
        n = sba.node(path)
        val = n["value"] if isinstance(n, dict) and "value" in n else n
        if isinstance(val, list):
            val = "; ".join(" ".join(map(str, x)) if isinstance(x, list) else str(x) for x in val)
        return esc(f"{sba.val('sop.short')}: {val}") + " " + self.rule_cite("sop")

    def t_loan(self):
        t1 = self.run["restructured"]
        rows = []
        for tr in t1["tranches"]:
            rate = fmt_pct(tr["rate"], 2) + (f" plus {fmt_pct(tr['mip'], 2)} MIP" if tr.get("mip") else "")
            rows.append([esc(tr["label"]), esc(tr["lender"]), fmt_money(tr["amount"]), rate, f"{tr['years']} years", fmt_money(tr["ds"])])
        rows.append({"cls": "total", "cells": ["Total debt", "", fmt_money(t1["loan_total"]), "", "", fmt_money(t1["ds"])]})
        out = self.table(["Tranche", "Lender", "Amount", "Rate", "Amortization", "Annual debt service"], rows, "data num wide")
        notes = []
        p = self.c.program
        if p == "sba_7a":
            if t1.get("rate_basis") == "prime_plus_max":
                notes.append(f"Rate: Prime of {self.c.sba.val('rates.prime')} {self.rule_cite('prime')} plus the maximum variable-rate spread SBA allows for this loan size {self.rule_cite('sop')}, held for the full term; a fixed-rate loan has its own, separate maximum, and a lender may price lower.")
            else:
                notes.append("Rate: " + self.input_basis("rate_7a") + ".")
            notes.append(f"Guaranty: {fmt_pct(self.run['vals']['sba_guaranty_pct'], 0)} of the loan, " + self.input_basis("sba_guaranty_pct") + ".")
        elif p == "sba_504":
            notes.append("Bank rate: " + self.input_basis("tpl_rate") + ". Debenture rate: " + self.input_basis("debenture_rate") + ".")
        elif p == "usda_bi":
            notes.append("Rate: " + self.input_basis("bi_rate") + ". Guarantee: " + self.input_basis("bi_guarantee_pct") + ". Term: " + self.input_basis("bi_amort_years") + ".")
        elif p == "hud_232":
            notes.append("Rate: " + self.input_basis("hud_rate") + ". MIP: " + self.input_basis("hud_mip_annual") + ". Term: " + self.input_basis("hud_amort_years") + ".")
        return out + '\n      <p class="table-source">' + " ".join(notes) + "</p>"

    def t_proforma(self):
        ys = self.run["years"]
        t1 = self.run["restructured"]
        cols = ["Line"] + [f"Year {i}" for i in range(1, YEARS + 1)]
        rows = []
        for i, line in enumerate(self.c.spec["revenue"]):
            rows.append([esc(line["label"])] + [fmt_money(y["revenue"][i]) for y in ys])
        rows.append({"cls": "total", "cells": ["Total revenue"] + [fmt_money(y["rev_total"]) for y in ys]})
        if self.c.spec.get("cost_of_sales"):
            for i, line in enumerate(self.c.spec["cost_of_sales"]):
                rows.append([esc(line["label"])] + [fmt_money(-y["cos"][i]) for y in ys])
            rows.append({"cls": "total", "cells": ["Gross profit"] + [fmt_money(y["gp_total"]) for y in ys]})
        for i, line in enumerate(self.c.spec["opex"]):
            rows.append([esc(line["label"])] + [fmt_money(-y["opex"][i]) for y in ys])
        rows.append({"cls": "total", "cells": ["Net operating income"] + [fmt_money(y["noi"]) for y in ys]})
        rows.append(["Debt service (as restructured)"] + [fmt_money(-t1["ds"]) for _ in ys])
        rows.append({"cls": "total", "cells": ["Cash flow after debt service"] + [fmt_money(y["noi"] - t1["ds"]) for y in ys]})
        rows.append(["DSCR"] + [fmt_x(y["noi"] / t1["ds"]) for y in ys])
        return self.table(cols, rows, "data num wide")

    def t_dscr(self):
        r = self.run
        t0, t1, floor = r["proposed"], r["restructured"], r["rules"]["floor"]
        rows = []
        for i in range(YEARS):
            n0, n1 = r["years_proposed"][i]["noi"], r["years"][i]["noi"]
            d0, d1 = n0 / t0["ds"], n1 / t1["ds"]
            mark = " (test year)" if r["rules"]["test"] == "projected" and r["rules"]["test_year"] == i + 1 else ""
            rows.append([f"Year {i + 1}{mark}", fmt_money(n1), fmt_money(t0["ds"]), fmt_x(d0), fmt_money(t1["ds"]), fmt_x(d1), fmt_x(floor)])
        out = self.table(["Year", "NOI", "Debt service, proposed", "DSCR, proposed", "Debt service, restructured", "DSCR, restructured", "Floor"], rows, "data num wide")
        if r["rules"]["test"] == "historical":
            h = self.c.spec["historical"]
            hrows = [[esc(x["label"]) + " (illustrative)", fmt_money(x["value"])] for x in h["ebitda"]]
            d0, e = self.c.historical_dscr(t0["ds"])
            d1, _ = self.c.historical_dscr(t1["ds"])
            basis = "last fiscal year" if h.get("use", "last") == "last" else "average of the last two fiscal years"
            hrows.append({"cls": "total", "cells": [f"Historical EBITDA tested ({basis})", fmt_money(e)]})
            hrows.append([f"DSCR on historical EBITDA, as proposed", fmt_x(d0)])
            hrows.append([f"DSCR on historical EBITDA, as restructured", fmt_x(d1)])
            hrows.append(["Floor for an initial acquisition", fmt_x(floor)])
            out += "\n      " + self.table(["Seller's trailing results", "Amount"], hrows, "data num")
        return out

    def test_rows(self):
        r = self.run
        rules = r["rules"]
        names = {"equity": "Equity injection", "cap": "Program size limit", "dscr": "Debt service coverage"}
        rows = []
        for a, b in zip(r["prop_tests"], r["res_tests"]):
            k = a["key"]
            if k == "equity":
                if self.c.program.startswith("sba"):
                    rule = self.rule_text(rules["equity_path"])
                elif self.c.program == "usda_bi":
                    rule = esc(f"Minimum equity {fmt_pct(rules['equity_req'])}") + " " + self.input_basis("bi_equity_min_pct")
                else:
                    rule = esc(f"Maximum loan-to-cost {fmt_pct(1 - rules['equity_req'])}") + " " + self.input_basis("hud_max_ltc")
                pa = f"{fmt_pct(r['proposed']['equity_pct'])} ({'meets' if a['ok'] else 'fails'})"
                pb = f"{fmt_pct(r['restructured']['equity_pct'])} ({'meets' if b['ok'] else 'fails'})"
            elif k == "cap":
                if self.c.program.startswith("sba"):
                    rule = self.rule_text(rules["cap_path"])
                else:
                    rule = esc(f"Maximum loan {fmt_money(rules['cap'])}") + " " + self.input_basis("bi_loan_cap")
                pa = f"{fmt_money(a['value'])} ({'meets' if a['ok'] else 'over the limit'})"
                pb = f"{fmt_money(b['value'] if self.c.program != 'sba_504' else r['restructured']['debenture'])} ({'meets' if b['ok'] else 'over the limit'})"
            else:
                if self.c.program.startswith("sba"):
                    rule = self.rule_text(rules["floor_path"])
                    if rules["test"] == "historical":
                        rule += " " + esc("Basis: " + str(self.c.sba.val("dscr.coo_basis")) + ".")
                    elif self.c.program == "sba_7a":
                        rule += " " + esc("Basis: " + str(self.c.sba.val("dscr.standard_7a_basis")) + ".")
                    else:
                        rule += " " + esc("Basis: " + str(self.c.sba.val("dscr.sba_504_basis")) + ".")
                elif self.c.program == "usda_bi":
                    rule = esc(f"Coverage of {fmt_x(rules['floor'])}") + " " + self.input_basis("bi_dscr_floor")
                else:
                    rule = esc(f"Coverage of {fmt_x(rules['floor'])}") + " " + self.input_basis("hud_dscr_floor")
                where = "historical EBITDA" if rules["test"] == "historical" else f"Year {rules['test_year']}"
                pa = f"{fmt_x(a['value'])} on {where} ({'meets' if a['ok'] else 'fails'})"
                pb = f"{fmt_x(b['value'])} on {where} ({'meets' if b['ok'] else 'fails'})"
            rows.append([names[k], rule, pa, pb])
        return rows

    def t_determination(self):
        return self.table(["Test", "Rule", "As proposed", "As restructured"], self.test_rows(), "data wide")

    def t_verdict(self):
        r = self.run
        t0, t1 = r["proposed"], r["restructured"]
        failed = [x["key"] for x in r["prop_tests"] if not x["ok"]]
        words = {"equity": "the equity injection is below the program minimum", "cap": "the loan exceeds the program size limit",
                 "dscr": "coverage falls below the floor"}
        prop = self.c.spec["proposed"]
        first = (f"<p><strong>As proposed:</strong> {esc(prop.get('note', 'the sponsor proposes'))}, with {fmt_pct(t0['equity_pct'])} equity "
                 f"({fmt_money(t0['equity'])}) and {fmt_money(t0['loan_total'])} of debt. ")
        if failed:
            first += "The structure does not qualify: " + "; ".join(words[k] for k in failed) + ".</p>"
        else:
            first += "The structure meets every test in the table above.</p>"
        if r["restructured_needed"]:
            second = (f"<p><strong>As restructured:</strong> {fmt_pct(t1['equity_pct'])} equity ({fmt_money(t1['equity'])}) and "
                      f"{fmt_money(t1['loan_total'])} of debt with {fmt_money(t1['ds'])} of annual debt service. ")
            ok = all(x["ok"] for x in r["res_tests"])
            second += ("Every test is met.</p>" if ok else "The project still fails at least one test; the market does not support this loan.</p>")
        else:
            second = "<p><strong>As restructured:</strong> no restructuring is needed; the proposed structure stands.</p>"
        return f'<div class="verdict">\n        {first}\n        {second}\n      </div>'

    def t_breakeven(self):
        be = self.be
        f = be["fmt"]
        rows = [[esc(f"Underwritten {be['label']}, Year {be['year']}"), fmt_value(be["base"], f)],
                ["Annual debt service (as restructured)", fmt_money(be["ds"])]]
        if be["m_breakeven"]:
            rows.append([esc(f"{be['label'].capitalize()} at which NOI equals debt service (1.00x)"),
                         f"{fmt_value(be['base'] * be['m_breakeven'], f)} ({fmt_pct(be['m_breakeven'])} of underwritten)"])
            rows.append(["Cushion before cash break-even", fmt_pct(1 - be["m_breakeven"])])
        if be["m_floor"]:
            rows.append([esc(f"{be['label'].capitalize()} at which coverage equals the {fmt_x(be['floor'])} floor"),
                         f"{fmt_value(be['base'] * be['m_floor'], f)} ({fmt_pct(be['m_floor'])} of underwritten)"])
        return self.table(["Measure", "Value"], rows, "data num")

    def t_sensitivity(self):
        s = self.sens
        floor = s["floor"]
        head = [esc(f"{s['rows']['label']} \\ {s['cols']['label']}")] + [("+" if x > 0 else "") + f"{x * 100:.0f}%" for x in s["cols"]["steps"]]
        th = "".join(f'<th scope="col">{h}</th>' for h in head)
        body = []
        for i, rs in enumerate(s["rows"]["steps"]):
            cells = [f"<td>{('+' if rs > 0 else '')}{rs * 100:.0f}%</td>"]
            for j, cs in enumerate(s["cols"]["steps"]):
                d = s["grid"][i][j]
                cls = "pass" if d >= floor else ("thin" if d >= 1.0 else "fail")
                if rs == 0 and cs == 0:
                    cls += " base"
                cells.append(f'<td class="{cls}">{fmt_x(d)}</td>')
            body.append("<tr>" + "".join(cells) + "</tr>")
        cap = (f"DSCR in Year {s['year']} on the restructured loan. Rows change {esc(s['rows']['label'].lower())}; "
               f"columns change {esc(s['cols']['label'].lower())}. Green meets the {fmt_x(floor)} floor, amber covers debt service "
               f"but misses the floor, red does not cover debt service. The outlined cell is the underwritten case.")
        return (f'<div class="data-table-wrap">\n        <table class="data matrix">\n          <thead><tr>{th}</tr></thead>\n'
                f"          <tbody>\n            " + "\n            ".join(body) + "\n          </tbody>\n        </table>\n      </div>\n"
                f'      <p class="table-source">{cap}</p>')

    def region(self, name):
        if name.startswith("v."):
            key = name[2:]
            if key not in self.values:
                raise ModelError(f"{self.c.slug}: unknown value v.{key}")
            return esc(self.values[key])
        fn = getattr(self, "t_" + name, None)
        if fn is None:
            raise ModelError(f"{self.c.slug}: unknown table {name}")
        return fn()


# ------------------------------------------------------------------ pages

def load_sba():
    return SBA(json.load(open(SBA_FILE, encoding="utf-8")))


def case_files():
    return sorted(os.path.join(CASES, f) for f in os.listdir(CASES) if f.endswith(".json"))


def page_file(case):
    return os.path.join(ROOT, case.spec["page"].strip("/"), "index.html")


def nsources(text):
    m = re.search(r'<ol class="sources">(.*?)</ol>', text, re.S)
    return len(re.findall(r"<li id=\"s\d+\"", m.group(1))) if m else 0


def process(case, check):
    path = page_file(case)
    if not os.path.exists(path):
        return [f"{case.slug}: page {case.spec['page']} not built yet"], False
    text = open(path, encoding="utf-8").read()
    rnd = Renderer(case, nsources(text))
    problems, changed = [], False
    m_be = rnd.be["m_breakeven"]
    if (m_be is None or m_be > 1) and f"<!--case:{case.slug}.v.cushion_pct-->" in text:
        problems.append(f"{case.slug}: the page shows a break-even cushion, but break-even is above plan or not reached")

    def sub(m):
        nonlocal changed
        slug, name, inner = m.group(1), m.group(2), m.group(3)
        if slug != case.slug:
            problems.append(f"{case.slug}: region for another case {slug}.{name}")
            return m.group(0)
        new = rnd.region(name)
        if new != inner:
            changed = True
            if check:
                problems.append(f"{case.slug}: stale region {name}")
        return f"<!--case:{slug}.{name}-->{new}<!--/case:{slug}.{name}-->"
    out = REGION.sub(sub, text)
    if not check and changed:
        open(path, "w", encoding="utf-8").write(out)
    return problems, changed


def process_index(cases, check):
    """Fill the factory cases' card regions on /case-studies/ from src/case-cards.json."""
    cards = {k: v for k, v in json.load(open(CARDS, encoding="utf-8")).items() if not k.startswith("_")}
    text = open(INDEX, encoding="utf-8").read()
    problems, changed = [], False
    for slug, tmpl in cards.items():
        case = cases.get(slug)
        if case is None:
            problems.append(f"case-cards: no case {slug}")
            continue
        pat = re.compile(r"(<!--case:%s\.card-->)(.*?)(<!--/case:%s\.card-->)" % (re.escape(slug), re.escape(slug)), re.S)
        found = pat.findall(text)
        if len(found) != 1:
            problems.append(f"case-studies/index.html: {len(found)} card regions for {slug}, expected 1")
            continue
        page = page_file(case)
        rnd = Renderer(case, nsources(open(page, encoding="utf-8").read()) if os.path.exists(page) else 0)
        new = rnd.card(tmpl)
        if found[0][1] != new:
            changed = True
            if check:
                problems.append(f"case-studies/index.html: stale card {slug}")
            text = pat.sub(lambda m: m.group(1) + new + m.group(3), text)
    for slug in set(re.findall(r"<!--case:([a-z0-9-]+)\.card-->", text)) - set(cards):
        problems.append(f"case-studies/index.html: card region for {slug} has no template")
    if changed and not check:
        open(INDEX, "w", encoding="utf-8").write(text)
    return problems, changed


# ------------------------------------------------------------------ returns on hand-built case pages

def balance(principal, rate, years, months):
    """Loan balance after a number of level monthly payments."""
    r = rate / 12.0
    pmt = payment(principal, rate, years) / 12.0
    if r == 0:
        return principal - pmt * months
    return principal * (1 + r) ** months - pmt * ((1 + r) ** months - 1) / r


def irr(cfs):
    f = lambda r: sum(c / (1 + r) ** i for i, c in enumerate(cfs))
    lo, hi = -0.95, 10.0
    if f(lo) * f(hi) > 0:
        raise ModelError("IRR has no root in range")
    for _ in range(300):
        mid = (lo + hi) / 2
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def levered_irr(spec):
    """Levered equity IRR: hold the stabilized NOI, sell at the exit cap less selling costs, repay both balances."""
    v = {k: x["value"] for k, x in spec["inputs"].items()}
    cost = v["cost"]
    bank, deb, eq = cost * v["bank_pct"], cost * v["debenture_pct"], cost * v["equity_pct"]
    if abs(v["bank_pct"] + v["debenture_pct"] + v["equity_pct"] - 1) > 1e-9:
        raise ModelError(f"{spec['slug']}: capital stack does not sum to 100%")
    ds = payment(bank, v["bank_rate"], v["bank_years"]) + payment(deb, v["debenture_rate"], v["debenture_years"])
    hold = int(v["hold_years"])
    noi = list(v["noi"]) + [v["noi"][-1]] * (hold - len(v["noi"]))
    cfs = [-eq]
    for t, n in enumerate(noi, start=1):
        d = n - ds
        if t == 1 and spec.get("year1_shortfall_from_reserve"):
            d = max(d, 0.0)
        cfs.append(d)
    bal = balance(bank, v["bank_rate"], v["bank_years"], 12 * hold) + balance(deb, v["debenture_rate"], v["debenture_years"], 12 * hold)
    cfs[-1] += v["noi"][-1] / v["exit_cap"] * (1 - v["selling_cost"]) - bal
    return {"irr": irr(cfs), "values": {
        "irr_pct": f"{round(irr(cfs) * 100):.0f}",
        "exit_cap_pct": f"{v['exit_cap'] * 100:.1f}".rstrip("0").rstrip("."),
        "selling_pct": f"{v['selling_cost'] * 100:.1f}".rstrip("0").rstrip("."),
        "hold_years": str(hold)}}


def process_returns(check):
    problems, written = [], []
    if not os.path.isdir(RETURNS):
        return problems, written
    for f in sorted(x for x in os.listdir(RETURNS) if x.endswith(".json")):
        spec = json.load(open(os.path.join(RETURNS, f), encoding="utf-8"))
        slug = spec["slug"]
        path = os.path.join(ROOT, spec["page"].strip("/"), "index.html")
        try:
            vals = levered_irr(spec)["values"]
        except (ModelError, KeyError, ValueError, ZeroDivisionError) as exc:
            problems.append(f"returns {slug}: {type(exc).__name__}: {exc}")
            continue
        text = open(path, encoding="utf-8").read()
        seen, changed = 0, False

        def sub(m):
            nonlocal seen, changed
            if m.group(1) != slug:
                return m.group(0)
            name = m.group(2)
            if not name.startswith("v.") or name[2:] not in vals:
                problems.append(f"returns {slug}: unknown region {name}")
                return m.group(0)
            seen += 1
            new = vals[name[2:]]
            if m.group(3) != new:
                changed = True
                if check:
                    problems.append(f"returns {slug}: stale region {name}")
            return f"<!--case:{slug}.{name}-->{new}<!--/case:{slug}.{name}-->"
        out = REGION.sub(sub, text)
        # every place a reader or a search engine can read an IRR: body text outside the computed regions, meta content, JSON-LD
        noregion = re.sub(r"<!--case:[^>]*-->.*?<!--/case:[^>]*-->", " ", text, flags=re.S)
        meta = " ".join(re.findall(r'<meta\b[^>]*\bcontent="([^"]*)"', noregion))
        ld = " ".join(re.findall(r'<script type="application/ld\+json">(.*?)</script>', noregion, flags=re.S))
        body = re.sub(r"<[^>]+>", " ", re.sub(r"<(script|style)\b.*?</\1>", " ", noregion, flags=re.S))
        bare = re.sub(r"\s+", " ", " ".join([body, meta, ld]))
        irr_words = r"(?:\bIRR\b|internal rate of return|levered (?:equity )?return|equity return)"
        for m in re.finditer(r"\d+(?:\.\d+)?\s?(?:%|percent)[^.]{0,60}" + irr_words + r"|" + irr_words + r"[^.]{0,60}?\d+(?:\.\d+)?\s?(?:%|percent)", bare, re.I):
            problems.append(f"returns {slug}: an IRR figure stated outside the computed regions: ...{m.group(0)[:90]}...")
        if not seen:
            problems.append(f"returns {slug}: the page has no case:{slug}.v.irr_pct region")
        if changed and not check:
            open(path, "w", encoding="utf-8").write(out)
            written.append(f"returns {slug}")
    return problems, written


def dump(case, rnd):
    r = rnd.run
    clean = lambda t: {k: v for k, v in t.items() if k != "tranches"} | {"tranches": t["tranches"]}
    return {"slug": case.slug, "program": case.program, "rules": r["rules"], "uses": r["uses"], "base": r["base"],
            "proposed": clean(r["proposed"]), "restructured": clean(r["restructured"]),
            "years": r["years"], "years_proposed": r["years_proposed"], "prop_tests": r["prop_tests"],
            "res_tests": r["res_tests"], "breakeven": rnd.be, "sensitivity": rnd.sens, "values": rnd.values}


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--case")
    ap.add_argument("--dump")
    ap.add_argument("--only", help="write (or with --check, check) one case only")
    args = ap.parse_args(argv)
    sba = load_sba()
    files = case_files()
    if args.case or args.only:
        files = [os.path.join(CASES, (args.case or args.only) + ".json")]
    problems, written, cases = [], [], {}
    for f in files:
        try:
            case = Case(f, sba)
            cases[case.slug] = case
            if args.case or args.dump:
                p = page_file(case)
                n = nsources(open(p, encoding="utf-8").read()) if os.path.exists(p) else 999
                rnd = Renderer(case, n)
                data = dump(case, rnd)
                if args.dump:
                    os.makedirs(args.dump, exist_ok=True)
                    with open(os.path.join(args.dump, case.slug + ".json"), "w", encoding="utf-8") as fh:
                        json.dump(data, fh, indent=1, sort_keys=True, default=float)
                else:
                    print(json.dumps(data, indent=1, sort_keys=True, default=float))
                continue
            pr, changed = process(case, args.check)
            problems += pr
            if changed and not args.check:
                written.append(case.slug)
        except (ModelError, KeyError, ValueError, ZeroDivisionError) as exc:
            problems.append(f"{os.path.basename(f)}: {type(exc).__name__}: {exc}")
    if args.case or args.dump:
        for p in problems:
            print(p)
        return 1 if problems else 0
    if not args.only:
        pr, wr = process_returns(args.check)
        problems += pr
        written += wr
        try:
            pr, changed = process_index(cases, args.check)
            problems += pr
            if changed and not args.check:
                written.append("case-studies index cards")
        except (ModelError, KeyError, ValueError, ZeroDivisionError) as exc:
            problems.append(f"case-cards: {type(exc).__name__}: {exc}")
    for p in problems:
        print(p)
    if args.check:
        print(f"{len(files)} case(s) checked, {len(problems)} problem(s)")
        return 1 if problems else 0
    for w in written:
        print("wrote", w)
    print(f"{len(files)} case(s), {len(written)} page(s) rewritten, {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
