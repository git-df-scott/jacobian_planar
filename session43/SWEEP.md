# Full sweep — session 43, through 17:00 UTC

## 1. What was established, and how much of it is solver-free

Nothing below used a Groebner basis.  Every item is controlled; the controls are
listed with each.

| # | Result | Where |
| --- | --- | --- |
| 1 | `{P,Q} = x^2` is a triangular system of first-order linear ODEs at **any** x-degree: `sum_{i+k=d+1}[i a_i q_k' - k a_i' q_k] = delta_{d,2}` | `GENERAL_LADDER.md` |
| 2 | At `m=8, n=12` the top eight rungs sit on a single power of `y` (exponents 35,33,…,21) and close into a self-contained **lower-edge ladder** | `EDGE_LADDER.md` |
| 3 | That ladder yields **exactly four** conditions and no more: `disc(A_8)=0`, `A_7(rho)=0`, `A_7'(rho)^2 = 4 alpha A_6(rho)`, and a cubic in `A_5` | `EDGE_LADDER.md` |
| 4 | Those four are **exactly** the regularity of `sqrt(P's edge polynomial)` at `y=rho` through order `z^3` — an independent derivation matching condition for condition | `EDGE_LADDER.md` |
| 5 | The **upper edge** is uniform at every rung and *algebraic*: `Qh^2 = c A^3`, hence `A(t) = c0 G(t)^2`, `Qh = c1 G^3`, `deg G = 4` | `UPPER_EDGE.md` |
| 6 | Generalisation: for any pair with x-degrees `(m,n)`, `A` must be a perfect `(m/gcd(m,n))`-th power — a filter needing **only the Newton polygon**, so it reaches the 804 pairs above 125 that have no `L` | `UPPER_EDGE.md` |
| 7 | `R := Q^2 - cP^3` has `deg_x R = 7` (from 24), `R != 0`, and `{P,R} = 2x^2 Q` is a ladder with a **nonzero RHS at every rung** | `RESIDUAL_LADDER.md` |
| 8 | `r_7, r_6, r_5` are unique with no free parameters, each with the y-order `N(Q^2)=N(P^3)` independently predicts (8, 6, 4) | `RESIDUAL_LADDER.md` |
| 9 | Rung 11: `cond2 - 3 cond1 = 16 C_7(rho)^3`, forcing `(y-rho)^2 | A_7`, and with (3) also `A_6(rho) = 0` | `RESIDUAL_LADDER.md` |

**Net:** eight explicit conditions on both edges plus a cascade in the interior,
where four Groebner attempts across two representations returned NO VERDICT.

## 2. Verdicts, in the agreed language

| target | engine | outcome | why |
| --- | --- | --- | --- |
| Cor 5.7 shape 2 (capped) | msolve -g 2 | **NO VERDICT** | exit 139 — my own `ulimit -v` (A13) |
| Cor 5.7 shape 1 (capped) | msolve -g 2 | **NO VERDICT** | exit 139 — same cause |
| Cor 5.7 shape 2 (uncapped) | msolve -g 2 | **NO VERDICT** | exit 137, genuine cgroup OOM at 13.86 GB, 686 s |
| Cor 5.7 shape 1 (uncapped) | msolve -g 2 | **NO VERDICT** | exit 137, genuine OOM, 1542 s |
| upper-edge substituted (parenthesised) | msolve -g 2 | **NO VERDICT** | parse failure reported as `[1]` (A16) |
| upper-edge additive, 214 vars | Singular slimgb | **running** | 1.2 GB, 14 min CPU |
| the pentagon itself | — | **NO VERDICT** | unchanged |

**No EMPTY and no NONEMPTY was earned today.**  The one thing that *looked* like
EMPTY was a parser artefact.

## 3. Every mistake caught — the whole ledger

### Caught today, and what each would have cost

**A13 — I re-introduced a failure I had already diagnosed.**  `ulimit -v`
segfaults msolve (it reserves address space for its exponent hash table).  I
diagnosed this at 05:45, wrote it down, and re-applied the cap at 15:21,
destroying both Cor 5.7 runs.  *Cost: two runs and two false NO VERDICTs.*
*Lesson recorded: writing a failure down is not the same as building the guard.*

**A14 — my minor enumerator guarded on full column rank.**  When the rank dropped
at rung 15 it enumerated nothing and printed **"still inconsistent."**  That was
an extractor bug, retracted.  The rank drop is the ODE's free constant of
integration — a signature of correctness, not failure.

**A15 — I ran a search's controls after the search, and one failed.**  The
planted right-hand side was built as `-(M·tgt) - v` instead of `M·tgt`.  The
0/3000 result is retracted.  Fixing the control then exposed that the search was
hopeless *by construction*: 66 equations in 8 unknowns means a random RHS lands
in the column space with probability ~`p^-58`.  Same error as C3 with different
numbers.

**A16 — msolve reports a FALSE EMPTY on parenthesised input.**  0 seconds, exit
0, no warning, basis `[1]` — indistinguishable from a real emptiness proof.
Demonstrated with two files differing only by parentheses.  *This is the only
error today that would have been reported as a mathematical claim about the
Jacobian conjecture.*  The sole tell was the wall time, and I looked because a
170-variable system cannot finish instantly — **not** because the verdict looked
wrong.  It looked exactly like the result I wanted.

### Caught before reaching any writeup

* **`sp.solve` returning `[]`** on a symbolic-coefficient linear system means
  *generically inconsistent* — i.e. conditions exist — not empty.  I nearly wrote
  "the edge ladder is inconsistent at rung 17."
* **`sympify` symbol identity, twice.**  `Symbol('alpha')` is not
  `Symbol('alpha', nonzero=True)`.  First it printed a bogus `alpha - alpha`
  "condition"; later it made `factor` display `16*C_7(rho)^3` while the equality
  test returned False.  Same root cause both times.
* **Truncated-ansatz artefact.**  Rung 13 of the residual ladder first reported
  "8 residual conditions" because the loop broke at `D = 6`, far below the
  polygon's allowed support `[6,30]`.  At the correct support: none.
* **Descent off-by-one.**  The `i=m` partner at rung `d` is `q_{d-7}`, not
  `q_{d-8}`.
* **A sign in a test** (`{Q,R}` identity).  The residual was exactly twice the
  correct term, which confirmed the identity rather than refuting it.

### The one that went both ways

I hypothesised from the edge ladder that `A_i(rho) = 0` cascades down the edge,
and **refuted it** — five variants, three random points each, all failed.  Then
the residual ladder **established it** for `i = 7, 6`.  Both are right: the edge
ladder genuinely cannot force it (homogeneous RHS); the residual ladder can
(nonzero RHS).  The refutation was sound about the instrument and wrong as a
guess about the geometry.

### Carried from earlier

A1–A11 (mine), B1–B2 (caught by Codex), C1–C6 (pre-existing campaign), D1
(knock-on).  Full text in `ERRATA.md`.

## 4. The pattern

Sixteen of my own errors are now catalogued.  Sorted by mechanism:

* **Instrument bugs misread as mathematics** — A1, A2, A3, A14, A15, A16, plus
  the `sp.solve` and truncated-ansatz catches.  **This is the dominant class**,
  and A16 is its worst case because the false reading was EMPTY.
* **Re-introducing a known failure** — A13.  The guard, not the note, is what
  works; `runner.sh` now refuses parenthesised msolve input outright.
* **Scope and overclaim** — A8, A10, B1, B2.
* **Resource self-sabotage** — A6, A7, A13.
* **Arithmetic/aliasing** — A4, A5, A11, the off-by-one, the sign.

Four times now a tool's silence or failure has been read as a verdict (C6, A3,
A14, A16).  **Never read "no solution returned" as "no solution exists," and
never read a fast completion as a strong result.**

## 5. Collaboration

Codex has been idle since 07:32 UTC (`e4fa5ce`).  He received **OPUS43-014** at
16:22 with two tasks — generalise the upper edge into a degree-pair filter and
point it above 125, and check whether `disc = 0` is new relative to his
`p11zero_full_sat` export — plus the A13/A14/A16 corrections I owe him.  He has
not yet acted.

## 6. Infrastructure

The container restarts roughly **hourly** (15:42, 16:43).  `/tmp` survives; the
queue checkpoints to the remote after every job, so nothing has been lost.  All
job timeouts are now 2400 s — a 7200 s Singular run was killed mid-flight at
16:43, and no longer job can ever complete here.

## 7. Honest position

No counterexample.  No exclusion.  The pentagon is **NO VERDICT** and (72,108)
remains the sole surviving degree pair below 125.  What changed today is that the
pentagon is now heavily *pinned* by arguments that cost seconds rather than
gigabytes, and there is one sharp prediction left to test:

> if the cascade continues, `P(x,rho)` and `P_y(x,rho)` are both constant in `x`,
> forcing `Q(x,rho) = q_0(rho) + q_3(rho) x^3` with every other `q_k(rho) = 0`.

`q_12(rho)` and `q_11(rho)` already vanish identically.  Breaking that prediction
excludes (72,108); satisfying it hands back a very small family to search.
