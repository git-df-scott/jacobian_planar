#!/usr/bin/env python3
"""Derive the mutable nonzero vertices from the stated pentagon supports."""

from pentagon_core import P_ROWS, Q_ROWS


def convex_hull(points):
    """Return the strict convex hull in counter-clockwise order."""
    points = sorted(set(points))
    if len(points) <= 1:
        return points

    def cross(o, a, b):
        return ((a[0] - o[0]) * (b[1] - o[1]) -
                (a[1] - o[1]) * (b[0] - o[0]))

    lower = []
    for point in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], point) <= 0:
            lower.pop()
        lower.append(point)
    upper = []
    for point in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], point) <= 0:
            upper.pop()
        upper.append(point)
    return lower[:-1] + upper[:-1]


def support_points(rows):
    return [(i, j) for j, (lo, hi) in rows.items()
            for i in range(lo, hi + 1)]


def coefficient(prefix, vertex):
    i, j = vertex
    return f"{prefix}_{j}_{i}"


def main():
    p_hull = convex_hull(support_points(P_ROWS))
    q_hull = convex_hull(support_points(Q_ROWS))
    expected_p = {(0, 0), (1, 0), (8, 14), (8, 16), (0, 8)}
    expected_q = {(0, 0), (2, 1), (12, 21), (12, 24), (0, 12)}
    assert set(p_hull) == expected_p, p_hull
    assert set(q_hull) == expected_q, q_hull

    print("P hull vertices (x-degree,y-degree):", p_hull)
    print("Q hull vertices (x-degree,y-degree):", q_hull)
    print("fixed/gauge P vertices: p_0_0 additive, p_0_1=1")
    print("fixed/gauge Q vertices: q_0_0 additive, q_1_2=1")

    mutable_p = sorted(expected_p - {(0, 0), (1, 0)})
    mutable_q = sorted(expected_q - {(0, 0), (2, 1)})
    print("mutable required P nonzeros:",
          ", ".join(coefficient("p", v) for v in mutable_p))
    print("mutable required Q nonzeros:",
          ", ".join(coefficient("q", v) for v in mutable_q))
    print("p_16_8 != 0 is necessary but is not the complete candidate test")
    print("VERDICT: NO VERDICT")


if __name__ == "__main__":
    main()
