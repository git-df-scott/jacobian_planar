"""night16 -- C4: controls for EXACT-PRIM (the per-fibre exactness certificate).

EXACT-PRIM must (a) produce a verified certificate exactly when the periods
really do all vanish, and (b) produce none when a period is known nonzero.
The known answers are night15's, from independent instruments.
"""
import json
import sympy as sp
import period16 as PR

x, y = PR.x, PR.y
rows = []
print("=" * 78)
print("C4  EXACT-PRIM CONTROLS  ([P,F] = 1 mod h, verified by exact division)")
print("=" * 78)
CASES = [
    # (name, P, c, expected, why)
    ("x + y^2                (coordinate)", x + y**2, 0, "VANISHING_EXACT",
     "a coordinate; every fibre is C, H_1 = 0"),
    ("x + x^2*y              (classical, ON its atypical fibre)", x + x**2 * y, 0,
     "VANISHING_EXACT", "F_0 = {x=0} u {1+xy=0}: on each piece eta is d(a linear form)"),
    ("x + x^2*y              (generic fibre)", x + x**2 * y, 1, "VANISHING_EXACT",
     "F_c ~ C*, and eta = dy/P_x is exact on it"),
    ("y + x*y^3              (EXACT-G1 n=1,m=3: night15 VANISHING)", y + x * y**3, 1,
     "VANISHING_EXACT", "night15 EXACT-G1 case ii: genus 0, all residues zero"),
    ("y + x^3*y^4            (EXACT-G1 n=3,m=4: night15 VANISHING)", y + x**3 * y**4, 1,
     "VANISHING_EXACT", "night15 EXACT-G1 case ii (the fibre that caught the NUM-MONO bug)"),
    ("y + x^2*y^2            (EXACT-G1 n=2,m=2: night15 NONVANISHING)", y + x**2 * y**2, 1,
     "NO_EXACT_CERTIFICATE", "night15 EXACT-G1 case i: nonzero residues at the places over y=0"),
    ("y + x^2*y^4            (EXACT-G1 n=2,m=4: night15 NONVANISHING)", y + x**2 * y**4, 1,
     "NO_EXACT_CERTIFICATE", "night15 EXACT-G1 case i (n | m); NUM-MONO residue 0.176777"),
    ("y + x^4*y^2            (EXACT-G1 n=4,m=2: night15 NONVANISHING)", y + x**4 * y**2, 1,
     "NO_EXACT_CERTIFICATE", "night15 EXACT-G1 case iii: holomorphic nonzero form, genus 1"),
    ("y + x^5*y^3            (EXACT-G1 n=5,m=3: night15 NONVANISHING)", y + x**5 * y**3, 1,
     "NO_EXACT_CERTIFICATE", "night15 EXACT-G1 case iii, genus 2"),
]
ok = True
for name, P, c, exp, why in CASES:
    r = PR.exact_periods_vanish(P, sp.Integer(c), Dmax=6)
    good = (r["verdict"] == exp)
    ok &= good
    print("  %-58s c=%d" % (name, c))
    print("      got %-22s expected %-22s MATCH %s" % (r["verdict"], exp, good))
    print("      components: %s" % [(cp["h"], "degF=%s" % cp.get("degF") if cp["ok"]
                                     else "none to deg 6") for cp in r["components"]])
    print("      why: %s" % why)
    rows.append({"name": name, "c": c, "got": r["verdict"], "expected": exp,
                 "match": bool(good),
                 "components": [(cp["h"], cp.get("degF"), cp["ok"], cp.get("F"))
                                for cp in r["components"]]})
print()
print("GATE C4: %s" % ("PASS" if ok else "FAIL"))
json.dump({"rows": rows, "pass": bool(ok)}, open("controls16b.json", "w"), indent=1)
