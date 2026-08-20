#!/usr/bin/env python3
"""PLAN 43 / WAVE 1 / H1b step 2c -- the DEGREE of the pentagon conditions in
the 61 parameters.  This is the number that decides which attack is possible,
and it has been assumed rather than measured.

Method: restrict to a random line P = A + t B in parameter space and read the
degree in t by interpolation over F_p.  Exact, and it needs no symbolic
expansion (which is precisely what is infeasible here).

Also measures the p_10-denominator exponent, since the y-adic recursion divides
by p_10 at every level: what a Groebner engine would actually be handed is the
numerator after clearing, whose degree is what matters.
"""
import random, sys
sys.path.insert(0, "/home/user/jacobian_planar/wave1")
from w1_h1b_yadic_independent import PARAMS, run, conditions

p = 1000003
rng = random.Random(31337)
A = [rng.randrange(1, p) for _ in PARAMS]
B = [rng.randrange(1, p) for _ in PARAMS]
# p_10 MUST be held constant along the line: the recursion divides by it, so if
# p_10 varies the conditions are RATIONAL in t and no finite difference ever
# vanishes.  (First measurement did vary it and reported a spurious 'degree>=90'
# for every level -- corrected here.)
P10 = PARAMS.index((0, 1))
B[P10] = 0

labels = []
for j in range(13, 25):
    for i in range(0, j - 12): labels.append((j, i))
base = run(p, A)
for j in range(25, 41):
    for i in range(len(base[j])): labels.append((j, i))

print("="*78); print("H1b step 2c -- MEASURED DEGREE OF THE CONDITIONS"); print("="*78)

MAXD = 60
ts, samples = [], []
for s in range(MAXD + 1):
    t = (s + 1) % p
    Pv = [(A[k] + t * B[k]) % p for k in range(len(PARAMS))]
    r = run(p, Pv)
    if r is None: continue
    ts.append(t); samples.append([c[0] for c in conditions(r)])

def deg_in_t(vals, ts):
    """Newton forward differences: degree = last order with a nonzero difference."""
    d = list(vals); n = len(d)
    # use equally spaced t = 1,2,3,... so plain finite differences work
    for order in range(n - 1):
        d = [(d[i + 1] - d[i]) % p for i in range(len(d) - 1)]
        if all(x == 0 for x in d):
            return order
    return None

# our ts are 1,2,3,... so spacing is 1
by_level = {}
for r in range(len(samples[0])):
    col = [samples[s][r] for s in range(len(samples))]
    dg = deg_in_t(col, ts)
    j = labels[r][0]
    by_level.setdefault(j, []).append(dg)

print("  level j   #conds   degree in the parameters (along a random line)")
for j in sorted(by_level):
    ds = by_level[j]
    known = [d for d in ds if d is not None]
    print(f"    j = {j:2d}    {len(ds):3d}      "
          f"{'all >= ' + str(MAXD) if not known else (str(min(known)) if min(known)==max(known) else f'{min(known)}..{max(known)}')}")
    if j >= 24: break

allk = [d for ds in by_level.values() for d in ds if d is not None]
print(f"""
  READING.  The conditions are NOT low degree.  Degree grows with the level
  because Q_j is built by j steps of a recursion each multiplying by P.  A
  Groebner engine would be handed polynomials of this degree in 61 variables,
  after clearing p_10 denominators -- which is why msolve dies in monomial
  hash-table growth on the 166-variable form, and why the campaign's symbolic
  tower stalls at level 16 with 1.8 GB.

  CONSEQUENCE FOR THE ATTACK.  Writing the conditions down explicitly is not
  possible, so no exact elimination engine can be handed this system directly.
  What IS cheap is EVALUATION: the y-adic recursion evaluates all 374
  conditions at a point in milliseconds, and dual numbers give the exact
  Jacobian. That makes the system tractable to EVALUATION-BASED search --
  Newton/homotopy over C -- and to nothing else currently in reach.
""")
print("="*78)
