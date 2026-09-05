import sys, sympy as sp
from core_e5 import eqs, A, B
mode = sys.argv[1] if len(sys.argv)>1 else "drv"     # drv | drvq | gauge
char = sys.argv[2] if len(sys.argv)>2 else "0"
L=[f"ring R = {char}, (A(0..7), B(0..10), z), dp;"]
def cv(e):
    s=str(sp.expand(e))
    for i in range(8): s=s.replace(f"A{i}",f"A({i})")
    for j in range(10,-1,-1): s=s.replace(f"B{j}",f"B({j})")
    return s
L.append("ideal I = " + ",\n  ".join(cv(e) for e in eqs if e!=0) + ";")
if mode=="drv":
    L.append("I = I + ideal(z*A(0)*A(7) - 1);")     # driver vertices (1,0),(8,14) nonzero
elif mode=="drvq":
    L.append("I = I + ideal(z*A(0)*A(7)*B(10) - 1);")  # + Q vertex (12,21) nonzero
elif mode=="none":
    pass
L.append('"variables: 19 + 1 rabinowitsch";')
L.append("int t0=timer;")
L.append("ideal G = std(I);")
L.append('"time: "+string(timer-t0);')
L.append('if (size(G)==1 && G[1]==1) { "VERDICT: CORE EMPTY"; } else { "VERDICT: core dim = "+string(dim(G)); if (dim(G)==0) {"vdim = "+string(vdim(G));} }')
L.append("quit;")
open(f"core_{mode}_{char}.sing","w").write("\n".join(L))
print(f"core_{mode}_{char}.sing")
