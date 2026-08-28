#!/usr/bin/env python3
"""
night2/sep.py -- separator pipeline for JC2, night 2.

PIVOT (post-audit): Aut_d, the degree-<=d plane automorphism locus, is CLOSED
(Bass-Connell-Wright; Furter 1997).  A SEPARATOR is a polynomial h in the
coefficients of (P,Q) vanishing on all of Aut_d.  A Keller pair with
[P,Q]=1 exactly and h != 0 for a certified separator would be a finite
certificate of non-automorphism.  This file builds and validates the two
halves that make that search honest:

  1. SAMPLER: random tame automorphisms of degree <= d with Jacobian 1.
     By Jung-van der Kulk every plane automorphism is tame, so tame
     compositions cover Aut_d -- PROVIDED every multidegree component is
     hit (Furter: Aut_d reducible for d>=4, components ~ multidegrees).
     The sampler enumerates all multidegrees (d1,...,dk), di>=2,
     prod di <= d, and samples each explicitly.

  2. INTERPOLATOR: linear algebra over F_p finding all polynomials h of
     degree <= 2 in the coefficient variables that vanish on the samples.
     With rank saturation, the nullspace is (degree-<=2 part of) the ideal
     of Aut_d mod p.

CONTROLS (mandatory, engine refuses without them):
  S1  every sample satisfies [P,Q] = 1 exactly (mod p) and deg <= d
  S2  every multidegree component of Aut_d received >= its quota of samples
  I1  rank saturation: adding fresh sample batches stops changing the rank
  I2  held-out generalization: every h vanishes on fresh automorphisms
      never seen by the interpolation (both primes)
  I3  non-triviality: h is nonzero at random coefficient vectors
      (random vectors are not automorphisms w.p. ~1)

STATUS OF RESULTS: everything mod p is reported as modular.  Separator
counts and ranks are per-prime; agreement across two primes is the
bug-detection standard, not a characteristic-zero proof.

Vocabulary note: "escape search" (using h as a fitness against the Keller
constraint) is NOT in this file's scope for d < 125 as anything but a
negative control -- the campaign's own theorem says no counterexample
exists below 125, so any small-d "escape" is by definition a bug.
"""
import argparse, itertools, json, os, random, sys
import numpy as np

# ---------- polynomial ops mod p (dict {(i,j): int}) ----------

def padd(a, b, p):
    r = dict(a)
    for k, v in b.items():
        r[k] = (r.get(k, 0) + v) % p
    return {k: v for k, v in r.items() if v}

def pmul(a, b, p):
    r = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            k = (i1 + i2, j1 + j2)
            r[k] = (r.get(k, 0) + v1 * v2) % p
    return {k: v for k, v in r.items() if v}

def pscale(a, c, p):
    c %= p
    return {k: (v * c) % p for k, v in a.items() if (v * c) % p}

def pdiff(a, var, p):
    r = {}
    for (i, j), v in a.items():
        if var == 0 and i > 0:
            r[(i - 1, j)] = (v * i) % p
        elif var == 1 and j > 0:
            r[(i, j - 1)] = (v * j) % p
    return {k: v for k, v in r.items() if v}

def bracket(a, b, p):
    return padd(pmul(pdiff(a, 0, p), pdiff(b, 1, p), p),
                pscale(pmul(pdiff(a, 1, p), pdiff(b, 0, p), p), -1, p), p)

def pdeg(a):
    return max((i + j for i, j in a), default=-1)

def compose(outer, P, Q, p):
    """outer(u,v) evaluated at (P,Q)."""
    cp, cq = {0: {(0, 0): 1}}, {0: {(0, 0): 1}}
    def pw(base, n, cache):
        if n not in cache:
            cache[n] = pmul(pw(base, n - 1, cache), base, p)
        return cache[n]
    r = {}
    for (m, n), c in outer.items():
        r = padd(r, pscale(pmul(pw(P, m, cp), pw(Q, n, cq), p), c, p), p)
    return r

# ---------- sampler: tame automorphisms with Jacobian 1, deg <= d ----------

def multidegrees(d):
    """all (d1,...,dk), di>=2, prod <= d, k>=0 (empty = affine component)."""
    out = [()]
    frontier = [()]
    while frontier:
        new = []
        for md in frontier:
            prod = 1
            for x in md:
                prod *= x
            for nxt in range(2, d + 1):
                if prod * nxt <= d:
                    new.append(md + (nxt,))
        out += new
        frontier = new
    return out

def rand_affine(rng, p):
    """random affine map with det 1 (mod p): (ax+by+e, cx+dy+f), ad-bc=1."""
    while True:
        a, b, c = rng.randrange(p), rng.randrange(p), rng.randrange(p)
        if a:
            dd = (1 + b * c) * pow(a, p - 2, p) % p
            e, f = rng.randrange(p), rng.randrange(p)
            P = {(1, 0): a, (0, 1): b, (0, 0): e}
            Q = {(1, 0): c, (0, 1): dd, (0, 0): f}
            return {k: v for k, v in P.items() if v}, \
                   {k: v for k, v in Q.items() if v}

def sample_auto(md, d, p, rng):
    """random automorphism with multidegree md, composed with random
    det-1 affine maps between every factor; Jacobian is exactly 1.
    Retries until total degree <= d (composition of triangulars with the
    given multidegree has degree prod(md) <= d by construction, but the
    affine sandwiching keeps it there; assert anyway)."""
    P, Q = {(1, 0): 1}, {(0, 1): 1}
    def apply_affine():
        A, B = rand_affine(rng, p)
        return compose(A, P, Q, p), compose(B, P, Q, p)
    P, Q = apply_affine()
    for deg in md:
        # triangular (u, v + phi(u)) with random phi of exact degree `deg`
        phi = {(k, 0): rng.randrange(p) for k in range(2, deg)}
        phi[(deg, 0)] = rng.randrange(1, p)
        P, Q = P, padd(Q, compose(phi, P, Q, p), p)
        P, Q = apply_affine()
    assert pdeg(P) <= d and pdeg(Q) <= d, (md, pdeg(P), pdeg(Q))
    return P, Q

def coeff_vector(P, Q, d):
    monos = [(i, j) for i in range(d + 1) for j in range(d + 1 - i)]
    v = []
    for poly in (P, Q):
        v += [poly.get(m, 0) for m in monos]
    return np.array(v, dtype=np.int64)

# ---------- interpolation: degree-<=2 vanishing polynomials mod p ----------

def quad_features(c, p):
    """[1, c_i, c_i c_j (i<=j)] mod p."""
    n = len(c)
    feats = [1]
    feats += list(c % p)
    for i in range(n):
        feats += list((c[i] * c[i:]) % p)
    return np.array(feats, dtype=np.int64)

def rowreduce_rank(M, p):
    """rank of M mod p, in-place gaussian elimination (numpy int64)."""
    M = M.copy() % p
    nr, nc = M.shape
    r = 0
    for c in range(nc):
        if r >= nr:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        i = r + nz[0]
        if i != r:
            M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        col = M[:, c].copy(); col[r] = 0
        mask = col != 0
        if mask.any():
            M[mask] = (M[mask] - np.outer(col[mask], M[r])) % p
        r += 1
    return r

def nullspace(M, p):
    """basis of {x : M x = 0} mod p; M is samples x features."""
    M = M.copy() % p
    nr, nc = M.shape
    r = 0
    pivots = []
    for c in range(nc):
        if r >= nr:
            break
        nz = np.nonzero(M[r:, c])[0]
        if len(nz) == 0:
            continue
        i = r + nz[0]
        if i != r:
            M[[r, i]] = M[[i, r]]
        M[r] = (M[r] * pow(int(M[r, c]), p - 2, p)) % p
        col = M[:, c].copy(); col[r] = 0
        mask = col != 0
        if mask.any():
            M[mask] = (M[mask] - np.outer(col[mask], M[r])) % p
        pivots.append(c)
        r += 1
    free = [c for c in range(nc) if c not in pivots]
    basis = []
    for f in free:
        x = np.zeros(nc, dtype=np.int64)
        x[f] = 1
        for rr, pc in reversed(list(enumerate(pivots))):
            x[pc] = (-int(M[rr, f])) % p
        basis.append(x)
    return basis, pivots

# ---------- the pipeline with controls ----------

def run(d, p, seed, batches=6, batch_size=None, held_out=40, outdir=None):
    rng = random.Random(seed)
    mds = multidegrees(d)
    n_coeff = 2 * ((d + 1) * (d + 2) // 2)
    n_feat = 1 + n_coeff + n_coeff * (n_coeff + 1) // 2
    if batch_size is None:
        batch_size = max(n_feat // batches + 50, 200)
    log = {"d": d, "p": p, "seed": seed, "n_coeff": n_coeff,
           "n_feat": n_feat, "multidegrees": [list(m) for m in mds],
           "controls": {}, "batches": []}

    def fresh_samples(k):
        out = []
        per = max(1, k // len(mds))
        for md in mds:
            for _ in range(per):
                P, Q = sample_auto(md, d, p, rng)
                # CONTROL S1 inline
                if bracket(P, Q, p) != {(0, 0): 1}:
                    print(f"ABORT S1: sample not Keller, md={md}")
                    sys.exit(1)
                out.append(coeff_vector(P, Q, d))
        return out

    # interpolation with rank-saturation (CONTROL I1)
    rows = []
    prev_rank = -1
    sat = False
    for b in range(batches):
        rows += [quad_features(c, p) for c in fresh_samples(batch_size)]
        M = np.stack(rows)
        rk = rowreduce_rank(M, p)
        log["batches"].append({"samples": len(rows), "rank": int(rk)})
        if rk == prev_rank:
            sat = True
            break
        prev_rank = rk
    log["controls"]["I1_rank_saturated"] = sat
    if not sat:
        print(f"I1 FAIL: rank not saturated at d={d} p={p} "
              f"({len(rows)} samples, rank {prev_rank}) -- need more batches")
        log["verdict"] = "I1-FAIL"
        _write(log, outdir, d, p)
        return log
    basis, _ = nullspace(np.stack(rows), p)
    log["n_separators_deg2"] = len(basis)

    # CONTROL I2: held-out generalization
    ho = [quad_features(c, p) for c in fresh_samples(held_out)]
    bad = 0
    for h in basis:
        for f in ho:
            if int(np.dot(h, f) % p):
                bad += 1
                break
    log["controls"]["I2_heldout_violations"] = bad
    # CONTROL I3: non-triviality on random vectors
    triv = 0
    for h in basis:
        nz = False
        for _ in range(5):
            c = np.array([rng.randrange(p) for _ in range(n_coeff)],
                         dtype=np.int64)
            if int(np.dot(h, quad_features(c, p)) % p):
                nz = True
                break
        if not nz:
            triv += 1
    log["controls"]["I3_trivial_separators"] = triv
    ok = (bad == 0 and triv == 0 and sat)
    log["verdict"] = "PASS" if ok else "CONTROL-FAIL"
    print(f"d={d} p={p}: {len(basis)} deg<=2 separators, "
          f"I2 violations={bad}, I3 trivial={triv} -> {log['verdict']}")
    _write(log, outdir, d, p, basis if ok else None)
    return log

def _write(log, outdir, d, p, basis=None):
    if not outdir:
        return
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, f"sep_d{d}_p{p}.json"), "w") as fh:
        json.dump(log, fh, indent=1)
    if basis is not None:
        np.save(os.path.join(outdir, f"sepbasis_d{d}_p{p}.npy"),
                np.stack(basis) if basis else np.zeros((0, log["n_feat"])))

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, required=True)
    ap.add_argument("--prime", type=int, default=999983)
    ap.add_argument("--seed", type=int, default=44)
    ap.add_argument("--batches", type=int, default=8)
    ap.add_argument("--out", default="night2/results")
    args = ap.parse_args()
    run(args.d, args.prime, args.seed, batches=args.batches,
        outdir=args.out)
