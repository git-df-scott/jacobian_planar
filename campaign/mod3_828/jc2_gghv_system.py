"""
jc2_gghv_system.py
===================

Symbolic (exact, sympy, no floats) constructor for the "naive" Newton-polygon
coefficient-matching polynomial system implied by

    Guccione, Guccione, Horruitiner, Valqui,
    "Increasing the degree of a possible counterexample to the Jacobian
    Conjecture from 100 to 108", arXiv:2204.14178 ("GGHV22"),
    Proposition 4.3 ("Case (8,28)") -- the OPEN sub-case of the last live
    case (deg P, deg Q) = (72,108) of the plane Jacobian Conjecture.

READ jc2_gghv_system.md FIRST. Short version of what this file is and is not:

  * GGHV22 gives, for the open case, ONLY a Newton polygon shape for a
    reduced pair (P,Q) in L^(1) = K[x,x^-1,y] and the exact bracket value
    [P,Q] = x^2 (Proposition 4.3, two sub-cases). It does NOT give the
    further-reduced, tractable ("Section-5-style") system that it gives for
    the sibling closed case (9,27) -- that reduction (a bespoke recursive
    power-series construction, a differential equation, a CAS elimination,
    and a degree-counting contradiction spanning GGHV22 Section 5) has no
    published analogue for (8,28). See jc2_gghv_system.md Sections 4 and 6
    for exactly what is missing and why it is not reproduced here.

  * What THIS file builds instead is the mechanical, unambiguous system you
    get by taking Proposition 4.3's data at face value: P (resp. Q) is a
    generic polynomial supported on the lattice points of the stated Newton
    polygon (one unknown coefficient per lattice point -- vertices, edge
    points, and interior points alike), and [P,Q] = P_x Q_y - P_y Q_x = x^2
    is imposed as a polynomial identity, i.e. one equation per monomial that
    can appear on either side. This is called the NAIVE system throughout,
    precisely to distinguish it from the (unreconstructed) reduced system
    GGHV22 actually means by "the corresponding system of polynomial
    equations". Emptiness of the naive system (both sub-cases, with the
    corner/vertex coefficients forced nonzero) is logically sufficient to
    close the open case -- see jc2_gghv_system.md Section 9 -- but the naive
    system is far larger (72 or 186 unknowns) than the O(10)-unknown system
    the reduced approach would produce, and is not expected to be tractable
    by a generic Groebner run; see jc2_gghv_system.md Section 5.5.

  * This script only CONSTRUCTS systems and reports their size. It never
    attempts to solve/Groebner anything.

Validation performed by this script (run it directly, `python3
jc2_gghv_system.py`):
  1. A hand-verifiable linear (degree-1) sanity check: for P = p00 + p10 x +
     p01 y, Q = q00 + q10 x + q01 y (Newton polygon = unit triangle for
     both) and target bracket = 1, the single equation the constructor
     produces must be exactly p10*q01 - p01*q10 - 1 = 0, i.e. the classical
     "determinant of the linear part is 1" condition. Checked by exact
     symbolic comparison, not just by eye.
  2. Every Newton polygon used below (Proposition 4.3's two open sub-cases,
     plus Proposition 4.1's closed (9,27) sub-case used as a size
     comparator) is checked to be genuinely convex: the convex hull of the
     listed vertices must equal the listed vertex set exactly (no vertex is
     redundant / interior to the others). This both validates the
     transcription from the PDF and is the check that would have caught the
     Theorem 6.1 transposition typo noted in jc2_gghv_system.md's Appendix
     (that shape is intentionally NOT included below, since it plays no
     role in the open case).
  3. Lattice-point counts (= number of unknowns for each of P, Q) are
     computed two independent ways -- direct enumeration inside the convex
     hull, and Pick's theorem (Area = I + B/2 - 1) -- and must agree exactly
     for every polygon.

Requires: sympy only.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from math import gcd
from typing import Dict, List, Sequence, Tuple

import sympy as sp

Point = Tuple[int, int]


# ---------------------------------------------------------------------------
# Geometry: convex hulls, lattice-point enumeration, Pick's theorem
# ---------------------------------------------------------------------------

def convex_hull(points: Sequence[Point]) -> List[Point]:
    """Monotone-chain convex hull, returned in CCW order, no collinear
    duplicates on an edge (standard algorithm; exact integer arithmetic)."""
    pts = sorted(set(points))
    if len(pts) <= 2:
        return pts

    def cross(o: Point, a: Point, b: Point) -> int:
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower: List[Point] = []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    upper: List[Point] = []
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]


def _point_in_convex_hull(hull_ccw: Sequence[Point], pt: Point) -> bool:
    """True iff pt is inside or on the boundary of the CCW convex polygon."""
    n = len(hull_ccw)
    for i in range(n):
        x1, y1 = hull_ccw[i]
        x2, y2 = hull_ccw[(i + 1) % n]
        cx = (x2 - x1) * (pt[1] - y1) - (y2 - y1) * (pt[0] - x1)
        if cx < 0:
            return False
    return True


def lattice_points(vertices: Sequence[Point]) -> Tuple[List[Point], List[Point]]:
    """Return (sorted list of ALL lattice points in conv(vertices)), hull)."""
    hull = convex_hull(vertices)
    xs = [p[0] for p in hull]
    ys = [p[1] for p in hull]
    pts = [
        (i, j)
        for i in range(min(xs), max(xs) + 1)
        for j in range(min(ys), max(ys) + 1)
        if _point_in_convex_hull(hull, (i, j))
    ]
    return sorted(pts), hull


def pick_lattice_count(vertices: Sequence[Point]) -> Fraction:
    """Total lattice points (interior + boundary) via Pick's theorem, as an
    independent cross-check on lattice_points() above."""
    hull = convex_hull(vertices)
    n = len(hull)
    area2 = 0
    boundary = 0
    for i in range(n):
        x1, y1 = hull[i]
        x2, y2 = hull[(i + 1) % n]
        area2 += x1 * y2 - x2 * y1
        boundary += gcd(abs(x2 - x1), abs(y2 - y1))
    area2 = abs(area2)
    interior = Fraction(area2, 2) - Fraction(boundary, 2) + 1
    return interior + boundary


def assert_valid_newton_polygon(name: str, vertices: Sequence[Point]) -> None:
    """Raise if `vertices` (as transcribed from the paper) is not itself a
    genuinely convex vertex set -- i.e. catches typos/mistranscriptions."""
    hull = convex_hull(vertices)
    if set(hull) != set(vertices):
        raise ValueError(
            f"{name}: listed vertices {sorted(vertices)} are NOT all extreme "
            f"points of their own convex hull (hull = {sorted(hull)}). "
            f"This is exactly the failure mode found in GGHV22 Theorem 6.1 "
            f"(see jc2_gghv_system.md Appendix) -- re-check the transcription."
        )


# ---------------------------------------------------------------------------
# Symbolic system construction
# ---------------------------------------------------------------------------

def build_symbols(prefix: str, points: Sequence[Point]) -> Dict[Point, sp.Symbol]:
    return {pt: sp.Symbol(f"{prefix}_{pt[0]}_{pt[1]}") for pt in points}


def bracket_system(
    p_points: Sequence[Point],
    p_syms: Dict[Point, sp.Symbol],
    q_points: Sequence[Point],
    q_syms: Dict[Point, sp.Symbol],
    rhs: Dict[Point, sp.Expr],
) -> Dict[Point, sp.Expr]:
    """
    Build, monomial by monomial, the coefficients of

        P_x Q_y - P_y Q_x - RHS

    where P = sum_{(i,j) in p_points} p_syms[i,j] x^i y^j, similarly Q, and
    RHS = sum_{(i,j)} rhs[i,j] x^i y^j (e.g. {(2,0): 1} for x^2).

    Returns {monomial: expression} for every monomial with a nonzero
    (symbolic) coefficient; "the system" is {expr == 0 for expr in result}.

    Implemented as a direct convolution (dict of lists of terms, one
    sp.Add per monomial at the end) rather than sympy expand() on the full
    bivariate polynomials, purely for speed -- this scales to hundreds of
    lattice points where naive symbolic expand() would not. The maths is
    elementary: d/dx(x^i y^j) = i x^(i-1) y^j, etc.
    """
    acc: Dict[Point, List[sp.Expr]] = defaultdict(list)

    # + P_x * Q_y
    for (i, j), c in p_syms.items():
        if i == 0:
            continue
        for (k, l), d in q_syms.items():
            if l == 0:
                continue
            acc[(i - 1 + k, j + l - 1)].append(i * l * c * d)

    # - P_y * Q_x
    for (i, j), c in p_syms.items():
        if j == 0:
            continue
        for (k, l), d in q_syms.items():
            if k == 0:
                continue
            acc[(i + k - 1, j - 1 + l)].append(-j * k * c * d)

    # - RHS
    for key, v in rhs.items():
        acc[key].append(-v)

    eqs: Dict[Point, sp.Expr] = {}
    for key, terms in acc.items():
        expr = sp.Add(*terms)
        if expr != 0:
            eqs[key] = sp.expand(expr)
    return eqs


def nonzero_side_conditions(vertices: Sequence[Point], syms: Dict[Point, sp.Symbol]) -> List[sp.Symbol]:
    """The coefficients that MUST be nonzero for the polygon to genuinely
    have these vertices (Newton polygon = convex hull of the support, so a
    vertex of the hull must carry a nonzero coefficient). Interior/edge
    lattice points carry no such requirement from the proposition alone."""
    hull = convex_hull(vertices)
    return [syms[v] for v in hull]


def to_singular(
    eqs: Dict[Point, sp.Expr],
    all_symbols: Sequence[sp.Symbol],
    ring_name: str = "r",
    ideal_name: str = "I",
    char: int = 0,
) -> str:
    """Emit a Singular `ring`/`ideal` block for this system. Variable order
    is whatever `all_symbols` is given in; Singular needs a fixed, finite
    variable list. No solving/std() call is emitted -- construction only."""
    var_list = ",".join(str(s) for s in all_symbols)
    lines = [f"ring {ring_name} = {char},({var_list}),dp;", f"ideal {ideal_name} ="]
    gens = [sp.printing.sstr(e).replace("**", "^") for e in eqs.values()]
    lines.append("    " + ",\n    ".join(gens) + ";")
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Data: exact Newton polygons transcribed from GGHV22 (verbatim, see .md)
# ---------------------------------------------------------------------------

# --- OPEN case: Proposition 4.3 ("Case (8,28)"), [P,Q] = x^2 ---
OPEN_CASE_1 = dict(
    label="open case (1)  [Prop 4.3, sub-case 1; with y-axis edge]",
    P=[(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)],
    Q=[(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)],
    rhs={(2, 0): sp.Integer(1)},  # x^2
)
OPEN_CASE_2 = dict(
    label="open case (2)  [Prop 4.3, sub-case 2; no y-axis edge]",
    P=[(0, 0), (1, 0), (8, 14), (8, 16)],
    Q=[(0, 0), (2, 1), (12, 21), (12, 24)],
    rhs={(2, 0): sp.Integer(1)},  # x^2
)

# --- CLOSED sibling, used only as a size/scale comparator and to validate
#     the constructor on paper data other than the open case:
#     Proposition 4.1 ("Case (9,27)"), [P,Q] = x  ---
CLOSED_927 = dict(
    label="closed case (9,27)  [Prop 4.1; SOLVED in GGHV22 Sec.5 -- naive "
    "system shown here for SIZE COMPARISON ONLY, GGHV22 does not solve "
    "this naive system either, it solves a much-reduced one, see .md Sec.4]",
    P=[(0, 0), (1, 1), (6, 16), (6, 18), (0, 18)],
    Q=[(0, 0), (1, 0), (9, 24), (9, 27), (0, 27)],
    rhs={(1, 0): sp.Integer(1)},  # x
)

ALL_CASES = [OPEN_CASE_1, OPEN_CASE_2, CLOSED_927]


# ---------------------------------------------------------------------------
# Driver
# ---------------------------------------------------------------------------

def _linear_sanity_check() -> None:
    print("=" * 78)
    print("VALIDATION 1: linear (degree-1) hand-verifiable sanity check")
    print("=" * 78)
    unit_triangle = [(0, 0), (1, 0), (0, 1)]
    p_pts, _ = lattice_points(unit_triangle)
    q_pts, _ = lattice_points(unit_triangle)
    p_syms = build_symbols("p", p_pts)
    q_syms = build_symbols("q", q_pts)
    eqs = bracket_system(p_pts, p_syms, q_pts, q_syms, {(0, 0): sp.Integer(1)})
    assert len(eqs) == 1, eqs
    (only_key, only_expr), = eqs.items()
    expected = p_syms[(1, 0)] * q_syms[(0, 1)] - p_syms[(0, 1)] * q_syms[(1, 0)] - 1
    assert sp.expand(only_expr - expected) == 0, (only_expr, expected)
    print("P = p00 + p10*x + p01*y,  Q = q00 + q10*x + q01*y,  target [P,Q] = 1")
    print(f"constructor produced exactly one equation, at monomial {only_key}:")
    print(f"    {only_expr} = 0")
    print("  which is p10*q01 - p01*q10 = 1, the classical linear-Jacobian "
          "condition. MATCHES expected form exactly.")
    print()


def _convexity_checks() -> None:
    print("=" * 78)
    print("VALIDATION 2+3: convexity of every polygon used, and two "
          "independent lattice-point counts agreeing")
    print("=" * 78)
    for case in ALL_CASES:
        for name, verts in [("P", case["P"]), ("Q", case["Q"])]:
            full_name = f"{case['label']} :: N({name})"
            assert_valid_newton_polygon(full_name, verts)
            pts, hull = lattice_points(verts)
            pick = pick_lattice_count(verts)
            assert pick == len(pts), (full_name, pick, len(pts))
        print(f"  OK  {case['label']}")
    print("  All polygons: convex-hull(vertices) == vertices (no spurious "
          "or mistranscribed vertex), and enumeration count == Pick's-"
          "theorem count, for every N(P) and N(Q) above.")
    print()


def _report_case(case: dict) -> None:
    p_pts, p_hull = lattice_points(case["P"])
    q_pts, q_hull = lattice_points(case["Q"])
    p_syms = build_symbols("c", p_pts)
    q_syms = build_symbols("d", q_pts)
    eqs = bracket_system(p_pts, p_syms, q_pts, q_syms, case["rhs"])
    p_nz = nonzero_side_conditions(case["P"], p_syms)
    q_nz = nonzero_side_conditions(case["Q"], q_syms)

    print("-" * 78)
    print(case["label"])
    print("-" * 78)
    print(f"  N(P) vertices = {case['P']}")
    print(f"  N(Q) vertices = {case['Q']}")
    print(f"  target [P,Q]  = " + " + ".join(f"{v}*x^{i}y^{j}" for (i, j), v in case["rhs"].items()))
    print(f"  #unknowns in P = {len(p_pts)}   (vertices requiring nonzero coeff: {len(p_nz)})")
    print(f"  #unknowns in Q = {len(q_pts)}   (vertices requiring nonzero coeff: {len(q_nz)})")
    print(f"  TOTAL unknowns  = {len(p_pts) + len(q_pts)}")
    print(f"  #equations      = {len(eqs)}   (each quadratic/bilinear in the unknowns)")
    xs = [m[0] for m in eqs] or [0]
    ys = [m[1] for m in eqs] or [0]
    print(f"  equation monomial support spans x-degree [{min(xs)},{max(xs)}], "
          f"y-degree [{min(ys)},{max(ys)}]")
    print()
    return p_pts, p_syms, q_pts, q_syms, eqs


def main() -> None:
    _linear_sanity_check()
    _convexity_checks()

    print("=" * 78)
    print("SYSTEM SIZES")
    print("=" * 78)
    results = {}
    for case in ALL_CASES:
        results[case["label"]] = _report_case(case)

    print("=" * 78)
    print("Sample Singular emission (smaller OPEN sub-case, i.e. case (2))")
    print("=" * 78)
    p_pts, p_syms, q_pts, q_syms, eqs = results[OPEN_CASE_2["label"]]
    all_syms = list(p_syms.values()) + list(q_syms.values())
    sing = to_singular(eqs, all_syms, ring_name="r_open2", ideal_name="I_open2")
    # Print only a manageable preview -- the full ideal has ~92 generators.
    preview_lines = sing.splitlines()
    head = preview_lines[:2]
    tail_count = len(preview_lines) - 2
    print("\n".join(head))
    print(f"    ... ({tail_count - 1} more generator lines) ...")
    print(preview_lines[-1])
    print()
    print("(Call to_singular(...) directly for the full text; not printed in "
          "full here to keep this report readable. See jc2_gghv_system.md "
          "Section 5.5 for why running Groebner on this is not expected to "
          "finish, and what the actually-tractable next step would be.)")


if __name__ == "__main__":
    main()
