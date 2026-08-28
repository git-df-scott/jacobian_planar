"""night6 -- characteristic zero, CHART A  (alpha = 1, beta = be free).

In chart A the kernel element is (p_,s_) = v1 + be*v2, so the 38 affine-linear
equations E1, E2 in the 32 unknowns (f,g,r) have coefficients polynomial in
`be`: degree <= 1 in the coefficient block M(be), degree <= 2 in the
right-hand column b(be).

The chart is non-empty at a value of `be` only if that linear system is
CONSISTENT there, i.e. only if rank[M(be) | b(be)] = rank M(be) <= 32, i.e.
only if EVERY 33 x 33 minor of the 38 x 33 augmented matrix N(be) vanishes.
Each such minor is a polynomial in `be` of degree <= 34, computed here exactly
by evaluating the determinant over K = Q[T]/(h) at 40 rational values of `be`
and interpolating (40 > 34 nodes, so the degree bound is itself checked by the
interpolation).

If a family of these minors has gcd 1 in K[be], they have no common root, so
the linear system is inconsistent for every value of `be` in the algebraic
closure, and chart A is empty over characteristic zero -- in both variants,
since the Rabinowitsch vertex conditions only add constraints.
"""
import os, sys, json, time
from fractions import Fraction as F

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import char0_lib as C
import char0_linear as L
from char0_linear_run import load_face, flush

NODES = list(range(0, 40))
SUBSETS = {
    "rows 0..32": list(range(0, 33)),
    "rows 5..37": list(range(5, 38)),
    "rows 0..15,21..37": list(range(0, 16)) + list(range(21, 38)),
}


def main():
    t0 = time.time()
    D = load_face()
    K, q, t = D['K'], D['q'], D['t']
    pv1, sv1 = C.split(D['basis'][0], D['cols'])
    pv2, sv2 = C.split(D['basis'][1], D['cols'])
    flush("=" * 78)
    flush("CHARACTERISTIC ZERO -- CHART A  (alpha = 1, beta = be free)")
    flush("=" * 78)
    flush("   K = Q[T]/(h), deg h = %d, irreducible over Q; covers 35 of 35"
          " face solutions" % D['h'].degree())
    flush("   E3 kernel dimension over char 0: %d (free columns %s)"
          % (D['kerdim'], D['free']))

    # quick look at two specialisations
    for x in (0, 1):
        pv, sv = L.chartA_pv_sv(pv1, sv1, pv2, sv2, x, K)
        M, b, lab = L.build_rows(q, t, pv, sv, K)
        rank, coef, rhs, tr, piv = L.rref_tracked(M, b, K)
        inc = L.inconsistent_rows(coef, rhs, K)
        flush("   specialisation be = %d : rank %d, inconsistent rows %d"
              % (x, rank, len(inc)))

    flush("")
    flush("   minors of the 38 x 33 augmented matrix N(be), as polynomials"
          " in be (interpolation through %d rational nodes):" % len(NODES))
    polys = {}
    for name, rows in SUBSETS.items():
        te = time.time()
        xs, ys = [], []
        for x in NODES:
            pv, sv = L.chartA_pv_sv(pv1, sv1, pv2, sv2, x, K)
            M, b, lab = L.build_rows(q, t, pv, sv, K)
            sub = [[M[i][j] for j in range(len(M[0]))] + [b[i]]
                   for i in rows]
            xs.append(F(x))
            ys.append(L.det_K(sub, K))
        p = L.interpolate(xs, ys, K)
        polys[name] = p
        deg = len(p) - 1
        flush("      %-20s : degree in be = %d  (bound 34), identically"
              " zero: %s   (%.0fs)"
              % (name, deg, not p, time.time() - te))
    live = [(n, p) for n, p in polys.items() if p]
    assert live, "every minor tried vanishes identically -- choose other rows"
    g = live[0][1]
    for n, p in live[1:]:
        g = L.poly_gcd_K(g, p, K)
    flush("")
    flush("   gcd of the %d non-vanishing minors in K[be]: degree %d"
          % (len(live), len(g) - 1))
    empty = (len(g) - 1 == 0)
    if empty:
        flush("   => the minors have NO common root: for EVERY value of be in"
              " the algebraic closure the linear system E1+E2 is"
              " inconsistent.")
        flush("   => CHART A IS EMPTY over characteristic zero, free variant"
              " and Rabinowitsch variant alike.")
    else:
        flush("   => common roots exist; the surviving values of be are the"
              " roots of a polynomial of degree %d -- these must still be"
              " examined." % (len(g) - 1))
        flush("      gcd coefficients (low -> high): %s"
              % [K.show(c)[:40] for c in g])
    json.dump(dict(nodes=len(NODES),
                   minors={n: (len(p) - 1) for n, p in polys.items()},
                   gcd_degree=len(g) - 1, chartA_empty=empty,
                   seconds=time.time() - t0),
              open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                'char0_chartA_results.json'), 'w'), indent=1)
    flush("")
    flush("wall %.0fs" % (time.time() - t0))


if __name__ == '__main__':
    main()
