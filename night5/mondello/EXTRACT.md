# night5 mondello — extraction and verification (TASK B)

Executor record. Transcription and measurement only.

## Source

| item | value |
|---|---|
| arXiv id | 2608.02634 |
| title | A Dimension-Two Counterexample to the Separable Jacobian Conjecture in Characteristic Two |
| author | Mondello, Romy |
| arXiv date | 2026/07/29 |
| primary source | `https://arxiv.org/e-print/2608.02634` — original LaTeX, single top-level file `main.tex` (24078 bytes) |
| `main.tex` sha256 | `e10aab38e859b719c101f9e11610896fe2961b179f481a638d86b3fdbecf537c` |
| base field, verbatim | `k = \overline{\F}_2` |

As with the GGHV extraction, working from the authors' LaTeX rather than a
rendered page means the map's exponents are the author's own characters, with no
OCR or layout reconstruction in the path.

The source package also ships an ancillary Lean formalization under `anc/lean/`
(19 files). It was **not** used, read for content, or relied on for anything
below; noted only because it exists.

Note on numbering: the request calls this Theorem 1.2. `main.tex` contains exactly
one `theorem` environment, labelled `\label{thm:main}`, at source lines 104–133,
and it is the theorem carrying the degree-11 pair. That is what was extracted.

Verbatim excerpts are saved alongside this file:

- `theorem_1_2_verbatim.tex` — source lines 104–133, the theorem statement
- `jacobian_collision_verbatim.tex` — source lines 155–187, the Jacobian and
  collision subsection
- `mondello_map.json` — machine-readable transcription

## The extracted object

```
P(x,y) = x + x^2 y + x^4 + x^6 y^2
Q(x,y) = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3
```

Every printed coefficient is 1. deg P = 8, deg Q = 11 — the degree-11 pair.
Both have zero constant term; the degree-1 part of P is `x` and of Q is `y`, so
the linear part is the identity matrix, which the paper independently states as
`JF(0,0) = I_2`.

Stated collision, verbatim: `F(0,1)=F(1,0)=F(1,1)=(0,1)`, with the paper's
remark "They are distinct as \(k\)-points, so \(F\) is not injective on points."

The five numbered claims of the theorem are transcribed verbatim into
`mondello_map.json` under `theorem_claims_verbatim`.

## Ambiguity

**None.** `"ambiguous": false` throughout. Every monomial, exponent and
coefficient is printed explicitly in the displayed equations; there are no
ellipses, no parameters, no unreduced or irregular expressions. Because the map's
data is completely unambiguous, the verification script was written, as the task
conditioned.

**Independent cross-check.** `night5/campaign_restore/session44_md/LIT_MONDELLO_AUG2026.md`,
restored in TASK A from a different source entirely (a git ref, not the arXiv
fetch), records the same paper and the identical pair:

```
P = x + x^2 y + x^4 + x^6 y^2
Q = y + x^5 + x^6 y + x^7 y^2 + x^8 y^3
```

Two independent paths to the same characters. This was noticed after the
extraction was complete and did not inform it.

## Verification

`night5/mondello/verify_mondello.py`, standard library only except for the
`night4/tail.py` import that the task asks for (itself pure standard library).
Full output in `verify_mondello.out`. The script never adjusts the object.

### (1) F_2 arithmetic — PASS

Ten checks: `1+1=0`, `A+A=0`, commutativity of `+` and `*`, associativity,
distributivity, Frobenius `(A+B)^2 = A^2+B^2`, the Leibniz rule for `d/dx`, and
`d/dx(x^2)=0` in characteristic 2. Plus a brute-force cross-check of the
polynomial product against pointwise evaluation at **all 16 points of F_4**
(F_4 implemented as `F_2[t]/(t^2+t+1)`): 0 mismatches.

### (2) Jacobian is exactly 1 — PASS

Derivatives computed independently and compared with the paper's printed values:

| | computed | paper prints | match |
|---|---|---|---|
| `P_x` | `1` | `1` | yes |
| `P_y` | `x^2` | `x^2` | yes |
| `Q_x` | `x^4 + x^6y^2` | `x^4+x^6y^2` | yes |
| `Q_y` | `1 + x^6 + x^8y^2` | `1+x^6+x^8y^2` | yes |

`det JF = 1` **exactly** in `F_2[x,y]` — the computed determinant is the single
monomial 1, not merely a constant.

### (3) Stated collision — PASS

The three printed points are pairwise distinct, and:

```
F(0,1) = (0,1)
F(1,0) = (0,1)
F(1,1) = (0,1)
```

All three images equal, and equal to the printed common image `(0,1)`. The
paper's separate claim `F(0,0) = (0,0)` also checks.

### (4) night4/tail.py recursion mod 2, D = 24 — self-check PASS, tail NONZERO

Linear part mod 2 is `[[1,0],[0,1]]`, det = 1, so it is invertible and the
recursion applies to the pair exactly as printed. No coordinate change was made
or needed.

deg F = 11. Composition self-check **PASS** (the assembled `G_{<=24}` recomposed
with F from scratch equals the identity through degree 24).

**TAIL profile, m = 12..24:**

```
[0, 1, 0, 4, 3, 2, 1, 2, 1, 2, 1, 0, 0]
```

| m | 12 | 13 | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| norm | 0 | 1 | 0 | 4 | 3 | 2 | 1 | 2 | 1 | 2 | 1 | 0 | 0 |

**Tail is NONZERO**, first at m = 13.

### Supplementary measurement (beyond the requested D)

The profile ends `…, 1, 0, 0` at m = 22, 23, 24, which on its own could be read as
the tail terminating. It does not. Re-running at larger bounds, self-check PASS in
both:

```
D = 32 : [0, 1, 0, 4, 3, 2, 1, 2, 1, 2, 1, 0, 0, 1, 0, 2, 2, 1, 0, 6, 4]
D = 40 : [0, 1, 0, 4, 3, 2, 1, 2, 1, 2, 1, 0, 0, 1, 0, 2, 2, 1, 0, 6, 4, 4, 2, 2, 1, 3, 1, 4, 3]
```

The zeros at m = 23, 24 are a local gap, not the end of the tail; nonzero entries
continue to the top of every bound tried (last nonzero m = 32 at D = 32, m = 40 at
D = 40). Recorded so the D = 24 window is not mistaken for termination. No
interpretation offered beyond the measurement.

## Outcome against expectation

The task recorded an expectation of Jacobian PASS, collision PASS, tail NONZERO.
All three came out that way, and no check had to be excused, retried, or adjusted.
Nothing about the object was modified at any point.

## Scope

Checks (1)–(3) are exact statements in `F_2[x,y]` and about `F_2`-points — not
sampled, not modular approximations. Check (4) is the formal-inverse recursion in
characteristic 2, truncated at the stated bound; a tail nonzero within a window is
a statement about the coefficients computed in that window. The paper's remaining
claims — étaleness, `[k(x,y):k(P,Q)]=3`, separability, the three-point geometric
generic fiber — were **not** verified here and nothing above bears on them.
