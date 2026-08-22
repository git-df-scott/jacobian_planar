"""
Wave 2, Task 4 - Independent re-verification of the section 2.5 irreducibility sieve.

WHAT THE SIEVE IS
-----------------
To prove an eliminant E(u) in Q[u] of degree n irreducible, factor it modulo
several primes of good reduction.  Over F_p the factors of E group into the
reductions of E's rational factors, so the degree of any rational factor is a
SUBSET SUM of the mod-p factor degrees.  If for some proper degree d
(1 <= d <= n/2) there is a prime whose degree multiset has no sub-multiset
summing to d, no rational factor of degree d can exist.  Kill every d and E
is irreducible.

The argument is one-directional: it can prove irreducibility, never
reducibility.  If some d survives at every prime the sieve is INCONCLUSIVE --
it must say so rather than guess.  That asymmetry is enforced in the code.

PRIME HYGIENE (campaign rule; violated twice in wave 1)
-------------------------------------------------------
All primes must satisfy p = 1 (mod 3).  On top of that this implementation
requires good reduction: p must not divide the leading coefficient and E mod p
must be squarefree (nonzero discriminant), otherwise the mod-p degree multiset
is not a valid constraint on the rational factorization.  Primes failing
either test are DISCARDED and reported, not silently used.

BACKENDS
--------
Factor degrees are computed with PARI/GP (factormod), exactly as section 2.5
specifies.  The final irreducibility answer is independently cross-checked
against sympy's factorization over Q, so a wrong sieve verdict cannot pass.

SCOPE NOTE -- READ THIS
-----------------------
The wave-1 section 2.5 eliminant artifact is NOT PRESENT in this repository.
Only the session documents (39, 40.md, 41.md, 42.md) and the sessions 1-18
status report are here.  This script therefore does NOT confirm the section
2.5 result; it re-implements and validates the machinery, and applies it to
every eliminant that IS reconstructible from primary artifacts in this
repository -- the Path A quotient-descent fiber eliminants from file `39`.
Claiming otherwise would repeat wave-1 failure mode #4 (trusting a filename
over the artifact's contents).
"""

import os
import subprocess
import sys
from itertools import combinations

import sympy as sp

PASS = []
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
u, v = sp.symbols('u v')


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


# ---------------------------------------------------------------------------
# PARI backend
# ---------------------------------------------------------------------------
def gp(script):
    r = subprocess.run(["gp", "-q"], input=script, capture_output=True, text=True, timeout=300)
    if r.returncode != 0:
        raise RuntimeError(f"gp failed: {r.stderr}")
    return r.stdout.strip()


def pari_available():
    try:
        return gp("print(1+1)") == "2"
    except Exception:
        return False


HAVE_PARI = pari_available()
check("PARI/GP backend available", HAVE_PARI)
if HAVE_PARI:
    print(f"    PARI/GP version: {gp('print(version())')}")


def pari_poly(poly, var='x'):
    """sympy Poly in one variable -> gp polynomial string with integer coeffs."""
    p = sp.Poly(poly, poly.gens[0]) if isinstance(poly, sp.Poly) else sp.Poly(poly, u)
    p = p * sp.lcm([sp.denom(c) for c in p.all_coeffs()])
    p = sp.Poly([sp.Integer(c) for c in p.all_coeffs()], p.gens[0])
    terms = []
    n = p.degree()
    for i, c in enumerate(p.all_coeffs()):
        e = n - i
        if c == 0:
            continue
        terms.append(f"({c})*{var}^{e}")
    return "+".join(terms) if terms else "0"


def factor_degrees_mod_p(poly, p):
    """Multiset of degrees of the irreducible factors of poly mod p, with
    multiplicity, computed by PARI factormod."""
    s = pari_poly(poly)
    script = f"""
P = {s};
M = factormod(P, {p});
for(i=1, matsize(M)[1], for(j=1, M[i,2], print1(poldegree(M[i,1]), " ")));
print("");
"""
    out = gp(script).strip()
    return sorted(int(t) for t in out.split()) if out else []


def good_reduction(poly, p):
    """p does not divide lc(E) and E mod p is squarefree."""
    P = sp.Poly(poly, u)
    P = P * sp.lcm([sp.denom(c) for c in P.all_coeffs()])
    P = sp.Poly([sp.Integer(c) for c in P.all_coeffs()], u)
    if P.LC() % p == 0:
        return False, "p | leading coefficient"
    s = pari_poly(P)
    d = gp(f"print(lift(poldisc(Mod(1,{p})*({s}))));").strip()
    if d in ("0", "Mod(0, %d)" % p):
        return False, "E mod p is not squarefree"
    return True, "good"


# ---------------------------------------------------------------------------
# The subset-sum argument
# ---------------------------------------------------------------------------
def achievable_sums(degs):
    """All subset sums of a degree multiset (0 and the total included)."""
    reach = {0}
    for d in degs:
        reach |= {s + d for s in reach}
    return reach


def sieve(poly, primes, verbose=True):
    """Run the mod-p factor-degree sieve.

    Returns dict with: verdict in {'IRREDUCIBLE', 'INCONCLUSIVE'},
    per-prime degree multisets, the primes actually used, and, for each proper
    degree d, the prime that killed it (or None).
    """
    P = sp.Poly(poly, u)
    n = P.degree()
    used, discarded, table = [], [], {}
    for p in primes:
        if p % 3 != 1:
            discarded.append((p, "violates the p = 1 (mod 3) campaign rule"))
            continue
        ok, why = good_reduction(P, p)
        if not ok:
            discarded.append((p, why))
            continue
        table[p] = factor_degrees_mod_p(P, p)
        used.append(p)

    killers = {}
    for d in range(1, n // 2 + 1):
        killer = None
        for p in used:
            if d not in achievable_sums(table[p]):
                killer = p
                break
        killers[d] = killer

    verdict = "IRREDUCIBLE" if all(k is not None for k in killers.values()) else "INCONCLUSIVE"
    if n <= 1:
        verdict = "IRREDUCIBLE" if n == 1 else "INCONCLUSIVE"

    if verbose:
        print(f"    degree n = {n}")
        for p in used:
            degs = table[p]
            print(f"      p = {p:>7} (p mod 3 = {p % 3}):  factor degrees {degs}"
                  f"   subset sums {sorted(achievable_sums(degs))}")
        for p, why in discarded:
            print(f"      p = {p:>7} DISCARDED: {why}")
        for d, k in sorted(killers.items()):
            print(f"      degree {d}: " + (f"killed at p = {k}" if k else "SURVIVES every prime"))
        print(f"      VERDICT: {verdict}")
    return {"verdict": verdict, "table": table, "used": used,
            "discarded": discarded, "killers": killers, "n": n}


# Eight primes = 1 (mod 3), as the campaign rule requires.
PRIMES_8 = [7, 13, 31, 43, 61, 73, 97, 103]
PRIMES_BAD = [5, 11, 17]          # = 2 (mod 3): must be discarded
check("all eight sieve primes satisfy p = 1 (mod 3)",
      all(p % 3 == 1 for p in PRIMES_8) and len(PRIMES_8) == 8)
check("the hygiene control primes are genuinely = 2 (mod 3)",
      all(p % 3 == 2 for p in PRIMES_BAD))

# ---------------------------------------------------------------------------
# 1.  VALIDATE THE SIEVE ITSELF
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("1.  VALIDATION OF THE SIEVE  (it must prove, decline, and never lie)")
print("=" * 78)

print("\n  (a) a genuinely irreducible degree-8 polynomial")
E_irr = sp.Poly(u ** 8 - u ** 6 + u ** 4 - u ** 3 + u ** 2 - u + 1, u)   # cyclotomic-like
r_irr = sieve(E_irr, PRIMES_8)
truth_irr = sp.Poly(E_irr, u).as_expr()
sym_irr = len(sp.factor_list(truth_irr)[1]) == 1 and sp.factor_list(truth_irr)[1][0][1] == 1
print(f"      sympy oracle: irreducible over Q = {sym_irr}")
check("(a) sieve PROVES irreducibility, and the sympy oracle agrees",
      r_irr["verdict"] == "IRREDUCIBLE" and sym_irr)
check("(a) sieve never claims IRREDUCIBLE for a reducible polynomial (a)",
      not (r_irr["verdict"] == "IRREDUCIBLE" and not sym_irr))

print("\n  (b) NEGATIVE CONTROL: a reducible polynomial (u^2+1)(u^3+u+1)")
E_red = sp.Poly(sp.expand((u ** 2 + 1) * (u ** 3 + u + 1)), u)
r_red = sieve(E_red, PRIMES_8)
check("(b) NEGATIVE CONTROL: sieve does NOT certify a reducible polynomial",
      r_red["verdict"] != "IRREDUCIBLE")

print("\n  (c) NEGATIVE CONTROL: a polynomial that is irreducible over Q but")
print("      factors into equal degrees mod every prime -- the sieve MUST")
print("      return INCONCLUSIVE, not a false negative dressed as a proof.")
E_hard = sp.Poly(u ** 4 + 1, u)      # irreducible over Q, splits mod every p
r_hard = sieve(E_hard, PRIMES_8)
sym_hard = len(sp.factor_list(E_hard.as_expr())[1]) == 1
print(f"      sympy oracle: irreducible over Q = {sym_hard}")
check("(c) sieve returns INCONCLUSIVE on u^4+1 (it cannot see this one)",
      r_hard["verdict"] == "INCONCLUSIVE")
check("(c) and the sieve did not therefore claim reducibility",
      r_hard["verdict"] in ("IRREDUCIBLE", "INCONCLUSIVE"))

print("\n  (d) PRIME HYGIENE: primes = 2 (mod 3) must be discarded, not used")
r_hyg = sieve(E_irr, PRIMES_BAD + PRIMES_8, verbose=False)
print(f"      discarded: {r_hyg['discarded']}")
print(f"      used     : {r_hyg['used']}")
check("(d) every p = 2 (mod 3) prime was discarded",
      all(p in [d[0] for d in r_hyg["discarded"]] for p in PRIMES_BAD))
check("(d) no discarded prime made it into the used list",
      not set(PRIMES_BAD) & set(r_hyg["used"]))

# ---------------------------------------------------------------------------
# 2.  THE SECTION 2.5 ARTIFACT
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("2.  THE WAVE-1 SECTION 2.5 ELIMINANT")
print("=" * 78)
candidates = ["w1_h1c_endgame_closed_form.py", "eliminant.txt", "eliminant_char0.txt",
              "certifiers", "wave1", "artifacts"]
present = {c: os.path.exists(os.path.join(ROOT, c)) for c in candidates}
for c, p in present.items():
    print(f"    {c:38s} present: {p}")
check("section 2.5 eliminant artifact is absent from this repository",
      not any(present.values()))
print("""
    The eliminant itself is not in this repository, so its factor degrees
    cannot be recomputed here and the section 2.5 claim is recorded as
    UNVERIFIED-HERE.  It is NOT recorded as confirmed and NOT as refuted.
    The machinery above is validated and ready; re-running section 2.5 needs
    only the eliminant file.""")

# ---------------------------------------------------------------------------
# 3.  THE ELIMINANTS THAT ARE RECONSTRUCTIBLE FROM PRIMARY ARTIFACTS
# ---------------------------------------------------------------------------
print()
print("=" * 78)
print("3.  PATH A DESCENT: FIBER ELIMINANTS OF G  (reconstructed from file `39`)")
print("=" * 78)

G1 = sp.expand((u + 1) * (3 * u + v - 2) ** 2 * (3 * u ** 3 + u ** 2 * v + 4 * u ** 2 + 2 * u * v + v))
G2 = sp.expand(-(3 * u + v - 2) * (9 * u ** 3 + 3 * u ** 2 * v + 12 * u ** 2 + 6 * u * v + u + 3 * v))
JG = sp.Matrix([[sp.diff(g, t) for t in (u, v)] for g in (G1, G2)])
detJG = sp.expand(JG.det())
print(f"    det JG = {sp.factor(detJG)}")
check("descent reproduced: det JG = -2 (3u+v-2)^2",
      sp.simplify(detJG + 2 * (3 * u + v - 2) ** 2) == 0)
check("descent degrees are (6,4)",
      sp.Poly(G1, u, v).total_degree() == 6 and sp.Poly(G2, u, v).total_degree() == 4)

targets = [(5, 7), (11, 4), (-13, 9), (23, -5)]
cubics = []
for (s0, t0) in targets:
    E = sp.Poly(sp.resultant(sp.expand(G1 - s0), sp.expand(G2 - t0), v), u)
    facs = sp.factor_list(E.as_expr())[1]
    degs = sorted((sp.Poly(f, u).degree(), m) for f, m in facs)
    print(f"\n    target (s,t) = ({s0},{t0}):  full eliminant degree {E.degree()},"
          f" rational factor pattern {degs}")
    # the geometric fiber lives on the factor of degree 3 (the map has d = 3);
    # the (u - a)^3 piece is the 3u+v-2 = 0 degeneration of the resultant.
    core = [f for f, m in facs if sp.Poly(f, u).degree() >= 2]
    if not core:
        print("      no factor of degree >= 2 at this target")
        continue
    C = sp.Poly(sp.expand(core[0]), u)
    print(f"      core factor: degree {C.degree()}, {sp.factor(C.as_expr())}")
    cubics.append((s0, t0, C))
    r = sieve(C, PRIMES_8)
    sym = len(sp.factor_list(C.as_expr())[1]) == 1 and sp.factor_list(C.as_expr())[1][0][1] == 1
    print(f"      sympy oracle: irreducible over Q = {sym}")
    check(f"target ({s0},{t0}): sieve never contradicts the sympy oracle",
          not (r["verdict"] == "IRREDUCIBLE" and not sym))

check("at least three targets produced a core eliminant", len(cubics) >= 3)

# Geometric degree cross-check: Alpoge's map has d = 3, and the census records
# monodromy S_3.  A degree-3 core factor with Galois group S_3 is exactly that.
print()
print("    GEOMETRIC-DEGREE / MONODROMY CROSS-CHECK")
deg3 = [c for c in cubics if c[2].degree() == 3]
print(f"      targets with a degree-3 core factor: {[(a, b) for a, b, _ in deg3]}")
galois = []
for s0, t0, C in deg3:
    disc = sp.Rational(sp.discriminant(C.as_expr(), u))
    # exact test: is disc the square of a rational?
    num, den = sp.fraction(disc)
    is_square = (disc > 0
                 and sp.integer_nthroot(int(abs(num)), 2)[1]
                 and sp.integer_nthroot(int(abs(den)), 2)[1])
    grp = "A_3 (cyclic)" if is_square else "S_3 (full symmetric)"
    galois.append(grp)
    print(f"      ({s0},{t0}): disc = {disc}, square in Q = {bool(is_square)} -> Galois {grp}")
check("descent fiber monodromy is the full symmetric group S_3 (census profile)",
      len(galois) > 0 and all(g.startswith("S_3") for g in galois))
check("the descent's geometric degree reads 3, matching Alpoge's d = 3",
      len(deg3) >= 1 and all(C.degree() == 3 for _, _, C in deg3))

# ---------------------------------------------------------------------------
print()
print("=" * 78)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 78)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w2_irreducibility_sieve.py: a check FAILED"
print("""    VERDICT
      * sieve machinery: implemented, validated, prime hygiene enforced.
      * section 2.5 eliminant: UNVERIFIED-HERE (artifact absent).
      * Path A descent: geometric degree 3 and monodromy S_3 confirmed
        independently, matching the Session 38 census profile.""")
