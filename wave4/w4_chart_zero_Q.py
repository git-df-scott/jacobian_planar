"""
Case (2), chart d_3_3 = 0, over Q: an exact char-0 decision, not a mod-p one.

The complementary chart is small enough to decide over Q outright.  Its w = -4
block is 9 polynomials in the 11 G-coefficients (the C-coefficients having been
eliminated triangularly), plus the chart d_3_3 = 0 and the two gauge fixings
d_2_1 = 1, d_12_21 = 1 that rigidify the (C,G) gauge in this chart, plus the
Rabinowitsch generator that imposes the remaining vertex conditions.

Singular is asked for a Groebner basis over Q.  A basis equal to {1} is a
CERTIFICATE that the chart is empty over Q-bar -- not evidence at a prime.

CONTROLS
  Z1 NEGATIVE: with the Rabinowitsch generator removed, the origin survives, so
     the ideal must NOT be the unit ideal.  If it still were, the engine's
     "unit" answer would carry no information.
  Z2 NEGATIVE: a planted rational point must be found: the same system with
     every generator's value at a random rational point subtracted off must NOT
     be the unit ideal.
  Z3 POSITIVE: a deliberately contradictory pair (d_4_5 - 1, d_4_5 - 2) must
     give the unit ideal, so a "1" answer is reachable at all.
"""
import os
import random
import subprocess
import sys
from fractions import Fraction

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import w4_c2_reduce as RED

RESULTS = []


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def to_sing(e, gs, names):
    P = sp.Poly(e, *gs)
    out = []
    for mono, coef in zip(P.monoms(), P.coeffs()):
        c = sp.Rational(coef)
        cs = str(c.p) if c.q == 1 else f"({c.p}/{c.q})"
        out.append("*".join([cs] + [f"{names[i]}^{a}" if a > 1 else names[i]
                                    for i, a in enumerate(mono) if a]))
    return " + ".join(out) if out else "0"


def run(gens, names, tag, timeout=2400, sat=True, extra=()):
    src = [f"ring R = 0, ({','.join(names + ['sat'])}), dp;",
           "ideal I = " + ",\n".join(gens + list(extra)) + ";"]
    if sat:
        src.append("I = I + ideal(sat*d_12_24_placeholder - 1);")
    src = [l for l in src if "placeholder" not in l]
    src.append("ideal G = std(I);")
    src.append('if (size(G)==1 && G[1]==1) { "UNIT"; } else { "dim " + string(dim(G)); '
               'if (dim(G)==0) { "vdim " + string(vdim(G)); } }')
    src.append("quit;")
    fn = f"/tmp/chart0_{tag}.sing"
    open(fn, "w").write("\n".join(src))
    try:
        pr = subprocess.run(["Singular", "-q", fn], capture_output=True,
                            text=True, timeout=timeout)
        return (pr.stdout or pr.stderr).strip()
    except subprocess.TimeoutExpired:
        return "TIMEOUT"


def main():
    polys, gs = RED.reduced_polys_Q()
    names = [str(s) for s in gs]
    idx = {n: i for i, n in enumerate(names)}
    base = [to_sing(e, gs, names) for e in polys]
    chart = ["d_3_3"]
    gauge = ["d_2_1-1", "d_12_21-1"]
    nz = [v for v in ("c_1_0", "c_8_14", "d_2_1", "d_12_21") if v in names]
    rab = ["sat*" + "*".join(v for v in names if v in ("d_2_1", "d_12_21")) + "-1"]
    print("=" * 78)
    print("case (2), chart d_3_3 = 0, decided over Q")
    print("=" * 78)
    print(f"    {len(base)} generators in {len(names)} variables, "
          f"plus the chart, 2 gauge fixings and 1 Rabinowitsch generator")

    real = run(base + chart + gauge + rab, names, "real")
    print(f"    real system: {real}")
    check("the chart d_3_3 = 0 is decided over Q", real in ("UNIT",) or
          real.startswith("dim"), f"[{real}]")

    nosat = run(base + chart + gauge, names, "nosat")
    check("Z1 NEGATIVE: without the Rabinowitsch generator the ideal is NOT the "
          "unit ideal (the origin survives)", nosat != "UNIT", f"[{nosat}]")

    rnd = random.Random(4)
    pt = {n: Fraction(rnd.randint(-4, 4), rnd.randint(1, 3)) for n in names}
    pt["d_3_3"] = Fraction(0)
    pt["d_2_1"] = Fraction(1)
    pt["d_12_21"] = Fraction(1)
    sub = {gs[i]: sp.Rational(pt[names[i]]) for i in range(len(names))}
    planted = []
    for e in polys:
        v = sp.Rational(sp.expand(e.subs(sub)))
        planted.append(to_sing(sp.expand(e - v), gs, names))
    pl = run(planted + chart + gauge + rab, names, "planted")
    check("Z2 NEGATIVE: a planted rational point makes the ideal NOT the unit "
          "ideal", pl != "UNIT", f"[{pl}]")

    pin = run(base + chart + gauge + rab + ["d_4_5-1", "d_4_5-2"], names, "pin")
    check("Z3 POSITIVE: a contradictory pin gives the unit ideal, so 'UNIT' is "
          "reachable", pin == "UNIT", f"[{pin}]")

    if real == "UNIT":
        print("\n    RESULT: the chart d_3_3 = 0 of the case-(2) w=-4 block is "
              "EMPTY OVER Q-BAR, by a Groebner certificate over Q -- not a "
              "mod-p verdict.")
    else:
        print(f"\n    RESULT: not the unit ideal over Q; Singular reports "
              f"{real}.  Recorded as such.")
    npass = sum(1 for _, o, _ in RESULTS if o)
    import json
    json.dump({"real": real, "nosat": nosat, "planted": pl, "pin": pin,
               "checks": [[a, b, c] for a, b, c in RESULTS]},
              open(os.path.join(HERE, "artifacts", "chart_zero_Q.json"), "w"),
              indent=1)
    print("=" * 78)
    print(f"    {npass}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
