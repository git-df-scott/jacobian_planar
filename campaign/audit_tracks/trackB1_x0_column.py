#!/usr/bin/env python3
"""The x^0 column of case (1): does g^{3/2} having no poles force g to be a square?

Write T := P^{1/2} (weight-graded square root; it exists because P_8 = a S^2).
The ladder forces every slice T_w to be a z-polynomial, and inductively
deg_z T_w <= 4 (numerators have degree <= 8, divided by T_4 = sqrt(a) S of
degree 4).  So

        T = sum_{i=0}^{4} x^i f_i(y),      f_i in C((1/y)),

and P = T^2 gives P^(k) = sum_{i+j=k} f_i f_j for the x^k column of P.  In
particular the x^0 column obeys

        f_0^2 = P^(0)(y),   deg P^(0) = 8,  P^(0)(0) != 0

(the i = 0 edge of N(P) runs (0,0)-(0,8), both endpoints vertices).

Now F = sqrt(gamma) T^3 has x^0 column sqrt(gamma) f_0^3, and the cascade
conditions on F say, in the x^0 column:

    Q_-1 is supported at i = 2 only (vertex (2,1))   =>  [y^-1] f_0^3 = 0
    F_w = 0 for w = -2..-9                           =>  [y^-2..-9] f_0^3 = 0

So with g := P^(0),

    ***  [y^-1] g^{3/2} = ... = [y^-9] g^{3/2} = 0  ***

is a NECESSARY condition: 9 equations on the 9 coefficients of g.  Perfect
squares g = h^2 satisfy them trivially (g^{3/2} = h^3 is a polynomial), giving
a 4-dimensional locus after scaling.  This script computes the FULL variety and
asks whether anything else survives.

If the variety is exactly the perfect squares, f_0 is a polynomial -- the first
step of the argument that T terminates, which closes case (1) (P = T^2 forces
N(P) = 2N(T), impossible since (1,0) is a vertex of N(P)).
"""
import sys, subprocess, os
import sympy as sp

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")

def conditions(nc=8, mlo=13, mhi=21):
    """[y^-m] of (1+u)^{3/2}, u = sum_{k=1..nc} c_k t^k  (t = 1/y)."""
    t = sp.symbols('t')
    c = sp.symbols(f'c1:{nc+1}')
    u = sum(c[k - 1] * t**k for k in range(1, nc + 1))
    ser = sp.series((1 + u)**sp.Rational(3, 2), t, 0, mhi + 1).removeO()
    ser = sp.expand(ser)
    eqs = []
    for m in range(mlo, mhi + 1):
        eqs.append(sp.expand(ser.coeff(t, m)))
    return c, eqs

def square_locus_check(c, eqs):
    """g = h^2 with h = y^4 + h1 y^3 + h2 y^2 + h3 y + h4  =>  c_k = coeff."""
    h = sp.symbols('h1:5')
    y = sp.symbols('y')
    H = y**4 + h[0] * y**3 + h[1] * y**2 + h[2] * y + h[3]
    G = sp.expand(H**2)
    subs = {}
    for k in range(1, 9):
        subs[c[k - 1]] = sp.expand(G.coeff(y, 8 - k))
    bad = 0
    for e in eqs:
        r = sp.simplify(sp.expand(e.subs(subs)))
        if r != 0:
            bad += 1
    return bad

def singular_variety(c, eqs, p=65521):
    def conv(e):
        e = sp.nsimplify(e)
        e = sp.together(e)
        num, den = sp.fraction(e)
        num = sp.expand(num)
        pol = sp.Poly(num, *c)
        terms = []
        for mono, coeff in zip(pol.monoms(), pol.coeffs()):
            q = sp.Rational(coeff)
            v = (int(q.p) * pow(int(q.q), p - 2, p)) % p
            if v == 0:
                continue
            s = str(v)
            for i, e2 in enumerate(mono):
                if e2:
                    s += f"*c({i+1})" + (f"^{e2}" if e2 > 1 else "")
            terms.append(s)
        return "+".join(terms) if terms else "0"
    polys = [conv(e) for e in eqs]
    src = f"""
option(redSB);
ring R = {p}, c(1..8), dp;
ideal I = {','.join(polys)};
ideal G = std(I);
if (size(G) == 1 && G[1] == 1) {{ "EMPTY"; }}
else {{ "DIM " + string(dim(G)); "DEG " + string(degree(G)); }}
// compare with the perfect-square locus: eliminate h from c = coeffs(h^2)
quit;
"""
    fn = os.path.join(SCRATCH, "x0col.sing")
    os.makedirs(SCRATCH, exist_ok=True)
    open(fn, "w").write(src)
    r = subprocess.run(["Singular", "-q", fn], capture_output=True, text=True,
                       timeout=1800)
    return r.stdout.strip()

def singular_compare(p=65521):
    """Is the variety EQUAL to the perfect-square locus?  Compute the ideal of
    the square locus by elimination and compare radicals."""
    src = f"""
option(redSB);
ring R = {p}, (h(1..4), c(1..8)), dp;
poly H = 1;
// h = y^4 + h1 y^3 + h2 y^2 + h3 y + h4 ; g = h^2 ; c_k = coeff of y^(8-k)
ideal SQ =
  c(1) - (2*h(1)),
  c(2) - (h(1)^2 + 2*h(2)),
  c(3) - (2*h(1)*h(2) + 2*h(3)),
  c(4) - (h(2)^2 + 2*h(1)*h(3) + 2*h(4)),
  c(5) - (2*h(2)*h(3) + 2*h(1)*h(4)),
  c(6) - (h(3)^2 + 2*h(2)*h(4)),
  c(7) - (2*h(3)*h(4)),
  c(8) - (h(4)^2);
ideal E = eliminate(SQ, h(1)*h(2)*h(3)*h(4));
"square locus: dim = " + string(dim(std(E))) + ", ngens = " + string(size(E));
quit;
"""
    fn = os.path.join(SCRATCH, "x0sq.sing")
    open(fn, "w").write(src)
    r = subprocess.run(["Singular", "-q", fn], capture_output=True, text=True,
                       timeout=1800)
    return r.stdout.strip()

if __name__ == "__main__":
    print("Building [y^-m] (1+u)^{3/2} for m = 13..21  (the 9 conditions)...")
    c, eqs = conditions()
    print(f"  built {len(eqs)} conditions in {len(c)} unknowns")
    bad = square_locus_check(c, eqs)
    print(f"  perfect squares g = h^2 satisfy them: "
          f"{len(eqs)-bad}/{len(eqs)} conditions vanish identically")
    print("\nSingular: the full variety of the 9 conditions")
    print("  " + singular_variety(c, eqs).replace("\n", "\n  "))
    print("\nSingular: the perfect-square locus for comparison")
    print("  " + singular_compare().replace("\n", "\n  "))
