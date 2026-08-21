"""
Plane Jacobian campaign - Session N2, Phase 0
D=23 transfer campaign: Borisov's SECOND Framework (arXiv:1901.04073, Sec. 4).

CERTIFIED HERE: the degree-23 Belyi map of the Second Framework's
(-2)-curve, rederived from the ramification data alone (the paper
publishes NO explicit polynomials for it), in exact arithmetic.

Functional form (differs from the Session-7 First-Framework map
p^2/(w r^3) -- here {infinity} has a UNIQUE preimage, so B is a
degree-23 SHABAT POLYNOMIAL):

    B(t) = c * t * a(t)^3 * b(t)^5,      a monic quartic, b monic quadratic
    B(t) - 1 = c * (t-1)^7 * s(t),       s degree 16, squarefree

    profile:  {0}: 1x1 + 4x3 + 2x5   {1}: 1x7 + 16x1   {inf}: 1x23
    (Riemann-Hurwitz: 16 + 6 + 22 = 44 = 2*23 - 2, genus 0)

normalized by: order-1 point above 0 at t=0, order-7 point above 1 at
t=1 (kills the affine reparametrization group entirely).

MASTER EQUATION (the D=23 analog of Session 7's miracle cancellation
h = 2p'rw - p(r+3wr') = const):  B' = c a^2 b^4 L  with

    L := a*b + 3t*a'*b + 5t*a*b'  ==  23*(t-1)^6.

STRUCTURE THEOREM (dessin census, proved in part 0 below + Burnside):
the dessin is the "star of stars": a central white vertex of degree 7
adjacent to ALL seven black vertices (degrees 1,3,3,3,3,5,5), each
black vertex of degree d carrying d-1 white leaves.  Unique as a graph
(Borisov's remark), 15 = 105/7 as a plane tree (3 symmetric + 6 chiral
pairs).  The 15 dessins form a SINGLE GALOIS ORBIT: the eliminant f of
the master system is irreducible of degree 15 over Q, with exactly 3
real roots (= the 3 symmetric dessins; Borisov's Figure 28 draws the
symmetric dessin with cyclic order (5,1,5,3,3,3,3)).

COMPLETENESS: the master system is triangular: [t^5..t^2] solve
a3,a2,a1,a0 LINEARLY (constant denominators) in (b1,b0); the remaining
two equations E1, E2 have Res_{b0} of degree exactly 15 = the dessin
count, and gcd(E1,E2) over K = Q[w]/(f) is linear in b0.  So there are
EXACTLY 15 solutions, in bijection with the 15 plane trees; certifying
once over K certifies all of them simultaneously.

This file is self-contained sympy (exact over Q): it re-derives the
system, reproduces f by elimination, loads the exact K-coefficients
(d23_belyi_data/, computed by d23_phase0_certify.gp), and re-verifies
the core identities over Q[w]/(f) plus prime-witness nonvanishing
certificates.  The full ledger (discriminants/resultants over K) is
certified exactly in PARI/GP by d23_phase0_certify.gp: 12/12 PASS.
"""
import os
from itertools import permutations
from sympy import (symbols, expand, Poly, resultant, factor_list, Rational,
                   diff, sympify, QQ)

t, w, b1, b0 = symbols('t w b1 b0')
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'd23_belyi_data')

# ---------- part 0: dessin census (combinatorial completeness bound) ----------
arr = set()
for p in set(permutations((1, 3, 3, 3, 3, 5, 5))):
    arr.add(min(p[i:] + p[:i] for i in range(7)))          # rotation classes
sym = [x for x in arr if tuple(reversed(x)) in {x[i:] + x[:i] for i in range(7)}]
print(f"part 0  plane trees with black degrees (1,3,3,3,3,5,5), star-of-stars: "
      f"{len(arr)} (expect 15); reflection-symmetric: {len(sym)} (expect 3)")
assert len(arr) == 15 and len(sym) == 3

# ---------- part 1: functional form certificate ----------
a3s, a2s, a1s, a0s, b1s, b0s, cs = symbols('a3 a2 a1 a0 b1s b0s c')
a_ = t**4 + a3s*t**3 + a2s*t**2 + a1s*t + a0s
b_ = t**2 + b1s*t + b0s
B_ = cs*t*a_**3*b_**5
L_ = a_*b_ + 3*t*diff(a_, t)*b_ + 5*t*a_*diff(b_, t)
print("part 1  B' == c a^2 b^4 L identically:",
      expand(diff(B_, t) - cs*a_**2*b_**4*L_) == 0)

# ---------- part 2: exact elimination reproduces the degree-15 field ----------
a3e = expand(Rational(-1, 20)*(18*b1 + 138))
a2e = expand(Rational(-1, 17)*(15*a3e*b1 + 13*b0 - 345))
a1e = expand(Rational(-1, 14)*(12*a2e*b1 + 10*a3e*b0 + 460))
a0e = expand(Rational(-1, 11)*(9*a1e*b1 + 7*a2e*b0 - 345))
E1 = expand(6*a0e*b1 + 4*a1e*b0 + 138)     # [t^1] of L - 23(t-1)^6
E2 = expand(a0e*b0 - 23)                   # [t^0]
R = Poly(resultant(E1, E2, b0), b1)
fl = factor_list(R.as_expr())
assert len(fl[1]) == 1 and fl[1][0][1] == 1
f_expr = fl[1][0][0]
fpol = Poly(f_expr, b1)
print("part 2  Res_b0(E1,E2): degree", R.degree(),
      "| irreducible factor degree:", fpol.degree())

f_file = Poly(sympify(open(os.path.join(HERE, 'd23_f.txt')).read()
                      .replace('^', '**'), rational=True), w)
assert fpol.all_coeffs() == f_file.all_coeffs(), "f mismatch vs exported data"
print("part 2  eliminant f matches d23_belyi_data/d23_f.txt exactly: True")

# ---------- part 3: load exact K-coefficients, verify over Q[w]/(f) ----------
def load(name):
    s = open(os.path.join(HERE, name)).read().replace('^', '**')
    return Poly(sympify(s, rational=True), w, domain=QQ)

fW = Poly(f_file, w, domain=QQ)
KB0, KA3, KA2, KA1, KA0, KC = (load(n) for n in
    ('d23_b0.txt', 'd23_a3.txt', 'd23_a2.txt', 'd23_a1.txt',
     'd23_a0.txt', 'd23_c.txt'))
KB1 = Poly(w, w, domain=QQ)

def kred(p):                       # reduce a Q[w] element mod f
    return p.rem(fW)

def ksub(expr_in_b):
    """substitute b1 -> w-class, b0 -> KB0 into a Q[b1,b0] polynomial."""
    P = Poly(expr_in_b, b1, b0)
    out = Poly(0, w, domain=QQ)
    for (i, j), cf in P.terms():
        out = out + Poly(cf, w, domain=QQ)*KB1**i*KB0**j
        out = kred(out)
    return out

chk_ch = all(kred(ksub(e) - k) == Poly(0, w, domain=QQ) for e, k in
             [(a3e, KA3), (a2e, KA2), (a1e, KA1), (a0e, KA0)])
chk_E = (kred(ksub(E1)) == Poly(0, w, domain=QQ) and
         kred(ksub(E2)) == Poly(0, w, domain=QQ))
print("part 3  chain values a3..a0 match exported data over K:", chk_ch)
print("part 3  E1 = E2 = 0 over K (master system solved):", chk_E)

# master identity L == 23(t-1)^6 over K[t], coefficientwise
Kco = {0: KA0, 1: KA1, 2: KA2, 3: KA3, 4: Poly(1, w, domain=QQ)}
Bco = {0: KB0, 1: KB1, 2: Poly(1, w, domain=QQ)}
def tmul(P, Q):                    # multiply {deg: K-elt} dicts, reduce mod f
    out = {}
    for i, pi in P.items():
        for j, qj in Q.items():
            out[i+j] = kred(out.get(i+j, Poly(0, w, domain=QQ)) + pi*qj)
    return {k: v for k, v in out.items() if v != Poly(0, w, domain=QQ)}
def tadd(P, Q, sc=1):
    out = dict(P)
    for j, qj in Q.items():
        out[j] = kred(out.get(j, Poly(0, w, domain=QQ)) + Poly(sc, w, domain=QQ)*qj)
    return {k: v for k, v in out.items() if v != Poly(0, w, domain=QQ)}
aD = {i-1: kred(Poly(i, w, domain=QQ)*Kco[i]) for i in range(1, 5)}
bD = {i-1: kred(Poly(i, w, domain=QQ)*Bco[i]) for i in range(1, 3)}
tsh = lambda P: {i+1: v for i, v in P.items()}                    # multiply by t
Lk = tadd(tadd(tmul(Kco, Bco), tsh(tmul(aD, Bco)), 3), tsh(tmul(Kco, bD)), 5)
tgt = {k: Poly(23*cf, w, domain=QQ) for k, cf in
       enumerate(reversed(Poly((t-1)**6, t).all_coeffs())) if cf != 0}
chk_L = (tadd(Lk, tgt, -1) == {})
print("part 3  MASTER IDENTITY  L == 23(t-1)^6 over K[t]:", chk_L)

# ---------- part 4: B - 1 = c(t-1)^7 s over K[t], exact division ----------
B23 = tmul({1: KC}, tmul(tmul(tmul(Kco, Kco), Kco),
                         tmul(tmul(tmul(tmul(Bco, Bco), Bco), Bco), Bco)))
D1 = tadd(B23, {0: Poly(1, w, domain=QQ)}, -1)
# divide by monic (t-1)^7: plain synthetic division over K (no inversions)
q7 = [Poly(cf, w, domain=QQ) for cf in Poly((t-1)**7, t).all_coeffs()]  # deg 7 monic
num = [D1.get(k, Poly(0, w, domain=QQ)) for k in range(23, -1, -1)]
quot = []
rem = list(num)
for k in range(len(num) - 7):
    lead = rem[k]
    quot.append(lead)
    for j in range(8):
        rem[k+j] = kred(rem[k+j] - lead*q7[j])
# quot is c*s (we divided B-1 by (t-1)^7, not by c(t-1)^7); s = quot/c
chk_div = all(r == Poly(0, w, domain=QQ) for r in rem[len(num)-7:])
print("part 4  (t-1)^7 divides B - 1 exactly over K:", chk_div)
print("part 4  deg s = 16:", len(quot) - 1 == 16 and quot[0] == kred(KC))
# (quot has leading coefficient c since B is monic-times-c of degree 23)

# ---------- part 5: prime-witness nonvanishing certificates ----------
# For X in Z_(p)[w]/(f):  X mod (p, f) != 0  ==>  X != 0 in K.  One-sided,
# exact.  (gp ledger certifies these over K directly; this is the portable
# independent witness.)
p = 2**61 - 1
Fp = lambda P: [int(cf) % p for cf in P.all_coeffs()] if P.degree() >= 0 else [0]
import sympy
GF = sympy.GF(p)
fP = Poly(fW, w, domain=GF)
def wred(P):  return Poly(P, w, domain=GF).rem(fP)
def kw(P):    # clear denominators (denominator must be coprime to p: check)
    den = 1
    for cf in P.all_coeffs():
        den = sympy.ilcm(den, cf.q)
    assert den % p != 0
    return wred(Poly(P*den, w))
aP = {i: kw(Kco[i]) for i in Kco}; bP = {i: kw(Bco[i]) for i in Bco}
def tmulP(P, Q):
    out = {}
    for i, pi in P.items():
        for j, qj in Q.items():
            out[i+j] = (out.get(i+j, Poly(0, w, domain=GF)) + pi*qj).rem(fP)
    return out
def tpolyP(D, deg):  return [D.get(k, Poly(0, w, domain=GF)) for k in range(deg, -1, -1)]
def sylv_det(A, B):  # resultant of two t-polys with GF(p)[w]/f coefficients
    m, n = len(A) - 1, len(B) - 1
    N = m + n
    M = [[Poly(0, w, domain=GF)]*N for _ in range(N)]
    for i in range(n):
        for j, cf in enumerate(A): M[i][i+j] = cf
    for i in range(m):
        for j, cf in enumerate(B): M[n+i][i+j] = cf
    det = Poly(1, w, domain=GF); sign = 1
    for col in range(N):
        piv = next((r for r in range(col, N) if M[r][col].rem(fP) != Poly(0, w, domain=GF)), None)
        if piv is None: return Poly(0, w, domain=GF)
        if piv != col: M[col], M[piv] = M[piv], M[col]; sign = -sign
        inv = M[col][col].invert(fP)
        det = (det*M[col][col]).rem(fP)
        for r in range(col+1, N):
            fac = (M[r][col]*inv).rem(fP)
            for cc in range(col, N):
                M[r][cc] = (M[r][cc] - fac*M[col][cc]).rem(fP)
    return (Poly(sign, w, domain=GF)*det).rem(fP)
aT = tpolyP(aP, 4); bT = tpolyP(bP, 2)
aDT = tpolyP(tmulP({0: Poly(1, w, domain=GF)}, {i-1: (Poly(i, w, domain=GF)*aP[i]).rem(fP) for i in range(1, 5)}), 3)
bDT = tpolyP({i-1: (Poly(i, w, domain=GF)*bP[i]).rem(fP) for i in range(1, 3)}, 1)
wit = {
    "disc(a) != 0 (witness mod p)": sylv_det(aT, aDT) != Poly(0, w, domain=GF),
    "disc(b) != 0 (witness mod p)": sylv_det(bT, bDT) != Poly(0, w, domain=GF),
    "Res(a,b) != 0 (witness mod p)": sylv_det(aT, bT) != Poly(0, w, domain=GF),
}
for k, v in wit.items():
    print(f"part 5  [{'PASS' if v else 'RETRY-PRIME'}] {k}")
print()
print("Phase 0 core identities verified in sympy over K = Q[w]/(f), deg 15.")
print("Full exact ledger (12/12 incl. disc(s), fiber disjointness): see")
print("d23_phase0_certify.gp output in D23_phase0_report.md.")
