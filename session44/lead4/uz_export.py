#!/usr/bin/env python3
"""Export the (u,z) obstruction system to msolve / Singular."""
import os
import subprocess
import sys
import time
from fractions import Fraction

from uz_eliminate import run
from uz_system import NVARS_P, PVARS

SCRATCH = os.path.dirname(os.path.abspath(__file__))


def obstruction_system(fixed):
    obs, _ = run(mod=None, fixed=fixed, verbose=False)
    live = [v for v in PVARS if v not in fixed]
    polys = []
    for key, o in obs:
        den = 1
        for c in o.values():
            den = den * c.denominator // _gcd(den, c.denominator)
        terms = []
        for m, c in sorted(o.items()):
            n = int(c * den)
            assert Fraction(n) == c * den
            f = [str(abs(n))]
            for i, e in enumerate(m):
                if e:
                    f.append(PVARS[i] + ("^%d" % e if e > 1 else ""))
            terms.append(("-" if n < 0 else "+") + "*".join(f))
        s = "".join(terms).lstrip("+")
        polys.append((key, s))
    return live, polys


def _gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def write_ms(path, variables, polys, char, extra=()):
    body = list(polys) + list(extra)
    with open(path, "w") as fh:
        fh.write(",".join(variables) + "\n")
        fh.write(f"{char}\n")
        fh.write(",\n".join(body) + "\n")
    return path


def write_singular(path, variables, polys, char, extra=(), cmd="dimension"):
    body = list(polys) + list(extra)
    with open(path, "w") as fh:
        fh.write(f"ring R = {char}, ({','.join(variables)}), dp;\n")
        fh.write("ideal I = " + ",\n  ".join(body) + ";\n")
        fh.write('option(redSB);\n')
        fh.write("ideal G = groebner(I);\n")
        fh.write('if (size(G) == 1 and G[1] == 1) { "VERDICT: IDEAL = (1) '
                 '-- NO SOLUTION"; } else { "VERDICT: proper ideal"; '
                 '"dim = " + string(dim(G)); "size = " + string(size(G)); }\n')
        fh.write("exit;\n")
    return path


if __name__ == "__main__":
    pass
