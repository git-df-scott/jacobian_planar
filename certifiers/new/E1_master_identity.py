"""
E1 - INDEPENDENT RE-DERIVATION OF THE SESSIONS 16-18 ENDGAME MASTER IDENTITY.

Sessions 16-18 asserted, with the certificate living only in a lost transcript:

    "the leading Keller block pairs the deviation's first block g^3 R/(2 v^27)
     with y2's leading block g^2 v^-18 ... and the block collapses, via
     13(9v+8) - 117(v+1) = -13, to   alpha^5 (v+1)^4 (3v(v+1) R' - 13 R) = -c."

This file re-derives that identity FROM SCRATCH with symbolic framework data,
so the identity no longer depends on the lost certificate.  It also extracts
the two structural relations that determine the endgame parameters:

    N = (2e + 3b)(1 + G)/b            (the v-power in R := v^N W~_-5 / g^6)
    D = 3(2e + 3b)/b = 3N/(1 + G)     (the coefficient in 3 v(v+1) R' - D R)

FRAMEWORK DATA (all of it, named):
    beta   q-pole order of y2 on the (-2)-curve      ((99,66): 6)
    gam    q-pole order of y1 on the (-2)-curve      ((99,66): 9)
    sig    q-index of the first surviving block of W = y1^2 - y2^3   ((99,66): 5)
    G      v-exponent of the boundary polynomial g = alpha*U*v^G     ((99,66): 8)
    N      v-power normalising R                                     ((99,66): 39)
    p      q-exponent of the Keller chart form  J = -c q^-p v^-tau    ((99,66): 3)
    tau    v-exponent of the Keller chart form                        ((99,66): 6)
    e := gam - sig  is the q-index of the deviation's first block.
"""
import sympy as sp

v, alpha, c = sp.symbols('v alpha c')
a, b, e, beta, G, N = sp.symbols('a b e beta G N')
U = v + 1
R = sp.Function('R')(v)
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)));  print(("  [PASS] " if cond else "  [FAIL] ") + name)

# ---------------------------------------------------------------- step 1
# y2  = q^-beta * eta(v),          eta = g^2 v^{-3 beta}     = alpha^2 U^2 v^a
# Delta = q^{ e } * delta(v),      delta = (g^3/2) R v^{3e-N} = (alpha^3/2) U^3 R v^b
# with g = alpha U v^G, a = 2G - 3beta, b = 3G + 3e - N.
eta   = alpha**2 * U**2 * v**a
delta = sp.Rational(1,2) * alpha**3 * U**3 * R * v**b

# Leading Keller block:  J = Delta_q y2_v - Delta_v y2_q  at  q^{e-beta-1}
#   = q^{e-beta-1} [ e*delta*eta' + beta*delta'*eta ]
block = e*delta*sp.diff(eta, v) + beta*sp.diff(delta, v)*eta

# ---------------------------------------------------------------- step 2
# Claimed closed form, symbolic in a,b,e,beta:
claim = (alpha**5/2) * U**4 * v**(a+b-1) * (
        beta*U*v*sp.diff(R, v) + (2*e + 3*beta)*v*R + (e*a + beta*b)*U*R)
chk("general block == (alpha^5/2) U^4 v^{a+b-1} [ b U v R' + (2e+3b) v R + (ea+bb) U R ]",
    sp.simplify(sp.expand(sp.powsimp(block - claim, force=True))) == 0)

# ---------------------------------------------------------------- step 3
# Substitute a = 2G-3beta, b = 3G+3e-N and collect the U-coefficient of the R-part.
aa = 2*G - 3*beta
bb = 3*G + 3*e - N
# (2e+3beta) v R + (e a + beta b) U R,  v = U - 1:
coeffU = sp.expand((2*e + 3*beta) + (e*aa + beta*bb))
chk("U-coefficient of the R-part = (2e+3b)(1+G) - b*N",
    sp.expand(coeffU - ((2*e + 3*beta)*(1 + G) - beta*N)) == 0)
Nstar = sp.simplify(sp.solve(sp.Eq(coeffU, 0), N)[0])
print("    => collapse condition:  N =", sp.factor(Nstar))

# With the collapse, block  =  (alpha^5/2) U^4 v^{a+b-1} [ beta U v R' - (2e+3beta) R ]
#   normalise to  3 U v R' - D R  by dividing by beta/3:
Dsym = sp.simplify(3*(2*e + 3*beta)/beta)
print("    => D = 3(2e+3beta)/beta =", sp.factor(Dsym),
      " and with N = N*:  D = 3N/(1+G) =", sp.simplify(3*Nstar/(1+G)))
chk("D = 3N/(1+G) at the collapse", sp.simplify(Dsym - 3*Nstar/(1+G)) == 0)

# ---------------------------------------------------------------- step 4
#   the (99,66) First Framework instantiation
DATA = dict(beta=6, gam=9, sig=5, G=8, N=39, p=3, tau=6)
Bt, Gam, Sg, Gg, Nn, pp, tt = (DATA[k] for k in ('beta','gam','sig','G','N','p','tau'))
ee = Gam - Sg
chk("(99,66): e = gam - sig = 4", ee == 4)
chk("(99,66): q-exponent of J is e-beta-1 = -p = -3", ee - Bt - 1 == -pp)
aN, bN = 2*Gg - 3*Bt, 3*Gg + 3*ee - Nn
chk("(99,66): a = 2G-3beta = -2", aN == -2)
chk("(99,66): b = 3G+3e-N = -3", bN == -3)
chk("(99,66): a+b-1 = -tau = -6", aN + bN - 1 == -tt)
chk("(99,66): collapse condition N = (2e+3beta)(1+G)/beta holds at N=39",
    sp.simplify(Nstar.subs({e: ee, beta: Bt, G: Gg})) == Nn)
D13 = sp.simplify(Dsym.subs({e: ee, beta: Bt}))
chk("(99,66): D = 13", D13 == 13)

blockN = block.subs({a: aN, b: bN, e: ee, beta: Bt})
target = alpha**5 * U**4 * (3*U*v*sp.diff(R, v) - 13*R) / v**6
chk("(99,66) master identity: block == alpha^5 (v+1)^4 (3 v(v+1) R' - 13 R)/v^6",
    sp.simplify(sp.expand(blockN - target)) == 0)

# the arithmetic step the archive quotes
chk("archive's collapse arithmetic 13(9v+8) - 117(v+1) == -13",
    sp.expand(13*(9*v + 8) - 117*(v + 1)) == -13)

# ---------------------------------------------------------------- step 5
#   D as a function of beta alone, using e = beta + 1 - p  (from J's q-exponent)
Dbeta = sp.simplify(Dsym.subs(e, beta + 1 - sp.Symbol('p')))
print("\n    D(beta,p) = 3(2(beta+1-p)+3beta)/beta =", sp.simplify(sp.expand(Dbeta)))
print("    at p = 3:  D =", sp.simplify(Dbeta.subs(sp.Symbol('p'), 3)), " -> beta=6 gives", 
      sp.simplify(Dbeta.subs({sp.Symbol('p'): 3, beta: 6})))
chk("D = 15 - 12/beta when p = 3", sp.simplify(Dbeta.subs(sp.Symbol('p'),3) - (15 - sp.Integer(12)/beta)) == 0)
print("    CONSEQUENCE: with p = 3 the endgame D is bounded: D = 15 - 12/beta < 15")
print("                 for every beta > 0.  D is NOT the chain degree in general.")

print()
for n, ok in PASS:
    if not ok: print("FAILED:", n)
assert all(ok for _, ok in PASS), "E1 FAILED"
print("E1: ALL %d CHECKS PASS" % len(PASS))
