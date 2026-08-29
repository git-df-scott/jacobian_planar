"""night20 -- the mandatory control on the mate solver: it must RECOVER the
mate of a known coordinate of degree >= 10, and it must produce no lambda
there."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import mate20 as MT
import inst20 as I
x, y = I.x, I.y
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)


say("=" * 78)
say("M1  the mate solver must FIND the mate of a coordinate of degree >= 10")
say("=" * 78)
ok = True
cases = [
    ("P10 = (y + x^5)^2 - x", sp.expand((y + x**5)**2 - x), 10),
    ("P12 = ((y + x^3)^2 + (y + x^3))^2 - x", sp.expand(((y + x**3)**2 + (y + x**3))**2 - x), 12),
    ("P15 = (y + x^5)^3 - x", sp.expand((y + x**5)**3 - x), 15),
]
for name, P, d in cases:
    dd = sp.Poly(P, x, y).total_degree()
    v, rows = MT.mate_verdict(P, MT.schedule(P, mult=2, cap=2 * dd))
    last = rows[-1]
    say("  %-40s deg = %-3d  verdict = %s" % (name, dd, v))
    if v == "MATE":
        say("      Q = %s" % last["Q"])
        say("      deg Q = %d ; [P,Q] - 1 = %s ; verified = %s"
            % (last["deg_Q"], last["bracket_minus_1"], last["verified"]))
        ok &= bool(last["verified"])
    else:
        say("      NO MATE FOUND -- control FAILED")
        ok = False
say("  M1 verdict: %s" % ("PASS" if ok else "FAIL"))
say()
say("=" * 78)
say("M2  the same code path must return EMPTY with a re-verified lambda on")
say("    night19's P = x*y^2 + y (proved mate-free there)")
say("=" * 78)
P = sp.expand(x * y**2 + y)
v, rows = MT.mate_verdict(P, [1, 2, 3, 4, 6, 8, 10, 12])
say("  P = x*y^2 + y   verdict = %s" % v)
for r in rows[:4] + rows[-1:]:
    say("      D=%-3d %-14s |lambda| = %s  lambda re-verified = %s"
        % (r["D"], r["verdict"], r.get("lambda_support"), r.get("lambda_verified")))
ok2 = (v == "EMPTY" and all(r.get("lambda_verified") for r in rows))
say("  M2 verdict: %s" % ("PASS" if ok2 else "FAIL"))
ok &= ok2
say()
say("=" * 78)
say("M3  the rational-mate solver must recover night19's rational mate")
say("    Q_inf = -x/(x*y + 1)  of  P = x*y^2 + y   (gamma = c = 1)")
say("=" * 78)
r = MT.rational_mate(P, sp.expand(x * y + 1), kmax=2, DAmax=4)
say("  " + json.dumps(r))
ok3 = bool(r.get("found"))
say("  M3 verdict: %s" % ("PASS" if ok3 else "FAIL"))
ok &= ok3
say()
say("MATE-SOLVER CONTROLS %s" % ("PASS" if ok else "FAIL"))
open(os.path.join(HERE, "matectl20_log.txt"), "w").write("\n".join(OUT) + "\n")
sys.exit(0 if ok else 1)
