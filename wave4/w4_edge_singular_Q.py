"""
The case-(2) w = -4 residual system over Q, decided by SINGULAR rather than
msolve.

msolve -P 1 on this system (12 variables, 9 generators, chart, gauge and the
Rabinowitsch generator) has produced no output in over two hours.  Singular is
an independent engine on the identical generators; whatever it returns is a
cross-check on the mod-p picture, which says the solution set is a single
Galois orbit of size 5.

What is computed is dim/vdim of the ideal over Q and, when it is zero
dimensional, its univariate eliminant in the separating variable.  The
eliminant must be the degree-5 polynomial already certified by
w4_edge_eliminant_structure.py -- that agreement is the point of the run.

CONTROLS
  S1 POSITIVE: Singular reproduces dim 0 and vdim 5 over Q;
  S2 POSITIVE: the eliminant Singular returns equals the certified one up to a
     rational scalar;
  S3 NEGATIVE: adding a contradictory pin makes the ideal the unit ideal
     (dim -1), so S1 is not reporting a fixed answer.
"""
import json
import os
import subprocess
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
MS = sys.argv[1] if len(sys.argv) > 1 else "/tmp/w4Q.ms"
RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def read_ms(path):
    lines = [l.strip() for l in open(path) if l.strip()]
    varline, _, *gens = lines
    return varline.split(","), [g.rstrip(",") for g in gens]


def singular(vars_, gens, extra, tag, timeout):
    src = [f"ring R = 0,({','.join(vars_)}),dp;",
           "ideal I = " + ",\n  ".join(gens + extra) + ";",
           "ideal G = std(I);",
           'printf("DIM %s", dim(G));',
           "if (dim(G) == 0) {",
           "  ring L = 0,(" + ",".join(vars_) + "),lp;",
           "  ideal J = fglm(R, G);",
           '  printf("VDIM %s", vdim(std(J)));',
           f'  printf("ELIM %s", J[size(J)]);',
           "}",
           "exit;"]
    path = f"/tmp/{tag}.sing"
    open(path, "w").write("\n".join(src) + "\n")
    try:
        r = subprocess.run(["Singular", "-q", path], capture_output=True,
                           text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return {"status": "TIMEOUT"}
    out = r.stdout
    d = {"status": "OK", "raw": out[-4000:]}
    for k in ("DIM", "VDIM", "ELIM"):
        for line in out.splitlines():
            if line.startswith(k + " "):
                d[k.lower()] = line[len(k) + 1:].strip()
    return d


def main():
    print("=" * 78)
    print("the case-(2) w = -4 residual system over Q, decided by Singular")
    print("=" * 78)
    vars_, gens = read_ms(MS)
    print(f"    {len(gens)} generators in {len(vars_)} variables from {MS}")
    real = singular(vars_, gens, [], "w4Qsing", 20000)
    print(f"    dim={real.get('dim')} vdim={real.get('vdim')} "
          f"status={real['status']}")
    check("S1 POSITIVE: Singular decides the system over Q with dim 0 and "
          "vdim 5", real.get("dim") == "0" and real.get("vdim") == "5",
          f"dim {real.get('dim')}, vdim {real.get('vdim')}")

    ok2, note2 = False, "no eliminant returned"
    if real.get("elim"):
        w = sp.Symbol(vars_[-1])
        got = sp.Poly(sp.sympify(real["elim"].replace("^", "**")), w)
        ej = json.load(open(os.path.join(HERE, "artifacts",
                                         "edge_eliminant_Q_one.json")))
        want = sp.Poly(sum(sp.Rational(c) * w ** i
                           for i, c in enumerate(ej["coefficients"])), w)
        ok2 = sp.simplify(got.as_expr() * want.LC() -
                          want.as_expr() * got.LC()) == 0
        note2 = f"degree {got.degree()} vs {want.degree()}"
    check("S2 POSITIVE: the eliminant matches the certified degree-5 "
          "polynomial up to a scalar", ok2, note2)

    bad = singular(vars_, gens, [f"{vars_[1]} - 7"], "w4Qsing_neg", 20000)
    check("S3 NEGATIVE: a contradictory pin collapses the ideal", 
          bad.get("dim") == "-1", f"dim {bad.get('dim')}")

    json.dump({"source": MS, "real": real, "pinned": bad,
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "artifacts", "edge_singular_Q.json"), "w"),
              indent=1)
    n = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {n}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if n == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
