"""night17 -- THE INVERTED SEARCH: synthesise P satisfying (a) unimodularity,
(b) non-coordinacy and (c') vanishing Gelfand-Leray residues BY CONSTRUCTION,
support by support, then hand every survivor to the exact mate solver.

Per support: the residue-equation system (systems17), its solution structure by
Groebner over Q, the instances built from the solution parametrisation, and for
each instance the three certificates and the mate verdict.
"""
import hashlib
import json
import os
import sys
import time
from fractions import Fraction as F

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "night15"))

import pk17 as pk                                          # noqa: E402
import res17 as R                                          # noqa: E402
import certs17 as CE                                       # noqa: E402
import systems17 as SY                                     # noqa: E402
import mate17 as MT                                        # noqa: E402

X = R.X
LOG = []


def say(s):
    print(s)
    sys.stdout.flush()
    LOG.append(s)


def phash(P):
    return hashlib.sha1(repr(sorted((k, str(v)) for k, v in P.items()))
                        .encode()).hexdigest()[:12]


# ----------------------------------------------------------- instance builders
def he_instance(gamma, a, hc, alpha, g_const=None):
    """P = g y^2 + h y + k with Delta = h^2 - 4 g k = alpha x + beta forced.

    g = gamma (x - a)  (or the constant g_const), h = sum hc[i] x^i, and
    beta is fixed by the divisibility  4 g | h^2 - (alpha x + beta), i.e.
    h(a)^2 = alpha a + beta in the linear-g case.
    """
    h = sum(sp.Rational(c) * X ** i for i, c in enumerate(hc))
    if g_const is not None:
        g = sp.Rational(g_const)
        beta = sp.Symbol("bb")
        k = sp.cancel((h ** 2 - sp.Rational(alpha) * X - beta) / (4 * g))
        k = sp.expand(k.subs(beta, 0))
        Delta = sp.expand(h ** 2 - 4 * g * k)
    else:
        g = sp.Rational(gamma) * (X - sp.Rational(a))
        beta = sp.expand(h.subs(X, sp.Rational(a)) ** 2 - sp.Rational(alpha) * sp.Rational(a))
        num = sp.Poly(sp.expand(h ** 2 - sp.Rational(alpha) * X - beta), X)
        k, rem = sp.div(num, sp.Poly(4 * g, X))
        assert rem.as_expr() == 0, "divisibility failed"
        k = k.as_expr()
        Delta = sp.expand(h ** 2 - 4 * g * k)
    P = {}
    for e, j in ((g, 2), (h, 1), (k, 0)):
        p = sp.Poly(sp.expand(e), X)
        for m, c in zip(p.monoms(), p.coeffs()):
            P[(int(m[0]), j)] = P.get((int(m[0]), j), F(0)) + F(str(c))
    return pk.clean(P), {"g": sp.sstr(g), "h": sp.sstr(h), "k": sp.sstr(k),
                         "Delta": sp.sstr(Delta)}


def se_instance(alpha, beta, c, roots, m, swap=False):
    """P = alpha x + beta + c prod (x - a_i)^(e_i) y^m  (or the (x,y) swap)."""
    B = sp.Rational(c) * sp.prod([(X - sp.Rational(a)) ** e for a, e in roots])
    A = sp.Rational(alpha) * X + sp.Rational(beta)
    P = {}
    pa = sp.Poly(sp.expand(A), X)
    for mm, cc in zip(pa.monoms(), pa.coeffs()):
        P[(int(mm[0]), 0)] = F(str(cc))
    pb = sp.Poly(sp.expand(B), X)
    for mm, cc in zip(pb.monoms(), pb.coeffs()):
        P[(int(mm[0]), m)] = P.get((int(mm[0]), m), F(0)) + F(str(cc))
    P = pk.clean(P)
    if swap:
        P = pk.clean({(j, i): v for (i, j), v in P.items()})
    return P


def shear(P, t_coeffs=None, s_coeffs=None):
    """Jacobian-1 shears: y -> y + t(x) then x -> x + s(y)."""
    Q = P
    if t_coeffs:
        t = {(i, 0): F(c) for i, c in enumerate(t_coeffs) if F(c) != 0}
        Q = pk.compose(Q, {(1, 0): F(1)}, pk.padd({(0, 1): F(1)}, t))
    if s_coeffs:
        s = {(0, i): F(c) for i, c in enumerate(s_coeffs) if F(c) != 0}
        Q = pk.compose(Q, pk.padd({(1, 0): F(1)}, s), {(0, 1): F(1)})
    return Q


# ------------------------------------------------------------------ screening
def he_screen(P):
    g = sum(sp.Rational(F(c).numerator, F(c).denominator) * X ** i
            for (i, j), c in P.items() if j == 2)
    h = sum(sp.Rational(F(c).numerator, F(c).denominator) * X ** i
            for (i, j), c in P.items() if j == 1)
    k = sum(sp.Rational(F(c).numerator, F(c).denominator) * X ** i
            for (i, j), c in P.items() if j == 0)
    d = R.he17(g, h, k)
    d["instrument"] = "HE17"
    d["periods_vanish"] = bool(d["residues_all_zero"] and d["genus"] == 0)
    d["verdict"] = ("PERIODS_VANISH" if d["periods_vanish"] else
                    ("RESIDUE_NONVANISHING" if not d["residues_all_zero"]
                     else "UNDECIDED_BY_RESIDUES_genus>=1"))
    return d


def se_screen(alpha, beta, c, roots, m):
    o = R.se17(sp.Rational(alpha) * X + sp.Rational(beta),
               [(sp.Rational(a), e) for a, e in roots], m, Bc=sp.Rational(c))
    eqs = [sp.simplify(e) for e in o["equations"]]
    allzero = all(e == 0 for e in eqs)
    o["instrument"] = "SE17"
    o["residues_all_zero"] = bool(allzero)
    o["genus"] = int(o["genus"])
    o["periods_vanish"] = bool(allzero and o["genus"] == 0)
    o["verdict"] = ("PERIODS_VANISH" if o["periods_vanish"] else
                    ("RESIDUE_NONVANISHING" if not allzero
                     else "UNDECIDED_BY_RESIDUES_genus>=1"))
    o["equations_evaluated"] = [sp.sstr(e) for e in eqs]
    return o


def numeric(P, cs=(1, -1)):
    try:
        import mono15
    except Exception as e:                                   # noqa: BLE001
        return {"error": str(e)}
    out = {}
    Pi = {k: (int(v) if F(v).denominator == 1 else F(v)) for k, v in P.items()}
    for cc in cs:
        try:
            r = mono15.screen_fibre(Pi, cc, budget=60.0)
            out[str(cc)] = {"rel": r["ls_residual"] / max(r["scale"], 1e-30),
                            "punct": r["n_punctures"], "genus": r.get("genus_sum")}
        except Exception as e:                               # noqa: BLE001
            out[str(cc)] = {"error": str(e)[:90]}
    return out


def certify_and_mate(P, screen, support_id, note, do_mate=True, do_num=True,
                     mate_cap=1400):
    rec = {"support": support_id, "hash": phash(P), "deg": pk.tdeg(P),
           "deg_y": pk.degy(P), "n_terms": len(P), "P": pk.to_str(P),
           "note": note, "screen": screen}
    t = time.time()
    u = CE.unimodular(P)
    rec["unimodular"] = u["verdict"]
    rec["bezout_method"] = u.get("method")
    rec["bezout_residual_terms"] = u.get("residual_terms")
    syv, st = CE.sy(P)
    rec["sy"] = syv
    rec["sy_nodes"] = st["nodes"]
    rec["fibre_witness"] = ("NON_COORDINATE (generic fibre: genus %s, %s punctures)"
                            % (screen.get("genus"), screen.get("n_punctures"))
                            if (screen.get("genus", 0) or 0) >= 1
                            or (screen.get("n_punctures") or 1) >= 2
                            else "no witness (genus 0, 1 puncture)")
    if do_num:
        rec["numeric_NUM_MONO"] = numeric(P)
    rec["survivor"] = bool(rec["unimodular"] == "UNIMODULAR_CERTIFIED"
                           and syv == "NON_COORDINATE"
                           and screen.get("periods_vanish"))
    if do_mate and rec["survivor"]:
        d = pk.tdeg(P)
        degs = (d, (3 * d + 1) // 2, 2 * d)
        rec["mate"] = MT.solve(P, max_cols=mate_cap, verbose=True, degs=degs)
    rec["secs"] = round(time.time() - t, 1)
    return rec
