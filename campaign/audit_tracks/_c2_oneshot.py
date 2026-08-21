"""Case (2) in ONE Singular system, with the vertex coefficient a_8 inverted.

The branch pipeline (_c2_branch.py) decided case (2) over F_65521 by solving
the edge equation first and then running the linear chain over each of the
four residue fields.  Its answer was that B = 0 on every solution, and the
hand lemma

    B = 0  =>  A' = 0  =>  a_8 = 0,  and then  2CD' = 0  =>  d_12 = 0

then removes the vertices (8,16) of N(P) and (12,24) of N(Q).  Equivalently:

    a_8 != 0  =>  B != 0,

so the entire case turns on whether a_8 can be nonzero.

This script asks that question directly, without the RUR: it writes the whole
five-equation system in the original coefficients and adjoins the
Rabinowitsch equation  w * a_8 = 1.  If the ideal is (1) the case is closed.
Running it over Q (char 0) rather than F_p would close it unconditionally --
a mod-p emptiness alone does not imply emptiness in characteristic zero.

Normalization: c_1 = c_8 = 1.  This is legitimate -- the polygon requires
c_1, c_8 != 0, and the two scalings t -> lambda t, (C,G) -> (mu C, G/mu) act
on (c_1, c_8) by (mu*lambda, mu*lambda^8), which can be brought to (1,1) (with
a residual mu_7 that just permutes solutions).  a_0 and d_0 are dropped since
A and D enter only through A' and D'.
"""
import sys, os, subprocess, time

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")


def build(char, extra_sat=None, method="std"):
    coef = "0" if char == 0 else str(char)
    v = ["c(2..7)", "g(2..12)", "a(1..8)", "b(1..8)",
         "d(1..12)", "e(1..12)", "f(1..12)", "w"]
    L = [f"ring R = {coef}, ({', '.join(v)}, t), dp;"]
    L.append("poly C = t + " + " + ".join(f"c({i})*t^{i}" for i in range(2, 8))
             + " + t^8;")
    L.append("poly G = " + " + ".join(f"g({i})*t^{i}" for i in range(2, 13))
             + ";")
    # A' only, so a(0) is irrelevant; a(8) is the vertex (8,16)
    L.append("poly A = " + " + ".join(f"a({i})*t^{i}" for i in range(1, 9))
             + ";")
    L.append("poly B = " + " + ".join(f"b({i})*t^{i}" for i in range(1, 9))
             + ";")
    L.append("poly D = " + " + ".join(f"d({i})*t^{i}" for i in range(1, 13))
             + ";")
    L.append("poly E = " + " + ".join(f"e({i})*t^{i}" for i in range(1, 13))
             + ";")
    L.append("poly F = " + " + ".join(f"f({i})*t^{i}" for i in range(1, 13))
             + ";")
    L.append("poly Ap = diff(A,t); poly Bp = diff(B,t); poly Cp = diff(C,t);")
    L.append("poly Dp = diff(D,t); poly Ep = diff(E,t); poly Fp = diff(F,t);")
    L.append("poly Gp = diff(G,t);")
    eqs = [
        ("w4", "2*C*Gp - 3*Cp*G - t^2"),
        ("w3", "B*Gp - 3*Bp*G + 2*C*Fp - 2*Cp*F"),
        ("w2", "-3*Ap*G + B*Fp - 2*Bp*F + 2*C*Ep - Cp*E"),
        ("w1", "-2*Ap*F + B*Ep - Bp*E + 2*C*Dp"),
        ("w0", "B*Dp - Ap*E"),
    ]
    L.append("ideal I;")
    L.append("matrix MM;")
    L.append("int k;")
    for nm, ex in eqs:
        L.append(f"poly {nm} = {ex};")
        L.append(f"MM = coeffs({nm}, t);")
        L.append("for (k = 1; k <= nrows(MM); k++) { I = I + ideal(MM[k,1]); }")
    L.append("I = I + ideal(w*a(8) - 1);")
    if extra_sat:
        L.append(f"I = I + ideal({extra_sat});")
    L.append('"equations: " + string(size(simplify(I,2)));')
    L.append(f"ring R2 = {coef}, ({', '.join(v)}), dp;")
    L.append("ideal J = simplify(imap(R, I), 2);")
    L.append("int t0 = timer;")
    L.append(f"ideal Gb = {method}(J);")
    L.append('"time: " + string(timer - t0);')
    L.append('if (size(Gb) == 1 && Gb[1] == 1)')
    L.append('  { "VERDICT: EMPTY -- a_8 != 0 is impossible, CASE (2) CLOSED"; }')
    L.append('else { "VERDICT: NONEMPTY, dim = " + string(dim(Gb))')
    L.append('       + "  ngens " + string(size(Gb)); }')
    L.append("quit;")
    return "\n".join(L)


if __name__ == "__main__":
    char = int(sys.argv[1]) if len(sys.argv) > 1 else 65521
    method = sys.argv[2] if len(sys.argv) > 2 else "std"
    os.makedirs(SCRATCH, exist_ok=True)
    fn = os.path.join(SCRATCH, f"c2oneshot_{char}_{method}.sing")
    open(fn, "w").write(build(char, method=method))
    print(f"[{fn}]  char = {char}, method = {method}", flush=True)
    t0 = time.time()
    r = subprocess.run(["Singular", "-q", fn], capture_output=True, text=True)
    print(r.stdout.strip())
    if r.stderr.strip():
        print("STDERR:", r.stderr.strip()[:2000])
    print(f"[wall {time.time()-t0:.0f}s]")
