#!/usr/bin/env python3
"""Attack the UNPINNED trackB1 system -- a genuine Q-system, unlike the pinned one.

WHY THIS IS THE RIGHT TARGET FOR CHARACTERISTIC ZERO
The seed-pinned system is NOT defined over Q: the seed is a root of the
irreducible quintic, so that system lives over a degree-5 number field and its
certificate cannot be rationally reconstructed by CRT over Q.

The UNPINNED system is defined over Q. If it is empty over Q (saturated at all
four nondegeneracy conditions), then case (1) is empty in characteristic zero
outright -- a STRONGER statement than the seed result, and it needs no
prime-goodness argument.

Plan: certificate at several primes on this one fixed Q-system, CRT, rationally
reconstruct, verify exactly.  This is the CRT route with the field problem fixed.
"""
import sys, re, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from w6_prime2 import load_exact, reduce_modp

SCR = ('/tmp/claude-0/-home-user-jacobian-planar/'
       'fbce63e6-c914-5e2b-b23c-4ee014d7f3e3/scratchpad')


def fmt(t):
    return "+".join("*".join([str(c)] + [f"{v}^{e}" if e > 1 else v for v, e in m])
                    for m, c in t.items()).replace("+-", "-")


def build(p):
    V, eqs_q, nz = load_exact()
    eqs = reduce_modp(eqs_q, p)
    body = [fmt(t) for t in eqs if t]
    vs = sorted(V) + ['zsat']
    body.append("*".join(['zsat'] + sorted(nz)) + "-1")
    used = {t for t in re.findall(r'[A-Za-z_]\w*', "\n".join(body))}
    leak = sorted(used - set(vs))
    assert not leak, f"MALFORMED: undeclared {leak[:6]}"
    f = f'{SCR}/tb1_{p}.sing'
    open(f, 'w').write(
        f'ring R = {p}, ({",".join(vs)}), dp;\nideal I = ' + ",\n".join(body) +
        ';\noption(redSB);\nideal G = slimgb(I);\n'
        'if (size(G)==1 && G[1]==1) { "RESULT UNIT"; matrix T = lift(I,G);\n'
        'int i; for(i=1;i<=nrows(T);i++){ if(T[i,1]!=0){ "LAM",i,":",T[i,1]; } } }\n'
        'else { "RESULT NOTUNIT"; "dim:"; dim(G); }\n"END";\nexit;\n')
    print(f"p={p}: {len(vs)} vars, {len(body)} equations, saturated on {sorted(nz)} "
          f"-> {os.path.basename(f)} ({os.path.getsize(f)} bytes)", flush=True)
    return f


if __name__ == '__main__':
    for p in [int(x) for x in sys.argv[1:]] or [1000003]:
        build(p)
