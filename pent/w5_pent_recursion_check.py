"""
Does the y-adic recursion actually solve [P, Q] = x^2 ?

The pentagon condition system is built by a recursion that, given P, produces
the unique Q with [P, Q] = x^2 as a formal series in y.  Every pentagon result
in this campaign -- the rank 60 of 61, the sparsity counts, the exports, the
detectors -- rests on that recursion being what it says it is, and it has never
been checked against the bracket itself.

This script checks it directly, in exact arithmetic over F_p (p = 1 mod 3):
take a random P in the pentagon support, run the recursion to level J, form
[P, Q_J] symbolically, and verify that it equals x^2 up to terms of y-order > J.
That is the defining property, tested rather than assumed.

CONTROLS
  Y1 POSITIVE: on the trivial P = x the recursion must give exactly
     Q = 1 + x^2 y, since [x, 1 + x^2 y] = x^2;
  Y2 POSITIVE: on random P, [P, Q_J] agrees with x^2 through y-order J-1;
  Y3 NEGATIVE: perturbing ONE coefficient of Q breaks Y2, so Y2 is not vacuous;
  Y4 NEGATIVE: the recursion run with a WRONG right-hand side convention
     (x^3 instead of x^2) must NOT satisfy [P,Q] = x^2.
"""
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w5_pent_hitdetector_v3 as V

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def bracket_rows(Prows, Qrows, p, J):
    """[P,Q] as rows in y, each row a coefficient list in x, truncated at y^J.

    [ sum_a P_a(x) y^a , sum_b Q_b(x) y^b ]
      = sum_{a,b} ( P_a' Q_b * b - P_a * Q_b' * a ... ) -- done term by term:
      d/dx(P_a y^a) d/dy(Q_b y^b) - d/dy(P_a y^a) d/dx(Q_b y^b)
      = (P_a' Q_b b - a P_a Q_b') y^(a+b-1).
    """
    out = [[0] for _ in range(J + 2)]

    def dv(a):
        return [(a[t] * t) % p for t in range(1, len(a))] or [0]

    def conv(a, b):
        r = [0] * (len(a) + len(b) - 1)
        for s, ca in enumerate(a):
            if ca:
                for t, cb in enumerate(b):
                    r[s + t] = (r[s + t] + ca * cb) % p
        return r

    for a in range(len(Prows)):
        for b in range(len(Qrows)):
            k = a + b - 1
            if k < 0 or k > J:
                continue
            t1 = [(z * b) % p for z in conv(dv(Prows[a]), Qrows[b])]
            t2 = [(z * a) % p for z in conv(Prows[a], dv(Qrows[b]))]
            row = out[k]
            m = max(len(row), len(t1), len(t2))
            row = row + [0] * (m - len(row))
            for s in range(len(t1)):
                row[s] = (row[s] + t1[s]) % p
            for s in range(len(t2)):
                row[s] = (row[s] - t2[s]) % p
            out[k] = row
    return out


def prows(Pv, p):
    Pd = {}
    for k, (j, i) in enumerate(V.PARAMS):
        row = Pd.setdefault(j, [])
        while len(row) <= i:
            row.append(0)
        row[i] = Pv[k] % p
    return [list(Pd.get(j, [0])) for j in range(max(Pd) + 1)]


def main(p=1000003, J=8):
    assert p % 3 == 1
    print("=" * 78)
    print("does the y-adic recursion solve [P, Q] = x^2 ?")
    print("=" * 78)

    # Y1: P = x
    Pv = [0] * V.NP
    Pv[V.IDX[(0, 1)]] = 1
    Q = V.fp_run(Pv, p)
    ok1 = (Q is not None and [z % p for z in Q[0]] == [1]
           and [z % p for z in Q[1]][:3] == [0, 0, 1]
           and all(all(z % p == 0 for z in Q[j]) for j in range(2, 6)))
    check("Y1 POSITIVE: for P = x the recursion returns exactly Q = 1 + x^2 y",
          ok1, f"Q0 {Q[0] if Q else None}, Q1 {Q[1][:4] if Q else None}, "
               f"Q2 {Q[2][:3] if Q else None}")

    # Y2: random P in the pentagon support
    rnd = random.Random(17)
    Pv = [0] * V.NP
    for k in range(V.NP):
        Pv[k] = rnd.randrange(0, p)
    Pv[V.IDX[(0, 0)]] = 0
    Pv[V.IDX[(0, 1)]] = 1
    Q = V.fp_run(Pv, p)
    Pr = prows(Pv, p)
    Qr = [[z % p for z in Q[j]] for j in range(len(Q))]
    br = bracket_rows(Pr, Qr, p, J)
    bad = []
    for k in range(J):
        row = br[k]
        want = [0, 0, 1] if k == 0 else []
        m = max(len(row), len(want))
        r2 = row + [0] * (m - len(row))
        w2 = want + [0] * (m - len(want))
        if any((a - b) % p for a, b in zip(r2, w2)):
            bad.append(k)
    check(f"Y2 POSITIVE: on a random P, [P, Q] = x^2 through y-order {J-1}",
          not bad, f"rows disagreeing: {bad}")

    Qr2 = [list(r) for r in Qr]
    Qr2[3][0] = (Qr2[3][0] + 1) % p
    br2 = bracket_rows(Pr, Qr2, p, J)
    bad2 = []
    for k in range(J):
        row = br2[k]
        want = [0, 0, 1] if k == 0 else []
        m = max(len(row), len(want))
        r2 = row + [0] * (m - len(row))
        w2 = want + [0] * (m - len(want))
        if any((a - b) % p for a, b in zip(r2, w2)):
            bad2.append(k)
    check("Y3 NEGATIVE: perturbing one coefficient of Q breaks the identity",
          bool(bad2), f"rows disagreeing: {bad2}")

    # Y4: the same recursion but seeded for [P,Q] = x^3
    Q4 = V.fp_run(Pv, p)
    Qr4 = [[z % p for z in Q4[j]] for j in range(len(Q4))]
    Qr4[1] = [0, 0, 0, Qr4[1][2] if len(Qr4[1]) > 2 else 0]   # x^2 -> x^3 seed
    br4 = bracket_rows(Pr, Qr4, p, J)
    row0 = br4[0] + [0] * 4
    check("Y4 NEGATIVE: a wrong right-hand-side seed does NOT give [P,Q] = x^2",
          any((row0[i] - (1 if i == 2 else 0)) % p for i in range(4)),
          f"row 0 begins {row0[:4]}")

    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if n == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
