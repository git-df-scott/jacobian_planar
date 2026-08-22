#!/usr/bin/env python3
"""Convert an msolve .ms file to a Singular script that tests EMPTINESS.

Air France 447: one solver's verdict is a data point, not a result.  This gives
an INDEPENDENT engine (Singular slimgb) on the identical input.

The variety is empty over the algebraic closure iff the ideal is the unit ideal,
iff its Groebner basis is {1}.  So we print exactly that test.
"""
import sys, os, re
src, out = sys.argv[1], sys.argv[2]
L = open(src).read().split('\n')
vs = [v.strip() for v in L[0].split(',') if v.strip()]
p = L[1].strip()
body = [b.strip().rstrip(',') for b in "\n".join(L[2:]).split(',\n') if b.strip()]
# symbol guard, again, before handing anything to a second engine
used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
leak = sorted(used - set(vs))
assert not leak, f"MALFORMED input, refusing: undeclared {leak[:8]}"
with open(out, 'w') as f:
    f.write(f'ring R = {p}, ({",".join(vs)}), dp;\n')
    f.write("ideal I = " + ",\n".join(body) + ";\n")
    f.write('option(redSB);\n')
    f.write('ideal G = slimgb(I);\n')
    f.write('int isunit = (size(G)==1 && G[1]==1);\n')
    f.write('if (isunit) { "SINGULAR_VERDICT: UNIT IDEAL -> VARIETY IS EMPTY"; }\n')
    f.write('else { "SINGULAR_VERDICT: NOT the unit ideal -> variety NONEMPTY"; '
            '"GB size:"; size(G); "dim:"; dim(G); }\n')
    f.write('exit;\n')
print(f"wrote {out}: {len(vs)} vars, {len(body)} equations, char {p}")
