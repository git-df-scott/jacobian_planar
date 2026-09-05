#!/usr/bin/env python3
"""Solve the triangular lex basis for explicit face points and VERIFY each.

The basis is triangular in (t9, t8, rest):  a quintic in t9, then t8^7 = h(t9),
then every other coordinate a polynomial in t8, t9.  With 7 not dividing p-1
the map x -> x^7 is a bijection of F_p*, so each root of the quintic gives
EXACTLY ONE F_p-rational point -- which is why the primes were chosen that way.

Every point is accepted only after 2 q t' - 3 q' t = u^2 is checked exactly.
"""
import json, re, sys
import sympy as sp
from face_solve_indep import face_system
from uz_indep import u

def parse(logfile, prime, unk):
    syms = {str(v): v for v in unk}
    rels = {}
    quintic = None
    for line in open(logfile):
        if not line.startswith("GL "):
            continue
        e = sp.sympify(line[3:].strip(), locals=syms)
        fs = sorted(e.free_symbols, key=str)
        if fs == [syms["t9"]]:
            quintic = e
        elif sp.degree(e, syms["t8"]) == 7:
            rels["t8"] = e
        else:
            lead = [v for v in fs if v not in (syms["t8"], syms["t9"])]
            if len(lead) == 1:
                rels[str(lead[0])] = e
    return quintic, rels

def main(prime, logfile):
    eqs, unk, coef, poly = face_system(prime, {"q1": 1, "q8": 1})
    quintic, rels = parse(logfile, prime, unk)
    t9, t8 = sp.Symbol("t9"), sp.Symbol("t8")
    co = [int(c) % prime for c in reversed(sp.Poly(quintic, t9).all_coeffs())]
    roots9 = [c for c in range(prime)
              if sum(a * pow(c, j, prime) for j, a in enumerate(co)) % prime == 0]
    print(f"quintic in t9 has {len(roots9)} roots in F_{prime}: {roots9}")
    e7 = pow(7, prime - 2, prime - 1) if (prime - 1) % 7 else None
    assert (prime - 1) % 7 != 0, "need 7 not dividing p-1 for a unique 7th root"
    inv7 = pow(7, -1, prime - 1)
    pts = []
    for r9 in roots9:
        h = sp.Poly(rels["t8"], t8).all_coeffs()
        rhs = (-int(sp.Poly(rels["t8"] - t8**7, t9).as_expr().subs(t9, r9))) % prime
        r8 = pow(rhs, inv7, prime)                       # unique 7th root
        assert pow(r8, 7, prime) == rhs % prime
        sol = {t9: r9, t8: r8}
        for name, rel in rels.items():
            if name == "t8":
                continue
            v = sp.Symbol(name)
            val = (-int(sp.expand(rel - v).subs(sol))) % prime
            sol[v] = val
        sol[sp.Symbol("q1")] = 1
        sol[sp.Symbol("q8")] = 1
        q = poly["q"].subs(sol); t = poly["t"].subs(sol)
        E = sp.expand(2*q*sp.diff(t, u) - 3*sp.diff(q, u)*t - u**2)
        P = sp.Poly(E, u) if E != 0 else None
        ok = (P is None) or all(int(c) % prime == 0 for c in P.coeffs())
        print(f"  cover t9={r9:5d}  t8={r8:5d}  -> "
              f"VERIFY 2qt'-3q't == u^2 : {ok}")
        if ok:
            pts.append({str(k): int(v) % prime for k, v in sol.items()})
    print(f"{len(pts)} of {len(roots9)} points VERIFIED exactly")
    if pts:
        json.dump(pts, open(f"facepts_verified_p{prime}.json", "w"), indent=1)
        print(f"wrote facepts_verified_p{prime}.json")
    return pts

if __name__ == "__main__":
    main(int(sys.argv[1]), sys.argv[2])
