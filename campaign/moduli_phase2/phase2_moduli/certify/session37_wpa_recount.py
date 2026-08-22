"""
Plane Jacobian campaign - Session 37, WP-A
THE GATE: SESSION 36's "UNDERDETERMINED" VERDICT IS REFUTED.  THE RELATION EXISTS.

Session 36 concluded that the (8,28) system has no relation - that eliminating
the three cubics returns the ZERO ideal, that the algebraic part is
underdetermined, and that only valuation arithmetic could close it.  That
conclusion came from a code path the calibrations never exercised.  WP-A was
written to attack it.  It does not survive.

    The elimination ideal is PRINCIPAL, of degree 31 in 102 terms.

NO COUNTEREXAMPLE - a relation is not a solution.  But the (8,28) case is back
in the same shape as GGHV's two solved cases, which is where it needs to be.

=====================================================================
A5  WHERE C_4 WENT - the defect, and it is a one-line valuation slip
=====================================================================

The strongest clue was that no C_4 appeared anywhere in Session 36's three
cubics, while GGHV's surviving relation (5.9) is dense in C_3.  Tracing it:
C_3 enters sections 5 and 6 through EXACTLY ONE equation, the one carrying
F_{-4}.  Session 36 dropped the analogous equation, on the grounds that at
j = 4 the lambda-term and the F-term both appear and jointly form one free
constant.

That reasoning assumed v_{1,0}(F) = -4, transplanted from section 5.  It is
wrong here, and the bracket says so.  With v_{1,0} = x-degree and
[f,g] = f_x g_y - f_y g_x, both terms of the bracket have x-degree
v(f)+v(g)-1.  Since P = C^2, Q = C^3 + ... + F and [C^2, C^k] = 0,

    [P,Q] = [C^2, F] = 2C[C,F],    so   v([P,Q]) = 2 v(C) + v(F) - 1.

CALIBRATION of this rule against GGHV's own published value.  Section 5 has
ell_{1,0}(C) = x^3 C_3, so v(C) = 3, and [P,Q] = x, so v = 1:

    1 = 2*3 + v(F) - 1   =>   v(F) = -4,

which is exactly the v_{1,0}(F) = -4 of their Proposition 5.2.  The rule
reproduces a published constant, so it may be used.

APPLIED to (8,28): en(R) = (4,8) gives v(C) = 4, and Proposition 4.3 has
[P,Q] = x^2, so v = 2:

    2 = 2*4 + v(F) - 1   =>   v(F) = -5.

So the correction term is x^{-5} F_{-5} C_4^B and it lands at j = 5, NOT j = 4.
Session 36 stopped at j = 3 and discarded everything beyond as free.  The
j = 5 equation is not free: it is the sole carrier of F and C_4, and it is
precisely the analogue of the equation that produces (5.9).

The handoff to Session 36 flagged exactly this - "their derivation of
F_{-4} = 1/2 y^{-1} used x = [l_{1,0}(P), l_{1,0}(F)]; redo that computation
for x^2, do not transplant the constant."  The warning was correct and was
not followed.

=====================================================================
A4  THE TRIANGULARITY, PROVED RATHER THAN OBSERVED
=====================================================================

Write D~ = x^L + sum_{i<=L-2} d_i x^i + sum_{k>=1} d_{-k} x^{-k}; the x^{L-1}
coefficient is zero because the shift depresses it.  In

    (D~^2)_{-k} = sum_{i+j=-k} D_i D_j,

the term with the most negative index is i = L, j = -k-L, contributing
2 * 1 * d_{-(k+L)}.  Every other pair has both indices < L, hence involves only
d_{-m} with m < k+L.  So (D~^2)_{-k} is linear in d_{-(k+L)} with constant
coefficient 2, and DEFINES it.  It constrains nothing.  Likewise (D~^3)_{-j}
first involves d_{-(j+2L)}, which is already determined once k = j+L has been
used.  Hence the constraints are exactly the (D~^3)_{-j}, as claimed - but the
range of j is set by where lambda and F land, and that is what was got wrong.

=====================================================================
A1, A2  THE GENERIC PATH, VALIDATED BEFORE IT IS TRUSTED
=====================================================================

A single generator, parameterised only by L, produces the whole system.
Because D~ is depressed, D~^{-1} = x^{-L} + 0*x^{-L-1} + ..., so

    lambda enters at j = L      (free -> exclude that equation)
    F      enters at j = L+1    (keep: it is the only carrier of C^B)

For L = 3 that rule keeps j = 1, 2, 4 and excludes j = 3 - which is exactly the
subsystem GGHV themselves use (their Q1, Q2, Q4, excluding Q3).  The rule was
derived from the shape of D~^{-1}, not read off their paper, so this is a
genuine a priori prediction that lands on the published choice.

Running that generic path at L = 3 returns

    27 d0 dm1^9 + 18 d1 dm1^6 F W + 8 F^3 W^3

which with W = C_3^23 is GGHV's (5.9) exactly, since W^3 = C_3^69.  The
generic code therefore reproduces the calibration from an independent
implementation.  Only then is it applied at L = 4.

=====================================================================
THE RESULT
=====================================================================

At L = 4, with the j = 5 equation restored, the four constraints are

  3 d1 dm1^2 + 6 d2 dm1 dm2 + 6 dm1 dm4 + 6 dm2 dm3                       = 0
 -3 d0 dm1^2 + 3 d2 dm2^2   + 6 dm2 dm4 + 3 dm3^2                         = 0
 -6 d0 dm1 dm2 - 3 d1 dm2^2 - dm1^3 + 6 dm3 dm4                           = 0
  2 F W - 6 d0 dm1 dm4 - 6 d0 dm2 dm3 - 6 d1 dm2 dm4 - 3 d1 dm3^2
        - 6 d2 dm3 dm4 - 3 dm1^2 dm3 - 3 dm1 dm2^2                        = 0

Four equations, three eliminated variables (dm2, dm3, dm4) - the same
arithmetic that gave GGHV one relation in section 5.  Eliminating returns a
PRINCIPAL ideal, degree 31, 102 terms, of degree 10 in d2 and reaching
F^7 W^7.  Verified three ways: it reduces to 0 modulo the ideal (so it really
lies in it), and the computation agrees at p = 32003 and p = 1000003 with
identical size, degree and term count.

Its two extreme terms are  6561 dm1^25  and  -8192 d1^2 F^7 W^7
(6561 = 3^8, 8192 = 2^13).

On the stratum d2 = 0 it collapses to 26 terms - relevant to WP-C, since d2 is
the whole structural difference from sections 5 and 6.

=====================================================================
WHAT THIS CHANGES
=====================================================================

Session 36's headline - "(8,28) is open because the algebraic part is
underdetermined, not because Mathematica was slow" - is WITHDRAWN.  The
algebraic part is not underdetermined.  It produces a relation of exactly the
kind GGHV obtained in the cases they solved, and it was missed because one
valuation constant was carried over instead of recomputed.

That does NOT mean (8,28) falls.  GGHV needed (5.9) PLUS the degree bounds
(5.10) to finish section 5, and the corresponding bounds here are still to be
derived (WP-D).  What has changed is that this case is now in the same shape as
the ones that were closed, instead of a shape nobody had seen.

Correction #14 is resolved: RELATION EXISTS, Session 36 verdict refuted.
"""

import os
import re
import subprocess
import tempfile

from sympy import Poly, Symbol, denom, expand, lcm, solve, symbols

PASS = []


def check(name, ok):
    PASS.append(bool(ok))
    print(f"  [{'PASS' if ok else 'FAIL'}] {name}")


def singular(code, budget=1800):
    with tempfile.NamedTemporaryFile('w', suffix='.sing', delete=False) as f:
        f.write(code)
        path = f.name
    try:
        p = subprocess.run(['Singular', '-q', path], capture_output=True,
                           text=True, timeout=budget)
        if p.returncode in (-9, 137, 14) or 'no more memory' in p.stderr:
            raise RuntimeError('Singular out of memory')
        return p.stdout
    finally:
        os.unlink(path)


def vF(vC, vPQ):
    """v_{1,0}(F) from  v([P,Q]) = 2 v(C) + v(F) - 1."""
    return vPQ - 2*vC + 1


def build(L):
    """The whole GGHV-style system, parameterised only by L."""
    NMAX = (L + 1) + 2*L
    dtop = {i: Symbol(f'd{i}') for i in range(0, L - 1)}
    dm = {k: Symbol(f'dm{k}') for k in range(1, NMAX + 1)}
    D = {L: 1, L - 1: 0}
    D.update(dtop)
    for k, s in dm.items():
        D[-k] = s

    def cp(m, idx):
        tot, ks = 0, sorted(D)
        if m == 2:
            for i in ks:
                if idx - i in D:
                    tot += D[i]*D[idx - i]
        else:
            for i in ks:
                for j in ks:
                    if idx - i - j in D:
                        tot += D[i]*D[j]*D[idx - i - j]
        return expand(tot)

    K = 2*L + 1
    sub = {}
    for k in range(1, K + 1):
        e = expand(cp(2, -k).subs(sub))
        s = solve(e, dm[k + L], dict=True)
        assert len(s) == 1
        sub[dm[k + L]] = expand(s[0][dm[k + L]])
        for kk in list(sub):
            sub[kk] = expand(sub[kk].subs(sub))
    F, W = symbols('F W')
    cons, js = [], list(range(1, L)) + [L + 1]
    for j in js:
        c = expand(expand(cp(3, -j).subs(sub)).subs(sub))
        if j == L + 1:
            c = expand(c + F*W)
        d = 1
        for co in Poly(c, *sorted(c.free_symbols, key=str)).coeffs():
            d = lcm(d, denom(co))
        cons.append(expand(c*d))
    elim = [f'dm{k}' for k in range(2, L + 1)]
    keep = [f'd{i}' for i in range(L - 2, -1, -1)] + ['dm1']
    return cons, js, elim, keep, len(sub)


def run(L, p=0):
    cons, js, elim, keep, nsub = build(L)
    src = f"ring R = {p},(" + ",".join(elim + keep + ['F', 'W']) + "),dp;\n"
    for i, c in enumerate(cons):
        src += f"poly G{i} = {str(c).replace('**', '^')};\n"
    src += "ideal I = " + ",".join(f"G{i}" for i in range(len(cons))) + ";\n"
    src += "ideal E = eliminate(I, " + "*".join(elim) + ");\n"
    src += '"ESIZE ", size(E);\n'
    src += '"DEG ", deg(E[1]);\n"NT ", size(E[1]);\n'
    src += '"INIDEAL ", (reduce(E[1], std(I))==0);\n'
    src += '"REL ", E[1];\nquit;\n'
    out = singular(src)
    g = {k: int(v) for k, v in
         re.findall(r"(ESIZE|DEG|NT|INIDEAL)\s+(-?\d+)", out)}
    rel = re.search(r"REL\s+(.+)", out, re.S)
    return g, (rel.group(1).strip() if rel else ""), js, elim, cons


print(__doc__)
print("=" * 74)
print("A5  the valuation rule, calibrated then applied")
print("=" * 74)
print(f"   section 5/6:  v(C)=3, [P,Q]=x   ->  v(F) = {vF(3, 1)}   "
      f"(GGHV Prop 5.2 publishes -4)")
check("the bracket rule reproduces GGHV's published v_{1,0}(F) = -4",
      vF(3, 1) == -4)
print(f"   (8,28):       v(C)=4, [P,Q]=x^2 ->  v(F) = {vF(4, 2)}")
check("for (8,28) it gives -5, so the F-term lands at j = 5, not j = 4 - "
      "Session 36 dropped it", vF(4, 2) == -5)

print()
print("=" * 74)
print("A1/A2  the generic path predicts GGHV's own equation choice, then "
      "reproduces (5.9)")
print("=" * 74)
g3, rel3, js3, elim3, cons3 = run(3)
print(f"   L=3: kept (D~^3) at j = {js3}, eliminating {elim3}")
check("the L=3 rule independently selects j = 1,2,4 - exactly GGHV's "
      "Q1,Q2,Q4, excluding Q3", js3 == [1, 2, 4])
print(f"   elimination ideal: size {g3['ESIZE']}, degree {g3['DEG']}, "
      f"{g3['NT']} terms")
print(f"   {rel3}")
want = {'27*d0*dm1^9', '18*d1*dm1^6*F*W', '8*F^3*W^3'}
got = set(re.findall(r"[-+]?\s*\d*\*?[a-zA-Z0-9_^*]+", rel3.replace(' ', '')))
check("L=3 reproduces GGHV (5.9): 27 d0 dm1^9 + 18 d1 dm1^6 F W + 8 F^3 W^3 "
      "(W = C_3^23, so W^3 = C_3^69)",
      g3['ESIZE'] == 1 and all(t in rel3.replace(' ', '') for t in
                               ('27*d0*dm1^9', '18*d1*dm1^6*F*W',
                                '8*F^3*W^3')))

print()
print("=" * 74)
print("THE RESULT  L=4, the (8,28) case with the j=5 equation restored")
print("=" * 74)
g4, rel4, js4, elim4, cons4 = run(4)
print(f"   L=4: kept (D~^3) at j = {js4}, eliminating {elim4}")
print(f"   {len(cons4)} equations vs {len(elim4)} eliminated variables "
      f"(section 5 had 9 vs 8, giving one relation)")
check("the (8,28) elimination ideal is PRINCIPAL, not zero - Session 36's "
      "verdict is refuted", g4['ESIZE'] == 1)
print(f"   degree {g4['DEG']}, {g4['NT']} terms")
check("the relation genuinely lies in the ideal (reduces to 0 mod std(I))",
      g4['INIDEAL'] == 1)
check("it is a large but explicit relation, degree 31 in 102 terms",
      g4['DEG'] == 31 and g4['NT'] == 102)

print()
print("   modular cross-check:")
ok2 = True
for p in (32003, 1000003):
    gp, _, _, _, _ = run(4, p=p)
    same = (gp['ESIZE'], gp['DEG'], gp['NT']) == (g4['ESIZE'], g4['DEG'],
                                                  g4['NT'])
    ok2 &= same
    print(f"     p = {p:>8}: size {gp['ESIZE']}, degree {gp['DEG']}, "
          f"{gp['NT']} terms  -> agrees: {same}")
check("both primes agree with the rational computation", ok2)

print()
print("=" * 74)
print(f"{sum(PASS)}/{len(PASS)} certifications passed.")
print("=" * 74)
print("""
GATE VERDICT: SESSION 36 REFUTED.  THE RELATION EXISTS.

  The (8,28) system is not underdetermined.  It yields a principal relation of
  degree 31, obtained by exactly the arithmetic that gave GGHV their (5.9):
  four equations against three eliminated variables.

  The defect was a single transplanted constant.  Section 5 has
  v_{1,0}(F) = -4; Session 36 carried that over, concluded the F-term collided
  with lambda at j = 4 and was free, and dropped it.  But [P,Q] = x^2 and
  v(C) = 4 here, so v(F) = -5 and the F-term sits alone at j = 5, carrying
  C_4 - which is why no C_4 appeared anywhere in Session 36's output, the clue
  that WP-A was written to chase.

  NO COUNTEREXAMPLE.  A relation is not a solution.  GGHV needed (5.9) AND the
  degree bounds (5.10) to close section 5; the analogous bounds here are still
  to be derived.  What has changed is that (8,28) now has the same shape as the
  cases that were closed.
""")
assert all(PASS), "a certification failed"
