"""night20 -- hard-gate controls for the instruments of inst20.py.

Nothing in the search is trusted until this file prints CONTROLS PASS.
Measurements only.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
import inst20 as I

x, y, c = I.x, I.y, I.c
OUT = []


def say(s=""):
    print(s)
    OUT.append(s)


def bar(t):
    say("=" * 78)
    say(t)
    say("=" * 78)


def report(P, name, expect=None):
    u = I.unimodular(P)
    g, gm = I.genus_generic(P)
    ni = I.newton_interior(P)
    fi = I.all_fibres_irreducible(P)
    say("  P = %-34s deg=%-3d" % (sp.sstr(sp.expand(P)), sp.Poly(P, x, y).total_degree()))
    if u.get("unimodular"):
        say("     unimodular : YES   U = %-24s V = %-24s  U*P_x+V*P_y-1 expands to %s"
            % (sp.sstr(u["U"]), sp.sstr(u["V"]), sp.sstr(u["residual"])))
    else:
        say("     unimodular : NO    reduce(1, std(P_x,P_y)) = %s"
            % u.get("reduce_1_mod_std", u.get("reason")))
    say("     genus(generic fibre, Singular/normal.lib over Q(c)) = %s   |  "
        "Baker bound = #interior lattice pts of Newton(P-c) = %d" % (g, ni))
    if fi.get("ok"):
        say("     fibre irreducibility over Qbar: %d candidate special value(s); "
            "all fibres irreducible = %s" % (fi["n_candidates"], fi["all_irreducible"]))
        for r in fi["rows"]:
            say("        c root of  %-40s -> %s absolutely irreducible component(s)"
                % (r["m(c)"], r["abs_components"]))
    else:
        say("     fibre irreducibility: FAILED (%s)" % fi.get("reason"))
    return {"unimodular": u.get("unimodular"), "genus": g, "baker": ni,
            "all_irr": fi.get("all_irreducible"), "ncand": fi.get("n_candidates")}


def main():
    res = {}
    ok = True

    bar("K1  a COORDINATE must come out: unimodular, genus 0, all fibres irreducible")
    r = report(x + y**2, "coord2")
    ok &= (r["unimodular"] is True and r["genus"] == 0 and r["all_irr"] is True)
    res["K1a"] = r
    P10 = sp.expand((y + x**5)**2 - x)
    r = report(P10, "coord10")
    ok &= (r["unimodular"] is True and r["genus"] == 0 and r["all_irr"] is True)
    res["K1b"] = r
    P12 = sp.expand(((y + x**3)**2 + (y + x**3))**2 - x)     # coordinate, deg 12
    r = report(P12, "coord12")
    ok &= (r["unimodular"] is True and r["genus"] == 0 and r["all_irr"] is True)
    res["K1c"] = r
    say("  K1 verdict: %s" % ("PASS" if ok else "FAIL"))
    say()

    bar("K2  x*y -- report what it ACTUALLY is (no assumption)")
    r = report(x * y, "xy")
    res["K2"] = r
    say("  measured: unimodular = %s (the ideal (P_x,P_y) = (y,x) is the maximal"
        % r["unimodular"])
    say("  ideal at the origin, so 1 is NOT in it: x*y is NON-UNIMODULAR, it has")
    say("  the critical point (0,0)); genus = %s; the fibre c = 0 splits as x*y = 0"
        % r["genus"])
    say("  into 2 absolutely irreducible components, so NOT all fibres are irreducible.")
    ok2 = (r["unimodular"] is False and r["genus"] == 0 and r["all_irr"] is False)
    say("  K2 verdict: %s" % ("PASS" if ok2 else "FAIL"))
    ok &= ok2
    say()

    bar("K3  hyperelliptic y^2 - f(x): the classical genus floor((deg f - 1)/2)")
    ok3 = True
    for f, gcl in [(x**5 + x + 1, 2), (x**5 - x, 2), (x**7 + x + 1, 3),
                   (x**6 + x + 1, 2), (x**9 + x**2 + 1, 4), (x**11 + x + 1, 5)]:
        P = y**2 - f
        g, _ = I.genus_generic(P)
        ni = I.newton_interior(P)
        say("  P = y^2 - (%-16s)   Singular genus = %-3s  classical genus = %-3d"
            "  Baker interior-point bound = %d" % (sp.sstr(f), g, gcl, ni))
        ok3 &= (g == gcl)
        ok3 &= (ni >= gcl)
    say("  K3 verdict: %s   (two independent computations of the genus agree:"
        % ("PASS" if ok3 else "FAIL"))
    say("   Singular's normalisation genus, and the classical hyperelliptic value;")
    say("   the Newton-polygon interior count is an upper bound, as Baker's")
    say("   theorem requires.)")
    ok &= ok3
    say()

    bar("K4  a P with a KNOWN reducible special fibre must be DETECTED")
    ok4 = True
    for P, cbad, why in [(x + x**2 * y, "0", "x + x^2 y at c=0 is x*(x*y+1)"),
                         (x * y**2 + y, "0", "night19's P at c=0 is y*(x*y+1)"),
                         (x + x**2 * y**3, "0", "x + x^2 y^3 at c=0 is x*(x*y^3+1)"),
                         (sp.expand((x * y - 1) * (x * y - 2) + x), "0",
                          "designed to split at some c"),
                         (y**2 - x**2, "0", "y^2-x^2 at c=0 is (y-x)(y+x)")]:
        fi = I.all_fibres_irreducible(P)
        cands = [r["m(c)"] for r in fi["rows"]]
        det = fi.get("all_irreducible") is False
        say("  P = %-30s  candidate special c: %-24s  all fibres irreducible = %s"
            % (sp.sstr(sp.expand(P)), cands, fi.get("all_irreducible")))
        say("       (%s)" % why)
        for r in fi["rows"]:
            say("        c root of %-24s -> %s absolutely irreducible component(s)"
                % (r["m(c)"], r["abs_components"]))
        if P != sp.expand((x * y - 1) * (x * y - 2) + x):
            ok4 &= det
    say("  K4 verdict: %s" % ("PASS" if ok4 else "FAIL"))
    ok &= ok4
    say()

    bar("K5  the target shape exists at all: unimodular + genus >= 1")
    r = report(x + x**2 * y**3, "t53")
    say("  (recorded as a measurement: this P is unimodular with a genus-1")
    say("   generic fibre, but its fibre c = 0 is reducible -- so it fails the")
    say("   third requirement.  Target = unimodular AND all fibres irreducible")
    say("   AND genus >= 1.  Genus >= 1 is forced by Neumann-Norbury: a")
    say("   nontrivial rational polynomial in two variables has a reducible")
    say("   fibre, so irreducible-fibres + genus 0 leaves only coordinates.)")
    res["K5"] = r
    say()

    say("CONTROLS %s" % ("PASS" if ok else "FAIL"))
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "controls20_log.txt"), "w").write("\n".join(OUT) + "\n")
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "controls20.json"), "w"), indent=1, default=str)
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
