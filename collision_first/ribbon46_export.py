#!/usr/bin/env python3
"""Export the exact reduced (4,6) collision system to Singular syntax.

`--scale 21` is the live degree-(84,126) frontier.  Smaller scales are useful
for planted controls and solver-pipeline tests.  The P collision is imposed
identically.  Both Q collision values and one explicit vertex saturation row
are exported; consequently a solver point is already an original-coordinate
collision candidate (but still requires characteristic-zero lifting/replay).
"""
from __future__ import annotations

import argparse
from pathlib import Path

import sympy as sp

from ribbon46_reduction import A, c, dp, p, q, survivors


def polynomial(prefix, degree, x):
    coefficients = sp.symbols(f"{prefix}0:{degree+1}")
    return sum(coefficients[i]*x**i for i in range(degree+1)), list(coefficients)


def build(scale):
    x = sp.Symbol("x")
    degrees = [4*scale, 3*scale, 2*scale, scale]

    # p0(0)=p0(1)=0 identically: omit its constant and solve its top
    # coefficient as minus the sum of the remaining bottom coefficients.
    bottom_free = list(sp.symbols(f"p0_1:{degrees[0]}"))
    bottom_top = -sum(bottom_free)
    rows = [sum(bottom_free[i-1]*x**i for i in range(1, degrees[0]))
            + bottom_top*x**degrees[0]]
    variables = bottom_free[:]
    for index, degree in enumerate(degrees[1:], 1):
        row, coefficients = polynomial(f"p{index}_", degree, x)
        rows.append(row)
        variables.extend(coefficients)

    substitution = {p[i]: rows[i] for i in range(4)}
    substitution.update({dp[i]: sp.diff(rows[i], x) for i in range(4)})
    equations = []
    expected = {}
    for degree, target in ((2, 0), (1, 0), (0, 1)):
        expression = sp.together(survivors[degree].subs(substitution)-target)
        poly = sp.Poly(expression, x)
        coefficients = [sp.factor(poly.coeff_monomial(x**i))
                        for i in range(9*scale-3*degree+1)]
        equations.extend(coefficients)
        expected[degree] = len(coefficients)

    q0 = sp.together(q[0].subs(substitution))
    equations.extend([q0.subs(x, 0), q0.subs(x, 1)])
    lead_q0 = sp.Poly(q0, x).coeff_monomial(x**(6*scale))
    saturation = sp.Symbol("sat")
    equations.append(saturation*bottom_top*c*lead_q0-1)
    variables.extend(A)
    variables.extend([c, saturation])
    return variables, equations, expected


def singular(expression):
    numerator = sp.together(expression).as_numer_denom()[0]
    return str(sp.expand(numerator)).replace("**", "^").replace(" ", "")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--scale", type=int, default=1)
    parser.add_argument("--prime", type=int, default=1000003)
    parser.add_argument("--output", type=Path,
                        default=Path("collision_first/ribbon46_p1000003.sing"))
    ns = parser.parse_args()
    if ns.scale < 1:
        raise ValueError("scale must be positive")
    if ns.scale > 4:
        raise ValueError(
            "dense coefficient export is intentionally capped at scale 4; "
            "the live scale-21 system must use an evaluation/straight-line "
            "representation to avoid expansion blow-up"
        )
    variables, equations, counts = build(ns.scale)
    names = ",".join(map(str, variables))
    body = ",\n".join(singular(equation) for equation in equations)
    program = (f"option(redSB);\nring r={ns.prime},({names}),dp;\n"
               f"ideal I=\n{body};\n"
               "print(size(I));\nideal G=std(I);\nprint(G);\n")
    ns.output.write_text(program)
    print("COLLISION RIBBON (4,6) EXPORT: PASS")
    print(f"scale={ns.scale} variables={len(variables)} equations={len(equations)}")
    print(f"Jacobian rows={counts}; plus two Q collisions and one saturation")
    print(ns.output)


if __name__ == "__main__":
    main()
