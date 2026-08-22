import sys, re, random, time
sys.path.insert(0,'/tmp/hunt')
from pentev import conditions, VARS, p

t0=time.time()
lines=[l.rstrip() for l in open('/tmp/w/wave1/pent_L23.ms')]
fvars=[v.strip() for v in lines[0].split(',')]
assert fvars==VARS, ("VAR MISMATCH", fvars[:5], VARS[:5], len(fvars), len(VARS))
body="\n".join(lines[2:]).rstrip().rstrip(',')
polys=[s.strip() for s in body.split(",\n") if s.strip()]
print("parsed",len(polys),"polys in %.1fs"%(time.time()-t0), flush=True)

tok=re.compile(r'([+-]?)\s*([^+-]+)')
def ev(poly, val):
    tot=0
    for sign,term in tok.findall(poly):
        term=term.strip()
        if not term: continue
        c=1; 
        for fac in term.split('*'):
            fac=fac.strip()
            if not fac: continue
            if '^' in fac:
                v,e=fac.split('^'); v=v.strip()
                c=c*pow(val[v], int(e), p)%p if not v.isdigit() else c*pow(int(v),int(e),p)%p
            elif fac.isdigit():
                c=c*int(fac)%p
            else:
                c=c*val[fac]%p
        tot=(tot-c if sign=='-' else tot+c)%p
    return tot

random.seed(int(sys.argv[1]) if len(sys.argv)>1 else 7)
ok=True
for trial in range(2):
    val={v:random.randrange(p) for v in VARS}
    mine=conditions(val)
    t1=time.time()
    theirs=[ev(q,val) for q in polys]
    match=sum(1 for a,b in zip(mine,theirs) if a==b)
    print(f"trial {trial}: {match}/66 match  (export eval {time.time()-t1:.1f}s)", flush=True)
    if match!=66:
        ok=False
        bad=[(k,mine[k],theirs[k]) for k in range(66) if mine[k]!=theirs[k]][:5]
        print("  MISMATCH sample:",bad)
print("CONTROL", "PASS" if ok else "FAIL")
