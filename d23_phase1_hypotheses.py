"""
Plane Jacobian campaign - Session N2, Phase 1: transfer hypotheses
checkable directly from the published Second Framework data
(arXiv:1901.04073 Sec. 4).  All checks exact.

H1. Cusp type (2,3): every published (y1,y2) valuation/pole pair is
    proportional to (3,2) -- the same single cusp function
    c2 = y1^2 - y2^3 governs the outer boundary, as in Sessions 15-18.
H2. Target degree pair (435,290) = 145*(3,2); FF comparison (99,66) = 33*(3,2).
H3. Degree bookkeeping of the (-5)-curve Belyi map: 28 = 14*2 = 9*3+1*1
    = 1*23+5*1, Riemann-Hurwitz exact (genus 0), and the chain degree
    D = 23 is the order of the {1}-marked point -- the analog of FF's
    16 = 8*2 = 5*3+1 = 1*13+3*1 with D = 13.
H4. The (-2)-curve realization target is a POLYNOMIAL Belyi map of
    degree 23 by the paper's own normalization ("so that the Belyi map
    is given by a polynomial") -- certified explicitly in Phase 0.
    Realization forces deg R = 23 exactly.
H5. The (-5)-curve Belyi map of the Second Framework has the SAME
    functional form as Session 7's FF map: B = P^2/(w R^3), deg P = 14,
    deg R = 9, with predicted miracle cancellation
    deg(P^2 - w R^3) = 5 = 28 - 23.  (Not yet derived -- this is the
    Session-7-analog target for the next session.)
"""
# H1: published valuation / pole pairs (paper Sec. 4)
pairs = {
    "Y curves 12,13,14 (stated)": (-15, -10),
    "Z E_-1 pole orders (stated)": (60, 40),
    "Z E_0 pole orders (stated)": (105, 70),
    "reconstructed curve 2 (stated)": (165, 110),
    "reconstructed curve 10 (stated)": (270, 180),
    "reconstructed curve 1 = degree pair (stated)": (435, 290),
}
ok = True
for k, (u1, u2) in pairs.items():
    p = (2*u1 == 3*u2)
    ok &= p
    print(f"H1  {k}: ({u1},{u2}) ~ (3,2): {p}")
print("H1  all published pairs proportional to (3,2):", ok)

# H2
print("\nH2  (435,290) = 145*(3,2):", (435, 290) == (145*3, 145*2),
      " | FF (99,66) = 33*(3,2):", (99, 66) == (33*3, 33*2))

# H3: RH for the degree-28 (-5)-curve map
deg = 28
prof = {"{0}": [2]*14, "{inf}": [3]*9 + [1], "{1}": [23] + [1]*5}
sums = {k: sum(v) for k, v in prof.items()}
rh = sum(e - 1 for v in prof.values() for e in v)
print("\nH3  fiber sums:", sums, "all == 28:", all(s == deg for s in sums.values()))
print("H3  Riemann-Hurwitz: sum(e-1) =", rh, "== 2*28-2 =", 2*deg - 2,
      ":", rh == 2*deg - 2)
print("H3  chain degree = order of the {1}-marked point = 23; branch")
print("    decomposition over {1}: 28 = 1*23 + 5*1 (five degree-1 sections,")
print("    certified against the projection formula in d23_phase1_chaindata.py)")

# H4
print("\nH4  realization target: the Phase-0-certified degree-23 Shabat")
print("    polynomial; any affine realization R = lambda*B((v-v0)/sigma)+nu")
print("    has deg R = 23 exactly (lambda, sigma != 0).")

# H5: form bookkeeping for the SF (-5)-map (next-session target)
print("\nH5  predicted (-5)-map: B = P^2/(w R^3), deg P = 14, deg R = 9:")
print("    deg P^2 =", 2*14, "= deg w*R^3 =", 1 + 3*9, ";")
print("    predicted miracle cancellation deg(P^2 - w R^3) = 28 - 23 =",
      28 - 23)
