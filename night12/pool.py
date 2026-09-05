"""night12 v1 -- the screened P pool.

Pools, in the order the brief asks for them:

  M1        the cusp-square mu_3 carrier at the exact 2:3 profiles
            (126,189) (128,192) (130,195) (132,198)
  M1L       the same shape with the lower part forced to carry (1,j) terms,
            which is the only way the lower part can change P_x on the line
            x = 0
  HDC       high-degree coordinates at and around the M1 profile degrees
            (triangular compositions) -- these are the P that pass S1 by
            construction and carry the pipeline end to end at degree ~126
  V0        the 174 P of the v0 sweep, rescreened

Every P is screened by S2 then S1 before any mate matrix is built.
"""

import random
import matekit as M
import carriers

SEED = 20260831


def pool_M1(n_per_profile):
    return carriers.build_M1(n_per_profile)


def pool_M1L(n_per_profile):
    """M1 shape with the lower part forced to contain (1,j) monomials."""
    rnd = random.Random(SEED + 1)
    out = []
    for (n, dq) in carriers.PROFILES:
        m = n // 2
        made = 0
        tries = 0
        while made < n_per_profile and tries < 600:
            tries += 1
            H = carriers.rand_H(rnd, m, rnd.randrange(2, 7))
            if H is None:
                continue
            A = rnd.choice([1, -1, 2, 3])
            P = {(1, 0): 1}
            for k, v in M.pmul(H, H).items():
                P[k] = P.get(k, 0) + A * v
            for _ in range(rnd.randrange(1, 4)):
                j = rnd.randrange(1, 2 * m - 1)
                P[(1, j)] = P.get((1, j), 0) + rnd.randrange(1, 4) * rnd.choice([1, -1])
            P = {k: v for k, v in P.items() if v != 0}
            if M.pdeg(P) != n or any(i % 3 != 1 for (i, j) in P):
                continue
            out.append({"family": "M1L", "profile": "(%d,%d)" % (n, dq),
                        "deg_P": n, "deg_Q_target": dq, "m": m,
                        "H_terms": len(H), "P": P, "H": H})
            made += 1
    return out


def pool_HDC():
    """high-degree coordinates: triangular compositions, degrees near the M1
    profiles.  Each carries a known mate, so they exercise the exact solver at
    degree ~126 as scaled positive controls."""
    out = []
    X = {(1, 0): 1}
    Y = {(0, 1): 1}
    seen = set()
    for k in range(2, 14):
        for e in (2, 3, 4, 5, 7, 11):
            u = M.padd(Y, {(k, 0): 1})
            P = M.padd(X, M.ppow(u, e))
            d = M.pdeg(P)
            if not (100 <= d <= 200):
                continue
            key = tuple(sorted(P.items()))
            if key in seen:
                continue
            seen.add(key)
            out.append({"family": "HDC", "profile": "(%d,%d)" % (d, M.pdeg(u)),
                        "deg_P": d, "deg_Q_target": M.pdeg(u), "m": d // 2,
                        "H_terms": 0, "P": P, "H": None, "known_mate": u})
    for d in (126, 128, 130, 132):
        P = M.padd(X, {(0, d): 1})
        out.append({"family": "HDC", "profile": "(%d,1)" % d, "deg_P": d,
                    "deg_Q_target": 1, "m": d // 2, "H_terms": 0,
                    "P": P, "H": None, "known_mate": Y})
    return out


def pool_V0():
    import ansatz, sweep
    out = []
    for r in ansatz.build_all():
        P = sweep.parse_P(r)
        out.append({"family": "V0_" + r["tag"], "profile": "(%d,-)" % r["deg"],
                    "deg_P": r["deg"], "deg_Q_target": None,
                    "m": r["deg"] // 2, "H_terms": 0, "P": P, "H": None})
    return out
