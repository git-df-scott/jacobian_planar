"""The leading level's solution count, m = 2..8, and the observed pattern.

vdim of E1 in the slice F_{m-1} = 1 (all at p = 32003, and for m=8 also at
p = 65521 and p = 1000003):

    m  = 2   4   6   8
   vdim= 1   3  10  35

which is  C(m-1, m/2-1).  The residual weighted scaling F_i -> mu^i F_i with
mu^(m-1) = 1 acts freely, so the number of ORBITS is C(m-1,m/2-1)/(m-1):

    m  = 2   4   6   8      (predicted 10)
 orbits= 1   1   2   5      (predicted 14)

1, 1, 2, 5, 14 are the Catalan numbers C_{m/2-1}.  E1 is the condition that
T^2 dT / y^5 be exact on the genus-(m/2-1) hyperelliptic curve y^2 = f2(T);
the count of such f2 being Catalan is an observation from four data points,
not a theorem, and m = 10 is the first real test of it.
"""
from math import comb

print(f"{'m':>3} {'genus':>5} {'vdim':>6} {'orbits':>7} {'Catalan':>8}")
def catalan(n):
    return comb(2 * n, n) // (n + 1)
for m in range(2, 15, 2):
    g = m // 2 - 1
    v = comb(m - 1, m // 2 - 1)
    print(f"{m:>3} {g:>5} {v:>6} {v // (m - 1):>7} {catalan(g):>8}")
