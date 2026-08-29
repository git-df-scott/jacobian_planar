#!/usr/bin/env python3
"""Build exact factor/coordinate certificates for eigensearch21.json.

This one-time certificate generator requires SymPy. Its output is checked by
verify_eigenfactor21.py, which uses only the standard library and expands every
displayed product or mate independently.
"""

import json
import os
import re

try:
    import sympy as sp
except ImportError:
    raise SystemExit("generator requires SymPy; verifier has no dependency")

HERE = os.path.dirname(os.path.abspath(__file__))
x, y = sp.symbols("x y")
TERM = re.compile(r"\(([-()0-9/]+)\)\*x\^(\d+)\*y\^(\d+)")


def parse(s):
    z = 0
    for a, i, j in TERM.findall(s):
        z += sp.Rational(a.replace("(", "").replace(")", ""))*x**int(i)*y**int(j)
    return sp.Poly(z, x, y, domain=sp.QQ)


def qpair(a):
    a = sp.Rational(a)
    return [int(a.p), int(a.q)]


def pdict(f):
    f = sp.Poly(f, x, y, domain=sp.QQ)
    return {"%d,%d" % m: qpair(a) for m, a in f.terms()}


def main():
    with open(os.path.join(HERE, "eigensearch21.json")) as f:
        raw = json.load(f)
    unique = {}
    for row in raw["rows"]:
        unique.setdefault(row["P"], row)
    records = []
    nr = nt = 0
    for s in unique:
        P = parse(s)
        coeff, factors = sp.factor_list(P.as_expr(), x, y)
        # factor_list represents an irreducible polynomial by [(P, 1)].
        # A genuine nontrivial factorization has at least two factors counted
        # with multiplicity.
        if sum(e for _, e in factors) >= 2:
            nr += 1
            records.append({
                "class": "reducible_Q",
                "P": pdict(P),
                "constant": qpair(coeff),
                "factors": [{"exp": int(e), "poly": pdict(f)} for f, e in factors],
            })
            continue
        px = sp.Poly(P.as_expr(), x)
        py = sp.Poly(P.as_expr(), y)
        if px.degree() == 1 and not (px.LC().has(x) or px.LC().has(y)):
            a = sp.Rational(px.LC())
            Q = sp.Poly(y/a, x, y, domain=sp.QQ)
            axis = "x"
        elif py.degree() == 1 and not (py.LC().has(x) or py.LC().has(y)):
            a = sp.Rational(py.LC())
            Q = sp.Poly(-x/a, x, y, domain=sp.QQ)
            axis = "y"
        else:
            raise RuntimeError("unclassified factor-free polynomial: " + s)
        nt += 1
        records.append({"class": "triangular_coordinate", "axis": axis,
                        "P": pdict(P), "Q": pdict(Q)})
    out = {
        "source_rows": len(raw["rows"]),
        "unique_P": len(unique),
        "reducible_Q_with_factor_witness": nr,
        "triangular_coordinates_with_mate": nt,
        "unclassified": 0,
        "records": records,
    }
    with open(os.path.join(HERE, "eigenfactor21.json"), "w") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    print({k: v for k, v in out.items() if k != "records"})


if __name__ == "__main__":
    main()
