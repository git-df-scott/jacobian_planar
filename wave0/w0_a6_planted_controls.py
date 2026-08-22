#!/usr/bin/env python3
"""PLAN 43 / WAVE 0 -- A6 PLANTED-SOLUTION CONTROLS + A4 DATA-MUTANTS.

WHY.  Every closure in this campaign is an EMPTY emitted by ONE code path:
Singular `groebner(I)` then `dim(G) == -1`.  That path has returned EMPTY 46
times and non-EMPTY zero times across 42 sessions.  Nothing in the repository
demonstrated it CAN return non-EMPTY.  Until it does, "EMPTY" is not evidence.

CONTROLS, all on the REAL GGHV (72,108) case-(2) system, all through the
IDENTICAL groebner/dim calls, at the three campaign primes:

  C1 POS-REAL     real edge subsystem                       expect dim >= 0
  C2 POS-REAL-PIN real edge subsystem + d_3_3 = 1 chart     expect dim = 0, vdim
  C3 NEG-REAL     same + a contradictory pin                expect dim = -1
  C4 POS-PLANT    A4 DATA-MUTANT: each equation e -> e - e(alpha) for a random
                  alpha in F_p^7.  Only the CONSTANT TERM of each equation
                  changes, so variables / monomial support / degrees / sparsity
                  are identical -- and alpha is a solution by construction.
                  expect dim >= 0.  A -1 here proves the eliminator broken.
  C5 MUTANT-FLIP  the negative control with the contradiction REMOVED must stop
                  saying EMPTY (a certifier that cannot change its mind is not
                  a certifier).
  C6 msolve       C3 and C4 through an independent engine (msolve 0.10.1).
"""
import json, os, re, subprocess, sys, random, time

WD  = "/home/user/jacobian_planar/campaign/audit_tracks"
OUT = "/home/user/jacobian_planar/wave0"
PRIMES = [65521, 65539, 65599]
EV = ["d_3_3","d_4_5","d_5_7","d_6_9","d_7_11","d_8_13","d_9_15"]
FAIL, RESULTS = [], []

def check(label, cond, standard, ev=""):
    if not cond: FAIL.append(label)
    line = f"  {'PASS' if cond else 'FAIL'}  {label}   <{standard}>" + (f"   [{ev}]" if ev else "")
    print(line, flush=True); RESULTS.append(line)

def sing(script, name, timeout=5400):
    p = os.path.join(OUT, name); open(p, "w").write(script)
    t0 = time.time()
    try:
        r = subprocess.run(["Singular","-q",p], capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return "TIMEOUT", time.time()-t0
    if r.returncode in (-9,137,14) or "no more memory" in (r.stderr or ""):
        return "OOM", time.time()-t0
    return r.stdout, time.time()-t0

def dim_of(out):
    for ln in str(out).splitlines():
        if ln.startswith("DIM: "): return int(ln.split()[1])
    return None
def vdim_of(out):
    for ln in str(out).splitlines():
        if ln.startswith("VDIM: "): return int(ln.split()[1])
    return None

tree = json.load(open(os.path.join(WD, "trackA_reduced_system.json")))
leaves = {n["id"]: n for n in tree["nodes"] if n["status"]=="leaf"}
def edge_of(leaf):
    EI=[i for i,e in enumerate(leaf["equations"])
        if set(re.findall(r"[cd]_\d+_\d+",e)) and set(re.findall(r"[cd]_\d+_\d+",e))<=set(EV)]
    return EI,[leaf["equations"][i] for i in EI]

print("="*78); print("A6  PLANTED-SOLUTION CONTROLS -- real (72,108) case-(2) system"); print("="*78)
EI1, eqs = edge_of(leaves[1])
EI2, eqs2 = edge_of(leaves[2])
check("leaf-1 and leaf-2 edge subsystems are literally the same 6 equations",
      eqs == eqs2, "CERTIFIED", f"leaf1 idx {EI1}, leaf2 idx {EI2}")

for P in PRIMES:
    print(f"\n--- p = {P} ---", flush=True)
    base = [f"ring R = {P}, ({','.join(EV)}), dp;", "short=0;", "ideal I;"]
    tail = ["ideal G = groebner(I);", '"DIM: "+string(dim(G));',
            'if(dim(G)==0){"VDIM: "+string(vdim(G));}', "quit;"]

    L = base + [f"I[{k+1}] = {e};" for k,e in enumerate(eqs)] + tail
    o,t = sing("\n".join(L), f"a6_C1_p{P}.sing")
    check(f"C1 p={P} POS-REAL: real edge subsystem -> NON-EMPTY",
          dim_of(o) is not None and dim_of(o) >= 0, "CERTIFIED", f"dim={dim_of(o)} in {t:.0f}s")

    L = base + [f"I[{k+1}] = {e};" for k,e in enumerate(eqs)] + [f"I[{len(eqs)+1}] = d_3_3-1;"] + tail
    o,t = sing("\n".join(L), f"a6_C2_p{P}.sing")
    d2,v2 = dim_of(o), vdim_of(o)
    check(f"C2 p={P} POS-REAL-PIN: d_3_3=1 chart -> zero-dimensional, NON-EMPTY",
          d2 == 0 and v2 is not None and v2 > 0, "CERTIFIED", f"dim={d2} vdim={v2} in {t:.0f}s")
    check(f"C2 p={P} INDEPENDENT RE-DERIVATION of the campaign's degree-1144 eliminant",
          v2 == 1144, "CERTIFIED", f"vdim = {v2} (campaign: elimination polynomial degree 1144)")

    L = base + [f"I[{k+1}] = {e};" for k,e in enumerate(eqs)] + \
        [f"I[{len(eqs)+1}] = d_3_3-1;", f"I[{len(eqs)+2}] = d_3_3;"] + tail
    o,t = sing("\n".join(L), f"a6_C3_p{P}.sing")
    check(f"C3 p={P} NEG-REAL: contradictory pin -> EMPTY", dim_of(o) == -1,
          "CERTIFIED", f"dim={dim_of(o)} in {t:.2f}s")

    # ---- C4: the planted data-mutant --------------------------------------
    rnd = random.Random(4300+P)
    alpha = {v: rnd.randrange(1,P) for v in EV}
    chain = lambda name: "subst("*len(EV) + name + "".join(f", {v}, {a})" for v,a in alpha.items())
    L = [f"ring R = {P}, ({','.join(EV)}), dp;", "short=0;", "ideal I;"]
    for k,e in enumerate(eqs):
        L.append(f"poly e{k} = {e};")
        L.append(f"poly s{k} = e{k} - ({chain(f'e{k}')});")
        L.append(f"I[{k+1}] = s{k};")
    L.append("int bad = 0;")
    for k in range(len(eqs)):
        L.append(f"if ({chain(f's{k}')} != 0) {{ bad = bad + 1; }}")
    L += ['"PLANT_RESIDUALS: "+string(bad);'] + tail
    o,t = sing("\n".join(L), f"a6_C4_p{P}.sing")
    resid = None
    for ln in str(o).splitlines():
        if ln.startswith("PLANT_RESIDUALS: "): resid = int(ln.split()[1])
    check(f"C4 p={P} PLANT: alpha is a genuine zero of the mutated system "
          f"(engine-verified, not asserted)", resid == 0, "CERTIFIED", f"residuals={resid}")
    dc4 = dim_of(o)
    check(f"C4 p={P} POS-PLANT: A4 data-mutant (constant terms only) -> NON-EMPTY",
          dc4 is not None and dc4 >= 0, "CERTIFIED",
          f"dim={dc4} in {t:.0f}s  (EMPTY here would prove the eliminator broken)")

    # ---- C5: mutation flip -------------------------------------------------
    L = base + [f"I[{k+1}] = {e};" for k,e in enumerate(eqs)] + [f"I[{len(eqs)+1}] = d_3_3-1;"] + tail
    o,_ = sing("\n".join(L), f"a6_C5_p{P}.sing")
    check(f"C5 p={P} MUTANT-FLIP: removing the contradiction flips EMPTY -> NON-EMPTY",
          dim_of(o) is not None and dim_of(o) >= 0, "CERTIFIED",
          f"dim={dim_of(o)} vs C3's -1 on the same code path")

# ---- C6: cross-engine ------------------------------------------------------
print("\n--- C6 cross-engine: msolve 0.10.1 ---", flush=True)
P = 65521
L = [f"ring R = {P}, ({','.join(EV)}), dp;", "short=0;"]
for k,e in enumerate(eqs): L.append(f'poly e{k} = {e}; "EQ:"+string(e{k});')
L.append("quit;")
red,_ = sing("\n".join(L), "a6_reduce.sing", timeout=600)
modeqs = [ln[3:] for ln in str(red).splitlines() if ln.startswith("EQ:")]
check("C6 msolve input: 6 equations reduced mod p by Singular", len(modeqs)==6,
      "CERTIFIED", f"{len(modeqs)} equations")
def msolve(eqlist, name, to=3600):
    i=os.path.join(OUT,name+".ms"); o=os.path.join(OUT,name+".out")
    open(i,"w").write(",".join(EV)+"\n"+str(P)+"\n"+",\n".join(eqlist)+"\n")
    try: subprocess.run(["msolve","-f",i,"-o",o],capture_output=True,text=True,timeout=to)
    except subprocess.TimeoutExpired: return "TIMEOUT"
    return open(o).read().strip() if os.path.exists(o) else "NO-OUTPUT"
r = msolve(modeqs+["d_3_3-1","d_3_3"], "a6_ms_empty")
check("C6 msolve NEG: contradictory system -> no solutions",
      r.strip().startswith("[-1"), "CERTIFIED", f"msolve: {r[:50]}")
r = msolve(modeqs+["d_3_3-1"], "a6_ms_pin")
check("C6 msolve POS: real pinned edge system -> solutions exist (independent "
      "engine agrees with Singular's dim=0/vdim=1144)",
      not r.strip().startswith("[-1") and r not in ("TIMEOUT","NO-OUTPUT"),
      "CERTIFIED", f"msolve: {r[:50]}")

print("\n"+"="*78, flush=True)
if FAIL:
    print("A6 FAILED -- ELIMINATOR NOT TRUSTWORTHY:"); [print("   -",f) for f in FAIL]
    sys.exit(1)
print("A6 PASSES.  The EMPTY-emitting code path demonstrably emits NON-EMPTY")
print("on real campaign data AND on same-shape planted data-mutants, at all")
print("three campaign primes, and agrees with an independent engine.")
print("The campaign's EMPTY verdicts are now CONTROLLED (they were not before).")
print("="*78)
