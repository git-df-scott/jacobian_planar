#!/usr/bin/env python3
"""Session 44 — exact function-field walk of the u=0 chart, mod a large prime.

K = F_p(v)[w] / (3 v w^2 + 18 w + 2 v^4)   (w^2 = -(6/v) w - (2/3) v^3).

Elements are triples (A, B, D) of nmod_poly's in v, meaning (A + B w)/D.
The u=0 recurrence is walked with series coefficients in K, carrying the one
active kernel t_m as a short polynomial in t with K coefficients (t-degree
<= 3, asserted).  At rung n the E0 row gives a condition c0 + c1 t; the
kernel is solved t = -c0/c1 in K (branching stratum: numerator of c1 —
RECORDED, its zero locus walked separately).  E2/E1 pivots are checked to be
t-free K-units.  Past the p3 cap the E0 rows are pure K conditions; their
numerators N_23(v), N_24(v), ... are the output.

The final object per prime: g = gcd(N_23, N_24, ...) in F_p[v].  A stable
nontrivial factor across primes = the characteristic-zero surviving locus
candidate; g = 1 at two large primes = the chart is empty away from the
recorded strata (up to finitely many bad primes; exact certificate then
computed on demand).
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "vendor"))
from flint import nmod_poly  # noqa: E402

from uvw_hunt import TERMS  # noqa: E402

P = None  # set in main


def npoly(coeffs):
    return nmod_poly(coeffs, P)


class K:
    """(A + B w)/D with A,B,D in F_p[v]."""

    __slots__ = ("A", "B", "D")

    def __init__(self, A, B, D):
        self.A, self.B, self.D = A, B, D

    @staticmethod
    def const(c):
        return K(npoly([c % P]), npoly([]), npoly([1]))

    @staticmethod
    def v_pow(e, c=1):
        return K(npoly([0] * e + [c % P]), npoly([]), npoly([1]))

    @staticmethod
    def w():
        return K(npoly([]), npoly([1]), npoly([1]))

    def is_zero(self):
        return not self.A and not self.B

    def reduce(self):
        g = self.A.gcd(self.B.gcd(self.D)) if self.D.degree() > 0 else None
        if g is not None and g.degree() > 0:
            self.A //= g
            self.B //= g
            self.D //= g
        # normalize leading coeff of D
        if self.D.degree() >= 0:
            lc = self.D[self.D.degree()]
            if lc != 1:
                inv = pow(int(lc), P - 2, P)
                self.A *= inv
                self.B *= inv
                self.D *= inv
        return self

    def add(self, o):
        if self.is_zero():
            return o
        if o.is_zero():
            return self
        if self.D == o.D:
            return K(self.A + o.A, self.B + o.B, self.D).reduce()
        return K(self.A * o.D + o.A * self.D,
                 self.B * o.D + o.B * self.D, self.D * o.D).reduce()

    def neg(self):
        return K(-self.A, -self.B, self.D)

    def mul(self, o):
        if self.is_zero() or o.is_zero():
            return K_ZERO
        # (A1+B1 w)(A2+B2 w); w^2 = (-6 w - (2/3) v^4)/v  [times v]
        A1, B1, A2, B2 = self.A, self.B, o.A, o.B
        bb = B1 * B2
        v = npoly([0, 1])
        inv3 = pow(3, P - 2, P)
        A = v * (A1 * A2) - npoly([0, 0, 0, 0, (2 * inv3) % P]) * bb
        B = v * (A1 * B2 + A2 * B1) - 6 * bb
        return K(A, B, v * self.D * o.D).reduce()

    def inv(self):
        # 1/(A+Bw) = ((Av-6B) - Bv w)/(v A^2 - 6AB + (2/3) v^4 B^2)
        A, B = self.A, self.B
        v = npoly([0, 1])
        inv3 = pow(3, P - 2, P)
        num_a = A * v - 6 * B
        num_b = -(B * v)
        den = v * A * A - 6 * A * B + npoly([0, 0, 0, 0, (2 * inv3) % P]) * B * B
        assert den, "K.inv of zero-norm element"
        return K(self.D * num_a, self.D * num_b, den).reduce()

    def scal(self, c):
        c %= P
        return K(self.A * c, self.B * c, self.D).reduce() if c else K_ZERO


# ---- t-polynomials over K: dict {(e1,e2): K} over the two active slots ----
# slot 1 = oldest unsolved kernel (solved at the current rung),
# slot 2 = newest kernel (solved next rung).


def tz():
    return {}


def tconst(k):
    return {} if k.is_zero() else {(0, 0): k}


def tslot2():
    return {(0, 1): K.const(1)}


def tadd(a, b):
    out = dict(a)
    for e, k in b.items():
        cur = out.get(e)
        s = k if cur is None else cur.add(k)
        if s.is_zero():
            out.pop(e, None)
        else:
            out[e] = s
    return out


def tmul(a, b):
    if not a or not b:
        return {}
    out = {}
    for ea, ka in a.items():
        for eb, kb in b.items():
            e = (ea[0] + eb[0], ea[1] + eb[1])
            assert e[0] <= 3 and e[1] <= 3, f"t-degree overflow {e}"
            prod = ka.mul(kb)
            cur = out.get(e)
            s = prod if cur is None else cur.add(prod)
            if s.is_zero():
                out.pop(e, None)
            else:
                out[e] = s
    return out


def tscal(a, c):
    out = {}
    for e, k in a.items():
        s = k.scal(c)
        if not s.is_zero():
            out[e] = s
    return out


def t_shift_slots(a):
    """After slot-1 substitution: move slot-2 exponents into slot 1."""
    out = {}
    for (e1, e2), k in a.items():
        assert e1 == 0
        out[(e2, 0)] = k
    return out


def tsubs_slot1(a, val):
    """Substitute slot-1 kernel := val (in K); keep slot 2."""
    out = {}
    for (e1, e2), k in a.items():
        c = k
        for _ in range(e1):
            c = c.mul(val)
        cur = out.get((0, e2))
        s = c if cur is None else cur.add(c)
        if s.is_zero():
            out.pop((0, e2), None)
        else:
            out[(0, e2)] = s
    return out


class Walk:
    def __init__(self, horizon):
        self.N = horizon
        self.strata = []       # recorded exceptional-locus numerators
        self.conds = {}        # rung -> K condition (past p3 cap)
        inv2, inv3, inv5, inv8 = (pow(x, P - 2, P) for x in (2, 3, 5, 8))
        v1 = K.v_pow(1)
        w = K.w()
        # a2 = (v w + 3)/2 ; b2 = 3(v^3 + w^2)/8
        a2 = v1.mul(w).add(K.const(3)).scal(inv2)
        w2 = w.mul(w)
        b2 = K.v_pow(3).add(w2).scal((3 * inv8) % P)
        self.s1 = {0: tz(), 1: tz(), 2: tconst(a2)}
        self.s2 = {0: tz(), 1: tconst(v1), 2: tconst(b2)}
        self.s3 = {0: tz(), 1: tconst(w), 2: {(1, 0): K.const(1)}}  # t2 in slot 1
        self.active_m = 2
        self.A = {0: tz(), 1: tconst(K.const(P - 1)), 2: tz(),
                  3: tconst(K.v_pow(1, P - inv3 % P)),
                  4: tz(),
                  5: tconst(K.v_pow(2).scal(P - inv5 % P))}

    def series_for(self, idx, n):
        if idx == 0:
            out = [tz()] * (n + 1)
            if n >= 1:
                out[1] = tconst(K.const(P - 1))
            if n >= 84:
                out[84] = tconst(K.const(1))
            return out
        if idx < 4:
            src = (None, self.s1, self.s2, self.s3)[idx]
            return [src.get(k, tz()) for k in range(n + 1)]
        if idx == 4:
            out = [tconst(K.const(P - 1))] + [tz()] * n
            if n >= 83:
                out[83] = tconst(K.const(84))
            return out
        if idx < 8:
            src = (None, self.s1, self.s2, self.s3)[idx - 4]
            return [tscal(src.get(k + 1, tz()), k + 1) for k in range(n + 1)]
        if idx < 14:
            out = [tz()] * (n + 1)
            out[0] = self.A[idx - 8]
            return out
        out = [tz()] * (n + 1)
        out[0] = tconst(K.const(1))
        return out

    def row_coeff(self, row, n):
        cache = {}
        total = tz()
        for num, den, factors in TERMS[row]:
            c0 = num * pow(den, P - 2, P) % P
            acc = [tconst(K.const(c0))] + [tz()] * n
            for idx, power in factors:
                if idx not in cache:
                    cache[idx] = self.series_for(idx, n)
                fs = cache[idx]
                for _ in range(power):
                    new = [tz()] * (n + 1)
                    for i, av in enumerate(acc):
                        if not av:
                            continue
                        for j in range(n + 1 - i):
                            bv = fs[j]
                            if bv:
                                new[i + j] = tadd(new[i + j], tmul(av, bv))
                    acc = new
            total = tadd(total, acc[n])
        return total

    def substitute_kernel(self, val):
        for store in (self.s1, self.s2, self.s3):
            for k in list(store):
                if store[k]:
                    store[k] = t_shift_slots(tsubs_slot1(store[k], val))

    def run(self, verbose=True):
        n = 2
        while n <= self.N:
            for row, store, cap in ((0, self.s2, 42), (1, self.s1, 63)):
                m = n + 1
                if m > cap:
                    continue
                store[m] = tz()
                base = self.row_coeff(row, n)
                store[m] = tconst(K.const(1))
                shift = self.row_coeff(row, n)
                store[m] = tz()
                piv = tadd(shift, tscal(base, P - 1))
                assert set(piv) == {(0, 0)}, \
                    f"rung {n} E-row {row}: pivot not t-free: {set(piv)}"
                pk = piv[(0, 0)]
                assert pk.B.degree() < 0 and pk.A.degree() == 0 and \
                    pk.D.degree() == 0, f"rung {n} row {row}: pivot not const"
                c = int(pk.A[0]) * pow(int(pk.D[0]), P - 2, P) % P
                sol = tscal(base, (P - pow(c, P - 2, P)) % P)
                store[m] = sol
            cond = self.row_coeff(2, n)
            assert all(e[1] == 0 for e in cond), \
                f"rung {n}: condition touches slot-2 kernel: {set(cond)}"
            maxdeg = max((e[0] for e in cond), default=0)
            if maxdeg >= 1:
                assert maxdeg == 1, f"rung {n}: condition t-degree {maxdeg}"
                c1 = cond[(1, 0)]
                assert not c1.is_zero(), f"rung {n}: c1 identically zero"
                self.strata.append((n, c1.A, c1.B))
                c0 = cond.get((0, 0), K_ZERO)
                tval = c0.neg().mul(c1.inv())
                self.substitute_kernel(tval)
                if verbose:
                    dg = max(tval.A.degree(), tval.B.degree(), tval.D.degree())
                    print(f"rung {n}: solved slot-1 kernel in K, deg ~ {dg}",
                          flush=True)
            else:
                c0 = cond.get((0, 0), K_ZERO)
                if not c0.is_zero():
                    self.conds[n] = c0
                    if verbose:
                        dg = max(c0.A.degree(), c0.B.degree())
                        print(f"rung {n}: PURE CONDITION, num deg ~ {dg}",
                              flush=True)
                else:
                    # identically zero on the curve: at rung 2 this is the
                    # quartic itself (the defining relation of K) — the slot-1
                    # kernel stays unsolved until the next rung.  Slot 2 must
                    # be empty here or a third kernel would activate.
                    assert n == 2, f"rung {n}: unexpected 0=0 condition row"
            # introduce next kernel
            if n + 1 <= 21:
                m = n + 1
                self.s3[m] = tslot2()
                self.active_m = m
            n += 1
        return self.conds


def main():
    global P, K_ZERO
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("prime", type=int)
    ap.add_argument("--horizon", type=int, default=26)
    a = ap.parse_args()
    P = a.prime
    K_ZERO = K(npoly([]), npoly([]), npoly([1]))
    wk = Walk(a.horizon)
    conds = wk.run()
    print(f"== conditions mod {P} ==")
    polys = []
    for n, c in sorted(conds.items()):
        # numerator: resultant-free — condition zero iff A + Bw = 0 on curve
        # iff (A, B) proportional to... on the curve: A + Bw = 0 for one of
        # the two w-branches iff Norm = A^2 v - 6AB + (2/3) v^4 B^2 = 0
        inv3 = pow(3, P - 2, P)
        v = npoly([0, 1])
        norm = v * c.A * c.A - 6 * c.A * c.B + \
            npoly([0, 0, 0, 0, (2 * inv3) % P]) * c.B * c.B
        polys.append((n, norm))
        print(f"N_{n}: deg {norm.degree()}")
    if len(polys) >= 2:
        g = polys[0][1].gcd(polys[1][1])
        for n, q in polys[2:]:
            g = g.gcd(q)
        print(f"gcd of all condition norms mod {P}: deg {g.degree()}")
        if g.degree() > 0:
            print("NONTRIVIAL FACTOR:", g)
    for n, cA, cB in wk.strata:
        print(f"stratum rung {n}: c1 numerator degs "
              f"({cA.degree()},{cB.degree()})")


if __name__ == "__main__":
    K_ZERO = None
    main()
