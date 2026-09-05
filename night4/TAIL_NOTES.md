# night4 TAIL_NOTES — formal-inverse tail evaluator

Executor record. Measurements only, no interpretation.

Implementation: `night4/tail.py` (standard library only; imports nothing from
`night2/` or `night3/` — the tame sampler is reimplemented in the file). Full
console output: `night4/tail_run.out`.

Run parameters: p = 999983, seed = 20260831. Total wall: **24.30 s**.

## Definitions as implemented

For F = (P, Q) over F_p with P(0,0) = Q(0,0) = 0 and invertible linear part L,
the formal inverse G is built degree by degree from

    G^(1) = L^{-1},        G^(d) = (-K_d) o L^{-1}  for d >= 2,

where K_d is the degree-d part of the composition of the already-known parts
G^(m), m < d, with F. `TAIL(F, D)` is the list of nonzero-coefficient counts of
G^(m), summed over the two components, for m from deg F + 1 to D.

The mandatory self-check recomposes the assembled `G_{<=D}` with F **from
scratch**, independently of the incremental recursion that produced it, and
requires the result to equal the identity exactly, coefficient by coefficient,
through degree D.

## T0 — known-answer check (added by the executor)

Not in the requested control list. Added because T3 as specified checks the
recursion against its own composition, which a self-consistent but wrong
recursion could in principle satisfy; T0 anchors it to independently known
closed-form inverses.

| input F | expected G | result |
|---|---|---|
| (x + y^2, y) | (x - y^2, y) | PASS |
| (x, y + x^2) | (x, y - x^2) | PASS |
| (x + y^3, y) | (x - y^3, y) | PASS |
| (2x + 3y, x + 2y) | (2x - 3y, -x + 2y) | PASS |

**T0 PASS**, 0.001 s. All four reproduced exactly mod p.

## T1 — tails of tame automorphisms

20 random tame automorphisms, target degrees cycling through 4..12, constant
terms stripped, each evaluated to D = 2·deg F + 6.

- Every sample hit its target degree exactly (deg F = target in all 20).
- **`TAIL` all zero in 20 of 20.**
- deg G = deg F in all 20 (4→4, 5→5, …, 12→12).
- Composition self-check PASS in 20 of 20.

**T1 PASS**, 18.41 s.

## T2 — non-automorphism, P = x + y^2 + x^3, Q = y + x^2

Linear part is the identity; deg F = 3; D = 12.

`TAIL` for m = 4..12: **[6, 8, 11, 14, 17, 18, 22, 24, 26]** — nonzero at every
degree in range. Self-check PASS.

**T2 PASS**, 0.004 s.

## T3 — composition self-check

Run inside every `tail()` and `formal_inverse()` call in this session: 4 (T0) +
20 (T1) + 1 (T2) + 10 (perturbation baseline and perturbed) = 35 invocations.

**T3 PASS — 35 of 35.** No hard exit was triggered anywhere.

## Perturbation measurement

Procedure: sample a tame automorphism, pick one component (P or Q) at random,
pick at random one lattice point of that component's Newton polygon that is
**not** a hull vertex and is not the origin, and add 1 to the coefficient there.
The resulting linear part is re-checked for invertibility (a singular one would
be resampled; none occurred). Baseline and perturbed tails both evaluated to
D = 2·deg F + 6.

| # | deg F | D | component | monomial | already in support | baseline tail all zero | perturbed tail lights up | first nonzero degree |
|---|---|---|---|---|---|---|---|---|
| 1 | 4 | 14 | Q | (1,3) | yes | yes | **yes** | 5 |
| 2 | 5 | 16 | Q | (0,4) | yes | yes | **yes** | 6 |
| 3 | 6 | 18 | P | (2,0) | yes | yes | **yes** | 7 |
| 4 | 7 | 20 | P | (3,3) | yes | yes | **yes** | 8 |
| 5 | 8 | 22 | P | (0,4) | yes | yes | **yes** | 9 |

**Lit up in 5 of 5.** In every case the tail is nonzero at the very first degree
above deg F and at every degree thereafter up to D. Perturbed self-check PASS in
all 5.

Perturbed tail vectors as measured:

| # | perturbed `TAIL` (m = deg F + 1 … D) |
|---|---|
| 1 | [12, 14, 16, 18, 20, 22, 24, 26, 28, 30] |
| 2 | [14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34] |
| 3 | [16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38] |
| 4 | [18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42] |
| 5 | [20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46] |

Perturbation wall: 5.86 s.

## Wall times

| stage | wall |
|---|---|
| T0 | 0.001 s |
| T1 | 18.41 s |
| T2 | 0.004 s |
| perturbation | 5.86 s |
| **total** | **24.30 s** |

## Scope

Everything above is mod p at the single prime 999983 and is reported as modular.
`TAIL` all-zero on the 20 T1 samples is a statement about those 20 sampled maps
at that prime and to those bounds D, not a proof of the degree bound. No
characteristic-zero claim is made or implied.
