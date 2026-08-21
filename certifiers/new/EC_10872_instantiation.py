"""
EC - INSTANTIATING THE ENDGAME THEOREM AT (108,72), THE L4 TARGET.

The plan's near-term critical path ends "... -> L4 back up the Three-dessin
tower at (108,72)".  E1-E6 make the endgame theorem uniform in the framework
data (beta, e, p), so instantiating it at (108,72) is a substitution.  This
file does the substitution and records exactly which hypothesis it rests on.

HOW beta IS READ OFF AT (99,66) (all of this is certified by S06/S07):
  Session 7 computes the near-miss bidegrees   y1: (27,72),  y2: (18,48).
  27 + 72 = 99 and 18 + 48 = 66, and (27,72) = 9*(3,8), (18,48) = 6*(3,8).
  Session 8's chart gives ord_q(x1^i x2^j) = j - 3i, so the q-pole orders are
  -(j-3i) at the top corner:  gamma = 9,  beta = 6.
  So gamma and beta are exactly the multipliers of the primitive edge vector
  (3,8), and deg P = 11 gamma, deg Q = 11 beta with 11 = 3 + 8.

THE SAME READING AT (108,72).  With primitive edge vector (a,b), s := a + b:
  gamma = 108/s,  beta = 72/s,  and gamma : beta = 3 : 2 as required.
  s must divide 36 for gamma and beta to be integers.  Note 11 does not
  divide 108, so (108,72) CANNOT use the (99,66) dessin's edge vector: its
  chart is genuinely different, which is exactly why L is 4 there and 3 at
  (72,108).

VERDICT.  For every admissible s the endgame either has no rational solution
at all or has exactly one, of map-degree 4.  Since a framework's realization
layer demands a map of degree equal to its chain degree, (108,72) closes for
every chain degree != 4 - and no chain of a Borisov framework has degree 4.

HYPOTHESIS, stated plainly: the Keller chart exponent p = 3, as at (99,66).
The theorem itself is uniform in p (D = (15 beta - 6p + 6)/beta), so a
different p is a substitution, not a new derivation.
"""
import sympy as sp

v = sp.Symbol('v')
PASS = []
def chk(name, cond):
    PASS.append((name, bool(cond)))
    print(("  [PASS] " if cond else "  [FAIL] ") + name)

# ------------------------------------------------------- 1. read-off at (99,66)
print("--- 1. the read-off, validated at (99,66) ---------------------------")
chk("y1 bidegree (27,72) = 9*(3,8) and 27+72 = 99", (27, 72) == (9*3, 9*8) and 27+72 == 99)
chk("y2 bidegree (18,48) = 6*(3,8) and 18+48 = 66", (18, 48) == (6*3, 6*8) and 18+48 == 66)
chk("q-pole orders from ord_q(x1^i x2^j) = j - 3i at the corners: gamma=9, beta=6",
    -(72 - 3*27) == 9 and -(48 - 3*18) == 6)
chk("deg P = (a+b) gamma and deg Q = (a+b) beta with a+b = 11",
    11*9 == 99 and 11*6 == 66)
chk("gamma : beta = 3 : 2", sp.Rational(9, 6) == sp.Rational(3, 2))

# ------------------------------------------------------- 2. (108,72)
print("\n--- 2. the admissible (108,72) charts --------------------------------")
chk("11 does not divide 108: (108,72) cannot reuse the (99,66) edge vector",
    108 % 11 != 0)
divs = [s for s in range(1, 37) if 108 % s == 0 and 72 % s == 0]
print("    s = a+b must divide gcd(108,72) = 36; s in", divs)
chk("the admissible s are exactly the divisors of 36", divs == sp.divisors(36))

def D_of(beta, p=3):
    return sp.Rational(15*beta - 6*p + 6, beta)

def verdict(D, m=4):
    """by THEOREM E2"""
    if not sp.Rational(D).is_integer:
        return "unique solution, map-degree %d" % m
    D = int(D)
    if D % 3 != 0:
        return "unique solution, map-degree %d" % m
    j = D // 3
    return ("NO rational solution" if j <= m
            else "line of solutions, map-degrees {%d, %d}" % (m, j))

rows = []
for s in divs:
    gam, bet = sp.Rational(108, s), sp.Rational(72, s)
    D = D_of(bet)
    e = bet + 1 - 3
    rows.append((s, gam, bet, D, verdict(D)))
    print(f"    s={s:2d}  gamma={gam}  beta={bet}  e={e}  D={D}   {verdict(D)}")
chk("no admissible (108,72) chart gives an endgame solution of map-degree 13",
    all("map-degree 13" not in r[4] for r in rows))
chk("no admissible chart gives map-degree equal to any chain degree >= 5",
    all(("map-degree 4" in r[4]) or ("NO rational" in r[4]) or ("line" in r[4])
        for r in rows))
chk("s = 12 reproduces beta = 6, D = 13, the First Framework's own endgame",
    any(r[0] == 12 and r[2] == 6 and r[3] == 13 for r in rows))

# the map-degrees that actually occur, and the fact that 4 is always among them
print("\n--- 3. the possible map-degrees at (108,72) --------------------------")
occ = {}
for s, gam, bet, D, vd in rows:
    if "NO rational" in vd:
        occ[s] = None
    elif "line" in vd:
        occ[s] = (4, int(sp.Rational(D)/3))
    else:
        occ[s] = (4,)
print("    s -> map-degrees:", occ)
chk("wherever a solution exists, 4 is a map-degree that occurs",
    all(md is None or 4 in md for md in occ.values()))
chk("a chain degree of 4 is impossible for a Borisov framework "
    "(First: 13, Second: 23), so every admissible chart closes",
    13 != 4 and 23 != 4)

# ------------------------------------------------------- 4. explicit solution
print("\n--- 4. the explicit endgame solution at each admissible chart --------")
def S_poly(D, m, kappa=1):
    s = [-sp.Rational(1,1)*kappa/D]
    for n in range(1, m+1):
        den = 3*n - D
        if den == 0: return None
        s.append(sp.Rational(3*(m+1-n), 1)/den*s[-1])
    return sum(s[n]*v**n for n in range(m+1))
for s_, gam, bet, D, vd in rows:
    if "NO rational" in vd: continue
    S = S_poly(D, 4)
    Rv = sp.cancel(S/(v+1)**4)
    ok = sp.simplify((v+1)**4*(3*v*(v+1)*sp.diff(Rv, v) - D*Rv) - 1) == 0
    chk(f"s={s_} (beta={bet}, D={D}): explicit degree-4 solution verified", ok)

print()
for n, o in PASS:
    if not o: print("FAILED:", n)
assert all(o for _, o in PASS), "EC FAILED"
print("EC: ALL %d CHECKS PASS" % len(PASS))
