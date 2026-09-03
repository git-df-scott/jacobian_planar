#!/bin/bash
# usage: decide_shape.sh <sid> <prime> <jextra>   -> full pipeline: generate, gauge, eliminate, decide END branches
sid=$1; p=$2; J=$3; tag=${sid}_j${J}_p${p}; cd /tmp/wt/charts
python3 - $sid $p $J <<'PY'
import sys, hashlib; sys.path.insert(0,'/tmp/wt/fastx'); sys.path.insert(0,'/tmp/wt/canon/campaign/audit_tracks')
import fastx, trackD_chain_map as T
sid,p,J=sys.argv[1],int(sys.argv[2]),int(sys.argv[3])
for ch in T.all_chains():
    for c in T.reduced_candidates(ch)[0]:
        tag=f"{ch.name} | a={c['a']} b={c['b']} c'={c['cprime']} r={c['r']} eps={c['epsP']},{c['epsQ']}"
        if 's'+hashlib.sha1(tag.encode()).hexdigest()[:6]==sid:
            ctx,names,gens,info=fastx.build(c['NP'],c['NQ'],c['r'],p,jextra=J)
            keep=fastx.write_ms(f'/tmp/wt/fastx/ms/{sid}_j{J}_p{p}.ms',names,gens,p); print('GEN',tag,'vars',len(keep),'gens',len(gens)); raise SystemExit
PY
( ulimit -v 3000000; timeout 1200 python3 torus_charts.py /tmp/wt/fastx/ms/$tag.ms /tmp/wt/charts/$tag $tag > $tag.reduce.out 2>&1 )
f=$(ls /tmp/wt/charts/$tag/*_chart0.ms 2>/dev/null | head -1); [ -s "$f" ] || { echo "$tag | NO CHART FILE" >> decide_shape.log; exit 1; }
nch=$(ls /tmp/wt/charts/$tag/*chart*.ms | wc -l)
S=$(date +%s); MAXBR=600 timeout 3000 python3 -u lincascade3.py $f lin3_$tag > lin3_$tag.log 2>&1
br=$(grep BRANCHES lin3_$tag.log)
timeout 3000 python3 -u decide_ends.py lin3_$tag/results.json dec_$tag > dec_$tag.log 2>&1
ends=$(grep -c "^(" dec_$tag.log); emp=$(grep -c "EMPTY \[1\]" dec_$tag.log); non=$(grep -c "NONUNIT" dec_$tag.log); wall=$(grep -c "WALL" dec_$tag.log)
echo "$tag | charts $nch | $br | END decided: $ends (EMPTY $emp, NONUNIT $non, WALL $wall) | $(( $(date +%s)-S ))s" >> decide_shape.log
