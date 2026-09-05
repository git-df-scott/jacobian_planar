#!/usr/bin/env python3
"""Independent kernel-retaining local recurrence for the collision (4,6) ribbon.

Structure (re-derived from scratch and cross-checked against
``ribbon46_reduction.py``'s exact objects):

    P = p0 + p1 y + p2 y^2 + p3 y^3 + y^4 ,   Q = q0 + ... + q5 y^5 + c y^6

The y^{j+3} Jacobian row gives, for j = 5,4,3,2,1,0,

    4 q_j' = sum_{i=0..3, k=j+4-i <= 6} [ k P_i' q_k - i P_i q_k' ]

and the three surviving rows are

    E2 = 3 p0' q3 + 2 p1' q2 - p1 q2' + p2' q1 - 2 p2 q1' - 3 p3 q0'
    E1 = 2 p0' q2 +   p1' q1 - p1 q1' - 2 p2 q0'
    E0 =   p0' q1 - p1 q0'

with E2 = E1 = 0, E0 = 1.  Locally p0 = x^84 - x, which for rungs n < 83 is
just p0 = -x (dp0[0] = -1, dp0[m] = 0 otherwise).

Rung bookkeeping (all verified below, not assumed):
  n = 0 : A1, A2, A3 determined; u = p1[1], v = p2[1], w = p3[1] FREE.
  n = 1 : A5 determined from E0[1] (coefficient 5/4); p1[2], p2[2] from
          E1[1], E2[1]; p3[2] retained as kernel.
  n >= 2: E0[n] is linear in p3[n] with pivot (n+1)*u/4; E1[n] is linear in
          p1[n+1] with coefficient -(n+1); E2[n] is then linear in p2[n+1]
          with coefficient -(n+1).  p3[n+1] is the next retained kernel.

So the whole u != 0 sub-chart is a 3-parameter shooting problem in (u, v, w).
A0 and A4 provably do not occur in E2, E1, E0 (checked against sympy), so they
are set to 0.  c is gauge-fixed to 1 exactly as in the prior scripts.
"""
import numpy as np
from fractions import Fraction


# --------------------------------------------------------------------------
# Coefficient rings.  Both expose arrays of shape (size, npts).
# --------------------------------------------------------------------------
class QQRing:
    """Exact rationals; npts = 1."""

    name = "QQ"

    def __init__(self):
        self.npts = 1

    def zeros(self, size):
        a = np.empty((size, 1), dtype=object)
        a[:] = Fraction(0)
        return a

    def const(self, k):
        a = np.empty(1, dtype=object)
        a[0] = Fraction(k)
        return a

    def red(self, a):
        return a

    def invint(self, n):
        n = int(n)
        cached = getattr(self, "_ic", None)
        if cached is None:
            cached = self._ic = {}
        if n not in cached:
            a = np.empty(1, dtype=object)
            a[0] = Fraction(1, n)
            cached[n] = a
        return cached[n]

    def invarr(self, a):
        out = np.empty_like(a)
        for i in range(len(a)):
            out[i] = Fraction(1) / a[i]
        return out

    def conv(self, A, B, k):
        return (A[: k + 1] * B[k::-1]).sum(axis=0)

    def is_zero(self, a):
        return np.array([x == 0 for x in a])


class FpRing:
    """F_p, vectorised over npts parameter points."""

    def __init__(self, p, npts):
        self.p = int(p)
        self.npts = int(npts)
        self.name = "F_%d" % p

    def zeros(self, size):
        return np.zeros((size, self.npts), dtype=np.int64)

    def const(self, k):
        return np.full(self.npts, int(k) % self.p, dtype=np.int64)

    def red(self, a):
        return a % self.p

    def invint(self, n):
        key = int(n)
        cached = getattr(self, "_ic", None)
        if cached is None:
            cached = self._ic = {}
        if key not in cached:
            r = key % self.p
            if r == 0:
                raise ZeroDivisionError(
                    "integer %d vanishes mod %d: rung is modularly degenerate"
                    % (key, self.p))
            cached[key] = self.const(pow(r, self.p - 2, self.p))
        return cached[key]

    def invarr(self, a):
        r = np.ones_like(a)
        b = a % self.p
        e = self.p - 2
        while e:
            if e & 1:
                r = (r * b) % self.p
            b = (b * b) % self.p
            e >>= 1
        return r

    def conv(self, A, B, k):
        return np.einsum("ij,ij->j", A[: k + 1], B[k::-1]) % self.p

    def is_zero(self, a):
        return (a % self.p) == 0


# --------------------------------------------------------------------------
# The recurrence.
# --------------------------------------------------------------------------
def run(R, u, v, w, N, caps=None, selfcheck=False, cval=None, aval=None):
    """Carry the kernel-retaining recurrence to rung N.

    ``caps=None``   : free shooting, every p3[n] / p1[n+1] / p2[n+1] solved.
    ``caps=dict(p3=22, p2=43, p1=64)`` : polynomiality caps imposed; the
    corresponding equations become *conditions* recorded in ``cond``.

    Returns dict with the coefficient arrays, the constants, and ``cond``,
    a dict  (row, index) -> residual that must vanish for a candidate.
    """
    assert N < 83, "p0 = x^84 - x is locally -x only for rungs below 83"
    size = N + 3
    Z = R.zeros
    red = R.red

    p1 = Z(size)
    p2 = Z(size)
    p3 = Z(size)
    dp1 = Z(size)
    dp2 = Z(size)
    dp3 = Z(size)
    q5 = Z(size)
    q4 = Z(size)
    q3 = Z(size)
    q2 = Z(size)
    q1 = Z(size)
    q5p = Z(size)
    q4p = Z(size)
    q3p = Z(size)
    q2p = Z(size)
    q1p = Z(size)
    q0p = Z(size)

    one = R.const(1)
    # c = leading y^6 coefficient of Q; a = scale of p0 = a(x^84 - x), so
    # locally p0 = -a x and dp0[0] = -a.  Prior scripts gauge-fix a = c = 1;
    # both are sweepable here so the gauge is not an assumption.
    c = R.const(1) if cval is None else red(cval)
    a = R.const(1) if aval is None else red(aval)
    ainv = R.invarr(a)
    inv2 = R.invint(2)
    inv3 = R.invint(3)
    inv4 = R.invint(4)
    inv5 = R.invint(5)

    # dp0 has the single entry dp0[0] = -a for all rungs below 83.
    def cdp0(X, k):              # conv(dp0, X, k)
        return red(-a * X[k])

    # ---- rung 0: A1, A2, A3 -------------------------------------------
    p1[1] = red(u)
    p2[1] = red(v)
    p3[1] = red(w)
    dp1[0] = red(u)
    dp2[0] = red(v)
    dp3[0] = red(w)

    A1 = red(-one * ainv)                    # E0[0] = -a*A1 = 1
    A2 = red(u * A1 * inv2 * ainv)           # E1[0] = u*A1 - 2a*A2
    A3 = red((v * A1 + 2 * u * A2) * inv3 * ainv)   # E2[0] = vA1+2uA2-3aA3
    A4 = R.const(0)                                  # provably absent
    q1[0] = A1
    q2[0] = A2
    q3[0] = A3
    q4[0] = A4
    A5 = R.const(0)                                  # set at rung 1
    q5[0] = A5

    if selfcheck:
        assert np.all(R.is_zero(red(cdp0(q1, 0) - one))), "E0[0] != 1"
        assert np.all(R.is_zero(red(dp1[0] * q1[0] + 2 * cdp0(q2, 0)))), "E1[0]"
        assert np.all(R.is_zero(red(dp2[0] * q1[0] + 2 * dp1[0] * q2[0]
                                    + 3 * cdp0(q3, 0)))), "E2[0]"

    # ---- the q-chain at rung n ----------------------------------------
    def chain(n):
        m = n - 1
        q5[n] = red(3 * c * p3[n] * inv2)
        q5p[m] = red(3 * c * dp3[m] * inv2)
        q4p[m] = red((5 * R.conv(dp3, q5, m) - 3 * R.conv(p3, q5p, m)
                      + 6 * c * dp2[m]) * inv4)
        q4[n] = red(q4p[m] * R.invint(n))
        q3p[m] = red((4 * R.conv(dp3, q4, m) - 3 * R.conv(p3, q4p, m)
                      + 5 * R.conv(dp2, q5, m) - 2 * R.conv(p2, q5p, m)
                      + 6 * c * dp1[m]) * inv4)
        q3[n] = red(q3p[m] * R.invint(n))
        t = (3 * R.conv(dp3, q3, m) - 3 * R.conv(p3, q3p, m)
             + 4 * R.conv(dp2, q4, m) - 2 * R.conv(p2, q4p, m)
             + 5 * R.conv(dp1, q5, m) - R.conv(p1, q5p, m))
        if m == 0:
            t = t + 6 * c * (-a)            # 6 c dp0[0]
        q2p[m] = red(t * inv4)
        q2[n] = red(q2p[m] * R.invint(n))
        q1p[m] = red((2 * R.conv(dp3, q2, m) - 3 * R.conv(p3, q2p, m)
                      + 3 * R.conv(dp2, q3, m) - 2 * R.conv(p2, q3p, m)
                      + 4 * R.conv(dp1, q4, m) - R.conv(p1, q4p, m)
                      + 5 * cdp0(q5, m)) * inv4)
        q1[n] = red(q1p[m] * R.invint(n))
        q0p[m] = red((R.conv(dp3, q1, m) - 3 * R.conv(p3, q1p, m)
                      + 2 * R.conv(dp2, q2, m) - 2 * R.conv(p2, q2p, m)
                      + 3 * R.conv(dp1, q3, m) - R.conv(p1, q3p, m)
                      + 4 * cdp0(q4, m)) * inv4)

    def E0(n):
        return red(-R.conv(p1, q0p, n) + cdp0(q1, n))

    def E1(n):
        return red(-2 * R.conv(p2, q0p, n) + R.conv(dp1, q1, n)
                   - R.conv(p1, q1p, n) + 2 * cdp0(q2, n))

    def E2(n):
        return red(-3 * R.conv(p3, q0p, n) + R.conv(dp2, q1, n)
                   - 2 * R.conv(p2, q1p, n) + 2 * R.conv(dp1, q2, n)
                   - R.conv(p1, q2p, n) + 3 * cdp0(q3, n))

    cond = {}
    cap3 = caps.get("p3") if caps else None
    cap2 = caps.get("p2") if caps else None
    cap1 = caps.get("p1") if caps else None
    uinv = R.invarr(u)

    for n in range(1, N + 1):
        # -- E0[n]: rung 1 fixes A5, rung n>=2 fixes p3[n] ---------------
        if n == 1:
            chain(1)
            c0 = E0(1)
            # E0[1] = c0 + (5 a^2 / 4) A5   (A5 was 0 in the pass above)
            A5 = red(-4 * c0 * inv5 * ainv * ainv)
            q5[0] = A5
            chain(1)
            if selfcheck:
                assert np.all(R.is_zero(E0(1))), "A5 solve failed"
        else:
            p3[n] = R.const(0)
            dp3[n - 1] = R.const(0)
            chain(n)
            c0 = E0(n)
            if cap3 is not None and n >= cap3:
                cond[("p3", n)] = c0        # p3[n] forced 0 -> E0[n] = c0 = 0
            else:
                # pivot (n+1)*u/(4a)  =>  p3[n] = -4 a c0 / ((n+1) u)
                p3[n] = red(-4 * a * c0 * R.invint(n + 1) * uinv)
                dp3[n - 1] = red(n * p3[n])
                chain(n)
                if selfcheck:
                    assert np.all(R.is_zero(E0(n))), "p3[%d] solve failed" % n

        # -- E1[n] -> p1[n+1] -------------------------------------------
        dp1[n] = R.const(0)
        e1 = E1(n)                          # E1[n] = e1 - (n+1) p1[n+1]/a
        if cap1 is not None and n + 1 >= cap1:
            cond[("p1", n + 1)] = e1
        else:
            p1[n + 1] = red(a * e1 * R.invint(n + 1))
            dp1[n] = red((n + 1) * p1[n + 1])
            if selfcheck:
                assert np.all(R.is_zero(E1(n))), "p1[%d] solve failed" % (n + 1)

        # -- E2[n] -> p2[n+1] -------------------------------------------
        dp2[n] = R.const(0)
        e2 = E2(n)                          # E2[n] = e2 - (n+1) p2[n+1]/a
        if cap2 is not None and n + 1 >= cap2:
            cond[("p2", n + 1)] = e2
        else:
            p2[n + 1] = red(a * e2 * R.invint(n + 1))
            dp2[n] = red((n + 1) * p2[n + 1])
            if selfcheck:
                assert np.all(R.is_zero(E2(n))), "p2[%d] solve failed" % (n + 1)

    return dict(a=a, c=c, p1=p1, p2=p2, p3=p3, q1=q1, q2=q2, q3=q3, q4=q4, q5=q5,
                A1=A1, A2=A2, A3=A3, A5=A5, cond=cond)
