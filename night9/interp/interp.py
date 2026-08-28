"""night9 — CRT interpolation across the primes of a single support.

Measurements only.  This script takes ONE support hash together with the list
of primes at which the cross-prime matrix recorded NON-DEGENERATE NONEMPTY,
enumerates the COMPLETE non-degenerate solution set over F_p for each of those
primes, matches solutions across the primes by the criterion stated below,
CRT-combines each matched tuple coefficient-wise, attempts rational
reconstruction, and then verifies the produced coefficient vector EXACTLY over
Q by symbolic substitution.  Every produced object is written out labelled
CANDIDATE-UNVERIFIED regardless of whether the exact check over Q passed or
failed; the check's own boolean is recorded beside it.

THE MATCHING CRITERION (stated, not argued).  Two solutions at two different
primes are declared MATCHED when both of the following hold.

  (M1) SUPPORT PATTERN.  The zero/non-zero pattern of the coefficient vector
       is identical: {i : a_i != 0 in F_p} and {j : b_j != 0 in F_p} agree
       across the primes.

  (M2) COLLISION IMAGE.  The two collision values
           v_P = P(0,1) = P(1,0)  and  v_Q = Q(0,1) = Q(1,0)
       (equal by (C), computed with 0^0 = 1) are simultaneously congruent to a
       single pair of integers in the symmetric range mod M = prod p, i.e. the
       coefficient-wise CRT lift of the tuple has collision values reducing to
       v_P, v_Q at every prime.  Because v_P and v_Q are integer-linear in the
       coefficients, (M2) is implied by the coefficient-wise CRT and is
       recorded as a check, not used to prune.

A MATCHED TUPLE is one solution per prime satisfying (M1); coefficient-wise
CRT then gives a residue mod M = prod of the primes.  Two lifts are recorded
for each coefficient:

  (R1) the symmetric integer representative in (-M/2, M/2];
  (R2) rational reconstruction with numerator and denominator bounded by
       floor(sqrt(M/2)) (Wang), recorded as FAILED for that coefficient when
       no such rational exists.

Both lifts are then substituted exactly (sympy, rational arithmetic) into
    det J - 1 = P_x Q_y - P_y Q_x - 1
and into the two collision equalities.  Results go to
night9/interp/<hash>_interp.json and are summarised in
night9/interp/INTERP.md.

Usage:  python3 interp.py <hash> <p1> <p2> ...
"""
import itertools
import json
import os
import sys
from fractions import Fraction

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
NIGHT9 = os.path.dirname(HERE)
sys.path.insert(0, NIGHT9)

from census import all_solutions                      # noqa: E402
from keller_solver import degenerate_screen           # noqa: E402
from tear import tear_data                            # noqa: E402


# --------------------------------------------------------------- lifting

def crt_pair(r1, m1, r2, m2):
    g, x = 0, 0
    # extended gcd
    old_r, r = m1, m2
    old_s, s = 1, 0
    while r:
        q = old_r // r
        old_r, r = r, old_r - q * r
        old_s, s = s, old_s - q * s
    g, x = old_r, old_s
    assert g == 1, "primes must be coprime"
    m = m1 * m2
    return ((r1 + m1 * ((x * (r2 - r1)) % m2)) % m), m


def crt_list(residues, moduli):
    r, m = residues[0] % moduli[0], moduli[0]
    for r2, m2 in zip(residues[1:], moduli[1:]):
        r, m = crt_pair(r, m, r2, m2)
    return r, m


def sym_rep(r, m):
    """Symmetric integer representative of r mod m in (-m/2, m/2]."""
    r %= m
    return r - m if 2 * r > m else r


def rational_reconstruct(r, m):
    """Wang rational reconstruction with |num|, den <= floor(sqrt(m/2)).

    Returns a Fraction or None.
    """
    bound = int((m // 2) ** 0.5)
    while (bound + 1) * (bound + 1) * 2 <= m:
        bound += 1
    while bound * bound * 2 > m:
        bound -= 1
    r %= m
    u0, u1 = m, r
    v0, v1 = 0, 1
    while u1 > bound:
        q = u0 // u1
        u0, u1 = u1, u0 - q * u1
        v0, v1 = v1, v0 - q * v1
    num, den = u1, v1
    if den == 0:
        return None
    if den < 0:
        num, den = -num, -den
    if den > bound:
        return None
    from math import gcd
    if gcd(abs(num), den) != 1:
        return None
    if (num - r * den) % m != 0:
        return None
    return Fraction(num, den)


# ------------------------------------------------------- exact check / Q

X, Y = sp.symbols("x y")


def build_poly(S, coef):
    return sum(sp.Rational(c.numerator, c.denominator) * X ** m[0] * Y ** m[1]
               for m, c in zip(S, coef))


def exact_check_over_Q(SP, SQ, a, b):
    """a, b are lists of Fraction.  Exact symbolic verification over Q."""
    P = build_poly(SP, a)
    Q = build_poly(SQ, b)
    det = sp.expand(sp.diff(P, X) * sp.diff(Q, Y) - sp.diff(P, Y) * sp.diff(Q, X) - 1)
    det_ok = sp.simplify(det) == 0

    def ev(S, coef, x0, y0):
        t = 0
        for m, c in zip(S, coef):
            t += sp.Rational(c.numerator, c.denominator) * \
                (sp.Integer(1) if m[0] == 0 else sp.Integer(x0) ** m[0]) * \
                (sp.Integer(1) if m[1] == 0 else sp.Integer(y0) ** m[1])
        return sp.nsimplify(t)

    cP = ev(SP, a, 0, 1) - ev(SP, a, 1, 0)
    cQ = ev(SQ, b, 0, 1) - ev(SQ, b, 1, 0)
    return {"det_minus_one_identically_zero": bool(det_ok),
            "det_minus_one_residual": sp.srepr(sp.expand(det))
                                      if not det_ok else "0",
            "det_minus_one_residual_str": str(sp.expand(det)),
            "collision_P_diff": str(sp.simplify(cP)),
            "collision_Q_diff": str(sp.simplify(cQ)),
            "collision_ok": bool(sp.simplify(cP) == 0 and sp.simplify(cQ) == 0)}


# ------------------------------------------------------------- collision

def collision_values(S, coef, p):
    v01 = sum(c for m, c in zip(S, coef) if m[0] == 0) % p
    v10 = sum(c for m, c in zip(S, coef) if m[1] == 0) % p
    return v01 % p, v10 % p


# ------------------------------------------------------------------ main

def main():
    h = sys.argv[1]
    primes = [int(t) for t in sys.argv[2:]]
    d = json.load(open(os.path.join(NIGHT9, "supports", h + ".json")))
    SP = [tuple(m) for m in d["support_P"]]
    SQ = [tuple(m) for m in d["support_Q"]]

    per_prime = {}
    for p in primes:
        sols, trunc = all_solutions(SP, SQ, p)
        assert not trunc, "solution list truncated at p=%d" % p
        nd = [s for s in sols if not degenerate_screen(SP, SQ, s[0], s[1])[0]]
        per_prime[p] = nd
        print("p=%d  total=%d  non-degenerate=%d" % (p, len(sols), len(nd)))

    def pattern(a, b):
        return (tuple(i for i, v in enumerate(a) if v % 1e9 != 0),
                tuple(j for j, v in enumerate(b) if v != 0))

    # (M1): group by support pattern, keep patterns present at EVERY prime
    groups = {}
    for p in primes:
        for (a, b) in per_prime[p]:
            pat = (tuple(i for i, v in enumerate(a) if v != 0),
                   tuple(j for j, v in enumerate(b) if v != 0))
            groups.setdefault(pat, {}).setdefault(p, []).append((a, b))
    shared = {pat: g for pat, g in groups.items()
              if all(p in g for p in primes)}
    print("support patterns seen: %d ; present at all %d primes: %d"
          % (len(groups), len(primes), len(shared)))

    M = 1
    for p in primes:
        M *= p

    results = []
    for pat, g in sorted(shared.items()):
        for combo in itertools.product(*[g[p] for p in primes]):
            avecs = [c[0] for c in combo]
            bvecs = [c[1] for c in combo]
            a_int = [sym_rep(*crt_list([av[i] for av in avecs], primes))
                     for i in range(len(SP))]
            b_int = [sym_rep(*crt_list([bv[j] for bv in bvecs], primes))
                     for j in range(len(SQ))]
            a_rat, b_rat, rr_ok = [], [], True
            for i in range(len(SP)):
                r, m = crt_list([av[i] for av in avecs], primes)
                f = rational_reconstruct(r, m)
                if f is None:
                    rr_ok = False
                    f = Fraction(0)
                a_rat.append(f)
            for j in range(len(SQ)):
                r, m = crt_list([bv[j] for bv in bvecs], primes)
                f = rational_reconstruct(r, m)
                if f is None:
                    rr_ok = False
                    f = Fraction(0)
                b_rat.append(f)

            rec = {
                "label": "CANDIDATE-UNVERIFIED",
                "support_pattern": {"P_nonzero_indices": list(pat[0]),
                                    "Q_nonzero_indices": list(pat[1])},
                "primes": primes,
                "modulus": M,
                "matched_residues": [
                    {"p": p, "characteristic": p, "a": list(map(int, c[0])),
                     "b": list(map(int, c[1])),
                     "collision_P_(v01,v10)": list(collision_values(SP, c[0], p)),
                     "collision_Q_(v01,v10)": list(collision_values(SQ, c[1], p)),
                     "tear": tear_data(SP, SQ, c[0], c[1], p)["tear"]}
                    for p, c in zip(primes, combo)],
                "lift_R1_symmetric_integer": {"a": a_int, "b": b_int},
                "lift_R2_rational_reconstruction": {
                    "succeeded_for_every_coefficient": rr_ok,
                    "a": [str(f) for f in a_rat],
                    "b": [str(f) for f in b_rat]},
            }
            rec["exact_check_over_Q_R1"] = exact_check_over_Q(
                SP, SQ, [Fraction(v) for v in a_int],
                [Fraction(v) for v in b_int])
            if rr_ok:
                rec["exact_check_over_Q_R2"] = exact_check_over_Q(
                    SP, SQ, a_rat, b_rat)
            else:
                rec["exact_check_over_Q_R2"] = None
            # (M2) recorded as a check on the R1 lift
            m2 = []
            for p, c in zip(primes, combo):
                lp = collision_values(SP, [v % p for v in a_int], p)
                lq = collision_values(SQ, [v % p for v in b_int], p)
                m2.append({"p": p,
                           "R1_lift_reduces_to_same_collision_images":
                           list(lp) == list(collision_values(SP, c[0], p)) and
                           list(lq) == list(collision_values(SQ, c[1], p))})
            rec["criterion_M2_check"] = m2
            results.append(rec)

    out = {
        "hash": h,
        "support_P": [list(m) for m in SP],
        "support_Q": [list(m) for m in SQ],
        "primes_with_nondegenerate_NONEMPTY": primes,
        "modulus": M,
        "matching_criterion": (
            "(M1) identical zero/non-zero coefficient pattern across the "
            "primes; (M2) collision images (P(0,1)=P(1,0), Q(0,1)=Q(1,0), "
            "0^0=1) of the coefficient-wise CRT lift reduce to each prime's "
            "values -- recorded as a check, implied by coefficient-wise CRT."),
        "nondegenerate_counts": {str(p): len(per_prime[p]) for p in primes},
        "n_shared_support_patterns": len(shared),
        "n_matched_tuples": len(results),
        "everything_below_is_labelled": "CANDIDATE-UNVERIFIED",
        "matched_tuples": results,
    }
    path = os.path.join(HERE, "%s_interp.json" % h)
    with open(path, "w") as f:
        json.dump(out, f, indent=1)
    npass = sum(1 for r in results
                if r["exact_check_over_Q_R1"]["det_minus_one_identically_zero"]
                and r["exact_check_over_Q_R1"]["collision_ok"])
    npass2 = sum(1 for r in results
                 if r["exact_check_over_Q_R2"] is not None
                 and r["exact_check_over_Q_R2"]["det_minus_one_identically_zero"]
                 and r["exact_check_over_Q_R2"]["collision_ok"])
    print("matched tuples: %d ; R1 exact-over-Q pass: %d ; R2 exact-over-Q pass: %d"
          % (len(results), npass, npass2))
    print("written:", path)


if __name__ == "__main__":
    main()
