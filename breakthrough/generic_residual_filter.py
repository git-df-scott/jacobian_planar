#!/usr/bin/env python3
"""Conservative, evidence-driven residual-edge filter for degree-pair sweeps.

Degree arithmetic never certifies a Newton face.  Consequently a bare pair is
reported as NO VERDICT; PASS FILTER requires an explicit certificate that all
face hypotheses were checked.  An observed exceptional edge is routed to a
SEPARATE STRATUM and is never rejected.
"""

from __future__ import annotations

import argparse
import json
from math import gcd
from pathlib import Path


REQUIRED_CERTIFICATES = (
    "leading_edges_nonzero",
    "leading_edges_exact_degree",
    "common_face",
    "leading_bracket_vanishes",
    "primitive_residual_cancels_face",
    "residual_edge_nonzero",
    "residual_edge_exact_degree_m_minus_1",
    "jacobian_rhs_strictly_below_next_face",
    "next_face_endpoints_nonzero",
)


def classify(record: dict) -> dict:
    """Classify one record without ever returning an emptiness verdict."""
    m, n = int(record["m"]), int(record["n"])
    if m < 1 or n < 1:
        raise ValueError("m and n must be positive")
    g = gcd(m, n)
    result = {
        "m": m,
        "n": n,
        "gcd": g,
        "a": m // g,
        "b": n // g,
        "hypotheses_automatic_from_degrees": False,
        "collapses_to_full_power_leading_row": False,
        "status": "NO VERDICT",
        "reason": "degree data do not determine a Newton face or residual edge",
    }

    evidence = record.get("edge_certificate")
    if evidence is None:
        return result
    missing = [name for name in REQUIRED_CERTIFICATES if name not in evidence]
    if missing:
        result["reason"] = "incomplete edge certificate: " + ", ".join(missing)
        return result
    failed = [name for name in REQUIRED_CERTIFICATES if evidence[name] is not True]
    if failed:
        result["status"] = "SEPARATE STRATUM"
        result["reason"] = "generic theorem excluded by: " + ", ".join(failed)
        return result

    result["status"] = "PASS FILTER"
    result["collapses_to_full_power_leading_row"] = True
    result["reason"] = "complete face certificate; full-power row is necessary only"
    return result


def load_records(path: Path) -> list[dict]:
    payload = json.loads(path.read_text())
    if isinstance(payload, dict):
        payload = payload.get("pairs")
    if not isinstance(payload, list):
        raise ValueError("input must be a JSON list or an object with a 'pairs' list")
    return payload


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="JSON candidate records")
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()
    results = [classify(record) for record in load_records(args.input)]
    rendered = json.dumps({"pairs": results}, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
