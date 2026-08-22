#!/usr/bin/env python3
"""Case (2) exact elimination — stage 1 of the case-(2) pipeline.

GGHV Prop 4.3 case (2):
    N(P) = {(0,0),(1,0),(8,14),(8,16)},  N(Q) = {(0,0),(2,1),(12,21),(12,24)},
    [P,Q] = x^2,   degrees (72,108)  -- BELOW 125, the live window.

Two exact reductions over the previous script:

R1. **p_00 is deleted, not carried.**  In the y-adic recursion P_0 enters only
    through P_0' = p_10, so the constant term p_00 NEVER appears in any
    condition.  (Measured independently: its Jacobian column is identically
    zero, and it is the ONLY such column.)  It is a genuine gauge --
    P -> P + nu leaves [P,Q] = x^2 and hence Q unchanged.  24 -> 23 parameters.

R2. **The ideal is mapped to a parameter-only ring.**  The generators are
    coefficients in x, so they involve no x at all; carrying x in the ring makes
    Singular order one extra variable for nothing, and forces dim = paramdim + 1
    bookkeeping.  After `imap` the reported dim IS the parameter dimension.

p_10 = 1 by the scaling P -> cP (Q -> Q/c, which does not move any condition,
since the conditions all say "this coefficient vanishes").

Vertex conditions: the x^8 coefficients of P_14 and P_16 (vertices (8,14) and
(8,16)) must be NONZERO, so the geometric question is about the SATURATION of
the ideal by them; `--sat` does that.  p_00 (vertex (0,0)) is unconstrained
because it does not appear, and p_10 = 1 is nonzero by construction.
"""
import sys, os, subprocess, time
from trackB1_polygon import CASE2

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")
PRIME = 65521

def params():
    """Lattice points of N(P) excluding (0,1) [=p_10, normalized to 1] and
    (0,0) [=p_00, which provably never appears]."""
    out = []
    for j in sorted(CASE2.PR):
        lo, hi = CASE2.PR[j]
        for i in range(lo, hi + 1):
            if (j, i) in ((0, 0), (0, 1)):
                continue
            out.append((j, i))
    return out

PAR = params()

def vertex_params():
    """indices (1-based) of the coefficients at vertices (8,14) and (8,16)."""
    out = []
    for v in ((14, 8), (16, 8)):
        out.append(PAR.index(v) + 1)
    return out

def build(jmax, sat=False, want_roots=False):
    PR, QR = CASE2.PR, CASE2.QR
    n = len(PAR)
    L = [f"ring R = {PRIME}, (c(1..{n}), x), dp;"]
    for j in sorted(PR):
        lo, hi = PR[j]
        terms = []
        for i in range(lo, hi + 1):
            if (j, i) == (0, 1):
                terms.append("x")
            elif (j, i) == (0, 0):
                continue                      # p_00 dropped (never appears)
            else:
                k = PAR.index((j, i)) + 1
                terms.append(f"c({k})*x^{i}" if i else f"c({k})")
        L.append(f"poly P{j} = {' + '.join(terms) if terms else '0'};")
    for j in range(max(PR) + 1, jmax + 2):
        L.append(f"poly P{j} = 0;")
    L.append("poly Q0 = 0;")
    L.append("poly Q1 = x^2;")
    for k in range(1, jmax + 1):
        ts = []
        for a in range(0, k + 1):
            b = k - a
            if a + 1 <= jmax + 1:
                ts.append(f"{a+1}*P{a+1}*diff(Q{b}, x)")
            if a >= 1:
                ts.append(f"-{b+1}*diff(P{a}, x)*Q{b+1}")
        inv = pow(k + 1, PRIME - 2, PRIME)
        L.append(f"poly Q{k+1} = {inv} * ({' + '.join(ts)});")
    L.append("ideal I;")
    for j in range(1, jmax + 1):
        lo, hi = QR.get(j, (1, 0))
        L.append(f"matrix M{j} = coeffs(Q{j}, x);")
        L.append(f"for (int t{j} = 1; t{j} <= nrows(M{j}); t{j}++) {{")
        L.append(f"  if (t{j}-1 < {lo} || t{j}-1 > {hi}) "
                 f"{{ I = I + ideal(M{j}[t{j},1]); }} }}")
    L.append('"conditions: " + string(size(I));')
    # ---- map to the parameter-only ring
    L.append(f"ring R2 = {PRIME}, c(1..{n}), dp;")
    L.append("ideal J = imap(R, I);")
    L.append("J = simplify(J, 2);")
    if sat:
        vp = vertex_params()
        L.append(f"poly nz = c({vp[0]})*c({vp[1]});")
        L.append("J = sat(J, nz)[1];")
    L.append("ideal G = std(J);")
    L.append('if (size(G) == 1 && G[1] == 1) { "VERDICT: EMPTY"; }')
    L.append('else { "VERDICT: dim = " + string(dim(G)) '
             '+ "  (parameters = ' + str(n) + ')"; '
             'if (dim(G) == 0) { "vdim = " + string(vdim(G)); } '
             '"ngens = " + string(size(G)); }')
    if want_roots:
        L.append('if (dim(G) == 0) { ')
        L.append('  ring R3 = ' + str(PRIME) + ', c(1..' + str(n) + '), lp;')
        L.append('  ideal Gl = std(imap(R2, J));')
        L.append('  "lex GB size: " + string(size(Gl));')
        L.append('  "last generator: " + string(Gl[size(Gl)]); }')
    L.append("quit;")
    return "\n".join(L), n

def run(jmax, timeout, sat=False, want_roots=False, tag=""):
    src, n = build(jmax, sat, want_roots)
    os.makedirs(SCRATCH, exist_ok=True)
    fn = os.path.join(SCRATCH, f"c2elim_{tag}{jmax}{'_sat' if sat else ''}.sing")
    with open(fn, "w") as f:
        f.write(src)
    t0 = time.time()
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        out = (r.stdout.strip() or r.stderr.strip()[:300])
    except subprocess.TimeoutExpired:
        out = "TIMEOUT"
    return n, out, time.time() - t0

if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 26
    to = int(sys.argv[3]) if len(sys.argv) > 3 else 3000
    sat = "--sat" in sys.argv
    roots = "--roots" in sys.argv
    print(f"case (2): {len(PAR)} parameters after dropping p_00 and p_10")
    print(f"vertex-nonzero params (1-based): {vertex_params()}  "
          f"[coefficients at (8,14) and (8,16)]")
    print(f"saturation: {sat}   roots: {roots}\n", flush=True)
    for j in range(lo, hi + 1):
        n, out, dt = run(j, to, sat, roots, tag="")
        print(f"y^{j}: {out.replace(chr(10),' | ')}   [{dt:.0f}s]", flush=True)
        if "EMPTY" in out:
            print(f"\n*** CASE (2) CLOSED at order y^{j} ***")
            break
