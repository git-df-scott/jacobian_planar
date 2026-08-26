"""Session 43 -- the single sharpest question in the C*-equivariant family.

THE CHAIN, in one place.

  * A C*-equivariant Keller map on C^3 with weights (-1,1,2) is
        F_p = x*alpha(u,v),  F_q = y*beta + xz*epsilon,  F_r = y^2*delta + z*gamma
    with u = xy, v = x^2 z, and (descent_keller.py) it is Keller iff
        W := A{alpha,B} - 2B{alpha,A} + alpha{A,B} = c != 0
    for A = u*beta + v*epsilon in (u,v) and B = u^2*delta + v*gamma in (u^2,v).

  * Path S slices with Sigma = {F_p = k}.  That slice is
        x^3 * alpha_v(u,v) * z  =  k - (the rest)
    an AFFINE MODIFICATION -- the object this session's machinery handles --
    exactly when deg_v alpha = 1, i.e. alpha = alpha0(u) + alpha1(u) v.  The
    obstruction found by pathS_highdegree.py is alpha_v constant, and all seven
    known counterexamples have alpha_v = +/-1.

  * With alpha = alpha0(u) + alpha1(u) v, the modification's centre points are
    the nonzero roots r of alpha1 with alpha0(r) != 0, and
        chi(S) = #{such roots}.
    S ~ C^2 needs chi(S) = 1, so alpha1 must have EXACTLY ONE such root.

  * The source automorphism (x,y,z) -> (l1 x, l2 y, l3 z) acts on the invariants
    by u -> s u, v -> t v with s = l1 l2 and t = l1^2 l3 INDEPENDENT, so the
    three coefficients of alpha = k - r v + u v scale as (k, -r t, s t).  With
    r != 0 -- which is what chi(S) = 1 requires -- take t = 1/r, s = r to get

        alpha = k + (u - 1) v

    and alpha -> lam*alpha rescales c, so c = 1 is free.  ONE parameter, k != 0.

So the whole Path S programme for C*-equivariant counterexamples comes down to:

    does  W(alpha, A, B) = 1  have a solution with alpha = k + (u-1)v, k != 0,
    A in (u,v), B in (u^2,v)?

That is what this file asks, exactly, over F_p, with the generator controlled.
"""
import os
import subprocess
import sys
import sympy as sp

u, v = sp.symbols('u v')
OUT = []
SCRATCH = os.environ.get('SCRATCH', '/tmp')
P = 1000003


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    return bool(ok)


def br(f, g):
    return sp.expand(sp.diff(f, u) * sp.diff(g, v) - sp.diff(f, v) * sp.diff(g, u))


def W(al, A, B):
    return sp.expand(A * br(al, B) - 2 * B * br(al, A) + al * br(A, B))


def mons(d):
    return [(a, b) for t in range(d + 1) for a in range(t + 1) for b in [t - a]]


def build(dA, dB, alpha_shape='target'):
    """alpha_shape 'target'  : alpha = k + (u-1)v      -- alpha_v NON-constant
       alpha_shape 'known'   : alpha = k + c1*u + c2*v -- alpha_v constant (control)
    """
    kk = sp.Symbol('k')
    if alpha_shape == 'target':
        al = kk + (u - 1) * v
        extra = [kk]
    else:
        c1, c2 = sp.symbols('c1 c2')
        al = kk + c1 * u + c2 * v
        extra = [kk, c1, c2]
    mA = [m for m in mons(dA) if m != (0, 0)]
    mB = [m for m in mons(dB) if m not in ((0, 0), (1, 0))]
    vA = {m: sp.Symbol('A_%d_%d' % m) for m in mA}
    vB = {m: sp.Symbol('B_%d_%d' % m) for m in mB}
    A = sum(vA[m] * u**m[0] * v**m[1] for m in mA)
    B = sum(vB[m] * u**m[0] * v**m[1] for m in mB)
    w = sp.expand(W(al, A, B))
    eqs = [sp.expand(c - (1 if m == (0, 0) else 0)) for m, c in sp.Poly(w, u, v).terms()]
    # k != 0 by saturation: k*sk = 1
    sk = sp.Symbol('sk')
    eqs.append(sp.expand(kk * sk - 1))
    varlist = sorted({t for e in eqs for t in e.free_symbols}, key=str)
    return varlist, eqs, (al, A, B, vA, vB, extra)


def singular_unit(varlist, eqs, timeout=2400, tag='t'):
    path = os.path.join(SCRATCH, 'pst_%s.sing' % tag)
    body = ["ring R = %d, (%s), dp;" % (P, ','.join(str(s) for s in varlist)),
            "ideal I = " + ",\n  ".join(str(e).replace('**', '^') for e in eqs) + ";",
            "ideal G = slimgb(I);",
            'if (size(G) == 1 and G[1] == 1) { "RESULT:EMPTY"; }',
            'else { "RESULT:NONEMPTY"; "ngens="; size(G); }',
            "quit;"]
    open(path, 'w').write('\n'.join(body) + '\n')
    try:
        r = subprocess.run(['Singular', '-q', path], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 'NOVERDICT', 'timeout %ds' % timeout
    out = r.stdout
    if 'RESULT:EMPTY' in out:
        return 'EMPTY', ''
    if 'RESULT:NONEMPTY' in out:
        return 'NONEMPTY', out.strip().splitlines()[-1][:40]
    return 'NOVERDICT', (out or r.stderr).strip()[:120]


def main():
    print("[A]  generator control: the equations really are W's coefficients")
    import random
    random.seed(7)
    for dA, dB in ((3, 4), (4, 5)):
        varlist, eqs, (al, A, B, vA, vB, extra) = build(dA, dB)
        assign = {t: sp.Integer(random.randrange(1, 40)) for t in varlist}
        wtrue = sp.expand(W(al.subs(assign), A.subs(assign), B.subs(assign)))
        # rebuild what the equations say W's coefficients are
        ok = True
        pw = dict(sp.Poly(wtrue, u, v).terms())
        for e, (m, _c) in zip(eqs, sp.Poly(sp.expand(W(al, A, B)), u, v).terms()):
            want = pw.get(m, 0) - (1 if m == (0, 0) else 0)
            if sp.expand(e.subs(assign) - want) != 0:
                ok = False
                break
        rec("deg A = %d, deg B = %d: every generated equation equals the matching "
            "coefficient of W, on a random point" % (dA, dB), ok,
            "[%d vars, %d eqs]" % (len(varlist), len(eqs)))
    print()

    print("[B]  CONTROL: alpha_v CONSTANT (alpha = k + c1 u + c2 v).  Alpoge lives")
    print("     here, so EMPTY would prove the pipeline broken.")
    varlist, eqs, _ = build(3, 4, alpha_shape='known')
    st, det = singular_unit(varlist, eqs, timeout=2000, tag='ctrl')
    if st == 'NOVERDICT':
        rec("control: NO VERDICT (%s) -- everything below is UNCALIBRATED" % det, False)
    else:
        rec("control: alpha_v constant gives a NONEMPTY system", st == 'NONEMPTY',
            "%s  [%d vars, %d eqs]" % (st, len(varlist), len(eqs)))
    print()

    print("[C]  THE QUESTION: alpha = k + (u-1)v, k != 0 (saturated).")
    print("     alpha_v = u - 1 is NON-constant, alpha1 has exactly one root and it")
    print("     is nonzero, so chi(S) = 1 -- the only shape Path S can use.")
    for dA, dB in ((3, 4), (4, 5), (5, 6)):
        varlist, eqs, _ = build(dA, dB)
        st, det = singular_unit(varlist, eqs, timeout=2700, tag='q%d%d' % (dA, dB))
        lab = "deg A <= %d, deg B <= %d" % (dA, dB)
        if st == 'EMPTY':
            rec("%s: NO SOLUTION -- 1 is in the ideal, exact over F_%d" % (lab, P),
                True, "[%d vars, %d eqs]" % (len(varlist), len(eqs)))
        elif st == 'NONEMPTY':
            rec("%s: *** SOLUTIONS EXIST -- FOLLOW UP IMMEDIATELY ***" % lab, True,
                "%s [%d vars, %d eqs]" % (det, len(varlist), len(eqs)))
        else:
            rec("%s: NO VERDICT (%s)" % (lab, det), False, "resource failure, NOT a result")
    print()


if __name__ == '__main__':
    main()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("=" * 72)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
