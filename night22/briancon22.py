#!/usr/bin/env python3
"""Exact strike on the degree-10 Briancon target profile.

Standard-library only.  It builds
  s=xy+1, p=xs+1, u=s^2+y,
  P=p^2*u-(5/3)*p*s-(1/3)*s,
then solves [P,A]=P and [P,Q]=1 over Q on a total-degree carrier.  EMPTY
verdicts carry independently expanded lambda certificates.
"""

from fractions import Fraction as F
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "night21"))
from pole21 import clean, add, scale, mul, dx, dy, D, ONE  # noqa: E402


def power(a, n):
    z = ONE
    for _ in range(n):
        z = mul(z, a)
    return z


def carrier(d):
    return [(i, n-i) for n in range(d+1) for i in range(n+1)]


def solve_linear(rows, rhs, ncols):
    rows = [dict(r) for r in rows]
    rhs = [F(v) for v in rhs]
    piv = []
    rr = 0
    for c in range(ncols):
        k = next((k for k in range(rr, len(rows)) if rows[k].get(c)), None)
        if k is None:
            continue
        rows[rr], rows[k] = rows[k], rows[rr]
        rhs[rr], rhs[k] = rhs[k], rhs[rr]
        a = rows[rr][c]
        rows[rr] = {j: v/a for j, v in rows[rr].items()}
        rhs[rr] /= a
        for k in range(len(rows)):
            if k == rr or not rows[k].get(c):
                continue
            a = rows[k][c]
            nr = dict(rows[k])
            for j, v in rows[rr].items():
                q = nr.get(j, F(0))-a*v
                if q:
                    nr[j] = q
                elif j in nr:
                    del nr[j]
            rows[k] = nr
            rhs[k] -= a*rhs[rr]
        piv.append(c)
        rr += 1
        if rr == len(rows):
            break
    if any(not row and b for row, b in zip(rows, rhs)):
        return None
    z = [F(0)]*ncols
    for r, c in enumerate(piv):
        z[c] = rhs[r]
    return z


def verify_lambda(lam, cols, target):
    for col in cols:
        assert sum(lam.get(m, F(0))*a for m, a in col.items()) == 0
    assert sum(lam.get(m, F(0))*a for m, a in target.items()) == 1


def decide(P, target, degree):
    S = carrier(degree)
    cols = [D(P, {m: F(1)}) for m in S]
    R = sorted(set(target) | set().union(*(set(c) for c in cols)))
    ri = {m: i for i, m in enumerate(R)}
    rows = [dict() for _ in R]
    for j, col in enumerate(cols):
        for m, a in col.items():
            rows[ri[m]][j] = a
    rhs = [target.get(m, F(0)) for m in R]
    sol = solve_linear(rows, rhs, len(S))
    if sol is not None:
        A = clean({m: a for m, a in zip(S, sol) if a})
        assert add(D(P, A), scale(-1, target)) == {}
        return {"verdict": "SOLVABLE", "degree": degree,
                "solution": enc(A), "solution_degree": max(map(sum, A)) if A else -1}
    # M^T lambda=0, target^T lambda=1.
    dual = [dict() for _ in range(len(S)+1)]
    for j, col in enumerate(cols):
        for m, a in col.items():
            dual[j][ri[m]] = a
    for m, a in target.items():
        dual[-1][ri[m]] = a
    lvec = solve_linear(dual, [F(0)]*len(S)+[F(1)], len(R))
    assert lvec is not None
    lam = {m: a for m, a in zip(R, lvec) if a}
    verify_lambda(lam, cols, target)
    return {"verdict": "EMPTY_over_Q", "degree": degree,
            "unknowns": len(S), "rows": len(R), "lambda_support": len(lam),
            "lambda": enc(lam), "lambda_verified": True}


def enc(P):
    return {"%d,%d" % m: [a.numerator, a.denominator] for m, a in sorted(P.items())}


def briancon(a=F(-5, 3), b=F(-1, 3)):
    x, y = {(1, 0): F(1)}, {(0, 1): F(1)}
    s = add(mul(x, y), ONE)
    p = add(mul(x, s), ONE)
    u = add(power(s, 2), y)
    P = add(mul(power(p, 2), u), scale(a, mul(p, s)), scale(b, s))
    return P


def main():
    degree = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    specs = [
        ("g", briancon(), [
            {"value": "0", "genus": 0, "places": 4, "chi": -2, "jump": 1},
            {"value": "-16/9", "genus": 0, "places": 2, "chi": 0, "jump": 3}]),
        ("gprime", briancon(F(-7, 9), F(1, 9)), [
            {"value": "0", "genus": 0, "places": 3, "chi": -1, "jump": 2},
            {"value": "-64/81", "genus": 0, "places": 3, "chi": -1, "jump": 2}]),
    ]
    out = {"carrier_degree": degree, "targets": {}}
    for name, P, atyp in specs:
        assert max(map(sum, P)) == 10
        out["targets"][name] = {
            "P": enc(P), "degree_P": 10,
            "profile": {"generic": {"genus": 1, "places": 3, "chi": -3},
                        "atypical": atyp},
            "DP_A_eq_P": decide(P, P, degree),
            "DP_Q_eq_1": decide(P, ONE, degree),
        }
        assert sum(z["jump"] for z in atyp) == 4
    with open(os.path.join(HERE, "briancon22.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    for name, target in out["targets"].items():
        for k in ("DP_A_eq_P", "DP_Q_eq_1"):
            z = target[k]
            print(name, k, z["verdict"], "D=%d" % degree,
                  "lambda=%s" % z.get("lambda_support"), "verified=%s" % z.get("lambda_verified"))
    print("PASS profile jumps sum to 4 and all exact certificates re-expanded")


if __name__ == "__main__":
    main()
