#!/usr/bin/env python3
"""Solve the w-cascade upward from the bottom, level by level.

Each level is LINEAR in its newly-appearing unknowns given the levels below, so
the blocks are solved by rank, not by sp.solve (which returns [] for
'generically inconsistent' and would be misread as empty -- ERRATA A14/A16).
"""
import io, contextlib, sympy as sp
src = open('session43/pentagon/wcascade.py').read(); g = {}
with contextlib.redirect_stdout(io.StringIO()): exec(src, g)
x, y, level = g['x'], g['y'], g['level']

sub = {}
for L in range(-1, 21):
    e = sp.expand(level(L).subs(sub))
    if e == 0:
        print(f"level {L:3d}: identically satisfied", flush=True); continue
    eqs = sp.Poly(e, x, y).coeffs()
    vs = sorted(set().union(*[c.free_symbols for c in eqs]), key=str)
    # is this level linear in the unknowns it introduces?
    lin = all(sp.Poly(c, *vs).total_degree() <= 1 for c in eqs)
    if lin:
        Mat, vec = sp.linear_eq_to_matrix(eqs, vs)
        rM, rA = Mat.rank(), Mat.row_join(vec).rank()
        status = "CONSISTENT" if rM == rA else "needs conditions on lower levels"
        print(f"level {L:3d}: {len(eqs):2d} eqs, {len(vs):3d} unk, LINEAR, "
              f"rank {rM}, kernel {len(vs)-rM} -> {status}", flush=True)
        if rM == rA:
            s = sp.solve(eqs, vs, dict=True)
            if s: sub.update({k: sp.expand(v) for k, v in s[0].items()})
    else:
        deg = max(sp.Poly(c, *vs).total_degree() for c in eqs)
        print(f"level {L:3d}: {len(eqs):2d} eqs, {len(vs):3d} unk, NONLINEAR "
              f"(degree {deg}) -- stopping the sequential solve here", flush=True)
        break
