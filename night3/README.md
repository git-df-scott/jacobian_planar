# night3 — collision-system search

Executor record. No interpretation.

Implementation: `night3/collision.py`. Results: `night3/collision_sweep.csv`,
`night3/supports/support_<hash>.json` (one per support pair, exact supports),
`night3/results/controls.json`, `night3/results/keller_only_check.json`.

---

## The system as implemented

For a support pair (S_P, S_Q), finite subsets of Z_{>=0}^2 each containing (0,0),
with one unknown coefficient per support monomial:

    P = sum_{(i,j) in S_P} a_{ij} x^i y^j
    Q = sum_{(i,j) in S_Q} b_{ij} x^i y^j

over GF(p), p in {999983, 1000003}:

- **(K)** every coefficient of `P_x*Q_y - P_y*Q_x - 1`, as a polynomial in x and y,
  equals 0;
- **(C)** `P(0,0) = 0`, `Q(0,0) = 0`, `P(1,0) = 0`, `Q(1,0) = 0`.

Solved by Groebner basis (grevlex) over GF(p). **Unit ideal = EMPTY.** The full
system (K)+(C) is handed to the solver as written; the driver pre-eliminates
nothing.

Solver: sympy 1.14.0 `groebner(..., modulus=p)`. Per the night3 tooling audit no
dedicated Groebner system (msolve / Singular / Macaulay2 / sage) is present on this
container, so the audit's fallback engine is what is used here.

---

## Mandatory controls

Run via `python3 night3/collision.py controls`; raw record in
`night3/results/controls.json`. All passed; nothing was hard-exited.

| control | requirement | result |
|---|---|---|
| P2 | `P = x^2 - x`, `Q = y` satisfies (C) by direct substitution | **PASS** — P(0,0)=0, Q(0,0)=0, P(1,0)=0, Q(1,0)=0 |
| P1 | (C) alone, dense degree-2 supports, must be NONEMPTY | **PASS** — NONEMPTY at 999983 (0.60 s) and at 1000003 (0.72 s) |
| N1 | (K)+(C), dense supports of total degree <= 2, must be EMPTY at both primes | **PASS** — EMPTY at 999983 (0.46 s) and at 1000003 (0.48 s) |
| N1 | (K)+(C), dense supports of total degree <= 3, must be EMPTY at both primes | **PASS** — EMPTY at 999983 (4.18 s) and at 1000003 (4.13 s) |

N1 did not return NONEMPTY at any point, so no instrument anomaly was raised.

---

## Sweep

Seed 20260829, per-solve timeout 300 s, both primes on every support pair.

Construction, as specified: degree pairs `(a*t, b*t)` for coprime `(a,b)` in
{(2,3), (3,4), (4,5), (5,6), (3,5)} with the maximum degree in [126, 200]; P's
Newton polygon from 3–5 random base vertices including (0,0) and one realizing the
top degree, checked to be genuinely 2-dimensional; Q's polygon the same base scaled
by `b/a`, so the two are similar with ratio `deg Q / deg P` and integral; each
support filled with its polygon vertices plus random interior lattice points up to a
monomial budget `k` in {10, 14, 18}.

| item | value |
|---|---|
| support pairs run | 261 |
| rows (pairs x primes) | 522 |
| rows per prime | 261 at 999983, 261 at 1000003 |
| rows per k | 174 each at k=10, 14, 18 |
| deg Q range | 126 – 200 |
| deg P range | 78 – 165 |
| support sizes realized | 10 – 18 monomials |
| total solver wall time | 284.3 s (max 1.70 s, mean 0.54 s per solve) |

**Verdict tally: EMPTY 522, NONEMPTY 0, TIMEOUT 0, ERROR 0.**

No cell returned NONEMPTY, so the halt-and-report protocol was not triggered and no
`night3/NONEMPTY_<hash>/` directory exists.

---

## Additional executor check (not part of the contract)

Recorded because it bears on what the sweep rows do and do not cover, and is stated
as a measurement only.

The Keller equations **(K) alone**, with the collision equations (C) omitted, were
run against 25 randomly chosen sweep support pairs at p=999983. Raw record in
`night3/results/keller_only_check.json`.

- Result: **EMPTY in 25 of 25.**
- On dense degree-<=2 supports the same (K)-alone system returns NONEMPTY, so the
  check does distinguish the two outcomes.

So on the support pairs sampled, (K) alone is already the unit ideal, and the
EMPTY verdicts recorded in the sweep are produced without the collision equations
(C) contributing. Interpretation of this is out of scope here.

---

## Honest scope statement

- **This sweep is modular.** Every verdict is a statement about the ideal over
  GF(p) for p in {999983, 1000003}. A mod-p solution is not a characteristic-zero
  result of any kind until it is lifted and verified exactly, and agreement across
  the two primes is a bug-detection standard, not a proof in characteristic zero.
- **Sparse supports are an exploratory subfamily.** EMPTY closes only the supports
  actually run — the 261 support pairs listed in `night3/supports/`. It says
  nothing about supports not in that list, about other monomial budgets, about
  degrees outside [126, 200], or about dense supports at these degrees.
- **Normalization scope (external audit finding).** The fixed normalization of the
  collision to (0,0) and (1,0) can densify a sparse pair out of its carrier, so on
  non-affine-saturated supports the formulation can produce false EMPTYs; it never
  produces false NONEMPTYs. Accordingly: EMPTY verdicts in sweeps 1–2 certify only
  the absence of solutions with a collision normalizable to (0,0),(1,0) within the
  fixed carrier; they do not close the support family under general affine
  position. NONEMPTY verdicts are unaffected by this and remain fully valid.
- NONEMPTY, had it occurred, would mean only that the Groebner basis is not the
  unit ideal, i.e. the ideal is proper over the algebraic closure of GF(p). It
  would not by itself assert a solution with coordinates in GF(p).

---

# Sweep 2 — Keller-admissible supports

Implementation: `night3/collision2.py` (imports the sweep-1 system builder, solver
wrapper and hashing from `night3/collision.py` unchanged). Results:
`night3/collision_sweep2.csv`, `night3/supports2/support2_<hash>.json`.

Same contract (K)+(C), same solver, same unit-ideal = EMPTY rule. Seed 20260830,
per-solve timeout 600 s, both primes on every cell.

## Support generator

Supports are the exact supports of an actual sparse automorphism, built as a
composition of monomial elementary maps `(x, y + c*x^a)` and `(x + c*y^b, y)` —
2–4 of them, alternating type, random nonzero `c` mod 999983 — with one general
det-1 affine factor inserted at a random position, exponents rejected unless the
composition's max degree lands in [126, 220]. (0,0) is added to both supports. A
pair is rejected if `|S_P| + |S_Q| > 140`. Each support record stores the
generating word, its exponents, the degrees and the support sizes.

Variants solved per support pair:
- **V0** — the exact support;
- **V1** — each support enlarged by 4 random extra lattice points inside its own
  convex hull.

Recorded structural observation: of the 15 accepted words, the affine factor sits
last in 14 and second-of-three in 1. Support sizes realized: `|S_P|` 12–120,
`|S_Q|` 4–24.

## Witness control

Per support and per variant, the generating automorphism's own coefficients are
substituted into the (K) equation vector; every entry must be exactly zero mod p.
This replaces sweep 1's (K)-alone check and certifies the support admits a Keller
point.

**Witness tally: 30 checks (15 pairs x 2 variants), 30 PASS, 0 FAIL.** No hard exit.

## Rows and verdicts

| item | value |
|---|---|
| support pairs | 15 |
| rows | 66 (34 V0, 32 V1; both primes) |
| **EMPTY** | **62** |
| **NONEMPTY** | **0** |
| **TIMEOUT** | **4** |
| ERROR | 0 |

No cell returned NONEMPTY, so the halt-and-report protocol was not triggered and no
`night3/NONEMPTY_<hash>/` directory exists. TIMEOUT is recorded as a real outcome.

Five slowest cells:

| wall | hash | variant | prime | verdict |
|---|---|---|---|---|
| 600.1 s | 4470c68c7758 | V1 | 999983 | TIMEOUT |
| 600.1 s | 4470c68c7758 | V1 | 1000003 | TIMEOUT |
| 600.1 s | 97455928a391 | V0 | 999983 | TIMEOUT |
| 600.1 s | 97455928a391 | V0 | 1000003 | TIMEOUT |
| 66.8 s | 4470c68c7758 | V0 | 999983 | EMPTY |

## Framing recorded for sweep 2

On these supports the Keller variety is nonempty — the witness control certifies a
Keller point on every one — but automorphisms never satisfy (C), since they are
injective. Any NONEMPTY here would therefore be exactly a Keller point outside the
generating family, which is why the halt-and-report protocol matters more in this
sweep than in sweep 1. No NONEMPTY occurred.

## Closure note

Sweep 2 was closed at 66 rows on coordinator instruction; no further sweep-2 cells
were run. The coordinator's closure note, recorded verbatim:

> Sweep 2 closed at 66 rows (62 EMPTY, 4 TIMEOUT, 0 NONEMPTY). Post-hoc review:
> many sweep-2 support pairs have equal or divisible degree pairs (e.g. 126/126,
> 144/72), where invertibility of Keller pairs is already a known theorem; those
> EMPTY verdicts were therefore expected independent of the collision system.
> Future sweeps must filter degree pairs by the published necessary conditions
> before solving.

Executor check of the numbers in that note against `night3/collision_sweep2.csv`:
66 rows, 62 EMPTY, 4 TIMEOUT, 0 NONEMPTY — matches. Degree pairs of the 15 support
pairs: 13 equal (126/126, 130/130, 133/133, 143/143, 150/150, 171/171, 176/176,
180/180, 187/187, 190/190, 208/208, 209/209, 209/209) and 2 divisible non-equal
(133/19, 144/72) — so all 15 fall in the equal-or-divisible class, and both
examples cited in the note appear in the data. The theorem claim and the
forward-looking instruction in the note are the coordinator's; they are recorded
here as received and are not an executor finding.

A reformulated sweep 3 (unnormalized collision points with saturation) is to follow
separately and was not designed or started here.
