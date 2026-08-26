#!/usr/bin/env python3
"""Lane 7 control suite.  Every control is designed to be able to FAIL."""
from __future__ import annotations

import numpy as np

import incidence as eng
from incidence import Incidence, weighted_triangle
from lane7_lib import (TEMPLATES, analyse, bottom_block_consistent,
                       coordinate_P, random_dense_P, replay, solve_mod,
                       sympy_bracket)

P_MAIN = 1000003
P_ALT = 1000033
RESULTS = []


def record(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}", flush=True)
    return ok


def main():
    p = P_MAIN
    print("=" * 78)
    print("LANE 7 CONTROLS   p =", p)
    print("=" * 78)

    record("engine.controls() (shipped internal controls)", eng.controls() is True)

    tpl = TEMPLATES["ribbon12"]

    # ---------------------------------------------------------------- (a)
    # A1: P with zero linear part.  The constant coefficient of [P,Q] is
    # P10*Q01 - P01*Q10, so P10=P01=0 makes the (0,0) row identically zero
    # while its right-hand side is 1.  PROVABLY inconsistent.
    P = {(2, 0): -1 % p, (3, 0): 1}          # x^3 - x^2 ; P(0,0)=P(1,0)=0
    got = tpl.inc.solve(P, p)
    fast = analyse(tpl, tpl.pvec(P, p), p)
    record("A1 zero-linear-part P is inconsistent (engine)", got is None)
    record("A1 zero-linear-part P is inconsistent (fast path)",
           not fast["full_consistent"] and not fast["bracket_consistent"])

    # A2: y | P.  Restricting [P,Q]=1 to y=0 gives -P_y(x,0) q'(x) = 1 with
    # P_y(x,0)=x^2-x nonconstant, so no polynomial Q exists at all.
    P = {(1, 1): -1 % p, (2, 1): 1}          # y*(x^2-x)
    got = tpl.inc.solve(P, p)
    fast = analyse(tpl, tpl.pvec(P, p), p)
    record("A2 y|P with nonconstant P_y(x,0) is inconsistent (engine)", got is None)
    record("A2 same, bracket-only is inconsistent too (fast path)",
           not fast["bracket_consistent"])

    # A3: P = y.  [P,Q]=1 IS solvable (Q=-x) but Q(1,0)-Q(0,0) = -1 != 0 for
    # every solution, so the two collision rows must kill it.  This control
    # fails if the collision rows are dropped or mis-indexed.
    P = {(0, 1): 1}
    fast = analyse(tpl, tpl.pvec(P, p), p)
    record("A3 P=y: bracket-only consistent", fast["bracket_consistent"])
    record("A3 P=y: full (collision) system inconsistent",
           not fast["full_consistent"], f"delta={fast['delta']} movable={fast['delta_movable']}")
    record("A3 engine agrees", tpl.inc.solve(P, p) is None)

    # A4: THE CONSTANT-ROW GUARD.  Build a support pair for which no basis
    # element of Q can produce a constant term in [P,Q].  The correct answer
    # is "inconsistent"; the classic bug (omitting the constant row) returns a
    # Q solving [P,Q]=0 and calls it success.
    p_sup = [(0, 0), (1, 0), (2, 0)]
    q_sup = [(0, 0), (1, 0), (2, 0), (1, 1), (2, 1)]      # (0,1) deliberately absent
    inc2 = Incidence.create(p_sup, q_sup)
    P = {(1, 0): -1 % p, (2, 0): 1}
    M, rhs = inc2.system(P, p)
    zero_row = inc2.targets.index((0, 0))
    row_is_zero = all(v % p == 0 for v in M[zero_row])
    record("A4 the constant row exists and is identically zero for this support",
           row_is_zero and rhs[zero_row] % p == 1)
    record("A4 engine reports INCONSISTENT (constant row present)",
           inc2.solve(P, p) is None)
    # show the control can fail: delete that row and the solver "succeeds" on [P,Q]=0
    M2 = [r for i, r in enumerate(M) if i != zero_row]
    r2 = [v for i, v in enumerate(rhs) if i != zero_row]
    bug = eng.solve_affine(M2, r2, p)
    bugQ = None
    if bug is not None:
        bugQ = {m: int(bug[0][i]) for i, m in enumerate(inc2.q_support) if bug[0][i] % p}
    record("A4 (negative control) dropping the row makes the solver REPORT SUCCESS "
           "on a system whose true answer is inconsistent",
           bug is not None and sympy_bracket(P, bugQ or {}, p) != {(0, 0): 1},
           f"bogus Q={bugQ if bugQ else '0 (identically zero)'} "
           f"bracket={sympy_bracket(P, bugQ or {}, p) or '0'} != 1")

    # C0: END-TO-END POSITIVE CONTROL for the collision rows.  Over F_3 the
    # Artin-Schreier pair P = x^3-x, Q = -y really does satisfy [P,Q]=1 with
    # P(0,0)=P(1,0)=Q(0,0)=Q(1,0)=0.  The full pipeline MUST find it at p=3,
    # and MUST reject the same P at p=1000003 (where 3x^2-1 is nonconstant).
    small = weighted_triangle(3, 1)
    inc3 = Incidence.create(small, small)
    Pas = {(3, 0): 1, (1, 0): -1 % 3}
    got3 = inc3.solve(Pas, 3)
    ok3 = got3 is not None
    if ok3:
        rp = replay(Pas, got3[0], 3)
        ok3 = (rp["bracket_is_one"] and rp["P00"] == rp["P10"] == 0
               and rp["Q00"] == rp["Q10"] == 0)
    record("C0 p=3 Artin-Schreier collision pair is FOUND and replays exactly", ok3,
           f"Q={got3[0] if got3 else None}")
    Pbig = {(3, 0): 1, (1, 0): -1 % p}
    incbig = Incidence.create(small, small)
    record("C0 same P is REJECTED at p=1000003", incbig.solve(Pbig, p) is None)

    # ---------------------------------------------------------------- (c)
    # C1: P = x is known to admit Q = y + x^2 - x with both collisions.
    P = {(1, 0): 1}
    got = tpl.inc.solve(P, p)
    ok = got is not None
    if ok:
        Q = got[0]
        rp = replay(P, Q, p)
        ok = rp["bracket_is_one"] and rp["Q00"] == 0 and rp["Q10"] == 0
    record("C1 P=x returns a Q, replayed independently as [P,Q]=1 with Q collisions", ok)

    # C2: the coordinate families.  P = lam*((y+f)^py - f(1)^py x) is a genuine
    # coordinate, so [P,Q]=1 MUST be solvable inside the template.
    rng = np.random.default_rng(7)
    for name in ("ribbon12", "t44", "t84"):
        t = TEMPLATES[name]
        d = t.px // t.py
        allok, deltas = True, []
        for _ in range(25):
            f = rng.integers(1, p, size=d).tolist()
            lam = int(rng.integers(1, p))
            pv = coordinate_P(t, f, lam, p)
            res = analyse(t, pv, p)
            if not res["bracket_consistent"]:
                allok = False
                break
            deltas.append(res["delta"])
            # independent replay of the bracket-only solution
            A, b = t.matrix(pv, p), t.rhs(p)
            sol = solve_mod(A, b, p)
            Q = {m: int(sol["particular"][i]) for i, m in enumerate(t.qs)
                 if sol["particular"][i] % p}
            Pd = {m: int(pv[i]) for i, m in enumerate(t.ps) if pv[i] % p}
            if not replay(Pd, Q, p)["bracket_is_one"]:
                allok = False
                break
            # closed form check: delta = -1/(lam*f(1)^(py-1))
            f1 = sum(f) % p
            pred = (-pow(lam * pow(f1, t.py - 1, p) % p, p - 2, p)) % p
            if res["delta"] % p != pred:
                allok = False
                break
        record(f"C2 {name}: 25 coordinate P are bracket-consistent, replay [P,Q]=1, "
               f"delta matches closed form", allok,
               f"all delta nonzero={all(d % p for d in deltas)}")
        record(f"C2 {name}: no coordinate P satisfies the collision rows", allok and
               all(analyse(t, coordinate_P(t, rng.integers(1, p, size=d).tolist(),
                                           int(rng.integers(1, p)), p), p)["full_consistent"]
                   is False for _ in range(10)))

    # -------------------------------------------------- fast path vs engine
    agree = True
    detail = ""
    for _ in range(40):
        pv = random_dense_P(tpl, rng, p)
        Pd = {m: int(pv[i]) for i, m in enumerate(tpl.ps) if pv[i] % p}
        engine = tpl.inc.solve(Pd, p)
        fast = analyse(tpl, pv, p)
        if (engine is None) != (not fast["full_consistent"]):
            agree = False
            detail = "consistency mismatch"
            break
        if engine is not None and engine[2] != fast["full_rank"]:
            agree = False
            detail = f"rank mismatch {engine[2]} vs {fast['full_rank']}"
            break
        A, b = tpl.full_system(pv, p)
        M, rhs = tpl.inc.system(Pd, p)
        if not np.array_equal(np.array(M, dtype=np.int64) % p, A % p):
            agree = False
            detail = "matrix mismatch"
            break
    record("X1 fast numpy path reproduces incidence.py matrix, rank and consistency",
           agree, detail)

    # rank of A must always leave the known kernel {1, P}
    ok = True
    for _ in range(20):
        pv = random_dense_P(tpl, rng, p)
        res = analyse(tpl, pv, p)
        if res["bracket_nullity"] < 2:
            ok = False
            break
    record("X2 bracket nullity >= 2 always (constants and P lie in ker X_P)", ok)

    # A5: bottom-block necessary test never rejects a genuinely consistent P
    ok = True
    for _ in range(15):
        f = rng.integers(1, p, size=tpl.px // tpl.py).tolist()
        pv = coordinate_P(tpl, f, int(rng.integers(1, p)), p)
        if not bottom_block_consistent(tpl, pv, p):
            # bottom block includes the collision rows, so coordinates may fail
            # it only if they fail the full system too -- check that
            if analyse(tpl, pv, p)["full_consistent"]:
                ok = False
                break
    record("A5 bottom-row sub-block never rejects a full-system solution", ok)

    print("=" * 78)
    bad = [n for n, ok, _ in RESULTS if not ok]
    print(f"CONTROLS: {len(RESULTS)-len(bad)}/{len(RESULTS)} pass")
    if bad:
        print("FAILING:", bad)
    return not bad


if __name__ == "__main__":
    ok = main()
    raise SystemExit(0 if ok else 1)
