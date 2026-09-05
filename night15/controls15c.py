"""night15 -- the SHEAR control, done correctly.

G3: if phi is a polynomial automorphism with Jacobian 1 then P o phi has fibres
isomorphic to those of P by a map pulling eta back to eta, so the period
verdict of P and P o phi must agree.  The first attempt at this control
compared EXACT-HE verdicts, but the shear (x, y) -> (x + s(y), y) RAISES deg_y,
so EXACT-HE stopped applying to the sheared member and the comparison was
vacuous.  Here both members are measured with NUM-MONO, which applies to any
deg_y, and the base member is also measured with its exact instrument.
"""

import json
import os
import sys
from fractions import Fraction as F

import pk15 as P14
import mono15
import exact_he15
import exact_g1_15
import gen15

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    rows = []
    CASES = [
        ("G1 n=1 m=2", gen15.G1(F(1), F(1), F(0), 1, 2, {0: F(2)})[0], 1, 2),
        ("G1 n=2 m=2", gen15.G1(F(1), F(1), F(0), 2, 2, {})[0], 2, 2),
        ("G1 n=1 m=3", gen15.G1(F(-1), F(1), F(0), 1, 3, {})[0], 1, 3),
        ("G1 n=2 m=3", gen15.G1(F(1), F(2), F(0), 2, 3, {})[0], 2, 3),
    ]
    for lab, P, n, m in CASES:
        Ps = gen15.shear(P, {1: F(1), 2: F(-1)}, {1: F(2), 0: F(1)})
        g1 = exact_g1_15.screen(n, m)
        he = exact_he15.screen(P, F(1)) if max(j for (i, j) in P) == 2 else {}
        r0 = mono15.screen_fibre_checked(P, F(1))
        r1 = mono15.screen_fibre_checked(Ps, F(1))
        row = {"label": lab, "deg_base": P14.tdeg(P), "deg_sheared": P14.tdeg(Ps),
               "deg_y_base": max(j for (i, j) in P),
               "deg_y_sheared": max(j for (i, j) in Ps),
               "EXACT_G1": g1["verdict"], "EXACT_HE": he.get("verdict"),
               "NUM_base": r0["verdict"], "NUM_sheared": r1["verdict"],
               "ls_base": r0["ls_residual"], "ls_sheared": r1["ls_residual"],
               "genus_base": r0["genus_sum"], "genus_sheared": r1["genus_sum"],
               "punct_base": r0["n_punctures"], "punct_sheared": r1["n_punctures"]}
        row["match"] = (row["NUM_base"] == row["NUM_sheared"] == row["EXACT_G1"])
        rows.append(row)
        print("%-12s deg %2d -> %2d (deg_y %d -> %d)  EXACT-G1=%-14s EXACT-HE=%-14s "
              "NUM base=%-13s sheared=%-13s  MATCH=%s"
              % (lab, row["deg_base"], row["deg_sheared"], row["deg_y_base"],
                 row["deg_y_sheared"], row["EXACT_G1"], row["EXACT_HE"],
                 row["NUM_base"], row["NUM_sheared"], row["match"]))
        sys.stdout.flush()
    json.dump(rows, open(os.path.join(HERE, "controls15c.json"), "w"),
              indent=1, default=str)
    print("\nall match:", all(r["match"] for r in rows))


if __name__ == "__main__":
    main()
