"""
The graded (one-variable) system for p108_525122, built from scratch.

Unknowns (after the scaling normalisation c2 = F0 = 1):
    F = (F0..F7)      f_2 = T*F(T)      [P's rho=2 slice]
    A = (A0..A7)      f_1 = T*A(T)      [P's rho=1 slice]
    B = (B0..B8)      f_0 = B(T)        [P's rho=0 slice]
    G  (G0..G10)      g_3 = T^2*G(T)
    G2 (G2_0..G2_10)  g_2 = T^2*G2(T)
    G1 (G1_0..G1_11)  g_1 = T*G1(T)
    G0 (G0_0..G0_11)  g_0 = T*G0(T)

Levels (rho+sigma = s), each  sum_rho ( rho f_rho g_sigma' - sigma f_rho' g_sigma ):
 s=5 : 2f2 g3' - 3f2' g3 = T^2
 s=4 : 2f2 g2' - 2f2' g2 + f1 g3' - 3f1' g3 = 0
 s=3 : 2f2 g1' - 1f2' g1 + f1 g2' - 2f1' g2 - 3f0' g3 = 0
 s=2 : 2f2 g0' + f1 g1' - 1f1' g1 - 2f0' g2 = 0
 s=1 : f1 g0' - f0' g1 = 0

Expanded coefficientwise (derived once, checked against the 2-variable cascade
in verify.py):
 E1 [T^n]      : sum_{i+j=n} (1+2j-3i) F_i G_j            = delta_{n,0}
 E2 [T^{2+n}]  : sum_{i+j=n} (2+2j-2i) F_i G2_j + sum_{i+j=n} (-1+j-3i) A_i G_j = 0
 E3 [T^{1+m}]  : sum_{i+j=m} (1+2j-i) F_i G1_j
                 + sum_{i+j=m-1} (j-2i) A_i G2_j - 3 sum_{i+j=m} i B_i G_j = 0
 E4 [T^{1+m}]  : sum_{i+j=m} (2+2j) F_i G0_j
                 + sum_{i+j=m} (j-i) A_i G1_j - 2 sum_{i+j=m} i B_i G2_j = 0
 E5 [T^{m}]    : sum_{i+j=m-1} (1+j) A_i G0_j - sum_{i+j=m} i B_i G1_j = 0
"""
dF, dA, dB = 7, 7, 8
dG, dG2, dG1, dG0 = 10, 10, 11, 11


def _conv(coef, X, Y, n, dX, dY):
    t = 0
    for i in range(0, dX + 1):
        j = n - i
        if 0 <= j <= dY:
            t = t + coef(i, j) * X[i] * Y[j]
    return t


def solve_G(F, zero):
    """E1: triangular solve for G0..G10; returns G and residuals for n=11..16."""
    G = [zero] * (dG + 1)
    res = []
    for n in range(0, dF + dG + 1):
        e = _conv(lambda i, j: (1 + 2 * j - 3 * i), F, G, n, dF, dG)
        rhs = 1 if n == 0 else 0
        if n <= dG:
            G[n] = (rhs - e) / (1 + 2 * n)   # G[n] entered with coeff (1+2n)
        else:
            res.append(e - rhs)
    return G, res


def solve_G2(F, A, G, zero):
    G2 = [zero] * (dG2 + 1)
    res = []
    for n in range(0, max(dF + dG2, dA + dG) + 1):
        e = (_conv(lambda i, j: (2 + 2 * j - 2 * i), F, G2, n, dF, dG2)
             + _conv(lambda i, j: (-1 + j - 3 * i), A, G, n, dA, dG))
        if n <= dG2:
            G2[n] = -e / (2 + 2 * n)
        else:
            res.append(e)
    return G2, res


def solve_G1(F, A, B, G, G2, zero):
    G1 = [zero] * (dG1 + 1)
    res = []
    top = max(dF + dG1, dA + dG2 + 1, dB + dG)
    for m in range(0, top + 1):
        e = (_conv(lambda i, j: (1 + 2 * j - i), F, G1, m, dF, dG1)
             + _conv(lambda i, j: (j - 2 * i), A, G2, m - 1, dA, dG2)
             - 3 * _conv(lambda i, j: i, B, G, m, dB, dG))
        if m <= dG1:
            G1[m] = -e / (1 + 2 * m)
        else:
            res.append(e)
    return G1, res


def solve_G0(F, A, B, G1, G2, zero):
    G0 = [zero] * (dG0 + 1)
    res = []
    top = max(dF + dG0, dA + dG1, dB + dG2)
    for m in range(0, top + 1):
        e = (_conv(lambda i, j: (2 + 2 * j), F, G0, m, dF, dG0)
             + _conv(lambda i, j: (j - i), A, G1, m, dA, dG1)
             - 2 * _conv(lambda i, j: i, B, G2, m, dB, dG2))
        if m <= dG0:
            G0[m] = -e / (2 + 2 * m)
        else:
            res.append(e)
    return G0, res


def resid_E5(A, B, G0, G1, zero):
    res = []
    top = max(dA + dG0 + 1, dB + dG1)
    for m in range(0, top + 1):
        e = (_conv(lambda i, j: (1 + j), A, G0, m - 1, dA, dG0)
             - _conv(lambda i, j: i, B, G1, m, dB, dG1))
        res.append(e)
    return res


def all_residuals(F, A, B, zero=0):
    G, r1 = solve_G(F, zero)
    G2, r2 = solve_G2(F, A, G, zero)
    G1, r3 = solve_G1(F, A, B, G, G2, zero)
    G0, r4 = solve_G0(F, A, B, G1, G2, zero)
    r5 = resid_E5(A, B, G0, G1, zero)
    return dict(G=G, G2=G2, G1=G1, G0=G0, r1=r1, r2=r2, r3=r3, r4=r4, r5=r5)
