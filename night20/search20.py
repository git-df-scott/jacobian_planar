"""night20 -- the sweep.  Measurements only."""
import sys, os, json, time, itertools
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import gen20 as G

x, y, c = I.x, I.y, I.c


def poly_from(S, coeffs):
    return sp.expand(sum(a * x**i * y**j for a, (i, j) in zip(coeffs, S)))


def axis_free(P):
    """P has no critical point on x = 0 and none on y = 0.  Combined with
    MV(N(P_x), N(P_y)) = 0 (which kills the torus) this is exactly
    unimodularity -- but it is only used as a FAST FILTER; every survivor is
    re-decided by Singular's Groebner basis plus an explicit Bezout pair."""
    Px, Py = sp.expand(sp.diff(P, x)), sp.expand(sp.diff(P, y))
    for sub, v in ((x, y), (y, x)):
        a = sp.Poly(Px.subs(sub, 0), v) if Px.subs(sub, 0) != 0 else None
        b = sp.Poly(Py.subs(sub, 0), v) if Py.subs(sub, 0) != 0 else None
        if a is None and b is None:
            return False
        if a is None:
            g = b
        elif b is None:
            g = a
        else:
            g = sp.gcd(a, b)
        if sp.Poly(g, v).degree() >= 1:
            return False
    return True


def canon(P):
    """canonical key up to the torus action x->lx, y->my, P->nP and the swap
    x<->y: the sorted support, and the support of the swap, take the min."""
    S = tuple(sorted(sp.Poly(P, x, y).monoms()))
    T = tuple(sorted((j, i) for (i, j) in S))
    return min(S, T)


def main(Dmax=12, sizes=(2, 3, 4), out="search20_raw.json", tlim=None):
    t0 = time.time()
    seen = set()
    found = []
    ntried = 0
    for size in sizes:
        sup = G.supports(Dmax, size)
        print("size %d: %d supports with MV=0, interior>=1, degree<=%d"
              % (size, len(sup), Dmax), flush=True)
        for S in sup:
            # torus normalisation: 3 free scalings, so for |S|<=3 all-ones is
            # a full normal form when the exponent matrix is invertible; for
            # |S|=4 sweep the last coefficient.
            if size <= 3:
                cofs = [tuple([1]*size), tuple([1]*(size-1) + [-1])]
            else:
                cofs = [(1, 1, 1, t) for t in (1, -1, 2, -2, sp.Rational(1, 2), 3)]
            for cf in cofs:
                ntried += 1
                P = poly_from(S, cf)
                if not axis_free(P):
                    continue
                k = (canon(P), tuple(str(t) for t in cf))
                if k in seen:
                    continue
                seen.add(k)
                found.append({"support": [list(m) for m in S],
                              "coeffs": [str(t) for t in cf],
                              "P": sp.sstr(P),
                              "deg": sp.Poly(P, x, y).total_degree(),
                              "baker": G.interior(S)})
            if tlim and time.time() - t0 > tlim:
                print("  time limit", flush=True)
                break
    print("fast-filter survivors: %d  (of %d coefficient vectors tried) in %.1fs"
          % (len(found), ntried, time.time() - t0), flush=True)
    json.dump(found, open(os.path.join(HERE, out), "w"), indent=1)
    return found


if __name__ == "__main__":
    main(Dmax=int(sys.argv[1]) if len(sys.argv) > 1 else 12)
