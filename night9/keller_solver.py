"""night9 — solver for Keller-plus-collision systems over F_p.

SYSTEM CONTRACT (all statements below are definitions of what is computed;
no interpretation is offered anywhere in this lane).

Given a support pair (S_P, S_Q) of exponent vectors in Z_{>=0}^2, put

    P(x,y) = sum_{m in S_P} a_m x^{m0} y^{m1}
    Q(x,y) = sum_{n in S_Q} b_n x^{n0} y^{n1}

with unknown coefficients a_m, b_n.  Then

    P_x Q_y - P_y Q_x = sum_{m,n} (m0 n1 - m1 n0) a_m b_n
                        x^{m0+n0-1} y^{m1+n1-1}

so the (K) equations "every coefficient of P_x Q_y - P_y Q_x - 1 vanishes"
read, for each lattice point e:

    sum_{(m,n): (m0+n0-1, m1+n1-1) = e}  (m0 n1 - m1 n0) a_m b_n  =  [e == (0,0)]

The equation set E used here is  {e : some pair has nonzero INTEGER bracket}
union {(0,0)}.  (0,0) is always present because of the -1; if no pair reaches
it the equation is 0 = 1.

The (C) equations are the Mondello-style fixed collision at the two points
(0,1) and (1,0), with 0^0 = 1:

    C_P:  P(0,1) - P(1,0) = sum_m ([m0==0] - [m1==0]) a_m = 0
    C_Q:  Q(0,1) - Q(1,0) = sum_n ([n0==0] - [n1==0]) b_n = 0

Every (K) equation is bilinear: linear in a for fixed b and linear in b for
fixed a.  C_P involves only a, C_Q only b.  The exhaustive method used here
exploits exactly that: enumerate the smaller side inside the linear subspace
cut out by its own collision equation, and for each enumerated point solve the
resulting LINEAR system over F_p for the other side.  This is exact and
complete -- it visits every F_p point of the system -- and returns the exact
solution count.
"""

import itertools
import numpy as np


# ----------------------------------------------------------------- system

def build_system(SP, SQ):
    """Return (eqs, pairs, cP, cQ).

    eqs   : list of lattice points e, the (K) equation index set
    pairs : dict e -> list of (mi, ni, c) with integer bracket c != 0
    cP    : integer row vector over S_P for C_P
    cQ    : integer row vector over S_Q for C_Q
    """
    pairs = {}
    for mi, m in enumerate(SP):
        for ni, n in enumerate(SQ):
            c = m[0] * n[1] - m[1] * n[0]
            if c == 0:
                continue
            e = (m[0] + n[0] - 1, m[1] + n[1] - 1)
            pairs.setdefault(e, []).append((mi, ni, c))
    if (0, 0) not in pairs:
        pairs[(0, 0)] = []
    eqs = sorted(pairs.keys())
    cP = [(1 if m[0] == 0 else 0) - (1 if m[1] == 0 else 0) for m in SP]
    cQ = [(1 if n[0] == 0 else 0) - (1 if n[1] == 0 else 0) for n in SQ]
    return eqs, pairs, cP, cQ


def residual_int(SP, SQ, a, b):
    """Integer residual vector of the full system at (a, b), in the order
    eqs + [C_P, C_Q]."""
    eqs, pairs, cP, cQ = build_system(SP, SQ)
    out = []
    for e in eqs:
        s = sum(c * a[mi] * b[ni] for (mi, ni, c) in pairs[e])
        if e == (0, 0):
            s -= 1
        out.append(s)
    out.append(sum(cP[i] * a[i] for i in range(len(SP))))
    out.append(sum(cQ[i] * b[i] for i in range(len(SQ))))
    return out


def jacobian_int(SP, SQ, a, b):
    """Integer Jacobian of the full system at (a, b); columns a then b."""
    eqs, pairs, cP, cQ = build_system(SP, SQ)
    NA, NB = len(SP), len(SQ)
    J = []
    for e in eqs:
        row = [0] * (NA + NB)
        for (mi, ni, c) in pairs[e]:
            row[mi] += c * b[ni]
            row[NA + ni] += c * a[mi]
        J.append(row)
    J.append(list(cP) + [0] * NB)
    J.append([0] * NA + list(cQ))
    return J


# ------------------------------------------------------------ verification

def poly_det_minus_one(SP, SQ, a, b, p):
    """dict of the mod-p coefficients of P_x Q_y - P_y Q_x - 1 (nonzero only)."""
    d = {}
    for mi, m in enumerate(SP):
        for ni, n in enumerate(SQ):
            c = (m[0] * n[1] - m[1] * n[0]) % p
            if c == 0:
                continue
            v = (c * a[mi] * b[ni]) % p
            if v == 0:
                continue
            e = (m[0] + n[0] - 1, m[1] + n[1] - 1)
            d[e] = (d.get(e, 0) + v) % p
    d[(0, 0)] = (d.get((0, 0), 0) - 1) % p
    return {k: v for k, v in d.items() if v % p}


def eval_poly(S, coef, x, y, p):
    s = 0
    for i, (e0, e1) in enumerate(S):
        s += coef[i] * pow(x, e0, p) * pow(y, e1, p)   # 0**0 == 1
    return s % p


def verify_solution(SP, SQ, a, b, p):
    """Direct substitution check.  Returns dict with det_ok, coll_ok, values."""
    res = poly_det_minus_one(SP, SQ, a, b, p)
    P01 = eval_poly(SP, a, 0, 1, p); P10 = eval_poly(SP, a, 1, 0, p)
    Q01 = eval_poly(SQ, b, 0, 1, p); Q10 = eval_poly(SQ, b, 1, 0, p)
    return {
        "det_J_minus_1_residual": {str(k): v for k, v in res.items()},
        "det_ok": len(res) == 0,
        "P_at_0_1": P01, "P_at_1_0": P10,
        "Q_at_0_1": Q01, "Q_at_1_0": Q10,
        "coll_ok": (P01 == P10) and (Q01 == Q10),
        "image_0_1": [P01, Q01], "image_1_0": [P10, Q10],
    }


# ------------------------------------------------- linear algebra over F_p

def _inv_table(p):
    t = [0] * p
    for i in range(1, p):
        t[i] = pow(i, p - 2, p)
    return t


def solve_gfp(A, rhs, p):
    """Plain solve of A x = rhs over F_p.  A: list of rows (lists).
    Returns (particular, nullspace_basis) or None if inconsistent."""
    m = len(A)
    k = len(A[0]) if m else 0
    M = [[A[i][j] % p for j in range(k)] + [rhs[i] % p] for i in range(m)]
    inv = _inv_table(p)
    piv = []
    r = 0
    for j in range(k):
        pr = None
        for i in range(r, m):
            if M[i][j]:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv[M[r][j]]
        M[r] = [(v * iv) % p for v in M[r]]
        for i in range(m):
            if i != r and M[i][j]:
                f = M[i][j]
                M[i] = [(M[i][t] - f * M[r][t]) % p for t in range(k + 1)]
        piv.append(j)
        r += 1
        if r == m:
            break
    for i in range(r, m):
        if M[i][k]:
            return None
    part = [0] * k
    for i, j in enumerate(piv):
        part[j] = M[i][k]
    free = [j for j in range(k) if j not in piv]
    basis = []
    for f in free:
        v = [0] * k
        v[f] = 1
        for i, j in enumerate(piv):
            v[j] = (-M[i][f]) % p
        basis.append(v)
    return part, basis


def batch_rank_consistent(A, p):
    """Batched Gauss-Jordan over F_p.

    A : int64 array (B, M, K+1), last column is the right-hand side.
    Returns (rank, consistent) arrays of shape (B,).
    Modified in place.
    """
    Bn, M, W = A.shape
    K = W - 1
    inv = np.array(_inv_table(p), dtype=np.int64)
    rows = np.arange(M)
    r = np.zeros(Bn, dtype=np.int64)
    for j in range(K):
        col = A[:, :, j]
        valid = (rows[None, :] >= r[:, None]) & (col != 0)
        has = valid.any(axis=1)
        if not has.any():
            continue
        pr = np.argmax(valid, axis=1)
        sel = np.nonzero(has)[0]
        ra = r[sel]
        pa = pr[sel]
        sub = A[sel]
        idx = np.arange(sel.size)
        tmp = sub[idx, ra, :].copy()
        sub[idx, ra, :] = sub[idx, pa, :]
        sub[idx, pa, :] = tmp
        piv = sub[idx, ra, j]
        sub[idx, ra, :] = (sub[idx, ra, :] * inv[piv][:, None]) % p
        prow = sub[idx, ra, :]
        fac = sub[:, :, j].copy()
        fac[idx, ra] = 0
        sub = (sub - fac[:, :, None] * prow[:, None, :]) % p
        A[sel] = sub
        r[sel] += 1
    last = A[:, :, K]
    bad = ((rows[None, :] >= r[:, None]) & (last != 0)).any(axis=1)
    return r, ~bad


# ------------------------------------------------------- exhaustive method

def _affine_enum_spec(v, N, p):
    """Enumerate {a in F_p^N : v.a = 0}.  Returns (nfree, expand) where
    expand(free_array (B,nfree)) -> (B,N) array."""
    vv = [x % p for x in v]
    nz = [j for j in range(N) if vv[j] % p]
    if not nz:
        def expand(F):
            return F
        return N, expand
    j0 = nz[0]
    others = [j for j in range(N) if j != j0]
    invp = pow(vv[j0], p - 2, p)
    coef = np.array([(-vv[j] * invp) % p for j in others], dtype=np.int64)
    others_a = np.array(others, dtype=np.int64)

    def expand(F):
        B = F.shape[0]
        out = np.zeros((B, N), dtype=np.int64)
        out[:, others_a] = F
        out[:, j0] = (F @ coef) % p
        return out
    return N - 1, expand


def exhaustive(SP, SQ, p, budget=400000, max_solutions=20, chunk=8192):
    """Complete enumeration of the F_p solution set via the bilinear split.

    Returns dict: feasible(bool -- whether within budget), enum_side,
    n_enum, count (exact number of F_p solutions), solutions (sample).
    """
    eqs, pairs, cP, cQ = build_system(SP, SQ)
    NA, NB = len(SP), len(SQ)

    # decide which side to enumerate
    dimA = NA - (1 if any(x % p for x in cP) else 0)
    dimB = NB - (1 if any(x % p for x in cQ) else 0)
    side = "P" if dimA <= dimB else "Q"
    if side == "P":
        NF, NS, cF, cS = NA, NB, cP, cQ
    else:
        NF, NS, cF, cS = NB, NA, cQ, cP
    nfree, expand = _affine_enum_spec(cF, NF, p)
    total = p ** nfree
    if total > budget:
        return {"feasible": False, "n_enum": total, "enum_side": side}

    # tensor T[eq, s, f] : coefficient of (fixed_f * solve_s) in equation eq
    M = len(eqs) + 1                      # (K) rows + the other collision row
    T = np.zeros((len(eqs), NS, NF), dtype=np.int64)
    rhs0 = np.zeros(len(eqs), dtype=np.int64)
    for k, e in enumerate(eqs):
        for (mi, ni, c) in pairs[e]:
            f, s = (mi, ni) if side == "P" else (ni, mi)
            T[k, s, f] = (T[k, s, f] + c) % p
        if e == (0, 0):
            rhs0[k] = 1 % p
    cS_row = np.array([x % p for x in cS], dtype=np.int64)

    count = 0
    sols = []
    n_consistent = 0
    for start in range(0, total, chunk):
        stop = min(start + chunk, total)
        idx = np.arange(start, stop)
        F = np.zeros((stop - start, nfree), dtype=np.int64)
        t = idx.copy()
        for d in range(nfree - 1, -1, -1):
            F[:, d] = t % p
            t //= p
        fixed = expand(F)                       # (B, NF)
        Bn = fixed.shape[0]
        A = np.zeros((Bn, M, NS + 1), dtype=np.int64)
        A[:, :len(eqs), :NS] = np.einsum('ksf,bf->bks', T, fixed) % p
        A[:, :len(eqs), NS] = rhs0[None, :]
        A[:, len(eqs), :NS] = cS_row[None, :]
        rank, cons = batch_rank_consistent(A, p)
        nsol = np.where(cons, p ** (NS - rank), 0)
        count += int(nsol.sum())
        n_consistent += int(cons.sum())
        if len(sols) < max_solutions:
            for bi in np.nonzero(cons)[0]:
                if len(sols) >= max_solutions:
                    break
                fx = [int(v) for v in fixed[bi]]
                rows = []
                rr = []
                for k, e in enumerate(eqs):
                    rows.append([int(T[k, s, :] @ np.array(fx)) % p for s in range(NS)])
                    rr.append(int(rhs0[k]))
                rows.append([int(x) for x in cS_row])
                rr.append(0)
                got = solve_gfp(rows, rr, p)
                if got is None:
                    continue
                part, basis = got
                cands = [part]
                for v in basis[:3]:
                    cands.append([(part[i] + v[i]) % p for i in range(NS)])
                for sv in cands:
                    if len(sols) >= max_solutions:
                        break
                    if side == "P":
                        sols.append((fx, [int(z) for z in sv]))
                    else:
                        sols.append(([int(z) for z in sv], fx))
    return {"feasible": True, "n_enum": total, "enum_side": side,
            "count": count, "n_consistent_fibres": n_consistent,
            "solutions": sols}


# ------------------------------------------------------------ Hensel climb

def hensel_step(SP, SQ, a, b, p, level):
    """One linear Hensel step from Z/p^level to Z/p^{level+1}.

    Rederivation (in lane).  The residual map r : Z^N -> Z^M of (K)+(C) is
    quadratic in the unknowns, so Taylor is exact:
        r(x + h) = r(x) + Dr(x) h + B(h,h).
    If r(x_k) = 0 mod p^k, set x_{k+1} = x_k + p^k d.  Then
        r(x_k + p^k d) = r(x_k) + p^k Dr(x_k) d + p^{2k} B(d,d),
    and 2k >= k+1 for k >= 1, so mod p^{k+1}
        r(x_{k+1}) = p^k ( s_k + Dr(x_k) d ),   r(x_k) = p^k s_k.
    Hence a lift exists iff  Dr(x_k) d = -s_k  is solvable mod p, and
    Dr(x_k) = Dr(x_0) mod p since x_k = x_0 mod p.  The condition is
    necessary and sufficient.

    Returns (lifted_a, lifted_b) or None.
    """
    N_A = len(SP)
    r = residual_int(SP, SQ, a, b)
    pk = p ** level
    assert all(v % pk == 0 for v in r), "input is not a solution mod p^level"
    s = [v // pk for v in r]
    J = jacobian_int(SP, SQ, a, b)
    Jm = [[x % p for x in row] for row in J]
    rhsv = [(-x) % p for x in s]
    got = solve_gfp(Jm, rhsv, p)
    if got is None:
        return None
    part, _ = got
    na = [a[i] + pk * part[i] for i in range(N_A)]
    nb = [b[i] + pk * part[N_A + i] for i in range(len(SQ))]
    r2 = residual_int(SP, SQ, na, nb)
    if any(v % (pk * p) for v in r2):
        return None
    return na, nb
