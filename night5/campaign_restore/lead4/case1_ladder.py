#!/usr/bin/env python3
"""The essential-face system for subcase 1, and a validation ladder.

Derived (and independently re-derived symbolically in case1_face_derive.py)
from the polygons of subcase 1:

  direction (2,-1), weight w = 2i - j.
  face(P) = x f(u),  face(Q) = x^2 y g(u),  u = x y^2,  deg f = 7, deg g = 10.
  w(face P) = 2, w(face Q) = 3, w([P,Q]-top) = 2+3-1 = 4 = w(x^2),
  so the top component MUST EQUAL the target:

      [face P, face Q] = x^2 ( f g + 2 u f g' - 3 u f' g )  ==  x^2

  i.e.   W(u) := f g + 2 u f g' - 3 u f' g == 1 ,
  coefficientwise   W_n = sum_{i+j=n} (1 + 2j - 3i) a_i b_j = delta_{n,0}.

The top coefficient n = m+n vanishes identically iff 1 + 2n - 3m = 0, which
for (m,n) = (7,10) holds: 1+20-21 = 0.  The same equation with
(m,n) = (2k+1, 3k+1) is the essential face of the analogous smaller shape;
k = 0,1,2 give a VALIDATION LADDER whose answers can be cross-checked
against an independent combinatorial instrument (case1_hurwitz.py).

Symmetries used to normalise (both act on solutions, neither loses any):
  (a,b) -> (lam a, lam^{-1} b)     : W invariant       -> set a_0 = 1
  u -> t u, a_i -> t^i a_i, b_j -> t^j b_j : W_n -> t^n W_n -> set a_m = 1
and then W_0 = a_0 b_0 = 1 gives b_0 = 1.  Remaining: a_1..a_{m-1}, b_1..b_n
(m+n-1 unknowns) against W_1..W_{m+n-1} (m+n-1 equations).
Non-degeneracy still to impose: b_n != 0 (the vertex at the far end of the
Q-face), imposed by Rabinowitsch.
"""
import sys, subprocess, os, json

SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "_scratch_case1")
os.makedirs(SCRATCH, exist_ok=True)


def coeffs(m, n):
    """W_n as a dict n -> list of (coef, i, j)."""
    out = {}
    for N in range(0, m + n + 1):
        terms = []
        for i in range(max(0, N - n), min(m, N) + 1):
            j = N - i
            c = 1 + 2 * j - 3 * i
            if c:
                terms.append((c, i, j))
        out[N] = terms
    return out


def sym(nm, k, m):
    """a_0 = 1, a_m = 1, b_0 = 1; others are variables."""
    if nm == "a":
        if k == 0 or k == m:
            return "1"
        return f"a{k}"
    if k == 0:
        return "1"
    return f"b{k}"


def build(m, n, char=0, sat=True):
    W = coeffs(m, n)
    avars = [f"a{k}" for k in range(1, m)]
    bvars = [f"b{k}" for k in range(1, n + 1)]
    vs = avars + bvars + (["z"] if sat else [])
    L = [f"ring R = {char}, ({','.join(vs)}), dp;", "ideal I;"]
    neq = 0
    for N in range(1, m + n + 1):
        terms = []
        for (c, i, j) in W[N]:
            terms.append(f"({c})*{sym('a',i,m)}*{sym('b',j,m)}")
        if not terms:
            continue
        e = " + ".join(terms)
        L.append(f"I = I + ideal({e});")
        neq += 1
    if sat:
        L.append(f"I = I + ideal(z*b{n} - 1);")
    L.append(f'"equations: {neq}  unknowns: {len(vs)}";')
    L.append("ideal G = std(I);")
    L.append('if (size(G)==1 && G[1]==1) { "VERDICT: EMPTY"; }')
    L.append('else { "VERDICT: NONEMPTY  dim = " + string(dim(G));'
             ' if (dim(G)==0) { "  vdim = " + string(vdim(G)); } }')
    L.append("quit;")
    return "\n".join(L)


def run(m, n, char=0, sat=True, timeout=3600, tag=""):
    src = build(m, n, char, sat)
    fn = os.path.join(SCRATCH, f"case1_face_{m}_{n}_{char}_{int(sat)}{tag}.sing")
    open(fn, "w").write(src)
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=timeout)
        return pr.stdout.strip() + (("\nSTDERR " + pr.stderr.strip())
                                    if pr.stderr.strip() else "")
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


if __name__ == "__main__":
    ks = [int(v) for v in sys.argv[1:]] or [0, 1, 2, 3]
    for k in ks:
        m, n = 2 * k + 1, 3 * k + 1
        assert 1 + 2 * n - 3 * m == 0, (k, m, n)
        print(f"=== k={k}  deg f = {m}, deg g = {n} "
              f"(k=3 IS subcase 1's essential face) ===", flush=True)
        for char in (0, 32003):
            for sat in (True,):
                o = run(m, n, char, sat)
                print(f"  char {char} sat(b{n}!=0) : ", flush=True)
                for line in o.splitlines():
                    print("     ", line)
