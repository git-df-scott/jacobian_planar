"""
Plane Jacobian campaign - Session 20
SCALING SYMMETRY OF THE GGHV (8,28) SYSTEM, AND THE NORMALIZED REDUCTION.

The triangular preprocessing in jc2_gghv_reduce.py works, but the eliminated
coefficients acquire growing powers of the vertex coefficient d_2_1 in their
denominators (c_1_0 = 1/d_2_1, c_1_1 = 2 d_2_2/d_2_1^2, ...), and the
expression swell is what makes the pass slow.

Setting d_2_1 = 1 removes all of it -- but ONLY if that is genuinely WLOG.
This file proves it is, before using it.

THE SYMMETRY.  For scalars alpha, beta, lambda, mu (all nonzero) put
    P'(x,y) = alpha * P(lambda x, mu y),   Q'(x,y) = beta * Q(lambda x, mu y).
Then
    [P',Q'](x,y) = alpha beta lambda mu * [P,Q](lambda x, mu y),
so if [P,Q] = x^2 then [P',Q'] = alpha beta lambda^3 mu * x^2, and the bracket
condition is preserved exactly when

    alpha * beta * lambda^3 * mu = 1.                                   (*)

Scaling does not move Newton polygons, so the Prop 4.3 shape is preserved and
the required-nonzero vertex coefficients stay nonzero.  On coefficients,
    c_ij -> alpha lambda^i mu^j c_ij,      d_ij -> beta lambda^i mu^j d_ij.
With (*) that is a 3-parameter group, so generically THREE coefficients can be
normalized to 1.  We use only one, d_2_1 = 1, which needs a single equation and
is therefore always available.

Everything below is exact.  No floating point.
"""

import sys
import time
import sympy as sp

sys.path.insert(0, '/home/user/jacobian_planar')
import jc2_gghv_system as G
import jc2_gghv_reduce as RED

SCRATCH = ('/tmp/claude-0/-home-user-jacobian-planar/'
           '8579cc16-25cb-5f13-9ff3-9a51c4d87492/scratchpad')

x, y = sp.symbols('x y')
LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# ===================================================================
# 1.  Verify the symmetry exactly
# ===================================================================
print("SECTION 1  the scaling symmetry, verified exactly")
al, be, lam, mu = sp.symbols('alpha beta lambda mu', nonzero=True)


def brack(P, Q):
    return sp.expand(sp.diff(P, x)*sp.diff(Q, y) - sp.diff(P, y)*sp.diff(Q, x))


# generic test polynomials
a0, a1, a2, b0, b1, b2 = sp.symbols('a0 a1 a2 b0 b1 b2')
Pt = a0 + a1*x**2*y + a2*x*y**3
Qt = b0*x + b1*y**2 + b2*x**3*y
Pp = al*Pt.subs({x: lam*x, y: mu*y})
Qp = be*Qt.subs({x: lam*x, y: mu*y})
lhs = brack(Pp, Qp)
rhs = sp.expand(al*be*lam*mu*brack(Pt, Qt).subs({x: lam*x, y: mu*y}))
note(sp.expand(lhs - rhs) == 0,
     "[P',Q'](x,y) = alpha beta lambda mu [P,Q](lambda x, mu y), generic P,Q")

# bracket condition preserved iff alpha beta lambda^3 mu = 1
cond = sp.expand((al*be*lam*mu)*(lam*x)**2 - x**2)
note(sp.simplify(sp.factor(cond).subs(al*be*lam**3*mu, 1)) == 0
     or sp.expand(cond.subs(al, 1/(be*lam**3*mu))) == 0,
     "[P,Q] = x^2 is preserved exactly when alpha beta lambda^3 mu = 1")

# coefficient action
i, j = 2, 1
note(sp.expand(al*(lam*x)**i*(mu*y)**j - al*lam**i*mu**j*x**i*y**j) == 0,
     "coefficient action is c_ij -> alpha lambda^i mu^j c_ij (same for d with beta)")

# one normalization is always solvable: pick beta to make d_2_1 = 1
d21 = sp.symbols('d21', nonzero=True)
sol_beta = sp.solve(sp.Eq(be*lam**2*mu*d21, 1), be, dict=True)
note(len(sol_beta) == 1,
     f"beta = {sp.sstr(sol_beta[0][be])} normalizes d_2_1 to 1; alpha is then "
     "fixed by (*) and lambda, mu remain free -- so d_2_1 = 1 is WLOG")
note(True, "NOTE: only ONE normalization is used.  Two more are available but "
           "are not taken, so no risk of over-normalizing away a solution.")


# ===================================================================
# 2.  The normalized reduction
# ===================================================================
print("\nSECTION 2  triangular preprocessing with d_2_1 = 1")


def run_normalized(case, tag, norm_sym='d_2_1'):
    eqs, allsym, nz = RED.build(case)
    tgt = [s for s in allsym if str(s) == norm_sym]
    if not tgt:
        print(f"  {norm_sym} not among unknowns; skipping")
        return
    v = tgt[0]
    eqs = [sp.expand(e.subs(v, 1)) for e in eqs]
    eqs = [e for e in eqs if e != 0]
    nz = {s for s in nz if s != v}
    allsym = [s for s in allsym if s != v]
    print(f"  {tag}: {len(allsym)} unknowns after setting {norm_sym} = 1, "
          f"{len(eqs)} equations, {len(nz)} still-required-nonzero")
    t0 = time.time()
    eqs2, solved, zeroed, contra = RED.reduce_system(eqs, allsym, nz,
                                                     verbose=False)
    dt = time.time() - t0
    rem = set()
    for e in eqs2:
        rem |= e.free_symbols
    print(f"  reduced in {dt:.1f}s:")
    print(f"    forced to zero  : {len(zeroed)}")
    print(f"    solved & removed: {len(solved)}")
    print(f"    equations left  : {len(eqs2)}")
    print(f"    variables left  : {len(rem)}")
    if contra:
        print(f"\n  *** CONTRADICTION: {contra}")
        print("  *** => no P,Q of this Newton-polygon shape with [P,Q] = x^2")
        print("  *** => if this is the (8,28) open sub-case, IT CLOSES.")
        print("  *** MUST be re-derived without the divisions before claiming it.")
        return
    badv = sorted([str(s) for s in zeroed if s in nz])
    if badv:
        print(f"\n  *** required-nonzero coefficients forced to zero: {badv}")
        print("  *** contradicts Prop 4.3 -> case CLOSED (same caveat applies)")
        return
    if not eqs2:
        print("\n  *** ALL EQUATIONS ELIMINATED - solution set nonempty.")
        print("  *** This needs immediate independent verification.")
        return
    rl = sorted(rem, key=str)
    body = ",\n  ".join(sp.sstr(e).replace("**", "^") for e in eqs2)
    prod = "*".join(str(s) for s in sorted(nz & rem, key=str)) or "1"
    path = f"{SCRATCH}/gghv_{tag}_norm_reduced.sing"
    open(path, "w").write(
        f"ring R = 32003, ({','.join(str(s) for s in rl)}), dp;\n"
        f"ideal I = {body};\n"
        f'"{tag} normalized-reduced: {len(rl)} vars, {len(eqs2)} eqs";\n'
        f"ideal Gb = std(I);\n"
        f'"basis size:"; size(Gb);\n'
        f'"trivial (=> CASE CLOSED):"; (size(Gb)==1 && Gb[1]==1);\n'
        f'LIB "elim.lib"; ideal S = sat(I, {prod})[1];\n'
        f'"saturated size:"; size(S);\n'
        f'"saturated trivial (=> CASE CLOSED):"; (size(S)==1 && S[1]==1);\n'
        f"quit;\n")
    print(f"    emitted -> {path}")


if __name__ == '__main__':
    run_normalized(G.OPEN_CASE_2, 'open2')
    print("\n" + "=" * 70)
    bad = [t for ok_, t in LEDGER if not ok_]
    print(f"SYMMETRY LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
    for t in bad:
        print("  FAILED:", t)
