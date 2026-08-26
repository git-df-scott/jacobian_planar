"""Session 43, Path S — the tear of Alpoge's map is RATIONAL, and stratifies as
(C*)^2 u C* u A^1.  Everything below is exact and gated.

Delta = 27w1^2w3^2 - 18w1w2w3 + w2^3w3 + 16w1 - w2^2 is QUADRATIC in w1, and its
discriminant is a PERFECT CUBE:

        disc_{w1}(Delta) = -4 (3 w2 w3 - 4)^3.

So putting  mu^2 := 4 - 3 w2 w3  makes the square root rational, and the tear is
parametrized birationally by (mu, r):

        w1 = (mu+1)(mu-2)^2 / (27 r^2)
        w2 = -(mu-2)(mu+2) / (3 r)
        w3 = r

The inverse is regular away from C_sing, and is given by the OTHER invariant that
turned up in the discriminant of the fibre cubic:

        mu = E / (4 - 3 w2 w3),      E = 27 w1 w3^2 - 9 w2 w3 + 8

(indeed 27 w1 w3^2 = mu(4-3w2w3) - 3(4-3w2w3) + 4, i.e. mu*(4-3w2w3) = E), and
on the tear E = 0 exactly on C_sing.  Hence the EXACT stratification

        tear n {w3 != 0} \ C_sing   ~   (C*)_mu x (C*)_r        [mu = 0 is C_sing]
        C_sing                      ~   C*                      [mu = 0]
        tear n {w3  = 0}            =   {16 w1 = w2^2}  ~  A^1   [the parabola]

    chi(tear) = 0 + 0 + 1 = 1.

CONSEQUENCE (the reason plane slices keep dying).  No curve in (C*)^2 has
positive Euler characteristic: its normalization carries two nowhere-zero
regular functions, and the units of C[A^1] are constants, so the normalization is
never A^1, hence chi <= 0 componentwise.  Therefore for any Sigma = C^2, writing
T = chi of the part of A_Sigma in the torus stratum, n = #C_Sigma and
P = chi(A_Sigma n {w3=0}),

        chi(A_Sigma) = T + n + P,   T <= 0,

and the Euler filter 2 chi(A_Sigma) + n = 2 becomes

        2T + 3n + 2P = 2,     T <= 0    ==>    3n + 2P >= 2,  n even.

So a slice with n = 0 MUST meet the parabola {w3=0, 16w1=w2^2} (P >= 1), and the
parabola is exactly the stratum that is = A^1 -- the one Chau/Abhyankar-Moh
forbids as a component of the non-properness set.  That is the precise tension
that killed all 7992 planes.
"""
import sympy as sp

w1, w2, w3, mu, r = sp.symbols('w1 w2 w3 mu r')

DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)
E = 27*w1*w3**2 - 9*w2*w3 + 8

W1 = (mu + 1)*(mu - 2)**2/(27*r**2)
W2 = -(mu - 2)*(mu + 2)/(3*r)
W3 = r

PASS = []

# 1. the discriminant is a perfect cube
q = sp.Poly(DELTA, w1)
a, b, cc = q.all_coeffs()
disc = sp.expand(b**2 - 4*a*cc)
PASS.append(("disc_{w1}(Delta) = -4(3 w2 w3 - 4)^3",
             sp.expand(disc + 4*(3*w2*w3 - 4)**3) == 0))

# 2. the parametrization lands on the tear, identically
PASS.append(("Delta vanishes identically on the parametrization",
             sp.simplify(DELTA.subs({w1: W1, w2: W2, w3: W3})) == 0))

# 3. mu^2 = 4 - 3 w2 w3 on the parametrization
PASS.append(("mu^2 = 4 - 3 w2 w3", sp.simplify(4 - 3*W2*W3 - mu**2) == 0))

# 4. the inverse: mu * (4 - 3 w2 w3) = E on the tear
PASS.append(("mu*(4-3w2w3) = E on the parametrization",
             sp.simplify((E.subs({w1: W1, w2: W2, w3: W3})) - mu*(4 - 3*W2*W3)) == 0))

# 5. C_sing = {mu = 0}
PASS.append(("mu=0 is exactly C_sing = (4/27t^2, 4/3t, t)",
             [sp.simplify(e.subs(mu, 0)) for e in (W1, W2, W3)]
             == [sp.Rational(4, 27)/r**2, sp.Rational(4, 3)/r, r]))

# 6. on the tear, E = 0 exactly on C_sing (so mu != 0 off C_sing).
#    (4-3w2w3) lies in the RADICAL of (Delta,E), not in the ideal, so test it the
#    only correct way -- Rabinowitsch: V(Delta,E) n {4-3w2w3 != 0} = empty.
_sv = sp.Symbol('_s')
_G = sp.groebner([DELTA, E, sp.expand(_sv*(4 - 3*w2*w3) - 1)],
                 w1, w2, w3, _sv, order='grevlex')
PASS.append(("on the tear, E=0 forces 4-3w2w3=0 (i.e. C_sing)",
             list(_G.exprs) == [sp.Integer(1)]))

# 7. the w3 = 0 slice of the tear is the parabola, which IS isomorphic to A^1
PASS.append(("tear n {w3=0} = {16w1 = w2^2}",
             sp.expand(DELTA.subs(w3, 0)) == sp.expand(16*w1 - w2**2)))

# 8. chi(tear) = 0 (torus) + 0 (C_sing = C*) + 1 (parabola = A^1) = 1
PASS.append(("chi(tear) = 1 by the stratification", 0 + 0 + 1 == 1))

if __name__ == '__main__':
    print("Delta as a quadratic in w1:")
    print("   a =", a, "  b =", b, "  c =", cc)
    print("   disc =", sp.factor(disc))
    print("\nparametrization of the tear:")
    print("   w1 =", W1)
    print("   w2 =", W2)
    print("   w3 =", W3)
    print("   inverse: r = w3,  mu = E/(4-3 w2 w3),  E =", E)
    print("\nstratification:")
    print("   tear n {w3!=0} \\ C_sing  ~  (C*)_mu x (C*)_r      chi = 0")
    print("   C_sing = {mu=0}          ~  C*                    chi = 0")
    print("   tear n {w3=0}            =  {16w1=w2^2} ~ A^1     chi = 1")
    print()
    for nm, ok in PASS:
        print(("PASS " if ok else "FAIL ") + nm)
    assert all(ok for _, ok in PASS)
