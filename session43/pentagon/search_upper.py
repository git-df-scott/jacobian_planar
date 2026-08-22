#!/usr/bin/env python3
"""Search the upper-edge family against the 66 pentagon conditions.

The upper-edge theorem (upperedge.py, four controls PASS) says
    A(t) = sum_{i=0}^{8} p_{i+8,i} t^i  =  c0 * G(t)^2,  deg G = 4.
So nine of the pentagon's coefficients are a rational function of five
parameters.  Four of the nine are EARLY (p_8_0 .. p_11_3) and five are LATE
(p_12_4 .. p_16_8), so pinning them leaves 8 free late variables, in which the
66 conditions are still exactly affine.  Consistency is then a rank test costing
9 evaluations of the straight-line recursion -- milliseconds.

This is the NONEMPTY-seeking direction: a consistent point is a candidate.
"""
import sys, random
sys.path.insert(0, '.')
from pentev import conditions, VARS, EARLY, LATE, p

UP   = [f'p_{i+8}_{i}' for i in range(9)]
FREE = [v for v in LATE if v not in UP]            # 8 late unknowns
assert len(FREE) == 8

def Asq(g, c0):
    """coefficients of c0 * G(t)^2, G = sum g[i] t^i, deg 4 -> deg 8"""
    out = [0]*9
    for i in range(5):
        for j in range(5):
            out[i+j] = (out[i+j] + g[i]*g[j]) % p
    return [(c0*v) % p for v in out]

def rank_pair(M, v, ncols):
    """rank(M) and rank([M|v]) over F_p"""
    def rref(rows, nc):
        rows = [r[:] for r in rows]; rk = 0
        for c in range(nc):
            sel = next((i for i in range(rk, len(rows)) if rows[i][c] % p), None)
            if sel is None: continue
            rows[rk], rows[sel] = rows[sel], rows[rk]
            inv = pow(rows[rk][c], p-2, p)
            rows[rk] = [(z*inv) % p for z in rows[rk]]
            for i in range(len(rows)):
                if i != rk and rows[i][c] % p:
                    f = rows[i][c]
                    rows[i] = [(rows[i][j]-f*rows[rk][j]) % p for j in range(len(rows[i]))]
            rk += 1
            if rk == len(rows): break
        return rk
    rM = rref(M, ncols)
    rA = rref([M[i]+[v[i]] for i in range(len(M))], ncols+1)
    return rM, rA

def build(base, unknowns):
    """conditions = M . unknowns + v"""
    b = dict(base)
    for u in unknowns: b[u] = 0
    v = conditions(b)
    cols = []
    for u in unknowns:
        d = dict(b); d[u] = 1
        c = conditions(d)
        cols.append([(c[r]-v[r]) % p for r in range(66)])
    M = [[cols[c][r] for c in range(len(unknowns))] for r in range(66)]
    return M, v

def trial(seed, pin_upper=True):
    rnd = random.Random(seed)
    base = {v: rnd.randrange(1, p) for v in EARLY}
    if pin_upper:
        g  = [rnd.randrange(1, p) for _ in range(5)]
        c0 = rnd.randrange(1, p)
        ah = Asq(g, c0)
        for i in range(9):
            base[f'p_{i+8}_{i}'] = ah[i]
        unk = FREE
    else:
        unk = LATE
    M, v = build(base, unk)
    rM, rA = rank_pair(M, [(-z) % p for z in v], len(unk))
    return rM, rA, rM == rA

print("CONTROL A (baseline, all 13 late free, upper edge NOT pinned):")
base_hits = sum(trial(s, pin_upper=False)[2] for s in range(200))
print(f"   consistent at {base_hits}/200 random early points")

print("CONTROL B (rank test sanity: a planted right-hand side must be consistent)")
rnd = random.Random(99)
b = {v: rnd.randrange(1, p) for v in EARLY}
tgt = {u: rnd.randrange(1, p) for u in FREE}
M, v = build(b, FREE)
vplant = []
for r in range(66):
    s = v[r]
    for c, u in enumerate(FREE): s = (s + M[r][c]*tgt[u]) % p
    vplant.append(s)
rM, rA = rank_pair(M, [(-(vplant[r]-v[r]) - v[r]) % p for r in range(66)], len(FREE))
print(f"   planted: rank {rM} vs {rA} -> {'PASS' if rM == rA else 'FAIL'}")

print("CONTROL C (negative: perturb the rhs off the column space)")
vbad = [(-(v[r]) + (7 if r == 0 else 0)) % p for r in range(66)]
rM, rA = rank_pair(M, vbad, len(FREE))
print(f"   perturbed: rank {rM} vs {rA} -> {'PASS (inconsistent)' if rM != rA else 'INCONCLUSIVE'}")

print("\nSEARCH (upper edge pinned to c0*G^2):")
hits = []
N = 3000
for s in range(N):
    rM, rA, ok = trial(s, pin_upper=True)
    if ok: hits.append(s)
print(f"   consistent at {len(hits)}/{N} random (G, early) points")
if hits: print("   seeds:", hits[:20])
