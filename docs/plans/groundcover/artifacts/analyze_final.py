import msparse, json, random, re
from fractions import Fraction
F='/tmp/claude-0/-home-user-jacobian-planar/bffaee33-4b8d-59cb-b6bb-ff5a3ac3aeb8/scratchpad/wt/mailbox/wave6/frontier/'
V,CH,P = msparse.load(F+'trackB1_sat_Q.ms'); idx={v:i for i,v in enumerate(V)}; n=len(V); R={}
def ij(v):
    m=re.fullmatch(r'[cds]_(\d+)_(\d+)',v); return (int(m.group(1)),int(m.group(2))) if m else None
def wvec(f):
    w={}
    for v in V: w[v]=f(*ij(v)) if ij(v) else 0
    return w
def viol_gens(w):
    out=[]
    for gi,g in enumerate(P):
        if gi==283: continue
        ws={sum(w[v]*e for v,e in m) for m in g}
        if len(ws)>1: out.append(gi)
    return out
for nm,f in [('2i-j',lambda i,j:2*i-j),('i',lambda i,j:i),('j',lambda i,j:j),('i+j',lambda i,j:i+j)]:
    vg=viol_gens(wvec(f)); R['viol_%s'%nm]={'n':len(vg),'first':vg[:12]}
# what breaks w=i?
w=wvec(lambda i,j:i); ex=[]
for gi in viol_gens(w)[:6]:
    g=P[gi]; ex.append({'gen':gi,'weights':sorted({sum(w[v]*e for v,e in m) for m in g}),
      'sample_monos':['*'.join(v for v,e in m for _ in range(e)) or '1' for m in list(g)[:4]]})
R['w_eq_i_breakers']=ex

# ---------- (5) free branch, FULL affine-linear fixed point ----------
def pmul(a,b):
    o={}
    for m1,c1 in a.items():
        for m2,c2 in b.items():
            d=dict(m1)
            for v,e in m2: d[v]=d.get(v,0)+e
            k=tuple(sorted(d.items())); o[k]=o.get(k,Fraction(0))+c1*c2
    return {m:c for m,c in o.items() if c!=0}
def subst(g,var,L):
    o={}
    for m,c in g.items():
        d=dict(m); e=d.pop(var,0)
        cur={tuple(sorted(d.items())):c}
        for _ in range(e): cur=pmul(cur,L)
        for k,v in cur.items():
            o[k]=o.get(k,Fraction(0))+v
    return {m:c for m,c in o.items() if c!=0}
Pb=[dict(g) for g in P]
for z in ('d_0_1','d_1_1'):
    Pb=[subst(g,z,{}) for g in Pb]
elim={'d_0_1':'0','d_1_1':'0'}; consts=[]; rounds=0; log=[]
while rounds<3000:
    rounds+=1
    Pb=[g for g in Pb if g]
    bad=[i for i,g in enumerate(Pb) if len(g)==1 and () in g]
    if bad: consts.append({'gen':bad[0],'value':str(Pb[bad[0]][()])}); break
    pick=None
    for gi,g in enumerate(Pb):
        if all(sum(e for _,e in m)<=1 for m in g):
            vs=[m for m in g if m!=()]
            if not vs: continue
            # prefer single-variable
            pick=(gi,vs[0][0][0],len(vs))
            if len(vs)==1: break
    if pick is None: break
    gi,var,nv=pick; g=Pb[gi]; a=g[((var,1),)]
    L={m:-c/a for m,c in g.items() if m!=((var,1),)}
    log.append({'var':var,'from_gen':gi,'n_terms_in_solution':len(L)})
    elim[var]=' + '.join(('%s*%s'%(c,'*'.join(x for x,_ in m)) if m else str(c)) for m,c in L.items()) or '0'
    Pb=[subst(g2,var,L) for j,g2 in enumerate(Pb) if j!=gi]
    if sum(len(x) for x in Pb)>400000: log.append({'ABORT':'term blowup'}); break
Pb=[g for g in Pb if g]
used=set(v for g in Pb for m in g for v,_ in m)
R['free_branch']={'rounds':rounds,'eqs_after':len(Pb),'vars_after':len(used),
 'vars_eliminated':len(elim),'eliminations':log,'assignments':elim,
 'constants_found':consts,'empty_over_Q':bool(consts),'terms_after':sum(len(g) for g in Pb),
 'max_degree_after':max((sum(e for _,e in m) for g in Pb for m in g),default=0)}

# ---------- (6) c-linear system, two independent random d-points ----------
CB=[v for v in V if v.startswith('c_')]; ci={v:i for i,v in enumerate(CB)}; nc=len(CB)
def rank(mat,ncol):
    mat=[list(r) for r in mat]; rk=0
    for col in range(ncol):
        sel=next((i for i in range(rk,len(mat)) if mat[i][col]!=0),None)
        if sel is None: continue
        mat[rk],mat[sel]=mat[sel],mat[rk]; pv=mat[rk][col]
        for i in range(rk+1,len(mat)):
            if mat[i][col]:
                f=mat[i][col]/pv; mat[i]=[a-f*b for a,b in zip(mat[i],mat[rk])]
        rk+=1
    return rk
runs=[]
for seed in (11,4242):
    random.seed(seed)
    val={v:Fraction(random.randint(1,10**6),random.randint(1,997)) for v in V if not v.startswith('c_')}
    rows=[]
    for gi,g in enumerate(P):
        if gi==283: continue
        r=[Fraction(0)]*nc; rhs=Fraction(0)
        for m,c in g.items():
            cv=[v for v,e in m if v.startswith('c_') for _ in range(e)]
            coef=c
            for v,e in m:
                if not v.startswith('c_'): coef*=val[v]**e
            if cv: r[ci[cv[0]]]+=coef
            else: rhs-=coef
        rows.append(r+[rhs])
    rM=rank([r[:nc] for r in rows],nc); rA=rank(rows,nc+1)
    runs.append({'seed':seed,'rows':len(rows),'rank_M':rM,'rank_aug':rA,'consistent':rM==rA})
R['c_linear_system']={'n_c_unknowns':nc,'runs':runs,'generic_rank':runs[0]['rank_M'],
 'determined':'over','n_equations':283,
 'note':'gen 283 (saturation, deg_c=2) excluded'}
json.dump(R,open('final.json','w'),indent=1,default=str)
print(json.dumps(R,indent=1,default=str)[:7000])
