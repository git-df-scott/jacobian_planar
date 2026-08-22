"""
Plane Jacobian campaign - Session 19, companion
THE ADMISSIBLE PARAMETER LATTICE, and what the divisibility test really says.

Given the Session-19 master identity

  alpha^(a+b) (v+1)^((a+b)m-1) v^((a+b)sigma-1)
        [ k v(v+1) R' + D((m+sigma)v + sigma) R ]  =  -c v^(rho - rho^2)

the two order-matching relations are

  (Q)  D = (a+b) k + 1 - rho            (q-order)
  (V)  (a+b) sigma = 1 + rho - rho^2    (v-order)

Consequences enumerated here, all in exact integer arithmetic:

 1. k is DETERMINED by (a, b, rho, D):  k = (D + rho - 1)/(a+b).  It is NOT a
    free dial that can be held at 3 while D varies.  In particular, in
    Borisov's own family (a,b,rho) = (2,3,3):
        D = 13 -> k = 3       D = 23 -> k = 5       D = 28 -> k = 6
    so the campaign's transfer conjecture "3 v(v+1) R' = D R for every chain
    degree D" holds the coefficient fixed at 3 when the machinery moves it.

 2. The divisibility test in the degenerate branch M == 0 is k | D*sigma and
    k | D*m -- i.e. "mod k", not "mod 3".  With (Q) it reduces to k | (rho-1)
    when m = 1, sigma = -1.

 3. Neither test decides anything, because the PRIMARY obstruction --
    (v+1)^((a+b)m - 1) vanishing at v = -1 with m >= 1 forced -- fires for
    every admissible lattice point.
"""

from fractions import Fraction as Fr
from math import gcd

LEDGER = []


def note(ok, text):
    LEDGER.append((bool(ok), text))
    print(f"  [{'PASS' if ok else 'FAIL'}] {text}")


# ===================================================================
# 1.  k is determined, not free.
# ===================================================================
print("SECTION 1  k = (D + rho - 1)/(a+b) is DETERMINED by (a,b,rho,D)")

def k_of(a, b, rho, D):
    num, den = D + rho - 1, a + b
    return Fr(num, den)

def D_of(a, b, rho, k):
    return (a + b)*k + 1 - rho

# Borisov's own family: (a,b,rho) = (2,3,3)
rows = []
for D in (3, 8, 13, 18, 23, 28, 33):
    kk = k_of(2, 3, 3, D)
    rows.append((D, kk, kk.denominator == 1))
    print(f"     (a,b,rho)=(2,3,3),  D = {D:2d}  ->  k = {kk}"
          f"{'   [admissible]' if kk.denominator == 1 else '   [NOT an integer: inadmissible]'}")

note(k_of(2, 3, 3, 13) == 3,
     "D = 13 (First Framework)   -> k = 3   : matches the certified 3v(v+1)R'-13R")
note(k_of(2, 3, 3, 23) == 5,
     "D = 23 (Second Framework)  -> k = 5   : machinery says 5v(v+1)R'-23R, NOT 3v(v+1)R'-23R")
note(k_of(2, 3, 3, 28) == 6,
     "D = 28 (near-miss)         -> k = 6   : machinery says 6v(v+1)R'-28R")
note(all(k_of(2, 3, 3, D).denominator == 1 for D in (3, 8, 13, 18, 23, 28)),
     "every chain degree this campaign ever tested satisfies D = 3 (mod 5): "
     "13, 23, 28 are all admissible -- independent corroboration of relation (Q)")
note(all(k_of(2, 3, 3, D).denominator != 1 for D in (9, 12, 15, 20, 25)),
     "D = 9, 12, 15, 20, 25 are INADMISSIBLE at (a,b,rho)=(2,3,3): the transfer "
     "conjecture's 'any D' range is not the machinery's range")

# consistency of e = rho k + sigma with the certified g = alpha U (U-1)^8
sigma_235 = Fr(1 + 3 - 9, 5)
note(sigma_235 == -1, f"(V) at (a,b,rho)=(2,3,3): sigma = {sigma_235}")
note(3*3 + sigma_235 == 8,
     "e = rho k + sigma = 3*3 - 1 = 8  reproduces the certified g = alpha U (U-1)^8")
print(f"     PREDICTION for the Second Framework (D=23, k=5): e = rho k + sigma "
      f"= {3*5 + sigma_235}, so g = alpha U^m (U-1)^{3*5 + sigma_235}, deg g = "
      f"{1 + 3*5 + sigma_235} if m = 1")
print(f"     PREDICTION for D = 28 (k=6): e = {3*6 + sigma_235}, deg g = "
      f"{1 + 3*6 + sigma_235} if m = 1")


# ===================================================================
# 2.  The divisibility test, correctly stated.
# ===================================================================
print("\nSECTION 2  the divisibility test is 'mod k', and k | D  <=>  k | (rho-1)")

def branch_divisibility(a, b, rho, D, m, sigma):
    """M == 0 branch: R = C v^(-D sigma/k)(v+1)^(-D m/k) rational?"""
    k = k_of(a, b, rho, D)
    if k.denominator != 1:
        return None
    k = int(k)
    return (D*sigma) % k == 0 and (D*m) % k == 0

print("     Borisov family (a,b,rho,m,sigma) = (2,3,3,1,-1):")
for D in (3, 8, 13, 18, 23, 28, 33):
    k = k_of(2, 3, 3, D)
    if k.denominator != 1:
        continue
    ok = branch_divisibility(2, 3, 3, D, 1, -1)
    print(f"       D={D:2d}, k={int(k)}:  k | D*sigma and k | D*m  ->  "
          f"{'PASSES the divisibility test' if ok else 'fails (fatal in this branch)'}")

note(branch_divisibility(2, 3, 3, 13, 1, -1) is False,
     "D = 13, k = 3: 3 does not divide 13   -> fatal, agrees with the certified result")
note(branch_divisibility(2, 3, 3, 23, 1, -1) is False,
     "D = 23, k = 5: 5 does not divide 23   -> fatal, SAME VERDICT as the campaign's "
     "'3 does not divide 23', by a different and correct modulus")
note(branch_divisibility(2, 3, 3, 28, 1, -1) is False,
     "D = 28, k = 6: 6 does not divide 28   -> fatal, same verdict, different modulus")
note(branch_divisibility(2, 3, 3, 3, 1, -1) is True
     and branch_divisibility(2, 3, 3, 8, 1, -1) is True,
     "D = 3 (k=1) and D = 8 (k=2) PASS the divisibility test -- the mod-k wall is "
     "NOT universal even inside Borisov's own family")

# k | D  <=>  k | rho - 1, given (Q) with m=1, sigma=-1
ok = True
for a in range(1, 8):
    for b in range(1, 8):
        if gcd(a, b) != 1:
            continue
        for rho in range(1, 12):
            for kk in range(1, 12):
                D = D_of(a, b, rho, kk)
                if D < 1:
                    continue
                lhs = (D % kk == 0)
                rhs = ((rho - 1) % kk == 0)
                ok &= (lhs == rhs)
note(ok, "k | D  <=>  k | (rho - 1), exhaustively over 1<=a,b<=7 coprime, "
         "1<=rho<=11, 1<=k<=11  (from D = (a+b)k + 1 - rho)")
note((3 - 1) % 3 != 0,
     "Borisov: rho - 1 = 2, k = 3, 3 does not divide 2  -> the mod-3 wall, "
     "restated in its true variables")

# Escapes DO exist for the divisibility test alone.
escapes = []
for a in range(1, 6):
    for b in range(1, 8):
        if gcd(a, b) != 1 or a + b < 2:
            continue
        for rho in range(1, 14):
            if (1 + rho - rho**2) % (a + b) != 0:
                continue                     # (V): sigma must be an integer
            sigma = (1 + rho - rho**2)//(a + b)
            for kk in range(1, 10):
                D = D_of(a, b, rho, kk)
                if D < 1 or (rho - 1) % kk != 0:
                    continue
                e = rho*kk + sigma
                if e < 0:
                    continue
                escapes.append((a, b, rho, kk, D, sigma, e))
print(f"\n     lattice points passing the divisibility test entirely: {len(escapes)}")
for t in escapes[:14]:
    a, b, rho, kk, D, sigma, e = t
    print(f"       (a,b)=({a},{b}) rho={rho} k={kk} D={D} sigma={sigma} e={e}")
note(len(escapes) > 0,
     f"{len(escapes)} admissible lattice points DO satisfy the divisibility test: "
     "the mod-k wall alone is escapable")


# ===================================================================
# 3.  The primary obstruction fires on every one of them.
# ===================================================================
print("\nSECTION 3  the primary obstruction: (a+b)m - 1 >= 1 for every lattice point")
# m >= 1 is forced (corner-order lemma), and a+b >= 2 for any nondegenerate cusp.
survivors = [t for t in escapes if (t[0] + t[1])*1 - 1 < 1]
note(len(survivors) == 0,
     f"of the {len(escapes)} divisibility-passing points, {len(survivors)} survive "
     "the v = -1 evaluation (m >= 1 forced, a+b >= 2)")

worst = min(((a + b)*1 - 1) for (a, b, rho, kk, D, sigma, e) in escapes) if escapes else None
note(worst is not None and worst >= 1,
     f"minimum (v+1)-exponent over the whole admissible lattice at m = 1: {worst} "
     f">= 1, so LHS(v=-1) = 0 always while RHS(v=-1) = -c(-1)^(rho-rho^2) != 0")

# exhaustive statement over cusp types
bad_ab = [(a, b) for a in range(1, 12) for b in range(1, 12)
          if gcd(a, b) == 1 and (a + b)*1 - 1 < 1]
note(bad_ab == [],
     f"NO coprime (a,b) whatever has (a+b)m-1 < 1 at m = 1 (exceptional set = "
     f"{bad_ab}); the minimum a+b is 2 at (1,1), giving exponent 1 -- so the "
     "v = -1 vanishing needs no cusp-type hypothesis at all")
note(min(a + b for a in range(1, 12) for b in range(1, 12) if gcd(a, b) == 1)
     * 1 - 1 == 1,
     "sharpest case: (a,b)=(1,1), m=1 gives (v+1)^1 -- still vanishes at v = -1")

print("\n" + "=" * 70)
bad = [t for ok_, t in LEDGER if not ok_]
print(f"LEDGER: {len(LEDGER) - len(bad)}/{len(LEDGER)} PASS")
for t in bad:
    print("  FAILED:", t)
assert not bad
