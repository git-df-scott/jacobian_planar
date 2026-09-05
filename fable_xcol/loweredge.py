"""Is the LOWER edge of the pentagon also a perfect-power relation?
The campaign established Qh^2 = c A^3 for the UPPER edge (OPUS43-014).
Claim: the lower edge gives the SAME shape, from the resonance of valuations.

val a_i = 2(i-1) (i>=1),  val b_k = 2k-3 (k>=2).  For i+k = d+1 every term of
rung d has y-valuation exactly 2d-4, so the lowest coefficient of rung d is one
equation in the lower-edge coefficients A_i (= lowest coeff of a_i), B_k.
"""
import sympy as sp
y, t = sp.symbols('y t')
NA, NB = 9, 13
A = [sp.Symbol(f'A{i}') for i in range(NA)]
B = [sp.Symbol(f'B{k}') for k in range(NB)]

print("=== 1. valuation resonance check ===")
va = {i: (2*(i-1) if i >= 1 else 1) for i in range(NA)}
vb = {k: (2*k-3 if k >= 2 else 1) for k in range(NB)}
for d in range(4, 20):
    vals = set()
    for i in range(NA):
        k = d+1-i
        if 0 <= k < NB and i >= 1 and k >= 2:
            vals.add(va[i] + vb[k] - 1)
    if vals: print(f"  d={d}: term valuations {sorted(vals)}  resonant={len(vals)==1}")

print("\n=== 2. the lowest-order coefficient of rung d ===")
# a_i = A_i y^{va[i]} + ... ; b_k = B_k y^{vb[k]} + ...
# i*a_i*b_k' - k*a_i'*b_k  ->  [ i*vb[k] - k*va[i] ] A_i B_k y^{va+vb-1}
for d in range(6, 20):
    terms = []
    for i in range(1, NA):
        k = d+1-i
        if 2 <= k < NB:
            terms.append((i*vb[k] - k*va[i], i, k))
    if terms:
        expr = " + ".join(f"({c})A{i}B{k}" for c, i, k in terms)
        # check the coefficient equals 2k-3i
        ok = all(c == 2*k-3*i for c, i, k in terms)
        print(f"  d={d}: coefficient is (2k-3i) for every term: {ok}")

print("\n=== 3. generating-function form ===")
Ag = sum(A[i]*t**i for i in range(NA)); Bg = sum(B[k]*t**k for k in range(NB))
lhs = sp.expand(2*Ag*sp.diff(Bg, t) - 3*sp.diff(Ag, t)*Bg)
ok = True
for d in range(0, 21):
    gf = sp.expand(lhs.coeff(t, d))
    direct = sp.expand(sum((2*(d+1-i) - 3*i)*A[i]*B[d+1-i]
                           for i in range(NA) if 0 <= d+1-i < NB))
    if sp.simplify(gf - direct) != 0:
        ok = False; print("   mismatch at d =", d)
print("  rung equations == coefficients of  2 A B' - 3 A' B :", ok)
print("  => 2 A B' = 3 A' B  =>  B'/B = (3/2) A'/A  =>  **B^2 = c A^3**")

print("\n=== 4. consequence, with the pentagon's degrees ===")
print("  deg A <= 8 (i = 0..8), deg B <= 12 (k = 0..12), and 2*12 = 3*8.")
print("  B^2 = c A^3 with B polynomial forces every root of A to have even")
print("  multiplicity:   A = a*G^2,  B = b*G^3,  deg G = 4.")
print("  This is the SAME shape the campaign proved for the UPPER edge only.")

print("\n=== 5. control: does A with simple roots kill B? ===")
G = sp.Symbol('g')
Atest = sp.prod([t - j for j in range(1, 9)])          # 8 distinct roots
Bs = [sp.Symbol(f'b{k}') for k in range(13)]
Btest = sum(Bs[k]*t**k for k in range(13))
eqs = sp.Poly(sp.expand(2*Atest*sp.diff(Btest, t) - 3*sp.diff(Atest, t)*Btest), t).all_coeffs()
sol = sp.solve(eqs, Bs, dict=True)
print("  A with 8 simple roots -> B solutions:", sol)
print("  (must force B = 0, i.e. the degenerate branch)")
