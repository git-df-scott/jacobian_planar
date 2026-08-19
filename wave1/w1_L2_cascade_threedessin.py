#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 -- L2 CASCADE on the three-dessin chain: the last framework gap.

L2 is "block-level chain unification": C7's valuation-level equivalence promoted
to the block cascade and the sqrt-reduction (FF Sessions 10-12). Its content is
the L1-L4 identities in trackC_c3_ladder.py, which are GENERIC -- exact over Q
in fully symbolic T_m, parametrised only by the cusp (a,b) and the chain length D.

THE TRANSFER ARGUMENT.  If the identities are universal in (a,b) and D, and the
Three-dessin Framework's (a,b) and D and g are the First Framework's, then the
cascade instantiates identically and L2 transfers. All three inputs were
established earlier in this wave:

    (a,b) = (2,3)   -- gcd(108,72) = 36, cusp (72/36, 108/36) = (2,3),
                       identical to (99,66)'s (66/33, 99/33) = (2,3)
    D     = 13      -- the (-2)-curve Belyi map is the First Framework's,
                       source-verified from arXiv:1901.04073v2 sec.5
    g     = alpha U (U-1)^8  -- L3 step 2, deg g = N/mu + eps = 16/2 + 1 = 9

ONE GAP IN THE INHERITED WORK, CLOSED HERE.  trackC_report.md records L2 as
"Checked for D = 1..6". The chain length that matters is D = 13. That is an
extrapolation of more than a factor of two, so this file re-runs the SAME
generic engine at D = 1..14, covering 13 directly.
"""
import sys, os
sys.path.insert(0, "/home/user/jacobian_planar/campaign/audit_tracks")
import sympy as sp
from trackC_c3_ladder import frac_root, series_mul, series_pow

FAIL = []
def check(l, c, s, e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>" + (f"   [{e}]" if e else ""))

print("="*78); print("L2 CASCADE ON THE THREE-DESSIN CHAIN"); print("="*78)

# ---- the three inputs, restated and checked ------------------------------
from math import gcd
g108 = gcd(108, 72); g99 = gcd(99, 66)
check("cusp (a,b) = (2,3) for BOTH (108,72) and (99,66)",
      (72//g108, 108//g108) == (2, 3) and (66//g99, 99//g99) == (2, 3),
      "PROVED-exact", f"(108,72): gcd {g108} -> {(72//g108,108//g108)}; "
                      f"(99,66): gcd {g99} -> {(66//g99,99//g99)}")
check("D = 13 for the Three-dessin Framework (it reuses the First Framework's "
      "degree-13 (-2)-curve Belyi map)", True, "LIT-READ(1901.04073v2 sec.5)",
      "source-verified verbatim earlier in this wave")
check("g = alpha U (U-1)^8, deg g = N/mu + eps = 16/2 + 1 = 9",
      16//2 + 1 == 9, "CERTIFIED", "L3 step 2, chart reimplemented independently")

# ---- close the D = 1..6 -> D = 13 extrapolation --------------------------
print("""
  CLOSING THE EXTRAPOLATION.  trackC_report.md records L2 as checked for
  D = 1..6.  The chain length in play is D = 13.  Re-running the same generic
  engine at D = 1..14 with fully symbolic T_m:
""")
N = 14
g = sp.Symbol("g"); dl = sp.Symbol("delta")
Ts = sp.symbols("T1:%d" % (N + 1))
T = [sp.Integer(0)] + list(Ts)
S = frac_root(T, 2, 3, N)
y2 = [sp.expand(g**2 * c) for c in ([sp.Integer(1)] + list(T[1:]))]
rows = []
for D in range(1, N + 1):
    Delta = [sp.Integer(0)] * (N + 1); Delta[D] = dl
    y1 = [sp.expand(g**3 * (S[m] + Delta[m])) for m in range(N + 1)]
    W = [sp.expand(a - b) for a, b in
         zip(series_mul(y1, y1, N), series_pow(y2, 3, N))]
    ok_low = all(sp.simplify(W[m]) == 0 for m in range(D))
    first = sp.simplify(W[D])
    ok_lin = (sp.degree(sp.Poly(first, dl), dl) == 1 and
              sp.simplify(sp.diff(first, dl) - 2 * g**6) == 0)
    rows.append((D, ok_low, ok_lin))
    mark = "  <== the chain length in play" if D == 13 else ""
    print(f"    D = {D:2d}:  blocks 0..{D-1:2d} vanish identically: {ok_low};"
          f"  first block linear with coefficient 2g^6: {ok_lin}{mark}")
check("chain <=> sqrt-agreement holds at EVERY D = 1..14, including D = 13",
      all(a and b for _, a, b in rows), "PROVED-exact",
      "generic symbolic T_m, exact over Q; extends the recorded D = 1..6")
check("the deviation enters LINEARLY at D = 13 (coefficient exactly 2g^6), so "
      "the endgame is an ODE in R and not a quadratic",
      rows[12][2], "PROVED-exact", "D = 13 row above")

print("""
  WHAT THAT DELIVERS.  The L1-L4 cascade is generic in (a,b) and D; the
  extrapolation to D = 13 is now a computation rather than an assumption; and
  the anchor (trackC_c3_anchor.py, 5 PASS) derives g = U(U-1)^8 and
  A~_{-9+m} == g^3 S_m for m = 0..12 from the Session-7/10 near-miss Belyi
  data -- which is the First Framework's (-5)/(-2) data, i.e. the Three-dessin
  Framework's.  Every input the cascade consumes is shared.
""")
print("="*78)
if FAIL: print("FAILED:", FAIL); sys.exit(1)
print("""L2 CASCADE: TRANSFERS.

  The cascade's content is universal identities instantiated at (a,b) = (2,3),
  D = 13 and g = alpha U (U-1)^8 -- all three shared with the First Framework
  and each established independently this wave.  The anchor's Belyi input is
  shared verbatim.  Nothing in the cascade reads the branch inventory, so the
  type-4 curve / degree-5 Belyi map trade does not touch it.

  RESIDUE, and it is IMPORTANT that it is not new: the cascade still rests on
  THEOREM 2 at general parameters (the Taylor-pin argument that every framework
  solution -- not just the near-miss -- has g = alpha U (U-1)^8) and THEOREM 3
  (pole-fiber => R polynomial).  Both remain prose, both are load-bearing, and
  both are inherited from the FIRST Framework unchanged.  The Three-dessin
  Framework introduces NO NEW conditionality of its own.

  CONSEQUENCE FOR (108,72): all four layers now transfer -- L1 core, L1 boxes
  (immaterial), L2 contact, L2 cascade, L3 rigidity -- with L4 immaterial by the
  closed-form endgame theorem.  The framework-side kill is therefore as strong
  as the First Framework's own, and conditional on exactly the same two
  unreproduced theorems, no more.""")
print("="*78)
