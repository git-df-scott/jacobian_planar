#!/bin/bash
# Restart-resilient prime sweep for the bottom-edge orbit structure.
# The container drops every ~30-50 min (6 occurrences), so each prime is solved,
# ANALYSED and COMMITTED before the next one starts.  A restart costs one prime,
# never the sweep.
cd /home/user/jacobian_planar
for p in 999979 999961 1000117 1000121 1000133 1000151 1000159 1000171; do
  f=wave6/bottomedge/be_c2is1_p${p}.ms
  [ -f "$f" ] || python3 - "$p" <<'PY'
import sympy as sp, sys
p=int(sys.argv[1]); w=sp.Symbol('w')
C=[sp.Symbol(f'c{i}') for i in range(1,9)]; D=[sp.Symbol(f'd{j}') for j in range(3,13)]
f=sum(C[i-1]*w**i for i in range(1,9)); g=w**2+sum(D[j-3]*w**j for j in range(3,13))
E=sp.expand(2*f*sp.diff(g,w)-3*sp.diff(f,w)*g-w**2)
eqs=[sp.expand(v) for k,v in sp.Poly(E,w).as_dict().items() if sp.expand(v)!=0]+[C[1]-1]
unk=sorted({v for e in eqs for v in e.free_symbols}, key=str)
head=",".join(str(u) for u in unk)+"\n"
body=",\n".join(str(sp.Poly(e,*unk).as_expr()).replace('**','^').replace(' ','') for e in eqs)
open(f"wave6/bottomedge/be_c2is1_p{p}.ms","w").write(head+str(p)+"\n"+body+"\n")
PY
  echo "$(date +%T) solving p=$p"
  timeout 600 msolve -f "$f" -o wave6/bottomedge/be_p${p}.out 2>/dev/null
  python3 wave6/bottomedge/analyse.py $p >> wave6/bottomedge/orbit_data.txt 2>&1
  git add -A >/dev/null 2>&1
  git commit -q -m "prime sweep: p=$p bottom-edge seed census (restart-resilient, one prime per commit)" >/dev/null 2>&1
  git push -q origin claude/opus-5-counterexample-plan-sep6yk >/dev/null 2>&1
  echo "$(date +%T) p=$p committed"
done
echo "SWEEPDONE"
