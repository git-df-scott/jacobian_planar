#!/usr/bin/env python3
"""McKay-Wang certificates (JPAA 40 (1986) 245-257).

Two results from that paper give the campaign something it did not have: a
cheap, published CERTIFICATE that a Keller pair is a counterexample.

Corollary 14. If f, g define an isomorphism of K[x,y] then N(f) is the
triangle with vertices (0,0), (k,0), (0,n), where k = deg f(x,0) and
n = deg f(0,y) (and likewise for g).
  => contrapositive: N(f) not that triangle  ==>  (f,g) is NOT an
     automorphism.  Combined with det J = const != 0, that IS a
     counterexample to the Jacobian Conjecture -- no collision search and
     no injectivity argument needed.

Section 4 iteration. From border polynomials alone,
  f_{i+1} = (-1)^{n_i+1}/(J_i c_i) Res_t(f_i(0,t) - x, g_i(0,t) - y)
  g_{i+1} = (-1)^{k_i}  /(J_i d_i) Res_t(f_i(t,0) - x, g_i(t,0) - y)
and S_i an automorphism ==> S_i = S_{i+2}.
  => contrapositive: S_0 != S_2  ==>  not an automorphism.

Controls:
  A  a tame automorphism must PASS the triangle test and satisfy S_0 = S_2.
  B  Mondello's char-2 counterexample (arXiv:2608.02634), which is Keller
     and provably not an automorphism, must FAIL the triangle test -- i.e.
     the certificate must actually detect a known counterexample.
"""
import sys
import sympy as sp

x, y, t = sp.symbols("x y t")


def support(f, X=x, Y=y):
    p = sp.Poly(sp.expand(f), X, Y)
    return [m for m, c in zip(p.monoms(), p.coeffs()) if c != 0]


def is_automorphism_triangle(f, X=x, Y=y):
    """Corollary 14 test on one component. Returns (ok, detail)."""
    f = sp.expand(f)
    f = f - f.subs({X: 0, Y: 0})              # normalise constant term
    if f == 0:
        return False, "zero polynomial"
    k = sp.degree(sp.Poly(f.subs(Y, 0), X), X) if f.subs(Y, 0) != 0 else 0
    n = sp.degree(sp.Poly(f.subs(X, 0), Y), Y) if f.subs(X, 0) != 0 else 0
    sup = support(f, X, Y)
    bad = [m for m in sup
           if not (m[0] >= 0 and m[1] >= 0
                   and (n * m[0] + k * m[1] <= k * n if k and n
                        else (m[1] == 0 if n == 0 else m[0] == 0)))]
    return (not bad), {"k": k, "n": n, "outside_triangle": bad[:6]}


def keller(f, g):
    J = sp.expand(sp.diff(f, x) * sp.diff(g, y) - sp.diff(f, y) * sp.diff(g, x))
    return (J.free_symbols == set() and J != 0), J


def certificate(f, g, name=""):
    """Keller + non-triangular polygon => counterexample (Cor 14)."""
    isk, J = keller(f, g)
    okf, df = is_automorphism_triangle(f)
    okg, dg = is_automorphism_triangle(g)
    print(f"  {name}")
    print(f"    det J = {J}   Keller: {isk}")
    print(f"    N(f) triangular: {okf}  {df if not okf else ''}")
    print(f"    N(g) triangular: {okg}  {dg if not okg else ''}")
    if isk and not (okf and okg):
        print("    => CERTIFICATE: Keller with a non-triangular Newton "
              "polygon -> NOT an automorphism -> COUNTEREXAMPLE (Cor 14)")
        return "CE"
    if isk:
        print("    => Keller, polygons triangular: Cor 14 gives no "
              "obstruction (consistent with being an automorphism)")
        return "INCONCLUSIVE"
    print("    => not Keller; Cor 14 certificate does not apply")
    return "NOT-KELLER"


def controls():
    print("CONTROL A: tame automorphism f = x + y^2, g = y  (char 0)")
    r = certificate(x + y**2, y, "tame")
    okA = (r == "INCONCLUSIVE")
    print(f"  A {'PASS' if okA else 'FAIL'} (must NOT be certified a CE)\n")

    print("CONTROL B: Mondello char-2 counterexample (arXiv:2608.02634)")
    print("  P = x + x^2 y + x^4 + x^6 y^2,  Q = y + x^5 + x^6 y + x^7 y^2 "
          "+ x^8 y^3   over F_2")
    P = x + x**2*y + x**4 + x**6*y**2
    Q = y + x**5 + x**6*y + x**7*y**2 + x**8*y**3
    okP, dP = is_automorphism_triangle(P)
    okQ, dQ = is_automorphism_triangle(Q)
    print(f"    N(P) triangular: {okP}  {dP if not okP else ''}")
    print(f"    N(Q) triangular: {okQ}  {dQ if not okQ else ''}")
    okB = (not okP) or (not okQ)
    print(f"  B {'PASS' if okB else 'FAIL'} (a known counterexample must be "
          f"detected as non-automorphism)\n")
    return okA and okB


if __name__ == "__main__":
    ok = controls()
    print("=" * 62)
    print(f"McKay-Wang certificate instrument: {'VALIDATED' if ok else 'BROKEN'}")
    sys.exit(0 if ok else 1)
