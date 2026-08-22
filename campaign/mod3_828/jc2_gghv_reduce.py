"""
Plane Jacobian campaign - Session 20
TRIANGULAR PREPROCESSING OF THE GGHV (8,28) OPEN-CASE SYSTEM.

GGHV (arXiv:2204.14178) leave exactly one case open below degree 125:
(deg P, deg Q) = (72,108) in the shape their Proposition 4.3 labels "(8,28)".
They never publish the system.  jc2_gghv_system.py builds the unreduced
Newton-polygon system that Prop 4.3 implies mechanically:

    P, Q supported on the stated Newton polygons, [P,Q] = Px Qy - Py Qx = x^2,
    with the polygon VERTEX coefficients required nonzero.

Sub-case (2): 72 unknowns, 92 quadratic equations.
A generic Groebner run on that is not expected to finish, and the
jc2_gghv_system.md assessment says so.

THIS FILE TESTS THAT ASSESSMENT rather than accepting it.  The system is sparse
(avg 10.6 terms/equation, some single monomials) and, crucially, the bracket
equations are TRIANGULAR with respect to the Newton-polygon grading: the
extreme monomials of [P,Q] involve only the extreme coefficients of P and Q.
So before invoking any Groebner engine, run the elimination the structure hands
you for free:

  * MONOMIAL equations (single term c*u*w = 0) force u = 0 or w = 0.  Any
    factor that is a required-nonzero vertex coefficient is discarded, which
    frequently forces the OTHER factor to vanish outright - a free kill.
  * Equations LINEAR in some unknown, whose coefficient is a nonzero constant
    or a monomial in the invertible vertex coefficients, solve for that unknown
    and substitute everywhere.

Iterating these two rules to a fixed point costs nothing and can collapse the
system by a large factor.  Whatever remains is what a Groebner engine actually
has to face.

Exact arithmetic throughout (sympy Rational / integers).  No floating point.
"""

import sys
import time
import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar')
import jc2_gghv_system as G

SCRATCH = ('/tmp/claude-0/-home-user-jacobian-planar/'
           '8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad')


def build(case):
    pp, _ = G.lattice_points(case["P"])
    qq, _ = G.lattice_points(case["Q"])
    ps = G.build_symbols("c", pp)
    qs = G.build_symbols("d", qq)
    eqs = G.bracket_system(pp, ps, qq, qs, case["rhs"])
    nz = set(G.nonzero_side_conditions(case["P"], ps)) | \
         set(G.nonzero_side_conditions(case["Q"], qs))
    allsym = list(ps.values()) + list(qs.values())
    return list(eqs.values()), allsym, nz


def is_invertible(expr, nz):
    """True if expr is a nonzero constant or a monomial in known-nonzero syms."""
    expr = sp.expand(expr)
    if expr.is_number:
        return expr != 0
    # fast path: a bare product of known-nonzero symbols and a nonzero rational
    args = sp.Mul.make_args(sp.together(expr))
    ok = True
    for f in args:
        b, _e = f.as_base_exp()
        if b.is_number:
            if b == 0:
                return False
            continue
        if b in nz:
            continue
        ok = False
        break
    if ok:
        return True
    num, _den = sp.fraction(sp.together(expr))
    facs = sp.factor_list(sp.expand(num))
    if facs[0] == 0:
        return False
    for (f, _m) in facs[1]:
        if f.is_number:
            continue
        if f in nz:
            continue
        return False
    return True


def polish(e):
    """Substitutions produce rational functions whose denominators are products
    of required-nonzero vertex coefficients.  Clearing them does not change the
    solution set in the saturated setting, and keeps every equation polynomial."""
    e = sp.together(sp.expand(e))
    if e == 0:
        return sp.Integer(0)
    n, _d = sp.fraction(e)
    n = sp.expand(n)
    if n == 0:
        return sp.Integer(0)
    # strip a purely numeric content factor
    try:
        c, _ = sp.factor_terms(n).as_coeff_Mul()
        if c.is_Rational and c != 0 and c != 1:
            n = sp.expand(n/c)
    except Exception:
        pass
    return n


def reduce_system(eqs, allsym, nz, max_rounds=400, verbose=True):
    """Iterate monomial-kill and linear-solve to a fixed point."""
    eqs = [polish(e) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    zeroed, solved = set(), {}
    contradiction = None
    for rnd in range(max_rounds):
        changed = False

        # --- rule 1: single-monomial equations ---
        for e in list(eqs):
            e = sp.expand(e)
            if e == 0:
                continue
            terms = sp.Add.make_args(e)
            if len(terms) != 1:
                continue
            facs = sp.factor_list(e)
            vars_in = [f for (f, _m) in facs[1] if not f.is_number and f.free_symbols]
            live = [f for f in vars_in if f not in nz]
            if not vars_in:
                contradiction = f"nonzero constant equation: {e}"
                return eqs, solved, zeroed, contradiction
            if len(live) == 0:
                contradiction = (f"monomial equation in only-nonzero symbols: {e}")
                return eqs, solved, zeroed, contradiction
            if len(live) == 1 and live[0].is_Symbol:
                v = live[0]
                if v not in zeroed:
                    zeroed.add(v)
                    eqs = [polish(x.subs(v, 0)) for x in eqs]
                    eqs = [x for x in eqs if x != 0]
                    changed = True
                    if verbose:
                        print(f"    r{rnd}: monomial kill  {v} = 0")
                    break
        if changed:
            continue

        # --- rule 2: equations linear in a variable with invertible coeff ---
        best = None
        for e in eqs:
            e = sp.expand(e)
            for v in sorted(e.free_symbols, key=str):
                # cheap linearity test: equations are kept expanded, so a plain
                # second derivative is exact and avoids a simplify() per pair
                if sp.expand(e.diff(v, 2)) != 0:
                    continue
                a = sp.expand(e.diff(v))
                if a == 0:
                    continue
                if v in a.free_symbols:
                    continue
                if not is_invertible(a, nz):
                    continue
                rest = sp.expand(e - a*v)
                score = len(sp.Add.make_args(rest))
                if best is None or score < best[0]:
                    best = (score, v, sp.cancel(-rest/a), e)
        if best is not None:
            _s, v, val, src = best
            solved[v] = val
            eqs = [polish(x.subs(v, val)) for x in eqs if x is not src]
            eqs = [x for x in eqs if x != 0]
            if verbose and rnd < 12:
                print(f"    r{rnd}: linear solve   {v} := {sp.sstr(val)[:60]}")
            changed = True
        if not changed:
            break
    return eqs, solved, zeroed, contradiction


def run(case, tag):
    print("=" * 74)
    print(f"CASE {tag}: {case['label']}")
    print("=" * 74)
    eqs, allsym, nz = build(case)
    print(f"  start: {len(allsym)} unknowns, {len(eqs)} equations, "
          f"{len(nz)} required-nonzero vertex coefficients")
    t0 = time.time()
    eqs2, solved, zeroed, contra = reduce_system(eqs, allsym, nz)
    dt = time.time() - t0
    remaining = set()
    for e in eqs2:
        remaining |= e.free_symbols
    print(f"\n  after triangular preprocessing ({dt:.1f}s):")
    print(f"    variables forced to 0        : {len(zeroed)}")
    print(f"    variables solved & eliminated: {len(solved)}")
    print(f"    equations remaining          : {len(eqs2)}")
    print(f"    variables remaining          : {len(remaining)}")
    if contra:
        print(f"\n  *** CONTRADICTION FOUND: {contra}")
        print("  *** No P,Q of this Newton-polygon shape exist with [P,Q]=x^2.")
        print("  *** If this is the (8,28) open sub-case, that CLOSES it.")
        return eqs2, remaining, contra
    if not eqs2:
        print("\n  *** ALL EQUATIONS ELIMINATED: the system is consistent and the")
        print("  *** remaining variables are free. A solution exists -- this needs")
        print("  *** immediate hard verification, since it would be a counterexample.")
        return eqs2, remaining, None
    # any vertex coefficient forced to zero is itself a contradiction
    bad = [v for v in zeroed if v in nz]
    if bad:
        print(f"\n  *** vertex coefficients forced to zero: {bad}")
        print("  *** contradicts Prop 4.3's nonvanishing requirement -> case CLOSED")
        return eqs2, remaining, f"vertex coeffs zero: {bad}"
    degs = sorted({sp.Poly(e, *sorted(remaining, key=str)).total_degree()
                   for e in eqs2}) if remaining else []
    print(f"    degrees of remaining eqs     : {degs}")
    # emit the reduced system for Singular
    if remaining:
        rl = sorted(remaining, key=str)
        body = ",\n  ".join(sp.sstr(e).replace("**", "^") for e in eqs2)
        prod = "*".join(str(s) for s in sorted(nz & remaining, key=str)) or "1"
        path = f"{SCRATCH}/gghv_{tag}_reduced.sing"
        open(path, "w").write(
            f"ring R = 32003, ({','.join(str(s) for s in rl)}), dp;\n"
            f"ideal I = {body};\n"
            f'"{tag} reduced: {len(rl)} vars, {len(eqs2)} eqs";\n'
            f"ideal Gb = std(I);\n"
            f'"basis size:"; size(Gb);\n'
            f'"trivial (=> case CLOSED):"; (size(Gb)==1 && Gb[1]==1);\n'
            f'LIB "elim.lib"; ideal S = sat(I, {prod})[1];\n'
            f'"saturated basis size:"; size(S);\n'
            f'"saturated trivial (=> case CLOSED):"; (size(S)==1 && S[1]==1);\n'
            f"quit;\n")
        print(f"    reduced system emitted -> {path}")
    return eqs2, remaining, None


if __name__ == '__main__':
    for case, tag in [(G.OPEN_CASE_2, 'open2'), (G.OPEN_CASE_1, 'open1')]:
        run(case, tag)
        print()
