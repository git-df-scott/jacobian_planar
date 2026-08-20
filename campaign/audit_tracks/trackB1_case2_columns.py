#!/usr/bin/env python3
"""Case (2) by COLUMNS — the decomposition that makes the elimination tractable.

Writing P = sum_i P^(i)(y) x^i and Q = sum_i Q^(i)(y) x^i, the x^n coefficient
of [P,Q] = x^2 is

    sum_{i+j=n+1} [ i P^(i) (Q^(j))' - j (P^(i))' Q^(j) ]  =  delta_{n,2}.

N(P)'s two slanted edges are j = 2(i-1) and j = 2i, so **P^(i) is supported on
j in {2i-2, 2i-1, 2i}: only THREE coefficients per column**.  N(Q)'s are
j = 2i-3 and j = 2i, so Q^(i) has four.  In particular the only conditions are
N(Q)'s upper-left edge, i.e.

    ***  deg_y Q^(i) <= 2i,  i.e. the x^i coefficient of Q_j vanishes
         for every j > 2i.  ***

(Measured: every violation of N(Q) sits at the low-i boundary; the upper bound
propagates automatically.)

Because column n's equation involves P^(i) only for i <= n-1, the x^i column
conditions involve exactly the 3(i-1) parameters of P's columns 1..i-1 --
verified by exact Jacobian: x^2 -> 3 params, x^3 -> 6, x^4 -> 9.  So the system
solves as a NESTED cascade, three new parameters at a time, instead of one
23-variable Groebner basis.

Column 2 is already decisive by hand.  With g := P^(1) (degree <= 2, g(0) =
p_10 != 0), n = 1 gives the vanishing Wronskian of P^(1), Q^(1), so Q^(1) = c g;
and (1,0) not in N(Q) forces c = 0, hence Q^(1) = 0.  Then n = 2 gives

        g (Q^(2))' - 2 g' Q^(2) = 1,    so   Q^(2) = g^2 ( int dy/g^3 + C ).

If g has two distinct roots, int dy/g^3 has nonzero residues (a triple pole of
1/g^3 at a simple root of g), so it has log terms and is not rational.  If g has
a double root r, Q^(2) = -1/(5 p_12 (y-r)) + C p_12^2 (y-r)^4, which has a pole.
Only deg g <= 1 survives:  **p_12 = 0**, and then every column-2 condition holds
for arbitrary p_11 (checked 200/200 both ways).
"""
import sys, os, subprocess, time
from trackB1_polygon import CASE2

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")
PRIME = 65521

def params():
    out = []
    for j in sorted(CASE2.PR):
        lo, hi = CASE2.PR[j]
        for i in range(lo, hi + 1):
            if (j, i) in ((0, 0), (0, 1)):
                continue
            out.append((j, i))
    return out

PAR = params()

def build(colmax, jmax, sat=False, showgens=False, zeros=(), subs=None,
          only_high=False):
    """`zeros` = parameters (j,i) known to vanish; they are substituted OUT of
    the polynomials, not merely added to the ideal.  Column 2 proves p_12 = 0
    (Singular returns the single generator c(2)^2, radical (c(2))), so passing
    zeros=((2,1),) is sound and shrinks the system by a variable."""
    PR = CASE2.PR
    n = len(PAR)
    L = [f"ring R = {PRIME}, (c(1..{n}), x), dp;"]
    for j in sorted(PR):
        lo, hi = PR[j]
        terms = []
        for i in range(lo, hi + 1):
            if (j, i) == (0, 1):
                terms.append("x")
            elif (j, i) == (0, 0):
                continue
            elif (j, i) in zeros:
                continue
            elif subs and (j, i) in subs:
                v = subs[(j, i)]
                if v == "0":
                    continue
                terms.append(f"{v}*x^{i}" if i else v)
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
    # Conditions come in TWO families, and using only the first under-imposes:
    #  (a) N(Q)'s upper-left edge j <= 2i, for the columns i = 2..12 that N(Q)
    #      actually has:  x^i coefficient of Q_j vanishes for j > 2i.
    #  (b) N(Q) has NO column beyond i = 12, but the recursion's degree bound
    #      deg_x Q_j <= (j+3)/2 reaches 14 at j = 25,26 -- so columns 13 and 14
    #      must vanish IDENTICALLY.  That is 56 further conditions at jmax = 26,
    #      and omitting them makes the cascade look far weaker than it is.
    QTOP = max(CASE2.QR)                      # = 12 columns in N(Q)
    QCOLMAX = max(hi for lo, hi in CASE2.QR.values())
    L.append("ideal I;")
    lo_col = (QCOLMAX + 1) if only_high else 2
    for i in range(lo_col, min(colmax, QCOLMAX) + 1):
        for j in range(2 * i + 1, jmax + 1):
            L.append(f"I = I + ideal(coeffs(coeffs(Q{j}, x)[{i}+1,1], x)[1,1]);")
    if colmax > QCOLMAX:
        for i in range(QCOLMAX + 1, colmax + 1):
            for j in range(1, jmax + 1):
                L.append(f"if (size(coeffs(Q{j}, x)) > {i}) "
                         f"{{ I = I + ideal(coeffs(coeffs(Q{j}, x)[{i}+1,1], "
                         f"x)[1,1]); }}")
    L.append('"conditions: " + string(size(simplify(I,2)));')
    L.append(f"ring R2 = {PRIME}, c(1..{n}), dp;")
    L.append("ideal J = simplify(imap(R, I), 2);")
    if sat:
        v1 = PAR.index((14, 8)) + 1
        v2 = PAR.index((16, 8)) + 1
        L.append(f"J = sat(J, c({v1})*c({v2}))[1];")
    L.append("ideal G = std(J);")
    L.append('if (size(G) == 1 && G[1] == 1) { "VERDICT: EMPTY"; }')
    L.append('else { "VERDICT: dim = " + string(dim(G)); '
             'if (dim(G)==0) { "vdim = " + string(vdim(G)); } '
             '"ngens = " + string(size(G)); }')
    if showgens:
        L.append('for (int gi = 1; gi <= size(G); gi++) '
                 '{ "GEN " + string(gi) + ": " + string(G[gi]); }')
    L.append("quit;")
    return "\n".join(L), n

def run(colmax, jmax, timeout, sat=False, showgens=False, zeros=(), subs=None,
        only_high=False):
    src, n = build(colmax, jmax, sat, showgens, zeros, subs, only_high)
    os.makedirs(SCRATCH, exist_ok=True)
    tagp = ('_p' + str(subs[(1, 1)])) if subs and (1, 1) in subs else ''
    fn = os.path.join(SCRATCH, f"c2col_{colmax}_{jmax}{'_s' if sat else ''}"
                      f"{'_z' if zeros else ''}{tagp}{'_hi' if only_high else ''}.sing")
    open(fn, "w").write(src)
    t0 = time.time()
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        out = (r.stdout.strip() or r.stderr.strip()[:400])
    except subprocess.TimeoutExpired:
        out = "TIMEOUT"
    return n, out, time.time() - t0

if __name__ == "__main__":
    lo = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    hi = int(sys.argv[2]) if len(sys.argv) > 2 else 8
    jmax = int(sys.argv[3]) if len(sys.argv) > 3 else 26
    to = int(sys.argv[4]) if len(sys.argv) > 4 else 1800
    sat = "--sat" in sys.argv
    gens = "--gens" in sys.argv
    zeros = ((2, 1),) if "--z12" in sys.argv else ()
    subs = None
    for a in sys.argv:
        if a.startswith("--p11="):
            subs = {(1, 1): a.split("=")[1]}
    only_high = "--only-high" in sys.argv
    print(f"case (2): {len(PAR)} parameters (p_00 dropped, p_10 = 1); "
          f"jmax = {jmax}, sat={sat}, p12 subst={bool(zeros)}, "
          f"p11 subst={subs.get((1,1)) if subs else None}, "
          f"only-high-cols={only_high}\n", flush=True)
    for c in range(lo, hi + 1):
        n, out, dt = run(c, jmax, to, sat, gens, zeros, subs, only_high)
        print(f"columns 2..{c}: {out.replace(chr(10),' | ')}   [{dt:.0f}s]",
              flush=True)
        if "EMPTY" in out:
            print(f"\n*** CASE (2) CLOSED: columns 2..{c} are inconsistent ***")
            break
