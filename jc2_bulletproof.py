#!/usr/bin/env python3
"""jc2_bulletproof.py — bulletproof acceptance gate for candidate JC2 counterexample
pairs (P, Q) in Q[x,y]^2 (Track F deliverable).

CONTRACT
  - Default verdict: REJECT. A pair is ACCEPTED only if EVERY gate G0..G6 PASSes.
  - Errored gate = FAILED gate = REJECT.  Timeouts count as errors.
  - Every gate prints PASS/FAIL with concrete evidence.

GATES
  G0  exact rational coefficients: characteristic 0, no floats anywhere, all
      coefficients in Q (exact algebraic coefficients such as Q(sqrt(-3)) are
      recognized and handled exactly by the machinery, but G0 conservatively FAILS
      them: the campaign standard is Q).  Also validates the sympy<->dict converter
      by exact round-trip.
  G1  J(P,Q) is exactly a nonzero constant — decided by TWO independent
      implementations that share no arithmetic code:
        (a) sympy diff/expand on the expression form;
        (b) hand-rolled dict-of-monomials convolution over Fraction pairs.
      Both must agree (constant?, and on the exact value).  Disagreement = FAIL
      loudly (soundness alarm).
  G2  non-dividing total degrees.  CONSERVATIVE DIRECTION, on purpose: by
      Jung–van der Kulk every automorphism of C^2 is tame, and the classical
      minimal-counterexample reduction says: if (P,Q) is Keller and deg P | deg Q
      (or vice versa), then G4's leading-form proportionality lets one subtract
      zeta*P^(d2/d1) from Q (zeta a root of the proportionality constant, over C)
      and strictly lower the degree while staying Keller.  Hence a MINIMAL
      counterexample has non-dividing degrees.  The gate therefore rejects any
      dividing-degree pair.  This can reject a genuine but non-minimal
      counterexample — that is the safe direction for a gate whose false ACCEPT
      is the catastrophe; a candidate rejected only by G2 should be degree-reduced
      and resubmitted.
  G3  exact non-injectivity evidence.  Mode GENERIC: R = Res_y(P-p, Q-q) over
      Q(p,q)[x] (and the x<->y swap).  After stripping the (p,q)-free content
      (which absorbs all leading-coefficient artifacts; if a factor (x-x0) of R
      persists for ALL (p,q) it lies in the content), >= 2 distinct generic roots
      each extending to a fiber point certifies generic fiber cardinality >= 2.
      If instead the resultant degrees certify fiber <= 1, that is a definitive
      injectivity witness: FAIL.  Mode SPECIFIC (fallback): exact fiber counts at
      rational targets via resultants + squarefree factorization + exact
      back-substitution (gcd over Q[x]/(f) for each irreducible factor f).  The
      mode used is recorded in the evidence.  No evidence within budget = FAIL.
  G4  leading forms: Pbar^{d2} = c * Qbar^{d1} exactly for some nonzero constant c
      (necessary for any Keller pair with d1,d2 >= 2: J(Pbar,Qbar) = 0 forces the
      top forms to be proportional powers of a common form).  Checked exactly:
      single-monomial fast path, else exact evaluation at d1*d2+1 points on the
      line x=1 (a homogeneous form of degree N vanishing at N+1 distinct points of
      that line is identically zero).
  G5  sanity: P, Q nonconstant; each genuinely bivariate (a Keller counterexample
      with a univariate member is impossible: P in Q[x] and J = P'(x) Q_y = const
      forces P affine — conservative gate, commented); J not identically 0.
  G6  multi-prime re-check of bracket constancy: 3 primes p = 1 (mod 3) (so that
      sqrt(-3) exists mod p, matching the campaign's field conventions), skipping
      any prime dividing a coefficient denominator (and the numerator/denominator
      of the claimed constant).  J mod p must be the constant c mod p.  Mod-p
      constancy is necessary, never sufficient — G6 is a re-check, it can only
      veto.

USAGE
  python3 jc2_bulletproof.py --battery [--md OUT.md]   run the validation battery
  As a library:  from jc2_bulletproof import bulletproof_gate
                 verdict, results = bulletproof_gate(P, Q, x, y)
"""

import signal
import sys
import time
import traceback
from contextlib import contextmanager
from fractions import Fraction as F

import sympy as sp

# ============================================================================
# 0.  Exact coefficient arithmetic over Q(sqrt(-3)): pairs (a, b) = a + b*sqrt(-3)
#     (pure-Q polynomials simply have b = 0 everywhere)
# ============================================================================

Q3_ZERO = (F(0), F(0))
Q3_ONE = (F(1), F(0))


def q3_add(u, v):
    return (u[0] + v[0], u[1] + v[1])


def q3_sub(u, v):
    return (u[0] - v[0], u[1] - v[1])


def q3_mul(u, v):
    # (a + b s)(c + d s), s^2 = -3
    return (u[0] * v[0] - 3 * u[1] * v[1], u[0] * v[1] + u[1] * v[0])


def q3_scal(k, u):
    return (k * u[0], k * u[1])


def q3_neg(u):
    return (-u[0], -u[1])


def q3_div(u, v):
    # u / v = u * conj(v) / (c^2 + 3 d^2)
    n = v[0] * v[0] + 3 * v[1] * v[1]
    if n == 0:
        raise ZeroDivisionError("division by zero in Q(sqrt(-3))")
    w = q3_mul(u, (v[0], -v[1]))
    return (w[0] / n, w[1] / n)


def q3_pow(u, e):
    out = Q3_ONE
    base = u
    while e:
        if e & 1:
            out = q3_mul(out, base)
        base = q3_mul(base, base)
        e >>= 1
    return out


def q3_str(u):
    if u[1] == 0:
        return str(u[0])
    return f"({u[0]} + {u[1]}*sqrt(-3))"


# ============================================================================
# 1.  Dict polynomials: {(i, j): q3coeff}, zero coefficients never stored
# ============================================================================


def pd_clean(d):
    return {k: c for k, c in d.items() if c != Q3_ZERO}


def pd_add(a, b):
    out = dict(a)
    for k, c in b.items():
        out[k] = q3_add(out.get(k, Q3_ZERO), c)
    return pd_clean(out)


def pd_sub(a, b):
    out = dict(a)
    for k, c in b.items():
        out[k] = q3_sub(out.get(k, Q3_ZERO), c)
    return pd_clean(out)


def pd_mul(a, b):
    out = {}
    for (i1, j1), c1 in a.items():
        for (i2, j2), c2 in b.items():
            k = (i1 + i2, j1 + j2)
            out[k] = q3_add(out.get(k, Q3_ZERO), q3_mul(c1, c2))
    return pd_clean(out)


def pd_diff_x(a):
    return pd_clean({(i - 1, j): q3_scal(F(i), c) for (i, j), c in a.items() if i > 0})


def pd_diff_y(a):
    return pd_clean({(i, j - 1): q3_scal(F(j), c) for (i, j), c in a.items() if j > 0})


def pd_total_deg(a):
    return max((i + j for (i, j) in a), default=-1)


def pd_leading_form(a):
    d = pd_total_deg(a)
    return {k: c for k, c in a.items() if k[0] + k[1] == d}, d


def pd_pow(a, e):
    out = {(0, 0): Q3_ONE}
    base = dict(a)
    while e:
        if e & 1:
            out = pd_mul(out, base)
        base = pd_mul(base, base)
        e >>= 1
    return out


def bracket_dict(Pd, Qd):
    """Hand-rolled Jacobian bracket: convolution arithmetic only, no sympy."""
    return pd_sub(pd_mul(pd_diff_x(Pd), pd_diff_y(Qd)),
                  pd_mul(pd_diff_y(Pd), pd_diff_x(Qd)))


# ============================================================================
# 2.  sympy <-> dict conversion (input plumbing; validated by round-trip in G0)
# ============================================================================

class ExactnessError(Exception):
    pass


def parse_q3(c):
    """Exact sympy number -> (Fraction, Fraction) = a + b*sqrt(-3), or raise."""
    c = sp.expand(c)
    if c.has(sp.Float):
        raise ExactnessError(f"float coefficient: {c}")
    re_, im_ = c.as_real_imag()
    re_ = sp.simplify(re_)
    bpart = sp.simplify(im_ / sp.sqrt(3))
    if not (re_.is_Rational and bpart.is_Rational):
        raise ExactnessError(f"coefficient not in Q(sqrt(-3)): {c}")
    return (F(int(re_.p), int(re_.q)), F(int(bpart.p), int(bpart.q)))


def to_dict(expr, x, y):
    expr = sp.expand(expr)
    poly = sp.Poly(expr, x, y, domain='EX')
    out = {}
    for (i, j), c in poly.terms():
        v = parse_q3(c)
        if v != Q3_ZERO:
            out[(int(i), int(j))] = v
    return out


def from_dict(d, x, y):
    s3 = sp.I * sp.sqrt(3)
    return sp.expand(sp.Add(*[
        (sp.Rational(c[0].numerator, c[0].denominator)
         + sp.Rational(c[1].numerator, c[1].denominator) * s3) * x**i * y**j
        for (i, j), c in d.items()]))


# ============================================================================
# 3.  Timeout machinery (errored gate = rejected gate; timeout = error)
# ============================================================================

class GateTimeout(Exception):
    pass


@contextmanager
def time_limit(seconds):
    seconds = max(1, int(seconds))   # alarm(0) would DISABLE the timeout

    def handler(signum, frame):
        raise GateTimeout(f"gate exceeded {seconds}s budget")
    old = signal.signal(signal.SIGALRM, handler)
    signal.alarm(seconds)
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old)


# ============================================================================
# 4.  The gates.  Each returns (passed: bool, evidence: [str]).
# ============================================================================


def gate0_exact_rational(ctx):
    ev = []
    floats = [a for a in sp.preorder_traversal(ctx['P']) if isinstance(a, sp.Float)]
    floats += [a for a in sp.preorder_traversal(ctx['Q']) if isinstance(a, sp.Float)]
    if floats:
        ev.append(f"FLOAT coefficients found: {floats[:3]} ... -> not exact")
        return False, ev
    ev.append("no floating-point atoms in either polynomial")
    Pd, Qd = ctx['Pd'], ctx['Qd']          # raises earlier if not exact
    # converter round-trip validation (protects every dict-based gate)
    rtP = sp.expand(from_dict(Pd, ctx['x'], ctx['y']) - ctx['P'])
    rtQ = sp.expand(from_dict(Qd, ctx['x'], ctx['y']) - ctx['Q'])
    if rtP != 0 or rtQ != 0:
        ev.append("sympy<->dict round-trip FAILED — converter bug, all bets off")
        return False, ev
    ev.append("sympy<->dict round-trip exact for both P and Q")
    irr = [(k, c) for k, c in list(Pd.items()) + list(Qd.items()) if c[1] != 0]
    if irr:
        ev.append(f"{len(irr)} coefficients lie in Q(sqrt(-3)) \\ Q "
                  f"(exact, but NOT rational; e.g. monomial {irr[0][0]} has "
                  f"coefficient {q3_str(irr[0][1])})")
        ev.append("campaign standard demands coefficients in Q -> conservative FAIL")
        return False, ev
    ev.append("all coefficients are exact rationals (char 0)")
    return True, ev


def gate1_jacobian_constant(ctx):
    ev = []
    x, y = ctx['x'], ctx['y']
    # --- implementation (a): sympy diff/expand on the expression form ---
    Ja = sp.expand(sp.diff(ctx['P'], x) * sp.diff(ctx['Q'], y)
                   - sp.diff(ctx['P'], y) * sp.diff(ctx['Q'], x))
    a_const = not (Ja.has(x) or Ja.has(y))
    # --- implementation (b): hand-rolled Fraction dict convolution ---
    Jb = bracket_dict(ctx['Pd'], ctx['Qd'])
    ctx['J_dict'] = Jb
    b_const = set(Jb) <= {(0, 0)}
    if a_const != b_const:
        ev.append(f"SOUNDNESS ALARM: implementations DISAGREE on constancy "
                  f"(sympy: {a_const}, dict: {b_const})")
        return False, ev
    if not a_const:
        n_terms = len(Jb)
        sample = sorted(Jb)[:4]
        ev.append(f"both implementations agree: J(P,Q) is NOT constant "
                  f"({n_terms} monomial(s))")
        for k in sample:
            ev.append(f"  J term: {q3_str(Jb[k])} * x^{k[0]} * y^{k[1]}")
        return False, ev
    # both say constant; compare exact values
    ca = parse_q3(Ja)
    cb = Jb.get((0, 0), Q3_ZERO)
    if ca != cb:
        ev.append(f"SOUNDNESS ALARM: constant values differ "
                  f"(sympy: {q3_str(ca)}, dict: {q3_str(cb)})")
        return False, ev
    if cb == Q3_ZERO:
        ev.append("both implementations agree: J(P,Q) == 0 identically "
                  "(degenerate, not Keller)")
        return False, ev
    ctx['J_const'] = cb
    ev.append(f"both independent implementations agree: J(P,Q) = {q3_str(cb)} "
              f"(nonzero constant)")
    return True, ev


def gate2_nondividing_degrees(ctx):
    # CONSERVATIVE (see module docstring): rejects dividing degrees because a
    # minimal counterexample must have non-dividing degrees (JvdK + leading-form
    # reduction).  May reject a non-minimal true counterexample: safe direction.
    ev = []
    d1 = pd_total_deg(ctx['Pd'])
    d2 = pd_total_deg(ctx['Qd'])
    ev.append(f"total degrees: deg P = {d1}, deg Q = {d2}")
    if d1 < 1 or d2 < 1:
        ev.append("a degree is < 1 (constant member) -> FAIL")
        return False, ev
    if d1 % d2 == 0 or d2 % d1 == 0:
        ev.append("degrees divide -> Jung-van der Kulk reduction applies; a "
                  "minimal counterexample cannot look like this -> FAIL")
        return False, ev
    ev.append("neither degree divides the other -> PASS")
    return True, ev


def _distinct_fiber_count_at(Pex, Qex, x, y, p0, q0):
    """Exact number of distinct complex solutions of P = p0, Q = q0.

    Resultant + squarefree factorization + exact back-substitution:
    for each irreducible factor f(x) of the squarefree part of Res_y, adjoin a
    root alpha = RootOf(f), compute gcd of P-p0, Q-q0 in Q(alpha)[y], and count
    distinct y-roots (degree of the gcd's squarefree part).  Total is
    sum_f deg(f) * (#distinct y over each root of f) — Galois conjugation makes
    the per-root count constant across the roots of one irreducible f.
    Returns (count, notes) or raises.
    """
    A = sp.expand(Pex - p0)
    B = sp.expand(Qex - q0)
    R = sp.resultant(A, B, y)
    notes = []
    if R == 0:
        return None, ["Res_y == 0: common component through this target "
                      "(degenerate fiber)"]
    Rp = sp.Poly(R, x)
    if Rp.degree() == 0:
        return 0, [f"Res_y is a nonzero constant: empty fiber over ({p0},{q0})"]
    sf = sp.quo(Rp, sp.gcd(Rp, Rp.diff(x)))
    total = 0
    for f, _m in sp.factor_list(sf.as_expr(), x)[1]:
        fp = sp.Poly(f, x)
        if fp.degree() == 0:
            continue
        alpha = sp.RootOf(fp, 0)
        Ay = sp.Poly(sp.expand(A.subs(x, alpha)), y, extension=True)
        By = sp.Poly(sp.expand(B.subs(x, alpha)), y, extension=True)
        if Ay.degree() < 0 or By.degree() < 0:   # one vanished identically
            notes.append(f"factor {f}: a member vanishes identically at alpha "
                         f"(positive-dimensional slice) — skipped")
            continue
        g = sp.gcd(Ay, By)
        if g.degree() <= 0:
            notes.append(f"factor {f}: no common y-root (leading-coefficient "
                         f"artifact) — contributes 0")
            continue
        gsf = sp.quo(g, sp.gcd(g, g.diff(y)))
        cnt = fp.degree() * gsf.degree()
        notes.append(f"factor {f} (deg {fp.degree()}): {gsf.degree()} distinct "
                     f"y-value(s) per root -> {cnt} point(s)")
        total += cnt
    return total, notes


def gate3_noninjectivity(ctx):
    ev = []
    x, y = ctx['x'], ctx['y']
    Pex, Qex = ctx['P'], ctx['Q']
    bud_gen = ctx['budgets'].get('G3_generic', 60)
    bud_spec = ctx['budgets'].get('G3_specific', 60)
    p, q = sp.symbols('__jc2_p __jc2_q')

    # ---------- MODE GENERIC: resultants over Q(p,q) ----------
    generic_result = None      # (passfail or None, evidence)
    try:
        with time_limit(bud_gen):
            A = Pex - p
            B = Qex - q
            info = {}
            for (u, v, tag) in ((y, x, 'Res_y -> Q(p,q)[x]'),
                                (x, y, 'Res_x -> Q(p,q)[y]')):
                R = sp.expand(sp.resultant(A, B, u))
                if R == 0:
                    info[tag] = ('ZERO', 0, False)
                    continue
                Rv = sp.Poly(R, v)         # coeffs in Q[p,q]
                degR = Rv.degree()
                # strip (p,q)-free content: gcd of coefficients as polys in v?
                # content in Q[v]: collect R as poly in (p,q), gcd of coeffs.
                Rpq = sp.Poly(R, p, q)
                cont = 0
                for c in Rpq.coeffs():
                    cont = sp.gcd(cont, c)
                Rstar = sp.cancel(R / cont)
                Rsv = sp.Poly(Rstar, v)
                degRs = Rsv.degree()
                gg = sp.gcd(Rsv, Rsv.diff(v))
                sq_free = (sp.Poly(gg, v).degree() == 0) if gg != 0 else False
                info[tag] = (degR, degRs, sq_free)
            ev.append(f"mode GENERIC: {info}")
            # positive evidence: content-stripped, squarefree, degree >= 2
            for tag, dat in info.items():
                if dat[0] == 'ZERO':
                    continue
                degR, degRs, sq_free = dat
                if degRs >= 2 and sq_free:
                    ev.append(f"  {tag}: content-stripped degree {degRs} >= 2, "
                              f"squarefree over Q(p,q) -> generic fiber has >= "
                              f"{degRs} distinct coordinate values, each "
                              f"extending to a fiber point (artifact roots live "
                              f"in the stripped content) -> non-injective")
                    generic_result = (True, 'GENERIC')
                    break
            if generic_result is None:
                # definitive injectivity witness?
                dy_min = min(sp.Poly(A, y).degree(), sp.Poly(B, y).degree())
                dx_min = min(sp.Poly(A, x).degree(), sp.Poly(B, x).degree())
                ry = info.get('Res_y -> Q(p,q)[x]', (None,))[0]
                rx = info.get('Res_x -> Q(p,q)[y]', (None,))[0]
                if (isinstance(ry, int) and ry <= 1 and dy_min <= 1) or \
                   (isinstance(rx, int) and rx <= 1 and dx_min <= 1):
                    ev.append("  definitive: <= 1 coordinate value on the "
                              "generic fiber and <= 1 partner value (min "
                              "codegree <= 1) -> generic fiber cardinality <= 1 "
                              "-> map is generically injective, NOT a "
                              "counterexample")
                    generic_result = (False, 'GENERIC')
    except GateTimeout as e:
        ev.append(f"mode GENERIC infeasible: {e}")
    except Exception as e:
        ev.append(f"mode GENERIC errored: {type(e).__name__}: {e}")

    if generic_result is not None:
        ok = generic_result[0]
        ev.append(f"mode used: GENERIC (resultants over Q(p,q))")
        return ok, ev

    # ---------- MODE SPECIFIC: exact fiber counts at rational targets ----------
    targets = [(sp.Integer(3), sp.Integer(5)), (sp.Integer(7), sp.Integer(-2)),
               (sp.Rational(-4), sp.Integer(9))]
    best = 0
    try:
        with time_limit(bud_spec):
            for (p0, q0) in targets:
                cnt, notes = _distinct_fiber_count_at(Pex, Qex, x, y, p0, q0)
                ev.append(f"mode SPECIFIC target ({p0},{q0}): "
                          f"{'degenerate' if cnt is None else f'{cnt} distinct point(s)'}")
                for n in notes:
                    ev.append(f"    {n}")
                if cnt is not None:
                    best = max(best, cnt)
                if best >= 2:
                    break
    except GateTimeout as e:
        ev.append(f"mode SPECIFIC infeasible: {e}")
    except Exception as e:
        ev.append(f"mode SPECIFIC errored: {type(e).__name__}: {e}")

    if best >= 2:
        ev.append("mode used: SPECIFIC — exact rational-target fiber count >= 2 "
                  "(evidence of non-injectivity; for an etale Keller candidate "
                  "the specific count equals the generic count)")
        return True, ev
    ev.append("no exact non-injectivity evidence obtained within budget -> "
              "default FAIL (mode: NONE)")
    return False, ev


def gate4_leading_forms(ctx):
    ev = []
    Pd, Qd = ctx['Pd'], ctx['Qd']
    LP, d1 = pd_leading_form(Pd)
    LQ, d2 = pd_leading_form(Qd)
    ev.append(f"leading forms: deg {d1} ({len(LP)} term(s)), "
              f"deg {d2} ({len(LQ)} term(s))")
    if d1 < 1 or d2 < 1:
        ev.append("constant member -> FAIL")
        return False, ev
    # fast path: both single monomials
    if len(LP) == 1 and len(LQ) == 1:
        (iP, jP), cP = next(iter(LP.items()))
        (iQ, jQ), cQ = next(iter(LQ.items()))
        if (iP * d2, jP * d2) != (iQ * d1, jQ * d1):
            ev.append(f"single-monomial forms with mismatched exponents: "
                      f"({iP},{jP})*{d2} != ({iQ},{jQ})*{d1} -> FAIL")
            return False, ev
        c = q3_div(q3_pow(cP, d2), q3_pow(cQ, d1))
        ev.append(f"single-monomial fast path: Pbar^{d2} = c * Qbar^{d1} with "
                  f"c = {q3_str(c)} -> PASS")
        return True, ev
    # general path: exact evaluation on the line x = 1 at N+1 points
    N = d1 * d2

    def eval_form(L, t):    # value of form at (x, y) = (1, t), exact q3
        acc = Q3_ZERO
        for (i, j), cc in L.items():
            acc = q3_add(acc, q3_mul(cc, (F(t)**j, F(0))))
        return acc

    c = None
    t_used = None
    for t in range(0, N + 2):
        vQ = eval_form(LQ, t)
        if vQ != Q3_ZERO:
            vP = eval_form(LP, t)
            c = q3_div(q3_pow(vP, d2), q3_pow(vQ, d1))
            t_used = t
            break
    if c is None or c == Q3_ZERO:
        ev.append("no nonzero proportionality constant exists "
                  f"(c = {None if c is None else q3_str(c)}) -> FAIL")
        return False, ev
    for t in range(0, N + 1):
        lhs = q3_pow(eval_form(LP, t), d2)
        rhs = q3_mul(c, q3_pow(eval_form(LQ, t), d1))
        if lhs != rhs:
            ev.append(f"identity Pbar^{d2} = c*Qbar^{d1} FAILS at (1,{t}) "
                      f"(c fitted at t = {t_used}: {q3_str(c)}) -> FAIL")
            return False, ev
    ev.append(f"Pbar^{d2} = c * Qbar^{d1} verified exactly at {N + 1} points of "
              f"the line x = 1 (degree-{N} homogeneous identity => identical), "
              f"c = {q3_str(c)} -> PASS")
    return True, ev


def gate5_sanity(ctx):
    # Conservative bivariate requirement: if P (or Q) were univariate, say
    # P in Q[x], then J = P'(x)*Q_y must be the constant c, forcing P' | c in
    # Q[x], i.e. P affine — impossible for a counterexample surviving G2.
    # Requiring genuine bivariateness of both members is therefore sound for
    # candidates and safely conservative in general.
    ev = []
    Pd, Qd = ctx['Pd'], ctx['Qd']
    ok = True
    for nm, d in (('P', Pd), ('Q', Qd)):
        if pd_total_deg(d) < 1:
            ev.append(f"{nm} is constant -> FAIL")
            ok = False
            continue
        usesx = any(i > 0 for (i, j) in d)
        usesy = any(j > 0 for (i, j) in d)
        if not (usesx and usesy):
            ev.append(f"{nm} is univariate (uses x: {usesx}, uses y: {usesy}) "
                      f"-> FAIL (counterexample members must be genuinely "
                      f"bivariate)")
            ok = False
        else:
            ev.append(f"{nm}: nonconstant and genuinely bivariate")
    Jd = ctx.get('J_dict')
    if Jd is None:
        Jd = bracket_dict(Pd, Qd)
        ctx['J_dict'] = Jd
    if not Jd:
        ev.append("J(P,Q) == 0 identically -> FAIL")
        ok = False
    else:
        ev.append("J(P,Q) is not identically zero")
    return ok, ev


def _primes_1mod3(start, bad_divisors, count=3):
    out = []
    p = start
    while len(out) < count and p > 3:
        if sp.isprime(p) and p % 3 == 1 and all(d % p != 0 for d in bad_divisors):
            out.append(p)
        p -= 1
    return out


def _sqrt_m3_mod(p):
    target = (-3) % p
    # p = 1 (mod 3) guarantees existence; 16-bit loop is fine
    for t in range(1, p):
        if (t * t) % p == target:
            return t
    raise ValueError(f"no sqrt(-3) mod {p} (is p = 1 mod 3?)")


def gate6_multiprime(ctx):
    ev = []
    Pd, Qd = ctx['Pd'], ctx['Qd']
    dens = set()
    nums = set()
    for d in (Pd, Qd):
        for c in d.values():
            dens.add(c[0].denominator)
            dens.add(c[1].denominator)
    cQ = ctx.get('J_const')
    if cQ is not None:
        dens.add(cQ[0].denominator)
        dens.add(cQ[1].denominator)
        if cQ[0] != 0:
            nums.add(abs(cQ[0].numerator))
        if cQ[1] != 0:
            nums.add(abs(cQ[1].numerator))
    bad = {d for d in dens if d > 1} | nums
    primes = _primes_1mod3(65521, bad, count=3)
    if len(primes) < 3:
        ev.append("could not find 3 admissible primes -> FAIL")
        return False, ev
    ev.append(f"primes used (all = 1 mod 3, skipping denominator/constant "
              f"divisors): {primes}")
    ok = True
    for p in primes:
        s3 = _sqrt_m3_mod(p)

        def red(c):
            a = c[0].numerator * pow(c[0].denominator, -1, p) % p
            b = c[1].numerator * pow(c[1].denominator, -1, p) % p
            return (a + b * s3) % p

        Pp = {k: red(c) for k, c in Pd.items()}
        Qp = {k: red(c) for k, c in Qd.items()}

        def dmul(A, B):
            out = {}
            for (i1, j1), c1 in A.items():
                for (i2, j2), c2 in B.items():
                    k = (i1 + i2, j1 + j2)
                    out[k] = (out.get(k, 0) + c1 * c2) % p
            return {k: c for k, c in out.items() if c}

        def ddx(A):
            return {(i - 1, j): (i * c) % p for (i, j), c in A.items()
                    if i > 0 and (i * c) % p}

        def ddy(A):
            return {(i, j - 1): (j * c) % p for (i, j), c in A.items()
                    if j > 0 and (j * c) % p}

        J1 = dmul(ddx(Pp), ddy(Qp))
        J2 = dmul(ddy(Pp), ddx(Qp))
        Jp = dict(J1)
        for k, c in J2.items():
            Jp[k] = (Jp.get(k, 0) - c) % p
        Jp = {k: c for k, c in Jp.items() if c}
        if set(Jp) - {(0, 0)}:
            ev.append(f"p = {p} (sqrt(-3) = {s3}): J mod p NONCONSTANT "
                      f"({len(Jp)} monomials, e.g. exponent "
                      f"{sorted(set(Jp) - {(0, 0)})[0]}) -> FAIL")
            ok = False
            continue
        cp = Jp.get((0, 0), 0)
        if cQ is not None:
            expect = ((cQ[0].numerator * pow(cQ[0].denominator, -1, p)
                       + cQ[1].numerator * pow(cQ[1].denominator, -1, p) * s3) % p)
            match = (cp == expect)
            ev.append(f"p = {p}: J mod p == {cp} (constant); expected "
                      f"c mod p = {expect}: {'MATCH' if match else 'MISMATCH'}")
            ok = ok and match and cp != 0
        else:
            ev.append(f"p = {p}: J mod p == {cp} (constant mod p; no exact "
                      f"constant from G1 to compare against)")
            ok = ok and cp != 0
    if ok:
        ev.append("bracket constancy corroborated at all 3 primes "
                  "(necessary-condition re-check only, never sufficient)")
    return ok, ev


# ============================================================================
# 5.  Driver
# ============================================================================

GATES = [
    ("G0", "exact rational coefficients", gate0_exact_rational),
    ("G1", "Jacobian exactly a nonzero constant (2 independent impls)",
     gate1_jacobian_constant),
    ("G2", "non-dividing degrees (Jung-van der Kulk, conservative)",
     gate2_nondividing_degrees),
    ("G3", "exact non-injectivity evidence", gate3_noninjectivity),
    ("G4", "leading forms Pbar^d2 = c*Qbar^d1", gate4_leading_forms),
    ("G5", "nonconstant / bivariate / J not identically 0", gate5_sanity),
    ("G6", "multi-prime bracket constancy re-check", gate6_multiprime),
]


def bulletproof_gate(P, Q, x, y, budgets=None, log=print):
    """Run all gates.  Returns (verdict_str, results) where verdict is
    'ACCEPT' only if every gate passed; results maps gate id ->
    (passed, evidence_list, elapsed_seconds)."""
    budgets = dict(budgets or {})
    default_budget = budgets.get('default', 120)
    ctx = {'P': sp.expand(P), 'Q': sp.expand(Q), 'x': x, 'y': y,
           'budgets': budgets}
    # exact dict forms (shared input plumbing, validated by G0's round-trip)
    try:
        ctx['Pd'] = to_dict(ctx['P'], x, y)
        ctx['Qd'] = to_dict(ctx['Q'], x, y)
    except Exception as e:
        ctx['Pd'] = ctx['Qd'] = None
        ctx['dict_error'] = f"{type(e).__name__}: {e}"

    results = {}
    for gid, gname, fn in GATES:
        t0 = time.time()
        try:
            if ctx['Pd'] is None:
                raise ExactnessError(
                    f"no exact dict representation: {ctx['dict_error']}")
            if fn is gate3_noninjectivity:
                # G3 manages its own per-mode alarms; signal.alarm does not
                # nest, so no outer alarm here.
                passed, ev = fn(ctx)
            else:
                with time_limit(budgets.get(gid, default_budget)):
                    passed, ev = fn(ctx)
        except Exception as e:
            passed = False
            ev = [f"GATE ERRORED -> FAIL: {type(e).__name__}: {e}"]
            if not isinstance(e, (GateTimeout, ExactnessError)):
                ev.append("  " + traceback.format_exc(limit=2).strip()
                          .replace("\n", " | "))
        elapsed = time.time() - t0
        results[gid] = (passed, ev, elapsed)
        log(f"  [{'PASS' if passed else 'FAIL'}] {gid} {gname} "
            f"({elapsed:.1f}s)")
        for line in ev:
            log(f"        {line}")
    verdict = 'ACCEPT' if all(r[0] for r in results.values()) else 'REJECT'
    failed = [g for g, r in results.items() if not r[0]]
    log(f"  VERDICT: {verdict}"
        + (f"  (failed: {', '.join(failed)})" if failed else ""))
    return verdict, results


# ============================================================================
# 6.  Validation battery (all pairs are KNOWN NON-COUNTEREXAMPLES: must REJECT)
# ============================================================================


def build_nearmiss():
    """Session-7 near-miss pair, built from the repo report's certified
    (and paper-corrected) Belyi coefficients over Q(sqrt(-3)):
        y1 = x1^3 x2^8 p(v^3/x2),  y2 = x1^2 x2^5 v r(v^3/x2),  v = x1 x2^3 - 1.
    Its Jacobian is -h0 * x1^4 * x2^12 (h0 = (1664 - 832 sqrt(-3))/3): G1 must
    reject."""
    w, x1, x2 = sp.symbols('w x1 x2')
    s = sp.I * sp.sqrt(3)
    R = sp.Rational
    p = (w**8 + (2 + 8*s)*w**7 + (R(-233, 3) + R(50, 3)*s)*w**6
         + (R(-4600, 27) - R(376, 3)*s)*w**5 + (R(835, 3) - R(890, 3)*s)*w**4
         + (R(2420, 3) + R(22, 3)*s)*w**3 + (R(1043, 3) + 336*s)*w**2
         + (-118 + 158*s)*w + (-28 + 4*s))
    r = (w**5 + (R(4, 3) + R(16, 3)*s)*w**4 + (R(-278, 9) + R(68, 9)*s)*w**3
         + (R(-140, 3) - 24*s)*w**2 + (R(35, 3) - R(112, 3)*s)*w
         + R(68, 3) - R(20, 3)*s)
    v = x1 * x2**3 - 1
    y1 = sp.expand(x1**3 * x2**8 * p.subs(w, v**3 / x2))
    y2 = sp.expand(x1**2 * x2**5 * v * r.subs(w, v**3 / x2))
    return y1, y2, x1, x2


def battery(md_path=None):
    x, y = sp.symbols('x y')
    pairs = []
    pairs.append(("V1: (y^3+x, y^2+x)", y**3 + x, y**2 + x, x, y, {},
                  "J = 2y - 3y^2 nonconstant; degrees (3,2) non-dividing; "
                  "genuinely 3:1 -> only G1/G6 can reject it"))
    pairs.append(("V2: (y^2+x, y)", y**2 + x, y, x, y, {},
                  "a Keller pair (J = 1) that IS an automorphism-piece: "
                  "G2/G3/G5 must reject"))
    pairs.append(("V3: (x+y^2, y)", x + y**2, y, x, y, {},
                  "same pair written differently (argument-order robustness)"))
    pairs.append(("V4: (x, y+x^2)", x, y + x**2, x, y, {},
                  "triangular automorphism, J = 1: G2/G3/G5 must reject"))
    y1, y2, x1, x2 = build_nearmiss()
    pairs.append(("V5: Session-7 near-miss (99,66) over Q(sqrt(-3))",
                  y1, y2, x1, x2,
                  {'G3_generic': 20, 'G3_specific': 20, 'G3': 60,
                   'default': 300},
                  "J = -h0*x1^4*x2^12: G1 MUST reject; G0 rejects "
                  "non-rational (exact) coefficients"))
    pairs.append(("V6: (x+(y+x^2)^2, y+x^2) [extra control]",
                  x + (y + x**2)**2, y + x**2, x, y, {},
                  "composed tame automorphism, J = 1, both members bivariate: "
                  "only G2/G3 can reject it"))

    lines = []
    all_reject = True
    summary = []
    for name, P, Q, vx, vy, budgets, why in pairs:
        print(f"\n=== {name} ===")
        print(f"  battery intent: {why}")
        buf = []
        verdict, results = bulletproof_gate(P, Q, vx, vy, budgets=budgets,
                                            log=lambda s: (print(s),
                                                           buf.append(s)))
        all_reject &= (verdict == 'REJECT')
        failed = [g for g, r in results.items() if not r[0]]
        passed = [g for g, r in results.items() if r[0]]
        summary.append((name, verdict, failed, passed, why))
        lines.append((name, why, verdict, results, buf))

    # ---- robustness demos (recorded in the md): G3 SPECIFIC path + errors ----
    rob = []
    print("\n=== robustness demos ===")
    rob.append("G3 SPECIFIC-mode path exercised directly "
               "(the battery pairs all decided in GENERIC mode):")
    for (name, P, Q) in [("V1", y**3 + x, y**2 + x),
                         ("V6", x + (y + x**2)**2, y + x**2)]:
        for (p0, q0) in [(sp.Integer(3), sp.Integer(5))]:
            cnt, notes = _distinct_fiber_count_at(P, Q, x, y, p0, q0)
            rob.append(f"  {name} at target ({p0},{q0}): {cnt} distinct "
                       f"point(s) — {'non-injectivity evidence' if cnt and cnt >= 2 else 'no evidence (injective here)'}")
            for n in notes:
                rob.append(f"      {n}")
    rob.append("errored-input robustness (default REJECT):")
    for (nm, P, Q) in [("float coefficient (0.5*x^2+y, x+y^3)",
                        0.5 * x**2 + y, x + y**3),
                       ("non-polynomial (sin(x)+y, x+y)",
                        sp.sin(x) + y, x + y)]:
        v, _ = bulletproof_gate(P, Q, x, y, log=lambda s: None)
        rob.append(f"  {nm}: every gate errors -> verdict {v}")
        all_reject &= (v == 'REJECT')
    for line in rob:
        print(line)

    print("\n================ BATTERY SUMMARY ================")
    for name, verdict, failed, passed, _ in summary:
        print(f"  {verdict:6s} {name}  rejected-by: {', '.join(failed) or '-'}")
    print(f"ALL NON-COUNTEREXAMPLES REJECTED: {all_reject}")

    if md_path:
        write_md(md_path, summary, lines, rob)
        print(f"validation log written: {md_path}")
    return all_reject


def write_md(path, summary, lines, rob=()):
    out = []
    out.append("# jc2_bulletproof.py — gate validation log\n")
    out.append(f"Generated by `python3 jc2_bulletproof.py --battery --md {path}` "
               f"on {time.strftime('%Y-%m-%d %H:%M UTC', time.gmtime())}.\n")
    out.append("Contract: default REJECT; any errored/timed-out gate = REJECT; "
               "ACCEPT requires all of G0..G6 to PASS. Every pair below is a "
               "known non-counterexample, so the required outcome is REJECT "
               "for every one of them.\n")
    out.append("## Battery summary\n")
    out.append("| Pair | Verdict | Rejecting gate(s) | Passing gate(s) |")
    out.append("|---|---|---|---|")
    ok = True
    for name, verdict, failed, passed, _ in summary:
        ok &= verdict == 'REJECT'
        out.append(f"| {name} | **{verdict}** | {', '.join(failed) or '-'} | "
                   f"{', '.join(passed) or '-'} |")
    out.append("")
    out.append(f"**All non-counterexamples rejected: {ok}**\n")
    out.append("## Why each pair is in the battery, and full per-gate evidence\n")
    for name, why, verdict, results, buf in lines:
        out.append(f"### {name}\n")
        out.append(f"*Battery intent:* {why}\n")
        out.append("```text")
        out.extend(buf)
        out.append("```\n")
    if rob:
        out.append("## Robustness demos\n")
        out.append("```text")
        out.extend(rob)
        out.append("```\n")
    out.append("## Notes\n")
    out.append("- G1 is the load-bearing gate: two implementations that share no "
               "arithmetic code (sympy diff/expand vs hand-rolled Fraction-pair "
               "dict convolution) must agree exactly. On the Session-7 near-miss "
               "both agree the Jacobian is the single monomial "
               "-h0*x1^4*x2^12 (h0 = (1664 - 832 sqrt(-3))/3), hence FAIL, as "
               "the campaign brief demands.\n")
    out.append("- G2 is deliberately conservative (may reject a non-minimal true "
               "counterexample); the reduction argument is in the module "
               "docstring.\n")
    out.append("- G3 marks its mode (GENERIC resultants over Q(p,q) / SPECIFIC "
               "rational-target exact fiber counts / NONE-infeasible). "
               "Specific-target counts are evidence, exact but per-target; for "
               "an etale Keller candidate they equal the generic count.\n")
    out.append("- G6 is a necessary-condition re-check mod 3 primes = 1 (mod 3) "
               "(so sqrt(-3) reduces), never sufficient on its own.\n")
    out.append("- No ACCEPT path is exercised here: no known Keller "
               "counterexample exists to test it. The gate's default is REJECT, "
               "so an all-gates bug that errors out yields REJECT, not a false "
               "ACCEPT.\n")
    with open(path, "w") as f:
        f.write("\n".join(out))


def main(argv):
    if '--battery' in argv:
        md = None
        if '--md' in argv:
            md = argv[argv.index('--md') + 1]
        ok = battery(md_path=md)
        return 0 if ok else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
