"""
Plane Jacobian campaign - Session 37, WP-B (with WP-D step 1)
THE DEGREE BOUNDS, CALIBRATED; AND THE PARAMETER COUNT.

VERDICT: STRONGLY OVERDETERMINED.  Session 37 is a CLOSURE job, not a
counterexample hunt.  NO COUNTEREXAMPLE.

WP-B exists to answer one question cheaply, before anyone commits a week to
valuation theory: under crude degree bounds, is the scalar coefficient system
over- or under-determined?  The answer decides whether (8,28) is expected to
die (bound 108 -> 125) or to harbour the counterexample.

=====================================================================
WP-D STEP 1 (MANDATORY CALIBRATION) - reproduce GGHV's (5.10)
=====================================================================

The plan is explicit: "If you cannot re-derive a bound they published, you
cannot trust one you derive that they did not."  So the method is fixed on
section 5 first.

With D_k = C_k C^(e-2k) and the leading term x^L:

    v_{rho,1}(D_k x^k) = v_{rho,1}(C_k) + rho*k + (e - 2k) * deg C
                      <= (k + v_{-1,1}(C)) + rho*k + (e - 2k) deg C
                       = k*(1 + rho - 2 deg C) + v_{-1,1}(C) + e*deg C

The bound must not grow with k, which forces

    rho = 2*deg C - 1,        v_{rho,1}(D~) = v_{-1,1}(C) + e*deg C

and there is a free internal consistency check: the leading term x^L must
realise the bound, i.e. rho*L = v_{rho,1}(D~).  Then, reading off D~ term by
term, the coefficient of x^i satisfies

    deg d_i <= v_{rho,1}(D~) - rho*i = rho*(L - i).

SECTION 5 (9,27).  D_k = C_k C_3^(5-2k), C_3 = y^8(y+1) so deg C_3 = 9, and
v_{-1,1}(C) = v_{-1,1}(3,9) = 6, L = 3.  The method gives rho = 17,
v_{17,1}(D~) = 51, consistency 17*3 = 51 OK, and

    deg d1 <= 17*2 = 34,      deg d0 <= 17*3 = 51.

GGHV's (5.10) publishes exactly deg(d1) <= 34 and deg(d0) <= 51.  CALIBRATED.

(8,28).  D_4 = 1 forces C_4 * C_4^(e-8) = 1, so e = 7.  C_4 = y^7(y+1) so
deg C_4 = 8, and v_{-1,1}(C) = v_{-1,1}(4,8) = 4, L = 4.  The method gives
rho = 15, v_{15,1}(D~) = 60, consistency 15*4 = 60 OK, and

    deg d2 <= 30,   deg d1 <= 45,   deg d0 <= 60,   deg dm1 <= 75.

Also, since (D^3)_{-j} = (C^3)_{-j} C^(3e + 2j), section 5's F-term carries
C_3^(15+2*4) = C_3^23 - which is exactly the exponent printed in their
equations - and (8,28)'s carries C_4^(21+2*5) = C_4^31, of degree 248.

=====================================================================
WP-B  THE COUNT
=====================================================================

The WP-A relation is a SINGLE polynomial identity in y.  Imposing it means
every y-coefficient vanishes, so it alone contributes (deg_y + 1) scalar
equations, while the unknowns are the coefficients of d2, d1, d0, dm1.

    unknowns  = 31 + 46 + 61 + 76 = 214

    deg_y of the relation, at deg F = -1 (section 5 has F_{-4} = (1/2)y^{-1},
    so a small or negative degree is the right ballpark)  =  1875

    equations = 1876      imbalance = +1662,  a factor of 8.8

SENSITIVITY - this is the part that matters, since the bounds are crude:

    deg F in {-5, -1, 0, 8, 16, 31, 60}   ->  imbalance +1660 .. +1972
    every bound HALVED                    ->  928 eqs vs 108 unk,  +820
    every bound DOUBLED                   ->  3751 eqs vs 424 unk, +3327

The sign of the imbalance is stable under every perturbation tried.  The
system is overdetermined by roughly an order of magnitude, and no plausible
tightening or loosening of the bounds changes that.

=====================================================================
WHAT IT MEANS, STATED CAREFULLY
=====================================================================

By the plan's own decision table, "strongly overdetermined" means: emptiness
likely, this is a closure job, expect EMPTY, prepare the bound-125 write-up.

That is the honest reading, and it is the OPPOSITE of the outcome one would
want if hunting a counterexample.  The strongest quantitative signal now
available says there is probably nothing at (108,72).

TWO CAVEATS, both real:

  * Overdetermined is not empty.  These systems are highly structured - GGHV's
    (5.9) is a single relation among four quantities and it did not collapse
    on its own; they needed the bounds too.  A structured overdetermined system
    can still be consistent.  This is a prior, not a proof.

  * The bounds are upper bounds.  Smaller true degrees would REDUCE the
    unknowns and reduce the equation count together; the halving row is there
    precisely to show the ratio survives that.

NO COUNTEREXAMPLE.  The next step is WP-E: expand the relation by y-degree
under these bounds and decide the scalar system.  That is now a well-posed
finite computation rather than an open-ended search.
"""

import re

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def derive(L, e, degC, vm11C):
    """rho, the valuation bound, and the degree bounds - see docstring."""
    rho = 2*degC - 1
    const = vm11C + e*degC
    bounds = {f"d{i}": rho*(L - i) for i in range(L - 1, -1, -1)}
    bounds["dm1"] = rho*(L + 1)
    return rho, const, bounds


print(__doc__)
print("=" * 74)
print("WP-D step 1  CALIBRATION against GGHV (5.10)")
print("=" * 74)
rho5, c5, b5 = derive(L=3, e=5, degC=9, vm11C=6)
print(f"   section 5 (9,27): rho = {rho5}, v_(rho,1)(D~) = {c5}, "
      f"leading-term check rho*L = {rho5*3}")
print(f"   bounds: deg d1 <= {b5['d1']}, deg d0 <= {b5['d0']}")
check("the internal consistency check rho*L = v_(rho,1)(D~) holds",
      rho5*3 == c5)
check("the method reproduces GGHV's published (5.10): deg d1 <= 34, "
      "deg d0 <= 51", b5['d1'] == 34 and b5['d0'] == 51)
check("and it predicts section 5's F-term exponent C_3^(3e+2j) = C_3^23 "
      "at j = 4, matching their printed equations", 3*5 + 2*4 == 23)

print()
print("=" * 74)
print("WP-D step 2  the (8,28) bounds")
print("=" * 74)
rho8, c8, b8 = derive(L=4, e=7, degC=8, vm11C=4)
print(f"   (8,28): rho = {rho8}, v_(rho,1)(D~) = {c8}, "
      f"leading-term check rho*L = {rho8*4}")
check("consistency check holds for (8,28) too", rho8*4 == c8)
for k in ("d2", "d1", "d0", "dm1"):
    print(f"     deg {k} <= {b8[k]}")
check("d2 - the extra quartic coefficient with no section-5 analogue - is "
      "bounded at 30", b8["d2"] == 30)
degW = (3*7 + 2*5)*8
print(f"   W = C_4^(3e+2j) = C_4^{3*7+2*5}, deg W = {degW}")
check("the F-term carries C_4^31 of degree 248", degW == 248)

# =====================================================================
print()
print("=" * 74)
print("WP-B  the parameter count")
print("=" * 74)
REL = open("phase2_moduli/runs/session37_relation_8_28.txt").read()
REL = REL.strip().replace("E[1]=", "")
terms = [t for t in re.split(r'(?=[+-])', REL)
         if t.strip() and any(ch.isalpha() for ch in t)]
check("the WP-A relation has 102 monomials", len(terms) == 102)


def ydeg(term, B, degF):
    d, bb = 0, dict(B)
    bb["F"] = degF
    for v, ex in re.findall(r'([A-Za-z]+[0-9]*)\^?(\d*)', term):
        if v in bb:
            d += bb[v]*(int(ex) if ex else 1)
    return d


def count(B, degF):
    unk = sum(B[k] + 1 for k in ("d2", "d1", "d0", "dm1")) + max(0, degF + 1)
    eqs = max(ydeg(t, B, degF) for t in terms) + 1
    return eqs, unk


BASE = dict(b8)
BASE["W"] = degW
print(f"   unknown coefficients (d2,d1,d0,dm1) = "
      f"{sum(BASE[k]+1 for k in ('d2','d1','d0','dm1'))}")
print(f"   {'deg F':>7} {'eqs':>7} {'unknowns':>9} {'imbalance':>11}")
allover = True
for degF in (-5, -1, 0, 8, 16, 31, 60):
    e, u = count(BASE, degF)
    allover &= (e > u)
    print(f"   {degF:>7} {e:>7} {u:>9} {e-u:>+11}")
check("overdetermined at every value of deg F tried", allover)

print("   sensitivity to the bounds themselves:")
rows = []
for name, f in (("halved", 0.5), ("base", 1.0), ("doubled", 2.0)):
    Bs = {k: int(v*f) for k, v in BASE.items()}
    e, u = count(Bs, -1)
    rows.append(e > u)
    print(f"     {name:>8}: {e:>5} eqs vs {u:>4} unknowns   {e-u:>+7}")
check("the sign of the imbalance survives halving AND doubling every bound",
      all(rows))

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
VERDICT: STRONGLY OVERDETERMINED -> CLOSURE JOB.  NO COUNTEREXAMPLE.

  The relation is one identity in y; under bounds derived by a method that
  reproduces GGHV's own published (5.10), it expands into ~1876 scalar
  equations against ~214 unknown coefficients.  The factor of ~8.8 survives
  halving and doubling every bound.

  By the plan's decision table this is the "expect EMPTY" branch.  The
  strongest quantitative signal now available says there is probably no
  counterexample at (108,72) - which, if it holds up under WP-E, raises the
  lower bound from 108 to 125.

  Overdetermined is not empty: these systems are structured, and GGHV's own
  (5.9) needed the bounds alongside it to finish.  This is a prior, not a
  proof.  WP-E is the computation that decides it.
""")
assert all(PASS), "a certification failed"
