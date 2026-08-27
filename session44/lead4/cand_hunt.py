#!/usr/bin/env python3
"""Candidate hunt: modular Newton on the reduced residual of loose charts.

The campaign's run_pair only RANK-PROBES (linear tangent dimension). It never
tries to SOLVE  residual(vec) = 0  with the required Newton vertices nonzero.
A zero of the residual with live vertices IS a candidate reduced solution of
the Keller system for that published shape -- the first from an open case.

This reuses trackB1_shapes' exact build/conds (so it is calibrated by
construction: same recurrence, same modulus p=65521) and runs Newton mod p
from many random starts on each loose chart, checking at each hit that the
required driver/partner vertices are nonzero.  Hits are CANDIDATE-UNVERIFIED
until char-0 reconstruction + exact replay.
"""
import random
import sys

import trackB1_shapes as SH
from trackB1_polygon import p
from trackD_chain_map import all_chains, reduced_candidates, check_eps

INV = lambda a: pow(a % p, p - 2, p)  # noqa: E731


def residual_and_jac(pair, vec):
    """Return (val, J) at parameter vector vec, or None if p10=0."""
    o = pair.orient()
    if o is None:
        return None
    val0 = _conds(pair, vec, None)
    if val0 is None:
        return None
    n = len(vec)
    cols = []
    for k in range(n):
        c = _conds(pair, vec, k)
        if c is None:
            return None
        cols.append(c[1])   # derivative wrt param k (the eps channel)
    m = len(val0)
    J = [[cols[k][r] for k in range(n)] for r in range(m)]
    return val0, J


def _conds(pair, vec, k):
    """Thin wrapper reproducing run_pair's inner conds(build(vec,k))."""
    import trackB1_shapes as S
    # Rebuild the closures by calling run_pair's machinery indirectly:
    # easier to inline via the module's helpers.
    return S._external_conds(pair, vec, k)  # provided by patch below


def newton(pair, idx, rng, iters=40):
    vec = [rng.randrange(p) for _ in idx]
    vec[idx.index((0, 1))] = rng.randrange(1, p)
    for _ in range(iters):
        rj = residual_and_jac(pair, vec)
        if rj is None:
            return None
        val, J = rj
        if all(v % p == 0 for v in val):
            return vec
        vec = gauss_newton_step(vec, val, J)
        if vec is None:
            return None
    rj = residual_and_jac(pair, vec)
    if rj and all(v % p == 0 for v in rj[0]):
        return vec
    return None


def gauss_newton_step(vec, val, J):
    """One least-norm Newton step over F_p: solve J dx = val, dx minimal."""
    m = len(val)
    n = len(vec)
    A = [row[:] + [val[r] % p] for r, row in enumerate(J)]
    piv_col = {}
    r = 0
    for c in range(n):
        pr = next((k for k in range(r, m) if A[k][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = INV(A[r][c])
        A[r] = [(x * iv) % p for x in A[r]]
        for k in range(m):
            if k != r and A[k][c] % p:
                f = A[k][c]
                A[k] = [(A[k][j] - f * A[r][j]) % p for j in range(n + 1)]
        piv_col[c] = r
        r += 1
        if r == m:
            break
    for k in range(r, m):
        if A[k][n] % p:
            return None   # inconsistent -> Newton stuck
    dx = [0] * n
    for c, rr in piv_col.items():
        dx[c] = A[rr][n]
    return [(vec[i] - dx[i]) % p for i in range(n)]


def main():
    seed = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    starts = int(sys.argv[2]) if len(sys.argv) > 2 else 200
    rng = random.Random(seed)
    existing_names = set()
    charts = []
    for ch in all_chains():
        cands, _ = reduced_candidates(ch)
        for cd in cands:
            if not check_eps(cd)[0]:
                continue
            cd["mode"] = "hunt"
            cd["size"] = 0
            charts.append((ch, cd))
    print(f"{len(charts)} eps-passing charts to probe", flush=True)
    for ch, cd in charts:
        pair = SH.Pair(f"{ch.name}", cd["NP"], cd["NQ"], [(cd["r"], 0, 1)], "")
        o = pair.orient()
        if o is None:
            continue
        DR = o[0]
        idx = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]
        hits = 0
        for _ in range(starts):
            sol = newton(pair, idx, rng)
            if sol is not None:
                # vertex liveness: driver top and p10 nonzero
                if sol[idx.index((0, 1))] % p:
                    hits += 1
        tag = f"{ch.name} max={ch.maxdeg} r={cd['r']}"
        if hits:
            print(f"  CANDIDATE HITS {hits}/{starts}: {tag}", flush=True)
        else:
            print(f"  0/{starts} (residual has no live-vertex zero found): {tag}",
                  flush=True)


if __name__ == "__main__":
    main()
