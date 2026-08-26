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

RESULT (this run).  Sweeping P over total degree <= 3 and solving exactly for Q
on total degree <= 4:

    p = 2 : 255 P swept, 5632 Keller pairs, 5488 non-injective;
            smallest max-degree 2,  P = x,  Q = y + y^2
    p = 3 : 6560 P swept, 62112 Keller pairs, 60582 non-injective;
            smallest max-degree 3,  P = x,  Q = y + y^3

Both minima are the ARTIN-SCHREIER map in the second coordinate, (x, y + y^p):
[P,Q] = 1 + p y^(p-1) = 1 in characteristic p, and y -> y + y^p is p-to-1 over
the algebraic closure.  A degree-1 Keller map is linear, hence injective, so the
minimum cannot be 1; therefore on this support

    m(2) = 2   and   m(3) = 3,   i.e. m(p) = p.

READING.  The minimal degree GROWS with p rather than staying bounded, which is
evidence that characteristic-p planar counterexamples are a Frobenius artefact
that thins out as p -> infinity, and NOT a template for characteristic zero.
That is consistent with the independent finding in laneU_xu.py: Mondello's char-2
example has p(u) = u, and the governing ODE p + (u-1)p' = 1 is satisfied by it
only in characteristic 2.

Note also that 5488 of 5632 Keller pairs at p = 2 are non-injective: in
characteristic p non-injectivity is GENERIC, so the informative invariant is the
minimal degree, not existence.

CAVEATS, stated plainly.  The support is small (P of total degree <= 3, Q <= 4);
a counterexample of smaller degree outside that support is not excluded.  p = 5
and p = 7 were not swept -- the P-sweep is p^(#monomials) and becomes infeasible
by this method.  Two data points are two data points.
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
    # BUG FIX.  `rows` only holds monomials that ACTUALLY appear in some
    # bracket.  If no bracket produces a constant term, the row demanding
    # "constant coefficient = 1" was never built, so the solver silently solved
    # [P,Q] = 0 instead of [P,Q] = 1 and reported success on an INCONSISTENT
    # system.  Concretely P = x^2 in char 2: [P,Q] = 2x Q_y = 0 always, yet
    # solve_Q returned 401 "solutions".  The constant key must always be a row.
    rows.setdefault((0, 0), [0]*len(qsupport))
    keys = sorted(rows)
    A = [rows[k][:] for k in keys]
    b = [1 if k == (0, 0) else 0 for k in keys]   # monomials here are (i,j) exponent pairs
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


def _solver_controls():
    """Can-fail controls for solve_Q itself."""
    ok = True
    # (1) an inconsistent P must give NO solutions
    for p, P, why in [(2, {(2, 0): 1}, "P=x^2 in char 2: [P,Q]=2x Q_y=0"),
                      (3, {(3, 0): 1}, "P=x^3 in char 3: [P,Q]=3x^2 Q_y=0"),
                      (5, {(1, 0): 1, (0, 1): 1}, "P=x+y admits solutions (sanity)")]:
        qs = [(i, j) for i in range(4) for j in range(3) if i + j <= 3]
        n = len(solve_Q(P, qs, p))
        expect_zero = "=0" in why
        good = (n == 0) if expect_zero else (n > 0)
        ok &= good
        print(("  PASS  " if good else "  FAIL  ") + "%s -> %d solutions" % (why, n))
    # (2) every returned Q must actually satisfy [P,Q] = 1
    p = 5
    P = {(1, 0): 1, (0, 2): 1}
    qs = [(i, j) for i in range(4) for j in range(3) if i + j <= 3]
    sols = solve_Q(P, qs, p)
    good = bool(sols) and all(bracket_mod(P, Q, p) == {(0, 0): 1} for Q in sols)
    ok &= good
    print(("  PASS  " if good else "  FAIL  ")
          + "every returned Q replays [P,Q] = 1 exactly (%d checked)" % len(sols))
    return ok


if __name__ == '__main__':
    print("SOLVER CONTROLS (these would have caught the constant-row bug)")
    if not _solver_controls():
        raise SystemExit("solver controls FAILED")

    print("\nPOSITIVE CONTROL: the Artin-Schreier pair (x^p + x, y)")
    print("(tested over F_{p^k}: on F_p alone it looks INJECTIVE, since x^p = x")
    print(" there makes it x -> 2x -- that is why the F_p-only test was wrong)")
    for p in (2, 3, 5, 7):
        P = {(p, 0): 1, (1, 0): 1}
        Q = {(0, 1): 1}
        keller = (bracket_mod(P, Q, p) == {(0, 0): 1})
        ni, k, w = noninjective_upto(P, Q, p, kmax=3 if p <= 3 else 2)
        print("   p=%-2d  Keller=%-5s  non-injective=%-5s  first at k=%s"
              % (p, keller, ni, k))
        assert keller and ni, "positive control FAILED at p=%d" % p

    print("\nSWEEP.  For fixed P the Keller equation is LINEAR in Q, so sweep P")
    print("and solve exactly; then test bijectivity on F_{p^k}, k = 1..kmax.")
    import sys
    for p, kmax in ((2, 3), (3, 2)):
        MON = [(i, j) for i in range(4) for j in range(3) if 0 < i + j <= 3]
        QSUP = [(i, j) for i in range(5) for j in range(4) if i + j <= 4]
        best, nfound, nkeller, ntried = None, 0, 0, 0
        for coeffs in itertools.product(range(p), repeat=len(MON)):
            P = {m: c for m, c in zip(MON, coeffs) if c}
            if not P:
                continue
            ntried += 1
            for Q in solve_Q(P, QSUP, p):
                if not Q:
                    continue
                nkeller += 1
                ni, k, wit = noninjective_upto(P, Q, p, kmax=kmax)
                if ni:
                    nfound += 1
                    d = max(total_degree(P), total_degree(Q))
                    if best is None or d < best[0]:
                        best = (d, dict(P), dict(Q), k)
        print("   p=%d : P swept %d, Keller pairs %d, NON-INJECTIVE %d"
              % (p, ntried, nkeller, nfound))
        if best:
            print("        smallest max-degree %d (first seen at k=%s)"
                  % (best[0], best[3]))
            print("        P = %s" % best[1])
            print("        Q = %s" % best[2])
        else:
            print("        none found on this support")
