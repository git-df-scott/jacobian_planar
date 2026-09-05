"""THE PERIOD CRITERION -- reformulating {P,Q}=x^2 as a vanishing-cycles problem,
and asking whether P can be COMPOSITE.

{P,Q} = x^2 is X_P(Q) = x^2 with X_P the Hamiltonian field of P.  So the whole
problem is:   for which P does  x^2  lie in the IMAGE of X_P ?
(Confirms the determinantal finding: Q is determined by P, up to Q -> Q + h(P).)

Solvability is classical: Q exists iff the Gelfand-Leray form  x^2 dx^dy / dP
has VANISHING PERIOD on every cycle of every generic fibre.  The number of
independent conditions per fibre is b_1(F_c) = 1 - chi(F_c).

Two consequences tested below.
"""
import sympy as sp
x,y=sp.symbols('x y')

print("=== 1. why the degenerate families are 'easy' ===")
for P,Q,lab in [(x**3/3+y, y, 'P = x^3/3 + y'),
                (x**3/3+y**2, y, 'P = x^3/3 + y^2'),
                (x**3/3+y**5, y, 'P = x^3/3 + y^5')]:
    J=sp.expand(sp.diff(P,x)*sp.diff(Q,y)-sp.diff(P,y)*sp.diff(Q,x))
    print(f"  {lab:20s}, Q = y : {{P,Q}} = {J}")
print("  Any P with P_x = x^2 solves it with Q = y: {P,y} = P_x.")
print("  Those fibres are graphs, simply connected, NO cycles -> periods vanish")
print("  trivially.  That is exactly why every search collapses onto them.\n")

print("=== 2. CAN A PENTAGON P BE COMPOSITE?  P = R(h), deg R = d >= 2 ===")
print("  If P = R(h) then the Newton polygon satisfies N(P) = d * N(h),")
print("  so EVERY vertex of N(P) must have both coordinates divisible by d.")
for nm,V in [("pentagon  N(P)",[(0,0),(1,0),(8,14),(8,16),(0,8)]),
             ("quadrilat N(P)",[(0,0),(1,0),(8,14),(8,16)]),
             ("pentagon  N(Q)",[(0,0),(2,1),(12,21),(12,24),(0,12)])]:
    ok=[d for d in range(2,25) if all(a%d==0 and b%d==0 for a,b in V)]
    print(f"  {nm}: vertices {V}")
    print(f"     d >= 2 dividing every vertex: {ok if ok else 'NONE'}"
          f"   -> {'composite possible' if ok else 'P CANNOT BE COMPOSITE'}")
print("\n  The vertex (1,0) alone forces d = 1: it is the normalisation p_{0,1} != 0.")
print("  So P is NOT a composite polynomial, in either sub-case.\n")

print("=== 3. what that means ===")
print("  Classical tangential-centre / polynomial-moment theory: for many families")
print("  the ONLY way all periods vanish is that P is composite and the form is")
print("  aligned with the composition ('composition conjecture').  Here composition")
print("  is impossible.  So a nondegenerate pentagon solution must exhibit")
print("  VANISHING PERIODS WITHOUT COMPOSITION.")
print("  The composition conjecture is known FALSE in general (Pakovich et al.),")
print("  so this is not an emptiness proof -- but it localises the hunt exactly:")
print("  a counterexample must live in the non-composite vanishing-period locus,")
print("  which is a thin, well-studied, and classifiable phenomenon.")
