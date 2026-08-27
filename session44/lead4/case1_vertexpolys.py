#!/usr/bin/env python3
"""Print the four vertex coefficients as explicit polynomials in the cascade
parameters, plus the level-0 condition, to expose the structure of the
obstruction."""
import sys
import case1_descend as CD
from case1_cascade import SP, SQ, base
from case1_point import find

p = int(sys.argv[1]); which = int(sys.argv[2])
stopW = int(sys.argv[3]) if len(sys.argv) > 3 else -12
r, err = find(p, which)
assert not err, err
CD.run(p, which, verbose=False, check_at=(), dump=None, stopW=stopW)
L = CD.LAST
RG, Pw, Qw = L["RG"], L["Pw"], L["Qw"]
names = ["t%d" % (i + 1) for i in range(len(L["params"]))]
def sgn(v):
    return v - p if 2 * v > p else v
def show(poly):
    return "  +  ".join(
        "%d%s" % (sgn(c), "".join("*" + names[i] +
                                  ("^%d" % m.count(i) if m.count(i) > 1 else "")
                                  for i in sorted(set(m))))
        for m, c in sorted(poly.items(), key=lambda kv: (len(kv[0]), kv[0])))
print("p =", p, " cover", which)
for lbl, tgt, S, w, i in [("P(8,16)", Pw, SP, 0, 8),
                          ("Q(12,24)", Qw, SQ, 0, 12),
                          ("P(0,8)", Pw, SP, -8, 0),
                          ("Q(0,12)", Qw, SQ, -12, 0)]:
    a, b, n = base(S, w)
    pol = tgt[w][i - a]
    txt = show(pol)
    print("%-9s = %s" % (lbl, txt if len(txt) < 300 else
                         "(%d terms, degree %d)" % (len(pol), RG.deg(pol))))
print("\nlevel-0 conditions:")
for c in L["conds"][:2]:
    print("   ", show(c))
