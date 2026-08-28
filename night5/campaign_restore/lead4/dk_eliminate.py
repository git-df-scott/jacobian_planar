#!/usr/bin/env python3
"""Re-derive GGHV's elimination; control = their published equation (5.9).

GGHV (arXiv:2204.14178 sec 5) reduce the (9,24)/(9,27) case to conditions on
    D = x^3 + d1 x + d0 + d_-1 x^-1 + d_-2 x^-2 + ...
namely (D^2)_-k = 0 for k=1..5,7; (D^3)_-k = 0 for k=1,2; and
(D^3)_-4 + G = 0 with G := F_-4 * C3^23. They eliminate eight d's with a CAS
and obtain (5.9):
    18 C3^23 d1 d_-1^6 F_-4 + 8 C3^69 F_-4^3 + 27 d0 d_-1^9 = 0
i.e. in terms of G:   18 G d1 d_-1^6 + 8 G^3 + 27 d0 d_-1^9 = 0.

Structure exploited (why this is fast): each (D^2)_-k contains exactly one
new unknown d_-(k+3), linearly, so those six equations CASCADE by
substitution -- no Groebner basis. Three equations remain, in
d1, d0, d_-1, d_-2, d_-3, G; two resultants finish the elimination.

All coefficients are derived by series multiplication; the printed
equations are used only as checks (CHK1). Reproducing (5.9) validates the
machinery before it is pointed at the open (72,108) case.
"""
import sys
import sympy as sp

NEG = 10
d1, d0 = sp.symbols("d1 d0")
dm = {k: sp.Symbol(f"dm{k}") for k in range(1, NEG + 1)}
G = sp.Symbol("G")

D = {3: sp.Integer(1), 1: d1, 0: d0}
for k in range(1, NEG + 1):
    D[-k] = dm[k]


def mul(A, B, lo=-8):
    out = {}
    for e1, c1 in A.items():
        for e2, c2 in B.items():
            e = e1 + e2
            if e >= lo:
                out[e] = sp.expand(out.get(e, 0) + c1 * c2)
    return out


D2 = mul(D, D)
D3 = mul(D2, D)

checks = [
    (D2[-2], dm[1]**2 + 2*d0*dm[2] + 2*d1*dm[3] + 2*dm[5], "(D^2)_-2"),
    (D2[-3], 2*dm[1]*dm[2] + 2*d0*dm[3] + 2*d1*dm[4] + 2*dm[6], "(D^2)_-3"),
    (D2[-4], dm[2]**2 + 2*dm[1]*dm[3] + 2*d0*dm[4] + 2*d1*dm[5] + 2*dm[7],
     "(D^2)_-4"),
    (D3[-1], 3*d0**2*dm[1] + 3*d1*dm[1]**2 + 6*d0*d1*dm[2] + 3*dm[2]**2
     + 3*d1**2*dm[3] + 6*dm[1]*dm[3] + 6*d0*dm[4] + 6*d1*dm[5] + 3*dm[7],
     "(D^3)_-1"),
]
ok = True
for a, b, name in checks:
    if sp.expand(a - b) != 0:
        print(f"CHK1 FAIL {name}: {sp.expand(a-b)}")
        ok = False
print(f"CHK1 derived series coefficients vs GGHV printed equations: "
      f"{'PASS' if ok else 'FAIL'}", flush=True)
if not ok:
    sys.exit(1)

sub = {}
for k in (1, 2, 3, 4, 5, 7):
    e = sp.expand(D2[-k].subs(sub))
    v = dm[k + 3]
    sol = sp.solve(sp.Eq(e, 0), v, dict=True)
    assert len(sol) == 1, f"(D^2)_-{k} not linear in {v}"
    sub[v] = sp.expand(sol[0][v])
    for w in list(sub):
        sub[w] = sp.expand(sub[w].subs({v: sub[v]}))
print(f"cascade solved by substitution: {sorted(str(k) for k in sub)}",
      flush=True)

E = [sp.expand(D3[-1].subs(sub)),
     sp.expand(D3[-2].subs(sub)),
     sp.expand((D3[-4] + G).subs(sub))]
rem = sorted({str(s) for e in E for s in e.free_symbols})
print(f"remaining: 3 equations in {rem}", flush=True)
for i, e in enumerate(E):
    print(f"   E{i}: deg dm3={sp.degree(e, dm[3])} dm2={sp.degree(e, dm[2])} "
          f"terms={len(e.args)}", flush=True)

R1 = sp.expand(sp.resultant(E[0], E[1], dm[3]))
print(f"R1 done: deg dm2 = {sp.degree(R1, dm[2])}", flush=True)
R2 = sp.expand(sp.resultant(E[0], E[2], dm[3]))
print(f"R2 done: deg dm2 = {sp.degree(R2, dm[2])}", flush=True)
F = sp.resultant(R1, R2, dm[2])
print("final resultant computed", flush=True)
target = 18*G*d1*dm[1]**6 + 8*G**3 + 27*d0*dm[1]**9
fac = sp.factor_list(F)
print(f"final eliminant: {len(fac[1])} irreducible factors")
hit = None
for base, mult in fac[1]:
    for s in (1, -1):
        if sp.expand(s * base - target) == 0:
            hit = (base, mult)
if hit:
    print("\n*** CONTROL PASS: GGHV equation (5.9) reproduced exactly ***")
    print("   ", sp.expand(hit[0]), f"  (multiplicity {hit[1]})")
else:
    print("\n(5.9) not among factors. Factor degrees:",
          [sp.total_degree(b) for b, _ in fac[1]][:10])
    print("target:", target)
