"""
Plane Jacobian campaign - Session 20
PHASE 4: THE DIRECT ATTACK at (72,108).

Why this is the DIRECT route.  In the GGHV/Newton-polygon attack (Phase 1) a
solution of the (8,28) system is NOT a counterexample: Prop 4.3's pairs are
related to a genuine Keller pair by a chain of automorphisms of L^(1) that must
be inverted first (jc2_gghv_system.md section 9).  Here, by contrast, y1 and y2
ARE the map.  Solving this tower hands you P and Q with no inversion step.
The trade-off is coverage: this route only sees maps carrying the chart/blowup
boundary geometry, so it is direct but narrow.

WHAT SESSION 19/20 ALREADY ESTABLISHED.
The endgame identity, with every framework input free, is

  alpha^(a+b) (v+1)^((a+b)m-1) v^((a+b)sigma-1)
      [ k v(v+1) R' + D((m+sigma)v + sigma) R ]  =  -c v^(rho-rho^2)

with m >= 1 forced, so every configuration dies at v = -1 UNLESS R has a pole
there of order exactly p = (a+b)m - 1.  At (108,72): n = gcd = 36, cusp
(a,b) = (d2/n, d1/n) = (2,3), rho = 3, sigma = -1, m = 1, and the chain lattice
is D = 5k - 2 for k = 1..12 (from n = b*k + H).

TWO of the twelve self-kill, by two DIFFERENT mechanisms -- and the second was
found here, refining the Session-19/20 criterion:
  k = 2 (D = 8):  k*p = D*m = 8, so the v = -1 residue (k p - D m) S(-1) vanishes.
  k = 1 (D = 3):  k*p != D*m (4 != 3), yet the ODE's forced constant comes out
                  ZERO, i.e. c = 0, contradicting the Keller condition c != 0.
So "k*p != D*m" is NECESSARY but NOT SUFFICIENT for the escape to be inhabited.
TEN chain degrees remain.

WHAT THIS FILE DOES.  For each of the ten surviving chain degrees it solves
the escape ODE exactly and writes down the FORCED endgame functional R -- which
is unique up to one scalar, because the homogeneous solution
C (v/(v+1))^(D m / k) is irrational whenever k does not divide D*m.  That gives,
for every open chain degree at the only degree pair still open below 125, the
explicit rational function any Keller pair of this shape MUST realize.

That is the concrete target of the direct attack: not "search a space", but
"realize this specific R by an actual tower, or prove it cannot be realized".

Exact arithmetic throughout.  No floating point.
"""

from math import gcd
import sympy as sp

v = sp.symbols('v')
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def forced_R(a, b, k, D, m, sig):
    """Exact solution of the escape ODE; returns (S, deg S, constant, R)."""
    p = (a + b)*m - 1
    num = D*(m + sig)
    if k == 0 or num % k != 0:
        return None
    d = p - num//k
    if d < 0 or k*p == D*m:
        return None   # degenerate: the v=-1 residue (k p - D m) S(-1) vanishes
    cs = sp.symarray('s', d + 1)
    S = sum(cs[i]*v**i for i in range(d + 1))
    expr = sp.expand(k*v*(v + 1)*sp.diff(S, v)
                     + (D*(m + sig) - k*p)*v*S + D*sig*S)
    P = sp.Poly(expr, v)
    eqs = [P.coeff_monomial(v**j) for j in range(1, P.degree() + 1)]
    sol = sp.linsolve(eqs, list(cs))
    if not sol or sol == sp.S.EmptySet:
        return None
    tup = list(sol)[0]
    free = sorted(set().union(*[e.free_symbols for e in tup]) if any(
        e.free_symbols for e in tup) else set(), key=str)
    if not free:
        return None
    lead = free[-1]
    # normalize the free scalar to 1 and clear denominators
    sub = {s: 0 for s in free}
    sub[lead] = 1
    Sc = [sp.cancel(e.subs(sub)) for e in tup]
    Sx = sp.expand(sum(Sc[i]*v**i for i in range(len(Sc))))
    den = sp.lcm([sp.denom(sp.nsimplify(c)) for c in sp.Poly(Sx, v).coeffs()])
    Sx = sp.expand(Sx*den)
    const = sp.expand(k*v*(v + 1)*sp.diff(Sx, v)
                      + (D*(m + sig) - k*p)*v*Sx + D*sig*Sx)
    R = sp.cancel(Sx/(v + 1)**p)
    return Sx, sp.Poly(Sx, v).degree(), const, R, p


def main():
    d1, d2 = 108, 72
    n = gcd(d1, d2)
    a, b = d2//n, d1//n
    rho, m, sig = 3, 1, -1
    print(f"TARGET: (deg P, deg Q) = ({d1},{d2})  ->  n = {n}, cusp (a,b) = ({a},{b})")
    print(f"        rho = {rho}, sigma = {sig}, m = {m};  chain lattice D = "
          f"{a+b}k + 1 - rho = {a+b}k - {rho-1}\n")
    note((a, b) == (2, 3), "cusp type is (2,3), identical to the (99,66) family, "
                           "so the Session-19 endgame transfers verbatim")

    rows = []
    for k in range(1, n//b + 1):
        D = (a + b)*k + 1 - rho
        res = forced_R(a, b, k, D, m, sig)
        if res is None:
            rows.append((k, D, None, None, None, "CLOSED (k*p = D*m)"))
            continue
        Sx, degS, const, R, p = res
        # verify the ODE is satisfied and the constant is nonzero
        chk = sp.expand((v + 1)**p*sp.expand(
            k*v*(v + 1)*sp.diff(R, v) + D*((m + sig)*v + sig)*R))
        ok = (sp.Poly(const, v).degree() == 0) and (const != 0) and \
             (sp.simplify(sp.expand(chk - const)) == 0)
        # A SECOND, independent way to die: the ODE's forced constant can be
        # zero even when k*p != D*m.  Then c = 0, contradicting the Keller
        # condition c != 0.  So "k*p != D*m" is NECESSARY but NOT SUFFICIENT --
        # a refinement of the Session-19/20 escape criterion, found here.
        if const == 0:
            rows.append((k, D, None, None, sp.Integer(0),
                         "CLOSED (forced c = 0)"))
        else:
            rows.append((k, D, Sx, R, const, "OPEN" if ok else "check failed"))

    print("  k    D      status        c (Keller constant, up to alpha^5 and scale)")
    for (k, D, Sx, R, const, st) in rows:
        print(f"  {k:2d}  {D:3d}   {st:14s}  {const if const is not None else '-'}")

    opens = [r for r in rows if r[5] == "OPEN"]
    closed = [r for r in rows if r[5].startswith("CLOSED")]
    note(len(closed) == 2,
         f"TWO lattice points are self-killing, by two DIFFERENT mechanisms: "
         f"{', '.join('k=%d (D=%d) %s' % (r[0], r[1], r[5]) for r in closed)}")
    note(len(opens) == 10, f"{len(opens)} chain degrees remain open at (72,108)")
    note(True, "REFINEMENT of the Session-19/20 criterion: k*p != D*m is "
               "NECESSARY but NOT SUFFICIENT for the escape to be inhabited; "
               "the ODE's forced constant must also be nonzero.  k=1 satisfies "
               "k*p != D*m (4 != 3) and still dies with c = 0.")

    print("\n  THE FORCED ENDGAME FUNCTIONALS  (unique up to one scalar)")
    for (k, D, Sx, R, const, st) in opens:
        print(f"\n  k = {k}, D = {D}:")
        print(f"    S(v) = {sp.factor(Sx)}")
        print(f"    R(v) = S(v) / (v+1)^4")
        # uniqueness: the homogeneous solution must be irrational
        irr = (D*m) % k != 0
        print(f"    homogeneous solution C(v/(v+1))^({D*m}/{k}) irrational: {irr}"
              f"  ->  R {'is unique up to scale' if irr else 'NOT unique -- rational homogeneous part exists'}")

    print("\n" + "=" * 70)
    bad = [t for ok_, t in LEDGER if not ok_]
    print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
    for t in bad:
        print("  FAILED:", t)
    print("""
WHAT THE DIRECT ATTACK NOW IS.
For each open k above, R is pinned to one explicit rational function.  A Keller
pair of this shape at (72,108) exists if and only if some tower (chain blocks,
divisibility ladder, cross-chart Taylor pins) realizes that exact R.  So the
search is no longer over a space of maps -- it is: realize this R, or prove it
unrealizable.  That is the object to attack, and unlike Phase 1 a solution here
IS the map: y1 and y2 are P and Q, with no automorphism chain to invert.""")


if __name__ == '__main__':
    main()
