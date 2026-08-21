import json, os, sys, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sympy as sp
from w5_samesign_sweep import (check, RESULTS, bracket, is_keller, cell_system,
                               singular_decompose, classify_branch,
                               is_automorphism, generic_fibre_size, monomials,
                               x, y)

DEGCAP = 20
AB_CAP = 12
print("=" * 78)
print("T2  SAME-SIGN WEIGHTED-HOMOGENEOUS SECTOR -- exact sweep")
print("=" * 78)

# ---- structural fact, COMPUTED not assumed -------------------------------
bad = []
for a in range(0, AB_CAP + 1):
    for b in range(0, AB_CAP + 1 - a):
        for dP in range(0, a + b + 4):
            for dQ in range(0, a + b + 4):
                if dP + dQ == a + b:
                    continue
                cell = cell_system(a, b, dP, dQ, 8)
                if cell is None:
                    continue
                if cell["const"] != 0:
                    bad.append((a, b, dP, dQ, cell["const"]))
check("degree identity: [P,Q] can only have a nonzero constant term when "
      "dP + dQ = a + b (checked on every off-shell cell, not assumed)",
      not bad, f"violations {bad[:3]}")

# ---- the sweep ------------------------------------------------------------
rows = []
for a in range(0, AB_CAP + 1):
    for b in range(0, AB_CAP + 1 - a):
        if a == 0 and b == 0:
            continue
        for dP in range(1, a + b):
            dQ = a + b - dP
            cell = cell_system(a, b, dP, dQ, DEGCAP)
            if cell is None:
                continue
            out = singular_decompose(cell)
            row = {"weights": [a, b], "dP": dP, "dQ": dQ,
                   "MP": [list(m) for m in cell["MP"]],
                   "MQ": [list(m) for m in cell["MQ"]],
                   "singular": out.strip().split("\n")[:2],
                   "branches": []}
            if out.startswith("NOCONST") or out.strip() == "" or "EMPTY" in out:
                row["verdict"] = "NO-KELLER-PAIR"
            elif out == "TIMEOUT":
                row["verdict"] = "STALLED-singular-timeout"
            else:
                comps = re.findall(r"GENS (.+)", out)
                row["verdict"] = "KELLER-PAIRS"
                for gs in comps:
                    pts = classify_branch(cell, gs)
                    for (P, Q, J) in pts:
                        auto, ev = is_automorphism(P, Q)
                        row["branches"].append({
                            "component": gs[:200],
                            "P": sp.sstr(P), "Q": sp.sstr(Q), "detJ": sp.sstr(J),
                            "is_automorphism": bool(auto), "evidence": ev})
                if not row["branches"]:
                    row["verdict"] = "KELLER-IDEAL-NONEMPTY-NO-RATIONAL-POINT-FOUND"
            rows.append(row)
            print(f"  (a,b)=({a},{b}) dP={dP} dQ={dQ}  |MP|={len(cell['MP'])} "
                  f"|MQ|={len(cell['MQ'])}  -> {row['verdict']}"
                  + (f"  branches={len(row['branches'])}" if row["branches"] else ""))

nonauto = [(r, br) for r in rows for br in r["branches"] if not br["is_automorphism"]]
print(f"\n  cells swept: {len(rows)}")
print(f"  Keller branches found: {sum(len(r['branches']) for r in rows)}")
print(f"  branches that are NOT automorphisms: {len(nonauto)}")
for r, br in nonauto:
    print(f"    CANDIDATE-UNVERIFIED  weights={r['weights']} dP={r['dP']} "
          f"P={br['P']}  Q={br['Q']}  detJ={br['detJ']}")

# ---- controls -------------------------------------------------------------
print("\n  CONTROLS")
found_triangular = []
for m in range(2, 6):
    hits = [r for r in rows
            for br in r["branches"]
            if sp.simplify(sp.sympify(br["Q"]) - (y + x ** m)) == 0
            or sp.simplify(sp.sympify(br["P"]) - (y + x ** m)) == 0]
    cellsok = any(r for r in rows if r["weights"] == [1, m] and r["dP"] in (1, m)
                  and (0, 1) in [tuple(z) for z in r["MP"]] + [tuple(z) for z in r["MQ"]])
    found_triangular.append((m, bool(hits) or cellsok))
check("POSITIVE: the weight cell containing (x, y + x^m) is swept for m=2..5",
      all(v for _, v in found_triangular), str(found_triangular))

okA, JA = is_keller(x, y + x ** 3)
check("POSITIVE: the sweep's Keller test ACCEPTS (x, y + x^3)", okA and JA == 1,
      f"detJ = {JA}")
autoA, evA = is_automorphism(x, y + x ** 3)
check("POSITIVE: the sweep's automorphism test ACCEPTS (x, y + x^3)", autoA,
      str(evA))
autoB, evB = is_automorphism(x + 2 * y, y)
check("POSITIVE: the sweep's automorphism test ACCEPTS (x + 2y, y)", autoB,
      str(evB))

okC, JC = is_keller(x, x * y)
check("NEGATIVE: the Keller test REJECTS (x, x*y)", not okC, f"detJ = {JC}")
okD, JD = is_keller((3 * x + y) ** 2, 3 * x + y)
check("NEGATIVE: the Keller test REJECTS ((3x+y)^2, 3x+y)", not okD, f"detJ = {JD}")
fib = generic_fibre_size(sp.expand(x ** 2 - y ** 2), sp.expand(x * y))
check("NEGATIVE: the generic-fibre leg REJECTS the non-injective (x^2-y^2, x*y)",
      fib is not None and fib > 1, f"generic fibre size = {fib}")
autoE, evE = is_automorphism(sp.expand(x ** 2 - y ** 2), sp.expand(x * y))
check("NEGATIVE: the automorphism test REJECTS (x^2-y^2, x*y)", not autoE, str(evE))

HERE = os.path.dirname(os.path.abspath(__file__))
json.dump({"degcap": DEGCAP, "ab_cap": AB_CAP, "rows": rows,
           "non_automorphism_branches": len(nonauto),
           "controls": [[n, o, note] for n, o, note in RESULTS]},
          open(os.path.join(HERE, "sweep_results.json"), "w"), indent=1)

print("\n" + "=" * 78)
npass = sum(1 for _, o, _ in RESULTS if o)
print(f"    {npass}/{len(RESULTS)} checks passed")
print("=" * 78)
sys.exit(0 if npass == len(RESULTS) else 1)
