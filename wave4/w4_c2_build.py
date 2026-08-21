"""
wave4 / builder: msolve and Singular inputs for the case-(2) system.

Everything is generated from campaign/audit_tracks/trackA_system_case2.json via
w4_case2_system.py.  No downstream artifact (edgeQ_input.ms, the RUR, any prior
verdict) is read here.

Charts and controls
-------------------
The system carries a scaling gauge, so a chart on one G-coefficient is used.
Both charts are generated and both are run:

    chart "one"   d_3_3 - 1          (the chart every prior run used)
    chart "zero"  d_3_3              (the complementary chart, untested before)

Nonzero conditions from the JSON ("nonzero": the polygon-vertex coefficients
that must not vanish, or the Newton polygon degenerates) are imposed by the
Rabinowitsch trick: one extra variable `sat` and one extra equation
`sat * prod(nonzero) - 1`.

Controls generated alongside every real system:

    MUTANT   the 92 bracket equations have their value at a random admissible
             point xi subtracted off, so xi IS a solution.  A solver that
             reports EMPTY on this has failed, and the run is void.
    PIN      an explicitly contradictory pair c_1_0 - 1, c_1_0 - 2 is added.
             A solver that reports anything but EMPTY has failed.

Neither control shares code paths with the real system beyond this file, and
both are required to come back with the expected verdict before any real
verdict is reported.
"""

import os
import random
import sys
from fractions import Fraction

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import w4_case2_system as S

VARS, NONZERO, EQS, META, CHASH = S.load()
BYW = S.split_by_weight(EQS)


def _mono_str(m, star="*"):
    return star.join(v if e == 1 else f"{v}^{e}" for v in sorted(m) for e in [m[v]])


def poly_str(terms, p=None):
    """terms: [(Fraction, {var:exp})].  Coefficients reduced mod p when given."""
    out = []
    for c, m in terms:
        if p is not None:
            num = c.numerator % p
            den = pow(c.denominator % p, p - 2, p)
            cc = (num * den) % p
            if cc == 0:
                continue
            lead = str(cc)
        else:
            lead = str(c.numerator) if c.denominator == 1 else f"{c.numerator}/{c.denominator}"
        out.append(lead if not m else lead + "*" + _mono_str(m))
    return " + ".join(out) if out else "0"


def eval_terms(terms, pt, p):
    """Value of a term list at pt (dict var->int) in F_p."""
    tot = 0
    for c, m in terms:
        v = (c.numerator % p) * pow(c.denominator % p, p - 2, p) % p
        for var, e in m.items():
            v = v * pow(pt[var], e, p) % p
        tot = (tot + v) % p
    return tot % p


def random_point(p, seed, chart):
    """A random point with the chart honoured and every nonzero condition met."""
    rnd = random.Random(seed)
    pt = {}
    for v in VARS:
        while True:
            val = rnd.randrange(1, p) if v in NONZERO else rnd.randrange(0, p)
            if v not in NONZERO or val % p != 0:
                break
        pt[v] = val
    if chart == "one":
        pt["d_3_3"] = 1
    elif chart == "zero":
        pt["d_3_3"] = 0
    if "d_3_3" in NONZERO:
        raise SystemExit("d_3_3 is a nonzero condition: the chart split is ill-posed")
    return pt


def build_system(p, chart, variant="real", eq_idx=None, seed=0, extra_vars=(),
                 want_sat=True):
    """Return (varnames, [poly strings]) for msolve.

    variant: "real" | "mutant" | "pin"
    eq_idx : which equation indices to include (default: all 92)
    """
    idx = list(range(len(EQS))) if eq_idx is None else list(eq_idx)
    used = set()
    for k in idx:
        used |= S.eq_vars(EQS[k])
    used.add("d_3_3")
    used |= set(extra_vars)
    nz = [v for v in NONZERO if v in used]
    varlist = sorted(used) + (["sat"] if (want_sat and nz) else [])

    polys = []
    pt = random_point(p, seed, chart) if variant == "mutant" else None
    for k in idx:
        terms = S.eq_terms(EQS[k])
        s = poly_str(terms, p)
        if variant == "mutant":
            val = eval_terms(terms, pt, p)
            if val:
                s = f"{s} + {(-val) % p}"
        polys.append(s)
    if chart == "one":
        polys.append("d_3_3 + " + str((-1) % p))
    elif chart == "zero":
        polys.append("d_3_3")
    elif chart is not None:
        raise SystemExit(f"unknown chart {chart!r}")
    if want_sat and nz:
        polys.append("sat*" + "*".join(nz) + " + " + str((-1) % p))
    if variant == "pin":
        polys.append("c_1_0 + " + str((-1) % p))
        polys.append("c_1_0 + " + str((-2) % p))
    return varlist, polys, pt


def write_ms(path, p, varlist, polys):
    with open(path, "w") as f:
        f.write(",".join(varlist) + "\n")
        f.write(f"{p}\n")
        f.write(",\n".join(polys) + "\n")
    return path
