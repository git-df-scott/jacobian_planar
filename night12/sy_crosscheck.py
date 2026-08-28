"""night12 v1 -- independent cross-check on the Shpilrain-Yu verdicts.

This does NOT feed any decision and does not touch sy.py.  The SY certificate
algorithm is frozen; this file only measures a second, logically independent
necessary condition and reports where the two agree.

The condition.  If P is a coordinate then some automorphism carries P to x,
and x - c is irreducible for every constant c; irreducibility is preserved by
an automorphism of the polynomial ring, so

    P a coordinate  ==>  P - c is irreducible for every c in Qbar.

Contrapositive: exhibiting a single c for which P - c FACTORS is a proof that
P is not a coordinate.  It is one-sided -- failing to find such a c proves
nothing -- so the check reports REDUCIBLE_FIBRE_c (a non-coordinate proof) or
NO_FACTORISATION_FOUND (no information).

Factorisation is done by Singular over Q in ring 0,(x,y),dp.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import screens
import sy

CVALS = [0, 1, -1, 2, -2]


def fibre_factors(P, c, timeout=120):
    """number of irreducible factors of P - c over Q, counted without
    multiplicity, ignoring the unit factor Singular puts first."""
    s = """ring r = 0,(x,y),dp;
poly F = %s - (%d);
list L = factorize(F);
int i; int n = 0; string s = "";
for (i = 1; i <= size(L[1]); i++) {
  if (deg(L[1][i]) > 0) { n = n + L[2][i]; s = s + string(L[1][i]) + " | "; }
}
"NFACT:" + string(n);
"FACT:" + s;
quit;
""" % (screens.poly_str(P), c)
    out, rc = screens._singular(s, timeout)
    if out is None:
        return None, "timeout"
    n = None
    fs = ""
    for line in out.splitlines():
        if line.startswith("NFACT:"):
            n = int(line[6:])
        if line.startswith("FACT:"):
            fs = line[5:].strip()
    return n, fs


def crosscheck(P, timeout=120):
    for c in CVALS:
        n, fs = fibre_factors(P, c, timeout)
        if n is None:
            continue
        if n >= 2:
            return "REDUCIBLE_FIBRE", {"c": c, "n_factors": n, "factors": fs}
    return "NO_FACTORISATION_FOUND", {"c_tried": CVALS}


def main():
    rows = []
    print("independent cross-check: reducible fibre => NON_COORDINATE")
    print("(one-sided; NO_FACTORISATION_FOUND carries no information)\n")
    for name, P, brief in sy.VALIDATION:
        v, _ = sy.certify(P)
        cc, det = crosscheck(P)
        agree = ("-" if cc == "NO_FACTORISATION_FOUND"
                 else ("agrees" if v == "NON_COORDINATE" else "DISAGREES"))
        print("  %-28s SY=%-16s brief=%-16s fibre=%-24s %s"
              % (name, v, brief, cc, agree))
        if cc == "REDUCIBLE_FIBRE":
            print("        P - (%s) = %s" % (det["c"], det["factors"]))
        rows.append({"name": name, "SY": v, "brief_label": brief,
                     "fibre_check": cc, "detail": det, "agreement": agree})
    json.dump(rows, open(os.path.join(HERE, "sy_crosscheck.json"), "w"), indent=1)
    dis = [r for r in rows if r["agreement"] == "DISAGREES"]
    print("\nDISAGREEMENTS: %d" % len(dis))
    return 1 if dis else 0


if __name__ == "__main__":
    sys.exit(main())
