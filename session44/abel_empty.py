#!/usr/bin/env python3
"""B=16 Abel ladder — emptiness query "is there a solution with mu0 != 0?"

Builds the deg(q1)=k system from abel_b16.build_identity, sets mu3=1 (the
inhomogeneous chart; mu3=0 is the homogeneous chart the paper fully settled),
saturates mu0 != 0 by Rabinowitsch (mu0*s - 1), and computes a Groebner basis
over F_p.  Basis == {1}  <=>  NO solution with mu0 != 0 at that degree
(mod p; a genuine char-0 emptiness needs the basis over Q or agreement at
several primes, done on demand).  A non-trivial basis => LIVE candidate:
solutions with mu0 != 0 exist mod p, and the exact system is then handed to
reconstruction + the paper's Section-2 lift + the binding gate.

Calibration built in: deg(q1)=3 mu3=1 must be EMPTY (paper: only mu0=0),
and a planted mu0!=0 solution of a decoy consistent system must be NON-empty.
"""
import argparse
import sys

import sympy as sp

import abel_b16 as ab


def emptiness(k, p, chart_mu3=1, saturate_mu0=True, verbose=True):
    eqs, unk, q1, A = ab.build_identity(k)
    s = sp.Symbol("s_sat")
    # chart_mu3 == -1 means mu3 is left FREE (no gauge assumption).
    if chart_mu3 == -1:
        sub = {}
        vars2 = list(unk)
    else:
        sub = {ab.mu3: chart_mu3}
        vars2 = [v for v in unk if v != ab.mu3]

    def clear_den(expr):
        e = sp.expand(expr.subs(sub))
        pe = sp.Poly(e, *vars2, domain="QQ")
        dens = [sp.Rational(c).q for c in pe.coeffs()]
        from sympy import ilcm
        L = 1
        for d in dens:
            L = ilcm(L, d)
        return sp.expand(e * L)

    gens = [clear_den(e) for e in eqs]
    if saturate_mu0:
        gens = gens + [ab.mu0 * s - 1]
        vars2 = vars2 + [s]
    dom = sp.GF(p)
    try:
        G = sp.groebner(gens, *vars2, order="grevlex", domain=dom)
    except Exception as exc:                # noqa: BLE001
        return f"GB-ERROR: {exc}"
    is_one = list(G.exprs) == [sp.GF(p)(1)] or G.exprs == (sp.Integer(1),) \
        or (len(G.exprs) == 1 and G.exprs[0] == 1)
    if verbose:
        print(f"deg(q1)={k} mu3={chart_mu3} sat_mu0={saturate_mu0} "
              f"mod {p}: |GB|={len(G.exprs)}  "
              f"{'EMPTY (no mu0!=0 solution)' if is_one else 'NONEMPTY -> LIVE'}",
              flush=True)
    return "EMPTY" if is_one else "NONEMPTY"


def calibrate(p):
    ok = ab.calibrate()
    # deg 3 inhomogeneous saturated must be EMPTY
    r3 = emptiness(3, p, chart_mu3=1, saturate_mu0=True, verbose=False)
    print(f"CAL deg3 mu3=1 mu0!=0 mod {p}: {r3}  (expect EMPTY)")
    # deg 3 UNSATURATED must be NONEMPTY (the mu0=0 solution exists)
    r3u = emptiness(3, p, chart_mu3=1, saturate_mu0=False, verbose=False)
    print(f"CAL deg3 mu3=1 unsat mod {p}: {r3u}  (expect NONEMPTY)")
    return ok and r3 == "EMPTY" and r3u == "NONEMPTY"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("k", type=int)
    ap.add_argument("--p", type=int, default=32003)
    ap.add_argument("--chart", type=int, default=1)
    ap.add_argument("--nosat", action="store_true")
    ap.add_argument("--skipcal", action="store_true")
    a = ap.parse_args()
    if not a.skipcal:
        if not calibrate(a.p):
            print("CALIBRATION FAILED — stop.")
            sys.exit(1)
    emptiness(a.k, a.p, chart_mu3=a.chart, saturate_mu0=not a.nosat)


if __name__ == "__main__":
    main()
