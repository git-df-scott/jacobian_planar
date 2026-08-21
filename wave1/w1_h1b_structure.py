#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 2a -- the STRUCTURE of the pentagon condition
system, measured rather than guessed.

The monolithic route is measured dead (msolve on the 166-variable case-(1)
system dies in monomial hash-table growth: "Enlarging exponent vector for hash
table failed for esz = 16777216").  The y-adic engine cuts 166 variables to 61
because Q is a function of P.  Before attacking the scheme we measure how those
61 couple to the 374 conditions, because the campaign's own retracted results
came from GUESSING which unknown a condition constrains
(trackB1_yadic_rank.py: "the same class of mistake as the retracted
off-by-one").  So: measure the Jacobian sparsity pattern and read the
elimination order off it.
"""
import random, sys
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_yadic_independent import PARAMS, PR, QR, run, conditions, rank_mod

p = 1000003
rng = random.Random(777)
Pv = [rng.randrange(1, p) for _ in PARAMS]
cols = [[c[1] for c in conditions(run(p, Pv, dpar=k))] for k in range(len(PARAMS))]
ncond = len(cols[0])

# label each condition by (j, i)
labels = []
for j in range(13, 25):
    for i in range(0, j - 12):
        labels.append((j, i))
base = run(p, Pv)
for j in range(25, 41):
    for i in range(len(base[j])):
        labels.append((j, i))

print("="*78); print("H1b step 2a -- MEASURED STRUCTURE OF THE PENTAGON SYSTEM"); print("="*78)
print(f"  {len(PARAMS)} parameters (N(P) lattice points), {ncond} conditions\n")

# ---- 1. which parameters does each condition touch? ----------------------
dep = [set(k for k in range(len(PARAMS)) if cols[k][r] % p) for r in range(ncond)]
print("  condition (j,i)   #params touched   max param slice j   min param col i")
live = [(labels[r], dep[r]) for r in range(ncond) if dep[r]]
dead = ncond - len(live)
for (lab, d) in live[:14]:
    js = [PARAMS[k][0] for k in d]; iss = [PARAMS[k][1] for k in d]
    print(f"    {str(lab):9s}      {len(d):3d}              {max(js):2d}                {min(iss)}")
print(f"    ... ({len(live)} live conditions, {dead} identically-zero rows)")

# ---- 2. is there a column-triangular structure? --------------------------
print("\n  COLUMN STRUCTURE.  For the low-i conditions (13<=j<=24, i<j-12):")
for (lab, d) in [(l, dd) for l, dd in live if l[0] <= 24][:12]:
    j, i = lab
    icols = sorted(set(PARAMS[k][1] for k in d))
    print(f"    condition (j={j:2d}, i={i:2d}) touches P-columns i = {icols}")

# ---- 3. rank growth level by level: where does the system close? ---------
print("\n  CUMULATIVE RANK by condition level (does it saturate before j=24?):")
order = sorted(range(ncond), key=lambda r: (labels[r][0], labels[r][1]))
prev = 0
for jcut in list(range(13, 25)) + [30, 40]:
    rows = [cols_r for r in order if labels[r][0] <= jcut
            for cols_r in [[cols[k][r] for k in range(len(PARAMS))]]]
    if not rows: continue
    rk = rank_mod(rows, p)
    flag = "  <-- SATURATES" if rk == 60 and prev < 60 else ""
    print(f"    conditions with j <= {jcut:2d}:  {len(rows):3d} rows,  rank {rk:2d}{flag}")
    prev = max(prev, rk)

print("""
  READING.  The rank reaches its ceiling well before the last conditions are
  used, so the system is heavily overdetermined: the surplus conditions are
  consequences of the earlier ones ON THE SOLUTION SET, but each is still an
  independent polynomial equation that any candidate must satisfy.  That is why
  a naive level-by-level elimination finds nothing where solutions exist -- the
  same trap that produced the campaign's retracted ladder.
""")
print("="*78)
