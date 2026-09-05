"""Branching cascade over F_p-bar: incremental GB by greedy blocks, with
 - squarefree parts of univariate GB elements added, linear ones substituted,
 - monomial GB elements split into coordinate-hyperplane branches (v = 0),
so every branch shrinks. Union of branch varieties = variety of the input (sound for emptiness)."""
import re, sys, os, subprocess, time, json, collections
import flint
src, outdir = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True)
M='/tmp/msolve-0.10.1/bin/msolve'; CAP=int(os.environ.get('CAP_KB','5000000')); TMO=int(os.environ.get('TMO','900')); THR=os.environ.get('THR','2')
MAXBR=int(os.environ.get('MAXBR','400'))
lines=open(src).read().split('\n'); names=lines[0].split(','); p=int(lines[1])
body='\n'.join(lines[2:]); gens0=[g.strip().rstrip(',') for g in re.split(r',\s*\n', body) if g.strip()]
def terms(g):
    out={}
    for term in re.findall(r'[+-]?[^+-]+', g.replace(' ','')):
        cf=1; mon={}
        for fac in term.split('*'):
            if re.fullmatch(r'[+-]?\d+', fac): cf=int(fac)
            else:
                m=re.fullmatch(r'([+-]?)([A-Za-z_]\w*)(?:\^(\d+))?', fac)
                if m.group(1)=='-': cf=-cf
                mon[m.group(2)]=mon.get(m.group(2),0)+int(m.group(3) or 1)
        k=tuple(sorted(mon.items())); out[k]=(out.get(k,0)+cf)%p
    return {k:c for k,c in out.items() if c}
def tostr(T):
    if not T: return None
    return '+'.join(str(c)+''.join(f'*{v}^{e}' if e>1 else f'*{v}' for v,e in k) for k,c in sorted(T.items()))
def subst(T, fixed):
    acc={}
    for k,c in T.items():
        cc=c; m2=[]
        for v,e in k:
            if v in fixed: cc=cc*pow(fixed[v],e,p)%p
            else: m2.append((v,e))
        if cc: kk=tuple(m2); acc[kk]=(acc.get(kk,0)+cc)%p
    return {k:c for k,c in acc.items() if c}
def sqf_univ(T, v):
    deg=max(e for k,_ in T.items() for vv,e in k) if any(k for k in T) else 0
    coeffs=[0]*(deg+1)
    for k,c in T.items(): coeffs[k[0][1] if k else 0]=c
    f=flint.nmod_poly(coeffs, p); g=f.gcd(f.derivative()); s=f//g
    cs=[int(x) for x in s.coeffs()]
    return {((v,i),) if i>0 else (): c for i,c in enumerate(cs) if c}
def run_gb(polys, vs, tag):
    fn=f'{outdir}/{tag}.ms'; open(fn,'w').write(','.join(vs)+'\n'+str(p)+'\n'+',\n'.join(polys)+'\n')
    pr=subprocess.run(f'ulimit -v {CAP}; timeout {TMO} {M} -g 2 -t {THR} -f {fn} -o {fn}.out', shell=True, capture_output=True, text=True)
    out=open(fn+'.out').read() if os.path.exists(fn+'.out') else ''
    if not out.strip(): return None, f'NO OUTPUT exit={pr.returncode} {pr.stderr.strip()[-100:]}'
    basis=re.search(r'\[(.*)\]:\s*$', out, re.S).group(1)
    return [re.sub(r'\^1(?![0-9])','',b.strip()) for b in basis.split(',\n') if b.strip()], None
# worklist of branches: (fixed, remaining_terms(list of dict), gb_terms(list of dict), hist)
work=[({}, [terms(g) for g in gens0], [], [])]
results=[]; nrun=0; t0=time.time()
while work:
    fixed, rem, gb, hist = work.pop()
    if len(results)>MAXBR: results.append(dict(hist=hist, result='BRANCH LIMIT')); break
    # normalise: substitute fixed, drop zeros, detect constants
    rem=[subst(T,fixed) for T in rem]; gb=[subst(T,fixed) for T in gb]
    rem=[T for T in rem if T]; gb=[T for T in gb if T]
    if any(all(not k for k in T) for T in rem+gb): results.append(dict(hist=hist, result='EMPTY (constant)')); continue
    # simplifications loop
    progress=True
    while progress:
        progress=False
        for T in list(gb)+list(rem):
            vs=set(v for k in T for v,_ in k)
            if len(T)==1 and len(vs)>=1:   # monomial => branch on variables
                k=list(T.keys())[0]
                branch_vars=[v for v,_ in k]
                # branch: first var = 0 | (first var != 0 handled by next var = 0 ... ) -> exhaustive union: v_i = 0 for some i
                for v in branch_vars:
                    f2=dict(fixed); f2[v]=0
                    work.append((f2, [dict(x) for x in rem], [dict(x) for x in gb], hist+[f'{v}=0']))
                progress=False; T=None
                break
            if len(vs)==1:                    # univariate: squarefree part; linear => substitute
                v=list(vs)[0]; S=sqf_univ(T, v)
                if max((e for k in S for _,e in k), default=0)==1:
                    a=[c for k,c in S.items() if k][0]; b=S.get((),0); val=(-b*pow(a,p-2,p))%p
                    f2=dict(fixed); f2[v]=val
                    work.append((f2, rem, gb, hist+[f'{v}={val}'])); T=None; break
                elif S!=T:
                    gb.append(S); progress=True
        else:
            continue
        break
    else:
        pass
    if T is None: continue   # branched or substituted; the branch(es) were pushed
    if not rem:
        vs=sorted(set(v for T in gb for k in T for v,_ in k))
        results.append(dict(hist=hist, result='NONUNIT', nvars=len(vs), gb_size=len(gb), maxdeg=max(sum(e for _,e in k) for T in gb for k in T),
                            gb=[tostr(T) for T in gb][:50], fixed=fixed)); print('NONUNIT branch', hist, len(vs), 'vars', len(gb), 'gb', flush=True); continue
    # next block: greedy fewest new variables then most gens
    cur=set(v for T in gb for k in T for v,_ in k)
    blocks=collections.OrderedDict()
    for T in rem: blocks.setdefault(frozenset(v for k in T for v,_ in k), []).append(T)
    s=min(blocks, key=lambda s:(len(s-cur), -len(blocks[s]), sorted(s)))
    newrem=[T for T in rem if frozenset(v for k in T for v,_ in k)!=s]
    vs=[v for v in names if v in (cur|s)]
    nrun+=1
    B,err=run_gb([tostr(T) for T in gb+blocks[s]], vs, f'b{nrun}')
    if err: results.append(dict(hist=hist, result='WALL '+err, nvars=len(vs), ngens=len(gb)+len(blocks[s]))); print('WALL', hist, err[:80], flush=True); continue
    if B==['1']: results.append(dict(hist=hist, result='EMPTY [1]', stage_vars=len(vs))); print('EMPTY branch', hist, flush=True); continue
    gbT=[terms(b) for b in B]
    print(f'run {nrun}: hist {hist} vars {len(vs)} gens {len(gb)+len(blocks[s])} -> gb {len(B)} maxdeg {max(sum(e for _,e in k) for T in gbT for k in T)} rem {len(newrem)} ({round(time.time()-t0)}s)', flush=True)
    work.append((fixed, newrem, gbT, hist))
summary=collections.Counter(r['result'].split(' ')[0] for r in results)
print('DONE runs', nrun, 'branches', len(results), dict(summary), round(time.time()-t0),'s')
json.dump(results, open(f'{outdir}/results.json','w'), indent=1)
