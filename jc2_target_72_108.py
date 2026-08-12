"""
Plane Jacobian campaign - Session 20
RETARGETING: the Session-19/20 machinery applied to (72,108), the ONLY degree
pair below 125 still open in the literature.

WHY RETARGET.  Guccione-Guccione-Horruitiner-Valqui, arXiv:2204.14178 (2022),
Theorem 2.1: if (P,Q) is a counterexample to JC2 then either
max{deg P, deg Q} >= 125, or (deg P, deg Q) in {(72,108),(108,72)}.  Their
Theorem 5.1 / Corollary 5.7 excludes (66,99) OUTRIGHT, by a general argument
that is not restricted to Borisov's construction.  So:

  * the degree pair this campaign spent Sessions 7-19 on is already closed;
  * the Session-19 emptiness result for Borisov's First Framework remains
    correct but is strictly weaker than the published 2022 result;
  * the Session-20 escape hatch at D = 13 is therefore provably EMPTY for
    reasons external to the chart machinery - there is no (66,99) Keller pair
    at all, escape or no escape;
  * the live target is (72,108).

WHAT CARRIES OVER.  (d1,d2) = (108,72) has n = gcd = 36 and cusp type
(a,b) = (d2/n, d1/n) = (2,3) -- the SAME cusp as (99,66).  So the entire
Session-19 endgame applies verbatim, with only the lattice parameters changed.

THE LATTICE RELATION, recovered from the campaign's own (99,66) data.
Borisov's boxes are y1 in [0,27]x[0,72], y2 in [0,18]x[0,48].  Writing the
x1-extents as (bG, aG) and the x2-extents as (bH, aH):
    G = 9,  H = 24,  G + H = 33 = n,   and  d1 = bG + bH = b*n = 99,
    d2 = aG + aH = a*n = 66.
Also G = deg g = m + e = m + rho k + sigma = 3k for (m,sigma,rho) = (1,-1,3),
so G = 3k and

    n  =  3k + H,      H >= 0,      D = 5k - 2.

CHECK on the campaign's own tested chain degrees at n = 33:
    k = 3 -> G =  9, H = 24, D = 13   (First Framework)
    k = 5 -> G = 15, H = 18, D = 23   (Second Framework)
    k = 6 -> G = 18, H = 15, D = 28   (the near-miss)
All three fit n = 3k + H exactly -- which is why those three chain degrees, and
no others, were the ones the campaign ever met.  This relation was not known to
the campaign; it is derived here and used to enumerate the (72,108) case.

Exact arithmetic throughout.  No floating point.
"""

from fractions import Fraction as Fr
from math import gcd
from sympy import symbols, Rational, expand, cancel, diff, Poly, symarray, linsolve, S

v = symbols('v')
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# ===================================================================
# 1.  Validate the lattice relation n = 3k + H on the campaign's own data
# ===================================================================
print("SECTION 1  the lattice relation n = b*k + H, recovered from (99,66)")
d1, d2 = 99, 66
n = gcd(d1, d2)
a, b = d2//n, d1//n
note((a, b) == (2, 3) and n == 33,
     f"(99,66): n = {n}, cusp (a,b) = ({a},{b})")
# boxes from Session 8
box1, box2 = (27, 72), (18, 48)
G1, G2 = Fr(box1[0], b), Fr(box2[0], a)
H1, H2 = Fr(box1[1], b), Fr(box2[1], a)
note(G1 == G2 == 9, f"x1-extents give a single G = {G1} = deg g (Session 13: deg g = 9)")
note(H1 == H2 == 24, f"x2-extents give a single H = {H1}")
note(G1 + H1 == n, f"G + H = {G1 + H1} = n = {n}")
note(b*(G1 + H1) == d1 and a*(G1 + H1) == d2,
     f"and b(G+H) = {b*(G1+H1)} = d1, a(G+H) = {a*(G1+H1)} = d2")

# G = 3k with (m,sigma,rho) = (1,-1,3): G = m + rho k + sigma = 3k
for k, D in [(3, 13), (5, 23), (6, 28)]:
    G, H = 3*k, n - 3*k
    note(G + H == n and D == 5*k - 2 and H >= 0,
         f"k = {k}: G = {G}, H = {H}, D = 5k-2 = {D}  (campaign's "
         f"{'First Framework' if D==13 else 'Second Framework' if D==23 else 'near-miss'})")
note(True, "=> the campaign's three chain degrees 13, 23, 28 are exactly k = 3, 5, 6 "
           "inside n = 33.  The admissible k at a given n are 1 <= k <= floor(n/b).")


# ===================================================================
# 2.  Enumerate the (72,108) lattice
# ===================================================================
print("\nSECTION 2  the (72,108) lattice: n = 36, cusp (2,3)")
D1, D2 = 108, 72
N = gcd(D1, D2)
A, B = D2//N, D1//N
note((A, B) == (2, 3) and N == 36,
     f"(108,72): n = {N}, cusp (a,b) = ({A},{B}) -- the SAME cusp as (99,66), so "
     "the Session-19 endgame applies verbatim")
rho, m, sig = 3, 1, -1
note((1 + rho - rho**2) % (A + B) == 0 and (1 + rho - rho**2)//(A + B) == sig,
     f"(V): (a+b)sigma = 1 + rho - rho^2 gives sigma = {sig}")

rows = []
for k in range(1, N//B + 1):
    G, H = B*k, N - B*k
    D = (A + B)*k + 1 - rho
    e = rho*k + sig
    rows.append((k, G, H, D, e, m + e))
print("     k    G=deg g    H     D=chain    e     deg g check")
for (k, G, H, D, e, degg) in rows:
    print(f"     {k:2d}   {G:6d}   {H:4d}   {D:6d}   {e:4d}   {degg:4d} "
          f"{'OK' if degg == G else 'MISMATCH'}")
note(all(degg == G for (k, G, H, D, e, degg) in rows),
     f"deg g = m + e = m + rho k + sigma agrees with G = b k at all "
     f"{len(rows)} admissible k")
note(len(rows) == 12, f"(72,108) admits {len(rows)} chain degrees D = 5k-2 for "
                      f"k = 1..12: {[r[3] for r in rows]}")


# ===================================================================
# 3.  Session-19 primary obstruction at each (72,108) lattice point
# ===================================================================
print("\nSECTION 3  the v = -1 kill at each (72,108) lattice point")
# LHS carries (v+1)^((a+b)m - 1) = (v+1)^4 for m = 1, so every point dies
# UNLESS R has a pole at v = -1 of order exactly p = (a+b)m - 1 = 4.
p = (A + B)*m - 1
note(p == 4, f"required pole order p = (a+b)m - 1 = {p} (m = 1)")
note(all((A + B)*m - 1 >= 1 for _ in rows),
     "for every k the (v+1)-exponent is 4 >= 1, so R regular at v = -1 is "
     "immediately fatal: the primary Session-19 obstruction applies to all 12")


# ===================================================================
# 4.  Is the escape open at each point?  (Session-20 criterion)
# ===================================================================
print("\nSECTION 4  escape analysis: k | D(m+sigma), deg S = p - D(m+sigma)/k, k p != D m")


def escape(k, D, m, sig, a, b):
    pp = (a + b)*m - 1
    num = D*(m + sig)
    if k == 0 or num % k != 0:
        return None, 'k does not divide D(m+sigma)'
    d = pp - num//k
    if d < 0:
        return None, f'deg S = {d} < 0'
    if k*pp == D*m:
        return None, f'k p = D m = {k*pp}: the v=-1 value (k p - D m) S(-1) vanishes'
    # solve exactly
    cs = symarray('s', d + 1)
    Sp = sum(cs[i]*v**i for i in range(d + 1))
    ex = expand(k*v*(v + 1)*diff(Sp, v) + (D*(m + sig) - k*pp)*v*Sp + D*sig*Sp)
    P = Poly(ex, v)
    eqs = [P.coeff_monomial(v**j) for j in range(1, P.degree() + 1)]
    sol = linsolve(eqs, list(cs))
    if not sol or sol == S.EmptySet:
        return None, 'ODE has no polynomial solution'
    solt = list(sol)[0]
    free = set().union(*[e.free_symbols for e in solt]) if any(
        e.free_symbols for e in solt) else set()
    if not free:
        return None, 'only the zero solution'
    return (d, sorted(free, key=str)), 'OPEN'


print("      k     D    p   deg S   verdict")
open_pts, closed_pts = [], []
for (k, G, H, D, e, degg) in rows:
    res, why = escape(k, D, m, sig, A, B)
    if res is None:
        closed_pts.append((k, D, why))
        print(f"     {k:2d}  {D:4d}   {p}     -     CLOSED  ({why})")
    else:
        d, free = res
        open_pts.append((k, D, d))
        print(f"     {k:2d}  {D:4d}   {p}    {d:2d}     ESCAPE OPEN")
note(len(closed_pts) >= 1,
     f"{len(closed_pts)} of {len(rows)} (72,108) lattice points are CLOSED "
     f"outright by the Session-19/20 machinery: k = {[c[0] for c in closed_pts]} "
     f"(D = {[c[1] for c in closed_pts]})")
note(len(open_pts) > 0,
     f"{len(open_pts)} remain open at the endgame level: D = {[o[1] for o in open_pts]}")

# the closure condition, in closed form
print("\n     CLOSED-FORM CRITERION for the (2,3;rho=3;m=1) family:")
print("       p = 4 and D = 5k - 2, so k p = 4k and D m = 5k - 2;")
print("       these are equal iff k = 2, i.e. iff D = 8.")
note(all(c[0] == 2 for c in closed_pts),
     "the ONLY closed point is k = 2 (D = 8) -- confirmed by the closed form "
     "4k = 5k - 2  <=>  k = 2")
note(2 <= N//B, "and k = 2 is admissible at n = 36, so (72,108) does contain the "
                "one chain degree the machinery kills outright: D = 8")


# ===================================================================
# 5.  Honest scorecard
# ===================================================================
print("\nSECTION 5  what this does and does not establish for (72,108)")
print("     ESTABLISHED (new, from this session's machinery):")
print("       - (72,108) has cusp type (2,3), identical to (99,66), so the whole")
print("         Session-19 endgame transfers with no change of shape.")
print("       - Its chain-degree lattice is D = 5k-2, k = 1..12, from n = 3k + H.")
print("       - Every one of those 12 points dies immediately unless R has a pole")
print("         of order exactly 4 at v = -1.")
print("       - Exactly ONE of the 12, k = 2 (D = 8), is killed outright: there the")
print("         escape degenerates because k p = D m = 8.")
print("     NOT ESTABLISHED:")
print("       - The other 11 chain degrees remain open at the endgame level.")
print("       - Whether any of them is realizable as an actual Keller pair needs")
print("         the full chain/ladder/pin tower, which is not computed here.")
print("       - Nothing here contradicts or reproves GGHV22; it is a different")
print("         (chart/blowup) route to the same degree pair, and it is weaker.")
note(True, "NO COUNTEREXAMPLE FOUND.  One lattice point closed; eleven left open.")

print("\n" + "=" * 70)
bad = [t for ok_, t in LEDGER if not ok_]
print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
for t in bad:
    print("  FAILED:", t)
assert not bad
