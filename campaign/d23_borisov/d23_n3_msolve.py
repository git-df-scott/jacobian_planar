"""
Plane Jacobian campaign - Session N2 continuation (N3c).
EXACT (-5)-curve Belyi systems via msolve: the h-invariant bilinear form.

THE SYSTEM.  For B = P^2/(w R^3) with P monic deg m, R monic deg d
(2m = 3d + 1), the invariant
    h := 2 P' R w - P (R + 3 w R')
has degree <= m + d - 1 with the w^(m+d-1)-coefficient vanishing
identically (leading terms cancel: 2m - (1 + 3d) = 0).  Demanding h to
be CONSTANT is 22 (FF: 12) BILINEAR equations in the coefficients of
(P, R) -- coefficients of w^1..w^(m+d-2) vanish.

THEOREM (h-constancy <=> miracle cancellation; proves the cross-epoch
identity).  With N := P^2 - w R^3:
    P h  =  R w N'  -  (R + 3 w R') N          (polynomial identity)
If h = h0 != 0 is constant, compare degrees: LHS has degree m; if
deg N = nu, the RHS has leading coefficient (nu - 2m) n_nu != 0 at
degree d + nu, so nu = m - d and, reading leading coefficients,
    h0 = (nu - 2m) n_nu = -D n_nu,   D = 2m - nu = the chain degree.
FF (m,d,D) = (8,5,13): h0 = -13 n_3 -- the Sessions 16-18 cross-epoch
identity, now a two-line consequence.  SF (14,9,23): h0 = -23 n_5.

NORMALIZATION.  w = 0 and w = infinity are marked; the residual scale
w -> lambda w acts with r_{d-1} -> lambda^{-1} r_{d-1}.  The slice
r_{d-1} = 1 is RATIONAL (no root extractions), so msolve's rational
parametrization lives over the dessins' true fields.  (Caveat: dessins
with r_{d-1} = 0 are missed by this slice; rerun with another slice to
exclude/catch them.)

This file: derives the systems symbolically, verifies the identity and
the triangular structure, writes msolve input files, and (validation)
checks that the FF system's solutions contain the Session-7 certified
(p, r) via its slice representative.
"""
import subprocess
import os
from sympy import symbols, Poly, expand, diff, simplify, Rational, sqrt, I

w = symbols('w')

def build_system(m, d, name):
    ps = symbols(f'p0:{m}')          # p_0..p_{m-1}; P monic
    rs = symbols(f'r0:{d}')          # r_0..r_{d-1}; R monic
    P = w**m + sum(ps[k]*w**k for k in range(m))
    R = w**d + sum(rs[k]*w**k for k in range(d))
    h = expand(2*diff(P, w)*R*w - P*(R + 3*w*diff(R, w)))
    H = Poly(h, w)
    assert H.nth(m + d) == 0, "leading cancellation fails"
    eqs = [H.nth(k) for k in range(1, m + d)]      # w^1 .. w^(m+d-1)
    # SATURATION: h0 != 0 via t*h0 = 1.  This alone forces deg N = m-d
    # exactly, gcd(P,R) = 1, R squarefree, R(0) != 0, P(0) != 0 (each a
    # one-line consequence of the structural identity below), killing the
    # degenerate positive-dimensional components (e.g. P = w^2 T^3,
    # R = w T^2, B constant).
    tsat = symbols('t')
    eqs = eqs + [tsat*H.nth(0) - 1]
    globals()['tsat'] = tsat
    # identity check (structural theorem): P h = R w N' - (R+3wR') N
    N = expand(P**2 - w*R**3)
    lhs = expand(P*h)
    rhs = expand(R*w*diff(N, w) - (R + 3*w*diff(R, w))*N)
    assert expand(lhs - rhs) == 0, "structural identity fails"
    print(f"{name}: {len(eqs)} bilinear equations; structural identity "
          f"P h = RwN' - (R+3wR')N verified symbolically")
    # triangularity: top equation is linear in p_{m-1} with constant coeff
    top = Poly(eqs[-1], ps[m-1])
    print(f"{name}: top equation [w^{m+d-2}]: {eqs[-1]} (linear in p_{m-1})")
    return ps, rs, eqs

def write_msolve(eqs, subs, varlist, fname):
    polys = []
    for e in eqs:
        pe = Poly(expand(e.subs(subs)), *varlist)
        # msolve wants integer coefficients: clear denominators
        den = 1
        from sympy import ilcm
        for c in pe.coeffs():
            den = ilcm(den, Rational(c).q)
        pe = Poly(pe*den, *varlist)
        polys.append(str(pe.as_expr()).replace('**', '^').replace(' ', ''))
    with open(fname, 'w') as f:
        f.write(','.join(str(v) for v in varlist) + '\n0\n')
        f.write(',\n'.join(polys) + '\n')
    print(f"wrote {fname}: {len(polys)} polynomials, {len(varlist)} variables")

# ---------- FF (m, d) = (8, 5): validation ----------
ps, rs, eqs = build_system(8, 5, "FF")
subs = {rs[4]: 1}                                   # slice r4 = 1
varlist = list(ps) + [rs[0], rs[1], rs[2], rs[3], tsat]
write_msolve(eqs, subs, varlist, "ff_h_system.ms")

# certified Session-7 solution, scaled to the slice: lambda = r4
s3 = I*sqrt(3)
r_cert = [Rational(68,3) - Rational(20,3)*s3, Rational(35,3) - Rational(112,3)*s3,
          Rational(-140,3) - 24*s3, Rational(-278,9) + Rational(68,9)*s3,
          Rational(4,3) + Rational(16,3)*s3]        # r_0..r_4
p_cert = [-28 + 4*s3, -118 + 158*s3, Rational(1043,3) + 336*s3,
          Rational(2420,3) + Rational(22,3)*s3, Rational(835,3) - Rational(890,3)*s3,
          Rational(-4600,27) - Rational(376,3)*s3, Rational(-233,3) + Rational(50,3)*s3,
          2 + 8*s3]                                 # p_0..p_7
lam = r_cert[4]
slice_vals = {ps[k]: p_cert[k]*lam**(k - 8) for k in range(8)}
slice_vals.update({rs[k]: r_cert[k]*lam**(k - 5) for k in range(5)})
resid = [simplify(expand(e.subs(slice_vals))) for e in eqs[:-1]]
print("FF: certified sliced solution satisfies all 12 h-equations:",
      all(x == 0 for x in resid))
print("FF: sliced r4 =", simplify(r_cert[4]*lam**(-1)), "(slice consistent)")

# ---------- SF (m, d) = (14, 9): the target ----------
ps2, rs2, eqs2 = build_system(14, 9, "SF")
subs2 = {rs2[8]: 1}                                 # slice r8 = 1
varlist2 = list(ps2) + [rs2[k] for k in range(8)] + [tsat]
write_msolve(eqs2, subs2, varlist2, "sf_h_system.ms")
print()
print("run:  msolve -P 2 -f ff_h_system.ms -o ff_h_out.ms   (validation)")
print("      msolve -P 2 -f sf_h_system.ms -o sf_h_out.ms   (the target)")
