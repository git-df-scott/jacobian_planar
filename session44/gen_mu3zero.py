"""Generate the mu3=0 companion systems for the B=16 F-system ladder.

The ladder's verdicts were produced in the gauge mu3=1, justified by the
scaling (x,y) -> (l^a x, l^b y), which rescales mu3 by l^(a+b) and so
normalizes any NONZERO mu3 to 1.  The mu3=0 stratum is fixed by that
action and needs its own query; this was never run on the derivation-grade
F-system.  This script emits msolve inputs (char 0 and mod-p) for
j, satvar given on the command line, with mu3 = 0 substituted exactly.
"""
import sys

import sympy as sp

import f_system as FS


def export(j, satvar, chars, timeout_note=""):
    q0p, p0p, E = FS.derive()
    eqs, unks = FS.instantiate(j, q0p, p0p, E)
    eqs = [sp.expand(e.subs(FS.mu3, 0)) for e in eqs]
    unks = [u for u in unks if u != FS.mu3]
    s = sp.Symbol("s_sat")
    sv = {"mu0": FS.mu0, "mu1": FS.mu1, "mu2": FS.mu2}[satvar]
    eqs = [e for e in eqs if e != 0] + [sv * s - 1]
    unks = unks + [s]
    base = FS.to_msolve(eqs, unks)
    body = base.split("\n", 2)
    for ch in chars:
        txt = body[0] + "\n" + str(ch) + "\n" + body[2]
        fn = f"lead4/j{j}{satvar}_mu3zero_" + ("char0" if ch == 0
                                               else f"p{ch}") + ".ms"
        open(fn, "w").write(txt)
        print(fn, len(txt))


if __name__ == "__main__":
    j = int(sys.argv[1])
    satvar = sys.argv[2]
    export(j, satvar, [0, 65521, 65539])
