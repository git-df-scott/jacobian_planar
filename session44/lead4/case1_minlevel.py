#!/usr/bin/env python3
"""How deep must the cascade go before the obstruction bites?

Adds the Rabinowitsch inverse of the vertex product (and separately of t2)
to the conditions accumulated down to each level, and reports the first
level at which the ideal becomes the unit ideal."""
import subprocess, sys
import case1_descend as CD
from case1_cascade import SP, SQ, base
from case1_point import find

p = int(sys.argv[1]); which = int(sys.argv[2])
r, err = find(p, which); assert not err, err
for stopW in range(0, -13, -1):
    CD.run(p, which, verbose=False, check_at=(), dump=None, stopW=stopW)
    L = CD.LAST
    RG, Pw, Qw, conds = L["RG"], L["Pw"], L["Qw"], L["conds"]
    if not conds:
        print("levels down to W=%d : no conditions yet" % (stopW + 1))
        continue
    names = ["t%d" % (i + 1) for i in range(len(L["params"]))]
    picks = []
    for lbl, tgt, S, w, i in [("P(0,8)", Pw, SP, -8, 0),
                              ("P(8,16)", Pw, SP, 0, 8),
                              ("Q(0,12)", Qw, SQ, -12, 0),
                              ("Q(12,24)", Qw, SQ, 0, 12)]:
        if w in tgt:
            a, b, n = base(S, w)
            pol = tgt[w][i - a]
            if pol:
                picks.append(RG.s(pol, names))
    if not picks:
        print("levels down to W=%d : vertices not yet reached" % (stopW + 1))
        continue
    nd = "*".join("(%s)" % q for q in picks)
    src = ["ring R = %d, (%s,z), dp;" % (p, ",".join(names)),
           "ideal I = " + ",\n".join(RG.s(c, names) for c in conds) + ";",
           "I = I + ideal(z*(%s) - 1);" % nd,
           "list LL = facstd(I); int i; int alive = 0;",
           "for (i=1;i<=size(LL);i++) { ideal Gi = std(LL[i]);",
           " if (size(Gi)!=1 || Gi[1]!=1) { alive = alive+1; } }",
           'if (alive==0) { "EMPTY"; } else { "alive " + string(alive); }',
           "quit;"]
    fn = "_scratch_case1/ml_%d_%d_%d.sing" % (p, which, -stopW)
    open(fn, "w").write("\n".join(src))
    o = subprocess.run(["Singular", "-q", fn], capture_output=True,
                       text=True, timeout=3000).stdout.strip()
    print("levels down to W=%d : %d conditions, %d vertices available -> %s"
          % (stopW + 1, len(conds), len(picks),
             o.splitlines()[-1] if o else "?"), flush=True)
    if o.strip().endswith("EMPTY"):
        break
