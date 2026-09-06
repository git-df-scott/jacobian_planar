#!/usr/bin/env python3
"""Dependency-free regression tests for the conservative pair filter."""

from generic_residual_filter import REQUIRED_CERTIFICATES, classify


def certificate(**changes):
    result = {name: True for name in REQUIRED_CERTIFICATES}
    result.update(changes)
    return result


def main():
    # A degree pair alone can never manufacture face information.
    bare = classify({"m": 72, "n": 108})
    assert bare["gcd"] == 36 and (bare["a"], bare["b"]) == (2, 3)
    assert bare["status"] == "NO VERDICT"
    assert not bare["hypotheses_automatic_from_degrees"]

    # Every excluded mode is routed, never rejected.
    for key in (
        "residual_edge_nonzero",
        "residual_edge_exact_degree_m_minus_1",
        "primitive_residual_cancels_face",
        "next_face_endpoints_nonzero",
    ):
        routed = classify({"m": 8, "n": 12, "edge_certificate": certificate(**{key: False})})
        assert routed["status"] == "SEPARATE STRATUM"

    # Known tame Keller controls satisfy the necessary full-power conclusion.
    for m, n in ((1, 2), (2, 4), (2, 6)):
        control = classify({"m": m, "n": n, "edge_certificate": certificate()})
        assert control["status"] == "PASS FILTER"
        assert control["collapses_to_full_power_leading_row"]
        assert (control["a"], control["b"]) == (1, n // m)

    print("PASS: conservative residual filter and three tame controls")


if __name__ == "__main__":
    main()
