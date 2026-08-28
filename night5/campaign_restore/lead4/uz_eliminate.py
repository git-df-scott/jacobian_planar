#!/usr/bin/env python3
"""Triangular elimination of the Q-side unknowns in the (u,z) system.

At order n the equations of z-degree 4,3,2,1 have the shape

    (3-2n) t_n + (older) = 0
    (2-2n) s_n + (older) = 0
    (1-2n) r_n + (older) = 0
    ( -2n) g_n + (older) = 0

(the diagonal coefficients come from the a=1 term  A_1 B_n' - n A_1' B_n
with A_1's leading coefficient q_1 = 1), so g_n, r_n, s_n, t_n are uniquely
determined for n = 1..12.  The z-degree 0 equation at order n involves no
order-n Q unknown at all, hence is an OBSTRUCTION on the P-side
coefficients; so are all five equations at orders n = 13..19 (no Q unknowns
are left there).

That leaves an exact system of obstructions in the 23 unknowns
f1..f8, p1..p8, q2..q8 (q1 = 1 by the scaling gauge).
"""
import sys
import time
from fractions import Fraction

from uz_system import (NVARS_P, PVARS, PIDX, QVARS, build_equations,
                       padd, pscal, pmul, pmulvar, pstr)


def run(mod=None, fixed=None, verbose=True, maxorder=19):
    """fixed: dict P-var name -> integer value substituted from the start."""
    fixed = dict(fixed or {})
    eqs, const = build_equations()
    sub = {}          # Q-var -> polynomial in P-vars
    obstructions = []

    def one():
        return {(0,) * NVARS_P: (1 % mod) if mod else Fraction(1)}

    def atomA_apply(poly, atom):
        """multiply poly by the A-atom"""
        if atom[0] == "c":
            return pscal(poly, atom[1], mod)
        nm = atom[1]
        if nm in fixed:
            return pscal(poly, fixed[nm], mod)
        return pmulvar(poly, nm, mod)

    def value(key, skip=None):
        """evaluate equation `key`, treating Q-var `skip` as absent;
        return (poly, coefficient-poly-of-skip)"""
        tot = {}
        coef = {}
        c0 = const[key]
        if c0:
            tot = padd(tot, pscal(one(), c0, mod), mod)
        for c, x, y in eqs[key]:
            qname = y[1]
            if qname == skip:
                coef = padd(coef, atomA_apply(pscal(one(), c, mod), x), mod)
                continue
            if qname not in sub:
                raise RuntimeError(f"unsubstituted Q-var {qname} in {key}")
            term = pscal(sub[qname], c, mod)
            term = atomA_apply(term, x)
            tot = padd(tot, term, mod)
        return tot, coef

    def inv(c):
        if mod:
            return pow(c % mod, mod - 2, mod)
        return Fraction(1, c)

    t0 = time.time()
    for n in range(1, maxorder + 1):
        # solve for the order-n Q unknowns
        plan = []
        if n >= 2:
            plan = [(4, f"t{n}", 3 - 2 * n), (3, f"s{n}", 2 - 2 * n),
                    (2, f"r{n}", 1 - 2 * n), (1, f"g{n}", -2 * n)]
        elif n == 1:
            plan = [(2, "r1", 1 - 2 * n), (1, "g1", -2 * n)]
        if n > 12:
            plan = []
        for k, var, diag in plan:
            rest, coef = value((n, k), skip=var)
            # the coefficient of `var` must be the constant `diag`
            cc = coef.get((0,) * NVARS_P, 0)
            if len(coef) != 1 or (cc - diag) % (mod if mod else 1) != 0:
                if mod is None and coef != {(0,) * NVARS_P: Fraction(diag)}:
                    raise RuntimeError(f"unexpected pivot at {(n,k)}: "
                                       f"{pstr(coef)} vs {diag}")
            sub[var] = pscal(rest, -inv(diag) if not mod
                             else (-inv(diag)) % mod, mod)
            if mod:
                sub[var] = {m: c % mod for m, c in sub[var].items() if c % mod}
        # the leftover equations at this order are obstructions
        ks = [0] if n <= 12 else [0, 1, 2, 3, 4]
        for k in ks:
            val, _ = value((n, k))
            if val:
                obstructions.append(((n, k), val))
        if verbose:
            sz = sum(len(sub[v]) for v in sub)
            print(f"  order {n:2d}: solved {[v for _,v,_ in plan]}, "
                  f"obstructions so far {len(obstructions)}, "
                  f"total Q-terms {sz}, {time.time()-t0:.1f}s", flush=True)
    return obstructions, sub


if __name__ == "__main__":
    mod = None
    if len(sys.argv) > 1 and sys.argv[1] != "QQ":
        mod = int(sys.argv[1])
    fixed = {}
    for a in sys.argv[2:]:
        k, v = a.split("=")
        fixed[k] = int(v)
    print(f"modulus = {mod or 'QQ (exact)'}   fixed = {fixed}")
    obs, sub = run(mod=mod, fixed=fixed)
    print(f"\n{len(obs)} obstruction polynomials")
    for key, o in obs[:6]:
        print(f"  {key}: {len(o)} terms   {pstr(o)[:200]}")
