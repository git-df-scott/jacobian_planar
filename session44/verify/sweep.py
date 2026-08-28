#!/usr/bin/env python3
"""Sweep primes: FGLM -> five covers -> verdict, all self-verifying.

A prime is usable when 7 does not divide p-1 (so each quintic root has a
unique seventh root, giving exactly one rational point per cover) and the
quintic splits completely.  Every face point is checked against
2 q t' - 3 q' t = u^2 before any verdict is believed.
"""
import json, subprocess, sys
import sympy as sp
from face_solve_indep import face_system
import solve_lex, own_verdict

def fglm(prime):
    eqs, unk, coef, poly = face_system(prime, {"q1": 1, "q8": 1})
    body = ",\n ".join(str(e) for e in eqs)
    L = [f"ring D = {prime}, ({','.join(map(str,unk))}), dp;",
         f"ideal I = {body};", "ideal G = std(I);",
         '"vdim = " + string(vdim(G));',
         f"ring L = {prime}, ({','.join(map(str,unk))}), lp;",
         "setring L; ideal I = fetch(D,I);",
         "ideal GL = stdfglm(I);",
         '"lex GB size = " + string(size(GL));',
         "int i; for(i=1;i<=size(GL);i++){ \"GL \"+string(GL[i]); }", "quit;"]
    fn = f"sw_{prime}.sing"
    open(fn, "w").write("\n".join(L) + "\n")
    o = subprocess.run(["Singular", "-q", fn], capture_output=True,
                       text=True, timeout=900).stdout
    open(f"sw_{prime}.log", "w").write(o)
    return o

if __name__ == "__main__":
    results = {}
    for prime in [int(a) for a in sys.argv[1:]]:
        if (prime - 1) % 7 == 0:
            print(f"p={prime}: skip (7 | p-1)"); continue
        if not sp.isprime(prime):
            print(f"p={prime}: skip (not prime)"); continue
        o = fglm(prime)
        if "vdim = 35" not in o:
            print(f"p={prime}: vdim not 35, skip"); continue
        try:
            pts = solve_lex.main(prime, f"sw_{prime}.log")
        except Exception as ex:
            print(f"p={prime}: extraction failed ({ex})"); continue
        if len(pts) != 5:
            print(f"p={prime}: only {len(pts)}/5 covers rational, skip")
            continue
        json.dump(pts, open(f"facepts_verified_p{prime}.json", "w"))
        eqs, unks = own_verdict.systems(pts[0], prime)
        ctrl = own_verdict.run(eqs, unks, prime, [], f"sw_ctrl_{prime}")
        if ctrl:
            print(f"p={prime}: CONTROL FAILED (empty without vertex cond)")
            continue
        v = []
        for i, pt in enumerate(pts):
            e, un = own_verdict.systems(pt, prime)
            v.append(own_verdict.run(e, un, prime, ["f8", "g12"],
                                     f"sw_main_{prime}_{i}"))
        results[prime] = (sum(v), len(v))
        print(f"p={prime}: control OK, {sum(v)}/{len(v)} covers EMPTY",
              flush=True)
    print("\n=== SWEEP SUMMARY ===")
    for k, (a, b) in sorted(results.items()):
        print(f"  p={k:8d}: {a}/{b} covers EMPTY")
    print(f"  primes with complete 5/5 emptiness: "
          f"{sum(1 for a,b in results.values() if a==b==5)}/{len(results)}")
