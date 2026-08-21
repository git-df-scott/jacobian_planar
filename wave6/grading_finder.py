#!/usr/bin/env python3
"""Grading/torus finder for the resister systems (treasure-map strategy).

For each extract_*.sing: a weight vector w on the variables makes the ideal
quasi-homogeneous iff every generator's monomials share one w-degree, i.e.
w is in the nullspace of the exponent-difference matrix.  Torus rank =
nvars - rank(M) computed mod two primes (agreement required).  Rank >= 1
means the system carries a torus action -> slicing can shrink it (this is
exactly what explained the pentagon OOM).  Pure integer linear algebra.
"""
import sys, os, re, json

NAMES = ["w6_35657_0","w6_35657_1","w6_35657_2","w6_35657_3","w6_35657_4",
         "w6_35657_5","w6_35657_6","w6_35657_7","w6_79970_0","w6_79970_1",
         "w6_79970_2","w6_79970_3","p108_525122","p108_638901","p108_671059",
         "orph_345092","w6_289012_0"]
SCR = "/home/user/jacobian_planar/campaign/audit_tracks/_scratch"

def rank_mod(rows, ncols, p):
    # Gaussian elimination mod p on a list of int rows
    mat = [r[:] for r in rows]
    rank, col = 0, 0
    nrows = len(mat)
    while rank < nrows and col < ncols:
        piv = None
        for i in range(rank, nrows):
            if mat[i][col] % p:
                piv = i; break
        if piv is None:
            col += 1; continue
        mat[rank], mat[piv] = mat[piv], mat[rank]
        inv = pow(mat[rank][col] % p, p - 2, p)
        mat[rank] = [(v * inv) % p for v in mat[rank]]
        for i in range(nrows):
            if i != rank and mat[i][col] % p:
                f = mat[i][col] % p
                mat[i] = [(a - f * b) % p for a, b in zip(mat[i], mat[rank])]
        rank += 1; col += 1
    return rank

TERM = re.compile(r'([a-zA-Z_][a-zA-Z_0-9]*)(?:\^(\d+))?')

def analyze(name):
    txt = open(os.path.join(SCR, f"extract_{name}.sing")).read()
    m = re.search(r'ring R = (\d+), \(([^)]*\([^)]*\)[^)]*|[^)]*)\), dp', txt)
    # variables: expand c(1..N) style
    vdecl = m.group(2)
    mm = re.search(r'c\(1\.\.(\d+)\)', vdecl)
    nvars_c = int(mm.group(1)) if mm else 0
    extras = [v.strip() for v in re.sub(r'c\(1\.\.\d+\),?', '', vdecl).split(',') if v.strip()]
    vars_ = [f"c_{i}" for i in range(1, nvars_c + 1)] + extras
    vidx = {v: i for i, v in enumerate(vars_)}
    body = txt[txt.index('ideal I ='):]
    body = body[len('ideal I ='):body.index(';')]
    body = body.replace('c(', 'c_').replace(')', '')
    gens = [g.strip() for g in body.replace('\n', '').split(',') if g.strip()]
    rows = []
    nv = len(vars_)
    for g in gens:
        # split into terms at top level (+/- separators)
        terms = re.split(r'(?<![\^*])[+-]', g)
        evs = []
        for t in terms:
            t = t.strip()
            if not t:
                continue
            ev = [0] * nv
            for vm in TERM.finditer(t):
                v, e = vm.group(1), int(vm.group(2) or 1)
                if v in vidx:
                    ev[vidx[v]] += e
            evs.append(ev)
        for ev in evs[1:]:
            rows.append([a - b for a, b in zip(ev, evs[0])])
    r1 = rank_mod(rows, nv, 1000003)
    r2 = rank_mod(rows, nv, 65521)
    tor = nv - r1
    return {"name": name, "nvars": nv, "ngens": len(gens), "diffrows": len(rows),
            "rank_p1": r1, "rank_p2": r2, "agree": r1 == r2, "torus_rank": tor}

if __name__ == "__main__":
    out = []
    for n in NAMES:
        try:
            r = analyze(n)
        except Exception as e:
            r = {"name": n, "error": str(e)[:120]}
        print(json.dumps(r), flush=True)
        out.append(r)
    json.dump(out, open("/home/user/jacobian_planar/wave6/grading_results.json", "w"), indent=1)
