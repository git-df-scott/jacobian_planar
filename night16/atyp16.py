"""night16 -- ATYPICAL-VALUE DETECTOR (exact, over Q and over number fields).

WHAT IS MEASURED
----------------
For P in Q[x,y] with unimodular gradient (so every fibre F_c = {P = c} is a
SMOOTH affine curve, possibly reducible / disconnected) we compute the
topological Euler characteristic chi(F_c) EXACTLY, as a function of c, and
report every c at which chi(F_c) differs from the generic value.

For a polynomial with no critical points those are exactly the ATYPICAL
values of the fibration (Suzuki / Ha-Le: chi(F_c) = chi(F_gen) for all c iff
P is a locally trivial fibration; a jump is a jump at infinity, since no
critical point exists).

HOW chi IS COMPUTED (the x-projection decomposition)
----------------------------------------------------
Write f = P - c = sum_j a_j(x) y^j, N = deg_y f (a_j for j >= 1 do not
involve c; a_0 does).

(0) Vertical components.  cont = gcd(a_0, ..., a_N) in K[x].  Each distinct
    root s of cont gives a vertical line {x = s} contained in F_c; the fibre
    is smooth, so these lines are connected components, each isomorphic to C,
    each contributing chi = 1.  Put f1 = f / cont, n_vert = #distinct roots
    of cont.

(1) Take S = the set of distinct roots of  W(x) = A(x) * Res_y(f1, d f1/dy),
    A = leading y-coefficient of f1.  (Any superset of the true branch set is
    admissible -- see the identity below.)  Over C \ S the projection
    pi : F1_c -> C_x is an unramified N-sheeted covering, so

        chi(pi^{-1}(C \ S)) = N * (1 - |S|).

    Over each s in S the fibre pi^{-1}(s) is the finite set of DISTINCT roots
    of f1(s, y).  chi is additive over this constructible decomposition, so

        chi(F1_c) = N*(1 - |S|) + sum_{s in S} #{distinct roots of f1(s,y)}.

    Adding a non-branch point to S changes the two terms by -N and +N, so the
    formula is insensitive to over-inclusion.

(2) chi(F_c) = n_vert + chi(F1_c).

Equivalently chi(F_c) = sum over components (2 - 2 g_i - r_i) with r_i the
number of places at infinity; the projection formula computes the same
integer without ever computing g or r.

The counts "#distinct roots of f1(s,y)" are computed for ALL conjugate roots
s of an irreducible / squarefree factor at once, by arithmetic in the ring
K[x]/(V) using dynamic evaluation (D5): whenever an inversion fails, V is
split by the gcd and both halves are pursued.  No factorisation of V and no
numerical root finding is used anywhere.

CANDIDATE ATYPICAL VALUES (algebraic, not by luck)
--------------------------------------------------
chi(F_c) can only change at c where the root pattern of W(x,c) degenerates or
where a vertical component appears.  Factor W(x,c) = prod F_i(x,c)^{e_i} in
Q[x,c].  The candidate set is the set of roots in c of

  * u0(c)                      -- any factor of W involving c only
  * lc_x(F_i)(c)               -- a root of F_i escapes to x = infinity
  * disc_x(F_i)(c)             -- two roots of F_i collide
  * Res_x(F_i, F_j)(c), i<j    -- roots of two different factors collide
  * Res_x(g, a_0 - c)(c),  g = gcd(a_1,...,a_N)   -- vertical component appears

together with (for completeness of the report) c = 0.  Every candidate is
then TESTED by computing chi exactly there; the generic value is fixed by
computing chi at several random rationals.
"""

import itertools
from fractions import Fraction as Fr

import sympy as sp

x, y, cc = sp.symbols('x y c')


# ------------------------------------------------------------------ P plumbing

def dict_to_expr(P):
    """P as {(i,j): Fraction} -> sympy expression."""
    e = sp.Integer(0)
    for (i, j), v in P.items():
        e += sp.Rational(v.numerator, v.denominator) * x**i * y**j
    return sp.expand(e)


def rec_to_dict(Pj):
    """screen15_records.json 'P' field {"i,j": [num, den]} -> {(i,j): Fraction}."""
    out = {}
    for k, v in Pj.items():
        i, j = (int(t) for t in k.split(','))
        out[(i, j)] = Fr(int(v[0]), int(v[1]))
    return out


# ------------------------------------------------- K[x]/(V) dynamic evaluation

class Split(Exception):
    def __init__(self, g):
        self.g = g


def _strip(L):
    while L and L[-1].is_zero:
        L.pop()
    return L


def _inv_mod(a, V):
    """inverse of a in K[x]/(V); raises Split if a is a zero divisor."""
    g = V.gcd(a)
    if g.degree() > 0:
        raise Split(g)
    s, t, h = a.gcdex(V)
    # s*a + t*V = h, h a nonzero constant (as gcd(a,V)=1, h is monic => 1)
    return s.rem(V)


def _rem_monic(A, B, V):
    """A mod B in (K[x]/V)[y], B monic (B[-1] == 1).  Lists ascending in y."""
    A = list(A)
    db = len(B) - 1
    while len(A) - 1 >= db and _strip(A):
        da = len(A) - 1
        if da < db:
            break
        lead = A[-1]
        for i in range(db + 1):
            A[da - db + i] = (A[da - db + i] - lead * B[i]).rem(V)
        _strip(A)
    return A


def _gcd_deg(V, A, B):
    """degree of gcd(A,B) in (K[x]/V)[y]; may raise Split."""
    A = _strip([a.rem(V) for a in A])
    B = _strip([b.rem(V) for b in B])
    while B:
        inv = _inv_mod(B[-1], V)
        B = _strip([(b * inv).rem(V) for b in B])
        R = _rem_monic(A, B, V)
        A, B = B, R
    return (len(A) - 1) if A else -1


def dr_sum(V, coeffs):
    """sum over the distinct roots s of V (squarefree) of
       #{distinct roots of  sum_j coeffs[j](s) y^j }, counted with deg V."""
    total = 0
    stack = [V]
    while stack:
        Vp = stack.pop()
        if Vp.degree() <= 0:
            continue
        cs = _strip([c.rem(Vp) for c in coeffs])
        if not cs:
            raise ValueError("vertical component not removed")
        a = cs[-1]
        g = Vp.gcd(a)
        if g.degree() > 0:
            stack.append(g)
            stack.append(Vp.quo(g))
            continue
        d = len(cs) - 1
        if d == 0:
            continue                       # nonzero constant: no roots
        dcs = _strip([cs[k].mul_ground(k) for k in range(1, len(cs))])
        try:
            gd = _gcd_deg(Vp, cs, dcs)
        except Split as e:
            stack.append(e.g)
            stack.append(Vp.quo(e.g))
            continue
        total += Vp.degree() * (d - max(gd, 0))
    return total


# ------------------------------------------------------------------ chi

def chi_fibre(Pexpr, cval, dom=sp.QQ, extra=False, reduce_=True):
    """exact chi(F_c) for f = Pexpr - cval over the field dom."""
    f = sp.expand(Pexpr - cval)
    if reduce_:
        fp = sp.Poly(f, x, y, domain=dom)
        if not sp.Poly(fp.as_expr(), y, domain=dom[x]).is_sqf:
            f = fp.sqf_part().as_expr()
    Pf = sp.Poly(f, y)
    N = Pf.degree()
    if N < 1:
        raise ValueError("deg_y P must be >= 1")
    co = [sp.Poly(Pf.nth(j), x, domain=dom) for j in range(N + 1)]
    cont = co[0]
    for a in co[1:]:
        cont = cont.gcd(a)
    n_vert = cont.sqf_part().degree() if cont.degree() > 0 else 0
    if cont.degree() > 0:
        co = [a.quo(cont) for a in co]
    co = _strip(co)
    N1 = len(co) - 1
    if N1 < 1:
        return {"chi": n_vert, "n_vert": n_vert, "N1": N1, "Sdeg": 0}
    A = co[-1]
    f1 = sum((co[j].as_expr()) * y**j for j in range(N1 + 1))
    if N1 >= 2:
        R = sp.Poly(sp.resultant(sp.Poly(f1, y, domain=dom[x]),
                                 sp.Poly(sp.diff(f1, y), y, domain=dom[x])),
                    x, domain=dom)
    else:
        R = sp.Poly(1, x, domain=dom)
    W = A * R
    if W.is_zero:
        raise ValueError("W == 0")
    V = W.sqf_part()
    Sdeg = V.degree()
    tot = dr_sum(V, co) if Sdeg > 0 else 0
    chi = n_vert + N1 * (1 - Sdeg) + tot
    out = {"chi": int(chi), "n_vert": int(n_vert), "N1": int(N1),
           "Sdeg": int(Sdeg), "sum_fibre_pts": int(tot)}
    if extra:
        fl = sp.factor_list(sp.expand(Pexpr - cval), x, y)
        out["n_Qfactors"] = sum(m for _, m in fl[1])
        out["Qfactor_degs"] = sorted(sp.Poly(g, x, y).total_degree()
                                     for g, m in fl[1] for _ in range(m))
    return out


# ------------------------------------------------------------------ candidates

def candidates(Pexpr):
    """polynomials in c whose roots contain every possible atypical value."""
    Pf = sp.Poly(Pexpr, y)
    N = Pf.degree()
    a = [sp.Poly(Pf.nth(j), x, domain=sp.QQ) for j in range(N + 1)]
    a0c = sp.Poly(a[0].as_expr() - cc, x, domain=sp.QQ[cc])
    pieces = []
    notes = []
    # (a) vertical components
    if N >= 1:
        g = a[1]
        for t in a[2:]:
            g = g.gcd(t)
        if g.degree() > 0:
            r = sp.Poly(sp.resultant(g.as_expr(), a0c.as_expr(), x), cc)
            if not r.is_zero and r.degree() > 0:
                pieces.append(r.as_expr())
                notes.append("Res_x(gcd(a_1..a_N), a_0 - c)")
    # (b) degeneration of W(x,c)
    f = sp.expand(Pexpr - cc)
    A = sp.Poly(sp.Poly(f, y).nth(N), x)
    if N >= 2:
        R = sp.resultant(sp.Poly(f, y), sp.Poly(sp.diff(f, y), y), y)
    else:
        R = sp.Integer(1)
    W = sp.expand(A.as_expr() * R)
    for F, m in sp.factor_list(W, x, cc)[1]:
        Fp = sp.Poly(F, x)
        dx_ = Fp.degree()
        if dx_ == 0:
            q = sp.Poly(F, cc)
            if q.degree() > 0:
                pieces.append(F)
                notes.append("c-only factor of W")
            continue
        lc = sp.Poly(Fp.LC(), cc)
        if lc.degree() > 0:
            pieces.append(lc.as_expr())
            notes.append("lc_x of a factor of W")
        if dx_ >= 2:
            d = sp.Poly(sp.discriminant(F, x), cc)
            if not d.is_zero and d.degree() > 0:
                pieces.append(d.as_expr())
                notes.append("disc_x of a factor of W")
    facs = [sp.Poly(F, x) for F, m in sp.factor_list(W, x, cc)[1]
            if sp.Poly(F, x).degree() >= 1]
    for F1, F2 in itertools.combinations(facs, 2):
        r = sp.resultant(F1.as_expr(), F2.as_expr(), x)
        rp = sp.Poly(r, cc)
        if not rp.is_zero and rp.degree() > 0:
            pieces.append(r)
            notes.append("Res_x of two factors of W")
    return pieces, notes


def candidate_roots(pieces):
    """factor every candidate polynomial over Q; return
       (rational roots as Rational, irreducible factors of degree >= 2)."""
    rat, irr = set(), []
    seen = set()
    for p in pieces:
        pp = sp.Poly(sp.expand(p), cc)
        if pp.is_zero or pp.degree() == 0:
            continue
        for F, m in sp.factor_list(pp.as_expr(), cc)[1]:
            Fp = sp.Poly(F, cc)
            if Fp.degree() == 1:
                b, aa = Fp.all_coeffs()[1], Fp.all_coeffs()[0]
                rat.add(sp.Rational(-b, aa))
            elif Fp.degree() >= 2:
                key = sp.srepr(sp.factor(Fp.monic().as_expr()))
                if key not in seen:
                    seen.add(key)
                    irr.append(Fp.monic())
    return sorted(rat, key=lambda z: (sp.Rational(z).q, sp.Rational(z).p)), irr


# ------------------------------------------------------------------ driver

def atypical(Pexpr, n_generic=6, verbose=False):
    """full detector.  Returns a dict."""
    import random
    rng = random.Random(20250829)
    gen_vals, gen_chis = [], []
    tries = 0
    while len(gen_chis) < n_generic and tries < 60:
        tries += 1
        v = sp.Rational(rng.randint(-40, 40) * 2 + 1, rng.choice([1, 1, 2, 3, 5, 7]))
        if v in gen_vals:
            continue
        try:
            r = chi_fibre(Pexpr, v)
        except Exception as e:
            continue
        gen_vals.append(v)
        gen_chis.append(r["chi"])
    if not gen_chis:
        return {"error": "no generic chi"}
    from collections import Counter
    chi_gen, nmode = Counter(gen_chis).most_common(1)[0]
    pieces, notes = candidates(Pexpr)
    rat, irr = candidate_roots(pieces)
    if sp.Integer(0) not in rat:
        rat = [sp.Integer(0)] + list(rat)
    tested = []
    atyp = []
    for v in rat:
        if v in gen_vals:
            r = {"chi": gen_chis[gen_vals.index(v)]}
            r.update(chi_fibre(Pexpr, v, extra=True))
        else:
            r = chi_fibre(Pexpr, v, extra=True)
        tested.append({"c": str(v), "kind": "rational", "chi": r["chi"], "detail": r})
        if r["chi"] != chi_gen:
            atyp.append({"c": str(v), "kind": "rational", "chi": r["chi"],
                         "chi_gen": chi_gen, "detail": r})
    for Fp in irr:
        alpha = sp.CRootOf(Fp.as_expr(), 0)
        dom = sp.QQ.algebraic_field(alpha)
        try:
            r = chi_fibre(Pexpr, alpha, dom=dom)
        except Exception as e:
            tested.append({"c": "root of %s" % Fp.as_expr(), "kind": "algebraic",
                           "chi": None, "error": str(e)})
            continue
        tested.append({"c": "root of %s" % Fp.as_expr(), "kind": "algebraic",
                       "chi": r["chi"], "detail": r})
        if r["chi"] != chi_gen:
            atyp.append({"c": "root of %s" % Fp.as_expr(), "kind": "algebraic",
                         "chi": r["chi"], "chi_gen": chi_gen, "detail": r,
                         "minpoly": str(Fp.as_expr()), "deg": Fp.degree()})
    return {"chi_gen": chi_gen, "chi_gen_votes": "%d/%d" % (nmode, len(gen_chis)),
            "generic_c": [str(v) for v in gen_vals], "generic_chi": gen_chis,
            "n_candidates_rational": len(rat),
            "n_candidates_algebraic": len(irr),
            "candidate_notes": sorted(set(notes)),
            "tested": tested, "atypical": atyp}
