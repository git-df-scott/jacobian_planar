"""Independent reference: the campaign's own y-adic Singular pipeline on the
validation target, at the two primes it used and (new) in characteristic 0."""
import json, os, sys
import trackD_extract as EX
T=json.load(open("trackD_targets_validate.json"))[0]
NP=[tuple(p) for p in T["NP"]]; NQ=[tuple(p) for p in T["NQ"]]
print(T["tag"], flush=True)
import export_char0 as EC
src,info = EX.build_singular(NP,NQ,T["r"],name="valref")
open("_scratch_wg/valref_p.sing","w").write(src)
open("_scratch_wg/valref_0.sing","w").write(EC.to_char0(src))
import subprocess, time
for tag in ("p","0"):
    t0=time.time()
    pr=subprocess.run(["Singular","-q",f"_scratch_wg/valref_{tag}.sing"],
                      capture_output=True,text=True,timeout=1800)
    print(f"  [{'mod 65521' if tag=='p' else 'char 0'}] {time.time()-t0:.0f}s")
    for l in pr.stdout.strip().splitlines(): print("    "+l)
