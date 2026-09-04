#!/usr/bin/env python3
"""Independent exact-Q controls for the Briancon mate strike.

The script verifies Gate 0 for the two published degree-ten submersions and
reconstructs the boundary calculation that makes their Gelfand--Leray form a
nonzero holomorphic differential on the cited genus-one fibre.  The genus and
irreducibility statements remain explicit theorem inputs; the script does not
pretend to re-prove them.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp


x, y, t = sp.symbols("x y t")
s, p = sp.symbols("s p")
a, b = sp.symbols("a b")


def original_polynomial(aa, bb):
    ss = x * y + 1
    pp = x * ss + 1
    uu = ss**2 + y
    polynomial = sp.expand(pp**2 * uu + aa * pp * ss + bb * ss)
    return ss, pp, uu, polynomial


def cleared_fibre(aa, bb, fibre_value=1):
    return sp.expand(
        s**2 * p**3
        + (aa - 1) * s * p**2
        + (bb - aa) * s * p
        - bb * s
        - fibre_value * p
        + fibre_value
    )


def certify_target(name: str, aa: sp.Rational, bb: sp.Rational) -> dict:
    ss, pp, uu, polynomial = original_polynomial(aa, bb)
    relation = sp.expand((pp - 1) * uu - ss * (ss * pp - 1))
    if relation != 0:
        raise AssertionError("Briancon chart relation failed")

    hxy = cleared_fibre(aa, bb).subs({s: ss, p: pp})
    if sp.expand(hxy - (pp - 1) * (polynomial - 1)) != 0:
        raise AssertionError("cleared fibre identity failed")
    jac_sp = sp.expand(sp.diff(ss, x) * sp.diff(pp, y) - sp.diff(ss, y) * sp.diff(pp, x))
    if sp.expand(jac_sp + pp - 1) != 0:
        raise AssertionError("chart Jacobian identity failed")

    # Gate 0: exact Groebner basis over Q, not a sampled critical-point test.
    gradient_basis = sp.groebner(
        [sp.diff(polynomial, x), sp.diff(polynomial, y)],
        x,
        y,
        domain=sp.QQ,
        order="lex",
        method="f5b",
    )
    if list(gradient_basis) != [1]:
        raise AssertionError(f"{name}: gradient ideal is not certified as (1)")

    # At p=infinity put q=1/p.  The lowest face is
    # L^2 + (a-1)L - 1, while the leading denominator is
    # (a-1)L - 2.  Their coprimality gives valuation zero on both branches.
    lam = sp.symbols("lam")
    tangent = lam**2 + (aa - 1) * lam - 1
    denominator = (aa - 1) * lam - 2
    tangent_discriminant = sp.discriminant(tangent, lam)
    if tangent_discriminant == 0:
        raise AssertionError("coincident p-infinity tangents")
    if sp.gcd(sp.Poly(tangent, lam, domain=sp.QQ), sp.Poly(lam, lam, domain=sp.QQ)).degree() != 0:
        raise AssertionError("zero p-infinity tangent")
    if sp.gcd(
        sp.Poly(tangent, lam, domain=sp.QQ),
        sp.Poly(denominator, lam, domain=sp.QQ),
    ).degree() != 0:
        raise AssertionError("leading Gelfand--Leray denominator vanishes")

    # At s=infinity, wt(p)=1 and wt(z)=3 gives p^3-b*z.  b != 0 gives
    # one smooth branch and valuation zero for eta.
    if bb == 0:
        raise AssertionError("the all-irreducible boundary stratum has degenerated")

    return {
        "name": name,
        "parameters": {"a": str(aa), "b": str(bb)},
        "degree": int(sp.Poly(polynomial, x, y).total_degree()),
        "gradient_groebner_basis": [str(g) for g in gradient_basis],
        "gradient_ideal": "(1)",
        "cleared_fibre_t1": str(cleared_fibre(aa, bb)),
        "chart_relation_verified": True,
        "cleared_fibre_identity_verified": True,
        "chart_jacobian_verified": True,
        "p_infinity": {
            "branches": 2,
            "tangent_polynomial": str(tangent),
            "discriminant": str(tangent_discriminant),
            "eta_valuations": [0, 0],
            "coprimality_verified": True,
        },
        "s_infinity": {
            "branches": 1,
            "initial_form": f"p^3 - ({bb})*z",
            "eta_valuation": 0,
        },
        "theorem_inputs": {
            "t1_compact_genus": 1,
            "fibres_irreducible": True,
            "source": "Dimca--Sticlaru, arXiv:2406.19795, Theorem 1.7 and Propositions 3.3--3.4",
        },
        "mate_verdict": "NO: nonzero holomorphic Gelfand--Leray differential",
        "evidence": "EXACT-Q plus stated theorem inputs",
    }


def family_control() -> dict:
    ss, pp, uu, polynomial = original_polynomial(a, b)
    symbolic_h = cleared_fibre(a, b, t)
    if sp.expand(symbolic_h.subs({s: ss, p: pp}) - (pp - 1) * (polynomial - t)) != 0:
        raise AssertionError("two-parameter family identity failed")
    boundary_member = sp.factor(polynomial.subs(b, 0))
    expected = sp.factor(pp * (pp * uu + a * ss))
    if sp.expand(boundary_member - expected) != 0:
        raise AssertionError("b=0 reducible-fibre factorization failed")
    return {
        "family": "P_(a,b)=p^2*u+a*p*s+b*s",
        "cleared_generic_fibre": str(symbolic_h),
        "b_nonzero_boundary_profile": {
            "p_infinity_branches": 2,
            "s_infinity_branches": 1,
            "necessary_exception_at_t1": "(a-1)^2+4=0",
        },
        "b_zero_factorization": "P_(a,0)=p*(p*u+a*s)",
        "b_zero_leaves_all_fibres_irreducible_class": True,
        "identity_verified": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = {
        "evidence_label": "EXACT-Q",
        "controls": [
            certify_target("g", sp.Rational(-5, 3), sp.Rational(-1, 3)),
            certify_target("gprime", sp.Rational(-7, 9), sp.Rational(1, 9)),
        ],
        "family_boundary": family_control(),
        "status": "PASS",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
