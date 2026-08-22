#!/usr/bin/env python3
"""G4 -- descent-recursion data table for d = 3..10.  NO SOLVING.

Pure sympy extraction from the certified builder wave5/w5_b16_abel.build_system,
in the reduced variables of wave5/w5_b16_reduce (the linear eliminations
a0 = -mu3^2/4, a1 = mu2, b0 = mu3, b1 = 0, mu1 = -mu3*(a2+2*b2)/3).

Recorded per d, from the TOP THREE coefficient rows of (1.3) (the coefficients
of y^{4d}, y^{4d-1}, y^{4d-2}):
  row 0 : the univariate polynomial satisfied by a_{2d}; its coefficient list,
          its discriminant, and its exact roots (listed as data);
  row 1 : the linear coefficient multiplying the next unknown a_{2d-1},
          plus the full linear part of the row in every variable it contains;
  row 2 : the same for a_{2d-2}.

Controls in this file:
  * structural: row 0 must involve a_{2d} and no other unknown; rows 1 and 2
    must be degree 1 in a_{2d-1} resp. a_{2d-2} -- all computed, not asserted;
  * round-trip: for each recorded linear coefficient c and row r in variable v,
    expand(r - c*v) must be free of v;
  * NEGATIVE CONTROL, required to fail: perturbing row 0 by +1 must change both
    the recorded a_{2d} polynomial and its discriminant.
"""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "wave5"))
from w5_b16_abel import build_system, mu0, mu1, mu2, mu3, y
from sympy import symbols, expand, Poly, Rational, discriminant, roots, srepr

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAIL = []

def check(label, cond, note=""):
    print(("PASS " if cond else "FAIL ") + label + (f"   [{note}]" if note else ""))
    if not cond:
        FAIL.append(label)

def reduced_rows(d):
    """The (1.3) coefficient rows in descending y-degree, in reduced variables."""
    eqs, unk, A, q1 = build_system(d)
    a = symbols(f'a0:{2*d+1}'); b = symbols(f'b0:{d}')
    sub = {a[0]: -mu3**2/4, a[1]: mu2, b[0]: mu3, b[1]: 0,
           mu1: -mu3*(a[2] + 2*b[2])/3}
    rows13 = eqs[:-5]                    # build_system: (1.3) rows, then 3x(1.2), then 2 gauge
    return [expand(r.subs(sub)) for r in rows13], a, b

def linear_part(row, var):
    p = Poly(row, var)
    return p.degree(), (p.coeff_monomial(var) if p.degree() >= 1 else 0)

def analyse(d):
    rows, a, b = reduced_rows(d)
    allvars = [v for v in list(a) + list(b) + [mu0, mu1, mu2, mu3]]
    r0, r1, r2 = rows[0], rows[1], rows[2]
    top, nxt1, nxt2 = a[2*d], a[2*d-1], a[2*d-2]

    # --- row 0: univariate in a_{2d} ---
    others = [v for v in allvars if v != top and r0.has(v)]
    check(f"d={d} row0 involves a_{2*d} and no other unknown",
          r0.has(top) and not others, f"others={others}")
    p0 = Poly(r0, top)
    disc = expand(discriminant(p0.as_expr(), top))
    rts = roots(p0.as_expr(), top)

    # --- rows 1 and 2: linear in the next unknown ---
    deg1, c1 = linear_part(r1, nxt1)
    deg2, c2 = linear_part(r2, nxt2)
    check(f"d={d} row1 is degree 1 in a_{2*d-1}", deg1 == 1, f"deg={deg1}")
    check(f"d={d} row2 is degree 1 in a_{2*d-2}", deg2 == 1, f"deg={deg2}")
    check(f"d={d} row1 round-trip: r1 - c1*a_{2*d-1} is free of a_{2*d-1}",
          not expand(r1 - c1*nxt1).has(nxt1))
    check(f"d={d} row2 round-trip: r2 - c2*a_{2*d-2} is free of a_{2*d-2}",
          not expand(r2 - c2*nxt2).has(nxt2))

    def lin_dict(row):
        out = {}
        for v in allvars:
            if not row.has(v):
                continue
            dg, c = linear_part(row, v)
            if dg == 1:
                out[str(v)] = str(c)
        return out

    # --- negative control: perturbing row 0 must change poly AND discriminant ---
    p0b = Poly(expand(r0 + 1), top)
    discb = expand(discriminant(p0b.as_expr(), top))
    check(f"d={d} NEGATIVE CONTROL: perturbed row0 changes the a_{2*d} polynomial",
          p0b.as_expr() != p0.as_expr())
    check(f"d={d} NEGATIVE CONTROL: perturbed row0 changes the discriminant",
          expand(discb - disc) != 0, f"delta={expand(discb-disc)}")

    return {
        "d": d,
        "n_13_rows": len(rows),
        "top_variable": str(top),
        "row0_y_degree": 4*d,
        "row0_polynomial_in_a2d": str(p0.as_expr()),
        "row0_degree_in_a2d": p0.degree(),
        "row0_coeffs_desc_in_a2d": [str(c) for c in p0.all_coeffs()],
        "row0_discriminant": str(disc),
        "row0_roots": {str(k): int(v) for k, v in rts.items()},
        "row1_y_degree": 4*d-1,
        "row1_next_unknown": str(nxt1),
        "row1_linear_coeff_of_next_unknown": str(c1),
        "row1_full_linear_part": lin_dict(r1),
        "row1_polynomial": str(r1),
        "row2_y_degree": 4*d-2,
        "row2_next_unknown": str(nxt2),
        "row2_linear_coeff_of_next_unknown": str(c2),
        "row2_full_linear_part": lin_dict(r2),
        "row2_polynomial": str(r2),
    }

def main(ds):
    table = {}
    for d in ds:
        table[str(d)] = analyse(d)
        print(f"  d={d}: a_{2*d} poly = {table[str(d)]['row0_polynomial_in_a2d']}"
              f"   roots={table[str(d)]['row0_roots']}", flush=True)

    # G4 control at d=5, stated AS DATA: the roots of the recorded a_10 polynomial.
    if "5" in table:
        r5 = table["5"]["row0_roots"]
        print(f"  D=5 CONTROL DATA: roots of the recorded a_10 polynomial = {r5}")
        check("d=5 control: the recorded a_10 polynomial has at least one root recorded",
              len(r5) >= 1, str(r5))
        table["5"]["d5_control_roots_listed"] = r5

    out = os.path.join(REPO, "ggv", "recursion_table.json")
    json.dump({"source_builder": "wave5/w5_b16_abel.py::build_system",
               "reduction": "wave5/w5_b16_reduce.py step 1 linear eliminations",
               "solving_performed": False,
               "rows": table}, open(out, "w"), indent=2, sort_keys=True)
    print("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL))
    return 1 if FAIL else 0

if __name__ == "__main__":
    sys.exit(main([int(x) for x in (sys.argv[1:] or list(map(str, range(3, 11))))]))
