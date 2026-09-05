"""night15 -- hard-gate controls C1..C4 for the period screen.

C1 POSITIVE  coordinates with an explicitly verified mate: every period must
             vanish.
C2 NEGATIVE  polynomials with a demonstrably nonzero period, so the instrument
             is shown able to detect nonvanishing at all.
C3 CONSISTENCY  sum of residues over all places = 0 on every fibre measured.
C4 CROSS-CHECK  the period screen on three night12 V2 F2-family targets (their
             P is read from the records; no mate system is recomputed here).
"""

import json
import os
import sys
import time
from fractions import Fraction as F

import pk15 as P14
import mono15
import exact_he15
import sy15

HERE = os.path.dirname(os.path.abspath(__file__))
V2 = os.path.join(HERE, "..", "night12", "V2_RECORDS")


# ------------------------------------------------------ coordinate factory

def bracket(P, Q):
    return P14.psub(P14.pmul(P14.dx(P), P14.dy(Q)),
                    P14.pmul(P14.dy(P), P14.dx(Q)))


def T_shift(FG, p):
    """(F, G) -> (F, G + p(F)); preserves [F, G]."""
    Fp, Gp = FG
    add = {}
    for i, c in p.items():
        add = P14.padd(add, P14.pscal(c, P14.ppow(Fp, i)))
    return (Fp, P14.padd(Gp, add))


def S_swap(FG):
    """(F, G) -> (G, -F); preserves [F, G]."""
    return (FG[1], P14.pscal(-1, FG[0]))


def coordinate_pairs():
    """(label, P, Q) with [P, Q] = 1 verified exactly, P a coordinate."""
    x = {(1, 0): F(1)}
    y = {(0, 1): F(1)}
    out = []
    # 1. P = x + y^2, Q = y
    out.append(("x + y^2", P14.padd(x, {(0, 2): F(1)}), y))
    # 2. the sy15 triangular example, built so its mate is explicit
    FG = (x, y)
    FG = T_shift(FG, {2: F(1)})          # (x, y + x^2)
    FG = S_swap(FG)                      # (y + x^2, -x)
    FG = T_shift(FG, {2: F(1)})          # (y+x^2, -x + (y+x^2)^2)
    out.append(("deg4 triangular", FG[0], FG[1]))
    out.append(("deg4 triangular (swapped)", FG[1], P14.pscal(-1, FG[0])))
    # 3. a degree-10 coordinate
    FG = (x, y)
    FG = T_shift(FG, {2: F(1), 1: F(-3)})
    FG = S_swap(FG)
    FG = T_shift(FG, {2: F(2), 0: F(1)})
    FG = S_swap(FG)
    FG = T_shift(FG, {2: F(1), 1: F(1)})
    out.append(("deg10 coordinate", FG[0], FG[1]))
    # 4. a degree-9 coordinate (odd degree, deg_y = 3)
    FG = (x, y)
    FG = T_shift(FG, {3: F(1)})
    FG = S_swap(FG)
    FG = T_shift(FG, {3: F(1), 1: F(2)})
    out.append(("deg9 coordinate", FG[0], FG[1]))
    return out


# --------------------------------------------------------------- the runner

def run_screen(P, cs, tag, want_num=True):
    rows = []
    for c in cs:
        row = {"c": str(c), "tag": tag}
        he = exact_he15.screen(P, c)
        row["exact_he"] = he
        if want_num:
            t = time.time()
            try:
                nm = mono15.screen_fibre_checked(P, c)
            except Exception as e:                       # noqa: BLE001
                nm = {"error": "%s: %s" % (type(e).__name__, e)}
            nm["secs"] = round(time.time() - t, 1)
            row["num_mono"] = nm
        rows.append(row)
    return rows


def brief(row):
    he = row["exact_he"]
    nm = row.get("num_mono", {})
    hev = he.get("verdict", "n/a") if he.get("applicable") else "n/a"
    if "error" in nm:
        nms = "ERR(%s)" % nm["error"][:40]
    elif nm:
        nms = "%s ls=%.2e err=%.1e sumres=%.1e g=%s npunct=%s" % (
            nm["verdict"], nm["ls_residual"], nm["err_ls_residual"],
            nm["infinity"].get("sum_abs", float("nan")),
            nm.get("genus_sum"), nm.get("n_punctures"))
    else:
        nms = "-"
    return "c=%-4s EXACT-HE=%-16s NUM-MONO=%s" % (row["c"], hev, nms)


def main():
    CS = [F(0), F(1), F(-1), F(3, 2)]
    out = {"C1": [], "C2": [], "C3": [], "C4": []}

    print("=" * 78)
    print("C1 POSITIVE -- coordinates with an exactly verified mate")
    print("=" * 78)
    for lab, P, Q in coordinate_pairs():
        br = bracket(P, Q)
        assert br == {(0, 0): F(1)}, (lab, br)
        sy, _ = sy15.certify(P)
        rec = {"label": lab, "deg_P": P14.tdeg(P), "deg_Q": P14.tdeg(Q),
               "P": P14.to_str(P), "Q": P14.to_str(Q),
               "bracket_is_1": True, "SY": sy,
               "fibres": run_screen(P, CS, lab)}
        out["C1"].append(rec)
        print("\n%s   deg P=%d  [P,Q]-1 = 0 exactly, SY=%s" % (lab, P14.tdeg(P), sy))
        print("   P = %s" % P14.to_str(P))
        for r in rec["fibres"]:
            print("   " + brief(r))
        sys.stdout.flush()

    print()
    print("=" * 78)
    print("C2 NEGATIVE -- a demonstrably nonzero period")
    print("=" * 78)
    NEG = [("x*y", {(1, 1): F(1)}, [F(1), F(-1), F(3, 2)],
            "eta = dy/y on {xy=c}: simple pole at the place x=inf (y->0)"),
           ("x^2 + y^2", {(2, 0): F(1), (0, 2): F(1)}, [F(1), F(-1), F(3, 2)],
            "eta = -dx/sqrt(4c-4x^2): residues -+ i/2 at the two places at infinity"),
           ("y^2 - x^3 - x - 1", {(0, 2): F(1), (3, 0): F(-1), (1, 0): F(-1),
                                  (0, 0): F(-1)}, [F(0), F(1)],
            "eta = -dx/w, w^2 = 4(x^3+x+1+c): nonzero HOLOMORPHIC form, genus 1"),
           ("x*y^3 + y", {(1, 3): F(1), (0, 1): F(1)}, [F(1)],
            "deg_y 3, places over the root of lc")]
    for lab, P, cs, why in NEG:
        rec = {"label": lab, "why": why, "P": P14.to_str(P),
               "fibres": run_screen(P, cs, lab)}
        out["C2"].append(rec)
        print("\n%s   (%s)" % (lab, why))
        for r in rec["fibres"]:
            print("   " + brief(r))
        sys.stdout.flush()

    print()
    print("=" * 78)
    print("C4 CROSS-CHECK -- night12 V2 F2-family targets (P read from record)")
    print("=" * 78)
    picks = ["09d8d1d05e63", "7aabbefe44c8", "dada805afbd2"]
    for h in picks:
        d = json.load(open(os.path.join(V2, h + ".json")))
        P = P14.clean({tuple(int(t) for t in k.split(",")): F(v[0], v[1])
                       for k, v in d["P"].items()})
        rec = {"hash": h, "family": d["family"], "tag": d["tag"],
               "deg_P": d["deg_P"], "night12_outcome": d["outcome"],
               "night12_certificate": d["stages"][0].get("certificate"),
               "fibres": run_screen(P, [F(1), F(-1), F(3, 2)], h,
                                    want_num=False)}
        out["C4"].append(rec)
        print("\n%s  %s  deg=%d  night12: %s" % (h, d["tag"], d["deg_P"], d["outcome"]))
        for r in rec["fibres"]:
            he = r["exact_he"]
            print("   c=%-4s EXACT-HE=%-14s case=%s deg_Delta0=%s genus=%s places_inf=%s"
                  % (r["c"], he.get("verdict"), he.get("case"),
                     he.get("deg_Delta0"), he.get("genus"),
                     he.get("n_places_at_infinity")))
        sys.stdout.flush()

    # C3 is a property of every fibre measured above.
    bad = []
    for key in ("C1", "C2"):
        for rec in out[key]:
            for r in rec["fibres"]:
                nm = r.get("num_mono", {})
                if "error" in nm:
                    continue
                s = nm.get("infinity", {}).get("sum_abs")
                sc = max(nm.get("scale", 1.0), 1.0)
                if s is not None and s > 1e-7 * sc:
                    bad.append((rec["label"], r["c"], s))
                he = r["exact_he"]
                if he.get("applicable") and he.get("sum_residues") not in (None, "0"):
                    bad.append((rec["label"], r["c"], "exact " + str(he["sum_residues"])))
    out["C3"] = {"violations": bad,
                 "note": "sum of residues over all places, both instruments"}
    print()
    print("=" * 78)
    print("C3 CONSISTENCY -- sum of residues = 0 on every fibre measured")
    print("=" * 78)
    print("violations:", bad if bad else "NONE")

    with open(os.path.join(HERE, "controls15.json"), "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print("\nwritten controls15.json")


if __name__ == "__main__":
    main()
