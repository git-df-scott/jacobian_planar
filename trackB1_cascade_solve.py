#!/usr/bin/env python3
"""Level-by-level cascade solver on the PERFECT-SQUARE locus (S = A^2).

By trackB1_THEOREM_S_square.md, S = A^2. The ladder is triangular: at level m
the divisibility condition S^3 | N_m is LINEAR in the newest undetermined slice
P_{9-m} (the term 3*gamma*P_8^2*P_{8-m} is S^4-divisible, so the newest slice
never obstructs its own level). So the whole of P below weight 7 is DETERMINED,
one slice per level, by linear solves — and each level is overdetermined
(up to 12 divisibility conditions against <= 9 unknowns), so the generic
outcome is death at a specific level.

Free data after normalization: A (2 coeffs, A(0)=1), and P_7 = A*M with
deg M <= 6 (the level-2 condition S | P_7^2 <=> A | P_7). ~9 parameters.
"""
import random, sys
from trackB1_sqrt import pmul, padd, pscal, pderiv, ptrim, pdiv_exact, prange

def prem(f, g, p):
    f = list(f)
    if len(f) < len(g): return ptrim(f)
    inv = pow(g[-1], p-2, p)
    for k in range(len(f)-len(g), -1, -1):
        c = (f[k+len(g)-1]*inv) % p
        if c:
            for i, gi in enumerate(g):
                f[k+i] = (f[k+i] - c*gi) % p
    return ptrim(f[:len(g)-1])

def run(A, M, p, a=1, b=1, verbose=False):
    S = pmul(A, A, p)
    S3 = pmul(pmul(S,S,p), S, p)
    gamma = (b*b % p) * pow(pow(a,3,p), p-2, p) % p
    P = {8: pscal(pmul(S,S,p), a, p), 7: pmul(A, M, p)}
    F = {12: pscal(pmul(pmul(S,S,p),S,p), b, p)}
    twoF12 = pscal(F[12], 2, p)

    def build(m, trial):          # N_m with trial value for P_{9-m}
        Pl = dict(P); Fl = dict(F)
        w_new = 9 - m
        if trial is not None and w_new >= -1: Pl[w_new] = trial
        # F_{12-k} for k < m needs P_{8-k}; compute lazily
        for k in range(1, m):
            if 12-k in Fl: continue
            W2 = 24-k
            N = pscal(p3(Pl, W2, p), gamma, p)
            for q in list(Fl):
                if W2-q in Fl and q <= 11 and W2-q <= 11:
                    N = padd(N, pscal(pmul(Fl[W2-q], Fl[q], p), -1, p), p)
            q_ = pdiv_exact(N, twoF12, p)
            if q_ is None: return None
            Fl[12-k] = q_
        W = 24-m
        N = pscal(p3(Pl, W, p), gamma, p)
        for q in list(Fl):
            if W-q in Fl and q <= 11 and W-q <= 11:
                N = padd(N, pscal(pmul(Fl[W-q], Fl[q], p), -1, p), p)
        return N

    def p3(Pd, W, p):
        out = []
        ws = sorted(Pd)
        for w1 in ws:
            for w2 in ws:
                for w3 in ws:
                    if w1+w2+w3 == W:
                        out = padd(out, pmul(pmul(Pd[w1],Pd[w2],p),Pd[w3],p), p)
        return out

    for m in range(2, 23):
        w_new = 9 - m
        rng = prange(w_new) if w_new >= -1 else None
        if rng is None:            # pure obstruction level
            N = build(m, None)
            if N is None: return ("LADDER_BREAK", m, None)
            if prem(N, S3, p): return ("OBSTRUCTED", m, None)
        else:
            lo, hi = rng
            nun = hi - lo + 1
            base = build(m, [0]*(hi+1))
            if base is None: return ("LADDER_BREAK", m, None)
            r0 = prem(base, S3, p)
            cols = []
            for i in range(lo, hi+1):
                e = [0]*i + [1]
                Ni = build(m, e)
                if Ni is None: return ("LADDER_BREAK", m, None)
                cols.append(padd(prem(Ni, S3, p), pscal(r0, -1, p), p))
            n = max([len(c) for c in cols] + [len(r0), 1])
            Mx = [[(cols[k][r] if r < len(cols[k]) else 0) for k in range(nun)] +
                  [(-r0[r]) % p if r < len(r0) else 0] for r in range(n)]
            row = 0; piv_of = {}
            for col in range(nun):
                piv = next((r for r in range(row, n) if Mx[r][col]), None)
                if piv is None: continue
                Mx[row], Mx[piv] = Mx[piv], Mx[row]
                inv = pow(Mx[row][col], p-2, p)
                Mx[row] = [(v*inv) % p for v in Mx[row]]
                for r in range(n):
                    if r != row and Mx[r][col]:
                        f = Mx[r][col]
                        Mx[r] = [(Mx[r][c]-f*Mx[row][c]) % p for c in range(nun+1)]
                piv_of[col] = row; row += 1
            if any(all(Mx[r][c] == 0 for c in range(nun)) and Mx[r][nun] for r in range(n)):
                return ("OBSTRUCTED", m, None)
            sol = [0]*(hi+1)
            for col in range(nun):
                if col in piv_of: sol[lo+col] = Mx[piv_of[col]][nun]
            P[w_new] = ptrim(sol)
        F.clear(); F[12] = pscal(pmul(pmul(S,S,p),S,p), b, p)
    return ("SURVIVED_LADDER", None, P)

if __name__ == "__main__":
    p = 65521; random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
    n = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    from collections import Counter
    tally = Counter()
    for _ in range(n):
        A = [1, random.randrange(p), random.randrange(1, p)]
        M = [random.randrange(p) for _ in range(7)]
        v, lvl, *_ = run(A, M, p)
        tally[(v, lvl)] += 1
    for k, c in sorted(tally.items(), key=lambda t: (-t[1], str(t[0]))):
        print(f"  {k[0]:>16}  level {k[1]}:  {c}/{n}")
