#!/usr/bin/env python3
"""VERIFY (not assert) that the u-scaling used to normalise the essential
face is induced by a genuine symmetry of the whole problem.

Claim: for any t != 0, the map  phi(x,y) = (t x, y)  followed by
P -> t^{-1} (P o phi),  Q -> t^{-2} (Q o phi)
  * preserves both Newton polygons (only coefficients are scaled),
  * preserves [P,Q] = x^2, and
  * acts on the essential-face coefficients exactly as a_i -> t^i a_i,
    b_j -> t^j b_j  (the u-scaling u -> t u).
Consequences: the 35 face points form 5 orbits of size 7 under this action,
so testing ONE representative per cover is enough -- which is what the
verdict runs do (mod p with 7 not dividing p-1 exactly one point of each
mu_7 orbit is F_p-rational).
"""
import sys
from case1_point import find, build_fg
from case1_validate import bracket
from case1_cascade import inside, NP, NQ
from case1_ladder import coeffs

p = int(sys.argv[1]) if len(sys.argv) > 1 else 5189
which = int(sys.argv[2]) if len(sys.argv) > 2 else 0
r, err = find(p, which)
assert not err, err
av, f, g, bad, nr = r
assert not bad

def facepolys(f, g):
    P = {(1 + i, 2 * i): c for i, c in enumerate(f) if c}
    Q = {(2 + j, 1 + 2 * j): c for j, c in enumerate(g) if c}
    return P, Q

def W(f, g, n):
    return sum(c * f[i] * g[j] for (c, i, j) in coeffs(7, 10)[n]) % p

P0, Q0 = facepolys(f, g)
print("base point: [P,Q] =", bracket(P0, Q0, p),
      "  (expect {(2,0): 1})")
ok = True
for t in (2, 3, 5, 7, 11, p - 1):
    # coefficient rule from phi and the rescalings
    P1 = {(i, j): c * pow(t, i, p) % p * pow(t, -1, p) % p
          for (i, j), c in P0.items()}
    Q1 = {(i, j): c * pow(t, i, p) % p * pow(t, -2, p) % p
          for (i, j), c in Q0.items()}
    f1 = [c * pow(t, i, p) % p for i, c in enumerate(f)]
    g1 = [c * pow(t, j, p) % p for j, c in enumerate(g)]
    P2, Q2 = facepolys(f1, g1)
    same = (P1 == P2 and Q1 == Q2)
    br = bracket(P1, Q1, p)
    wok = all(W(f1, g1, n) == (1 if n == 0 else 0) for n in range(0, 18))
    supp = all(inside(k, NP) for k in P1) and all(inside(k, NQ) for k in Q1)
    good = same and br == {(2, 0): 1 % p} and wok and supp
    ok = ok and good
    print("  t=%-5d  coefficient rule == u-scaling: %-5s  [P,Q]=x^2: %-5s  "
          "W==1: %-5s  supports ok: %-5s" %
          (t, same, br == {(2, 0): 1 % p}, wok, supp))
print("SYMMETRY VERIFIED" if ok else "*** SYMMETRY CLAIM FAILS ***")
