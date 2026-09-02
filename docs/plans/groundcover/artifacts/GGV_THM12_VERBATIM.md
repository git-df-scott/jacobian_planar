# GGV, Pro Mathematica 27 (2013) — Theorem 1.2 verbatim, and the (1.2) row-3 misprint

Source: `wt/canon/papers/GGV_ProMathematica27_2013.pdf`, 17 PDF pages, journal pagination 83–98.
"A differential equation for polynomials related to the Jacobian Conjecture", Christian Valqui,
Jorge A. Guccione, Juan J. Guccione, October 2013. Extraction: `pdftotext -layout` →
`ggv2013_layout.txt`. Theorem 1.2 is on **journal p. 85 = PDF p. 3** (`ggv2013_layout.txt:89-103`);
it is re-derived as (3.5)/(3.6) on **journal p. 93 = PDF p. 11** (`ggv2013_layout.txt:465-478`).

---

## Theorem 1.1 (journal p. 84, `ggv2013_layout.txt:57-72`), verbatim — context for 1.2

> **Theorem 1.1** If B = 16, then there exist µ0 , µ1 , µ2 , µ3 ∈ K with **µ0 ≠ 0** and P, Q ∈ L := K[x, y]
> such that
> &nbsp;&nbsp;&nbsp;&nbsp;ℓ1,−1 (P ) = x³y + µ3 x² ,  ℓ1,−1 (Q) = x²y + µ3 x
> and
> &nbsp;&nbsp;&nbsp;&nbsp;[P, Q] = x⁴y + µ0 + µ1 x + µ2 x² + µ3 x³ .  (1.1)
> Moreover, there exists j ∈ N such that {(j, 1)} = Dir(P ) = Dir(Q),
> &nbsp;&nbsp;&nbsp;&nbsp;st_{j,1}(P ) = (3, 1), st_{j,1}(Q) = (2, 1), en_{j,1}(P ) = (0, m), en_{j,1}(Q) = (0, n),
> where m = 3j + 1 and n = 2j + 1.

B is defined (p. 84) as ∞ if JC is true, else min gcd(deg P, deg Q) over counterexamples.
Theorem 1.1 is cited as **[1, Theorem 8.10]**; B ≥ 16 is cited as **[2, Theorem 2.23]**.
The Ansatz feeding §3 (p. 84, `:72`):
`P = x³y + x²p2(y) + xp1(y) + p0(y)` and `Q = x²y + xq1(y) + q0(y)`.

---

## Theorem 1.2 (journal p. 85, `ggv2013_layout.txt:89-103`), VERBATIM AS PRINTED

> **Theorem 1.2** B = 16 **if and only if** there exist A, q1 ∈ K[y] and µ0 , µ1 , µ2 , µ3 ∈ K with **µ0 ≠ 0**,
>
> &nbsp;&nbsp;&nbsp;&nbsp;A(0) = − ¼ µ3² ,  A′(0) = µ2  and  **µ3 A″(0) = −6µ1 − 2µ3 q1″(0)**,  (1.2)
>
> such that
>
> &nbsp;&nbsp;&nbsp;&nbsp;6 ( A − q1²/4 + (µ3/4) q1 − (µ2/6) y )² = 4yAA′ + 6 ( (µ3/4) q1 − (µ2/6) y )²
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;− µ2 y q1² + 3µ1 y² q1 − 6µ0 y³ .  (1.3)

(The `pdftotext -layout` rendering of the fraction stack is reproduced verbatim in
`ggv2013_layout.txt:93-103`; the exponent "2" on both squared parentheses sits on its own text line.)

Immediately following (p. 85, `:105-112`):

> We were not able to obtain a solution of (1.3) satisfying (1.2) with µ0 ≠ 0 (which would yield a
> counterexample to the JC), nor could we discard the existence of such a solution (which would
> prove B > 16). We analyze some particular cases of (1.3), for example we show that for
> µ3 = µ2 = µ1 = µ0 = 0 the only possible solutions are (ρ, σ)-homogeneous for (ρ, σ) = (j, 1),
> where j + 1 = deg(q1 ). We also recognize (1.3) as an Abel differential equation of second kind ...

## The same content restated in §3 (journal p. 93, `ggv2013_layout.txt:465-478`)

> ... and we can express (3.4) as a differential equation for A and q1 :
> &nbsp;&nbsp;&nbsp;&nbsp;[ identical equation ]  (3.5)
> Moreover we have
> &nbsp;&nbsp;&nbsp;&nbsp;A(0) = − ¼ µ3² , A′(0) = µ2 and **u3 A″(0) = −6µ1 − 2µ3 q1″(0)**.  (3.6)
> In fact, from the definition of A we have that A(0) = −q1(0)p2(0) + ¾ q1²(0) = − ¼ µ3² . **The other
> two conditions follow from the requirement that q0′(y) and p0′(y) defined by (3.2) and (3.3) are
> polynomials.**
> &nbsp;&nbsp;&nbsp;&nbsp;This proves Theorem 1.2 ...

(`u3` is a further typo for `µ3` in (3.6).) The definition of A (p. 92, `:463-465`):

> A := y p1 − q1 p2 + ¾ q1² = − ¼ µ3² + y p1 − µ3 yF − µ3 y²F′ − y³FF′ − ¾ y⁴(F′)²

with (p. 91–92) the general solution of the first equation `q1 = µ3 + y²F′`,
`p2 = µ3 + yF + (3/2)y²F′` for any `F ∈ yK[y]`, and (3.2), (3.3) giving q0′, p0′.

---

## Answers to the recorded questions

**Is it stated as an iff?** **YES** — literally "B = 16 **if and only if** there exist ...". The forward
direction rests on Theorem 1.1 = [1, Thm 8.10] and B ≥ 16 = [2, Thm 2.23]; the reverse direction is
§2 ("Construction of a counterexample", pp. 85–89), which starts from a pair as in Theorem 1.1 and
applies ψ1, ψ3 ∈ Aut(L), Aut(L^(1)) to build (P̃, Q̃) with gcd(deg P̃, deg Q̃) = 16.

**What object's existence is equivalent to a B = 16 counterexample?** **Not full polynomials and not
"leading data" either** — it is a *reduced* datum: **two polynomials A, q1 ∈ K[y] plus four constants
µ0, µ1, µ2, µ3 ∈ K**. A is not one of P, Q's coefficient polynomials; it is the combination
`A = y p1 − q1 p2 + (3/4)q1²` built from the Ansatz `P = x³y + x²p2 + xp1 + p0`,
`Q = x²y + xq1 + q0`. Given (A, q1, µ), the paper recovers p2 and F from q1, then p1 from A, then
q0 and p0 by integrating (3.2)/(3.3) — so the full P, Q are recoverable, and the polynomiality of
q0, p0 is exactly what (1.2) enforces. §3.1 (p. 93) makes this explicit: dropping (3.6) admits
solutions with µ0 ≠ 0 (e.g. A = 1 − y³ − y⁶/4, q1 = y³ + 2, µ0 = 1, µ1 = µ2 = 0, µ3 = 2) which fail
because p1(y) = y⁵ + 2y² + y/2 ∉ K[y].

**Nondegeneracy conditions that ARE part of the statement:**
1. `µ0 ≠ 0` (explicit; it is the JC-counterexample condition, cf. (1.1)).
2. `A, q1 ∈ K[y]` — polynomials, not rational/formal (this is the real force of the theorem).
3. `A(0) = −µ3²/4`; 4. `A′(0) = µ2`; 5. the row-3 condition.

**Conditions that are NOT part of Theorem 1.2 as printed:**
* **No `deg q1 = d` (or any degree) condition.** `deg(q1) = j + 1` appears only in the *discussion* of
  the special case µ3 = µ2 = µ1 = µ0 = 0 (p. 85), tying back to Theorem 1.1's j; it is not a
  hypothesis of Theorem 1.2. Nor are m = 3j+1, n = 2j+1, or Dir(P) = Dir(Q) = {(j,1)} carried over.
* No condition on µ1, µ2, µ3 (any of them may vanish); no leading-coefficient condition on q1 or A.
* The normalisations `q1(0) = µ3`, `q1′(0) = 0`, `p2(0) = µ3`, `p2′(0) = 0`, `F(0) = 0` are derived
  inside §3 ("we can and will assume", p. 92) and are **not** restated in Theorem 1.2 — note
  `q1(0) = µ3` is implied by A(0) = −µ3²/4 only together with p2(0) = µ3.

**Row 3 as printed:** the `−2µ3 q1″(0)` term **IS present**, in both places:
`(1.2)`: `µ3 A″(0) = −6µ1 − 2µ3 q1″(0)`  and  `(3.6)`: `u3 A″(0) = −6µ1 − 2µ3 q1″(0)`.
So the campaign's description of *what is printed* is exactly right.

---

## Independent check of the campaign's correction — CONFIRMED

Script `run/row3_check.py`. Re-derived row 3 from the paper's own §3, i.e. from "the requirement
that q0′(y) and p0′(y) defined by (3.2) and (3.3) are polynomials", using the paper's
`q1 = µ3 + y²F′`, `p2 = µ3 + yF + (3/2)y²F′`, `F ∈ yK[y]`, generic p1, and
`A = y p1 − q1 p2 + (3/4) q1²`. sympy output:

```
cond from (3.2) polynomiality [num(0)=0]: -2*c0 + 2*mu2      => p1(0) = mu2
q0'(0) = c1/3 + f1*mu3/3
cond from (3.3) polynomiality [num(0)=0]: -c1*mu3/3 + 2*f1*mu3**2/3 - mu1
   => c1 = p1'(0) = 2*f1*mu3 - 3*mu1/mu3
A(0)  = -mu3**2/4      (matches the paper)
A'(0) = mu2            (matches the paper)
A''(0) = 2*c1 - 4*f1*mu3 ,   q1''(0) = 2*f1

WITH the (3.3) condition imposed:
  mu3*A''(0)                          = -6*mu1
  PRINTED RHS  -6*mu1 - 2*mu3*q1''(0) = -6*mu1 - 4*f1*mu3
  printed identity holds identically?  False
  campaign identity holds identically? True
  difference (printed - true) = -4*f1*mu3        [ = -2*mu3*q1''(0) ]
```

**Conclusion: the printed row 3 is a misprint. The correct condition is `µ3 A″(0) = −6µ1`.**
The spurious term is exactly `−2µ3 q1″(0) = −4µ3 F′(0)`.

**Important scope note:** the solve for p1′(0) divides by µ3, i.e. assumes **µ3 ≠ 0**. If µ3 = 0 the
(3.3) condition degenerates to µ1 = 0 and both forms read `0 = −6µ1 = 0` — they agree. So the
misprint is **material only on the µ3 ≠ 0 stratum**, where it imposes a spurious extra linear
relation and therefore cuts the variety down. Any B = 16 emptiness verdict computed from the printed
row 3 is a verdict about a proper subvariety, except on the µ3 = 0 slice where it is unaffected.

## Comparison with arXiv 1310.8249v3 eq. (3.9)

**Not possible here.** `1310.8249` is **not present** anywhere under the worktrees
(`find $WT -iname "*1310*"` returns nothing; `wt/canon/papers/` holds 1401.1784, 1406.0886,
1605.09430, 1708.07936, 1901.04073, 1902.05923, 2204.14178, 2506.05697, 2607.22198, 2608.00222,
GGV_ProMathematica27_2013). No web fetch was made (task said local PDFs only). The comparison
against 1310.8249v3 (3.9) — the natural way to distinguish "journal typesetting error" from
"error present in the authors' source" — remains **OPEN** and is a cheap next step if that PDF
can be added to the canon.
