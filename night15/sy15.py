"""night15 -- (instrument reimplemented in-lane; night14 source read for reference) SY-certificate: Shpilrain-Yu gradient-row reduction over Q.

Instrument as specified for this lane:

  rows            : the ordered pair (P_x, P_y), coefficients in Q
  monomial order  : total degree, then lex on the x-exponent
  elementary step : f <- f - (LT(f)/LT(g)) * g   whenever LM(g) | LM(f)
  branching       : when LM(f) | LM(g) and LM(g) | LM(f) (i.e. LM(f)=LM(g))
                    both directions are explored
  memoization     : rows normalized to leading coefficient 1, unordered pair
  leaves          : a node with no applicable reduction

  verdict COORDINATE      : some node is {c, 0}, c a nonzero constant
  verdict NON_COORDINATE  : DAG exhausted, no such node

Every step strictly lowers the leading monomial of the reduced row in a
well-order, so the DAG is finite; a node budget guards pathological blowup.
"""

from fractions import Fraction as F
import pk15 as P14


def key(m):
    return (m[0] + m[1], m[0])


def LM(f):
    return max(f, key=key) if f else None


def divides(a, b):
    return a[0] <= b[0] and a[1] <= b[1]


def step(f, g):
    mf, mg = LM(f), LM(g)
    q = (mf[0] - mg[0], mf[1] - mg[1])
    c = F(f[mf]) / F(g[mg])
    out = dict(f)
    for (i, j), v in g.items():
        k = (i + q[0], j + q[1])
        out[k] = out.get(k, F(0)) - c * F(v)
    return {k: v for k, v in out.items() if v != 0}


def norm(f):
    if not f:
        return ()
    c = f[LM(f)]
    return tuple(sorted((k, F(v) / F(c)) for k, v in f.items()))


def nonzero_const(f):
    return len(f) == 1 and (0, 0) in f and f[(0, 0)] != 0


def certify(P, node_budget=300000):
    f0 = P14.clean(P14.dx(P))
    g0 = P14.clean(P14.dy(P))
    seen = set()
    stack = [(f0, g0)]
    nodes = 0
    leaves = 0
    while stack:
        f, g = stack.pop()
        a, b = norm(f), norm(g)
        mk = (a, b) if a <= b else (b, a)
        if mk in seen:
            continue
        seen.add(mk)
        nodes += 1
        if nodes > node_budget:
            return "BUDGET_EXHAUSTED", {"nodes": nodes, "leaves": leaves}
        if (not g and nonzero_const(f)) or (not f and nonzero_const(g)):
            return "COORDINATE", {"nodes": nodes, "leaves": leaves}
        kids = []
        if f and g:
            mf, mg = LM(f), LM(g)
            if divides(mg, mf):
                kids.append((step(f, g), g))
            if divides(mf, mg):
                kids.append((f, step(g, f)))
        if not kids:
            leaves += 1
        stack.extend(kids)
    return "NON_COORDINATE", {"nodes": nodes, "leaves": leaves}


VALIDATION = [
    # (label, polynomial, expected SY verdict, note)
    ("x",         {(1, 0): 1},                     "COORDINATE",     "coordinate"),
    ("y",         {(0, 1): 1},                     "COORDINATE",     "coordinate"),
    ("x + y^2",   {(1, 0): 1, (0, 2): 1},          "COORDINATE",     "coordinate"),
    ("x + x^2*y", {(1, 0): 1, (2, 1): 1},          "NON_COORDINATE", "non-coordinate, U-PASS"),
    ("y + x^3",   {(0, 1): 1, (3, 0): 1},          "COORDINATE",     "coordinate"),
    ("x*y",       {(1, 1): 1},                     "NON_COORDINATE", "non-coordinate, U-FAIL control"),
    ("x^2 + y^2", {(2, 0): 1, (0, 2): 1},          "NON_COORDINATE", "non-coordinate, U-FAIL control"),
    ("x + y^2 + 2*x^2*y + x^4",
     {(1, 0): 1, (0, 2): 1, (2, 1): 2, (4, 0): 1}, "COORDINATE",     "coordinate (triangular image)"),
]

if __name__ == "__main__":
    import time
    ok = True
    for lab, p, exp, note in VALIDATION:
        t = time.time()
        v, st = certify(P14.clean(p))
        good = (v == exp)
        ok &= good
        print("%-26s -> %-16s expected %-16s %s  nodes=%d leaves=%d %.3fs  [%s]"
              % (lab, v, exp, "ok" if good else "MISMATCH", st["nodes"], st["leaves"],
                 time.time() - t, note))
    print("ALL MATCH" if ok else "SOME MISMATCH")
