#!/usr/bin/env python3
"""r0 closer: recursive sub-branching of the r0a/r0b edge fibers.

The r0 edge fibers are too big to push through stage2b whole (vdim 338 for
r0b, ~280 expected for r0a). Strategy: compute the lex GB of the edge ideal
with the branch pins; if its vdim is small enough, run the full-system
residual (stage2b). Otherwise find a univariate generator, factor it mod p,
and recurse on each irreducible factor. Every verdict appends to the log of
record; marker files make every node restart-proof.
"""
import json, os, re, sys, time
import trackB_staged as S

CAP = 6      # max edge vdim pushed straight to stage2b
MAXDEPTH = 4

def edge_gb(tag, pin, extras):
    mark = os.path.join(S.WD, f"trackB_r0_gb_{tag}.json")
    if os.path.exists(mark):
        return json.load(open(mark))
    scr = [f"ring R = {S.P}, ({','.join(S.EDGE_VARS)}), lp;", "ideal I;"]
    n = 0
    for i in S.EDGE_IDX:
        n += 1; scr.append(f"I[{n}] = {S.leaf['equations'][i]};")
    for x in [pin, "d_9_15"] + extras:
        n += 1; scr.append(f"I[{n}] = {x};")
    scr += ["short=0;", "option(redSB);", "ideal G = groebner(I);",
            'int d = dim(G);', '"DIM: " + string(d);',
            'if (d==0) { "VDIM: " + string(vdim(G)); }',
            '"GB:"; G;', "quit;"]
    out = S.sing("\n".join(scr), f"trackB_r0_gb_{tag}.sing", timeout=900)
    dim = -2; vdim = None
    for ln in out.splitlines():
        if ln.startswith("DIM: "):
            dim = int(ln.split()[1])
        if ln.startswith("VDIM: "):
            vdim = int(ln.split()[1])
    res = {"dim": dim, "vdim": vdim,
           "gb": [l for l in out.splitlines() if l.startswith("G[")]}
    json.dump(res, open(mark, "w"), indent=1)
    return res

def find_univariate(gb_lines):
    """Prefer a univariate generator in the deepest lex variable available."""
    best = None
    for ln in gb_lines:
        body = ln.split("=", 1)[1]
        p = S.parse_poly(S.normalize_sing(body))
        vs = set(v for m in p for v, _ in m)
        if len(vs) == 1:
            v = next(iter(vs))
            deg = max(e for m in p for vv, e in m if vv == v)
            rank = S.EDGE_VARS.index(v)
            if deg > 1 and (best is None or rank > best[2]):
                best = (body, v, rank, deg)
    return best

def factorize(body, tag):
    scr = [f"ring R = {S.P}, ({','.join(S.EDGE_VARS)}), lp;",
           "short=0;", f"poly f = {body};", "list L = factorize(f);",
           '"FACTORS:"; L[1];', "quit;"]
    out = S.sing("\n".join(scr), f"trackB_r0_fac_{tag}.sing", timeout=300)
    facs = []
    for ln in out.splitlines():
        m = re.match(r"_\[\d+\]=(.+)$", ln.strip())
        if m and m.group(1) != "1":
            facs.append(m.group(1))
    return facs

def close(tag, pin, extras, d33, depth):
    donemark = os.path.join(S.WD, f"trackB_r0_done_{tag}")
    if os.path.exists(donemark):
        return
    g = edge_gb(tag, pin, extras)
    if g["dim"] == -1:
        S.log(f"BRANCH {tag}: DEAD (edge fiber empty)")
        open(donemark, "w").write("dead-edge\n")
        return
    vd = g.get("vdim")
    S.log(f"BRANCH {tag}: edge fiber dim {g['dim']} vdim {vd} (depth {depth})")
    if g["dim"] == 0 and (vd is not None and vd <= CAP or depth >= MAXDEPTH):
        S.stage2b(tag, {}, g["gb"], d33)
        open(donemark, "w").write("closed-via-stage2b\n")
        return
    uni = find_univariate(g["gb"])
    if uni is None:
        S.log(f"BRANCH {tag}: no univariate to split (dim {g['dim']}) — forcing stage2b")
        S.stage2b(tag, {}, g["gb"], d33)
        open(donemark, "w").write("closed-via-stage2b-forced\n")
        return
    body, var, _, deg = uni
    facs = factorize(body, tag)
    S.log(f"BRANCH {tag}: splitting on {var} (deg {deg}) -> {len(facs)} factors")
    for k, f in enumerate(facs):
        close(f"{tag}_f{k}", pin, extras + [f], d33, depth + 1)
    open(donemark, "w").write(f"split:{var}:{len(facs)}\n")

def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "r0b"
    t0 = time.time()
    if which == "r0b":
        close("r0b", "d_3_3", [], 0, 0)
    else:
        close("r0a", "d_3_3-1", [], 1, 0)
    S.log(f"R0 CLOSER {which}: COMPLETE in {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
