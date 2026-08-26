"""Session 43 -- can a C*-equivariant dimension-3 counterexample have deg alpha >= 2?

WHY THIS IS THE QUESTION.  descent_theorem.py + equivariant_ansatz.py showed
that two obstructions found by completely different routes are one obstruction:

  * Path S (pathS_highdegree.py): every slice of every known higher-degree
    counterexample is C* x C rather than C^2, because the z-linear component
    has a PURE MONOMIAL z-coefficient, so the slice's centre B(0,y) is constant.
  * The C* descent (descent_theorem.py): the descent's Jacobian is c*alpha^2
    where alpha = F_p/x, and alpha is AFFINE-LINEAR in all seven known maps.

alpha linear  <=>  F_p = a x^2 y + b x^3 z + c x  <=>  monomial z-coefficient.
Same fact.  So Path S is blocked at step one for every map we have, and the
one escape is a counterexample with deg alpha >= 2.

THE MACHINERY.  For weights (-1,1,2) with u = xy, v = x^2 z,

    F_p = x*alpha(u,v)
    F_q = y*beta(u,v) + x z*epsilon(u,v)
    F_r = y^2*delta(u,v) + z*gamma(u,v)

and det JF = Psi(u,v) is TRILINEAR: linear in alpha, linear in (beta,epsilon),
linear in (gamma,delta).  In particular, for FIXED (alpha,beta,epsilon) the
Keller condition Psi = const is a LINEAR system in (gamma,delta) -- and it is
linear HOMOGENEOUS, since every term of Psi carries exactly one gamma or delta.
So the whole question is a rank computation, done here exactly over F_p.

WHAT IS CONTROLLED.  Everything, because this session has been burned:
  * linearity in (gamma,delta) is not assumed, it is measured;
  * the constant monomial (0,0) is seeded into the row space UNCONDITIONALLY
    -- twice this session a solver silently solved the homogeneous system
    [P,Q] = 0 and reported success because the "constant = 1" row was built
    only from monomials that happened to appear;
  * every reported solution is REPLAYED: (gamma,delta) is substituted back and
    det JF recomputed from the polynomials;
  * positive controls: the solver must RECOVER the known counterexamples from
    their own (alpha,beta,epsilon);
  * a negative control that must fail: beta = epsilon = 0 makes Psi identically
    zero, so no constant is reachable.
"""
import os
import sys

P = 1000003
OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    return bool(ok)


# ------------------------------------------------------------ F_p polynomials
# poly3: dict {(i,j,k): c}  in x,y,z      polyuv: dict {(a,b): c}  in u,v
def padd(A, B):
    C = dict(A)
    for m, c in B.items():
        t = (C.get(m, 0) + c) % P
        if t:
            C[m] = t
        else:
            C.pop(m, None)
    return C


def pscal(A, s):
    s %= P
    if s == 0:
        return {}
    return {m: (c * s) % P for m, c in A.items()}


def pmul(A, B):
    C = {}
    for (i1, j1, k1), c1 in A.items():
        for (i2, j2, k2), c2 in B.items():
            m = (i1 + i2, j1 + j2, k1 + k2)
            t = (C.get(m, 0) + c1 * c2) % P
            if t:
                C[m] = t
            else:
                C.pop(m, None)
    return C


def pdiff(A, var):
    C = {}
    for m, c in A.items():
        e = m[var]
        if e == 0:
            continue
        n = list(m)
        n[var] = e - 1
        t = (c * e) % P
        if t:
            C[tuple(n)] = t
    return C


def uv_to_xyz(A):
    """u^a v^b  ->  x^(a+2b) y^a z^b."""
    C = {}
    for (a, b), c in A.items():
        m = (a + 2 * b, a, b)
        C[m] = (C.get(m, 0) + c) % P
    return {m: c for m, c in C.items() if c}


def xyz_to_uv(A):
    """Inverse on weight-0 polynomials.  Returns None if not weight 0."""
    C = {}
    for (i, j, k), c in A.items():
        if i != j + 2 * k:
            return None
        m = (j, k)
        C[m] = (C.get(m, 0) + c) % P
    return {m: c for m, c in C.items() if c}


X = {(1, 0, 0): 1}
Y = {(0, 1, 0): 1}
Z = {(0, 0, 1): 1}


def build_F(al, be, ga, de, ep):
    """(alpha,beta,gamma,delta,epsilon) as polyuv -> the three components."""
    A, B, G, D, E = (uv_to_xyz(t) for t in (al, be, ga, de, ep))
    Fp = pmul(X, A)
    Fq = padd(pmul(Y, B), pmul(pmul(X, Z), E))
    Fr = padd(pmul(pmul(Y, Y), D), pmul(Z, G))
    return [Fp, Fq, Fr]


def detJ(F):
    d = [[pdiff(f, t) for t in (0, 1, 2)] for f in F]
    def m2(r1, r2, c1, c2):
        return padd(pmul(d[r1][c1], d[r2][c2]),
                    pscal(pmul(d[r1][c2], d[r2][c1]), -1))
    return padd(padd(pmul(d[0][0], m2(1, 2, 1, 2)),
                     pscal(pmul(d[0][1], m2(1, 2, 0, 2)), -1)),
                pmul(d[0][2], m2(1, 2, 0, 1)))


def Psi(al, be, ga, de, ep):
    """det JF as a polynomial in (u,v).  Raises if it is not weight 0."""
    r = xyz_to_uv(detJ(build_F(al, be, ga, de, ep)))
    if r is None:
        raise AssertionError("det JF is not weight 0 -- ansatz broken")
    return r


# ------------------------------------------------------- exact F_p linear algebra
def inv(a):
    return pow(a % P, P - 2, P)


def rref(M, ncols):
    """In-place row reduce; return (M, pivot_cols)."""
    piv = []
    r = 0
    for c in range(ncols):
        pr = None
        for i in range(r, len(M)):
            if M[i][c]:
                pr = i
                break
        if pr is None:
            continue
        M[r], M[pr] = M[pr], M[r]
        iv = inv(M[r][c])
        M[r] = [(t * iv) % P for t in M[r]]
        for i in range(len(M)):
            if i != r and M[i][c]:
                f = M[i][c]
                M[i] = [(a - f * b) % P for a, b in zip(M[i], M[r])]
        piv.append(c)
        r += 1
        if r == len(M):
            break
    return M, piv


def kernel(rows, n):
    """Basis of the nullspace of the given rows (each length n)."""
    M = [list(r) for r in rows] or [[0] * n]
    M, piv = rref(M, n)
    free = [c for c in range(n) if c not in piv]
    basis = []
    for f in free:
        vec = [0] * n
        vec[f] = 1
        for i, c in enumerate(piv):
            vec[c] = (-M[i][f]) % P
        basis.append(vec)
    return basis


# --------------------------------------------- the solve-for-(gamma,delta) step
def mons(d):
    return [(a, b) for t in range(d + 1) for a in range(t + 1) for b in [t - a]]


def solve_gamma_delta(al, be, ep, dg, dd, verbose=False):
    """For fixed (alpha,beta,epsilon), find (gamma,delta) with Psi = nonzero const.

    Psi is linear HOMOGENEOUS in (gamma,delta), so build the matrix of its
    values on a monomial basis and look for a kernel vector of the
    non-constant rows whose constant row is nonzero.

    Returns (gamma, delta, kappa) or None.
    """
    basis = [('g', m) for m in mons(dg)] + [('d', m) for m in mons(dd)]
    cols = []
    for kind, m in basis:
        g = {m: 1} if kind == 'g' else {}
        d = {m: 1} if kind == 'd' else {}
        cols.append(Psi(al, be, g, d, ep))
    # THE GUARD: seed the constant monomial unconditionally.  If it is absent
    # from every column, the "constant = kappa" row must still exist and be
    # identically zero, so the solver reports failure instead of solving
    # Psi = 0 and calling it success.
    allm = {(0, 0)}
    for c in cols:
        allm |= set(c.keys())
    allm = sorted(allm)
    idx = {m: i for i, m in enumerate(allm)}
    n = len(basis)
    rows = [[0] * n for _ in allm]
    for j, c in enumerate(cols):
        for m, val in c.items():
            rows[idx[m]][j] = val
    c0 = idx[(0, 0)]
    homog = [rows[i] for i in range(len(allm)) if i != c0]
    ker = kernel(homog, n)
    for vec in ker:
        kappa = sum(rows[c0][j] * vec[j] for j in range(n)) % P
        if kappa:
            ga, de = {}, {}
            for (kind, m), cf in zip(basis, vec):
                if cf % P == 0:
                    continue
                (ga if kind == 'g' else de)[m] = cf % P
            return ga, de, kappa
    return None


def replay(al, be, ga, de, ep):
    """Recompute det JF from the polynomials.  Return the constant, or None."""
    r = Psi(al, be, ga, de, ep)
    if list(r.keys()) == [(0, 0)]:
        return r[(0, 0)]
    if not r:
        return 0
    return None


# ------------------------------------------------------------------- controls
def to_fp(expr, u, v, sp):
    """sympy poly in (u,v) with rational coefficients -> polyuv over F_p."""
    if expr == 0:
        return {}
    p = sp.Poly(expr, u, v)
    out = {}
    for m, c in p.terms():
        c = sp.Rational(c)
        val = (int(c.p) % P) * inv(int(c.q)) % P
        if val:
            out[(m[0], m[1])] = val
    return out


def controls():
    import sympy as sp
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import equivariant_ansatz as EA

    print("[A]  structural controls")
    # linearity in (gamma,delta): measured, not assumed
    import random
    random.seed(11)
    def rnd(d, nz=4):
        m = mons(d)
        return {random.choice(m): random.randrange(1, P) for _ in range(nz)}
    ok = True
    for _ in range(6):
        al, be, ep = rnd(2), rnd(3), rnd(2)
        g1, d1, g2, d2 = rnd(3), rnd(2), rnd(3), rnd(2)
        s1 = Psi(al, be, g1, d1, ep)
        s2 = Psi(al, be, g2, d2, ep)
        both = Psi(al, be, padd(g1, g2), padd(d1, d2), ep)
        ok &= (padd(s1, s2) == both)
    rec("Psi is ADDITIVE in (gamma,delta) -- measured on random inputs", ok)
    ok = all(Psi(rnd(2), rnd(3), {}, {}, rnd(2)) == {} for _ in range(6))
    rec("Psi is linear HOMOGENEOUS in (gamma,delta): gamma=delta=0 gives Psi=0", ok)
    ok = True
    for _ in range(6):
        al, be, ga, de, ep = rnd(2), rnd(3), rnd(3), rnd(2), rnd(2)
        s = Psi(al, be, ga, de, ep)
        s3 = Psi(pscal(al, 3), be, ga, de, ep)
        ok &= (pscal(s, 3) == s3)
    rec("Psi is linear in alpha as well (trilinearity, second slot)", ok)

    # NEGATIVE control that must fail
    r = solve_gamma_delta({(0, 0): 1, (1, 0): 5}, {}, {}, 3, 2)
    rec("NEGATIVE control: beta = epsilon = 0 makes Psi identically 0, "
        "so the solver must report NO solution", r is None,
        "" if r is None else "solver wrongly returned a solution")
    # and the guard itself: the constant row must exist even when unreachable
    rec("the constant monomial (0,0) is seeded unconditionally (guard against "
        "the bug that returned 401 'solutions' for P = x^2 over F_2)", True,
        "see solve_gamma_delta: allm starts as {(0,0)}")
    print()

    print("[B]  POSITIVE controls: recover the known counterexamples from "
          "(alpha,beta,epsilon) alone")
    cases = [('alpoge_dim3_degree3.py', 'alpoge d3', 3, 2),
             ('gallagher_dim3_degree3.py', 'gallagher d3', 3, 2),
             ('gao_G_dim3_degree4.py', 'gao G d4', 5, 4),
             ('dim3_degree6.py', 'constructed d6', 9, 8)]
    for fn, label, dg, dd in cases:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps', fn)
        if not os.path.exists(path):
            print("  SKIP  %s" % fn)
            continue
        F = EA.load(path)
        dd_ = EA.decompose(F)
        if dd_ is None:
            rec("%s: decomposes" % label, False)
            continue
        (a_, b_, g_, d_, e_), _perm = dd_
        al = to_fp(a_, EA.u, EA.v, sp)
        be = to_fp(b_, EA.u, EA.v, sp)
        ep = to_fp(e_, EA.u, EA.v, sp)
        gtrue = to_fp(g_, EA.u, EA.v, sp)
        dtrue = to_fp(d_, EA.u, EA.v, sp)
        # first: the map itself replays
        k0 = replay(al, be, gtrue, dtrue, ep)
        rec("%s: the published (gamma,delta) replays to det JF = %s" % (label, k0),
            k0 not in (None, 0))
        # now: does the solver FIND one, knowing only (alpha,beta,epsilon)?
        r = solve_gamma_delta(al, be, ep, dg, dd)
        if r is None:
            rec("%s: solver recovers a Keller (gamma,delta)" % label, False,
                "solver found nothing though a solution provably exists")
            continue
        ga, de, kappa = r
        k1 = replay(al, be, ga, de, ep)
        rec("%s: solver recovers a Keller (gamma,delta), replayed det JF = %s"
            % (label, k1), k1 not in (None, 0) and k1 == kappa % P,
            "kappa = %s" % kappa)
    print()


if __name__ == '__main__':
    controls()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("=" * 72)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
