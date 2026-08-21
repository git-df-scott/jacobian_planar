#!/usr/bin/env python3
"""Full case-(2) leaf-2 sweep at an arbitrary prime P = 1 mod 3 (env JCP).

Branch roots are prime-specific, so this re-derives them: normalized edge
eliminant -> factorize mod P -> one staged closure per factor, plus the two
r0 charts. All artifact names carry p{P}, so sweeps at different primes
coexist. Verdict lines land in trackB_staged_verdicts.log.
"""
import os, re, sys, time
import trackB_staged as S
import trackB_r0 as R0

P = S.P

def eliminant_factors():
    scr = [f"ring R = {P}, ({','.join(S.EDGE_VARS)}), lp;", "ideal I;"]
    n = 0
    for i in S.EDGE_IDX:
        n += 1; scr.append(f"I[{n}] = {S.leaf['equations'][i]};")
    scr.append(f"I[{n+1}] = d_3_3-1;")
    scr += ["short=0;",
            "ideal E = eliminate(I, d_3_3*d_4_5*d_5_7*d_6_9*d_7_11*d_8_13);",
            '"ELIMDEG: " + string(deg(E[1]));',
            "list f = factorize(E[1]);", '"FACTORS:"; f[1];', "quit;"]
    out = S.sing("\n".join(scr), f"trackB_sweep_elim_p{P}.sing", timeout=900)
    facs = []
    for ln in out.splitlines():
        m = re.match(r"_\[\d+\]=(.+)$", ln.strip())
        if m and m.group(1) != "1":
            facs.append(m.group(1))
    deg = [l for l in out.splitlines() if l.startswith("ELIMDEG")]
    S.log(f"SWEEP p={P}: eliminant {deg}, {len(facs)} irreducible factors")
    return facs

def main():
    t0 = time.time()
    facs = eliminant_factors()
    nonzero_facs = [f for f in facs if f != "d_9_15"]
    for k, f in enumerate(nonzero_facs):
        tag = f"p{P}_rk{k}"
        s1 = S.stage1(tag, {"pin": "d_3_3-1", "factor": f})
        if len(s1["vals"]) == len(S.EDGE_VARS):
            S.stage2(tag, s1["vals"], 1)
        else:
            S.stage2b(tag, s1["vals"], s1["full_gb_lines"], 1)
    R0.close(f"p{P}_r0a", "d_3_3-1", [], 1, 0)
    R0.close(f"p{P}_r0b", "d_3_3", [], 0, 0)
    S.log(f"SWEEP p={P}: COMPLETE in {time.time()-t0:.0f}s "
          f"({len(nonzero_facs)} eliminant branches + r0a + r0b)")

if __name__ == "__main__":
    main()
