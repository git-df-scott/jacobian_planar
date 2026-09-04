#!/usr/bin/env python3
"""BREAKTHROUGH 3: do the w-cascade's TOP results satisfy the v-cascade's BOTTOM
conditions automatically, and which of the 45 are NEW information?

The eighth-power theorem (from the w-cascade's top level) fixes 22 coefficients:
    p_{i+8,i}  = c0 * C(8,i)  * (-tau)^(8-i)
    q_{12+k,k} = c1 * C(12,k) * (-tau)^(12-k)
The v-cascade's bottom (levels -20..-12) gives 45 bilinear conditions.  Any of
them that does NOT vanish under the substitution is new information joining the
two ends of the problem.
"""
import sympy as sp
from math import comb
import io, contextlib
r, tau, c0, c1 = sp.symbols('r tau c0 c1')
src = open('session43/pentagon/vbottom.py').read()
g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, g)
lev = g['lev']
conds = []
for V in range(-20, -11):
    e = lev(V)
    conds += [(V, c) for c in (sp.Poly(e, g['r']).all_coeffs() if e != 0 else []) if c != 0]
print(f"{len(conds)} v-bottom conditions")

sub = {}
for i in range(9):  sub[sp.Symbol(f'p_{i+8}_{i}')]  = c0*comb(8,i)*(-tau)**(8-i)
for k in range(13): sub[sp.Symbol(f'q_{12+k}_{k}')] = c1*comb(12,k)*(-tau)**(12-k)
print(f"eighth-power theorem fixes {len(sub)} coefficients\n")

auto, new = [], []
for V, c in conds:
    cs = sp.expand(c.subs(sub))
    (auto if sp.simplify(cs) == 0 else new).append((V, cs, c))
print(f"AUTOMATICALLY SATISFIED by the eighth-power theorem : {len(auto)}")
print(f"NOT automatic -> NEW information                     : {len(new)}\n")
from collections import Counter
print("by level:  V : auto / total")
tot = Counter(V for V, _ in conds); a = Counter(V for V, _, _ in auto)
for V in sorted(tot, reverse=True):
    print(f"   {V:4d} : {a[V]}/{tot[V]}")
print("\ndeepest condition V=-20, before and after substitution:")
V20 = [c for V, c in conds if V == -20]
for c in V20:
    print("   raw :", sp.factor(c))
    print("   sub :", sp.simplify(sp.expand(c.subs(sub))), " -> ",
          "VANISHES" if sp.simplify(sp.expand(c.subs(sub))) == 0 else "nonzero")
if new:
    print(f"\nfirst 2 NEW conditions (these tie the two cascades together):")
    for V, cs, craw in new[:2]:
        f = sp.factor(cs)
        print(f"   V={V}: {str(f)[:300]}")
