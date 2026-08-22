"""FAST exact x-column descent, gauge-fixed r=1, alpha=1 (proved legitimate in gauge.py).
beta is the one genuine modulus.  No sp.simplify anywhere (that was the blowup).
Canonical gates via left nullspace; denominator ledger; perfect-power gates imposed
unconditionally; reducible gates reported as branch points.
Usage: fast.py [beta_value|sym] [stop_rung]
"""
import sympy as sp, pickle, sys, time
from sympy import Rational as R
y = sp.Symbol('y')
BETA = sys.argv[1] if len(sys.argv) > 1 else 'sym'
STOP = int(sys.argv[2]) if len(sys.argv) > 2 else 0
be = sp.Symbol('beta') if BETA == 'sym' else sp.Integer(int(BETA))
al = sp.Integer(1); r = sp.Integer(1)
NONZERO = {sp.Symbol('beta')}

NP = [(0,0),(1,0),(8,14),(8,16),(0,8)]; NQ = [(0,0),(2,1),(12,21),(12,24),(0,12)]
def bounds(v, imax):
    lo, hi = {}, {}
    for i in range(imax+1):
        pts = []
        for t in range(len(v)):
            (x1,y1),(x2,y2) = v[t], v[(t+1)%len(v)]
            if x1 == x2 == i: pts += [y1, y2]
            elif (x1-i)*(x2-i) <= 0 and x1 != x2: pts.append(y1 + R(y2-y1, x2-x1)*(i-x1))
        lo[i] = int(sp.ceiling(min(pts))); hi[i] = int(sp.floor(max(pts)))
    return lo, hi
loP, hiP = bounds(NP, 8); loQ, hiQ = bounds(NQ, 12)
loP[0] = max(loP[0], 1); loQ[0] = max(loQ[0], 1)
W = y**7*(y-r)
a = {i: sum(sp.Symbol(f'a{i}_{j}')*y**j for j in range(loP[i], hiP[i]+1)) for i in range(9)}
b = {k: sum(sp.Symbol(f'b{k}_{j}')*y**j for j in range(loQ[k], hiQ[k]+1)) for k in range(13)}
a[8] = sp.expand(al*W**2); b[12] = sp.expand(be*W**3)

def newvars(d):
    out = []
    i0, k0 = d-11, d-7
    if 0 <= i0 <= 8: out += [sp.Symbol(f'a{i0}_{j}') for j in range(loP[i0], hiP[i0]+1)]
    if 0 <= k0 <= 12: out += [sp.Symbol(f'b{k0}_{j}') for j in range(loQ[k0], hiQ[k0]+1)]
    return out

def rung(d, sub):
    e = 0
    for i in range(9):
        k = d+1-i
        if 0 <= k <= 12:
            e += i*a[i]*sp.diff(b[k], y) - k*sp.diff(a[i], y)*b[k]
    e = sp.expand(e.xreplace(sub) - (1 if d == 2 else 0))
    return [] if e == 0 else [c for c in sp.Poly(e, y).all_coeffs() if c != 0]

def strip(g):
    g = sp.factor(sp.together(g)); n, _ = sp.fraction(g)
    out = []
    for f, m in sp.factor_list(sp.expand(n))[1]:
        if f.is_number or f in NONZERO: continue
        out.append((f, m))
    return out

def fixpoint(sub):
    for _ in range(20):
        nsub = {k: sp.expand(v.xreplace(sub)) for k, v in sub.items()}
        if nsub == sub: break
        sub = nsub
    return sub

sub = {}; denoms = set(); freep = []; conditions = []; t0 = time.time()
for d in range(18, STOP-1, -1):
    nv = [v for v in newvars(d) if v not in sub]
    imposed = []; branched = False
    for it in range(15):
        cs = rung(d, sub)
        nv = [v for v in nv if v not in sub]
        if not cs: break
        M = sp.zeros(len(cs), len(nv)); vv = sp.zeros(len(cs), 1)
        z0 = {n: sp.Integer(0) for n in nv}
        for ii, c in enumerate(cs):
            p = sp.expand(c)
            for jj, n in enumerate(nv): M[ii, jj] = sp.expand(sp.diff(p, n))
            vv[ii, 0] = sp.expand(p.xreplace(z0))
        ns = M.T.nullspace()
        gates = [sp.expand((n.T*vv)[0, 0]) for n in ns]
        gates = [g for g in gates if g != 0]
        if not gates: break
        prog = False
        for g in gates:
            fs = strip(g)
            if len(fs) == 0:
                print(f"d={d}: gate is a NONZERO CONSTANT -> EMPTY on this chart", flush=True)
                branched = True; break
            if len(fs) == 1:
                f = fs[0][0]
                vs = [x for x in f.free_symbols if x not in NONZERO]
                if not vs:
                    print(f"d={d}: gate has no free variable -> EMPTY: {f}", flush=True)
                    branched = True; break
                piv = sorted(vs, key=lambda s: sp.degree(sp.Poly(f, s)))[0]
                s1 = sp.solve(f, piv, dict=True)
                if s1:
                    val = sp.cancel(s1[0][piv])
                    for den in sp.denom(sp.together(val)).free_symbols: denoms.add(str(den))
                    sub[piv] = sp.expand(val); sub = fixpoint(sub)
                    imposed.append(f); conditions.append((d, f)); prog = True; break
            else:
                print(f"d={d}: REDUCIBLE gate -> BRANCH POINT: {[str(f) for f,_ in fs]}", flush=True)
                branched = True; break
        if branched or not prog: break
    if branched: break
    cs = rung(d, sub); nv = [v for v in nv if v not in sub]
    s = sp.solve(cs, nv, dict=True) if (cs and nv) else [{}]
    if not s:
        print(f"d={d}: STUCK after imposing {len(imposed)}", flush=True); break
    for k, v in s[0].items():
        for den in sp.denom(sp.together(v)).free_symbols: denoms.add(str(den))
        sub[k] = sp.expand(sp.cancel(v))
    sub = fixpoint(sub)
    res = rung(d, sub)
    fr = [v for v in nv if v not in sub]; freep += fr
    print(f"d={d}: imposed {len(imposed)}, solved {len(s[0])}, free {len(fr)}, "
          f"residual {len(res)}, t={time.time()-t0:.0f}s", flush=True)
    for f in imposed: print(f"      FORCED: {f}", flush=True)
print("\nDENOMINATORS:", sorted(denoms))
print("FREE PARAMS carried:", len(freep))
pickle.dump((sub, freep, conditions), open(f'fast_{BETA}.pkl', 'wb'))
