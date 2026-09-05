"""night20 -- verification of the two imported results, before anything is
built on them."""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import mate20 as MT
import pole20 as PL
x, y, c = I.x, I.y, I.c
OUT = []


def say(s=""):
    print(s, flush=True)
    OUT.append(s)


say("=" * 78)
say("V1  Result 2's identity, symbolically:  D_P(P) = 0  and")
say("    D_P(A/P) = D_P(A)/P ,  hence  D_P(A) = P  =>  Q = A/P is a rational mate")
say("=" * 78)
for k, v in PL.verify_identity():
    say("  %s  ->  %s" % (k, v))
say("  V1 verdict: PASS" if all(v == "0" for _, v in PL.verify_identity())
    else "  V1 verdict: FAIL")
say()

say("=" * 78)
say("V2  Result 1 (pole theorem) on three constructed examples: every finite")
say("    denominator component of a rational solution of D_P(Q) = 1 must be a")
say("    component of a fibre {P = c}.  Test: reduce P modulo the pole")
say("    component g; the component lies in a fibre iff P mod g is a CONSTANT.")
say("=" * 78)
ok2 = True

say("  (a) REDUCIBLE FIBRE.  P = x*y^2 + y = y*(x*y+1), unimodular, genus 0,")
say("      fibre c = 0 reducible.  Two rational mates, from night19 and from")
say("      the box search in this lane:")
P = sp.expand(x*y**2 + y)
for Q in [-x/(x*y+1), -sp.Integer(1)/y]:
    r = PL.verify_pole_theorem(P, Q)
    say("      Q = %-18s  [P,Q]-1 = %s" % (r["Q"], r["bracket_minus_1"]))
    for row in r["poles"]:
        say("         pole component  g = %-12s multiplicity %d ;  P mod g = %-8s "
            " -> lies in the fibre P = %s : %s"
            % (row["pole component g"], row["multiplicity"], row["P mod g"],
               row["g divides P - c with c ="], row["is a fibre component"]))
    say("         all poles are fibre components: %s"
        % r["all poles are fibre components"])
    ok2 &= r["all poles are fibre components"]
say("      and the components of that fibre, independently: P - 0 factors as %s"
    % sp.sstr(sp.factor(P)))
say()

say("  (b) COORDINATE.  P = x + y^2 (all fibres irreducible).  By the")
say("      consequence of Result 1 a rational mate must then be polynomial.")
Pc = sp.expand(x + y**2)
v, rows = MT.mate_verdict(Pc, [1, 2, 3])
say("      polynomial mate found: %s  ->  Q = %s, [P,Q]-1 = %s"
    % (v, rows[-1].get("Q"), rows[-1].get("bracket_minus_1")))
rr = MT.rational_mate_box(Pc, [Pc, Pc - 1, Pc + 1, x, y], kmax=2, DAmax=4)
say("      rational-mate box over the fibres P, P-1, P+1 and over x, y:")
say("         found = %s  (%d denominators tried, deg A <= %d)"
    % (rr.get("found"), rr["n_denominators_tried"], rr["DAmax"])
    if not rr.get("found") else
    "         found = True  poles = %s  Q = %s" % (rr.get("poles"), rr.get("Q")))
say("      D_P(A) = P is solvable with A = P*Q = %s :" % sp.sstr(sp.expand(Pc*y)))
say("         D_P(A) - P = %s" % sp.sstr(sp.expand(PL.D(Pc, Pc*y) - Pc)))
ok2 &= (sp.expand(PL.D(Pc, Pc*y) - Pc) == 0)
say()

say("  (c) ALL FIBRES IRREDUCIBLE, POSITIVE GENUS.  This lane certified no")
say("      unimodular example of that kind (see IRREDUCIBLE.md §4), so the")
say("      example constructed here is P = y^2 - x^5 - x - 1: all fibres")
say("      irreducible (measured), genus 2, but NOT unimodular -- recorded as")
say("      such, since the pole theorem's hypothesis is gradient-unimodularity.")
P2 = sp.expand(y**2 - x**5 - x - 1)
fi = I.all_fibres_irreducible(P2)
g2, _ = I.genus_generic(P2)
u2 = I.unimodular(P2)
say("      all fibres irreducible = %s ; genus = %s ; unimodular = %s"
    % (fi["all_irreducible"], g2, u2["unimodular"]))
for Dd in (2, 4, 6, 8):
    rA = PL.solve_A(P2, Dd)
    say("      D_P(A) = P on S(%d): %s%s" % (Dd, rA["verdict"],
        ("  |lambda| = %d verified = %s" % (rA["lambda_support"], rA["lambda_verified"]))
        if rA["verdict"] == "EMPTY_over_Q" else ("  A = %s, residual %s"
        % (rA.get("A"), rA.get("residual")))))
say()
say("  (d) the A-formulation reproduces night19's rational mate exactly:")
say("      A = -x*y ,  P = x*y^2 + y ,  D_P(A) - P = %s ,  A/P = %s"
    % (sp.sstr(sp.expand(PL.D(P, -x*y) - P)), sp.sstr(sp.cancel(-x*y/P))))
ok2 &= (sp.expand(PL.D(P, -x*y) - P) == 0)
rA = PL.solve_A(P, 4)
say("      and the linear solver finds it independently on S(4): %s, A = %s,"
    " residual %s" % (rA["verdict"], rA.get("A"), rA.get("residual")))
say()
say("  V2 verdict: %s" % ("PASS" if ok2 else "FAIL"))
say()
say("VERIFICATIONS %s" % ("PASS" if ok2 else "FAIL"))
open(os.path.join(HERE, "poletest20_log.txt"), "w").write("\n".join(OUT) + "\n")
