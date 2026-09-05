"""night9 — MANDATORY POSITIVE CONTROL at p = 2 on the exact Mondello support.

Two independent methods:
  (A) naive exhaustive enumeration of all 2^9 = 512 points of F_2^9, testing
      every solution by DIRECT SUBSTITUTION (poly_det_minus_one + collisions),
      i.e. not using the equation-assembly code path at all;
  (B) the bilinear exhaustive solver of night9/keller_solver.py.

night8/mondello_lift.json records that the E0 system has exactly 8 F_2 points.
Hard exit if (A) != 8, or if (A) != (B).
"""
import itertools, json, os, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from keller_solver import exhaustive, verify_solution, hensel_step

SP = [(1, 0), (2, 1), (4, 0), (6, 2)]
SQ = [(0, 1), (5, 0), (6, 1), (7, 2), (8, 3)]
p = 2

t0 = time.time()
naive = []
for v in itertools.product(range(p), repeat=len(SP) + len(SQ)):
    a = list(v[:len(SP)]); b = list(v[len(SP):])
    chk = verify_solution(SP, SQ, a, b, p)
    if chk["det_ok"] and chk["coll_ok"]:
        naive.append((a, b))
t_naive = time.time() - t0

t0 = time.time()
ex = exhaustive(SP, SQ, p, budget=10 ** 7, max_solutions=64)
t_ex = time.time() - t0

base = ([1, 1, 1, 1], [1, 1, 1, 1, 1])
climb = {}
for (a, b) in naive:
    r2 = hensel_step(SP, SQ, a, b, p, 1)
    key = "".join(map(str, a + b))
    climb[key] = {"to_p2": r2 is not None}
    if r2 is not None:
        r3 = hensel_step(SP, SQ, r2[0], r2[1], p, 2)
        climb[key]["to_p3"] = r3 is not None

out = {
    "support_P": SP, "support_Q": SQ, "p": p,
    "method_A_naive_F2_9": {"n_points_scanned": p ** 9,
                            "n_solutions": len(naive),
                            "solutions": [{"a": a, "b": b} for a, b in naive],
                            "wall_s": round(t_naive, 3)},
    "method_B_bilinear_exhaustive": {"count": ex["count"],
                                     "n_enum": ex["n_enum"],
                                     "enum_side": ex["enum_side"],
                                     "wall_s": round(t_ex, 3)},
    "night8_recorded_count": 8,
    "base_point_in_solution_set": list(base) in [[a, b] for a, b in naive],
    "hensel_climb_from_each_F2_point": climb,
    "AGREE_naive_vs_bilinear": len(naive) == ex["count"],
    "AGREE_with_night8": len(naive) == 8,
}
here = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(here, "control_p2.json"), "w") as f:
    json.dump(out, f, indent=1)

print(json.dumps({k: v for k, v in out.items()
                  if k not in ("hensel_climb_from_each_F2_point",)}, indent=1)[:2000])
print("climb:", json.dumps(climb))
if not (out["AGREE_with_night8"] and out["AGREE_naive_vs_bilinear"]):
    print("CONTROL FAILED — hard exit")
    sys.exit(1)
print("CONTROL PASSED")
