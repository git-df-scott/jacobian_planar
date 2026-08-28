#!/usr/bin/env python3
"""
night4/tail.py -- formal-inverse tail evaluator over F_p.

Self-contained: standard library only (numpy is permitted but not needed,
so it is not imported).  Nothing is imported from night2/ or night3/; the
tame-automorphism sampler is reimplemented here.

MATH CONTRACT
-------------
Input: a pair F = (P, Q) over F_p with P(0,0) = Q(0,0) = 0 and invertible
linear part L (the 2x2 matrix of the degree-1 coefficients, det L != 0;
for Keller pairs det L = 1).

Compute the formal inverse G = (G1, G2) with G(F) = id, homogeneous degree
by degree up to a bound D.  Writing G = sum_m G^(m) with G^(m) homogeneous
of degree m, the degree-d part of the composition G(F) is

    [G(F)]_d = G^(d) o L  +  K_d,

where K_d collects the contributions of the lower-degree parts G^(m), m < d,
composed with the higher-degree parts of F -- all of them already known when
G^(d) is being solved for.  Requiring [G(F)]_d = 0 for d >= 2 gives

    G^(d) = (-K_d) o L^{-1},        and        G^(1) = L^{-1}.

MANDATORY SELF-CHECK: at the end the assembled G is composed with F from
scratch, independently of the incremental recursion that produced it, and
the result must equal the identity exactly, coefficient by coefficient,
through degree D:  G_{<=D}(F) = id + O(degree D+1).

TAIL(F, D) = the list of norms (number of nonzero coefficients, counted
across both components) of G^(m) for m from deg F + 1 to D.

STATUS OF RESULTS: everything is mod p and reported as such.
"""
import argparse
import random
import sys
import time

# ---------------------------------------------------------------------------
# polynomials mod p: dict {(i, j): coeff}, always reduced and zero-stripped
# ---------------------------------------------------------------------------

def padd(a, b, p):
    r = dict(a)
    for k, v in b.items():
        nv = (r.get(k, 0) + v) % p
        if nv:
            r[k] = nv
        else:
            r.pop(k, None)
    return r


def pscale(a, c, p):
    c %= p
    if c == 0:
        return {}
    return {k: (v * c) % p for k, v in a.items() if (v * c) % p}


def pmul_trunc(a, b, p, D):
    r = {}
    for (i1, j1), v1 in a.items():
        for (i2, j2), v2 in b.items():
            if i1 + i2 + j1 + j2 > D:
                continue
            k = (i1 + i2, j1 + j2)
            nv = (r.get(k, 0) + v1 * v2) % p
            if nv:
                r[k] = nv
            else:
                r.pop(k, None)
    return r


def pdeg(a):
    return max((i + j for i, j in a), default=-1)


def homog_part(a, d):
    return {k: v for k, v in a.items() if k[0] + k[1] == d}


def truncate(a, D):
    return {k: v for k, v in a.items() if k[0] + k[1] <= D}


def nnz(a):
    return len(a)


# ---------------------------------------------------------------------------
# linear algebra mod p for the 2x2 linear part
# ---------------------------------------------------------------------------

def linear_part(P, Q, p):
    return [[P.get((1, 0), 0) % p, P.get((0, 1), 0) % p],
            [Q.get((1, 0), 0) % p, Q.get((0, 1), 0) % p]]


def det2(L, p):
    return (L[0][0] * L[1][1] - L[0][1] * L[1][0]) % p


def inv2(L, p):
    d = det2(L, p)
    if d == 0:
        raise ValueError("linear part is singular mod p")
    di = pow(d, p - 2, p)
    return [[(L[1][1] * di) % p, (-L[0][1] * di) % p],
            [(-L[1][0] * di) % p, (L[0][0] * di) % p]]


def subst_linear(A, M, p):
    """A(x, y) with x -> M[0][0]x + M[0][1]y, y -> M[1][0]x + M[1][1]y.
    Degree-preserving, so a homogeneous A stays homogeneous."""
    xs = {(1, 0): M[0][0] % p, (0, 1): M[0][1] % p}
    ys = {(1, 0): M[1][0] % p, (0, 1): M[1][1] % p}
    xs = {k: v for k, v in xs.items() if v}
    ys = {k: v for k, v in ys.items() if v}
    D = pdeg(A)
    xpow = [{(0, 0): 1}]
    ypow = [{(0, 0): 1}]
    for _ in range(D):
        xpow.append(pmul_trunc(xpow[-1], xs, p, D))
        ypow.append(pmul_trunc(ypow[-1], ys, p, D))
    out = {}
    for (i, j), c in A.items():
        out = padd(out, pscale(pmul_trunc(xpow[i], ypow[j], p, D), c, p), p)
    return out


# ---------------------------------------------------------------------------
# composition A(P, Q) truncated at total degree D
# ---------------------------------------------------------------------------

def make_powers(P, Q, p, D):
    Ppow = [{(0, 0): 1}]
    Qpow = [{(0, 0): 1}]
    for _ in range(D):
        Ppow.append(pmul_trunc(Ppow[-1], P, p, D))
        Qpow.append(pmul_trunc(Qpow[-1], Q, p, D))
    return Ppow, Qpow


def compose_trunc(A, Ppow, Qpow, p, D):
    out = {}
    for (i, j), c in A.items():
        if i + j > D:
            continue
        out = padd(out, pscale(pmul_trunc(Ppow[i], Qpow[j], p, D), c, p), p)
    return out


# ---------------------------------------------------------------------------
# the formal inverse
# ---------------------------------------------------------------------------

def formal_inverse(P, Q, p, D):
    """returns (Gparts, G1, G2, selfcheck) where Gparts[m] = (A_m, B_m),
    the homogeneous degree-m parts of the two components of G."""
    if P.get((0, 0), 0) % p or Q.get((0, 0), 0) % p:
        raise ValueError("F must satisfy P(0,0) = Q(0,0) = 0")
    L = linear_part(P, Q, p)
    if det2(L, p) == 0:
        raise ValueError("linear part of F is not invertible mod p")
    Linv = inv2(L, p)

    Ppow, Qpow = make_powers(P, Q, p, D)

    # G^(1) = L^{-1}
    A = {(1, 0): Linv[0][0], (0, 1): Linv[0][1]}
    B = {(1, 0): Linv[1][0], (0, 1): Linv[1][1]}
    A = {k: v for k, v in A.items() if v % p}
    B = {k: v for k, v in B.items() if v % p}
    Gparts = {1: (A, B)}

    # running composition S = sum_{m <= current} G^(m)(F), truncated at D
    S1 = compose_trunc(A, Ppow, Qpow, p, D)
    S2 = compose_trunc(B, Ppow, Qpow, p, D)

    for d in range(2, D + 1):
        K1 = homog_part(S1, d)
        K2 = homog_part(S2, d)
        Ad = subst_linear(pscale(K1, -1, p), Linv, p)
        Bd = subst_linear(pscale(K2, -1, p), Linv, p)
        Gparts[d] = (Ad, Bd)
        if Ad:
            S1 = padd(S1, compose_trunc(Ad, Ppow, Qpow, p, D), p)
        if Bd:
            S2 = padd(S2, compose_trunc(Bd, Ppow, Qpow, p, D), p)

    G1 = {}
    G2 = {}
    for d in range(1, D + 1):
        G1 = padd(G1, Gparts[d][0], p)
        G2 = padd(G2, Gparts[d][1], p)

    # MANDATORY self-check, recomposed from scratch
    C1 = compose_trunc(G1, Ppow, Qpow, p, D)
    C2 = compose_trunc(G2, Ppow, Qpow, p, D)
    ok = (C1 == {(1, 0): 1 % p}) and (C2 == {(0, 1): 1 % p})
    detail = None
    if not ok:
        bad = []
        for name, C, want in (("G1(F)", C1, {(1, 0): 1 % p}),
                              ("G2(F)", C2, {(0, 1): 1 % p})):
            for k in sorted(set(C) | set(want)):
                if C.get(k, 0) != want.get(k, 0):
                    bad.append((name, k, C.get(k, 0), want.get(k, 0)))
        detail = bad[:12]
    return Gparts, G1, G2, {"pass": ok, "mismatches": detail}


def tail(P, Q, p, D):
    degF = max(pdeg(P), pdeg(Q))
    Gparts, G1, G2, chk = formal_inverse(P, Q, p, D)
    norms = [nnz(Gparts[m][0]) + nnz(Gparts[m][1]) for m in range(degF + 1, D + 1)]
    return {"deg_F": degF, "D": D, "tail": norms,
            "tail_all_zero": all(n == 0 for n in norms),
            "selfcheck": chk, "deg_G": max(pdeg(G1), pdeg(G2))}


# ---------------------------------------------------------------------------
# tame automorphism sampler (reimplemented here; nothing imported)
# ---------------------------------------------------------------------------

def rand_affine(rng, p):
    """random det-1 affine map (a x + b y + e, c x + d y + f)."""
    while True:
        a = rng.randrange(1, p)
        b, c = rng.randrange(p), rng.randrange(p)
        d = (1 + b * c) % p * pow(a, p - 2, p) % p
        if (a * d - b * c) % p == 1 % p:
            return ({(1, 0): a, (0, 1): b, (0, 0): rng.randrange(p)},
                    {(1, 0): c, (0, 1): d, (0, 0): rng.randrange(p)})


def compose_pair(outer1, outer2, P, Q, p, D):
    Ppow, Qpow = make_powers(P, Q, p, D)
    return (compose_trunc(outer1, Ppow, Qpow, p, D),
            compose_trunc(outer2, Ppow, Qpow, p, D))


def factorizations(d):
    """multiplicative factorizations of d into factors >= 2 (non-increasing)."""
    out = []

    def rec(rem, lo, acc):
        if rem == 1:
            if acc:
                out.append(tuple(acc))
            return
        for f in range(lo, rem + 1):
            if rem % f == 0:
                rec(rem // f, f, acc + [f])
    rec(d, 2, [])
    return out


def sample_tame(rng, p, d, D):
    """random tame automorphism of total degree exactly d, constant terms
    removed so that P(0,0) = Q(0,0) = 0."""
    facs = factorizations(d)
    md = rng.choice(facs) if facs else ()
    P, Q = {(1, 0): 1}, {(0, 1): 1}
    A, B = rand_affine(rng, p)
    P, Q = compose_pair(A, B, P, Q, p, D)
    for e in md:
        # triangular (x, y + phi(x)) with phi of exact degree e
        phi = {(k, 0): rng.randrange(p) for k in range(2, e)}
        phi[(e, 0)] = rng.randrange(1, p)
        phi = {k: v for k, v in phi.items() if v}
        Ppow, Qpow = make_powers(P, Q, p, D)
        Q = padd(Q, compose_trunc(phi, Ppow, Qpow, p, D), p)
        A, B = rand_affine(rng, p)
        P, Q = compose_pair(A, B, P, Q, p, D)
    # strip constant terms (composition with a translation; still an automorphism)
    P = {k: v for k, v in P.items() if k != (0, 0)}
    Q = {k: v for k, v in Q.items() if k != (0, 0)}
    return P, Q


# ---------------------------------------------------------------------------
# Newton-polygon helpers for the perturbation measurement
# ---------------------------------------------------------------------------

def convex_hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts

    def half(seq):
        out = []
        for q in seq:
            while len(out) >= 2:
                u, v = out[-2], out[-1]
                if (v[0] - u[0]) * (q[1] - u[1]) - (v[1] - u[1]) * (q[0] - u[0]) <= 0:
                    out.pop()
                else:
                    break
            out.append(q)
        return out

    lo, hi = half(pts), half(list(reversed(pts)))
    return lo[:-1] + hi[:-1]


def in_hull(pt, hull):
    if len(hull) < 3:
        return pt in hull
    sign = 0
    n = len(hull)
    for i in range(n):
        u, v = hull[i], hull[(i + 1) % n]
        cr = (v[0] - u[0]) * (pt[1] - u[1]) - (v[1] - u[1]) * (pt[0] - u[0])
        if cr:
            s = 1 if cr > 0 else -1
            if sign == 0:
                sign = s
            elif s != sign:
                return False
    return True


def non_vertex_points(poly):
    """lattice points in the Newton polygon of `poly` that are NOT hull
    vertices and are not the origin."""
    sup = list(poly.keys())
    hull = convex_hull(sup)
    verts = set(hull)
    lo_i = min(i for i, _ in sup)
    hi_i = max(i for i, _ in sup)
    lo_j = min(j for _, j in sup)
    hi_j = max(j for _, j in sup)
    out = []
    for i in range(lo_i, hi_i + 1):
        for j in range(lo_j, hi_j + 1):
            pt = (i, j)
            if pt in verts or pt == (0, 0):
                continue
            if in_hull(pt, hull):
                out.append(pt)
    return out


# ---------------------------------------------------------------------------
# controls
# ---------------------------------------------------------------------------

def hard_exit(msg, code=2):
    print("CONTROL FAILED: %s -- hard exit" % msg)
    sys.exit(code)


def control_T1(rng, p, log):
    print("=== T1: tails of 20 random tame automorphisms, degrees 4..12 ===")
    t0 = time.time()
    rows = []
    ok_all = True
    for k in range(20):
        d = 4 + (k % 9)
        D = 2 * d + 6
        P, Q = sample_tame(rng, p, d, D)
        degF = max(pdeg(P), pdeg(Q))
        r = tail(P, Q, p, D)
        good = r["tail_all_zero"] and r["selfcheck"]["pass"] and degF == d
        ok_all &= good
        rows.append({"i": k + 1, "target_deg": d, "deg_F": degF, "D": D,
                     "deg_G": r["deg_G"], "tail": r["tail"],
                     "tail_all_zero": r["tail_all_zero"],
                     "selfcheck": r["selfcheck"]["pass"]})
        print("  %2d: deg F=%2d (target %2d) D=%2d deg G=%2d  tail all zero: %-5s "
              " self-check: %s"
              % (k + 1, degF, d, D, r["deg_G"], r["tail_all_zero"],
                 "PASS" if r["selfcheck"]["pass"] else "FAIL"))
        if not r["selfcheck"]["pass"]:
            print("    self-check mismatches: %s" % r["selfcheck"]["mismatches"])
        if not r["tail_all_zero"]:
            print("    NONZERO TAIL: %s" % r["tail"])
    wall = time.time() - t0
    log["T1"] = {"rows": rows, "wall_s": round(wall, 2), "pass": bool(ok_all)}
    print("  T1 wall: %.2f s" % wall)
    if not ok_all:
        hard_exit("T1 (an automorphism produced a nonzero tail, or a self-check "
                  "failed, or the sampled degree missed its target)")
    print("T1 PASS\n")


def control_T2(p, log):
    print("=== T2: non-Keller map P = x + y^2 + x^3, Q = y + x^2, D = 12 ===")
    t0 = time.time()
    P = {(1, 0): 1, (0, 2): 1, (3, 0): 1}
    Q = {(0, 1): 1, (2, 0): 1}
    D = 12
    r = tail(P, Q, p, D)
    wall = time.time() - t0
    print("  deg F = %d, D = %d, deg G (truncated) = %d" % (r["deg_F"], D, r["deg_G"]))
    print("  tail (m = %d..%d): %s" % (r["deg_F"] + 1, D, r["tail"]))
    print("  self-check: %s" % ("PASS" if r["selfcheck"]["pass"] else "FAIL"))
    nonzero = any(n for n in r["tail"])
    log["T2"] = {"deg_F": r["deg_F"], "D": D, "tail": r["tail"],
                 "tail_nonzero_somewhere": bool(nonzero),
                 "selfcheck": r["selfcheck"]["pass"], "wall_s": round(wall, 3)}
    print("  T2 wall: %.3f s" % wall)
    if not r["selfcheck"]["pass"]:
        hard_exit("T2 self-check")
    if not nonzero:
        hard_exit("T2 (the evaluator saw no tail on a non-automorphism)")
    print("T2 PASS\n")


# ---------------------------------------------------------------------------
# perturbation measurement
# ---------------------------------------------------------------------------

def perturbation(rng, p, log, n=5):
    print("=== perturbation measurement: +1 on one random non-vertex coefficient ===")
    t0 = time.time()
    rows = []
    for k in range(n):
        d = 4 + (k % 5)
        D = 2 * d + 6
        while True:
            P, Q = sample_tame(rng, p, d, D)
            which = rng.choice(("P", "Q"))
            target = P if which == "P" else Q
            cands = non_vertex_points(target)
            if not cands:
                continue
            pt = rng.choice(cands)
            P2, Q2 = dict(P), dict(Q)
            tgt = P2 if which == "P" else Q2
            nv = (tgt.get(pt, 0) + 1) % p
            if nv:
                tgt[pt] = nv
            else:
                tgt.pop(pt, None)
            L2 = linear_part(P2, Q2, p)
            if det2(L2, p) == 0:
                continue
            break
        base = tail(P, Q, p, D)
        pert = tail(P2, Q2, p, D)
        lit = any(x for x in pert["tail"])
        rows.append({"i": k + 1, "deg_F": base["deg_F"], "D": D,
                     "perturbed_component": which, "perturbed_monomial": list(pt),
                     "was_in_support": pt in (P if which == "P" else Q),
                     "baseline_tail_all_zero": base["tail_all_zero"],
                     "perturbed_tail": pert["tail"],
                     "perturbed_tail_lights_up": bool(lit),
                     "perturbed_selfcheck": pert["selfcheck"]["pass"],
                     "first_nonzero_degree":
                         next((base["deg_F"] + 1 + i
                               for i, x in enumerate(pert["tail"]) if x), None)})
        print("  %d: deg F=%d D=%d  perturbed %s at %s (was in support: %s)"
              % (k + 1, base["deg_F"], D, which, pt,
                 pt in (P if which == "P" else Q)))
        print("     baseline tail all zero: %s | perturbed tail lights up: %s"
              % (base["tail_all_zero"], lit))
        print("     perturbed tail: %s" % pert["tail"])
        print("     perturbed self-check: %s"
              % ("PASS" if pert["selfcheck"]["pass"] else "FAIL"))
        if not pert["selfcheck"]["pass"]:
            hard_exit("perturbation self-check")
    wall = time.time() - t0
    log["perturbation"] = {"rows": rows, "wall_s": round(wall, 2),
                           "n_lit": sum(1 for r in rows
                                        if r["perturbed_tail_lights_up"])}
    print("  perturbation wall: %.2f s" % wall)
    print("  lit up in %d of %d\n" % (log["perturbation"]["n_lit"], n))


# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--prime", type=int, default=999983)
    ap.add_argument("--seed", type=int, default=20260831)
    args = ap.parse_args()
    p = args.prime
    rng = random.Random(args.seed)
    log = {"prime": p, "seed": args.seed}
    t0 = time.time()
    print("night4/tail.py -- formal-inverse tail evaluator, p = %d, seed = %d\n"
          % (p, args.seed))
    control_T1(rng, p, log)
    control_T2(p, log)
    print("T3: the composition self-check is run inside every tail() call above "
          "and below; every one reported PASS so far.\n")
    perturbation(rng, p, log)
    log["total_wall_s"] = round(time.time() - t0, 2)
    print("TOTAL wall: %.2f s" % log["total_wall_s"])
    print("CONTROLS: PASS (T1, T2, T3)")
    return log


if __name__ == "__main__":
    main()
