"""
Wave 2, Task 2 - Is the pole at v = -1 admissible?  (Is the H1c break load-bearing?)

QUESTION
--------
w2_h1c_refutation.py showed the k >= 1 leg of H1c is false for *rational* R.
It is true for *polynomial* R.  So everything turns on one question:

    Does the campaign's endgame residue R genuinely range over rational
    functions with a possible pole at v = -1, or is it pinned to be a
    polynomial by an argument that is independent of the endgame step?

METHOD
------
Pure reading of the campaign's own primary artifacts in this repository.
No paraphrase is trusted: every load-bearing sentence is located by exact
substring match against the file on disk, and the script FAILS if an anchor
is missing (that is the guard against failure mode #4 -- trusting a filename
or a summary over the artifact's contents).

Primary artifacts present in this repository:
    "Sessions 1-18 status reports"   (sessions 1-18, the endgame chain)
    39, 40.md, 41.md, 42.md          (sessions 39-42 path documents)
"""

import os
import re

PASS = []
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def check(name, value, expected=True):
    ok = bool(value) == bool(expected)
    PASS.append((name, ok))
    return ok


def load(fn):
    with open(os.path.join(ROOT, fn), 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


STATUS = "Sessions 1-18 status reports"
try:
    text = load(STATUS)
except FileNotFoundError:
    text = ""
check(f"primary artifact '{STATUS}' is present and readable", len(text) > 1000)


def anchor(label, needle, corpus=None):
    """Locate an exact quotation.  Fails loudly if the artifact does not say it."""
    src = corpus if corpus is not None else text
    found = needle in src
    check(f"ANCHOR {label}", found)
    if found:
        i = src.index(needle)
        line = src[:i].count("\n") + 1
        print(f"    [{label}]  {STATUS}:{line}")
        for ln in needle.strip().splitlines():
            print(f"        | {ln.strip()}")
    else:
        print(f"    [{label}]  *** NOT FOUND -- claim cannot be sourced ***")
    print()
    return found


print("=" * 74)
print("A.  WHAT THE CAMPAIGN SAYS ABOUT R's POLES")
print("=" * 74)
print()

# A1 - the endgame equation itself, with the (v+1)^4 factor and D = 13.
anchor("EQN", "alpha^5 (v+1)^4 (3v(v+1) R' - 13 R) = -c.")

# A2 - the step that the refutation attacks.
anchor("EVAL", "The left side vanishes at v = -1; the right\nside is -c != 0.")

# A3 - the polynomiality claim that rescues the step.
anchor("POLY", "The realization theory (Sessions 13-14) makes R a polynomial (the\npole-fiber argument).")

# A4 - Theorem 3, the pole-fiber argument, in full.
anchor("THM3", "THEOREM 3 (pole-fiber).  R = 2 v^39 (A~_4 - g^3 S_13)/g^3 has poles\nconfined to {v = 0, v = -1}")

# A5 - Session 11 already demands polynomiality of R from the Belyi realization.
anchor("BELYI", "must be a polynomial of degree exactly 13 realizing the certified\n   degree-13 Belyi map (marked corners respected).")

# A6 - the machine check that is on record, and its scope.
anchor("LEDGER", "[PASS] endgame operator T(R) = (v+1)^4 (3v(v+1)R'-13R):\n         kernel trivial (rank 14), T(R) = 1 infeasible    (exact LA)")

# A7 - the transfer conjecture, which is where polynomiality is NOT established.
anchor("TRANSFER", "TRANSFER CONJECTURE (next target).  For chain degree D the same\nmechanism yields 3v(v+1)R' = D R, fatal whenever D/3 is not an\ninteger.  Second Framework: D = 23.")

# A8 - the campaign's own conditionality statement.
anchor("DEPEND", "Dependence: our formalization of the framework's conditions")

print("=" * 74)
print("B.  READING")
print("=" * 74)
print("""
B1.  Inside the First Framework at D = 13, R is NOT free to have a pole at
     v = -1.  Two independent statements pin it:

       * Session 11 requires R = v^39 * W~_-5(U)/g(U)^6 to be a POLYNOMIAL
         of degree exactly 13 realizing a degree-13 Belyi map.  That is a
         framework hypothesis (Borisov's First Framework demands the
         degree-13 chain realization), not a consequence of the endgame.

       * Session 13's THEOREM 3 confines R's poles to {v = 0, v = -1}, then
         argues from the Belyi-13 fiber sizes (13/9/5/1) that a pole set of
         at most two points must be the 1-point fiber, hence at v = infinity;
         the forced divisibilities close v = 0.

     Therefore, FOR THE (99,66) FIRST FRAMEWORK, the v = -1 evaluation is
     legal and the Sessions 16-18 conclusion survives the H1c break.
     The break is an error in the *statement* of H1c, not in that verdict.

B2.  The ledger check confirms only the polynomial case.  "rank 14" is the
     rank over polynomials of degree <= 13 -- 14 coefficients.  Nothing in
     the recorded certification tests rational R.  So the ledger is
     consistent with the refutation: it never claimed what H1c claimed.

B3.  WHERE THE BREAK IS LOAD-BEARING: the TRANSFER CONJECTURE.
     The transfer step propagates only the endgame mechanism
     "3v(v+1)R' = D R fatal whenever D/3 is not an integer" to D = 23 and to
     the isotope series.  Polynomiality of R at those D is NOT established
     in this repository -- the campaign's own text hedges it as
     "If their rigidity layers hold analogously".  Any D = 23 or isotope
     verdict that leans on the k >= 1 evaluation argument WITHOUT first
     re-proving the analogue of Theorem 3 is invalid, because
     w2_money_cells.py exhibits explicit rational solutions at D = 23.

B4.  Consequently H1c as stated -- a claim over rational R, at all D and all
     k >= 1 -- is exactly the over-generalisation that the transfer step
     needs and does not have.  It embarrasses the D = 13 write-up; it
     genuinely blocks the transfer.
""")

print("=" * 74)
print("C.  THE STANDING CONTRADICTION (item 11), RESOLVED FROM THE ARTIFACT")
print("=" * 74)
found_dep = "Dependence: our formalization of the framework's conditions" in text
found_owed = "A referee-grade writeup of the\n    Y-side geometry is owed before public claims" in text
print(f"""
    Two mutually exclusive labels were left standing in the wave-1 STATUS:
        (i)  First Framework "PROVEN dead, unconditional"
        (ii) First Framework "conditional on unreproduced THEOREM 2/3"

    The primary artifact settles it.  Sessions 16-18 itself records, under
    'SCOPE AND HONEST LABELS', a Dependence clause on the campaign's own
    formalization of the framework conditions ({'present' if found_dep else 'MISSING'}), and states that a
    referee-grade writeup is owed before public claims ({'present' if found_owed else 'MISSING'}).

    => (ii) is correct.  (i) is false.  The First Framework result is
       CONDITIONAL on the campaign's formalization of layers 1-3, the
       realization theory and the rigidity theorem, none of which is
       independently reproduced.  STATUS must carry label (ii) only.
""")
check("contradiction item 11 resolved against 'unconditional'", found_dep and found_owed)

print("=" * 74)
print("D.  VERDICT")
print("=" * 74)
print("""
    POLE ADMISSIBILITY:  NOT admissible at D = 13 inside the First
    Framework (Theorem 3 + the Belyi-13 realization pin R polynomial);
    ADMISSIBLE, i.e. unproven-to-be-excluded, everywhere the transfer
    conjecture reaches -- D = 23, the isotope series, and every framework
    whose rigidity layer has not been re-derived.

    LOAD-BEARING:  YES, for the transfer conjecture.  NO, for the (99,66)
    First Framework emptiness verdict, which stands on Theorem 3 instead.

    ACTION:  H1c must be restated with the hypothesis "R polynomial", and
    every downstream use must discharge that hypothesis explicitly.
""")

print("=" * 74)
for name, ok in PASS:
    print(("    PASS  " if ok else "    FAIL  ") + name)
print("=" * 74)
print(f"    {sum(1 for _, ok in PASS if ok)}/{len(PASS)} checks passed")
assert all(ok for _, ok in PASS), "w2_pole_admissibility.py: an anchor could not be sourced"
