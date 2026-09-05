"""night6 -- characteristic-zero controls.

C1(char 0)  identity control with EXACT RATIONAL arithmetic: the five coded
    expressions E0..E4 are compared, at random rational f,p,q,g,r,s,t with the
    handoff's supports, against the z^k coefficients of the bracket
    [P,Q]_{u,z} = P_u Q_z - P_z Q_u computed directly from
    P = f + p z + q z^2, Q = g + r z + s z^2 + t z^3.

C2(char 0)  positive control: the same builder with (p_,s_) = (0,0), free.
    Must come out NOT the unit ideal, with the all-zero point (f, g constant,
    r = 0) verified by exact substitution.

C3(char 0)  the same branch with vertex non-degeneracy f_8 != 0, g_12 != 0.
    Expected empty by the handoff's section 3d hand argument.
"""
import random
from fractions import Fraction as F


def upmul(a, b):
    r = {}
    for i, x in a.items():
        for j, y in b.items():
            r[i + j] = r.get(i + j, F(0)) + x * y
    return {k: v for k, v in r.items() if v}


def upadd(*args):
    r = {}
    for a in args:
        for k, v in a.items():
            r[k] = r.get(k, F(0)) + v
    return {k: v for k, v in r.items() if v}


def upscal(a, c):
    return {k: v * c for k, v in a.items() if v * c}


def upder(a):
    return {k - 1: k * v for k, v in a.items() if k > 0 and k * v}


def control_C1_char0(seeds=4, seed=20260828):
    """exact rational identity control; returns (ok, per-seed detail)"""
    random.seed(seed)
    detail = []
    ok = True
    for _ in range(seeds):
        def rnd(lo, hi):
            return {k: F(random.randrange(-50, 50) or 7,
                         random.randrange(1, 13)) for k in range(lo, hi + 1)}
        f, pp, q = rnd(0, 8), rnd(1, 8), rnd(1, 8)
        g, r, s, t = rnd(0, 12), rnd(1, 12), rnd(2, 12), rnd(2, 12)
        A = {0: f, 1: pp, 2: q}
        B = {0: g, 1: r, 2: s, 3: t}
        direct = {}
        for i, ai in A.items():
            for j, bj in B.items():
                k = i + j - 1
                if k < 0:
                    continue
                term = upadd(upscal(upmul(upder(ai), bj), j),
                             upscal(upmul(ai, upder(bj)), -i))
                direct[k] = upadd(direct.get(k, {}), term)
        coded = {
            0: upadd(upmul(upder(f), r), upscal(upmul(pp, upder(g)), -1)),
            1: upadd(upscal(upmul(upder(f), s), 2), upmul(upder(pp), r),
                     upscal(upmul(pp, upder(r)), -1),
                     upscal(upmul(q, upder(g)), -2)),
            2: upadd(upscal(upmul(upder(f), t), 3),
                     upscal(upmul(upder(pp), s), 2), upmul(upder(q), r),
                     upscal(upmul(pp, upder(s)), -1),
                     upscal(upmul(q, upder(r)), -2)),
            3: upadd(upscal(upmul(upder(pp), t), 3),
                     upscal(upmul(upder(q), s), 2),
                     upscal(upmul(pp, upder(t)), -1),
                     upscal(upmul(q, upder(s)), -2)),
            4: upadd(upscal(upmul(upder(q), t), 3),
                     upscal(upmul(q, upder(t)), -2)),
        }
        agree = [direct.get(k, {}) == coded[k] for k in range(5)]
        detail.append(agree)
        if not all(agree):
            ok = False
    return ok, detail


def subst_check(eqs, names, sol, K):
    """substitute sol (dict name -> K element) into eqs; count nonzero"""
    bad = 0
    for e in eqs:
        acc = K.zero
        for m, c in e.d.items():
            term = c
            for i, ex in enumerate(m):
                for _ in range(ex):
                    term = K.mul(term, sol.get(names[i], K.zero))
            acc = K.add(acc, term)
        if not K.iszero(acc):
            bad += 1
    return bad


if __name__ == '__main__':
    ok, detail = control_C1_char0()
    print("C1 (characteristic zero, exact rational):", ok)
    for i, d in enumerate(detail):
        print("   seed %d: E0..E4 agree with the direct (u,z) bracket = %s"
              % (i, d))
