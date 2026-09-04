#!/usr/bin/env python3
"""Direct counterexample hunt using bilinearity.  CONTROL FIRST.

For FIXED h the bracket is LINEAR in g, so one trial is a single linear solve
over F_p rather than a Groebner basis.  That makes a real search possible:
sample h, solve for g, and a consistent solve IS a counterexample candidate.

ERRATUM A15 DISCIPLINE.  Last time I built a search like this I ran 3000 points,
got 0/3000, and only THEN ran the planted control -- which failed, because the
harness had built the right-hand side wrong.  The whole run was void.  So here
the control runs FIRST and the search refuses to start unless it passes:

    pick random h and random g0, set v' = M(h) g0, and solve M(h) g = v'.
    g0 is a solution by construction, so the solve MUST report consistent.

Only if that passes does the real right-hand side get used.
"""
import sympy as sp, random, sys
P = 2147483647
z = sp.Symbol('z'); TAU = 1; s = z + 1
def hsup(a):
    return [i for i in range(9) if 0 <= i+a <= 16 and max(0,(i+a)-8) <= i <= min(8,(i+a)//2+1)]
def gsup(b):
    return [k for k in range(13) if (k+b) >= 0 and ((k+1)//2 if k <= 2 else 2*k-3) <= k+b <= 12+k]
HS = {a: hsup(a) for a in range(0,8)}
GS = {b: gsup(b) for b in range(0,12)}
gvars = [(b,k) for b in range(0,12) for k in GS[b]]
gidx = {vk: j for j, vk in enumerate(gvars)}
print(f"h-block free coefficients: {sum(len(v) for v in HS.values())}")
print(f"g-block unknowns: {len(gvars)}")

def poly_mul(A, B):
    C = [0]*(len(A)+len(B)-1)
    for i, a in enumerate(A):
        if a:
            for j, b in enumerate(B):
                if b: C[i+j] = (C[i+j] + a*b) % P
    return C
def dz(A): return [(i*a) % P for i, a in enumerate(A)][1:] or [0]

def build(hval):
    """rows: 261 equations; returns M (list of dict col->coef) and rhs list"""
    H = {8: [0]*8+[1], -1: [1,1]}
    for a in range(0,8):
        v = [0]*(max(HS[a])+1)
        for i in HS[a]: v[i] = hval[(a,i)]
        H[a] = v
    G12 = [0]*12+[1]; Gm1 = [1,2,1]          # s^2 = (z+1)^2
    rows = {}
    def add(L, coeffs, col):
        for e, c in enumerate(coeffs):
            if c % P: rows.setdefault((L,e), {})[col] = (rows.setdefault((L,e),{}).get(col,0)+c) % P
    rhs = {}
    for L in range(20,-3,-1):
        for a in range(-1,9):
            b = L-a
            if a not in H and a not in (8,-1): continue
            if a in H: Ha = H[a]
            else: continue
            if b == 12: Gb = G12
            elif b == -1: Gb = Gm1
            elif 0 <= b <= 11: Gb = None
            else: continue
            if Gb is not None:                              # known g -> right-hand side
                t = [(b*x) % P for x in poly_mul(dz(Ha), Gb)]
                u = [(a*x) % P for x in poly_mul(Ha, dz(Gb))]
                for e in range(max(len(t), len(u))):
                    val = ((t[e] if e < len(t) else 0) - (u[e] if e < len(u) else 0)) % P
                    if val: rhs[(L,e)] = (rhs.get((L,e),0) + val) % P
            else:                                            # unknown g -> matrix
                for k in GS[b]:
                    ek = [0]*k + [1]
                    t = [(b*x) % P for x in poly_mul(dz(Ha), ek)]
                    u = [(a*x) % P for x in poly_mul(Ha, dz(ek))]
                    for e in range(max(len(t), len(u))):
                        val = ((t[e] if e < len(t) else 0) - (u[e] if e < len(u) else 0)) % P
                        if val:
                            d = rows.setdefault((L,e), {})
                            d[gidx[(b,k)]] = (d.get(gidx[(b,k)],0) + val) % P
    # target: level -2 must equal s^2, everything else 0
    tgt = {}
    for e, c in enumerate([1,2,1]): tgt[(-2,e)] = c
    keys = sorted(set(list(rows.keys()) + list(rhs.keys()) + list(tgt.keys())))
    M = [[rows.get(k,{}).get(j,0) for j in range(len(gvars))] for k in keys]
    V = [ (tgt.get(k,0) - rhs.get(k,0)) % P for k in keys ]
    return M, V

def rank_and_consistent(M, V):
    m, n = len(M), len(M[0])
    A = [row[:] + [V[i]] for i, row in enumerate(M)]
    r = 0
    for c in range(n):
        piv = next((i for i in range(r, m) if A[i][c] % P), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        inv = pow(A[r][c], P-2, P)
        A[r] = [(x*inv) % P for x in A[r]]
        for i in range(m):
            if i != r and A[i][c] % P:
                f = A[i][c]
                A[i] = [(A[i][j] - f*A[r][j]) % P for j in range(n+1)]
        r += 1
        if r == m: break
    bad = any(all(A[i][j] % P == 0 for j in range(n)) and A[i][n] % P for i in range(m))
    return r, (not bad)

random.seed(12345)
def randh(): return {(a,i): random.randrange(1,P) for a in range(0,8) for i in HS[a]}

# ---------- PLANTED CONTROL, RUN FIRST ----------
h0 = randh()
M, V = build(h0)
print(f"system: {len(M)} equations x {len(M[0])} unknowns")
g0 = [random.randrange(0,P) for _ in range(len(gvars))]
Vp = [sum(M[i][j]*g0[j] for j in range(len(g0))) % P for i in range(len(M))]
r_c, ok_c = rank_and_consistent(M, Vp)
print(f"PLANTED CONTROL: rank {r_c}, consistent = {ok_c}  (MUST be True)")
if not ok_c:
    print("*** CONTROL FAILED -- harness is wrong, search aborted (A15) ***"); sys.exit(1)
Vn = [(v+1) % P for v in Vp]
r_n, ok_n = rank_and_consistent(M, Vn)
print(f"NEGATIVE CONTROL (rhs perturbed): consistent = {ok_n}  (should usually be False)")
r0, ok0 = rank_and_consistent(M, V)
print(f"\nREAL right-hand side at a random h: rank {r0} of {len(M[0])} columns, "
      f"consistent = {ok0}")
print(f"left-kernel dimension = {len(M)} - {r0} = {len(M)-r0}  "
      f"(that many conditions on h)")
