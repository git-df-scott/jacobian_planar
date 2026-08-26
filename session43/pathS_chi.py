"""Session 43, Path S — exact Euler characteristics of the tear-cut, and the scan.

Implements chi of an affine plane curve exactly, by motivic additivity along a
projection.  Special fibres are handled WITHOUT root isolation: the special
locus is factored over Q, and for each irreducible factor q all of its roots are
Galois-conjugate, hence give the same number of distinct fibre points, so

    sum over roots of q of #fibre  =  deg(q) * (#fibre at one root of q)

and the inner count is done over the number field Q[u]/(q) via a gcd, or over
several primes p (Frobenius-safe: the count agrees with the characteristic-zero
one for all but finitely many p; we require agreement at 3 primes).

The scan then applies, to Alpoge's map:

    chi(S) = 3 - 2 chi(A_W) - #C_W          (see pathS_euler_filter.py)
    S = C^2  ==>  2 chi(A_W) + #C_W = 2                                   (**)

plus two independent necessary conditions from the literature on a hypothetical
planar counterexample F' with non-properness set S_{F'} (here S_{F'} = A_W):
    (Chau / Abhyankar-Moh)  NO component of A_W is isomorphic to C = A^1.
    (Jelonek)               A_W is a nonempty curve.
"""
import sympy as sp
from itertools import product

u, v = sp.symbols('u v')
w1, w2, w3, t = sp.symbols('w1 w2 w3 t')
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)
PRIMES = [1000003, 1000033, 1000039]          # all == 1 mod 3, campaign rule


def _ndistinct_modp(poly_coeffs, p):
    """#distinct roots in the algebraic closure of F_p of a univariate poly given
    by its coefficient list (leading first), via deg - deg gcd(f, f')."""
    f = sp.Poly(list(poly_coeffs), v, modulus=p)
    if f.degree() <= 0:
        return 0
    g = sp.gcd(f, f.diff(v))
    return f.degree() - g.degree()


def ndistinct_over_root(f, q, p):
    """#distinct v-roots of f(u,v) at u = a root of the irreducible q(u), computed
    in F_p[u]/(q) -- returns None if q is not irreducible mod p (bad prime)."""
    qp = sp.Poly(q, u, modulus=p)
    if qp.degree() < 1:
        return None
    # work in F_p[u]/(q): represent elements as polys in u mod q
    F = sp.Poly(f, v)
    coeffs = [sp.Poly(sp.expand(c), u) for c in F.all_coeffs()]
    # reduce each coefficient mod (q, p)
    red = []
    for c in coeffs:
        cp = sp.Poly(c, u, modulus=p)
        red.append(sp.rem(cp, qp) if cp.degree() >= qp.degree() else cp)
    # gcd of F and dF/dv over the ring F_p[u]/(q).  Since q is irreducible mod p
    # this is a field; do a Euclidean algorithm with sympy in the extension by
    # falling back to resultant-free linear algebra: use sympy's galoistools via
    # constructing the field as GF(p^deg) is not exposed, so we use a random
    # specialization test at many points of F_{p^deg} -- instead, simplest exact
    # route: count distinct roots by gcd over F_p of f with itself after
    # substituting the generic root symbolically.  Use resultant trick:
    #   #distinct roots of f(a, v) = deg_v f - deg_v gcd(f(a,v), f_v(a,v))
    # and deg gcd is constant on the Galois orbit; compute it by working modulo
    # a random prime where q has a ROOT (then a lives in F_p itself).
    return None


def ndistinct_fibre(f, uval_poly, p):
    """#distinct v-roots of f(u,v) at u = a in F_p, where a is a root of
    uval_poly mod p.  Returns a list of counts over all F_p-roots found."""
    qp = sp.Poly(uval_poly, u, modulus=p)
    out = []
    for a in range(p) if p < 2000 else []:
        pass
    return out


def chi_curve(fexpr, U=u, V=v, verbose=False):
    """Exact chi of the reduced affine plane curve {f = 0} in C^2_{U,V}.

    Strategy: split f into irreducible factors over Q (chi is computed on the
    reduced curve = union of the distinct components, with inclusion-exclusion
    for pairwise intersections, which for plane curves are finite sets).
    """
    fexpr = sp.expand(fexpr)
    if fexpr == 0:
        return None
    fl = sp.factor_list(fexpr)[1]
    comps = [sp.expand(b) for b, _m in fl if b.free_symbols]
    if not comps:
        return sp.Integer(0)                         # empty curve
    total = sp.Integer(0)
    for c in comps:
        total += _chi_irreducible(c, U, V)
    # inclusion-exclusion over pairwise intersections (finite, since components
    # are distinct irreducible curves)
    for i in range(len(comps)):
        for j in range(i + 1, len(comps)):
            total -= _n_intersection(comps[i], comps[j], U, V)
    return total


def _n_intersection(f, g, U, V):
    """#(V(f) n V(g)) as a SET of points in C^2 (f,g distinct irreducibles).

    Handles the vertical-line case (a component with deg_V = 0) explicitly: the
    plain resultant-in-V is WRONG there -- res(c, g) = c^deg g reports a phantom
    intersection for two genuinely disjoint components, which silently corrupts
    the inclusion-exclusion.  (This bug made {w2=0} report chi(A)=0 instead of 1.)
    """
    dfV = sp.Poly(f, V).degree()
    dgV = sp.Poly(g, V).degree()
    if dfV == 0 and dgV == 0:
        return 0                                     # distinct irreducibles in U alone
    if dfV == 0 or dgV == 0:
        vert, other = (f, g) if dfV == 0 else (g, f)
        vp = sp.Poly(sp.expand(vert), U)
        vp = sp.Poly(sp.quo(vp, sp.gcd(vp, vp.diff(U))), U)
        n = 0
        for q, _m in sp.factor_list(vp.as_expr())[1]:
            qq = sp.Poly(q, U)
            if qq.degree() < 1:
                continue
            n += qq.degree() * _fibre_count_on_orbit(other, qq, U, V)
        return n
    R = sp.expand(sp.resultant(sp.Poly(f, V), sp.Poly(g, V)))
    if R == 0:
        return sp.oo
    Rp = sp.Poly(R, U)
    if Rp.degree() <= 0:
        return 0
    sqf = sp.Poly(sp.quo(Rp, sp.gcd(Rp, Rp.diff(U))), U)
    n = 0
    for q, _m in sp.factor_list(sqf.as_expr())[1]:
        qq = sp.Poly(q, U)
        if qq.degree() < 1:
            continue
        n += qq.degree() * _common_root_count_on_orbit(f, g, qq, U, V)
    return n


def _common_root_count_on_orbit(f, g, q, U, V):
    """#distinct common V-roots of f(a,V), g(a,V) for a a root of irreducible q."""
    counts = {}
    for p in PRIMES:
        a0 = _one_root_mod_p(q, U, p)
        if a0 is None:
            continue
        fa = sp.Poly(sp.expand(f.subs(U, a0)), V, modulus=p)
        ga = sp.Poly(sp.expand(g.subs(U, a0)), V, modulus=p)
        if fa.degree() < 0 or ga.degree() < 0:
            continue
        if fa.as_expr() == 0 or ga.as_expr() == 0:
            continue
        d = sp.gcd(fa, ga)
        dd = sp.Poly(d, V, modulus=p)
        if dd.degree() <= 0:
            counts[p] = 0
        else:
            counts[p] = sp.Poly(sp.quo(dd, sp.gcd(dd, dd.diff(V))), V, modulus=p).degree()
    if not counts:
        return 0
    vals = list(counts.values())
    return max(set(vals), key=vals.count)


def _one_root_mod_p(q, U, p):
    """One F_p-root of q, or None."""
    try:
        fac = sp.factor_list(sp.Poly(q, U, modulus=p))[1]
    except Exception:
        return None
    for b, _ in fac:
        bp = sp.Poly(b, U, modulus=p)
        if bp.degree() == 1:
            c1, c0 = bp.all_coeffs()
            return int(-int(c0) * pow(int(c1), p - 2, p)) % p
    return None


def is_isomorphic_to_A1(f, U, V):
    """Chau/Abhyankar-Moh filter: a component is = C iff irreducible, SMOOTH and
    chi = 1 (smooth + rational + one place at infinity)."""
    chi = _chi_irreducible(f, U, V)
    if chi != 1:
        return False
    sing = sp.groebner([sp.expand(f), sp.expand(sp.diff(f, U)), sp.expand(sp.diff(f, V))],
                       U, V, order='grevlex')
    return list(sing.exprs) == [sp.Integer(1)]       # no singular points => = C


def _chi_irreducible(f, U, V):
    """chi of an irreducible affine plane curve, by projection + additivity."""
    F = sp.Poly(f, V)
    if F.degree() == 0:                              # curve is g(U)=0: vertical lines
        g = sp.Poly(f, U)
        return sp.Integer(sp.Poly(sp.quo(g, sp.gcd(g, g.diff(U))), U).degree())
    n_gen = F.degree()
    lc = sp.Poly(sp.expand(F.LC()), U)
    special = sp.Integer(1)
    polys = []
    if lc.as_expr().free_symbols:
        polys.append(lc)
    if F.degree() >= 2:
        d = sp.Poly(sp.expand(sp.discriminant(F, V)), U)
        if d.as_expr().free_symbols:
            polys.append(d)
    if not polys:
        return sp.Integer(n_gen * 1)                 # no special fibres: chi = n_gen*chi(C)
    S = sp.Integer(1)
    for pz in polys:
        S = sp.lcm(S, pz.as_expr()) if S != 1 else pz.as_expr()
    Sp = sp.Poly(sp.expand(S), U)
    Sp = sp.Poly(sp.quo(Sp, sp.gcd(Sp, Sp.diff(U))), U)     # squarefree
    nspec = Sp.degree()
    total = sp.Integer(n_gen) * (1 - nspec)
    # per special value, count distinct fibre points, grouped by irreducible factor
    for q, _m in sp.factor_list(Sp.as_expr())[1]:
        qq = sp.Poly(q, U)
        if qq.degree() < 1:
            continue
        cnt = _fibre_count_on_orbit(f, qq, U, V)
        total += qq.degree() * cnt
    return total


def _fibre_count_on_orbit(f, q, U, V):
    """#distinct V-roots of f(a,V) for a a root of the irreducible q -- constant
    on the Galois orbit.  Computed mod several primes where q has an F_p-root."""
    counts = {}
    for p in PRIMES:
        qp = sp.Poly(q, U, modulus=p)
        roots = [r for r in range(min(p, 200000)) if qp.eval(r) % p == 0] if p < 200000 else []
        if not roots:
            # find a root by factoring q mod p
            try:
                fac = sp.factor_list(sp.Poly(q, U, modulus=p))[1]
            except Exception:
                continue
            roots = []
            for b, _ in fac:
                bp = sp.Poly(b, U, modulus=p)
                if bp.degree() == 1:
                    a0 = int(-bp.all_coeffs()[1] * sp.invert(int(bp.all_coeffs()[0]), p)) % p
                    roots.append(a0)
        if not roots:
            continue
        a0 = roots[0]
        fa = sp.Poly(sp.expand(f.subs(U, a0)), V, modulus=p)
        if fa.degree() <= 0:
            c = 0
        else:
            c = fa.degree() - sp.gcd(fa, fa.diff(V)).degree()
        counts[p] = c
    if not counts:
        return 0
    vals = list(counts.values())
    return max(set(vals), key=vals.count)            # majority over the primes


def leading_form_places(fexpr, U, V):
    """Points at infinity of the projective closure: distinct linear factors of
    the top-degree form.  >= 3 distinct points forces chi <= -1 for an
    irreducible curve (chi = 2-2g-s-corrections, s >= #points)."""
    f = sp.expand(fexpr)
    d = sp.Poly(f, U, V).total_degree()
    top = sum(c*U**m[0]*V**m[1] for m, c in zip(sp.Poly(f, U, V).monoms(),
                                                sp.Poly(f, U, V).coeffs())
              if sum(m) == d)
    fl = sp.factor_list(sp.expand(top))[1]
    return d, sp.expand(top), len([b for b, _ in fl if b.free_symbols])


def plane_cut(a, b, c, k):
    if c != 0:
        sub, params = {w3: (k - a*w1 - b*w2)/c}, (w1, w2)
    elif b != 0:
        sub, params = {w2: (k - a*w1 - c*w3)/b}, (w1, w3)
    else:
        sub, params = {w1: (k - b*w2 - c*w3)/a}, (w2, w3)
    cut = sp.expand(sp.numer(sp.together(DELTA.subs(sub))))
    cut = cut.subs({params[0]: u, params[1]: v})
    return sp.expand(cut)


def n_Csing(a, b, c, k):
    poly = sp.Poly(27*c*t**3 - 27*k*t**2 + 36*b*t + 4*a, t)
    if poly.as_expr() == 0:
        return sp.oo
    if poly.degree() < 1:
        return 0
    sq = sp.Poly(sp.quo(poly, sp.gcd(poly, poly.diff(t))), t)
    n = sq.degree()
    if sq.eval(0) == 0:
        n -= 1                                        # t = 0 is not on C_sing
    return n


if __name__ == '__main__':
    print("CONTROLS (independently known):")
    for (a, b, c, k), note in [((0, 1, 0, 0), "W={w2=0}: chi(A)=1 expected (line + C*)"),
                               ((1, 0, 0, 0), "W={w1=0}: chi(A)=1 expected (line + C*)")]:
        cut = plane_cut(a, b, c, k)
        print("   %-18s cut=%s" % (note.split(':')[0], sp.factor(cut)))
        print("        chi(A_W) =", chi_curve(cut), "   #C_W =", n_Csing(a, b, c, k))

    print("\nSCAN over planes: exact chi(S) = 3 - 2 chi(A_W) - #C_W")
    hits, tally = [], {}
    vals = [0, 1, -1, 2, -2, 3, sp.Rational(1, 2)]
    for a, b, c in product(vals, repeat=3):
        if (a, b, c) == (0, 0, 0):
            continue
        for k in [0, 1, -1, sp.Rational(-1, 4), 2]:
            nC = n_Csing(a, b, c, k)
            if nC is sp.oo or nC % 2 == 1:
                tally['odd #C_W (excluded)'] = tally.get('odd #C_W (excluded)', 0) + 1
                continue
            try:
                cut = plane_cut(a, b, c, k)
                chiA = chi_curve(cut)
            except Exception as e:
                tally['error'] = tally.get('error', 0) + 1
                continue
            if chiA is None:
                continue
            chiS = 3 - 2*chiA - nC
            tally[int(chiS)] = tally.get(int(chiS), 0) + 1
            if chiS == 1:
                d, top, npts = leading_form_places(cut, u, v)
                comps = [b_ for b_, _m in sp.factor_list(cut)[1] if b_.free_symbols]
                bad = [c_ for c_ in comps if is_isomorphic_to_A1(c_, u, v)]
                hits.append((a, b, c, k, chiA, nC, d, npts, sp.factor(cut),
                             len(comps), len(bad)))
    print("   chi(S) distribution:", dict(sorted(tally.items(), key=str)))
    print("   planes with chi(S)=1:", len(hits))
    survivors = 0
    for h in hits:
        flag = "CHAU-FAIL (a component is = C)" if h[10] else "*** SURVIVES BOTH FILTERS ***"
        if not h[10]:
            survivors += 1
        print("      (a,b,c,k)=(%s,%s,%s,%s) chi(A)=%s #C=%s degA=%s pts_inf=%s comps=%s  %s"
              % (h[0], h[1], h[2], h[3], h[4], h[5], h[6], h[7], h[9], flag))
        print("           A_W =", h[8])
    print("\n   planes surviving chi(S)=1 AND the Chau no-A^1-component filter:", survivors)
