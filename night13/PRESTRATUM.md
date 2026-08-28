# night13 — the compressed cusp prestratum at degrees (84, 126)

Scope note. This file records measurements only. It states what was computed,
in which ring and characteristic, and what the computations returned. It
contains no assessment of what any of these numbers mean beyond the algebraic
identities that were themselves verified.

Ring / characteristic labels used below:

* **ring Z** — exact integer arithmetic (python `int`, and Singular `ring 0`).
* **ring Q** — exact rational arithmetic (`fractions.Fraction`); reached only
  on the reconstruction branch, which was not entered.
* **char 999983** and **char 1000003** — the two prime fields of the lane.

---

## 1. The degree pair, and the divisibility fact

`deg P = 84`, `deg Q = 126`.

| quantity | value |
|---|---|
| `126 mod 84` | 42 (so 84 does not divide 126) |
| `84 mod 126` | 84 (so 126 does not divide 84) |
| `gcd(84, 126)` | 42 |
| `84 = 2·42`, `126 = 3·42` | the 2:3 profile |
| divisibility-ordered? | **no** |

Jung–van der Kulk: for a polynomial automorphism `(F, G)` of the affine plane
over a field of characteristic 0, `deg F` divides `deg G` or `deg G` divides
`deg F`. The pair `(84, 126)` is not divisibility-ordered, so **no polynomial
automorphism of the plane has this degree shape**. Recorded as the fixed
yardstick this lane's object is built against. (`carrier.json`:
`jvdk_84_divides_126`, `jvdk_126_divides_84`, `jvdk_divisibility_ordered`.)

---

## 2. The object

`H` is the four-term form of degree 42, normalised in the chart `h2 = 1`:

```
H = h2·x^2 y^40 + h14·x^14 y^28 + h29·x^29 y^13 + h41·x^41 y ,   h2 = 1
```

Prescribed leading forms, and the carriers below them:

```
P = A·H^2 + sum_{m in C_P} a_m·x^m ,   |C_P| =  96,  deg P = 84
Q = B·H^3 + sum_{m in C_Q} b_m·x^m ,   |C_Q| = 256,  deg Q = 126
```

Top parameters after the `h2 = 1` scaling: `h14, h29, h41, A, B` — **5**.
Total unknowns: `5 + 96 + 256 = 357`.

### 2.1 The mu_3 arithmetic (verified, ring Z)

| quantity | measured |
|---|---|
| `H` x-exponents | `2, 14, 29, 41` |
| the same mod 3 | `2, 2, 2, 2` — all equal to 2 |
| x-exponents of `H^2` | `4, 16, 28, 31, 43, 55, 58, 70, 82` (9 monomials) |
| the same mod 3 | `{1}` — every one is `1 mod 3` |
| x-exponents of `H^3` | `6, 18, 30, 33, 42, 45, 57, 60, 69, 72, 84, 87, 96, 99, 111, 123` (16 monomials) |
| the same mod 3 | `{0}` — every one is `0 mod 3` |

So the grading demanded by the recipe (every P-monomial `i = 1 mod 3`, every
Q-monomial `i = 0 mod 3`) is consistent with the prescribed leading forms:
`2 + 2 = 4 = 1 (mod 3)` and `2 + 2 + 2 = 6 = 0 (mod 3)`.

Consequence for the bracket, also checked on every assembled row: in
`P_x Q_y` a term has x-exponent `(1 − 1) + 0 = 0 (mod 3)`, and in `P_y Q_x` it
is `1 + (0 − 1) = 0 (mod 3)`. Every bracket row therefore sits at
`i = 0 (mod 3)`, which is where the constant monomial `(0,0)` of the Keller
equation `P_x Q_y − P_y Q_x = 1` lives.

**The constant row has exactly one route.** Pairs reaching `(0,0)` need
`p + a = (1,1)`. The pair `P·(0,1) × Q·(1,0)` is forbidden by the grading
(`0 ≠ 1` and `1 ≠ 0` mod 3), so the only route is `P·(1,0) × Q·(0,1)` with
factor `p1 a2 − p2 a1 = 1`. Measured over the maximal carrier:
`constant_row_adjustable_pairs = 1`. Hence `x ∈ C_P` and `y ∈ C_Q` are
mandatory, and the constant row reads

```
a_(1,0) · b_(0,1) = 1        (so both coefficients are nonzero)
```

---

## 3. Newton polygons and the admissible monomial pools (ring Z)

Exact integer monotone-chain hulls; exact in-hull tests.

| polygon | hull vertices | admissible lattice points |
|---|---|---|
| `NP(P_84) = conv(supp H^2 ∪ {(0,0), (1,0)})` | `(0,0), (1,0), (82,2), (4,80)` | 1087 points with `i = 1 mod 3`, total degree `< 84` |
| `NP(Q_126) = conv(supp H^3 ∪ {(0,0), (0,1)})` | `(0,0), (123,3), (6,120), (0,1)` | 2439 points with `i = 0 mod 3`, total degree `< 126`, `(0,0)` removed |

`(0,0)` is removed from the Q-pool because its bracket column is identically
zero (the factor `p1 a2 − p2 a1` vanishes at `a = (0,0)`); this is the same
kernel-deflation as in the earlier lanes. The origin-side mandatory points are
`x = (1,0)` for `P` and `y = (0,1)` for `Q` per §2.1; the origin itself is
adjoined to the hulls only, not to the carriers.

Compression ratios actually applied: `96 / 1087` on the P side and
`256 / 2439` on the Q side.

---

## 4. The bracket-row incidence hypergraph and the greedy

For a P-monomial `p = (p1,p2)` and a Q-monomial `a = (a1,a2)` the bracket picks
up exactly one term,

```
coeff_p · coeff_a · (p1 a2 − p2 a1) · x^(p1+a1−1) y^(p2+a2−1),
```

so the row key is `p + a − (1,1)` and the pair **contributes** iff
`p1 a2 − p2 a1 ≠ 0` (collinear pairs, e.g. two monomials both built from the
same `h_k`, drop out). A contributing pair is **adjustable** if at least one
of its two monomials is a lower-carrier monomial.

The pure-top part of every row sums to zero **key by key**, because
`[A·H^2, B·H^3] = 6·A·B·H^3·(H_x H_y − H_y H_x) = 0` identically — this is
control **Ca/S1** below, verified symbolically. So each row's equation is
carried entirely by its adjustable pairs, and:

* **mandatory row** = any row key other than `(0,0)` (it must vanish);
* **singleton mandatory row** = mandatory row with exactly one adjustable pair
  — its equation forces a single product of coefficients to vanish;
* **identity row** = mandatory row with no adjustable pair (pure top; cancels).

### 4.1 What was run

Seeds: `x = (1,0)` in `C_P`, `y = (0,1)` in `C_Q`, plus the polygon vertices
carrying the right residue. Measured: the only such vertices are `x` and `y`
themselves — `(82,2)`, `(4,80)`, `(123,3)`, `(6,120)` all lie on the
top-degree line and are already leading-form monomials, and `(0,0)` is
excluded above. So `seedsP = [(1,0)]`, `seedsQ = [(0,1)]`.

Then, repeatedly, the pool monomial with the best score is added, until
96 P-lower and 256 Q-lower are reached (350 greedy steps after the two
seeds). Recorded
implementation choices, stated as deviations from the literal recipe text:

1. **Score.** The recipe says "removes the most singleton mandatory rows".
   Adding a monomial can also create new singleton rows in previously untouched
   row keys, so the score used is the **net** reduction
   `(singletons removed) − (singletons created)`; both components are recorded
   per step in `carrier_trace.json` (`removed`, `created`).
2. **Tie-break.** Ties are broken by generic rank gain of the linearisation at
   **char 999983**: the Jacobian of the bracket rows in the currently selected
   lower unknowns at a random coefficient point, rank by random row
   compression to `ncols + 16` rows. Tie classes are large (up to ~2400
   pool monomials), so at most **8** tied pool monomials per step are rank-evaluated,
   in lexicographic order. This cap is a computational deviation and is
   recorded (`TIE_POOL_CAP = 8`, `rank_gain` per step in the trace).
3. **No row is ever discarded.** All generated bracket rows are kept in the
   probe (2308 nonzero rows on the greedy carrier at a dense sample, plus 32
   rows that cancel to zero identically; 6803 row keys over the maximal
   carrier) against 357 unknowns.

### 4.2 Carrier statistics at the stop point (96 + 256)

| quantity | value |
|---|---|
| greedy steps (after the two seeds) | 350 |
| `|C_P|` / `|C_Q|` | 96 / 256 |
| total unknowns | 357 |
| row keys with at least one adjustable pair | 2308 |
| constant-row adjustable pairs | 1 |
| **singleton mandatory rows remaining** | **177** |
| acceptance test | **REJECTED** |

---

## 5. Acceptance: the structural census (`structural.json`)

The acceptance rule — every mandatory nonconstant row is either an identity
row from `[H^2, H^3] = 0` or carries at least two adjustable contributing
coefficients — was then tested at the level of the **maximal carrier**, i.e.
with all 1087 + 2439 admissible lattice points present. A row key `k` can only
ever be reached by pairs with `p + a = k + (1,1)`, so a row that is singleton
over the maximal carrier is singleton for **every** sub-carrier: no addition
of monomials can repair it. Such a row can only be repaired by *removing* the
lower monomial in its unique pair.

| quantity, over the maximal carrier | value |
|---|---|
| row keys with at least one adjustable pair | 6803 |
| constant-row adjustable pairs | 1 |
| structurally singleton mandatory rows | 37 |
| of these, repairable by removing a lower monomial | 35 |
| of these, **unrepairable** | **2** |

The 35 repairable ones force lower coefficients to vanish: `a_(1,j) = 0` for
`j = 1..20` (rows `(0,j)`), `b_(3k,1) = 0` for `k = 1..13` (rows `(3k,0)`),
`b_(81,2) = 0` (row `(81,1)`) and `a_(4,79) = 0` (row `(3,79)`).

The two unrepairable rows are unrepairable because the lower monomial in the
unique pair is `x` or `y`, which §2.1 shows cannot be dropped without making
the constant bracket row unreachable, while the partner is a prescribed
leading-form monomial:

| row key | unique adjustable pair | factor | the equation it imposes |
|---|---|---|---|
| `(3, 80)` | `P·(4,80)` **leading** (`= A·h2^2 = A`) × `Q·(0,1)` lower | 4 | `4·A·b_(0,1) = 0` |
| `(123, 2)` | `P·(1,0)` lower × `Q·(123,3)` **leading** (`= B·h41^3`) | 3 | `3·a_(1,0)·B·h41^3 = 0` |

Together with the constant row `a_(1,0)·b_(0,1) = 1` of §2.1 (which forces
`a_(1,0) ≠ 0` and `b_(0,1) ≠ 0`), these two rows read, in any field:

* row `(3,80)`: `4·A = 0`;
* row `(123,2)`: `3·B·h41^3 = 0`.

Recorded arithmetic on the two coefficients: `4` is invertible in every
characteristic other than 2, and `3` in every characteristic other than 3; no
single characteristic annihilates both. The ansatz asks for `A ≠ 0` (else
`deg P < 84`), `B ≠ 0` (else `deg Q < 126`) and `h41 ≠ 0` (else `H` has three
terms, not four).

This is the acceptance verdict for the carrier at (84,126) with these Newton
polygons and this mu_3 grading, and it does not depend on which 96 + 256
lower monomials are chosen.

---

## 6. Controls (hard gate; all passed before the probe ran)

| control | ring / char | statement | result |
|---|---|---|---|
| **C0** positive control | char 999983 | `P = x + y^2`, `Q = y` fed through the same consistency routine; must be reported consistent, solved, and the solution's bracket must equal 1 | **PASS** (consistent, solve ok, bracket = 1) |
| **Ca** | Z | `[A·H^2, B·H^3] = 0` identically at 5 random integer parameter points; `deg P84 = 84`, `deg Q126 = 126`, bracket has 0 terms | **PASS** (5/5) |
| **Cb** degenerate control | Z | all lower coefficients zero except `a` on `x` and `b` on `y`; the machine bracket must equal the independent expansion `a·b + A·b·(H^2)_x + a·B·(H^3)_y`, and rows `(0,0)`, `(3,80)`, `(123,2)` must equal `a·b`, `4·A·b`, `3·a·B·h41^3` | **PASS** (3/3 parameter points, all four equalities each) |
| **Cc** rank sanity | char 999983 and char 1000003 | the linear Q-system at a random P-block has `rank > 0` and the constant row is present in the assembled matrix | **PASS** at both primes (`rank_A = 257`, constant row present, 2308 nonzero rows, 32 identically vanishing) |

### 6.1 Independent verification in Singular 4.3.2 (ring Q, char 0)

`night13/leading.sing`, generated by `singular_check.py`; raw output in
`night13/singular_out.txt`. Singular shares no code with the python kernel.

| check | result |
|---|---|
| **S1** `[A·H^2, B·H^3] = 0` with `h2, h14, h29, h41, A, B` all symbolic | `1` (true) |
| **S2** degenerate carrier: `br − (a·b + A·b·(H^2)_x + a·B·(H^3)_y) = 0` | `1` (true) |
| **S2** coefficient at `1` | `a*b` (expected `a*b`) |
| **S2** coefficient at `x^3 y^80` | `4*h2^2*A*b` (expected `4*h2^2*A*b`) |
| **S2** coefficient at `x^123 y^2` | `3*h41^3*B*a` (expected `3*h41^3*B*a`) |
| **S3** full greedy carrier, all 96 + 256 lower coefficients random nonzero integers, `h = (1,19,18,14)`, `A = 18`, `B = 17`: `deg P`, `deg Q` | `84`, `126` |
| **S3** coefficient at `x^3 y^80` | `432` = `4·A·b_(0,1)` (expected `432`) |
| **S3** coefficient at `x^123 y^2` | `3778488` = `3·a_(1,0)·B·h41^3` (expected `3778488`) |
| **S3** coefficient at `1` | `162` = `a_(1,0)·b_(0,1)` (expected `162`) |

S3 is the independent confirmation of the uniqueness claim of §5: with every
carrier coefficient present and nonzero, the two rows still consist of exactly
the single predicted term, so no second pair of carrier monomials reaches
them. (In S1/S2 the reported `deg P0 = 87`, `deg Q0 = 130` are total degrees in
the ring `Q[x,y,h2,h14,h29,h41,A,B,a,b]`, which counts the parameter
variables; S3 works in `Q[x,y]` and reports 84 and 126.)

---

## 7. The probe (`probe.json`, `probe_samples.json`)

The full 357-unknown system is bilinear. Fixing the P-block — `h14, h29, h41,
A` and the 96 lower coefficients — makes it **linear** in the Q-block, whose
257 columns are `B` (the whole leading form `H^3` as one unknown, `h` already
fixed) and the 256 lower coefficients. Every generated bracket row is kept.

Sampling: 220 samples, two structured arms alternating — a dense arm (all 96
lower P-coefficients uniform in `[1, p)`) and a sparse arm (each lower
coefficient independently zero with probability 0.35); `a_(1,0)` is drawn
nonzero in both arms, `h2 = 1` is the chart, `h14, h29, h41, A` uniform in
`[1, p)`. The *same* P-block is used at both primes. A sample counts as
consistent only if `rank(A) = rank([A | e])` at **both** primes.

| quantity | value |
|---|---|
| samples | 220 |
| rows in the assembled linear system, nonzero (dense-arm sample) | 2308 |
| rows assembled and found identically zero, all of total degree 208 | 32 |
| columns (Q-block) | 257 |
| `rank(A)` | 257 at both primes, every sample |
| `rank([A | e])` | 258 at both primes, every sample |
| **consistent at both primes** | **0** |
| consistent at 999983 only | 0 |
| consistent at 1000003 only | 0 |
| **inconsistent at both primes** | **220** |
| samples whose obstruction is the two-row certificate of §5 | **220 / 220** |
| dual-prime-consistent samples taken to exact solve / Hensel lift / rational reconstruction | 0 (branch not entered) |
| `HIT_<hash>/` directories written | 0 |
| wall clock | 91.9 s |

The certificate is read off the assembled matrix itself, per sample: row
`(3,80)` has a single nonzero entry, in the `b_(0,1)` column, equal to `4A mod
p`; row `(0,0)` has a single nonzero entry, in the same column, equal to
`a_(1,0) mod p`. Both were checked to hold in all 220 samples
(`all_certificates_are_two_row = true`).

Because no sample was dual-prime consistent, the lift path of night8
(`MONDELLO_LIFT.md` §5, read-only, adapted from 2-adic to p-adic: for `k ≥ 1`
the quadratic remainder `p^{2k}·B(d,d)` dies mod `p^{k+1}`, so every level is
the same `F_p` system `J·d = −s_k` and lifting to `p^4` is solvable iff
`rank(J) = rank([J | s_k])`, with the smoothness minor test being full column
rank of `J mod p`) was **not entered**. It remains coded in `probe.py` behind
that branch.

---

## 8. Scope of the negative tallies

Every verdict in §7 is a verdict about (i) this carrier — the greedy 96 + 256
lower monomials inside the two stated Newton polygons, under the mu_3 grading
with `h2 = 1` — (ii) the two named primes, and (iii) the sampled P-blocks. The
verdict in §5 is stronger in one respect and weaker in another: it is
independent of the choice of lower monomials and of the field, but it is a
statement about the two Newton polygons of §3 and the four-term `H` of §2, and
about nothing else.

---

## 9. File index

| file | content |
|---|---|
| `kit.py` | polynomial / Newton-polygon / mod-p linear-algebra kernel |
| `prestratum.py` | the object, the polygons, the incidence hypergraph, the greedy; writes `carrier.json`, `carrier_trace.json`, `carrier_log.txt` |
| `clean.py` | structural singleton census and the rejection certificate; writes `structural.json` |
| `probe.py` | controls C0/Ca/Cb/Cc and the 220-sample probe; writes `probe.json`, `probe_samples.json` |
| `singular_check.py` | generates and runs `leading.sing`; writes `singular_out.txt` |
| `build_out.txt`, `probe_log.txt` | raw run logs |
