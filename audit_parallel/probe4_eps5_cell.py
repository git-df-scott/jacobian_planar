import sympy as sp
v,c = sp.symbols('v c')
def T(R,D,k): return (v+1)**k*(3*v*(v+1)*sp.diff(R,v)-D*R)
def solve_box(D,k,m,n):
    a = sp.symbols('u0:%d'%(n+1))
    N = sum(a[i]*v**i for i in range(n+1))
    R = N/((v+1)**m)
    num,_ = sp.fraction(sp.cancel(sp.together(T(R,D,k)+c)))
    eqs = sp.Poly(sp.expand(num),v).all_coeffs()
    A,b = sp.linear_eq_to_matrix(eqs,a)
    return "NO SOLUTION" if A.rank()!=A.row_join(b).rank() else "solutions exist, nullity=%d"%(len(a)-A.rank())
print("(D,k)=(69,24), box m=24 n=28 :", solve_box(69,24,24,28))
