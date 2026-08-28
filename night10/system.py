"""night10 -- the (K)+(C2) system r: Z^9 -> Z^15, built from scratch in-lane.

Coordinate order (night8 E0 order):
    (a_1_0, a_2_1, a_4_0, a_6_2, b_0_1, b_5_0, b_6_1, b_7_2, b_8_3)

P = a_1_0 x + a_2_1 x^2 y + a_4_0 x^4 + a_6_2 x^6 y^2
Q = b_0_1 y + b_5_0 x^5 + b_6_1 x^6 y + b_7_2 x^7 y^2 + b_8_3 x^8 y^3

Rows: every coefficient of  P_x Q_y - P_y Q_x - 1  over Z, then
      C2_P = P(0,1) - P(1,0), C2_Q = Q(0,1) - Q(1,0).

The system is quadratic:  r(v) = c + L v + Q2(v),  Q2 the vector of pure
quadratic forms.  We export c, L, and the quadratic coefficient dicts so the
map can be evaluated over ANY commutative ring (used for Z[pi]/(pi^2-2) and
Z[pi]/(pi^3-2)).

Base ring of the system itself: Z.
"""

import sympy as sp

VARS = ["a_1_0", "a_2_1", "a_4_0", "a_6_2", "b_0_1", "b_5_0", "b_6_1", "b_7_2", "b_8_3"]
N = 9

P_SUPPORT = [(1, 0), (2, 1), (4, 0), (6, 2)]
Q_SUPPORT = [(0, 1), (5, 0), (6, 1), (7, 2), (8, 3)]


def build():
    x, y = sp.symbols("x y")
    a = sp.symbols(VARS)
    P = sum(a[i] * x ** e[0] * y ** e[1] for i, e in enumerate(P_SUPPORT))
    Q = sum(a[4 + i] * x ** e[0] * y ** e[1] for i, e in enumerate(Q_SUPPORT))

    Jac = sp.expand(sp.diff(P, x) * sp.diff(Q, y) - sp.diff(P, y) * sp.diff(Q, x) - 1)
    poly = sp.Poly(Jac, x, y)

    rows = []          # list of (label, sympy expression in a)
    for mono, coeff in sorted(poly.terms(), key=lambda t: (-t[0][0], -t[0][1])):
        e = sp.expand(coeff)
        if e != 0:
            rows.append(("K(%d,%d)" % mono, e))

    rows.append(("C2_P", sp.expand(P.subs({x: 0, y: 1}) - P.subs({x: 1, y: 0}))))
    rows.append(("C2_Q", sp.expand(Q.subs({x: 0, y: 1}) - Q.subs({x: 1, y: 0}))))

    labels = [r[0] for r in rows]
    exprs = [r[1] for r in rows]
    M = len(rows)

    const = []
    lin = []
    quad = []          # per row: dict (i,j) i<=j -> int coeff
    for e in exprs:
        p = sp.Poly(e, *a)
        c0 = 0
        Lrow = [0] * N
        qd = {}
        for mono, cf in p.terms():
            cf = int(cf)
            deg = sum(mono)
            idx = [i for i, m in enumerate(mono) for _ in range(m)]
            if deg == 0:
                c0 = cf
            elif deg == 1:
                Lrow[idx[0]] = cf
            elif deg == 2:
                qd[(min(idx), max(idx))] = cf
            else:
                raise AssertionError("row is not quadratic: %s" % e)
        const.append(c0)
        lin.append(Lrow)
        quad.append(qd)
    return dict(labels=labels, M=M, const=const, lin=lin, quad=quad, exprs=exprs,
                P=P, Q=Q, jac=Jac)


SYS = build()
LABELS = SYS["labels"]
M = SYS["M"]
CONST = SYS["const"]
LIN = SYS["lin"]
QUAD = SYS["quad"]


# ---------- ring-generic evaluation ----------
# A "ring" is a tiny object with zero(), from_int(n), add, sub, mul.

class ZRing:
    def zero(self):
        return 0

    def from_int(self, n):
        return int(n)

    def add(self, u, v):
        return u + v

    def sub(self, u, v):
        return u - v

    def mul(self, u, v):
        return u * v


ZZ = ZRing()


def r_eval(v, R=ZZ):
    """r(v) for a length-9 vector v of ring elements."""
    out = []
    for k in range(M):
        acc = R.from_int(CONST[k])
        for i in range(N):
            if LIN[k][i]:
                acc = R.add(acc, R.mul(R.from_int(LIN[k][i]), v[i]))
        for (i, j), cf in QUAD[k].items():
            acc = R.add(acc, R.mul(R.from_int(cf), R.mul(v[i], v[j])))
        out.append(acc)
    return out


def jac_eval(v, R=ZZ):
    """Dr(v): M x N matrix of ring elements."""
    J = []
    for k in range(M):
        row = [R.from_int(LIN[k][i]) for i in range(N)]
        for (i, j), cf in QUAD[k].items():
            if i == j:
                row[i] = R.add(row[i], R.mul(R.from_int(2 * cf), v[i]))
            else:
                row[i] = R.add(row[i], R.mul(R.from_int(cf), v[j]))
                row[j] = R.add(row[j], R.mul(R.from_int(cf), v[i]))
        J.append(row)
    return J


def Q2(d, R=ZZ):
    """The vector of pure quadratic forms, B(d,d)."""
    out = []
    for k in range(M):
        acc = R.zero()
        for (i, j), cf in QUAD[k].items():
            acc = R.add(acc, R.mul(R.from_int(cf), R.mul(d[i], d[j])))
        out.append(acc)
    return out


def Bpol(d, e, R=ZZ):
    """Integral polarization  Bpol(d,e) = Q2(d+e) - Q2(d) - Q2(e).
    (This is 2*B_sym(d,e); it is the cross-term that appears in the expansion.)"""
    out = []
    for k in range(M):
        acc = R.zero()
        for (i, j), cf in QUAD[k].items():
            if i == j:
                acc = R.add(acc, R.mul(R.from_int(2 * cf), R.mul(d[i], e[i])))
            else:
                t = R.add(R.mul(d[i], e[j]), R.mul(d[j], e[i]))
                acc = R.add(acc, R.mul(R.from_int(cf), t))
        out.append(acc)
    return out
