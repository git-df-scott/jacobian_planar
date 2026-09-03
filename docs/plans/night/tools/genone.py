import sys, re, json, hashlib, time
sys.path.insert(0,'/tmp/wt/canon/campaign/audit_tracks'); sys.path.insert(0,'/tmp/wt/handoff/docs/plans/groundcover/artifacts'); sys.path.insert(0,'/tmp/wt/fastx')
import trackD_chain_map as T, fastx, register_build as rb
sid_want, p = sys.argv[1], int(sys.argv[2])
for ch in T.all_chains():
    for c in T.reduced_candidates(ch)[0]:
        tag = f"{ch.name} | a={c['a']} b={c['b']} c'={c['cprime']} r={c['r']} eps={c['epsP']},{c['epsQ']}"
        sid = 's' + hashlib.sha1(tag.encode()).hexdigest()[:6]
        if sid != sid_want: continue
        t=time.time(); ctx, names, gens, info = fastx.build(c['NP'], c['NQ'], c['r'], p)
        path = f'/tmp/wt/fastx/ms/{sid}_p{p}.ms'; keep = fastx.write_ms(path, names, gens, p)
        txt=open(path).read().split('\n'); gl=[g for g in re.split(r',\s*\n', '\n'.join(txt[2:])) if g.strip()]
        gm=[rb.parse_poly(g,p) for g in gl]; vi={v:i for i,v in enumerate(keep)}; tr=rb.torus_rank(gm, vi)
        rec=dict(sid=sid, tag=tag, p=p, path=path, NP=c['NP'], NQ=c['NQ'], r=c['r'], nvars=len(keep), ngens=len(gens), excess=len(gens)-len(keep),
                 torus_rank=tr[0], secs=round(time.time()-t,1), sha=hashlib.sha256(open(path,'rb').read()).hexdigest()[:12], ndegen=info['ndegen'], jmax=info['jmax'])
        print(json.dumps(rec)); sys.exit(0)
print(json.dumps(dict(sid=sid_want, error='not found')))
