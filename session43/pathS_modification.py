"""Session 43, Path S — the slice family is a family of AFFINE MODIFICATIONS.

Every component of Alpoge's map is LINEAR in z:

    P = (1+xy)^3 z + y^2(1+xy)(4+3xy)
    Q = 3x(1+xy)^2 z + y + 3xy^2(4+3xy)
    R = -x^3 z + 2x - 3x^2 y

so for a target plane  W = { a w1 + b w2 + c w3 = k }  the slice

    S = F^{-1}(W) = { A(x,y) z = B(x,y) }  subset C^3

with

    A = a(1+xy)^3 + 3b x(1+xy)^2 - c x^3            (= (a,b,c) . dF/dz)
    B = k - [ a y^2(1+xy)(4+3xy) + b (y + 3xy^2(4+3xy)) + c (2x - 3x^2 y) ]

S is SMOOTH for every (a,b,c,k) != 0 (grad(l o F) = (a,b,c).JF never vanishes,
JF invertible), F|_S : S -> W is ETALE, and because F is 3:1 EVERYWHERE, F|_S is
NON-INJECTIVE for every W (the three preimages of a generic point of W all lie
in S by definition).  Hence:

    *** if S = C^2 for ANY (a,b,c,k), the planar Jacobian Conjecture is FALSE ***

(the Jacobian of F|_S in coordinates is a nowhere-zero regular function on C^2,
i.e. a nonzero constant, so Keller is automatic; non-injectivity is automatic.)

STRUCTURE.  pi: S -> C^2_{x,y} is an isomorphism over {A != 0}; over a point of
{A = 0} the fibre is a LINE if B also vanishes there and is EMPTY otherwise.
Therefore

    S \ pi^{-1}(A=0)  =  C^2 \ {A=0}                  (open, dense)
    S  =  (C^2 \ {A=0})  u  (one line over each point of {A=B=0})

giving two exact invariants:

    chi(S)   = 1 - chi({A=0}) + #{A=B=0}
    pi_1(S)  = pi_1(C^2 \ {A=0}) / <<meridians of the components that are HIT>>

so H_1(S) = Z^r / <mu_i : component i contains a point of {A=B=0}> where r is the
number of irreducible components of {A=0}.  A NECESSARY condition for S = C^2:

    *** every irreducible component of {A=0} must contain a point of {A=B=0} ***

This module implements that filter exactly and scans the (a,b,c,k) family.

Worked example proving the filter has teeth (verified below):
  (a,b,c,k)=(0,1,0,0), i.e. W = {w2 = 0}:  A = 3x(1+xy)^2, B = -(y+3xy^2(4+3xy)).
  chi(S) = 1  -- passes the Euler filter -- but {A=B=0} = {(0,0)} lies only on
  the component {x=0}; the component {1+xy=0} is NOT hit, so pi_1(S) = Z and
  S is NOT C^2.  The Euler characteristic alone is too weak; H_1 is the real gate.
"""
import sympy as sp
from itertools import product

x, y, z = sp.symbols('x y z')

U = 1 + x*y
P = U**3*z + y**2*U*(4 + 3*x*y)
Q = 3*x*U**2*z + y + 3*x*y**2*(4 + 3*x*y)
R = -x**3*z + 2*x - 3*x**2*y


def slice_AB(a, b, c, k):
    """S = {A z = B} for the plane a*w1 + b*w2 + c*w3 = k."""
    L = sp.expand(a*P + b*Q + c*R - k)
    A = sp.expand(sp.diff(L, z))
    B = sp.expand(-(L - A*z))
    assert sp.expand(A*z - B - L) == 0
    return sp.Poly(A, x, y), sp.Poly(B, x, y)


def components(A):
    """Irreducible components of {A=0} with multiplicities (constants dropped)."""
    out = []
    for base, mult in sp.factor_list(A.as_expr())[1]:
        if base.free_symbols:
            out.append((sp.expand(base), mult))
    return out


def meets(f, B):
    """Does the affine curve {f=0} meet {B=0} in C^2?  Exact, by the Nullstellensatz.

    NOTE: a resultant test is WRONG here.  res_y(f,B) picks up spurious roots
    wherever lc_y(f) vanishes.  Concretely for f = 1+xy and B = k - 3y^2(1+xy)(4+3xy)
    one gets res_y = k * x^(deg_y B), which vanishes at x=0 -- but {1+xy=0} has NO
    point with x=0, and in fact B == k != 0 on the whole component.  Groebner
    over Q decides emptiness correctly: V(f,B) = empty  iff  (f,B) = (1).
    """
    f = sp.expand(f)
    Bf = sp.expand(B.as_expr()) if hasattr(B, 'as_expr') else sp.expand(B)
    if Bf == 0:
        return True, 'B vanishes identically (1-dimensional centre)'
    G = sp.groebner([f, Bf], x, y, order='grevlex')
    if list(G.exprs) == [sp.Integer(1)]:
        return False, 'ideal (f,B) = (1): component NOT hit'
    return True, 'ideal (f,B) proper: component hit'


def analyse(a, b, c, k, verbose=True):
    A, B = slice_AB(a, b, c, k)
    comps = components(A)
    if not comps:                      # A is a nonzero constant: S = C^2_{x,y}!
        return dict(a=a, b=b, c=c, k=k, comps=[], hit=[], verdict='A CONSTANT')
    hit = []
    for f, m in comps:
        h, why = meets(f, B)
        hit.append((f, m, h, why))
    allhit = all(h for _, _, h, _ in hit)
    if verbose:
        print("\n(a,b,c,k)=(%s,%s,%s,%s)   A = %s" % (a, b, c, k, sp.factor(A.as_expr())))
        for f, m, h, why in hit:
            print("    comp %-28s mult %d   HIT=%-5s  (%s)" % (f, m, h, why))
        print("    ALL COMPONENTS HIT:", allhit, " -> H_1 filter", "PASS" if allhit else "FAIL")
    return dict(a=a, b=b, c=c, k=k, comps=comps, hit=hit, verdict='PASS' if allhit else 'FAIL')


if __name__ == '__main__':
    print("=" * 70)
    print("worked example: W = {w2 = 0}  (chi(S)=1 but H_1(S)=Z)")
    analyse(0, 1, 0, 0)

    print("\n" + "=" * 70)
    print("W = {w1 = -1/4} (through the collision value):")
    analyse(1, 0, 0, sp.Rational(-1, 4))

    print("\n" + "=" * 70)
    print("SCAN of the (a,b,c,k) family")
    vals = [0, 1, -1, 2, sp.Rational(1, 2), -2, 3, sp.Rational(-1, 4), 4, sp.Rational(1,3)]
    passes = []
    seen = set()
    for a, b, c in product([0, 1, -1, 2, sp.Rational(1, 3), 3], repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        for k in [0, 1, -1, sp.Rational(-1, 4), 2]:
            key = (a, b, c, k)
            if key in seen:
                continue
            seen.add(key)
            r = analyse(a, b, c, k, verbose=False)
            if r['verdict'] in ('PASS', 'A CONSTANT'):
                passes.append(r)
                print("  CANDIDATE (a,b,c,k)=(%s,%s,%s,%s)  verdict=%s  A=%s"
                      % (a, b, c, k, r['verdict'], sp.factor(slice_AB(a, b, c, k)[0].as_expr())))
    print("\ntotal candidates passing the H_1 filter:", len(passes))
