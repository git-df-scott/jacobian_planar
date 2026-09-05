"""night6 -- characteristic-zero library.

Mirrors night6/e3_final.py (the mod-p instrument) with exact arithmetic over
Q and over number fields K = Q[T]/(h):

    face equation  2*q*t' - 3*q'*t = u^2,  q on u^1..u^8, t on u^2..u^12,
                   gauge q_1 = q_8 = 1
    E3 operator    E3(p_,s_) = 3*p_'*t + 2*q'*s_ - p_*t' - 2*q*s_'

Every scalar here is an honest integer / rational; nothing is reduced modulo
anything.  Number-field elements are flint.fmpq_poly reduced mod h.
"""
import re
from fractions import Fraction as F
import flint

QIDX = list(range(1, 9))
TIDX = list(range(2, 13))
PIDX = list(range(1, 9))
SIDX = list(range(2, 13))


# ------------------------------------------------------- K = Q[T]/(h)
class Ext0:
    """number field Q[T]/(h), h irreducible over Q (or just squarefree)."""

    def __init__(self, h):
        self.h = h                      # flint.fmpq_poly, monic
        self.deg = h.degree()
        self.one = flint.fmpq_poly([1])
        self.zero = flint.fmpq_poly([])

    def c(self, k):
        if isinstance(k, int):
            return flint.fmpq_poly([k])
        k = F(k)
        return flint.fmpq_poly([flint.fmpq(k.numerator, k.denominator)])

    def gen(self):
        return flint.fmpq_poly([0, 1]) % self.h

    def mul(self, a, b):
        return (a * b) % self.h

    def add(self, a, b):
        return (a + b) % self.h

    def sub(self, a, b):
        return (a - b) % self.h

    def smul(self, k, a):
        return (self.c(k) * a) % self.h

    def inv(self, a):
        g, s, _ = a.xgcd(self.h)
        assert g.degree() == 0 and not g.is_zero(), "not invertible"
        return (s * flint.fmpq_poly([1]) / g.coeffs()[0]) % self.h

    def iszero(self, a):
        return a.is_zero()

    def show(self, a):
        return a.str().replace(' ', '') if not a.is_zero() else "0"

    def coeffs(self, a):
        """list of Fractions, low -> high, length = deg h"""
        cs = [F(int(c.p), int(c.q)) for c in a.coeffs()]
        return cs + [F(0)] * (self.deg - len(cs))


# --------------------------------------------- parsing Singular char-0 output
def parse_poly_A(s, nv=6):
    """Singular polynomial in A1..A6 with integer/rational coefficients."""
    s = s.replace(' ', '')
    out = {}
    for sign, body in re.findall(r'([+-]?)([^+-]+)', s):
        if not body:
            continue
        coef, mon = F(1), [0] * nv
        for part in body.split('*'):
            if re.fullmatch(r'\d+(/\d+)?', part):
                coef *= F(part)
            else:
                m = re.fullmatch(r'A(\d)(?:\^(\d+))?', part)
                assert m, (s, part)
                mon[int(m.group(1)) - 1] += int(m.group(2) or 1)
        if sign == '-':
            coef = -coef
        k = tuple(mon)
        out[k] = out.get(k, F(0)) + coef
    return {m: c for m, c in out.items() if c}


def split_shape(gb):
    """gb: list of dict-monomial polys in A1..A6 (lex, shape position).

    Returns (eliminant coeff list in A6, shape) where
    shape[k] = (num, den), both coefficient lists in A6, and
    A_k = -num(A6)/den(A6) for k = 1..5.
    """
    uni = [g for g in gb if all(m[i] == 0 for m in g for i in range(5))]
    assert len(uni) == 1, "no unique univariate element in the lex GB"
    U = uni[0]
    deg = max(m[5] for m in U)
    uc = [F(0)] * (deg + 1)
    for m, c in U.items():
        uc[m[5]] += c
    shape = {}
    for g in gb:
        if g is U:
            continue
        lin = [i for i in range(5) if any(m[i] for m in g)]
        assert len(lin) == 1, ("not in shape position", g)
        k = lin[0] + 1
        num, den = {}, {}
        for m, c in g.items():
            if m[k - 1]:
                assert m[k - 1] == 1, "not linear in A%d" % k
                den[m[5]] = den.get(m[5], F(0)) + c
            else:
                num[m[5]] = num.get(m[5], F(0)) + c
        nl = [F(0)] * (max(num or [0]) + 1)
        for e, c in num.items():
            nl[e] = c
        dl = [F(0)] * (max(den or [0]) + 1)
        for e, c in den.items():
            dl[e] = c
        shape[k] = (nl, dl)
    assert sorted(shape) == [1, 2, 3, 4, 5], sorted(shape)
    return uc, shape


def evalpoly(coeffs, x, K):
    r = K.zero
    for c in reversed(coeffs):
        r = K.add(K.mul(r, x), K.c(c))
    return r


# ------------------------------------------------ face point over K, char 0
def face_point0(K, x, shape):
    """rebuild (q,t) at the face solution with A_6 = q_7 = x in K."""
    A = {0: K.one, 7: K.one, 6: x}
    for k in range(1, 6):
        num, den = shape[k]
        A[k] = K.mul(K.sub(K.zero, evalpoly(num, x, K)),
                     K.inv(evalpoly(den, x, K)))
    B = {}
    for m in range(0, 11):
        acc = K.one if m == 0 else K.zero
        for i in range(1, min(m, 7) + 1):
            j = m - i
            if j > 10:
                continue
            c = 1 + 2 * j - 3 * i
            if c:
                acc = K.sub(acc, K.smul(c, K.mul(A[i], B[j])))
        B[m] = K.smul(F(1, 1 + 2 * m), acc)
    residual_rows = []
    for m in range(11, 18):
        acc = K.zero
        for i in range(0, 8):
            j = m - i
            if 0 <= j <= 10:
                c = 1 + 2 * j - 3 * i
                if c:
                    acc = K.add(acc, K.smul(c, K.mul(A[i], B[j])))
        if not K.iszero(acc):
            residual_rows.append(m)
    q = {i: A[i - 1] for i in QIDX}
    t = {j: B[j - 2] for j in TIDX}
    return q, t, residual_rows


def face_residual0(q, t, K):
    """residual of 2*q*t' - 3*q'*t - u^2, rebuilt from (q,t) directly."""
    res = {}
    for i, qi in q.items():
        for j, tj in t.items():
            c = 2 * j - 3 * i
            if c:
                k = i + j - 1
                res[k] = K.add(res.get(k, K.zero), K.smul(c, K.mul(qi, tj)))
    res[2] = K.sub(res.get(2, K.zero), K.one)
    return {k: v for k, v in res.items() if not K.iszero(v)}


# ---------------------------------------------------------- E3 over K, char 0
def e3_matrix0(q, t, K, s_min=2):
    sidx = list(range(s_min, 13))
    cols = [('p', i) for i in PIDX] + [('s', j) for j in sidx]
    ns = list(range(min(3, 1 + s_min), 21))
    M = [[K.zero] * len(cols) for _ in ns]
    for ri, n in enumerate(ns):
        for ci, (kind, k) in enumerate(cols):
            if kind == 'p':
                i, j = k, n - k
                if j in TIDX:
                    M[ri][ci] = K.smul(3 * i - j, t[j])
            else:
                j, i = k, n - k
                if i in QIDX:
                    M[ri][ci] = K.smul(2 * i - 2 * j, q[i])
    return M, cols, ns


def nullspace(M, K):
    m, n = len(M), len(M[0])
    A = [row[:] for row in M]
    piv, r = [], 0
    for c in range(n):
        pr = next((rr for rr in range(r, m) if not K.iszero(A[rr][c])), None)
        if pr is None:
            continue
        A[r], A[pr] = A[pr], A[r]
        iv = K.inv(A[r][c])
        A[r] = [K.mul(xx, iv) for xx in A[r]]
        for rr in range(m):
            if rr != r and not K.iszero(A[rr][c]):
                f = A[rr][c]
                A[rr] = [K.sub(a, K.mul(f, b)) for a, b in zip(A[rr], A[r])]
        piv.append(c)
        r += 1
        if r == m:
            break
    free = [c for c in range(n) if c not in piv]
    basis = []
    for fc in free:
        v = [K.zero] * n
        v[fc] = K.one
        for ri, pc in enumerate(piv):
            v[pc] = K.sub(K.zero, A[ri][fc])
        basis.append(v)
    return r, basis, piv, free


def apply_e30(pv, sv, q, t, K):
    res = {}
    for i, pi in pv.items():
        for j, tj in t.items():
            c = 3 * i - j
            if c:
                k = i + j - 1
                res[k] = K.add(res.get(k, K.zero), K.smul(c, K.mul(pi, tj)))
    for i, qi in q.items():
        for j, sj in sv.items():
            c = 2 * i - 2 * j
            if c:
                k = i + j - 1
                res[k] = K.add(res.get(k, K.zero), K.smul(c, K.mul(qi, sj)))
    return {k: v for k, v in res.items() if not K.iszero(v)}


def split(vec, cols):
    pv, sv = {}, {}
    for val, (kind, k) in zip(vec, cols):
        (pv if kind == 'p' else sv)[k] = val
    return pv, sv
