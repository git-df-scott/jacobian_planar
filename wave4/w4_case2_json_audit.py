"""
Audit of campaign/audit_tracks/trackA_system_case2.json against the bracket
itself.

Everything in Item 1 rests on this file.  It carries a content hash, but a hash
only says the bytes have not changed -- it says nothing about whether the 92
equations ARE the case-(2) system.  This script checks that directly:

    take the 25 c-variables and 47 d-variables at face value as the supports of
    P and Q (their indices ARE the exponent pairs),
    form  P = sum c_i_j x^i y^j,  Q = sum d_i_j x^i y^j,
    expand  [P, Q] - x^2 = P_x Q_y - P_y Q_x - x^2  symbolically over Q,
    and compare its coefficients, monomial by monomial, with the JSON's
    equations.

If the JSON's equation at bracket point (i,j) is not the coefficient of x^i y^j
in that expansion -- or if a nonzero coefficient has no equation -- the file is
not the system it claims to be, and Item 1's verdict would be about a different
object.

CONTROLS
  J1 POSITIVE: every JSON equation equals its bracket coefficient exactly;
  J2 POSITIVE: every nonzero bracket coefficient has a JSON equation;
  J3 NEGATIVE: perturbing one JSON coefficient breaks J1;
  J4 NEGATIVE: comparing against [Q,P] - x^2 instead of [P,Q] - x^2 breaks J1,
     so the orientation is pinned and not accidental;
  J5 the polygon vertices recorded in the JSON's meta really are vertices of the
     supports (extreme points), and the support sizes match SP_size / SQ_size.
"""
import json
import os
import sys
from fractions import Fraction

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_case2_system as S

x, y = sp.symbols("x y")
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def ij(v):
    _, i, j = v.split("_")
    return int(i), int(j)


def main():
    VARS, NONZERO, EQS, META, CHASH = S.load()
    syms = {v: sp.Symbol(v) for v in VARS}
    cs = [v for v in VARS if v.startswith("c_")]
    ds = [v for v in VARS if v.startswith("d_")]
    print("=" * 78)
    print("audit of trackA_system_case2.json against the bracket [P,Q] - x^2")
    print("=" * 78)
    print(f"    {len(cs)} c-variables, {len(ds)} d-variables, {len(EQS)} equations")
    print(f"    meta: SP_size {META['SP_size']}, SQ_size {META['SQ_size']}, "
          f"bracket_rhs {META['bracket_rhs']!r}")

    check("J5a the c-support size matches the meta's SP_size",
          len(cs) == META["SP_size"], f"{len(cs)} vs {META['SP_size']}")
    check("J5b the d-support size matches the meta's SQ_size",
          len(ds) == META["SQ_size"], f"{len(ds)} vs {META['SQ_size']}")

    from itertools import combinations
    def is_vertex(pt, pts):
        # a lattice point is a vertex of the hull iff it is not a convex
        # combination of the others; tested by a small LP-free argument: it is a
        # vertex iff some linear functional is uniquely maximised there
        import random
        rnd = random.Random(1)
        for _ in range(4000):
            a, b = rnd.uniform(-1, 1), rnd.uniform(-1, 1)
            vals = [a * q[0] + b * q[1] for q in pts]
            m = max(vals)
            if abs(a * pt[0] + b * pt[1] - m) < 1e-12 and \
               sum(1 for v in vals if abs(v - m) < 1e-12) == 1:
                return True
        return False

    P_pts = [ij(v) for v in cs]
    Q_pts = [ij(v) for v in ds]
    okv = all(is_vertex(tuple(v), P_pts) for v in META["P_vertices"]) and \
          all(is_vertex(tuple(v), Q_pts) for v in META["Q_vertices"])
    check("J5c every polygon vertex recorded in the meta is an extreme point of "
          "the corresponding support", okv,
          f"P {META['P_vertices']}  Q {META['Q_vertices']}")

    P = sum(syms[v] * x ** ij(v)[0] * y ** ij(v)[1] for v in cs)
    Q = sum(syms[v] * x ** ij(v)[0] * y ** ij(v)[1] for v in ds)
    br = sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x)
                   - x ** 2)
    pol = sp.Poly(br, x, y)
    coeff = {m: c for m, c in zip(pol.monoms(), pol.coeffs())}
    print(f"    the bracket has {len(coeff)} nonzero monomials")

    def json_expr(eq):
        e = sp.Integer(0)
        for c, m in S.eq_terms(eq):
            t = sp.Rational(c)
            for v, ex in m.items():
                t *= syms[v] ** ex
            e += t
        return sp.expand(e)

    bad = []
    for k, eq in enumerate(EQS):
        i, j = eq["bracket_point"]
        want = coeff.get((i, j), sp.Integer(0))
        if sp.expand(json_expr(eq) - want) != 0:
            bad.append((k, (i, j)))
    check("J1 POSITIVE: every JSON equation equals the corresponding coefficient "
          "of [P,Q] - x^2, exactly", not bad, f"mismatched {bad[:5]}")

    have = {tuple(eq["bracket_point"]) for eq in EQS}
    missing = [m for m in coeff if m not in have and sp.expand(coeff[m]) != 0]
    check("J2 POSITIVE: every nonzero bracket coefficient has a JSON equation",
          not missing, f"missing {missing[:6]} of {len(coeff)}")

    eq0 = EQS[0]
    e0 = json_expr(eq0) + 1
    i0, j0 = eq0["bracket_point"]
    check("J3 NEGATIVE: perturbing one JSON equation breaks the match",
          sp.expand(e0 - coeff.get((i0, j0), 0)) != 0)

    br2 = sp.expand(sp.diff(Q, x) * sp.diff(P, y) - sp.diff(Q, y) * sp.diff(P, x)
                    - x ** 2)
    pol2 = sp.Poly(br2, x, y)
    coeff2 = {m: c for m, c in zip(pol2.monoms(), pol2.coeffs())}
    bad2 = [k for k, eq in enumerate(EQS)
            if sp.expand(json_expr(eq)
                         - coeff2.get(tuple(eq["bracket_point"]), 0)) != 0]
    check("J4 NEGATIVE: the same comparison against [Q,P] - x^2 FAILS, so the "
          "orientation is pinned", bool(bad2),
          f"{len(bad2)} of {len(EQS)} equations disagree with the reversed bracket")

    n = sum(1 for _, o, _ in RESULTS if o)
    json.dump({"hash": CHASH, "nvars": len(VARS), "neqs": len(EQS),
               "bracket_monomials": len(coeff),
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "artifacts", "case2_json_audit.json"), "w"),
              indent=1)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if n == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
