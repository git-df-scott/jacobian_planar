"""night15 -- independent re-verification of every lambda certificate emitted
by mate15, rebuilding the Keller system from the recorded P and checking
lambda^T A = 0 on every column and lambda^T e = 1 in exact rational arithmetic."""
import json, sys
from fractions import Fraction as F
from math import gcd
sys.path.insert(0,'/home/user/jacobian_planar/night15')
sys.path.insert(0,'/home/user/jacobian_planar/night12')
import pk15 as P14, mate15
import matekit as M, exact as EX
H='/home/user/jacobian_planar/night15/'
recs={r['hash']:r for r in json.load(open(H+'screen15_records.json'))}
surv=json.load(open(H+'survivors15.json'))
ok=bad=0; bads=[]
for s in surv:
    r=recs[s['hash']]
    P=P14.clean({tuple(int(t) for t in k.split(',')):F(v[0],v[1]) for k,v in r['P'].items()})
    den=1
    for v in P.values(): den = den*v.denominator//gcd(den, v.denominator)
    Pi={k:int(v*den) for k,v in P.items()}
    assert all(F(v)*1==v for v in Pi.values())
    for st in s['stages']:
        lv=st.get('lambda_vector')
        if not lv: continue
        S=mate15.carrier(st['deg_Q_bound'])
        rows,_=M.build_system(Pi,S)
        lam={(e[0][0],e[0][1]):F(e[1][0],e[1][1]) for e in lv}
        if EX.verify_lambda(lam,rows,len(S)): ok+=1
        else: bad+=1; bads.append((s['hash'],st['deg_Q_bound']))
print('lambda certificates re-verified independently: %d ok, %d bad'%(ok,bad))
print(bads[:10])
