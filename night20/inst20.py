"""night20 -- instruments for the irreducible-fibre / positive-genus target.

Measurements only.  Everything here is a test that either returns a
machine-checkable certificate or returns a verdict together with the exact
data it was computed from.

Objects: a polynomial P in Q[x,y] is carried as a sympy Expr in the symbols
x, y (and, where a fibre parameter is needed, c).

External oracle: Singular (std / lift / resultant / factorize / absFactorize /
normal.lib::genus).  Every Singular call is a batch script terminated by
`quit;` and its answers are parsed off explicit markers.
"""
import os, re, subprocess, tempfile, json, itertools
from fractions import Fraction
import sympy as sp

x, y, c = sp.symbols('x y c')
SING = "Singular"


# --------------------------------------------------------------- Singular I/O
def singular(script, timeout=300):
    txt = script + "\nquit;\n"
    p = subprocess.run([SING, "-q"], input=txt, capture_output=True,
                       text=True, timeout=timeout)
    return p.stdout + p.stderr


def sstr(e):
    """sympy Expr -> Singular input string (^ is fine in Singular)."""
    e = sp.expand(e)
    s = sp.sstr(e)
    return s.replace("**", "^")


def parse_marked(out, key):
    for line in out.splitlines():
        if line.startswith(key + ":"):
            return line[len(key) + 1:].strip()
    return None


def s2sympy(s):
    """Singular polynomial string -> sympy Expr."""
    if s is None:
        return None
    s = s.strip()
    if s == "":
        return None
    s = s.replace("^", "**")
    # Singular prints 2xy3 for 2*x*y^3 ; insert the missing '*'
    s = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', s)
    s = re.sub(r'([a-zA-Z])(\d)', r'\1**\2', s)
    s = re.sub(r'([a-zA-Z])\(', r'\1*(', s)
    s = re.sub(r'\)([a-zA-Z0-9])', r')*\1', s)
    s = re.sub(r'([a-zA-Z\)])\s*([a-zA-Z])', r'\1*\2', s)
    return sp.sympify(s, locals={'x': x, 'y': y, 'c': c, 'a': sp.Symbol('a')})


# ------------------------------------------------------------- unimodularity
def unimodular(P):
    """1 in (P_x, P_y)?  Returns dict with the Groebner verdict and, on
    success, an explicit Bezout pair (U, V) whose residual U*P_x+V*P_y-1 is
    expanded in sympy and must be identically 0."""
    Px, Py = sp.expand(sp.diff(P, x)), sp.expand(sp.diff(P, y))
    if Px == 0 and Py == 0:
        return {"unimodular": False, "reason": "P constant"}
    sc = ("ring r=0,(x,y),dp;\npoly Px=%s;\npoly Py=%s;\n"
          "ideal I=Px,Py;\nideal G=std(I);\n"
          '"RED:",reduce(poly(1),G);\n' % (sstr(Px), sstr(Py)))
    out = singular(sc)
    red = parse_marked(out, "RED")
    if red is None:
        return {"unimodular": None, "reason": "singular failed", "raw": out[:400]}
    if red.strip() != "0":
        return {"unimodular": False, "reduce_1_mod_std": red.strip()}
    sc2 = ("ring r=0,(x,y),dp;\npoly Px=%s;\npoly Py=%s;\nideal I=Px,Py;\n"
           "matrix T=lift(I,ideal(1));\n"
           '"U:",T[1,1];\n"V:",T[2,1];\n' % (sstr(Px), sstr(Py)))
    out2 = singular(sc2)
    U, V = s2sympy(parse_marked(out2, "U")), s2sympy(parse_marked(out2, "V"))
    res = sp.expand(U * Px + V * Py - 1)
    return {"unimodular": True, "U": U, "V": V,
            "residual": res, "residual_zero": bool(res == 0)}


# --------------------------------------------------------- Newton polygon
def support(P):
    P = sp.Poly(sp.expand(P), x, y)
    return [m for m in P.monoms()]


def newton_interior(P):
    """number of interior lattice points of the Newton polygon of the generic
    fibre P - c (Baker's bound for its geometric genus)."""
    pts = support(P) + [(0, 0)]
    if len(pts) < 3:
        return 0
    hull = _hull(pts)
    if len(hull) < 3:
        return 0
    A2 = 0                      # twice the area
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        A2 += a[0] * b[1] - b[0] * a[1]
    A2 = abs(A2)
    B = 0
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        B += _gcd(abs(a[0] - b[0]), abs(a[1] - b[1]))
    # Pick: A = I + B/2 - 1  ->  I = (A2 - B + 2)/2
    return (A2 - B + 2) // 2


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def _hull(pts):
    pts = sorted(set(pts))
    if len(pts) <= 2:
        return pts
    def cross(o, a, b):
        return (a[0]-o[0])*(b[1]-o[1]) - (a[1]-o[1])*(b[0]-o[0])
    lo = []
    for p in pts:
        while len(lo) >= 2 and cross(lo[-2], lo[-1], p) <= 0:
            lo.pop()
        lo.append(p)
    up = []
    for p in reversed(pts):
        while len(up) >= 2 and cross(up[-2], up[-1], p) <= 0:
            up.pop()
        up.append(p)
    return lo[:-1] + up[:-1]


# ------------------------------------------------------------------- genus
def genus_generic(P, timeout=300):
    """geometric genus of the generic fibre P = c, computed over Q(c) by
    Singular's normal.lib::genus (genus of the normalisation of the
    projective closure)."""
    sc = ('LIB "normal.lib";\nring r=(0,c),(x,y),dp;\npoly f=%s-c;\n'
          '"G:",genus(ideal(f));\n' % sstr(P))
    try:
        out = singular(sc, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None, "timeout"
    g = parse_marked(out, "G")
    if g is None:
        return None, out[:300]
    try:
        return int(g), "ok"
    except ValueError:
        return None, g


def genus_at(P, c0, timeout=300):
    sc = ('LIB "normal.lib";\nring r=0,(x,y),dp;\npoly f=%s-(%s);\n'
          '"G:",genus(ideal(f));\n' % (sstr(P), c0))
    try:
        out = singular(sc, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    g = parse_marked(out, "G")
    try:
        return int(g)
    except (TypeError, ValueError):
        return None


# ------------------------------------------- absolute irreducibility over Qbar
def abs_factor_count(F, timeout=300):
    """number of absolutely irreducible factors (with multiplicity) of
    F in Q[x,y], via Singular's absFactorize."""
    sc = ('LIB "absfact.lib";\nring r=0,(x,y),dp;\npoly f=%s;\n'
          'def L=absFactorize(f); setring L;\n"N:",absolute_factors[4];\n'
          % sstr(F))
    try:
        out = singular(sc, timeout=timeout)
    except subprocess.TimeoutExpired:
        return None
    n = parse_marked(out, "N")
    try:
        return int(n)
    except (TypeError, ValueError):
        return None


def fibre_abs_components(P, m, timeout=300):
    """Number of absolutely irreducible components of the fibre P = c0, where
    c0 runs over the roots of the irreducible m(c) in Q[c].

    Uses  N(x,y) = Res_c( m(c), P(x,y) - c ) = prod_i (P - c_i).  The conjugate
    fibres all have the same number r of absolute factors, and N has k*r of
    them (k = deg m), so r = absFactorCount(N) / k.  This keeps every
    factorisation over Q, where absFactorize is available."""
    k = sp.Poly(m, c).degree()
    N = sp.expand(sp.resultant(sp.Poly(m, c), sp.Poly(P - c, c), c))
    n = abs_factor_count(N, timeout=timeout)
    if n is None:
        return None, None
    return sp.Rational(n, k), N


# ----------------------------------------- the finite candidate set of bad c
def _cand_proj(P, v, w):
    """Candidate bad c from projecting away the variable v (w = the other).
    Superset argument in bad_c_candidates.__doc__."""
    f = sp.expand(P - c)
    Pv = sp.Poly(f, v)
    n = Pv.degree()
    if n < 1:
        return None
    pieces = []
    # (0) content degeneration: the coefficients of f in v acquire a common
    #     factor -> a whole component splits off.
    co = Pv.all_coeffs()                      # leading first, constant last
    tail = [sp.expand(t) for t in co[:-1]]
    G = sp.gcd_list(tail) if tail else sp.Integer(1)
    G = sp.expand(G)
    a0 = sp.expand(co[-1] + c)                # the c-free constant term
    if sp.Poly(G, w).degree() >= 1:
        pieces.append(sp.expand(sp.resultant(sp.Poly(G, w), sp.Poly(a0 - c, w), w)))
    if n == 1:
        pass
    else:
        D = sp.expand(sp.discriminant(Pv, v))
        if D == 0:
            return None
        Dw = sp.Poly(D, w)
        if Dw.degree() == 0:
            pieces.append(sp.expand(D))
        else:
            Ds = Dw.sqf_part()
            pieces.append(sp.expand(sp.discriminant(Ds, w)))
            pieces.append(sp.expand(Dw.LC()))
            pieces.append(sp.expand(Ds.LC()))
            a = sp.Poly(Pv.LC(), w)
            if a.degree(w) >= 1:
                pieces.append(sp.expand(sp.resultant(a, Ds, w)))
            pieces.append(sp.expand(sp.gcd_list([sp.expand(t) for t in Dw.all_coeffs()])))
    facs = set()
    for pc in pieces:
        pc = sp.expand(pc)
        if pc == 0:
            continue
        pcp = sp.Poly(pc, c)
        if pcp.degree() == 0:
            continue
        for (fac, _) in sp.factor_list(pcp.as_expr(), c)[1]:
            fq = sp.Poly(fac, c)
            if fq.degree() >= 1:
                facs.add(sp.expand(fq.monic().as_expr()))
    return facs


def bad_c_candidates(P, timeout=300):
    """A finite superset of the values c for which the fibre P = c can fail to
    be irreducible over Qbar.

    The generic fibre is irreducible over Qbar(c) for EVERY P: the polynomial
    P(x,y) - c is irreducible in Qbar[x,y,c] (degree 1 in c, unit leading
    coefficient, and the two coefficients 1 and P are coprime), hence by Gauss
    irreducible in Qbar(c)[x,y].  So only finitely many special c can fail.

    Superset, projecting away y (the projection away x is symmetric):
    write P - c = sum_j b_j(x) y^j, n = deg_y, a(x) = b_n.  Off the roots of
    a(x) the fibre is an n-sheeted cover of the x-line branched over the roots
    of D(x,c) = disc_y(P-c).  Moving c inside a region where (i) no two roots
    of D collide, (ii) no root of D escapes to x = infinity, (iii) no root of D
    meets a root of a(x), (iv) the coefficients b_1..b_n and b_0 acquire no new
    common root, gives a locally trivial branched-cover family, so the number
    of connected components of the fibre is constant on that region.  The
    generic fibre is connected, hence the reducible values are contained in the
    zero set of
        disc_x(sqfree_x D) * lc_x(D) * lc_x(sqfree_x D) * Res_x(a, sqfree_x D)
        * cont_x(D) * Res_x( gcd(b_1..b_n), b_0 ).
    Both projections give valid supersets, so their INTERSECTION is used.
    Returns the list of irreducible factors over Q[c]."""
    S1 = _cand_proj(P, y, x)
    S2 = _cand_proj(P, x, y)
    if S1 is None and S2 is None:
        return None, "both projections degenerate"
    if S1 is None:
        S = S2
    elif S2 is None:
        S = S1
    else:
        S = S1 & S2
    return sorted(S, key=lambda e: (sp.Poly(e, c).degree(), sp.sstr(e))), "ok"


def all_fibres_irreducible(P, timeout=300, verbose=False):
    """Full fibre-irreducibility measurement: the generic fibre (free, see
    bad_c_candidates) plus every candidate special value."""
    cand, msg = bad_c_candidates(P, timeout=timeout)
    if cand is None:
        return {"ok": False, "reason": msg}
    rows = []
    allirr = True
    for m in cand:
        r, N = fibre_abs_components(P, m, timeout=timeout)
        if r is None:
            return {"ok": False, "reason": "absFactorize failed on %s" % m,
                    "rows": rows}
        rows.append({"m(c)": sp.sstr(m), "abs_components": str(r)})
        if r != 1:
            allirr = False
        if verbose:
            print("      c-factor %-28s abs components = %s" % (sp.sstr(m), r))
    return {"ok": True, "all_irreducible": allirr,
            "n_candidates": len(cand), "rows": rows}
