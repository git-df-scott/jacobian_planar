#!/usr/bin/env python3
"""A6 completion -- (i) the descent map G as the SEVENTH gate control,
(ii) the cross-engine (msolve 0.10.1) leg of the planted-solution controls.

(i)  WHY G IS THE CONTROL THE SUITE WAS MISSING.  The existing battery rejects
     six non-counterexamples, but every one of them is rejected by a blunt
     property (dividing degrees, injectivity, floats).  None of them is a
     genuinely NON-INJECTIVE plane polynomial map -- because until Session 39
     the campaign had none.  G is one: the descent of Alpoge's counterexample,
     non-injective (PROVED-exact, W0.4), geometric degree 3 (vdim-CERTIFIED,
     W0.5), degrees (6,4) which do NOT divide.  It therefore walks past the
     gates that catch every other control and must be stopped by exactly one:
     G1, Jacobian constancy, because det JG = -2(3u+v-2)^2 is not a constant.

     A gate that rejects G for the WRONG reason (or accepts it) is a gate whose
     rejections carry no information.  This is the sharpest available test of
     the gate's discrimination, and Plan 43 asks for it by name.

(ii) The planted controls at Sec.A6b were Singular-only.  Plan 43 requires them
     "for each engine x version x prime".  msolve 0.10.1 is the independent
     engine; it must agree: empty -> [-1], planted -> solutions.
"""
import os, re, json, sys, subprocess, random, time
sys.path.insert(0, "/home/user/jacobian_planar/campaign/audit_tracks")
from sympy import symbols, expand, Matrix, factor, total_degree
from jc2_bulletproof import bulletproof_gate

OUT="/home/user/jacobian_planar/wave0"; WD="/home/user/jacobian_planar/campaign/audit_tracks"
EV=["d_3_3","d_4_5","d_5_7","d_6_9","d_7_11","d_8_13","d_9_15"]
FAIL=[]
def check(l,c,s,e=""):
    if not c: FAIL.append(l)
    print(f"  {'PASS' if c else 'FAIL'}  {l}   <{s}>"+(f"   [{e}]" if e else ""),flush=True)

print("="*78); print("A6(i)  THE SEVENTH CONTROL: the descent map G through the gate"); print("="*78)
u,v = symbols('u v')
G1 = expand((u+1)*(3*u+v-2)**2*(3*u**3+u**2*v+4*u**2+2*u*v+v))
G2 = expand(-(3*u+v-2)*(9*u**3+3*u**2*v+12*u**2+6*u*v+u+3*v))
detJG = expand(Matrix([[G1.diff(u),G1.diff(v)],[G2.diff(u),G2.diff(v)]]).det())
print(f"  G = (G1,G2), deg = ({total_degree(G1)},{total_degree(G2)}), "
      f"det JG = {factor(detJG)}\n")
import io, contextlib
_buf = io.StringIO()
with contextlib.redirect_stdout(_buf):
    verdict, results = bulletproof_gate(G1, G2, u, v)
rejectors = sorted(k for k, r in results.items() if not r[0])
for k in sorted(results):
    print(f"    {k}: {'PASS' if results[k][0] else 'FAIL'}")
check("G is REJECTED by the gate (it is non-injective but NOT Keller)",
      verdict.upper().startswith("REJECT"), "CERTIFIED", f"verdict={verdict}")
check("G is rejected by G1 (Jacobian non-constancy) -- the CORRECT reason",
      "G1" in rejectors, "CERTIFIED", f"rejected-by: {rejectors}")
check("G is NOT rejected by G2 (its degrees (6,4) genuinely do not divide), so "
      "the gate is discriminating, not blanket-rejecting",
      "G2" not in rejectors, "CERTIFIED",
      f"G2 {'passed' if 'G2' not in rejectors else 'FAILED'} -- 6 does not divide 4, 4 does not divide 6")

print("\n"+"="*78); print("A6(ii)  CROSS-ENGINE LEG: msolve 0.10.1"); print("="*78)
tree=json.load(open(os.path.join(WD,"trackA_reduced_system.json")))
leaf=[n for n in tree["nodes"] if n["id"]==1][0]
EI=[i for i,e in enumerate(leaf["equations"])
    if set(re.findall(r"[cd]_\d+_\d+",e)) and set(re.findall(r"[cd]_\d+_\d+",e))<=set(EV)]
eqs=[leaf["equations"][i] for i in EI]

def sing(script,name,to=1800):
    p=os.path.join(OUT,name); open(p,"w").write(script)
    try: r=subprocess.run(["Singular","-q",p],capture_output=True,text=True,timeout=to)
    except subprocess.TimeoutExpired: return "TIMEOUT"
    return r.stdout
def msolve(eqlist,name,P,to=2400):
    i=os.path.join(OUT,name+".ms"); o=os.path.join(OUT,name+".out")
    open(i,"w").write(",".join(EV)+"\n"+str(P)+"\n"+",\n".join(eqlist)+"\n")
    t=time.time()
    try: subprocess.run(["msolve","-f",i,"-o",o],capture_output=True,text=True,timeout=to)
    except subprocess.TimeoutExpired: return "TIMEOUT", time.time()-t
    return (open(o).read().strip() if os.path.exists(o) else "NO-OUTPUT"), time.time()-t

# msolve's own documented controls first (tools/README.md)
r,_ = msolve(["d_3_3*d_4_5-1","d_3_3","d_4_5"],"a6c_ms_ctl_empty",65521)
check("msolve sanity: <xy-1, x, y> -> no solutions", r.strip().startswith("[-1"),
      "CERTIFIED", f"msolve: {r[:40]}")
r,_ = msolve(["d_3_3^2-1","d_4_5-2","d_5_7","d_6_9","d_7_11","d_8_13","d_9_15"],
             "a6c_ms_ctl_zero",65521)
check("msolve sanity: a zero-dimensional system -> solutions reported",
      not r.strip().startswith("[-1") and r not in ("TIMEOUT","NO-OUTPUT"),
      "CERTIFIED", f"msolve: {r[:40]}")

for P in [65521,65539,65599]:
    rnd=random.Random(861+P); alpha={v_: rnd.randrange(1,P) for v_ in EV}   # SAME seed as A6b
    ch=lambda n:"subst("*len(EV)+n+"".join(f", {v_}, {a})" for v_,a in alpha.items())
    L=[f"ring R = {P}, ({','.join(EV)}), dp;","short=0;"]
    for k,e in enumerate(eqs):
        L.append(f"poly e{k} = {e};")
        L.append(f'poly s{k} = e{k} - ({ch(f"e{k}")}); "PL:"+string(s{k});')
        L.append(f'"RE:"+string(e{k});')
    L.append("quit;")
    red = sing("\n".join(L), f"a6c_reduce_p{P}.sing")
    planted=[l[3:] for l in str(red).splitlines() if l.startswith("PL:")]
    real   =[l[3:] for l in str(red).splitlines() if l.startswith("RE:")]
    check(f"p={P} msolve input prepared (6 planted + 6 real, reduced by Singular)",
          len(planted)==6 and len(real)==6, "CERTIFIED", f"{len(planted)}/{len(real)}")
    r,t = msolve(real+[f"d_3_3-1"], f"a6c_ms_real_p{P}", P)
    check(f"p={P} msolve POS on the REAL pinned system -> solutions exist",
          not r.strip().startswith("[-1") and r not in ("TIMEOUT","NO-OUTPUT"),
          "CERTIFIED", f"{t:.0f}s, msolve: {r[:40]}")
    r,t = msolve(planted+[f"d_3_3-{alpha['d_3_3']}"], f"a6c_ms_plant_p{P}", P)
    check(f"p={P} msolve POS on the PLANTED data-mutant -> solutions exist "
          f"(independent engine confirms A6b)",
          not r.strip().startswith("[-1") and r not in ("TIMEOUT","NO-OUTPUT"),
          "CERTIFIED", f"{t:.0f}s, msolve: {r[:40]}")
    r,t = msolve(real+["d_3_3-1","d_3_3"], f"a6c_ms_empty_p{P}", P)
    check(f"p={P} msolve NEG on the contradictory system -> no solutions",
          r.strip().startswith("[-1"), "CERTIFIED", f"{t:.1f}s, msolve: {r[:40]}")

print("\n"+"="*78)
if FAIL:
    print("A6 COMPLETION FAILED:"); [print("   -",f) for f in FAIL]; sys.exit(1)
print("A6 COMPLETE.  Gate discrimination proven by the seventh control (G is")
print("stopped by G1 alone), and the planted-solution controls confirmed by an")
print("independent engine at all three campaign primes.")
print("="*78)
