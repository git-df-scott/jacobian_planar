#!/usr/bin/env python3
"""Session 44, Lead 3 — topological sieve for degree-d Keller maps with
irreducible tear, at the open floor d = 6.

Setting.  Let F be a planar Keller counterexample of geometric degree d whose
Jelonek/tear set A is irreducible with constant fibre count.  Session 43's
tear theorem (claude/jacobian-collision-counterexample-nsc6ul, session43/
tear_theorem.py + README) forces: fibre count on A is 1, chi(A) = 1, A is a
rational cuspidal curve with one place at infinity.  Off A the map is a
proper etale d-sheeted covering of U = C^2 \\ A.  For a one-Puiseux-pair tear
A ~ {y^q = x^p} (gcd(p,q)=1), pi_1(U) is the torus-knot group
G = <u, v | u^p = v^q> (Zariski), abelianization u -> q, v -> p, meridian
class m = u^alpha v^beta with q*alpha + p*beta = 1, center z = u^p.

Necessary conditions on the monodromy rho: G -> S_d of the covering:
  T  rho transitive (source connected);
  M  sigma = rho(m) fixes a sheet i0 (the unique point of F^{-1}(A) over a
     smooth point of A; unramified, so the filling sheet is a 1-cycle);
  L  the longitude ell = z * m^{-pq} also fixes i0, i.e. rho(z)(i0) = i0
     (F^{-1}(A) is irreducible and maps 1:1, so the filling sheet is
     preserved around the whole curve);
  H  the cover X' is again C^2 minus an irreducible curve (X' = C^2 \\
     F^{-1}(A), and F^{-1}(A) is a curve), so H_1(X') = Z and H_2(X') = 0.
     The presentation 2-complex of G is aspherical (one-relator, torsion
     free; X ~ S^3 \\ K(p,q)), so subgroup homology = homology of the lifted
     chain complex  Z^d --d2--> Z^{2d} --d1--> Z^d,  computed by Smith form.

The sieve enumerates all (U, V) in S_d^2 with U^p = V^q and reports the
surviving monodromy types up to simultaneous conjugacy.  Controls: d = 2
must be EMPTY by pure group theory (sigma with a fixed point in a transitive
subgroup of S_2 forces rho trivial); d = 3 must be NONEMPTY (Orevkov, not
topology, is what kills d = 3, and Alpoge's 3D map realizes the {3,1,0}
pattern) — the sieve is a necessary-condition filter, not a sufficiency
proof.  Survivors are construction targets, not counterexamples.
"""
import argparse
import itertools
from math import gcd


def perms(n):
    return list(itertools.permutations(range(n)))


def pmul(a, b):
    return tuple(a[b[i]] for i in range(len(b)))


def ppow(a, e):
    n = len(a)
    r = tuple(range(n))
    base = a
    while e:
        if e & 1:
            r = pmul(base, r)
        base = pmul(base, base)
        e >>= 1
    return r


def pinv(a):
    n = len(a)
    r = [0] * n
    for i in range(n):
        r[a[i]] = i
    return tuple(r)


def transitive(U, V):
    n = len(U)
    seen = {0}
    stack = [0]
    while stack:
        i = stack.pop()
        for g in (U, V):
            j = g[i]
            if j not in seen:
                seen.add(j)
                stack.append(j)
    return len(seen) == n


def cycle_type(a):
    n = len(a)
    seen = [False] * n
    out = []
    for i in range(n):
        if not seen[i]:
            l, j = 0, i
            while not seen[j]:
                seen[j] = True
                j = a[j]
                l += 1
            out.append(l)
    return tuple(sorted(out, reverse=True))


def smith(mat):
    """Smith normal form diagonal of an integer matrix (small sizes)."""
    import copy
    m = copy.deepcopy(mat)
    rows, cols = len(m), len(m[0]) if m else 0
    diag = []
    r = c = 0
    while r < rows and c < cols:
        # find pivot with minimal nonzero abs value
        best = None
        for i in range(r, rows):
            for j in range(c, cols):
                if m[i][j] and (best is None or abs(m[i][j]) < abs(best[2])):
                    best = (i, j, m[i][j])
        if best is None:
            break
        bi, bj, _ = best
        m[r], m[bi] = m[bi], m[r]
        for row in m:
            row[c], row[bj] = row[bj], row[c]
        again = True
        while again:
            again = False
            for i in range(r + 1, rows):
                if m[i][c]:
                    q = m[i][c] // m[r][c]
                    for j in range(c, cols):
                        m[i][j] -= q * m[r][j]
                    if m[i][c]:
                        m[r], m[i] = m[i], m[r]
                        again = True
            for j in range(c + 1, cols):
                col_val = m[r][j]
                if col_val:
                    q = col_val // m[r][c]
                    for i in range(r, rows):
                        m[i][j] -= q * m[i][c]
                    if m[r][j]:
                        for i in range(rows):
                            m[i][c], m[i][j] = m[i][j], m[i][c]
                        again = True
        diag.append(abs(m[r][c]))
        r += 1
        c += 1
    return diag, rows, cols


def cover_homology(U, V, p, q):
    """H_1 and H_2 of the d-sheet cover of the presentation complex of
    <u,v | u^p v^-q>, with sheets permuted by U (edge u) and V (edge v).
    Returns (h1_rank, h1_torsion, h2_rank)."""
    d = len(U)
    # C1 basis: u-edges 0..d-1, v-edges d..2d-1.  d1(u_i) = [U(i)] - [i].
    d1 = [[0] * (2 * d) for _ in range(d)]
    for i in range(d):
        d1[U[i]][i] += 1
        d1[i][i] -= 1
        d1[V[i]][d + i] += 1
        d1[i][d + i] -= 1
    # face lifted at sheet i: walk u^p then v^{-q}
    d2 = [[0] * d for _ in range(2 * d)]
    for i in range(d):
        cur = i
        for _ in range(p):
            d2[cur][i] += 1
            cur = U[cur]
        # now at U^p(i); walk v^{-q}: each step goes backwards along a v-edge
        for _ in range(q):
            cur = pinv(V)[cur]
            d2[d + cur][i] -= 1
    diag2, _, _ = smith([row[:] for row in d2])
    rank2 = sum(1 for x in diag2 if x)
    h2 = d - rank2
    diag1, _, _ = smith([row[:] for row in d1])
    rank1 = sum(1 for x in diag1 if x)
    # H1 = ker d1 / im d2 ; rank = (2d - rank1) - rank2 ; torsion from the
    # Smith form of d2 restricted to ker d1 — compute H1 of the pair by the
    # standard trick: H1 rank = 2d - rank1 - rank2; torsion = nontrivial
    # invariant factors of the composite... for our accept test (H1 = Z,
    # torsion-free) compute homology exactly on the quotient:
    h1_rank = 2 * d - rank1 - rank2
    torsion = [x for x in diag2 if x not in (0, 1)]
    return h1_rank, torsion, h2


def canonical(U, V, allp):
    best = None
    for g in allp:
        gi = pinv(g)
        cu = pmul(g, pmul(U, gi))
        cv = pmul(g, pmul(V, gi))
        key = (cu, cv)
        if best is None or key < best:
            best = key
    return best


def sieve(d, pmax, verbose=True):
    allp = perms(d)
    # one representative per conjugacy class of U (simultaneous conjugacy
    # lets us fix U up to conjugacy; survivors are canonicalized anyway)
    reps = {}
    for U in allp:
        reps.setdefault(cycle_type(U), U)
    ureps = list(reps.values())
    survivors = {}
    tried_pairs = 0
    for q in range(2, pmax + 1):
        for p in range(q + 1, pmax + 1):
            if gcd(p, q) != 1:
                continue
            # meridian exponents: q*alpha + p*beta = 1
            alpha = pow(q, -1, p) if p > 1 else 0
            beta = (1 - q * alpha) // p
            for U in ureps:
                Up = ppow(U, p)
                for V in allp:
                    if ppow(V, q) != Up:
                        continue
                    tried_pairs += 1
                    if not transitive(U, V):
                        continue
                    sigma = pmul(ppow(U, alpha % (10**6)) if alpha >= 0
                                 else pinv(ppow(U, -alpha)),
                                 ppow(V, beta) if beta >= 0
                                 else pinv(ppow(V, -beta)))
                    Z = Up
                    fills = [i for i in range(d)
                             if sigma[i] == i and Z[i] == i]
                    if not fills:
                        continue
                    h1r, tor, h2 = cover_homology(U, V, p, q)
                    if h1r != 1 or tor or h2 != 0:
                        continue
                    key = canonical(U, V, allp)
                    tag = (p, q)
                    if key not in survivors.get(tag, {}):
                        survivors.setdefault(tag, {})[key] = (
                            cycle_type(U), cycle_type(V), cycle_type(sigma),
                            len(fills))
                        if verbose:
                            print(f"d={d} (p,q)=({p},{q}) SURVIVOR "
                                  f"U~{cycle_type(U)} V~{cycle_type(V)} "
                                  f"meridian~{cycle_type(sigma)} "
                                  f"fills={len(fills)}", flush=True)
    total = sum(len(v) for v in survivors.values())
    print(f"d={d}, p,q <= {pmax}: {total} surviving monodromy types "
          f"({tried_pairs} pairs examined)")
    return survivors


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, default=6)
    ap.add_argument("--pmax", type=int, default=12)
    a = ap.parse_args()
    print("== control d=2 (must be EMPTY) ==")
    s2 = sieve(2, 7, verbose=False)
    assert not s2, f"d=2 control failed: {s2}"
    print("== control d=3 (must be NONEMPTY) ==")
    s3 = sieve(3, 7, verbose=False)
    assert s3, "d=3 control failed: sieve kills everything, too strong"
    print({k: len(v) for k, v in s3.items()})
    print(f"== main run d={a.d}, pmax={a.pmax} ==")
    s = sieve(a.d, a.pmax)
    for tag, reps in sorted(s.items()):
        kinds = {}
        for key, (cu, cv, cs, nf) in reps.items():
            kinds.setdefault((cu, cv, cs), 0)
            kinds[(cu, cv, cs)] += 1
        print(tag, "->", kinds)
