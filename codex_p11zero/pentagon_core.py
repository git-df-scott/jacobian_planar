#!/usr/bin/env python3
"""Independent exact arithmetic for the p_1_1 = 0 pentagon chart.

The recurrence is rebuilt from

    P_x Q_y - P_y Q_x = x^2

with p_0_0 = 0 and p_0_1 = 1.  All arithmetic is over F_p.  A genuine chart
witness must pass the 66 exported conditions, the omitted level-24 and
termination conditions, the bracket identity, and every Newton-polygon vertex
nonvanishing condition.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple


def p_rows(jmax: int = 16) -> Dict[int, Tuple[int, int]]:
    rows = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 8), min(8, j // 2 + 1)
        if lo <= hi:
            rows[j] = (lo, hi)
    return rows


def q_rows(jmax: int = 24) -> Dict[int, Tuple[int, int]]:
    rows = {}
    for j in range(jmax + 1):
        lo, hi = max(0, j - 12), min(12, 2 * j, (j + 3) // 2)
        if lo <= hi:
            rows[j] = (lo, hi)
    return rows


P_ROWS = p_rows()
Q_ROWS = q_rows()
P_PARAMS = [(j, i) for j in sorted(P_ROWS)
            for i in range(P_ROWS[j][0], P_ROWS[j][1] + 1)]
P_GAUGES = {(0, 0): 0, (0, 1): 1}
VARS = [f"p_{j}_{i}" for j, i in P_PARAMS if (j, i) not in P_GAUGES]

# These are exactly the four non-translation vertices of N(P) and all five
# vertices of N(Q).  p_0_1, q_0_0, and q_1_2 are fixed nonzero by normalization.
P_VERTEX_KEYS = ((0, 1), (8, 0), (14, 8), (16, 8))
Q_VERTEX_KEYS = ((0, 0), (1, 2), (12, 0), (21, 12), (24, 12))

# Direct finite-difference checks show joint affinity in this 14-variable block.
AFFINE_VARS = ["p_11_6"] + [f"p_{j}_{i}" for j, i in P_PARAMS if j >= 12]
EARLY_VARS = [name for name in VARS if name not in AFFINE_VARS]


def _trim(a: List[int]) -> List[int]:
    while a and a[-1] == 0:
        a.pop()
    return a


def _add(a: Sequence[int], b: Sequence[int], p: int) -> List[int]:
    n = max(len(a), len(b))
    return _trim([((a[i] if i < len(a) else 0) +
                   (b[i] if i < len(b) else 0)) % p for i in range(n)])


def _scale(a: Sequence[int], c: int, p: int) -> List[int]:
    c %= p
    return _trim([(c * x) % p for x in a]) if c else []


def _mul(a: Sequence[int], b: Sequence[int], p: int) -> List[int]:
    if not a or not b:
        return []
    out = [0] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if not ca:
            continue
        for j, cb in enumerate(b):
            if cb:
                out[i + j] = (out[i + j] + ca * cb) % p
    return _trim(out)


def _deriv(a: Sequence[int], p: int) -> List[int]:
    return _trim([(i * a[i]) % p for i in range(1, len(a))])


def build_p(values: Mapping[str, int], p: int, jmax: int = 40) -> List[List[int]]:
    out: List[List[int]] = [[] for _ in range(jmax + 1)]
    for j, (lo, hi) in P_ROWS.items():
        row = [0] * (hi + 1)
        for i in range(lo, hi + 1):
            if (j, i) in P_GAUGES:
                row[i] = P_GAUGES[(j, i)] % p
            else:
                row[i] = values.get(f"p_{j}_{i}", 0) % p
        out[j] = _trim(row)
    return out


def recur_q(values: Mapping[str, int], p: int, jmax: int = 40,
            q00: int = 1) -> Tuple[List[List[int]], List[List[int]]]:
    """Return (P,Q) through y-degree jmax using the exact y-adic recursion."""
    if p <= jmax:
        raise ValueError(f"prime {p} must exceed recursion depth {jmax}")
    P = build_p(values, p, jmax)
    p01 = P[0][1] if len(P[0]) > 1 else 0
    if p01 % p == 0:
        raise ValueError("p_0_1 must be nonzero")
    inv01 = pow(p01, p - 2, p)
    Q: List[List[int]] = [[] for _ in range(jmax + 1)]
    Q[0] = [q00 % p]
    Q[1] = [0, 0, inv01]
    for k in range(1, jmax):
        acc: List[int] = []
        for a in range(1, k + 1):
            b = k + 1 - a
            if a >= len(P) or b >= len(Q) or not P[a] or not Q[b]:
                continue
            acc = _add(acc, _scale(_mul(P[a], _deriv(Q[b], p), p), a, p), p)
            acc = _add(acc, _scale(_mul(_deriv(P[a], p), Q[b], p), -b, p), p)
        denom = ((k + 1) * p01) % p
        Q[k + 1] = _scale(acc, pow(denom, p - 2, p), p)
    return P, Q


def exported_conditions(Q: Sequence[Sequence[int]], p: int,
                        jtop: int = 23) -> List[int]:
    out = []
    for j in range(13, jtop + 1):
        for i in range(j - 12):
            out.append((Q[j][i] if i < len(Q[j]) else 0) % p)
    return out


def full_conditions(Q: Sequence[Sequence[int]], p: int) -> List[int]:
    """All support and termination conditions, including the 314 omitted ones."""
    out = exported_conditions(Q, p, 24)
    for j in range(25, 41):
        out.extend(x % p for x in Q[j])
    return out


def bracket(P: Sequence[Sequence[int]], Q: Sequence[Sequence[int]],
            p: int) -> Dict[Tuple[int, int], int]:
    """Sparse coefficients {(y-degree,x-degree): coefficient} of [P,Q]."""
    out: Dict[Tuple[int, int], int] = {}
    for a, pa in enumerate(P):
        if not pa:
            continue
        dpa = _deriv(pa, p)
        for b, qb in enumerate(Q):
            if not qb or a + b == 0:
                continue
            row: List[int] = []
            if b:
                row = _add(row, _scale(_mul(dpa, qb, p), b, p), p)
            if a:
                row = _add(row, _scale(_mul(pa, _deriv(qb, p), p), -a, p), p)
            ydeg = a + b - 1
            for xdeg, coefficient in enumerate(row):
                if coefficient:
                    key = (ydeg, xdeg)
                    out[key] = (out.get(key, 0) + coefficient) % p
                    if out[key] == 0:
                        del out[key]
    return out


def bracket_residual(P: Sequence[Sequence[int]], Q: Sequence[Sequence[int]],
                     p: int, max_y: int | None = None) -> Dict[Tuple[int, int], int]:
    # Q was recursively constructed only through Q_40.  This determines the
    # bracket coefficients through y^39; higher coefficients would require the
    # next Q rows unless the termination conditions Q_25..Q_40 already vanish.
    out = {key: value for key, value in bracket(P, Q, p).items()
           if max_y is None or key[0] <= max_y}
    out[(0, 2)] = (out.get((0, 2), 0) - 1) % p
    if out[(0, 2)] == 0:
        del out[(0, 2)]
    return out


def vertex_values(P: Sequence[Sequence[int]], Q: Sequence[Sequence[int]],
                  p: int) -> Dict[str, int]:
    def at(rows: Sequence[Sequence[int]], key: Tuple[int, int]) -> int:
        j, i = key
        return rows[j][i] % p if j < len(rows) and i < len(rows[j]) else 0

    vals = {f"P[{j},{i}]": at(P, (j, i)) for j, i in P_VERTEX_KEYS}
    vals.update({f"Q[{j},{i}]": at(Q, (j, i)) for j, i in Q_VERTEX_KEYS})
    return vals


@dataclass
class Verification:
    exported_zero: bool
    full_zero: bool
    bracket_zero: bool
    chart_ok: bool
    vertices_nonzero: bool
    exported_bad: int
    full_bad: int
    bracket_bad: int
    vertices: Dict[str, int]

    @property
    def candidate(self) -> bool:
        return (self.exported_zero and self.full_zero and self.bracket_zero and
                self.chart_ok and self.vertices_nonzero)


def verify(values: Mapping[str, int], p: int) -> Verification:
    # Reconstruct only the Q rows allowed by N(Q), then verify the entire
    # bracket directly.  This avoids dividing by 25..40 and is therefore valid
    # at every prime p > 24, including the campaign's intended p=31 sweep.
    P, Q = recur_q(values, p, jmax=24)
    exported = exported_conditions(Q, p)
    support = exported_conditions(Q, p, 24)
    bres = bracket_residual(P, Q, p)
    vertices = vertex_values(P, Q, p)
    chart_ok = (values.get("p_1_1", 0) % p == 0 and
                values.get("p_1_0", 0) % p != 0)
    return Verification(
        exported_zero=not any(exported),
        full_zero=not any(support) and not bres,
        bracket_zero=not bres,
        chart_ok=chart_ok,
        vertices_nonzero=all(vertices.values()),
        exported_bad=sum(x != 0 for x in exported),
        full_bad=sum(x != 0 for x in support) + len(bres),
        bracket_bad=len(bres),
        vertices=vertices,
    )


def rank_mod(rows: Sequence[Sequence[int]], p: int) -> int:
    a = [[x % p for x in row] for row in rows]
    if not a:
        return 0
    nr, nc, r = len(a), len(a[0]), 0
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(x * inv) % p for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(a[i][j] - f * a[r][j]) % p for j in range(nc)]
        r += 1
        if r == nr:
            break
    return r


def affine_system(early: Mapping[str, int], p: int) -> Tuple[List[List[int]], List[int]]:
    """Return M,v with exported_conditions = M*late + v."""
    base = dict(early)
    for name in AFFINE_VARS:
        base[name] = 0
    _, q0 = recur_q(base, p, jmax=23)
    v = exported_conditions(q0, p)
    cols = []
    for name in AFFINE_VARS:
        point = dict(base)
        point[name] = 1
        _, q1 = recur_q(point, p, jmax=23)
        col = exported_conditions(q1, p)
        cols.append([(col[i] - v[i]) % p for i in range(len(v))])
    return [[cols[c][r] for c in range(len(cols))] for r in range(len(v))], v


def solve_affine(M: Sequence[Sequence[int]], v: Sequence[int], p: int
                 ) -> Tuple[int, int, bool, List[int] | None]:
    """Solve M*x = -v, returning rank(M), rank(aug), consistency, one solution."""
    n = len(M[0]) if M else 0
    aug = [[x % p for x in M[i]] + [(-v[i]) % p] for i in range(len(M))]
    a = [row[:] for row in aug]
    pivots: List[int] = []
    r = 0
    for c in range(n + 1):
        pivot = next((i for i in range(r, len(a)) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(x * inv) % p for x in a[r]]
        for i in range(len(a)):
            if i != r and a[i][c]:
                f = a[i][c]
                a[i] = [(a[i][j] - f * a[r][j]) % p for j in range(n + 1)]
        pivots.append(c)
        r += 1
        if r == len(a):
            break
    rank_m = sum(c < n for c in pivots)
    inconsistent = n in pivots
    rank_aug = rank_m + int(inconsistent)
    if inconsistent:
        return rank_m, rank_aug, False, None
    sol = [0] * n
    for row, c in enumerate(pivots):
        if c < n:
            sol[c] = a[row][n]
    return rank_m, rank_aug, True, sol


def insert_affine(early: Mapping[str, int], late: Sequence[int]) -> Dict[str, int]:
    out = dict(early)
    out.update(zip(AFFINE_VARS, late))
    return out


# Exact first derivatives via dual numbers F_p[eps]/(eps^2).  This is kept
# separate from the value recurrence so the derivative control is genuinely
# different from a finite-difference/secant calculation.
Dual = Tuple[int, int]


def _dadd(a: Dual, b: Dual, p: int) -> Dual:
    return ((a[0] + b[0]) % p, (a[1] + b[1]) % p)


def _dmul(a: Dual, b: Dual, p: int) -> Dual:
    return (a[0] * b[0] % p,
            (a[0] * b[1] + a[1] * b[0]) % p)


def _dxadd(a: Sequence[Dual], b: Sequence[Dual], p: int) -> List[Dual]:
    n = max(len(a), len(b))
    out = [_dadd(a[i] if i < len(a) else (0, 0),
                 b[i] if i < len(b) else (0, 0), p) for i in range(n)]
    while out and out[-1] == (0, 0):
        out.pop()
    return out


def _dxscale(a: Sequence[Dual], c: int, p: int) -> List[Dual]:
    return [_dmul(x, (c % p, 0), p) for x in a] if c % p else []


def _dxmul(a: Sequence[Dual], b: Sequence[Dual], p: int) -> List[Dual]:
    if not a or not b:
        return []
    out = [(0, 0)] * (len(a) + len(b) - 1)
    for i, ca in enumerate(a):
        if ca == (0, 0):
            continue
        for j, cb in enumerate(b):
            if cb != (0, 0):
                out[i + j] = _dadd(out[i + j], _dmul(ca, cb, p), p)
    while out and out[-1] == (0, 0):
        out.pop()
    return out


def _dxderiv(a: Sequence[Dual], p: int) -> List[Dual]:
    out = [_dmul(a[i], (i % p, 0), p) for i in range(1, len(a))]
    while out and out[-1] == (0, 0):
        out.pop()
    return out


def dual_recur_q(values: Mapping[str, int], p: int, dvar: str,
                 jmax: int = 40) -> List[List[Dual]]:
    if p <= jmax:
        raise ValueError(f"prime {p} must exceed recursion depth {jmax}")
    P: List[List[Dual]] = [[] for _ in range(jmax + 1)]
    for j, (lo, hi) in P_ROWS.items():
        row = [(0, 0)] * (hi + 1)
        for i in range(lo, hi + 1):
            if (j, i) in P_GAUGES:
                value = P_GAUGES[(j, i)] % p
                derivative = 0
            else:
                name = f"p_{j}_{i}"
                value = values.get(name, 0) % p
                derivative = int(name == dvar)
            row[i] = (value, derivative)
        while row and row[-1] == (0, 0):
            row.pop()
        P[j] = row
    p01 = P[0][1][0]
    inv01 = pow(p01, p - 2, p)
    Q: List[List[Dual]] = [[] for _ in range(jmax + 1)]
    Q[0] = [(1, 0)]
    Q[1] = [(0, 0), (0, 0), (inv01, 0)]
    for k in range(1, jmax):
        acc: List[Dual] = []
        for a in range(1, k + 1):
            b = k + 1 - a
            if a >= len(P) or b >= len(Q) or not P[a] or not Q[b]:
                continue
            acc = _dxadd(acc, _dxscale(_dxmul(P[a], _dxderiv(Q[b], p), p), a, p), p)
            acc = _dxadd(acc, _dxscale(_dxmul(_dxderiv(P[a], p), Q[b], p), -b, p), p)
        invden = pow(((k + 1) * p01) % p, p - 2, p)
        Q[k + 1] = _dxscale(acc, invden, p)
    return Q


def dual_exported_conditions(Q: Sequence[Sequence[Dual]], jtop: int = 23
                             ) -> List[Dual]:
    out = []
    for j in range(13, jtop + 1):
        for i in range(j - 12):
            out.append(Q[j][i] if i < len(Q[j]) else (0, 0))
    return out


def dual_full_conditions(Q: Sequence[Sequence[Dual]]) -> List[Dual]:
    out = dual_exported_conditions(Q, 24)
    for j in range(25, 41):
        out.extend(Q[j])
    return out


def jacobian(values: Mapping[str, int], p: int, variables: Sequence[str],
             full: bool = False) -> List[List[int]]:
    cols = []
    for name in variables:
        q = dual_recur_q(values, p, name)
        conditions = dual_full_conditions(q) if full else dual_exported_conditions(q)
        cols.append([entry[1] % p for entry in conditions])
    return [[cols[c][r] for c in range(len(cols))] for r in range(len(cols[0]))]


def nullspace_mod(rows: Sequence[Sequence[int]], p: int) -> List[List[int]]:
    a = [[x % p for x in row] for row in rows]
    if not a:
        return []
    nr, nc, r = len(a), len(a[0]), 0
    pivots = []
    for c in range(nc):
        pivot = next((i for i in range(r, nr) if a[i][c]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][c], p - 2, p)
        a[r] = [(x * inv) % p for x in a[r]]
        for i in range(nr):
            if i != r and a[i][c]:
                factor = a[i][c]
                a[i] = [(a[i][j] - factor * a[r][j]) % p for j in range(nc)]
        pivots.append(c)
        r += 1
        if r == nr:
            break
    free = [c for c in range(nc) if c not in pivots]
    basis = []
    for f in free:
        vector = [0] * nc
        vector[f] = 1
        for row, pivot in enumerate(pivots):
            vector[pivot] = (-a[row][f]) % p
        basis.append(vector)
    return basis
