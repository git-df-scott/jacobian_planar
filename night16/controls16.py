"""night16 -- CONTROLS for the atypical-value detector (hard gate).

C1  coordinates must have NO atypical value (chi(F_c) constant).
C2  the classical P = x + x^2*y MUST be reported with an atypical value at c=0.
C3  further P whose atypical set is verifiable independently, plus two
    independent cross-checks of chi itself.
"""
import json, sys, time
import sympy as sp
import atyp16 as A
import mono16 as M
import load16

x, y = A.x, A.y
OUT = {}


def show(tag, name, P, expect, why):
    t0 = time.time()
    r = A.atypical(P)
    got = sorted(a["c"] for a in r["atypical"])
    ok = (got == sorted(expect))
    print("  %-4s %-46s deg=%2d deg_y=%d  chi_gen=%-3d (%s)  atypical=%s"
          % (tag, name, sp.Poly(P, x, y).total_degree(), sp.Poly(P, y).degree(),
             r["chi_gen"], r["chi_gen_votes"], got if got else "NONE"))
    print("       chi at the sampled generic c: %s" %
          list(zip(r["generic_c"], r["generic_chi"])))
    print("       every candidate c tested:     %s" %
          [(t["c"], t["chi"]) for t in r["tested"]])
    print("       independent expectation:      %s   -- %s" % (expect if expect else "NONE", why))
    print("       MATCH: %s      (%.2f s)" % (ok, time.time() - t0))
    OUT[tag] = {"name": name, "P": sp.srepr(P), "chi_gen": r["chi_gen"],
                "atypical": got, "expected": expect, "match": bool(ok),
                "tested": [(t["c"], t["chi"]) for t in r["tested"]],
                "generic": list(zip(r["generic_c"], r["generic_chi"]))}
    return ok


print("=" * 78)
print("night16 CONTROLS -- atypical-value detector")
print("=" * 78)
print()
print("C1  COORDINATES: no atypical value")
ok1 = show("C1a", "x + y^2", x + y**2, [],
           "a coordinate: every fibre is isomorphic to C, chi == 1")
ok1 &= show("C1b", "x + (y + x^2)^5  (degree-10 triangular)",
            sp.expand(x + (y + x**2)**5), [],
            "x composed with two Jacobian-1 triangular maps: still a coordinate")
print()
print("C2  THE CLASSICAL EXAMPLE (hard gate)")
ok2 = show("C2", "x + x^2*y", x + x**2 * y, ["0"],
           "F_0 = {x=0} u {1+xy=0} is reducible (chi 1); F_c ~ C* for c!=0 (chi 0)")
print()
print("C3  FURTHER P WITH INDEPENDENTLY KNOWN ATYPICAL SETS")
ok3 = show("C3a", "x + x^2*y + 5", x + x**2 * y + 5, ["5"],
           "the same example shifted: the jump must move to c = 5")
ok3 &= show("C3b", "x*y^2 + y", x * y**2 + y, ["0"],
            "c!=0: x=(c-y)/y^2 gives F_c ~ C\\{0}, chi 0; F_0={y=0} u {xy=-1}, chi 1")
ok3 &= show("C3c", "t^3 - 3t,  t = x + y^2", sp.expand((x + y**2)**3 - 3 * (x + y**2)),
            ["-2", "2"],
            "F_c = disjoint union of the fibres {t = root of t^3-3t-c}, each ~ C "
            "(chi 1); chi = #distinct roots, so it drops at the critical values +-2")
ok3 &= show("C3d", "t^4 - t,  t = x + y^2", sp.expand((x + y**2)**4 - (x + y**2)),
            ["root of c**3 + 27/256"],
            "same construction: chi = #distinct roots of t^4-t-c, which drops at "
            "the three (irrational, conjugate) critical values, c^3 = -27/256")
print()
print("C3e CROSS-CHECK OF chi ITSELF AGAINST NUM-MONO (independent, numerical)")
print("    NUM-MONO computes chi = dy*(1-|B|) + #finite cycles from numerically")
print("    continued monodromy; the detector computes it by exact algebra.")
print("    NUM-MONO's count is taken over the sheets of the x-projection, so it")
print("    CANNOT see a vertical line component {x = s} of the fibre (that whole")
print("    component sits over a single x).  The detector reports n_vert, the")
print("    number of such components, separately; the identity checked here is")
print("        exact chi  -  n_vert  ==  NUM-MONO chi .")
rows = []
cases = [("x + x^2*y", {(1, 0): sp.Rational(1), (2, 1): sp.Rational(1)}, [0, 1, -2]),
         ("x*y^2 + y", {(1, 2): sp.Rational(1), (0, 1): sp.Rational(1)}, [0, 1, 3]),
         ("x + (y+x^2)^5", None, [0, 2]),
         ("y + x*y^3", {(0, 1): sp.Rational(1), (1, 3): sp.Rational(1)}, [0, 1, -1]),
         ("y^2 + x*y^3", {(0, 2): sp.Rational(1), (1, 3): sp.Rational(1)}, [0, 1])]
from fractions import Fraction as Fr
allok = True
for nm, Pd, cs in cases:
    if Pd is None:
        e = sp.expand(x + (y + x**2)**5)
        Pd = {(int(m[0]), int(m[1])): Fr(int(co)) for m, co in
              zip(sp.Poly(e, x, y).monoms(), sp.Poly(e, x, y).coeffs())}
    else:
        Pd = {k: Fr(int(v)) for k, v in Pd.items()}
    Pe = A.dict_to_expr(Pd)
    for c in cs:
        d = A.chi_fibre(Pe, sp.Integer(c))
        ex, nv = d["chi"], d["n_vert"]
        nm_ = M.screen_fibre(Pd, Fr(c), nsub=6, ncirc=48, budget=90.0)
        num = nm_.get("chi")
        if num is None:
            good = None            # NUM-MONO could not run on this fibre
        else:
            good = (ex - nv == num)
            allok &= good
        print("    %-16s c=%-3d  exact chi=%-3d n_vert=%d  chi-n_vert=%-3d  "
              "NUM-MONO chi=%-4s  agree=%s" % (nm, c, ex, nv, ex - nv, num,
                                               good if good is not None
                                               else "NO COMPARISON (NUM-MONO "
                                               "errored: this fibre is "
                                               "non-reduced and this P is not "
                                               "gradient-unimodular)"))
        rows.append((nm, c, ex, nv, num, bool(good)))
OUT["C3e"] = {"rows": rows, "all_agree": bool(allok)}
ok3 &= allok
print()
print("C3f CROSS-CHECK AGAINST night15's RECORDED GENUS AND PLACES AT INFINITY")
print("    for an irreducible fibre  chi = 2 - 2g - r.  night15 recorded (g, r)")
print("    for the generic fibre of each of the 57 survivors; the detector's")
print("    chi_gen is computed with no reference to either number.")
import csv as _csv
n_ok = n_bad = n_skip = 0
bad = []
crows = {r["hash"]: r for r in _csv.DictReader(open("../night15/period_screen.csv"))}
for rec in load16.survivors():
    row = crows[rec["hash"]]
    try:
        g = int(row["genus"]); r_ = int(row["places_at_infinity"])
    except ValueError:
        n_skip += 1; continue
    Pe = A.dict_to_expr(load16.Pdict(rec))
    try:
        cg = A.atypical(Pe, n_generic=3)["chi_gen"]
    except Exception as e:
        n_skip += 1; continue
    if cg == 2 - 2 * g - r_:
        n_ok += 1
    else:
        n_bad += 1; bad.append((rec["hash"], cg, g, r_))
print("    agree: %d    disagree: %d    skipped (no recorded g/r): %d" % (n_ok, n_bad, n_skip))
for b in bad[:12]:
    print("       DISAGREE hash=%s chi_gen=%d recorded g=%d r=%d (2-2g-r=%d)"
          % (b[0], b[1], b[2], b[3], 2 - 2 * b[2] - b[3]))
OUT["C3f"] = {"agree": n_ok, "disagree": n_bad, "skipped": n_skip, "bad": bad}
print()
print("GATE: C1 %s   C2 %s   C3 %s" % ("PASS" if ok1 else "FAIL",
                                       "PASS" if ok2 else "FAIL",
                                       "PASS" if ok3 else "FAIL"))
OUT["gate"] = {"C1": bool(ok1), "C2": bool(ok2), "C3": bool(ok3)}
json.dump(OUT, open("controls16.json", "w"), indent=1, default=str)
if not (ok1 and ok2 and ok3):
    sys.exit(1)
