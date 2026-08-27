#!/usr/bin/env python3
"""For each GF(p)-rational q of the top layer, reduce to 4 unknowns and decide
which of f1..f8 are forced to vanish."""
import os
import subprocess
import sys

from uz_cascade_run import analyse, build_param_polys, subst, tstr, VN

HERE = os.path.dirname(os.path.abspath(__file__))


def to_str(P, names):
    if not P:
        return "0"
    out = []
    for m, c in sorted(P.items()):
        f = [str(c)]
        for i, e in enumerate(m):
            if e:
                f.append(names[i] + ("^%d" % e if e > 1 else ""))
        out.append("*".join(f))
    return "+".join(out)


def msolve_verdict(tag, names, body, char):
    path = os.path.join(HERE, f"{tag}.ms")
    out = os.path.join(HERE, f"{tag}.out")
    with open(path, "w") as fh:
        fh.write(",".join(names) + "\n" + f"{char}\n")
        fh.write(",\n".join(body) + "\n")
    subprocess.run(["msolve", "-f", path, "-o", out, "-t", "2"],
                   check=False, stdout=subprocess.DEVNULL,
                   stderr=subprocess.DEVNULL, timeout=3600)
    txt = open(out).read().strip()
    if txt.startswith("[-1]"):
        return "EMPTY"
    if ",-1,[]" in txt.replace(" ", "").replace("\n", ""):
        return "POSITIVE-DIM"
    return "SOLUTIONS"


if __name__ == "__main__":
    for path in sys.argv[1:]:
        for idx, res in enumerate(analyse(path)):
            MOD = res["mod"]
            if res["bad"]:
                print(f"mod {MOD} q#{idx}: f-layer inconsistent")
                continue
            pexpr, fexpr, NV = build_param_polys(res)
            names = VN[:NV]
            polys = []
            for e in res["E1"] + res["E0"]:
                P = subst(e, res, pexpr, fexpr, NV)
                if P:
                    polys.append(to_str(P, names))
            base = f"cas_{MOD}_{idx}"
            v = msolve_verdict(base, names, polys, MOD)
            print(f"mod {MOD} q#{idx}: system in {NV} unknowns, "
                  f"{len(polys)} eqs -> {v}", flush=True)
            if v == "EMPTY":
                continue
            for a in range(1, 9):
                fe = to_str(fexpr[a - 1], names)
                if fe == "0":
                    print(f"    f{a} = 0 identically")
                    continue
                sat = names + ["W"]
                bodysat = polys + [f"({fe})*W-1"]
                vv = msolve_verdict(f"{base}_f{a}", sat, bodysat, MOD)
                print(f"    f{a} != 0 possible? -> "
                      f"{'NO  (f%d forced to 0)' % a if vv=='EMPTY' else 'YES'}"
                      f"   [{vv}]", flush=True)
