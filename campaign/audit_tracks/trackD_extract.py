"""Exact extraction for one reduced shape: the y-adic system + non-degeneracy.

The sweep engine (trackB1_shapes.run_pair) imposes only SUPPORT conditions --
"the y-adic recursion's Q must vanish outside N(Q)".  It never asks that the
required vertex coefficients of Q are NONZERO.  That gap is exactly what made
case (2) of Prop 4.3 look alive at dim 2 until the elimination showed every
solution had B = 0, killing the vertices (8,16) and (12,24) and collapsing the
Newton polygons.  A shape can therefore pass the whole sweep and still be
degenerate.

This module closes the gap the same way case (2) was closed: it writes the
FULL polynomial system in the driver's coefficients,

    Q_1     = R_0 / p_10
    Q_{k+1} = ( R_k + sum_{a+b=k} (a+1) P_{a+1} Q_b'
                    - sum_{a>=1, a+b=k} (b+1) P_a' Q_{b+1} ) / ((k+1) p_10)
    conditions:  coefficients of Q_j outside N(Q)'s row j vanish

adjoins Rabinowitsch inverses so that p_10 and every required vertex
coefficient of BOTH polygons are invertible, and hands it to Singular.  The
verdict is then a real one:

    EMPTY  -> the shape admits no non-degenerate realization
    dim d  -> a genuine d-dimensional family survives, worth lifting

Degrees grow like the row index, so this is only run on the small shapes; the
sweep's dim bound is the triage that decides which ones are small enough.
"""
import os, sys, subprocess, time
from trackB1_polygon import hull_rows

# Scratch dir: the old hardcoded path pointed at a dead session's scratchpad and
# would ENOENT on any new container.  Resolve it at import time instead.
SCRATCH = os.environ.get("TRACKD_SCRATCH") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "_scratch")
os.makedirs(SCRATCH, exist_ok=True)

# Characteristic.  Overridable so the sweep can be repeated at a second prime;
# both defaults are == 1 mod 3, which the cusp-(2,3) structure needs.
P = int(os.environ.get("TRACKD_PRIME", 65521))


def orient(NP, NQ):
    """Return (driver_verts, other_verts, sign) -- driver's j=0 row is {0,1}."""
    RP, RQ = hull_rows(NP), hull_rows(NQ)
    if RP.get(0) == (0, 1) and RQ.get(0) == (0, 0):
        return NP, NQ, 1
    if RQ.get(0) == (0, 1) and RP.get(0) == (0, 0):
        return NQ, NP, -1
    return None


def build_singular(NP, NQ, r, jextra=2, name="shape", method="facstd"):
    o = orient(NP, NQ)
    if o is None:
        return None, "OUT OF SCOPE: neither j=0 row is {(0,0),(1,0)}"
    DV, OV, sign = o
    DR, OR_ = hull_rows(DV), hull_rows(OV)
    jmaxD, jmaxO = max(DR), max(OR_)
    jmax = max(jmaxD, jmaxO) + jextra

    params = [(j, i) for j in sorted(DR) for i in range(DR[j][0], DR[j][1] + 1)]
    pv = {(j, i): f"c({k+1})" for k, (j, i) in enumerate(params)}

    L = []
    vars_ = [f"c(1..{len(params)})", "w", "u", "x"]
    L.append(f"ring R = {P}, ({', '.join(vars_)}), dp;")
    # driver rows
    for j in sorted(DR):
        terms = " + ".join(f"{pv[(j,i)]}*x^{i}"
                           for i in range(DR[j][0], DR[j][1] + 1))
        L.append(f"poly Pd{j} = {terms};")
    for j in range(0, jmax + 2):
        if j not in DR:
            L.append(f"poly Pd{j} = 0;")
    # right-hand side rows: [P,Q] = sign * x^r  lives entirely in row 0
    rr = f"{r if sign == 1 else P - 1}" if False else None
    L.append(f"poly Rr0 = {'1' if sign == 1 else str(P-1)}*x^{r};")
    for j in range(1, jmax + 2):
        L.append(f"poly Rr{j} = 0;")
    # p_10 inverse
    p10 = pv[(0, 1)]
    L.append(f"poly p10 = {p10};")
    L.append("poly Q0 = 0;")
    L.append(f"poly Q1 = Rr0 * w;")
    for k in range(1, jmax + 1):
        acc = [f"Rr{k}"]
        for a in range(0, k + 1):
            b = k - a
            if (a + 1) <= jmax + 1 and b <= jmax + 1:
                acc.append(f"({a+1})*Pd{a+1}*diff(Q{b}, x)")
            if a >= 1 and b + 1 <= jmax + 1:
                acc.append(f"-({b+1})*diff(Pd{a}, x)*Q{b+1}")
        inv_k1 = pow(k + 1, P - 2, P)
        L.append(f"poly Q{k+1} = ({' + '.join(acc)}) * w * {inv_k1};")
    # support conditions
    L.append("ideal I;")
    # deg(t) is the TOTAL degree in Singular, not the x-degree; looping to it
    # overruns coeffs(t,x), which has exactly deg_x(t)+1 rows.  Drive the loop
    # off nrows() instead.  Row e holds the coefficient of x^(e-1).
    L.append("poly t; int e; matrix cf;")
    for j in range(1, jmax + 1):
        lo, hi = OR_.get(j, (None, None))
        L.append(f"t = Q{j};")
        L.append("cf = coeffs(t, x);")
        L.append("for (e = 1; e <= nrows(cf); e++) {")
        if lo is None:
            L.append("  I = I + ideal(cf[e, 1]);")
        else:
            L.append(f"  if (e-1 < {lo} || e-1 > {hi})"
                     f" {{ I = I + ideal(cf[e, 1]); }}")
        L.append("}")
    # Rabinowitsch: p_10 and every required vertex coefficient invertible
    nd = [p10]
    for (j, i) in params:
        if (i, j) in [tuple(v) for v in DV] and (i, j) != (0, 0):
            if pv[(j, i)] not in nd:
                nd.append(pv[(j, i)])
    L.append(f"poly nd = {' * '.join(nd)};")
    L.append("I = I + ideal(w*p10 - 1);")
    L.append("I = I + ideal(u*nd - 1);")
    L.append('"params: " + string(' + str(len(params)) + ');')
    L.append('"conditions: " + string(size(simplify(I,2)));')
    L.append("int t0 = timer;")
    if method == "facstd":
        # factorizing Groebner: splits the ideal into components as it goes,
        # so a system that collapses to (1) on every branch never has to build
        # one dense basis.  This is the cheap replacement for std() on the
        # overdetermined y-adic systems.
        L.append("list LL = facstd(I);")
        L.append('"time: " + string(timer - t0);')
        L.append('"components: " + string(size(LL));')
        L.append("int ii; int alive = 0; int dmax = -1;")
        L.append("for (ii = 1; ii <= size(LL); ii++) {")
        L.append("  ideal Gi = std(LL[ii]);")
        L.append("  if (size(Gi) != 1 || Gi[1] != 1) { alive = alive + 1;")
        L.append("    if (dim(Gi) > dmax) { dmax = dim(Gi); }")
        L.append('    "  live component " + string(ii) + ": dim " '
                 '+ string(dim(Gi)) + (dim(Gi)==0 ? ", vdim " '
                 '+ string(vdim(Gi)) : ""); }')
        L.append("}")
        L.append('if (alive == 0) { "VERDICT: EMPTY -- no non-degenerate '
                 'realization"; }')
        L.append('else { "VERDICT: " + string(alive) + " live component(s), '
                 'max dim " + string(dmax); }')
    else:
        L.append("ideal G = std(I);")
        L.append('"time: " + string(timer - t0);')
        L.append('if (size(G)==1 && G[1]==1) { "VERDICT: EMPTY -- no '
                 'non-degenerate realization"; }')
        L.append('else { "VERDICT: dim = " + string(dim(G));'
                 ' if (dim(G)==0) { "vdim = " + string(vdim(G)); } }')
    L.append("quit;")
    return "\n".join(L), dict(nparams=len(params), jmax=jmax,
                              driver_is_P=(sign == 1), ndegen=nd)


def run(NP, NQ, r, name, timeout=1800, jextra=2, method="facstd"):
    src, info = build_singular(NP, NQ, r, jextra=jextra, name=name, method=method)
    if src is None:
        return {"name": name, "status": "OUT OF SCOPE", "detail": info}
    fn = os.path.join(SCRATCH, f"extract_{name}.sing")
    open(fn, "w").write(src)
    t0 = time.time()
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=timeout)
        out = pr.stdout.strip()
    except subprocess.TimeoutExpired:
        return {"name": name, "status": "TIMEOUT", "secs": time.time() - t0,
                "info": info}
    # The engine contract is EMPTY | NONEMPTY | TIMEOUT | OOM, and OOM arrives
    # two ways: a kill signal (exit -9 / 137 / 14) or Singular's own
    # "no more memory" message.  This function previously ignored returncode
    # entirely and reported every non-timeout run as "RAN", so an OOM-killed
    # process came back as a successful run with empty output -- which the
    # callers then filed as UNKNOWN.  Eight targets in the two-prime sweep were
    # misfiled that way before this was caught.
    blob = ((pr.stdout or "") + (pr.stderr or "")).lower()
    if pr.returncode in (-9, 137, 14) or "no more memory" in blob:
        return {"name": name, "status": "OOM", "out": out, "rc": pr.returncode,
                "secs": time.time() - t0, "info": info}
    if pr.returncode != 0 and not out:
        return {"name": name, "status": "CRASH", "out": out, "rc": pr.returncode,
                "secs": time.time() - t0, "info": info}
    return {"name": name, "status": "RAN", "out": out, "rc": pr.returncode,
            "secs": time.time() - t0, "info": info}


if __name__ == "__main__":
    # self-test on the two shapes whose answer is already known:
    #   (8,28) case (2) -- closed this session, must come back EMPTY
    #   (8,28) case (1) -- still open, must NOT come back EMPTY
    KNOWN = [
        ("case2_quad", [(0, 0), (1, 0), (8, 14), (8, 16)],
         [(0, 0), (2, 1), (12, 21), (12, 24)], 2),
        ("case1_pent", [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)],
         [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)], 2),
    ]
    which = sys.argv[1:] or [k[0] for k in KNOWN]
    for nm, NPp, NQq, r in KNOWN:
        if nm not in which:
            continue
        print(f"=== {nm} ===", flush=True)
        res = run(NPp, NQq, r, nm, timeout=int(os.environ.get("TMO", 1800)))
        print(f"  status {res['status']}  [{res.get('secs',0):.0f}s]")
        if res.get("info"):
            print(f"  params={res['info']['nparams']} jmax={res['info']['jmax']}"
                  f" driver_is_P={res['info']['driver_is_P']}")
            print(f"  non-degeneracy product: {' * '.join(res['info']['ndegen'])}")
        for line in (res.get("out") or "").splitlines():
            print("    " + line)
