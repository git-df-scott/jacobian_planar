#!/usr/bin/env python3
"""Run every ASTRA exact control and refresh the machine-readable artifacts."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ARTIFACTS = HERE / "artifacts"


RUNS = [
    ("graded_control.py", "graded_positive_controls_2026-09-04.json"),
    ("briancon_control.py", "briancon_control_2026-09-04.json"),
    ("group_first_h3.py", "group_first_h3_2026-09-04.json"),
    ("abstract_target_screen.py", "abstract_target_screen_2026-09-04.json"),
    ("audit_graded_case2.py", "graded_case2_audit_2026-09-04.json"),
    ("joint_blueprint.py", "joint_blueprint_2026-09-04.json"),
]


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    for script, artifact in RUNS:
        command = [sys.executable, str(HERE / script), "--output", str(ARTIFACTS / artifact)]
        print("RUN", script, flush=True)
        subprocess.run(command, check=True, stdout=subprocess.DEVNULL)
        print("PASS", artifact, flush=True)
    print("ALL ASTRA CONTROLS: PASS")


if __name__ == "__main__":
    main()
