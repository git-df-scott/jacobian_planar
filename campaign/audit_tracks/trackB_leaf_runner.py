#!/usr/bin/env python3
"""Track B: run a reduced-system leaf through Singular over Z/p (p = 1 mod 3).

Generates a Singular script from a leaf of trackA_reduced_system.json:
  ring over Z/p, ideal = leaf equations + Rabinowitsch inverses for every
  nonzero variable and every transferred nonzero_expr, then groebner, dim,
  vdim, and (dim 0) the reduced basis + per-variable eliminants.
mod-p is SCOUTING EVIDENCE ONLY (JC is false in char p); exact Q is the
proof standard. Containment sanity: Rabinowitsch is used instead of sat(),
so no saturation containment check is needed; the w-variables make the
nonvanishing conditions part of the ideal itself.
"""
import json, re, subprocess, sys, time

def leaf_to_singular(leaf, p, elim_var=None):
    eqs = leaf["equations"]
    nz_vars = list(leaf.get("nonzero", []))
    nz_exprs = list(leaf.get("nonzero_exprs", []))
    vs = sorted(set(v for e in eqs + nz_exprs for v in re.findall(r"d_\d+_\d+", e)),
                key=lambda s: tuple(map(int, s.split("_")[1:])))
    for v in nz_vars:
        if v not in vs:
            vs.append(v)
    wties = []
    k = 0
    for v in nz_vars:
        k += 1; wties.append(f"w{k}*({v})-1")
    for ex in nz_exprs:
        k += 1; wties.append(f"w{k}*({ex})-1")
    ws = [f"w{i+1}" for i in range(k)]
    lines = [f"ring R = {p}, ({','.join(vs + ws)}), dp;"]
    lines.append("ideal I;")
    for i, e in enumerate(eqs):
        lines.append(f"I[{i+1}] = {e};")
    for j, t in enumerate(wties):
        lines.append(f"I[{len(eqs)+j+1}] = {t};")
    lines += [
        'short = 0;',
        '"NVARS: %s (incl %s rabinowitsch)";' % (len(vs) + len(ws), len(ws)),
        '"NEQS: %s";' % (len(eqs) + len(wties)),
        "ideal G = groebner(I);",
        '"GB done";',
        "int d = dim(G);",
        '"DIM: %s (in ring with rabinowitsch vars)";' % "\" + string(d) + \"",
    ]
    lines.append('if (d == 0) { "VDIM: " + string(vdim(G)); }')
    lines.append('if (d == 0) { "GBSIZE: " + string(size(G)); }')
    if elim_var:
        lines.append('if (d == 0) { poly el = 0; ideal E = eliminate(G, %s); "ELIM_DONE"; }'
                     % "*".join([v for v in vs if v != elim_var] + ws))
        lines.append('if (d == 0) { E; }')
    lines.append('if (d == -1) { "EMPTY: ideal is the whole ring (branch DEAD mod %s)"; }' % p)
    lines.append("quit;")
    return "\n".join(lines), vs, ws

def main():
    tree, leaf_id, p = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    elim_var = sys.argv[4] if len(sys.argv) > 4 else None
    d = json.load(open(tree))
    leaf = next(n for n in d["nodes"] if n["id"] == leaf_id)
    assert p % 3 == 1, "p must be = 1 mod 3"
    scr, vs, ws = leaf_to_singular(leaf, p, elim_var)
    sname = f"trackB_leaf{leaf_id}_p{p}.sing"
    open(sname, "w").write(scr)
    t0 = time.time()
    r = subprocess.run(["Singular", "-q", sname], capture_output=True, text=True, timeout=3000)
    out = r.stdout
    open(f"trackB_leaf{leaf_id}_p{p}.out", "w").write(out + ("\n[stderr]\n" + r.stderr if r.stderr.strip() else ""))
    print(f"# leaf {leaf_id}, p={p}, {time.time()-t0:.1f}s, vars {len(vs)}+{len(ws)}w")
    for ln in out.splitlines():
        if any(t in ln for t in ("NVARS", "NEQS", "DIM", "VDIM", "GBSIZE", "EMPTY", "ELIM")):
            print(ln)

if __name__ == "__main__":
    main()
