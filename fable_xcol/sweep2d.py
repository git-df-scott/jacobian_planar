"""CONSTRUCTIVE ROUTE: can a tangent-sweep construction produce {P,Q} = x^2 in
the PLANE, and can it carry the pentagon's Newton polygon?

The n>=3 counterexamples (Alpoge/Gallagher/Speyer/Gao, arXiv:2608.00222) sweep
tangent lines of a plane curve.  A LINEAR sweep T = K(w) + g*delta(w) has
det J = (a q' - p' b) + g (a b' - b a'), which is at most LINEAR in g -- it can
never equal g^2.  So try a QUADRATIC sweep:

    T(g,w) = ( p + g a + g^2 c ,  q + g b + g^2 d )

det J = T1_g T2_w - T1_w T2_g, and we demand det J == g^2 exactly, i.e. with
(g,w) playing the role of (x,y) this is {P,Q} = x^2 -- our target equation.
Collecting powers of g gives four conditions:

    g^0 :  a q' - p' b                       = 0
    g^1 :  a b' - a' b + 2(c q' - p' d)      = 0
    g^2 :  a d' + 2 c b' - c' b - 2 a' d     = 1
    g^3 :  2(c d' - c' d)                    = 0

Solve for polynomial p,q,a,b,c,d and inspect the Newton polygon of the result.
"""
import sympy as sp
g, w = sp.symbols('g w')

def sweep(p,q,a,b,c,d):
    T1 = p + g*a + g**2*c
    T2 = q + g*b + g**2*d
    return sp.expand(sp.diff(T1,g)*sp.diff(T2,w) - sp.diff(T1,w)*sp.diff(T2,g))

print("=== the four conditions, symbolically ===")
P_,Q_,A_,B_,C_,D_ = [sp.Function(n)(w) for n in 'pqabcd']
J = sweep(P_,Q_,A_,B_,C_,D_)
for k in range(4):
    print(f"  g^{k}: ", sp.simplify(sp.expand(J).coeff(g,k)))

print("\n=== search: low-degree polynomial solutions ===")
def trial(dp,dq,da,db,dc,dd,label):
    cs=[]
    def poly(deg,tag):
        co=[sp.Symbol(f'{tag}{i}') for i in range(deg+1)]
        cs.extend(co); return sum(co[i]*w**i for i in range(deg+1))
    p=poly(dp,'p'); q=poly(dq,'q'); a=poly(da,'a')
    b=poly(db,'b'); c=poly(dc,'c'); d=poly(dd,'d')
    J=sp.expand(sweep(p,q,a,b,c,d)-g**2)
    eqs=[]
    Pj=sp.Poly(J,g)
    for (e,),co in zip(Pj.monoms(),Pj.coeffs()):
        cc=sp.Poly(sp.expand(co),w).all_coeffs()
        eqs+= [t for t in cc if t!=0]
    sol=sp.solve(eqs,cs,dict=True)
    real=[s for s in sol if not all(v==0 for v in s.values())]
    print(f"  {label}: {len(eqs)} eqs, {len(cs)} unknowns -> {len(sol)} solution branch(es)")
    return sol,cs,(p,q,a,b,c,d)

for args in [(1,1,0,1,0,0,'deg p,q<=1, a const, b lin, c,d const'),
             (2,2,1,1,0,0,'deg 2 curve, linear a,b, constant c,d'),
             (3,3,2,2,1,1,'deg 3 curve, quadratic a,b, linear c,d')]:
    sol,cs,polys=trial(*args)
    if sol:
        s0=sol[0]
        got=[sp.simplify(x.subs(s0)) for x in polys]
        Jc=sp.expand(sweep(*got))
        print(f"     -> check det J = {sp.simplify(Jc)}  (target g^2)")
        if sp.simplify(Jc-g**2)==0:
            T1=sp.expand(got[0]+g*got[2]+g**2*got[4])
            T2=sp.expand(got[1]+g*got[3]+g**2*got[5])
            print("     EXPLICIT SOLUTION FOUND")
            print("       P =",T1)
            print("       Q =",T2)
            for nm,T in (("N(P)",T1),("N(Q)",T2)):
                if T==0: print(f"       {nm}: zero"); continue
                mon=sp.Poly(T,g,w).monoms()
                print(f"       {nm} support (x-exp,y-exp): {sorted(set(mon))}")
