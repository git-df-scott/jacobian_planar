#!/usr/bin/env python3
"""The cascade PLUS the vertex non-degeneracy conditions.

The all-parameters-zero point is ALWAYS a solution of the cascade: it gives
P = face(P) = x f(u), Q = face(Q) = x^2 y g(u), which really does satisfy
[P,Q] = x^2 -- but its Newton polygon is the single essential edge, not the
pentagon.  So the cascade ideal is never the unit ideal, and the question is
whether a solution exists with the OTHER vertices of N(P) and N(Q) present:

    P at (0,8)   -> slice P_{-8}, its only coefficient
    P at (8,16)  -> slice P_0, coefficient with i = 8
    Q at (0,12)  -> slice Q_{-12}, its only coefficient
    Q at (12,24) -> slice Q_0, coefficient with i = 12

(the vertices (1,0),(8,14),(2,1),(12,21) are on the essential face and are
already nonzero there).  This module reports those four polynomials in the
cascade parameters and hands  I + (z * product - 1)  to Singular.
"""
import subprocess
import sys

import case1_descend as CD
from case1_cascade import SP, SQ, base
from case1_point import find


def main(p, which, stopW=-22):
    r, err = find(p, which)
    if err:
        print(err)
        return
    res, err = CD.run(p, which, verbose=False, check_at=(),
                      dump=None, stopW=stopW)
    L = CD.LAST
    RG, Pw, Qw = L["RG"], L["Pw"], L["Qw"]
    names = ["t%d" % (i + 1) for i in range(max(len(L["params"]), 1))]
    picks = []
    for lbl, tgt, S, w, i in [("P(0,8)", Pw, SP, -8, 0),
                              ("P(8,16)", Pw, SP, 0, 8),
                              ("Q(0,12)", Qw, SQ, -12, 0),
                              ("Q(12,24)", Qw, SQ, 0, 12)]:
        a, b, n = base(S, w)
        k = i - a
        pol = tgt.get(w, [dict()] * n)[k]
        picks.append((lbl, pol))
        print("  %-9s slice w=%-4d coeff k=%d : %s"
              % (lbl, w, k, "IDENTICALLY ZERO" if not pol
                 else "%d terms, degree %d" % (len(pol), RG.deg(pol))))
    if any(not pol for _, pol in picks):
        print("\nVERDICT: a required vertex coefficient is identically zero "
              "in the cascade -- the pentagon cannot be realised, subcase 1 "
              "is EMPTY for this face point (mod %d)." % p)
        return
    conds = L["conds"]
    nd = "*".join("(" + RG.s(pol, names) + ")" for _, pol in picks)
    src = ["ring R = %d, (%s,z), dp;" % (p, ",".join(names)),
           "ideal I = " + ",\n".join(RG.s(c, names) for c in conds) + ";",
           "I = I + ideal(z*(%s) - 1);" % nd,
           '"conditions: " + string(size(I));',
           "int t0 = timer; list LL = facstd(I);",
           '"time " + string(timer-t0) + "  components " + string(size(LL));',
           "int i; int alive = 0;",
           "for (i=1;i<=size(LL);i++) { ideal Gi = std(LL[i]);",
           " if (size(Gi)!=1 || Gi[1]!=1) { alive = alive+1;",
           '  "  live component " + string(i) + "  dim " + string(dim(Gi)); } }',
           'if (alive==0) { "VERDICT: EMPTY -- no non-degenerate solution '
           'over the algebraic closure of F_%d for this face point"; }' % p,
           'else { "VERDICT: " + string(alive) + " live component(s) survive"; }',
           "quit;"]
    fn = "_scratch_case1/nd_%d_%d.sing" % (p, which)
    open(fn, "w").write("\n".join(src))
    pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                        text=True, timeout=5000)
    print(pr.stdout.strip())
    if pr.stderr.strip():
        print("STDERR", pr.stderr.strip()[:400])


if __name__ == "__main__":
    p = int(sys.argv[1]); which = int(sys.argv[2])
    stopW = int(sys.argv[3]) if len(sys.argv) > 3 else -22
    print("=== p=%d cover %d  (cascade to W=%d) ===" % (p, which, stopW + 1))
    main(p, which, stopW)
