#!/usr/bin/env python3
"""THE DOWNWARD W-CASCADE -- the whole pentagon as 21 linear solves.

At level L the only unknowns not already fixed by higher levels are P_{L-12} and
Q_{L-8}, and each meets an already-determined partner ({P_{L-12}, Q_12} and
{P_8, Q_{L-8}}), so every level below the top is LINEAR **in its newly introduced unknowns**.
It is NOT linear outright: a level can leave kernel freedom, and two carried-
forward free parameters can multiply each other at a later level (q_23_12^2
appears at level 18 this way).  Those products sit in the RIGHT-HAND SIDE, not
against the new unknowns, so the solve stays linear -- but the residual
conditions are polynomial in the carried parameters.  Only level 20 is bilinear
in its own unknowns, and it is solved: the eighth-power family.

New unknowns appear while L >= 11 (P side) and L >= 7 (Q side).  So levels
6,5,4,3,2,1,0,-1 introduce NOTHING and are pure conditions -- 59 equations.

Kernel freedom is carried SYMBOLICALLY at every step (lesson A3: a greedy
particular solution manufactures obstructions).
Consistency is decided by RANK, never by 'sp.solve returned []' (A14, A16).
"""
import io, contextlib, sympy as sp
from math import comb
src = open('session43/pentagon/wcascade.py').read(); g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, g)
x, y, level, PS, QS = g['x'], g['y'], g['level'], g['PS'], g['QS']
t, tau, c0, c1 = sp.symbols('t tau c0 c1')

# level 20: the eighth-power family
sub = {}
A  = sp.Poly(sp.expand(c0*(t-tau)**8), t)
Qh = sp.Poly(sp.expand(c1*(t-tau)**12), t)
for i in range(9):  sub[sp.Symbol(f'p_{i+8}_{i}')]  = A.coeff_monomial(t**i)
for k in range(13): sub[sp.Symbol(f'q_{12+k}_{k}')] = Qh.coeff_monomial(t**k)
chk = sp.expand(level(20).subs(sub))
print("CONTROL level 20 with the eighth-power family:",
      "PASS" if chk == 0 else f"FAIL {chk}", flush=True)

free = []
for L in range(19, -2, -1):
    e = sp.expand(level(L).subs(sub))
    if e == 0:
        print(f"level {L:3d}: identically satisfied", flush=True); continue
    eqs = sp.Poly(e, x, y).coeffs()
    new = sorted(set().union(*[c.free_symbols for c in eqs]) -
                 {tau, c0, c1} - set(free), key=str)
    unk = new + free
    if not unk:
        bad = [c for c in eqs if sp.simplify(c) != 0]
        print(f"level {L:3d}: {len(eqs):2d} eqs, NO unknowns -> "
              f"{len(bad)} PURE CONDITIONS", flush=True)
        for c in bad[:3]: print("        COND:", sp.factor(c), flush=True)
        continue
    deg = max(sp.Poly(c, *unk).total_degree() for c in eqs)
    dnew = max(sp.Poly(c, *new).total_degree() for c in eqs) if new else 0
    Mat, vec = sp.linear_eq_to_matrix(eqs, new)   # NEW unknowns only;
    rM = Mat.rank(); rA = Mat.row_join(vec).rank()  # carried params ride in vec
    ok = (rM == rA)
    print(f"level {L:3d}: {len(eqs):2d} eqs, {len(new):3d} NEW ({len(free)} carried), "
          f"deg in new = {dnew}, "
          f"rank {rM}, kernel {len(new)-rM} -> {'CONSISTENT' if ok else 'CONDITIONS'}",
          flush=True)
    if not ok:
        for n in Mat.T.nullspace():
            v = sp.simplify(sp.expand((n.T*vec)[0,0]))
            if v != 0: print("        COND:", sp.factor(v), flush=True)
        break
    s = sp.solve(eqs, new, dict=True)
    if not s:
        print("        !! rank says consistent but solve returned nothing", flush=True); break
    s = s[0]
    for k in list(s): s[k] = sp.expand(s[k])
    sub.update(s)
    free = sorted((set(new) - set(s)) | set(free), key=str)
