
import sys, json; sys.path.insert(0,'/tmp/wt/fastx'); import fastx
sh=json.load(open(sys.argv[1])); J=int(sys.argv[2]); p=65521
ctx,names,gens,info=fastx.build([tuple(v) for v in sh['NP']],[tuple(v) for v in sh['NQ']],sh['r'],p,jextra=J)
nz=set(info['ndegen'])|{'w'}; kills=[]
for g in gens:
    if len(g.monoms())==1:
        vs={names[i] for i,e in enumerate(g.monoms()[0]) if e}
        if vs and vs<=nz: kills.append(str(g))
print(json.dumps(dict(ngens=len(gens), kills=kills[:3], jmax=info['jmax'])))
