# night6 — the integration test in CHARACTERISTIC ZERO

**Status: PARTIAL — paused by order mid-run.** Stages 1 and 2 (face system
over Q, eliminant and its factorisation, face solution rebuilt and verified in
the number field, E3 kernel over char 0) are complete. Stage 3 (the four
Gröbner ideals per chart/variant, and the char-0 C2/C3 controls) had been
launched and had not returned when the pause order arrived; **no unit/non-unit
verdict of any kind was obtained over characteristic zero.**

Everything below is characteristic zero unless a line says otherwise.

Instruments (this session, from scratch, mirroring the mod-p instruments):
`night6/char0_lib.py` (exact Q and Q[T]/(h) arithmetic: face system, face
point, E3 matrix, nullspace), `night6/char0_integrate.py` (the five identities
and the Singular driver), `night6/char0_controls.py` (C1 char 0, exact
substitution helper), `night6/char0_run.py` (driver),
`night6/char0_face.py` (stage 1; predecessor draft, repaired — see §5).
Logs: `night6/CHAR0_FACE_modstd.log` (stage 1 Singular output),
`night6/CHAR0_KERNEL_run.log` (stages 1–2 as run).

---

## 1. The face system over Q — eliminant and factorisation

Same construction as the mod-p instrument (`night6/e3_final.py`), with exact
rational arithmetic: `q = u*A` (deg A = 7, `A_k = q_{k+1}`), `t = u^2*B`
(deg B = 10, `B_k = t_{k+2}`), gauge `A_0 = A_7 = 1`,

        sum_{i+j=m} (1 + 2j - 3i) A_i B_j = [m == 0],   m = 0..17

the `m = 17` row vanishing identically over Q, rows `m = 0..10` eliminating
`B_0..B_10`, leaving **6 residual equations in `A_1..A_6` of total degree 9**
(term counts 47, 56, 65, 73, 71, 59).

Singular, characteristic 0 (`modStd` + `fglm`, `modstd.lib`):

| quantity | value (char 0) |
|---|---|
| `dim` of the residual ideal | **0** |
| `vdim` | **35** |
| lex Gröbner basis | in shape position (`A_1..A_5` each linear over `A_6`) |
| eliminant in `A_6 = q_7` | degree **35**, a **quintic in `A_6^7`** |

        9374377445732*A6^35
      + 62410476400737833472*A6^28
      + 265472843532245531128968765*A6^21
      + 591414847960503971284831143987840*A6^14
      + 586529490054134032292876680565455306752*A6^7
      - 1888043347611739526396142670327809715470336

**Factorisation over Q: the degree-35 eliminant is IRREDUCIBLE.** Two
independent instruments agree: Singular's `factorize` (output in
`night6/CHAR0_FACE_modstd.log`) returns the single factor above with
multiplicity 1, and flint's `fmpq_poly.factor` on the monic form returns one
irreducible factor of degree 35, multiplicity 1.

So there is exactly **one irreducible factor `h` over Q**, of degree 35, and
the number field `K = Q[T]/(h)` carries **all 35 face solutions at once**
(coverage 35 of 35 in a single family). The handoff's "irreducible quintic in
`T^7`, degree 35" is what is found, sharpened: the degree-35 polynomial
itself is irreducible over Q, not merely the quintic in `T^7`.

Monic form of `h` (this is the `h` used downstream):

        T^35 + (42022389595776/6311981) T^28
             + (265472843532245531128968765/9374377445732) T^21
             + (147853711990125992821207785996960/2343594361433) T^14
             + (11279413270271808313324551549335678976/180276489341) T^7
             - (472010836902934881599035667581952428867584/2343594361433)

---

## 2. The face solution and the E3 kernel over characteristic zero

In `K = Q[T]/(h)` with `A_6 = q_7 = T`, the face solution `(q,t)` was rebuilt
from the shape polynomials of the lex GB and **verified by exact substitution**:

| check (char 0, in K) | result |
|---|---|
| all 7 residual rows `m = 11..17` of the face system vanish | yes |
| `2*q*t' - 3*q'*t - u^2` identically zero (rebuilt directly from `q,t`) | **yes** |
| gauge `q_1 = 1`, `q_8 = 1` | yes |
| `t_2 != 0`, `t_12 != 0` (so `deg q = 8`, `deg t = 12`) | yes |

E3 operator `E3(p_,s_) = 3p_'t + 2q's_ - p_t' - 2q s_'`, `p_` on `u^1..u^8`,
`s_` on `u^2..u^12`:

| quantity (char 0, in K) | value |
|---|---|
| support-restricted E3 matrix | 18 x 19 |
| rank | **17** |
| **kernel dimension** | **2** — *matches the mod-p value; no flag* |
| free columns of the rref | `s_11`, `s_12` |
| kernel basis vector 1 | `val p_ = 1, deg p_ = 7, val s_ = 2, deg s_ = 11` |
| kernel basis vector 2 | `val p_ = 1, deg p_ = 8, val s_ = 2, deg s_ = 12` |
| `E3(p_,s_)` identically zero in K for each basis vector (exact) | **yes, both** |
| relaxed matrix (`s_` allowed from `u^1`) | 19 x 20, rank 17, kernel dim 3 |

Coefficient size, for the record: the coordinates of `q`, `t` and of the two
kernel vectors are elements of a degree-35 field whose rational coordinates
run to about 371 bits (~112 decimal digits).

Because the free columns are exactly `s_11` and `s_12`, the kernel coordinates
`(alpha, beta)` of the handoff's parametrisation are literally the `u^11` and
`u^12` coefficients of `s_`, so the two charts

        chart A : alpha = 1, beta a free unknown
        chart B : alpha = 0, beta = 1

cover every nonzero kernel element exactly, as in the mod-p run.

---

## 3. Controls

| control | characteristic | result |
|---|---|---|
| **C0** char-0 face system reduces to the mod-p one | — | the 6 residual equations over Q reduce, up to a scalar, to the `e3_final.build_residuals` equations at `p = 999983` and `p = 1000003`: **True, both** |
| **C1** predecessor's identity control (mod p) | 999983, 1000003 | **True at both primes** (rerun this session) |
| **C1 (char 0)** the same control with exact rational arithmetic: coded `E0..E4` vs the direct bracket `[P,Q]_{u,z} = P_u Q_z - P_z Q_u` | 0 | **True at all 4 random rational seeds, all five identities** |
| **C2** `(p_,s_) = (0,0)`, free — must be NOT unit with the all-zero point verified | 0 | **NOT RUN — launched, did not return before the pause** |
| **C3** the same with vertex non-degeneracy | 0 | **NOT RUN** |

C1 is the hard gate on the coded identities and it passes in both
characteristics. C2/C3 over char 0 were not reached, so **the char-0 Gröbner
instrument is not yet validated and no char-0 ideal verdict is claimed.**

---

## 4. Stage 3 — what was set up and where it stopped

For the single factor `h` (degree 35, covering all 35 face solutions), the
four ideals were built over Q from the identities

        E0:  f'r - p_ g'                           = 0      (19 rows, u^1..u^19)
        E1:  2f's_ + p_'r - p_ r' - 2q g'          = 0      (19 rows)
        E2:  3f't + 2p_'s_ + q'r - p_ s_' - 2q r'  = 0      (19 rows)

with `(p_, s_) = alpha*(p1,s1) + beta*(p2,s2)` from the char-0 kernel above,
unknowns `f_1..f_8`, `g_1..g_12`, `r_1..r_12` (+ `be` in chart A), and the two
variants: free, and Rabinowitsch vertex non-degeneracy `f_8*Wf = 1`,
`g_12*Wg = 1`. E3 vanishes identically in the unknowns by construction (the
builder returns an empty E3 polynomial), which is the kernel property
re-derived inside the char-0 integration system.

Two encodings of the number field are implemented in
`night6/char0_integrate.run_singular0`:

* `mode='var'` — `T` carried as an extra ring variable with `h(T)` adjoined to
  the ideal (works for any degree);
* `mode='ext'` — Singular's algebraic extension `Q(a)` with `minpoly = h`.

**Where it stopped.** A first probe of the C2 control in `mode='var'` was
still running at the 2-minute mark when the pause order arrived; every
Singular process was then killed. The deterministic (non-`modStd`) char-0
`std` of the *face* system had also been running about 9 minutes without
returning and was killed; the stage-1 numbers above therefore rest on
`modStd`+`fglm`, cross-checked against the mod-p record (§3 C0) and against
flint's independent factorisation of the eliminant, but **not yet against a
deterministic char-0 `std`**.

Open engineering question for the resumption: which of the two encodings, if
either, brings the char-0 Gröbner runs into budget at 371-bit coefficients in
a degree-35 field. An untried third encoding, likely cheaper, is to keep
`A_1..A_6` as ring variables together with the 6 residual face equations and
the 19 unknowns `p_1..p_8, s_2..s_12` subject to the 18 E3 rows, with charts
imposed as `s_11 = 1` / `s_11 = 0, s_12 = 1` — legitimate precisely because
the free columns were measured to be `s_11, s_12` (§2) — which keeps every
coefficient a small integer.

---

## 5. Note on the predecessor's draft

`night6/char0_face.py` was an untested draft and failed on first execution:
Singular's parser rejects the very long single-line `ideal I = ...;`
statement. It was repaired here by emitting each generator as a sequence of
short `poly e_i = e_i + ...;` accumulation statements. The same wrapping is
used throughout `night6/char0_integrate.py`.

---

## 6. Scope

Characteristic zero for everything in §1–§2; the mod-p C1 rerun is labelled as
modular. No statement is made here about whether the char-0 integration ideals
are the unit ideal — that computation did not return.
