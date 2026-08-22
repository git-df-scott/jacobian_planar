#!/usr/bin/env python3
"""Where the divisibility obstruction lives, and how far down it reaches.

Level L isolates its new unknowns against h_8 = c0 sigma^8 and g_12 = c1 sigma^12:

  (8, L-8) term : 8 c0 sigma^7 [ (L-8) g_{L-8} - sigma g'_{L-8} ]
  (L-12, 12) term: 12 c1 sigma^11 [ sigma h'_{L-12} - (L-12) h_{L-12} ]

Both carry sigma^7, so every such level imposes  sigma^7 | (carried terms).

  * (8, b) exists while L-8 >= -1, i.e. L >= 7
  * (a, 12) exists while L-12 >= -1, i.e. L >= 11

So levels 20..7 all carry the sigma^7 divisibility obstruction -- FOURTEEN of
them -- and levels 6..-1 are pure conditions with no new unknowns at all.
"""
import sympy as sp
s, tau = sp.symbols('s tau')
sg = s - tau
def h_rng(a):
    lo, hi = max(0,-a), min(8, a+2)
    return [i for i in range(lo,hi+1) if 0 <= i+a <= 16]
print("level : has (8,L-8)? has (L-12,12)? -> sigma^7 obstruction?")
for L in range(20, -3, -1):
    A = (-1 <= L-8 <= 12); B = (-1 <= L-12 <= 8)
    print(f"  {L:3d} :     {str(A):5s}          {str(B):5s}      "
          f"{'YES' if (A or B) else 'no new unknowns -> PURE CONDITION'}")
print("\nThe gauge-fixed bottom pieces, and their sigma-orders:")
h_1 = s                       # p_0_1 = 1
h_0 = sp.Symbol('p_1_1')*s + sp.Symbol('p_2_2')*s**2   # p_0_0 = 0
print(f"  h_-1 = {h_1}      ord_sigma = 0   (h_-1(tau) = tau != 0)")
print(f"  h_0  = {h_0}   ord_sigma >= 0, and h_0(tau) = p_1_1 tau + p_2_2 tau^2")
print("\n  ** sigma^2 CANNOT divide h_-1 = s: it is degree 1 and fixed by the gauge. **")
print("  So if the descent forces ord_sigma(h_a) >= 2 all the way down to a = -1,")
print("  that is a contradiction and (72,108) is EMPTY.  Whether it propagates that")
print("  far is exactly what the descent decides -- levels 6..-1 have no new")
print("  unknowns at all, so they cannot absorb the requirement.")
print("\n  Established so far:  ord(h_8) = 8 (exactly, h_8 = c0 sigma^8)")
print("                       ord(h_7) >= 2   (level 18, proved)")
print("                       ord(h_6) >= 2   (level 17, under test: m=0,1 FAIL)")
