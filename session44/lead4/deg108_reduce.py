#!/usr/bin/env python3
"""Structured elimination on the (72,108) bracket systems.

The systems from deg108_direct are sparse: many equations are a single
monomial (forcing a coefficient to vanish) or are linear in one unknown
(determining it in terms of the others). Cascading those substitutions
shrinks the system exactly -- no approximation, no loss of solutions --
before any Groebner engine is involved. This is the classical hand method
GGHV used on the cases they closed, done mechanically.

Rules applied, repeatedly, until nothing changes:
  R1 monomial equation c * v^k = 0 with c a nonzero constant  ->  v = 0.
     (If v is a required-nonzero corner, the whole branch is contradictory
     and the system is EMPTY -- reported immediately.)
  R2 equation linear in some unknown v with a CONSTANT nonzero coefficient,
     i.e. e = a*v + b with a a nonzero number and v not in b
        ->  v = -b/a, substitute everywhere.
     A constant leading coefficient means no division by a possibly-zero
     quantity, so no branch is lost.
Anything needing division by a non-constant is left alone (that would
require case splitting, which is what the solver is for).

Reports the reduced system and writes it in msolve format.
"""
import argparse

import sympy as sp

import deg108_direct as DD


def reduce_system(eqs, unks, req, verbose=True):
    eqs = [sp.expand(e) for e in eqs]
    unks = list(unks)
    reqset = set(req)
    assign = {}
    changed = True
    rounds = 0
    while changed:
        changed = False
        rounds += 1
        # R1: monomial equations
        for e in list(eqs):
            if e == 0:
                continue
            terms = sp.Add.make_args(e)
            if len(terms) != 1:
                continue
            fs = terms[0].free_symbols
            if len(fs) != 1:
                continue
            v = fs.pop()
            if v in reqset:
                if verbose:
                    print(f"  CONTRADICTION: required corner {v} forced to 0")
                return None, None, None, "EMPTY (required corner forced zero)"
            assign[v] = sp.Integer(0)
            eqs = [sp.expand(q.subs({v: 0})) for q in eqs]
            eqs = [q for q in eqs if q != 0]
            if v in unks:
                unks.remove(v)
            changed = True
            break
        if changed:
            continue
        # R2: linear in one unknown with constant coefficient
        for e in list(eqs):
            if e == 0:
                continue
            done = False
            for v in sorted(e.free_symbols, key=str):
                if v not in unks:
                    continue
                pe = sp.Poly(e, v)
                if pe.degree() != 1:
                    continue
                a = pe.coeff_monomial(v)
                if not a.is_number or a == 0:
                    continue
                b = sp.expand(e - a * v)
                if v in b.free_symbols:
                    continue
                val = sp.expand(-b / a)
                assign[v] = val
                eqs = [sp.expand(q.subs({v: val})) for q in eqs]
                eqs = [q for q in eqs if q != 0]
                unks.remove(v)
                changed = True
                done = True
                break
            if done:
                break
    # a required corner that got assigned a nonzero constant is fine;
    # assigned zero is a contradiction
    for v, val in assign.items():
        if v in reqset and val == 0:
            return None, None, None, "EMPTY (required corner assigned zero)"
    if not eqs:
        return eqs, unks, assign, "NO EQUATIONS LEFT (unconstrained)"
    return eqs, unks, assign, "REDUCED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--subcase", type=int, default=2, choices=[1, 2])
    ap.add_argument("--char", type=int, default=65521)
    ap.add_argument("--normalize", default="a_1_0,a_8_16,b_12_24")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.subcase == 1:
        NP = [(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)]
        NQ = [(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)]
    else:
        NP = [(0, 0), (1, 0), (8, 14), (8, 16)]
        NQ = [(0, 0), (2, 1), (12, 21), (12, 24)]
    norm = tuple(s for s in a.normalize.split(",") if s)
    eqs, unks, req = DD.build(NP, NQ, 2, normalize=norm)
    print(f"before: {len(unks)} unknowns, {len(eqs)} equations")
    eqs2, unks2, assign, status = reduce_system(eqs, unks, req)
    print(f"status: {status}")
    if eqs2 is None:
        print("=> subcase decided EMPTY by elimination alone")
        return
    print(f"after:  {len(unks2)} unknowns, {len(eqs2)} equations, "
          f"{len(assign)} coefficients determined")
    if unks2:
        degs = sorted({sp.Poly(e, *unks2).total_degree() for e in eqs2})
        print(f"remaining equation degrees: {degs}")
    fn = a.out or f"deg108_sub{a.subcase}_reduced_p{a.char}.ms"
    txt = DD.to_msolve(eqs2, unks2, [r for r in req if r in unks2], a.char)
    with open(fn, "w") as f:
        f.write(txt)
    print(f"wrote {fn}")


if __name__ == "__main__":
    main()
