"""night13 stage 2 -- the unavoidable-singleton screen over all H-supports.

For an H-support E (a set of x-exponents of the degree-m form H, all in one
residue class mod 3) the induced objects are

    supp(H^2) = {(a+b, 2m-a-b) : a,b in E}      leading form of P, deg 2m
    supp(H^3) = {(a+b+c, 3m-a-b-c)}             leading form of Q, deg 3m
    NP(P) = conv(supp(H^2) u {(0,0), (1,0)})
    NP(Q) = conv(supp(H^3) u {(0,0), (0,1)})

and the MAXIMAL lower pools are all lattice points of those polygons carrying
the required residue, of total degree < 2m resp. < 3m, with (0,0) dropped
from the Q pool (its bracket column is identically zero).

ROUTES.  A route at a bracket row key k is a pair (p, a), p in the P-support
pool (leading u lower), a in the Q one, with p + a = k + (1,1) and
p1 a2 - p2 a1 != 0.  It is ADJUSTABLE if at least one of p, a is a lower
monomial (pure leading x leading contributions cancel key by key, since
[A H^2, B H^3] = 6 A B H^3 (H_x H_y - H_y H_x) = 0).

NORMALIZATION-FORCED ROWS.  The constant row (0,0) has the single route
x = (1,0) times y = (0,1) (section 2.1 of PRESTRATUM.md), so
a_(1,0) b_(0,1) = 1 and both are nonzero in every point of the stratum.  A
mandatory row k != (0,0) is called normalization-forced when EVERY adjustable
route at k pairs one of those two forced monomials with a LEADING-form
monomial.  Its equation is then

    (forced nonzero coefficient) x (an expression in the top parameters) = 0

and it constrains the top parameters alone, with no lower coefficient
available to absorb it.  Two counts are kept:

    F1  exactly one such route          -> a single top monomial must vanish
    F2  exactly two such routes         -> one nontrivial relation between
                                           the top parameters

(there can never be more: a route with a = (0,1) forces p = k + (1,0), and a
route with p = (1,0) forces a = k + (0,1), so at most one of each kind.)

A support SURVIVES the screen iff it has no F1 and no F2 row.

Also recorded, for ranking: NEAR-SINGLETON rows = mandatory rows with exactly
two adjustable routes.  That census is expensive and is computed only for
survivors.

Residue conventions.  With supp(H) in the class r mod 3, supp(P) sits in
2r and supp(Q) in 3r = 0.  The constant bracket row needs a route
P-(1,0) x Q-(0,1) or P-(0,1) x Q-(1,0), i.e. 1 = 2r and 0 = 0 (so r = 2), or
0 = 2r and 1 = 0 (impossible).  r = 0 and r = 1 are therefore screened
separately and are expected to have an unreachable constant row; this is
checked rather than assumed.
"""

import itertools
import json
import os
import sys
import time

import kit as K

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------- fast lattice points

def column_range(hl, i):
    """[ymin, ymax] of the polygon on the vertical line x = i, or None."""
    n = len(hl)
    lo, hi = None, None
    for t in range(n):
        x1, y1 = hl[t]
        x2, y2 = hl[(t + 1) % n]
        if x1 == x2:
            if x1 == i:
                a, b = min(y1, y2), max(y1, y2)
                lo = a if lo is None else min(lo, a)
                hi = b if hi is None else max(hi, b)
            continue
        if not (min(x1, x2) <= i <= max(x1, x2)):
            continue
        # y at x = i on this edge, as an exact rational
        num = y1 * (x2 - x1) + (y2 - y1) * (i - x1)
        den = x2 - x1
        v = (num, den) if den > 0 else (-num, -den)
        yv = v[0] / v[1]
        lo = yv if lo is None else min(lo, yv)
        hi = yv if hi is None else max(hi, yv)
    if lo is None:
        return None
    import math
    return math.ceil(lo - 1e-9), math.floor(hi + 1e-9)


def pool(hl, res, dmax, deg_lt, drop_origin=False):
    out = []
    for i in range(dmax + 1):
        if i % 3 != res:
            continue
        cr = column_range(hl, i)
        if cr is None:
            continue
        j0, j1 = cr
        j1 = min(j1, dmax - i, deg_lt - 1 - i)
        for j in range(max(j0, 0), j1 + 1):
            if drop_origin and i == 0 and j == 0:
                continue
            out.append((i, j))
    return out


# ------------------------------------------------------------- one H-support

def leading_supports(E, m, char=0):
    """supp(H^2) and supp(H^3) for generic h, in the given characteristic.

    The coefficient of x^s in H^k is a sum over multisets of E of size k, each
    with its multinomial coefficient (k = 2: 1 if a = b else 2; k = 3: 1 if
    a = b = c, 3 if exactly two agree, 6 if all differ).  Distinct multisets
    give distinct monomials in the h's, so no cancellation between them can
    occur for generic h, and x^s is in the support iff SOME multiset over it
    has multinomial coefficient nonzero in the characteristic.  In char 2 the
    cross terms of H^2 die (Frobenius: H^2 = sum h_e^2 x^(2e) y^(2m-2e)) and
    in char 3 those of H^3 do; the two extreme exponents 2e0, 2e1 and 3e0,
    3e1 survive in every characteristic, so the Newton polygons are the same.
    """
    nzc = (lambda v: v != 0) if char == 0 else (lambda v: v % char != 0)
    s2 = set()
    for i, a in enumerate(E):
        for b in E[i:]:
            if nzc(1 if a == b else 2):
                s2.add(a + b)
    s3 = set()
    for i, a in enumerate(E):
        for j in range(i, len(E)):
            b = E[j]
            for c in E[j:]:
                if a == b == c:
                    co = 1
                elif a == b or b == c or a == c:
                    co = 3
                else:
                    co = 6
                if nzc(co):
                    s3.add(a + b + c)
    return (sorted((s, 2 * m - s) for s in s2),
            sorted((s, 3 * m - s) for s in s3))



def analyse(E, m, resP, resQ, want_near=False, char=0):
    """E = tuple of H x-exponents.  Returns the screen record.

    char = 0 means "characteristic 0, and every characteristic that divides
    none of the integer factors below"; char = p applies the mod-p test to
    the factor p1 a2 - p2 a1, so routes whose factor is divisible by p do not
    contribute and MORE rows can become normalization-forced.
    """
    nz = (lambda v: v != 0) if char == 0 else (lambda v: v % char != 0)
    SP, SQ = leading_supports(E, m, char)
    hp = K.hull(SP + [(0, 0), (1, 0)])
    hq = K.hull(SQ + [(0, 0), (0, 1)])
    Plow = pool(hp, resP, 2 * m, 2 * m)
    Qlow = pool(hq, resQ, 3 * m, 3 * m, drop_origin=True)
    Pset, Qset = set(Plow), set(Qlow)
    SPset, SQset = set(SP), set(SQ)
    Pall = list(SPset | Pset)
    Qallset = SQset | Qset

    x, y = (1, 0), (0, 1)
    rec = {"E": list(E), "n_pool_P": len(Plow), "n_pool_Q": len(Qlow),
           "n_supp_H2": len(SP), "n_supp_H3": len(SQ),
           "x_in_pool": x in Pset, "y_in_pool": y in Qset}
    if not (x in Pset and y in Qset):
        rec.update({"constant_row_routes": 0, "F1": [], "F2": [],
                    "n_F1": 0, "n_F2": 0, "survives": False,
                    "reason": "constant row unreachable"})
        return rec

    # rows that can possibly be normalization-forced
    cand = {}
    for p in SP:                       # route (leading p) x y
        k = (p[0] - 1, p[1])
        if nz(p[0]) and k != (0, 0):
            cand.setdefault(k, []).append(("Py", p))
    for a in SQ:                       # route x x (leading a)
        k = (a[0], a[1] - 1)
        if nz(a[1]) and k != (0, 0):
            cand.setdefault(k, []).append(("xQ", a))

    F1, F2 = [], []
    for k, base in cand.items():
        K1, K2 = k[0] + 1, k[1] + 1
        other = False
        for p1, p2 in Pall:
            a1, a2 = K1 - p1, K2 - p2
            if a1 < 0 or a2 < 0:
                continue
            a = (a1, a2)
            if a not in Qallset:
                continue
            if not nz(p1 * a2 - p2 * a1):
                continue
            lowP = (p1, p2) in Pset
            lowQ = a in Qset
            if not (lowP or lowQ):
                continue
            if (lowQ and a == y and (p1, p2) in SPset) or \
               (lowP and (p1, p2) == x and a in SQset):
                continue                        # one of the base routes
            other = True
            break
        if other:
            continue
        entry = {"row": list(k),
                 "routes": [[kind, list(v)] for kind, v in base]}
        (F1 if len(base) == 1 else F2).append(entry)

    rec["char"] = char
    rec.update({"constant_row_routes": 1,
                "n_F1": len(F1), "n_F2": len(F2),
                "F1": F1[:6], "F2": F2[:6],
                "survives": not F1 and not F2})
    if rec["survives"] and want_near:
        rec["near_singleton"] = near_census(SP, SQ, Plow, Qlow)
    return rec


def near_census(SP, SQ, Plow, Qlow):
    """rows with exactly 1 / exactly 2 adjustable routes (full census)."""
    cnt = {}
    Ps, Qs = set(Plow), set(Qlow)
    for m in list(SP) + Plow:
        lowP = m in Ps
        for a in list(SQ) + Qlow:
            if not (lowP or a in Qs):
                continue
            if m[0] * a[1] - m[1] * a[0] == 0:
                continue
            kk = (m[0] + a[0] - 1, m[1] + a[1] - 1)
            cnt[kk] = cnt.get(kk, 0) + 1
    return {"n_rows": len(cnt),
            "n_1_route": sum(1 for k, c in cnt.items()
                             if c == 1 and k != (0, 0)),
            "n_2_route": sum(1 for k, c in cnt.items()
                             if c == 2 and k != (0, 0))}


# ------------------------------------------------------------------ the sweep

def exponents(m, r=2):
    return [i for i in range(m + 1) if i % 3 == r]


def sweep(m, resP, resQ, r=2, sizes=(3, 4, 5, 6), tag=""):
    exps = exponents(m, r)
    t0 = time.time()
    recs = []
    by_size = {}
    for s in sizes:
        n_tot = n_surv = 0
        f1hist = {}
        for E in itertools.combinations(exps, s):
            rec = analyse(E, m, resP, resQ)
            n_tot += 1
            f1hist[rec["n_F1"]] = f1hist.get(rec["n_F1"], 0) + 1
            if rec["survives"]:
                n_surv += 1
                rec2 = analyse(E, m, resP, resQ, want_near=True)
                recs.append(rec2)
            elif len(recs) < 4000 and n_tot <= 3:
                recs.append(rec)             # a few worked examples
        by_size[s] = {"n_supports": n_tot, "n_survivors": n_surv,
                      "F1_count_histogram": {str(k): v
                                             for k, v in sorted(f1hist.items())}}
        print("  m=%d %s size %d: %d supports, %d survivors, F1 hist %s (%.1fs)"
              % (m, tag, s, n_tot, n_surv, by_size[s]["F1_count_histogram"],
                 time.time() - t0), flush=True)
    return by_size, recs


def main():
    m = int(sys.argv[1]) if len(sys.argv) > 1 else 42
    out = {"H_degree": m, "deg_P": 2 * m, "deg_Q": 3 * m,
           "degree_pair_divisibility_ordered":
               K.divisibility_ordered(2 * m, 3 * m),
           "2m_mod_3m": (2 * m) % (3 * m), "3m_mod_2m": (3 * m) % (2 * m),
           "arms": {}}
    # the three residue conventions
    for r, resP, resQ, name in ((2, 1, 0, "r2_P1_Q0"),
                                (0, 0, 0, "r0_P0_Q0"),
                                (1, 2, 0, "r1_P2_Q0")):
        print("m=%d arm %s" % (m, name), flush=True)
        exps = exponents(m, r)
        # is the constant row reachable at all?  (1,0) needs 1 = resP,
        # (0,1) needs 0 = resQ; the mirrored route needs 0 = resP and
        # 1 = resQ.
        reach = ((1 % 3 == resP and 0 % 3 == resQ)
                 or (0 % 3 == resP and 1 % 3 == resQ))
        arm = {"H_exponent_residue": r, "P_residue": resP,
               "Q_residue": resQ, "n_exponents": len(exps),
               "exponents": exps,
               "constant_row_reachable_by_residue": reach}
        if not reach:
            arm["by_size"] = "not swept: no monomial pair (p,a) with "\
                             "p+a=(1,1) satisfies the residues"
        else:
            bs, recs = sweep(m, resP, resQ, r, tag=name)
            arm["by_size"] = bs
            arm["records"] = recs
        out["arms"][name] = arm
    path = os.path.join(HERE, "h_screen_m%d.json" % m)
    json.dump(out, open(path, "w"), indent=1)
    print("wrote", path)


if __name__ == "__main__":
    main()


# --------------------------------------------------- structural verification

def predicted_F1(E, m):
    """The two extreme-ray rows.

    Let e0 = min E, e1 = max E and put phi(v) = e1*v2 - (m-e1)*v1 (zero on the
    lower extreme ray of both polygons) and psi(v) = (m-e0)*v1 - e0*v2 (zero
    on the upper one).  Over NP(Q) the minimum of phi is 0, attained on the
    ray; over NP(P) it is -(m-e1), attained only at x = (1,0).  For the row
    k = (3e1, 3(m-e1)-1) one has phi(k + (1,1)) = -(m-e1), so every route
    must have phi(p) = -(m-e1) and phi(a) = 0, i.e. p = x and a the extreme
    H^3 monomial: the row is F1.  Symmetrically psi over NP(P) has minimum 0
    and over NP(Q) minimum -e0 attained only at y = (0,1), and the row
    k = (2e0-1, 2(m-e0)) is F1 with the extreme H^2 monomial.
    """
    e0, e1 = min(E), max(E)
    return sorted([(2 * e0 - 1, 2 * (m - e0)), (3 * e1, 3 * (m - e1) - 1)])


def verify(m, r=2, resP=1, resQ=0, sizes=(3, 4, 5, 6)):
    exps = exponents(m, r)
    n = ok = 0
    for s in sizes:
        for E in itertools.combinations(exps, s):
            rec = analyse(E, m, resP, resQ)
            n += 1
            got = sorted(tuple(f["row"]) for f in rec["F1"])
            if got == predicted_F1(E, m) and rec["n_F1"] == 2 \
                    and rec["n_F2"] == 0:
                ok += 1
    return {"H_degree": m, "n_supports": n, "n_matching_prediction": ok,
            "all_match": ok == n}
