"""night10 -- ramified local rings and the step calculus.

Base rings used here, always labelled:
  Z                     the integers (the system's own base ring)
  F_2                   residue field
  O2 = Z[pi]/(pi^2 - 2)  totally ramified quadratic, w(pi)=1, w(2)=2
  O3 = Z[pi]/(pi^3 - 2)  totally ramified cubic,     w(pi)=1, w(2)=3
"""

import system as S

N = S.N
M = S.M


# ---------------- O_e = Z[pi]/(pi^e - 2) ----------------

class Oram:
    """Elements are tuples of length e of integers: (c0,...,c_{e-1}) = sum c_k pi^k."""

    def __init__(self, e):
        self.e = e

    def zero(self):
        return (0,) * self.e

    def from_int(self, n):
        return (int(n),) + (0,) * (self.e - 1)

    def add(self, u, v):
        return tuple(a + b for a, b in zip(u, v))

    def sub(self, u, v):
        return tuple(a - b for a, b in zip(u, v))

    def mul(self, u, v):
        e = self.e
        out = [0] * e
        for i, a in enumerate(u):
            if a == 0:
                continue
            for j, b in enumerate(v):
                if b == 0:
                    continue
                k = i + j
                if k < e:
                    out[k] += a * b
                else:
                    out[k - e] += 2 * a * b   # pi^e = 2
        return tuple(out)

    def pi(self):
        z = [0] * self.e
        z[1 % self.e] = 1
        if self.e == 1:
            raise ValueError
        return tuple(z)

    def mul_pi(self, u):
        e = self.e
        out = [0] * e
        for i, a in enumerate(u):
            k = i + 1
            if k < e:
                out[k] += a
            else:
                out[k - e] += 2 * a
        return tuple(out)

    def is_zero(self, u):
        return all(a == 0 for a in u)

    def w(self, u, cap=10 ** 6):
        """integer valuation with w(pi)=1, w(2)=e.  Returns cap for 0."""
        e = self.e
        best = cap
        for k, a in enumerate(u):
            if a == 0:
                continue
            v = 0
            while a % 2 == 0:
                a //= 2
                v += 1
            best = min(best, k + e * v)
        return best

    def div_pi(self, u):
        """exact division by pi; requires w(u) >= 1."""
        e = self.e
        c0 = u[0]
        assert c0 % 2 == 0, "div_pi: not divisible by pi"
        out = [0] * e
        for k in range(1, e):
            out[k - 1] = u[k]
        out[e - 1] += c0 // 2
        return tuple(out)

    def div_pi_pow(self, u, m):
        for _ in range(m):
            u = self.div_pi(u)
        return u

    def residue(self, u):
        """image in F_2 = O/(pi)"""
        return u[0] % 2

    def from_intvec(self, v):
        return [self.from_int(t) for t in v]


O2 = Oram(2)
O3 = Oram(3)


# ---------------- F_2 linear algebra ----------------

def rref_mod2(rows, ncols):
    rows = [list(r) for r in rows]
    piv = []
    r = 0
    for c in range(ncols):
        p = None
        for i in range(r, len(rows)):
            if rows[i][c] & 1:
                p = i
                break
        if p is None:
            continue
        rows[r], rows[p] = rows[p], rows[r]
        for i in range(len(rows)):
            if i != r and rows[i][c] & 1:
                rows[i] = [(a ^ b) for a, b in zip(rows[i], rows[r])]
        piv.append(c)
        r += 1
        if r == len(rows):
            break
    return rows[:r], piv


def kernel_mod2(Jm):
    """kernel of the M x N matrix Jm over F_2, as a list of basis vectors."""
    R, piv = rref_mod2(Jm, N)
    free = [c for c in range(N) if c not in piv]
    basis = []
    for f in free:
        v = [0] * N
        v[f] = 1
        for i, c in enumerate(piv):
            v[c] = R[i][f] & 1
        basis.append(v)
    return basis


def in_column_space_mod2(Jm, b):
    """is b in the F_2-column space of Jm?  Also returns a particular solution."""
    aug = [list(Jm[k]) + [b[k] & 1] for k in range(len(Jm))]
    R, piv = rref_mod2(aug, N + 1)
    if N in piv:
        return False, None
    sol = [0] * N
    for i, c in enumerate(piv):
        sol[c] = R[i][N] & 1
    return True, sol


def rank_mod2(rows, ncols):
    R, piv = rref_mod2(rows, ncols)
    return len(piv)


def span_mod2(basis):
    out = []
    n = len(basis)
    for mask in range(1 << n):
        v = [0] * N
        for i in range(n):
            if mask >> i & 1:
                v = [a ^ b for a, b in zip(v, basis[i])]
        out.append(tuple(v))
    return out


# ---------------- generic ladder over O_e ----------------

def residual(x0, ds, R):
    """r(x0 + sum_{k>=1} pi^k d_k) evaluated exactly in O_e.
    x0 integer vector, ds a dict k -> integer vector."""
    v = R.from_intvec(x0)
    for k, d in ds.items():
        t = R.from_intvec(d)
        for _ in range(k):
            t = [R.mul_pi(u) for u in t]
        v = [R.add(a, b) for a, b in zip(v, t)]
    return S.r_eval(v, R)


def wmin(vec, R, cap=10 ** 6):
    return min(R.w(u, cap) for u in vec)
