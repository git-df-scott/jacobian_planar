#!/usr/bin/env python3
"""Locate the obstruction: which single vertex does the cascade kill?"""
import subprocess, sys
import case1_descend as CD
from case1_cascade import SP, SQ, base
from case1_point import find

p = int(sys.argv[1]); which = int(sys.argv[2])
stopW = int(sys.argv[3]) if len(sys.argv) > 3 else -12
r, err = find(p, which); assert not err, err
CD.run(p, which, verbose=False, check_at=(), dump=None, stopW=stopW)
L = CD.LAST
RG, Pw, Qw, conds = L["RG"], L["Pw"], L["Qw"], L["conds"]
names = ["t%d" % (i + 1) for i in range(len(L["params"]))]
tests = {}
for lbl, tgt, S, w, i in [("P(0,8)", Pw, SP, -8, 0), ("P(8,16)", Pw, SP, 0, 8),
                          ("Q(0,12)", Qw, SQ, -12, 0),
                          ("Q(12,24)", Qw, SQ, 0, 12)]:
    a, b, n = base(S, w)
    tests[lbl] = RG.s(tgt[w][i - a], names)
tests["t2 alone"] = "t2"
for lbl, poly in tests.items():
    src = ["ring R = %d, (%s,z), dp;" % (p, ",".join(names)),
           "ideal I = " + ",\n".join(RG.s(c, names) for c in conds) + ";",
           "I = I + ideal(z*(%s) - 1);" % poly,
           "list LL = facstd(I); int i; int alive = 0;",
           "for (i=1;i<=size(LL);i++) { ideal Gi = std(LL[i]);",
           " if (size(Gi)!=1 || Gi[1]!=1) { alive = alive+1; } }",
           'if (alive==0) { "FORCED TO ZERO by the cascade"; } '
           'else { "can be nonzero (" + string(alive) + " components)"; }',
           "quit;"]
    fn = "_scratch_case1/obs_%s.sing" % lbl.replace("(", "").replace(")", "") \
        .replace(",", "_").replace(" ", "")
    open(fn, "w").write("\n".join(src))
    o = subprocess.run(["Singular", "-q", fn], capture_output=True,
                       text=True, timeout=3000).stdout.strip()
    print("  %-10s : %s" % (lbl, o.splitlines()[-1] if o else "?"), flush=True)
