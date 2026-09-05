"""night12 v1 -- Shpilrain-Yu gradient-row reduction (the non-coordinate gate).

Rows are the gradient pair (P_x, P_y) over Q.  Monomial order: total degree,
then lex.  Elementary reduction

    f <- f - (LT(f)/LT(g)) * g      whenever LM(g) | LM(f)

and symmetrically.  Both directions apply only when LM(f) = LM(g); that is
the only place the search branches.  Normalized rows are memoized.
Termination: every reduction strictly decreases the leading monomial of the
row being reduced, in a well-order.

Leaf classification:
  reaching (c, 0) with c a nonzero constant  -> COORDINATE certificate
  a fully exhausted DAG with no such leaf    -> NON-COORDINATE certificate

All arithmetic is exact (ring: Q).
"""

from fractions import Fraction
import matekit as M


def key(mon):
    """total degree, then lex on (i, j).  Larger key = larger monomial."""
    return (mon[0] + mon[1], mon[0], mon[1])


def LM(f):
    return max(f, key=key) if f else None


def LT(f):
    m = LM(f)
    return (m, f[m]) if m is not None else (None, None)


def divides(a, b):
    return a[0] <= b[0] and a[1] <= b[1]


def reduce_step(f, g):
    """f <- f - (LT(f)/LT(g)) * g ; assumes LM(g) | LM(f)."""
    mf, cf = LT(f)
    mg, cg = LT(g)
    q = (mf[0] - mg[0], mf[1] - mg[1])
    c = Fraction(cf) / Fraction(cg)
    out = dict(f)
    for (i, j), v in g.items():
        k = (i + q[0], j + q[1])
        out[k] = out.get(k, Fraction(0)) + (-c) * Fraction(v)
    return {k: v for k, v in out.items() if v != 0}


def norm(f):
    """normalize a row to leading coefficient 1 (scaling is irrelevant to the
    reduction structure) and return a hashable form."""
    if not f:
        return ()
    m, c = LT(f)
    return tuple(sorted((k, Fraction(v) / Fraction(c)) for k, v in f.items()))


def is_nonzero_const(f):
    return len(f) == 1 and (0, 0) in f and f[(0, 0)] != 0


def certify(P, node_budget=200000):
    """Returns (verdict, stats).  verdict in
    {'COORDINATE', 'NON_COORDINATE', 'BUDGET_EXHAUSTED'}."""
    f0 = {k: Fraction(v) for k, v in M.dx(P).items()}
    g0 = {k: Fraction(v) for k, v in M.dy(P).items()}
    seen = set()
    stack = [(f0, g0)]
    nodes = 0
    leaves = 0
    while stack:
        f, g = stack.pop()
        nodes += 1
        if nodes > node_budget:
            return "BUDGET_EXHAUSTED", {"nodes": nodes, "leaves": leaves}
        # canonical (unordered) memo key
        a, b = norm(f), norm(g)
        mk = (a, b) if a <= b else (b, a)
        if mk in seen:
            continue
        seen.add(mk)
        # coordinate leaf: {c, 0} with c a nonzero constant
        if (not g and is_nonzero_const(f)) or (not f and is_nonzero_const(g)):
            return "COORDINATE", {"nodes": nodes, "leaves": leaves}
        children = []
        if f and g:
            mf, mg = LM(f), LM(g)
            if divides(mg, mf):
                children.append((reduce_step(f, g), g))
            if divides(mf, mg):
                children.append((f, reduce_step(g, f)))
        if not children:
            leaves += 1
        stack.extend(children)
    return "NON_COORDINATE", {"nodes": nodes, "leaves": leaves}


VALIDATION = [
    ("x", {(1, 0): 1}, "COORDINATE"),
    ("x + y^2", {(1, 0): 1, (0, 2): 1}, "COORDINATE"),
    ("x + x^2*y", {(1, 0): 1, (2, 1): 1}, "?"),
    ("x*y", {(1, 1): 1}, "NON_COORDINATE"),
    ("x^2*y", {(2, 1): 1}, "NON_COORDINATE"),
    ("x + y^126", {(1, 0): 1, (0, 126): 1}, "COORDINATE"),
    ("x^126 + y^127 + x^2*y^2", {(126, 0): 1, (0, 127): 1, (2, 2): 1}, "?"),
    ("x + y^2 + 2x^2y + x^4", {(1, 0): 1, (0, 2): 1, (2, 1): 2, (4, 0): 1}, "COORDINATE"),
]

if __name__ == "__main__":
    for name, P, expect in VALIDATION:
        v, st = certify(P)
        mark = "ok" if (expect == "?" or v == expect) else "MISMATCH"
        print("%-28s -> %-18s (brief label: %-16s) %s  nodes=%d leaves=%d"
              % (name, v, expect, mark, st["nodes"], st["leaves"]))
