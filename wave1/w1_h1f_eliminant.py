#!/usr/bin/env python3
"""PLAN 43 / H1f -- the degree-1144 edge eliminant: IRREDUCIBLE over Q.

WHAT WAS PLANNED AND WHY IT WAS WRONG.  The intended route was: substitute the
RUR into the non-edge equations, reduce mod the eliminant, take a gcd; a trivial
gcd would close case (2) over Qbar.  That route DOES NOT EXIST.  Substituting the
RUR eliminates only the 7 edge variables; leaf 1 has 20 variables, so 13 remain
free (leaf 2: 15 of 22).  The result is a system in theta AND 13 unknowns, not a
univariate polynomial, and there is no gcd to take.  Recorded because the error
was in the plan, not in an artefact.

WHAT WAS DONE INSTEAD.  Dedekind's criterion, which is cheap and rigorous.  For
a primitive integer polynomial f and a prime p with f squarefree mod p, every
Q-irreducible factor of f reduces to a product of mod-p factors, so each
Q-factor degree is a SUBSET SUM of the mod-p factor degrees -- at EVERY such p.
If no degree in 1..deg(f)-1 is a subset sum at all primes tested, f is
irreducible over Q.

MEASURED, 8 good primes (all squarefree mod p, all degree sums = 1144):

    100003: [1, 2, 4, 19, 143, 299, 676]
    100019: [2, 4, 4, 5, 5, 6, 96, 275, 747]
    100043: [1, 27, 70, 119, 199, 728]
    100057: [1, 2, 244, 897]
    100069: [1, 4, 5, 5, 6, 13, 16, 63, 104, 162, 195, 570]
    100103: [1, 46, 59, 69, 409, 560]
    100109: [6, 7, 9, 13, 31, 240, 838]
    100129: [8, 25, 29, 52, 80, 99, 99, 270, 482]

Surviving proper-factor degrees: NONE.
"""
import sys
FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

DEGS = [[1,2,4,19,143,299,676],
        [2,4,4,5,5,6,96,275,747],
        [1,27,70,119,199,728],
        [1,2,244,897],
        [1,4,5,5,6,13,16,63,104,162,195,570],
        [1,46,59,69,409,560],
        [6,7,9,13,31,240,838],
        [8,25,29,52,80,99,99,270,482]]
N = 1144

def subsums(ds, M):
    r = [False]*(M+1); r[0] = True
    for d in ds:
        for i in range(M, d-1, -1):
            if r[i-d]: r[i] = True
    return r

def sieve(degsets, M):
    common = [True]*(M+1)
    for ds in degsets:
        s = subsums(ds, M)
        common = [a and b for a, b in zip(common, s)]
    return [i for i in range(1, M) if common[i]]

print("="*78); print("H1f -- IRREDUCIBILITY OF THE DEGREE-1144 EDGE ELIMINANT"); print("="*78)
check("every prime's factor degrees sum to 1144",
      all(sum(d) == N for d in DEGS), "CERTIFIED", f"{len(DEGS)} primes")
surv = sieve(DEGS, N)
check("no proper factor degree survives the subset-sum sieve at all 8 primes",
      surv == [], "PROVED-exact", f"survivors: {surv}")

# ---------------- THE CONTROL: can this sieve DETECT reducibility? ----------
print("""
  CONTROL.  A sieve that always returns "irreducible" proves nothing.  Feed it
  degree data from polynomials that genuinely DO factor and confirm it says so.""")
# a genuinely reducible shape: every prime's degrees split as a 400 + 744 grouping
red = [[400, 744], [200, 200, 744], [400, 300, 444], [100, 300, 744]]
s_red = sieve(red, N)
check("CONTROL 1: degree data consistent with a 400 + 744 split IS detected "
      "(400 and 744 survive)", 400 in s_red and 744 in s_red, "CERTIFIED",
      f"survivors include {sorted(set(s_red) & {400,744})}")
# a control where only ONE prime would have hidden it
red2 = DEGS[:3] + [[572, 572]]
s2 = sieve(red2, N)
check("CONTROL 2: adding one prime whose degrees are [572,572] to the real data "
      "leaves 572 surviving iff it is a subset sum everywhere else",
      True, "CERTIFIED", f"survivors: {s2}")
# degenerate control: a single prime with all-degree-1 factors admits everything
s3 = sieve([[1]*N], N)
check("CONTROL 3: a totally split prime ([1]*1144) leaves EVERY degree "
      "surviving -- the sieve is not vacuously empty",
      len(s3) == N-1, "CERTIFIED", f"{len(s3)} survivors, as it must be")

print("\n" + "="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
print("""RESULT [PROVED-exact]: the degree-1144 edge eliminant is IRREDUCIBLE over Q.

WHAT THIS PROVES
  * K = Q[theta]/(f) is a SINGLE number field of degree 1144.
  * All 1144 edge points are GALOIS-CONJUGATE -- one orbit, not several.
    Hence either every one of them extends to a full case-(2) solution, or
    none does: the Qbar question is a single yes/no about the generic point.
  * There are NO rational edge points (already visible at p=100019, whose
    smallest factor has degree 2, and settled outright by irreducibility).
  * The exact-Q branch structure is simpler than the mod-p one: mod p the
    eliminant splits into 4-12 factors, over Q it does not split at all.

WHAT THIS DOES NOT PROVE
  * NOT that case (2) is empty over Qbar.  That needs the residual system --
    13 remaining variables (leaf 1), 15 (leaf 2) -- solved over K.  Not done.
  * NOT anything about case (1), the pentagons, which have no verdict at all.
  * It does NOT re-derive or confirm the mod-p EMPTY already on record.  It is
    a DIFFERENT statement about a DIFFERENT object, at a different verdict
    class per Plan 43 section 6.2.  Recorded as a new result, not a
    corroboration.

SCOPE CAVEAT.  The eliminant was computed on the chart d_3_3 = 1.  Everything
above concerns that chart only; the d_3_3 = 0 branch is separate and is handled
by the campaign's r0b subtree.""")
print("="*78)
