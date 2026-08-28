#!/usr/bin/env python3
"""Same cascade endgame, but decided with Singular (unambiguous verdicts)."""
import os
import subprocess
import sys

from uz_cascade_run import analyse, build_param_polys, subst, VN
from uz_final import to_str

HERE = os.path.dirname(os.path.abspath(__file__))


def singular(script, tag):
    path = os.path.join(HERE, f"{tag}.sing")
    open(path, "w").write(script)
    r = subprocess.run(["Singular", "-q", path], capture_output=True,
                       text=True, timeout=3600)
    return r.stdout.strip() + (("\nSTDERR:" + r.stderr) if r.stderr else "")


if __name__ == "__main__":
    for path in sys.argv[1:]:
        for idx, res in enumerate(analyse(path)):
            MOD = res["mod"]
            if res["bad"]:
                print(f"mod {MOD} q#{idx}: f-layer inconsistent")
                continue
            pexpr, fexpr, NV = build_param_polys(res)
            names = VN[:NV]
            polys = [to_str(subst(e, res, pexpr, fexpr, NV), names)
                     for e in res["E1"] + res["E0"]]
            polys = [p for p in polys if p != "0"]
            fs = [to_str(fexpr[a], names) for a in range(8)]
            ps = [to_str(pexpr[a], names) for a in range(8)]
            L = [f"ring R = {MOD}, ({','.join(names)},W), dp;",
                 "ideal I = " + ",".join(polys) + ";",
                 "ideal G = std(I);",
                 '"--- base system:";',
                 '"  dim  = " + string(dim(G));',
                 '"  vdim = " + string(vdim(G));',
                 '"  is (1)? " + string(size(G)==1 and G[1]==1);']
            for a in range(8):
                if fs[a] == "0":
                    L.append(f'"  f{a+1}: identically zero";')
                    continue
                L.append(f"ideal J{a} = I, ({fs[a]})*W-1;")
                L.append(f"ideal H{a} = std(J{a});")
                L.append(f'"  f{a+1} can be nonzero? " + '
                         f'string(!(size(H{a})==1 and H{a}[1]==1));')
            for a in range(8):
                if ps[a] == "0":
                    L.append(f'"  p{a+1}: identically zero";')
                    continue
                L.append(f"ideal K{a} = I, ({ps[a]})*W-1;")
                L.append(f"ideal M{a} = std(K{a});")
                L.append(f'"  p{a+1} can be nonzero? " + '
                         f'string(!(size(M{a})==1 and M{a}[1]==1));')
            L.append("exit;")
            print(f"=== mod {MOD} q#{idx} q={res['q']}", flush=True)
            print(singular("\n".join(L), f"sing_{MOD}_{idx}"), flush=True)
