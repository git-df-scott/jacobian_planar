#!/usr/bin/env python3
"""Lane 7 sweep: exact modular search on the collision-first incidence variety."""
from __future__ import annotations

import itertools
import json
import sys
import time
from collections import Counter

import numpy as np

from incidence import collision_polynomial
from lane7_lib import (TEMPLATES, Template, analyse, bottom_block_consistent,
                       coordinate_P, random_dense_P, replay, solve_mod)

P_MAIN = 1000003
P_ALT = 1000033
CANDIDATES = []
DEGENERATE_HITS = []


# --------------------------------------------------------------- utilities

def primitive_root(p: int) -> int:
    n = p - 1
    factors = set()
    m = n
    d = 2
    while d * d <= m:
        while m % d == 0:
            factors.add(d)
            m //= d
        d += 1
    if m > 1:
        factors.add(m)
    for g in range(2, 200):
        if all(pow(g, n // f, p) != 1 for f in factors):
            return g
    raise RuntimeError("no primitive root found")


def pdict(tpl: Template, pvec: np.ndarray, p: int):
    return {m: int(pvec[i]) for i, m in enumerate(tpl.ps) if int(pvec[i]) % p}


def qdict(tpl: Template, qvec: np.ndarray, p: int):
    return {m: int(qvec[i]) for i, m in enumerate(tpl.qs) if int(qvec[i]) % p}


def examine_hit(tpl: Template, pvec: np.ndarray, p: int, res: dict, origin: str):
    """A full-system-consistent P.  Classify, replay, and flag if nondegenerate."""
    Pd = pdict(tpl, pvec, p)
    Qv = res["Q"]
    Qd = qdict(tpl, Qv, p)
    rp = replay(Pd, Qd, p)
    p_x = bool(pvec[tpl.p_vertex[0]] % p)
    p_y = bool(pvec[tpl.p_vertex[1]] % p)
    # Q's vertices may be movable inside the solution space: try to switch them on
    q_x = bool(Qv[tpl.q_vertex[0]] % p)
    q_y = bool(Qv[tpl.q_vertex[1]] % p)
    K = res.get("Qkernel")
    if K is not None and len(K):
        for idx, flag in ((tpl.q_vertex[0], "q_x"), (tpl.q_vertex[1], "q_y")):
            if not (Qv[idx] % p) and np.any(K[:, idx] % p):
                t = int(np.nonzero(K[:, idx] % p)[0][0])
                Qv2 = (Qv + K[t]) % p
                if flag == "q_x":
                    q_x = bool(Qv2[idx] % p)
                else:
                    q_y = bool(Qv2[idx] % p)
    rec = {"origin": origin, "template": tpl.name, "p": p, "P": {str(k): v for k, v in Pd.items()},
           "Q": {str(k): v for k, v in Qd.items()},
           "replay_bracket_is_one": rp["bracket_is_one"],
           "P00": rp["P00"], "P10": rp["P10"], "Q00": rp["Q00"], "Q10": rp["Q10"],
           "P_vertex_x": p_x, "P_vertex_y": p_y,
           "Q_vertex_x": q_x, "Q_vertex_y": q_y,
           "full_nullity": res["full_nullity"]}
    nondeg = p_x and p_y and q_x and q_y
    if not rp["bracket_is_one"]:
        print("!! REPLAY FAILURE -- engine reported a hit that is not [P,Q]=1", rec)
        return rec
    if nondeg:
        CANDIDATES.append(rec)
        print("\n" + "!" * 78)
        print("NONDEGENERATE CONSISTENT HIT -- CANDIDATE-UNVERIFIED")
        print(json.dumps(rec, indent=1))
        print("!" * 78 + "\n", flush=True)
    else:
        DEGENERATE_HITS.append(rec)
    return rec


# ------------------------------------------------------------ sweep A: random

def sweep_random(tpl: Template, n: int, p: int, seed: int = 11):
    rng = np.random.default_rng(seed)
    bn, fn, br, fr = Counter(), Counter(), Counter(), Counter()
    n_bracket, n_full, n_bottom = 0, 0, 0
    t0 = time.time()
    for _ in range(n):
        pv = random_dense_P(tpl, rng, p)
        res = analyse(tpl, pv, p)
        bn[res["bracket_nullity"]] += 1
        fn[res["full_nullity"]] += 1
        br[res["bracket_rank"]] += 1
        fr[res["full_rank"]] += 1
        if res["bracket_consistent"]:
            n_bracket += 1
        if bottom_block_consistent(tpl, pv, p):
            n_bottom += 1
        if res["full_consistent"]:
            n_full += 1
            examine_hit(tpl, pv, p, res, "random-dense")
    return {"n": n, "seconds": round(time.time() - t0, 1),
            "bracket_nullity": dict(bn), "full_nullity": dict(fn),
            "bracket_rank": dict(br), "full_rank": dict(fr),
            "bracket_consistent": n_bracket, "bottom_block_consistent": n_bottom,
            "full_consistent": n_full}


# ------------------------------------------------- sweep B: coordinate stratum

def sweep_coordinates(tpl: Template, n: int, p: int, seed: int = 5):
    rng = np.random.default_rng(seed)
    d = tpl.px // tpl.py
    deltas, bad, nulls = [], 0, Counter()
    qdeg_x = qdeg_y = 0
    full_hits = 0
    for _ in range(n):
        f = rng.integers(1, p, size=d).tolist()
        lam = int(rng.integers(1, p))
        pv = coordinate_P(tpl, f, lam, p)
        res = analyse(tpl, pv, p)
        if not res["bracket_consistent"]:
            bad += 1
            continue
        nulls[res["bracket_nullity"]] += 1
        deltas.append(res["delta"])
        A, b = tpl.matrix(pv, p), tpl.rhs(p)
        sol = solve_mod(A, b, p)
        qv = sol["particular"]
        K = sol["kernel"]
        qx = bool(qv[tpl.q_vertex[0]] % p) or bool(np.any(K[:, tpl.q_vertex[0]] % p))
        qy = bool(qv[tpl.q_vertex[1]] % p) or bool(np.any(K[:, tpl.q_vertex[1]] % p))
        qdeg_x += qx
        qdeg_y += qy
        if res["full_consistent"]:
            full_hits += 1
            examine_hit(tpl, pv, p, res, "coordinate")
    # the degenerate boundary f(1)=0 (P becomes a py-th power, not a coordinate)
    boundary = []
    for _ in range(50):
        f = rng.integers(1, p, size=d).tolist()
        f[-1] = (-sum(f[:-1])) % p          # force f(1)=0
        if f[-1] == 0:
            continue
        pv = coordinate_P(tpl, f, int(rng.integers(1, p)), p)
        r = analyse(tpl, pv, p)
        boundary.append((r["bracket_consistent"], r["full_consistent"],
                         r["bracket_nullity"]))
    return {"n": n, "bracket_inconsistent": bad,
            "bracket_nullity": dict(nulls),
            "delta_zero_count": sum(1 for x in deltas if x % p == 0),
            "delta_sample": deltas[:5],
            "Q_top_vertex_reachable": qdeg_y, "Q_right_vertex_reachable": qdeg_x,
            "full_consistent": full_hits,
            "boundary_f1_eq_0_any_bracket_consistent": any(b[0] for b in boundary),
            "boundary_nullities": sorted({b[2] for b in boundary})}


# ------------------------------------------------- sweep D: composite P (rank drop)

def sweep_composite(tpl: Template, n: int, p: int, seed: int = 9):
    """P = A^k with A on a smaller triangle: predicted nullity >= k+1, and
    predicted ALWAYS inconsistent ([f(A),Q] = f'(A)[A,Q] is never 1)."""
    rng = np.random.default_rng(seed)
    out = []
    k = 2
    sub = Template(f"{tpl.name}_sub", tpl.px // k, tpl.py // k,
                   tpl.qx, tpl.qy) if tpl.py % k == 0 else None
    if sub is None:
        return {}
    for _ in range(n):
        # A(0,0)=A(1,0)=0 makes P=A^2 satisfy the collision automatically
        free = [m for m in sub.ps if m not in ((0, 0), (sub.px, 0))]
        vals = rng.integers(0, p, size=len(free)).tolist()
        A = collision_polynomial(sub.ps, vals, p)
        Pd = {}
        for m1, c1 in A.items():
            for m2, c2 in A.items():
                m = (m1[0] + m2[0], m1[1] + m2[1])
                Pd[m] = (Pd.get(m, 0) + c1 * c2) % p
        Pd = {m: c for m, c in Pd.items() if c}
        if any(m not in tpl.p_index for m in Pd):
            continue
        pv = tpl.pvec(Pd, p)
        res = analyse(tpl, pv, p)
        out.append((res["bracket_nullity"], res["bracket_consistent"],
                    res["full_nullity"], res["full_consistent"]))
    return {"n_used": len(out),
            "bracket_nullity": dict(Counter(o[0] for o in out)),
            "any_bracket_consistent": any(o[1] for o in out),
            "full_nullity": dict(Counter(o[2] for o in out)),
            "any_full_consistent": any(o[3] for o in out)}


# ------------------------------------------------------------ sweep C: sparse

def gauge_reps(js, p, g):
    """Orbit representatives of (alpha,s) -> (alpha s^{j_i}) acting on (F_p^*)^k.

    Fix c_1 = 1 with alpha.  The residual s acts by c_i -> s^{j_i-j_1} c_i.
    Returns a list of tuples of coefficient values covering every orbit.
    """
    k = len(js)
    if k == 1:
        return [(1,)]
    d = [(j - js[0]) % (p - 1) for j in js]
    pivot = next((i for i in range(1, k) if d[i] % (p - 1)), None)
    if pivot is None:                       # no residual action
        return None                          # caller must scan all of (F_p^*)^{k-1}
    e = np.gcd(d[pivot], p - 1)
    reps = [pow(g, t, p) for t in range(int(e))]
    return pivot, reps


def sparse_family(tpl: Template, mons, p, coeff_iter):
    """Yield P vectors for the given free monomials and coefficient tuples."""
    for coeffs in coeff_iter:
        Pd = {m: int(c) % p for m, c in zip(mons, coeffs) if int(c) % p}
        if len(Pd) != len(mons):
            continue
        bottom = sum(c for (i, j), c in Pd.items() if j == 0) % p
        if (tpl.px, 0) in Pd:
            continue
        Pd[(tpl.px, 0)] = (-bottom) % p
        Pd = {m: c for m, c in Pd.items() if c}
        yield Pd


def coeff_tuples(js, p, g, k, coeff_set, cap):
    """Coefficient tuples for one sparse pattern, plus a flag: is it exhaustive?

    Uses the (alpha, s) gauge  P_ij -> alpha s^j P_ij, which preserves the
    template, both collision points and solvability of [P,Q]=1.
    """
    if k == 1:
        return [(1,)], True
    d = [(j - js[0]) % (p - 1) for j in js]
    pivot = next((i for i in range(1, k) if d[i] % (p - 1)), None)
    if pivot is None:
        n_needed = (p - 1) ** (k - 1)
        if n_needed <= cap:
            return ([tuple([1] + list(rest))
                     for rest in itertools.product(range(1, p), repeat=k - 1)], True)
        return list(itertools.product([1], *[coeff_set] * (k - 1))), False
    e = int(np.gcd(d[pivot], p - 1))
    reps = [pow(g, t, p) for t in range(e)]
    others = [i for i in range(1, k) if i != pivot]
    n_needed = e * (p - 1) ** len(others)
    if n_needed <= cap:
        out = []
        for r in reps:
            for rest in itertools.product(range(1, p), repeat=len(others)):
                t = [1] * k
                t[pivot] = r
                for pos, v in zip(others, rest):
                    t[pos] = v
                out.append(tuple(t))
        return out, True
    out = []
    for r in reps:
        for rest in itertools.product(coeff_set, repeat=len(others)):
            t = [1] * k
            t[pivot] = r
            for pos, v in zip(others, rest):
                t[pos] = v
            out.append(tuple(t))
    return out, False


def sweep_sparse(tpl: Template, p: int, kmax: int, coeff_set, cap: int = 40000,
                 budget_seconds: float = 600.0, log=print):
    """Sparse P: a few monomials only, coefficients gauge-reduced.

    Two provable rejections are applied first (they are theorems, not filters):
      * supp(P) has no monomial with j>=1  ->  P_y=0, [P,Q]=p'(x)Q_y=1 forces
        p'=const, so p is linear and the collision p(0)=p(1)=0 gives p=0.
      * every monomial has j>=1  ->  y|P, and restricting [P,Q]=1 to y=0 gives
        -P_y(x,0) q'(x) = 1 with q(0)=q(1)=0, impossible.
    """
    g = primitive_root(p)
    free = [m for m in tpl.ps if m not in ((0, 0), (tpl.px, 0))]
    stats = {"patterns": 0, "patterns_exhaustive": 0, "patterns_provably_dead": 0,
             "systems": 0, "bracket_consistent": 0, "bottom_consistent": 0,
             "full_consistent": 0, "live_patterns": [], "kmax": kmax,
             "cap": cap, "truncated": False}
    t0 = time.time()
    for k in range(1, kmax + 1):
        for mons in itertools.combinations(free, k):
            stats["patterns"] += 1
            js = [m[1] for m in mons]
            has_bottom = any(j == 0 for j in js)          # else P_(px,0)=0 too
            if all(j == 0 for j in js) or not has_bottom:
                stats["patterns_provably_dead"] += 1
                continue
            if all(j >= 1 for j in js):
                stats["patterns_provably_dead"] += 1
                continue
            tuples, exhaustive = coeff_tuples(js, p, g, k, coeff_set, cap)
            stats["patterns_exhaustive"] += int(exhaustive)
            live = 0
            for Pd in sparse_family(tpl, mons, p, tuples):
                stats["systems"] += 1
                pv = tpl.pvec(Pd, p)
                if not (pv[tpl.p_index[(1, 0)]] % p) and not (pv[tpl.p_index[(0, 1)]] % p):
                    continue                # constant row identically zero
                if not bottom_block_consistent(tpl, pv, p):
                    continue
                stats["bottom_consistent"] += 1
                res = analyse(tpl, pv, p)
                if res["bracket_consistent"]:
                    stats["bracket_consistent"] += 1
                    live += 1
                if res["full_consistent"]:
                    stats["full_consistent"] += 1
                    examine_hit(tpl, pv, p, res, f"sparse-k{k}")
            if live:
                stats["live_patterns"].append({"mons": [list(m) for m in mons],
                                               "exhaustive": exhaustive,
                                               "n_bracket_consistent": live})
                log(f"    live pattern {mons} exhaustive={exhaustive}: "
                    f"{live} bracket-consistent")
            if time.time() - t0 > budget_seconds:
                stats["truncated"] = True
                break
        if stats["truncated"]:
            break
    stats["seconds"] = round(time.time() - t0, 1)
    return stats


# ------------------------------------------- sweep E: Newton leading-form stratum

def sweep_leading(tpl: Template, n: int, p: int, seed: int = 21, n_lower=None):
    """P whose EDGE form is lam*(y+f(x))^py -- the necessary Newton condition.

    Any Keller pair on these triangles has edge forms lam*h^py and mu*h^qy for a
    common weighted-homogeneous h, so this stratum contains every counterexample
    with this Newton polygon; a fully random dense P does not even lie in it.
    """
    from lane7_lib import edge_and_interior, leading_form_P
    rng = np.random.default_rng(seed)
    edge, inner = edge_and_interior(tpl)
    inner = [m for m in inner if m != (0, 0)]
    d = tpl.px // tpl.py
    bn, fn = Counter(), Counter()
    n_bracket = n_bottom = n_full = 0
    t0 = time.time()
    for _ in range(n):
        f = [0] * d
        f[-1] = int(rng.integers(1, p))          # top edge coefficient nonzero
        for i in range(d - 1):
            f[i] = int(rng.integers(0, p))
        lam = int(rng.integers(1, p))
        kk = len(inner) if n_lower is None else min(n_lower, len(inner))
        chosen = list(rng.choice(len(inner), size=kk, replace=False)) if kk else []
        lower = {inner[int(i)]: int(rng.integers(0, p)) for i in chosen}
        pv = leading_form_P(tpl, f, lam, lower, p)
        res = analyse(tpl, pv, p)
        bn[res["bracket_nullity"]] += 1
        fn[res["full_nullity"]] += 1
        if bottom_block_consistent(tpl, pv, p):
            n_bottom += 1
        if res["bracket_consistent"]:
            n_bracket += 1
        if res["full_consistent"]:
            n_full += 1
            examine_hit(tpl, pv, p, res, f"leading-form-lower{n_lower}")
    return {"n": n, "n_lower_terms": n_lower, "seconds": round(time.time() - t0, 1),
            "bracket_nullity": dict(bn), "full_nullity": dict(fn),
            "bottom_block_consistent": n_bottom,
            "bracket_consistent": n_bracket, "full_consistent": n_full}


def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    p = P_MAIN
    out = {}
    if which in ("all", "random"):
        for name in ("ribbon12", "t44", "t84"):
            t = TEMPLATES[name]
            n = 20000 if name != "t84" else 12000
            print(f"[random] {name} n={n}", flush=True)
            out[f"random/{name}/p{p}"] = sweep_random(t, n, p)
            print("   ", json.dumps(out[f"random/{name}/p{p}"]), flush=True)
        t = TEMPLATES["t44"]
        out[f"random/t44/p{P_ALT}"] = sweep_random(t, 5000, P_ALT, seed=99)
        print("   alt prime:", json.dumps(out[f"random/t44/p{P_ALT}"]), flush=True)
    if which in ("all", "coord"):
        for name in ("ribbon12", "t44", "t84", "t164"):
            t = TEMPLATES[name]
            print(f"[coord] {name}", flush=True)
            out[f"coord/{name}"] = sweep_coordinates(t, 400, p)
            print("   ", json.dumps(out[f"coord/{name}"]), flush=True)
        out["coord/t44/altprime"] = sweep_coordinates(TEMPLATES["t44"], 200, P_ALT)
        print("   alt:", json.dumps(out["coord/t44/altprime"]), flush=True)
    if which in ("all", "composite"):
        for name in ("ribbon12", "t44", "t84"):
            print(f"[composite] {name}", flush=True)
            out[f"composite/{name}"] = sweep_composite(TEMPLATES[name], 200, p)
            print("   ", json.dumps(out[f"composite/{name}"]), flush=True)
    if which in ("all", "sparse"):
        cs = [1, 2, 3, 5, p - 1, p - 2, p - 3, p - 5]
        for name, kmax, budget in (("t44", 4, 420), ("ribbon12", 3, 300),
                                   ("t84", 3, 300)):
            t = TEMPLATES[name]
            print(f"[sparse] {name} kmax={kmax}", flush=True)
            out[f"sparse/{name}"] = sweep_sparse(t, p, kmax, cs, budget_seconds=budget)
            print("   ", json.dumps({k: v for k, v in out[f"sparse/{name}"].items()
                                     if k != "live_patterns"}), flush=True)
            print("    live:", json.dumps(out[f"sparse/{name}"]["live_patterns"])[:2000],
                  flush=True)
    if which in ("all", "leading"):
        for name in ("t44", "t84", "ribbon12"):
            t = TEMPLATES[name]
            for nl in (None, 3, 1, 0):
                key = f"leading/{name}/lower{nl}"
                print(f"[leading] {name} lower={nl}", flush=True)
                out[key] = sweep_leading(t, 3000, p, n_lower=nl)
                print("   ", json.dumps(out[key]), flush=True)
    out["candidates"] = CANDIDATES
    out["degenerate_hits_count"] = len(DEGENERATE_HITS)
    out["degenerate_hits_sample"] = DEGENERATE_HITS[:10]
    with open(f"lane7_results_{which}.json", "w") as fh:
        json.dump(out, fh, indent=1, default=str)
    print(f"\nCANDIDATES (nondegenerate consistent hits): {len(CANDIDATES)}")
    print(f"degenerate consistent hits: {len(DEGENERATE_HITS)}")


if __name__ == "__main__":
    main()
