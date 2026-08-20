"""
T5 -- GAO FAMILY MECHANISM AUDIT   (papers/2608.00222.pdf, sha256 in
papers/SHA256SUMS).

The paper's own AI disclosure says Claude Fable 5 assisted in the proofs and
write-up, so nothing in it is taken on trust here: every dimension-3 map is
re-expanded from the printed components and re-verified in exact rational
arithmetic.

WHAT IS DONE, PER MEMBER
------------------------
dimension 3 (F of section 3.4 = Alpoge's map as Gao prints it; G of section 3.5,
the new degree-four map):
  (a) det J F is expanded exactly and checked to be a nonzero constant;
  (b) the C*-weight structure is FOUND, not assumed: every weight vector in a
      box is tested for making all components weight-graded, and the invariant
      ring's minimal generators are computed as a Hilbert basis;
  (c) the descent content exponent k is computed TWICE --
        (i)  k = deg p1 + deg p2 - 3          (LEMMA W3-4a)
        (ii) k = the exponent in det J(descent) = c * h^k, obtained by actually
             constructing the descent G and factoring its Jacobian
      and the two must AGREE.  That agreement is this module's control.
  (d) a non-injectivity witness is produced and verified by substitution.

dimension > 3 (F4, F5, F6, F7): recorded with degrees, det J and geometric
degree as printed, and skipped, per the brief.

CONTROLS
--------
POSITIVE  the two k-computations must agree on both dimension-3 maps;
POSITIVE  the printed non-injectivity witness of section 3.4 must verify;
POSITIVE  the weight finder must recover (1,-1,-2) for Alpoge's map;
NEGATIVE  the k=(ii) route must give a DIFFERENT exponent on a weight system
          where LEMMA W3-4a predicts a different k -- weights (1,-1,0), where
          k = 0, using an equivariant map built for that class;
NEGATIVE  a deliberately corrupted component (one coefficient changed) must
          make det J non-constant, i.e. the Keller test must fail on it;
NEGATIVE  the non-injectivity verifier must reject a non-witness.
"""

import itertools
import json
import os
import sys
from math import gcd

import sympy as sp

x, y, z = sp.symbols('x y z')
u, v = sp.symbols('u v')
V = (x, y, z)
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def detJ3(F):
    M = sp.Matrix([[sp.diff(f, w) for w in V] for f in F])
    return sp.expand(M.det())


# ---------------------------------------------------------------------------
# the printed dimension-3 maps
# ---------------------------------------------------------------------------
# section 3.4, p.6 -- Alpoge's map in Alpoge's component order
F_ALP = [sp.expand((1 + x * y) ** 3 * z + y ** 2 * (1 + x * y) * (4 + 3 * x * y)),
         sp.expand(y + 3 * x * (1 + x * y) ** 2 * z + 3 * x * y ** 2 * (4 + 3 * x * y)),
         sp.expand(2 * x - 3 * x ** 2 * y - x ** 3 * z)]

# section 3.5, p.7 -- the new degree-four map G = (g1, g2, g3)
G_GAO = [
    sp.expand(-x ** 3 * z - 4 * x ** 2 * y + 2 * x),
    sp.expand(x ** 6 * y ** 3 * z ** 2 + 8 * x ** 5 * y ** 4 * z + 3 * x ** 5 * y ** 2 * z ** 2
              + 16 * x ** 4 * y ** 5 + 20 * x ** 4 * y ** 3 * z + 3 * x ** 4 * y * z ** 2
              + 32 * x ** 3 * y ** 4 + 18 * x ** 3 * y ** 2 * z + x ** 3 * z ** 2
              + 28 * x ** 2 * y ** 3 + 8 * x ** 2 * y * z + 16 * x * y ** 2 + 2 * x * z + 2 * y),
    sp.expand(sp.Rational(3, 8) * x ** 6 * y ** 4 * z ** 2 + 3 * x ** 5 * y ** 5 * z
              + sp.Rational(3, 2) * x ** 5 * y ** 3 * z ** 2 + 6 * x ** 4 * y ** 6
              + sp.Rational(21, 2) * x ** 4 * y ** 4 * z + sp.Rational(9, 4) * x ** 4 * y ** 2 * z ** 2
              + 18 * x ** 3 * y ** 5 + 14 * x ** 3 * y ** 3 * z + sp.Rational(3, 2) * x ** 3 * y * z ** 2
              + sp.Rational(43, 2) * x ** 2 * y ** 4 + 9 * x ** 2 * y ** 2 * z
              + sp.Rational(3, 8) * x ** 2 * z ** 2 + 14 * x * y ** 3 + 3 * x * y * z
              + sp.Rational(9, 2) * y ** 2 + sp.Rational(1, 2) * z)]

# The paper also gives G in closed form; rebuild it from the recipe as an
# INDEPENDENT copy, and require the two to agree.
def gao_recipe(p_poly, q_poly, gamma):
    w = sp.Symbol('w')
    uu = 1 + x * y
    ww = sp.expand(gamma * uu)
    C = sp.expand(gamma * x)
    g2 = sp.cancel(sp.expand(p_poly.subs(w, ww) + 2 * gamma) / C)
    g3 = sp.cancel(sp.expand(q_poly.subs(w, ww) + gamma * ww) / C ** 2)
    return [sp.expand(C), sp.expand(sp.simplify(g2)), sp.expand(sp.simplify(g3))]


# ---------------------------------------------------------------------------
def find_weights(F, box=4):
    """Every primitive weight vector making each component weight-graded."""
    out = []
    polys = [sp.Poly(f, *V) for f in F]
    for wv in itertools.product(range(-box, box + 1), repeat=3):
        if all(c == 0 for c in wv):
            continue
        g = 0
        for c in wv:
            g = gcd(g, abs(c))
        if g != 1:
            continue
        ok, degs = True, []
        for pol in polys:
            ds = {sum(a * b for a, b in zip(m, wv)) for m in pol.monoms()}
            if len(ds) != 1:
                ok = False
                break
            degs.append(ds.pop())
        if ok:
            out.append((wv, tuple(degs)))
    return out


def invariant_generators(wv, B=8):
    """Minimal generators of {e >= 0 : e . w = 0} -- the invariant monomials."""
    S = {e for e in itertools.product(range(B + 1), repeat=3)
         if any(e) and sum(a * b for a, b in zip(e, wv)) == 0}
    gens = []
    for e in sorted(S, key=lambda t: (sum(t), t)):
        dec = False
        for f in S:
            if all(a >= b for a, b in zip(e, f)):
                d = tuple(a - b for a, b in zip(e, f))
                if any(d) and d in S:
                    dec = True
                    break
        if not dec:
            gens.append(e)
    return gens


def mono(e):
    return x ** e[0] * y ** e[1] * z ** e[2]


def build_descent(F, wv, gens):
    """G with G o pi = pi' o F, expressed in (u,v). Returns (G, detJG, h, k)."""
    if len(gens) != 2:
        return None
    p1, p2 = mono(gens[0]), mono(gens[1])
    Fw = [sp.Poly(f, *V).monoms()[0] for f in F]
    wdeg = []
    for f in F:
        pol = sp.Poly(f, *V)
        wdeg.append(sum(a * b for a, b in zip(pol.monoms()[0], wv)))
    # the target coordinates carry the same weights as the source ones, in the
    # order the components appear; build pi' o F by substituting each source
    # variable by the component of matching weight.
    sub = {}
    for var, wt in zip(V, wv):
        cands = [f for f, d in zip(F, wdeg) if d == wt]
        if len(cands) != 1:
            return None
        sub[var] = cands[0]
    q1 = sp.expand(p1.subs(sub, simultaneous=True))
    q2 = sp.expand(p2.subs(sub, simultaneous=True))
    # express q1, q2 in terms of p1, p2 by polynomial division in a lex order
    G = []
    for q in (q1, q2):
        expr = _rewrite_in(q, p1, p2)
        if expr is None:
            return None
        G.append(expr)
    JG = sp.Matrix([[sp.diff(g, w) for w in (u, v)] for g in G]).det()
    JG = sp.factor(sp.expand(JG))
    return G, JG, p1, p2


def _rewrite_in(q, p1, p2, maxdeg=14):
    """Write the invariant q as a polynomial in p1, p2 (brute force, exact)."""
    pol = sp.Poly(q, *V)
    terms = {}
    for m, c in zip(pol.monoms(), pol.coeffs()):
        terms[m] = c
    e1 = sp.Poly(p1, *V).monoms()[0]
    e2 = sp.Poly(p2, *V).monoms()[0]
    out = sp.Integer(0)
    work = dict(terms)
    guard = 0
    while work and guard < 4000:
        guard += 1
        m = max(work)
        c = work[m]
        # solve m = a*e1 + b*e2 over non-negative integers
        found = None
        for a in range(0, maxdeg + 1):
            for b in range(0, maxdeg + 1):
                if all(a * e1[i] + b * e2[i] == m[i] for i in range(3)):
                    found = (a, b)
                    break
            if found:
                break
        if not found:
            return None
        a, b = found
        out += c * u ** a * v ** b
        rem = sp.expand(c * (p1 ** a) * (p2 ** b))
        rp = sp.Poly(rem, *V)
        for mm, cc in zip(rp.monoms(), rp.coeffs()):
            work[mm] = work.get(mm, 0) - cc
            if work[mm] == 0:
                del work[mm]
    return sp.expand(out) if not work else None
