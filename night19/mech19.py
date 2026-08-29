"""night19 -- THE MECHANISM, made explicit and checked.

Three checks, all exact:

  (M1) the weight grading.  P = gamma x y^2 + c y is quasi-homogeneous for the
       weight w = (-1, +1), i.e. w(x) = -1, w(y) = +1: both monomials have
       w-weight 1.  [P, . ] then raises w-weight by exactly 1, so only the
       w-weight (-1) part of Q can contribute to [P,Q] = 1.  That part is
       spanned by { x^{m+1} y^m : m >= 0 } -- a single infinite chain.

  (M2) the recursion and its truncation.  Writing Q_N = sum_{m<=N} q_m x^{m+1}y^m
       with q_m = -(1/c) (-gamma/c)^m, the identity
           [P, Q_N] - 1  =  -gamma (N+2) q_N (x y)^{N+1}
       is verified for a range of N.  The right-hand side is NEVER zero, so no
       truncation is a mate: the recursion does not terminate.

  (M3) the rational mate.  Q_inf = -x / (gamma x y + c) satisfies
       [P, Q_inf] = 1 identically as rational functions.  Its polar locus is
       {gamma x y + c = 0}, the second component of the reducible zero fibre
       P = y (gamma x y + c).
"""
import json, os
import sympy as sp
import mate19 as m

HERE = os.path.dirname(os.path.abspath(__file__))
x, y = sp.symbols('x y')
gam, c = sp.symbols('gamma c')
OUT = {}
P = {(1, 2): gam, (0, 1): c}

print("=" * 78)
print("M1  the weight grading  w(x) = -1, w(y) = +1")
print("=" * 78)
wts = {(i, j): j - i for (i, j) in P}
print("  w-weights of the monomials of P: %s   -> P is w-isobaric of weight %s"
      % ({str(k): v for k, v in wts.items()}, set(wts.values())))
assert len(set(wts.values())) == 1
# [P, x^i y^j] lands in w-weight (j - i) + 1
ok1 = True
for (i, j) in m.carrier(10):
    br = m.bracket(P, {(i, j): 1})
    for (a, b) in br:
        ok1 &= ((b - a) == (j - i) + 1)
print("  for every monomial of every carrier i+j <= 10, every monomial of "
      "[P, x^i y^j] has w-weight (j - i) + 1: %s" % ok1)
print("  so [P,Q] = 1 (w-weight 0) can only be fed by the w-weight (-1) part of Q,")
print("  which is spanned by { x^{m+1} y^m : m >= 0 }, and the target row set is")
print("  the w-weight 0 line { (x y)^n : n >= 0 }.  Both are ONE-PARAMETER chains.")
OUT["M1"] = {"weights": {str(k): v for k, v in wts.items()},
             "isobaric_weight": list(set(wts.values()))[0],
             "bracket_raises_weight_by_1_on_carrier_10": bool(ok1)}

print()
print("=" * 78)
print("M2  the recursion, and what every truncation leaves behind")
print("=" * 78)
print("  q_0 = -1/c ,  q_m = -(gamma/c) q_{m-1}  =>  q_m = -(1/c)(-gamma/c)^m")
rows = []
ok2 = True
for N in range(0, 13):
    Q = {(mm + 1, mm): -sp.Rational(1, 1) / c * (-gam / c) ** mm for mm in range(N + 1)}
    resid = m.psub(m.bracket(P, Q), {(0, 0): 1})
    qN = -1 / c * (-gam / c) ** N
    pred = m.clean({(N + 1, N + 1): -gam * (N + 2) * qN})
    same = (set(resid) == set(pred) and
            all(m._iszero(sp.simplify(resid[k] - pred[k])) for k in pred))
    ok2 &= same
    rows.append({"N": N, "residual": m.to_str(resid), "predicted": m.to_str(pred),
                 "agree": bool(same), "residual_is_zero": len(resid) == 0})
    print("  N=%-3d [P, Q_N] - 1 = %-46s  matches -gamma(N+2)q_N (xy)^{N+1}: %-5s  zero: %s"
          % (N, m.to_str(resid), same, len(resid) == 0))
print("  the residual is nonzero for EVERY N: the chain never closes.")
OUT["M2"] = {"rows": rows, "all_match": bool(ok2),
             "any_truncation_is_a_mate": any(r["residual_is_zero"] for r in rows)}

print()
print("=" * 78)
print("M3  the rational mate and the reducible fibre")
print("=" * 78)
Pe = gam * x * y**2 + c * y
Qe = -x / (gam * x * y + c)
br = sp.simplify(sp.diff(Pe, x) * sp.diff(Qe, y) - sp.diff(Pe, y) * sp.diff(Qe, x))
print("  P = %s   factors as %s" % (sp.sstr(Pe), sp.sstr(sp.factor(Pe))))
print("  Q_inf = %s" % sp.sstr(Qe))
print("  [P, Q_inf] simplifies to %s   (must be 1)" % sp.sstr(br))
print("  polar locus of Q_inf: {gamma x y + c = 0} -- the second component of the")
print("  zero fibre of P.  It is isomorphic to A^1 minus a point, not to A^1.")
OUT["M3"] = {"rational_mate": sp.sstr(Qe), "bracket": sp.sstr(br),
             "bracket_is_one": bool(sp.simplify(br - 1) == 0),
             "fibre": sp.sstr(sp.factor(Pe))}
assert sp.simplify(br - 1) == 0

json.dump(OUT, open(os.path.join(HERE, 'mech19.json'), 'w'), indent=1)
print()
print("MECHANISM CHECKS PASS" if (ok1 and ok2 and OUT["M3"]["bracket_is_one"]) else "*** FAILED ***")
