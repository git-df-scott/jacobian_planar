#!/usr/bin/env python3
"""Relax the fixed=staying assumption in complete printed Euler signatures.

This is an audit of retained log rows, NOT a new group enumeration. Early
filtered and wrapped/incomplete rows are outside its coverage. The sole
coarse survivor is rejected by a written local node-incidence argument.
"""
import hashlib
import itertools
import json
from pathlib import Path
import re

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def ints(value):
    return tuple(map(int, re.findall(r"-?\d+", value)))


def main():
    signatures = {}
    inputs = {}
    pattern = re.compile(r"D=(\d+) n=\[([^]]*)\].* s=\[([^]]*)\] euler=(-?\d+) chiR=(-?\d+)")
    matched = 0
    for path in sorted((ROOT / "docs/plans/audit/vitushkin").glob("*.log")):
        source = str(path.relative_to(ROOT))
        inputs[source] = hashlib.sha256(path.read_bytes()).hexdigest()
        k = None
        curve = None
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if line.startswith("== "):
                curve = line.split()[1]
                k = None
            header = re.search(r"k=\[([^]]*)\]", line)
            if header:
                k = ints(header[1])
            match = pattern.search(line)
            if not match or k is None:
                continue
            D, n, fixed, eu, cr = int(match[1]), ints(match[2]), ints(match[3]), int(match[4]), int(match[5])
            if D < 6:
                continue
            assert len(n) == len(k)
            matched += 1
            key = D, n, k, fixed, eu, cr
            signatures.setdefault(key, []).append({"file": source, "line": number, "curve": curve, "text": line.strip()})

    survivors = []
    for (D, n, k, fixed, eu, cr), occurrences in sorted(signatures.items()):
        if eu + cr < 2:
            continue
        # Preserve the original necessary condition of at least one affine
        # preimage generically over each target component.
        for u in itertools.product(*(range(f) for f in n)):
            if not any(u):
                continue
            shift = sum(ui * (ki - 1) for ui, ki in zip(u, k))
            delta = eu + shift - 1
            if not 0 <= delta <= sum(fixed):
                continue
            assert eu + shift - delta == 1
            new_cr = cr - shift + delta
            assert new_cr >= 1
            survivors.append({"D": D, "old_n": n, "k": k, "old_s": fixed,
                              "old_euler": eu, "old_chiR": cr,
                              "escaping_fixed": u, "required_local_fixed_loss": delta,
                              "new_euler": 1, "new_chiR": new_cr, "occurrences": occurrences})

    assert len(survivors) == 1
    row = survivors[0]
    assert (row["D"], row["old_n"], row["k"], row["old_s"], row["escaping_fixed"],
            row["required_local_fixed_loss"]) == (6, (2, 2), (3, 2), (0, 2, 0), (0, 1), 2)
    assert all(o["curve"] == "cc_line_tan1" for o in row["occurrences"])
    # The only old local fixed points lie over the transverse intersection.
    # In each singleton local sheet the two divisors meet transversely.
    # At most u_cusp + u_line of those points can lie on deleted divisors.
    max_loss = sum(row["escaping_fixed"])
    assert row["required_local_fixed_loss"] > max_loss
    row["local_incidence_verdict"] = "REJECTED: loss 2 exceeds node capacity 1"

    # H3 cannot be rescued by marking either: chiX = 3u+s, s=0 or1.
    h3 = [(u, local) for u in range(2) for local in range(2) if 3*u+local == 1]
    assert h3 == [(0, 1)]
    output = {"scope": "Complete single-line printed Euler-stage signatures, D>=6; not all archived representations",
              "matched_rows": matched, "unique_signatures": len(signatures),
              "coarse_survivors": survivors, "survivors_after_node_incidence": 0,
              "H3_Euler_options": h3, "input_sha256": inputs,
              "script_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    (HERE / "marked_log_rescreen.json").write_text(json.dumps(output, indent=2) + "\n")
    print(f"MARKED_LOG_RESCREEN: {len(signatures)} distinct printed signatures; "
          f"{len(survivors)} relaxed survivor; 0 after local node incidence")


if __name__ == "__main__":
    main()
