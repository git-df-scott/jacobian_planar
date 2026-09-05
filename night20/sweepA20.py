"""night20 -- the INVERTED sweep: fix A, solve for P.

Direction used (stated explicitly): the equation  D_P(A) = P, i.e.
    A_y P_x - A_x P_y - P = 0 ,
is LINEAR IN THE COEFFICIENTS OF P once A is fixed.  So A is swept and the
whole solution SPACE of P is computed exactly over Q (pole20.kernel_P), rather
than sweeping P and testing A-solvability.  Every P in that space carries the
rational mate Q = A/P (pole20 verifies the identity), so this sweep enumerates
polynomials with a rational mate directly.

Design note recorded before the sweep, and then measured:  for A = mu*x*y the
equation reduces to Euler's identity for the torus action of weights (1,-1):
w1 x P_x + w2 y P_y = d P with (w1,w2) = (1,-1) forces every monomial of P to
have the same value of i - j, i.e. P = x^k f(xy) or y^k f(xy) -- which always
has a monomial factor and hence a reducible fibre unless f is a constant (and
then P is a coordinate).  Matching A_y = (w1/d) x and -A_x = (w2/d) y is
consistent only when w1 = -w2, so A proportional to x*y is the ONLY monomial
that can work.  The sweep below is therefore aimed at A far from x*y.
"""
import sys, os, json, itertools, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sympy as sp
import inst20 as I
import pole20 as PL
import gen20 as G
x, y, c = I.x, I.y, I.c


def analyse(P):
    P = sp.expand(P)
    if sp.Poly(P, x, y).total_degree() < 1:
        return None
    fac = sp.factor_list(P)
    nfac = sum(e for (f, e) in fac[1] if sp.Poly(f, x, y).total_degree() >= 1)
    return {"P": sp.sstr(P), "deg": int(sp.Poly(P, x, y).total_degree()),
            "P_factors": sp.sstr(sp.factor(P)),
            "P_reducible": bool(nfac > 1)}


def main(Dmax=7, sizes=(1, 2, 3), coefs=(1, -1, 2, -2, 3, -3), DP=12,
         out="sweepA20.json", tlim=100000):
    t0 = time.time()
    mons = [(i, j) for d in range(Dmax + 1) for i in range(d + 1) for j in [d - i]
            if (i, j) != (0, 0)]
    seenP = {}
    nA = nsol = 0
    rows = []
    for size in sizes:
        for S in itertools.combinations(mons, size):
            for cf in itertools.product(coefs, repeat=size):
                if cf[0] < 0:
                    continue
                nA += 1
                A = sp.expand(sum(a * x**i * y**j for a, (i, j) in zip(cf, S)))
                B = PL.kernel_P(A, DP)
                if not B:
                    continue
                nsol += 1
                # the whole space is a solution space; test the basis and a
                # generic member
                cands = list(B)
                if len(B) > 1:
                    cands.append(sp.expand(sum((k + 2) * b for k, b in enumerate(B))))
                    cands.append(sp.expand(sum((-1)**k * (k + 1) * b
                                               for k, b in enumerate(B))))
                for P in cands:
                    a = analyse(P)
                    if a is None:
                        continue
                    if a["P"] in seenP:
                        continue
                    seenP[a["P"]] = 1
                    a["A"] = sp.sstr(A)
                    a["kernel_dim"] = len(B)
                    a["residual_D_P(A)-P"] = sp.sstr(sp.expand(PL.D(P, A) - P))
                    rows.append(a)
            if time.time() - t0 > tlim:
                break
        print("size %d done: %d A swept, %d with a non-trivial P-space, "
              "%d distinct P, %.0fs" % (size, nA, nsol, len(rows),
                                        time.time() - t0), flush=True)
        json.dump(rows, open(os.path.join(HERE, out), "w"), indent=1)
    json.dump(rows, open(os.path.join(HERE, out), "w"), indent=1)
    red = sum(1 for r in rows if r["P_reducible"])
    print("TALLY: %d distinct P with a rational mate A/P ; %d have P itself "
          "reducible (so the fibre P = 0 is reducible) ; %d irreducible P"
          % (len(rows), red, len(rows) - red), flush=True)
    return rows


if __name__ == "__main__":
    main()
