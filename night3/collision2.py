#!/usr/bin/env python3
"""
night3/collision2.py -- collision-system search, sweep 2.

Same contract as sweep 1 (night3/collision.py): for a support pair
(S_P, S_Q) with one unknown per support monomial,

    (K) every coefficient of P_x*Q_y - P_y*Q_x - 1 vanishes;
    (C) P(0,0) = Q(0,0) = P(1,0) = Q(1,0) = 0;

solved by Groebner basis over GF(p); UNIT IDEAL = EMPTY.  The system
builder, solver wrapper and support hashing are imported unchanged from
night3/collision.py.

What is new here is the SUPPORT GENERATOR.  Supports are taken to be the
exact supports of an actual sparse automorphism, built as a composition of
monomial elementary maps

    (x, y + c*x^a)   and   (x + c*y^b, y)

(2-4 of them, alternating type, random nonzero c mod p) with one general
det-1 affine factor mixed in at a random position, exponents rejected
unless the composition's max degree lands in [126, 220].  (0,0) is added to
both supports.  A pair is rejected if |S_P| + |S_Q| > 140.

WITNESS CONTROL (per support, replaces the (K)-alone check of sweep 1):
the generating automorphism's own coefficients are substituted into the
(K) equation vector and must be exactly zero mod p.  That certifies the
support admits a Keller point.  A violation is a generator bug and
hard-exits.

STATUS OF RESULTS: everything is mod p and reported as such.  See
night3/README.md.
"""
import argparse, json, os, random, sys, time

import sympy

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from collision import (build_system, run_solve, support_hash, convex_hull,
                       in_hull, PRIMES)

# ---------------- numeric polynomial arithmetic mod p ---------------------

def npadd(a, b, p):
    r = dict(a)
    for k, v in b.items():
        r[k] = (r.get(k, 0) + v) % p
    return {k: v for k, v in r.items() if v}


def npmul(a, b, p):
    r = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            k = (i1 + i2, j1 + j2)
            r[k] = (r.get(k, 0) + v1 * v2) % p
    return {k: v for k, v in r.items() if v}


def npscale(a, c, p):
    c %= p
    return {k: (v * c) % p for k, v in a.items() if (v * c) % p}


def nppow(a, n, p):
    r = {(0, 0): 1}
    base = dict(a)
    while n:
        if n & 1:
            r = npmul(r, base, p)
        base = npmul(base, base, p)
        n >>= 1
    return r


def npdiff(a, var, p):
    r = {}
    for (i, j), v in a.items():
        if var == 0 and i > 0:
            r[(i - 1, j)] = (v * i) % p
        elif var == 1 and j > 0:
            r[(i, j - 1)] = (v * j) % p
    return {k: v for k, v in r.items() if v}


def npbracket(a, b, p):
    return npadd(npmul(npdiff(a, 0, p), npdiff(b, 1, p), p),
                 npscale(npmul(npdiff(a, 1, p), npdiff(b, 0, p), p), -1, p), p)


def npdeg(a):
    return max((i + j for i, j in a), default=-1)


# ---------------- the generator -------------------------------------------

def rand_affine_factor(rng, p):
    """general det-1 affine factor (alpha x + beta y + e, gamma x + delta y + f)."""
    while True:
        al = rng.randrange(1, p)
        be, ga = rng.randrange(p), rng.randrange(p)
        de = (1 + be * ga) % p * pow(al, p - 2, p) % p
        if (al * de - be * ga) % p == 1 % p:
            return {"type": "affine", "alpha": al, "beta": be, "gamma": ga,
                    "delta": de, "e": rng.randrange(p), "f": rng.randrange(p)}


def apply_factor(P, Q, fac, p):
    """compose factor after (P, Q): returns fac(P, Q)."""
    t = fac["type"]
    if t == "y":            # (x, y + c*x^a)
        return P, npadd(Q, npscale(nppow(P, fac["exp"], p), fac["c"], p), p)
    if t == "x":            # (x + c*y^b, y)
        return npadd(P, npscale(nppow(Q, fac["exp"], p), fac["c"], p), p), Q
    if t == "affine":
        nP = npadd(npadd(npscale(P, fac["alpha"], p), npscale(Q, fac["beta"], p), p),
                   {(0, 0): fac["e"] % p} if fac["e"] % p else {}, p)
        nQ = npadd(npadd(npscale(P, fac["gamma"], p), npscale(Q, fac["delta"], p), p),
                   {(0, 0): fac["f"] % p} if fac["f"] % p else {}, p)
        return nP, nQ
    raise ValueError(t)


def word_str(word):
    parts = []
    for f in word:
        if f["type"] == "y":
            parts.append("(x, y + %d*x^%d)" % (f["c"], f["exp"]))
        elif f["type"] == "x":
            parts.append("(x + %d*y^%d, y)" % (f["c"], f["exp"]))
        else:
            parts.append("affine[%d,%d;%d,%d]+(%d,%d)"
                         % (f["alpha"], f["beta"], f["gamma"], f["delta"],
                            f["e"], f["f"]))
    return " o ".join(reversed(parts)) + "   (applied left-to-right as listed)"


def gen_support_pair(rng, p, deg_lo=126, deg_hi=220, budget=140, tries=4000):
    """one sparse automorphism and its exact supports, or None."""
    for _ in range(tries):
        n_el = rng.randint(2, 4)
        exps = [rng.randint(2, 20) for _ in range(n_el)]
        prod = 1
        for e in exps:
            prod *= e
        if not (deg_lo <= prod <= deg_hi):
            continue
        start = rng.choice(("x", "y"))
        word = []
        for idx, e in enumerate(exps):
            t = start if idx % 2 == 0 else ("y" if start == "x" else "x")
            word.append({"type": t, "exp": e, "c": rng.randrange(1, p)})
        word.insert(rng.randint(0, len(word)), rand_affine_factor(rng, p))

        P, Q = {(1, 0): 1}, {(0, 1): 1}
        for fac in word:
            P, Q = apply_factor(P, Q, fac, p)
        mx = max(npdeg(P), npdeg(Q))
        if not (deg_lo <= mx <= deg_hi):
            continue
        SP = sorted(set(P) | {(0, 0)})
        SQ = sorted(set(Q) | {(0, 0)})
        if len(SP) + len(SQ) > budget:
            continue
        if npbracket(P, Q, p) != {(0, 0): 1 % p}:
            print("ABORT: generated pair is not Keller -- generator bug")
            sys.exit(4)
        return {"word": word, "word_str": word_str(word), "exps": exps,
                "P": P, "Q": Q, "SP": SP, "SQ": SQ,
                "deg_P": npdeg(P), "deg_Q": npdeg(Q), "max_deg": mx}
    return None


def enlarge(SP, SQ, rng, extra=4):
    """V1: each support enlarged by `extra` random lattice points inside its
    own convex hull."""
    out = []
    for S in (SP, SQ):
        s = set(S)
        verts = convex_hull(list(s))
        lo_i, hi_i = min(i for i, _ in s), max(i for i, _ in s)
        lo_j, hi_j = min(j for _, j in s), max(j for _, j in s)
        added, t = 0, 0
        while added < extra and t < 40000:
            t += 1
            pt = (rng.randint(lo_i, hi_i), rng.randint(lo_j, hi_j))
            if pt in s:
                continue
            if in_hull(pt, verts):
                s.add(pt)
                added += 1
        out.append(sorted(s))
    return out[0], out[1]


# ---------------- witness control -----------------------------------------

def witness_check(SP, SQ, P, Q, p):
    """substitute the generating automorphism's coefficients into the (K)
    equation vector; every entry must be exactly zero mod p."""
    eqs, _ = build_system(SP, SQ, keller=True, collision=False)
    mapping = {}
    for (i, j) in SP:
        mapping[sympy.Symbol("a_%d_%d" % (i, j))] = sympy.Integer(P.get((i, j), 0))
    for (i, j) in SQ:
        mapping[sympy.Symbol("b_%d_%d" % (i, j))] = sympy.Integer(Q.get((i, j), 0))
    bad = []
    for idx, e in enumerate(eqs):
        val = int(sympy.expand(e.xreplace(mapping))) % p
        if val:
            bad.append((idx, val))
    return {"n_keller_eqs": len(eqs), "n_nonzero": len(bad),
            "pass": not bad, "first_failures": bad[:5]}


# ---------------- sweep ----------------------------------------------------

def commit(rows, outdir):
    os.system('cd /home/user/jacobian_planar && git add night3 '
              '&& git commit -q -m "night3: sweep 2 progress" >/dev/null 2>&1; '
              'for i in 1 2 3 4 5; do git push -q >/dev/null 2>&1 && break; '
              'sleep $((2**i)); done')
    print("  [committed at %d rows]" % rows)


def main(args):
    outdir = args.out
    supdir = os.path.join(outdir, "supports2")
    resdir = os.path.join(outdir, "results")
    for d in (outdir, supdir, resdir):
        os.makedirs(d, exist_ok=True)
    csv_path = os.path.join(outdir, "collision_sweep2.csv")
    if not os.path.exists(csv_path):
        with open(csv_path, "w") as fh:
            fh.write("support_hash,variant,deg_P,deg_Q,n_mono_P,n_mono_Q,"
                     "prime,verdict,wall_s\n")

    rng = random.Random(args.seed)
    gen_p = PRIMES[0]          # coefficients of the generating word live here
    rows = 0
    tally = {}
    witness_tally = {"PASS": 0, "FAIL": 0}
    slowest = []
    t_start = time.time()
    pairs = 0

    while pairs < args.pairs:
        if time.time() - t_start > args.budget:
            print("BUDGET REACHED -- stopping sweep 2")
            break
        g = gen_support_pair(rng, gen_p)
        if g is None:
            print("generator exhausted its tries")
            break
        pairs += 1
        SP0, SQ0 = g["SP"], g["SQ"]
        SP1, SQ1 = enlarge(SP0, SQ0, rng, extra=4)
        h = support_hash(SP0, SQ0)

        rec = {"hash": h, "word_str": g["word_str"], "exps": g["exps"],
               "word": [{k: v for k, v in f.items()} for f in g["word"]],
               "deg_P": g["deg_P"], "deg_Q": g["deg_Q"], "max_deg": g["max_deg"],
               "n_mono_P": len(SP0), "n_mono_Q": len(SQ0),
               "generating_prime": gen_p,
               "V0": {"SP": [list(m) for m in SP0], "SQ": [list(m) for m in SQ0]},
               "V1": {"SP": [list(m) for m in SP1], "SQ": [list(m) for m in SQ1]},
               "witness": {}}
        print("pair %d: %s deg=(%d,%d) |SP|=%d |SQ|=%d word_exps=%s"
              % (pairs, h, g["deg_P"], g["deg_Q"], len(SP0), len(SQ0), g["exps"]))

        # WITNESS CONTROL on both variants
        for vname, (SPv, SQv) in (("V0", (SP0, SQ0)), ("V1", (SP1, SQ1))):
            w = witness_check(SPv, SQv, g["P"], g["Q"], gen_p)
            rec["witness"][vname] = w
            witness_tally["PASS" if w["pass"] else "FAIL"] += 1
            print("  witness %s: %s (%d Keller eqs, %d nonzero)"
                  % (vname, "PASS" if w["pass"] else "FAIL",
                     w["n_keller_eqs"], w["n_nonzero"]))
            if not w["pass"]:
                rec["ABORT"] = "witness control failed on " + vname
                with open(os.path.join(supdir, "support2_%s.json" % h), "w") as fh:
                    json.dump(rec, fh, indent=1)
                print("WITNESS CONTROL FAILED -- generator bug -- hard exit")
                commit(rows, outdir)
                sys.exit(5)

        with open(os.path.join(supdir, "support2_%s.json" % h), "w") as fh:
            json.dump(rec, fh, indent=1)

        for vname, (SPv, SQv) in (("V0", (SP0, SQ0)), ("V1", (SP1, SQ1))):
            for prime in PRIMES:
                res = run_solve(SPv, SQv, prime, args.timeout)
                v = res["verdict"]
                tally[v] = tally.get(v, 0) + 1
                slowest.append((res["wall_s"], h, vname, prime, v))
                with open(csv_path, "a") as fh:
                    fh.write("%s,%s,%d,%d,%d,%d,%d,%s,%s\n"
                             % (h, vname, g["deg_P"], g["deg_Q"], len(SPv),
                                len(SQv), prime, v, res["wall_s"]))
                rows += 1
                print("  row %d: %s %s p=%d -> %s (%.1fs)"
                      % (rows, h, vname, prime, v, res["wall_s"]))

                if v == "NONEMPTY":
                    d = os.path.join(outdir, "NONEMPTY_%s" % h)
                    os.makedirs(d, exist_ok=True)
                    eqs, variables = build_system(SPv, SQv)
                    with open(os.path.join(d, "system.txt"), "w") as fh:
                        fh.write("sweep 2, variant %s, prime %d\n" % (vname, prime))
                        fh.write("deg_P = %d, deg_Q = %d\n" % (g["deg_P"], g["deg_Q"]))
                        fh.write("generating word: %s\n" % g["word_str"])
                        fh.write("S_P = %s\nS_Q = %s\n\n" % (SPv, SQv))
                        fh.write("variables (%d):\n%s\n\n"
                                 % (len(variables), [str(s) for s in variables]))
                        fh.write("equations (%d):\n" % len(eqs))
                        for e in eqs:
                            fh.write("%s\n" % e)
                    with open(os.path.join(d, "solver_output.json"), "w") as fh:
                        json.dump({"record": rec, "variant": vname,
                                   "prime": prime, "raw_result": res}, fh, indent=1)
                    print("SWEEP 2 HALTED: NONEMPTY, files at %s" % d)
                    _finish(rows, tally, witness_tally, slowest, resdir)
                    commit(rows, outdir)
                    return d

                if rows % args.commit_every == 0:
                    commit(rows, outdir)

    _finish(rows, tally, witness_tally, slowest, resdir)
    commit(rows, outdir)
    print("SWEEP 2 DONE pairs=%d rows=%d tally=%s witness=%s"
          % (pairs, rows, tally, witness_tally))
    return None


def _finish(rows, tally, witness_tally, slowest, resdir):
    slowest.sort(reverse=True)
    top = [{"wall_s": w, "hash": h, "variant": v, "prime": p, "verdict": vd}
           for (w, h, v, p, vd) in slowest[:5]]
    with open(os.path.join(resdir, "sweep2_summary.json"), "w") as fh:
        json.dump({"rows": rows, "verdict_tally": tally,
                   "witness_tally": witness_tally, "slowest_5": top}, fh, indent=1)
    print("slowest 5: %s" % top)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, default=20260830)
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--out", default="night3")
    ap.add_argument("--pairs", type=int, default=25)
    ap.add_argument("--budget", type=float, default=1e9)
    ap.add_argument("--commit-every", type=int, default=10)
    main(ap.parse_args())
