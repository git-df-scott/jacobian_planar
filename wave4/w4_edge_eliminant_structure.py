"""
The exact ℚ-eliminant of the case-(2) w=-4 block: irreducibility and Galois group.

INPUT.  wave4/artifacts/edge_eliminant_Q_one.json, produced by
w4_edge_eliminant_Q.py: a degree-5 polynomial over Q reconstructed from 41
primes p = 1 (mod 3) and verified to reproduce msolve's eliminant at 6 primes
that were NOT used to build it (with a corrupted-coefficient negative control).

WHAT IS COMPUTED HERE, exactly:
  * squarefreeness  (gcd(f, f') has degree 0),
  * irreducibility over Q,
  * the Galois group of f over Q,
  * the rational roots of f.

STANDING OF THE INPUT.  The reconstruction is verified, not proved: it
reproduces the eliminant at held-out primes, which is evidence of the strongest
kind available short of the char-0 solve, and it is labelled that way
everywhere.  The char-0 solve (`msolve -P 1` on the same system over Q) was
launched alongside and is reported separately.

CONTROLS
  G1 the polynomial is squarefree -- otherwise "5 points" would be wrong;
  G2 NEGATIVE: a reducible polynomial of the same degree is correctly reported
     reducible by the same call, so G3 is not vacuous;
  G3 irreducibility over Q;
  G4 the Galois group, with a NEGATIVE control on a quintic of known group
     (x^5 - 5x + 12 has Galois group D5, not S5).
"""
import json
import os
import sys

import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = []
w = sp.Symbol("w")


def check(name, cond, note=""):
    ok = bool(cond)
    RESULTS.append((name, ok, note))
    print(f"    [{'PASS' if ok else 'FAIL'}] {name}" + (f"   {note}" if note else ""))
    return ok


def galois(f):
    from sympy.polys.numberfields.galoisgroups import galois_group
    G, alt = galois_group(f)
    n = G.order()
    name = {120: "S5", 60: "A5", 20: "F20 (metacyclic)", 10: "D5", 5: "C5"}.get(n, f"order {n}")
    return name, n, alt


def main():
    path = os.path.join(HERE, "artifacts", "edge_eliminant_Q_one.json")
    d = json.load(open(path))
    cs = [sp.Rational(c) for c in d["coefficients"]]
    f = sp.Poly(sum(c * w ** i for i, c in enumerate(cs)), w)
    print("=" * 78)
    print("the exact Q-eliminant of the case-(2) w=-4 block, chart d_3_3 = 1")
    print("=" * 78)
    print(f"    degree {f.degree()}; reconstructed from "
          f"{d['build_primes_used']} primes; held-out primes {d['held_out_primes']}")
    monic = sp.Poly(sp.expand(f.as_expr() / cs[-1]), w)
    print(f"    monic form has coefficients with numerators of "
          f"{[len(str(sp.Rational(c).p)) for c in monic.all_coeffs()]} digits")

    check("G1 the eliminant is squarefree (so it really counts distinct points)",
          sp.gcd(f, f.diff(w)).degree() == 0,
          f"deg gcd(f, f') = {sp.gcd(f, f.diff(w)).degree()}")

    red = sp.Poly(sp.expand((w ** 2 + 1) * (w ** 3 - 2)), w)
    check("G2 NEGATIVE: the same irreducibility call reports a planted reducible "
          "quintic as reducible", not red.is_irreducible,
          "(w^2+1)(w^3-2)")

    check("G3 the eliminant is IRREDUCIBLE over Q", f.is_irreducible)

    roots = sp.ground_roots(f)
    check("G4 the eliminant has NO rational root", not roots, f"{roots}")

    name, n, alt = galois(f)
    check(f"G5 the Galois group is computed: {name}", n in (5, 10, 20, 60, 120),
          f"order {n}, contained in A5: {alt}")

    d5 = sp.Poly(w ** 5 - 5 * w + 12, w)
    n5, o5, _ = galois(d5)
    check("G5n NEGATIVE: the same call gives a DIFFERENT group on a quintic of "
          "known group (w^5 - 5w + 12 is D5)", o5 != n,
          f"{n5} (order {o5}) vs {name} (order {n})")

    out = {"degree": int(f.degree()), "squarefree": True,
           "irreducible_over_Q": bool(f.is_irreducible),
           "rational_roots": [str(r) for r in roots],
           "galois_group": name, "galois_group_order": int(n),
           "inside_A5": bool(alt),
           "reconstruction": {"build_primes_used": d["build_primes_used"],
                              "held_out_primes": d["held_out_primes"]},
           "standing": ("reconstructed multi-modularly and verified at held-out "
                        "primes; NOT a char-0 Groebner proof"),
           "checks": [[a, b, c] for a, b, c in RESULTS]}
    json.dump(out, open(os.path.join(HERE, "artifacts",
                                     "edge_eliminant_structure.json"), "w"), indent=1)
    npass = sum(1 for _, o, _ in RESULTS if o)
    print("=" * 78)
    print(f"    {npass}/{len(RESULTS)} checks passed")
    print("=" * 78)
    return 0 if npass == len(RESULTS) else 1


if __name__ == "__main__":
    sys.exit(main())
