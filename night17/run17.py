"""night17 -- driver: sweep the supports, record everything, write the CSV."""
import csv
import json
import os
import sys
import time
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pk17 as pk                                          # noqa: E402
import res17 as R                                          # noqa: E402
import systems17 as SY                                     # noqa: E402
import sweep17 as SW                                       # noqa: E402
from sweep17 import say, LOG                               # noqa: E402

X = R.X
RECORDS = []
SUPPORTS = []


def mate_plan(d):
    if d <= 11:
        return (d, (3 * d + 1) // 2, 2 * d), 1500
    if d <= 16:
        return (d, (3 * d + 1) // 2), 900
    return (d,), 700


def check_system(system, subs):
    """substitute an instance's coefficient vector into the support's residue
    equations -- the by-construction check, and the shape of the mandatory
    control."""
    vals = [sp.simplify(sp.expand(e.subs(subs))) for e in system["eqs"]]
    return all(v == 0 for v in vals), [sp.sstr(v) for v in vals]


def he_subs(P, G, H, K):
    d = {}
    for j, nm, n in ((2, "g", G), (1, "h", H), (0, "k", K)):
        for i in range(n + 1):
            c = F(P.get((i, j), 0))
            d[sp.Symbol("%s%d" % (nm, i))] = sp.Rational(c.numerator, c.denominator)
    return d


def run_instance(P, screen, sid, note, do_num=True, system=None, subs=None):
    d = pk.tdeg(P)
    degs, cap = mate_plan(d)
    rec = SW.certify_and_mate(P, screen, sid, note, do_mate=False,
                              do_num=(do_num and d <= 11))
    if system is not None and subs is not None:
        okk, vals = check_system(system, subs)
        rec["satisfies_support_equations"] = bool(okk)
        rec["equation_values"] = vals
        say("      by-construction check: the coefficient vector satisfies the "
            "support equations = %s   (values %s)" % (okk, vals[:6]))
    if rec["survivor"]:
        say("      -> SURVIVOR %s deg %d : mate solve (D in %s)"
            % (rec["hash"], d, list(degs)))
        rec["mate"] = __import__("mate17").solve(P, max_cols=cap, verbose=True,
                                                 degs=degs)
        if rec["mate"]["verdict"] == "MATE_over_Q":
            say("      *** A MATE SYSTEM WAS CONSISTENT: %s ***" % rec["hash"])
    RECORDS.append(rec)
    say("      %-14s deg=%-3d %-22s unimod=%-22s SY=%-15s mate=%s"
        % (rec["hash"], d, screen["verdict"], rec["unimodular"], rec["sy"],
           rec.get("mate", {}).get("verdict", "-")))
    return rec


def support(sid, kind, label, system, note):
    s = {"id": sid, "kind": kind, "label": label, "note": note}
    s["n_unknowns"] = len(system["vars"])
    s["variables"] = [sp.sstr(v) for v in system["vars"]]
    s["equations"] = [sp.sstr(e) for e in system["eqs"]]
    s["n_equations"] = len(system["eqs"])
    s["structure"] = SY.dimension_hint(system["eqs"], system["vars"])
    SUPPORTS.append(s)
    say("")
    say("=" * 78)
    say("SUPPORT %s  %s   (%s)" % (sid, label, note))
    say("  unknowns (%d): %s" % (s["n_unknowns"], ", ".join(s["variables"])))
    say("  residue system (%d equations):" % s["n_equations"])
    for e in s["equations"]:
        say("      %s = 0" % e)
    say("  solution structure: %s" % str(s["structure"])[:700])
    return s


def main():
    t0 = time.time()

    # ------------------------------------------------------------------ HE
    # H1/H2: g constant -- the stratum that contains the coordinate x + y^2
    for sid, (G, H, K), hcs in (("H1", (0, 1, 2), ([1, 1], [0, 1])),
                                ("H2", (0, 3, 6), ([1, 0, 1, 2],))):
        sy_ = SY.he_system(G, H, K)
        s = support(sid, "HE", sy_["label"],
                    sy_, "deg g = 0: g constant")
        emp, b = SY.groebner_empty(sy_["eqs"], sy_["vars"],
                                   [sp.Symbol("h%d" % H)])
        s["groebner_empty_with_h%d_nonzero" % H] = emp
        s["groebner_basis_head"] = b
        say("  Rabinowitsch (h%d != 0): unsolvable = %s" % (H, emp))
        for hc in hcs:
            P, info = SW.he_instance(None, None, hc, 2, g_const=1)
            run_instance(P, SW.he_screen(P), sid, "g const, h = %s" % info["h"],
                         system=sy_, subs=he_subs(P, G, H, K))

    # H3..H8: g linear -- the stratum where the survivors live
    for sid, (G, H, K), hc, aa, gam, al in (
            ("H3", (1, 1, 1), [1, 1], 0, 1, 2),
            ("H4", (1, 2, 3), [1, 1, 1], 1, 1, 1),
            ("H5", (1, 3, 5), [1, 0, 1, 1], 0, 2, 3),
            ("H6", (1, 5, 9), [1, 1, 0, 0, 1, 1], -1, 1, 1),
            ("H7", (1, 8, 15), [1, 0, 1, 0, 0, 1, 0, 1, 1], 0, 1, 1),
            ("H8", (1, 15, 29), [1] + [0] * 13 + [1, 1], 0, 1, 1)):
        sy_ = SY.he_system(G, H, K)
        s = support(sid, "HE", sy_["label"], sy_,
                    "deg g = 1: Delta = h^2 - 4gk forced to degree <= 1")
        P, info = SW.he_instance(gam, aa, hc, al)
        s["parametrisation"] = ("g = gamma (x - a), h free, alpha free, "
                                "beta = h(a)^2 - alpha a, k = (h^2 - alpha x - beta)/(4g)")
        run_instance(P, SW.he_screen(P), sid, "g = %s, h = %s" % (info["g"], info["h"]),
                     system=sy_, subs=he_subs(P, G, H, K))

    # H9/H10: strata the residue system kills outright
    for sid, (G, H, K), nz in (("H9", (2, 2, 2), "g2"), ("H10", (0, 0, 2), "k2")):
        sy_ = SY.he_system(G, H, K)
        s = support(sid, "HE", sy_["label"], sy_,
                    "top coefficient %s required nonzero" % nz)
        emp, b = SY.groebner_empty(sy_["eqs"], sy_["vars"], [sp.Symbol(nz)])
        s["groebner_empty_with_%s_nonzero" % nz] = emp
        s["groebner_basis_head"] = b
        say("  Rabinowitsch (%s != 0): unsolvable = %s   basis = [%s]" % (nz, emp, b))

    # ------------------------------------------------------------------ SE
    se_supports = [
        ("E1", 2, (3,), [(1, 0, 1, [(0, 3)]), (2, 1, 3, [(1, 3)])]),
        ("E2", 2, (2,), []),
        ("E3", 2, (4,), []),
        ("E4", 2, (5,), [(1, 0, 1, [(0, 5)])]),
        ("E5", 2, (9,), [(1, 0, 1, [(0, 9)])]),
        ("E6", 3, (2,), [(1, 0, 1, [(0, 2)])]),
        ("E7", 3, (4,), [(1, 0, 1, [(0, 4)])]),
        ("E8", 3, (3,), []),
        ("E9", 2, (2, 3), []),
        ("E10", 2, (3, 3), [(1, 0, 1, [(0, 3), (1, 3)])]),
        ("E11", 3, (5, 4), [(1, 0, 1, [(0, 5), (2, 4)])]),
        ("E12", 2, (27,), [(1, 0, 1, [(0, 27)])]),
        ("E13", 4, (3,), [(1, 0, 1, [(0, 3)])]),
        ("E14", 5, (3,), [(1, 0, 1, [(0, 3)])]),
    ]
    for sid, m, mults, insts in se_supports:
        sy_ = SY.se_system(m, mults)
        s = support(sid, "SE", sy_["label"], sy_,
                    "P = alpha x + beta + c prod (x-a_i)^e_i y^%d ; genus %s, "
                    "%d punctures" % (m, sy_["genus"], sy_["n_punctures"]))
        s["genus"] = str(sy_["genus"])
        s["n_punctures"] = sy_["n_punctures"]
        s["places"] = sy_["places"]
        if sy_["eqs"]:
            emp, b = SY.groebner_empty(sy_["eqs"], sy_["vars"],
                                       [sp.Symbol("alpha"), sp.Symbol("c")])
            s["groebner_empty_with_alpha_c_nonzero"] = emp
            s["groebner_basis_head"] = b
            say("  Rabinowitsch (alpha != 0, c != 0 -- alpha != 0 is forced by "
                "unimodularity): unsolvable = %s   basis = [%s]" % (emp, b))
        for (al, be, cc, roots) in insts:
            P = SW.se_instance(al, be, cc, roots, m)
            sub = {sp.Symbol("alpha"): sp.Rational(al),
                   sp.Symbol("beta"): sp.Rational(be), sp.Symbol("c"): sp.Rational(cc)}
            for _i, (_a, _e) in enumerate(roots):
                sub[sp.Symbol("a%d" % (_i + 1))] = sp.Rational(_a)
            run_instance(P, SW.se_screen(al, be, cc, roots, m), sid,
                         "alpha=%s beta=%s c=%s roots=%s" % (al, be, cc, roots),
                         system=sy_, subs=sub)

    # ------------------------------------------------- SE with the (x,y) swap
    for sid, n, m, insts in (("V1", 1, 2, [(1, 0, 1)]),
                             ("V2", 2, 3, [(1, 0, 1)]),
                             ("V3", 2, 5, [(1, 0, 1)]),
                             ("V4", 3, 4, [(1, 0, 1)]),
                             ("V5", 4, 2, [(1, 0, 1)]),
                             ("V6", 2, 4, [])):
        sy_ = SY.se_system(n, (m,))
        s = support(sid, "SE-swap", "v-power  P = h0 y + c x^%d y^%d" % (n, m),
                    sy_, "the (x,y) swap of SE(m=%d; %d): night14 F2/F2b shape, "
                         "genus %s, %d punctures" % (n, m, sy_["genus"],
                                                     sy_["n_punctures"]))
        s["genus"] = str(sy_["genus"])
        s["n_punctures"] = sy_["n_punctures"]
        if sy_["eqs"]:
            emp, b = SY.groebner_empty(sy_["eqs"], sy_["vars"],
                                       [sp.Symbol("alpha"), sp.Symbol("c")])
            s["groebner_empty_with_alpha_c_nonzero"] = emp
            s["groebner_basis_head"] = b
            say("  Rabinowitsch (h0 != 0, c != 0): unsolvable = %s  basis = [%s]"
                % (emp, b))
        for (h0, be, cc) in insts:
            P = SW.se_instance(h0, be, cc, [(0, m)], n, swap=True)
            scr = SW.se_screen(h0, be, cc, [(0, m)], n)
            scr["note"] = "computed in the swapped variables"
            run_instance(P, scr, sid, "h0=%s c=%s" % (h0, cc))

    # ---------------------------------------------------------------- MIXED
    base, _ = SW.he_instance(1, 0, [1, 1], 2)               # x y^2 + x y + x/4 + y
    seb = SW.se_instance(1, 0, 1, [(0, 3)], 2)
    for sid, P0, tc, sc, note in (
            ("M1", base, [0, 1, 1], None,
             "y-shear y -> y + x + x^2 of the H3 survivor (deg_y stays 2)"),
            ("M2", base, [0, 1], [0, 0, 1],
             "y-shear then x-shear x -> x + y^2 (deg_y grows: genuinely mixed)"),
            ("M3", seb, None, [0, 1],
             "x-shear x -> x + y of the E1 survivor")):
        Pm = SW.shear(P0, tc, sc)
        say("")
        say("=" * 78)
        say("SUPPORT %s  MIXED NEWTON SUPPORT  (%s)" % (sid, note))
        say("  Newton support: %s" % sorted(Pm))
        SUPPORTS.append({"id": sid, "kind": "MIXED", "label": "shear image",
                         "note": note, "n_unknowns": len(Pm),
                         "variables": [], "equations": [],
                         "n_equations": 0,
                         "structure": {"structure": "shear image of a solved "
                                       "support; Jacobian-1 shears preserve "
                                       "eta and all periods (control G3)"},
                         "newton_support": sorted("%d,%d" % k for k in Pm)})
        if pk.degy(Pm) == 2:
            scr = SW.he_screen(Pm)
        else:
            scr = {"instrument": "shear-invariance + NUM-MONO",
                   "verdict": "PERIODS_VANISH", "periods_vanish": True,
                   "genus": 0, "n_punctures": 2,
                   "note": "inherited from the pre-shear member by G3"}
        run_instance(Pm, scr, sid, note)

    # ---------------------------------------------------------------- output
    json.dump({"supports": SUPPORTS, "records": RECORDS},
              open(os.path.join(HERE, "records17.json"), "w"),
              indent=1, default=str)
    with open(os.path.join(HERE, "synthesis.csv"), "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["support", "hash", "deg", "deg_y", "n_terms",
                    "instrument", "screen_verdict", "genus", "n_punctures",
                    "unimodular", "bezout_method", "bezout_residual_terms",
                    "sy", "fibre_witness", "survivor", "mate_verdict",
                    "mate_stages", "numeric_rel_max", "P"])
        for r in RECORDS:
            sc = r["screen"]
            num = r.get("numeric_NUM_MONO", {})
            rels = [v.get("rel") for v in num.values()
                    if isinstance(v, dict) and "rel" in v]
            w.writerow([r["support"], r["hash"], r["deg"], r["deg_y"],
                        r["n_terms"], sc.get("instrument"), sc.get("verdict"),
                        sc.get("genus"), sc.get("n_punctures"),
                        r["unimodular"], r.get("bezout_method"),
                        r.get("bezout_residual_terms"), r["sy"],
                        r["fibre_witness"], r["survivor"],
                        r.get("mate", {}).get("verdict", ""),
                        ";".join("D=%s:%s" % (s.get("deg_Q_bound"), s.get("verdict"))
                                 for s in r.get("mate", {}).get("stages", [])),
                        max(rels) if rels else "", r["P"]])
    open(os.path.join(HERE, "run17_log.txt"), "w").write("\n".join(LOG) + "\n")
    say("")
    say("supports swept: %d   instances: %d   survivors: %d   mates found: %d"
        % (len(SUPPORTS), len(RECORDS), sum(r["survivor"] for r in RECORDS),
           sum(1 for r in RECORDS
               if r.get("mate", {}).get("verdict") == "MATE_over_Q")))
    say("total %.1f s" % (time.time() - t0))
    open(os.path.join(HERE, "run17_log.txt"), "w").write("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
