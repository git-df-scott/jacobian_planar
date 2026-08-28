"""night12 -- hard-gate controls C1..C4 for the mate search."""

import os
import sys
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import matekit as M
import sweep

HERE = os.path.dirname(os.path.abspath(__file__))


def probe(name, P, expect):
    rec = {"tag": "control_" + name, "arm": "control", "deg": M.pdeg(P), "P": P}
    r = sweep.run_one(rec)
    r["expect"] = expect
    r["P_str"] = str(sorted(P.items()))
    return r


def main():
    log = []
    out = []

    # C1  P = x  must be consistent and Q = y must be found
    r = probe("C1_P_eq_x", {(1, 0): 1}, "consistent")
    out.append(r)
    log.append("C1  P = x                      unknowns=%d  consistent(dual)=%d  exact=%s  Q=%s  deg pair=(%d,%d)"
               % (r["n_unknowns"], r["dual_prime_consistent"], r["exact_status"], r["Q"], r["deg"], r["deg_Q"]))

    # C2  P = x + y^2
    r = probe("C2_P_eq_x_plus_y2", {(1, 0): 1, (0, 2): 1}, "consistent")
    out.append(r)
    log.append("C2  P = x + y^2                unknowns=%d  consistent(dual)=%d  exact=%s  Q=%s  deg pair=(%d,%d)"
               % (r["n_unknowns"], r["dual_prime_consistent"], r["exact_status"], r["Q"], r["deg"], r["deg_Q"]))

    # C4  random dense P of degree 5 (ring: Q), coefficients from seed 20260831
    import random
    rnd = random.Random(20260831)
    Pd = {}
    for i in range(6):
        for j in range(6 - i):
            Pd[(i, j)] = rnd.randrange(-9, 10)
    Pd[(5, 0)] = 3
    Pd = {k: v for k, v in Pd.items() if v != 0}
    r = probe("C4_dense_deg5", Pd, "inconsistent")
    out.append(r)
    log.append("C4  dense deg-5 P (%d monomials)  unknowns=%d  rank_A/rank_[A|e] = %d/%d (p=999983), %d/%d (p=1000003)  consistent(dual)=%d"
               % (len(Pd), r["n_unknowns"], r["rank_A_p999983"], r["rank_Ae_p999983"],
                  r["rank_A_p1000003"], r["rank_Ae_p1000003"], r["dual_prime_consistent"]))

    # C0  structural: constant coefficient of the bracket is
    #     P[1,0] Q[0,1] - P[0,1] Q[1,0]; a P with no linear term cannot meet it
    r = probe("C0_no_linear_term", {(2, 0): 1, (0, 3): 1, (1, 1): 1}, "inconsistent")
    out.append(r)
    log.append("C0  P = x^2 + y^3 + xy (no linear term)  consistent(dual)=%d  (constant row of the bracket is P[1,0]Q[0,1]-P[0,1]Q[1,0])"
               % r["dual_prime_consistent"])

    with open(os.path.join(HERE, "controls.json"), "w") as f:
        json.dump(out, f, indent=1)
    txt = "\n".join(log) + "\n"
    with open(os.path.join(HERE, "controls_log.txt"), "w") as f:
        f.write(txt)
    print(txt)


if __name__ == "__main__":
    main()
