#!/usr/bin/env python3
"""EXACT symbolic attack on GGHV Prop 4.3 case (2), via the y-adic engine.

Case (2):  N(P) = {(0,0),(1,0),(8,14),(8,16)},
           N(Q) = {(0,0),(2,1),(12,21),(12,24)},   [P,Q] = x^2.

These are case (1)'s polygons MINUS the vertices (0,8) and (0,12), so N(P)
collapses to 25 lattice points (against case (1)'s 61) and the x = 0 column of
both P and Q becomes a single constant -- which is why the x=0 Theorems A/B of
case (1) degenerate here and say nothing.  The y = 0 structure is unchanged, so
the y-adic engine applies verbatim:

    N(Q)'s j = 0 row is {(0,0)}  =>  Q_0 constant, Q_0' = 0
    N(P)'s j = 0 row is {(0,0),(1,0)}  =>  P_0 = p_00 + p_10 x
    order y^0:  p_10 Q_1 = x^2  =>  Q_1 = x^2 / p_10.

Normalize p_10 = 1 (the scaling P -> cP, Q -> Q/c), leaving 24 parameters and a
recursion with NO denominators except the integers k+1, which are units mod p.
So the whole condition system is polynomial in 24 variables over F_p, and can be
handed to Singular.

Rows (computed, not assumed):
    N(P): 0:0-1 1:1-1 2:1-2 3:2-2 4:2-3 5:3-3 6:3-4 7:4-4 8:4-5 9:5-5
          10:5-6 11:6-6 12:6-7 13:7-7 14:7-8 15:8-8 16:8-8
    N(Q): 0:0-0 1:1-2 2:1-2 3:2-3 4:2-3 ... 23:12-12 24:12-12

Vertex conditions (nonzero): p_00 (vertex (0,0)), p_10 = 1 (vertex (1,0)),
the x^8 coefficient of P_14 (vertex (8,14)) and of P_16 (vertex (8,16)).
"""
import sys, os, subprocess
from trackB1_polygon import CASE2, hull_rows

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")
P_PRIME = 65521

def build_singular(jmax, extra=""):
    PR, QR = CASE2.PR, CASE2.QR
    # parameter naming: c(1..N) over the lattice points EXCLUDING (0,1)=p_10
    params = []
    for j in sorted(PR):
        lo, hi = PR[j]
        for i in range(lo, hi + 1):
            if (j, i) == (0, 1):
                continue
            params.append((j, i))
    n = len(params)
    lines = []
    lines.append(f"ring R = {P_PRIME}, (c(1..{n}), x), dp;")
    # P_j as polynomials in x
    for j in sorted(PR):
        lo, hi = PR[j]
        terms = []
        for i in range(lo, hi + 1):
            if (j, i) == (0, 1):
                terms.append("x")
            else:
                k = params.index((j, i)) + 1
                terms.append(f"c({k})*x^{i}" if i else f"c({k})")
        lines.append(f"poly P{j} = {' + '.join(terms)};")
    for j in range(max(PR) + 1, jmax + 2):
        lines.append(f"poly P{j} = 0;")
    # recursion:  (k+1) p10 Q_{k+1} = sum (a+1) P_{a+1} Q_b'
    #                                - sum_{a>=1} (b+1) P_a' Q_{b+1}
    lines.append("poly Q0 = 0;")
    lines.append("poly Q1 = x^2;")
    for k in range(1, jmax + 1):
        ts = []
        for a in range(0, k + 1):
            b = k - a
            if a + 1 <= jmax + 1:
                ts.append(f"{a+1}*P{a+1}*diff(Q{b}, x)")
            if a >= 1:
                ts.append(f"-{b+1}*diff(P{a}, x)*Q{b+1}")
        inv = pow(k + 1, P_PRIME - 2, P_PRIME)
        lines.append(f"poly Q{k+1} = {inv} * ({' + '.join(ts)});")
    # conditions: coefficients of Q_j outside N(Q)'s j-th row
    lines.append("ideal I;")
    for j in range(1, jmax + 1):
        if j in QR:
            lo, hi = QR[j]
        else:
            lo, hi = 1, 0                      # empty row: Q_j must vanish
        lines.append(f"matrix M{j} = coeffs(Q{j}, x);")
        lines.append(f"for (int t{j} = 1; t{j} <= nrows(M{j}); t{j}++) {{")
        lines.append(f"  if (t{j}-1 < {lo} || t{j}-1 > {hi}) "
                     f"{{ I = I + ideal(M{j}[t{j},1]); }} }}")
    lines.append('"conditions: " + string(size(I));')
    lines.append(extra if extra else
                 'ideal G = std(I); '
                 'if (size(G)==1 && G[1]==1) { "VERDICT: EMPTY"; } '
                 'else { "VERDICT: dim = " + string(dim(G)); }')
    lines.append("quit;")
    return "\n".join(lines), n

def run(jmax, timeout=2400, extra=""):
    src, n = build_singular(jmax, extra)
    os.makedirs(SCRATCH, exist_ok=True)
    fn = os.path.join(SCRATCH, f"case2_j{jmax}.sing")
    with open(fn, "w") as f:
        f.write(src)
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        return n, (r.stdout.strip() or r.stderr.strip()[:400])
    except subprocess.TimeoutExpired:
        return n, "TIMEOUT"

if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 12
    to = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    print("case (2): P rows " +
          " ".join(f"{j}:{a}-{b}" for j, (a, b) in CASE2.PR.items()))
    print("case (2): Q rows " +
          " ".join(f"{j}:{a}-{b}" for j, (a, b) in CASE2.QR.items()))
    print()
    for j in range(lo, hi + 1):
        n, out = run(j, to)
        print(f"conditions through y^{j} ({n} parameters): "
              f"{out.replace(chr(10), ' | ')}", flush=True)
