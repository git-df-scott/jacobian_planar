"""night10 -- STEP 0 controls.  Hard-exits on any disagreement.

C1  exact step identity over Z:  r(x + e d) = r(x) + e Dr(x) d + e^2 Q2(d)
C2  polarization control: Bpol(d,d') extracted programmatically equals the
    direct expansion Q2(d+d') - Q2(d) - Q2(d')  and equals the cross term of
    Q2 on random integer vectors
C3  ring control for O2 = Z[pi]/(pi^2-2) and O3 = Z[pi]/(pi^3-2):
    associativity/distributivity on randoms, pi^e = 2, w additive
C4  the multi-level expansion identity used by the ladder:
    r(x0 + sum pi^k d_k) = r(x0) + sum_m pi^m [ J d_m + Q2(d_{m/2})
                            + sum_{i<j, i+j=m} Bpol(d_i,d_j) ]
    checked against exact O-arithmetic
R0  toy  f(x) = x^2 - 2  at x0 = 0:  unramified step must FAIL,
    ramified (O2) step must SUCCEED with d_1 = 1.
"""

import random
import sys
import system as S
import ram
from ram import O2, O3

random.seed(20260828)
FAIL = []


def check(name, ok, detail=""):
    print("%-46s %s %s" % (name, "OK" if ok else "FAIL", detail))
    if not ok:
        FAIL.append(name)


# ---- C1 ----
ok = True
for _ in range(200):
    x = [random.randint(-9, 9) for _ in range(S.N)]
    d = [random.randint(-9, 9) for _ in range(S.N)]
    e = random.randint(-6, 6)
    lhs = S.r_eval([xi + e * di for xi, di in zip(x, d)])
    J = S.jac_eval(x)
    q = S.Q2(d)
    rhs = [S.r_eval(x)[k] + e * sum(J[k][i] * d[i] for i in range(S.N)) + e * e * q[k]
           for k in range(S.M)]
    if lhs != rhs:
        ok = False
        break
check("C1 step identity over Z", ok)

# ---- C2 ----
ok = True
for _ in range(200):
    d = [random.randint(-9, 9) for _ in range(S.N)]
    e = [random.randint(-9, 9) for _ in range(S.N)]
    direct = [S.Q2([a + b for a, b in zip(d, e)])[k] - S.Q2(d)[k] - S.Q2(e)[k]
              for k in range(S.M)]
    if S.Bpol(d, e) != direct:
        ok = False
        break
check("C2 polarization Bpol over Z", ok)

# ---- C3 ----
def ring_control(R, name):
    ok = True
    for _ in range(300):
        u = tuple(random.randint(-9, 9) for _ in range(R.e))
        v = tuple(random.randint(-9, 9) for _ in range(R.e))
        w = tuple(random.randint(-9, 9) for _ in range(R.e))
        if R.mul(R.mul(u, v), w) != R.mul(u, R.mul(v, w)):
            ok = False
        if R.mul(u, R.add(v, w)) != R.add(R.mul(u, v), R.mul(u, w)):
            ok = False
        if R.mul_pi(u) != R.mul(u, R.pi()):
            ok = False
        # w additivity
        if not R.is_zero(u) and not R.is_zero(v):
            if R.w(R.mul(u, v)) != R.w(u) + R.w(v):
                ok = False
        # div_pi inverse of mul_pi
        if R.div_pi(R.mul_pi(u)) != u:
            ok = False
    p = R.pi()
    q = p
    for _ in range(R.e - 1):
        q = R.mul(q, p)
    if q != R.from_int(2):
        ok = False
    check("C3 ring control %s" % name, ok)


ring_control(O2, "O2 = Z[pi]/(pi^2-2)")
ring_control(O3, "O3 = Z[pi]/(pi^3-2)")

# ---- C4 : multi-level expansion vs exact O arithmetic ----
def c4(R, name):
    ok = True
    for _ in range(60):
        x0 = [random.randint(-3, 3) for _ in range(S.N)]
        L = 4
        ds = {k: [random.randint(-3, 3) for _ in range(S.N)] for k in range(1, L + 1)}
        exact = ram.residual(x0, ds, R)
        # assemble via the recursion
        J = S.jac_eval(x0)
        acc = [R.from_int(t) for t in S.r_eval(x0)]
        for m in range(1, 2 * L + 1):
            term = [0] * S.M
            if m <= L:
                for k in range(S.M):
                    term[k] += sum(J[k][i] * ds[m][i] for i in range(S.N))
            if m % 2 == 0 and m // 2 <= L:
                q = S.Q2(ds[m // 2])
                for k in range(S.M):
                    term[k] += q[k]
            for i in range(1, m):
                j = m - i
                if i < j and i <= L and j <= L:
                    bp = S.Bpol(ds[i], ds[j])
                    for k in range(S.M):
                        term[k] += bp[k]
            t = [R.from_int(v) for v in term]
            for _ in range(m):
                t = [R.mul_pi(u) for u in t]
            acc = [R.add(a, b) for a, b in zip(acc, t)]
        if acc != exact:
            ok = False
            break
    check("C4 multi-level expansion %s" % name, ok)


c4(O2, "over O2")
c4(O3, "over O3")


# ---- R0 toy ----
def toy():
    # f(x) = x^2 - 2, one variable, one equation; x0 = 0 is the F_2 point.
    def f(x, R):
        return R.sub(R.mul(x, x), R.from_int(2))

    print()
    print("R0 toy f(x) = x^2 - 2, base point x0 = 0 mod 2")
    # over Z: squares mod 4
    sq4 = sorted({(t * t) % 4 for t in range(4)})
    print("  squares mod 4 over Z:", sq4, "-- 2 present:", 2 in sq4)
    # unramified step  x = 0 + 2*d,  need f = 0 mod 4
    unram = [d for d in range(2) if (4 * d * d - 2) % 4 == 0]
    print("  unramified step x=0+2d, f(x) = 0 mod 4 : solutions d =", unram)
    # ramified step over O2: x = 0 + pi*d1, need w(f) > 2
    good = []
    for d1 in range(2):
        x = O2.mul_pi(O2.from_int(d1))
        val = f(x, O2)
        good.append((d1, val, O2.w(val)))
    print("  ramified step x = pi*d1 over O2 (pi^2=2):")
    for d1, val, w in good:
        print("     d1=%d  f = %s  w = %s" % (d1, val, w if w < 10**6 else "inf"))
    ram_ok = [d1 for d1, val, w in good if w > 2]
    # via the machinery's level-2 condition:  J d2 = s + Q2(d1) mod 2, J = 0, s = -1
    s = -1
    machinery = [d1 for d1 in range(2) if (s + d1 * d1) % 2 == 0]
    print("  machinery level-2 condition (J=0, s=-1): d1 passing =", machinery)
    check("R0 unramified step FAILS", unram == [])
    check("R0 ramified step SUCCEEDS with d1=1", ram_ok == [1] and machinery == [1])
    # exactness: pi^2 - 2 = 0
    check("R0 x=pi solves x^2-2 exactly in O2",
          O2.is_zero(f(O2.pi(), O2)))


toy()

print()
if FAIL:
    print("CONTROLS FAILED:", FAIL)
    sys.exit(1)
print("ALL CONTROLS PASSED")
