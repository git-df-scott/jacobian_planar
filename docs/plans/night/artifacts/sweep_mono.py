"""Monomial-certificate sweep over the compiler's whole shape library (all chains, all reduced candidates)."""
import sys, hashlib, json, time, subprocess, os
sys.path.insert(0,'/tmp/wt/canon/campaign/audit_tracks'); sys.path.insert(0,'/tmp/wt/fastx')
import trackD_chain_map as T
from trackB1_polygon import hull_rows
MAXPAR=int(os.environ.get('MAXPAR','70'))
shapes=[]
for ch in T.all_chains():
    cands,notes=T.reduced_candidates(ch)
    for c in cands:
        tag=f"{ch.name} | a={c['a']} b={c['b']} c'={c['cprime']} r={c['r']} eps={c['epsP']},{c['epsQ']}"
        RP,RQ=hull_rows(c['NP']),hull_rows(c['NQ'])
        if RP.get(0)==(0,1) and RQ.get(0)==(0,0): DR=RP
        elif RQ.get(0)==(0,1) and RP.get(0)==(0,0): DR=RQ
        else: DR=None
        npar=sum(hi-lo+1 for lo,hi in DR.values()) if DR else None
        shapes.append(dict(sid='s'+hashlib.sha1(tag.encode()).hexdigest()[:6], tag=tag, degrees=ch.degrees(), maxdeg=ch.maxdeg, NP=c['NP'], NQ=c['NQ'], r=c['r'], npar=npar, notes=c['notes']))
print(len(shapes),'shapes in the library', flush=True)
json.dump(shapes, open('/tmp/wt/fastx/library.json','w'), indent=1)
WORKER='''
import sys, json; sys.path.insert(0,'/tmp/wt/fastx'); import fastx
sh=json.load(open(sys.argv[1])); J=int(sys.argv[2]); p=65521
ctx,names,gens,info=fastx.build([tuple(v) for v in sh['NP']],[tuple(v) for v in sh['NQ']],sh['r'],p,jextra=J)
nz=set(info['ndegen'])|{'w'}; kills=[]
for g in gens:
    if len(g.monoms())==1:
        vs={names[i] for i,e in enumerate(g.monoms()[0]) if e}
        if vs and vs<=nz: kills.append(str(g))
print(json.dumps(dict(ngens=len(gens), kills=kills[:3], jmax=info['jmax'])))
'''
open('/tmp/wt/fastx/sweep_worker.py','w').write(WORKER)
out=[]
for sh in sorted(shapes, key=lambda s:(s['npar'] is None, s['npar'] or 0)):
    rec=dict(sh); rec['result']=None
    if sh['npar'] is None: rec['result']='OUT OF SCOPE'; out.append(rec); print(rec['sid'], rec['tag'][:50], 'OUT OF SCOPE', flush=True); continue
    if sh['npar']>MAXPAR: rec['result']=f'SKIPPED (npar {sh["npar"]} > {MAXPAR})'; out.append(rec); print(rec['sid'], rec['tag'][:50], rec['result'], flush=True); continue
    for J in (2,4,6,8,10,12):
        t=time.time()
        json.dump(sh, open('/tmp/wt/fastx/_sweep_arg.json','w'))
        pr=subprocess.run(f"ulimit -v 3000000; timeout 600 python3 /tmp/wt/fastx/sweep_worker.py /tmp/wt/fastx/_sweep_arg.json {J}", shell=True, capture_output=True, text=True)
        if pr.returncode!=0 or not pr.stdout.strip():
            rec['result']=f'UNBUILDABLE at jextra {J} (exit {pr.returncode})'; break
        r=json.loads(pr.stdout); rec.setdefault('depths',{})[J]=dict(ngens=r['ngens'], jmax=r['jmax'], kills=r['kills'], secs=round(time.time()-t,1))
        if r['kills']: rec['result']=f'KILLED at jextra {J} by {r["kills"][0]}'; break
    if rec['result'] is None: rec['result']='SURVIVES to jextra 12 (no monomial certificate)'
    out.append(rec); print(rec['sid'], rec['degrees'], rec['tag'][:60], '|', rec['result'], flush=True)
    json.dump(out, open('/tmp/wt/fastx/sweep_mono.json','w'), indent=1)
print('SWEEP_DONE')
