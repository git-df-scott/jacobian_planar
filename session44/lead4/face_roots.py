#!/usr/bin/env python3
"""Extract explicit face solutions mod p from msolve's RUR, then cascade.

msolve's mod-p output is a rational univariate representation:
  [0, [p, nvars, deg, varnames, linform, [1, [[d,[elim coeffs]], [den],
       [[[d1,[num1]]], [[d2,[num2]]], ...]]]]]
A root T of the eliminant gives each variable as num_i(T)/den(T).

Each root is one of the 35 essential-face solutions. Feeding each into the
linear cascade (cascade.py) tests whether it extends to a full (P,Q):

  all 35 fail  ->  strong mod-p evidence that the subcase is EMPTY
  one extends  ->  an explicit candidate, to be lifted to characteristic
                   zero and verified exactly before any claim.
"""
import ast, subprocess, sys
import sympy as sp

p = 65521


def get_rur(fn):
    r = subprocess.run(["msolve", "-f", fn], capture_output=True, text=True,
                       timeout=1800)
    s = (r.stdout or "").strip().rstrip(":")
    s = s.replace("[", "(").replace("]", ")")
    return ast.literal_eval(s)


def polyeval(co, T):
    v = 0
    for c in reversed(co):
        v = (v * T + c) % p
    return v


if __name__ == "__main__":
    fn = sys.argv[1] if len(sys.argv) > 1 else "facesolve_c65521.ms"
    print(f"parsing msolve RUR from {fn}")
    R = get_rur(fn)
    try:
        body = R[1]
        prime, nv, deg, names, linform = body[0], body[1], body[2], body[3], body[4]
        block = body[5]
        elim = block[1][0]
        den = block[1][1]
        nums = block[1][2]
        print(f"  prime {prime}, {nv} vars {list(names)}, degree {deg}")
        print(f"  eliminant degree {elim[0]}, linear form {list(linform)}")
    except Exception as e:
        print("  RUR shape unexpected:", e); print(str(R)[:300]); sys.exit(1)
    ec = list(elim[1])
    print(f"  scanning {p} field elements for eliminant roots ...", flush=True)
    roots = [T for T in range(p) if polyeval(ec, T) == 0]
    print(f"  found {len(roots)} roots in GF({p}) "
          f"(of {elim[0]} over the closure)")
    if roots:
        print(f"  first few: {roots[:8]}")
    import json
    json.dump({"roots": roots, "elim": ec, "den": den, "nums": nums,
               "names": list(names)}, open("face_roots.json", "w"))
    print("  wrote face_roots.json")
