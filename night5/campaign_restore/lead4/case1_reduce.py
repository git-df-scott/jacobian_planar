#!/usr/bin/env python3
"""Reduce the essential-face system by eliminating g's coefficients.

W_N = sum_{i+j=N} (1 + 2j - 3i) a_i b_j.  With a_0 = 1 the term j = N
contributes (1 + 2N) b_N, and 1 + 2N != 0, so for N = 1..n the equation
W_N = 0 SOLVES for b_N as a polynomial in a_1..a_{m-1} and b_<N.
The remaining equations W_{n+1} .. W_{m+n-1} (that is m-1 of them) then
involve only a_1..a_{m-1}: a square system of size m-1.

For subcase 1 (m,n) = (7,10) this is 6 equations in 6 unknowns.
"""
import os, subprocess, sys
from case1_ladder import coeffs, sym

SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "_scratch_case1")


def singular_reduce(m, n, char, out_prefix):
    W = coeffs(m, n)
    avars = ",".join(f"a{k}" for k in range(1, m))
    L = [f"ring R = {char}, ({avars}), dp;", "poly b0 = 1;"]
    for N in range(1, n + 1):
        # W_N = (1+2N) b_N + rest ; solve for b_N
        rest = []
        for (c, i, j) in W[N]:
            if i == 0 and j == N:
                assert c == 1 + 2 * N, (c, N)
                continue
            av = sym('a', i, m)
            rest.append(f"({c})*{av}*b{j}")
        r = " + ".join(rest) if rest else "0"
        L.append(f"poly b{N} = -({r}) / {1 + 2*N};")
    eqs = []
    for N in range(n + 1, m + n + 1):
        terms = []
        for (c, i, j) in W[N]:
            terms.append(f"({c})*{sym('a',i,m)}*b{j}")
        if terms:
            eqs.append(" + ".join(terms))
    for idx, e in enumerate(eqs):
        L.append(f"poly E{idx+1} = {e};")
    L.append(f'"residual equations: {len(eqs)}  unknowns: {m-1}";')
    for idx in range(len(eqs)):
        L.append(f'"E{idx+1} deg " + string(deg(E{idx+1})) '
                 f'+ " terms " + string(size(E{idx+1}));')
    # dump for msolve
    L.append(f'link ll = "write: {out_prefix}.txt"; ')
    for idx in range(len(eqs)):
        L.append(f'write(ll, string(E{idx+1}));')
    L.append("close(ll);")
    # and solve here too
    L.append("ideal I = " + ",".join(f"E{i+1}" for i in range(len(eqs))) + ";")
    L.append("int t0 = timer; ideal G = std(I);")
    L.append('"std time " + string(timer-t0);')
    L.append('if (size(G)==1 && G[1]==1) { "VERDICT: EMPTY"; } else '
             '{ "VERDICT: NONEMPTY dim " + string(dim(G)); '
             'if (dim(G)==0) { "vdim " + string(vdim(G)); } }')
    L.append("quit;")
    return "\n".join(L)


if __name__ == "__main__":
    k = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    char = int(sys.argv[2]) if len(sys.argv) > 2 else 0
    m, n = 2 * k + 1, 3 * k + 1
    pref = os.path.join(SCRATCH, f"case1_red_k{k}_c{char}")
    src = singular_reduce(m, n, char, pref)
    fn = pref + ".sing"
    open(fn, "w").write(src)
    pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                        text=True, timeout=3000)
    print(pr.stdout.strip())
    if pr.stderr.strip():
        print("STDERR", pr.stderr.strip()[:500])
