#!/usr/bin/env python3
"""Case (2) in the w = j - 2i grading: 5 ODEs in 7 univariate polynomials.

N(P) = {(0,0),(1,0),(8,14),(8,16)} has slanted edges j = 2i and j = 2i-2, so
in the grading w := j - 2i, **P has only weights 0, -1, -2**.  N(Q)'s edges are
j = 2i and j = 2i-3, so **Q has only weights 0, -1, -2, -3**.  Each weight piece
is a function of t := x y^2 times a power of y:

    P = A(t) + B(t)/y + C(t)/y^2,      Q = D(t) + E(t)/y + F(t)/y^2 + G(t)/y^3.

For such forms the bracket is exactly

    [ phi(t) y^-a , psi(t) y^-b ]  =  ( a phi psi' - b phi' psi ) y^(1-a-b),

so [P,Q] = x^2 = t^2 y^-4 splits by weight into FIVE equations (the weight-1
part [A,D] vanishes identically -- a = b = 0):

  (w= 0)   B D' = A' E
  (w=-1)   -2 A' F + B E' - B' E + 2 C D' = 0
  (w=-2)   -3 A' G + B F' - 2 B' F + 2 C E' - C' E = 0
  (w=-3)   B G' - 3 B' G + 2 C F' - 2 C' F = 0
  (w=-4)   ***  2 C G' - 3 C' G = t^2  ***

Coefficient counts match the lattice points exactly: A 9, B 8, C 8 (= 25 = N(P))
and D 13, E 12, F 12, G 11 (= 48 = N(Q)).

THE LAST EQUATION IS SELF-CONTAINED in (C, G).  Vertex conditions pin its
shape: (1,0) and (8,14) are the w = -2 corners so C = c_1 t + ... + c_8 t^8 with
c_1 != 0, c_8 != 0 (c_0 = 0 since (0,-2) is not a lattice point); (2,1) and
(12,21) are the w = -3 corners so G = g_2 t^2 + ... + g_12 t^12 with g_2 != 0,
g_12 != 0.

Two consequences by hand, before any computation:

* Setting W := G^2 - kappa C^3 with kappa = g_12^2/c_8^3 (so the degree-24 terms
  cancel), the equation gives  C W' - 3 C' W = t^2 G.  Comparing degrees, the
  left side has degree 7 + deg W (its leading coefficient carries deg W - 24,
  nonzero as deg W <= 23) and the right side has degree 14, so **deg W = 7**.
* W = 0 is impossible: it would force C = c M^2, G = gamma M^3, and then
  2 C G' - 3 C' G = 0, not t^2.

So the (C,G) subsystem is 19 unknowns and 17 equations (the t^2 coefficient
equals 1; the t^3..t^18 coefficients vanish -- the t^19 coefficient cancels
identically), with two scalings (t -> lambda t, and C -> mu C with G -> G/mu).
That is small enough to solve outright.
"""
import sys, os, subprocess, time

SCRATCH = ("/tmp/claude-0/-home-user-jacobian-planar/"
           "19771ba8-5fc7-5781-9122-dda56745e5ec/scratchpad")
PRIME = 65521

def build(sat=True, showgens=False, norm=None):
    """2 C G' - 3 C' G = t^2 with C = sum_{1..8} c_i t^i, G = sum_{2..12} g_i t^i."""
    L = [f"ring R = {PRIME}, (c(1..8), g(2..12), t), dp;"]
    L.append("poly C = " + " + ".join(f"c({i})*t^{i}" for i in range(1, 9)) + ";")
    L.append("poly G = " + " + ".join(f"g({i})*t^{i}" for i in range(2, 13)) + ";")
    if norm == "c8":
        L.append("C = subst(C, c(8), 1);")
    L.append("poly Eq = 2*C*diff(G,t) - 3*diff(C,t)*G - t^2;")
    L.append("ideal I;")
    L.append("matrix M = coeffs(Eq, t);")
    L.append("for (int k = 1; k <= nrows(M); k++) { I = I + ideal(M[k,1]); }")
    L.append('"equations: " + string(size(simplify(I,2)));')
    L.append(f"ring R2 = {PRIME}, (c(1..8), g(2..12)), dp;")
    L.append("ideal J = simplify(imap(R, I), 2);")
    if sat:
        # vertex conditions: c_1, c_8, g_2, g_12 all nonzero
        L.append("J = sat(J, c(1)*c(8)*g(2)*g(12))[1];")
    L.append("ideal Gb = std(J);")
    L.append('if (size(Gb) == 1 && Gb[1] == 1) { "VERDICT: EMPTY"; }')
    L.append('else { "VERDICT: dim = " + string(dim(Gb)); '
             'if (dim(Gb) == 0) { "vdim = " + string(vdim(Gb)); } '
             '"ngens = " + string(size(Gb)); }')
    if showgens:
        L.append('for (int gi = 1; gi <= size(Gb); gi++) '
                 '{ if (gi <= 12) { "GEN " + string(gi) + ": " '
                 '+ string(Gb[gi]); } }')
    L.append("quit;")
    return "\n".join(L)

def run(sat, showgens, norm, timeout):
    src = build(sat, showgens, norm)
    os.makedirs(SCRATCH, exist_ok=True)
    fn = os.path.join(SCRATCH,
                      f"c2edge_{'s' if sat else 'n'}_{norm or 'free'}.sing")
    open(fn, "w").write(src)
    t0 = time.time()
    try:
        r = subprocess.run(["Singular", "-q", fn], capture_output=True,
                           text=True, timeout=timeout)
        out = (r.stdout.strip() or r.stderr.strip()[:400])
    except subprocess.TimeoutExpired:
        out = "TIMEOUT"
    return out, time.time() - t0

if __name__ == "__main__":
    to = int(sys.argv[1]) if len(sys.argv) > 1 else 1800
    print("Case (2), lowest-weight edge equation  2 C G' - 3 C' G = t^2")
    print("  C: c_1..c_8 (c_1, c_8 != 0),  G: g_2..g_12 (g_2, g_12 != 0)\n",
          flush=True)
    for sat in (False, True):
        for norm in (None, "c8"):
            out, dt = run(sat, True, norm, to)
            print(f"[saturated={sat}, normalize c_8=1: {norm=='c8'}] "
                  f"{out.replace(chr(10), ' | ')}   [{dt:.0f}s]", flush=True)
