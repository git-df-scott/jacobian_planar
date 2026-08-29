"""night18 -- the mate system with SYMBOLIC parameters, and symbolic certificates.

For a carrier S (monomials for Q) the Keller equation [P,Q] = P_x Q_y - P_y Q_x = 1
is linear in q:      M(params) * q = e_{(0,0)} ,
with M's entries rational in the family's parameters.  All linear algebra is
done over the FIELD Q(params) with sympy's DomainMatrix (fraction-free rref in
the rational function field), never at sample points.

Fredholm over a field: exactly one of

  MATE   -- q over Q(params) with [P,Q] - 1 expanded coefficientwise = 0, or
  EMPTY  -- lambda over Q(params) with lambda^T M = 0 on EVERY column and
            lambda^T e = 1,

holds.  lambda is obtained as the solution of the transposed system
[M^T ; e_{(0,0)}^T] lambda = [0 ... 0 ; 1] -- no support guessing, no pivot
heuristics beyond the rref itself -- and is then RE-VERIFIED by exact expansion.
"""
import sys, os
import sympy as sp
from sympy.polys.matrices import DomainMatrix
import spk18 as spk

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'night17'))


def carrier(D):
    return sorted((i, j) for i in range(D + 1) for j in range(D + 1 - i))


def build(P, S):
    """columns of M: [P, x^i y^j]; rows: the monomials that occur."""
    cols = [spk.bracket(P, {m: sp.Integer(1)}) for m in S]
    rows = sorted({k for c in cols for k in c})
    return cols, rows


def field(gens):
    return sp.QQ.frac_field(*gens) if gens else sp.QQ


def _dm(rows2d, K):
    nr = len(rows2d)
    nc = len(rows2d[0]) if nr else 0
    E = [[K.from_sympy(sp.sympify(v)) for v in r] for r in rows2d]
    return DomainMatrix(E, (nr, nc), K)


def solve_linear(A, b, gens):
    """one solution of A z = b over Q(gens), free variables set to 0.

    returns (z, info) with z a list of sympy expressions, or (None, info) when
    the system is inconsistent."""
    K = field(gens)
    nr, nc = len(A), len(A[0]) if A else 0
    aug = _dm([list(A[i]) + [b[i]] for i in range(nr)], K)
    rref, piv = aug.rref()
    R = rref.to_Matrix()
    piv = list(piv)
    if nc in piv:                                  # pivot in the rhs column
        return None, {"rank": len(piv) - 1, "inconsistent": True}
    z = [sp.Integer(0)] * nc
    for r, c in enumerate(piv):
        z[c] = sp.cancel(sp.together(R[r, nc]))
    return z, {"rank": len(piv), "inconsistent": False, "n_unknowns": nc,
               "n_equations": nr, "free_dim": nc - len(piv)}


def rank_symbolic(cols, rows, gens):
    ridx = {m: i for i, m in enumerate(rows)}
    A = [[sp.Integer(0)] * len(cols) for _ in rows]
    for j, c in enumerate(cols):
        for m, v in c.items():
            A[ridx[m]][j] = v
    K = field(gens)
    return int(_dm(A, K).rank()), A


def solve_lambda(cols, rows, gens):
    """lambda^T M = 0 (one equation per column) with lambda_{(0,0)} = 1."""
    if (0, 0) not in rows:
        return {(0, 0): sp.Integer(1)}, {"note": "no column has a constant term",
                                         "rank": 0, "n_unknowns": len(rows)}
    n = len(rows)
    A = [[c.get(m, sp.Integer(0)) for m in rows] for c in cols]
    b = [sp.Integer(0)] * len(cols)
    e = [sp.Integer(0)] * n
    e[rows.index((0, 0))] = sp.Integer(1)
    A.append(e); b.append(sp.Integer(1))
    z, info = solve_linear(A, b, gens)
    if z is None:
        return None, info
    return {rows[i]: z[i] for i in range(n) if z[i] != 0}, info


def verify_lambda(lam, cols):
    """lambda^T M = 0 on every column and lambda^T e = 1, over Q(params)."""
    if sp.cancel(sp.together(lam.get((0, 0), 0) - 1)) != 0:
        return False, "lambda_(0,0) != 1"
    for j, c in enumerate(cols):
        s = sp.cancel(sp.together(sp.expand(sum(lam.get(m, 0) * v for m, v in c.items()))))
        if sp.simplify(s) != 0:
            return False, "column %d gives %s" % (j, sp.sstr(s))
    return True, "lambda^T M = 0 on all %d columns and lambda^T e = 1" % len(cols)


def solve_mate(cols, rows, S, gens):
    """M q = e over Q(gens)."""
    A = [[c.get(m, sp.Integer(0)) for c in cols] for m in rows]
    b = [sp.Integer(1) if m == (0, 0) else sp.Integer(0) for m in rows]
    z, info = solve_linear(A, b, gens)
    if z is None:
        return None, info
    return {S[j]: z[j] for j in range(len(S)) if z[j] != 0}, info


def denominators(lam):
    """generators of the denominator locus of a symbolic lambda, factored."""
    ds = {}
    for v in lam.values():
        d = sp.denom(sp.cancel(sp.together(v)))
        if d.is_number:
            continue
        for f, m in sp.factor_list(d)[1]:
            if not f.is_number:
                ds[sp.expand(f)] = max(ds.get(sp.expand(f), 0), m)
    return sorted(ds.items(), key=lambda kv: (sp.count_ops(kv[0]), sp.sstr(kv[0])))
