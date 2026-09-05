#!/usr/bin/env python3
"""Independent modular sampler/interpolator for Aut_{<=d}(A^2), Jacobian one.

All results are modular.  This program never calls an interpolated relation a
characteristic-zero certificate.  It uses the full alternating affine-triangular
factorization chart for a fixed polydegree and enumerates the proven component
indices for d <= 10.

Only Python's standard library and NumPy are used.
"""

from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path

import numpy as np

Mon = tuple[int, int]
Poly = dict[Mon, int]
Pair = tuple[Poly, Poly]


def clean(a: Poly, p: int) -> Poly:
    return {m: int(c % p) for m, c in a.items() if c % p}


def add(a: Poly, b: Poly, p: int) -> Poly:
    out = dict(a)
    for m, c in b.items():
        out[m] = (out.get(m, 0) + c) % p
    return clean(out, p)


def scale(a: Poly, s: int, p: int) -> Poly:
    return clean({m: c * s for m, c in a.items()}, p)


def mul(a: Poly, b: Poly, p: int, cap: int | None = None) -> Poly:
    out: Poly = {}
    for (i, j), x in a.items():
        for (k, l), y in b.items():
            if cap is None or i + j + k + l <= cap:
                m = (i + k, j + l)
                out[m] = (out.get(m, 0) + x * y) % p
    return clean(out, p)


def power(a: Poly, n: int, p: int, cap: int | None = None) -> Poly:
    out: Poly = {(0, 0): 1}
    base = a
    while n:
        if n & 1:
            out = mul(out, base, p, cap)
        n //= 2
        if n:
            base = mul(base, base, p, cap)
    return out


def deriv(a: Poly, axis: int, p: int) -> Poly:
    out: Poly = {}
    for (i, j), c in a.items():
        e = i if axis == 0 else j
        if e:
            m = (i - 1, j) if axis == 0 else (i, j - 1)
            out[m] = c * e % p
    return clean(out, p)


def bracket(a: Poly, b: Poly, p: int) -> Poly:
    return add(mul(deriv(a, 0, p), deriv(b, 1, p), p),
               scale(mul(deriv(a, 1, p), deriv(b, 0, p), p), -1, p), p)


def compose_poly(h: Poly, f: Pair, p: int, cap: int) -> Poly:
    xp = [{(0, 0): 1}]
    yp = [{(0, 0): 1}]
    for _ in range(max((i for i, _ in h), default=0)):
        xp.append(mul(xp[-1], f[0], p, cap))
    for _ in range(max((j for _, j in h), default=0)):
        yp.append(mul(yp[-1], f[1], p, cap))
    out: Poly = {}
    for (i, j), c in h.items():
        out = add(out, scale(mul(xp[i], yp[j], p, cap), c, p), p)
    return out


def compose(outer: Pair, inner: Pair, p: int, cap: int) -> Pair:
    return (compose_poly(outer[0], inner, p, cap),
            compose_poly(outer[1], inner, p, cap))


X: Poly = {(1, 0): 1}
Y: Poly = {(0, 1): 1}
ONE: Poly = {(0, 0): 1}


def total_degree(a: Poly) -> int:
    return max((i + j for i, j in a), default=-1)


def monomials(d: int) -> list[Mon]:
    return [(i, n - i) for n in range(d + 1) for i in range(n + 1)]


def all_polydegrees(d: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    def rec(prefix: tuple[int, ...], prod: int) -> None:
        for e in range(2, d // prod + 1):
            q = prod * e
            if q <= d:
                t = prefix + (e,)
                out.append(t)
                rec(t, q)
    rec((), 1)
    return out


def embeds(a: tuple[int, ...], b: tuple[int, ...]) -> bool:
    """Furter's subsequence/componentwise partial order a <= b."""
    j = 0
    for x in a:
        while j < len(b) and b[j] < x:
            j += 1
        if j == len(b):
            return False
        j += 1
    return True


def component_polydegrees(d: int) -> list[tuple[int, ...]]:
    seqs = all_polydegrees(d)
    return sorted([a for a in seqs if not any(a != b and embeds(a, b) for b in seqs)],
                  key=lambda z: (len(z), z))


def rand_nonzero(rng: random.Random, p: int) -> int:
    return rng.randrange(1, p)


def linear_map(det: int, rng: random.Random, p: int, require_lower_left: bool = False) -> Pair:
    a = rand_nonzero(rng, p)
    b = rng.randrange(p)
    c = rand_nonzero(rng, p) if require_lower_left else rng.randrange(p)
    e = ((det + b * c) * pow(a, -1, p)) % p
    return (add(scale(X, a, p), scale(Y, b, p), p),
            add(scale(X, c, p), scale(Y, e, p), p))


def affine_map(det: int, rng: random.Random, p: int,
               require_lower_left: bool = False) -> Pair:
    f = linear_map(det, rng, p, require_lower_left)
    return (add(f[0], {(0, 0): rng.randrange(p)}, p),
            add(f[1], {(0, 0): rng.randrange(p)}, p))


def gamma(deg: int, last: bool, rng: random.Random, p: int) -> Pair:
    lo = 2 if last else 1
    q: Poly = {}
    for j in range(lo, deg + 1):
        q[(0, j)] = rand_nonzero(rng, p) if j == deg else rng.randrange(p)
    return (add(X, q, p), Y)


def triangular(deg: int, rng: random.Random, p: int) -> tuple[Pair, int]:
    """General element of B of exact degree deg, with its determinant."""
    a, b = rand_nonzero(rng, p), rand_nonzero(rng, p)
    q: Poly = {}
    for j in range(deg + 1):
        q[(0, j)] = rand_nonzero(rng, p) if j == deg else rng.randrange(p)
    first = add(scale(X, a, p), q, p)
    second = add(scale(Y, b, p), {(0, 0): rng.randrange(p)}, p)
    return (first, second), (a * b) % p


def sample_chart(polydegree: tuple[int, ...], cap: int, rng: random.Random, p: int) -> Pair:
    """Full alternating A-B parameterization of a polydegree stratum.

    Standard composition convention:
      alpha_1 o beta_1 o alpha_2 o ... o beta_l o alpha_{l+1}.
    The interior alpha_i are forced outside the affine triangular subgroup.
    Determinants are random and the last affine determinant is chosen so that
    the full map has Jacobian one.
    """
    ell = len(polydegree)
    left_affines: list[Pair] = []
    det_product = 1
    for i in range(ell):
        det = rand_nonzero(rng, p)
        left_affines.append(affine_map(det, rng, p, require_lower_left=(i > 0)))
        det_product = det_product * det % p
    betas: list[Pair] = []
    for deg in polydegree:
        bmap, bdet = triangular(deg, rng, p)
        betas.append(bmap)
        det_product = det_product * bdet % p
    right = affine_map(pow(det_product, -1, p), rng, p)
    f = right
    for i in reversed(range(ell)):
        f = compose(betas[i], f, p, cap)
        f = compose(left_affines[i], f, p, cap)
    return f


def sample_component(polydegree: tuple[int, ...], cap: int, rng: random.Random, p: int) -> Pair:
    target = math.prod(polydegree)
    for _ in range(20):
        f = sample_chart(polydegree, cap, rng, p)
        if max(total_degree(f[0]), total_degree(f[1])) == target and bracket(f[0], f[1], p) == ONE:
            return f
    raise RuntimeError(f"failed to sample nondegenerate chart {polydegree}")


def coefficient_vector(f: Pair, d: int, p: int) -> np.ndarray:
    mons = monomials(d)
    return np.array([f[0].get(m, 0) for m in mons] + [f[1].get(m, 0) for m in mons],
                    dtype=np.int64) % p


def feature_vector(c: np.ndarray, p: int) -> np.ndarray:
    n = len(c)
    out = np.empty((n + 1) * (n + 2) // 2, dtype=np.int64)
    out[0] = 1
    out[1:n + 1] = c
    k = n + 1
    for i in range(n):
        z = (c[i] * c[i:]) % p
        out[k:k + n - i] = z
        k += n - i
    return out


class ModularRowSpace:
    def __init__(self, p: int, width: int):
        self.p = p
        self.width = width
        self.rows: dict[int, np.ndarray] = {}

    def reduce(self, row: np.ndarray) -> np.ndarray:
        v = row.copy() % self.p
        for col in sorted(self.rows):
            x = int(v[col])
            if x:
                v = (v - x * self.rows[col]) % self.p
        return v

    def add(self, row: np.ndarray) -> bool:
        v = self.reduce(row)
        nz = np.flatnonzero(v)
        if not len(nz):
            return False
        col = int(nz[0])
        v = (v * pow(int(v[col]), -1, self.p)) % self.p
        self.rows[col] = v
        return True

    @property
    def rank(self) -> int:
        return len(self.rows)

    def nullspace(self) -> np.ndarray:
        piv = sorted(self.rows)
        rows = {k: self.rows[k].copy() for k in piv}
        for k in reversed(piv):
            for j in piv:
                if j >= k:
                    break
                x = int(rows[j][k])
                if x:
                    rows[j] = (rows[j] - x * rows[k]) % self.p
        free = [j for j in range(self.width) if j not in rows]
        basis = np.zeros((len(free), self.width), dtype=np.int64)
        for bi, q in enumerate(free):
            basis[bi, q] = 1
            for k in reversed(piv):
                basis[bi, k] = (-rows[k][q]) % self.p
        return basis


@dataclass
class Result:
    d: int
    prime: int
    samples: int
    rank: int
    separators: int
    components: str
    S1: str
    S2: str
    I1: str
    I2: str
    I3: str


def controls_small() -> None:
    # Independent direct composition/control objects.
    p = 101
    rng = random.Random(717)
    comps = component_polydegrees(4)
    assert comps == [(4,), (2, 2)], comps
    for comp in comps:
        f = sample_component(comp, 4, rng, p)
        assert bracket(f[0], f[1], p) == ONE
    # A known nonidentity quadratic feature vector has the promised size.
    c = coefficient_vector(f, 4, p)
    assert len(feature_vector(c, p)) == (len(c) + 1) * (len(c) + 2) // 2
    print("PASS S0 independent sampler/Jacobian/feature controls")


def run_one(d: int, p: int, batch: int, patience: int, max_samples: int,
            holdout: int, seed: int) -> tuple[Result, np.ndarray | None]:
    rng = random.Random(seed + 1009 * d + p)
    comps = component_polydegrees(d)
    if not comps:
        raise RuntimeError("no component indices")
    width = (d + 1) * (d + 2)
    fwidth = (width + 1) * (width + 2) // 2
    space = ModularRowSpace(p, fwidth)
    seen = {c: 0 for c in comps}
    stale = 0
    samples = 0
    last_rank = 0
    while samples < max_samples and stale < patience:
        for _ in range(batch):
            comp = comps[samples % len(comps)]
            f = sample_component(comp, d, rng, p)
            if bracket(f[0], f[1], p) != ONE:
                print("FAIL S1 sampled Jacobian")
                raise SystemExit(2)
            seen[comp] += 1
            space.add(feature_vector(coefficient_vector(f, d, p), p))
            samples += 1
            if samples >= max_samples:
                break
        if space.rank == last_rank:
            stale += 1
        else:
            stale = 0
        last_rank = space.rank
        print(f"PROGRESS d={d} p={p} samples={samples} rank={space.rank} stale={stale}")
    S1 = "PASS"
    S2 = "PASS" if all(seen.values()) else "FAIL"
    I1 = "PASS" if stale >= patience else "FAIL"
    if S2 == "FAIL":
        print("FAIL S2 component coverage")
        raise SystemExit(2)
    if I1 == "FAIL":
        print(f"FAIL I1 rank did not saturate by {max_samples} samples")
        result = Result(d, p, samples, space.rank, fwidth-space.rank,
                        ";".join("x".join(map(str,c)) for c in comps), S1,S2,I1,"NOT_RUN","NOT_RUN")
        return result, None

    basis = space.nullspace()
    # I2 is equivalent to held-out evaluation rows belonging to the learned row space,
    # and is also checked directly against every returned basis vector.
    i2 = True
    for k in range(holdout):
        comp = comps[k % len(comps)]
        f = sample_component(comp, d, rng, p)
        v = feature_vector(coefficient_vector(f, d, p), p)
        if np.any((basis @ v) % p):
            i2 = False
            break
    I2 = "PASS" if i2 else "FAIL"
    if not i2:
        print("FAIL I2 held-out identity")
        raise SystemExit(2)
    # I3: each nonzero basis polynomial evaluates nonzero on at least one of 8
    # independently random ambient coefficient vectors. This is a nontriviality
    # control, not a proof about a symbolic polynomial (nonzero basis coordinates are that proof).
    alive = np.zeros(len(basis), dtype=bool)
    for _ in range(8):
        c = np.array([rng.randrange(p) for _ in range(width)], dtype=np.int64)
        v = feature_vector(c, p)
        alive |= ((basis @ v) % p) != 0
    I3 = "PASS" if bool(np.all(alive)) else "FAIL"
    if I3 == "FAIL":
        print("FAIL I3 random ambient nontriviality")
        raise SystemExit(2)
    print("PASS S1 sampled Jacobians")
    print("PASS S2 every proven component index sampled")
    print("PASS I1 empirical batch rank saturation")
    print("PASS I2 held-out automorphisms")
    print("PASS I3 ambient nontriviality")
    result = Result(d, p, samples, space.rank, len(basis),
                    ";".join("x".join(map(str,c)) for c in comps), S1,S2,I1,I2,I3)
    return result, basis


def write_csv(path: Path, results: list[Result]) -> None:
    with path.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(Result.__annotations__))
        w.writeheader()
        for r in results:
            w.writerow(r.__dict__)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int)
    ap.add_argument("--prime", type=int)
    ap.add_argument("--grid", action="store_true")
    ap.add_argument("--batch", type=int, default=32)
    ap.add_argument("--patience", type=int, default=3)
    ap.add_argument("--max-samples", type=int, default=10000)
    ap.add_argument("--holdout", type=int, default=24)
    ap.add_argument("--seed", type=int, default=20260828)
    ap.add_argument("--csv", default="separator_counts.csv")
    args = ap.parse_args()
    controls_small()
    jobs = ([(d,p) for d in range(3,11) for p in (999983,1000003)] if args.grid
            else [(args.d, args.prime)])
    if any(d is None or p is None for d,p in jobs):
        ap.error("supply --grid or both --d and --prime")
    results: list[Result] = []
    for d,p in jobs:
        r,_ = run_one(d,p,args.batch,args.patience,args.max_samples,args.holdout,args.seed)
        results.append(r)
        if r.I1 != "PASS":
            write_csv(Path(args.csv), results)
            raise SystemExit(3)
    write_csv(Path(args.csv), results)
    print("PASS GRID all requested modular runs completed")


if __name__ == "__main__":
    main()
