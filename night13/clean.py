"""night13 -- structural singleton census of the (84,126) prestratum carrier.

The acceptance rule of the recipe -- every mandatory nonconstant bracket row
is either an identity row from [H^2, H^3] = 0 or carries at least two
adjustable contributing coefficients -- is tested here at the level of the
MAXIMAL carrier, i.e. with every admissible lattice point of both Newton
polygons present.

A row key k can only ever be reached by pairs (p, a) with p + a = k + (1,1),
p in the P-pool, a in the Q-pool, and p1 a2 - p2 a1 != 0.  Over the maximal
carrier this set is as large as it can be, so a row that is singleton there is
singleton for EVERY sub-carrier: adding monomials cannot repair it.  Such a
row can only be repaired by REMOVING the lower monomial in its unique pair.

Two of the lower monomials are protected and can never be removed:

    x = (1,0) in C_P and y = (0,1) in C_Q

are the unique route to the constant bracket row (mu_3 forbids the other
route P-(0,1) x Q-(1,0)), so dropping either makes the Keller constant
unreachable.  The leading-form monomials supp(H^2), supp(H^3) are likewise
fixed by the ansatz.  A structurally singleton row whose unique pair consists
of a protected lower monomial and a leading-form monomial is therefore
UNREPAIRABLE, and its presence is a rejection certificate for the carrier
that does not depend on which lower monomials are selected.

Output: night13/structural.json.
"""

import json
import os

import kit as K
import prestratum as PS

HERE = os.path.dirname(os.path.abspath(__file__))
PROT_P = {(1, 0)}
PROT_Q = {(0, 1)}


def incidence(Ptop, Qtop, Ppool, Qpool):
    """cnt[key] = number of adjustable contributing pairs (a pair is
    adjustable iff at least one member is a lower monomial);
    one[key] = that unique pair when cnt == 1."""
    cnt, one = {}, {}
    Ps, Qs = set(Ppool), set(Qpool)
    for m in list(Ptop) + list(Ppool):
        lowP = m in Ps
        for a in list(Qtop) + list(Qpool):
            lowQ = a in Qs
            if not (lowP or lowQ):
                continue
            f = PS.fac(m, a)
            if f == 0:
                continue
            k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
            c = cnt.get(k, 0) + 1
            cnt[k] = c
            if c == 1:
                one[k] = (m, lowP, a, lowQ, f)
            elif k in one:
                del one[k]
    return cnt, one


def classify(sing):
    """Split the structurally singleton mandatory rows into repairable ones
    (the lower monomial of the pair may be dropped from the pool) and
    unrepairable ones (the lower monomial is protected)."""
    rep, unrep = {}, {}
    for k, (m, lowP, a, lowQ, f) in sing.items():
        prot = ((lowP and m in PROT_P and not lowQ)
                or (lowQ and a in PROT_Q and not lowP)
                or (lowP and lowQ and m in PROT_P and a in PROT_Q))
        (unrep if prot else rep)[k] = (m, lowP, a, lowQ, f)
    return rep, unrep


def main():
    cp, cq, hp, hq, SP, SQ = PS.candidates()
    cnt, one = incidence(SP, SQ, cp, cq)
    sing = {k: v for k, v in one.items() if k != (0, 0)}
    rep, unrep = classify(sing)

    def row(k, v):
        m, lowP, a, lowQ, f = v
        return {"row_key": list(k),
                "P_monomial": list(m), "P_kind": "lower" if lowP else "LEADING",
                "Q_monomial": list(a), "Q_kind": "lower" if lowQ else "LEADING",
                "factor_p1a2_minus_p2a1": f}

    out = {
        "pool_P": len(cp), "pool_Q": len(cq),
        "n_rows_over_maximal_carrier": len(cnt),
        "constant_row_adjustable_pairs": cnt.get((0, 0), 0),
        "n_structural_singleton_mandatory": len(sing),
        "n_repairable_by_removal": len(rep),
        "n_unrepairable": len(unrep),
        "unrepairable_rows": [row(k, sing[k]) for k in sorted(unrep)],
        "repairable_rows": [row(k, sing[k]) for k in sorted(rep)],
    }

    # The two equations these unrepairable rows impose, written out.  The
    # leading-form coefficients are A*h2^2 = A at (4,80) and B*h41^3 at
    # (123,3); the chart is h2 = 1.
    out["constant_row_equation"] = "a_(1,0) * b_(0,1) = 1"
    out["forced_equations"] = []
    for k in sorted(unrep):
        m, lowP, a, lowQ, f = sing[k]
        cP = "a_%s" % (str(m),) if lowP else ("A" if m == (4, 80)
                                              else "c_H2_%s" % (str(m),))
        cQ = "b_%s" % (str(a),) if lowQ else ("B*h41^3" if a == (123, 3)
                                              else "c_H3_%s" % (str(a),))
        out["forced_equations"].append(
            {"row_key": list(k), "equation": "%d * %s * %s = 0" % (f, cP, cQ)})
    with open(os.path.join(HERE, "structural.json"), "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: v for k, v in out.items()
                      if k != "repairable_rows"}, indent=1))


if __name__ == "__main__":
    main()
