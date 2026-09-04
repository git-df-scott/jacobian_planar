"""
wave4 / shared module: the case-(2) system, parsed from its primary artifact.

Source of truth: campaign/audit_tracks/trackA_system_case2.json --- the JSON
derived from GGHV arXiv:2204.14178 Prop 4.3, case (2), for the degree pair
(72,108) via the (8,28) polygon pair.  Nothing here reads edgeQ_input.ms or any
other downstream file: this module rebuilds the system from the JSON so that
every wave-4 verdict rests on the JSON alone.

The JSON encodes each equation as

    {"bracket_point": [i, j],
     "terms": [ [ [[var, exponent], ...], [num, den] ], ... ] }

meaning  sum_terms (num/den) * prod var^exponent = 0, the coefficient of
x^i y^j in the Poisson bracket [P, Q] - x^2.

This module exposes:

    load()          -> (variables, nonzero, equations, meta)
    weight(i, j)    -> j - 2i, the grading in which P and Q are quasi-homogeneous
    to_string(eq)   -> a plain-text polynomial in the JSON's own variable names

and is import-only: it makes no claims and prints nothing when imported.  Its
own self-test lives in w4_case2_selftest.py, which carries the negative
controls.
"""

import json
import os
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JSON_PATH = os.path.join(ROOT, "campaign", "audit_tracks", "trackA_system_case2.json")


def load(path=JSON_PATH):
    with open(path) as f:
        d = json.load(f)
    return d["variables"], d["nonzero"], d["equations"], d["meta"], d.get("content_hash")


def weight(i, j):
    """The w = j - 2i grading.  P has weights 0,-1,-2; Q has 0,-1,-2,-3."""
    return j - 2 * i


def var_weight(name):
    """Weight of a coefficient variable c_i_j / d_i_j."""
    _, i, j = name.split("_")
    return weight(int(i), int(j))


def eq_terms(eq):
    """[(Fraction coeff, {var: exponent}), ...] for one JSON equation."""
    out = []
    for mono, coef in eq["terms"]:
        c = Fraction(int(coef[0]), int(coef[1]))
        m = {}
        for v, e in mono:
            m[v] = m.get(v, 0) + int(e)
        out.append((c, m))
    return out


def eq_vars(eq):
    s = set()
    for _, m in eq_terms(eq):
        s.update(m)
    return s


def to_string(eq, subs=None, star="*"):
    """Plain text 'a*b + -3*c^2 + ...' in the JSON's variable names.

    `subs` maps a variable name to a replacement STRING (already parenthesised
    by the caller if it is not atomic).
    """
    subs = subs or {}
    pieces = []
    for c, m in eq_terms(eq):
        factors = []
        num, den = c.numerator, c.denominator
        lead = str(num) if den == 1 else f"{num}/{den}"
        factors.append(lead)
        for v in sorted(m):
            rep = subs.get(v, v)
            factors.append(rep if m[v] == 1 else f"{rep}^{m[v]}")
        pieces.append(star.join(factors))
    return " + ".join(pieces) if pieces else "0"


def split_by_weight(equations):
    """Group equation indices by the weight of their bracket point."""
    byw = {}
    for k, eq in enumerate(equations):
        i, j = eq["bracket_point"]
        byw.setdefault(weight(i, j), []).append(k)
    return byw


# The four quasi-homogeneous pieces, by weight.
#   P = A(t) + B(t)/y + C(t)/y^2          weights  0, -1, -2
#   Q = D(t) + E(t)/y + F(t)/y^2 + G(t)/y^3   weights  0, -1, -2, -3
def piece(variables, letter, w):
    pref = "c" if letter in "ABC" else "d"
    return [v for v in variables if v.startswith(pref + "_") and var_weight(v) == w]
