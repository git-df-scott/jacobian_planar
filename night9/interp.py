"""night9 — coefficient-wise CRT interpolation across primes.

Triggered by the cross-prime matrix: the support

    hash 9fad1aac9556
    S_P = {(0,10), (1,0), (2,1), (3,0)}      P = a0 y^10 + a1 x + a2 x^2 y + a3 x^3
    S_Q = {(0,1),  (2,1), (3,10), (4,0)}     Q = b0 y  + b1 x^2 y + b2 x^3 y^10 + b3 x^4

is the one support of the twelve that is non-degenerate NONEMPTY at three or
more distinct primes (p = 2, 3, 5).

MATCHING CRITERION (documented, applied before any lifting).  Two solutions at
two different primes are MATCHED when

  (M1) they have the same zero/nonzero coefficient pattern, i.e. the same
       effective support inside (S_P, S_Q);  and
  (M2) their collision images agree in pattern: P(0,1) vanishes at one prime
       iff it vanishes at the other, and likewise for Q(0,1).  (P(0,1) = P(1,0)
       and Q(0,1) = Q(1,0) hold by the (C) equations, so one of each pair
       suffices.)

A MATCHED TRIPLE is one solution from each of p = 2, 3, 5 that are pairwise
matched.  For each matched triple the nine coefficients are lifted
coefficient-wise by the Chinese Remainder Theorem to residues modulo
M = 2*3*5 = 30, and two reconstructions are attempted:

  * BALANCED-INTEGER: the representative in (-M/2, M/2];
  * RATIONAL: Wang rational reconstruction of each coefficient with the
    standard bound floor(sqrt(M/2)) = 3 on numerator and denominator.

Every reconstruction produced is then verified EXACTLY over Q, with exact
rational arithmetic: `P_x Q_y - P_y Q_x - 1 = 0` as an identity in Q[x,y], and
`P(0,1) = P(1,0)`, `Q(0,1) = Q(1,0)`.  Reconstructions are written out and
labelled CANDIDATE-UNVERIFIED regardless of the outcome of that check; the
exact residual is recorded alongside.

Output: night9/interp/<hash>.json and night9/interp/CRT_NOTES.md.
"""
import json, os, sys, itertools
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from census import all_solutions
from keller_solver import degenerate_screen, verify_solution
from tear import tear_data

HASH = "9fad1aac9556"
PRIMES = [2, 3, 5]


# ------------------------------------------------------- exact Q arithmetic
def det_minus_one_Q(SP, SQ, a, b):
    """P_x Q_y - P_y Q_x - 1 over Q, as a dict of nonzero coefficients."""
    d = {}
    for i, m in enumerate(SP):
        for j, n in enumerate(SQ):
            c = m[0] * n[1] - m[1] * n[0]
            if c == 0:
                continue
            v = Fraction(c) * a[i] * b[j]
            if v == 0:
                continue
            e = (m[0] + n[0] - 1, m[1] + n[1] - 1)
            d[e] = d.get(e, Fraction(0)) + v
    d[(0, 0)] = d.get((0, 0), Fraction(0)) - 1
    return {k: v for k, v in d.items() if v != 0}


def eval_Q(S, coef, x, y):
    s = Fraction(0)
    for i, (e0, e1) in enumerate(S):
        s += coef[i] * (Fraction(x) ** e0 if e0 else Fraction(1)) * \
             (Fraction(y) ** e1 if e1 else Fraction(1))
    return s


def verify_Q(SP, SQ, a, b):
    res = det_minus_one_Q(SP, SQ, a, b)
    P01 = eval_Q(SP, a, 0, 1); P10 = eval_Q(SP, a, 1, 0)
    Q01 = eval_Q(SQ, b, 0, 1); Q10 = eval_Q(SQ, b, 1, 0)
    return {
        "det_J_minus_1_residual_over_Q":
            {"x^%d y^%d" % k: str(v) for k, v in sorted(res.items())},
        "det_ok_over_Q": len(res) == 0,
        "P_at_0_1": str(P01), "P_at_1_0": str(P10),
        "Q_at_0_1": str(Q01), "Q_at_1_0": str(Q10),
        "coll_ok_over_Q": (P01 == P10) and (Q01 == Q10),
    }


# ------------------------------------------------------------- CRT / Wang
def crt(res, mods):
    M = 1
    for m in mods:
        M *= m
    x = 0
    for r, m in zip(res, mods):
        Mi = M // m
        x += r * Mi * pow(Mi, -1, m)
    return x % M, M


def balanced(r, M):
    return r - M if r > M // 2 else r


def wang(r, M):
    """Rational reconstruction of r mod M with |n|,d <= floor(sqrt(M/2))."""
    B = int((M // 2) ** 0.5)
    r0, r1 = M, r % M
    s0, s1 = 0, 1
    while r1 > B:
        q = r0 // r1
        r0, r1 = r1, r0 - q * r1
        s0, s1 = s1, s0 - q * s1
    if s1 == 0 or abs(s1) > B:
        return None
    n, d = r1, s1
    if d < 0:
        n, d = -n, -d
    if d == 0 or abs(n) > B or d > B:
        return None
    from math import gcd
    if gcd(abs(n), d) != 1:
        return None
    return Fraction(n, d)


# ------------------------------------------------------------------ main
def main():
    outdir = os.path.join(HERE, "interp")
    os.makedirs(outdir, exist_ok=True)
    d = json.load(open(os.path.join(HERE, "supports", HASH + ".json")))
    SP = [tuple(m) for m in d["support_P"]]
    SQ = [tuple(m) for m in d["support_Q"]]

    per = {}
    for p in PRIMES:
        sols, trunc = all_solutions(SP, SQ, p, cap=200000)
        nd = []
        for (a, b) in sols:
            if degenerate_screen(SP, SQ, a, b)[0]:
                continue
            chk = verify_solution(SP, SQ, a, b, p)
            assert chk["det_ok"] and chk["coll_ok"]
            nd.append({"a": a, "b": b,
                       "pattern": [1 if z else 0 for z in a] +
                                  [1 if z else 0 for z in b],
                       "image_0_1": chk["image_0_1"],
                       "image_1_0": chk["image_1_0"],
                       "tear": tear_data(SP, SQ, a, b, p)["tear"]})
        per[p] = {"total_solutions": len(sols), "truncated": trunc,
                  "non_degenerate": nd}
        print("p=%d  total=%d  non-degenerate=%d" % (p, len(sols), len(nd)))

    # matched triples
    triples = []
    for s2 in per[2]["non_degenerate"]:
        for s3 in per[3]["non_degenerate"]:
            if s3["pattern"] != s2["pattern"]:
                continue
            if [z == 0 for z in s3["image_0_1"]] != [z == 0 for z in s2["image_0_1"]]:
                continue
            for s5 in per[5]["non_degenerate"]:
                if s5["pattern"] != s2["pattern"]:
                    continue
                if [z == 0 for z in s5["image_0_1"]] != [z == 0 for z in s2["image_0_1"]]:
                    continue
                triples.append((s2, s3, s5))
    print("matched triples:", len(triples))

    recon = []
    for (s2, s3, s5) in triples:
        vec = [(s2["a"] + s2["b"]), (s3["a"] + s3["b"]), (s5["a"] + s5["b"])]
        res, M = [], 30
        crtvec = []
        for k in range(len(vec[0])):
            r, M = crt([vec[0][k], vec[1][k], vec[2][k]], PRIMES)
            crtvec.append(r)
        entry = {"triple": {"p2": {"a": s2["a"], "b": s2["b"], "tear": s2["tear"]},
                            "p3": {"a": s3["a"], "b": s3["b"], "tear": s3["tear"]},
                            "p5": {"a": s5["a"], "b": s5["b"], "tear": s5["tear"]}},
                 "pattern": s2["pattern"],
                 "crt_residues_mod_30": crtvec,
                 "modulus": M}
        nA = len(SP)
        # (1) balanced integer lift
        bal = [balanced(r, M) for r in crtvec]
        a = [Fraction(z) for z in bal[:nA]]
        b = [Fraction(z) for z in bal[nA:]]
        entry["BALANCED-INTEGER"] = {
            "label": "CANDIDATE-UNVERIFIED",
            "a": [str(z) for z in a], "b": [str(z) for z in b],
            "exact_check_over_Q": verify_Q(SP, SQ, a, b)}
        # (2) rational reconstruction
        rat = [wang(r, M) for r in crtvec]
        if all(z is not None for z in rat):
            a = rat[:nA]; b = rat[nA:]
            entry["RATIONAL"] = {
                "label": "CANDIDATE-UNVERIFIED",
                "a": [str(z) for z in a], "b": [str(z) for z in b],
                "exact_check_over_Q": verify_Q(SP, SQ, a, b)}
        else:
            entry["RATIONAL"] = {"status": "NO-RECONSTRUCTION",
                                 "reason": "at least one coefficient has no "
                                           "n/d with |n|,d <= floor(sqrt(15))=3"
                                           " congruent to it mod 30"}
        recon.append(entry)

    npass = sum(1 for e in recon
                for k in ("BALANCED-INTEGER", "RATIONAL")
                if isinstance(e.get(k), dict)
                and e[k].get("exact_check_over_Q", {}).get("det_ok_over_Q")
                and e[k]["exact_check_over_Q"].get("coll_ok_over_Q"))
    out = {"hash": HASH,
           "support_P": [list(m) for m in SP], "support_Q": [list(m) for m in SQ],
           "P": "a0*y^10 + a1*x + a2*x^2*y + a3*x^3",
           "Q": "b0*y + b1*x^2*y + b2*x^3*y^10 + b3*x^4",
           "primes": PRIMES, "modulus": 30,
           "matching_criterion": [
               "M1: identical zero/nonzero coefficient pattern",
               "M2: collision images agree in vanishing pattern"],
           "per_prime": per,
           "n_matched_triples": len(triples),
           "reconstructions": recon,
           "n_reconstructions_verified_exactly_over_Q": npass}
    with open(os.path.join(outdir, HASH + ".json"), "w") as f:
        json.dump(out, f, indent=1)
    print("reconstructions:", len(recon),
          " verified exactly over Q:", npass)


if __name__ == "__main__":
    main()
