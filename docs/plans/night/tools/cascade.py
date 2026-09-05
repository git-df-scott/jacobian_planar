"""Incremental (cascade) Groebner run on a chart system: exploit the y-adic block structure.
Stage k feeds msolve the previous stage's reduced GB plus the next support block. [1] at any stage = EMPTY."""
import re, sys, os, subprocess, time, json, collections
src, outdir = sys.argv[1], sys.argv[2]; os.makedirs(outdir, exist_ok=True)
M='/tmp/msolve-0.10.1/bin/msolve'; CAP=int(os.environ.get('CAP_KB','6000000')); TMO=int(os.environ.get('TMO','1800')); THR=os.environ.get('THR','2')
lines=open(src).read().split('\n'); names=lines[0].split(','); p=int(lines[1])
body='\n'.join(lines[2:]); gens=[g.strip().rstrip(',') for g in re.split(r',\s*\n', body) if g.strip()]
def terms(g):
    out=[]
    for term in re.findall(r'[+-]?[^+-]+', g.replace(' ','')):
        cf=1; mon={}
        for fac in term.split('*'):
            if re.fullmatch(r'[+-]?\d+', fac): cf=int(fac)
            else:
                m=re.fullmatch(r'([+-]?)([A-Za-z_]\w*)(?:\^(\d+))?', fac)
                if m.group(1)=='-': cf=-cf
                mon[m.group(2)]=mon.get(m.group(2),0)+int(m.group(3) or 1)
        out.append((mon,cf%p))
    return [(m,c) for m,c in out if c]
def tostr(T):
    T=[(m,c) for m,c in T if c]
    if not T: return None
    return '+'.join(str(c)+''.join(f'*{v}^{e}' if e>1 else f'*{v}' for v,e in sorted(m.items())) for m,c in T)
# 1. substitute variables fixed by linear univariate generators a*v+b
polys=[terms(g) for g in gens]; fixed={}
changed=True
while changed:
    changed=False
    for T in polys:
        vs=set(v for m,_ in T for v in m)
        if len(vs)==1 and all(sum(m.values())<=1 for m,_ in T) and len(T)<=2:
            v=list(vs)[0]; a=[c for m,c in T if m][0]; b=sum(c for m,c in T if not m)%p
            val=(-b*pow(a,p-2,p))%p
            if v not in fixed: fixed[v]=val; changed=True
    if changed:
        new=[]
        for T in polys:
            acc={}
            for m,c in T:
                cc=c; m2={}
                for v,e in m.items():
                    if v in fixed: cc=cc*pow(fixed[v],e,p)%p
                    else: m2[v]=e
                key=tuple(sorted(m2.items())); acc[key]=(acc.get(key,0)+cc)%p
            T2=[(dict(k),c) for k,c in acc.items() if c]
            if T2: new.append(T2)
        polys=new
print('fixed', fixed, 'remaining gens', len(polys), flush=True)
if any(all(not m for m,_ in T) for T in polys): print('VERDICT EMPTY (nonzero constant after substitution)'); sys.exit(0)
# 2. blocks by support
blocks=collections.OrderedDict()
for T in polys:
    s=frozenset(v for m,_ in T for v in m); blocks.setdefault(s,[]).append(tostr(T))
order=sorted(blocks, key=lambda s:(len(s), sorted(s, key=lambda v:(len(v),v))))
cur=set(); prevGB=[]; log=[]
for k,s in enumerate(order):
    cur|=s; vs=[v for v in names if v in cur]
    stage_gens=prevGB+blocks[s]
    fn=f'{outdir}/stage{k}.ms'; open(fn,'w').write(','.join(vs)+'\n'+str(p)+'\n'+',\n'.join(stage_gens)+'\n')
    t=time.time()
    pr=subprocess.run(f'ulimit -v {CAP}; timeout {TMO} {M} -g 2 -t {THR} -f {fn} -o {outdir}/stage{k}.out', shell=True, capture_output=True, text=True)
    W=round(time.time()-t,1); out=open(f'{outdir}/stage{k}.out').read() if os.path.exists(f'{outdir}/stage{k}.out') else ''
    if not out.strip():
        rec=dict(stage=k, nvars=len(vs), ngens=len(stage_gens), new=len(blocks[s]), wall=W, result=f'NO OUTPUT exit={pr.returncode} {pr.stderr[-120:].strip()}'); log.append(rec); print(rec, flush=True); break
    basis=re.search(r'\[(.*)\]:\s*$', out, re.S).group(1)
    bl=[b.strip() for b in basis.split(',\n') if b.strip()]
    if bl==['1']:
        rec=dict(stage=k, nvars=len(vs), ngens=len(stage_gens), new=len(blocks[s]), wall=W, result='EMPTY: [1]'); log.append(rec); print(rec, flush=True); print('VERDICT EMPTY-mod-p at stage', k); break
    # convert msolve terms "1*c_3^2*c_4^1" -> keep as is (valid input syntax)
    prevGB=[re.sub(r'\^1(?![0-9])','',b) for b in bl]
    rec=dict(stage=k, nvars=len(vs), ngens=len(stage_gens), new=len(blocks[s]), wall=W, gb_size=len(prevGB), gb_maxdeg=max(max(sum(m.values()) for m,_ in terms(b)) for b in prevGB)); log.append(rec); print(rec, flush=True)
else:
    print('VERDICT NONUNIT: final GB size', len(prevGB), '-- NOT EMPTY over F_p-bar; needs dimension/solve')
json.dump(log, open(f'{outdir}/cascade.json','w'), indent=1)
