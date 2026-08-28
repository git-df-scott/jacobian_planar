"""night13 stage 2d -- carrier build and probe for the top-ranked survivors.

The survivors of the screen (stage 2b/2c) survive only in a characteristic
dividing BOTH extreme-ray factors 2*e0 and 3*(m-e1).  The probe of
PRESTRATUM.md section 7 runs at 999983 and 1000003, and at both of those
primes these supports fail the screen exactly as the original H did, so
running it there would only re-measure the two-row obstruction.  The probe is
therefore run in the characteristics in which the support survives.  For the
two top-ranked supports at m = 42 those are 2 and 5 (2*e0 = 10 and
3*(m-e1) = 30 share the factors 2 and 5), and each support is probed in both
-- the analogue of the dual-prime discipline of section 7.

Recorded deviation from "220 samples, both primes": the two primes of the
lane are not where these objects live.  Over F_2 there is a further loss --
every nonzero coefficient equals 1, so the top parameters h_e (e != e0), A, B
are not free and the top chart is a single point, with all sampling freedom
in the lower blocks.  Over F_5 each top parameter has 4 admissible values.  A
probe with a large top-parameter space in characteristic 2 would need
F_(2^k); that was not built.

Everything else follows PRESTRATUM.md: same greedy (net singleton score,
rank-gain tie-break), same 96 + 256 stop, same controls, same halt protocol.
"""

import json
import os
import random
import sys
import time

import kit as K
import prestratum as PS
import probe as PR
import screen

HERE = os.path.dirname(os.path.abspath(__file__))
N_SAMPLES = int(os.environ.get("N13_SAMPLES", "220"))


class Inc(PS.Incidence):
    """char-aware incidence: a pair contributes only when its factor is
    nonzero in the characteristic."""

    def __init__(self, Ptop, Qtop, char):
        super().__init__(Ptop, Qtop)
        self.char = char

    def _nz(self, v):
        return (v % self.char != 0) if self.char else (v != 0)

    def delta_P(self, m):
        d = {}
        for a in self.Qall():
            if self._nz(PS.fac(m, a)):
                k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
                d[k] = d.get(k, 0) + 1
        return d

    def delta_Q(self, a):
        d = {}
        for m in self.Pall():
            if self._nz(PS.fac(m, a)):
                k = (m[0] + a[0] - 1, m[1] + a[1] - 1)
                d[k] = d.get(k, 0) + 1
        return d


def build_carrier(E, m, char, n_plow=96, n_qlow=256, verbose=True):
    SP, SQ = screen.leading_supports(list(E), m, char)
    hp = K.hull(SP + [(0, 0), (1, 0)])
    hq = K.hull(SQ + [(0, 0), (0, 1)])
    poolP = screen.pool(hp, 1, 2 * m, 2 * m)
    poolQ = screen.pool(hq, 0, 3 * m, 3 * m, drop_origin=True)
    inc = Inc(SP, SQ, char)
    inc.add_P((1, 0))
    inc.add_Q((0, 1))
    poolP = [p for p in poolP if p != (1, 0)]
    poolQ = [q for q in poolQ if q != (0, 1)]
    rng = random.Random(20260828)
    rp = K.P1                       # tie-break rank prime, as in stage 1
    cP_top = {p: rng.randrange(1, rp) for p in SP}
    cQ_top = {q: rng.randrange(1, rp) for q in SQ}
    step = 0
    while len(inc.Plow) < n_plow or len(inc.Qlow) < n_qlow:
        step += 1
        best, bs = [], None
        if len(inc.Plow) < n_plow:
            for p in poolP:
                s, r, c = inc.score(inc.delta_P(p))
                if bs is None or s > bs:
                    bs, best = s, [(s, "P", p)]
                elif s == bs:
                    best.append((s, "P", p))
        if len(inc.Qlow) < n_qlow:
            for q in poolQ:
                s, r, c = inc.score(inc.delta_Q(q))
                if bs is None or s > bs:
                    bs, best = s, [(s, "Q", q)]
                elif s == bs:
                    best.append((s, "Q", q))
        if not best:
            break
        if len(best) > 1:
            base = PS.generic_rank(inc, cP_top, cQ_top, random.Random(step), rp)
            sc = []
            for (s, side, mon) in best[:PS.TIE_POOL_CAP]:
                g = PS.generic_rank(inc, cP_top, cQ_top, random.Random(step),
                                    rp, extra_P=mon if side == "P" else None,
                                    extra_Q=mon if side == "Q" else None)
                sc.append((g - base, (s, side, mon)))
            sc.sort(key=lambda t: (-t[0], t[1][1], t[1][2]))
            pick = sc[0][1]
        else:
            pick = best[0]
        s, side, mon = pick
        if side == "P":
            inc.add_P(mon)
            poolP.remove(mon)
        else:
            inc.add_Q(mon)
            poolQ.remove(mon)
        if verbose and step % 50 == 0:
            print("    step %d sing=%d P=%d Q=%d"
                  % (step, inc.census()["n_singleton_mandatory"],
                     len(inc.Plow), len(inc.Qlow)), flush=True)
    return {"E": list(E), "m": m, "char": char, "SP": SP, "SQ": SQ,
            "hullP": hp, "hullQ": hq, "n_pool_P": len(poolP) + 1,
            "n_pool_Q": len(poolQ) + 1, "C_P": inc.Plow, "C_Q": inc.Qlow,
            "census": inc.census(), "steps": step}


def sample_P_char(rng, E, m, C_P, char, ones):
    """Top block: h_(e0) = 1 (chart) and every other h_e, together with A,
    drawn uniformly from the nonzero residues; over F_2 that leaves exactly
    one admissible top point, over F_5 there are 4 choices per parameter.
    Lower block: a random pattern with a_(1,0) forced nonzero."""
    e0 = min(E)
    H = {(e, m - e): (1 if e == e0 else rng.randrange(1, char)) for e in E}
    H = {k: v for k, v in H.items() if v}
    A = rng.randrange(1, char)
    P = K.pscale(K.ppow(H, 2, char), A, char)
    low = {}
    for mm in C_P:
        if mm == (1, 0):
            v = rng.randrange(1, char)
        else:
            v = rng.randrange(1, char) if rng.random() < ones else 0
        if v:
            low[mm] = v
            P[mm] = (P.get(mm, 0) + v) % char
    P = {k: v for k, v in P.items() if v}
    return P, {"H": H, "A": A, "low": low, "e0": e0}


def run(E, m, char, tag, n_plow=96, n_qlow=256, n_samples=None):
    t0 = time.time()
    n_samples = N_SAMPLES if n_samples is None else n_samples
    print("  building carrier for E=%s char=%d" % (list(E), char), flush=True)
    car = build_carrier(E, m, char, n_plow, n_qlow)
    C_P, C_Q = car["C_P"], car["C_Q"]
    e0, e1 = min(E), max(E)
    row_P = (2 * e0 - 1, 2 * (m - e0))          # the two extreme-ray rows
    row_Q = (3 * e1, 3 * (m - e1) - 1)

    # controls
    ctl = [PR.control_C0(char), PR.control_Ca(), PR.control_Cb()]
    # Cb in this characteristic: the two extreme rows must vanish mod char
    Hz = {(e, m - e): 1 for e in E}
    Pz = K.padd(K.ppow(Hz, 2), {(1, 0): 1})
    Qz = K.padd(K.ppow(Hz, 3), {(0, 1): 1})
    brz = K.bracket(Pz, Qz)
    ctl.append({"name": "Cb2_extreme_rows_vanish_mod_char", "ring": "Z->F_%d" % char,
                "row_P": list(row_P), "value_over_Z": brz.get(row_P, 0),
                "value_mod_char": brz.get(row_P, 0) % char,
                "row_Q": list(row_Q), "value_over_Z_Q": brz.get(row_Q, 0),
                "value_mod_char_Q": brz.get(row_Q, 0) % char,
                "pass": brz.get(row_P, 0) % char == 0
                        and brz.get(row_Q, 0) % char == 0})
    rng0 = random.Random(5)
    P0, meta0 = sample_P_char(rng0, E, m, C_P, char, 1.0)
    H3 = K.ppow(meta0["H"], 3, char)
    rows0 = PR.build_Q_system(P0, H3, C_Q, char)
    rk0 = K.rank_modp(rows0, 1 + len(C_Q), char, seed=3, augment=True)
    ctl.append({"name": "Cc_rank_sanity", "char": char,
                "n_rows_nonzero": len(rows0),
                "n_rows_identically_vanishing":
                    len(PR.build_Q_system.last_vanishing),
                "rank_A": rk0["rank_A"],
                "constant_row_present": bool(rows0.get((0, 0))),
                "extreme_row_P_absent_from_matrix": row_P not in rows0,
                "extreme_row_Q_absent_from_matrix": row_Q not in rows0,
                "pass": rk0["rank_A"] > 0 and bool(rows0.get((0, 0)))})
    gate = all(c["pass"] for c in ctl)

    tally = {"consistent": 0, "inconsistent": 0}
    hits = []
    samples = []
    for s in range(n_samples):
        rng = random.Random(7000 + s)
        ones = (1.0 if s == 0 else rng.choice([0.25, 0.5, 0.75]))
        P, meta = sample_P_char(rng, E, m, C_P, char, ones)
        H3 = K.ppow(meta["H"], 3, char)
        rows = PR.build_Q_system(P, H3, C_Q, char)
        rk = K.rank_modp(rows, 1 + len(C_Q), char, seed=11 + s, augment=True)
        rec = {"sample": s, "ones": ones, "n_rows_nonzero": len(rows),
               "rank_A": rk["rank_A"], "rank_Ae": rk["rank_Ae"],
               "consistent": rk["consistent"]}
        if rk["consistent"]:
            tally["consistent"] += 1
            sol, st = K.solve_modp(rows, 1 + len(C_Q), char)
            rec["solve_status"] = st
            if st == "ok":
                Q = K.pscale(K.ppow(meta["H"], 3, char), sol.get(0, 0), char)
                for c, v in sol.items():
                    if c:
                        mm = C_Q[c - 1]
                        Q[mm] = (Q.get(mm, 0) + v) % char
                Q = {k: v for k, v in Q.items() if v}
                rec["bracket_is_one"] = K.bracket(P, Q, char) == {(0, 0): 1}
                rec["deg_P"] = K.pdeg(P)
                rec["deg_Q"] = K.pdeg(Q)
                if rec["bracket_is_one"]:
                    hits.append({"rec": rec, "P": {str(k): v for k, v in P.items()},
                                 "Q": {str(k): v for k, v in Q.items()}})
        else:
            tally["inconsistent"] += 1
        samples.append(rec)
        if s % 40 == 0:
            print("    sample %d %s %.1fs" % (s, rk["consistent"],
                                              time.time() - t0), flush=True)
    out = {"tag": tag, "E": list(E), "m": m, "char": char,
           "deg_P": 2 * m, "deg_Q": 3 * m,
           "divisibility_ordered": K.divisibility_ordered(2 * m, 3 * m),
           "carrier": {k: v for k, v in car.items()
                       if k not in ("C_P", "C_Q", "SP", "SQ")},
           "C_P": [list(v) for v in C_P], "C_Q": [list(v) for v in C_Q],
           "controls": ctl, "gate": gate, "n_samples": n_samples,
           "tally": tally, "n_hits": len(hits),
           "samples_head": samples[:5], "elapsed_s": round(time.time() - t0, 1)}
    json.dump(out, open(os.path.join(HERE, "survivor_%s.json" % tag), "w"),
              indent=1)
    if hits:
        d = os.path.join(HERE, "HIT_char%d_%s" % (char, tag))
        os.makedirs(d, exist_ok=True)
        json.dump(hits, open(os.path.join(d, "hits.json"), "w"), indent=1)
        print("  HALT-AND-COMMIT:", d, flush=True)
    print("  %s: gate=%s tally=%s hits=%d (%.1fs)"
          % (tag, gate, tally, len(hits), time.time() - t0), flush=True)
    return out


if __name__ == "__main__":
    ranked = json.load(open(os.path.join(HERE, "rank_char2.json")))["42"]["ranked"]
    top = ranked[:2]
    res = []
    # each of the two top-ranked supports is probed in BOTH characteristics
    # in which it survives the screen (2 and 5 here), which is the analogue of
    # the dual-prime discipline of PRESTRATUM.md section 7.
    for i, r in enumerate(top):
        for ch in (2, 5):
            res.append(run(tuple(r["E"]), 42, ch, "top%d_char%d" % (i + 1, ch)))
    json.dump({"top": [r["E"] for r in top],
               "results": [{k: v for k, v in r.items()
                            if k not in ("C_P", "C_Q")} for r in res]},
              open(os.path.join(HERE, "survivor_probe.json"), "w"), indent=1)
