"""night20 -- the rational-mate measurement, genus 0 against genus >= 1.

night19's mechanism: for P = gamma*x*y^2 + c*y the formal solution of
[P,Q] = 1 sums to a RATIONAL mate whose poles sit on the second component of
the reducible zero fibre.  Question of interest here: does a rational mate
still exist once the generic fibre has positive genus?

Reason to expect a difference, recorded as the design reasoning: [P,Q] = 1
says that on each fibre P = c the restriction of dQ is the Gelfand-Leray form
omega_c = dx / P_y = -dy / P_x.  A rational function on a curve has a
differential with zero residues AND zero periods.  On a genus-0 fibre only the
residues can obstruct exactness; from genus 1 on there are 2g independent
periods to kill as well.  So the pole mechanism that produces night19's
Q_inf is expected to be unavailable exactly when the genus is positive.
"""
import sys, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import mate20 as MT
x, y, c = I.x, I.y, I.c

CASES = [
    ("x*y^2 + y            (night19)", x*y**2 + y),
    ("x + x^2*y", x + x**2*y),
    ("x + x^3*y", x + x**3*y),
    ("x + x^2*y^2", x + x**2*y**2),
    ("x + x^4*y", x + x**4*y),
    ("x*y^2 + 2*y", x*y**2 + 2*y),
    ("x^2*y^2 + y", x**2*y**2 + y),
    ("x + x^2*y^3", x + x**2*y**3),
    ("x^3*y^2 + y", x**3*y**2 + y),
    ("x^4*y^2 + y", x**4*y**2 + y),
    ("x^4*y^3 + y", x**4*y**3 + y),
    ("x^5*y^2 + y", x**5*y**2 + y),
    ("x + x^3*y^3", x + x**3*y**3),
    ("x^2*y^5 + x", x**2*y**5 + x),
]
rows = []
OUT = []
def say(s):
    print(s, flush=True)
    OUT.append(s)

say("=" * 100)
say("rational mate on the pole divisor of the reducible fibre: genus 0 vs genus >= 1")
say("=" * 100)
say("%-26s %4s %6s  %-9s  %-38s %s" %
    ("P", "deg", "genus", "rat mate", "pole divisor of Q (or box searched)", "Q"))
for name, P in CASES:
    P = sp.expand(P)
    g, _ = I.genus_generic(P)
    fi = I.all_fibres_irreducible(P)
    gens = []
    for r in fi.get("rows", []):
        if r["abs_components"] == "1":
            continue
        m = sp.Poly(sp.sympify(r["m(c)"], locals={'c': c}), c)
        if m.degree() != 1:
            continue
        c0 = list(sp.roots(m))[0]
        for (f, e) in sp.factor_list(sp.expand(P - c0))[1]:
            if sp.Poly(f, x, y).total_degree() >= 1:
                gens.append(sp.expand(f))
    ded, seen = [], set()
    for f in gens:
        if sp.sstr(f) not in seen:
            seen.add(sp.sstr(f))
            ded.append(f)
    rr = MT.rational_mate_box(P, ded, kmax=4,
                              DAmax=max(12, 2 * sp.Poly(P, x, y).total_degree()))
    say("%-26s %4d %6s  %-9s  %-38s %s"
        % (name, sp.Poly(P, x, y).total_degree(), g,
           "FOUND" if rr.get("found") else "none in box",
           rr.get("poles") if rr.get("found")
           else "%d denominators x deg A <= %d" % (rr["n_denominators_tried"], rr["DAmax"]),
           rr.get("Q", "")))
    rows.append({"P": sp.sstr(P), "genus": g,
                 "all_fibres_irreducible": fi.get("all_irreducible"),
                 "generators": [sp.sstr(f) for f in ded],
                 "rational_mate": rr})
say("")
say("tally: genus 0 with a rational mate: %d of %d ; genus >= 1 with a rational"
    " mate: %d of %d"
    % (sum(1 for r in rows if r["genus"] == 0 and r["rational_mate"].get("found")),
       sum(1 for r in rows if r["genus"] == 0),
       sum(1 for r in rows if r["genus"] and r["genus"] >= 1 and r["rational_mate"].get("found")),
       sum(1 for r in rows if r["genus"] and r["genus"] >= 1)))
open(os.path.join(HERE, "ratcmp20_log.txt"), "w").write("\n".join(OUT) + "\n")
json.dump(rows, open(os.path.join(HERE, "ratcmp20.json"), "w"), indent=1, default=str)
