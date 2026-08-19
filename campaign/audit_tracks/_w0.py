"""(w=0) in division-free form:  B(2A'F - BE' + B'E) = 2 C A' E.
Degree <= 4 in beta and <= 2 in alpha, so a 35*10 = 350 monomial basis.
Interpolate exactly over K and append to the (w=-1) ideal."""
import sys, itertools, random, time
import trackB1_case2_extend as M
import trackB1_case2_final as FN
p, DEG = M.p, M.DEG

def bmonos(d):
    out=[]
    for k in range(d+1):
        for c in itertools.combinations_with_replacement(range(3), k): out.append(c)
    return out
BM4, AM2 = bmonos(4), bmonos(2)
MON = [(b,a) for b in BM4 for a in AM2]

def setup(const):
    M.CONST = const % p
    C,G = M.build_CG()
    BF0,BFb = M.ksolve(*M.eq_w3_matrix(C,G))
    Mx,_ = M.eq_w2_system(C,G,*M.split_BF(BF0))
    _,Kb = M.ksolve(Mx, [M.kzero()]*len(Mx))
    return C,G,BF0,BFb,Kb

def w0_resid(C,G,BF0,BFb,Kb,beta,alpha):
    vec=list(BF0)
    for cf,bv in zip(beta,BFb):
        vec=[M.kadd(vec[k], M.kmul(cf,bv[k])) for k in range(len(vec))]
    B,F=M.split_BF(vec)
    s2=M.ksolve(*M.eq_w2_system(C,G,B,F))
    if s2 is None: return None
    sol=list(s2[0])
    for cf,kv in zip(alpha,Kb):
        sol=[M.kadd(sol[k], M.kmul(cf,kv[k])) for k in range(len(sol))]
    A=M.poly_from_coeffs(sol[:9],0); E=M.poly_from_coeffs(sol[9:],1)
    X=M.kpadd(M.kpscal(M.kpmul(M.kpder(A),F),2),
              M.kpadd(M.kpscal(M.kpmul(B,M.kpder(E)),-1),
                      M.kpmul(M.kpder(B),E)))
    lhs=M.kpmul(B,X)
    rhs=M.kpscal(M.kpmul(C, M.kpmul(M.kpder(A),E)),2)
    n=max(len(lhs),len(rhs))
    return [M.ksub(lhs[i] if i<len(lhs) else M.kzero(),
                   rhs[i] if i<len(rhs) else M.kzero()) for i in range(n)]

def monval(m,beta,alpha):
    b,a=m; v=M.kone()
    for i in b: v=M.kmul(v,beta[i])
    for i in a: v=M.kmul(v,alpha[i])
    return v

if __name__=="__main__":
    const=int(sys.argv[1]); rng=random.Random(int(sys.argv[2]))
    C,G,BF0,BFb,Kb=setup(const)
    t0=time.time(); rows=[]; vals=[]
    need=len(MON)+20
    while len(rows)<need:
        beta=[[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        alpha=[[rng.randrange(p) for _ in range(DEG)] for _ in range(3)]
        r=w0_resid(C,G,BF0,BFb,Kb,beta,alpha)
        if r is None: continue
        rows.append([monval(m,beta,alpha) for m in MON]); vals.append(r)
    print(f"evaluations done: {len(rows)} pts, {len(MON)} monomials [{time.time()-t0:.0f}s]", flush=True)
    NEQ=len(vals[0])
    polys=[]
    for w in range(NEQ):
        res=M.ksolve(rows,[v[w] if w<len(v) else M.kzero() for v in vals])
        if res is None:
            print(f"  cond {w}: interpolation INCONSISTENT (degree bound low)"); sys.exit(1)
        if len(res[1]): 
            print(f"  cond {w}: underdetermined ({len(res[1])} free)"); sys.exit(1)
        polys.append(res[0])
        print(f"  interpolated condition {w+1}/{NEQ} [{time.time()-t0:.0f}s]", flush=True)
    def kstr(e):
        ts=[(f"{e[i]}*a^{i}" if i>1 else (f"{e[i]}*a" if i==1 else f"{e[i]}")) for i in range(DEG) if e[i]]
        return "("+"+".join(ts)+")" if ts else "0"
    out=[]
    for cf in polys:
        terms=[]
        for c,(b,a) in zip(cf,MON):
            if M.kis0(c): continue
            s=kstr(c)
            for i in b: s+=f"*b({i+1})"
            for i in a: s+=f"*al({i+1})"
            terms.append(s)
        out.append("+".join(terms) if terms else "0")
    open(f"_w0_{const}.txt","w").write(",\n".join(out))
    print(f"[wrote _w0_{const}.txt : {len(out)} conditions]")
