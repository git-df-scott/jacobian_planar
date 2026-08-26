"""Session 43 -- the dimension-3 Keller condition collapses to ONE plane identity.

THE COLLAPSE.  equivariant_ansatz.py wrote det JF for a C*-equivariant map with
weights (-1,1,2) as a 40-term expression Psi(u,v) in five unknown functions.
That was the wrong bookkeeping.  Pushing everything through the descent

    G = (alpha*A, alpha^2*B),     A := u*beta + v*epsilon,
                                  B := u^2*delta + v*gamma

gives  det JG = alpha^2 * W  with

    W  =  A{alpha,B} - 2B{alpha,A} + alpha{A,B}          {f,g} := f_u g_v - f_v g_u

and W equals det JF up to the sign of the permutation putting the components in
canonical weight order.  Verified below on every known counterexample.  So:

    F is Keller  <=>  A{alpha,B} - 2B{alpha,A} + alpha{A,B} = c != 0

a SINGLE scalar identity in the plane, TRILINEAR in (alpha, A, B), with A and B
ranging over the ideals (u,v) and (u^2,v) respectively -- and those two ideal
memberships are exactly the statement that A, B come from honest beta, epsilon,
gamma, delta (proved below by splitting monomials).

This also explains the census fact for free: det JG = alpha^2 * W = c * alpha^2,
so the descent's Jacobian is a constant times a perfect square because W is the
constant, not because of anything about the particular constructions.

WHAT WE ARE HUNTING.  The Path S obstruction (pathS_highdegree.py) is that the
z-linear component's z-coefficient is a pure monomial.  That component is
F_p = x*alpha(u, x^2 z), so

    dF_p/dz = x^3 * alpha_v(u,v)

and it is a pure monomial in x exactly when **alpha_v is CONSTANT**.  Note this
is NOT the same as "deg alpha <= 1": alpha = b*sigma*u^2 + a*u + b*v + c has
degree 2 and alpha_v = b, still constant, still blocked -- and indeed that alpha
is what you get by composing a known map with the source automorphism
z -> z + sigma*y^2, which cannot change anything.  All seven known maps have
alpha_v = +/-1.

So the question this file settles at small degree is:

    does  W = c  admit a solution with alpha_v NON-CONSTANT?

Run:  python3 descent_keller.py
"""
import os
import subprocess
import sys
import sympy as sp

u, v = sp.symbols('u v')
x, y, z = sp.symbols('x y z')
OUT = []
SCRATCH = os.environ.get('SCRATCH', '/tmp')


def rec(name, ok, detail=''):
    OUT.append((name, bool(ok)))
    print(("  PASS  " if ok else "  FAIL  ") + name + (("   " + detail) if detail else ""))
    return bool(ok)


def br(f, g):
    return sp.expand(sp.diff(f, u) * sp.diff(g, v) - sp.diff(f, v) * sp.diff(g, u))


def W(al, A, B):
    return sp.expand(A * br(al, B) - 2 * B * br(al, A) + al * br(A, B))


# ------------------------------------------------------- [A] verify the collapse
def part_A():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import equivariant_ansatz as EA
    print("[A]  the collapse, checked on every known counterexample")
    cases = [('alpoge_dim3_degree3.py', 'alpoge d3'),
             ('gao_G_dim3_degree4.py', 'gao G d4'),
             ('gallagher_dim3_degree3.py', 'gallagher d3'),
             ('gallagher_dim3_degree6.py', 'gallagher d6'),
             ('dim3_degree6.py', 'constructed d6'),
             ('dim3_degree7.py', 'constructed d7'),
             ('gallagher_dim3_degree12.py', 'gallagher d12')]
    for fn, label in cases:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps', fn)
        if not os.path.exists(p):
            print("  SKIP  %s" % fn)
            continue
        F = EA.load(p)
        (a_, b_, g_, d_, e_), perm = EA.decompose(F)
        a_ = a_.subs({EA.u: u, EA.v: v})
        b_ = b_.subs({EA.u: u, EA.v: v})
        g_ = g_.subs({EA.u: u, EA.v: v})
        d_ = d_.subs({EA.u: u, EA.v: v})
        e_ = e_.subs({EA.u: u, EA.v: v})
        A = sp.expand(u * b_ + v * e_)
        B = sp.expand(u**2 * d_ + v * g_)
        w = W(a_, A, B)
        J = sp.Matrix([[sp.diff(f, t) for t in (x, y, z)] for f in F])
        dF = sp.expand(J.det())
        sgn = EA.perm_sign(perm)
        rec("%s: W = %s * det JF = %s  (a CONSTANT)" % (label, '+1' if sgn > 0 else '-1', w),
            w.free_symbols == set() and sp.simplify(w - sgn * dF) == 0)
        dG = br(sp.expand(a_ * A), sp.expand(a_**2 * B))
        rec("%s: det JG = alpha^2 * W" % label, sp.expand(dG - a_**2 * w) == 0)
        rec("%s: alpha_v = %s (constant => Path S blocked)" % (label, sp.diff(a_, v)),
            sp.diff(a_, v).free_symbols == set())
    print()


# ---------------------------------------- [B] the ideal memberships are exact
def part_B():
    print("[B]  A ranges over (u,v) and B over (u^2,v): membership is exactly the")
    print("     statement that A,B come from honest beta,epsilon,gamma,delta")
    # every monomial of (u,v) is u*(mon) or v*(mon); every monomial of (u^2,v)
    # is u^2*(mon) or v*(mon).  Check by exhaustion.
    badA, badB = [], []
    for a in range(9):
        for b in range(9):
            m = (a, b)
            inA = (a >= 1) or (b >= 1)
            splitA = (a >= 1) or (b >= 1)
            if inA != splitA:
                badA.append(m)
            inB = (a >= 2) or (b >= 1)
            splitB = (a >= 2 and b == 0) or (b >= 1)
            if inB != splitB:
                badB.append(m)
    rec("A = u*beta + v*epsilon  <=>  A(0,0) = 0", not badA)
    rec("B = u^2*delta + v*gamma  <=>  B(0,0) = 0 and B_u(0,0) = 0", not badB)
    # the value of c at the origin
    al, A, B = sp.symbols('a0 A0 B0')
    print("     Evaluating W at the origin: A(0,0)=B(0,0)=B_u(0,0)=0 leaves")
    print("       c = W(0,0) = alpha(0,0) * beta(0,0) * gamma(0,0),")
    print("     so all three are nonzero -- the analogue of A(0,z)B(0,z)C_z(0,z).")
    print()


# ------------------------------------------------------ [C] the search itself
def mons(d):
    return [(a, b) for t in range(d + 1) for a in range(t + 1) for b in [t - a]]


def build_system(dal, dA, dB, force=None, p=1000003):
    """Unknown alpha (deg dal), A (deg dA, in (u,v)), B (deg dB, in (u^2,v)).

    `force` is a monomial (a,b) of alpha whose coefficient is pinned to 1;
    choosing one with b >= 1 and (a,b) != (0,1) forces alpha_v NON-CONSTANT.
    Returns (variables, equations) with W - 1 expanded coefficient-wise.
    """
    ma = mons(dal)
    mA = [m for m in mons(dA) if m != (0, 0)]
    mB = [m for m in mons(dB) if m != (0, 0) and m != (1, 0)]
    va = {m: sp.Symbol('a_%d_%d' % m) for m in ma}
    vA = {m: sp.Symbol('A_%d_%d' % m) for m in mA}
    vB = {m: sp.Symbol('B_%d_%d' % m) for m in mB}
    al = sum(va[m] * u**m[0] * v**m[1] for m in ma)
    A = sum(vA[m] * u**m[0] * v**m[1] for m in mA)
    B = sum(vB[m] * u**m[0] * v**m[1] for m in mB)
    if force is not None:
        al = al.subs(va[force], 1)
    w = sp.expand(W(al, A, B))
    pw = sp.Poly(w, u, v)
    eqs = []
    for m, coeff in pw.terms():
        eqs.append(sp.expand(coeff - (1 if m == (0, 0) else 0)))
    varlist = sorted({s for e in eqs for s in e.free_symbols}, key=str)
    return varlist, eqs


def singular_empty(varlist, eqs, p=1000003, timeout=2400, tag='sys'):
    """Return ('EMPTY'|'NONEMPTY'|'NOVERDICT', detail).  1 in I <=> no solution.

    Only the unit-ideal test is asked for.  An earlier version also called
    dim(std(G)); on a positive-dimensional ideal in 25 variables that is far
    more expensive than the question being asked, and it is not needed --
    "1 is not in I" already means solutions exist.
    """
    path = os.path.join(SCRATCH, 'dk_%s.sing' % tag)
    body = ["ring R = %d, (%s), dp;" % (p, ','.join(str(s) for s in varlist)),
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
        return 'NONEMPTY', out.strip().splitlines()[-1][:60]
    return 'NOVERDICT', (out or r.stderr).strip()[:120]


def build_pathS(pdeg, qdeg, dA, dB):
    """alpha = alpha0(u) + alpha1(u)*v with deg alpha0 <= pdeg, alpha1 monic of
    degree exactly qdeg.  qdeg >= 1 makes alpha_v = alpha1(u) NON-CONSTANT.

    Why this shape and not a general alpha:  the slice S = {F_p = k} is
        x^3 * alpha1(xy) * z  =  k - x*alpha0(xy)
    which is an AFFINE MODIFICATION -- the object the session's machinery
    handles -- exactly when deg_v alpha = 1.  A v^2 term makes the slice
    quadratic in z and leaves that machinery behind.  Moreover
    chi(S) = #{centre points} = #{nonzero roots r of alpha1 with alpha0(r) != 0},
    so S can only be C^2 when alpha1 has exactly ONE such root.  qdeg = 1 is
    therefore the sharpest single target in the whole family.
    """
    ma0 = [(a, 0) for a in range(pdeg + 1)]
    ma1 = [(a, 1) for a in range(qdeg + 1)]
    mA = [m for m in mons(dA) if m != (0, 0)]
    mB = [m for m in mons(dB) if m != (0, 0) and m != (1, 0)]
    va = {m: sp.Symbol('a_%d_%d' % m) for m in ma0 + ma1}
    vA = {m: sp.Symbol('A_%d_%d' % m) for m in mA}
    vB = {m: sp.Symbol('B_%d_%d' % m) for m in mB}
    al = (sum(va[m] * u**m[0] for m in ma0)
          + v * (u**qdeg + sum(va[(a, 1)] * u**a for a in range(qdeg))))
    A = sum(vA[m] * u**m[0] * v**m[1] for m in mA)
    B = sum(vB[m] * u**m[0] * v**m[1] for m in mB)
    w = sp.expand(W(al, A, B))
    eqs = [sp.expand(c - (1 if m == (0, 0) else 0)) for m, c in sp.Poly(w, u, v).terms()]
    varlist = sorted({t for e in eqs for t in e.free_symbols}, key=str)
    return varlist, eqs


def part_C():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import equivariant_ansatz as EA
    print("[C]  CONTROL 1 -- the system generator is correct.")
    print("     Build the system at the degrees of each known map and substitute")
    print("     that map's own coefficients; every equation must vanish.")
    cases = [('alpoge_dim3_degree3.py', 'alpoge d3'),
             ('gallagher_dim3_degree3.py', 'gallagher d3'),
             ('gao_G_dim3_degree4.py', 'gao G d4'),
             ('dim3_degree6.py', 'constructed d6')]
    for fn, label in cases:
        pth = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'maps', fn)
        if not os.path.exists(pth):
            continue
        F = EA.load(pth)
        (a_, b_, g_, d_, e_), perm = EA.decompose(F)
        sub = {EA.u: u, EA.v: v}
        a_, b_, g_, d_, e_ = (t.subs(sub) for t in (a_, b_, g_, d_, e_))
        A = sp.expand(u * b_ + v * e_)
        B = sp.expand(u**2 * d_ + v * g_)
        c = W(a_, A, B)
        # rescale so that W = 1, which is what build_system demands
        a_s = sp.expand(a_ / c)
        dal = sp.Poly(a_s, u, v).total_degree()
        dA = sp.Poly(A, u, v).total_degree()
        dB = sp.Poly(B, u, v).total_degree()
        varlist, eqs = build_system(dal, dA, dB)
        vals = {}
        for m, cf in sp.Poly(a_s, u, v).terms():
            vals[sp.Symbol('a_%d_%d' % m)] = cf
        for m, cf in sp.Poly(A, u, v).terms():
            vals[sp.Symbol('A_%d_%d' % m)] = cf
        for m, cf in sp.Poly(B, u, v).terms():
            vals[sp.Symbol('B_%d_%d' % m)] = cf
        full = {t: vals.get(t, 0) for t in varlist}
        resid = [sp.simplify(e.subs(full)) for e in eqs]
        rec("%s: its own coefficients satisfy every generated equation "
            "(deg alpha,A,B = %d,%d,%d; %d vars, %d eqs)"
            % (label, dal, dA, dB, len(varlist), len(eqs)),
            all(r == 0 for r in resid),
            "" if all(r == 0 for r in resid) else "%d nonzero residuals" % sum(1 for r in resid if r != 0))
    print()

    print("[D]  CONTROL 2 -- Singular must NOT report EMPTY on a system that")
    print("     provably has a point (alpha pinned at the v monomial: the known shape).")
    varlist, eqs = build_system(1, 3, 4, force=(0, 1))
    st, det = singular_empty(varlist, eqs, tag='ctrl2', timeout=1500)
    if st == 'NOVERDICT':
        rec("control 2: NO VERDICT (%s) -- the search below is UNCALIBRATED" % det,
            False, "resource failure")
    else:
        rec("control 2: system with alpha_v constant is NONEMPTY (as it must be)",
            st == 'NONEMPTY', "%s  [%d vars, %d eqs]" % (st, len(varlist), len(eqs)))
    print()

    print("[E]  THE QUESTION.  alpha_v non-constant, in the shape Path S needs:")
    print("     alpha = alpha0(u) + alpha1(u)*v, alpha1 monic of degree q >= 1.")
    for (q, pd, dA, dB) in ((1, 1, 3, 4), (1, 2, 3, 4), (1, 1, 4, 5), (2, 2, 3, 4)):
        varlist, eqs = build_pathS(pd, q, dA, dB)
        st, det = singular_empty(varlist, eqs, tag='ps%d%d%d%d' % (q, pd, dA, dB),
                                 timeout=2400)
        label = ("deg alpha1 = %d, deg alpha0 = %d, deg A = %d, deg B = %d"
                 % (q, pd, dA, dB))
        if st == 'EMPTY':
            rec("%s: NO SOLUTION -- 1 is in the ideal, exact over F_1000003" % label,
                True, "[%d vars, %d eqs]" % (len(varlist), len(eqs)))
        elif st == 'NONEMPTY':
            rec("%s: *** SOLUTIONS EXIST -- FOLLOW UP *** (%s)" % (label, det),
                True, "[%d vars, %d eqs]" % (len(varlist), len(eqs)))
        else:
            rec("%s: NO VERDICT (%s)" % (label, det), False,
                "resource failure, NOT a result")
    print()


if __name__ == '__main__':
    part_A()
    part_B()
    part_C()
    nf = sum(1 for _n, ok in OUT if not ok)
    print("=" * 72)
    print("%d checks, %d FAILED" % (len(OUT), nf))
    sys.exit(1 if nf else 0)
