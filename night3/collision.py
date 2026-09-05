#!/usr/bin/env python3
"""
night3/collision.py -- collision-system search over GF(p).

CONTRACT (fixed, implemented exactly as specified):

  Input: a support pair (S_P, S_Q), finite subsets of Z_{>=0}^2, each
  containing (0,0).  Unknowns: one coefficient per support monomial,
  a_{ij} for S_P and b_{ij} for S_Q.

    P = sum_{(i,j) in S_P} a_{ij} x^i y^j
    Q = sum_{(i,j) in S_Q} b_{ij} x^i y^j

  System over GF(p):
    (K) every coefficient of  P_x*Q_y - P_y*Q_x - 1  (as a polynomial in
        x, y) equals 0;
    (C) P(0,0) = 0, Q(0,0) = 0, P(1,0) = 0, Q(1,0) = 0.

  A solution of (K)+(C) is a Keller pair with two distinct colliding
  points, namely (0,0) and (1,0), both mapping to (0,0).

  Solved by Groebner basis over GF(p).  UNIT IDEAL = EMPTY.

The full system is handed to the solver as-is; no equations are
pre-eliminated by this driver.

STATUS OF RESULTS: everything is mod p and reported as such.  See
night3/README.md.
"""
import argparse, hashlib, itertools, json, os, random, subprocess, sys, time

import sympy
from sympy import symbols, groebner

# ---------------- polynomial arithmetic with symbolic coefficients ----------

def mk_poly(support, prefix):
    """{(i,j): Symbol} for the given support."""
    return {(i, j): sympy.Symbol("%s_%d_%d" % (prefix, i, j)) for (i, j) in support}


def diff_x(poly):
    return {(i - 1, j): i * c for (i, j), c in poly.items() if i > 0}


def diff_y(poly):
    return {(i, j - 1): j * c for (i, j), c in poly.items() if j > 0}


def mul(a, b):
    r = {}
    for (i1, j1), c1 in a.items():
        for (i2, j2), c2 in b.items():
            k = (i1 + i2, j1 + j2)
            r[k] = r.get(k, 0) + c1 * c2
    return r


def sub(a, b):
    r = dict(a)
    for k, v in b.items():
        r[k] = r.get(k, 0) - v
    return r


def evaluate(poly, x, y):
    """numeric/symbolic evaluation of a coefficient-dict polynomial."""
    return sum(c * (x ** i) * (y ** j) for (i, j), c in poly.items())


# ---------------- the system ----------------------------------------------

def build_system(SP, SQ, keller=True, collision=True):
    """returns (equations, variables) for the contract system."""
    P, Q = mk_poly(SP, "a"), mk_poly(SQ, "b")
    eqs = []
    if keller:
        # P_x*Q_y - P_y*Q_x - 1
        expr = sub(mul(diff_x(P), diff_y(Q)), mul(diff_y(P), diff_x(Q)))
        expr[(0, 0)] = expr.get((0, 0), 0) - 1
        for _, c in sorted(expr.items()):
            e = sympy.expand(c)
            if e != 0:
                eqs.append(e)
    if collision:
        eqs.append(evaluate(P, 0, 0))
        eqs.append(evaluate(Q, 0, 0))
        eqs.append(evaluate(P, 1, 0))
        eqs.append(evaluate(Q, 1, 0))
    eqs = [sympy.expand(e) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    seen = set().union(*[e.free_symbols for e in eqs]) if eqs else set()
    variables = sorted(seen, key=str)
    return eqs, variables


def solve_system(SP, SQ, p, keller=True, collision=True):
    """EMPTY iff the Groebner basis is the unit ideal."""
    eqs, variables = build_system(SP, SQ, keller, collision)
    t0 = time.time()
    if not eqs:
        return {"verdict": "NONEMPTY", "wall_s": 0.0, "gb_len": 0,
                "note": "no equations"}
    if not variables:
        # constant equations only: nonzero constant => EMPTY
        nz = any(int(e) % p for e in eqs)
        return {"verdict": "EMPTY" if nz else "NONEMPTY",
                "wall_s": round(time.time() - t0, 4), "gb_len": 0,
                "note": "constant system"}
    G = groebner(eqs, *variables, order="grevlex", modulus=p)
    gb = [str(g) for g in G.exprs]
    unit = (gb == ["1"])
    return {"verdict": "EMPTY" if unit else "NONEMPTY",
            "wall_s": round(time.time() - t0, 4),
            "n_eqs": len(eqs), "n_vars": len(variables),
            "gb_len": len(gb),
            "gb": gb if not unit else ["1"]}


# ---------------- support construction ------------------------------------

def dense_support(d):
    return [(i, j) for i in range(d + 1) for j in range(d + 1 - i)]


def polygon_supports(rng, a, b, t, k):
    """P's Newton polygon from 3-5 random base vertices including (0,0) and
    one realizing the top degree; Q's polygon similar with ratio b/a.

    Base vertices v have sum(v) <= t with one at exactly t; P uses a*v and
    Q uses b*v, so deg P = a*t, deg Q = b*t and the two polygons are
    similar with ratio (b*t)/(a*t) = b/a, integrally.
    """
    for _ in range(400):
        nv = rng.randint(3, 5)
        base = [(0, 0)]
        # a vertex realizing the top degree
        i = rng.randint(0, t)
        base.append((i, t - i))
        while len(base) < nv:
            s = rng.randint(1, t)
            i = rng.randint(0, s)
            v = (i, s - i)
            if v not in base:
                base.append(v)
        if not two_dimensional(base):
            continue
        SP = fill_support([(a * i, a * j) for (i, j) in base], k, rng)
        SQ = fill_support([(b * i, b * j) for (i, j) in base], k, rng)
        if (0, 0) in SP and (0, 0) in SQ and \
           max(i + j for i, j in SP) == a * t and \
           max(i + j for i, j in SQ) == b * t:
            return base, sorted(SP), sorted(SQ)
    raise RuntimeError("could not build a 2-dimensional polygon pair")


def two_dimensional(pts):
    """true iff the points are not all collinear."""
    for u, v, w in itertools.combinations(pts, 3):
        cr = (v[0] - u[0]) * (w[1] - u[1]) - (v[1] - u[1]) * (w[0] - u[0])
        if cr != 0:
            return True
    return False


def in_hull(pt, verts):
    """lattice point inside or on the convex hull of verts (2-dimensional)."""
    hull = convex_hull(verts)
    n = len(hull)
    sign = 0
    for idx in range(n):
        u, v = hull[idx], hull[(idx + 1) % n]
        cr = (v[0] - u[0]) * (pt[1] - u[1]) - (v[1] - u[1]) * (pt[0] - u[0])
        if cr != 0:
            s = 1 if cr > 0 else -1
            if sign == 0:
                sign = s
            elif s != sign:
                return False
    return True


def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts

    def half(seq):
        out = []
        for pt in seq:
            while len(out) >= 2:
                u, v = out[-2], out[-1]
                if (v[0] - u[0]) * (pt[1] - u[1]) - (v[1] - u[1]) * (pt[0] - u[0]) <= 0:
                    out.pop()
                else:
                    break
            out.append(pt)
        return out

    lower, upper = half(pts), half(reversed(pts))
    return lower[:-1] + upper[:-1]


def fill_support(verts, k, rng):
    """polygon vertices plus random interior lattice points, budget k."""
    sup = set(convex_hull(verts)) | set(verts)
    lo_i = min(i for i, _ in verts)
    hi_i = max(i for i, _ in verts)
    lo_j = min(j for _, j in verts)
    hi_j = max(j for _, j in verts)
    tries = 0
    while len(sup) < k and tries < 6000:
        tries += 1
        pt = (rng.randint(lo_i, hi_i), rng.randint(lo_j, hi_j))
        if pt in sup:
            continue
        if in_hull(pt, verts):
            sup.add(pt)
    return sup


def support_hash(SP, SQ):
    blob = json.dumps({"P": sorted(map(list, SP)), "Q": sorted(map(list, SQ))},
                      sort_keys=True)
    return hashlib.sha256(blob.encode()).hexdigest()[:12]


# ---------------- worker mode (one solve, so the driver can time it out) ---

def worker(spec_path):
    spec = json.load(open(spec_path))
    SP = [tuple(m) for m in spec["SP"]]
    SQ = [tuple(m) for m in spec["SQ"]]
    res = solve_system(SP, SQ, spec["prime"],
                       keller=spec.get("keller", True),
                       collision=spec.get("collision", True))
    print("RESULT " + json.dumps(res))


def run_solve(SP, SQ, prime, timeout, keller=True, collision=True, tmpdir="/tmp"):
    """run one solve in a subprocess so it can be timed out cleanly."""
    spec = {"SP": [list(m) for m in SP], "SQ": [list(m) for m in SQ],
            "prime": prime, "keller": keller, "collision": collision}
    path = os.path.join(tmpdir, "spec_%s_%d.json" % (support_hash(SP, SQ), prime))
    with open(path, "w") as fh:
        json.dump(spec, fh)
    t0 = time.time()
    try:
        pr = subprocess.run([sys.executable, os.path.abspath(__file__),
                             "worker", "--spec", path],
                            capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"verdict": "TIMEOUT", "wall_s": round(time.time() - t0, 2)}
    wall = round(time.time() - t0, 2)
    for line in pr.stdout.splitlines():
        if line.startswith("RESULT "):
            res = json.loads(line[7:])
            res["wall_s"] = wall
            return res
    return {"verdict": "ERROR", "wall_s": wall,
            "stderr": pr.stderr[-4000:], "stdout": pr.stdout[-2000:]}


# ---------------- controls -------------------------------------------------

PRIMES = [999983, 1000003]


def controls(timeout, outdir):
    """MANDATORY. Hard-exit if violated."""
    log = {"N1": [], "P1": [], "P2": None}
    print("=== CONTROLS ===")

    # P2 first: pure evaluation check, no solver.
    P = {(2, 0): 1, (1, 0): -1}          # x^2 - x
    Q = {(0, 1): 1}                      # y
    vals = {"P(0,0)": evaluate(P, 0, 0), "Q(0,0)": evaluate(Q, 0, 0),
            "P(1,0)": evaluate(P, 1, 0), "Q(1,0)": evaluate(Q, 1, 0)}
    p2_ok = all(v == 0 for v in vals.values())
    log["P2"] = {"values": {k: int(v) for k, v in vals.items()}, "pass": bool(p2_ok)}
    print("P2 %s: P=x^2-x, Q=y satisfies (C): %s"
          % ("PASS" if p2_ok else "FAIL", log["P2"]["values"]))
    if not p2_ok:
        print("CONTROL P2 FAILED -- hard exit")
        _dump(log, outdir)
        sys.exit(2)

    # P1: collision equations alone, dense degree-2 supports -> NONEMPTY.
    S2 = dense_support(2)
    for prime in PRIMES:
        res = run_solve(S2, S2, prime, timeout, keller=False, collision=True)
        log["P1"].append({"prime": prime, **res})
        print("P1 p=%d: %s (%.2fs)" % (prime, res["verdict"], res["wall_s"]))
        if res["verdict"] != "NONEMPTY":
            print("CONTROL P1 FAILED (expected NONEMPTY) -- hard exit")
            _dump(log, outdir)
            sys.exit(2)

    # N1: dense supports of total degree <= 2 and <= 3 -> EMPTY at both primes.
    for d in (2, 3):
        S = dense_support(d)
        for prime in PRIMES:
            res = run_solve(S, S, prime, timeout, keller=True, collision=True)
            log["N1"].append({"degree": d, "prime": prime, **res})
            print("N1 d<=%d p=%d: %s (%.2fs)" % (d, prime, res["verdict"], res["wall_s"]))
            if res["verdict"] == "NONEMPTY":
                print("CONTROL N1 RETURNED NONEMPTY -- instrument anomaly. "
                      "STOPPING EVERYTHING.")
                log["N1_anomaly"] = True
                _dump(log, outdir)
                sys.exit(3)
            if res["verdict"] != "EMPTY":
                print("CONTROL N1 did not complete (%s) -- hard exit"
                      % res["verdict"])
                _dump(log, outdir)
                sys.exit(2)

    print("CONTROLS: PASS")
    log["verdict"] = "PASS"
    _dump(log, outdir)
    return log


def _dump(log, outdir):
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "controls.json"), "w") as fh:
        json.dump(log, fh, indent=1)


# ---------------- sweep ----------------------------------------------------

RATIOS = [(2, 3), (3, 4), (4, 5), (5, 6), (3, 5)]
KS = [10, 14, 18]


def sweep_specs(seed):
    """sparse support pairs at max degree in [126, 200]."""
    rng = random.Random(seed)
    specs = []
    for (a, b) in RATIOS:
        hi = max(a, b)
        ts = [t for t in range(1, 201) if 126 <= hi * t <= 200]
        for t in ts:
            for k in KS:
                specs.append((a, b, t, k))
    rng.shuffle(specs)
    return rng, specs


def sweep(args):
    outdir = args.out
    os.makedirs(outdir, exist_ok=True)
    csv_path = os.path.join(outdir, "collision_sweep.csv")
    supdir = os.path.join(outdir, "supports")
    os.makedirs(supdir, exist_ok=True)
    if not os.path.exists(csv_path):
        with open(csv_path, "w") as fh:
            fh.write("support_hash,deg_P,deg_Q,k,n_mono_P,n_mono_Q,prime,"
                     "verdict,wall_s\n")

    rng, specs = sweep_specs(args.seed)
    t_start = time.time()
    rows = 0
    tally = {}
    for (a, b, t, k) in specs:
        if rows >= args.max_rows:
            break
        if time.time() - t_start > args.budget:
            print("BUDGET REACHED -- stopping sweep")
            break
        try:
            base, SP, SQ = polygon_supports(rng, a, b, t, k)
        except RuntimeError as exc:
            print("skip (a,b,t,k)=%s: %s" % ((a, b, t, k), exc))
            continue
        h = support_hash(SP, SQ)
        degP, degQ = a * t, b * t
        with open(os.path.join(supdir, "support_%s.json" % h), "w") as fh:
            json.dump({"hash": h, "ratio": [a, b], "t": t, "k": k,
                       "deg_P": degP, "deg_Q": degQ,
                       "base_polygon": [list(v) for v in base],
                       "SP": [list(m) for m in SP],
                       "SQ": [list(m) for m in SQ]}, fh, indent=1)
        for prime in PRIMES:
            res = run_solve(SP, SQ, prime, args.timeout)
            v = res["verdict"]
            tally[v] = tally.get(v, 0) + 1
            with open(csv_path, "a") as fh:
                fh.write("%s,%d,%d,%d,%d,%d,%d,%s,%s\n"
                         % (h, degP, degQ, k, len(SP), len(SQ), prime, v,
                            res["wall_s"]))
            rows += 1
            print("row %d: %s deg=(%d,%d) k=%d p=%d -> %s (%.1fs)"
                  % (rows, h, degP, degQ, k, prime, v, res["wall_s"]))

            if v == "NONEMPTY":
                d = os.path.join(outdir, "NONEMPTY_%s" % h)
                os.makedirs(d, exist_ok=True)
                eqs, variables = build_system(SP, SQ)
                with open(os.path.join(d, "system.txt"), "w") as fh:
                    fh.write("prime = %d\n" % prime)
                    fh.write("deg_P = %d, deg_Q = %d, k = %d\n" % (degP, degQ, k))
                    fh.write("S_P = %s\n" % sorted(SP))
                    fh.write("S_Q = %s\n\n" % sorted(SQ))
                    fh.write("variables (%d):\n%s\n\n"
                             % (len(variables), [str(s) for s in variables]))
                    fh.write("equations (%d):\n" % len(eqs))
                    for e in eqs:
                        fh.write("%s\n" % e)
                with open(os.path.join(d, "solver_output.json"), "w") as fh:
                    json.dump({"hash": h, "prime": prime, "ratio": [a, b],
                               "t": t, "k": k, "deg_P": degP, "deg_Q": degQ,
                               "SP": [list(m) for m in SP],
                               "SQ": [list(m) for m in SQ],
                               "raw_result": res}, fh, indent=1)
                print("SWEEP HALTED: a sweep cell returned NONEMPTY, files at %s" % d)
                return rows, tally, d

            if rows % args.commit_every == 0:
                _commit(rows)

    _commit(rows)
    return rows, tally, None


def _commit(rows):
    os.system('cd /home/user/jacobian_planar && git add night3 '
              '&& git commit -q -m "night3: collision sweep progress" '
              '>/dev/null 2>&1; for i in 1 2 3 4 5; do git push -q '
              '>/dev/null 2>&1 && break; sleep $((2**i)); done')
    print("  [committed at %d rows]" % rows)


# ---------------- main -----------------------------------------------------

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sp = ap.add_subparsers(dest="cmd", required=True)

    w = sp.add_parser("worker")
    w.add_argument("--spec", required=True)

    c = sp.add_parser("controls")
    c.add_argument("--timeout", type=int, default=300)
    c.add_argument("--out", default="night3/results")

    s = sp.add_parser("sweep")
    s.add_argument("--seed", type=int, default=20260829)
    s.add_argument("--timeout", type=int, default=300)
    s.add_argument("--out", default="night3")
    s.add_argument("--max-rows", type=int, default=1000)
    s.add_argument("--budget", type=float, default=1e9)
    s.add_argument("--commit-every", type=int, default=10)

    args = ap.parse_args()
    if args.cmd == "worker":
        worker(args.spec)
    elif args.cmd == "controls":
        controls(args.timeout, args.out)
    else:
        rows, tally, hit = sweep(args)
        print("SWEEP DONE rows=%d tally=%s" % (rows, tally))
        if hit:
            print("a sweep cell returned NONEMPTY, files at %s" % hit)
