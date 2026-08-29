"""
SELF-TEST of the case-(2) machinery in wave4/.

Everything downstream (Item 1's verdicts, T3's symmetry slices) depends on four
structural facts about campaign/audit_tracks/trackA_system_case2.json.  None of
them is assumed anywhere: they are checked here, each with a negative control
that is REQUIRED to fail.

  S1  the weight grading w = j - 2i splits the 92 equations into blocks
      involving exactly the predicted pieces of P and Q;
  S2  the three-parameter gauge  c_i_j -> a mu^i nu^j c_i_j,
      d_i_j -> b mu^i nu^j d_i_j,  b = 1/(a mu^3 nu)  is an exact symmetry:
      every equation value scales by a*b*mu^(i+1)*nu^(j+1);
  S3  the gauge fixings used by w4_c2_full.py really do rigidify --- the 3x3
      exponent determinants are nonzero --- and the chart split d_3_3 = 1 or 0
      is exhaustive because the subgroup fixing d_2_1 and c_8_16 still moves
      d_3_3 with a nonzero weight;
  S4  the triangular elimination of c_1..c_8 in w4_c2_reduce.py reproduces the
      w = -4 block exactly: the first 8 equations vanish identically after the
      solve, and the remaining 9 agree with the exported residual polynomials.
"""

import os
import random
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_case2_system as S
import w4_c2_build as B
import w4_c2_reduce as RED

RESULTS = []
P = 1000003          # p = 1 (mod 3)


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)

print("=" * 78)
print("SELF-TEST -- the case-(2) machinery")
print("=" * 78)
print(f"  source: trackA_system_case2.json  hash {CHASH}")
print(f"  {len(VARS)} variables, {len(EQS)} equations, nonzero {NONZERO}")

# --- S1 --------------------------------------------------------------------
LETTER = {}
for v in VARS:
    w = S.var_weight(v)
    if v.startswith("c_"):
        LETTER[v] = {0: "A", -1: "B", -2: "C"}[w]
    else:
        LETTER[v] = {0: "D", -1: "E", -2: "F", -3: "G"}[w]
EXPECT = {-4: {"C", "G"}, -3: {"B", "C", "F", "G"},
          -2: {"A", "B", "C", "E", "F", "G"},
          -1: {"A", "B", "C", "D", "E", "F"}, 0: {"A", "B", "D", "E"}}
seen = {}
for w, idxs in BYW.items():
    L = set()
    for k in idxs:
        for v in S.eq_vars(EQS[k]):
            L.add(LETTER[v])
    seen[w] = L
check("S1  each weight block involves exactly the predicted pieces",
      seen == EXPECT, f"{ {k: sorted(v) for k, v in sorted(seen.items())} }")
# negative control: a scrambled letter map must break S1
SCR = dict(LETTER)
for v in VARS:
    if SCR[v] == "G":
        SCR[v] = "D"
seen2 = {}
for w, idxs in BYW.items():
    seen2[w] = {SCR[v] for k in idxs for v in S.eq_vars(EQS[k])}
check("S1n NEGATIVE: a scrambled piece-assignment is detected", seen2 != EXPECT)

# --- S2 --------------------------------------------------------------------
def gauge_point(pt, a, mu, nu, p):
    b = pow(a * pow(mu, 3, p) % p * nu % p, p - 2, p)
    out = {}
    for v in VARS:
        _, i, j = v.split("_")
        i, j = int(i), int(j)
        s = a if v.startswith("c_") else b
        out[v] = s * pow(mu, i, p) % p * pow(nu, j, p) % p * pt[v] % p
    return out, b


rnd = random.Random(20260820)
bad, badn = 0, 0
for trial in range(6):
    pt = {v: rnd.randrange(1, P) for v in VARS}
    a = rnd.randrange(1, P); mu = rnd.randrange(1, P); nu = rnd.randrange(1, P)
    pt2, b = gauge_point(pt, a, mu, nu, P)
    for k, eq in enumerate(EQS):
        i, j = eq["bracket_point"]
        terms = S.eq_terms(eq)
        v1 = B.eval_terms(terms, pt, P)
        v2 = B.eval_terms(terms, pt2, P)
        fac = a * b % P * pow(mu, i + 1, P) % P * pow(nu, j + 1, P) % P
        if (v2 - fac * v1) % P != 0:
            bad += 1
        badfac = a * b % P * pow(mu, i + 2, P) % P * pow(nu, j + 1, P) % P
        if (v2 - badfac * v1) % P != 0:
            badn += 1
check("S2  the three-parameter gauge is an exact symmetry of all 92 equations "
      "at 6 random points", bad == 0, f"{bad} mismatches")
check("S2n NEGATIVE: a wrong mu-exponent in the predicted factor is detected",
      badn > 0, f"{badn} of {6 * len(EQS)} equations reject the wrong factor")

# --- S3 --------------------------------------------------------------------
def expvec(v):
    """(a, mu, nu) exponents of the gauge action on the variable v."""
    _, i, j = v.split("_")
    i, j = int(i), int(j)
    if v.startswith("c_"):
        return (1, i, j)
    return (-1, i - 3, j - 1)          # b = a^-1 mu^-3 nu^-1


def det3(r1, r2, r3):
    return (r1[0] * (r2[1] * r3[2] - r2[2] * r3[1])
            - r1[1] * (r2[0] * r3[2] - r2[2] * r3[0])
            + r1[2] * (r2[0] * r3[1] - r2[1] * r3[0]))


d_one = det3(expvec("d_2_1"), expvec("c_8_16"), expvec("d_3_3"))
d_zero = det3(expvec("d_2_1"), expvec("c_8_16"), expvec("d_12_24"))
check("S3a chart d_3_3=1: (d_2_1, c_8_16, d_3_3) rigidifies the gauge",
      d_one != 0, f"det = {d_one}")
check("S3b chart d_3_3=0: (d_2_1, c_8_16, d_12_24) rigidifies the gauge",
      d_zero != 0, f"det = {d_zero}")
check("S3c the two extra gauge variables are nonzero conditions, so fixing "
      "them is a gauge fixing and not a case split",
      "d_2_1" in NONZERO and "c_8_16" in NONZERO and "d_12_24" in NONZERO)
check("S3d d_3_3 is NOT a nonzero condition, so d_3_3 = 1 or 0 is exhaustive",
      "d_3_3" not in NONZERO)
# the residual 1-parameter subgroup fixing d_2_1 and c_8_16 must move d_3_3
r1, r2, r3 = expvec("d_2_1"), expvec("c_8_16"), expvec("d_3_3")
ker = (r1[1] * r2[2] - r1[2] * r2[1],
       -(r1[0] * r2[2] - r1[2] * r2[0]),
       r1[0] * r2[1] - r1[1] * r2[0])
w_d33 = sum(x * y for x, y in zip(r3, ker))
check("S3e the subgroup fixing (d_2_1, c_8_16) moves d_3_3 with nonzero weight, "
      "so any d_3_3 != 0 can be scaled to 1", w_d33 != 0,
      f"kernel direction {ker}, weight on d_3_3 = {w_d33}")
w_bad = sum(x * y for x, y in zip(expvec("d_2_1"), ker))
check("S3n NEGATIVE: the same subgroup fixes d_2_1 (weight 0), i.e. the weight "
      "computation is not trivially nonzero", w_bad == 0, f"weight = {w_bad}")

# --- S4 --------------------------------------------------------------------
rows, consts = RED.w4_coefficients()
ks = sorted(rows)
ok4, mism = True, 0
for trial in range(5):
    g = {v: rnd.randrange(1, P) for v in RED.G_VARS}
    c, res = RED.reduced_edge_system_modp(P, g)
    if c is None:
        ok4 = False
        break
    full = dict(g)
    full.update(c)
    for v in VARS:
        full.setdefault(v, 0)
    vals = []
    for idx in BYW[-4]:
        vals.append(B.eval_terms(S.eq_terms(EQS[idx]), full, P))
    order = sorted(BYW[-4], key=lambda idx: EQS[idx]["bracket_point"][0])
    vals_sorted = [B.eval_terms(S.eq_terms(EQS[idx]), full, P) for idx in order]
    if any(v != 0 for v in vals_sorted[:8]):
        ok4 = False
    if [v % P for v in vals_sorted[8:]] != [v % P for v in res]:
        mism += 1
check("S4  the triangular c-solve kills the first 8 equations of the w=-4 block "
      "exactly, at 5 random g-points", ok4)
check("S4b the remaining 9 equation values equal the module's residual values",
      mism == 0, f"{mism} mismatching trials")
# negative control: perturb one c and the first 8 must no longer all vanish
g = {v: rnd.randrange(1, P) for v in RED.G_VARS}
c, res = RED.reduced_edge_system_modp(P, g)
c2 = dict(c)
c2["c_5_8"] = (c2["c_5_8"] + 1) % P
full = dict(g); full.update(c2)
for v in VARS:
    full.setdefault(v, 0)
order = sorted(BYW[-4], key=lambda idx: EQS[idx]["bracket_point"][0])
vals_bad = [B.eval_terms(S.eq_terms(EQS[idx]), full, P) for idx in order]
check("S4n NEGATIVE: perturbing one solved c breaks the block",
      any(v != 0 for v in vals_bad[:8]),
      f"{sum(1 for v in vals_bad[:8] if v != 0)} of 8 now nonzero")

print("\n" + "=" * 78)
npass = sum(1 for _, o, _ in RESULTS if o)
print(f"    {npass}/{len(RESULTS)} checks passed")
print("=" * 78)
sys.exit(0 if npass == len(RESULTS) else 1)
