#!/usr/bin/env python3
"""WAVE 6b -- msolve bridge for the virgin shapes that facstd cannot finish.

Each _scratch/extract_w6_*.sing assembles the exact realization ideal mod
65521 (a 1-mod-3 prime) and then runs facstd -- which TIMEOUTs on the
triage-dropped shapes.  This bridge reuses each script's own assembly
verbatim, replaces the solve block with a raw generator dump (no Groebner),
converts to msolve input (c(i) -> c_i), and runs msolve.

CONTROL: bridged verdict on a shape facstd DID decide (w6_289012_0, EMPTY)
must be [-1].
"""
import os, re, subprocess, sys, json, time

AT = "/home/user/jacobian_planar/campaign/audit_tracks/_scratch"
OUT = "/home/user/jacobian_planar/wave6/ms"
os.makedirs(OUT, exist_ok=True)

def bridge(name, timeout=300):
    src = os.path.join(AT, f"extract_{name}.sing")
    txt = open(src).read()
    cut = txt.index("int t0 = timer")
    dump = txt[:cut] + f'\nwrite(":w {OUT}/{name}.gens", string(simplify(I,2)));\nquit;\n'
    dpath = os.path.join(OUT, f"{name}_dump.sing")
    open(dpath, "w").write(dump)
    r = subprocess.run(["Singular", "-q", dpath], capture_output=True,
                       text=True, timeout=120)
    gens = open(os.path.join(OUT, f"{name}.gens")).read().strip().rstrip(",")
    gens = gens.replace("c(", "c_").replace(")", "@@").replace("@@", "")
    # careful: only c(i) parens exist in generator strings; verify
    if "(" in gens:
        raise RuntimeError("unexpected parens in generators")
    m = re.search(r"ring R = (\d+), \(c\(1\.\.(\d+)\), ([a-z0-9, ]+)\)", txt)
    char, nc, extra = m.group(1), int(m.group(2)), m.group(3)
    vars_ = [f"c_{i}" for i in range(1, nc+1)] + [v.strip() for v in extra.split(",")]
    ms = ",".join(vars_) + "\n" + char + "\n" + ",\n".join(
        g.strip() for g in gens.split(",") if g.strip()) + "\n"
    mpath = os.path.join(OUT, f"{name}.ms")
    open(mpath, "w").write(ms)
    opath = os.path.join(OUT, f"{name}.out")
    t0 = time.time()
    try:
        subprocess.run(["msolve", "-t", "2", "-f", mpath, "-o", opath],
                       timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"name": name, "verdict": "MS-TIMEOUT", "wall": round(time.time()-t0,1)}
    data = open(opath).read(80) if os.path.exists(opath) else ""
    if data.startswith("[-1]"):
        v = "EMPTY"
    elif len(data) == 0:
        v = "NO-OUTPUT"
    else:
        v = "CANDIDATE-UNVERIFIED"
    return {"name": name, "verdict": v, "head": data[:40],
            "wall": round(time.time()-t0, 1)}

if __name__ == "__main__":
    names = sys.argv[1:]
    res = []
    for n in names:
        try:
            r = bridge(n)
        except Exception as e:
            r = {"name": n, "verdict": f"BRIDGE-ERROR {e}"}
        print(r)
        res.append(r)
        json.dump(res, open(os.path.join(OUT, "bridge_results.json"), "w"), indent=1)
