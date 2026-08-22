#!/usr/bin/env python3
"""PLANTED-SOLUTION CONTROL for the trackB1 variable-projection probe.

WHY
---
w6_tb1_rank.py reported "inconsistent at every probe". A negative result from
an unvalidated instrument is worth nothing: the campaign has already produced a
false [-1] from msolve on a malformed export, and the case-(2) planted control
returned halt 1 / exit 124, i.e. it could not even be RUN at scale -- so that
control never actually validated anything.

This control CAN be run, because the probe is linear algebra, not Groebner.

WHAT IT DOES
------------
Takes the real A(d,s), b(d,s) at a random parameter point. The true b is not in
the column space of A (that is the finding). So plant one: choose c0 at random
and REPLACE b by A.c0. Now a solution provably exists, by construction.

The probe must then report CONSISTENT and must recover a c with A.c = A.c0.
If it reports inconsistent on a system that has a solution by construction, the
instrument is broken and the negative result on the real b means nothing.

Also runs the reverse control: perturb a planted b in a single coordinate by a
single unit. That must flip the verdict back to inconsistent -- an instrument
that says CONSISTENT for everything is equally useless.
"""
import sys, os, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_tb1_rank import load, parse_poly, evalmono, rank_modp, SRC


def build(pt, polys, lin, C, cset, p):
    cidx = {v: j for j, v in enumerate(C)}
    n = len(C)
    A, b = [], []
    for i in lin:
        row = [0] * n
        rhs = 0
        for m, co in polys[i].items():
            cv = [v for v, e in m if v in cset]
            rest = tuple((v, e) for v, e in m if v not in cset)
            val = co * evalmono(rest, pt, p) % p
            if cv:
                row[cidx[cv[0]]] = (row[cidx[cv[0]]] + val) % p
            else:
                rhs = (rhs - val) % p
        A.append(row); b.append(rhs)
    return A, b


def consistent(A, b, n, p):
    rA, _ = rank_modp([r[:] for r in A], n, p)
    aug = [A[i] + [b[i]] for i in range(len(A))]
    rAug, sol = rank_modp(aug, n + 1, p)
    return rA == rAug, rA, rAug, sol


def main():
    vs, p, body = load(SRC)
    C = sorted(v for v in vs if v.startswith('c_'))
    OTHER = sorted(v for v in vs if not v.startswith('c_'))
    cset = set(C); n = len(C)
    polys = [parse_poly(x, p) for x in body]
    lin = [i for i, q in enumerate(polys)
           if max((sum(e for v, e in m if v in cset) for m in q), default=0) <= 1]
    rng = random.Random(31337)
    pt = {v: rng.randrange(1, p) for v in OTHER}
    A, b_true = build(pt, polys, lin, C, cset, p)
    print(f"control at one random (d,s): A is {len(A)} x {n}")

    ok, rA, rAug, _ = consistent(A, b_true, n, p)
    print(f"  [real b]      rank A={rA}, rank[A|b]={rAug} -> "
          f"{'CONSISTENT' if ok else 'inconsistent'}   (expect inconsistent)")

    c0 = [rng.randrange(0, p) for _ in range(n)]
    b_plant = [sum(A[i][j] * c0[j] for j in range(n)) % p for i in range(len(A))]
    ok2, rA2, rAug2, sol = consistent(A, b_plant, n, p)
    print(f"  [planted b]   rank A={rA2}, rank[A|b]={rAug2} -> "
          f"{'CONSISTENT' if ok2 else 'inconsistent'}   (expect CONSISTENT)")
    if not ok2:
        print("  *** CONTROL FAILED: a system with a solution by construction was "
              "called inconsistent. The probe is broken and its negative result "
              "on the real b is WORTHLESS.")
        return 1
    # recover the solution and check it against the planted right-hand side
    kv = [v for v in sol if v[n] % p]
    assert kv, "consistent but no affine solution vector recovered"
    # kernel v of [A|b] obeys A.v[0:n] + b*v[n] = 0, so c = -v[0:n]/v[n].
    # The missing minus here was caught by this control's recovery leg.
    inv = pow(kv[0][n], p - 2, p)
    crec = [(-kv[0][j]) * inv % p for j in range(n)]
    resid = [(sum(A[i][j] * crec[j] for j in range(n)) - b_plant[i]) % p
             for i in range(len(A))]
    bad = [i for i, r in enumerate(resid) if r]
    print(f"  [recovery]    A.c_rec - b_plant nonzero in {len(bad)} of "
          f"{len(A)} rows   (expect 0)")
    if bad:
        print("  *** CONTROL FAILED: recovered c does not satisfy the planted system.")
        return 1

    b_pert = list(b_plant); b_pert[0] = (b_pert[0] + 1) % p
    ok3, _, rAug3, _ = consistent(A, b_pert, n, p)
    print(f"  [perturbed b] rank[A|b]={rAug3} -> "
          f"{'CONSISTENT' if ok3 else 'inconsistent'}   (expect inconsistent)")
    if ok3:
        print("  *** CONTROL FAILED: a one-unit perturbation off the column space "
              "was still called consistent. The probe says yes to everything.")
        return 1

    print("\nCONTROL PASSED on all three legs: the probe detects a planted "
          "solution, recovers it exactly, and rejects a one-unit perturbation.")
    print("The 'inconsistent at every probe' result on the real b is therefore "
          "a measurement, not an artifact of a broken instrument.")
    return 0


if __name__ == '__main__':
    sys.exit(main())
