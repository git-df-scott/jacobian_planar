"""Source-side enumeration: boundary trees of compactifications of C^2 and the
integer data of a Keller map at infinity.

A compactification Y of C^2 is obtained from P^2 by blowing up points on the boundary.
Each boundary component E_i carries its self-intersection, and k_i = -ord_{E_i}(dx dy)
(k = 3 on the line at infinity; blowing up a free point on E gives k_new = k_E - 1;
blowing up E1 meets E2 gives k_new = k_1 + k_2 - 1).  For a Keller map (P, Q) with
pole orders m_i, n_i along E_i:
  ord_{E_i}(dP dQ) >= -(m_i + n_i + 1), with equality iff the leading forms are independent,
and dP dQ = c dx dy forces ord = -k_i, so delta_i = m_i + n_i + 1 - k_i >= 0.
The pole vector m is determined by the P-dicritical components (where P is regular and
nonconstant, of degree d_j on E_j): M m = d_P with M the intersection matrix (unimodular).
Geometric degree D = m . d_Q = n . d_P.
"""
import itertools, sys
from fractions import Fraction
import numpy as np

class Tree:
    def __init__(self):
        self.selfint = [1]          # P^2 line at infinity
        self.k = [3]
        self.adj = {0: set()}
        self.history = []
    def copy(self):
        T = Tree(); T.selfint = list(self.selfint); T.k = list(self.k)
        T.adj = {i: set(s) for i, s in self.adj.items()}; T.history = list(self.history); return T
    def blowup_free(self, i):
        T = self.copy(); j = len(T.selfint)
        T.selfint.append(-1); T.k.append(T.k[i] - 1); T.selfint[i] -= 1
        T.adj[j] = {i}; T.adj[i].add(j); T.history.append(('f', i)); return T
    def blowup_edge(self, i, j):
        T = self.copy(); l = len(T.selfint)
        T.selfint.append(-1); T.k.append(T.k[i] + T.k[j] - 1)
        T.selfint[i] -= 1; T.selfint[j] -= 1
        T.adj[i].discard(j); T.adj[j].discard(i)
        T.adj[l] = {i, j}; T.adj[i].add(l); T.adj[j].add(l); T.history.append(('e', i, j)); return T
    def matrix(self):
        r = len(self.selfint); M = np.zeros((r, r), dtype=object)
        for i in range(r):
            M[i, i] = self.selfint[i]
            for j in self.adj[i]: M[i, j] = 1
        return M
    def canon(self):
        # crude canonical form: sorted multiset of (selfint, k, degree) plus edges up to relabel by (selfint,k)
        r = len(self.selfint)
        lab = sorted(((self.selfint[i], self.k[i], len(self.adj[i])) for i in range(r)))
        return tuple(lab)

def gen_trees(maxblow):
    out = {}
    frontier = [Tree()]
    for step in range(maxblow + 1):
        nxt = []
        for T in frontier:
            key = (len(T.selfint), T.canon(), tuple(sorted((min(i, j), max(i, j)) for i in T.adj for j in T.adj[i])))
            if key in out: continue
            out[key] = T
            if step == maxblow: continue
            r = len(T.selfint)
            for i in range(r):
                nxt.append(T.blowup_free(i))
                for j in T.adj[i]:
                    if j > i: nxt.append(T.blowup_edge(i, j))
        frontier = nxt
    return list(out.values())

def solve_int(M, d):
    r = len(d)
    A = [[Fraction(int(M[i, j])) for j in range(r)] + [Fraction(int(d[i]))] for i in range(r)]
    # gaussian elimination
    for c in range(r):
        p = next((i for i in range(c, r) if A[i][c] != 0), None)
        if p is None: return None
        A[c], A[p] = A[p], A[c]
        piv = A[c][c]
        A[c] = [x / piv for x in A[c]]
        for i in range(r):
            if i != c and A[i][c] != 0:
                f = A[i][c]; A[i] = [a - f * b for a, b in zip(A[i], A[c])]
    sol = [A[i][r] for i in range(r)]
    if any(x.denominator != 1 for x in sol): return None
    return [int(x) for x in sol]

def analyse_tree(T, maxdeg=2, Dmax=12):
    r = len(T.selfint); M = T.matrix()
    results = []
    comps = list(range(r))
    # choose P-dicritical set (nonempty) with degrees, Q-dicritical set with degrees
    choices = []
    for size in (1, 2):
        for sub in itertools.combinations(comps, size):
            for degs in itertools.product(range(1, maxdeg + 1), repeat=size):
                d = [0] * r
                for j, dj in zip(sub, degs): d[j] = dj
                m = solve_int(M, d)
                if m is None: continue
                if any(m[j] != 0 for j in sub): continue          # P regular on its dicriticals
                if any(x < 0 for x in m): continue                 # poles only
                choices.append((sub, degs, m))
    for (subP, degP, m) in choices:
        for (subQ, degQ, n) in choices:
            delta = [m[i] + n[i] + 1 - T.k[i] for i in range(r)]
            if min(delta) < 0: continue
            dQ = [0] * r
            for j, dj in zip(subQ, degQ): dQ[j] = dj
            D = sum(m[i] * dQ[i] for i in range(r))
            dP = [0] * r
            for j, dj in zip(subP, degP): dP[j] = dj
            D2 = sum(n[i] * dP[i] for i in range(r))
            if D != D2 or D < 2 or D > Dmax: continue
            # fibre genus of P by adjunction on the closure ~ sum m_i E_i
            KE = [-2 - T.selfint[i] for i in range(r)]
            mm = sum(m[i] * m[j] * int(M[i, j]) for i in range(r) for j in range(r))
            gP = (mm + sum(m[i] * KE[i] for i in range(r))) // 2 + 1
            nn = sum(n[i] * n[j] * int(M[i, j]) for i in range(r) for j in range(r))
            gQ = (nn + sum(n[i] * KE[i] for i in range(r))) // 2 + 1
            placesP = sum(degP); placesQ = sum(degQ)
            chiP = 2 - 2 * gP - placesP; chiQ = 2 - 2 * gQ - placesQ
            if gP < 0 or gQ < 0: continue
            if chiP > -1 or chiQ > -1: continue     # fibres are not C or C*
            # components of the escaping curve: m_i = n_i = 0 and not both dicritical-constant
            R = [i for i in range(r) if m[i] == 0 and n[i] == 0]
            results.append(dict(D=D, m=m, n=n, delta=delta, P=(subP, degP), Q=(subQ, degQ), gP=gP, gQ=gQ, chi=(chiP, chiQ), R=R))
    return results

if __name__ == '__main__':
    maxblow = int(sys.argv[1]) if len(sys.argv) > 1 else 5
    trees = gen_trees(maxblow)
    print(len(trees), 'trees with at most', maxblow, 'blowups')
    tot = 0
    for T in trees:
        res = analyse_tree(T)
        if res:
            tot += len(res)
            print('tree', T.history, 'selfint', T.selfint, 'k', T.k)
            for x in res[:6]:
                print('   ', x)
    print('total survivors', tot)
