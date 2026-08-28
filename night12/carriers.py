"""night12 v1 -- family M1 (the cusp-square mu_3 carrier) and the Q-carriers
for the degree-escalation stages Y / C / W.

M1, at the exact 2:3 profiles under degree 200:
    n = deg P = 2m,  deg Q = 3m,   (n, 3m) in {(126,189),(128,192),(130,195),(132,198)}
    H_m   sparse form, monomials x^i y^(m-i) with i = 2 (mod 3), 2..6 terms
    P     = x + A*H_m^2 + P_lower,  every P_lower monomial has i = 1 (mod 3)
    Q     searched on the carrier with top B*H_m^3 and exponents a = 0 (mod 3)

The mu_3 grading is consistent: supp(P) sits in a = 1 (mod 3), supp(Q) in
a = 0 (mod 3), and both P_x Q_y and P_y Q_x then land in a = 0 (mod 3),
which contains the constant monomial (0,0) that the Keller equation needs.

Kernel deflation.  The trivial directions Q -> Q + h(P) are quotiented out
automatically here: P^k has a = k (mod 3), so among the powers of P only
P^0 = 1 meets the carrier grading, and P^3 has degree 6m, above every stage
bound.  The single surviving direction is Q -> Q + const, whose column in the
matrix is identically zero (the factor p1*a2 - p2*a1 vanishes at a = (0,0)).
It is dropped explicitly and the deflated kernel dimension is recorded.
"""

import random
import matekit as M

SEED = 20260831
PROFILES = [(126, 189), (128, 192), (130, 195), (132, 198)]


def rand_H(rnd, m, terms):
    """sparse form of degree m, monomials x^i y^(m-i) with i = 2 (mod 3)."""
    idx = [i for i in range(m + 1) if i % 3 == 2]
    if len(idx) < terms:
        return None
    pick = sorted(rnd.sample(idx, terms))
    return {(i, m - i): rnd.randrange(1, 6) * rnd.choice([1, -1]) for i in pick}


def make_P(rnd, m, terms, n_lower):
    H = rand_H(rnd, m, terms)
    if H is None:
        return None, None
    A = rnd.choice([1, -1, 2, 3])
    P = {(1, 0): 1}
    for k, v in M.pmul(H, H).items():
        P[k] = P.get(k, 0) + A * v
    lower = {}
    for _ in range(n_lower):
        d = rnd.randrange(2, 2 * m)
        cand = [i for i in range(d + 1) if i % 3 == 1]
        if not cand:
            continue
        i = rnd.choice(cand)
        lower[(i, d - i)] = rnd.randrange(1, 4) * rnd.choice([1, -1])
    for k, v in lower.items():
        if k[0] + k[1] < 2 * m:
            P[k] = P.get(k, 0) + v
    P = {k: v for k, v in P.items() if v != 0}
    if M.pdeg(P) != 2 * m:
        return None, None
    if any(i % 3 != 1 for (i, j) in P):
        return None, None
    return P, H


def _hull_inside(pts, D):
    verts = M._hull(sorted(set(pts)))
    out = []
    for a in range(D + 1):
        for b in range(D + 1 - a):
            if a % 3 == 0 and M._inside(verts, (a, b)):
                out.append((a, b))
    return out


def carrier(H, m, stage, cap):
    """Q-carrier for the given escalation stage.

    Y : deg Q < deg P            (younger-mate stage)
    C : deg Q <= 3*deg P/2       (the H^3 carrier)
    W : deg Q <= 2*deg P - 1     (widened)

    The polygon is conv( supp(H^s) u {(0,0),(0,1)} ) scaled to the stage
    bound, and every point carries a = 0 (mod 3).  If the count exceeds the
    cap the carrier is thinned on the second exponent (b = 0 mod t) for the
    least t that fits; (0,0) and (0,1) are always retained and the thinning
    index is recorded.
    """
    H3 = M.ppow(H, 3)
    if stage == "Y":
        D = 2 * m - 1
    elif stage == "C":
        D = 3 * m
    elif stage == "W":
        D = 4 * m - 1
    else:
        raise ValueError(stage)
    # Scale the H^3 polygon to the stage bound (exact, on a common-denominator
    # lattice: a carrier point (a,b) is tested as (a*den, b*den)).
    #
    # The ANCHORS (0,0) and (0,1) are adjoined at their true positions, i.e.
    # already multiplied by den, and are NOT scaled by num.  H is a form, so
    # supp(H^3) lies on the single line a+b = 3m and conv(supp(H^3)) is a
    # segment; the anchors are what make the carrier two-dimensional and, in
    # particular, are what put the monomial (0,1) in it.  Scaling them by
    # num/den < 1 (which is every stage with D < 3m, i.e. stage Y) shrank
    # (0,1) below the lattice and dropped it, contradicting this function's
    # own stated contract that (0,0) and (0,1) are always retained.
    #
    # Consequence of the old behaviour, recorded: with (0,1) absent the row of
    # the Keller system at the constant monomial was identically zero, because
    # the only carrier column that can meet it through the linear term x of P
    # is exactly a = (1,1)-(1,0) = (0,1).  Stage Y then returned EMPTY_over_Q
    # by the degenerate zero-row certificate for every M1 P -- a true statement
    # about that carrier, but a vacuous one.  Restoring the anchors strictly
    # ENLARGES the carrier, so it can only strengthen an emptiness verdict and
    # can only help a mate be found; it cannot make a true emptiness false.
    # The anchors are adjoined BOTH scaled (as before) and unscaled, i.e. the
    # polygon is the convex hull of the union.  Taking the union rather than
    # replacing keeps the new carrier a superset of the old one at every
    # stage: when D > 3m the old scaling inflated the anchors outward, and
    # dropping that would have SHRUNK stage W, which weakens an emptiness
    # verdict.  Enlarging is the only safe direction here.
    num, den = D, 3 * m
    anchors = [(0, 0), (0, 1)]
    pts = ([(p[0] * num, p[1] * num) for p in H3]
           + [(p[0] * num, p[1] * num) for p in anchors]
           + [(p[0] * den, p[1] * den) for p in anchors])
    verts = M._hull(sorted(set(pts)))
    S = []
    for a in range(D + 1):
        if a % 3:
            continue
        for b in range(D + 1 - a):
            if M._inside(verts, (a * den, b * den)):
                S.append((a, b))
    info = {"stage": stage, "deg_Q_bound": D, "n_raw": len(S), "thin_t": 1}
    t = 1
    keep = set([(0, 0), (0, 1)])
    while len(S) > cap:
        t += 1
        S = sorted(set([p for p in S if p[1] % t == 0]) | (keep & set(S)))
        info["thin_t"] = t
        if t > 60:
            break
    # kernel deflation: the identically-zero column a = (0,0)
    S = [p for p in sorted(set(S)) if p != (0, 0)]
    info["n_used"] = len(S)
    info["deflated_kernel_dim"] = 1
    return S, info


def build_M1(n_per_profile=10):
    rnd = random.Random(SEED)
    out = []
    for (n, dq) in PROFILES:
        m = n // 2
        made = 0
        tries = 0
        while made < n_per_profile and tries < 400:
            tries += 1
            terms = rnd.randrange(2, 7)
            P, H = make_P(rnd, m, terms, rnd.randrange(0, 4))
            if P is None:
                continue
            out.append({"family": "M1", "profile": "(%d,%d)" % (n, dq),
                        "deg_P": n, "deg_Q_target": dq, "m": m,
                        "H_terms": terms, "P": P, "H": H})
            made += 1
    return out


if __name__ == "__main__":
    items = build_M1(3)
    for it in items[:12]:
        print(it["profile"], "|supp P|=%d" % len(it["P"]), "|H|=%d" % len(it["H"]), end="  ")
        for st in ("Y", "C", "W"):
            S, info = carrier(it["H"], it["m"], st, 100000)
            print("%s:raw=%d" % (st, info["n_raw"]), end=" ")
        print()
