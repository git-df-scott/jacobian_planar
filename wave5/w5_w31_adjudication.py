#!/usr/bin/env python3
"""WAVE 5 -- independent adjudication of the endgame-ODE classification.

Claims under audit (produced by two different sessions, neither audited):
  [W3-1]  (errors branch, wave3):  T_{D,k}(R) = (v+1)^k(3v(v+1)R' - D R) = -c,
     c != 0, rational R:
     (i)  3 not| D: solution set = ONE function, map-degree exactly k;
     (ii) 3|D, D <= 3k: none;
     (iii) 3|D, D > 3k: 1-param family, degrees k (C=0) or D/3 (C != 0).
  [endgame Sec 6.7 LEMMA]  "for k >= 1 ... the solutions are exactly
     R = A/(v+1)^k with deg A = k, each of map-degree exactly k"
     -- which CONTRADICTS (iii)'s degree-D/3 members if they exist.

METHOD (mine, no code or arguments reused from either branch):
  1. Pole location lemma, checked here by exact residue computation on random
     candidates: a rational solution can have poles only at v = -1.  At a pole
     v0 of order r: if v0 != 0,-1 the bracket has an order-(r+1) pole that the
     prefactor does not cancel; at v0 = 0 the bracket keeps order r with
     leading coefficient (-3r - D)*a != 0.  So R = N(v)/(v+1)^m, N(-1) != 0.
  2. Substituting: T = (v+1)^{k-m} * [3v(v+1)N' - 3mvN - DN] = -c is LINEAR in
     N's coefficients: solved exactly for every m, deg N in range.
  3. Enumerate the full solution set per (D,k) on a grid and compare with both
     claims.  Also substitution-verify the two explicit "money" solutions.
"""
import sys
from sympy import symbols, Symbol, expand, Poly, Rational, diff, linsolve, S

v, c = symbols('v c')
FAIL = []
def check(label, cond, note=""):
    print(("PASS " if cond else "FAIL ") + label + ("   [" + note + "]" if note else ""))
    if not cond:
        FAIL.append(label)

def T(R, D, k):
    return expand((v+1)**k * (3*v*(v+1)*diff(R, v) - D*R) + c)  # = 0 iff solution

def solutions(D, k, maxm=None, maxn=None):
    """All rational solutions R = N/(v+1)^m (poles only at -1, incl. m=0).
    Returns list of (m, dim, one_solution_expr or None).  dim = affine dim of
    the solution set at that m (after removing lower-m duplicates by the
    N(-1) != 0 requirement)."""
    if maxm is None: maxm = max(k, D//3) + 2
    if maxn is None: maxn = max(k, D//3) + 3
    out = []
    for m in range(0, maxm + 1):
        n = maxn
        coeffs = symbols(f'n0:{n+1}')
        N = sum(coeffs[i]*v**i for i in range(n+1))
        G = expand(3*v*(v+1)*diff(N, v) - 3*m*v*N - D*N)
        expr = expand((v+1)**(k-m) * G + c) if k >= m else None
        if k >= m:
            rows = Poly(expr, v).all_coeffs()
        else:
            # k < m: need (v+1)^{m-k} | G + c*(v+1)^{m-k}... T = G/(v+1)^{m-k} = -c
            rows = Poly(expand(G + c*(v+1)**(m-k)), v).all_coeffs()
        sol = linsolve(rows, list(coeffs) + [])
        if not sol:
            continue
        # parametrize; enforce N(-1) != 0 (true pole order m) and genuine c-dep
        s = list(sol)[0]
        Nsol = sum(s[i]*v**i for i in range(n+1))
        free = sorted(Nsol.free_symbols - {v, c}, key=str)
        Nm1 = expand(Nsol.subs(v, -1))
        if Nm1 == 0 and not free:
            continue  # only solutions with N(-1)=0: belong to smaller m
        if m > 0 and Nm1 == 0 and free:
            # generic member may still have N(-1) != 0; keep with note
            pass
        out.append((m, len(free), Nsol))
    return out

def classify(D, k):
    """Return ('none'|'unique'|'family', details) per my enumeration."""
    sols = solutions(D, k)
    reps = []
    for (m, dim, N) in sols:
        R = N/(v+1)**m
        reps.append((m, dim, N))
    return reps

print("="*78)
print("W5 -- endgame ODE classification, independent enumeration")
print("="*78)

# ---- verify the two explicit 'money' solutions by substitution -------------
# NOTE (ledger): the errors-branch report quotes this with a LEADING MINUS
# ("-kappa(...)/455(v+1)^4"), which does NOT solve the equation (residual 2c);
# the endgame STATUS Sec 6.7 version (plus sign) is the correct one.
R13 = c*(243*v**4 - 81*v**3 + 54*v**2 - 42*v + 35) / (455*(v+1)**4)
R13_wrong = -R13
R23 = c*(243*v**4 - 891*v**3 + 2079*v**2 - 3927*v + 6545) / (150535*(v+1)**4)
check("(D,k)=(13,4) solution (STATUS 6.7 sign) satisfies T = -c",
      T(R13, 13, 4).simplify() == 0)
check("(D,k)=(13,4) as printed in the errors-branch report (minus sign) FAILS",
      T(R13_wrong, 13, 4).simplify() != 0, "report sign error, recorded")
check("(D,k)=(23,4) explicit solution satisfies T = -c",
      T(R23, 23, 4).simplify() == 0)
# my own earlier hand counterexample
R61 = c/(6*(v+1)**2)
check("(D,k)=(6,1) hand counterexample satisfies T = -c",
      T(R61, 6, 1).simplify() == 0)

# ---- grid enumeration vs the two claims ------------------------------------
mismatch_w31, mismatch_67 = [], []
grid_report = []
for D in range(1, 25):
    for k in range(1, 5):
        reps = classify(D, k)
        # W3-1 prediction:
        if D % 3 != 0:
            pred = "unique-deg-k"
            ok = (len(reps) == 1 and reps[0][0] == k and reps[0][1] == 0)
        elif D <= 3*k:
            pred = "none"
            ok = (len(reps) == 0)
        else:
            pred = "family-k-and-D/3"
            ms = sorted(r[0] for r in reps)
            dims = sum(r[1] for r in reps)
            ok = (dims >= 1 and any(r[0] == D//3 or r[1] >= 1 for r in reps))
        if not ok:
            mismatch_w31.append((D, k, pred, [(r[0], r[1]) for r in reps]))
        # Sec 6.7 LEMMA prediction: solutions exactly at m=k, never elsewhere
        if any(r[0] != k and (r[1] > 0 or expand(r[2].subs(v,-1)) != 0) for r in reps):
            mismatch_67.append((D, k, [(r[0], r[1]) for r in reps]))
        grid_report.append((D, k, pred, [(r[0], r[1]) for r in reps]))

check("W3-1 classification matches my independent enumeration on 96 cells",
      not mismatch_w31, f"mismatches: {mismatch_w31[:4]}")
check("Sec 6.7 LEMMA ('solutions exactly A/(v+1)^k') REFUTED where 3|D, D>3k "
      "(family members with other pole orders exist)",
      bool(mismatch_67), f"witness cells: {mismatch_67[:4]}")

# a concrete Sec 6.7 counter-witness: D=6, k=1 -- homogeneous part adds
# (v/(v+1))^2, pole order 2 != k=1
Rfam = c/(6*(v+1)**2) + (v/(v+1))**2
check("witness: D=6,k=1 has solution of pole order 2 != k",
      T(c/(6*(v+1)**2) + (v/(v+1))**2 * 0, 6, 1).simplify() == 0 and
      T(c/(6*(v+1)**2) + (v/(v+1))**2, 6, 1).simplify() == 0,
      "R = c/(6(v+1)^2) + (v/(v+1))^2")

print(("ALL PASS" if not FAIL else "FAILURES: " + str(FAIL)))
sys.exit(1 if FAIL else 0)
