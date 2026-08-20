"""
ITEM 1 -- case (2) over Q-bar, run as a fully gauge-fixed system at fresh primes.

THE GAUGE, derived here rather than inherited
---------------------------------------------
Write P' = a P(mu x, nu y), Q' = b Q(mu x, nu y).  Then
[P',Q'] = a b mu nu [P,Q](mu x, nu y) = a b mu^3 nu x^2, so the case-(2) system
is invariant under the THREE-parameter group

        (mu, nu, a) free,      b = 1 / (a mu^3 nu).

On the pieces P = A + B/y + C/y^2, Q = D + E/y + F/y^2 + G/y^3 with t = x y^2:

        A -> a A,      B -> (a/nu) B,      C -> (a/nu^2) C
        D -> b D,      E -> (b/nu) E,      F -> (b/nu^2) F,   G -> (b/nu^3) G
        t -> mu nu^2 t

so THREE charts are needed to rigidify, and the campaign's single chart
d_3_3 = 1 leaves a positive-dimensional gauge orbit.  This module fixes:

        d_2_1 = 1     (g_2; d_2_1 is one of the JSON's nonzero conditions,
                       so this is a gauge fixing, never a case split)
        c_8_16 = 1    (the leading A coefficient; also a nonzero condition)
        d_3_3 = 1  OR  d_3_3 = 0    <- the genuine CHART SPLIT, both run

Everything else -- all 92 equations, all 72 variables -- is kept.  The
remaining nonzero conditions are imposed by one Rabinowitsch variable.

CONTROLS, run at every prime and in every chart
-----------------------------------------------
  MUTANT  the 92 equations get their value at a random admissible point
          subtracted off, so that point IS a solution.  msolve must NOT say
          EMPTY.  A run whose mutant says EMPTY is void and is reported as such.
  PIN     an explicitly contradictory pair is added.  msolve MUST say EMPTY.

Verdicts are read from the parsed .out artifact.  A zero-byte .out is a
failure, not a result.
"""

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w4_c2_build as B
import w4_run as RUN

# Gauge exponent vectors in (a, mu, nu):  c_i_j -> a mu^i nu^j c_i_j,
# d_i_j -> b mu^i nu^j d_i_j with b = 1/(a mu^3 nu).  Hence
#     d_2_1   -> ( -1, -1,  0)
#     c_8_16  -> (  1,  8, 16)
#     d_3_3   -> ( -1,  0,  2)
#     d_12_24 -> ( -1,  9, 23)
# det[d_2_1; c_8_16; d_3_3]   =  2  != 0  -> in the chart d_3_3 = 1 the pair
#     (d_2_1, c_8_16) together with the chart rigidifies the gauge completely.
# det[d_2_1; c_8_16; d_12_24] = -1 != 0  -> in the chart d_3_3 = 0 a THIRD
#     gauge fixing is needed, and d_12_24 (also a nonzero condition) supplies it.
# Both extra variables are in the JSON's "nonzero" list, so setting them to 1 is
# a gauge fixing and never a case split.  d_3_3 is NOT in that list, which is
# why d_3_3 = 1 / d_3_3 = 0 is a genuine, exhaustive chart split.
GAUGE_COMMON = [("d_2_1", 1), ("c_8_16", 1)]
GAUGE_ZERO_CHART = [("d_12_24", 1)]


def gauge_for(chart):
    return GAUGE_COMMON + (GAUGE_ZERO_CHART if chart == "zero" else [])


def build(p, chart, variant, seed=0):
    GAUGE = gauge_for(chart)
    varlist, polys, pt = B.build_system(p, chart, variant=variant, seed=seed)
    for v, val in GAUGE:
        if v not in varlist:
            raise SystemExit(f"gauge variable {v} absent from the system")
        polys.append(f"{v} + {(-val) % p}")
        if pt is not None:
            pt[v] = val
    if variant == "mutant":
        # rebuild the mutation at the gauge-fixed point so the point really is
        # a solution of the mutated system AND of the gauge equations
        varlist, polys, pt = B.build_system(p, chart, variant="real", seed=seed)
        pt0 = B.random_point(p, seed, chart)
        for v, val in GAUGE:
            pt0[v] = val
        polys = []
        for k in range(len(B.EQS)):
            terms = B.S.eq_terms(B.EQS[k])
            s = B.poly_str(terms, p)
            val = B.eval_terms(terms, pt0, p)
            polys.append(s if val == 0 else f"{s} + {(-val) % p}")
        polys.append("d_3_3 + " + str((-1) % p) if chart == "one" else "d_3_3")
        nz = [v for v in B.NONZERO]
        polys.append("sat*" + "*".join(nz) + " + " + str((-1) % p))
        for v, val in GAUGE:
            polys.append(f"{v} + {(-val) % p}")
        pt = pt0
    return varlist, polys, pt


def run_all(primes, out_dir, timeout=2700, threads=2):
    os.makedirs(out_dir, exist_ok=True)
    res = {}
    for p in primes:
        if p % 3 != 1:
            raise SystemExit(f"prime {p} violates p = 1 (mod 3)")
        for chart in ("one", "zero"):
            for variant in ("mutant", "pin", "real"):
                key = f"full_{chart}_{variant}_p{p}"
                vl, pl, pt = build(p, chart, variant, seed=abs(hash(key)) % 10 ** 6)
                ms = os.path.join(out_dir, f"c2_{key}.ms")
                B.write_ms(ms, p, vl, pl)
                r = RUN.run_msolve(ms, ms[:-3] + ".out", timeout=timeout,
                                   threads=threads)
                r.update(prime=p, chart=chart, variant=variant,
                         nvars=len(vl), npolys=len(pl))
                if pt is not None:
                    r["planted_point"] = {k: int(v) for k, v in sorted(pt.items())}
                res[key] = r
                print(f"  {key}: {r['verdict']}  {r['seconds']}s "
                      f"rss={r['peak_rss_kb_children']}kB", flush=True)
                RUN.save(res, os.path.join(out_dir, "c2_full_results.json"))
    return res


if __name__ == "__main__":
    PRIMES = [1000003, 1000033, 1000039]
    HERE = os.path.dirname(os.path.abspath(__file__))
    run_all(PRIMES, os.path.join(HERE, "artifacts"))
    print("DONE")
