"""Solve the case-(2) edge equation at an arbitrary prime and emit its RUR.

The hard-coded RUR in trackB1_case2_extend.py is for p = 65521.  A single
prime cannot certify a characteristic-0 statement, so this regenerates
everything at a fresh prime: solves

    2 C G' - 3 C' G = t^2,   C = t + c_2 t^2 + ... + c_7 t^7 + t^8,
                             G = g_2 t^2 + ... + g_12 t^12

(normalization c_1 = c_8 = 1; the two scalings t -> lambda t and
(C,G) -> (mu C, G/mu) move (c_1,c_8) by (mu*lambda, mu*lambda^8), so both can
be set to 1 up to a residual mu_7), checks the scheme is zero-dimensional,
puts it in shape position with respect to theta = g_12, factors the
eliminant, and writes a Python RUR table plus the branch list.

Output format (parsed by _c2_multiprime.py):
    VDIM <n>
    FACTOR <coefficients of one irreducible factor of the eliminant, ascending>
    VAR <name> <coefficients of its normal form as a polynomial in theta>
"""
import sys, os, subprocess, time

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")

VARS = [f"c({i})" for i in range(2, 8)] + [f"g({i})" for i in range(2, 12)]
NAMES = [f"c{i}" for i in range(2, 8)] + [f"g{i}" for i in range(2, 12)]


def build(q):
    L = [f"ring R = {q}, (c(2..7), g(2..12), t), dp;",
         "poly C = t + " + " + ".join(f"c({i})*t^{i}" for i in range(2, 8))
         + " + t^8;",
         "poly G = " + " + ".join(f"g({i})*t^{i}" for i in range(2, 13)) + ";",
         "poly Eq = 2*C*diff(G,t) - 3*diff(C,t)*G - t^2;",
         "ideal I;",
         "matrix MM = coeffs(Eq, t);",
         "int k;",
         "for (k = 1; k <= nrows(MM); k++) { I = I + ideal(MM[k,1]); }",
         f"ring R2 = {q}, (c(2..7), g(2..12)), dp;",
         "ideal J = simplify(imap(R, I), 2);",
         "ideal Gb = std(J);",
         'if (dim(Gb) != 0) { "NOT ZERO DIMENSIONAL: dim = " '
         '+ string(dim(Gb)); quit; }',
         '"VDIM " + string(vdim(Gb));',
         # shape position with theta = g(12) last
         f"ring RL = {q}, ({', '.join(VARS)}, g(12)), lp;",
         "ideal GL = stdfglm(imap(R2, J));",
         'if (size(GL) == 0) { "EMPTY EDGE"; quit; }',
         # the eliminant is the unique univariate element in g(12)
         "poly m = GL[size(GL)];",
         "int i;",
         "for (i = 1; i <= size(GL); i++) {",
         "  if (size(GL[i]) > 0 && deg(GL[i], intvec("
         + ",".join(["1"] * len(VARS)) + ",0)) == 0) { m = GL[i]; break; } }",
         '"MINPOLYDEG " + string(deg(m));',
         'LIB "poly.lib";',
         "list fl = factorize(m);",
         "for (i = 2; i <= size(fl[1]); i++) {",
         '  "FACTOR " + string(fl[1][i]);',
         "}",
         # normal forms of every other variable as a polynomial in g(12)
         "poly nf;"]
    for v, nm in zip(VARS, NAMES):
        L.append(f'nf = reduce({v}, GL);  "VAR {nm} " + string(nf);')
    L.append('"G12SELF ok";')
    L.append("quit;")
    return "\n".join(L)


if __name__ == "__main__":
    q = int(sys.argv[1]) if len(sys.argv) > 1 else 65521
    os.makedirs(SCRATCH, exist_ok=True)
    fn = os.path.join(SCRATCH, f"c2rur_{q}.sing")
    open(fn, "w").write(build(q))
    t0 = time.time()
    r = subprocess.run(["Singular", "-q", fn], capture_output=True, text=True,
                       timeout=int(sys.argv[2]) if len(sys.argv) > 2 else 3600)
    out = r.stdout
    open(os.path.join(SCRATCH, f"c2rur_{q}.txt"), "w").write(out)
    print(out.strip()[:4000])
    if r.stderr.strip():
        print("STDERR:", r.stderr.strip()[:1500])
    print(f"[wall {time.time()-t0:.0f}s]  -> {SCRATCH}/c2rur_{q}.txt")
