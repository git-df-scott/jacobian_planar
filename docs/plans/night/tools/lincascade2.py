"""Exact linear-chain elimination for the y-adic chart systems over F_p-bar.
After the nonlinear first block, every block is linear in its new variables. Each stage is a fraction-free
linear solve over F_p[free parameters]; pivots branch (pivot != 0 generic / pivot = 0 added as constraint);
compatibility rows become constraints. A branch ends with (free params F, constraints C, nonzeros N);
consistency is decided exactly (univariate gcd if |F| = 1, else msolve on the small system)."""
import re, sys, os, subprocess, json, time, collections, itertools
import flint
src, outdir = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True)
M='/tmp/msolve-0.10.1/bin/msolve'; MAXBR=int(os.environ.get('MAXBR','2000'))
lines=open(src).read().split('\n'); names=lines[0].split(','); p=int(lines[1])
body='\n'.join(lines[2:]); gens0=[g.strip().rstrip(',') for g in re.split(r',\s*\n', body) if g.strip()]
ctx=flint.nmod_mpoly_ctx.get(tuple(names), ordering='degrevlex', modulus=p)
G=dict(zip(names, ctx.gens())); ZERO=ctx.from_dict({}); ONE=ctx.from_dict({tuple([0]*len(names)):1})
def parse(g):
    d={}
    for term in re.findall(r'[+-]?[^+-]+', g.replace(' ','')):
        cf=1; mon=[0]*len(names)
        for fac in term.split('*'):
            if re.fullmatch(r'[+-]?\d+', fac): cf=int(fac)
            else:
                m=re.fullmatch(r'([+-]?)([A-Za-z_]\w*)(?:\^(\d+))?', fac)
                if m.group(1)=='-': cf=-cf
                mon[names.index(m.group(2))]+=int(m.group(3) or 1)
        k=tuple(mon); d[k]=(d.get(k,0)+cf)%p
    return ctx.from_dict({k:c for k,c in d.items() if c})
def vars_of(f): return set(names[i] for i,d in enumerate(f.degrees()) if d>0)
def is_const(f): return f.is_constant()
# ---- rational functions
class R:
    __slots__=('n','d')
    def __init__(s,n,d=None):
        if d is None: d=ONE
        if n==ZERO: s.n, s.d = ZERO, ONE; return
        g=n.gcd(d)
        if not g.is_one(): n=n/g; d=d/g   # exact division
        s.n, s.d = n, d
    def __add__(s,o):
        if s.n==ZERO: return o
        if o.n==ZERO: return s
        if s.d==o.d: return R(s.n+o.n, s.d)
        g=s.d.gcd(o.d); return R(s.n*(o.d/g)+o.n*(s.d/g), s.d*(o.d/g))
    def __mul__(s,o):
        if s.n==ZERO or o.n==ZERO: return R(ZERO)
        return R(s.n*o.n, s.d*o.d)
    def neg(s): return R(-s.n, s.d)
def rpow(r,e):
    out=R(ONE)
    for _ in range(e): out=out*r
    return out
def eval_rat(f, subs):
    """substitute subs (var -> R) into polynomial f; returns R"""
    if not (vars_of(f) & set(subs)): return R(f)
    acc=R(ZERO); cache={}
    for mon, cf in zip(f.monoms(), f.coeffs()):
        term=R(ctx.from_dict({tuple(0 if names[i] in subs else e for i,e in enumerate(mon)): int(cf)}))
        for i,e in enumerate(mon):
            if e and names[i] in subs:
                key=(names[i],e)
                if key not in cache: cache[key]=rpow(subs[names[i]], e)
                term=term*cache[key]
        acc=acc+term
    return acc
def subs_zero(f, zeros):
    if not (vars_of(f) & zeros): return f
    d={}
    for mon,cf in zip(f.monoms(), f.coeffs()):
        if any(mon[names.index(v)] for v in zeros if v in names): continue
        d[tuple(mon)]=(d.get(tuple(mon),0)+int(cf))%p
    return ctx.from_dict({k:c for k,c in d.items() if c})
def lin_split(f, newv):
    """f linear in newv: return ({v: A_v}, B) as polynomials"""
    A={v:ZERO for v in newv}; B=ZERO
    for mon,cf in zip(f.monoms(), f.coeffs()):
        nv=[names[i] for i,e in enumerate(mon) if e and names[i] in newv]
        m2=list(mon)
        if not nv: B+=ctx.from_dict({tuple(m2):int(cf)}); continue
        assert len(nv)==1 and mon[names.index(nv[0])]==1, 'not linear'
        m2[names.index(nv[0])]=0; A[nv[0]]+=ctx.from_dict({tuple(m2):int(cf)})
    return A,B
# ---- initial: linear univariate fixes (w=1,u=1)
polys=[parse(g) for g in gens0]; fixed_vals={}
for f in polys:
    vs=vars_of(f)
    if len(vs)==1 and f.total_degree()==1:
        v=list(vs)[0]; a=int(f.coefficient(0)) if False else None
        # f = a*v + b
        A,B=lin_split(f,{v}); fixed_vals[v]=(-int(B.coeffs()[0]) if B!=ZERO else 0)*pow(int(A[v].coeffs()[0]),p-2,p)%p
print('fixed', fixed_vals, flush=True)
def subs_vals(f, vals):
    if not (vars_of(f) & set(vals)): return f
    d={}
    for mon,cf in zip(f.monoms(), f.coeffs()):
        c=int(cf); m2=list(mon)
        for v,val in vals.items():
            i=names.index(v)
            if m2[i]: c=c*pow(val,m2[i],p)%p; m2[i]=0
        d[tuple(m2)]=(d.get(tuple(m2),0)+c)%p
    return ctx.from_dict({k:c for k,c in d.items() if c})
polys=[subs_vals(f,fixed_vals) for f in polys]; polys=[f for f in polys if f!=ZERO]
# ---- branch state: dict(zeros=set, det={var:R}, free=set, C=[polys], N=[polys], rem=[polys], hist=[])
def msolve_gb(polys, vs, tag):
    fn=f'{outdir}/{tag}.ms'; open(fn,'w').write(','.join(vs)+'\n'+str(p)+'\n'+',\n'.join(str(f) for f in polys)+'\n')
    subprocess.run(f'ulimit -v 3000000; timeout 600 {M} -g 2 -f {fn} -o {fn}.out', shell=True, capture_output=True)
    out=open(fn+'.out').read() if os.path.exists(fn+'.out') else ''
    if not out.strip(): return None
    basis=re.search(r'\[(.*)\]:\s*$', out, re.S).group(1)
    return [parse(re.sub(r'\^1(?![0-9])','',b.strip())) for b in basis.split(',\n') if b.strip()]
work=[dict(zeros=frozenset(), avoid=frozenset(), det={}, free=set(), C=[], N=[], nz=frozenset(), rem=polys, hist=[])]
visited=set(); results=[]; t0=time.time(); nb=0
def push_zero_branches(st, mvars, why):
    """the current branch is covered by the union over v in mvars of {v=0}: push fresh restarts"""
    for v in sorted(mvars):
        key=(st['zeros']|{v}, st['avoid'])
        if key in visited: continue
        visited.add(key)
        work.append(dict(zeros=st['zeros']|{v}, avoid=st['avoid'], det={}, free=set(), C=[], N=[], nz=frozenset(), rem=polys, hist=[f'{v}=0']))
def monomial_vars(f):
    return vars_of(f) if len(f.monoms())==1 else None
while work:
    st=work.pop(); nb+=1
    if nb>MAXBR: results.append(dict(hist=st['hist'], result='BRANCH LIMIT')); break
    rem=[subs_zero(f, st['zeros']) for f in st['rem']]; rem=[f for f in rem if f!=ZERO]
    if any(is_const(f) for f in rem): results.append(dict(hist=st['hist'], result='EMPTY (constant)')); continue
    Cs=[subs_zero(f, st['zeros']) for f in st['C']]; Cs=[f for f in Cs if f!=ZERO]
    if any(is_const(f) for f in Cs): results.append(dict(hist=st['hist'], result='EMPTY (constant constraint)')); continue
    mono=[monomial_vars(f) for f in Cs if monomial_vars(f) is not None]
    if mono:
        mv=min(mono, key=len); mv=mv-st['nz']
        if not mv: results.append(dict(hist=st['hist'], result='EMPTY (monomial constraint in nonzero variables)')); continue
        push_zero_branches(st, mv, 'constraint'); continue
    st['C']=Cs
    # monomial rem generators -> zero branches too
    monor=[monomial_vars(f) for f in rem if monomial_vars(f) is not None]
    if monor:
        mv=min(monor, key=len)-st['nz']
        if not mv: results.append(dict(hist=st['hist'], result='EMPTY (monomial generator in nonzero variables)')); continue
        push_zero_branches(st, mv, 'generator'); continue
    if not rem:
        results.append(dict(hist=st['hist'], result='END', zeros=sorted(st['zeros']), nz=sorted(st['nz']), avoid=sorted(st['avoid']), free=sorted(st['free']), nC=len(st['C']), nN=len(st['N']), C=[str(c) for c in st['C']], N=[str(n) for n in st['N']], det={k:(str(v.n),str(v.d)) for k,v in st['det'].items()})); print(f"[{nb}] END zeros {sorted(st['zeros'])} free {sorted(st['free'])} C {len(st['C'])} avoid {len(st['avoid'])}", flush=True); continue
    cur=set(st['free'])|set(st['det'])|st['zeros']
    blocks=collections.OrderedDict()
    for f in rem: blocks.setdefault(frozenset(vars_of(f)), []).append(f)
    s=min(blocks, key=lambda s:(len(s-cur), -len(blocks[s]), sorted(s)))
    newv=s-cur; blk=blocks[s]; newrem=[f for f in rem if frozenset(vars_of(f))!=s]
    dmax=max(max((sum(mon[names.index(v)] for v in newv) for mon in f.monoms()), default=0) for f in blk) if newv else 0
    if newv and dmax>1:
        if st['det'] or st['free']:
            results.append(dict(hist=st['hist'], result=f'NONLINEAR BLOCK with existing params: new {sorted(newv)} deg {dmax}')); continue
        B=msolve_gb(blk, sorted(s), f'nl{nb}')
        if B is None: results.append(dict(hist=st['hist'], result='WALL nonlinear block')); continue
        if B==[ONE]: results.append(dict(hist=st['hist'], result='EMPTY [1] (nonlinear block)')); continue
        nil=set()
        for b in B:
            vs=vars_of(b)
            if len(b.monoms())==1 and len(vs)==1: nil|=vs
        rest=[subs_zero(b, nil) for b in B]; rest=[b for b in rest if b!=ZERO]
        st2=dict(st); st2['zeros']=st['zeros']|frozenset(nil); st2['free']=st['free']|(s-nil); st2['C']=st['C']+rest; st2['rem']=newrem; st2['hist']=st['hist']+[f'{v}=0' for v in sorted(nil)]
        print(f"[{nb}] nonlinear block {sorted(s)}: GB {len(B)}, nilpotent {sorted(nil)}, residual constraints {len(rest)}, free {sorted(st2['free'])}", flush=True)
        work.append(st2); continue
    # linear stage: rows
    rows=[]
    for f in blk:
        A,Bc=lin_split(f, newv)
        Ar={v:eval_rat(A[v], st['det']) for v in newv}; Br=eval_rat(Bc, st['det'])
        L=ONE
        for r in list(Ar.values())+[Br]:
            g=L.gcd(r.d); L=L*(r.d/g)
        row=({v:Ar[v].n*(L/Ar[v].d) for v in newv}, Br.n*(L/Br.d))
        az=st.get('avoid',set())
        if az:
            row=({v:(ZERO if str(row[0][v]) in az else row[0][v]) for v in newv}, row[1])
        rows.append(row)
    # elimination with pivot branching
    cols=sorted(newv); piv={}; N=list(st['N']); C=list(st['C']); alt=[]
    for col in cols:
        cands=[i for i,(A,B) in enumerate(rows) if i not in piv.values() and A[col]!=ZERO and str(A[col]) not in st.get('avoid',set())]
        if not cands: continue
        i=min(cands, key=lambda i:(len(rows[i][0][col].monoms()), rows[i][0][col].total_degree()))
        pv=rows[i][0][col]
        if not is_const(pv):
            mvp=monomial_vars(pv)
            if mvp is not None:
                if mvp-st['nz']: push_zero_branches(st, mvp-st['nz'], 'pivot')
                st['nz']=st['nz']|mvp
            else:
                alt.append((i,col,pv))
            N.append(pv)
        piv[col]=i
        for k,(A,B) in enumerate(rows):
            if k==i or A[col]==ZERO: continue
            a=A[col]
            rows[k]=({v:pv*A[v]-a*rows[i][0][v] for v in cols}, pv*B-a*rows[i][1])
    for (i,col,pv) in alt:
        key=(st['zeros'], st['avoid']|{str(pv)})
        if key in visited: continue
        visited.add(key)
        work.append(dict(zeros=st['zeros'], avoid=st['avoid']|{str(pv)}, det={}, free=set(), C=[pv], N=[], nz=frozenset(), rem=polys, hist=[f'piv0:{col}']))
    # back-substitution
    det=dict(st['det']); free=set(st['free'])
    for col in reversed(cols):
        if col not in piv: free.add(col); continue
        A,B=rows[piv[col]]; num=R(B).neg()
        for v in cols:
            if v!=col and A[v]!=ZERO:
                num=num+(R(A[v])*det[v]).neg() if v in det else num+R(A[v]*(-1))*R(G[v])
        det[col]=R(num.n, num.d*A[col])
    newC=[]
    for k,(A,B) in enumerate(rows):
        if k in piv.values(): continue
        if all(A[v]==ZERO for v in cols) and B!=ZERO:
            if is_const(B): newC=None; break
            newC.append(B)
    if newC is None: results.append(dict(hist=st['hist'], result='EMPTY (constant compatibility row)')); print(f'[{nb}] EMPTY branch {st["hist"]}', flush=True); continue
    print(f"[{nb}] linear stage new {cols}: pivots {len(piv)}, compat rows {len(newC)} (max deg {max([c.total_degree() for c in newC], default=0)}), free {sorted(free)}, rem {len(newrem)}, {round(time.time()-t0,1)}s", flush=True)
    work.append(dict(zeros=st['zeros'], avoid=st['avoid'], det=det, free=free, C=C+newC, N=N, nz=st['nz'], rem=newrem, hist=st['hist']+[f'stage{sorted(cols)}']))
json.dump(results, open(f'{outdir}/results.json','w'), indent=1)
print('BRANCHES', collections.Counter(r['result'].split(' ')[0] for r in results))
for r in results:
    if r['result']=='END': print('END', 'zeros', r['zeros'], 'nz', r['nz'], 'free', r['free'], 'C', r['nC'], 'avoid', len(r['avoid']))
