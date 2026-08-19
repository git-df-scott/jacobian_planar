#!/bin/bash
cd /home/user/jacobian_planar
python3 - <<'PY' > wave0/probe_timing.log 2>&1
import json,re,subprocess,time,os
WD="/home/user/jacobian_planar/campaign/audit_tracks"
EV=["d_3_3","d_4_5","d_5_7","d_6_9","d_7_11","d_8_13","d_9_15"]
tree=json.load(open(os.path.join(WD,"trackA_reduced_system.json")))
leaf=[n for n in tree["nodes"] if n["id"]==1][0]
EI=[i for i,e in enumerate(leaf["equations"]) if set(re.findall(r"[cd]_\d+_\d+",e)) and set(re.findall(r"[cd]_\d+_\d+",e))<=set(EV)]
eqs=[leaf["equations"][i] for i in EI]
P=65521
def run(script,name,to=1800):
    p=os.path.join("/home/user/jacobian_planar/wave0",name); open(p,"w").write(script)
    t=time.time()
    try: r=subprocess.run(["Singular","-q",p],capture_output=True,text=True,timeout=to)
    except subprocess.TimeoutExpired: return "TIMEOUT",time.time()-t
    return r.stdout,time.time()-t
# probe 1: real edge subsystem, dp
L=[f"ring R = {P}, ({','.join(EV)}), dp;","short=0;","ideal I;"]
for k,e in enumerate(eqs): L.append(f"I[{k+1}] = {e};")
L+=["ideal G = groebner(I);",'"DIM: "+string(dim(G));','if(dim(G)==0){"VDIM: "+string(vdim(G));}',"quit;"]
o,t=run("\n".join(L),"probe_real_edge.sing")
print("PROBE real edge dp:",t,"s ->",[l for l in str(o).splitlines() if l.startswith(("DIM","VDIM"))])
# probe 2: real edge + d_3_3-1 pin (the normalized chart the campaign uses)
L2=L[:-4]+[f"I[{len(eqs)+1}] = d_3_3-1;","ideal G = groebner(I);",'"DIM: "+string(dim(G));','if(dim(G)==0){"VDIM: "+string(vdim(G));}',"quit;"]
o,t=run("\n".join(L2),"probe_real_edge_pin.sing")
print("PROBE real edge + d_3_3=1:",t,"s ->",[l for l in str(o).splitlines() if l.startswith(("DIM","VDIM"))])
# probe 3: contradictory (negative control)
L3=L[:-4]+[f"I[{len(eqs)+1}] = d_3_3-1;",f"I[{len(eqs)+2}] = d_3_3;","ideal G = groebner(I);",'"DIM: "+string(dim(G));',"quit;"]
o,t=run("\n".join(L3),"probe_neg.sing")
print("PROBE negative control:",t,"s ->",[l for l in str(o).splitlines() if l.startswith("DIM")])
PY
echo PROBE_DONE >> wave0/probe_timing.log
