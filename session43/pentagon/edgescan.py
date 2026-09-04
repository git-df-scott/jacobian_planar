#!/usr/bin/env python3
"""BREAKTHROUGH 1: scan ALL gradings for INHOMOGENEOUS top levels.

For weights (a,b) on (x,y), gamma(x^i y^j) = a i + b j:
    gamma(f_x g_y) = gamma(f) - a + gamma(g) - b, same for f_y g_x
so gamma({f,g}) <= gamma(P) + gamma(Q) - a - b, and gamma(x^2) = 2a.

**The top graded level carries the x^2 (is INHOMOGENEOUS) iff**

    gamma(P) + gamma(Q) = 3a + b .

Homogeneous tops (like the upper edge) vanish identically and say little at the
top; inhomogeneous tops (like the lower edge) pin an exact relation immediately
and are the decidable ones.

Verified against the two known cases:
    upper edge  w = j - i  -> (a,b) = (-1, 1): 8+12 = 20 vs 3a+b = -2  HOMOGENEOUS
    lower edge  v = 2i - j -> (a,b) = ( 2,-1): 2+3  =  5 vs 3a+b =  5  INHOMOGENEOUS
"""
from math import gcd
NP = [(0,0),(1,0),(8,14),(8,16),(0,8)]
NQ = [(0,0),(2,1),(12,21),(12,24),(0,12)]
def gam(V, a, b): return max(a*i + b*j for i, j in V)
def argmax(V, a, b):
    m = gam(V, a, b); return [p for p in V if a*p[0]+b*p[1] == m]

print("CONTROL, the two known gradings:")
for name, (a, b) in (("upper  w = j-i", (-1,1)), ("lower  v = 2i-j", (2,-1))):
    gP, gQ = gam(NP,a,b), gam(NQ,a,b)
    print(f"  {name:16s} (a,b)=({a:2d},{b:2d})  gP+gQ = {gP+gQ:3d}  3a+b = {3*a+b:3d}  "
          f"-> {'INHOMOGENEOUS' if gP+gQ == 3*a+b else 'homogeneous'}")

print("\nfull scan over primitive (a,b), |a|,|b| <= 12:")
hits = []
for a in range(-12, 13):
    for b in range(-12, 13):
        if (a, b) == (0, 0) or gcd(abs(a), abs(b)) != 1: continue
        gP, gQ = gam(NP,a,b), gam(NQ,a,b)
        if gP + gQ == 3*a + b:
            hits.append((a, b, gP, gQ, argmax(NP,a,b), argmax(NQ,a,b)))
print(f"  {len(hits)} inhomogeneous gradings found:\n")
for a,b,gP,gQ,fP,fQ in hits:
    kindP = "EDGE" if len(fP) > 1 else "vertex"
    kindQ = "EDGE" if len(fQ) > 1 else "vertex"
    print(f"  (a,b)=({a:3d},{b:3d})  gP={gP:3d} gQ={gQ:3d}   N(P) face {fP} [{kindP}]"
          f"   N(Q) face {fQ} [{kindQ}]")
print("\nOf these, the ones whose face on BOTH polygons is an EDGE (not a single")
print("vertex) give a genuine one-variable relation like the lower edge:")
for a,b,gP,gQ,fP,fQ in hits:
    if len(fP) > 1 and len(fQ) > 1:
        print(f"  ** (a,b)=({a},{b})  P-edge {fP}  Q-edge {fQ}")
