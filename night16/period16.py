"""night16 -- period instruments ON an atypical fibre.

EXACT-PRIM  (exact, decisive in the VANISHING direction, with a certificate)
---------------------------------------------------------------------------
On the smooth fibre F_c the module of regular 1-forms is free of rank 1 on
eta = dy/P_x = -dx/P_y, and for F in the coordinate ring

        dF|_{F_c} = [P, F] * eta ,      [P, F] = P_x F_y - P_y F_x .

So eta is EXACT on F_c (equivalently: every period of eta over every cycle of
H_1(F_c) vanishes) exactly when 1 lies in the image of the Jacobian derivation
on the coordinate ring, i.e. when

        [P, F] = 1   in   Q[x,y]/(P - c)                                   (E)

for some polynomial F.  ("Every period vanishes => a primitive exists as a
REGULAR function": eta is regular on the affine F_c, so a period-free primitive
is holomorphic on F_c and meromorphic at each puncture -- the local primitive of
a form with a pole and zero residue is meromorphic -- hence rational on the
smooth compactification with poles only at the punctures, i.e. regular on F_c.)

F_c is smooth, so it is the disjoint union of its irreducible components and
(E) holds iff it holds modulo every irreducible factor h of P - c separately
(CRT).  Working per component makes each system small.  The membership test
"[P,F] - 1 in (h)" is carried out by pseudo-division: with v the variable in
which h has positive degree,

        prem([P,F] - 1, h, v) == 0     <=>     [P,F] - 1 in (h)

(lc_v(h) is a unit modulo the irreducible h), and prem is LINEAR in the
unknown coefficients of F, so this is one rational linear system per (h, deg F).

A solution is a CERTIFICATE: it is verified afterwards by exact division,
[P,F] - 1 = G*h checked coefficientwise over Q.  Failure at degree <= Dmax is
recorded as NO_CERTIFICATE_TO_DEG_Dmax and is NOT read as an obstruction.

NUM-MONO  (numerical, decisive in the NONVANISHING direction)
-------------------------------------------------------------
night15's numerical monodromy period instrument, used unchanged (copied into
this lane as mono16.py), evaluated ON the atypical fibre and at nearby generic
fibres.
"""

import sympy as sp

x, y = sp.symbols('x y')


def _monoms(D):
    return [(i, j) for i in range(D + 1) for j in range(D + 1 - i)]


def primitive_mod(Pexpr, h, Dmax=6):
    """find F with [P,F] = 1 mod (h); returns dict with an exact certificate."""
    Px, Py = sp.diff(Pexpr, x), sp.diff(Pexpr, y)
    hp = sp.Poly(h, x, y)
    var = y if hp.degree(y) > 0 else x
    hv = sp.Poly(h, var)
    for D in range(1, Dmax + 1):
        ms = _monoms(D)
        us = [sp.Symbol('u_%d_%d' % m) for m in ms]
        F = sum(u * x**i * y**j for u, (i, j) in zip(us, ms))
        br = sp.expand(Px * sp.diff(F, y) - Py * sp.diff(F, x) - 1)
        R = sp.prem(sp.Poly(br, var), hv).as_expr()
        Rp = sp.Poly(sp.expand(R), x, y)
        eqs = [sp.expand(c) for c in Rp.coeffs()]
        if not eqs:
            continue
        Amat, b = sp.linear_eq_to_matrix(eqs, us)
        try:
            sol, params = Amat.gauss_jordan_solve(b)
        except ValueError:
            continue
        sub = {p: sp.Integer(0) for p in params}
        vals = [sp.nsimplify(v.subs(sub)) for v in sol]
        Fv = sp.expand(sum(v * x**i * y**j for v, (i, j) in zip(vals, ms)))
        brv = sp.expand(Px * sp.diff(Fv, y) - Py * sp.diff(Fv, x) - 1)
        q, r = sp.div(sp.expand(brv), sp.expand(h), x, y)
        ok = sp.expand(brv - q * h) == 0 and sp.expand(r) == 0
        if ok:
            return {"ok": True, "degF": D, "F": str(sp.factor(Fv)) if Fv != 0 else "0",
                    "F_expr": sp.srepr(Fv), "cofactor_deg": int(sp.Poly(q, x, y).total_degree())
                    if q != 0 else -1,
                    "verified": True,
                    "witness": "[P,F] - 1 = G*h verified coefficientwise over Q"}
    return {"ok": False, "Dmax": Dmax,
            "witness": "no F of degree <= %d with [P,F] = 1 mod h" % Dmax}


def exact_periods_vanish(Pexpr, cval, Dmax=6):
    """EXACT-PRIM on every irreducible component of {P = cval}."""
    f = sp.expand(Pexpr - cval)
    facs = sp.factor_list(f, x, y)[1]
    comps = []
    allok = True
    for h, mult in facs:
        r = primitive_mod(Pexpr, h, Dmax=Dmax)
        r["h"] = str(sp.factor(h))
        r["h_deg"] = int(sp.Poly(h, x, y).total_degree())
        r["mult"] = int(mult)
        comps.append(r)
        allok &= bool(r["ok"])
    return {"n_components_over_Q": len(facs), "all_exact": bool(allok),
            "components": comps,
            "verdict": "VANISHING_EXACT" if allok else "NO_EXACT_CERTIFICATE"}
