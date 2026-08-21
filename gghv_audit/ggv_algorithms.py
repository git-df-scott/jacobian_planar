"""
gghv_audit / an independent re-implementation of the GGHV enumeration apparatus.

WHAT THIS IS
------------
GGHV (arXiv:2204.14178) does NOT enumerate degree pairs itself.  Its Theorem 2.1
("max{deg P, deg Q} >= 125 or (deg P, deg Q) in {(72,108),(108,72)}") starts from
a table of TEN cases which it imports wholesale from

    [5] = Guccione, Guccione, Horruitiner, Valqui,
          "Some algorithms related to the Jacobian Conjecture", arXiv:1708.07936,
          sections 5 and 6.

So a mechanical re-derivation of GGHV's degree-pair claim is a re-derivation of
[5]'s Algorithms 1-9.  That is what this module is: a from-the-paper
re-implementation, written only from the pseudocode and definitions of
arXiv:1708.07936, with page/display references on every routine.

    Algorithm 1  GetPossibleLastLowerCorners   [5, p.3]
    Algorithm 2  GetStartingEdges              [5, p.5]
    Algorithm 3  GetGeneratedCorners           [5, p.10]  (Definitions 2.8-2.12)
    Algorithm 4  GetCornerChildrenList         [5, p.10]  (Remark 2.16)
    Algorithm 5  GetChildrenAndFinalList       [5, p.11]
    Algorithm 6  GetCompleteChains             [5, p.12]  (Definition 2.19)
    Algorithm 7  GetIsAdmissible               [5, p.18]  (Definition 2.25)
    Algorithm 8  Main                          [5, p.18]
    Definition 3.3 / Proposition 3.2           [5, p.21]  the (m,n) families

CONVENTIONS, taken from the paper
---------------------------------
* A corner is A = (a wr l, b); its geometric realization is A = (a/l, b).
* v_{rho,sigma}(A) := rho*(a/l) + sigma*b.
* dir(u,v) is the PRIMITIVE COVECTOR (rho,sigma) with rho*u + sigma*v = 0,
  normalised to rho > 0 (or rho = 0, sigma < 0).  This reproduces the paper's
  own display  (rho,sigma) = (f2*l - l, l - f1)/gcd(f1-l, f2*l-l)   [5, p.5].
* the order on directions is by slope sigma/rho; I = ](1,-1),(1,0)].
* gap(rho,l) := rho/gcd(rho,l).
* a corner (a wr l, b) is FINAL iff l - a/b > 1   [5, Definition 2.18].

This module makes no claims.  Its controls live in w5_gghv_controls.py.
"""

from fractions import Fraction
from math import gcd, isqrt


# --------------------------------------------------------------------------
# directions
# --------------------------------------------------------------------------
def _primitive(p, q):
    """Primitive integer form of the covector (p,q), given as Fractions."""
    p, q = Fraction(p), Fraction(q)
    den = p.denominator * q.denominator // gcd(p.denominator, q.denominator)
    P, Q = int(p * den), int(q * den)
    g = gcd(abs(P), abs(Q))
    if g == 0:
        raise ValueError("zero covector")
    P, Q = P // g, Q // g
    if P < 0 or (P == 0 and Q > 0):
        P, Q = -P, -Q
    return (P, Q)


def direction(u, v):
    """dir of the VECTOR (u,v): the primitive covector annihilating it."""
    return _primitive(v, -Fraction(u))


def dlt(d1, d2):
    """d1 < d2 in the slope order (valid for rho >= 0)."""
    return d1[1] * d2[0] < d2[1] * d1[0]


def val(d, A):
    """v_{rho,sigma}(A) for a corner A = (a, l, b), as a Fraction."""
    a, l, b = A
    return d[0] * Fraction(a, l) + d[1] * b


def geo(A):
    a, l, b = A
    return (Fraction(a, l), Fraction(b))


def gap(rho, l):
    return rho // gcd(rho, l)


def is_final(A):
    """[5, Definition 2.18]:  A = (a wr l, b) is final iff l - a/b > 1."""
    a, l, b = A
    if b == 0:
        return False
    return Fraction(l) - Fraction(a, b) > 1


def frac_gcd(*xs):
    """gcd of rationals: gcd(n_i/d_i) = gcd(n_i * D/d_i)/D with D = lcm(d_i)."""
    xs = [Fraction(x) for x in xs if x != 0]
    if not xs:
        return Fraction(0)
    D = 1
    for x in xs:
        D = D * x.denominator // gcd(D, x.denominator)
    g = 0
    for x in xs:
        g = gcd(g, abs(int(x * D)))
    return Fraction(g, D)


def nprimefactors(n):
    """Number of prime factors with multiplicity."""
    n = abs(int(n))
    if n <= 1:
        return 0
    c, d = 0, 2
    while d * d <= n:
        while n % d == 0:
            n //= d
            c += 1
        d += 1
    if n > 1:
        c += 1
    return c


# --------------------------------------------------------------------------
# Algorithm 1  [5, p.3]
# --------------------------------------------------------------------------
def get_possible_last_lower_corners(xmax, drop_theta=False, drop_vrho=False):
    """Returns (PLLC as a set of (a,b), PFL as a dict (a,b)->(rho,sigma)).

    drop_theta / drop_vrho are NEGATIVE-CONTROL switches: they disable one of
    the paper's filters, which must change the output.  They are never set in
    a production run.
    """
    PFL = {}
    PLLC = set()
    for a in range(1, xmax + 1):
        b = 0
        while b <= a - 1 and b <= (a - b - 1) ** 2:
            if b == 0:
                PFL[(a, b)] = (0, -1)
                PLLC.add((a, b))
            elif a > 2 * b > 0:
                PFL[(a, b)] = (1, -2)
                PLLC.add((a, b))
            else:
                cur = (1, -1)
                for (r, s), drs in PFL.items():
                    if not (r < a and s < b and r - s < a - b):
                        continue
                    N1 = gcd(a - r, b - s)
                    N2 = gcd(r, s)
                    d = ((b - s) // N1, (r - a) // N1)
                    if d[0] == 0 and d[1] == 0:
                        continue
                    g = gcd(abs(d[0] + d[1]), abs(d[0] * a + d[1] * b))
                    if g == 0:
                        continue
                    theta = abs(d[0] * a + d[1] * b) // g
                    ok_order = dlt(drs, d) and dlt(d, cur)
                    ok_v = drop_vrho or (d[0] * a + d[1] * b >= d[0])
                    ok_theta = drop_theta or (theta <= N1 or (N2 != 0 and N2 % theta == 0))
                    if ok_order and ok_v and ok_theta:
                        cur = d
                if dlt(cur, (1, -1)):
                    PFL[(a, b)] = cur
                    PLLC.add((a, b))
            b += 1
    return PLLC, PFL


# --------------------------------------------------------------------------
# valid-edge predicate  [5, Definition 2.2 + Remark 2.3]
# --------------------------------------------------------------------------
def edge_data(A, Ap):
    """(rho,sigma), d, and the simplicity flag for a candidate edge (A, A')."""
    a, l, b = A
    ap, lp, bp = Ap
    assert l == lp
    d = direction(Fraction(a - ap, l), Fraction(b - bp))
    return d


def is_simple(A, Ap, mu):
    """simple iff v01(enF) - 1 = gap(rho,l) and (gap > 1 or v01(A') > 0)."""
    a, l, b = A
    _, _, bp = Ap
    d0 = gcd(a, b)
    rho, sigma = edge_data(A, Ap)
    f2 = Fraction(mu, d0) * b
    return (f2 - 1 == gap(rho, l)) and (gap(rho, l) > 1 or bp > 0)


# --------------------------------------------------------------------------
# Algorithm 2  [5, p.5]
# --------------------------------------------------------------------------
def get_starting_edges(a, b, PLLC):
    """All valid edges (A, A') with A = (a,b) in N x N, a < b, l = 1."""
    out = []
    d0 = gcd(a, b)
    for mu in range(1, d0):
        f1 = Fraction(mu * a, d0)
        f2 = Fraction(mu * b, d0)
        if f1.denominator != 1 or f2.denominator != 1:
            continue
        if f2 <= 1 or f1 < 1:
            continue                      # enF must lie in N(l) x N and give rho > 0
        rho, sigma = direction(f1 - 1, f2 - 1)
        if not (rho > 0 and sigma <= 0 and rho + sigma > 0):
            continue                      # (rho,sigma) in I = ](1,-1),(1,0)]
        for i in range(1, b // rho + 1):
            ap = a + i * sigma
            bp = b - i * rho
            if ap < 1 or bp < 0:
                continue
            v = ap - bp                   # v_{1,-1}(A')
            if v < 0 or (v > 0 and (ap, bp) in PLLC):
                out.append(((a, 1, b), (ap, 1, bp), mu))
    return out


# --------------------------------------------------------------------------
# Algorithm 3  [5, p.10]
# --------------------------------------------------------------------------
def get_generated_corners(A, Ap, mu):
    a, l, b = A
    ap, _, bp = Ap
    rho, sigma = edge_data(A, Ap)
    out = []
    if Fraction(ap, l) - bp < 0:                      # v_{1,-1}(A') < 0
        out.append(Ap)
        return out
    l1 = l * rho // gcd(l, rho)
    gp = gap(rho, l)
    gmax = min(Fraction(b - bp, gp), Fraction(b - 1))
    if gmax.denominator != 1:
        gmax = Fraction(int(gmax))
    gmax = int(gmax)

    def corner(b1):
        a1 = Fraction(a * l1, l) + (b1 - b) * Fraction(-sigma * l1, rho)
        if a1.denominator != 1 or a1 <= 0:
            return None
        return (int(a1), l1, b1)

    if is_simple(A, Ap, mu):
        C = corner(gmax)
        if C is not None:
            a1, _, b1 = C
            if (Fraction(l1) - Fraction(a1, b1) > 1) or gcd(a1, b1) > 1:
                out.append(C)
    else:
        for b1 in range(bp + 1, gmax + 1):
            C = corner(b1)
            if C is None:
                continue
            a1, _, _ = C
            if Fraction(a1, l1) - b1 >= 0:            # need v_{1,-1}(A1) < 0
                continue
            if (Fraction(l1) - Fraction(a1, b1) > 1) or gcd(a1, b1) > 1:
                out.append(C)
    return out


# --------------------------------------------------------------------------
# Algorithm 4  [5, p.10]
# --------------------------------------------------------------------------
def get_corner_children(A, Ap, A1, PLLC):
    a1, l1, b1 = A1
    rho, sigma = edge_data(A, Ap)
    d1 = gcd(a1, b1)
    vA1 = val((rho, sigma), A1)
    if vA1 == 0:
        return []
    lo = int(Fraction(1) + Fraction(d1 * (rho + sigma)) / vA1)
    hi = d1
    if l1 > 1:
        hi = int(Fraction(l1 * (b1 * l1 - a1)) + Fraction(d1, b1))
    out = []
    for mu in range(max(lo, 1), hi + 1):
        if d1 != 0 and mu % d1 == 0:
            continue
        f1 = Fraction(mu, d1) * Fraction(a1, l1)
        f2 = Fraction(mu, d1) * b1
        if f2 <= 1:
            continue
        if (f1 * l1).denominator != 1 or f2.denominator != 1:
            continue
        rho1, sigma1 = direction(f1 - 1, f2 - 1)
        if not (rho1 > 0 and sigma1 <= 0 and rho1 + sigma1 > 0):
            continue
        gp1 = gap(rho1, l1)
        if gp1 > b1:
            continue
        for j in range(1, b1 // gp1 + 1):
            xa = Fraction(a1, l1) + j * Fraction(gp1 * sigma1, rho1)
            xb = b1 - j * gp1
            if xb < 0 or xa <= 0:
                continue
            num = xa * l1
            if num.denominator != 1:
                continue
            Ap1 = (int(num), l1, int(xb))
            v = xa - xb                                # v_{1,-1}(A'_1)
            ok = ((l1 > 1 and v != 0)
                  or (l1 == 1 and v < 0)
                  or (l1 == 1 and v > 0 and (Ap1[0], Ap1[2]) in PLLC))
            if ok:
                out.append((A1, Ap1, mu))
    return out


# --------------------------------------------------------------------------
# Algorithm 5  [5, p.11]
# --------------------------------------------------------------------------
def get_children_and_final(A, Ap, mu, PLLC):
    gen = get_generated_corners(A, Ap, mu)
    children, finals = [], []
    for A1 in gen:
        if is_final(A1):
            finals.append(A1)
        children.extend(get_corner_children(A, Ap, A1, PLLC))
    return children, finals


# --------------------------------------------------------------------------
# Algorithm 6  [5, p.12] + Definition 2.19
# --------------------------------------------------------------------------
def get_complete_chains(A, Ap, mu, PLLC):
    a, l, b = A
    _, _, bp = Ap
    rho, sigma = edge_data(A, Ap)
    D = gcd(b, (b - bp) // rho) if (b - bp) % rho == 0 else gcd(b, 0)
    Lmax = nprimefactors(D) + 1
    complete = []
    open_chains = [[(A, Ap, mu)]]
    j = 0
    while j < Lmax and open_chains:
        nxt = []
        for CH in open_chains:
            lastA, lastAp, lastmu = CH[-1]
            children, finals = get_children_and_final(lastA, lastAp, lastmu, PLLC)
            for A1 in finals:
                complete.append((list(CH), A1))
            for ch in children:
                nxt.append(list(CH) + [ch])
        open_chains = nxt
        j += 1
    return complete


# --------------------------------------------------------------------------
# Algorithm 7  [5, p.18] + Definition 2.25
# --------------------------------------------------------------------------
def q_of(A, Ap):
    d = edge_data(A, Ap)
    v = val(d, A)
    g = frac_gcd(d[0] + d[1], v)
    return v / g


def is_admissible(chain, last, drop=False):
    """chain = [(A_i, A'_i, mu_i)], last = A_{j+1}.  [5, Definition 2.25]."""
    if drop:
        return True
    j = len(chain) - 1
    corners = [c[0] for c in chain] + [last]
    for h in range(0, j + 1):
        Ah, Aph, _ = chain[h]
        ah, lh, bh = Ah
        aph, _, bph = Aph
        rho, sigma = edge_data(Ah, Aph)
        gp = gap(rho, lh)
        qh = q_of(Ah, Aph)
        for i in range(h + 1, j + 1):
            Ai, Api, _ = chain[i]
            li = Ai[1]
            qi = q_of(Ai, Api)
            bh1 = corners[h + 1][2]
            D = frac_gcd(Fraction(bh - bph, gp), bh, bh1,
                         Fraction(ah * li, lh), Fraction(aph * li, lh))
            if D == 0 or D.denominator != 1:
                return False
            Di = int(D)
            if nprimefactors(Di) < i - h:
                return False
            if qi.denominator != 1 or Di % int(qi) != 0:
                return False
            if qh.denominator != 1 or qi.denominator != 1:
                return False
            if int(qi) % int(qh) == 0:
                return False
    return True


# --------------------------------------------------------------------------
# Algorithm 8  [5, p.18]
# --------------------------------------------------------------------------
def admissible_complete_chains(M, PLLC=None, drop_admissibility=False):
    if PLLC is None:
        PLLC, _ = get_possible_last_lower_corners(M * M // 2 + 4)
    out = []
    for a in range(2, M // 2 + 1):
        for b in range(a + 1, M - a + 1):
            for (A, Ap, mu) in get_starting_edges(a, b, PLLC):
                for chain, last in get_complete_chains(A, Ap, mu, PLLC):
                    if is_admissible(chain, last, drop=drop_admissibility):
                        out.append((chain, last))
    return out


# --------------------------------------------------------------------------
# (m,n)-families:  Definition 3.3 and Proposition 3.2  [5, p.21]
# --------------------------------------------------------------------------
def mn_pairs(Afinal, max_mn=200):
    """MN(A) = union over k in I(A) of MN_k(A).

    I(A)     = { k in N : 1 <= k < l - a/b  and  gcd(b,(bl-a)/gcd(k,bl-a)) = 1 }
    MN_k(A)  = { (m,n) : m,n > 1, gcd(m,n)=1, (m+n)bk - n(bl-a) = k }
    """
    a, l, b = Afinal
    if b == 0:
        return []
    bl_a = b * l - a
    out = []
    kmax = Fraction(l) - Fraction(a, b)
    k = 1
    while k < kmax:
        ek = gcd(k, bl_a)
        if bl_a % ek == 0 and gcd(b, bl_a // ek) == 1:
            # (m+n) b k - n (bl-a) = k   ->   m b k = k - n(bk - (bl-a))
            for n in range(2, max_mn + 1):
                num = k + n * (bl_a - b * k)
                if b * k == 0:
                    continue
                if num % (b * k) != 0:
                    continue
                m = num // (b * k)
                if m > 1 and gcd(m, n) == 1:
                    out.append((k, m, n))
        k += 1
    return out
