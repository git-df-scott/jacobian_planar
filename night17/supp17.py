"""night17 -- supplement: the three loose ends left by the main sweep.

S1. H10's emptiness was stated with only k2 != 0 adjoined, and the Groebner
    basis came back [k2 z1 - 1, g0]: the only solutions have g0 = 0, i.e. no
    y^2 term at all, which is outside the support.  Redone with BOTH g0 != 0
    and k2 != 0.

S2. The H6 instance drawn by the driver had h(a) = 0, so it fell off the
    unimodular locus of its own stratum (2.1: unimodularity on the deg g = 1
    stratum is exactly h(a) != 0) and came back NOT_CERTIFIED -- a sharpness
    measurement, not a failure.  A second instance with h(a) != 0 is run here.

S3. E12 (deg 29, SE with B = x^27) got NOT_CERTIFIED from the generic Bezout
    producers: EUCLID cannot work because Res_y(P_x, P_y) = m^m B^m alpha^(m-1)
    is not constant, and the LINALG fallback was capped at degree 14 while the
    identity needs degree 28.  A CLOSED FORM is used instead.  With
    A = alpha x + beta, B = c prod (x-a_i)^(e_i), all e_i >= 2, N = prod (x-a_i),
    s = sum_i e_i prod_(j != i) (x-a_j)  (so B' N = B s), and M = B/N^2 (a
    polynomial exactly because every e_i >= 2):

        N P_x = alpha N + B' N y^m = alpha N + s B y^m = alpha N + (s/m) y P_y,
        so   alpha N = N P_x - (s/m) y P_y,
        and  alpha = P_x - B' y^m = P_x - M s N y^m,

    which combine to the identity

        U P_x + V P_y = 1,
        U = 1/alpha - M s N y^m / alpha^2,
        V = M s^2 y^(m+1) / (m alpha^2).

    It is expanded coefficientwise over Q like every other Bezout certificate.
"""
import json
import os
import sys
import time
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "night15"))

import pk17 as pk                                          # noqa: E402
import res17 as R                                          # noqa: E402
import certs17 as CE                                       # noqa: E402
import systems17 as SY                                     # noqa: E402
import sweep17 as SW                                       # noqa: E402
import mate17 as MT                                        # noqa: E402

X = R.X
OUT = []


def say(s):
    print(s)
    sys.stdout.flush()
    OUT.append(s)


def bezout_se(alpha, roots, c, m):
    """the closed-form Bezout pair for P = alpha x + beta + c prod (x-a_i)^e_i y^m."""
    al = sp.Rational(alpha)
    N = sp.prod([(X - sp.Rational(a)) for a, _ in roots])
    B = sp.Rational(c) * sp.prod([(X - sp.Rational(a)) ** e for a, e in roots])
    s = sum(e * sp.prod([(X - sp.Rational(b)) for b, _ in roots if b != a])
            for a, e in roots)
    M = sp.cancel(B / N ** 2)
    Y = sp.Symbol("y")
    U = sp.expand(1 / al - M * s * N * Y ** m / al ** 2)
    V = sp.expand(M * s ** 2 * Y ** (m + 1) / (m * al ** 2))
    return U, V


def check_bezout(P, U, V):
    Y = sp.Symbol("y")
    px = sum(sp.Rational(F(v).numerator, F(v).denominator) * X ** i * Y ** j
             for (i, j), v in pk.dx(P).items())
    py = sum(sp.Rational(F(v).numerator, F(v).denominator) * X ** i * Y ** j
             for (i, j), v in pk.dy(P).items())
    res = sp.expand(U * px + V * py - 1)
    return 0 if res == 0 else len(sp.Poly(res, X, Y).terms())


def main():
    recs = []
    say("=" * 78)
    say("S1  H10 = HE(G=0,H=0,K=2) with BOTH g0 != 0 and k2 != 0")
    sy_ = SY.he_system(0, 0, 2)
    say("    equations: %s" % [sp.sstr(e) for e in sy_["eqs"]])
    emp, b = SY.groebner_empty(sy_["eqs"], sy_["vars"],
                               [sp.Symbol("g0"), sp.Symbol("k2")])
    say("    Rabinowitsch (g0 != 0, k2 != 0): unsolvable = %s   basis = [%s]"
        % (emp, b))
    recs.append({"item": "S1", "support": "H10", "unsolvable": emp, "basis": b})

    say("")
    say("=" * 78)
    say("S2  H6 = HE(G=1,H=5,K=9), a second instance with h(a) != 0")
    P, info = SW.he_instance(1, -1, [1, 1, 0, 0, 1, 2], 1)
    say("    g = %s, h = %s, h(a) = %s, Delta = %s"
        % (info["g"], info["h"], sp.sympify(info["h"]).subs(X, -1), info["Delta"]))
    scr = SW.he_screen(P)
    rec = SW.certify_and_mate(P, scr, "H6", "second instance, h(a) != 0",
                              do_mate=False, do_num=True)
    say("    deg %d  %s  unimod=%s (%s, residual %s)  SY=%s"
        % (rec["deg"], scr["verdict"], rec["unimodular"], rec["bezout_method"],
           rec["bezout_residual_terms"], rec["sy"]))
    say("    NUM-MONO: %s" % rec.get("numeric_NUM_MONO"))
    if rec["survivor"]:
        d = rec["deg"]
        rec["mate"] = MT.solve(P, max_cols=1500, degs=(d, (3 * d + 1) // 2, 2 * d))
        say("    mate: %s" % rec["mate"]["verdict"])
        if rec["mate"]["verdict"] == "MATE_over_Q":
            say("    *** A MATE SYSTEM WAS CONSISTENT ***")
    recs.append(rec)

    say("")
    say("=" * 78)
    say("S3  E12 = SE(m=2; 27), deg 29, closed-form Bezout")
    P = SW.se_instance(1, 0, 1, [(0, 27)], 2)
    U, V = bezout_se(1, [(0, 27)], 1, 2)
    nt = check_bezout(P, U, V)
    say("    U = %s" % sp.sstr(U))
    say("    V = %s" % sp.sstr(V))
    say("    U P_x + V P_y - 1 expanded over Q: %d residual terms" % nt)
    scr = SW.se_screen(1, 0, 1, [(0, 27)], 2)
    syv, st = CE.sy(P)
    rec = {"support": "E12", "hash": SW.phash(P), "deg": pk.tdeg(P),
           "deg_y": pk.degy(P), "n_terms": len(P), "P": pk.to_str(P),
           "screen": scr, "unimodular": ("UNIMODULAR_CERTIFIED" if nt == 0
                                         else "NOT_CERTIFIED"),
           "bezout_method": "CLOSED_FORM_SE", "bezout_residual_terms": nt,
           "sy": syv, "sy_nodes": st["nodes"],
           "fibre_witness": "NON_COORDINATE (generic fibre: genus %s, %s punctures)"
                            % (scr["genus"], scr["n_punctures"]),
           "note": "closed-form Bezout, see supp17.py docstring"}
    rec["survivor"] = bool(nt == 0 and syv == "NON_COORDINATE"
                           and scr["periods_vanish"])
    say("    screen=%s  SY=%s  survivor=%s" % (scr["verdict"], syv, rec["survivor"]))
    if rec["survivor"]:
        t = time.time()
        rec["mate"] = MT.solve(P, max_cols=700, degs=(29,))
        say("    mate: %s  (%.0fs)" % (rec["mate"]["verdict"], time.time() - t))
        if rec["mate"]["verdict"] == "MATE_over_Q":
            say("    *** A MATE SYSTEM WAS CONSISTENT ***")
    recs.append(rec)

    # the same closed form, checked on three more members of the SE family
    say("")
    say("    closed-form Bezout re-checked on further SE members:")
    for al, roots, cc, m in ((1, [(0, 3)], 1, 2), (2, [(1, 3)], 3, 2),
                             (1, [(0, 5), (2, 4)], 1, 3), (1, [(0, 4)], 3, 3)):
        Pk = SW.se_instance(al, 0, cc, roots, m)
        Uk, Vk = bezout_se(al, roots, cc, m)
        say("      alpha=%s c=%s m=%s roots=%s  deg P=%d  residual terms = %d"
            % (al, cc, m, roots, pk.tdeg(Pk), check_bezout(Pk, Uk, Vk)))

    json.dump(recs, open(os.path.join(HERE, "supp17.json"), "w"), indent=1,
              default=str)
    open(os.path.join(HERE, "supp17_log.txt"), "w").write("\n".join(OUT) + "\n")


if __name__ == "__main__":
    main()
