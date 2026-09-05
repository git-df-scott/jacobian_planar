"""night12 v2 -- high-degree F2/F2b objects with derived certificates.

Construction (night14 `PROSPECTOR.md` section 2, reparametrised so that every
coefficient is an integer).  Write

    v  = y + tau(x)          tau in Z[x],  deg tau = T >= 1
    g  = c*(x - a)^n         c, a in Z,  c != 0,  n >= 1
    P  = h0*v + g*v^2 + kappa                     h0 in Z, h0 != 0

night14's `t` is `2*tau`, which is where its quarters come from; taking `tau`
integral clears them.  `kappa` is a rational constant, `0` for the F2 shape and
nonzero for the F2b shape -- it shifts which fibre is the reducible one and
changes nothing about the gradient.

    deg P = n + 2*max(1, T).

**Unimodularity, by derivation, with an explicit Bezout certificate.**
`v_y = 1` and `v_x = tau'`, so

    P_y = h0 + 2*g*v
    P_x = v_x*P_y + g'*v^2 ,        g' = c*n*(x-a)^(n-1)

and since `2*(x-a)*g' = 2*n*g`,

    2*(x-a)*(g'*v^2) = n*v*(2*g*v) = n*v*(P_y - h0) ,

which after substituting `g'*v^2 = P_x - v_x*P_y` and then eliminating `v`
through `h0 = P_y - 2*g*v` gives

    1 = A*P_x + B*P_y ,
        A = 4*g*(x-a) / (n*h0^2)
        B = ( h0 - (2*g/n)*( n*v + 2*(x-a)*v_x ) ) / h0^2

with `A`, `B` in `Q[x,y]`.  `bezout_certificate` returns them and the caller
expands `A*P_x + B*P_y - 1` coefficientwise over `Q` and checks it is zero.
That is a proof that `1` is in `(P_x, P_y)`, i.e. that the gradient is
unimodular -- and unlike a Groebner basis it costs nothing at degree 130, where
`S1` times out.

**Non-coordinacy, by derivation.**  `P - kappa = v*(h0 + g*v)` identically, and
both factors are nonconstant, so the fibre `P = kappa` is reducible.  For a `P`
with unimodular gradient every fibre is smooth, so a reducible fibre is a
disconnected one, while a coordinate has every fibre isomorphic to the affine
line and in particular connected.  `factor_certificate` returns the two factors
and the caller checks `P - kappa - v*(h0 + g*v) = 0` coefficientwise over `Q`.
The Shpilrain-Yu instrument (`sy.py`) is run independently on the same `P`.
"""

from fractions import Fraction
import matekit as M


def _u_to_P(u):
    """univariate dict {i: c} in x -> bivariate dict."""
    return {(i, 0): c for i, c in u.items() if c != 0}


def _xma_pow(a, n):
    """(x - a)^n as a bivariate dict, exact."""
    out = {(0, 0): Fraction(1)}
    base = {(1, 0): Fraction(1), (0, 0): Fraction(-a)}
    for _ in range(n):
        out = M.pmul(out, base)
    return out


def _scal(c, A):
    return {k: Fraction(c) * v for k, v in A.items() if Fraction(c) * v != 0}


def build(n, a, c, h0, tau, kappa=0):
    """returns a dict of the object and all its exact pieces."""
    tau = {i: Fraction(x) for i, x in tau.items() if Fraction(x) != 0}
    T = max(tau) if tau else 0
    v = M.padd({(0, 1): Fraction(1)}, _u_to_P(tau))
    g = _scal(c, _xma_pow(a, n))
    gp = _scal(Fraction(c) * n, _xma_pow(a, n - 1)) if n >= 1 else {}
    taup = {i - 1: i * cc for i, cc in tau.items() if i >= 1}
    vx = _u_to_P(taup)
    P = M.padd(_scal(h0, v), M.pmul(g, M.pmul(v, v)))
    if kappa:
        P = M.padd(P, {(0, 0): Fraction(kappa)})
    P = {k: x for k, x in P.items() if x != 0}
    return {"n": n, "a": Fraction(a), "c": Fraction(c), "h0": Fraction(h0),
            "T": T, "tau": tau, "kappa": Fraction(kappa),
            "v": v, "g": g, "gp": gp, "vx": vx, "P": P,
            "deg_P": M.pdeg(P)}


def bezout_certificate(ob):
    """(A, B) with A*P_x + B*P_y = 1, exact over Q."""
    n, h0, a = ob["n"], ob["h0"], ob["a"]
    g, v, vx = ob["g"], ob["v"], ob["vx"]
    xma = {(1, 0): Fraction(1), (0, 0): -a}
    A = _scal(Fraction(4, 1) / (n * h0 * h0), M.pmul(g, xma))
    inner = M.padd(_scal(n, v), _scal(2, M.pmul(xma, vx)))
    B = _scal(Fraction(1) / (h0 * h0),
              M.padd({(0, 0): h0}, _scal(Fraction(-2, 1) / n, M.pmul(g, inner))))
    return A, B


def verify_bezout(ob):
    """expand A*P_x + B*P_y - 1 over Q and check every coefficient is zero."""
    A, B = bezout_certificate(ob)
    P = ob["P"]
    R = M.padd(M.pmul(A, M.dx(P)), M.pmul(B, M.dy(P)))
    R = M.padd(R, {(0, 0): Fraction(-1)})
    bad = {k: x for k, x in R.items() if x != 0}
    return (not bad), len(bad)


def factor_certificate(ob):
    """(f1, f2, kappa) with P - kappa = f1*f2, both factors nonconstant."""
    f1 = ob["v"]
    f2 = M.padd({(0, 0): ob["h0"]}, M.pmul(ob["g"], ob["v"]))
    return f1, f2, ob["kappa"]


def verify_factorisation(ob):
    f1, f2, kap = factor_certificate(ob)
    R = M.padd(ob["P"], {(0, 0): -kap})
    R = M.padd(R, _scal(-1, M.pmul(f1, f2)))
    bad = {k: x for k, x in R.items() if x != 0}
    ok = (not bad) and M.pdeg(f1) >= 1 and M.pdeg(f2) >= 1
    return ok, len(bad), M.pdeg(f1), M.pdeg(f2)


# --------------------------------------------------------------- the A pool

def pool_A():
    """F2/F2b objects with deg P in [124, 132].

    deg P = n + 2*max(1,T); the combinations below spread the shape from
    'almost all of the degree in x' (T = 1) to 'most of it in tau' (T = 61),
    which is what varies the Newton polygon the mate carrier is built from.
    """
    specs = [
        # (n, a, c, h0, tau, kappa, tag)
        (122, 0,  1,  1, {1: 1},                 0,      "F2  T=1 a=0"),
        (126, 1,  2, -1, {1: 1, 0: -3},          0,      "F2  T=1 a=1"),
        (130, -1, 1,  2, {1: -1, 0: 2},          0,      "F2  T=1 a=-1"),
        (120, 0,  1,  1, {2: 1, 0: 1},           0,      "F2  T=2 a=0"),
        (124, 2, -1,  1, {2: 1, 1: -1},          Fraction(3, 4), "F2b T=2 a=2"),
        (128, 0,  2,  1, {2: -1, 1: 2, 0: 1},    Fraction(-1, 2), "F2b T=2 a=0"),
        (120, 1,  1, -2, {3: 1, 1: 1},           0,      "F2  T=3 a=1"),
        (124, 0,  1,  1, {3: 2, 2: -1, 0: 1},    Fraction(5, 2),  "F2b T=3 a=0"),
        (116, 0,  1,  1, {5: 1, 2: 1},           0,      "F2  T=5 a=0"),
        (120, -1, 2,  1, {5: -1, 3: 1, 0: 2},    Fraction(1, 4),  "F2b T=5 a=-1"),
        (2,   0,  1,  1, {61: 1, 1: 1},          0,      "F2  T=61 a=0"),
        (8,   1,  1, -1, {61: 1, 2: -1, 0: 1},   Fraction(-3, 2), "F2b T=61 a=1"),
    ]
    out = []
    for (n, a, c, h0, tau, kappa, tag) in specs:
        ob = build(n, a, c, h0, tau, kappa)
        ob["tag"] = tag
        ob["family"] = "F2b" if ob["kappa"] else "F2"
        out.append(ob)
    return out


if __name__ == "__main__":
    for ob in pool_A():
        okb, nb = verify_bezout(ob)
        okf, nf, d1, d2 = verify_factorisation(ob)
        print("%-16s n=%-4d T=%-3d deg P=%-4d |supp|=%-4d  bezout=%s  factors=%s (%d,%d)"
              % (ob["tag"], ob["n"], ob["T"], ob["deg_P"], len(ob["P"]),
                 okb, okf, d1, d2))
