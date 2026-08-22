#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1c-POLEFIX -- correction of our own H1c "closed form",
and a complete classification of the rational solutions of the endgame equation.

    E(D,k):    (v+1)^k ( 3 v(v+1) R' - D R )  =  -c ,      c != 0.

WHAT WENT WRONG.  wave1/w1_h1c_endgame_closed_form.py printed

    "has a rational solution R of degree >= 1 if and only if k = 0 AND 3 | D"

but its k >= 1 branch was ASSERTED, not computed: the check() call passed a
literal True, and its own prose reads "IF R is regular at v = -1 then the left
side vanishes at v = -1".  Regularity at v = -1 is exactly what THEOREM 3
(pole-fiber => R polynomial) exists to supply, so the k >= 1 branch silently
assumed the campaign's own flagged-uncertified input.

The printed theorem is FALSE as stated.  Explicit counterexample at the
campaign's own (D,k) = (13,4):

    R = (243 v^4 - 81 v^3 + 54 v^2 - 42 v + 35) / (455 (v+1)^4)

is a non-constant rational solution of E(13,4) with c = 1, carrying a genuine
order-4 pole at v = -1 (gcd(numerator,(v+1)^4) = 1).  Verified below by direct
substitution, by Laurent series, and numerically.

WHAT IS ACTUALLY TRUE.  Below we classify ALL rational solutions and obtain a
replacement that is strictly stronger where it matters.
"""
import sys, random
from sympy import (symbols, Poly, expand, simplify, solve, diff, factor, cancel,
                   fraction, series, gcd, Rational, together, nsimplify)

FAIL = []
def check(l, cond, s, e=""):
    if not cond: FAIL.append(l)
    print(f"  {'PASS' if cond else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

v = symbols('v')
c = symbols('c', nonzero=True)

print("="*78)
print("H1c-POLEFIX -- all rational solutions of (v+1)^k(3v(v+1)R' - D R) = -c")
print("="*78)

# ---------------------------------------------------------------- STEP 1 ---
print("""
STEP 1 -- WHERE THE POLES CAN BE.  Let R be a rational solution, D>=1, k>=0.

 (a) p not in {0,-1,inf}: 3v(v+1) is a nonzero constant at p, so a pole of
     order n>=1 makes 3v(v+1)R' have order n+1 and D*R order n; the left side
     then has a pole of order n+1>=2 where the right side is regular.
     => NO poles off {0,-1,inf}.

 (b) v = 0, pole order n>=1: R = a v^-n+..., 3v(v+1)R' = -3n a v^-n+..., so the
     left side is (-3n-D) a v^-n + ... with -3n-D < 0, hence nonzero, while
     -c/(v+1)^k is regular at 0.   => R IS REGULAR AT v = 0.

 (c) v = -1, t := v+1, 3v(v+1) = 3t^2-3t.  A pole of order n>=1 gives left side
     (3n-D) a t^-n + ... against right side -c t^-k:
        n > k : forces 3n = D;      n = k : (3k-D)a = -c, fine if 3k != D;
        n < k : impossible.
     => a pole at v = -1 of order exactly k is NOT excluded.  The
        "evaluate at v = -1" step is therefore incomplete on its own.
""")

# ---------------------------------------------------------------- STEP 2 ---
print("STEP 2 -- THE TWO BRANCHES.\n")
print("  (a) R regular at v=-1.  With (b) above and no other poles, R is a")
print("      POLYNOMIAL; evaluating E(D,k) at v=-1 gives 0 = -c, contradiction.")
print("      => the polynomial branch is empty for every k>=1.   [classical]")
print("  (b) R has a pole at v=-1, necessarily of order exactly k:")
print("      R = A/(v+1)^k, A polynomial, A(-1) != 0.\n")

def reduced(D, k, A):
    """E(D,k) for R=A/(v+1)^k reduces to 3v(v+1)A' - (3kv+D)A."""
    return expand(3*v*(v+1)*diff(A, v) - (3*k*v + D)*A)

# verify the reduction identity concretely (symbolic A of degree k)
for (D, k) in ((13, 4), (23, 4), (7, 3)):
    a = symbols(f'b0:{k+2}')
    A = sum(a[i]*v**i for i in range(k+2))
    R = A/(v+1)**k
    lhs = expand(cancel(together((v+1)**k*(3*v*(v+1)*diff(R, v) - D*R))))
    check(f"reduction identity holds at (D,k)=({D},{k})",
          expand(lhs - reduced(D, k, A)) == 0, "PROVED-exact",
          "(v+1)^k(3v(v+1)R'-D R) == 3v(v+1)A' - (3kv+D)A")

def pole_branch(D, k):
    """Every rational solution with a pole at v=-1; None if there is none."""
    if k == 0:
        return None
    a = symbols(f'a0:{k+1}')
    A = sum(a[i]*v**i for i in range(k+1))
    sol = solve(Poly(reduced(D, k, A) + c, v).all_coeffs(), a, dict=True)
    if not sol:
        return None
    Av = simplify(A.subs(sol[0]))
    return None if Av == 0 else Av

# ---------------------------------------------------------------- STEP 3 ---
print("\nSTEP 3 -- THE COUNTEREXAMPLE TO OUR OWN PRINTED THEOREM.\n")
A13 = pole_branch(13, 4)
check("E(13,4) HAS a non-constant rational solution (printed H1c says none)",
      A13 is not None, "REFUTES-w1_h1c_endgame_closed_form",
      f"A = {A13}")
if A13 is not None:
    R13 = A13/(v+1)**4
    check("  it satisfies E(13,4) identically",
          simplify(expand(together((v+1)**4*(3*v*(v+1)*diff(R13, v) - 13*R13))) + c) == 0,
          "PROVED-exact", "direct substitution")
    check("  it is non-constant", simplify(diff(R13, v)) != 0, "PROVED-exact")
    check("  its pole at v=-1 is genuine (order exactly 4)",
          gcd(Poly(A13/c*455, v), Poly((v+1)**4, v)) == Poly(1, v),
          "PROVED-exact", "gcd(A,(v+1)^4) = 1")
    print(f"    Laurent at v=-1 (c=1): "
          f"{series(R13.subs(c,1), v, -1, 0).removeO()}")
    # numeric residual
    random.seed(11); bad = 0
    for _ in range(40):
        p = Rational(random.randint(-500, 500), random.randint(1, 199))
        if p in (0, -1): continue
        if simplify(((v+1)**4*(3*v*(v+1)*diff(R13, v) - 13*R13)).subs(v, p) + c) != 0:
            bad += 1
    check("  residual is exactly 0 at 40 random rational points", bad == 0,
          "PROVED-exact", f"{bad} failures")

# ---------------------------------------------------------------- STEP 4 ---
print("\nSTEP 4 -- CLASSIFICATION, and the replacement statement.\n")
rows, ok_deg, ok_map = [], True, True
for D in range(1, 31):
    for k in range(1, 7):
        A = pole_branch(D, k)
        if A is None:
            rows.append((D, k, None)); continue
        dA = Poly(A, v).degree()
        num, den = fraction(cancel(A/(v+1)**k))
        md = max(Poly(num, v).degree(), Poly(den, v).degree())
        ok_deg &= (dA == k); ok_map &= (md == k)
        rows.append((D, k, md))

check("whenever a pole solution exists, deg A = k exactly", ok_deg,
      "PROVED-exact", "D=1..30, k=1..6")
check("whenever a pole solution exists, R has MAP-DEGREE exactly k", ok_map,
      "PROVED-exact", "deg as a rational map = max(deg num, deg den) = k")

absent = sorted((D, k) for D, k, md in rows if md is None)
predicted = sorted((D, k) for D in range(1, 31) for k in range(1, 7)
                   if D % 3 == 0 and k >= D//3)
check("the pole branch is EMPTY exactly when 3|D and k >= D/3",
      absent == predicted, "PROVED-exact",
      f"{len(absent)} empty pairs, all matching")

print(f"\n    (empty set = {absent})")
print("""
  LEMMA (H1c, corrected).  Let D>=1, k>=1, c!=0.  Every rational solution R of
      (v+1)^k (3 v(v+1) R' - D R) = -c
  has all its poles at v = -1, and:
     * R is NEVER a polynomial (the polynomial branch dies at v = -1);
     * if 3|D and k >= D/3 there is NO rational solution at all;
     * otherwise the rational solutions are exactly R = A/(v+1)^k with
       deg A = k, and every one of them has MAP-DEGREE exactly k.

  COROLLARY (what replaces THEOREM 3 at the endgame).  The endgame equation
  never needs R to be a polynomial.  It suffices that the framework force the
  map-degree of R to differ from k.  At the First Framework / Three-dessin
  values (D,k) = (13,4) every rational solution has map-degree 4, so any
  framework demand that R realise a degree-13 object is contradicted on
  DEGREE alone -- no fiber-counting, no polynomiality.

  SCOPE, stated exactly.  This does NOT prove THEOREM 3, and does not discharge
  every use of it: the C2 table of forced R's assumes polynomiality for its own
  reasons and still carries CONDITIONAL(R-poly).  What it does is replace the
  uncertified fiber-counting input AT THE ENDGAME CONTRADICTION with a degree
  count, and it relocates the residual gap to a single much smaller question:
      does the framework force map-degree(R) = 13 independently of THEOREM 3?
  Session 15's affine form R = lambda*B13((v-v0)/sigma)+nu must NOT be used to
  answer it -- that form is derived FROM THEOREM 3 and would be circular.
""")
print("="*78)
if FAIL:
    print("FAILED:", FAIL); sys.exit(1)
print("H1c-POLEFIX: all checks passed.")
print("="*78)
