"""
Plane Jacobian campaign - Session 5
Finishing move for: min(deg_y P, deg_y Q) <= 2  =>  tame.

Remaining case: (2, n) pairs, n odd >= 5, lead A = s^2 nonconstant.
Rational shift y -> y + a1/(2s^2) diagonalizes the cascade:
    beta_{n-2j} = gamma_j * s^(n-2j) * atilde^j,
    gamma_0 = tau,  gamma_{j+1} = (n-2j) gamma_j / (2(j+1)),
    final condition:  s * (Psi(atilde))' = c.
Residue gate: (rational)' has zero residues; c/s has nonzero residue
at any simple root  =>  s has no simple roots.  Single-point survivor
s = x^k needs pi := (k-1)/D a positive even integer (D = (n+1)/2).

This script constructs the surviving templates EXPLICITLY (exact
monomial arithmetic) and measures the back-translation obstruction:
the y^0 coefficient of Q(x,y) = Qtilde(x, y + h), h = a1/(2 x^{2k}),
acquires a pole; we report its order and leading coefficient, and the
maximal pole order the free even chain could ever reach at y^0.
Obstruction certified  <=>  odd-chain pole order > even-chain reach
and leading coefficient != 0.
"""

from fractions import Fraction as F

def certify(n, k, verbose=True):
    D = (n + 1) // 2
    assert (k - 1) % D == 0 and ((k - 1) // D) % 2 == 0 and k > 1
    pi = (k - 1) // D                    # pole order of atilde at 0
    v_a1 = k - pi // 2                   # a1 = x^{v_a1}  (u0 = 1)
    # gamma_j for the odd chain, tau = 1
    gam = [F(1)]
    for j in range((n - 1) // 2):
        gam.append(gam[-1] * (n - 2*j) * F(1, 2*(j + 1)))
    # sanity: final condition atilde' * beta1 = const
    # atilde = -1/(4 x^pi); beta1 = gam[(n-1)//2] * x^k * atilde^{(n-1)//2}
    jmax = (n - 1) // 2
    c_beta1 = gam[jmax] * F(-1, 4)**jmax
    e_beta1 = k - pi * jmax
    c_final = c_beta1 * pi * F(1, 4)     # atilde' = (pi/4) x^{-pi-1}
    e_final = e_beta1 - pi - 1
    assert e_final == 0, "final condition not constant"
    # ---- odd-chain y^0 pole: sum_j gam_j x^{k(n-2j)} atilde^j h^{n-2j}
    # h = x^{v_a1 - 2k} / 2
    ledger = {}
    for j in range(jmax + 1):
        m = n - 2*j
        coeff = gam[j] * F(-1, 4)**j * F(1, 2)**m
        expo = k*m - pi*j + (v_a1 - 2*k)*m
        ledger[expo] = ledger.get(expo, F(0)) + coeff
    ledger = {e: c for e, c in ledger.items() if c != 0}
    odd_pole = -min(ledger)              # pole order at x = 0
    lead = ledger[min(ledger)]
    # ---- even-chain reach at y^0: contributions beta_{2i} h^{2i};
    # beta_{2i} spans s^{2i} * atilde^t for 0 <= t <= (n-1-2i)/2,
    # so most negative exponent = 2i*k - pi*t + 2i*(v_a1 - 2k), t max.
    reach = 0
    for i in range((n - 1)//2 + 1):
        tmax = (n - 1 - 2*i) // 2
        expo = 2*i*k - pi*tmax + 2*i*(v_a1 - 2*k)
        reach = max(reach, -expo)
    ok = odd_pole > reach and lead != 0
    if verbose:
        print(f"  (n,k)=({n},{k}): pi={pi}, a1=x^{v_a1}; "
              f"c = {c_final} (const, checks); y^0 odd-chain pole order "
              f"{odd_pole}, leading coeff {lead}; even-chain reach {reach}"
              f"  ->  {'OBSTRUCTED (template dies)' if ok else 'NOT decided'}")
    return odd_pole, lead, reach, ok

print("Universal-obstruction certification across admissible (n, k):")
all_ok, constants = True, {}
for n in (3, 5, 7, 9, 11):
    D = (n + 1)//2
    ks = [1 + 2*D*t for t in (1, 2, 3)]
    for k in ks:
        p, lead, r, ok = certify(n, k)
        all_ok &= ok
        constants.setdefault(n, set()).add(lead * 2**n * 4**((n-1)//2))
print("\nall admissible templates obstructed:", all_ok)
print("normalized universal constants  2^n*4^((n-1)/2)*lead  by n:")
for n, cs in constants.items():
    print(f"   n={n}: {sorted(cs)}   (k-independent: {len(cs)==1})")
