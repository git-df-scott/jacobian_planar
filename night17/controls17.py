"""night17 -- CONTROLS for the residue engine.

MANDATORY CONTROL (the brief's).  On any support that contains a KNOWN
COORDINATE, the coordinate's coefficient vector must satisfy the residue
equations: a coordinate has a mate, a mate makes eta = dQ exact on every fibre,
and an exact form has no residues.  If a coordinate FAILS the equations the
derivation is wrong.

Also run here:
  * NEGATIVE controls -- polynomials with a residue known to be nonzero.
  * CROSS-INSTRUMENT -- HE17 and SE17 both apply to P = A(x) + B(x) y^2 and
    must agree.
  * CROSS-NIGHT NUMERIC -- night15's NUM-MONO (mono15, imported read-only) on
    the same fibres; its ls_residual and puncture count are independent of the
    algebra here.
"""
import json
import os
import sys
from fractions import Fraction as F

import sympy as sp

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "night15"))

import pk17 as pk                                    # noqa: E402
import res17 as R                                    # noqa: E402
import certs17 as CE                                 # noqa: E402
import coord17 as CO                                 # noqa: E402

X = R.X
LAM = R.LAM
LOG = []


def say(s):
    print(s)
    sys.stdout.flush()
    LOG.append(s)


def ghk(P):
    """split P (deg_y <= 2) into g, h, k, as sympy expressions in x."""
    out = []
    for jj in (2, 1, 0):
        out.append(sum(sp.Rational(F(c).numerator, F(c).denominator) * X ** i
                       for (i, j), c in P.items() if j == jj))
    return out


def he_verdict(P, cc=R.C):
    g, h, k = ghk(P)
    d = R.he17(g, h, k, cc)
    d["residues_at_infinity_all_zero"] = (d["residue_at_infinity"] == "identically 0")
    d["period_vanishing_system_satisfied"] = bool(d["residues_all_zero"]
                                                  and d["genus"] == 0)
    return d


def numeric_check(P, cs=(1, -1)):
    try:
        import mono15
    except Exception as e:                              # noqa: BLE001
        return {"error": str(e)}
    out = {}
    Pi = {k: (int(v) if F(v).denominator == 1 else F(v)) for k, v in P.items()}
    for c in cs:
        try:
            r = mono15.screen_fibre(Pi, c, budget=90.0)
            out[str(c)] = {"ls_residual": r["ls_residual"], "scale": r["scale"],
                           "n_punctures": r["n_punctures"],
                           "genus_sum": r.get("genus_sum"),
                           "max_period": r.get("max_period")}
        except Exception as e:                          # noqa: BLE001
            out[str(c)] = {"error": str(e)[:120]}
    return out


def main():
    res = {"C1_coordinates": [], "C2_negative": [], "C4_cross": [],
           "C5_numeric": []}
    ok = True

    say("=" * 78)
    say("C1  MANDATORY CONTROL -- coordinates must SATISFY the residue equations")
    say("=" * 78)

    # ---- HE supports (deg_y = 2) containing a coordinate
    he_coords = [("x + y^2", {(1, 0): 1, (0, 2): 1}, None)]
    for d in (5, 6):
        P, Q = CO.deg_y2_coordinate(d)
        he_coords.append(("triangular composition, deg %d" % pk.tdeg(P), P, Q))
    # a genuinely mixed-support coordinate: shear x -> x + s(y) of the above
    P, Q = CO.deg_y2_coordinate(3)
    he_coords.append(("triangular composition, deg %d" % pk.tdeg(P), P, Q))

    for lab, P, Q in he_coords:
        P = pk.clean(P)
        d = he_verdict(P)
        syv, _ = CE.sy(P)
        good = d["period_vanishing_system_satisfied"]
        ok &= good
        if Q is not None:
            assert pk.bracket(P, Q) == {(0, 0): F(1)}
        say("HE  %-42s deg=%-3d deg_y=%d  deg Delta_c=%d genus=%d  all-res-zero=%s  SY=%s  -> %s"
            % (lab, pk.tdeg(P), pk.degy(P), d["deg_Delta_c"], d["genus"],
               d["residues_all_zero"], syv,
               "SATISFIES the equations" if good else "*** FAILS ***"))
        res["C1_coordinates"].append({"label": lab, "instrument": "HE17",
                                      "deg": pk.tdeg(P), "data": d,
                                      "sy": syv, "pass": bool(good)})

    # ---- SE supports (P = A(x) + B(x) y^m) containing a coordinate
    for m in (2, 3, 4, 5):
        o = R.se17(X, [], m, Bc=sp.Integer(1))
        eqs = [sp.simplify(e) for e in o["equations"]]
        good = all(e == 0 for e in eqs)
        ok &= good
        P = pk.clean({(1, 0): 1, (0, m): 1})
        syv, _ = CE.sy(P)
        say("SE  %-42s genus=%s punctures=%d  equations=%s  SY=%s  -> %s"
            % ("x + y^%d (coordinate)" % m, o["genus"], o["n_punctures"],
               [sp.sstr(e) for e in eqs], syv,
               "SATISFIES" if good else "*** FAILS ***"))
        res["C1_coordinates"].append({"label": "x + y^%d" % m, "instrument": "SE17",
                                      "equations": [sp.sstr(e) for e in eqs],
                                      "genus": str(o["genus"]),
                                      "n_punctures": o["n_punctures"],
                                      "sy": syv, "pass": bool(good)})

    say("")
    say("=" * 78)
    say("C2  NEGATIVE controls -- a residue that must NOT vanish")
    say("=" * 78)
    neg = [("x^2 + y^2 (HE)", "HE", {(2, 0): 1, (0, 2): 1}),
           ("x*y (HE, g=x)", "HE", {(1, 1): 1}),
           ("y + x^2 y^4 (SE-swap n=2 m=4, night15 witness)", "SE", (2, 4)),
           ("y + x^2 y^2 (SE-swap n=2 m=2)", "SE", (2, 2)),
           ("y + x^3 y^6 (SE-swap n=3 m=6)", "SE", (3, 6))]
    for lab, kind, dat in neg:
        if kind == "HE":
            d = he_verdict(pk.clean(dat))
            nz = not d["residues_all_zero"]
            say("    %-46s res_inf = %-14s -> %s" %
                (lab, d["residue_at_infinity"], "NONZERO ok" if nz else "*** ZERO ***"))
            res["C2_negative"].append({"label": lab, "res_inf": d["residue_at_infinity"],
                                       "pass": bool(nz)})
        else:
            n, m = dat
            o = R.se17(sp.Symbol("h0") * X, [(0, m)], n, Bc=sp.Symbol("c"))
            eqs = [sp.simplify(e) for e in o["equations"]]
            nz = any(e != 0 for e in eqs)
            say("    %-46s equations = %-16s -> %s" %
                (lab, [sp.sstr(e) for e in eqs], "NONZERO ok" if nz else "*** ZERO ***"))
            res["C2_negative"].append({"label": lab,
                                       "equations": [sp.sstr(e) for e in eqs],
                                       "pass": bool(nz)})
        ok &= res["C2_negative"][-1]["pass"]

    say("")
    say("=" * 78)
    say("C4  CROSS-INSTRUMENT -- HE17 vs SE17 on P = A(x) + B(x) y^2")
    say("=" * 78)
    for lab, A, Br in (("x + y^2", X, []),
                       ("x + (x-1)^2 y^2", X, [(1, 2)]),
                       ("x + (x-1)^3 y^2", X, [(1, 3)]),
                       ("x + x^2(x-1)^2 y^2", X, [(0, 2), (1, 2)]),
                       ("x + (x-1)^4 y^2", X, [(1, 4)]),
                       ("x + x^2 (x-1)^3 y^2", X, [(0, 2), (1, 3)]),
                       ("x^2 + y^2", X ** 2, [])):
        o = R.se17(A, Br, 2, Bc=sp.Integer(1))
        se_zero = all(sp.simplify(e) == 0 for e in o["equations"])
        B = sp.prod([(X - a) ** e for a, e in Br]) if Br else sp.Integer(1)
        d = R.he17(B, sp.Integer(0), A)
        he_zero = bool(d["residues_all_zero"])
        agree = (se_zero == he_zero) and (int(o["genus"]) == d["genus"])
        ok &= agree
        say("    %-26s SE17: res-zero=%-5s genus=%s | HE17: res-zero=%-5s genus=%d"
            "  -> %s"
            % (lab, se_zero, o["genus"], he_zero, d["genus"],
               "AGREE" if agree else "*** DISAGREE ***"))
        res["C4_cross"].append({"label": lab, "se_zero": bool(se_zero),
                                "he_zero": he_zero, "genus_se": str(o["genus"]),
                                "genus_he": d["genus"], "agree": bool(agree)})

    say("")
    say("=" * 78)
    say("C5  CROSS-NIGHT NUMERIC -- night15 NUM-MONO (read-only) on the same P")
    say("=" * 78)
    num = [("x + y^2 (coordinate)", {(1, 0): 1, (0, 2): 1}, "VANISHING"),
           ("x*y^2 + y", {(1, 2): 1, (0, 1): 1}, "VANISHING"),
           ("x^2 + y^2", {(2, 0): 1, (0, 2): 1}, "NONVANISHING"),
           ("y + x^2 y^4", {(0, 1): 1, (2, 4): 1}, "NONVANISHING"),
           ("y + x^2 y^3", {(0, 1): 1, (2, 3): 1}, "VANISHING"),
           ("x + (x-1)^3 y^2", {(1, 0): 1, (3, 2): 1, (2, 2): -3,
                                (1, 2): 3, (0, 2): -1}, "VANISHING")]
    for lab, P, expect in num:
        r = numeric_check(pk.clean(P))
        vals = []
        verd = "VANISHING"
        for c, v in r.items():
            if "error" in v:
                verd = "ERROR"
                vals.append("c=%s ERR %s" % (c, v["error"]))
                continue
            rel = v["ls_residual"] / max(v["scale"], 1e-30)
            vals.append("c=%s rel=%.2e punct=%s g=%s" %
                        (c, rel, v["n_punctures"], v["genus_sum"]))
            if rel > 1e-6:
                verd = "NONVANISHING"
        good = (verd == expect)
        ok &= good
        say("    %-26s %-14s expect %-14s %s   [%s]" %
            (lab, verd, expect, "ok" if good else "*** MISMATCH ***", "; ".join(vals)))
        res["C5_numeric"].append({"label": lab, "verdict": verd, "expect": expect,
                                  "detail": r, "pass": bool(good)})

    say("")
    say("ALL CONTROLS PASS" if ok else "*** SOME CONTROL FAILED ***")
    res["all_pass"] = bool(ok)
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                     "controls17.json"), "w"), indent=1, default=str)
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                      "controls17_log.txt"), "w").write("\n".join(LOG) + "\n")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
