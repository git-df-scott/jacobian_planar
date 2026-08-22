#!/usr/bin/env python3
"""Controls and first exact probes for the p_1_1=0, p_1_0!=0 chart."""

import random
import sys

from pentagon_core import (
    AFFINE_VARS,
    EARLY_VARS,
    VARS,
    affine_system,
    bracket_residual,
    exported_conditions,
    insert_affine,
    recur_q,
    solve_affine,
    verify,
)


def check(label, condition, detail=""):
    print(f"{'PASS' if condition else 'FAIL'} {label}" + (f" -- {detail}" if detail else ""))
    if not condition:
        raise AssertionError(label)


def main(prime=43):
    print(f"p={prime}; {len(VARS)} exported variables; "
          f"{len(AFFINE_VARS)} affine + {len(EARLY_VARS)} early")

    rng = random.Random(20260822)
    point = {name: rng.randrange(prime) for name in VARS}
    point["p_1_1"] = 0
    point["p_1_0"] = 1

    # The recurrence must make the original bracket identity exact, independent
    # of whether the Newton-support conditions vanish.
    pfull, qfull = recur_q(point, prime, jmax=40)
    recurrence_residual = bracket_residual(pfull, qfull, prime, max_y=39)
    check("recurrence gives [P,Q]=x^2 exactly through y^39",
          not recurrence_residual, f"bracket residues={len(recurrence_residual)}")

    early = {name: point[name] for name in EARLY_VARS}
    M, v = affine_system(early, prime)
    chosen = [rng.randrange(prime) for _ in AFFINE_VARS]
    combined = insert_affine(early, chosen)
    _, q = recur_q(combined, prime)
    actual = exported_conditions(q, prime)
    predicted = [(v[r] + sum(M[r][c] * chosen[c]
                              for c in range(len(chosen)))) % prime
                 for r in range(len(v))]
    check("14-variable block is jointly affine", actual == predicted,
          f"{len(actual)}/{len(actual)} coordinates checked")

    # Positive control: plant a right-hand side in col(M).
    vpos = [(-sum(M[r][c] * chosen[c] for c in range(len(chosen)))) % prime
            for r in range(len(M))]
    rm, ra, ok, sol = solve_affine(M, vpos, prime)
    planted_ok = ok and sol is not None and all(
        (sum(M[r][c] * sol[c] for c in range(len(sol))) + vpos[r]) % prime == 0
        for r in range(len(M)))
    check("POS planted affine system is consistent and recovered", planted_ok,
          f"rank={rm}/{ra}")

    # Negative control: use a unit vector outside col(M), found deterministically.
    neg_ok = False
    neg_detail = ""
    for row in range(len(M)):
        vneg = vpos[:]
        vneg[row] = (vneg[row] + 1) % prime
        rm2, ra2, ok2, _ = solve_affine(M, vneg, prime)
        if not ok2:
            neg_ok = True
            neg_detail = f"row={row}, rank={rm2}/{ra2}"
            break
    check("NEG perturbed affine system is inconsistent", neg_ok, neg_detail)

    # The easy root of the 66 equations is deliberately rejected: it destroys
    # the exact Newton polygons and therefore cannot be a CE candidate.
    degenerate = {name: 0 for name in VARS}
    degenerate["p_1_0"] = 1
    degenerate["p_1_1"] = 0
    dcheck = verify(degenerate, prime)
    check("degenerate point solves the 66 exported equations", dcheck.exported_zero)
    check("degenerate point is rejected by vertex nonvanishing",
          not dcheck.vertices_nonzero, str(dcheck.vertices))

    # First coordinate-sparse probe: enforce the necessary P vertex p_8_0 != 0,
    # solve all 14 affine variables, and test every original condition.
    sparse = {name: 0 for name in EARLY_VARS}
    sparse["p_1_0"] = 1
    sparse["p_1_1"] = 0
    sparse["p_8_0"] = 1
    Ms, vs = affine_system(sparse, prime)
    rms, ras, oks, sols = solve_affine(Ms, vs, prime)
    print(f"SPARSE-BASE rank={rms}/{ras} consistent={oks}")
    if oks and sols is not None:
        candidate = insert_affine(sparse, sols)
        ccheck = verify(candidate, prime)
        print("SPARSE-BASE verification:", ccheck)
        if ccheck.candidate:
            print("MOD-p NONEMPTY -- CE LEAD")
            return 0

    print("VERDICT: NO VERDICT")
    return 0


if __name__ == "__main__":
    sys.exit(main(int(sys.argv[1]) if len(sys.argv) > 1 else 43))
