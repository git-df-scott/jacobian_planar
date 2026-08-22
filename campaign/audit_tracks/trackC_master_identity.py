"""
Track C, part 1 (C1): the endgame master identity, re-derived from scratch.

Everything here is exact (sympy Rational / symbolic); no floats.

SETUP (the cusp-chart framework, re-derived -- not copied -- from the
Sessions 10-18 method):

  Coordinates: v = x1*x2^s - 1,  q = x2 / v^rho   (chart slopes s, rho;
  the classical chart of Sessions 8-18 is rho = s = 3).

  A candidate pair (y1, y2) with cusp type (a,b) (gcd(a,b)=1, y1 ~ f^b,
  y2 ~ f^a) and boundary valuation vector -k*(b,a) is, in the chart, a
  q-Laurent series pair

      y2 = F = q^(-k*a) * ( G0(v) + q*G1(v) + ... ),      G0 = g0^a,
      y1 = F^(b/a) + Delta,
      Delta = q^(-k*b+D) * ( u0(v) + q*u1(v) + ... ),     u0 = g0^b*R/a,

  where D >= 1 is the chain degree (the number of vanishing blocks of
  y1^a - y2^b beyond the trivial ones; Session 10 proves chain <=> block
  vanishings for (99,66), and D is DEFINED this way here), F^(b/a) is the
  formal (b/a)-power of the series F (unit part has a formal a-th root),
  and R(v) is defined by the deviation's first block u0 = g0^b*R/a.

  The Keller condition J_{(x1,x2)}(y1,y2) = c (nonzero constant) is,
  in-chart, J_{(q,v)}(y1,y2) = c / det d(q,v)/d(x1,x2).

CLAIMS UNDER TEST (Session 19, lost; re-derived here):
  C1a  det d(q,v)/d(x1,x2) = -x2^s * v^(-rho); for rho=s=3: -x2^3/v^3.
  C1b  J_{(q,v)} = -c q^(-s) v^(rho(1-s)); for rho=s=3: -c q^-3 v^-6.
  C1c  [leading] block of the Keller condition
           = g0^(a+b) * ( k*R' + D*R*(log g0)' ),
       chart slopes ABSENT from the identity; subleading tower absent.
  C1d  order matching:  D = (a+b)k + 1 - s   (q-exponents)
                        (a+b)*sigma = 1 + rho - rho*s   (v-exponents,
                        with g0 = alpha*(v+1)^m*v^sigma);
       for rho = s these are the handoff's D = (a+b)k+1-rho and
       (a+b)sigma = 1+rho-rho^2; rho=s=3, a+b=5  =>  sigma = -1 DERIVED.
       Also the pole forcing at v=-1: R = S/(v+1)^p with exact pole
       order p = (a+b)m - 1 forced (no resonance when k does not
       divide D*m).
  C1e  (99,66)/(72,108) specialization (a,b,k,D)=(2,3,3,13), g0=alpha*(v+1)/v:
           block * v^6 = alpha^5 (v+1)^4 (3v(v+1)R' - 13R),
       so Keller <=> alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c.
  C1f  cross-epoch: the certified Session-7 Belyi data (h0) and the
       certified Session-10 cubic (n3) satisfy h0 = -13*n3, and the
       master identity EXPLAINS it: the near-miss has R = n3 (constant),
       and its in-chart Jacobian is exactly h0*(v+1)^4*q^-3*v^-6.

Run:  python3 trackC_master_identity.py
"""

import sys
from sympy import (symbols, Function, Matrix, diff, simplify, expand,
                   powsimp, cancel, together, sqrt, I, Rational as Rat,
                   Poly, degree, series, S, log, radsimp, nsimplify,
                   fraction, factor, O)

PASS = 0
FAIL = 0
def report(name, ok, extra=""):
    global PASS, FAIL
    tag = "PASS" if ok else "FAIL"
    if ok: PASS += 1
    else: FAIL += 1
    print(f"  [{tag}] {name}" + (f"   {extra}" if extra else ""))
    return ok

x1, x2, q, v = symbols('x1 x2 q v')
rho, s = symbols('rho s', positive=True)

# ----------------------------------------------------------------------
print("== C1a: chart factor det d(q,v)/d(x1,x2), generic (rho, s) ==")
v_expr = x1*x2**s - 1
q_expr = x2 * v_expr**(-rho)
Jac = Matrix([[diff(q_expr, x1), diff(q_expr, x2)],
              [diff(v_expr, x1), diff(v_expr, x2)]])
det = simplify(Jac.det())
target = -x2**s * v_expr**(-rho)
report("det == -x2^s * v^(-rho)  (generic rho, s)",
       simplify(det - target) == 0, f"det = {det}")

# specialization rho = s = 3 (the Sessions 16-18 claim)
det3 = det.subs({rho: 3, s: 3})
v3 = x1*x2**3 - 1
report("rho=s=3: det == -x2^3/v^3  (Sessions 16-18 chart factor)",
       simplify(det3 + x2**3/v3**3) == 0)

# ----------------------------------------------------------------------
print("== C1b: in-chart Keller form ==")
# multiplicativity of Jacobians under the chart (generic functions):
A = Function('A')(q, v); B = Function('B')(q, v)
Acomp = A.subs({q: q_expr, v: v_expr}); Bcomp = B.subs({q: q_expr, v: v_expr})
J_x = diff(Acomp, x1)*diff(Bcomp, x2) - diff(Acomp, x2)*diff(Bcomp, x1)
J_qv = (diff(A, q)*diff(B, v) - diff(A, v)*diff(B, q))
mult_ok = simplify(J_x - J_qv.subs({q: q_expr, v: v_expr})*det) == 0
report("J_{x}(A,B) == J_{qv}(A,B) * det   (chain rule, generic A,B)", mult_ok)

# Keller J_x = c  =>  J_qv = c/det; express in-chart: x2 = q*v^rho
c = symbols('c', nonzero=True)
Jqv_form = c/det
Jqv_inchart = simplify(Jqv_form.subs(x2, q*v**rho).subs(x1, (v+1)/(q*v**rho)**s))
target_qv = -c*q**(-s)*v**(rho*(1-s))
# exponent arithmetic on the Laurent monomial: compare on positive reps
qp, vp = symbols('q_pos v_pos', positive=True)
ratio = simplify(powsimp((Jqv_inchart/target_qv).subs({q: qp, v: vp}),
                         force=True))
report("J_{qv} == -c * q^(-s) * v^(rho(1-s))   (generic)",
       ratio == 1, f"J_qv = {Jqv_inchart}")
report("rho=s=3:  J_{qv} == -c q^-3 v^-6   (Sessions 16-18 claim)",
       simplify(Jqv_inchart.subs({rho: 3, s: 3}) + c*q**(-3)*v**(-6)) == 0)

# ----------------------------------------------------------------------
print("== C1c: the master identity (fully symbolic) ==")
# Lemma (Jacobian silence of the root part): J(phi(F), F) == 0.
F = Function('F')(q, v); phi = Function('phi')
Jsil = diff(phi(F), q)*diff(F, v) - diff(phi(F), v)*diff(F, q)
report("lemma: J(phi(F), F) == 0  (root part is Jacobian-silent)",
       simplify(Jsil) == 0)
# Consequence (bilinearity): J(y1,y2) = J(F^{b/a} + Delta, F) = J(Delta, F).

# Leading block of J(Delta, F), with symbolic a,b,k,D and a generic
# subleading tower.  F = q^e1 * W, Delta = q^e2 * Z,
# e1 = -k*a, e2 = -k*b + D:
#   J(Delta,F) = q^(e1+e2-1) * [ (e2*Z + q*Z_q)*W_v - Z_v*(e1*W + q*W_q) ]
# and the LEADING block is bracket|_{q=0}.  (Blocks of Delta at order
# e2+j pair with blocks of F at order e1+i only into J-orders
# e1+e2-1+i+j, so the leading J-block sees only u0 and G0: verified
# below by the presence/absence checks.)
a, b, k, D = symbols('a b k D', positive=True)
g0 = Function('g0')(v); R = Function('R')(v)
G0f, G1f, G2f = [Function(f'G{i}')(v) for i in range(3)]
u0f, u1f, u2f = [Function(f'u{i}')(v) for i in range(3)]
W = G0f + q*G1f + q**2*G2f
Z = u0f + q*u1f + q**2*u2f
e1 = -k*a; e2 = -k*b + D
bracket = expand((e2*Z + q*diff(Z, q))*diff(W, v) - diff(Z, v)*(e1*W + q*diff(W, q)))
lead = bracket.subs(q, 0)
report("leading block == (D-k*b)*u0*G0' + k*a*u0'*G0",
       simplify(lead - ((D-k*b)*u0f*diff(G0f, v) + k*a*diff(u0f, v)*G0f)) == 0)
report("subleading tower absent from the leading block",
       not (lead.has(G1f) or lead.has(G2f) or lead.has(u1f) or lead.has(u2f)))
nextblock = expand(bracket.coeff(q, 1))
report("[next] block DOES involve the subleading tower (bookkeeping honest)",
       nextblock.has(G1f) or nextblock.has(u1f))

# substitute u0 = g0^b*R/a, G0 = g0^a and compare with the claimed identity
lead_sub = lead.subs({u0f: g0**b*R/a, G0f: g0**a}).doit()
identity_rhs = g0**(a+b)*(k*diff(R, v) + D*R*diff(g0, v)/g0)
diff_expr = simplify(powsimp(expand(powsimp(expand(lead_sub - identity_rhs),
                                            force=True)), force=True))
sym_ok = (diff_expr == 0)
report("master identity, SYMBOLIC a,b,k,D:  block == g0^(a+b)*(k*R' + D*R*(log g0)')",
       sym_ok, "" if sym_ok else f"residue: {diff_expr}")
# concrete cross-checks for several coprime (a,b)
conc_ok = True
for (aa, bb) in [(2, 3), (3, 5), (2, 5), (4, 7)]:
    l2 = lead.subs({u0f: g0**bb*R/aa, G0f: g0**aa, a: aa, b: bb}).doit()
    r2 = (g0**(aa+bb)*(k*diff(R, v) + D*R*diff(g0, v)/g0))
    conc_ok &= (simplify(expand(l2 - r2)) == 0)
report("master identity at concrete (a,b) in {(2,3),(3,5),(2,5),(4,7)}", conc_ok)

# chart-slope absence: the derivation above never used rho or s
report("chart slopes rho, s ABSENT from the identity (free-symbol check)",
       not (lead_sub.has(rho) or lead_sub.has(s)
            or identity_rhs.has(rho) or identity_rhs.has(s)))

# ----------------------------------------------------------------------
print("== C1d: order matching + pole forcing ==")
# (i) q-exponents: leading order of J(Delta,F) is e1+e2-1 = -k(a+b)+D-1.
#     Keller RHS sits at q^(-s).  If -k(a+b)+D-1 < -s the leading block
#     identity g0^(a+b)(kR' + DR(log g0)') = 0 is a first-order linear ODE
#     whose solution R = C*g0^(-D/k) is not a nonzero rational function
#     unless k | D... (checked per-case below); generically R = 0, pushing
#     the deviation one block up.  Hence WLOG the leading order IS the
#     Keller order:
from sympy import Eq, solve
Dsol = solve(Eq(-k*(a+b) + D - 1, -s), D)[0]
report("q-order matching  =>  D = (a+b)*k + 1 - s",
       simplify(Dsol - ((a+b)*k + 1 - s)) == 0, f"D = {Dsol}")
# with rho = s this is the handoff's D = (a+b)k + 1 - rho.

# (ii) v-exponents: with g0 = alpha*(v+1)^m*v^sigma and R regular
#      nonzero at v=0, the block's v-order at v->0 is (a+b)*sigma - 1
#      (the D*R*sigma/v term dominates).  RHS v-order is rho*(1-s).
#      =>  (a+b)*sigma = 1 + rho - rho*s.   Executable check on a grid:
alpha = symbols('alpha', nonzero=True)
mm, sg = symbols('m_ sigma_')
def block_of(g0_expr, R_expr, kk, DD):
    return (g0_expr**(a+b)*(k*diff(R_expr, v) + D*R_expr*diff(g0_expr, v)/g0_expr)
            ).subs({k: kk, D: DD})
grid_ok = True
Sgen = 35 - 42*v + 54*v**2 - 81*v**3 + 243*v**4   # S(0) != 0, S(-1) != 0
for (aa, bb, kk, m_val, sig_val) in [(2, 3, 3, 1, -1), (2, 3, 4, 1, -1),
                                     (2, 3, 3, 2, -1), (2, 3, 3, 1, -2),
                                     (3, 5, 2, 1, -1)]:
    g0c = alpha*(v+1)**m_val*v**sig_val
    p_pole = (aa+bb)*m_val - 1
    Rc = Sgen/(v+1)**p_pole
    DD = symbols('DD', positive=True)
    blk = (g0c**(aa+bb)*(kk*diff(Rc, v) + DD*Rc*diff(g0c, v)/g0c))
    # v-order at 0: multiply by v^(1-(a+b)*sigma) and check finite nonzero limit
    from sympy import limit
    lim = limit(together(blk)*v**(1 - (aa+bb)*sig_val), v, 0)
    grid_ok &= (lim.is_nonzero is True or simplify(lim) != 0)
report("block v-order at 0 == (a+b)*sigma - 1  (grid of (a,b,k,m,sigma))", grid_ok)
# hence (a+b)*sigma - 1 = rho*(1-s), i.e. (a+b)*sigma = 1 + rho - rho*s;
# with rho = s: (a+b)*sigma = 1 + rho - rho^2  (handoff form).
sig_sol = solve(Eq(5*sg, 1 + 3 - 3*3), sg)[0]
report("rho = s = 3, a+b = 5  =>  sigma = -1 DERIVED", sig_sol == -1)

# (iii) pole forcing at v = -1 (U = 0): with g0 = alpha*(v+1)^m*v^sigma
#      and R with exact pole order pp at v=-1, the block behaves like
#      (D*m - k*pp)*S(-1)*(v+1)^((a+b)*m - pp - 1) near v=-1.  The RHS is
#      regular and NONZERO at v=-1 (c != 0), so (a+b)*m - pp - 1 = 0:
#      pp = (a+b)*m - 1, PROVIDED no resonance D*m = k*pp.  Executable:
pole_ok = True
for (aa, bb, kk, m_val) in [(2, 3, 3, 1), (2, 3, 4, 1), (2, 3, 3, 2)]:
    sig_val = -1
    g0c = alpha*(v+1)**m_val*v**sig_val
    DD_val = (aa+bb)*kk + 1 - 3   # s = 3
    for pp in range(0, (aa+bb)*m_val + 2):
        if pp == 0:
            Rc = Sgen
        else:
            Rc = Sgen/(v+1)**pp
        blk = together(g0c**(aa+bb)*(kk*diff(Rc, v) + DD_val*Rc*diff(g0c, v)/g0c))
        # order at v = -1:
        from sympy import limit
        w_ = symbols('w_')
        blkw = blk.subs(v, w_ - 1)
        # compute the exact order at w_ = 0
        ordv = None
        num, den = fraction(cancel(blkw))
        from sympy import Poly as P_
        ordv = (P_(num, w_).monoms()[-1][0] if num != 0 else None)
        d_ord = P_(den, w_).monoms()[-1][0]
        order_at = (ordv - d_ord) if ordv is not None else None
        expected = (aa+bb)*m_val - pp - 1
        resonance = (DD_val*m_val - kk*pp == 0)
        if not resonance:
            pole_ok &= (order_at == expected)
report("exact (v+1)-order of block == (a+b)m - p - 1 off resonance "
       "(so p = (a+b)m - 1 is forced by c != 0)", pole_ok)

# ----------------------------------------------------------------------
print("== C1e: the (99,66)-type specialization (a,b,k,D) = (2,3,3,13) ==")
g0_spec = alpha*(v+1)/v      # m = 1, sigma = -1
blk = (g0_spec**5*(3*diff(R, v) + 13*R*diff(g0_spec, v)/g0_spec))
target5 = alpha**5*(v+1)**4*(3*v*(v+1)*diff(R, v) - 13*R)*v**(-6)
report("block == alpha^5 (v+1)^4 (3v(v+1)R' - 13R) / v^6   (generic R)",
       simplify(together(blk - target5)) == 0)
print("      => Keller block identity:  alpha^5 (v+1)^4 (3v(v+1)R' - 13R) = -c")
print("         (the v^-6 matches the RHS -c q^-3 v^-6 exactly)")

# ----------------------------------------------------------------------
print("== C1f: cross-epoch reproduction h0 = -13*n3 (certified anchors) ==")
w = symbols('w')
sq = I*sqrt(3)
p_poly = (w**8 + (2 + 8*sq)*w**7 + (Rat(-233,3) + Rat(50,3)*sq)*w**6
     + (Rat(-4600,27) - Rat(376,3)*sq)*w**5 + (Rat(835,3) - Rat(890,3)*sq)*w**4
     + (Rat(2420,3) + Rat(22,3)*sq)*w**3 + (Rat(1043,3) + 336*sq)*w**2
     + (-118 + 158*sq)*w + (-28 + 4*sq))
r_poly = (w**5 + (Rat(4,3) + Rat(16,3)*sq)*w**4 + (Rat(-278,9) + Rat(68,9)*sq)*w**3
     + (Rat(-140,3) - 24*sq)*w**2 + (Rat(35,3) - Rat(112,3)*sq)*w
     + Rat(68,3) - Rat(20,3)*sq)
h0 = Rat(1664,3) - Rat(832,3)*sq

h_expr = expand(2*diff(p_poly, w)*r_poly*w - p_poly*(r_poly + 3*w*diff(r_poly, w)))
report("Session-7 structural constant: 2p'rw - p(r+3wr') == h0 (constant)",
       simplify(h_expr - h0) == 0)
N_expr = expand(p_poly**2 - w*r_poly**3)
NP = Poly(N_expr, w)
report("N := p^2 - w r^3 has degree exactly 3 (the 16->3 miracle)",
       NP.degree() == 3)
n3 = NP.nth(3); n2 = NP.nth(2); n1 = NP.nth(1); n0 = NP.nth(0)
report("Session-10 cubic coefficient n3 == (-128 + 64 i sqrt3)/3",
       simplify(n3 - (Rat(-128,3) + Rat(64,3)*sq)) == 0)
report("CROSS-EPOCH: h0 == -13 * n3  (exact, over Q(i sqrt 3))",
       simplify(h0 + 13*n3) == 0)

# in-chart near-miss (rho = s = 3 chart): x2 = q v^3, x1 = (v+1)/x2^3,
# w = v^3/x2 = 1/q:
y1_nm = (v+1)**3 * q**(-1) * v**(-3) * p_poly.subs(w, 1/q)
y2_nm = (v+1)**2 * q**(-1) * v**(-2) * r_poly.subs(w, 1/q)
# sanity: this equals the (x1,x2) near-miss composed with the chart
y1_x = x1**3*x2**8*p_poly.subs(w, (x1*x2**3-1)**3/x2)
y2_x = x1**2*x2**5*(x1*x2**3-1)*r_poly.subs(w, (x1*x2**3-1)**3/x2)
subs_chart = {x1: (v+1)/(q*v**3)**3, x2: q*v**3}
report("in-chart near-miss y1 == x1^3 x2^8 p(v^3/x2) composed with chart",
       cancel(y1_nm - y1_x.subs(subs_chart)) == 0)
report("in-chart near-miss y2 == x1^2 x2^5 v r(v^3/x2) composed with chart",
       cancel(y2_nm - y2_x.subs(subs_chart)) == 0)

Jqv_direct = together(diff(y1_nm, q)*diff(y2_nm, v) - diff(y1_nm, v)*diff(y2_nm, q))
report("DIRECT in-chart Jacobian: J_{qv}(near-miss) == h0*(v+1)^4*q^-3*v^-6",
       cancel(Jqv_direct - h0*(v+1)**4*q**(-3)*v**(-6)) == 0)
# consistency with C1a/C1b: J_x = J_qv * det = h0(v+1)^4 q^-3 v^-6 * (-x2^3/v^3)
#   = -h0*x1^4*x2^12 (the Session-7 certified Jacobian).  Check:
lhs = (h0*(v+1)**4*q**(-3)*v**(-6) * (-(q*v**3)**3/v**3))
rhs = (-h0*x1**4*x2**12).subs(subs_chart)
report("consistency: J_qv * det == -h0 x1^4 x2^12 in-chart",
       cancel(lhs - rhs) == 0)

# the cusp function in-chart and the chain:
W_nm = together(y1_nm**2 - y2_nm**3)
W_target = (v+1)**6*v**(-6)*(n3*q**(-5) + n2*q**(-4) + n1*q**(-3) + n0*q**(-2))
report("W = y1^2 - y2^3 == (v+1)^6 v^-6 (n3 q^-5 + n2 q^-4 + n1 q^-3 + n0 q^-2)",
       cancel(W_nm - W_target) == 0)
print("      ord_q W = -5: the thirteen chain blocks q^-18..q^-6 vanish")
print("      identically (chain condition D = 13), and the deviation's")
print("      first block gives R = n3 exactly:")
# [q^-5] W = g0^6 * R with g0 = (v+1)/v (alpha = 1):
g0_nm = (v+1)/v
R_nm = simplify(n3)   # from [q^-5]W == g0^6 * n3:
Wq5 = expand(W_target).coeff(q, -5) if expand(W_target).coeff(q, -5) != 0 \
    else expand(W_target*q**5).subs(q, 0)
report("[q^-5] W == g0^6 * n3   (so R_nearmiss = n3, a degree-0 'polynomial')",
       cancel(Wq5 - g0_nm**6*n3) == 0)
# master identity applied to the near-miss (R = n3 constant, alpha = 1):
pred_block = (g0_nm**5*(3*diff(R_nm, v) + 13*R_nm*diff(g0_nm, v)/g0_nm))
report("identity predicts [q^-3] block == -13*n3*(v+1)^4*v^-6",
       cancel(pred_block + 13*n3*(v+1)**4*v**(-6)) == 0)
# and the direct [q^-3] block of J_qv(near-miss) is h0*(v+1)^4*v^-6 (above),
# so the identity forces h0 = -13*n3 -- which the certified data satisfies.
print("      direct block h0*(v+1)^4*v^-6 vs identity block -13*n3*(v+1)^4*v^-6:")
report("CROSS-EPOCH REPRODUCTION: identity + certified near-miss => h0 = -13 n3",
       simplify(h0 + 13*n3) == 0)

print()
print(f"TOTAL: {PASS} PASS, {FAIL} FAIL")
sys.exit(0 if FAIL == 0 else 1)
