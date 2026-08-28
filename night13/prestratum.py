"""night13 -- the compressed cusp prestratum at degrees (deg P, deg Q) = (84, 126).

THE OBJECT
----------
H is the FOUR-TERM form of degree 42

    H = h2 x^2 y^40 + h14 x^14 y^28 + h29 x^29 y^13 + h41 x^41 y,

normalised in the chart h2 = 1.  The leading forms are prescribed:

    P_84  = A * H^2        (degree 84)
    Q_126 = B * H^3        (degree 126)

so the five top parameters after scaling are  h14, h29, h41, A, B.

    P = A*H^2 + sum_{m in C_P} a_m x^m,     |C_P| = 96
    Q = B*H^3 + sum_{m in C_Q} b_m x^m,     |C_Q| = 256

Total unknowns: 5 + 96 + 256 = 357.

MU_3 GRADING
------------
All four H-exponents 2, 14, 29, 41 are = 2 (mod 3), so every x-exponent of
H^2 is = 4 = 1 (mod 3) and every x-exponent of H^3 is = 6 = 0 (mod 3).  The
carriers are required to respect this: every P-monomial has i = 1 (mod 3),
every Q-monomial has i = 0 (mod 3).  Then in P_x Q_y every term has
x-exponent (1 - 1) + 0 = 0 (mod 3) and likewise in P_y Q_x (1 + 0 - 1 = 0),
so every bracket row sits at i = 0 (mod 3) -- which is where the constant
monomial (0,0) of the Keller equation lives.

The constant bracket row is reachable only through the single pair
P-monomial (1,0) x Q-monomial (0,1): the other pair that could hit (0,0),
namely P-(0,1) x Q-(1,0), is forbidden by the grading (0 != 1 and 1 != 0
mod 3).  Hence x is mandatory in C_P and y is mandatory in C_Q; both are
greedy seeds.

CARRIERS
--------
C_P: lattice points of conv(supp H^2 u {(0,0), (1,0)}) with i = 1 (mod 3) and
total degree < 84.  C_Q: lattice points of conv(supp H^3 u {(0,0), (0,1)})
with i = 0 (mod 3), total degree < 126, minus (0,0) whose bracket column is
identically zero (the factor p1 a2 - p2 a1 vanishes at a = (0,0)).

THE INCIDENCE HYPERGRAPH AND THE GREEDY
---------------------------------------
For a P-monomial p = (p1,p2) and a Q-monomial a = (a1,a2) the bracket picks
up exactly one term,

    coeff_p * coeff_a * (p1 a2 - p2 a1) * x^(p1+a1-1) y^(p2+a2-1),

so the row key is p + a - (1,1) and the pair CONTRIBUTES iff p1 a2 - p2 a1
is nonzero (collinear pairs, e.g. two monomials both coming from the same
h_k, drop out).  Call a contributing pair ADJUSTABLE if at least one of its
two monomials is a lower-carrier monomial.  The pure-top part of every row
sums to zero key by key, because [A H^2, B H^3] = 6 A B H^3 (H_x H_y - H_y
H_x) = 0 identically -- this is control (a) and is verified independently
both symbolically and numerically.  So each row's equation is carried
entirely by its adjustable pairs.

  * a mandatory row = any row key other than (0,0) (it must vanish);
  * a SINGLETON mandatory row = a mandatory row with exactly one adjustable
    pair -- its equation then forces a single product of coefficients to
    vanish;
  * an IDENTITY row = a mandatory row with no adjustable pair at all (pure
    top, cancels by [H^2, H^3] = 0).

Greedy: seed C_P with x = (1,0) and the vertices of the P-polygon that carry
i = 1 (mod 3); seed C_Q with y = (0,1) and the analogous Q-polygon vertices.
Then repeatedly add the pool monomial that removes the most singleton
mandatory rows, scored as (singletons removed) - (singletons created), with
ties broken by generic rank gain of the linearisation at char p = 999983.
Stop at 96 P-lower and 256 Q-lower.

ACCEPTANCE (as specified): the carrier is accepted only if the constant
bracket row is reachable and every mandatory nonconstant row is either an
identity row from [H^2, H^3] = 0 or carries at least two adjustable
contributing coefficients.  No bracket row is ever discarded to meet the
parameter target; all rows are kept in the probe.
"""

import json
import os
import random
import sys

import kit as K

HERE = os.path.dirname(os.path.abspath(__file__))

DEG_H = 42
H_EXPS = (2, 14, 29, 41)          # x-exponents of the four H terms
H_NAMES = ("h2", "h14", "h29", "h41")
DEG_P = 84
DEG_Q = 126
N_PLOW = 96
N_QLOW = 256
TIE_PRIME = K.P1
TIE_POOL_CAP = 8             # at most this many tied pool monomials get the
                                  # rank-gain tie-break (recorded deviation)


def H_form(vals):
    """H with x^2 y^40 coefficient pinned to 1 (the chart)."""
    h2, h14, h29, h41 = vals
    return {(e, DEG_H - e): c
            for e, c in zip(H_EXPS, (h2, h14, h29, h41)) if c != 0}


def supp_H2():
    return sorted({(a + b, 2 * DEG_H - a - b) for a in H_EXPS for b in H_EXPS})


def supp_H3():
    return sorted({(a + b + c, 3 * DEG_H - a - b - c)
                   for a in H_EXPS for b in H_EXPS for c in H_EXPS})


def polygons():
    SP = supp_H2()
    SQ = supp_H3()
    hp = K.hull(SP + [(0, 0), (1, 0)])
    hq = K.hull(SQ + [(0, 0), (0, 1)])
    return hp, hq, SP, SQ


def pools():
    hp, hq, SP, SQ = polygons()
    cp = [m for m in K.lattice_in(hp, DEG_P, 3, 1, deg_lt=DEG_P)]
    cq = [m for m in K.lattice_in(hq, DEG_Q, 3, 0, deg_lt=DEG_Q)
          if m != (0, 0)]
    return cp, cq, hp, hq, SP, SQ


def fac(p, a):
    return p[0] * a[1] - p[1] * a[0]


# ------------------------------------------------------------- greedy engine

class Incidence:
    """cnt[key] = number of ADJUSTABLE contributing pairs at that row key."""

    def __init__(self, Ptop, Qtop):
        self.Ptop = list(Ptop)
        self.Qtop = list(Qtop)
        self.Plow = []
        self.Qlow = []
        self.cnt = {}

    def Pall(self):
        return self.Ptop + self.Plow

    def Qall(self):
        return self.Qtop + self.Qlow

    def delta_P(self, m):
        d = {}
        for a in self.Qall():
            if fac(m, a):
                k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
                d[k] = d.get(k, 0) + 1
        return d

    def delta_Q(self, a):
        d = {}
        for m in self.Pall():
            if fac(m, a):
                k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
                d[k] = d.get(k, 0) + 1
        return d

    def score(self, d):
        removed = created = 0
        for k, n in d.items():
            if k == (0, 0):
                continue
            c = self.cnt.get(k, 0)
            if c == 1:
                removed += 1
            elif c == 0 and n == 1:
                created += 1
        return removed - created, removed, created

    def apply(self, d):
        for k, n in d.items():
            self.cnt[k] = self.cnt.get(k, 0) + n

    def add_P(self, m):
        d = self.delta_P(m)
        self.apply(d)
        self.Plow.append(m)

    def add_Q(self, a):
        d = self.delta_Q(a)
        self.apply(d)
        self.Qlow.append(a)

    def census(self):
        sing = [k for k, c in self.cnt.items() if c == 1 and k != (0, 0)]
        return {
            "n_rows_with_adjustable_pairs": len(self.cnt),
            "n_singleton_mandatory": len(sing),
            "constant_row_adjustable_pairs": self.cnt.get((0, 0), 0),
            "singletons": sorted(sing)[:40],
        }


# ------------------------------------------------ generic rank of the linearisation

def _rand_coeffs(rng, mons, p):
    return {m: rng.randrange(1, p) for m in mons}


def jacobian_rows(cP, cQ, Plow, Qlow, p):
    """d(bracket)/d(lower coefficients) at the coefficient point (cP, cQ).

    Columns 0..len(Plow)-1 are the P-lower unknowns, the rest the Q-lower
    unknowns.  char p.
    """
    rows = {}
    for j, m in enumerate(Plow):
        for a, ca in cQ.items():
            f = fac(m, a)
            if f % p == 0:
                continue
            k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
            r = rows.setdefault(k, {})
            r[j] = (r.get(j, 0) + ca * f) % p
    off = len(Plow)
    for j, a in enumerate(Qlow):
        for m, cm in cP.items():
            f = fac(m, a)
            if f % p == 0:
                continue
            k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
            r = rows.setdefault(k, {})
            r[off + j] = (r.get(off + j, 0) + cm * f) % p
    return {k: {c: v for c, v in r.items() if v} for k, r in rows.items()}


def generic_rank(inc, cP_top, cQ_top, rng, p, extra_P=None, extra_Q=None):
    Plow = list(inc.Plow) + ([extra_P] if extra_P else [])
    Qlow = list(inc.Qlow) + ([extra_Q] if extra_Q else [])
    if not Plow and not Qlow:
        return 0
    cP = dict(cP_top)
    cQ = dict(cQ_top)
    for m in Plow:
        cP[m] = rng.randrange(1, p)
    for a in Qlow:
        cQ[a] = rng.randrange(1, p)
    rows = jacobian_rows(cP, cQ, Plow, Qlow, p)
    return K.rank_modp(rows, len(Plow) + len(Qlow), p, seed=12345)["rank"]


# ------------------------------------------------------------------- builder

def build(verbose=True, n_plow=N_PLOW, n_qlow=N_QLOW, log=None):
    cp, cq, hp, hq, SP, SQ = pools()
    vertsP = [v for v in hp if v[0] % 3 == 1 and v[0] + v[1] < DEG_P]
    vertsQ = [v for v in hq if v[0] % 3 == 0 and v[0] + v[1] < DEG_Q
              and v != (0, 0)]
    inc = Incidence(SP, SQ)

    seedsP = [(1, 0)] + [v for v in vertsP if v != (1, 0)]
    seedsQ = [(0, 1)] + [v for v in vertsQ if v != (0, 1)]
    for m in seedsP:
        inc.add_P(m)
    for a in seedsQ:
        inc.add_Q(a)

    rng = random.Random(20260828)
    p = TIE_PRIME
    cP_top = {m: rng.randrange(1, p) for m in SP}
    cQ_top = {a: rng.randrange(1, p) for a in SQ}

    poolP = [m for m in cp if m not in set(inc.Plow)]
    poolQ = [a for a in cq if a not in set(inc.Qlow)]

    trace = []
    step = 0
    while len(inc.Plow) < n_plow or len(inc.Qlow) < n_qlow:
        step += 1
        best = []            # (score, removed, created, side, mon)
        bs = None
        if len(inc.Plow) < n_plow:
            for m in poolP:
                s, r, c = inc.score(inc.delta_P(m))
                if bs is None or s > bs:
                    bs, best = s, [(s, r, c, "P", m)]
                elif s == bs:
                    best.append((s, r, c, "P", m))
        if len(inc.Qlow) < n_qlow:
            for a in poolQ:
                s, r, c = inc.score(inc.delta_Q(a))
                if bs is None or s > bs:
                    bs, best = s, [(s, r, c, "Q", a)]
                elif s == bs:
                    best.append((s, r, c, "Q", a))
        if not best:
            break
        tie = len(best)
        if tie > 1:
            base = generic_rank(inc, cP_top, cQ_top, random.Random(step), p)
            scored = []
            for poolmon in best[:TIE_POOL_CAP]:
                _, _, _, side, mon = poolmon
                g = generic_rank(inc, cP_top, cQ_top, random.Random(step), p,
                                 extra_P=mon if side == "P" else None,
                                 extra_Q=mon if side == "Q" else None)
                scored.append((g - base, poolmon))
            scored.sort(key=lambda t: (-t[0], t[1][3], t[1][4]))
            gain, pick = scored[0]
        else:
            gain, pick = None, best[0]
        s, r, c, side, mon = pick
        if side == "P":
            inc.add_P(mon)
            poolP.remove(mon)
        else:
            inc.add_Q(mon)
            poolQ.remove(mon)
        cs = inc.census()
        trace.append({"step": step, "side": side, "mon": list(mon),
                      "score": s, "removed": r, "created": c,
                      "ties": tie, "rank_gain": gain,
                      "n_singleton_after": cs["n_singleton_mandatory"],
                      "n_plow": len(inc.Plow), "n_qlow": len(inc.Qlow)})
        if verbose and (step % 10 == 0 or step < 5):
            msg = ("step %4d %s %-10s score=%+4d ties=%5d gain=%s  "
                   "sing=%6d  P=%3d Q=%3d"
                   % (step, side, str(mon), s, tie, gain,
                      cs["n_singleton_mandatory"], len(inc.Plow),
                      len(inc.Qlow)))
            print(msg, flush=True)
            if log:
                log.write(msg + "\n")
                log.flush()
    return inc, trace, {"hullP": hp, "hullQ": hq, "SP": SP, "SQ": SQ,
                        "poolmonP": cp, "poolmonQ": cq,
                        "seedsP": seedsP, "seedsQ": seedsQ}


def main():
    logf = open(os.path.join(HERE, "carrier_log.txt"), "w")
    cp, cq, hp, hq, SP, SQ = pools()
    head = {
        "H_exponents": list(H_EXPS),
        "H_exponents_mod3": [e % 3 for e in H_EXPS],
        "H2_x_exponents": sorted({m[0] for m in SP}),
        "H2_x_exponents_mod3": sorted({m[0] % 3 for m in SP}),
        "H3_x_exponents": sorted({m[0] for m in SQ}),
        "H3_x_exponents_mod3": sorted({m[0] % 3 for m in SQ}),
        "n_supp_H2": len(SP), "n_supp_H3": len(SQ),
        "hull_P_vertices": [list(v) for v in hp],
        "hull_Q_vertices": [list(v) for v in hq],
        "n_pool_P": len(cp), "n_pool_Q": len(cq),
        "deg_P": DEG_P, "deg_Q": DEG_Q,
        "jvdk_84_divides_126": DEG_Q % DEG_P == 0,
        "jvdk_126_divides_84": DEG_P % DEG_Q == 0,
        "jvdk_divisibility_ordered": K.divisibility_ordered(DEG_P, DEG_Q),
    }
    print(json.dumps(head, indent=1), flush=True)
    logf.write(json.dumps(head, indent=1) + "\n")

    inc, trace, info = build(log=logf)
    cs = inc.census()
    out = dict(head)
    out.update({
        "n_plow": len(inc.Plow), "n_qlow": len(inc.Qlow),
        "n_unknowns_total": 5 + len(inc.Plow) + len(inc.Qlow),
        "C_P": [list(m) for m in inc.Plow],
        "C_Q": [list(m) for m in inc.Qlow],
        "seedsP": [list(m) for m in info["seedsP"]],
        "seedsQ": [list(m) for m in info["seedsQ"]],
        "census": cs,
        "accepted": (cs["constant_row_adjustable_pairs"] >= 1
                     and cs["n_singleton_mandatory"] == 0),
        "trace_tail": trace[-25:],
        "trace_head": trace[:25],
    })
    with open(os.path.join(HERE, "carrier.json"), "w") as f:
        json.dump(out, f, indent=1)
    with open(os.path.join(HERE, "carrier_trace.json"), "w") as f:
        json.dump(trace, f)
    print("census", json.dumps(cs)[:400], flush=True)
    print("accepted:", out["accepted"], flush=True)
    logf.write("census " + json.dumps(cs)[:2000] + "\naccepted: %s\n"
               % out["accepted"])
    logf.close()


if __name__ == "__main__":
    main()
