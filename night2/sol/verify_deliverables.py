#!/usr/bin/env python3
"""Fast integrity checks for the shipped JC2 separator artifacts."""

from __future__ import annotations

import csv
import py_compile
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def main() -> int:
    try:
        for name in ("separator_pipeline.py", "certify_separator_d3.py"):
            py_compile.compile(str(ROOT / name), doraise=True)
        print("PASS V1 Python syntax")

        rows = list(csv.DictReader((ROOT / "separator_counts.csv").open()))
        assert len(rows) == 16
        by_d: dict[int, list[dict[str, str]]] = {}
        for row in rows:
            by_d.setdefault(int(row["d"]), []).append(row)
            assert all(row[k] == "PASS" for k in ("S1", "S2", "I1", "I2", "I3"))
            assert row["status"] == "MODULAR-CORRECTED"
            assert int(row["rank"]) + int(row["separators"]) == (
                ((int(row["d"]) + 1) * (int(row["d"]) + 2) + 1)
                * ((int(row["d"]) + 1) * (int(row["d"]) + 2) + 2) // 2
            )
        for d in range(3, 11):
            pair = by_d[d]
            assert {int(x["prime"]) for x in pair} == {999983, 1000003}
            assert len({(x["rank"], x["separators"]) for x in pair}) == 1
        print("PASS V2 CSV shape, controls, rank-nullity, and cross-prime agreement")

        run = subprocess.run([sys.executable, str(ROOT / "certify_separator_d3.py")],
                             cwd=ROOT, text=True, capture_output=True, check=True)
        assert "PASS CERTIFICATE" in run.stdout and "CANDIDATE-UNVERIFIED: none" in run.stdout
        print("PASS V3 exact d=3 certificate checker")

        report = (ROOT / "FULL_NIGHT_REPORT.md").read_text()
        theory = (ROOT / "ROUND2_THEORY.md").read_text()
        assert "Current answer: no" in report
        assert "VERDICT: UNCLEAR" in report
        assert "128,056,006" in report and "Conjecture 7.3" in report
        assert "Exact certification protocol" in theory
        print("PASS V4 report/theory required conclusions")
        print("PASS DELIVERABLES all fast integrity checks completed")
        return 0
    except Exception as exc:
        print(f"FAIL DELIVERABLES {exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
