"""
T3 -- mu_n-equivariant slices of the case-(2) quadrilateral system.

THE ANSATZ
----------
Let zeta be a primitive n-th root of unity and impose

        P(zeta^a x, zeta^b y) = zeta^p P(x,y),
        Q(zeta^a x, zeta^b y) = zeta^q Q(x,y).

Then a coefficient c_i_j survives iff a*i + b*j = p (mod n), and d_i_j survives
iff a*i + b*j = q (mod n).  The brief fixes a = 1; this module sweeps a as well,
so the enumeration is over all (a, b, p, q) mod n with gcd(a, b, n) = 1 (a
faithful action).  a = 1 is included and is reported separately.

THE COMPATIBILITY CONDITION, DERIVED HERE, NOT IMPORTED
-------------------------------------------------------
Differentiating the two displays gives
        P_x(zeta^a x, zeta^b y) = zeta^(p-a) P_x, etc.,
so  [P,Q](zeta^a x, zeta^b y) = zeta^(p+q-a-b) [P,Q].  The case-(2) system of
campaign/audit_tracks/trackA_system_case2.json has bracket right-hand side x^2
(its meta records bracket_rhs = "x^2"), and (zeta^a x)^2 = zeta^(2a) x^2, so the
compatibility condition is

        p + q = 3a + b   (mod n).

(The brief's "p + q = 1 + b (mod n)" is the condition for [P,Q] a nonzero
CONSTANT; with the x^2 right-hand side of these reduced coordinates the correct
condition is the one above.  Both are enumerated below and labelled, so the
difference is visible rather than assumed away.)

Nothing is asserted about which slices are empty: for every (n,a,b,p,q) the
module builds the restricted system mechanically and hands it to msolve.
Degeneracies -- a killed vertex coefficient, or a killed x^2 equation -- are
DETECTED from the restricted system, not predicted.

CONTROLS
--------
  n = 1  must reproduce the unrestricted system exactly (same variable count,
         same equation count, same msolve verdict as the unrestricted run).
  MUTANT for every slice actually handed to msolve.
  PIN    for every slice actually handed to msolve.
"""

import itertools
import json
import os
import sys
from math import gcd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "wave4"))
import w4_case2_system as S
import w4_c2_build as B
import w4_run as RUN

VARS, NONZERO, EQS, META, CHASH = S.load()


def ij(v):
    _, i, j = v.split("_")
    return int(i), int(j)


def surviving(n, a, b, p, q):
    keep = set()
    for v in VARS:
        i, j = ij(v)
        r = (a * i + b * j) % n
        if v.startswith("c_") and r == p % n:
            keep.add(v)
        if v.startswith("d_") and r == q % n:
            keep.add(v)
    return keep


def restrict(n, a, b, p, q):
    """Return (keep, eqs_kept, degeneracies)."""
    keep = surviving(n, a, b, p, q)
    deg = []
    for v in NONZERO:
        if v not in keep:
            deg.append(f"nonzero condition {v} is killed by the ansatz")
    # the x^2 equation is the one carrying a constant term
    for k, eq in enumerate(EQS):
        terms = S.eq_terms(eq)
        const = sum(c for c, m in terms if not m)
        alive = [(c, m) for c, m in terms if m and all(v in keep for v in m)]
        if const != 0 and not alive:
            deg.append(f"equation {k} at bracket point {eq['bracket_point']} "
                       f"reduces to {const} = 0")
    eqs = []
    for k, eq in enumerate(EQS):
        terms = S.eq_terms(eq)
        alive = [(c, m) for c, m in terms if not m or all(v in keep for v in m)]
        if alive:
            eqs.append((k, alive))
    return keep, eqs, deg


def write_ms(path, p_char, keep, eqs, chart, gauge, variant="real", seed=0,
             saturate=True):
    import random
    names = sorted(keep)
    nz = [v for v in NONZERO if v in keep]
    rnd = random.Random(seed)
    pt = None
    if variant == "mutant":
        pt = {v: rnd.randrange(1, p_char) for v in names}
        for v, val in list(gauge) + ([("d_3_3", 1 if chart == "one" else 0)]
                                     if "d_3_3" in keep else []):
            if v in pt:
                pt[v] = val
    lines = []
    for k, alive in eqs:
        s = B.poly_str(alive, p_char)
        if pt is not None:
            val = B.eval_terms(alive, {**{v: 0 for v in VARS}, **pt}, p_char)
            if val:
                s = s + " + " + str((-val) % p_char)
        lines.append(s)
    if "d_3_3" in keep:
        lines.append("d_3_3 + " + str((-1) % p_char) if chart == "one" else "d_3_3")
    for v, val in gauge:
        if v in keep:
            lines.append(f"{v} + {(-val) % p_char}")
    if nz and saturate:
        lines.append("sat*" + "*".join(nz) + " + " + str((-1) % p_char))
        names = names + ["sat"]
    if variant == "pin":
        v0 = sorted(keep)[0]
        lines += [f"{v0} + {(-1) % p_char}", f"{v0} + {(-2) % p_char}"]
    with open(path, "w") as f:
        f.write(",".join(names) + "\n")
        f.write(f"{p_char}\n")
        f.write(",\n".join(lines) + "\n")
    return path, len(names), len(lines), pt
