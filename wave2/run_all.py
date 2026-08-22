"""Run every wave-2 and wave-3 certifier and report a single pass/fail line.

Usage:  python3 wave2/run_all.py
Exit code 0 iff every certifier passes and the can't-fail audit is clean.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SCRIPTS = [
    "wave2/w2_h1c_refutation.py",
    "wave2/w2_pole_admissibility.py",
    "wave2/w2_money_cells.py",
    "wave2/w2_irreducibility_sieve.py",
    "wave2/w2_alpoge_detjf.py",
    "wave2/w2_cantfail_audit.py",
    "wave3/w3_endgame_degree_obstruction.py",
    "wave3/w3_weighted_homogeneous_theorem.py",
    "wave3/w3_descent_jacobian_formula.py",
    "wave3/w3_hit_protocol.py",
    "wave3/w3_claim_ledger.py",
]

results = []
for s in SCRIPTS:
    path = os.path.join(ROOT, s)
    print("=" * 78)
    print(f"RUNNING {s}")
    print("=" * 78)
    r = subprocess.run([sys.executable, path], capture_output=True, text=True)
    tail = [ln for ln in r.stdout.splitlines()
            if "checks passed" in ln or "VERDICT" in ln
            or "rigged checks in tree" in ln or "self-test" in ln
            or "ledger findings" in ln or "clean-ledger" in ln]
    for ln in tail:
        print(ln)
    if r.returncode != 0:
        print(r.stdout[-3000:])
        print(r.stderr[-3000:])
    results.append((s, r.returncode == 0))
    print()

print("=" * 78)
print("WAVE 2 SUMMARY")
print("=" * 78)
for s, ok in results:
    print(("    PASS  " if ok else "    FAIL  ") + s)
allok = all(ok for _, ok in results)
print(f"\n    {sum(1 for _, ok in results if ok)}/{len(results)} certifiers passed")
sys.exit(0 if allok else 1)
