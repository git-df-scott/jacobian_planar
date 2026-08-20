"""
Wave 3 - The claim ledger, and the linter that makes contradictions impossible
to leave standing.

WHY
---
Wave 1 left two mutually exclusive labels on the same claim ("PROVEN dead,
unconditional" vs "conditional on unreproduced THEOREM 2/3") in two different
files, and nobody noticed because nothing was checking.  It also recorded
theorems without their hypotheses (H1c: "for rational R" when the proof needed
"for polynomial R"; Session 38: "weighted-homogeneous forces diagonal linear"
when the sweep had a > 0 > b built in).  Both are the same bug: a claim stored
as prose has no machine-checkable structure, so nothing can detect that it
contradicts another claim or that it has outrun its own hypotheses.

WHAT THIS IS
------------
Every campaign claim is stored as a record with:

    key        stable identifier; two records with the same key MUST agree
    statement  the claim
    domain     the EXACT quantifier domain -- what it ranges over
    label      one of PROVED, DERIVED, ASSERTED, REFUTED, UNVERIFIED, CONDITIONAL
    evidence   (script, check-name) pointing at an executable check, or None
    depends    keys this claim rests on

and the linter enforces:

    L1  no two records with the same key carry incompatible labels
    L2  PROVED and REFUTED require an evidence pointer
    L3  PROVED requires a stated domain that is not the string "unrestricted"
        unless a domain probe exists -- a recorded input just OUTSIDE the
        intended domain on which the claim is required to fail
    L4  no claim may depend on a REFUTED claim
    L5  a CONDITIONAL claim must name what it is conditional on
    L6  every evidence pointer must name a script that exists on disk
    L7  a WITHDRAWN claim must record why it was withdrawn.  WITHDRAWN is the
        honest label for a claim retracted on external authority rather than by
        an in-repository artifact -- it must never be dressed up as REFUTED,
        which the linter requires evidence for.

The linter exits nonzero on any violation.  It is self-tested: a synthetic
ledger containing one instance of each violation must produce exactly six
findings.
"""

import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LABELS = {"PROVED", "DERIVED", "ASSERTED", "REFUTED", "UNVERIFIED",
          "CONDITIONAL", "WITHDRAWN"}
INCOMPATIBLE = {frozenset({"PROVED", "REFUTED"}),
                frozenset({"PROVED", "UNVERIFIED"}),
                frozenset({"PROVED", "CONDITIONAL"}),
                frozenset({"PROVED", "ASSERTED"}),
                frozenset({"REFUTED", "DERIVED"}),
                frozenset({"REFUTED", "CONDITIONAL"})}


def claim(key, statement, domain, label, evidence=None, depends=(), probe=None,
          conditional_on=None, withdrawn_reason=None):
    return dict(key=key, statement=statement, domain=domain, label=label,
                evidence=evidence, depends=tuple(depends), probe=probe,
                conditional_on=conditional_on, withdrawn_reason=withdrawn_reason)


def lint(ledger, root=ROOT):
    findings = []
    by_key = {}
    for r in ledger:
        by_key.setdefault(r["key"], []).append(r)

    for key, rs in by_key.items():
        labels = {r["label"] for r in rs}
        for bad in INCOMPATIBLE:
            if bad <= labels:
                findings.append(("L1", key, f"incompatible labels {sorted(bad)} on one key"))
        for r in rs:
            if r["label"] not in LABELS:
                findings.append(("L0", key, f"unknown label {r['label']}"))
            if r["label"] in ("PROVED", "REFUTED") and not r["evidence"]:
                findings.append(("L2", key, f"{r['label']} with no evidence pointer"))
            if r["label"] == "PROVED":
                if (not r["domain"]) or r["domain"].strip().lower() == "unrestricted":
                    if not r["probe"]:
                        findings.append(("L3", key,
                                         "PROVED with unrestricted/empty domain and no domain probe"))
            if r["label"] == "CONDITIONAL" and not r["conditional_on"]:
                findings.append(("L5", key, "CONDITIONAL without naming the condition"))
            if r["label"] == "WITHDRAWN" and not r["withdrawn_reason"]:
                findings.append(("L7", key, "WITHDRAWN without recording why"))
            if r["evidence"]:
                script = r["evidence"][0]
                if not os.path.exists(os.path.join(root, script)):
                    findings.append(("L6", key, f"evidence script missing: {script}"))

    refuted = {k for k, rs in by_key.items() if any(r["label"] == "REFUTED" for r in rs)}
    for r in ledger:
        for d in r["depends"]:
            if d in refuted:
                findings.append(("L4", r["key"], f"depends on REFUTED claim {d}"))
    return findings


# ---------------------------------------------------------------------------
# SELF-TEST: a synthetic ledger with exactly one of each violation.
# ---------------------------------------------------------------------------
SYNTH = [
    claim("dup", "s", "all x", "PROVED", ("wave3/w3_claim_ledger.py", "c")),
    claim("dup", "s", "all x", "REFUTED", ("wave3/w3_claim_ledger.py", "c")),   # L1
    claim("noev", "s", "all x", "PROVED"),                                       # L2 (+L3? no, domain set)
    claim("nodom", "s", "unrestricted", "PROVED", ("wave3/w3_claim_ledger.py", "c")),  # L3
    claim("dep", "s", "all x", "DERIVED", ("wave3/w3_claim_ledger.py", "c"), depends=("dup",)),  # L4
    claim("cond", "s", "all x", "CONDITIONAL", ("wave3/w3_claim_ledger.py", "c")),     # L5
    claim("miss", "s", "all x", "REFUTED", ("wave3/does_not_exist.py", "c")),          # L6
    claim("wd", "s", "all x", "WITHDRAWN"),                                           # L7
]
synth_findings = lint(SYNTH)
codes = sorted({f[0] for f in synth_findings})
print("=" * 78)
print("SELF-TEST OF THE LINTER")
print("=" * 78)
for f in synth_findings:
    print(f"    {f[0]}  {f[1]}: {f[2]}")
expected_codes = ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]
selftest_ok = codes == expected_codes
print(f"    codes found: {codes}   expected: {expected_codes}   "
      f"self-test {'PASS' if selftest_ok else 'FAIL'}")

# A clean synthetic ledger must produce ZERO findings, or the linter is
# trivially "finding" things.
CLEAN = [claim("ok", "s", "all rational R with a pole at v=-1", "PROVED",
               ("wave3/w3_claim_ledger.py", "c"), probe="D=6,k=1")]
clean_ok = lint(CLEAN) == []
print(f"    clean ledger produces {len(lint(CLEAN))} findings   "
      f"(must be 0): {'PASS' if clean_ok else 'FAIL'}")

# ---------------------------------------------------------------------------
# THE CAMPAIGN LEDGER
# ---------------------------------------------------------------------------
LEDGER = [
    claim("H1C-K>=1",
          "For c != 0 and k >= 1 there is no rational R with "
          "(v+1)^k (3v(v+1)R' - D R) = -c",
          "all rational R, all D, all k >= 1",
          "REFUTED",
          ("wave2/w2_h1c_refutation.py", "D=6,k=1: R=c/(6(v+1)^2) satisfies T(R) = -c exactly")),

    claim("H1C-POLY",
          "The same statement with R restricted to POLYNOMIALS",
          "polynomial R only",
          "PROVED",
          ("wave2/w2_h1c_refutation.py", "CHECK P: no POLYNOMIAL solution for any tested (D,k) with k >= 1"),
          probe="rational R with a pole at v = -1, on which the claim fails"),

    claim("W2-1",
          "(v+1)^k (3v(v+1)R' - D R) = -c has a rational solution iff "
          "D is not in {3, 6, ..., 3k}",
          "integer D >= 1, integer k >= 0, c != 0, rational R",
          "PROVED",
          ("wave2/w2_h1c_refutation.py", "THEOREM W2-1 holds on the whole D=1..25, k=0..5 grid"),
          probe="the bogus rule 'solvable iff k==0', which the same grid rejects"),

    claim("W3-1",
          "The endgame admits a degree-D realization iff 3 does not divide D and k = D; "
          "for 3 not dividing D the rational solution is unique of degree exactly k",
          "integer D >= 1, integer k >= 0, c != 0, rational R, realization demand deg R = D",
          "PROVED",
          ("wave3/w3_endgame_degree_obstruction.py", "COROLLARY holds on every grid cell"),
          depends=("W2-1",),
          probe="the bogus rules 'deg R = D always' and 'deg R = k always', both rejected"),

    claim("FIRST-FRAMEWORK",
          "No Keller map of C^2 realizes Borisov's First Framework at (99,66)",
          "the First Framework as formalized by this campaign, D = 13, endgame exponent k = 4",
          "PROVED",
          ("wave3/w3_endgame_degree_obstruction.py", "First Framework (99,66): its degree is 4, not 13"),
          depends=("W3-1",),
          probe="k = D = 13, where the realization demand IS satisfiable"),

    claim("FIRST-FRAMEWORK-WAVE1-ROUTE",
          "The wave-1 route to the same conclusion (v = -1 evaluation + THEOREM 3 pole-fiber)",
          "the First Framework as formalized by this campaign",
          "CONDITIONAL",
          ("wave2/w2_pole_admissibility.py", "contradiction item 11 resolved against 'unconditional'"),
          conditional_on="the campaign's own THEOREM 2/3 (rigidity, pole-fiber), not independently reproduced"),

    claim("TRANSFER",
          "For chain degree D the endgame mechanism is fatal whenever D/3 is not an integer",
          "all frameworks with chain degree D",
          "REFUTED",
          ("wave2/w2_money_cells.py", "D=23, k=4: solution verified through the operator")),

    claim("SECOND-FRAMEWORK",
          "The Second Framework (D = 23) dies to the endgame",
          "D = 23 with endgame exponent k != 23",
          "PROVED",
          ("wave3/w3_endgame_degree_obstruction.py", "Second Framework: its degree is 4, not 23"),
          depends=("W3-1",),
          probe="k = D = 23, where the realization demand IS satisfiable"),

    claim("S38-COLLAPSE",
          "Plane weighted-homogeneous Keller maps collapse to diagonal linear",
          "unrestricted",
          "REFUTED",
          ("wave3/w3_weighted_homogeneous_theorem.py", "m=2: the map is NOT linear")),

    claim("W3-2",
          "A plane weighted-homogeneous Keller map with MIXED-SIGN weights (a*b < 0) is linear",
          "integer weights (a,b) with a*b < 0, every degree",
          "PROVED",
          ("wave3/w3_weighted_homogeneous_theorem.py", "STEP 1: the identity holds symbolically for generic A, B"),
          probe="same-sign weights (1,m), where (x, y + x^m) breaks it"),

    claim("W3-4",
          "(det JG) o pi * D = (det JF) * (D' o F), where D, D' are the contents of the "
          "maximal-minor vectors of the source and target quotient maps",
          "C*-actions on C^3 with a free rank-2 invariant ring, equivariant F with descent G",
          "PROVED",
          ("wave3/w3_descent_jacobian_formula.py", "THEOREM W3-4 holds exactly on Alpoge's map"),
          probe="the same identity with the content factor D dropped, which fails"),

    claim("A1-SQUARE-FORCED",
          "For every C*-equivariant Keller map on C^(n+1) with polynomial invariant rings, "
          "the descent has det JG = c*h^k with k >= 2 (the square is forced)",
          "all such weight systems",
          "REFUTED",
          ("wave3/w3_descent_jacobian_formula.py", "D = 1 occurs -- the square is NOT forced")),

    claim("A1-K0-CLASS",
          "The k = 0 weight systems are exactly (+-1, -+1, 0) up to permutation, and there "
          "the descent is Jacobian-preserving, so a C^3 counterexample in that class IS a "
          "plane counterexample with a factored first coordinate",
          "C*-actions on C^3 with a free rank-2 invariant ring",
          "PROVED",
          ("wave3/w3_descent_jacobian_formula.py",
           "k = 0 class: the descent is Jacobian-PRESERVING, det JG o pi = det JF"),
          depends=("W3-4",),
          probe="Alpoge's k = 2 class, where the same identity fails"),

    claim("ALPOGE-DETJF",
          "det JF = -2 on Alpoge's degree-7 map of C^3",
          "the map as recorded in Session 1 and file `39`",
          "PROVED",
          ("wave2/w2_alpoge_detjf.py", "det JF == -2 exactly (symbolic)"),
          probe="the same map with f3 perturbed by +x, whose Jacobian is not constant"),

    claim("DESCENT-D3-S3",
          "The Path A quotient descent has geometric degree 3 and fiber monodromy S_3",
          "the descent G of file `39`, at four rational targets",
          "DERIVED",
          ("wave2/w2_irreducibility_sieve.py", "descent fiber monodromy is the full symmetric group S_3 (census profile)")),

    claim("SEC-2.5-SIEVE",
          "The section 2.5 eliminant is irreducible",
          "the wave-1 section 2.5 eliminant",
          "UNVERIFIED",
          ("wave2/w2_irreducibility_sieve.py", "section 2.5 eliminant artifact is absent from this repository")),

    claim("NGUYEN-104",
          "The Nguyen 104 result is unverified",
          "the literature",
          "WITHDRAWN",
          None,
          withdrawn_reason="asserted from three failed web searches; the result is real "
                           "and refereed.  Absence of search hits is evidence about the "
                           "search, not about the literature.  No in-repository artifact "
                           "bears on it, so the honest label is WITHDRAWN, not REFUTED."),

    claim("HIT-NONE",
          "No candidate in this repository passes the HIT protocol",
          "every candidate recorded in this repository",
          "PROVED",
          ("wave3/w3_hit_protocol.py", "Path A descent G is correctly NOT a hit (det JG = -2 h^2, fails H2)"),
          probe="the Alpoge positive control, which the gate's H2/H3 logic accepts"),

    claim("JC-PLANE",
          "The plane Jacobian Conjecture is false",
          "Keller maps of C^2",
          "ASSERTED",
          None),
]

print()
print("=" * 78)
print("CAMPAIGN LEDGER")
print("=" * 78)
for r in sorted(LEDGER, key=lambda r: r["key"]):
    ev = f"{r['evidence'][0]}" if r["evidence"] else "-"
    print(f"    {r['key']:<28} {r['label']:<12} evidence: {ev}")
    print(f"        domain: {r['domain']}")
    if r["depends"]:
        print(f"        depends: {', '.join(r['depends'])}")
    if r["conditional_on"]:
        print(f"        conditional on: {r['conditional_on']}")
    if r["withdrawn_reason"]:
        print(f"        withdrawn because: {r['withdrawn_reason']}")
    if r["probe"]:
        print(f"        domain probe: {r['probe']}")

findings = lint(LEDGER)
print()
print("=" * 78)
print("LINT")
print("=" * 78)
if findings:
    for f in findings:
        print(f"    {f[0]}  {f[1]}: {f[2]}")
else:
    print("    no findings: the ledger is internally consistent")

print()
print("=" * 78)
print(f"    linter self-test        : {'PASS' if selftest_ok else 'FAIL'}")
print(f"    clean-ledger control    : {'PASS' if clean_ok else 'FAIL'}")
print(f"    campaign ledger findings: {len(findings)}")
print("=" * 78)
sys.exit(0 if (selftest_ok and clean_ok and not findings) else 1)
