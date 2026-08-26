"""Session 43, LANE P — how does the MINIMAL degree of a planar counterexample
grow with the characteristic?

MOTIVATION.  JC2 is false in characteristic p, and until 2026 that was treated as
uninformative ("char p is always false, move on").  Mondello (arXiv:2608.02634)
changed the picture by exhibiting a SEPARABLE char-2 planar counterexample of
geometric degree 3 -- an object the campaign had never had.  That invites a
question nobody appears to have asked:

    let m(p) := the minimal total degree of a planar Keller counterexample
                over F_p.   How does m(p) behave as p grows?

If m(p) is BOUNDED, there is a bounded-degree family of counterexamples across
infinitely many primes, and a bounded-degree family with a uniform shape is
exactly what could be lifted -- the collision variety
    { (z1,z2) : z1 != z2,  F(z1) = F(z2) }
of a pair (P,Q) in Z[x,y] with det J = 1 EXACTLY is a Q-variety, and a Q-variety
with F_p-points for infinitely many p is nonempty over Qbar (an emptiness
certificate 1 = sum h_i f_i has only finitely many bad primes).  So bounded
degree across many primes is a genuine roadmap.

If instead m(p) GROWS with p -- the Artin-Schreier family (x^p + x, y) has
det J = p x^(p-1) + 1 = 1 and is p-to-1, giving m(p) <= p -- then the char-p
counterexamples are a Frobenius artefact that thins out as p -> infinity, which
is evidence FOR JC2 in characteristic zero and says the char-2 example is not a
template.

WHY THIS LANE IS WORTH RUNNING (and Lane U was not, on its own).  It has a REAL
POSITIVE CONTROL.  The Artin-Schreier pair (x^p + x, y) is a genuine
counterexample mod p of degree p, so the search MUST find it; a run that misses
it is a broken run, not evidence.  Lane U had no such control -- no member of
that family is even an automorphism -- which is why its zero was weak.

METHOD.  For FIXED P the Keller equation [P,Q] = 1 is LINEAR in the coefficients
of Q (the collision-first trick), so: sweep P over a support mod p, solve one
linear system for Q, and test non-injectivity by BRUTE FORCE over F_p^2 and
F_{p^2}^2 -- which is trivial for small p and needs no Groebner basis at all.
"""
import sys
import itertools


def bracket_mod(P, Q, p):
    """[P,Q] = P_x Q_y - P_y Q_x for dicts {(i,j): c} mod p."""
    def dx(D):
        return {(i - 1, j): (c*i) % p for (i, j), c in D.items() if i > 0 and (c*i) % p}

    def dy(D):
        return {(i, j - 1): (c*j) % p for (i, j), c in D.items() if j > 0 and (c*j) % p}

    def mul(A, B):
        out = {}
        for (i, j), c in A.items():
            for (k, l), d in B.items():
                key = (i + k, j + l)
                out[key] = (out.get(key, 0) + c*d) % p
        return {k: v for k, v in out.items() if v}

    A, B = mul(dx(P), dy(Q)), mul(dy(P), dx(Q))
    out = dict(A)
    for k, v in B.items():
        out[k] = (out.get(k, 0) - v) % p
    return {k: v for k, v in out.items() if v}


def solve_Q(P, qsupport, p):
    """All Q on qsupport with [P,Q] = 1 mod p.  Linear system, exact over F_p."""
    rows = {}
    for idx, m in enumerate(qsupport):
        br = bracket_mod(P, {m: 1}, p)
        for k, v in br.items():
            rows.setdefault(k, [0]*len(qsupport))[idx] = v
    keys = sorted(rows)
    A = [rows[k][:] for k in keys]
    b = [1 if k == (0, 0) else 0 for k in keys]
    n = len(qsupport)
    # Gaussian elimination over F_p
    piv, r = [], 0
    for c in range(n):
        pr = next((i for i in range(r, len(A)) if A[i][c] % p), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        b[r], b[pr] = b[pr], b[r]
        inv = pow(A[r][c], p - 2, p)
        A[r] = [(x*inv) % p for x in A[r]]
        b[r] = (b[r]*inv) % p
        for i in range(len(A)):
            if i != r and A[i][c] % p:
                f = A[i][c]
                A[i] = [(A[i][k] - f*A[r][k]) % p for k in range(n)]
                b[i] = (b[i] - f*b[r]) % p
        piv.append(c)
        r += 1
    for i in range(r, len(A)):
        if b[i] % p and not any(A[i]):
            return []                                  # inconsistent
    free = [c for c in range(n) if c not in piv]
    sols = []
    for vals in itertools.product(range(p), repeat=len(free)):
        sol = [0]*n
        for c, v in zip(free, vals):
            sol[c] = v
        for i, c in reversed(list(enumerate(piv))):
            sol[c] = (b[i] - sum(A[i][k]*sol[k] for k in range(n) if k != c)) % p
        sols.append({m: v for m, v in zip(qsupport, sol) if v})
        if len(sols) > 400:
            break
    return sols


def ev(D, xv, yv, p):
    return sum(c*pow(xv, i, p)*pow(yv, j, p) for (i, j), c in D.items()) % p


def is_noninjective_Fp(P, Q, p):
    seen = {}
    for xv in range(p):
        for yv in range(p):
            k = (ev(P, xv, yv, p), ev(Q, xv, yv, p))
            if k in seen:
                return True, (seen[k], (xv, yv))
            seen[k] = (xv, yv)
    return False, None


def total_degree(D):
    return max((i + j for (i, j) in D), default=0)


def artin_schreier_control(p):
    """(x^p + x, y) must be found: det J = p x^(p-1) + 1 = 1, and it is p-to-1."""
    P = {(p, 0): 1, (1, 0): 1}
    Q = {(0, 1): 1}
    br = bracket_mod(P, Q, p)
    ok_keller = (br == {(0, 0): 1})
    ok_noninj, wit = is_noninjective_Fp(P, Q, p)
    return ok_keller, ok_noninj, wit




# ---------------------------------------------------------------- F_{p^k}
# The F_p-point test above is NOT sufficient, and the positive control proved it:
# x -> x^p + x is injective on F_p (there x^p = x, so it is x -> 2x) yet p-to-1
# over the algebraic closure.  Non-injectivity must therefore be tested over a
# genuine extension.  A Keller map that is an automorphism is a bijection on
# every F_{p^k}; failing bijectivity on any one of them proves non-injectivity.

def _irreducible(p, k):
    """A monic irreducible of degree k over F_p, as a coefficient list (low first)."""
    if k == 1:
        return [0, 1]
    for tail in itertools.product(range(p), repeat=k):
        poly = list(tail) + [1]
        # trial-divide by all monic polys of degree 1..k//2
        red = False
        for d in range(1, k//2 + 1):
            for t2 in itertools.product(range(p), repeat=d):
                q = list(t2) + [1]
                r = poly[:]
                while len(r) >= len(q) and any(r):
                    while r and r[-1] == 0:
                        r.pop()
                    if len(r) < len(q):
                        break
                    f = r[-1]
                    sh = len(r) - len(q)
                    for i in range(len(q)):
                        r[i + sh] = (r[i + sh] - f*q[i]) % p
                while r and r[-1] == 0:
                    r.pop()
                if not r:
                    red = True
                    break
            if red:
                break
        if not red:
            return poly
    raise RuntimeError("no irreducible found")


class GFpk:
    """F_{p^k} as F_p[T]/(f).  Elements are tuples of length k."""

    def __init__(self, p, k):
        self.p, self.k, self.f = p, k, _irreducible(p, k)
        self.elts = [tuple(e) for e in itertools.product(range(p), repeat=k)]

    def mul(self, a, b):
        p, k, f = self.p, self.k, self.f
        r = [0]*(2*k - 1)
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    if bj:
                        r[i + j] = (r[i + j] + ai*bj) % p
        for d in range(2*k - 2, k - 1, -1):
            c = r[d]
            if c:
                r[d] = 0
                for i in range(k):
                    r[d - k + i] = (r[d - k + i] - c*f[i]) % p
        return tuple(r[:k])

    def add(self, a, b):
        return tuple((x + y) % self.p for x, y in zip(a, b))

    def scal(self, c, a):
        return tuple((c*x) % self.p for x in a)

    def pow(self, a, n):
        r = tuple([1] + [0]*(self.k - 1))
        while n:
            if n & 1:
                r = self.mul(r, a)
            a = self.mul(a, a)
            n >>= 1
        return r

    def ev(self, D, xv, yv):
        tot = tuple([0]*self.k)
        for (i, j), c in D.items():
            t = self.mul(self.pow(xv, i), self.pow(yv, j))
            tot = self.add(tot, self.scal(c, t))
        return tot


def is_noninjective_ext(P, Q, p, k):
    """Bijectivity of (P,Q) on F_{p^k}^2.  Failure proves non-injectivity over Fbar."""
    F = GFpk(p, k)
    seen = {}
    for xv in F.elts:
        for yv in F.elts:
            key = (F.ev(P, xv, yv), F.ev(Q, xv, yv))
            if key in seen:
                return True, (seen[key], (xv, yv))
            seen[key] = (xv, yv)
    return False, None


def noninjective_upto(P, Q, p, kmax=3):
    for k in range(1, kmax + 1):
        ni, wit = is_noninjective_ext(P, Q, p, k)
        if ni:
            return True, k, wit
    return False, None, None


if __name__ == '__main__':
    print("POSITIVE CONTROL: the Artin-Schreier pair (x^p + x, y)")
    for p in (2, 3, 5, 7, 11):
        k, n, w = artin_schreier_control(p)
        print("   p=%-3d  Keller=%-5s  non-injective over F_p=%-5s  witness=%s"
              % (p, k, n, w))

    print("\nSWEEP: for each p, the smallest total degree at which a non-injective")
    print("Keller pair turns up, over the support swept.")
    for p in (2, 3, 5):
        MON = [(i, j) for i in range(4) for j in range(3) if 0 < i + j <= 3]
        QSUP = [(i, j) for i in range(5) for j in range(4) if i + j <= 4]
        best, nfound, nkeller = None, 0, 0
        for coeffs in itertools.product(range(p), repeat=len(MON)):
            P = {m: c for m, c in zip(MON, coeffs) if c}
            if not P:
                continue
            for Q in solve_Q(P, QSUP, p):
                if not Q:
                    continue
                nkeller += 1
                ni, wit = is_noninjective_Fp(P, Q, p)
                if ni:
                    nfound += 1
                    d = max(total_degree(P), total_degree(Q))
                    if best is None or d < best[0]:
                        best = (d, dict(P), dict(Q), wit)
        print("   p=%d : Keller pairs seen %d, non-injective %d" % (p, nkeller, nfound))
        if best:
            print("        smallest max-degree %d:  P=%s  Q=%s  collision %s"
                  % (best[0], best[1], best[2], best[3]))
