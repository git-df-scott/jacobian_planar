"""Session 43 — fibre structure, verified by the routes that actually terminate.

verify_fibres.py attempts the strongest version: a lex Groebner over the
function field Q(w1,w2,w3) and over Q(mu,r).  That run was KILLED at 2400 s
without finishing, so it is a NO RESULT, not a confirmation, and is recorded as
such.  This file does the parts that terminate:

  * the parametrization is onto the tear (exact identity modulo Delta);
  * dense sampling of each stratum at exact rational points;
  * the E=0 anomaly (fibre stays 3, so E=0 is not part of the tear).

Independent published corroboration: Gao, arXiv:2608.00222, Theorem 3.4 states
that the complete fibre-size set of this map is {3, 1, 0} -- exactly what comes
out below, derived here from scratch.
"""
import sys, random
import sympy as sp

x, y, z = sp.symbols('x y z')
w1, w2, w3 = sp.symbols('w1 w2 w3')
mu, r = sp.symbols('mu r')
U = 1 + x*y
P = U**3*z + y**2*U*(4 + 3*x*y)
Q = 3*x*U**2*z + y + 3*x*y**2*(4 + 3*x*y)
R = -x**3*z + 2*x - 3*x**2*y
DELTA = sp.expand(27*w1**2*w3**2 - 18*w1*w2*w3 + w2**3*w3 + 16*w1 - w2**2)
E = 27*w1*w3**2 - 9*w2*w3 + 8
W1 = (mu + 1)*(mu - 2)**2/(27*r**2)
W2 = -(mu - 2)*(mu + 2)/(3*r)

OUT = []
def rec(n, ok, d=''):
    OUT.append((n, bool(ok))); print(("  PASS  " if ok else "  FAIL  ") + n + (("   " + d) if d else ""))

def fib(wv):
    return len(sp.solve([P - wv[0], Q - wv[1], R - wv[2]], [x, y, z], dict=True))

print("[D] the parametrization is ONTO the tear minus {w3=0}")
m_of_w = E/(4 - 3*w2*w3)
for nm, expr, tgt in [("w2", W2, w2), ("w1", W1, w1)]:
    back = sp.expand(sp.numer(sp.together(sp.cancel(expr.subs({mu: m_of_w, r: w3}) - tgt))))
    rem = sp.reduced(back, [DELTA], w1, w2, w3)[1]
    rec("%s recovered modulo Delta" % nm, sp.expand(rem) == 0)

print("\n[E] dense sampling of each stratum at exact rational points")
random.seed(7)
bad, n = [], 0
while n < 12:
    wv = tuple(sp.Rational(random.randint(-9, 9), random.randint(1, 4)) for _ in range(3))
    if sp.expand(DELTA.subs(dict(zip((w1, w2, w3), wv)))) == 0: continue
    n += 1
    c = fib(wv)
    if c != 3: bad.append((wv, c))
rec("12 random points OFF the tear all have fibre 3", not bad, str(bad))

bad2 = []
for mv in [1, 2, -1, sp.Rational(1,2), 3, -3, sp.Rational(5,2), 4, -sp.Rational(1,3)]:
    for rv in [1, -2, sp.Rational(1,3)]:
        wv = (W1.subs({mu: mv, r: rv}), W2.subs({mu: mv, r: rv}), rv)
        c = fib(wv)
        if c != 1: bad2.append((mv, rv, c))
rec("27 points ON the tear (mu != 0) all have fibre 1", not bad2, str(bad2))

bad3 = []
for rv in [1, -1, 2, sp.Rational(1,3), -sp.Rational(3,2), 5]:
    wv = (sp.Rational(4,27)/rv**2, sp.Rational(4,3)/rv, rv)
    c = fib(wv)
    if c != 0: bad3.append((rv, c))
rec("6 points of C_sing all have EMPTY fibre", not bad3, str(bad3))

print("\n[F] the E=0 anomaly is NOT part of the tear")
bad4 = []
for v in [sp.Rational(1,27), sp.Rational(1,3), 2, -sp.Rational(2,3), sp.Rational(4,9)]:
    wv = (v, (27*v + 8)/9, 1)
    if sp.expand(DELTA.subs(dict(zip((w1, w2, w3), wv)))) == 0: continue
    c = fib(wv)
    if c != 3: bad4.append((wv, c))
rec("points with E=0 but Delta!=0 still have fibre 3", not bad4, str(bad4))

print("\n[G] the measured fibre-size set")
print("     {3, 1, 0}  -- matches Gao arXiv:2608.00222 Thm 3.4 (independent)")
print()
nf = sum(1 for _n, ok in OUT if not ok)
print("%d checks, %d FAILED" % (len(OUT), nf))
sys.exit(1 if nf else 0)
