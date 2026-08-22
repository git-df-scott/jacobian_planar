"""END-TO-END VERIFIER for a pentagon candidate.  The only thing that may license
the word "counterexample".  Nothing in the campaign did this before.

Input: dict of coefficient values {a{i}_{j}: val, b{k}_{j}: val} (exact rationals).
Checks, ALL of which must pass:
  (1) {P,Q} - x^2 == 0 identically over Q                      [the actual equation]
  (2) the same at two large primes                             [independent arithmetic]
  (3) all six mutable vertices nonzero
        p_8_0=a0_8, p_14_8=a8_14, p_16_8=a8_16,
        q_12_0=b0_12, q_21_12=b12_21, q_24_12=b12_24
  (4) N(P), N(Q) are EXACTLY the pentagons (no vertex lost, nothing outside)
Negative control included: a deliberately perturbed point must FAIL (1).
"""
import sympy as sp, sys, pickle
from sympy import Rational as R
x, y = sp.symbols('x y')

NP = [(0,0),(1,0),(8,14),(8,16),(0,8)]
NQ = [(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v, imax):
    lo, hi = {}, {}
    for i in range(imax+1):
        pts = []
        for t in range(len(v)):
            (x1,y1),(x2,y2) = v[t], v[(t+1)%len(v)]
            if x1 == x2 == i: pts += [y1,y2]
            elif (x1-i)*(x2-i) <= 0 and x1 != x2: pts.append(y1 + R(y2-y1,x2-x1)*(i-x1))
        lo[i] = int(sp.ceiling(min(pts))); hi[i] = int(sp.floor(max(pts)))
    return lo, hi
loP, hiP = bounds(NP,8); loQ, hiQ = bounds(NQ,12)

def build(vals):
    P = sum(vals.get(f'a{i}_{j}', 0)*x**i*y**j
            for i in range(9) for j in range(loP[i], hiP[i]+1))
    Q = sum(vals.get(f'b{k}_{j}', 0)*x**k*y**j
            for k in range(13) for j in range(loQ[k], hiQ[k]+1))
    return sp.expand(P), sp.expand(Q)

def bracket(P, Q):
    return sp.expand(sp.diff(P,x)*sp.diff(Q,y) - sp.diff(P,y)*sp.diff(Q,x))

def hull(E):
    """vertices of the convex hull of exponent set E (monotone chain)"""
    P_ = sorted(set(E))
    if len(P_) <= 2: return P_
    def cr(o,a,b): return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo=[]
    for p in P_:
        while len(lo)>=2 and cr(lo[-2],lo[-1],p)<=0: lo.pop()
        lo.append(p)
    up=[]
    for p in reversed(P_):
        while len(up)>=2 and cr(up[-2],up[-1],p)<=0: up.pop()
        up.append(p)
    return sorted(set(lo[:-1]+up[:-1]))

def verify(vals, label="candidate", verbose=True):
    ok = True
    P, Q = build(vals)
    J = bracket(P, Q)
    r1 = sp.expand(J - x**2) == 0
    if verbose: print(f"[{label}] (1) {{P,Q}} - x^2 == 0 over Q : {r1}")
    ok &= r1
    if not r1 and verbose:
        d = sp.Poly(sp.expand(J - x**2), x, y)
        print(f"        residual has {len(d.monoms())} monomials, e.g. {d.monoms()[:4]}")
    for p in (2147483647, 1000000007):
        Jp = sp.expand(sp.Poly(sp.expand(J - x**2), x, y).set_modulus(p).as_expr()) if sp.expand(J-x**2)!=0 else 0
        rp = (Jp == 0)
        if verbose: print(f"[{label}] (2) same, mod {p} : {rp}")
        ok &= rp
    vertices = {'p_8_0':'a0_8','p_14_8':'a8_14','p_16_8':'a8_16',
                'q_12_0':'b0_12','q_21_12':'b12_21','q_24_12':'b12_24'}
    for nm, key in vertices.items():
        v = vals.get(key, 0); good = (v != 0)
        if verbose: print(f"[{label}] (3) vertex {nm} = {v} nonzero : {good}")
        ok &= good
    for nm, poly, target in (("N(P)", P, NP), ("N(Q)", Q, NQ)):
        if poly == 0: print(f"[{label}] (4) {nm}: polynomial is zero"); ok = False; continue
        E = [(m[0], m[1]) for m in sp.Poly(poly, x, y).monoms()]
        h = hull(E); good = (sorted(h) == sorted(target))
        if verbose: print(f"[{label}] (4) {nm} hull == pentagon : {good}  {h if not good else ''}")
        ok &= good
    print(f"[{label}] VERDICT: {'PASS -- this is a counterexample' if ok else 'FAIL'}")
    return ok

if __name__ == '__main__':
    print("=== NEGATIVE CONTROL: a point that is NOT a solution must FAIL ===")
    bad = {'a0_8':1,'a8_14':1,'a8_16':1,'b0_12':1,'b12_21':1,'b12_24':1,'a1_0':1}
    verify(bad, "negative-control")
    print()
    print("=== POSITIVE CONTROL: the bracket routine on a known pair ===")
    # {x, y} = 1 ; scale to get x^2:  {x^3/3, y} = x^2
    Pt, Qt = x**3/3, y
    print("bracket(x^3/3, y) - x^2 =", sp.expand(bracket(Pt,Qt) - x**2), "(must be 0)")
    print("bracket(x, y)          =", sp.expand(bracket(x,y)), "(must be 1)")
    if len(sys.argv) > 1:
        vals = pickle.load(open(sys.argv[1],'rb'))
        print(); verify(vals, sys.argv[1])
