import json, os, random, sys, time
import numpy as np
import subprocess
HERE=os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0,HERE)
from w5_pent_hitdetector_v3 import *
import w5_pent_hitdetector_v3 as V
from pent_slice import slice_search

PRIMES=[1000003,1000033,1000039]      # all == 1 (mod 3)
NSTART=int(sys.argv[1]) if len(sys.argv)>1 else 40
print("="*78); print("ITEM 2 -- PENTAGON HIT DETECTOR v3 (all three gauges fixed)"); print("="*78)
print(f"  parameters: {V.NP} total, {len(V.free_indices('one'))} essential after "
      f"3 gauges (p_00 translation, p_10 scale, p_1_0 coordinate scale)")
print(f"  objective: ABSOLUTE max |forbidden coefficient| over levels 13..23 "
      f"({66} conditions)")
print(f"  acceptance: |forbidden| < {TOL}, allowed scale in [{1/BAND:.0e},{BAND:.0e}], "
      f"|x| <= {XCAP:.0e}")
print()
print("  CONTROLS")
rng=np.random.default_rng(20260820)

# POS-1 : planted float target
x0=rng.normal(size=58)+1j*rng.normal(size=58)
tgt,_=V.Fvec(x0,'one')
r,xf=V.newton(x0+1e-3*(rng.normal(size=58)+1j*rng.normal(size=58)),'one',target=tgt)
V.check("POS-1 float: Newton recovers a planted root of F(x) = F(x0)",
        r<V.TOL, f"final max |F - F(x0)| = {r:.3e}")

# NEG-1 : the v1 artefact must be rejected
xbig=x0*1e6
fbig,Qbig=V.Fvec(xbig,'one')
okbig,why=V.accept(xbig,Qbig,fbig)
V.check("NEG-1 the acceptance test REJECTS a blown-up point (the v1 artefact)",
        not okbig, why)

# NEG-2 : forbidden not small must be rejected
f2,Q2=V.Fvec(x0,'one')
ok2,why2=V.accept(x0,Q2,f2)
V.check("NEG-2 the acceptance test REJECTS a random point", not ok2, why2)

# POS-2 : the test must ACCEPT the planted root (against its own target)
fA,QA=V.Fvec(xf,'one',target=tgt)
a=V.allowed_scale(QA); fmax=float(np.max(np.abs(fA))); xmax=float(np.max(np.abs(xf)))
V.check("POS-2 the same test ACCEPTS the planted root (so it is not vacuous)",
        fmax<V.TOL and 1/V.BAND<=a<=V.BAND and xmax<=V.XCAP,
        f"forbidden {fmax:.3e}, allowed {a:.3e}, |x| {xmax:.3e}")

# POS-3 / NEG-3 : the EXACT mod-p leg.
# Newton is NOT a search method over a finite field -- there is no metric, so
# "start near a root" is meaningless and a descent has nothing to descend.  The
# exact leg is therefore a RANDOM LINEAR SLICE search: fix r of the 58 essential
# parameters to random values in F_p and hand the sliced system to msolve.  A
# non-empty slice is a genuine mod-p point OF THE FULL SYSTEM (slicing only
# removes solutions, never adds them), so this leg can produce a hit; an empty
# slice says nothing, and is not reported as evidence of anything.
p0 = PRIMES[0]
rnd = random.Random(7)
xs = [rnd.randrange(0, p0) for _ in range(58)]
fs, _ = V.dual_F(xs, 'one', p0)
fs2, _ = V.fp_F(xs, 'one', p0)
V.check("POS-3 the exact mod-p evaluator agrees with the dual-number evaluator "
        "on the same random point (two independent code paths)",
        [a for a, _ in fs] == [v % p0 for v in fs2],
        f"{len(fs)} coefficients compared")
V.check("NEG-3 mod-p: a random point is NOT an exact root",
        any(a % p0 for a, _ in fs), "as expected")
_d0 = V.dual_F(xs, 'one', p0, dcol=0)[0]
V.check("NEG-3b the exact (dual-number) Jacobian column is not identically zero, "
        "so the derivative machinery is not vacuous",
        any(b % p0 for _, b in _d0),
        f"{sum(1 for _, b in _d0 if b % p0)} of {len(_d0)} entries nonzero")

import pent_slice as PS
for n_, ok_, note_ in PS.controls():
    V.check(n_, ok_, note_)

print()
print("  SEARCH")
out={"controls":[[a,b,c] for a,b,c in V.RESULTS],"float":[],"modp":[]}
t0=time.time()
for chart in ("one","zero"):
    hits=[]
    for s in range(NSTART):
        x0=rng.normal(size=58)+1j*rng.normal(size=58)
        r,x=V.newton(x0,chart)
        f,Q=V.Fvec(x,chart)
        ok,why=V.accept(x,Q,f)
        out["float"].append({"chart":chart,"start":s,"best_abs_forbidden":float(r),
                             "accepted":bool(ok),"why":why})
        if ok:
            hits.append((chart,s,[complex(z) for z in x]))
            print(f"    *** chart {chart} start {s}: ACCEPTED -- {why}", flush=True)
    print(f"    chart {chart}: {NSTART} float starts, {len(hits)} accepted, "
          f"best |forbidden| = "
          f"{min(d['best_abs_forbidden'] for d in out['float'] if d['chart']==chart):.3e}"
          f"   ({time.time()-t0:.0f}s)", flush=True)
    for p in PRIMES:
        assert p % 3 == 1
        for r in (50, 45, 40):
            res = slice_search(chart, p, r, nslices=NSTART, rng=rnd)
            out["modp"].append(res)
            print(f"    chart {chart} p={p} slice r={r}: {res['nslices']} slices, "
                  f"{res['nonempty']} non-empty, {res['empty']} empty, "
                  f"{res['other']} other", flush=True)
            for h in res["hits"]:
                print(f"    *** chart {chart} p={p} r={r}: NON-EMPTY SLICE -- "
                      f"CANDIDATE-UNVERIFIED, witness in {h['ms']}", flush=True)
json.dump(out,open(os.path.join(HERE,'pent_v3_results.json'),'w'),indent=1)
npass=sum(1 for _,o,_ in V.RESULTS if o)
print("\n"+"="*78)
print(f"    {npass}/{len(V.RESULTS)} controls passed")
print("="*78)
