# night6 — the integration test in CHARACTERISTIC ZERO

Everything in this file is **characteristic zero**, computed in exact rational
and number-field arithmetic, except §5 which is explicitly labelled modular.
No result here is reduced modulo anything.

**Nothing returned a non-unit ideal.** The stop rule of
`night6/RUNBOOK_KERNEL_NONZERO.md` was not triggered.

Instruments (all written this session, from scratch):

| file | what it is |
|---|---|
| `night6/char0_face.py` | the face system over Q; emits the Singular char-0 script (predecessor draft, repaired — §7) |
| `night6/char0_lib.py` | exact Q and Q[T]/(h) arithmetic: face point, face residual, E3 matrix, nullspace |
| `night6/char0_controls.py` | control C1 in characteristic zero (exact rational) |
| `night6/char0_linear.py` | the 38 x 32 affine-linear system of E1+E2, with tracked inconsistency certificates |
| `night6/char0_projective.py` | the projective (both-charts-at-once) computation and its Bezout certificate |
| `night6/char0_projective_run.py` | the driver that produced the verdict |
| `night6/char0_linear_modp_control.py`, `night6/char0_projective_modp.py` | controls C4 and C5: the same code paths run mod p against the recorded verdict |

Logs: `night6/CHAR0_FACE_modstd.log` (face system, Singular),
`night6/CHAR0_INTEGRATION_run.log` (the run below, 343 s),
`night6/CHAR0_KERNEL_run.log` (kernel stage alone),
`night6/CHAR0_CONTROL_C4_modp.log`, `night6/CHAR0_CONTROL_C5_modp.log`.
Machine-readable: `night6/char0_results.json`,
`night6/char0_linear_results.json`.

---

## 1. The face system over Q — eliminant and factorisation

Construction as in the mod-p instrument (`night6/e3_final.py`) but over Q:
`q = u*A` (deg A = 7, `A_k = q_{k+1}`), `t = u^2*B` (deg B = 10,
`B_k = t_{k+2}`), gauge `A_0 = A_7 = 1`,

        sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m == 0],   m = 0..17

the `m = 17` row vanishing identically over Q, rows `m = 0..10` eliminating
`B_0..B_10`, leaving **6 residual equations in `A_1..A_6`, total degree 9**
(term counts 47, 56, 65, 73, 71, 59).

Singular char 0 (`modStd(I,1)` from `modstd.lib` — `exactness = 1`, which the
library documents as computing a standard basis "for sure" — then `fglm` to
lex):

| quantity (char 0) | value |
|---|---|
| `dim` of the residual ideal | **0** |
| `vdim` | **35** |
| lex Gröbner basis | shape position (`A_1..A_5` each linear over `A_6`) |
| eliminant in `A_6 = q_7` | degree **35**, a **quintic in `A_6^7`** |

        9374377445732*A6^35
      + 62410476400737833472*A6^28
      + 265472843532245531128968765*A6^21
      + 591414847960503971284831143987840*A6^14
      + 586529490054134032292876680565455306752*A6^7
      - 1888043347611739526396142670327809715470336

**Factorisation over Q: the degree-35 eliminant is IRREDUCIBLE.** Two
independent instruments agree — Singular's `factorize` (one factor,
multiplicity 1) and flint's `fmpq_poly.factor` on the monic form (one
irreducible factor of degree 35, multiplicity 1).

So there is **exactly one irreducible factor `h`, of degree 35**, and the
single number field

        K = Q[T]/(h),   T = A_6 = q_7

carries **all 35 face solutions at once** — the 35 roots of `h` are the 35
values of `q_7`, and every computation below is done over the field `K`, hence
holds simultaneously at every one of them. Coverage is 35 of 35 in one family.

The handoff's "irreducible quintic in `T^7`, degree 35" is what is found, and
sharpened: the degree-35 polynomial itself is irreducible over Q, not merely
the quintic in `T^7`.

Monic form of `h`:

        T^35 + (42022389595776/6311981) T^28
             + (265472843532245531128968765/9374377445732) T^21
             + (147853711990125992821207785996960/2343594361433) T^14
             + (11279413270271808313324551549335678976/180276489341) T^7
             - (472010836902934881599035667581952428867584/2343594361433)

---

## 2. The face solution and the E3 kernel over characteristic zero

Rebuilt in `K` from the shape polynomials of the lex GB, then **verified by
exact substitution**:

| check (char 0, in K) | result |
|---|---|
| all 7 residual rows `m = 11..17` of the face system vanish | yes |
| `2*q*t' - 3*q'*t - u^2` identically zero, recomputed directly from `q,t` | **yes** |
| gauge `q_1 = 1`, `q_8 = 1` | yes |
| `t_2 != 0`, `t_12 != 0` (so `deg q = 8`, `deg t = 12`) | yes |

E3 operator `E3(p_,s_) = 3p_'t + 2q's_ - p_t' - 2q s_'`, `p_` on `u^1..u^8`,
`s_` on `u^2..u^12`:

| quantity (char 0, in K) | value |
|---|---|
| support-restricted E3 matrix | 18 x 19 |
| rank | **17** |
| **kernel dimension** | **2** |
| free columns of the rref | `s_11`, `s_12` |
| kernel basis vector 1 | `val p_ = 1, deg p_ = 7, val s_ = 2, deg s_ = 11` |
| kernel basis vector 2 | `val p_ = 1, deg p_ = 8, val s_ = 2, deg s_ = 12` |
| `E3(p_,s_)` identically zero in K for each basis vector (exact) | **yes, both** |
| relaxed matrix (`s_` allowed from `u^1`) | 19 x 20, rank 17, kernel dim 3 |

**The characteristic-zero kernel dimension is 2 — the same as the mod-p value.
No flag is raised.** (Semicontinuity gives only `<= 2` from the mod-p rank; the
value 2 here is measured directly over K, and both basis vectors are verified
by exact substitution.)

For the record: the coordinates of `q`, `t` and of the two kernel vectors are
elements of a degree-35 field whose rational coordinates run to about 371 bits
(~112 decimal digits).

---

## 3. What was computed, and how the four ideals were decided

The four ideals asked for, at the single factor `h` (all 35 face solutions):

        chart A : alpha = 1, beta a free unknown      variants: free, and
        chart B : alpha = 0, beta = 1                 Rabinowitsch
                                                      f_8*Wf = 1, g_12*Wg = 1

with `(p_, s_) = alpha*(p1,s1) + beta*(p2,s2)` the general element of the
char-0 E3 kernel, and the unknowns `f_1..f_8`, `g_1..g_12`, `r_1..r_12`.

They were decided **without a Gröbner engine**, by exact linear algebra over
`K`, using this structure of the identities:

* **E2** `3f't + 2p_'s_ + q'r - p_ s_' - 2q r' = 0` (19 rows) is affine-linear
  in `(f,r)` — `g` does not occur — and its *coefficient* matrix `M2` (19 x 20)
  does not involve `(p_,s_)` at all. All of the `(alpha,beta)` dependence sits
  in the inhomogeneous term, a homogeneous **quadratic**
  `b = alpha^2 b11 + alpha*beta b12 + beta^2 b22`.
  Measured over K: `rank M2 = 18`, `dim ker M2 = 2`, and the single left null
  vector `c` of `M2` satisfies `c.b11 = c.b12 = c.b22 = 0`, so **E2 is
  consistent for every `(alpha,beta)`** and its solution set is
  `(f,r) = x(alpha,beta) + lam1*w1 + lam2*w2` with `w1,w2` fixed and
  `x(alpha,beta)` homogeneous quadratic.
* **E1** `2f's_ + p_'r - p_ r' - 2q g' = 0` (19 rows): its `(f,r)` block is
  homogeneous **linear** in `(alpha,beta)`, `P = alpha*P1 + beta*P2`, and its
  `g` block `G` (19 x 12) is independent of `(alpha,beta)`, of **rank 12**,
  with a **7-dimensional left null space**.

Substituting the E2 solution set into E1 and applying the 7 left null vectors
`z` of `G` removes `g` entirely and leaves, for each `z`, one equation

        lam1 * L1_z(alpha,beta) + lam2 * L2_z(alpha,beta) = C_z(alpha,beta)

with `L1_z, L2_z` binary **linear** forms and `C_z` a binary **cubic** form
over `K`. A solution of the identities at `[alpha:beta]` forces this 7 x 3
system `[L1 | L2 | C]` to have rank <= 2 there, i.e. forces every 3 x 3 minor
— a binary form of degree 5 — to vanish at `[alpha:beta]`.

**Measured over K:**

| quantity | value |
|---|---|
| 3 x 3 minors of `[L1 | L2 | C]` | 35 of 35 **not identically zero** |
| gcd of those minors in `K[alpha]` (i.e. `beta = 1`) | **degree 0** (a nonzero constant) |
| common zero at `[alpha:beta] = [1:0]` | **no** |

so the minors have **no common zero in `P^1` over the algebraic closure**.
Hence for **every** `(alpha,beta) != (0,0)` the identities E1 and E2 already
have no common solution in `(f,g,r)` — E0 is not even needed, and imposing the
Rabinowitsch vertex conditions can only remove solutions further. By the
Nullstellensatz an empty variety over the algebraic closure is exactly the
unit ideal.

### Verdict

| factor `h` (deg 35, covers 35/35) | chart | variant | ideal |
|---|---|---|---|
| the only one | A (`alpha=1, beta` free) | free | **unit ideal** |
| the only one | A | Rabinowitsch `f_8*Wf=1, g_12*Wg=1` | **unit ideal** |
| the only one | B (`alpha=0, beta=1`) | free | **unit ideal** |
| the only one | B | Rabinowitsch | **unit ideal** |

        unit ideal = True  : 4 / 4
        unit ideal = False : 0 / 4

Stated as a measurement: **at all 35 face solutions, in characteristic zero,
in both charts and both variants, the identities E0, E1, E2 have no common
zero once `(alpha,beta)` is scaled to be nonzero.** Equivalently
`(alpha,beta) = (0,0)` is forced, hence `p_ = 0` and `s_ = 0`. This agrees
with the recorded mod-p verdict (`night6/INTEGRATION_TEST.md`, 68/68 unit) and
with the handoff's section 3a. Nothing disagrees with it. What the handoff's
section 3d then does with `p = s = 0` by hand is not part of this measurement
and is not claimed here.

---

## 4. Certificates

An emptiness verdict is only as good as its evidence, so each one here is
backed by an identity re-checked against the original data:

* **Bezout certificate for the verdict.** Cofactors `u_i(alpha)` over `K` with
  `sum_i u_i(alpha) * m_i(alpha) = 1` were produced from 2 of the 35 minors
  and the identity **expanded and verified exactly** (normalised to exactly 1).
  This proves the minors have no common root with `beta != 0` without relying
  on the gcd routine; the case `beta = 0` is settled separately by the
  `[1:0]` line of the table above.
* **Inconsistency certificates at individual points**, by a different code
  path (`night6/char0_linear.py`: the direct 38 x 32 augmented reduction of
  E1+E2 with the row operations tracked on an appended identity block). At
  chart B and at chart A `be = 0` and `be = 1`, each gives an explicit vector
  `c` with `c.M = 0` and `c.b != 0`, **re-verified against the original rows**
  in exact arithmetic: rank 32, 6 inconsistent rows, certificate verified,
  every time.

---

## 5. Controls

| control | characteristic | result |
|---|---|---|
| **C0** the char-0 face system reduces to the mod-p one | — | the 6 residual equations over Q reduce, up to a scalar, to `e3_final.build_residuals` at `p = 999983` and `p = 1000003`: **True, both** |
| **C1** predecessor's identity control | 999983, 1000003 | **True at both primes** (rerun this session) |
| **C1 (char 0)** the same control in exact rational arithmetic: coded `E0..E4` vs the direct bracket `[P,Q]_{u,z} = P_u Q_z - P_z Q_u` | 0 | **True**, 4 random rational seeds, all five identities |
| **C2 (char 0)** positive control, `(p_,s_) = (0,0)`, free | 0 | linear system 38 x 32, rank 30, **0 inconsistent rows — CONSISTENT**, solution space dimension 2, and the known point `f_1..f_8 = g_1..g_12 = r_1..r_12 = 0` (`f`, `g` constant, `r = 0`) **satisfies all 38 equations exactly**. So **NOT the unit ideal**, as required. |
| **C3 (char 0)** the same branch with the vertex non-degeneracy | 0 | on the *entire* solution space of E1+E2 at `(p_,s_) = (0,0)`, `g_1..g_12` are **identically zero**, so `g_12 = 0` throughout and `g_12*Wg = 1` is unsatisfiable: **EMPTY**. Exactly what the handoff's section 3d hand argument predicts. |
| **C4** the linear instrument run **mod p** | 999983, 1000003 | at all 17 face families (35 of 35 face solutions, both primes): `(p_,s_)=(0,0)` consistent with rank 30; chart B and chart A at `be = 0,1,2,3` inconsistent with rank 32, **certificate verified in every case**. Reproduces `night6/INTEGRATION_TEST.md`. |
| **C5** the projective instrument run **mod p** | 999983, 1000003 | **17 of 17 face families** at both primes: E2 rank 18 / kernel 2, `G` rank 12 / left-null 7, 35 of 35 minors nonzero, gcd degree 0, no common zero at `[1:0]`, **Bezout certificate verified**. Reproduces the recorded 68/68 unit-ideal verdict. |

C2 and C3 together are the hard gate: the instrument produces a **non-empty**
answer exactly where a solution is known to exist, and an **empty** one exactly
where the handoff's hand argument says there is none. C4 and C5 show that the
two code paths that produce the characteristic-zero verdict reproduce the
already-recorded modular verdict at all 35 face solutions at two primes.

The char-0 numbers agree with the mod-p ones on every quantity that both
measure: E3 kernel dimension 2, E2 rank 18 with kernel 2, `G` rank 12 with
7-dimensional left null space, 35 nonzero minors with gcd of degree 0, C2 rank
30 with a 2-dimensional solution space, chart rank 32 with 6 inconsistent rows.

---

## 6. Wall times

| stage | wall |
|---|---|
| face system over Q, `modStd` + `fglm` + `factorize` (Singular) | ~4 min |
| face point + E3 kernel in `K` (flint, exact) | 1.1 s |
| C1 char 0 | < 1 s |
| C2 / C3 char 0 (38 x 32 reduction over K) | 1.2 s |
| the projective verdict (E2 solve, `G` left null space, 35 minors, gcd) | 70 s |
| Bezout certificate | seconds |
| three independent spot checks with tracked certificates | ~30 s |
| **the whole char-0 driver end to end** | **343 s** |
| C4 mod-p control (17 families x 6 cases x 2 primes) | ~5 min |
| C5 mod-p control (17 families, 2 primes) | ~3 min |

A deterministic (non-`modStd`) char-0 `std` of the *face* system was also
started; it had run about 9 minutes without returning and was killed. It is
not needed for anything above: the face system's lex GB is corroborated by C0
(it reduces to the mod-p system already used), by the shape-position rebuild
of `(q,t)` being **verified to satisfy the face equation exactly in K**, and
by `vdim = 35` matching six independent instruments recorded in the handoff.
Two Gröbner encodings of the four ideals (an explicit one carrying `K` as a
ring variable, and an implicit one carrying `A_1..A_6` with the residual face
equations — `night6/char0_integrate.py`, `night6/char0_implicit.py`) were also
built and launched; both were far too slow to return, and were abandoned in
favour of the linear algebra above, which decides the same question exactly.

---

## 7. Note on the predecessor's draft

`night6/char0_face.py` was an untested draft and failed on first execution:
Singular's parser rejects the very long single-line `ideal I = ...;`
statement. It was repaired by emitting each generator as a sequence of short
`poly e_i = e_i + ...;` accumulation statements.

---

## 8. Scope

Characteristic zero throughout, except §5's C1/C4/C5 rows, which are labelled
modular. The verdict covers all 35 face solutions, both charts, both variants.
No claim is made here about anything downstream — about lifting to honest
polynomials in original coordinates, about the Newton polygons, or about the
subcase as a whole. What is measured is that in characteristic zero the E3
kernel direction does not integrate against E0, E1, E2 for any nonzero
`(alpha, beta)`.
