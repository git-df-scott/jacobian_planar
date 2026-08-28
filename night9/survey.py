"""night9 — the prime survey.

Sweeps support pairs (S_P, S_Q) at small primes and records, per cell, whether
the Keller-plus-collision system has an F_p point.  Measurements only.

FAMILIES
--------
F1  "Frobenius ansatz", modelled on the p = 2 Mondello object
        P = x + x^2 y + x^4 + x^6 y^2 ,  Q = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3
    whose exponents read, in terms of p = 2, as
        S_P = {(1,0), (p,1), (2p,0), (2p+2,2)}
        S_Q = {(0,1), (2p+1,0), (2p+2,1), (2p+3,2), (2p+4,3)}
    The family keeps that shape and varies three parameters:
        S_P = {(1,0), (A,1), (2p,0), (2p+C,2)}      A in {2, p, p+1, 2p-1}
                                                    C in {0, 2, 3}
        S_Q = {(0,1), (D,0), (D+1,1), (D+2,2), (D+3,3)}
                                                    D in {p+1, 2p, 2p+1, 2p+2}
    4 x 3 x 4 = 48 patterns per prime (deduplicated; degenerate ones, where a
    support would have a repeated exponent, are dropped).  n = |S_P|+|S_Q| = 9.
    Maximum degree reached: 2p+5.

F2  random sparse.  40 support pairs per prime, deterministic seed
    1000003*p + 17.  |S_P|, |S_Q| drawn from {4,...,7}; total degrees deg P,
    deg Q drawn from {4,...,20} and attained.  (1,0) is always in S_P and
    (0,1) always in S_Q, so the linear part can be invertible; each support is
    forced to contain at least one pure-x monomial (y-exponent 0) and at least
    one mixed monomial (both exponents > 0).  n <= 14.

F3  the p = 2 Mondello support verbatim, run at every prime.

METHOD LADDER (recorded per cell)
---------------------------------
exhaustive-bilinear : complete.  The (K) equations are bilinear and each
    collision equation touches only one side, so we enumerate the smaller side
    inside the affine subspace cut out by its own collision equation
    (p^nfree points, nfree = |side| - 1 when that equation is nonzero) and for
    each enumerated point solve the LINEAR system over F_p for the other side
    by batched Gauss-Jordan.  Every F_p point of the system is visited, so the
    reported count is exact.  Used when p^nfree <= 400000.
groebner-gfp-field : sympy.groebner over GF(p) of the system TOGETHER WITH the
    field equations z^p - z for every unknown, so that V = the set of
    F_p-rational points exactly.  basis == [1]  <=>  EMPTY.  300 s timeout.
sampling-linear-fibres : lower-bound probe only.  200000 random draws of the
    smaller side (inside its collision subspace), each followed by an exact
    linear solve for the other side, so each draw covers p^{other} points and
    the probe covers >= 10^6 points.  A miss is recorded INCONCLUSIVE, never
    EMPTY.

VERDICTS: NONEMPTY / EMPTY / INCONCLUSIVE / TIMEOUT.
"""

import csv, hashlib, json, os, random, signal, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
from keller_solver import (build_system, exhaustive, verify_solution,
                           hensel_step, solve_gfp, _affine_enum_spec,
                           tear_data, degenerate_screen)

BUDGET = 400000
GB_TIMEOUT = 300
N_DRAWS = 200000
PRIMES = [3, 5, 7, 11, 13, 17]

MONDELLO_P = [(1, 0), (2, 1), (4, 0), (6, 2)]
MONDELLO_Q = [(0, 1), (5, 0), (6, 1), (7, 2), (8, 3)]


def shash(SP, SQ):
    s = json.dumps([sorted(map(list, SP)), sorted(map(list, SQ))])
    return hashlib.sha1(s.encode()).hexdigest()[:12]


# --------------------------------------------------------------- families

def family_F1(p):
    out = []
    for A in sorted({2, p, p + 1, 2 * p - 1}):
        for C in (0, 2, 3):
            SP = [(1, 0), (A, 1), (2 * p, 0), (2 * p + C, 2)]
            if len(set(SP)) != 4:
                continue
            for D in sorted({p + 1, 2 * p, 2 * p + 1, 2 * p + 2}):
                SQ = [(0, 1), (D, 0), (D + 1, 1), (D + 2, 2), (D + 3, 3)]
                if len(set(SQ)) != 5:
                    continue
                out.append((sorted(SP), sorted(SQ)))
    seen, ded = set(), []
    for SP, SQ in out:
        h = shash(SP, SQ)
        if h in seen:
            continue
        seen.add(h)
        ded.append((SP, SQ))
    return ded


def _rand_support(rng, k, deg, must, want_pure_x, want_mixed):
    """k monomials of total degree <= deg, degree deg attained, containing
    `must`, at least one pure-x and at least one mixed monomial."""
    pool = [(i, j) for i in range(deg + 1) for j in range(deg + 1)
            if 0 < i + j <= deg]
    for _ in range(400):
        S = set(must)
        top = [m for m in pool if m[0] + m[1] == deg]
        S.add(rng.choice(top))
        if want_pure_x:
            S.add(rng.choice([m for m in pool if m[1] == 0]))
        if want_mixed:
            S.add(rng.choice([m for m in pool if m[0] > 0 and m[1] > 0]))
        while len(S) < k:
            S.add(rng.choice(pool))
        S = sorted(S)
        if len(S) != k:
            continue
        if max(i + j for i, j in S) != deg:
            continue
        if not any(j == 0 for i, j in S):
            continue
        if not any(i > 0 and j > 0 for i, j in S):
            continue
        return S
    return None


def family_F2(p, n=40):
    rng = random.Random(1000003 * p + 17)
    out, seen = [], set()
    tries = 0
    while len(out) < n and tries < 4000:
        tries += 1
        kP = rng.randint(4, 7); kQ = rng.randint(4, 7)
        dP = rng.randint(4, 20); dQ = rng.randint(4, 20)
        SP = _rand_support(rng, kP, dP, [(1, 0)], True, True)
        SQ = _rand_support(rng, kQ, dQ, [(0, 1)], True, True)
        if SP is None or SQ is None:
            continue
        h = shash(SP, SQ)
        if h in seen:
            continue
        seen.add(h)
        out.append((SP, SQ))
    return out


def family_F3(p):
    return [(MONDELLO_P, MONDELLO_Q)]


# ---------------------------------------------------------------- methods

class _TO(Exception):
    pass


def _alarm(sig, frm):
    raise _TO()


def groebner_cell(SP, SQ, p, timeout=GB_TIMEOUT):
    import sympy
    eqs, pairs, cP, cQ = build_system(SP, SQ)
    A = sympy.symbols('a0:%d' % len(SP))
    B = sympy.symbols('b0:%d' % len(SQ))
    polys = []
    for e in eqs:
        s = sum(c * A[mi] * B[ni] for (mi, ni, c) in pairs[e])
        if e == (0, 0):
            s = s - 1
        if s != 0:
            polys.append(sympy.expand(s))
    cp = sum(cP[i] * A[i] for i in range(len(SP)))
    cq = sum(cQ[i] * B[i] for i in range(len(SQ)))
    if cp != 0:
        polys.append(cp)
    if cq != 0:
        polys.append(cq)
    for z in list(A) + list(B):
        polys.append(z ** p - z)
    signal.signal(signal.SIGALRM, _alarm)
    signal.alarm(timeout)
    try:
        G = sympy.groebner(polys, *(list(A) + list(B)),
                           order='grevlex', modulus=p)
        signal.alarm(0)
    except _TO:
        return {"status": "TIMEOUT"}
    except Exception as ex:
        signal.alarm(0)
        return {"status": "ERROR", "err": str(ex)[:200]}
    ex_ = [sympy.expand(g) for g in G.exprs]
    trivial = len(ex_) == 1 and ex_[0] == 1
    return {"status": "OK", "empty": bool(trivial), "n_basis": len(ex_)}


def sampling_cell(SP, SQ, p, n_draws=N_DRAWS, seed=0, max_solutions=20):
    eqs, pairs, cP, cQ = build_system(SP, SQ)
    NA, NB = len(SP), len(SQ)
    dimA = NA - (1 if any(x % p for x in cP) else 0)
    dimB = NB - (1 if any(x % p for x in cQ) else 0)
    side = "P" if dimA <= dimB else "Q"
    if side == "P":
        NF, NS, cF, cS = NA, NB, cP, cQ
    else:
        NF, NS, cF, cS = NB, NA, cQ, cP
    nfree, expand = _affine_enum_spec(cF, NF, p)
    T = np.zeros((len(eqs), NS, NF), dtype=np.int64)
    rhs0 = np.zeros(len(eqs), dtype=np.int64)
    for k, e in enumerate(eqs):
        for (mi, ni, c) in pairs[e]:
            f, s = (mi, ni) if side == "P" else (ni, mi)
            T[k, s, f] = (T[k, s, f] + c) % p
        if e == (0, 0):
            rhs0[k] = 1 % p
    cS_row = np.array([x % p for x in cS], dtype=np.int64)
    M = len(eqs) + 1
    rng = np.random.default_rng(seed)
    hits, sols = 0, []
    done = 0
    chunk = 8192
    while done < n_draws:
        b = min(chunk, n_draws - done)
        done += b
        F = rng.integers(0, p, size=(b, nfree), dtype=np.int64)
        fixed = expand(F)
        Amat = np.zeros((b, M, NS + 1), dtype=np.int64)
        Amat[:, :len(eqs), :NS] = np.einsum('ksf,bf->bks', T, fixed) % p
        Amat[:, :len(eqs), NS] = rhs0[None, :]
        Amat[:, len(eqs), :NS] = cS_row[None, :]
        from keller_solver import batch_rank_consistent
        rank, cons = batch_rank_consistent(Amat, p)
        hits += int(cons.sum())
        if cons.any() and len(sols) < max_solutions:
            for bi in np.nonzero(cons)[0][:max_solutions]:
                fx = [int(v) for v in fixed[bi]]
                rows = [[int(T[k, s, :] @ np.array(fx)) % p for s in range(NS)]
                        for k in range(len(eqs))]
                rr = [int(x) for x in rhs0]
                rows.append([int(x) for x in cS_row]); rr.append(0)
                got = solve_gfp(rows, rr, p)
                if got is None:
                    continue
                part, _ = got
                sols.append((fx, part) if side == "P" else (part, fx))
                if len(sols) >= max_solutions:
                    break
    return {"n_draws": n_draws, "points_covered": n_draws * (p ** NS),
            "n_hit_fibres": hits, "solutions": sols}


# ------------------------------------------------------------------ cell

def run_cell(SP, SQ, p, family, hitdir):
    t0 = time.time()
    h = shash(SP, SQ)
    NA, NB = len(SP), len(SQ)
    rec = {"hash": h, "p": p, "family": family, "nP": NA, "nB": NB,
           "n": NA + NB}
    ex = exhaustive(SP, SQ, p, budget=BUDGET, max_solutions=20)
    sols = []
    if ex["feasible"]:
        rec["method"] = "exhaustive-bilinear"
        rec["n_enum"] = ex["n_enum"]
        rec["count"] = ex["count"]
        rec["verdict"] = "NONEMPTY" if ex["count"] > 0 else "EMPTY"
        sols = ex["solutions"]
    else:
        gb = groebner_cell(SP, SQ, p)
        if gb["status"] == "OK":
            rec["method"] = "groebner-gfp-field"
            rec["n_enum"] = ex["n_enum"]
            rec["count"] = ""
            rec["verdict"] = "EMPTY" if gb["empty"] else "NONEMPTY"
            if not gb["empty"]:
                sp = sampling_cell(SP, SQ, p, seed=p)
                sols = sp["solutions"]
                rec["sampling_after_groebner_hits"] = sp["n_hit_fibres"]
        else:
            sp = sampling_cell(SP, SQ, p, seed=p)
            rec["method"] = "sampling-linear-fibres"
            rec["n_enum"] = sp["points_covered"]
            rec["count"] = ""
            if sp["n_hit_fibres"] > 0:
                rec["verdict"] = "NONEMPTY"
                sols = sp["solutions"]
            else:
                rec["verdict"] = ("TIMEOUT" if gb["status"] == "TIMEOUT"
                                  else "INCONCLUSIVE")
                if gb["status"] == "TIMEOUT":
                    rec["verdict"] = "INCONCLUSIVE"
                    rec["note"] = "groebner TIMEOUT, sampling MISS"
                else:
                    rec["note"] = "groebner " + gb["status"] + ", sampling MISS"

    nver = nfail = climb2 = climb3 = 0
    ndeg = nte = ntn = ntother = 0
    climb2_tn = 0
    if rec["verdict"] == "NONEMPTY" and sols:
        details = []
        staged = []
        for (a, b) in sols[:20]:
            # cheap additive-type screen first: DEGENERATE hits are recorded
            # and go no further (no verification, no tear, no Hensel).
            isdeg, why = degenerate_screen(SP, SQ, a, b)
            if isdeg:
                ndeg += 1
                details.append({"a": a, "b": b, "status": "DEGENERATE",
                                "reason": why})
                continue
            chk = verify_solution(SP, SQ, a, b, p)
            ok = chk["det_ok"] and chk["coll_ok"]
            nver += 1
            if not ok:
                nfail += 1
                details.append({"a": a, "b": b, "status": "VERIFY-FAIL",
                                "verify": chk})
                continue
            td = tear_data(SP, SQ, a, b, p, timeout=30)
            if td["tear"] == "TEAR-NONEMPTY":
                ntn += 1
            elif td["tear"] == "TEAR-EMPTY":
                nte += 1
            else:
                ntother += 1
            staged.append({"a": a, "b": b, "status": "VERIFIED",
                           "verify": chk, "tear": td})
        # PRIORITY RULE: TEAR-NONEMPTY hits get the Hensel p^2/p^3 steps first.
        order = {"TEAR-NONEMPTY": 0}
        staged.sort(key=lambda d: order.get(d["tear"]["tear"], 1))
        for d in staged:
            a, b = d["a"], d["b"]
            l2 = hensel_step(SP, SQ, a, b, p, 1)
            d["lift_to_p2"] = l2 is not None
            if l2 is not None:
                climb2 += 1
                if d["tear"]["tear"] == "TEAR-NONEMPTY":
                    climb2_tn += 1
                d["p2_point"] = {"a": l2[0], "b": l2[1]}
                l3 = hensel_step(SP, SQ, l2[0], l2[1], p, 2)
                d["lift_to_p3"] = l3 is not None
                if l3 is not None:
                    climb3 += 1
                    d["p3_point"] = {"a": l3[0], "b": l3[1]}
            details.append(d)
        with open(os.path.join(hitdir, "%s_p%d.json" % (h, p)), "w") as f:
            json.dump({"hash": h, "p": p, "family": family,
                       "characteristic": p,
                       "support_P": [list(m) for m in SP],
                       "support_Q": [list(m) for m in SQ],
                       "method": rec["method"],
                       "exact_count": rec.get("count", ""),
                       "solutions": details}, f, indent=1)
    rec["n_verified"] = nver
    rec["n_verify_fail"] = nfail
    rec["n_degenerate"] = ndeg
    rec["n_tear_nonempty"] = ntn
    rec["n_tear_empty"] = nte
    rec["n_tear_other"] = ntother
    rec["climb_p2"] = climb2
    rec["climb_p2_tear_nonempty"] = climb2_tn
    rec["climb_p3"] = climb3
    rec["wall_s"] = round(time.time() - t0, 3)
    return rec


FIELDS = ["hash", "p", "family", "nP", "nB", "n", "method", "n_enum",
          "verdict", "count", "n_verified", "n_verify_fail", "n_degenerate",
          "n_tear_nonempty", "n_tear_empty", "n_tear_other", "climb_p2",
          "climb_p2_tear_nonempty", "climb_p3", "wall_s", "note"]


def main():
    supdir = os.path.join(HERE, "supports")
    hitdir = os.path.join(HERE, "hits")
    os.makedirs(supdir, exist_ok=True)
    os.makedirs(hitdir, exist_ok=True)
    csvpath = os.path.join(HERE, "prime_survey.csv")
    done = set()
    if os.path.exists(csvpath):
        with open(csvpath) as f:
            for row in csv.DictReader(f):
                done.add((row["hash"], int(row["p"])))
    newfile = not os.path.exists(csvpath)
    fh = open(csvpath, "a", newline="")
    w = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
    if newfile:
        w.writeheader()

    cells = []
    for p in PRIMES:
        for fam, gen in (("F1", family_F1), ("F2", family_F2), ("F3", family_F3)):
            for SP, SQ in gen(p):
                cells.append((p, fam, SP, SQ))

    n = 0
    for (p, fam, SP, SQ) in cells:
        h = shash(SP, SQ)
        sp = os.path.join(supdir, h + ".json")
        if not os.path.exists(sp):
            with open(sp, "w") as f:
                json.dump({"hash": h, "family": fam,
                           "support_P": [list(m) for m in SP],
                           "support_Q": [list(m) for m in SQ],
                           "nP": len(SP), "nQ": len(SQ)}, f, indent=1)
        if (h, p) in done:
            continue
        rec = run_cell(SP, SQ, p, fam, hitdir)
        w.writerow(rec)
        fh.flush()
        n += 1
        print("%-13s p=%-3d %-3s %-22s %-13s cnt=%-8s %.1fs" %
              (h, p, fam, rec["method"], rec["verdict"],
               str(rec.get("count", "")), rec["wall_s"]), flush=True)
    fh.close()
    print("cells run this pass:", n)


if __name__ == "__main__":
    main()
