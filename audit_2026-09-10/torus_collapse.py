"""
Planar Keller maps with a nontrivial C* symmetry collapse.

C* acts on C^2 with coprime weights (a,-b), a,b>0 (mixed signs; same-sign weights make
the map proper hence trivial).  Invariant: u = x^b y^a.  A map equivariant for the
same action on the target has P of weight a and Q of weight -b, i.e.
    P = x * A(u),   Q = y * B(u)      (only possibility: monomials x^{1+bk} y^{ak}, etc.)
Claim: det J(P,Q) = A B + u (a A B' + b A' B)   (exact, checked below for several (a,b)),
and this is constant iff A,B are constants (leading coefficient a0 b0 (1 + a q + b p) != 0).
So no plane Keller map with a nontrivial torus symmetry can be a counterexample.
Also check the case (a,0): P = x A(y), Q = B(y) -> det = A(y) B'(y) -> triangular.
"""
import sympy as sp
x,y,u = sp.symbols('x y u')
N = 4
A = sum(sp.Symbol(f'a{i}')*u**i for i in range(N+1))
B = sum(sp.Symbol(f'b{i}')*u**i for i in range(N+1))
for (a,b) in [(1,1),(1,2),(2,1),(2,3),(3,2),(1,3)]:
    U = x**b*y**a
    P = sp.expand(x*A.subs(u,U)); Q = sp.expand(y*B.subs(u,U))
    det = sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x))
    formula = sp.expand((A*B + u*(a*A*sp.diff(B,u) + b*sp.diff(A,u)*B)).subs(u,U))
    assert sp.expand(det-formula)==0, (a,b)
    # leading coefficient in u of the formula:
    lead = sp.Poly(sp.expand(A*B + u*(a*A*sp.diff(B,u)+b*sp.diff(A,u)*B)), u).LC()
    print(f"weights ({a},-{b}): det J = A B + u(a A B' + b A' B)  [verified];  top u-coefficient = {sp.factor(lead)}")
print("=> top coefficient a_N b_N (1 + aN + bN) is nonzero unless deg A = deg B = 0: constant Jacobian forces A,B constant.")
# Now the concrete question for Alpoge-type examples: is there ANY C*-equivariant plane Keller map beyond linear/triangular?
# weights (a,0): P = x*A(y), Q = B(y)
Ay = sum(sp.Symbol(f'a{i}')*y**i for i in range(N+1)); By = sum(sp.Symbol(f'b{i}')*y**i for i in range(N+1))
P = x*Ay; Q = By
det = sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x))
print("weights (a,0): det J =", sp.factor(det), " -> constant iff A const and B linear: triangular map.")
