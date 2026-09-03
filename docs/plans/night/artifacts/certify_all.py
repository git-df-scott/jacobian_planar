"""Exact-Q certification of every monomial kill recorded by the sweep."""
import json, sys, re, time
sys.path.insert(0,'/tmp/wt/fastx'); from fastx_q import build_q
from fractions import Fraction
S=json.load(open('/tmp/wt/fastx/sweep_mono.json')); out=[]
done=set()
try:
    for r in json.load(open('/tmp/wt/fastx/certified.json')): done.add(r['sid']); out.append(r)
except Exception: pass
for r in S:
    if not r['result'].startswith('KILLED') or r['sid'] in done: continue
    J=int(re.search(r'jextra (\d+)', r['result']).group(1)); t=time.time()
    try:
        ctx,names,conds,info=build_q([tuple(v) for v in r['NP']],[tuple(v) for v in r['NQ']],r['r'],jextra=J)
    except MemoryError:
        out.append(dict(sid=r['sid'], tag=r['tag'], degrees=r['degrees'], jextra=J, exactQ='MEMORY')); continue
    nz=set(info['ndegen'])|{'w'}; certs=[]
    for (j,e,g) in conds:
        if len(g.monoms())==1:
            vs={names[i] for i,ee in enumerate(g.monoms()[0]) if ee}
            if vs and vs<=nz: certs.append(dict(row=int(j), xexp=int(e), gen=str(g)))
    out.append(dict(sid=r['sid'], tag=r['tag'], degrees=r['degrees'], maxdeg=r['maxdeg'], jextra=J, jmax=info['jmax'], exactQ=('CERTIFIED' if certs else 'NO EXACT MONOMIAL (mod-p artefact?)'), certs=certs[:3], secs=round(time.time()-t,1), notes=r.get('notes')))
    print(r['sid'], r['degrees'], r['tag'][:50], '|', out[-1]['exactQ'], certs[:1], flush=True)
json.dump(out, open('/tmp/wt/fastx/certified.json','w'), indent=1)
