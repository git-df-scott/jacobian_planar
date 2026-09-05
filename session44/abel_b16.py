#!/usr/bin/env python3
"""Session 44, Lead (Apollo-13 / O-rings) — the B=16 Abel-equation ladder.

Source: Guccione-Guccione-Valqui, "A differential equation for polynomials
related to the Jacobian conjecture", Pro Mathematica 27 (2013), 83-98.
Their Theorem 1.2: B = 16 iff there exist A, q1 in K[y] and mu0..mu3 in K,
mu0 != 0, with

  (3.6)  A(0) = -mu3^2/4,  A'(0) = mu2,  mu3 A''(0) = -6 mu1 - 2 mu3 q1''(0)

satisfying the polynomial identity (3.5):

  6 ( A - q1^2/4 + (mu3/4) q1 - (mu2/6) y )^2
      = 4 y A A' + 6 (mu3/4 q1 - mu2/6 y^2)   [see note] ... (paper's (3.5))

We transcribe (3.5) EXACTLY from the PDF (session44/promath27_gguv.txt,
lines 464-492) and CALIBRATE on the paper's own deg(q1)=3 solution
  mu2=mu1=mu0=0,  A = -y^6/4 - mu3 y^3/2 - mu3^2/4,  q1 = y^3 + mu3
before trusting it.  Then we solve deg(q1)=k for k=2..K exactly (msolve/
sympy over Q), asking the one question that matters: is there a solution
with mu0 != 0?  Any such solution is the first live B=16 signal the campaign
would ever have had; it then feeds the paper's Section-2 construction and the
full binding gate.  If every k gives only mu0=0 / homogeneous solutions, we
are extending the paper's own exclusion toward its conjecture (=> B>16).

deg(q1)=3,4 were solved by the authors in 2013; deg(q1)=5 was NOT
("after an hour the PC hadn't solved the resulting system").  That is the
frontier this script pushes.
"""
import argparse
import sys

import sympy as sp

y = sp.Symbol("y")
mu0, mu1, mu2, mu3 = sp.symbols("mu0 mu1 mu2 mu3")


def build_identity(k):
    """Return (equations, unknowns) for deg(q1)=k, q1 monic, deg(A)=2k."""
    # q1 = y^k + sum_{i<k} q_i y^i ; but q1(0)=mu3, q1'(0)=0 are imposed.
    qc = sp.symbols(f"q0:{k}")           # q1 coefficients below the top
    q1 = y**k + sum(qc[i] * y**i for i in range(k))
    Ac = sp.symbols(f"A0:{2 * k + 1}")   # A coefficients 0..2k
    A = sum(Ac[i] * y**i for i in range(2 * k + 1))
    Ap = sp.diff(A, y)

    # (3.5) transcribed from the PDF:
    #   6*(A - q1^2/4 + (mu3/4)*q1 - (mu2/6)*y)^2
    #     = 4*y*A*A' + 6*((mu3/4)*q1 - (mu2/6)*y^2)^2   ... WAIT: verify sign
    # The PDF line-broken form (464-492) reads, regrouped:
    #   6*( A - q1^2/4 + (mu3/4) q1 - (mu2/6) y )^2
    #     = 4 y A A' + 6 ( (mu3/4) q1 - (mu2/6) y^2 )^2
    #       - mu2 y q1^2 + 3 mu1 y^2 q1 - 6 mu0 y^3
    lhs = 6 * (A - q1**2 / 4 + (mu3 / 4) * q1 - (mu2 / 6) * y)**2
    rhs = (4 * y * A * Ap
           + 6 * ((mu3 / 4) * q1 - (mu2 / 6) * y**2)**2
           - mu2 * y * q1**2 + 3 * mu1 * y**2 * q1 - 6 * mu0 * y**3)
    identity = sp.expand(lhs - rhs)
    poly = sp.Poly(identity, y)
    eqs = [sp.expand(c) for c in poly.all_coeffs()]

    # initial conditions
    q1_0 = q1.subs(y, 0)
    q1p_0 = sp.diff(q1, y).subs(y, 0)
    q1pp_0 = sp.diff(q1, y, 2).subs(y, 0)
    A_0 = A.subs(y, 0)
    Ap_0 = Ap.subs(y, 0)
    App_0 = sp.diff(A, y, 2).subs(y, 0)
    cond = [
        q1_0 - mu3,                       # q1(0) = mu3
        q1p_0,                            # q1'(0) = 0
        A_0 + mu3**2 / 4,                 # A(0) = -mu3^2/4
        Ap_0 - mu2,                       # A'(0) = mu2
        mu3 * App_0 + 6 * mu1 + 2 * mu3 * q1pp_0,   # (3.6) third
    ]
    unknowns = list(qc) + list(Ac) + [mu0, mu1, mu2, mu3]
    return eqs + cond, unknowns, q1, A


def calibrate():
    """The paper's deg(q1)=3 solution must satisfy the transcribed identity."""
    eqs, unk, q1, A = build_identity(3)
    sol = {mu2: 0, mu1: 0, mu0: 0}
    # A = -y^6/4 - mu3 y^3/2 - mu3^2/4 ; q1 = y^3 + mu3 (so q0..q2 = mu3,0,0)
    Ac = sp.symbols("A0:7")
    qc = sp.symbols("q0:3")
    sol.update({qc[0]: mu3, qc[1]: 0, qc[2]: 0})
    sol.update({Ac[0]: -mu3**2 / 4, Ac[1]: 0, Ac[2]: 0,
                Ac[3]: -mu3 / 2, Ac[4]: 0, Ac[5]: 0, Ac[6]: sp.Rational(-1, 4)})
    residuals = [sp.simplify(e.subs(sol)) for e in eqs]
    ok = all(r == 0 for r in residuals)
    print(f"CALIBRATION deg(q1)=3 paper solution: "
          f"{'PASS' if ok else 'FAIL'}  (nonzero: "
          f"{[r for r in residuals if r != 0][:3]})")
    return ok


def solve_case(k, drop_mu0=False):
    """Solve deg(q1)=k.  Returns solutions; flags any with mu0 != 0."""
    eqs, unk, q1, A = build_identity(k)
    print(f"deg(q1)={k}: {len(eqs)} equations, {len(unk)} unknowns", flush=True)
    # gauge mu3: it only ever appears as a scale; set mu3 in {0,1} to split
    # the homogeneous (mu3=0) and inhomogeneous (mu3=1) charts.
    out = {}
    for m3 in (0, 1):
        sub = {mu3: m3}
        e2 = [sp.expand(e.subs(sub)) for e in eqs]
        vars2 = [v for v in unk if v != mu3]
        try:
            sols = sp.solve(e2, vars2, dict=True)
        except Exception as exc:            # noqa: BLE001
            print(f"  mu3={m3}: solve raised {exc}")
            out[m3] = "SOLVE-ERROR"
            continue
        live = []
        for s in sols:
            m0 = s.get(mu0, None)
            # mu0 may remain free/parametric; check it can be nonzero
            if m0 is None or (m0 != 0 and m0 is not sp.S.Zero):
                live.append(s)
        print(f"  mu3={m3}: {len(sols)} solution branches; "
              f"{len(live)} with mu0 possibly != 0", flush=True)
        for s in live:
            print("    LIVE:", {str(kk): vv for kk, vv in s.items()
                                if kk in (mu0, mu1, mu2)})
        out[m3] = (len(sols), len(live))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["calibrate", "solve"])
    ap.add_argument("k", nargs="?", type=int, default=3)
    a = ap.parse_args()
    if not calibrate():
        print("Calibration failed — transcription of (3.5) is wrong; STOP.")
        sys.exit(1)
    if a.mode == "solve":
        solve_case(a.k)


if __name__ == "__main__":
    main()
