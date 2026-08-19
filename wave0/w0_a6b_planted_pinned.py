#!/usr/bin/env python3
"""A6b -- planted control in the ZERO-DIMENSIONAL chart the campaign branches in.

C4 in w0_a6_planted_controls.py plants into the dim-1 edge system; a generic
constant shift there makes the ideal generic and the GB expensive.  This variant
plants into the PINNED chart (d_3_3 normalised), which is the chart every
campaign branch actually lives in and which is zero-dimensional (dim 0,
vdim 1144).  Same data-mutant principle -- ONLY constant terms move, so the
monomial support, degrees and sparsity are identical to the real system -- but
the planted system stays zero-dimensional and finishes.

The plant is verified INSIDE Singular (subst chain -> residual must be 0), so no
external arithmetic can disagree with the engine under test.
"""
import json, os, re, subprocess, sys, random, time
WD="/home/user/jacobian_planar/campaign/audit_tracks"; OUT="/home/user/jacobian_planar/wave0"
EV=["d_3_3","d_4_5","d_5_7","d_6_9","d_7_11","d_8_13","d_9_15"]
FAIL=[]
def check(l,c,s,e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>"+(f"   [{e}]" if e else ""),flush=True)
def sing(script,name,to=5400):
    p=os.path.join(OUT,name); open(p,"w").write(script); t=time.time()
    try: r=subprocess.run(["Singular","-q",p],capture_output=True,text=True,timeout=to)
    except subprocess.TimeoutExpired: return "TIMEOUT",time.time()-t
    if r.returncode in (-9,137,14) or "no more memory" in (r.stderr or ""): return "OOM",time.time()-t
    return r.stdout,time.time()-t
def val(o,k):
    for ln in str(o).splitlines():
        if ln.startswith(k): return int(ln.split()[1])
    return None
tree=json.load(open(os.path.join(WD,"trackA_reduced_system.json")))
leaf=[n for n in tree["nodes"] if n["id"]==1][0]
EI=[i for i,e in enumerate(leaf["equations"]) if set(re.findall(r"[cd]_\d+_\d+",e)) and set(re.findall(r"[cd]_\d+_\d+",e))<=set(EV)]
eqs=[leaf["equations"][i] for i in EI]
print("="*78); print("A6b  PLANTED CONTROL IN THE PINNED (ZERO-DIMENSIONAL) CHART"); print("="*78)
for P in [65521,65539,65599]:
    rnd=random.Random(861+P); alpha={v:rnd.randrange(1,P) for v in EV}
    ch=lambda n:"subst("*len(EV)+n+"".join(f", {v}, {a})" for v,a in alpha.items())
    L=[f"ring R = {P}, ({','.join(EV)}), dp;","short=0;","ideal I;"]
    for k,e in enumerate(eqs):
        L.append(f"poly e{k} = {e};")
        L.append(f"poly s{k} = e{k} - ({ch(f'e{k}')});")
        L.append(f"I[{k+1}] = s{k};")
    # the pin, shifted so that alpha satisfies it too: d_3_3 - alpha(d_3_3)
    L.append(f"I[{len(eqs)+1}] = d_3_3 - {alpha['d_3_3']};")
    L.append("int bad = 0;")
    for k in range(len(eqs)): L.append(f"if ({ch(f's{k}')} != 0) {{ bad = bad + 1; }}")
    L+=['"PLANT_RESIDUALS: "+string(bad);',"ideal G = groebner(I);",
        '"DIM: "+string(dim(G));','if(dim(G)==0){"VDIM: "+string(vdim(G));}',"quit;"]
    o,t=sing("\n".join(L),f"a6b_plant_p{P}.sing")
    check(f"p={P} plant is a genuine zero of the mutated system (engine-verified)",
          val(o,"PLANT_RESIDUALS: ")==0,"CERTIFIED",f"residuals={val(o,'PLANT_RESIDUALS: ')}")
    d=val(o,"DIM: ")
    check(f"p={P} PLANTED data-mutant -> eliminator says NON-EMPTY",
          d is not None and d>=0,"CERTIFIED",
          f"dim={d} vdim={val(o,'VDIM: ')} in {t:.0f}s  (a -1 here would prove the eliminator broken)")
print("="*78)
if FAIL: print("A6b FAILED:",FAIL); sys.exit(1)
print("A6b PASSES -- the EMPTY-emitting path returns NON-EMPTY on a planted")
print("same-support mutant of the real system at all three campaign primes.")
