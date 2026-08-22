import sympy as sp
v,c = sp.symbols('v c')
def T(R,D,k): return (v+1)**k*(3*v*(v+1)*sp.diff(R,v)-D*R)
def solve_box(D,k,m,l,n):
    a = sp.symbols('u0:%d'%(n+1))
    N = sum(a[i]*v**i for i in range(n+1))
    R = N/((v+1)**m*v**l)
    expr = sp.together(T(R,D,k)+c)
    num,_ = sp.fraction(sp.cancel(expr)); num = sp.expand(num)
    eqs = sp.Poly(num,v).all_coeffs()
    A,b = sp.linear_eq_to_matrix(eqs,a)
    if A.rank()!=A.row_join(b).rank(): return None
    tup = list(sp.linsolve((A,b),a))[0]
    free = sorted({s for e in tup for s in e.free_symbols}&set(a),key=str)
    reps=[]
    for assign in [{f:0 for f in free}]+[{f:(1 if f==g else 0) for f in free} for g in free]:
        reps.append(sp.cancel(sum(tup[i].subs(assign)*v**i for i in range(n+1))/((v+1)**m*v**l)))
    return (len(free),reps)
def mapdeg(R):
    if R==0: return 0
    nu,de = sp.fraction(sp.cancel(R))
    dn = sp.Poly(sp.expand(nu),v).degree() if sp.expand(nu).has(v) else 0
    dd = sp.Poly(sp.expand(de),v).degree() if sp.expand(de).has(v) else 0
    return max(dn,dd)
def report(D,k,m,extra=4):
    r = solve_box(D,k,m,0,m+extra)
    if r is None: print(f"  D={D} k={k}: NO SOLUTION (box m={m},n={m+extra})"); return
    nf,reps = r
    ds = sorted({mapdeg(R) for R in reps if R!=0})
    print(f"  D={D} k={k}: {'unique' if nf==0 else 'dim%d'%nf}, map-degrees {ds}")
    if nf==0:
        R=reps[0]; print("     verify T(R)+c==0 :", sp.simplify(sp.cancel(sp.together(T(R,D,k)+c)))==0)
print("A. NON-INTEGER D (never tested in the wave3 grid):")
for (D,k,m) in [(sp.Rational(69,5),4,4),(sp.Rational(138,5),9,9),(sp.Rational(69,5),9,9)]:
    report(D,k,m)
print("B. OUT-OF-GRID INTEGER CELLS used downstream (grid was D<=30,k<=6):")
for (D,k,m) in [(39,14,14),(39,13,13),(42,14,14)]:
    report(D,k,m)
