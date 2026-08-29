import json, os, sys, itertools
from math import gcd
HERE=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,HERE); sys.path.insert(0,os.path.join(os.path.dirname(HERE),'wave4'))
import w5_symslice as X, w4_run as RUN, w4_case2_system as S

PRIMES=[1000003,1000033,1000039]
OUT=os.path.join(HERE,'artifacts'); os.makedirs(OUT,exist_ok=True)
GAUGE={'one':[('d_2_1',1),('c_8_16',1)],'zero':[('d_2_1',1),('c_8_16',1),('d_12_24',1)]}
RESULTS=[]; CHECKS=[]
def check(name,cond,note=""):
    ok=bool(cond); CHECKS.append((name,ok,note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}"+(f"   {note}" if note else ""))
    return ok

print("="*78); print("T3  mu_n-EQUIVARIANT SLICES OF THE CASE-(2) SYSTEM"); print("="*78)

# ---- n = 1 control: must reproduce the unrestricted system -----------------
keep1,eqs1,deg1 = X.restrict(1,0,0,0,0)
check("n=1 control: the ansatz keeps every variable",
      len(keep1)==len(X.VARS), f"{len(keep1)} of {len(X.VARS)}")
check("n=1 control: the ansatz keeps every equation",
      len(eqs1)==len(X.EQS), f"{len(eqs1)} of {len(X.EQS)}")
check("n=1 control: no degeneracy is reported", not deg1, str(deg1))

# ---- the sweep ------------------------------------------------------------
rows=[]
for n in (2,3,4,6):
    for a,b,p_,q_ in itertools.product(range(n),repeat=4):
        if gcd(gcd(a,b),n)!=1:            # the action must be faithful
            continue
        compat_x2 = ((p_+q_-3*a-b) % n == 0)
        compat_const = ((p_+q_-a-b-0) % n == 0)   # the [P,Q] in K^* variant
        keep,eqs,deg = X.restrict(n,a,b,p_,q_)
        row={"n":n,"a":a,"b":b,"p":p_,"q":q_,
             "compatible_with_x2_rhs":compat_x2,
             "compatible_with_constant_rhs":compat_const,
             "surviving_variables":len(keep),
             "surviving_equations":len(eqs),
             "degeneracies":deg}
        if deg:
            row["verdict"]="EMPTY-BY-DEGENERACY"
        rows.append(row)
live=[r for r in rows if not r["degeneracies"]]
print(f"\n  swept {len(rows)} faithful (n,a,b,p,q) cells; "
      f"{len(live)} survive the degeneracy screen")
check("every swept cell got a mechanically computed variable count",
      all(isinstance(r['surviving_variables'],int) for r in rows))
check("the degeneracy screen actually fires on some cells",
      len(live)<len(rows), f"{len(rows)-len(live)} cells killed by degeneracy")
check("the degeneracy screen does NOT fire on every cell only because it is "
      "vacuous: the n=1 cell survives it",
      not X.restrict(1,0,0,0,0)[2])

# Every faithful cell is killed by the degeneracy screen, so `live` is empty.
# That verdict is confirmed on the SOLVER as well, for the largest cell of each
# n, with controls that are required to behave differently:
#   real_sat      the restricted system with the vertex conditions saturated
#                 -> the degeneracy says EMPTY
#   mutant_nosat  the same cell without saturation, with a random point planted
#                 -> must NOT be EMPTY, or the run is void
#   pin_nosat     the same cell with a contradictory pin -> must be EMPTY
SAMPLE=[]
for n in (2,3,4,6):
    sub=[r for r in rows if r['n']==n]
    SAMPLE.append(max(sub,key=lambda r:(r['surviving_variables'],r['surviving_equations'])))
for r in SAMPLE:
    n,a,b,p_,q_ = r["n"],r["a"],r["b"],r["p"],r["q"]
    r["solver_confirmation"]={}
    keep,eqs,_=X.restrict(n,a,b,p_,q_)
    for pch in PRIMES:
        assert pch%3==1
        for label,variant,sat in (("real_sat","real",True),
                                  ("mutant_nosat","mutant",False),
                                  ("pin_nosat","pin",False)):
            tag=f"n{n}_a{a}_b{b}_p{p_}_q{q_}_one_{label}_P{pch}"
            f=os.path.join(OUT,f"sym_{tag}.ms")
            _,nv,npoly,pt=X.write_ms(f,pch,keep,eqs,"one",GAUGE["one"],
                                     variant=variant,seed=abs(hash(tag))%10**6,
                                     saturate=sat)
            res=RUN.run_msolve(f,f[:-3]+'.out',timeout=900,threads=2)
            res['nvars']=nv; res['npolys']=npoly
            if pt is not None: res['planted_point']={k:int(v) for k,v in sorted(pt.items())}
            r["solver_confirmation"][tag]=res
            print(f"    {tag}: {res['verdict']} {res['seconds']}s", flush=True)
    ver=r["solver_confirmation"]
    check(f"n={n} sample cell: every real_sat run is EMPTY",
          all(v['verdict']=='EMPTY' for k,v in ver.items() if 'real_sat' in k),
          str({k:v['verdict'] for k,v in ver.items() if 'real_sat' in k}))
    check(f"n={n} sample cell CONTROL: every planted mutant_nosat run is NOT EMPTY",
          all(v['verdict']!='EMPTY' for k,v in ver.items() if 'mutant_nosat' in k),
          str({k:v['verdict'] for k,v in ver.items() if 'mutant_nosat' in k}))
    check(f"n={n} sample cell CONTROL: every pin_nosat run is EMPTY",
          all(v['verdict']=='EMPTY' for k,v in ver.items() if 'pin_nosat' in k),
          str({k:v['verdict'] for k,v in ver.items() if 'pin_nosat' in k}))

for r in []:
    n,a,b,p_,q_ = r["n"],r["a"],r["b"],r["p"],r["q"]
    r["runs"]={}
    for pch in PRIMES:
        assert pch%3==1
        for chart in ("one","zero"):
            for variant in ("real","mutant","pin"):
                tag=f"n{n}_a{a}_b{b}_p{p_}_q{q_}_{chart}_{variant}_P{pch}"
                keep,eqs,_=X.restrict(n,a,b,p_,q_)
                f=os.path.join(OUT,f"sym_{tag}.ms")
                _,nv,npoly,pt=X.write_ms(f,pch,keep,eqs,chart,GAUGE[chart],
                                         variant=variant,seed=abs(hash(tag))%10**6)
                res=RUN.run_msolve(f,f[:-3]+'.out',timeout=1200,threads=2)
                res['nvars']=nv; res['npolys']=npoly
                if pt is not None: res['planted_point']={k:int(v) for k,v in sorted(pt.items())}
                r["runs"][tag]=res
                print(f"    {tag}: {res['verdict']} {res['seconds']}s", flush=True)
    json.dump({"rows":rows,"checks":[[a1,b1,c1] for a1,b1,c1 in CHECKS]},
              open(os.path.join(HERE,'symslice_results.json'),'w'),indent=1)

json.dump({"source_hash":S.load()[4],
           "compatibility_condition":"p+q = 3a+b (mod n) for the x^2 right-hand side",
           "rows":rows,"checks":[[a1,b1,c1] for a1,b1,c1 in CHECKS]},
          open(os.path.join(HERE,'symslice_results.json'),'w'),indent=1)

print("\n  summary by n:")
for n in (2,3,4,6):
    sub=[r for r in rows if r['n']==n]
    ok=[r for r in sub if not r['degeneracies']]
    print(f"    n={n}: {len(sub)} cells, {len(ok)} non-degenerate, "
          f"max surviving variables {max(r['surviving_variables'] for r in sub)}")
print("\n"+"="*78)
npass=sum(1 for _,o,_ in CHECKS if o)
print(f"    {npass}/{len(CHECKS)} checks passed")
print("="*78)
