"""night9 — non-degenerate census.

The per-cell hit files record the FIRST few solutions found in enumeration
order, which is not a random sample.  This pass enumerates, for every
NONEMPTY cell whose exact F_p solution count is at most CAP, the COMPLETE
solution set, and splits it into

  * DEGENERATE   -- the additive-type screen fires (P in F_p[x] and Q carries
                    no y outside its pure-y part, or the x <-> y mirror);
  * NON-DEGENERATE.

For up to SAMPLE non-degenerate solutions per cell it then runs the direct
substitution check, the tear classification mod p, and the Hensel steps to
Z/p^2 and (when that succeeds) Z/p^3, exactly as in survey.py, with the same
TEAR-NONEMPTY-first priority rule.

Output: night9/census.csv and night9/hits_nondegenerate/<hash>_p<p>.json.
"""
import csv, itertools, json, os, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from keller_solver import (build_system, solve_gfp, verify_solution,
                           hensel_step, degenerate_screen, _affine_enum_spec,
                           batch_rank_consistent)
from tear import tear_data
from survey import shash

CAP = 20000
SAMPLE = 8


def all_solutions(SP, SQ, p, cap=CAP):
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
    total = p ** nfree
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
    out = []
    for start in range(0, total, 8192):
        stop = min(start + 8192, total)
        idx = np.arange(start, stop)
        F = np.zeros((stop - start, nfree), dtype=np.int64)
        t = idx.copy()
        for d in range(nfree - 1, -1, -1):
            F[:, d] = t % p
            t //= p
        fixed = expand(F)
        Bn = fixed.shape[0]
        A = np.zeros((Bn, M, NS + 1), dtype=np.int64)
        A[:, :len(eqs), :NS] = np.einsum('ksf,bf->bks', T, fixed) % p
        A[:, :len(eqs), NS] = rhs0[None, :]
        A[:, len(eqs), :NS] = cS_row[None, :]
        rank, cons = batch_rank_consistent(A.copy(), p)
        for bi in np.nonzero(cons)[0]:
            fx = [int(z) for z in fixed[bi]]
            rows = [[int(T[k, s, :] @ np.array(fx)) % p for s in range(NS)]
                    for k in range(len(eqs))]
            rr = [int(z) for z in rhs0]
            rows.append([int(z) for z in cS_row]); rr.append(0)
            got = solve_gfp(rows, rr, p)
            if got is None:
                continue
            part, basis = got
            for co in itertools.product(range(p), repeat=len(basis)):
                sv = list(part)
                for j, cc in enumerate(co):
                    if cc:
                        sv = [(sv[i] + cc * basis[j][i]) % p for i in range(NS)]
                out.append((fx, sv) if side == "P" else (sv, fx))
                if len(out) > cap:
                    return out, True
    return out, False


def main():
    rows = list(csv.DictReader(open(os.path.join(HERE, "prime_survey.csv"))))
    sup = {}
    for f in os.listdir(os.path.join(HERE, "supports")):
        d = json.load(open(os.path.join(HERE, "supports", f)))
        sup[d["hash"]] = d
    hd = os.path.join(HERE, "hits_nondegenerate")
    os.makedirs(hd, exist_ok=True)
    fh = open(os.path.join(HERE, "census.csv"), "w", newline="")
    F = ["hash", "p", "family", "exact_count", "enumerated", "truncated",
         "n_degenerate", "n_nondegenerate", "n_sampled", "n_verify_fail",
         "tear_nonempty", "tear_empty", "tear_other", "climb_p2", "climb_p3",
         "wall_s"]
    w = csv.DictWriter(fh, fieldnames=F)
    w.writeheader()
    for r in rows:
        if r["verdict"] != "NONEMPTY":
            continue
        p = int(r["p"]); h = r["hash"]
        d = sup[h]
        SP = [tuple(m) for m in d["support_P"]]
        SQ = [tuple(m) for m in d["support_Q"]]
        t0 = time.time()
        sols, trunc = all_solutions(SP, SQ, p)
        nd = [s for s in sols if not degenerate_screen(SP, SQ, s[0], s[1])[0]]
        rec = {"hash": h, "p": p, "family": r["family"],
               "exact_count": r["count"], "enumerated": len(sols),
               "truncated": trunc, "n_degenerate": len(sols) - len(nd),
               "n_nondegenerate": len(nd)}
        staged = []
        nfail = 0
        for (a, b) in nd[:SAMPLE]:
            chk = verify_solution(SP, SQ, a, b, p)
            if not (chk["det_ok"] and chk["coll_ok"]):
                nfail += 1
                continue
            staged.append({"a": a, "b": b, "verify": chk,
                           "tear": tear_data(SP, SQ, a, b, p)})
        staged.sort(key=lambda z: 0 if z["tear"]["tear"] == "TEAR-NONEMPTY" else 1)
        c2 = c3 = 0
        tc = {"TEAR-NONEMPTY": 0, "TEAR-EMPTY": 0}
        other = 0
        for z in staged:
            k = z["tear"]["tear"]
            if k in tc:
                tc[k] += 1
            else:
                other += 1
            l2 = hensel_step(SP, SQ, z["a"], z["b"], p, 1)
            z["lift_to_p2"] = l2 is not None
            if l2 is not None:
                c2 += 1
                z["p2_point"] = {"a": l2[0], "b": l2[1]}
                l3 = hensel_step(SP, SQ, l2[0], l2[1], p, 2)
                z["lift_to_p3"] = l3 is not None
                if l3 is not None:
                    c3 += 1
                    z["p3_point"] = {"a": l3[0], "b": l3[1]}
        rec.update({"n_sampled": len(staged), "n_verify_fail": nfail,
                    "tear_nonempty": tc["TEAR-NONEMPTY"],
                    "tear_empty": tc["TEAR-EMPTY"], "tear_other": other,
                    "climb_p2": c2, "climb_p3": c3,
                    "wall_s": round(time.time() - t0, 3)})
        w.writerow(rec); fh.flush()
        if staged:
            with open(os.path.join(hd, "%s_p%d.json" % (h, p)), "w") as g:
                json.dump({"hash": h, "p": p, "characteristic": p,
                           "family": r["family"],
                           "support_P": [list(m) for m in SP],
                           "support_Q": [list(m) for m in SQ],
                           "exact_count": r["count"],
                           "n_degenerate": rec["n_degenerate"],
                           "n_nondegenerate": rec["n_nondegenerate"],
                           "solutions": staged}, g, indent=1)
        print("%s p=%-3d %-3s tot=%-6s nondeg=%-6d tearNE=%d climb2=%d %.1fs" %
              (h, p, r["family"], r["count"], len(nd), tc["TEAR-NONEMPTY"],
               c2, rec["wall_s"]), flush=True)
    fh.close()


if __name__ == "__main__":
    main()
