"""night19 -- CONTROLS.  Run and passed before any result is claimed.

C1  the machinery must FIND the mate on coordinates, and must NOT produce a
    lambda certificate there.
C2  the closed-form lambda, checked at rational (gamma, c) specialisations and
    several carriers, entirely over Q, independently of the symbolic proof.
C3  P = gamma x y^2 + c y is UNIMODULAR (exact Bezout identity, zero residual)
    and NON-COORDINATE (Shpilrain-Yu certificate, night14/sy14.py read-only,
    plus a fibre witness).
"""
import json, os, sys, time
from fractions import Fraction as F
import sympy as sp
import mate19 as m

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'night14'))
import sy14, poly14                                   # read-only reference lane

HERE = os.path.dirname(os.path.abspath(__file__))
gam, c = sp.symbols('gamma c')
OUT = {}
ALLOK = True


def line(s=""):
    print(s)
    sys.stdout.flush()


# ---------------------------------------------------------------------- C1
line("=" * 78)
line("C1  a COORDINATE with a known mate: the machinery must FIND the mate")
line("    and must NOT produce a valid lambda")
line("=" * 78)
c1 = []
ok1 = True

# (a) P = x + y^2, mate Q = y
Pa = {(1, 0): F(1), (0, 2): F(1)}
for D in range(1, 7):
    d = m.decide(Pa, D)
    lam, cols = m.certificate_search(Pa, D)
    good = (d["verdict"] == "MATE_over_Q" and d["residual_terms"] == 0 and lam is None)
    ok1 &= good
    line("  P = x + y^2        D=%-2d %-14s Q = %-22s [P,Q]-1 terms = %-2s | lambda exists = %-5s  %s"
         % (D, d["verdict"], d.get("Q_str", "-"), d.get("residual_terms", "-"),
            lam is not None, "ok" if good else "MISMATCH"))
    c1.append({"P": "x + y^2", "D": D, "verdict": d["verdict"],
               "Q": d.get("Q_str"), "residual_terms": d.get("residual_terms"),
               "lambda_exists": lam is not None, "ok": bool(good)})

# (b) a degree-10 triangular composition, built by Jacobian-1 moves from (x, y)
def moveA(P, Q, p):                      # (P,Q) -> (P, Q + p(P)) ; Jacobian preserved
    R = {(0, 0): F(0)}
    for k, coef in p:
        T = {(0, 0): F(1)}
        for _ in range(k):
            T = m.pmul(T, P)
        R = m.padd(R, m.pscal(F(coef), T))
    return P, m.padd(Q, R)


def moveB(P, Q):                         # (P,Q) -> (Q, -P) ; Jacobian preserved
    return Q, m.pscal(F(-1), P)


P0, Q0 = {(1, 0): F(1)}, {(0, 1): F(1)}
P0, Q0 = moveA(P0, Q0, [(5, 1)])
P0, Q0 = moveB(P0, Q0)
P0, Q0 = moveA(P0, Q0, [(2, 1)])
P0, Q0 = moveB(P0, Q0)
Pb, Qb = P0, Q0
res0 = m.psub(m.bracket(Pb, Qb), {(0, 0): F(1)})
line("  P10 = (y + x^5)^2 - x   deg P = %d ; construction's own mate deg %d ; [P,Q0]-1 terms = %d"
     % (m.tdeg(Pb), m.tdeg(Qb), len(res0)))
ok1 &= (len(res0) == 0)
for D in [5, 6, 7]:
    t0 = time.time()
    d = m.decide(Pb, D)
    lam, cols = m.certificate_search(Pb, D)
    good = (d["verdict"] == "MATE_over_Q" and d["residual_terms"] == 0 and lam is None)
    ok1 &= good
    line("  P10                D=%-2d %-14s Q = %-22s [P,Q]-1 terms = %-2s | lambda exists = %-5s  %s (%.1fs)"
         % (D, d["verdict"], d.get("Q_str", "-"), d.get("residual_terms", "-"),
            lam is not None, "ok" if good else "MISMATCH", time.time() - t0))
    c1.append({"P": "(y + x^5)^2 - x", "D": D, "verdict": d["verdict"],
               "Q": d.get("Q_str"), "residual_terms": d.get("residual_terms"),
               "lambda_exists": lam is not None, "ok": bool(good)})
line("  C1 %s" % ("PASS" if ok1 else "FAIL"))
OUT["C1"] = {"pass": bool(ok1), "rows": c1}
ALLOK &= ok1

# ---------------------------------------------------------------------- C2
line()
line("=" * 78)
line("C2  the closed-form lambda at rational (gamma, c), verified over Q alone")
line("=" * 78)
c2 = []
ok2 = True
SPEC = [(F(1), F(1)), (F(2), F(3)), (F(-1), F(5)), (F(3), F(-7)), (F(1, 2), F(2, 3)),
        (F(-4), F(-9)), (F(7), F(1, 5))]
for (g, cc) in SPEC:
    for D in [2, 3, 5, 8, 11, 14]:
        P = {(1, 2): g, (0, 1): cc}
        S = m.carrier(D)
        cols, rows = m.build(P, S)
        lam = {(n, n): F((-1) ** n, n + 1) * cc ** n / g ** n
               for n in range((D + 1) // 2 + 1)}
        good, msg = m.verify_lambda(lam, cols)
        d = m.decide(P, D)
        agree = (d["verdict"] == "EMPTY_over_Q")
        ok2 &= (good and agree)
        c2.append({"gamma": str(g), "c": str(cc), "D": D, "closed_lambda_verified": bool(good),
                   "independent_verdict": d["verdict"], "solver_lambda_support": d.get("lambda_support"),
                   "solver_lambda_verified": d.get("lambda_verified")})
        line("  gamma=%-5s c=%-5s D=%-3d closed lambda verified over Q: %-5s | independent solve: %-14s"
             " (own lambda |supp|=%s verified=%s)"
             % (g, cc, D, good, d["verdict"], d.get("lambda_support"), d.get("lambda_verified")))
line("  C2 %s" % ("PASS" if ok2 else "FAIL"))
OUT["C2"] = {"pass": bool(ok2), "rows": c2}
ALLOK &= ok2

# ---------------------------------------------------------------------- C3
line()
line("=" * 78)
line("C3  unimodular (exact Bezout, zero residual) and NON-COORDINATE (SY + fibre)")
line("=" * 78)
ok3 = True
# (a) the symbolic Bezout identity over Q(gamma, c)
Psym = {(1, 2): gam, (0, 1): c}
U = {(2, 0): 4 * gam / c**2}
V = {(0, 0): 1 / c, (1, 1): -2 * gam / c**2}
resid = m.psub(m.padd(m.pmul(U, m.dx(Psym)), m.pmul(V, m.dy(Psym))), {(0, 0): 1})
line("  Bezout over Q(gamma,c):  U = 4*gamma*x^2/c^2 ,  V = (c - 2*gamma*x*y)/c^2")
line("     U*P_x + V*P_y - 1  expands to %d terms  (must be 0)" % len(resid))
ok3 &= (len(resid) == 0)
# (b) numeric Bezout at specialisations, found by search
bez = []
for (g, cc) in SPEC:
    P = {(1, 2): g, (0, 1): cc}
    r = m.bezout(P, maxdeg=4)
    good = r is not None and len(r[3]) == 0
    ok3 &= good
    bez.append({"gamma": str(g), "c": str(cc), "found": bool(r is not None),
                "deg_bound": r[2] if r else None, "residual_terms": len(r[3]) if r else None,
                "U": m.to_str(r[0]) if r else None, "V": m.to_str(r[1]) if r else None})
    line("     search at gamma=%-5s c=%-5s : U*P_x + V*P_y = 1 found at deg <= %s, residual %d terms"
         % (g, cc, r[2] if r else "-", len(r[3]) if r else -1))
# (c) Shpilrain-Yu
sy = []
for (g, cc) in SPEC:
    P = poly14.clean({(1, 2): g, (0, 1): cc})
    v, st = sy14.certify(P)
    good = (v == "NON_COORDINATE")
    ok3 &= good
    sy.append({"gamma": str(g), "c": str(cc), "SY": v, "nodes": st["nodes"], "leaves": st["leaves"]})
    line("     Shpilrain-Yu at gamma=%-5s c=%-5s : %-16s nodes=%d leaves=%d"
         % (g, cc, v, st["nodes"], st["leaves"]))
# SY sanity on the C1 coordinates
for lab, P in [("x + y^2", {(1, 0): 1, (0, 2): 1}), ("(y+x^5)^2 - x", Pb)]:
    v, st = sy14.certify(poly14.clean({k: F(x) for k, x in P.items()}))
    line("     Shpilrain-Yu sanity  %-16s : %-16s (a coordinate; must be COORDINATE)" % (lab, v))
    ok3 &= (v == "COORDINATE")
    sy.append({"sanity": lab, "SY": v})
# (d) fibre witness
x, y = sp.symbols('x y')
Pe = gam * x * y**2 + c * y
fac = sp.factor_list(sp.Poly(Pe, x, y))
line("     fibre witness: P = %s  factors as %s" % (sp.sstr(Pe), sp.sstr(sp.factor(Pe))))
line("       -> the zero fibre P = 0 has %d distinct irreducible components: {y = 0} and"
     " {gamma x y + c = 0}." % len(fac[1]))
line("       -> {gamma x y + c = 0} is isomorphic to A^1 minus a point (x = -c/(gamma y)),")
line("          so it is not isomorphic to the affine line; a coordinate has every fibre")
line("          irreducible and isomorphic to A^1.")
ok3 &= (len(fac[1]) == 2)
OUT["C3"] = {"pass": bool(ok3), "bezout_symbolic_residual_terms": len(resid),
             "bezout_numeric": bez, "shpilrain_yu": sy,
             "fibre_factors": [sp.sstr(f) for f, _ in fac[1]]}
line("  C3 %s" % ("PASS" if ok3 else "FAIL"))
ALLOK &= ok3

line()
line("CONTROLS %s" % ("PASS" if ALLOK else "FAIL"))
OUT["all_pass"] = bool(ALLOK)
json.dump(OUT, open(os.path.join(HERE, 'controls19.json'), 'w'), indent=1)
