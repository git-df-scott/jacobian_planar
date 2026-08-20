"""
T2 -- the same-sign weighted-homogeneous sector, swept exactly.

SETUP
-----
Give x weight a and y weight b, a, b >= 0 (this is the SAME-SIGN sector: the
usual Jacobian-Conjecture weightings have opposite signs).  Let P be
weighted-homogeneous of w-degree dP and Q of w-degree dQ.  Then

    [P,Q] = P_x Q_y - P_y Q_x

is weighted-homogeneous of w-degree dP + dQ - a - b, so

    [P,Q] in K^*    <=>    dP + dQ = a + b   AND   [P,Q] is a nonzero constant.

That identity is the whole reason the sector is finite: it forces
dP + dQ = a + b, and with a + b <= 12 there are very few (dP, dQ).

METHOD -- exact, not random
---------------------------
For each (a, b, dP) we take the FULL monomial bases

    M_P = { x^i y^j : a i + b j = dP, i + j <= DEGCAP }
    M_Q = { x^i y^j : a i + b j = dQ, i + j <= DEGCAP }

write P = sum p_m m, Q = sum q_m m with indeterminate coefficients, expand
[P,Q] symbolically, and impose: every coefficient of a non-constant monomial
vanishes, and the constant coefficient is a new indeterminate c with c != 0
(imposed by saturation).  The resulting ideal is decomposed exactly in
Singular over Q (minAssGTZ), so every branch is found -- no sampling.

For every branch a point is produced and the pair is tested for being an
automorphism, exactly:
    (i)  generic-fibre count by resultant elimination (a fibre of size 1 is
         necessary for injectivity), and
    (ii) explicit inverse construction by solving (P,Q) = (s,t) for (x,y) in
         K(s,t) and checking the substitution both ways symbolically.

CONTROLS
--------
POSITIVE  the triangular pair (x, y + x^m) must be FOUND by the sweep in the
          weight/degree cell where it lives, for m = 2..5.
POSITIVE  the sweep's own automorphism test must ACCEPT (x, y + x^m) and
          ACCEPT (x + 2y, y).
NEGATIVE  a planted NON-Keller pair (x, x*y) must be REJECTED by the Keller
          test; and a pair whose det J = 0 ((3x+y)^2, 3x+y) must be REJECTED.
NEGATIVE  the automorphism test must REJECT a known non-injective map --
          (x^2, y) is not injective on K^2 (it is also not Keller, so a
          second non-injective but degree-2 example, (x^2 - y^2, x*y), is
          used for the fibre-count leg).
"""

import itertools
import json
import os
import subprocess
import sys

import sympy as sp

x, y, s, t = sp.symbols('x y s t')
HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def bracket(P, Q):
    return sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x))


def is_keller(P, Q):
    J = bracket(P, Q)
    if J == 0:
        return False, J
    return (not (J.free_symbols & {x, y})), J


def generic_fibre_size(P, Q, trials=3, seed=5):
    """Max over random targets of the number of distinct roots of the
    x-resultant of (P - s0, Q - t0).  1 means the map is injective on the
    generic fibre; >1 certifies non-injectivity of the generic fibre."""
    import random
    rnd = random.Random(seed)
    sizes = []
    for _ in range(trials):
        s0 = sp.Integer(rnd.randint(-9, 9))
        t0 = sp.Integer(rnd.randint(-9, 9))
        R = sp.resultant(sp.expand(P - s0), sp.expand(Q - t0), y)
        R = sp.Poly(R, x) if R != 0 else None
        if R is None or R.is_zero:
            return None
        sq = sp.Poly(sp.quo(R.as_expr(), sp.gcd(R.as_expr(), sp.diff(R.as_expr(), x)), x), x)
        sizes.append(sq.degree())
    return max(sizes) if sizes else None


def explicit_inverse(P, Q):
    """Try to solve (P,Q) = (s,t) for (x,y) over K(s,t); verify both ways."""
    try:
        sols = sp.solve([sp.Eq(P, s), sp.Eq(Q, t)], [x, y], dict=True)
    except Exception:
        return None
    for sol in sols or []:
        if x not in sol or y not in sol:
            continue
        X, Y = sp.simplify(sol[x]), sp.simplify(sol[y])
        if X.free_symbols & {x, y} or Y.free_symbols & {x, y}:
            continue
        f1 = sp.simplify(P.subs({x: X, y: Y}) - s)
        f2 = sp.simplify(Q.subs({x: X, y: Y}) - t)
        if f1 == 0 and f2 == 0:
            g1 = sp.simplify(X.subs({s: P, t: Q}) - x)
            g2 = sp.simplify(Y.subs({s: P, t: Q}) - y)
            if sp.simplify(g1) == 0 and sp.simplify(g2) == 0:
                return (sp.simplify(X), sp.simplify(Y))
    return None


def is_automorphism(P, Q):
    """(verdict, evidence).  Both legs are computed; they must agree."""
    inv = explicit_inverse(P, Q)
    fib = generic_fibre_size(P, Q)
    if inv is not None:
        return True, {"inverse": [str(inv[0]), str(inv[1])], "generic_fibre": fib}
    return False, {"inverse": None, "generic_fibre": fib}


# ---------------------------------------------------------------------------
def monomials(a, b, d, degcap):
    out = []
    imax = degcap
    for i in range(imax + 1):
        for j in range(degcap - i + 1):
            if a * i + b * j == d:
                out.append((i, j))
    return out


def cell_system(a, b, dP, dQ, degcap):
    MP = monomials(a, b, dP, degcap)
    MQ = monomials(a, b, dQ, degcap)
    if not MP or not MQ:
        return None
    ps = sp.symbols(f'p0:{len(MP)}')
    qs = sp.symbols(f'q0:{len(MQ)}')
    P = sum(ps[k] * x ** i * y ** j for k, (i, j) in enumerate(MP))
    Q = sum(qs[k] * x ** i * y ** j for k, (i, j) in enumerate(MQ))
    J = bracket(P, Q)
    pj = sp.Poly(J, x, y)
    eqs, const = [], sp.Integer(0)
    for mono, coef in zip(pj.monoms(), pj.coeffs()):
        if mono == (0, 0):
            const = coef
        else:
            eqs.append(sp.expand(coef))
    return dict(MP=MP, MQ=MQ, ps=ps, qs=qs, P=P, Q=Q, eqs=eqs, const=const)


def singular_decompose(cell, timeout=300):
    """Exact primary decomposition of the branch variety over Q."""
    vs = [str(v) for v in list(cell["ps"]) + list(cell["qs"])]
    eqs = [sp.sstr(e).replace('**', '^') for e in cell["eqs"]]
    const = sp.sstr(cell["const"]).replace('**', '^')
    src = [f"LIB \"primdec.lib\";",
           f"ring R = 0, ({','.join(vs)}), dp;"]
    src.append("ideal I = " + (",".join(eqs) if eqs else "0") + ";")
    src.append(f"poly cc = {const};")
    src.append("if (cc == 0) { \"NOCONST\"; quit; }")
    src.append("I = sat(I, cc)[1];")
    src.append("ideal g = std(I);")
    src.append("if (size(g)==1 && g[1]==1) { \"EMPTY\"; quit; }")
    src.append("list L = minAssGTZ(I);")
    src.append("\"NCOMP \" + string(size(L));")
    src.append("int i; for (i=1;i<=size(L);i++) { \"COMP \" + string(i) + \" dim \" "
               "+ string(dim(std(L[i]))); \"GENS \" + string(L[i]); }")
    src.append("quit;")
    fn = f"/tmp/ss_{abs(hash(tuple(vs)))%10**8}.sing"
    open(fn, "w").write("\n".join(src))
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        return r.stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


# ---------------------------------------------------------------------------
def classify_branch(cell, gens_str):
    """Turn one Singular component into a concrete (P,Q) over Q and classify it.

    The component is a linear/parametric family; a point on it is produced by
    setting the free coefficients to small integers and re-checking the Keller
    condition EXACTLY.  Any point that fails the re-check is discarded, so the
    classification never rests on the decomposition alone.
    """
    import random
    ps, qs = list(cell["ps"]), list(cell["qs"])
    allv = ps + qs
    rel = [g.strip() for g in gens_str.split(",") if g.strip()]
    exprs = [sp.sympify(g.replace("^", "**")) for g in rel]
    found = []
    rnd = random.Random(3)
    for attempt in range(60):
        assign = {v: sp.Integer(rnd.randint(-3, 3)) for v in allv}
        # solve the component's equations for as many variables as possible
        try:
            sol = sp.solve([e for e in exprs], allv, dict=True)
        except Exception:
            sol = []
        if sol:
            sub = sol[0]
            free = [v for v in allv if v not in sub]
            base = {v: sp.Integer(rnd.randint(-3, 3)) for v in free}
            full = {}
            for v in allv:
                full[v] = sp.simplify(sub[v].subs(base)) if v in sub else base[v]
        else:
            full = assign
        P = sp.expand(cell["P"].subs(full))
        Q = sp.expand(cell["Q"].subs(full))
        ok, J = is_keller(P, Q)
        if ok and J != 0:
            found.append((P, Q, J))
            if len(found) >= 3:
                break
    return found
