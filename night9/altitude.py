"""night9 — the redirected accumulator: votes at legal altitude.

Measurements only.  Every result is labelled with its characteristic or with
the ring it was computed in.  No assessment of what any of these numbers mean
is offered anywhere in this file.

DESIGN RATIONALE AS HANDED DOWN (recorded verbatim as the reason this sweep
was scoped the way it is, not as a finding of this lane): supports whose
maximum total degree is below 125 are excluded, on the stated ground that a
published bound rules out a characteristic-zero object at such degrees, so
multi-prime hits there are residual-divisibility coincidences; the sweep is
therefore restricted to maximum total degree in [126, 160].

WHAT IS SWEPT.  Sparse support pairs (S_P, S_Q), 5 to 8 monomials each,
generated with seed 20260830, subject to:

  * (1,0) in S_P and (0,1) in S_Q;
  * each of S_P, S_Q contains at least one PURE monomial (one exponent zero)
    of total degree >= 100 and at least one MIXED monomial (both exponents
    strictly positive) of total degree >= 100;
  * max over both supports of the total degree lies in [126, 160].

WHAT IS COMPUTED, at p = 2 and p = 3 ONLY.  The (K)+(C) system of
night9/README.md, solved by the complete `exhaustive-bilinear` method (the
system is linear in the coefficients of one side once the other side is
fixed; the smaller side is enumerated inside its own collision subspace, so
the reported count is exact and every F_p point is visited).  For every
NONEMPTY cell: the complete solution set, the additive degeneracy screen,
direct-substitution verification of a sample, and the tear class mod p
(TEAR-NOT-COMPUTED where tear.py's Sylvester caps bite).

THE QUANTITY OF INTEREST.  For each support that is NONEMPTY at BOTH p = 2
and p = 3, every pair (s2, s3) of NON-DEGENERATE solutions with the SAME
zero/non-zero coefficient pattern is CRT-combined coefficient-wise to a
balanced integer lift mod 6 (representatives in (-3, 3]), and the residual

    R(x,y) = P_x Q_y - P_y Q_x - 1   computed EXACTLY OVER Z

is recorded together with the factorisation of its integer content and the
two collision differences over Z.  Recorded flags: whether R is identically
zero, and whether both collision differences vanish over Z.

Outputs: night9/altitude.csv, night9/altitude/<hash>.json.
"""
import csv
import json
import os
import random
import sys
import time
from math import gcd

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from keller_solver import exhaustive, verify_solution, degenerate_screen  # noqa: E402
from tear import tear_data                                               # noqa: E402
from census import all_solutions                                         # noqa: E402
from survey import shash                                                 # noqa: E402

SEED = 20260830
N_SUPPORTS = 60
PRIMES = [2, 3]
DEG_LO, DEG_HI = 126, 160
HIGH = 100                    # threshold for "high-degree" in the generator
BUDGET = 10 ** 7
CAP = 20000
SAMPLE = 8                    # solutions verified / tear-classified per cell
PAIR_CAP = 4000               # matched (p=2, p=3) pairs examined per support

X, Y = sp.symbols("x y")

FIELDS = ["hash", "p", "nP", "nQ", "n", "max_total_degree", "method",
          "n_enum", "verdict", "count", "truncated", "n_degenerate",
          "n_nondegenerate", "n_sampled", "n_verify_fail", "tear_nonempty",
          "tear_empty", "tear_other", "wall_s", "note"]


# ------------------------------------------------------------- generation

def gen_support(rng, is_P):
    """One support: 5..8 monomials meeting the stated shape constraints."""
    k = rng.randint(5, 8)
    anchor = (1, 0) if is_P else (0, 1)
    S = {anchor}
    # one high-degree pure monomial
    dpure = rng.randint(HIGH, DEG_HI)
    S.add((dpure, 0) if rng.random() < 0.5 else (0, dpure))
    # one high-degree mixed monomial
    dmix = rng.randint(HIGH, DEG_HI)
    i = rng.randint(1, dmix - 1)
    S.add((i, dmix - i))
    while len(S) < k:
        d = rng.randint(2, DEG_HI)
        if rng.random() < 0.45:
            m = (d, 0) if rng.random() < 0.5 else (0, d)
        else:
            i = rng.randint(1, d - 1)
            m = (i, d - i)
        S.add(m)
    return sorted(S)


def gen_pair(rng):
    for _ in range(4000):
        SP = gen_support(rng, True)
        SQ = gen_support(rng, False)
        D = max(m[0] + m[1] for m in SP + SQ)
        if DEG_LO <= D <= DEG_HI and 5 <= len(SP) <= 8 and 5 <= len(SQ) <= 8:
            return SP, SQ, D
    raise RuntimeError("generator failed")


# ------------------------------------------------------------ exact over Z

def residual_over_Z(SP, SQ, a, b):
    """Exact integer residual P_x Q_y - P_y Q_x - 1 and the collisions."""
    P = sum(int(c) * X ** m[0] * Y ** m[1] for m, c in zip(SP, a))
    Q = sum(int(c) * X ** n[0] * Y ** n[1] for n, c in zip(SQ, b))
    R = sp.expand(sp.diff(P, X) * sp.diff(Q, Y) - sp.diff(P, Y) * sp.diff(Q, X) - 1)
    pd = sp.Poly(R, X, Y) if R != 0 else None
    coeffs = [int(c) for c in pd.coeffs()] if pd is not None else []
    content = 0
    for c in coeffs:
        content = gcd(content, abs(c))
    fac = sp.factorint(content) if content > 1 else {}
    cP = sum(int(c) for m, c in zip(SP, a) if m[0] == 0) - \
        sum(int(c) for m, c in zip(SP, a) if m[1] == 0)
    cQ = sum(int(c) for n, c in zip(SQ, b) if n[0] == 0) - \
        sum(int(c) for n, c in zip(SQ, b) if n[1] == 0)
    return {
        "residual_is_identically_zero": R == 0,
        "residual_n_terms": len(coeffs),
        "residual_str": str(R)[:4000],
        "residual_content": content,
        "residual_content_factorization":
            {str(q): int(e) for q, e in fac.items()},
        "residual_content_n_distinct_primes": len(fac),
        "residual_content_n_prime_factors_with_multiplicity":
            sum(fac.values()),
        "collision_P_diff_over_Z": cP,
        "collision_Q_diff_over_Z": cQ,
        "collisions_hold_over_Z": cP == 0 and cQ == 0,
    }


def balanced(r, m):
    r %= m
    return r - m if 2 * r > m else r


# -------------------------------------------------------------- one cell

def run_cell(SP, SQ, p, h, D):
    t0 = time.time()
    rec = {"hash": h, "p": p, "nP": len(SP), "nQ": len(SQ),
           "n": len(SP) + len(SQ), "max_total_degree": D,
           "method": "exhaustive-bilinear", "truncated": False}
    ex = exhaustive(SP, SQ, p, budget=BUDGET, max_solutions=SAMPLE)
    rec["n_enum"] = ex["n_enum"]
    if not ex["feasible"]:
        rec["verdict"] = "NOT-ATTEMPTED"
        rec["note"] = "p^nfree = %d exceeds budget %d" % (ex["n_enum"], BUDGET)
        rec["wall_s"] = round(time.time() - t0, 2)
        return rec, []
    rec["count"] = ex["count"]
    rec["verdict"] = "NONEMPTY" if ex["count"] > 0 else "EMPTY"
    nd = []
    if rec["verdict"] == "NONEMPTY":
        sols, trunc = all_solutions(SP, SQ, p, cap=CAP)
        rec["truncated"] = trunc
        nd = [s for s in sols if not degenerate_screen(SP, SQ, s[0], s[1])[0]]
        rec["n_degenerate"] = len(sols) - len(nd)
        rec["n_nondegenerate"] = len(nd)
        tc = {"TEAR-NONEMPTY": 0, "TEAR-EMPTY": 0}
        other = nfail = nsamp = 0
        for (a, b) in nd[:SAMPLE]:
            chk = verify_solution(SP, SQ, a, b, p)
            if not (chk["det_ok"] and chk["coll_ok"]):
                nfail += 1
                continue
            nsamp += 1
            k = tear_data(SP, SQ, a, b, p)["tear"]
            if k in tc:
                tc[k] += 1
            else:
                other += 1
        rec.update({"n_sampled": nsamp, "n_verify_fail": nfail,
                    "tear_nonempty": tc["TEAR-NONEMPTY"],
                    "tear_empty": tc["TEAR-EMPTY"], "tear_other": other})
    rec["wall_s"] = round(time.time() - t0, 2)
    return rec, nd


def pattern(a, b):
    return (tuple(i for i, v in enumerate(a) if v != 0),
            tuple(j for j, v in enumerate(b) if v != 0))


def main():
    outdir = os.path.join(HERE, "altitude")
    os.makedirs(outdir, exist_ok=True)
    rng = random.Random(SEED)
    pairs = [gen_pair(rng) for _ in range(N_SUPPORTS)]

    cpath = os.path.join(HERE, "altitude.csv")
    done = set()
    if os.path.exists(cpath):
        for r in csv.DictReader(open(cpath)):
            done.add((r["hash"], int(r["p"])))
    newf = not os.path.exists(cpath)
    fh = open(cpath, "a", newline="")
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    if newf:
        w.writeheader()

    for idx, (SP, SQ, D) in enumerate(pairs):
        h = shash(SP, SQ)
        jpath = os.path.join(outdir, "%s.json" % h)
        if all((h, p) in done for p in PRIMES) and os.path.exists(jpath):
            continue
        per = {}
        recs = {}
        for p in PRIMES:
            rec, nd = run_cell(SP, SQ, p, h, D)
            recs[p] = rec
            per[p] = nd
            if (h, p) not in done:
                w.writerow(rec)
                fh.flush()
            print("[%2d/%d] %s D=%3d n=%d p=%d %-9s cnt=%-6s nondeg=%-6s %.1fs"
                  % (idx + 1, N_SUPPORTS, h, D, len(SP) + len(SQ), p,
                     rec["verdict"], str(rec.get("count", "")),
                     str(rec.get("n_nondegenerate", "")), rec["wall_s"]),
                  flush=True)

        # ---- the quantity of interest: matched (p=2, p=3) lifts over Z
        lifts = []
        pat2, pat3 = {}, {}
        for (a, b) in per.get(2, []):
            pat2.setdefault(pattern(a, b), []).append((a, b))
        for (a, b) in per.get(3, []):
            pat3.setdefault(pattern(a, b), []).append((a, b))
        shared = sorted(set(pat2) & set(pat3))
        npairs = 0
        truncated_pairs = False
        for pat in shared:
            for c2 in pat2[pat]:
                for c3 in pat3[pat]:
                    if npairs >= PAIR_CAP:
                        truncated_pairs = True
                        break
                    npairs += 1
                    # CRT mod 6, balanced representatives in (-3, 3]
                    aZ = [balanced((3 * (u % 2) + 4 * (v % 3)) % 6, 6)
                          for u, v in zip(c2[0], c3[0])]
                    bZ = [balanced((3 * (u % 2) + 4 * (v % 3)) % 6, 6)
                          for u, v in zip(c2[1], c3[1])]
                    z = residual_over_Z(SP, SQ, aZ, bZ)
                    z.update({
                        "label": "CANDIDATE-UNVERIFIED",
                        "support_pattern": {"P_nonzero_indices": list(pat[0]),
                                            "Q_nonzero_indices": list(pat[1])},
                        "p2_solution": {"characteristic": 2,
                                        "a": list(map(int, c2[0])),
                                        "b": list(map(int, c2[1]))},
                        "p3_solution": {"characteristic": 3,
                                        "a": list(map(int, c3[0])),
                                        "b": list(map(int, c3[1]))},
                        "balanced_lift_mod_6": {"a": aZ, "b": bZ},
                    })
                    lifts.append(z)
                if truncated_pairs:
                    break
            if truncated_pairs:
                break
        lifts.sort(key=lambda z: (-z["residual_content_n_distinct_primes"],
                                  z["residual_n_terms"]))
        with open(jpath, "w") as g:
            json.dump({
                "hash": h, "max_total_degree": D,
                "support_P": [list(m) for m in SP],
                "support_Q": [list(m) for m in SQ],
                "primes": PRIMES,
                "per_prime": {str(p): {k: v for k, v in recs[p].items()}
                              for p in PRIMES},
                "n_shared_support_patterns": len(shared),
                "n_matched_pairs_examined": npairs,
                "matched_pair_list_truncated": truncated_pairs,
                "everything_below_is_labelled": "CANDIDATE-UNVERIFIED",
                "matched_lifts_over_Z": lifts[:200],
            }, g, indent=1)
        if lifts:
            best = lifts[0]
            print("      shared patterns=%d pairs=%d  best content=%s (%d distinct primes)  zero=%s"
                  % (len(shared), npairs, best["residual_content"],
                     best["residual_content_n_distinct_primes"],
                     best["residual_is_identically_zero"]), flush=True)
    fh.close()


if __name__ == "__main__":
    main()
