"""Session 43 — Path S on the counterexamples ABOVE Orevkov's floor.

Alpoge's map has geometric degree 3, and Orevkov (1986) proves a planar Keller
map of geometric degree 3 is an automorphism, so every slice of it was dead
before any computation.  The floor is: degrees 2,3,4,5 excluded, 6 OPEN.

Dimension-3 counterexamples above the floor now exist and are verified here
independently (det J recomputed from the polynomials, not taken on trust):

    gallagher_dim3_degree6   det J = 1,  geometric degree 6
    gallagher_dim3_degree12  det J = 1,  geometric degree 12
    dim3_degree6             det J = 2,  geometric degree 6
    dim3_degree7             det J = 2,  geometric degree 7

so Path S applies to them with NO Orevkov obstruction.

WHAT IS COMPUTABLE.  These maps have degrees like (22,21,4) and (52,51,4), so
their tear is out of reach of direct elimination.  But every one of them has
exactly ONE component that is LINEAR IN z -- the "monomial twist" component of
the tangent-sweep construction -- and for that component the slice is an affine
modification of C^2, which the machinery of this session handles exactly.

THE RESULT, and it is uniform.  In every case the z-linear component has the shape

    F = c x^3 z + a x^2 y + b x           (c, a, b nonzero constants)

so the slice {F = k} is  A z = B  with  A = c x^3  and  B = k - a x^2 y - b x.
The only component of {A = 0} is {x = 0}, and there

    B(0, y) = k   --  a CONSTANT, independent of y.

That single fact decides the whole family:
  * k != 0 : B has no zero on {x=0}, so there is no centre point, the fibre over
    {x=0} is EMPTY, and S is exactly C^2 minus {x=0} = C* x C.  Hence
    pi_1(S) = Z != 1 and S is NOT C^2.  (It is a perfectly good non-proper etale
    surface -- just not the plane.)
  * k  = 0 : B = -x(a x y + b) is divisible by x, so B vanishes on the WHOLE
    component: a 1-DIMENSIONAL centre, S is reducible, hence disconnected since
    S is smooth, and again not C^2.

So the obstruction is precisely that B(0,y) is CONSTANT, which is forced by the
monomial-twist shape (its only monomials are x^3 z, x^2 y and x, all of which
vanish at x = 0 except the constant k).

WHAT THE MATERIAL WOULD NEED (Blue-LED reading).  A slice of this kind can only
be C^2 if the z-linear component has either a NON-MONOMIAL z-coefficient, or a
B whose restriction to a component of {A=0} is NON-CONSTANT.  Alpoge's map does
have non-monomial z-coefficients -- (1+xy)^3 and 3x(1+xy)^2 -- which is why its
scan was interesting at all; but its geometric degree is 3, so Orevkov kills it.
The gap this leaves is sharp and worth stating: we would want a counterexample of
geometric degree >= 6 whose z-linear component has a non-monomial z-coefficient.
Composing with target automorphisms does not produce one: the only combinations
of (F1,F2,F3) that stay linear in z are the affine ones a*F3 + b, which give
back the same family.
"""
import os
import sys
import sympy as sp

x, y, z, k = sp.symbols('x y z k')
MAPS = os.path.join('/tmp/claude-0/-home-user-jacobian-planar/9c0f56a7-85d4-5d2a-8150-2daa4480a93e/scratchpad/maps')
OUT = []


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))


def load(path):
    src = open(path).read()
    g = {'sp': sp, 'x': x, 'y': y, 'z': z, 'w': sp.Symbol('w'),
         'R': sp.Rational, 'sys': sys, 'FAILURES': []}
    end = src.index('\n', src.index('F3 = (') + src[src.index('F3 = ('):].index('\n)'))
    exec(compile(src[:end + 2], '<m>', 'exec'), g)
    return [sp.expand(g['F1']), sp.expand(g['F2']), sp.expand(g['F3'])]


def analyse(F, label, expect_detJ):
    J = sp.Matrix([[sp.diff(f, v) for v in (x, y, z)] for f in F])
    d = sp.expand(J.det())
    rec("%s: det J = %s (recomputed independently)" % (label, expect_detJ), d == expect_detJ,
        "got %s" % d)
    zlin = [i for i, f in enumerate(F) if sp.Poly(f, z).degree() == 1]
    rec("%s: exactly one component is linear in z" % label, len(zlin) == 1, str(zlin))
    if not zlin:
        return
    f = F[zlin[0]]
    A = sp.expand(sp.diff(f, z))
    B = sp.expand(-(f - A*z - k))
    rec("%s: the z-coefficient is a pure power of x" % label,
        sp.factor_list(A)[1] == [(x, 3)] or
        [b for b, _m in sp.factor_list(A)[1] if b.free_symbols] == [x],
        "A = %s" % sp.factor(A))
    B0 = sp.expand(B.subs(x, 0))
    rec("%s: B restricted to {x=0} is the CONSTANT k" % label,
        sp.simplify(B0 - k) == 0, "B(0,y) = %s" % B0)
    # k != 0: fibre over {x=0} empty, so S = C^2 minus {x=0} = C* x C
    Bk = B.subs(k, 1)
    G = sp.groebner([x, sp.expand(Bk)], x, y, order='grevlex')
    rec("%s: for k != 0 there is NO centre point, so S = C* x C, pi_1 = Z" % label,
        list(G.exprs) == [sp.Integer(1)])
    # k = 0: B divisible by x -> 1-dimensional centre -> S reducible
    B0k = sp.expand(B.subs(k, 0))
    rec("%s: for k = 0 the component divides B: 1-dim centre, S reducible" % label,
        sp.simplify(sp.rem(B0k, x, x)) == 0, "B|_{k=0} = %s" % sp.factor(B0k))


if __name__ == '__main__':
    for fn, label, dj in [('gallagher_dim3_degree6.py', 'gallagher-d6', 1),
                          ('gallagher_dim3_degree12.py', 'gallagher-d12', 1),
                          ('dim3_degree6.py', 'constructed-d6', 2),
                          ('dim3_degree7.py', 'constructed-d7', 2)]:
        path = os.path.join(MAPS, fn)
        if not os.path.exists(path):
            print("  SKIP  %s (not present)" % fn)
            continue
        try:
            analyse(load(path), label, dj)
        except Exception as e:
            rec("%s: loaded" % label, False, "%s: %s" % (type(e).__name__, str(e)[:60]))
        print()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
