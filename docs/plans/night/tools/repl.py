import sys, hashlib
sys.path.insert(0,'/tmp/wt/fastx'); sys.path.insert(0,'/tmp/wt/canon/campaign/audit_tracks')
import fastx, trackD_chain_map as T
shapes={}
for ch in T.all_chains():
    for c in T.reduced_candidates(ch)[0]:
        tag=f"{ch.name} | a={c['a']} b={c['b']} c'={c['cprime']} r={c['r']} eps={c['epsP']},{c['epsQ']}"
        shapes['s'+hashlib.sha1(tag.encode()).hexdigest()[:6]]=(tag,c)
def kills(sid,p,J):
    tag,c=shapes[sid]; ctx,names,gens,info=fastx.build(c['NP'],c['NQ'],c['r'],p,jextra=J)
    nz=set(info['ndegen'])|{'w'}; out=[]
    for g in gens:
        if len(g.monoms())==1:
            vs={names[i] for i,e in enumerate(g.monoms()[0]) if e}
            if vs and vs<=nz: out.append(str(g))
    return len(gens), out
mode=sys.argv[1]
if mode=='repl':
    for sid,J in [('s4f232a',6),('s20640c',6),('s831b26',4),('s6cc334',2)]:
        for p in (1000003,1000033):
            n,k=kills(sid,p,J); print('REPL',sid,'p',p,'jextra',J,'gens',n,'kills',k[:2], flush=True)
else:
    for sid in ('scb0881','sab7d9e','s3bab7b'):
        for J in (16,20,24):
            n,k=kills(sid,65521,J); print('DEEP',sid,'jextra',J,'gens',n,'kills',k[:2], flush=True)
            if k: break
