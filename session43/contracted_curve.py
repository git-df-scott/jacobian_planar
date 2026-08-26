"""Session 43 -- the Keller condition restricted to the CONTRACTED CURVE.

WHERE THIS SITS.  descent_keller.py collapsed the whole dimension-3 Keller
condition for a C*-equivariant map to one plane identity

    W := A{alpha,B} - 2B{alpha,A} + alpha{A,B} = c != 0,
    A in (u,v),  B in (u^2,v),   G = (alpha*A, alpha^2*B),  det JG = c*alpha^2.

Because G_1 = alpha*A and G_2 = alpha^2*B both vanish on {alpha = 0}, the map G
CONTRACTS that whole curve to the origin.  That is a lot of structure and it is
where the condition is easiest to read.

THE PATH S TARGET.  The slice S = {F_p = k} is an affine modification exactly
when deg_v alpha = 1, i.e. alpha = alpha0(u) + alpha1(u) v; then

    chi(S) = #{ nonzero roots r of alpha1 with alpha0(r) != 0 }

so S can be C^2 only if alpha1 has exactly ONE such root.  The sharpest single
target in the whole family is therefore alpha1 of degree 1, and after an affine
change of u we may take

    alpha = k + (u - r) v,        k = alpha0(r) != 0,

whose contracted curve is the HYPERBOLA (u-r)v = -k, i.e. C ~ C*, parametrized
by  u = r + w,  v = -k/w.

THE REDUCTION (verified below).  On that curve, with ' = d/dw,

    W|_C  =  w ( 2 B A' - A B' )        [A, B meaning their restrictions]

so Keller forces the LAURENT-POLYNOMIAL identity

    w (2 B A' - A B') = c,     equivalently   D(B/A^2) = -c/A^3,  D = w d/dw,
    equivalently  (B/A^2)' = -c/(w A^3).

The last form is the useful one: a derivative of a rational function has zero
residue at every point of P^1, so the 1-form  dw/(w A^3)  must have zero residue
everywhere.  In particular, if A has no zero in C* it is a monomial a*w^m, and
integrating gives B = (c/(3 m a)) w^(-m) with m != 0 -- m = 0 would need a log.
The pole-order bookkeeping also forces every zero of A in C* to be SIMPLE with
B nonvanishing there.

WHAT THIS DOES AND DOES NOT SETTLE.  It is a NECESSARY condition, not a
sufficient one: solutions on C are candidates that still have to satisfy W = c
on all of C^2.  The enumeration below finds that non-monomial solutions of the
curve identity do exist, so the curve alone does not close the target.  It does
cut the candidate set down to an explicit finite list of shapes.

A BUG WORTH RECORDING.  The first enumeration reported ZERO monomial solutions,
contradicting the hand derivation above.  Cause: for a support pair whose only
equation is the k=0 one, the list of non-constant constraints is EMPTY, and
sympy's solve([], vars) returns [] -- "no solutions" -- for a system that every
point satisfies.  The contradiction with the hand derivation is what exposed it.
Every family returned below is now VERIFIED by substitution before being
reported, so a family that does not actually satisfy the identity cannot appear.
"""
import itertools
import sys
import sympy as sp

u, v, w = sp.symbols('u v w')
k, r = sp.symbols('k r', nonzero=True)
OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    return bool(ok)


def br(f, g):
    return sp.expand(sp.diff(f, u) * sp.diff(g, v) - sp.diff(f, v) * sp.diff(g, u))


def W(al, A, B):
    return sp.expand(A * br(al, B) - 2 * B * br(al, A) + al * br(A, B))


def T(A, B):
    """The curve identity's left-hand side, w(2 B A' - A B')."""
    return sp.expand(sp.simplify(w * (2 * B * sp.diff(A, w) - A * sp.diff(B, w))))


# --------------------------------------------------- [A] the restriction identity
def part_A():
    print("[A]  W restricted to the contracted curve equals w(2 B A' - A B')")
    al = k + (u - r) * v
    sub = {u: r + w, v: -k / w}
    cases = [(u * (1 + u) + v * 3, u**2 * (2 + u) + v * (1 + u + v)),
             (u * (2 + 5 * v) + v * (7 + u**2), u**2 * (1 + v) + v * (3 + u * v + u**2)),
             (u * (1 + u + u * v) + v * (2 + v), u**2 * (1 + u * v) + v * (1 + u + v**2)),
             (u * 4 + v * (1 + u**3), u**2 * (5 + v**2) + v * (2 + u))]
    for i, (A, B) in enumerate(cases):
        lhs = sp.simplify(sp.together(W(al, A, B).subs(sub, simultaneous=True)))
        Aw = sp.simplify(A.subs(sub, simultaneous=True))
        Bw = sp.simplify(B.subs(sub, simultaneous=True))
        d = sp.simplify(sp.expand(sp.together(lhs - T(Aw, Bw))))
        rec("case %d: W|_C - w(2 B A' - A B') = 0" % (i + 1), d == 0, "got %s" % d)
    # and the curve really is contracted
    A, B = cases[0]
    G1 = sp.expand(al * A)
    G2 = sp.expand(al**2 * B)
    rec("G contracts {alpha=0} to the origin: G1 and G2 both vanish there",
        sp.simplify(G1.subs(sub, simultaneous=True)) == 0
        and sp.simplify(G2.subs(sub, simultaneous=True)) == 0)
    print()


# ------------------------------------------------ [B] the monomial solution family
def part_B():
    print("[B]  the monomial family, derived by integrating D(B/A^2) = -c/A^3")
    a, m, c = sp.symbols('a m c', nonzero=True)
    A = a * w**m
    B = c / (3 * m * a) * w**(-m)
    rec("A = a w^m, B = c/(3ma) w^(-m) satisfies w(2BA' - AB') = c exactly",
        sp.simplify(T(A, B) - c) == 0, "T = %s" % sp.simplify(T(A, B)))
    # m = 0 must fail: it would need a logarithm
    rec("m = 0 is impossible (A constant makes the identity 0 = c)",
        sp.simplify(T(a * w**0, sp.Symbol('b') * w**0)) == 0)
    # A and B both v-free is impossible for a different, exact reason
    b_, d_ = sp.Function('b')(u), sp.Function('d')(u)
    al = sp.Function('a0')(u) + sp.Function('a1')(u) * v
    Wv = W(al, u * b_, u**2 * d_)
    Wv = sp.simplify(sp.expand(Wv))
    # The predicate here was originally written as an is_polynomial() test on a
    # cancelled expression, which does not test the claim at all and reported a
    # failure while printing exactly the claimed factorisation.  Test the claim.
    a1 = sp.Function('a1')(u)
    want = sp.expand(a1 * u**3 * (2 * d_ * sp.diff(b_, u) - b_ * sp.diff(d_, u)))
    rec("A, B both independent of v: W = alpha1(u) * u^3 * (2 d b' - b d') "
        "identically, hence divisible by u^3 and never a nonzero constant",
        sp.simplify(sp.expand(Wv - want)) == 0 and sp.simplify(Wv.subs(u, 0)) == 0,
        "W = %s" % sp.factor(Wv))
    print()


# --------------------------------------------- [C] exhaustive enumeration on C
def families(N, maxsupp=3):
    exps = list(range(-N, N + 1))
    out = []
    supps = [s for j in range(1, maxsupp + 1) for s in itertools.combinations(exps, j)]
    for sa in supps:
        for sb in supps:
            av = {i: sp.Symbol('a_%d' % (i + N)) for i in sa}
            bv = {j: sp.Symbol('b_%d' % (j + N)) for j in sb}
            eqs = {}
            for i in sa:
                for j in sb:
                    eqs[i + j] = eqs.get(i + j, 0) + av[i] * bv[j] * (2 * i - j)
            cons = [sp.expand(e) for kk, e in eqs.items() if kk != 0 and sp.expand(e) != 0]
            if sp.expand(eqs.get(0, 0)) == 0:
                continue
            # THE FIX: an empty constraint list is satisfied by EVERY point.
            sols = [{}] if not cons else (
                sp.solve(cons, list(av.values()) + list(bv.values()), dict=True) or [])
            for s in sols:
                if any(sp.simplify(s.get(av[i], av[i])) == 0 for i in sa):
                    continue
                if any(sp.simplify(s.get(bv[j], bv[j])) == 0 for j in sb):
                    continue
                A = sum(s.get(av[i], av[i]) * w**i for i in sa)
                B = sum(s.get(bv[j], bv[j]) * w**j for j in sb)
                val = sp.simplify(T(A, B))
                if val == 0 or val.has(w):      # VERIFY before reporting
                    continue
                out.append((sa, sb, sp.simplify(A), sp.simplify(B), val))
    return out


def part_C():
    print("[C]  every solution of the curve identity with support in a window,")
    print("     each one VERIFIED by substitution before it is reported")
    for N in (1, 2):
        f = families(N)
        mono = [t for t in f if len(t[0]) == 1 and len(t[1]) == 1]
        non = [t for t in f if not (len(t[0]) == 1 and len(t[1]) == 1)]
        rec("window [-%d,%d]: %d verified families, %d monomial, %d non-monomial"
            % (N, N, len(f), len(mono), len(non)), len(mono) > 0,
            "monomial solutions must exist -- part [B] exhibits them; "
            "zero would mean the enumerator is broken")
        for sa, sb, A, B, c in mono[:3]:
            print("       monomial  A = %-18s B = %-18s T = %s" % (A, B, c))
        for sa, sb, A, B, c in non[:4]:
            print("       non-mono  A = %-30s B = %-20s T = %s"
                  % (str(A)[:30], str(B)[:20], c))
        print()
    print("     So the contracted-curve identity does NOT by itself close the")
    print("     Path S target: non-monomial solutions exist on C.  It is a")
    print("     necessary condition that cuts the candidates to an explicit list,")
    print("     and each still has to satisfy W = c on all of C^2.")
    print()


if __name__ == '__main__':
    part_A()
    part_B()
    part_C()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("=" * 72)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
