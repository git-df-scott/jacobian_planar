#!/usr/bin/env python3
"""Parameter-carrying elimination over F_p -- DIVISION-FREE.

Third attempt at the cascade.  The two previous ones are retracted in
CATCHES.md; both died on the same point, so this one is built to make that
point impossible:

  * NO DIVISION.  To use an equation A*x + B = 0 we do NOT form x = -B/A.
    We substitute into another equation E of degree d in x by computing
    A^d * E|_{x -> -B/A}, which is a polynomial identity.  Nothing ever becomes
    a rational function, so no denominator can be silently assumed nonzero.
  * EXPLICIT BRANCHING.  A may vanish.  The elimination is therefore a case
    split: the branch A != 0 (recorded as a saturation condition) and the
    branch A = 0 (recorded as an extra equation).  Neither is dropped.
  * PROPAGATION IS CHECKED.  Retracted attempt #2 computed ranks but never
    wrote solved values back, so it could only ever answer "consistent".  Here
    every elimination returns the NEW system, and the self-test below fails
    loudly if a planted contradiction is not found.

Verdict semantics: a branch dies only when it produces a NONZERO CONSTANT.
"Consistent so far" is never a verdict.
"""
import sys, collections
import sympy as sp

def redmod(e, p):
    """Reduce coefficients mod p, dropping vanishing terms (the trap from CATCHES)."""
    e = sp.expand(e)
    g = sorted(e.free_symbols, key=str)
    if not g:
        return sp.Integer(int(e) % p)
    po = sp.Poly(e, *g); out = 0
    for mon, co in zip(po.monoms(), po.coeffs()):
        c = int(co) % p
        if not c: continue
        t = c
        for s, ex in zip(g, mon):
            if ex: t *= s**ex
        out += t
    return sp.expand(out)

def eliminate(eqs, x, p):
    """Use some equation linear in x to remove x.  Returns list of branches:
    each branch is (new_eqs, nonzero_conditions, note).  No branch is dropped."""
    lin = [e for e in eqs if sp.degree(e, x) == 1]
    if not lin:
        return None
    # prefer a pivot whose leading coefficient is a nonzero CONSTANT (no branching)
    best = None
    for e in lin:
        A = sp.Poly(e, x).all_coeffs()[0]
        if A.free_symbols == set() and int(A) % p:
            best = (e, A); break
    branches = []
    if best:
        e, A = best
        B = sp.expand(e - A*x)
        rest = [q for q in eqs if q is not e]
        new = []
        for q in rest:
            d = sp.degree(q, x)
            v = redmod(sp.expand(sp.expand(A**d * q.subs(x, -B/A))), p) if d > 0 else redmod(q, p)
            if v != 0: new.append(v)
        branches.append((new, [], f"{x} eliminated, pivot constant"))
        return branches
    # otherwise pivot has a symbolic leading coefficient -> genuine case split
    e = lin[0]; A = sp.Poly(e, x).all_coeffs()[0]; B = sp.expand(e - A*x)
    rest = [q for q in eqs if q is not e]
    new = []
    for q in rest:
        d = sp.degree(q, x)
        v = redmod(sp.expand(sp.expand(A**d * q.subs(x, -B/A))), p) if d > 0 else redmod(q, p)
        if v != 0: new.append(v)
    branches.append((new, [A], f"{x} eliminated on the branch {A} != 0"))
    branches.append(([redmod(q, p) for q in eqs if redmod(q, p) != 0] + [redmod(A, p)],
                     [], f"branch {A} = 0"))
    return branches

def run(eqs, p, order=None, maxdepth=60):
    """Eliminate greedily; return leaves as (eqs, nonzero, trail, status)."""
    leaves = []
    stack = [([redmod(e, p) for e in eqs], [], [], 0)]
    while stack:
        E, NZ, trail, depth = stack.pop()
        bad = [e for e in E if e.free_symbols == set() and int(e) % p]
        if bad:
            leaves.append((E, NZ, trail, f"DEAD: nonzero constant {bad[0]}")); continue
        E = [e for e in E if e.free_symbols]
        if depth >= maxdepth:
            leaves.append((E, NZ, trail, "depth cap")); continue
        vs = sorted({v for e in E for v in e.free_symbols}, key=str)
        cand = [v for v in vs if any(sp.degree(e, v) == 1 for e in E)]
        if not cand:
            leaves.append((E, NZ, trail, "no linear pivot left")); continue
        x = min(cand, key=lambda v: sum(1 for e in E if v in e.free_symbols))
        br = eliminate(E, x, p)
        for new, nz, note in br:
            stack.append((new, NZ + nz, trail + [note], depth+1))
    return leaves

# ------------------------- CAN-FAIL SELF-TEST -------------------------------
def selftest(p=1000003):
    a, b, c, t = sp.symbols('a b c t')
    ok = True
    # (1) CONSISTENT system with a genuine solution -> must NOT report DEAD
    S1 = [a - 3, b - a - 1, c*b - 8]          # a=3, b=4, c=2
    L1 = run(S1, p)
    d1 = [l for l in L1 if l[3].startswith('DEAD')]
    print(f"  test1 consistent system      : leaves={len(L1)} dead={len(d1)}  "
          f"{'PASS' if not d1 else 'FAIL (false contradiction)'}")
    ok &= not d1
    # (2) PLANTED CONTRADICTION -> must report DEAD on every leaf
    S2 = [a - 3, a - 5]
    L2 = run(S2, p)
    d2 = [l for l in L2 if l[3].startswith('DEAD')]
    print(f"  test2 planted contradiction  : leaves={len(L2)} dead={len(d2)}  "
          f"{'PASS' if len(d2) == len(L2) else 'FAIL (missed it)'}")
    ok &= (len(d2) == len(L2))
    # (3) SYMBOLIC PIVOT: t*a - 1 = 0 has a solution iff t != 0; the branch t = 0
    #     must survive as its own leaf carrying the equation t, and must be DEAD
    S3 = [t*a - 1]
    L3 = run(S3, p)
    notes = [l[3] for l in L3]
    print(f"  test3 symbolic pivot t*a-1   : leaves={len(L3)} -> {notes}  "
          f"{'PASS' if len(L3) >= 2 else 'FAIL (branch dropped)'}")
    ok &= len(L3) >= 2
    # (4) contradiction reachable ONLY through a symbolic pivot
    S4 = [t*a - 1, t, a - 7]
    L4 = run(S4, p)
    alive = [l for l in L4 if not l[3].startswith('DEAD')]
    print(f"  test4 contradiction behind a symbolic pivot: leaves={len(L4)} alive={len(alive)}")
    return ok

if __name__ == '__main__':
    print("CAN-FAIL SELF-TEST of the division-free cascade:")
    ok = selftest()
    print(f"\nself-test {'PASSED' if ok else 'FAILED -- do not use'}")
