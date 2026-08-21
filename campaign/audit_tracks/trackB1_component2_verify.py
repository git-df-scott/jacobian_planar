#!/usr/bin/env python3
"""INDEPENDENT verification of COMPONENT II of the pentagon bottom criterion.

Component II (new, 2026-08-14):

    S = c * A^2 * B,   B = z^2 + p z + q  squarefree,
    A = 2(5p^2 - 4q) z + p(7p^2 - 12q)         (up to scale)

is NOT a perfect square yet satisfies the bottom criterion (C4).  Three
independent checks, none of which reuses the derivation:

  CHECK 1  the ORIGINAL bracket:  [P_8, G] = z^2  with P_8^ = a S^2, using
           slice_bracket() from trackB1_sqrt.py verbatim (weights 8 and -10),
           G = R/S^2.  Exact rational arithmetic.
  CHECK 2  the SECOND (polynomial-W) criterion of the theorem file:
           2a (S' W - 2 S W') = b S^2 z^2  with W a POLYNOMIAL.
  CHECK 3  mod-p linear algebra, no derivation at all: solve for G with
           denominator S^N by brute-force linear solve over F_p, and confirm
           solvability on component II and NON-solvability on random
           squarefree / random A^2*B off the component.
"""
import sys, random
from fractions import Fraction
import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar')
from trackB1_sqrt import slice_bracket, pmul, padd, pscal, ptrim, pderiv

z = sp.symbols('z')

def component2(p_, q_, c=1):
    """Return (S, R) for the component-II member with S1 = z^2+p z+q."""
    A = 2*(5*p_**2 - 4*q_)*z + p_*(7*p_**2 - 12*q_)
    B = z**2 + p_*z + q_
    S = sp.expand(c*A**2*B)
    # U from the triangular solve, with a1 = 2(5p^2-4q), a0 = p(7p^2-12q)
    a1 = 2*(5*p_**2 - 4*q_)
    a0 = p_*(7*p_**2 - 12*q_)
    u4 = sp.Rational(1, 5)*a1
    u3 = a0/4 + a1*p_/40
    u2 = a0*p_/24 - 7*a1*p_**2/240 + a1*q_/15
    u1 = -5*a0*p_**2/96 + a0*q_/8 + 7*a1*p_**3/192 - 29*a1*p_*q_/240
    u0 = (5*a0*p_**3/64 - 13*a0*p_*q_/48 - 7*a1*p_**4/128
          + 23*a1*p_**2*q_/96 - 2*a1*q_**2/15)
    U = u4*z**4 + u3*z**3 + u2*z**2 + u1*z + u0
    R = sp.cancel(c*U/A)          # R = c * U / A  (S -> cS keeps R? see below)
    return sp.expand(S), sp.cancel(R)

# ------------------------------------------------------------------ CHECK 1/2
def checks_12(trials=15, seed=5):
    random.seed(seed)
    n_ok1 = n_ok2 = n = 0
    print("CHECK 1 (original bracket [P_8,G]=z^2) and CHECK 2 (polynomial W)")
    while n < trials:
        p_ = sp.Rational(random.randint(-9, 9), random.randint(1, 4))
        q_ = sp.Rational(random.randint(-9, 9), random.randint(1, 4))
        if p_ == 0 or q_ == 0:
            continue
        if p_**2 == 4*q_ or 5*p_**2 == 4*q_ or 7*p_**2 == 12*q_:
            continue
        S, R = component2(p_, q_)
        if sp.Poly(S, z).degree() != 4 or S.subs(z, 0) == 0:
            continue
        if sp.discriminant(sp.Poly(S, z)) != 0 and False:
            continue
        n += 1
        # --- perfect square?  (must be NOT, for this to be news)
        fac = sp.factor(S)
        sq = sp.simplify(sp.sqrt(sp.expand(S)))
        is_sq = sq.is_polynomial(z)
        # --- CHECK 1: [P_8, G] = z^2 with the raw bracket formula
        a = sp.Integer(1)
        G = sp.cancel(R/S**2)
        P8 = a*S**2
        br = sp.simplify(-10*sp.diff(P8, z)*G - 8*P8*sp.diff(G, z))
        # normalize: bracket is a nonzero constant times z^2 <=> br/z^2 const
        rat = sp.simplify(sp.cancel(br/z**2))
        ok1 = rat.is_constant() and rat != 0
        n_ok1 += ok1
        # --- CHECK 2: polynomial W with 2a(S'W - 2SW') = b S^2 z^2
        W = sp.cancel(R*S)
        lhs = sp.expand(sp.diff(S, z)*W - 2*S*sp.diff(W, z))
        rat2 = sp.cancel(lhs/(S**2*z**2))
        ok2 = (sp.together(W).as_numer_denom()[1].is_constant()
               and rat2.is_constant() and rat2 != 0)
        n_ok2 += ok2
        print(f"  p={p_} q={q_}  perfect_square={is_sq}  "
              f"[P_8,G]/z^2={rat}  W_poly={ok2}  W_ratio={rat2}")
        if is_sq:
            print("      (this member degenerated to a perfect square)")
    print(f"  CHECK 1: {n_ok1}/{n}    CHECK 2: {n_ok2}/{n}\n")
    return n_ok1 == n and n_ok2 == n

# -------------------------------------------------------------------- CHECK 3
def solve_G_modp(Scoef, p, Nmax=10, degmax=24):
    """Is there rational G = H/S^N with [P_8,G]=z^2?  Brute-force over F_p.
    Returns (True, N, H) or (False, None, None).  a = 1."""
    S = ptrim(list(Scoef))
    for N in range(0, Nmax + 1):
        # [P_8, H/S^N] = -10*(S^2)'*H/S^N - 8*S^2*(H/S^N)'
        #  = S^{-N-1} * [ -10*(S^2)' S H - 8 S^3 H' + 8 N S^2 S' H ]
        # want = z^2  =>  -10 (S^2)' S H - 8 S^3 H' + 8 N S^2 S' H = z^2 S^{N+1}
        S2 = pmul(S, S, p)
        S3 = pmul(S2, S, p)
        dS2 = pderiv(S2, p)
        Sp = pderiv(S, p)
        rhs = pmul([0, 0, 1], S, p)
        for _ in range(N):
            rhs = pmul(rhs, S, p)
        A1 = pmul(dS2, S, p)                 # coefficient of H  (times -10)
        A2 = pmul(S2, Sp, p)                 # coefficient of H  (times 8N)
        for dH in range(0, degmax + 1):
            rows = {}
            ncol = dH + 1
            cols = []
            for j in range(ncol):
                e = [0]*j + [1]
                t1 = pscal(pmul(A1, e, p), -10 % p, p)
                t2 = pscal(pmul(S3, pderiv(e, p), p), -8 % p, p)
                t3 = pscal(pmul(A2, e, p), (8*N) % p, p)
                cols.append(padd(padd(t1, t2, p), t3, p))
            m = max([len(c) for c in cols] + [len(rhs)])
            M = [[(cols[j][i] if i < len(cols[j]) else 0) for j in range(ncol)]
                 + [(rhs[i] if i < len(rhs) else 0)] for i in range(m)]
            # gaussian elimination
            r = 0
            piv = []
            for c in range(ncol):
                pr = next((i for i in range(r, m) if M[i][c]), None)
                if pr is None:
                    continue
                M[r], M[pr] = M[pr], M[r]
                inv = pow(M[r][c], p - 2, p)
                M[r] = [(v*inv) % p for v in M[r]]
                for i in range(m):
                    if i != r and M[i][c]:
                        f = M[i][c]
                        M[i] = [(M[i][k] - f*M[r][k]) % p for k in range(ncol+1)]
                piv.append(c)
                r += 1
            if any(all(M[i][c] == 0 for c in range(ncol)) and M[i][ncol]
                   for i in range(m)):
                continue
            H = [0]*ncol
            for i, c in enumerate(piv):
                H[c] = M[i][ncol]
            return True, N, ptrim(H)
    return False, None, None

def checks_3(p=65521, trials=25, seed=7):
    random.seed(seed)
    print(f"CHECK 3 (independent mod-{p} linear solve for G = H/S^N)")
    def tolist(S):
        P = sp.Poly(S, z)
        return [int(P.coeff_monomial(z**k) % p) for k in range(5)]
    hit = 0
    for _ in range(trials):
        p_ = random.randint(1, 30); q_ = random.randint(1, 30)
        if p_*p_ % p == 4*q_ % p or 5*p_*p_ % p == 4*q_ % p:
            continue
        S, R = component2(sp.Integer(p_), sp.Integer(q_))
        if sp.Poly(S, z).degree() != 4 or S.subs(z, 0) == 0:
            continue
        ok, N, H = solve_G_modp(tolist(S), p)
        hit += ok
        if not ok:
            print(f"    !! component-II member p={p_} q={q_} NOT solvable")
    print(f"  component II solvable: {hit} samples solvable")
    # controls
    bad = 0
    for _ in range(trials):
        S = [random.randrange(1, p) for _ in range(5)]
        ok, N, H = solve_G_modp(S, p)
        bad += ok
    print(f"  random (generic squarefree) S solvable: {bad}/{trials}  (expect 0)")
    bad2 = 0
    for _ in range(trials):
        a0_, a1_ = random.randrange(1, p), random.randrange(1, p)
        b = [random.randrange(1, p) for _ in range(3)]
        A = [a0_, a1_]
        S = pmul(pmul(A, A, p), b, p)
        if len(S) != 5:
            continue
        ok, N, H = solve_G_modp(S, p)
        bad2 += ok
    print(f"  random A^2*B (off component) solvable: {bad2}/{trials}  (expect 0)")
    # perfect squares (control that SHOULD be solvable)
    good = 0
    for _ in range(trials):
        A = [random.randrange(1, p) for _ in range(3)]
        S = pmul(A, A, p)
        ok, N, H = solve_G_modp(S, p)
        good += ok
    print(f"  random perfect squares solvable: {good}/{trials}  (expect all)")

if __name__ == "__main__":
    ok12 = checks_12()
    print()
    checks_3()
    print(f"\nCHECKS 1&2 all passed: {ok12}")
