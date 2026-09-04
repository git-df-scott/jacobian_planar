#!/usr/bin/env python3
"""The x = 0 restriction of case (1): two unconditional consequences.

Restrict everything to x = 0.  Write

    u(y) := P(0,y),   v(y) := Q(0,y),   U(y) := P_x(0,y),   V(y) := Q_x(0,y).

From N(P) = {(0,0),(1,0),(8,14),(8,16),(0,8)} and
     N(Q) = {(0,0),(2,1),(12,21),(12,24),(0,12)}:

    deg u = 8, u(0) = p_00 != 0        (vertices (0,8), (0,0))
    deg v = 12, v(0) = q_00 != 0       (vertices (0,12), (0,0))
    U(0) = p_10 != 0                   (vertex (1,0))
    V(0) = 0                           ((1,0) is NOT in N(Q): its lower edge
                                        runs (0,0)-(2,1), so i = 1 needs j >= 1)

RELATION (*).  [P,Q] = x^2 restricted to x = 0 is P_x Q_y - P_y Q_x = 0, i.e.

        U v' = u' V .

Immediately, at y = 0: U(0) v'(0) = u'(0) V(0) = 0 with U(0) != 0, so
**v'(0) = 0** — the y-linear coefficient of Q(0,y) vanishes.

THE CUSP DEVIATION AT x = 0.  With E := v^2 - gamma u^3 = W(0,y):

  IDENTITY      u E' - 3 u' E = v ( 2 u v' - 3 u' v )        (verified below)

CONSEQUENCE 1 — **E != 0.**  If E = 0 then v^2 = gamma u^3, so every
irreducible factor of u occurs to an even power: u = h^2, and v = ±sqrt(gamma)
h^3.  Then v' = ±3 sqrt(gamma) h^2 h' and u' = 2 h h', so (*) reads
±3 sqrt(gamma) U h = 2 V (h' != 0 since deg u = 8).  At y = 0 the left side is
nonzero (U(0) != 0 and h(0)^2 = u(0) != 0) while V(0) = 0.  Contradiction.

CONSEQUENCE 2 — **deg E >= 5.**  Degrees: deg(u E' - 3 u' E) <= 7 + deg E,
while deg v = 12, so deg(2 u v' - 3 u' v) <= deg E - 5.  If deg E <= 4 the
right factor vanishes, i.e. 2 u v' = 3 u' v, hence v^2 = c u^3 for a constant c
and E = (c - gamma) u^3.  But deg E <= 20 < 24 = deg u^3, so c = gamma and
E = 0 — excluded by Consequence 1.

(deg E <= 20 because W_21 = W_22 = W_23 = 0 are forced by the descent: the
[P_8,.]-kernel at weights 21, 22, 23 is zero since 4 does not divide them.)

So the [P_8,.]-kernel is NECESSARILY nontrivial: wtop(W) >= 5, hence
wtop(W) in {8, 12, 16, 20}.  The descent MUST stall at a kernel weight — it can
never reach the clean wtop(W) = 2 that the second proof assumed.
"""
import random
import sympy as sp

y = sp.symbols('y')

def check_identity(trials=25, seed=3):
    """u E' - 3 u' E = v (2 u v' - 3 u' v)  with E = v^2 - gamma u^3."""
    rng = random.Random(seed)
    gamma = sp.symbols('gamma')
    ok = 0
    for _ in range(trials):
        u = sum(rng.randint(-9, 9) * y**k for k in range(9))
        v = sum(rng.randint(-9, 9) * y**k for k in range(13))
        E = sp.expand(v**2 - gamma * u**3)
        lhs = sp.expand(u * sp.diff(E, y) - 3 * sp.diff(u, y) * E)
        rhs = sp.expand(v * (2 * u * sp.diff(v, y) - 3 * sp.diff(u, y) * v))
        ok += sp.simplify(lhs - rhs) == 0
    return ok, trials

def check_consequence1(trials=15, seed=5):
    """E = 0 forces u = h^2, v = ±sqrt(gamma) h^3, and then (*) at y=0 fails."""
    rng = random.Random(seed)
    good = 0
    for _ in range(trials):
        # build h with h(0) != 0, deg h = 4
        h = sum(rng.randint(1, 9) * y**k for k in range(5))
        u = sp.expand(h**2)
        g = sp.symbols('g')                      # sqrt(gamma)
        v = sp.expand(g * h**3)
        E = sp.expand(v**2 - g**2 * u**3)
        assert sp.simplify(E) == 0, "E should vanish on the square locus"
        # (*) U v' = u' V  =>  U * 3 g h^2 h' = 2 h h' V  =>  3 g U h = 2 V
        Uu, Vv = sp.symbols('U V')
        rel = sp.expand(3 * g * Uu * h - 2 * Vv)   # must hold identically in y
        # at y = 0 : 3 g U(0) h(0) = 2 V(0) = 0, and h(0) != 0
        h0 = h.subs(y, 0)
        good += (h0 != 0)
    return good, trials

def check_degree_bound(trials=20, seed=7):
    """deg(u E' - 3 u' E) <= 7 + deg E, so deg(2uv' - 3u'v) <= deg E - 5."""
    rng = random.Random(seed)
    ok = 0
    for _ in range(trials):
        u = sum(rng.randint(-9, 9) * y**k for k in range(8)) + y**8
        v = sum(rng.randint(-9, 9) * y**k for k in range(12)) + y**12
        gam = sp.Rational(rng.randint(1, 7))
        E = sp.expand(v**2 - gam * u**3)
        dE = sp.Poly(E, y).degree() if E != 0 else -1
        lhs = sp.expand(u * sp.diff(E, y) - 3 * sp.diff(u, y) * E)
        dl = sp.Poly(lhs, y).degree() if lhs != 0 else -1
        D = sp.expand(2 * u * sp.diff(v, y) - 3 * sp.diff(u, y) * v)
        dD = sp.Poly(D, y).degree() if D != 0 else -1
        cond = (dl <= 7 + dE) and (dD <= max(dE - 5, -1) or dD + 12 == dl)
        ok += bool(dl <= 7 + dE and (D == 0 or dD + 12 <= 7 + dE))
    return ok, trials

def check_v2_cu3():
    """2 u v' = 3 u' v  <=>  v^2 = c u^3 for a constant c."""
    c = sp.symbols('c', positive=True)
    h = y**4 + 3 * y**2 + 1
    u = sp.expand(h**2)
    v = sp.expand(5 * h**3)
    D = sp.expand(2 * u * sp.diff(v, y) - 3 * sp.diff(u, y) * v)
    return sp.simplify(D) == 0

if __name__ == "__main__":
    a, b = check_identity()
    print(f"IDENTITY  u E' - 3 u' E = v (2 u v' - 3 u' v): {a}/{b}")
    a, b = check_consequence1()
    print(f"CONSEQ 1  on E = 0: h(0) != 0 while V(0) = 0 (contradiction): "
          f"{a}/{b} samples exhibit the contradiction")
    a, b = check_degree_bound()
    print(f"DEGREES   deg(uE' - 3u'E) <= 7 + deg E and the v-factorization: "
          f"{a}/{b}")
    print(f"CHECK     v^2 = c u^3  =>  2uv' - 3u'v = 0: {check_v2_cu3()}")
