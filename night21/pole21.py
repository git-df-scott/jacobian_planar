#!/usr/bin/env python3
"""Dependency-free exact checks for POLE_THEOREM.md."""

from fractions import Fraction as F
from math import gcd


def clean(a):
    return {m: F(v) for m, v in a.items() if v}


def add(*aa):
    out = {}
    for a in aa:
        for m, v in a.items():
            out[m] = out.get(m, F(0)) + v
    return clean(out)


def scale(c, a):
    return clean({m: F(c)*v for m, v in a.items()})


def mul(a, b):
    out = {}
    for (i, j), u in a.items():
        for (r, s), v in b.items():
            m = (i+r, j+s)
            out[m] = out.get(m, F(0)) + u*v
    return clean(out)


def dx(a):
    return clean({(i-1, j): i*v for (i, j), v in a.items() if i})


def dy(a):
    return clean({(i, j-1): j*v for (i, j), v in a.items() if j})


def D(P, Q):
    return add(mul(dx(P), dy(Q)), scale(-1, mul(dy(P), dx(Q))))


ONE = {(0, 0): F(1)}
X = {(1, 0): F(1)}
Y = {(0, 1): F(1)}


def quotient_identity(P, A, B):
    """Numerator of D(A/B)-1 over B^2."""
    return add(mul(D(P, A), B), scale(-1, mul(A, D(P, B))),
               scale(-1, mul(B, B)))


def up_clean(a):
    return {i: F(v) for i, v in a.items() if v}


def up_add(*aa):
    out = {}
    for a in aa:
        for i, v in a.items():
            out[i] = out.get(i, F(0)) + v
    return up_clean(out)


def up_scale(c, a):
    return up_clean({i: F(c)*v for i, v in a.items()})


def up_mul(a, b):
    out = {}
    for i, u in a.items():
        for j, v in b.items():
            out[i+j] = out.get(i+j, F(0)) + u*v
    return up_clean(out)


def up_der(a):
    return up_clean({i-1: i*v for i, v in a.items() if i})


def up_divmod(a, b):
    a, b = up_clean(a), up_clean(b)
    q = {}
    db, lb = max(b), b[max(b)]
    while a and max(a) >= db:
        da = max(a)
        t, c = da-db, a[da]/lb
        q[t] = q.get(t, F(0)) + c
        a = up_add(a, up_scale(-c, {i+t: v for i, v in b.items()}))
    return up_clean(q), a


def up_gcd(a, b):
    a, b = up_clean(a), up_clean(b)
    while b:
        _, r = up_divmod(a, b)
        a, b = b, r
    if not a:
        return {}
    lc = a[max(a)]
    return up_scale(1/lc, a)


def subst_z(H, p, q, outside=(0, 0)):
    return clean({(outside[0]+q*r, outside[1]+p*r): a
                  for r, a in H.items()})


def check_night19_rational_mate():
    for gamma in (F(1), F(-2), F(3, 2)):
        for c in (F(1), F(-3), F(5, 2)):
            P = {(1, 2): gamma, (0, 1): c}
            A = scale(-1, X)
            B = {(1, 1): gamma, (0, 0): c}
            assert quotient_identity(P, A, B) == {}


def check_vertical_pole_cancellation():
    # P=y, D=-d/dx.  A=-x*b(y)+a(y), so D(A)=b(P); A/b(P)
    # is a rational mate and deleting a(P)/b(P) gives Q=-x.
    bs = [{(0, 0): -1, (0, 1): 1},
          {(0, 0): 2, (0, 1): -3, (0, 3): 1},
          {(0, 0): 2, (0, 3): 1}]
    aa = [{(0, 0): 1, (0, 1): 1},
          {(0, 0): 2, (0, 1): -3, (0, 4): 1}]
    for b in bs:
        for a in aa:
            A = add(scale(-1, mul(X, b)), a)
            assert D(Y, A) == b
            assert quotient_identity(Y, A, b) == {}
            assert D(Y, scale(-1, X)) == ONE


def check_mixed_operator():
    Hs = [{0: 1, 1: 2}, {0: 2, 1: -1, 2: 3}, {0: 3, 1: 1, 3: 1}]
    Ss = [{0: 1}, {1: 1}, {0: 2, 1: -1, 2: 1}]
    count = 0
    for p in range(1, 5):
        for q in range(1, 5):
            if gcd(p, q) != 1:
                continue
            for H in Hs:
                P = subst_z(H, p, q, (0, 1))
                for S in Ss:
                    Q = subst_z(S, p, q, (1, 0))
                    z_h_sp = {r+1: a for r, a in up_mul(H, up_der(S)).items()}
                    z_hp_s = {r+1: a for r, a in up_mul(up_der(H), S).items()}
                    want_u = up_scale(-1, up_add(up_mul(H, S),
                                                up_scale(q, z_h_sp),
                                                up_scale(p, z_hp_s)))
                    want = subst_z(want_u, p, q)
                    assert D(P, Q) == want, (p, q, H, S)
                    count += 1
    assert count == 99, count


def check_top_nontermination():
    count = 0
    for p in range(1, 6):
        for q in range(1, 6):
            for n in range(1, 7):
                for s in range(0, 7):
                    assert 1 + q*s + p*n > 0
                    count += 1
    assert count == 1050


def check_squarefree_criterion():
    good = [{0: 1, 1: 1}, {0: 2, 1: -1, 2: 1}, {0: 3, 1: 1, 3: 1}]
    bad = [up_mul({0: 1, 1: 1}, {0: 1, 1: 1}),
           up_mul(up_mul({0: -2, 1: 1}, {0: -2, 1: 1}), {0: 1, 1: 1})]
    for H in good:
        assert up_gcd(H, up_der(H)) == {0: F(1)}
        assert H.get(0, 0) != 0
    for H in bad:
        assert max(up_gcd(H, up_der(H))) >= 1
        assert H.get(0, 0) != 0


def main():
    check_night19_rational_mate()
    check_vertical_pole_cancellation()
    check_mixed_operator()
    check_top_nontermination()
    check_squarefree_criterion()
    print("PASS night19 rational mate: 9 exact parameter cases")
    print("PASS whole-fibre denominator cancellation: 6 exact cases")
    print("PASS mixed-isobaric operator identity: 99 exact cases")
    print("PASS mixed-isobaric highest-term obstruction: 1050 integer cases")
    print("PASS squarefree/unimodular criterion: 5 exact univariate cases")


if __name__ == "__main__":
    main()
