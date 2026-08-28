import json, os, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "mate_search.json")))
print("total P swept:", len(R))
print()
print("by (arm, deg): consistent(dual) / total")
tab = defaultdict(lambda: [0, 0])
for r in R:
    k = (r["arm"], r["deg"])
    tab[k][1] += 1
    tab[k][0] += r["dual_prime_consistent"]
for k in sorted(tab, key=lambda t: (t[0], t[1])):
    print("  %-6s deg %-4d  %3d / %3d" % (k[0], k[1], tab[k][0], tab[k][1]))
print()
print("by tag: consistent(dual) / total")
tt = defaultdict(lambda: [0, 0])
for r in R:
    tt[r["tag"]][1] += 1
    tt[r["tag"]][0] += r["dual_prime_consistent"]
for k in sorted(tt):
    print("  %-22s %3d / %3d" % (k, tt[k][0], tt[k][1]))
print()
print("prime disagreement (p1 vs p2):",
      sum(1 for r in R if r["consistent_p999983"] != r["consistent_p1000003"]))
print("has_linear_term=0 and consistent:",
      sum(1 for r in R if not r["has_linear_term"] and r["dual_prime_consistent"]))
print("has_linear_term=0 total:", sum(1 for r in R if not r["has_linear_term"]))
print()
print("corank of A (n_unknowns - rank_A, p=999983):",
      dict(Counter(r["nullity_p999983"] for r in R)))
print()
print("support sizes: n_full_support min/median/max, thin_k distribution")
ns = sorted(r["n_full_support"] for r in R)
print("  n_full:", ns[0], ns[len(ns)//2], ns[-1])
nu = sorted(r["n_unknowns"] for r in R)
print("  n_unknowns:", nu[0], nu[len(nu)//2], nu[-1])
print("  thin_k:", dict(Counter(r["thin_k"] for r in R)))
print("  thinned (k>1):", sum(1 for r in R if r["thin_k"] > 1))
print()
print("exact_status:", dict(Counter(r["exact_status"] for r in R)))
print()
print("exactly verified mates (ring: Q):")
for r in R:
    if r["exact_status"] == "verified_bracket_eq_1":
        print("  %-8s %-18s arm=%-5s deg pair (P,Q)=(%d,%d) div_ordered=%s  |supp Q|=%d"
              % (r["hash"], r["tag"], r["arm"], r["deg"], r["deg_Q"],
                 r["div_ordered"], len(r["Q"])))
print()
q = [r for r in R if r["arm"] == "main" and r["exact_status"] == "verified_bracket_eq_1"
     and r["div_ordered"] == "False"]
print("QUANTITY OF INTEREST -- main-arm exactly verified mates with a "
      "non-divisibility-ordered degree pair:", len(q))
for r in q:
    print("  HIT", r["hash"], r["deg"], r["deg_Q"])
print()
print("total wall time (sum over P, s): %.1f" % sum(r["secs"] for r in R))
