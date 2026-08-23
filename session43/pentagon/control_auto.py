#!/usr/bin/env python3
"""END-TO-END POSITIVE CONTROL on a case with a KNOWN solution.

Every EMPTY verdict in this campaign comes from the same pipeline: build the
s-ladder, run the descent, hand the residue to msolve, read [1] as empty.  That
pipeline has never once been run on a system that HAS a solution.  If it can
report EMPTY spuriously -- a wrong support, a sign, a mis-set target -- then
every verdict is void and a counterexample could have been missed.

The campaign recorded that an end-to-end positive control is "structurally
impossible" at ratio 3:2, because by Jung-van der Kulk any solution there is
already a counterexample.  That is true AT 3:2 and nowhere else.  At a ratio
where genuine automorphisms exist, the control is perfectly available.

The witness used here is an honest polynomial automorphism:

    P = x + y^2 ,   Q = y + P^2 = y + x^2 + 2 x y^2 + y^4
    {P,Q} = {P,y} + {P,P^2} = 1 + 0 = 1        (deg P = 2, deg Q = 4)

In the s-ladder, s = xy and x^i y^j sits at w = j - i as y^w s^i:

    P : x -> w=-1, s^1 ;   y^2 -> w=2, s^0
    Q : y -> w=1,  s^0 ;   x^2 -> w=-2, s^2 ;
        2xy^2 -> w=1, s^1 ;  y^4 -> w=4, s^0

The target is {P,Q} = 1 = y^0 s^0, i.e. level 0 carries 1.

The machinery MUST return NONEMPTY here and recover this map.  If it returns
EMPTY, the pipeline is broken and every EMPTY verdict it has produced is void.
"""
import sympy as sp, sys
z = sp.Symbol('z')          # here s itself; no tau shift is needed for the control
s = z
# supports, read straight off the two Newton polygons above
HSUP = {-1: [1], 2: [0]}
GSUP = {-2: [2], 1: [0, 1], 4: [0]}
H = {a: sum(sp.Symbol(f'h{a}_{i}')*z**i for i in sup) for a, sup in HSUP.items()}
G = {b: sum(sp.Symbol(f'g{b}_{k}')*z**k for k in sup) for b, sup in GSUP.items()}
KNOWN = {'h-1_1': 1, 'h2_0': 1, 'g-2_2': 1, 'g1_0': 1, 'g1_1': 2, 'g4_0': 1}
def lev(L):
    e = 0
    for a in H:
        b = L - a
        if b in G: e += b*sp.diff(H[a],z)*G[b] - a*H[a]*sp.diff(G[b],z)
    return sp.expand(e - (1 if L == 0 else 0))
LEVELS = sorted({a+b for a in H for b in G}, reverse=True)
print("levels present:", LEVELS)
eqs = []
for L in LEVELS + [0]:
    e = lev(L)
    if e == 0: continue
    eqs += [c for c in sp.Poly(e, z).all_coeffs() if c != 0]
eqs = list(dict.fromkeys(eqs))
V = sorted(set().union(*[c.free_symbols for c in eqs]), key=str)
print(f"{len(eqs)} equations, {len(V)} unknowns: {[str(v) for v in V]}")

# --- CHECK 1: the known map really does satisfy every level ---
subK = {sp.Symbol(k): sp.Integer(v) for k, v in KNOWN.items()}
bad = [sp.expand(c.subs(subK)) for c in eqs]
bad = [b for b in bad if b != 0]
print(f"CHECK 1  known automorphism satisfies all {len(eqs)} equations: "
      f"{'PASS' if not bad else 'FAIL ' + str(bad[:3])}")
if bad: sys.exit(1)

# --- CHECK 2: msolve must NOT return [1] ---
def ms_poly(c):
    P = sp.Poly(c, *V).primitive()[1]
    o = ""
    for mon, co in sorted(P.terms(), reverse=True):
        parts = [str(abs(co))] if abs(co) != 1 or all(e==0 for e in mon) else []
        for v, e in zip(V, mon):
            if e == 1: parts.append(str(v))
            elif e > 1: parts.append(f"{v}^{e}")
        o += ("-" if co < 0 else ("+" if o else "")) + "*".join(parts)
    return o
name = lambda v: str(v).replace('-','m')
VN = [name(v) for v in V]
txt = ",".join(VN) + "\n0\n" + ",\n".join(ms_poly(c) for c in eqs) + "\n"
for v in V: txt = txt.replace(str(v), name(v))
assert "(" not in txt and ")" not in txt, "PARENTHESIS -- A16"
open('control_auto.ms','w').write(txt)
print("wrote control_auto.ms")
