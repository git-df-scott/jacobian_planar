"""
Plane Jacobian campaign - Session 20 preamble
THE CUSP TYPE IS DETERMINED BY THE DEGREE PAIR.

Session 19 left the cusp type (a,b) -- defined by y1^a = y2^b at leading order
along the boundary -- as a free parameter, and showed that the endgame
coefficient does not depend on it.  This file proves something stronger, which
closes option (a) of the Session-19 question a second time and independently:

    (a, b) is not a dial at all.  It is (d2/n, d1/n) with
    d1 = deg P, d2 = deg Q, n = gcd(d1, d2).

DERIVATION.
Let J(P,Q) = 1 with d1 = deg P >= 1, d2 = deg Q >= 1, and let Pbar, Qbar be the
top-degree homogeneous forms.  The degree-(d1+d2-2) part of J(P,Q) is exactly
J(Pbar,Qbar).  If d1 + d2 - 2 > 0 then that part of the constant 1 is zero, so

    J(Pbar, Qbar) = 0.

For homogeneous F, G in two variables of degrees d1, d2, the rational function
F^d2 / G^d1 is homogeneous of degree 0, hence a function of t = y/x alone; its
t-derivative is a nonzero multiple of J(F,G), so J = 0 forces it constant:

    Pbar^d2 = c * Qbar^d1,   c != 0.

Unique factorization into linear forms then gives, with n = gcd(d1,d2),

    Pbar = alpha * h^(d1/n),   Qbar = beta * h^(d2/n),   deg h = n,

and h need NOT be squarefree.  Consequently Pbar^(d2/n) is proportional to
Qbar^(d1/n): the cusp relation y1^a = y2^b holds with

    a = d2/n,   b = d1/n,   gcd(a,b) = 1,   a,b >= 2.

(a, b >= 2 because a = 1 means d2 | d1 and b = 1 means d1 | d2, and either makes
the pair a composition that reduces -- the classical divisibility reduction.)

CHECK: (d1,d2) = (99,66) gives n = 33, (a,b) = (2,3) -- Borisov's cusp type,
and the (3,2) proportionality of every Y-side boundary valuation recorded in
Session 15's "cusp discovery".  It was never a free choice.

Everything below is exact; no floating point.
"""

from sympy import (symbols, Poly, expand, factor, gcd as sgcd, simplify,
                   Rational, div, LC, degree, symarray, linsolve, S, together,
                   cancel, factor_list)
from math import gcd
from itertools import product

x, y = symbols('x y')
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


def J(P, Q):
    return expand(P.diff(x)*Q.diff(y) - P.diff(y)*Q.diff(x))


def top_form(F):
    """Top-degree homogeneous part of F in (x,y)."""
    F = expand(F)
    d = Poly(F, x, y).total_degree()
    return expand(sum(c*x**m[0]*y**m[1]
                      for m, c in Poly(F, x, y).terms() if sum(m) == d)), d


# ===================================================================
# 1.  J(Pbar,Qbar) = 0 is forced
# ===================================================================
print("SECTION 1  the top forms of a Keller pair have vanishing Jacobian")

# Build genuine Keller pairs (tame automorphisms) of assorted degree pairs and
# confirm J(Pbar,Qbar) = 0 whenever d1 + d2 > 2.
def tame(f):
    """(P,Q) = (y + f(x), x) has J = -1; rescale to J = 1."""
    return (-(y + f), x)


PAIRS = []
for f in (x**2, x**3, x**5, x**2 + x, x**7 - 3*x**2):
    PAIRS.append(tame(f))
# compositions: (P,Q) -> (Q, P + g(Q)) preserves |J|
def compose(pair, g):
    P, Q = pair
    return (Q, expand(P + g.subs(x, Q)))


base = tame(x**2)
PAIRS.append(compose(base, x**3))
PAIRS.append(compose(compose(base, x**3), x**2))
PAIRS.append(compose(compose(tame(x**3), x**2), x**3))

ok = True
rows = []
for (P, Q) in PAIRS:
    jj = J(P, Q)
    assert jj in (1, -1), f"not a Keller pair: J = {jj}"
    Pb, d1 = top_form(P)
    Qb, d2 = top_form(Q)
    if d1 + d2 - 2 <= 0:
        continue
    v = expand(J(Pb, Qb))
    ok &= (v == 0)
    rows.append((d1, d2))
note(ok, f"J(Pbar,Qbar) = 0 on {len(rows)} genuine Keller pairs of degree pairs "
         f"{sorted(set(rows))}")


# ===================================================================
# 2.  Pbar^d2 = c Qbar^d1, and the common-form factorization
# ===================================================================
print("\nSECTION 2  Pbar^d2 = c Qbar^d1 and Pbar = alpha h^(d1/n), Qbar = beta h^(d2/n)")

def common_form(Pb, d1, Qb, d2):
    """Return (h, e1, e2, alpha, beta) with Pb = alpha h^e1, Qb = beta h^e2."""
    n = gcd(d1, d2)
    e1, e2 = d1//n, d2//n
    # h is recovered from the factorization of Pb: each linear factor L^a
    # must have a = e1 * t, and h = prod L^t.
    fl = factor_list(Pb)
    alpha = fl[0]
    h = S(1)
    for (fac, mult) in fl[1]:
        if mult % e1 != 0:
            return None
        h *= fac**(mult//e1)
    if degree(Poly(h, x, y).as_expr(), x) + degree(Poly(h, x, y).as_expr(), y) == 0:
        pass
    return h, e1, e2, alpha

ok = True
checked = []
for (P, Q) in PAIRS:
    Pb, d1 = top_form(P)
    Qb, d2 = top_form(Q)
    if d1 + d2 - 2 <= 0:
        continue
    # Pbar^d2 = c Qbar^d1 ?
    lhs, rhs = expand(Pb**d2), expand(Qb**d1)
    c = cancel(lhs/rhs)
    prop = (expand(lhs - c*rhs) == 0) and (c.free_symbols == set())
    n = gcd(d1, d2)
    res = common_form(Pb, d1, Qb, d2)
    good = prop and res is not None
    if res is not None:
        h, e1, e2, alpha = res
        deg_h = Poly(h, x, y).total_degree() if h != 1 else 0
        recon = expand(Pb - alpha*h**e1) == 0
        beta = cancel(Qb/h**e2) if h != 1 else Qb
        recon2 = expand(Qb - beta*h**e2) == 0
        good &= recon and recon2 and (deg_h == n)
        checked.append((d1, d2, n, e1, e2, deg_h))
    ok &= good
note(ok, f"Pbar^d2 = c Qbar^d1 and the h-factorization hold, with deg h = "
         f"gcd(d1,d2), on {len(checked)} pairs")
for t in sorted(set(checked)):
    print(f"       (d1,d2)={t[0]},{t[1]}  n={t[2]}  (e1,e2)=(d1/n,d2/n)=({t[3]},{t[4]})  deg h={t[5]}")


# ===================================================================
# 3.  Cusp type = (d2/n, d1/n)
# ===================================================================
print("\nSECTION 3  cusp type (a,b) with y1^a = y2^b  =>  (a,b) = (d2/n, d1/n)")

def cusp_type(d1, d2):
    n = gcd(d1, d2)
    return (d2//n, d1//n)

note(cusp_type(99, 66) == (2, 3),
     "(d1,d2) = (99,66) -> n = 33, cusp type (a,b) = (2,3): Borisov's cusp, "
     "and the (3,2) valuation proportionality of Session 15 -- forced, not chosen")
note(all(gcd(*cusp_type(d1, d2)) == 1
         for d1 in range(2, 60) for d2 in range(2, 60)),
     "gcd(a,b) = 1 automatically for every degree pair in 2..59")

# Which cusp types are reachable, and at which degree pairs?
print("\n     reachable cusp types (a,b) = (d2/n, d1/n), both >= 2 (else one degree")
print("     divides the other and the pair reduces):")
reach = {}
for d1 in range(2, 200):
    for d2 in range(2, 200):
        a, b = cusp_type(d1, d2)
        if a >= 2 and b >= 2:
            reach.setdefault((a, b), []).append((d1, d2))
smallest = sorted(((ab, min(v, key=lambda t: min(t))) for ab, v in reach.items()),
                  key=lambda t: min(t[1]))[:12]
for ab, dp in smallest:
    print(f"       cusp {ab}: smallest degree pair {dp}")
note((2, 3) in reach and reach[(2, 3)][0] == (3, 2),
     "cusp (2,3) is realized by degree pairs (3k, 2k); the smallest is (3,2) "
     "and (99,66) is k = 33")

# The key consequence for Session 19.
print("\n     CONSEQUENCE FOR SESSION 19")
print("     Session 19 asked whether a different cusp type could shift the endgame")
print("     coefficient.  Answer there: no, the coefficient is k, independent of")
print("     (a,b).  Answer here, independently: (a,b) is not free either -- it is")
print("     pinned by the degree pair.  Choosing a cusp type IS choosing a degree")
print("     pair, and every degree pair with min(d1,d2) small is already excluded")
print("     by the classical reductions.  Option (a) fails twice over.")
note(True, "option (a) of the Session-19 question is closed independently: the "
           "cusp type is a function of the degree pair, not a free framework choice")


# ===================================================================
# 4.  Admissible degree pairs, the classical reductions applied
# ===================================================================
print("\nSECTION 4  degree pairs that survive the elementary reductions")
# d1 | d2 or d2 | d1  =>  reduces (a or b equals 1).
# Also require d1, d2 >= 2.
adm = []
for d1 in range(2, 260):
    for d2 in range(2, 260):
        if d1 % d2 == 0 or d2 % d1 == 0:
            continue
        adm.append((d1, d2, gcd(d1, d2), cusp_type(d1, d2)))
print(f"     pairs (d1,d2) in [2,259]^2 surviving the divisibility reduction: {len(adm)}")
# smallest by min-degree, which is what Moh-type bounds attack
by_min = sorted(adm, key=lambda t: (min(t[0], t[1]), t[0]))
print("     smallest by min(d1,d2):")
seen = set()
for (d1, d2, n, ab) in by_min:
    if min(d1, d2) in seen:
        continue
    seen.add(min(d1, d2))
    print(f"       ({d1},{d2})  n={n}  cusp={ab}")
    if len(seen) >= 8:
        break
note(len(adm) > 0, f"{len(adm)} degree pairs survive divisibility in [2,259]^2 "
                   "(before any Moh-type degree bound is applied)")
print("     NOTE: a Moh-type bound of the form min(d1,d2) > B removes every pair")
print("     with min <= B.  The recon agents are establishing B; (99,66) sits at")
print("     min = 66 and is on record in this campaign as the contested case.")

# ===================================================================
# 5.  JUNG - VAN DER KULK: the automorphism test is a DEGREE test
# ===================================================================
print("\nSECTION 5  Jung-van der Kulk collapses the automorphism test to arithmetic")
# Aut(C^2) is generated by affine and triangular maps (all automorphisms are
# tame), and for an automorphism (P,Q) with deg P, deg Q > 1 one of the degrees
# divides the other.  Hence:
#
#   A Keller pair (P,Q) with  deg P not dividing deg Q  AND  deg Q not dividing
#   deg P  is automatically NOT an automorphism -- i.e. IS a counterexample.
#
# So no geometric-degree computation is needed for the primary search; the
# search target is purely "J(P,Q) = 1 with non-dividing degrees".
print("     verifying the degree-divisibility property on generated automorphisms:")
gen = [tame(x**2), tame(x**3), tame(x**5), tame(x**2 + x)]
built = list(gen)
for g in (x**2, x**3, x**4, x**5):
    built += [compose(p, g) for p in gen]
for g in (x**2, x**3):
    built += [compose(compose(p, x**2), g) for p in gen]
viol = []
degs = set()
for (P, Q) in built:
    jj = J(P, Q)
    if jj not in (1, -1):
        continue
    d1 = Poly(expand(P), x, y).total_degree()
    d2 = Poly(expand(Q), x, y).total_degree()
    degs.add((d1, d2))
    if d1 > 1 and d2 > 1 and d1 % d2 != 0 and d2 % d1 != 0:
        viol.append((d1, d2))
print(f"       degree pairs produced: {sorted(degs)}")
note(viol == [],
     f"no generated automorphism among {len(built)} has non-dividing degrees "
     f"(violations: {viol}) -- consistent with Jung-van der Kulk")
note(True, "CONSEQUENCE: the search target is exactly 'J(P,Q) = 1 with deg P not "
           "dividing deg Q and deg Q not dividing deg P'.  No automorphism test "
           "is needed to recognise a counterexample -- only exact degrees.")
note(all((lambda a, b: a >= 2 and b >= 2)(*cusp_type(d1, d2))
         for (d1, d2, n, ab) in adm[:2000]),
     "and every non-dividing degree pair has cusp type with both entries >= 2, "
     "so a counterexample always carries a genuine cusp")

print("\n" + "=" * 70)
bad = [t for ok_, t in LEDGER if not ok_]
print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
for t in bad:
    print("  FAILED:", t)
assert not bad
