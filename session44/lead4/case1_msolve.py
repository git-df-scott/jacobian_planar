#!/usr/bin/env python3
"""msolve driver for the essential-face system (independent of Singular)."""
import os, subprocess, sys
from case1_ladder import coeffs, sym

SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "_scratch_case1")
os.makedirs(SCRATCH, exist_ok=True)


def gen(m, n, char, sat=True):
    W = coeffs(m, n)
    vs = [f"a{k}" for k in range(1, m)] + [f"b{k}" for k in range(1, n + 1)]
    if sat:
        vs = vs + ["z"]
    polys = []
    for N in range(1, m + n + 1):
        terms = []
        for (c, i, j) in W[N]:
            terms.append(f"({c})*{sym('a',i,m)}*{sym('b',j,m)}")
        if terms:
            polys.append(" + ".join(terms))
    if sat:
        polys.append(f"z*b{n} - 1")
    return ",".join(vs) + "\n" + str(char) + "\n" + ",\n".join(polys) + "\n"


if __name__ == "__main__":
    k = int(sys.argv[1]); char = int(sys.argv[2]) if len(sys.argv) > 2 else 1073741827
    m, n = 2 * k + 1, 3 * k + 1
    src = gen(m, n, char)
    fn = os.path.join(SCRATCH, f"case1_face_k{k}_p{char}.ms")
    open(fn, "w").write(src)
    out = os.path.join(SCRATCH, f"case1_face_k{k}_p{char}.res")
    pr = subprocess.run(["msolve", "-f", fn, "-o", out, "-g", "2", "-v", "1"],
                        capture_output=True, text=True, timeout=3000)
    print(pr.stdout[-3000:]); print("ERR", pr.stderr[-2000:])
    txt = open(out).read()
    print("output size", len(txt))
    print(txt[:600])
