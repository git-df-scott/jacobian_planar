#!/usr/bin/env python3
"""Staged, restart-proof leaf-2 branch hunt mod p (p = 65521, p = 1 mod 3).

Per branch: (1) tiny edge GB with the branch factor pinned -> explicit edge
point(s); (2) substitute edge values into the 38 non-edge equations + the
nonvanishing product; (3) small residual GB -> verdict. Every stage writes its
artifact immediately; a rerun skips completed stages (marker files).

Verdicts append to trackB_staged_verdicts.log (the checkpoint of record).
mod-p is scouting evidence only; exact Q follows for anything interesting.
"""
import json, re, subprocess, sys, os, time

P = int(os.environ.get("JCP", "65521"))  # prime, must be 1 mod 3
assert P % 3 == 1
WD = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(WD, "trackB_staged_verdicts.log")

def log(msg):
    with open(LOG, "a") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {msg}\n")
    print(msg, flush=True)

# Stage timeouts are env-tunable: a branch that needs longer than the
# default must not silently cost its verdict, and on a shared/oversubscribed
# box the same branch can take several times its usual wall clock.
ST1_TIMEOUT = int(os.environ.get("JC_ST1_TIMEOUT", "900"))
ST2_TIMEOUT = int(os.environ.get("JC_ST2_TIMEOUT", "2400"))

def sing(script, name, timeout=1500):
    fn = os.path.join(WD, name)
    open(fn, "w").write(script)
    r = subprocess.run(["Singular", "-q", fn], capture_output=True, text=True, timeout=timeout)
    open(fn + ".out", "w").write(r.stdout + ("\n[stderr]\n" + r.stderr if r.stderr.strip() else ""))
    return r.stdout

# ---------- exact GF(p) polynomial layer (strings -> dicts) ----------
def parse_poly(s):
    """'a/b*v1^2*v2 + -c*v3' -> {frozenset_monomial: coeff mod P} with monomial as tuple((var,exp),...)"""
    out = {}
    for term in s.split(" + "):
        term = term.strip()
        if not term:
            continue
        parts = term.split("*")
        coef = 1
        mono = {}
        for pt in parts:
            m = re.fullmatch(r"([+-]?\d+)(?:/(\d+))?", pt)
            if m:
                num = int(m.group(1)) % P
                if m.group(2):
                    num = num * pow(int(m.group(2)), P - 2, P) % P
                coef = coef * num % P
                continue
            m = re.fullmatch(r"([+-])?(d_\d+_\d+)(?:\^(\d+))?", pt)
            assert m, f"bad factor {pt!r} in {term[:80]!r}"
            if m.group(1) == "-":
                coef = coef * (P - 1) % P
            mono[m.group(2)] = mono.get(m.group(2), 0) + int(m.group(3) or 1)
        key = tuple(sorted(mono.items()))
        out[key] = (out.get(key, 0) + coef) % P
    return {k: v for k, v in out.items() if v}

def subst(poly, vals):
    out = {}
    for mono, c in poly.items():
        keep = []
        for v, e in mono:
            if v in vals:
                c = c * pow(vals[v], e, P) % P
            else:
                keep.append((v, e))
        if c:
            k = tuple(keep)
            out[k] = (out.get(k, 0) + c) % P
            if not out[k]:
                del out[k]
    return out

def poly_str(poly):
    if not poly:
        return "0"
    terms = []
    for mono, c in sorted(poly.items()):
        f = [str(c)] + [f"{v}^{e}" if e > 1 else v for v, e in mono]
        terms.append("*".join(f))
    return " + ".join(terms)

# ---------- load the leaf (id from env JCLEAF; 2 = the new ground, 1 = the
# old campaign's d_2_2 = 0 slice) ----------
LEAF_ID = int(os.environ.get("JCLEAF", "2"))
tree = json.load(open(os.path.join(WD, "trackA_reduced_system.json")))
leaf = next(n for n in tree["nodes"] if n["id"] == LEAF_ID)
EQS = [parse_poly(e) for e in leaf["equations"]]
NZV = list(leaf.get("nonzero", []))
NZE = [parse_poly(e) for e in leaf.get("nonzero_exprs", [])]
EDGE_VARS = ["d_3_3", "d_4_5", "d_5_7", "d_6_9", "d_7_11", "d_8_13", "d_9_15"]
# Derived, never hardcoded: the Newton-edge subsystem is exactly the set of
# equations all of whose variables are edge variables. For leaf 2 this
# reproduces the previously hardcoded [38..43]; leaf 1 indexes them at
# [34..39] (same six equations — the edge subsystem is shared).
EDGE_IDX = [i for i, e in enumerate(leaf["equations"])
            if set(re.findall(r"[cd]_\d+_\d+", e))
            and set(re.findall(r"[cd]_\d+_\d+", e)) <= set(EDGE_VARS)]
if LEAF_ID == 2:
    assert EDGE_IDX == [38, 39, 40, 41, 42, 43], EDGE_IDX  # regression pin
REST_IDX = [i for i in range(len(EQS)) if i not in EDGE_IDX]

BRANCHES = {
    "r1": {"pin": "d_3_3-1", "factor": "d_9_15-28232"},
    "r2": {"pin": "d_3_3-1", "factor": "d_9_15-21444"},
    "r3": {"pin": "d_3_3-1", "factor": "d_9_15-16066"},
    "r5": {"pin": "d_3_3-1", "factor": "d_9_15-19859"},
    "r6": {"pin": "d_3_3-1", "factor": "d_9_15-796"},
    "r4": {"pin": "d_3_3-1", "factor": "d_9_15^2-13963*d_9_15+24777"},
    # r0a: d_9_15 = 0 on the normalized (d_3_3 != 0) chart.
    # r0b: d_3_3 = 0; d_9_15 = 0 is then forced (edge-zero eliminant = d_9_15^8,
    #      certified in trackB_edge_zero.out) — included as derived, not assumed.
    "r0a": {"pin": "d_3_3-1", "factor": "d_9_15"},
    "r0b": {"pin": "d_3_3", "factor": "d_9_15"},
}

def stage1(tag, spec):
    """Edge GB with the branch pin + factor; parse points (vdim may exceed 1)."""
    mark = os.path.join(WD, f"trackB_st1_{tag}.json")
    if os.path.exists(mark):
        return json.load(open(mark))
    factor = spec["factor"]
    scr = [f"ring R = {P}, ({','.join(EDGE_VARS)}), lp;", "ideal I;"]
    for k, i in enumerate(EDGE_IDX):
        scr.append(f"I[{k+1}] = {leaf['equations'][i]};")
    scr.append(f"I[{len(EDGE_IDX)+1}] = {spec['pin']};")
    scr.append(f"I[{len(EDGE_IDX)+2}] = {factor};")
    scr += ["short=0;", "option(redSB);", "ideal G = groebner(I);",
            '"DIM: " + string(dim(G));', '"VDIM: " + string(vdim(G));',
            '"GB:"; G;', "quit;"]
    out = sing("\n".join(scr), f"trackB_st1_{tag}.sing", timeout=ST1_TIMEOUT)
    # parse lex GB of a vdim-1 ideal: expect generators var-const (triangular)
    vals = {}
    quad_var = None
    for ln in out.splitlines():
        m = re.match(r"G\[\d+\]=(d_\d+_\d+)([+-]\d+)$", ln.strip())
        if m:
            vals[m.group(1)] = (-int(m.group(2))) % P
    res = {"tag": tag, "vals": vals, "raw_dim_vdim": [l for l in out.splitlines() if "DIM" in l],
           "full_gb_lines": [l for l in out.splitlines() if l.startswith("G[")]}
    json.dump(res, open(mark, "w"), indent=1)
    return res

def stage2(tag, vals, d33=1):
    """Substitute edge point into non-edge equations; residual GB; verdict."""
    mark = os.path.join(WD, f"trackB_st2_{tag}.done")
    if os.path.exists(mark):
        return
    sub = dict(vals)
    sub["d_3_3"] = d33
    res_eqs = []
    contradiction = False
    for i in REST_IDX:
        q = subst(EQS[i], sub)
        if not q:
            continue
        if all(len(m) == 0 for m in q):  # nonzero constant = contradiction
            contradiction = True
            break
        res_eqs.append(q)
    # nonzero product: vars + exprs, substituted
    nz_parts = []
    for v in NZV:
        nz_parts.append(parse_poly(v) if v not in sub else {(): sub[v]})
    for e in NZE:
        nz_parts.append(subst(e, sub))
    if any(p == {} for p in nz_parts):
        log(f"BRANCH {tag}: DEAD (a required-nonzero expression is identically 0 at the edge point)")
        open(mark, "w").write("dead-nz\n")
        return
    if contradiction:
        log(f"BRANCH {tag}: DEAD (constant contradiction after substitution)")
        open(mark, "w").write("dead-const\n")
        return
    rvars = sorted(set(v for q in res_eqs for m in q for v, _ in m)
                   | set(v for pp in nz_parts for m in pp for v, _ in m),
                   key=lambda s: tuple(map(int, s.split("_")[1:])))
    prod = "*".join(f"({poly_str(pp)})" for pp in nz_parts if pp != {(): 1})
    scr = [f"ring R = {P}, ({','.join(rvars)},w), dp;", "ideal I;"]
    for k, q in enumerate(res_eqs):
        scr.append(f"I[{k+1}] = {poly_str(q)};")
    scr.append(f"I[{len(res_eqs)+1}] = w*({prod})-1;" if prod else f"I[{len(res_eqs)+1}] = w-1;")
    scr += ["short=0;", "ideal G = groebner(I);", "int d = dim(G);",
            f'"BRANCH {tag} RESIDUAL DIM: " + string(d);',
            f'if (d==0) {{ "BRANCH {tag} RESIDUAL VDIM: " + string(vdim(G)); }}',
            f'if (d==-1) {{ "BRANCH {tag} EMPTY"; }}',
            "quit;"]
    out = sing("\n".join(scr), f"trackB_st2_{tag}.sing", timeout=ST2_TIMEOUT)
    verdict = [l for l in out.splitlines() if "BRANCH" in l or "// **" in l]
    log(f"BRANCH {tag}: stage2 vars={len(rvars)} eqs={len(res_eqs)} -> " + " | ".join(verdict[:3]))
    if verdict:
        open(mark, "w").write(out[-2000:])
    else:
        log(f"BRANCH {tag}: NO VERDICT (killed mid-run) — marker NOT written, will retry")

def normalize_sing(s):
    """Singular compact poly ('a2-3*b+4') -> parse_poly format ('a^2 + -3*b + 4')."""
    return re.sub(r"(?<=[0-9a-zA-Z_])([+-])", r" + \1", s)

def stage2b(tag, vals, gb_lines, d33=1):
    """Two-point (or extension) edge fiber: keep unpinned edge vars symbolic;
    ideal = all 44 eqs + stage-1 GB relations, pinned vals substituted."""
    mark = os.path.join(WD, f"trackB_st2_{tag}.done")
    if os.path.exists(mark):
        return
    sub = dict(vals)
    sub["d_3_3"] = d33
    gens = []
    for i in range(len(EQS)):
        q = subst(EQS[i], sub)
        if q and not all(len(m) == 0 for m in q):
            gens.append(q)
        elif q:
            log(f"BRANCH {tag}: DEAD (constant contradiction)"); open(mark, "w").write("dead\n"); return
    for ln in gb_lines:
        body = ln.split("=", 1)[1]
        q = subst(parse_poly(normalize_sing(body)), sub)
        if q and not all(len(m) == 0 for m in q):
            gens.append(q)
        elif q:
            log(f"BRANCH {tag}: DEAD (edge relation contradiction)"); open(mark, "w").write("dead\n"); return
    nz_parts = []
    for v in NZV:
        nz_parts.append(parse_poly(v) if v not in sub else {(): sub[v]})
    for e in NZE:
        pp = subst(e, sub)
        if not pp:
            log(f"BRANCH {tag}: DEAD (required-nonzero expr = 0)"); open(mark, "w").write("dead-nz\n"); return
        nz_parts.append(pp)
    rvars = sorted(set(v for q in gens for m in q for v, _ in m)
                   | set(v for pp in nz_parts for m in pp for v, _ in m),
                   key=lambda s: tuple(map(int, s.split("_")[1:])))
    prod = "*".join(f"({poly_str(pp)})" for pp in nz_parts if pp != {(): 1})
    scr = [f"ring R = {P}, ({','.join(rvars)},w), dp;", "ideal I;"]
    for k, q in enumerate(gens):
        scr.append(f"I[{k+1}] = {poly_str(q)};")
    scr.append(f"I[{len(gens)+1}] = w*({prod})-1;" if prod else f"I[{len(gens)+1}] = w-1;")
    scr += ["short=0;", "ideal G = groebner(I);", "int d = dim(G);",
            f'"BRANCH {tag} RESIDUAL DIM: " + string(d);',
            f'if (d==0) {{ "BRANCH {tag} RESIDUAL VDIM: " + string(vdim(G)); }}',
            f'if (d==-1) {{ "BRANCH {tag} EMPTY"; }}',
            "quit;"]
    out = sing("\n".join(scr), f"trackB_st2_{tag}.sing", timeout=ST2_TIMEOUT)
    verdict = [l for l in out.splitlines() if "BRANCH" in l]
    log(f"BRANCH {tag}: stage2b vars={len(rvars)} gens={len(gens)} -> " + " | ".join(verdict[:3]))
    if verdict:
        open(mark, "w").write(out[-2000:])
    else:
        log(f"BRANCH {tag}: NO VERDICT (killed mid-run) — marker NOT written, will retry")

def main():
    only = sys.argv[1:] or list(BRANCHES)
    for tag in only:
        if tag not in BRANCHES:
            log(f"skip unknown {tag}")
            continue
        t0 = time.time()
        s1 = stage1(tag, BRANCHES[tag])
        nvals = len(s1["vals"])
        log(f"BRANCH {tag}: stage1 done ({s1['raw_dim_vdim']}), {nvals} pinned vars")
        d33 = 0 if BRANCHES[tag]["pin"] == "d_3_3" else 1
        if nvals == len(EDGE_VARS):
            stage2(tag, s1["vals"], d33)
        else:
            stage2b(tag, s1["vals"], s1["full_gb_lines"], d33)
        log(f"BRANCH {tag}: total {time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
