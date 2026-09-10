"""
Exact row recursion for the degree-(108,144) rational leading branch (Astra 11/12/13 chart).

Chart: X = x^4 (y+1), Y = 1/x, J(X,Y) = x^2.  Original Keller pair => {P,Q} = kappa x^2 in (x,y).
P = c^3 x^12 + sum_{k<12} p_k(y) x^k,  Q = c^4 x^16 + sum_{l<16} q_l(y) x^l,  c = y^3 (1+y^5).
Row bounds (original rectangle 24x84 for P, 32x112 for Q; terminal 4k-5j<=3 (P), <=4 (Q)):
  p_k: y^{max(0,k-3)} | p_k   (Astra 13 shifted-chart bound),  (y+1)^{max(0,ceil(k/4))} | p_k,  deg <= min(24, floor((84+k)/4))
  q_l: y^{max(0,l-4)} | q_l,  (y+1)^{max(0,ceil(l/4))} | q_l,  deg <= min(32, floor((112+l)/4))
Bracket coefficient at x^n:  sum_{k+l=n+1} ( k p_k q_l' - l q_l p_k' ) = kappa [n==2].
Given all rows above, row n = l+11 is a first-order linear ODE for q_l with source involving p_{l-4}.
We solve for polynomial q_l with symbolic coefficients (exact linear algebra) and record the
polynomiality/bound conditions on the p rows.  Necessary conditions only.
"""
import sympy as s, sys, time, json
from math import ceil, floor
y = s.symbols('y'); tau = s.symbols('tau')
h = 1 + y**5; c = y**3*h

def pb(k):  # (min y-order, mult at -1, max deg) for p_k
    return (max(0, k-3), max(0, ceil(k/4)), min(24, floor((84+k)/4)))
def qb(l):
    return (max(0, l-4), max(0, ceil(l/4)), min(32, floor((112+l)/4)))

def row_equation(P, Q, n):
    """coefficient of x^n in P_x Q_y - P_y Q_x, with P,Q dicts k->poly."""
    tot = 0
    for k, pk in P.items():
        l = n + 1 - k
        if l in Q:
            tot += k*pk*s.diff(Q[l], y) - l*Q[l]*s.diff(pk, y)
    return s.expand(tot)

def solve_q_row(P, Q, l, params):
    """Solve row n=l+11 for polynomial q_l within its bounds. Returns (q_l, conditions_on_params)."""
    lo, m1, hi = qb(l)
    coeffs = s.symbols(f'q{l}_0:{hi-lo+1}')
    ql = sum(cf*y**(lo+i) for i, cf in enumerate(coeffs))
    Q2 = dict(Q); Q2[l] = ql
    eq = row_equation(P, Q2, l+11)
    eqs = s.Poly(eq, y).all_coeffs()
    # multiplicity at -1
    eqs += [s.diff(ql, y, j).subs(y, -1) for j in range(m1)]
    sol = s.linsolve(eqs, list(coeffs))
    return ql, coeffs, sol

if __name__ == '__main__':
    t0 = time.time()
    # Astra 13 data, mu = 1
    E1 = 3+5*y**4+8*y**5; E2 = 3+5*y**2+8*y**5
    R = 12+5*y**3+60*y**4+79*y**5+30*y**8+110*y**9+92*y**10
    P = {12: s.expand(c**3), 11: s.expand(y**8*h**2*E1), 10: s.expand(y**7*h*R/3 + tau*y**8*h**2*E2)}
    Q = {16: s.expand(c**4)}
    # reproduce q15, q14 and check they are polynomial (known from Astra 12)
    for l in (15, 14):
        ql, cf, sol = solve_q_row(P, Q, l, [tau])
        sol = list(sol); assert len(sol) == 1, (l, sol)
        Q[l] = s.expand(ql.subs(dict(zip(cf, sol[0]))))
        print(f"q{l} solved: deg {s.degree(Q[l], y)}, free q-params: {sorted(Q[l].free_symbols - {y, tau}, key=str)}", flush=True)
    print("elapsed", round(time.time()-t0, 1), flush=True)
    # sanity: q15 = 4/3 c p11
    assert s.expand(Q[15] - s.Rational(4,3)*c*P[11]) == 0
    print("PASS: q15 = 4/3 c p11 reproduced", flush=True)
