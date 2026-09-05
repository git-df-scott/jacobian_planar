"""Greedy exact solver for an extract system.

Runs the Q-cascade, and after each Q_k imposes the window constraints,
eliminating unknowns by back-substitution whenever a constraint is linear in
some unknown with a coefficient that is a nonzero constant (or a product of
units -- the vertex coefficients, which the system forces to be invertible).

Case splits are recorded, not swept under the rug.
"""
import sys, itertools
import sympy as sp
from sympy import expand, factor, Poly, together, simplify
sys.path.insert(0, '/home/user/jacobian_planar/x2')
import cascade as CA
import singspec


class Infeasible(Exception):
    pass


def units_stripped(g, units):
    """Divide out any factor that is forced nonzero (a unit)."""
    g = sp.factor(g)
    if g.is_Mul:
        keep = []
        for f in g.args:
            b, e = f.as_base_exp()
            if b in units or (b.is_Number and b != 0):
                continue
            keep.append(f)
        g = sp.Mul(*keep) if keep else sp.Integer(1)
    elif g in units:
        g = sp.Integer(1)
    return sp.expand(g)


def solve_system(spec, verbose=True, max_branch=0, log=print):
    c = spec['c']
    units = {c[i - 1] for i in spec['nd']}
    # normalisation: scale so that c_{p10} = 1  (allowed: (x,y,P) -> (lam x,
    # lam^-3 y, nu P) preserves {P,Q}=x^2 and acts on c_(a,j) by nu*lam^(a-3j))
    sub = {c[spec['p10'] - 1]: sp.Integer(1)}
    Pd = [{e: sp.expand(v.subs(sub)) for e, v in d.items()} for d in spec['Pd']]
    cas = CA.Cascade(Pd, spec['Rr'], sp.Integer(1))

    pending = []
    kmax = max(spec['windows']) if spec['windows'] else 0
    trace = []
    for m in range(0, kmax):
        k = m + 1
        Qk = cas.step(m)
        Qk = {e: sp.expand(v.subs(sub)) for e, v in Qk.items()}
        Qk = {e: v for e, v in Qk.items() if v != 0}
        cas.Q[k] = Qk
        win = spec['windows'].get(k, None) if k in spec['windows'] else 'free'
        if win == 'free':
            continue
        if win is None:
            bad = list(Qk.items())
        else:
            lo, hi = win
            bad = [(e, v) for e, v in Qk.items() if e < lo or e > hi]
        for e, v in bad:
            pending.append((k, e, v))
        # eliminate
        progress = True
        while progress:
            progress = False
            newpending = []
            for (kk, ee, g) in pending:
                g = sp.expand(g.subs(sub))
                if g == 0:
                    continue
                g = units_stripped(g, units)
                if g.is_Number:
                    raise Infeasible(f"Q{kk} coeff x^{ee} -> nonzero constant {g}")
                newpending.append((kk, ee, g))
            pending = newpending
            # find a linear-in-a-variable constraint with constant coeff
            for idx, (kk, ee, g) in enumerate(pending):
                p = sp.Poly(g, *[v for v in c if v not in sub])
                for v in p.gens:
                    d = sp.degree(g, v)
                    if d != 1:
                        continue
                    a = sp.expand(sp.diff(g, v))
                    if a.free_symbols:
                        continue
                    if a == 0:
                        continue
                    rest = sp.expand(g - a * v)
                    val = sp.expand(-rest / a)
                    sub[v] = val
                    for w in list(sub):
                        sub[w] = sp.expand(sub[w].subs({v: val}))
                    trace.append((kk, ee, v, val))
                    if verbose:
                        log(f"  Q{kk}[x^{ee}]  =>  {v} = {sp.simplify(val)}")
                    pending.pop(idx)
                    progress = True
                    break
                if progress:
                    break
        if verbose:
            free = [v for v in c if v not in sub]
            log(f"Q{k}: support={sorted(Qk)} win={win} "
                f"pending={len(pending)} free={len(free)}")
    return sub, pending, cas, units


def build_PQ(spec, sub, cas):
    P = {}
    for j, d in enumerate(spec['Pd']):
        for e, v in d.items():
            val = sp.expand(v.subs(sub))
            if val != 0:
                P[(e, j)] = val
    Q = {}
    for k, d in enumerate(cas.Q):
        for e, v in d.items():
            val = sp.expand(v.subs(sub))
            if val != 0:
                Q[(e, k)] = val
    return P, Q


if __name__ == '__main__':
    path = sys.argv[1]
    spec = singspec.parse(path)
    print(f"{path}: n={spec['n']} nd={spec['nd']}")
    try:
        sub, pending, cas, units = solve_system(spec)
    except Infeasible as e:
        print("INFEASIBLE:", e)
        sys.exit(0)
    free = [v for v in spec['c'] if v not in sub]
    print("free vars:", free)
    print("remaining constraints:", len(pending))
    for kk, ee, g in pending[:20]:
        print(f"  Q{kk}[x^{ee}]: {sp.factor(g)}")
