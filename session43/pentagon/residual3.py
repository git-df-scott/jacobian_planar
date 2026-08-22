#!/usr/bin/env python3
"""R-ladder rungs 12, 11, 10:  {P,R} = 2 x^2 Q,  R = Q^2 - c P^3.

Every input is EXACT, not an edge approximation -- the pentagon's supports make
each of these polynomials exactly what the edge results give:
    a_8 = alpha y^14 (y-rho)^2        (support j in [14,16], disc = 0)
    a_7 = y^12 (y-rho) C_7            (support j in [12,15], A_7(rho) = 0)
    a_6 = y^10 A_6                    (support j in [10,14])
    a_5 = y^8 A_5                     (support j in [8,13])
    q_12 = beta y^21 (y-rho)^3        (support j in [21,24])
    q_11 = y^19 (3 beta/2 alpha)(y-rho)^2 C_7
Rung d:  sum_{i+k=d+1} [i a_i r_k' - k a_i' r_k] = 2 q_{d-2}.
r_k support from N(Q^2) = N(P^3): j in [max(0,2k-6), 24+k].
"""
import sympy as sp
y, rho, al, be = sp.symbols('y rho alpha beta', nonzero=True)
NZ = {al, be, rho}
def gen(n, d, lo=0):
    cs = [sp.Symbol(f'{n}{i}') for i in range(lo, d+1)]
    return sum(cs[i-lo]*y**i for i in range(lo, d+1)), cs

C7, cC7 = gen('c7_', 2)
A6, cA6 = gen('a6_', 4)
A5, cA5 = gen('a5_', 5)
a = {8: al*y**14*(y-rho)**2, 7: y**12*(y-rho)*C7, 6: y**10*A6, 5: y**8*A5}
q = {12: be*y**21*(y-rho)**3, 11: y**19*sp.Rational(3,2)*be/al*(y-rho)**2*C7}
r = {7: be*y**8*(y-rho)**2*(195*rho**4+240*rho**3*y+320*rho**2*y**2
                           +512*rho*y**3+2048*y**4)/(3315*al*rho**5)}
r[6] = be*y**6*(-rho+y)*(10465*cC7[0]*rho**5+12115*cC7[0]*rho**4*y+14680*cC7[0]*rho**3*y**2
      +19952*cC7[0]*rho**2*y**3+79808*cC7[0]*rho*y**4+141440*cC7[0]*y**5
      +9360*cC7[1]*rho**5*y+9684*cC7[1]*rho**4*y**2+7608*cC7[1]*rho**3*y**3
      -26016*cC7[1]*rho**2*y**4+277824*cC7[1]*rho*y**5+7371*cC7[2]*rho**5*y**2
      +3717*cC7[2]*rho**4*y**3-32172*cC7[2]*rho**3*y**4+149016*cC7[2]*rho**2*y**5
      +150528*cC7[2]*rho*y**6)/(278460*al**2*rho**6)

def rung(d, aa, rr, qq):
    s = 0
    for i in range(9):
        k = d+1-i
        if 0 <= k <= 7 and i in aa and k in rr:
            s += i*aa[i]*sp.diff(rr[k], y) - k*sp.diff(aa[i], y)*rr[k]
    return sp.expand(s - 2*qq.get(d-2, 0))

for d, need in ((13, None), (12, 5), (11, 4)):
    if need is None:
        chk = sp.simplify(rung(13, a, r, q))
        print("rung 13 re-check:", "PASS" if chk == 0 else "FAIL"); continue
    k = need
    R, rs = gen(f's{k}_', 24+k, 0)
    E = rung(d, a, {**r, k: R}, q)
    num, _ = sp.fraction(sp.together(sp.expand(E)))
    eqs = sp.Poly(sp.expand(num), y).all_coeffs()
    Mat, vec = sp.linear_eq_to_matrix(eqs, rs)
    conds = set()
    for n in Mat.T.nullspace():
        v = sp.simplify(sp.expand((n.T*vec)[0,0]))
        if v != 0:
            nn, _ = sp.fraction(sp.together(v))
            for f, m in sp.factor_list(sp.expand(nn))[1]:
                if not f.is_number and f not in NZ: conds.add(sp.expand(f))
    print(f"\nrung {d}: {Mat.shape[0]} eqs, {Mat.shape[1]} unk, rank {Mat.rank()}, "
          f"conditions {len(conds)}")
    for x in sorted(conds, key=sp.count_ops)[:4]:
        print("    COND:", sp.factor(x))
    if not conds:
        sol = sp.solve(eqs, rs, dict=True)
        if sol:
            r[k] = sp.expand(R.subs(sol[0]))
            free = [v for v in rs if r[k].has(v)]
            print(f"    solved r_{k}, free params: {free}, "
                  f"y-order {sp.Poly(sp.numer(sp.together(r[k])), y).monoms()[-1][0] if r[k]!=0 else '-'}")
        else:
            print("    !! consistent by rank but solve returned nothing"); break
    else:
        break
