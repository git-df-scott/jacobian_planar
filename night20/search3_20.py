"""night20 -- third sweep, the DESIGNED one.

Supports are restricted to those for which the Newton polygon already FORCES
every fibre to be irreducible (gen20.newton_forces_all_fibres_irreducible: both
conv(S u {0}) and conv(S \\ {0}) 2-dimensional, Minkowski-indecomposable, and
touching both axes), and which have an interior lattice point (Baker: the only
way the generic fibre can have genus >= 1).  On those supports the coefficients
are swept and filtered for "no critical point": the axis test, then the
Bernstein degeneracy test on the torus, then Singular's Groebner verdict.

This is the exact intersection of the three target conditions, attacked from
the geometric side.
"""
import sys, os, json, itertools, time
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen20 as G
from search2_20 import axis_free


def singular_filter(cands, res, out, t0):
    import sympy as sp
    import inst20 as I
    x, y = sp.symbols('x y')
    B = 250
    for b in range(0, len(cands), B):
        chunk = cands[b:b + B]
        lines = ["ring r=0,(x,y),dp;"]
        for n, (S, cf) in enumerate(chunk):
            Ps = "+".join("(%s)*x^%d*y^%d" % (a, i, j) for a, (i, j) in zip(cf, S))
            lines.append("poly P%d=%s;" % (n, Ps))
            lines.append("ideal I%d=diff(P%d,x),diff(P%d,y);" % (n, n, n))
            lines.append('"R%d:",reduce(poly(1),std(I%d));' % (n, n))
        try:
            outp = I.singular("\n".join(lines), timeout=1800)
        except Exception as e:
            print("  batch failed %s" % e, flush=True)
            continue
        for n, (S, cf) in enumerate(chunk):
            v = I.parse_marked(outp, "R%d" % n)
            if v is not None and v.strip() == "0":
                P = sp.expand(sum(sp.Rational(a) * x**i * y**j
                                  for a, (i, j) in zip(cf, S)))
                res.append({"support": [list(m) for m in S],
                            "coeffs": [str(t) for t in cf],
                            "P": sp.sstr(P),
                            "deg": max(i + j for (i, j) in S),
                            "baker": G.interior(S)})
                print("   UNIMODULAR ON A DESIGNED SUPPORT: %s" % sp.sstr(P),
                      flush=True)
        json.dump(res, open(os.path.join(HERE, out), "w"), indent=1)
    print("  singular stage done: %d designed-support unimodular so far (%.0fs)"
          % (len(res), time.time() - t0), flush=True)


def main(jobs, coefs, out="search3_raw.json", tlim=100000):
    import sympy as sp
    import inst20 as I
    x, y = sp.symbols('x y')
    t0 = time.time()
    cands = []
    RES = []
    seen = set()
    nsup_tot = 0
    for (D, size) in jobs:
        mons = [(i, j) for d in range(D + 1) for i in range(d + 1) for j in [d - i]]
        nsup = ntry = 0
        for S in itertools.combinations(mons, size):
            if max(i + j for (i, j) in S) != D:
                continue
            if G.interior(S) < 1:
                continue
            if not G.newton_forces_all_fibres_irreducible(S):
                continue
            nsup += 1
            for cf in itertools.product(coefs, repeat=size):
                if cf[-1] < 0:
                    continue
                ntry += 1
                if not axis_free(S, cf):
                    continue
                if not G.torus_may_be_empty(S, cf):
                    continue
                key = tuple(sorted((m, str(a)) for a, m in zip(cf, S)))
                if key in seen:
                    continue
                seen.add(key)
                cands.append((S, cf))
        nsup_tot += nsup
        singular_filter(cands, RES, out, t0)
        cands = []
        print("D=%2d size=%d : %6d designed supports, %9d coefficient vectors,"
              " %5d survivors, %.0fs" % (D, size, nsup, ntry, len(cands),
                                         time.time() - t0), flush=True)
        if time.time() - t0 > tlim:
            break
    print("designed supports total %d ; DESIGNED-SUPPORT UNIMODULAR FOUND: %d"
          % (nsup_tot, len(RES)), flush=True)
    json.dump(RES, open(os.path.join(HERE, out), "w"), indent=1)


if __name__ == "__main__":
    jobs = [(D, s) for D in range(4, 13) for s in (3, 4)]
    main(jobs, [F(1), F(-1), F(2), F(-2), F(3), F(-3), F(1, 2), F(-1, 2),
                F(4), F(-4), F(6), F(-6)])
