#!/usr/bin/env python3
"""Provenance and certificate audit for the graded case-(2) archive.

This does not re-run Singular.  It pins and hashes the archived inputs/logs,
checks their required certificate lines, and independently factors the
five-orbit eliminant over F_32003.  The output intentionally preserves the
distinction between EMPTY-mod-p and an exact characteristic-zero verdict.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path


COMMIT = "10469087a97ca4143ce8a278f3ce0211143ced19"
PREFIX = "x2/"
HASHES = {
    "c19711d9c1808fefd6c0a8236cf67dfbe61b4764.sing": "c86029c1be31134c0ba49fb07f8d4a17afd9c93d0aeb918b09791c35143ee0b4",
    "stage_0.log": "91ab204bd2833a9be0fdb597f2a34aea0f86d27b5e5af56878276209774a92b5",
    "stage_1.log": "91ab204bd2833a9be0fdb597f2a34aea0f86d27b5e5af56878276209774a92b5",
    "stage_ext3.log": "71b0bc3c33487676fb027b0f97d584f05437b8bdf9eeac0395ca08fa2f34d9a7",
    "stage_p1000003_0.log": "91ab204bd2833a9be0fdb597f2a34aea0f86d27b5e5af56878276209774a92b5",
    "e1_points.log": "f1bff0764676b0a04a7aa03227a0877876c5a0486dc0aac09ad7d07a9dbc4324",
    "decide_m_8.log": "dea07f0217f08fc6a7e273fbf7328e61a38c38bab58b4851b38ecc764a2b8942",
}


def git_blob(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{COMMIT}:{PREFIX}{path}"])


def evaluate(coefficients: list[int], value: int, prime: int) -> int:
    result = 0
    for coefficient in reversed(coefficients):
        result = (result * value + coefficient) % prime
    return result


def synthetic_divide(coefficients: list[int], root: int, prime: int) -> list[int]:
    # Coefficients are low-to-high.  Divide by z-root and assert zero remainder.
    descending = list(reversed([x % prime for x in coefficients]))
    quotient_descending = [descending[0]]
    for coefficient in descending[1:-1]:
        quotient_descending.append((coefficient + root * quotient_descending[-1]) % prime)
    remainder = (descending[-1] + root * quotient_descending[-1]) % prime
    if remainder:
        raise AssertionError("claimed modular root is not a root")
    return list(reversed(quotient_descending))


def factor_orbit_eliminant() -> dict:
    # e1_points.log writes h(F6)=H(F6^7).  H is this quintic.
    prime = 32003
    coefficients = [3114, 4712, 5742, 10358, -1464, 1]
    roots = [x for x in range(prime) if evaluate(coefficients, x, prime) == 0]
    if roots != [5934, 14549]:
        raise AssertionError(f"unexpected F_{prime} roots: {roots}")
    residual = coefficients
    for root in roots:
        residual = synthetic_divide(residual, root, prime)
    # A cubic over a finite field is irreducible iff it has no field root.
    if any(evaluate(residual, x, prime) == 0 for x in range(prime)):
        raise AssertionError("residual cubic is reducible")
    return {
        "prime": prime,
        "quintic_coefficients_low_to_high": coefficients,
        "linear_roots": roots,
        "residual_cubic_coefficients_low_to_high": residual,
        "irreducible_factor_degrees": [1, 1, 3],
        "residual_scaling_orbits": 5,
        "status": "PASS",
    }


def require(text: str, *needles: str) -> None:
    absent = [needle for needle in needles if needle not in text]
    if absent:
        raise AssertionError(f"archive log misses {absent}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    checked_hashes = {}
    blobs = {}
    for path, expected in HASHES.items():
        blob = git_blob(path)
        digest = hashlib.sha256(blob).hexdigest()
        if digest != expected:
            raise AssertionError(f"{path}: expected {expected}, got {digest}")
        checked_hashes[path] = digest
        blobs[path] = blob.decode("utf-8")

    require(blobs["e1_points.log"], "dim 0  vdim 35", "lex GB size 7", "triangular components: 1")
    require(blobs["decide_m_8.log"], "m=8 p=32003", "E1 vdim 35")
    for path in ("stage_0.log", "stage_1.log", "stage_ext3.log"):
        require(blobs[path], "E1 residual (must be 0): 0", "dim = -1", "GB[1] = 1")
    require(blobs["stage_ext3.log"], "minpoly check (must be 0): 0")
    require(blobs["stage_p1000003_0.log"], "E1 residual (must be 0): 0", "dim = -1", "GB[1] = 1")

    report = {
        "archive_commit": COMMIT,
        "sha256": checked_hashes,
        "archive_integrity": "PASS",
        "independent_F32003_factor_check": factor_orbit_eliminant(),
        "F32003": {
            "leading_solutions_geometric": 35,
            "residual_scaling_orbits": 5,
            "orbit_factor_degrees": [1, 1, 3],
            "lower_level_certificate_logs": ["stage_0.log", "stage_1.log", "stage_ext3.log"],
            "verdict": "EMPTY-mod-p",
        },
        "F1000003": {
            "leading_solutions_geometric": 35,
            "certified_lower_level_scope": "one rational orbit only",
            "verdict": "partial EMPTY-mod-p; not a full-prime verdict",
        },
        "characteristic_zero": {
            "verdict": "UNKNOWN",
            "reason": "no exact-Q lower-level certificate was found; archived degree-35 and degree-1144 characteristic-zero descriptions are not proven to be the same residual object",
        },
        "overall_evidence_label": "EMPTY-mod-p at p=32003; UNKNOWN over characteristic zero",
    }
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered)
    print(rendered, end="")


if __name__ == "__main__":
    main()
