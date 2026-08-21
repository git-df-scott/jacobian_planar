"""
jc2_degree_lattice_literature_check.py

Exact-arithmetic sanity checks supporting the Session 20 literature review
of published degree-pair restrictions on a hypothetical plane Jacobian
counterexample (P, Q), (d1, d2) = (deg P, deg Q).

This script does NOT establish any new mathematical result. It only
verifies, with exact integer arithmetic (sympy / fractions, no floats),
numeric claims quoted from the literature during the review, so that
every gcd / primality / divisibility / membership claim in the writeup
is checked rather than asserted from memory.

Sources (see session20_degree_lattice_report for full citations):
  [Moh83]  T.T. Moh, J. Reine Angew. Math. 340 (1983), 140-212.
  [GGHV22] Guccione, Guccione, Horruitiner, Valqui, arXiv:2204.14178.
  [Mos18]  V. Moskowicz, arXiv:1810.08202 (states Theorem 1.1/1.2 with
           attributions to Magnus 1955, Nakai-Baba 1977,
           Appelgate-Onishi 1985 + Nagata 1989/1990, Zoladek 2008).
  [Bor19]  A. Borisov, arXiv:1901.04073 ("Frameworks for two-dimensional
           Keller maps"), Remark 3.1 and the k=2..6 family, eq. near
           line 1161 of the extracted text ("(99,66),(135,90),...").
  [GGHV17] Guccione, Guccione, Horruitiner, Valqui, arXiv:1708.09367
           (gcd(d1,d2) >= 36 claim, quoted via [Mos18] section 4 --
           NOT independently verified against the primary source; see
           report for the honesty flag on this one item).
"""
from sympy import gcd, isprime, factorint, Rational

def is_semiprime(n):
    """n is a product of exactly two primes (with multiplicity), i.e. n in P^2."""
    f = factorint(n)
    return sum(f.values()) == 2

def in_2P(n):
    return n % 2 == 0 and isprime(n // 2)

def in_4P(n):
    return n % 4 == 0 and isprime(n // 4)

def classical_gcd_set_membership(n):
    """Theorem 1.1 (Magnus / Nakai-Baba / Appelgate-Onishi+Nagata / Zoladek):
    gcd in {1,8} u P u 2P => automorphism."""
    return n == 1 or n == 8 or isprime(n) or in_2P(n)

def theorem_1_2_membership(n):
    """Theorem 1.2: deg in P u P^2 u 4P => automorphism."""
    return isprime(n) or is_semiprime(n) or in_4P(n)

checks = []

def record(name, cond, detail):
    checks.append((name, bool(cond), detail))

# ---------------------------------------------------------------
# 1. The four "hard" pairs from Guccione et al. 2022 (max < 125),
#    listed in their abstract: (56,84), (66,99), (72,108) x2, (80,120).
# ---------------------------------------------------------------
hard_pairs = {
    "(56,84)":  (56, 84),
    "(66,99)":  (66, 99),
    "(72,108)": (72, 108),
    "(80,120)": (80, 120),
}

for name, (a, b) in hard_pairs.items():
    g = int(gcd(a, b))
    record(f"{name}: gcd={g}",
           True,
           f"gcd({a},{b})={g}; classical-gcd-set membership (Thm 1.1) = "
           f"{classical_gcd_set_membership(g)}; a|b={b % a == 0}; b|a={a % b == 0}")

# All four historically-hard pairs must have ratio 2:3 exactly (a:b = 2:3),
# i.e. correspond to a (2,3)-cusp / gcd(a,b) = a/2 = b/3.
for name, (a, b) in hard_pairs.items():
    ratio_ok = Rational(a, b) == Rational(2, 3)
    record(f"{name}: ratio is exactly 2:3", ratio_ok, f"{a}/{b} == 2/3 -> {ratio_ok}")

# Neither a|b nor b|a for the still-open pair (72,108) -- must be false for
# both, else the classical divisibility reduction alone would already kill it.
a, b = 72, 108
record("(72,108): neither divides the other",
       (b % a != 0) and (a % b != 0),
       f"72 | 108 = {108 % 72 == 0}; 108 | 72 = {72 % 108 == 0}")

# ---------------------------------------------------------------
# 2. Theorem 1.1 / 1.2 do NOT already resolve (72,108) or (66,99)
#    (if they did, the dedicated Newton-polygon papers would be moot).
# ---------------------------------------------------------------
for name, (a, b) in [("(66,99)", (66, 99)), ("(72,108)", (72, 108))]:
    g = int(gcd(a, b))
    t11 = classical_gcd_set_membership(g)
    t12 = theorem_1_2_membership(a) or theorem_1_2_membership(b)
    record(f"{name}: Thm 1.1 inapplicable (gcd not in {{1,8}} u P u 2P)",
           not t11, f"gcd={g}, factorint(gcd)={factorint(g)}")
    record(f"{name}: Thm 1.2 inapplicable (neither degree in P u P^2 u 4P)",
           not t12,
           f"deg a={a} factorint={factorint(a)} semiprime={is_semiprime(a)}; "
           f"deg b={b} factorint={factorint(b)} semiprime={is_semiprime(b)}")

# ---------------------------------------------------------------
# 3. gcd(72,108) = 36 sits exactly at the boundary of the quoted
#    "gcd(d1,d2) >= 36" heuristic bound from [GGHV17] (via [Mos18] Sec 4).
# ---------------------------------------------------------------
record("gcd(72,108) == 36 (the quoted general lower bound)",
       int(gcd(72, 108)) == 36, f"gcd(72,108) = {int(gcd(72,108))}")

# The two named exceptions to that gcd>=36 heuristic, per [Mos18] Sec 4:
for name, (a, b) in [("(75,125)", (75, 125)), ("(64,224)", (64, 224))]:
    g = int(gcd(a, b))
    record(f"{name}: gcd={g} < 36 (named exception to the gcd>=36 heuristic)",
           g < 36, f"gcd({a},{b}) = {g}")
    record(f"{name}: max{{a,b}} >= 125 (already outside the <125 frontier)",
           max(a, b) >= 125, f"max({a},{b}) = {max(a,b)}")

# ---------------------------------------------------------------
# 4. (99,66) is itself NOT one of the two named exceptions, so if the
#    gcd>=36 theorem's hypotheses applied to it unconditionally, it would
#    already be excluded that way (gcd=33<36). This is flagged as an
#    UNVERIFIED tension in the report (we did not read the 2017 primary
#    source directly), not used as a certification.
# ---------------------------------------------------------------
record("(99,66): gcd=33 < 36 and NOT in the named exception list "
       "{(75,125),(64,224)} -- flag only, not relied upon",
       int(gcd(99, 66)) == 33, f"gcd(99,66) = {int(gcd(99,66))}")

# ---------------------------------------------------------------
# 5. Borisov's k=2..6 family (36k+27, 24k+18), First-Framework-type
#    frameworks; check the printed values and which fall below the
#    current max<125 frontier.
# ---------------------------------------------------------------
borisov_family = {k: (36 * k + 27, 24 * k + 18) for k in range(2, 7)}
expected = {
    2: (99, 66), 3: (135, 90), 4: (171, 114), 5: (207, 138), 6: (243, 162),
}
for k in range(2, 7):
    computed = borisov_family[k]
    record(f"Borisov family k={k}: (36k+27,24k+18) = {computed}",
           computed == expected[k], f"expected {expected[k]}, got {computed}")
    g = int(gcd(*computed))
    ratio_ok = Rational(computed[1], computed[0]) == Rational(2, 3)
    record(f"Borisov family k={k}: ratio deg2:deg1 == 2:3, gcd={g}",
           ratio_ok, f"{computed}, gcd={g}, ratio={Rational(computed[1],computed[0])}")
    record(f"Borisov family k={k}: below current <125 frontier only for k=2",
           (max(computed) < 125) == (k == 2),
           f"max{computed} = {max(computed)}")

# ---------------------------------------------------------------
# 6. Reconstruction of the FULL 10-case table of [GGHV22] Section 2
#    from (A0, (m,n), max) -> actual (deg P, deg Q), using the rule
#    "the pair is the unique integer multiple of (m,n) whose max
#    component equals the table's max{deg P, deg Q} value". Cross-
#    checked against every pair the paper states explicitly in prose
#    (56,84),(66,99),(72,108),(80,120),(80,112).
# ---------------------------------------------------------------
table_rows = [
    # (A0, (m,n), max_deg, discarded_by)
    ((4, 12), (3, 4), 64,  "Moh 1983 (full detail) + Heitmann 1990 (independent)"),
    ((4, 12), (5, 7), 112, "Guccione-Guccione-Valqui, Pro Mathematica 2013, Sec 3.5"),
    ((5, 20), (2, 3), 75,  "Guccione-Guccione-Valqui arXiv:1406.0886 Sec 5"),
    ((5, 20), (3, 2), 75,  "Guccione-Guccione-Valqui arXiv:1406.0886 Sec 5"),
    ((7, 21), (2, 3), 84,  "GGHV22 Sec 3 (via [6, Thm 7.3]) and Sec 6 (2nd proof)"),
    ((8, 24), (2, 3), 96,  "Guccione et al. arXiv:1708.07936, Prop 6.1"),
    ((8, 28), (3, 2), 108, "OPEN -- system of polynomial equations unsolved [GGHV22]"),
    ((8, 32), (3, 2), 120, "GGHV22 Sec 3 (via [2, Remark 3.31])"),
    ((9, 24), (2, 3), 99,  "GGHV22 Sec 5, Thm 5.1 / Cor 5.7 (Moh's pair)"),
    ((9, 27), (2, 3), 108, "GGHV22 Sec 5, Thm 5.1 / Cor 5.7"),
]

# explicit pairs GGHV22 states in prose, used only to cross-check the
# reconstruction rule below (not used to derive it):
known_pairs_from_prose = {64: None, 112: (80, 112), 75: (50, 75),
                           84: (56, 84), 96: None, 108: (72, 108),
                           120: (80, 120), 99: (66, 99)}

print("\n--- Reconstructed full <125 table ---")
for A0, (m, n), maxdeg, who in table_rows:
    scale = Rational(maxdeg, max(m, n))
    pair = (scale * m, scale * n)
    is_int = pair[0].q == 1 and pair[1].q == 1
    record(f"A0={A0} (m,n)=({m},{n}) max={maxdeg}: reconstructed pair {pair}",
           is_int, f"scale={scale}, pair={pair}, discarded by: {who}")
    kp = known_pairs_from_prose.get(maxdeg)
    if kp is not None:
        match = (int(pair[0]), int(pair[1])) in (kp, (kp[1], kp[0]))
        record(f"  cross-check vs prose-stated pair {kp} for max={maxdeg}",
               match, f"reconstructed {pair} vs prose {kp}")
    print(f"  A0={A0} (m,n)=({m},{n}) max={maxdeg} -> pair={tuple(int(x) for x in pair)}  [{who}]")

# ---------------------------------------------------------------
# Report
# ---------------------------------------------------------------
n_pass = sum(1 for _, ok, _ in checks if ok)
n_fail = len(checks) - n_pass
for name, ok, detail in checks:
    status = "PASS" if ok else "FAIL"
    print(f"[{status}] {name}\n        {detail}")

print(f"\n{n_pass} PASS, {n_fail} FAIL out of {len(checks)} checks "
      f"(exact sympy Rational/integer arithmetic throughout, no floats).")
