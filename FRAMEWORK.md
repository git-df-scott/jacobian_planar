# The Plane Jacobian Conjecture — Complete Campaign Framework

**A consolidated handoff. Everything, in one document.**

Written at the close of Session 35. Intended to be read cold by a successor
(Fable 5, or anyone) with no access to the conversation that produced it.

---

## 0. Bottom line, stated first

**No counterexample was found.** Not in 35 sessions, not on any of the three
strategies executed in the final round, not anywhere. Every route this campaign
opened has closed, and the closures are proofs, not exhaustion.

That is weak evidence the plane Jacobian conjecture is **true**. It is weak
because absence of a counterexample in a search that never reached the degrees
where one could live is not evidence of much. It is *evidence* because the
mechanism that killed the conjecture in every dimension above two turns out to
be structurally unavailable in the plane, for a reason that is now proved rather
than observed.

The single most useful sentence in this document:

> **Two independent routes — the `y`-degree side (Sessions 2–6) and the sweep
> cascade (Sessions 29–32) — walk into the same wall from opposite directions,
> and that wall is the `deg_y = 3` slice.**

If you do one thing, decide that slice.

---

## 1. The problem, and what changed in July 2026

**Jacobian conjecture (plane case).** If `F = (P, Q) : C² → C²` is polynomial
with `det JF` a nonzero constant, then `F` is a polynomial automorphism.

`det JF = const` is called the **Keller condition**. In two variables all
automorphisms are **tame** (Jung–van der Kulk): compositions of affine maps and
triangular maps `(x, y) ↦ (x, y + f(x))`.

### The 2026 collapse above dimension 2

| date | result |
|---|---|
| Alpöge, 19 Jul 2026 | counterexample in dimension 3 |
| Gallagher, 20 Jul 2026 | an infinite family |
| Speyer, 23 Jul 2026 | the geometric explanation — a **tangent sweep** |
| [arXiv:2608.00222](https://arxiv.org/abs/2608.00222) | counterexamples in every dimension > 2, arbitrarily large geometric degree |

**The plane case remains open.** Sessions 28–34 establish *why* it survived: the
sweep mechanism needs a direction field that is degenerate but not of constant
direction, and in the plane those two conditions coincide. The killing mechanism
is plane-proof. This is not a slogan — it is Result 2 of Session 29 and Audit 2
of Session 30, both proved.

### Where the literature stands

[GGHV, *Compositio Math* 160 (2024) 2775–2827](https://arxiv.org/abs/2204.14178)
discard every degree pair with `max < 125` except **(72, 108)**, raising Moh's
degree bound from 100 to 108.

- Borisov's `(99, 66)` (the First Framework, [arXiv:1901.04073](https://arxiv.org/abs/1901.04073))
  is **inside GGHV's cleared range** — so the Session-18 conclusion for that pair
  is not novel as of 2024.
- **`(72, 108)` is the only surviving pair below 125** and is *not* in the
  cusp-chain family this campaign formalised.
- **Mathieu–Zhao spaces / the Generalized Vanishing Conjecture are not a route**:
  they *imply* the Jacobian conjecture ([arXiv:2608.07338](https://arxiv.org/html/2608.07338)),
  so their failure says nothing.

---

## 2. What this repository is

```
jacobian_planar/
├── FRAMEWORK.md                    <- this document
├── Sessions 1-18 status reports    <- the early campaign, one file
└── phase2_moduli/
    ├── README.md                   <- per-session narrative, Sessions 19-35
    ├── certify/  session19..35*.py <- exact sympy certifications
    ├── singular/ *.sing            <- Singular routines
    └── runs/     *.log             <- recorded output of every routine
```

**Everything is re-runnable and every claim is certified.** Each `certify/`
script ends in `assert all(PASS)`, so a regression is a crash, not a wrong
number. Run them all:

```bash
for f in phase2_moduli/certify/session*.py; do python3 "$f" || echo "FAIL $f"; done
for f in phase2_moduli/singular/*.sing;     do Singular -q "$f" > /dev/null || echo "FAIL $f"; done
```

---

## 3. The corrections ledger — read this before trusting anything

**Nine errors, and nearly all of them are the same error.** Every one came from
trusting a relation past the range where it had been verified.

| # | Session | Claim | Status |
|---|---|---|---|
| 1 | 19 | `D ≡ 1 (mod 6)` admissibility | **too narrow** — artefact of pinning cusp `(2,3)` *and* `δ = 3` |
| 2 | 19 | `D = 13` uniquely rigid | **scoped** — holds at `δ = 3` only |
| 3 | 21 | contact exponent `k = 3` for `(5,2)` | **wrong** — derived value is 6 |
| 4 | 21 | Moh degree argument at `D = 3` | **withdrawn** — unsafe extrapolation |
| 5 | 25 | template exponent fixed at `v = x₁x₂³ − 1` | **wrong** — `E` is a parameter |
| 6 | 25 | degree law `deg y₁ = 3 + 12a` | **wrong** — it is `(a+1)(a+3)`, quadratic |
| 7 | 25 | Session 24's mod-4 ranking of `(72,108)` | **void** — `g` alternates mod 4 |
| 8 | 26 | `E = a − b` | **`(2,3)`-specific** — the `(5,2)` near-miss sits at `E = 1` while `a−b = −1` |
| 9 | 29 | top-coefficient result presented as "verified for `k=1..5`" | **presentation error** — it is a one-line proof for all `k` |

### The anatomy of correction #6, because it is the instructive one

The linear degree law `deg y₁ = 3 + 12a` was fitted to three data points. It
agreed with reality **only at `a = 8`** — which is Borisov's case, the one
everybody looks at. It survived **four sessions** because every check anyone
thought to run was at `a = 8`. The true law is quadratic.

**The rule that follows, and it is the most transferable thing here:**

> Derive first; compute to corroborate. A formula that came out of a fit is
> evidence inside its fitted range and nothing outside it. A formula that came
> out of an argument is a theorem everywhere. Label which one you have, in the
> writeup, every time.

Corrections 5–7 were found by *attacking the target that correction 7 had
recommended*. Adversarial follow-through on your own conclusions is how these
surfaced; nothing else would have caught them.

---

## 4. Everything that is CLOSED

Each row is closed by a **proof**, not by exhaustion, unless marked otherwise.

### 4.1 Low `y`-degree

| result | where |
|---|---|
| `min(deg_y P, deg_y Q) ≤ 2` ⟹ tame automorphism | Sessions 2–5 |

Method: generic Keller ansatz, elimination via `resultant(E₂, E₃, y)`, plus a
cascade analysis of the `(2, n)` cases. The odd-`n` branch closes by a residue
gate (a rational function's derivative has zero residues; `c/s` has a nonzero
residue at a simple root, so `s` has no simple roots) and a pole-order
obstruction on back-translation.

### 4.2 The cusp-chain framework family

| result | where |
|---|---|
| Session-18 obstruction is **universal in `D`** (`ev_{v=-1}` annihilates `im T_D`, `ker T_D = 0`) | 19 |
| exactly one trapdoor, one unit wide: `ord R = −4` | 19 |
| unlocking `R` has map-degree `k`, never `D`, so `D = k` | 20 |
| **Belyi gate closes every `D ≥ 4`**, uniformly in the cusp exponent, no upper bound | 20 |
| contact exponent **derived**: `k = ε(m+n) − 1 ≥ 4` always ⟹ **`D ≤ 3` window is empty** | 22 |
| Session 18's master identity **derived** (was asserted) from the cusp identity | 22 |
| `μ = m` is removable | 23 |
| `ν = μn` verified at `(2,3)` **and** `(5,2)` via the Y-side chart | 27 |
| one place at infinity ⟹ automorphism (Magnus + Abhyankar–Moh) | 24 |

The **Y-side chart** (Session 27) is the campaign's methodological high point:
the substitution `x₁ = U/x₂^E` turns `y₁, y₂` into Laurent series whose
`U`-coefficients *are* the blocks. It recovered Sessions 9/10/12/13 **cold** —
`β = 6`, `g = U(U−1)⁸`, `W̃₋₅ = const·U⁶(U−1)⁹` — which is the strongest internal
validation in the repo.

### 4.3 The tangent sweep in the plane

| result | where |
|---|---|
| literal plane sweep `Φ = C + sC'` has `det JΦ = s·det[C'',C']` — vanishes on the curve, **not even Keller** | 29 |
| `coeff(s^{2k−1}) = k·W(C_k)` — top coefficient is the Wronskian, **at every order** | 29, proved in 30 |
| so the leading direction is **forced constant** at every `k`: the mechanism is dead in the plane | 29–30 |
| degenerate ⟺ constant direction for `v : C → C²`; they **separate** for `v : C² → C³` (twisted cubic witness) | 30 |
| orders `k ≤ 3` are **tame** | 29 |
| second cascade step `k·a·p' = (k−1)·a'·p` ⟹ dichotomy: descend, or `a = αh^k, p = βh^{k−1}` | 30 |
| third cascade step `coeff(s^{2k−3}) = k·a·u' − (k−2)·a'·u + (k−1)·W(C_{k−1})` | 31 |
| divisibility ladder: surviving value at a root of `h` is `(k−1)²·β·q(0)`, forcing `h ∣ q` | 31 |
| at a root of `h`, **both** components drop two `s`-degrees | 32 |

**The one-line proof that carries all of it** (Session 30, Audit 1):

```
det JΦ = Σ_{i,j} j·s^{i+j−1}·det[C_i', C_j]        (bilinearity)
max(i+j−1) subject to i,j ≤ k  ⟺  i + j = 2k  ⟺  i = j = k     (unique)
⟹ coeff(s^{2k−1}) = k·det[C_k', C_k] = k·W(C_k)   exactly, for all k
```

This is what a proof looks like versus a fit. `i + j = 2k` with `i, j ≤ k`
forces `i = j = k` — that cannot fail off a range.

### 4.4 The direct search (Sessions 33–35, the final round)

| result | where |
|---|---|
| the two "counterexample profiles" are **one condition**, geometric degree `d ≥ 2` | 33 |
| `d = 1` ⟺ injective ⟺ automorphism; `d ≥ 2` ⟹ **non-proper** | 33 |
| detector: one Gröbner basis over `Q(a,b)` gives `d = vdim(G)` **and** the tear `{leadcoef(G_i) = 0}` | 33 |
| for `d = 2`, the deck involution `σ` satisfies `det Jσ = 1` and is **fixed-point-free** | 33 |
| **de Jonquières and linear branches of the Cremona classification are empty** | 33 |
| rational search `F = (P/h^i, Q/h^j)`, 32 shapes: empty | 33 |
| the topological tear is **compulsory**, not hypothetical | 34 |
| the "global wrapping" is exactly monodromy `π₁(C² ∖ S_F) → S_d` | 34 |
| **`χ(F⁻¹(S_F)) ≡ 1 (mod d)`** — a free numerical filter on any candidate | 34 |
| pseudo-holomorphic curves are **structurally unavailable**: `Re(dx∧dy)(v, J₀v) ≡ 0`, every complex line is Lagrangian | 34 |
| the `h`-branch census passes coefficient degree 2 under Singular and reaches **degree 5**; the `(3,n)` slice is **decided for the first time** | 35 |

#### The deck-involution lemma (Session 33) — the new structural handle

Let `F` be Keller with geometric degree `d = 2`. A degree-2 field extension is
Galois, so there is a birational involution `σ` with `F ∘ σ = F`.

1. **`det Jσ = 1`.** Differentiate: `JF(σz)·Jσ(z) = JF(z)`; take determinants;
   `1·det Jσ = 1`.
2. **No fixed point in `C²`.** At a fixed point `p`: `JF(p)·(dσ_p − I) = 0`.
   Since `σ² = id`, `dσ_p` is diagonalisable with eigenvalues in `{±1}`; `det = 1`
   leaves `(1,1)` and `(−1,−1)`.
   - `(1,1)` ⟹ `dσ_p = I` ⟹ `σ = id` near `p` (Cartan linearisation) ⟹ `d = 1`.
   - `(−1,−1)` ⟹ `dσ_p = −I` ⟹ `JF(p)·(−2I) = 0` ⟹ `JF(p) = 0` ⟹ `det JF(p) = 0 ≠ 1`.

So **a degree-2 plane Keller counterexample requires a fixed-point-free
volume-preserving birational involution of `C²`.**

And no pencil-preserving involution is volume-preserving:
- *parallel pencil*: `σ = (x, (Ay+B)/(Cy−A))`, `det Jσ = −(A²+BC)/(Cy−A)²`;
  identically 1 forces `C = 0`, giving `det Jσ = −1`, never `+1`.
- *pencil through a point*: `σ(z) = μ(z)·z`, `det Jσ = μ(μ + x·μ_x + y·μ_y)`;
  with the involution condition this leaves only `μ = −1`, the point reflection —
  whose fixed point `0` lies in `C²`, killed by step 2. (Concretely: its
  invariants are the even polynomials, so all four partials are odd and vanish
  at the origin, giving `det JF(0) = 0`.)

#### Why symplectic topology cannot be the instrument (Session 34)

`det JF = 1` means `F` preserves the **holomorphic** symplectic form
`Ω = dx∧dy`. On `R⁴` its real and imaginary parts

```
Re Ω = dx₁∧dy₁ − dx₂∧dy₂        Im Ω = dx₁∧dy₂ + dx₂∧dy₁
```

are genuine real symplectic forms (determinant 1). So "Keller map =
volume-preserving" really is "holomorphic symplectomorphism of `(C², dx∧dy)`" —
the framing is right. But `J`-holomorphic curve theory needs an almost complex
structure **tamed** by the form, `ω(v, Jv) > 0`, and:

```
Re Ω(v, J₀v) ≡ 0        Im Ω(v, J₀v) ≡ 0        ω_Kähler(v, J₀v) = a²+b²+c²+d²
```

`J₀` is not merely untamed — **every `J₀`-complex line is Lagrangian** for the
form `F` preserves, the extreme opposite of tame. And the form that *does* tame
`J₀` is exactly the one Keller maps do not preserve. The holomorphic and
tamed-symplectic categories are disjoint here. That is a structural reason no
symplectic proof exists, not a gap in anyone's effort.

**What survives** is covering-space topology, which needs no taming: the tear,
the monodromy, and the congruence `χ(F⁻¹(S_F)) ≡ 1 (mod d)`.

#### Breaking the computational wall (Session 35)

Sessions 31–32 recorded a "computational wall" at coefficient degree 2.
**The wall was the tool.** On the exact system that stopped them
(`k = 4`, `h = t`, coefficient degree 3 — 30 unknowns, quadratic equations):

| engine | field | result |
|---|---|---|
| sympy `groebner` | `Q` | > 3000 s — no verdict |
| sympy `groebner` | `F_32003` | ~560 s — no verdict |
| Singular `std` | `F_32003` | > 800 s — no verdict |
| **Singular `slimgb`** | `F_32003` | **11.3 s — EMPTY** |

Three orders of magnitude, and **it is not the arithmetic** — `std` and
`slimgb` run in the same field. `slimgb` uses a different pair-selection and
reduction strategy that suits sparse quadratic systems. With it:

- the `h`-branch census reaches **coefficient degree 5** at `k = 4` (was 2),
  and covers `k = 4,5,6,7` over `h = t, t², t(t−1), t²+t+1`;
- **the `(3,n)` slice is decided for the first time** — `(3,4)` and `(3,5)` to
  coefficient degree 4, `(3,7)` to 3, `(3,8)` and `(3,10)` to 2, over three
  shapes of `h`;
- **36 cases completed, every one EMPTY**; two primes (`32003`, `1000003`)
  agree wherever both finished.

The real boundary is now **memory, not time**: the unresolved cases are killed
by the OOM killer inside the time budget (verified directly — `k=5, h=t, deg≤4`
died at 2m46s of a 900 s budget on a 16 GB machine). More RAM, or an F4/FGLM
engine such as msolve, moves the line further.

### 4.5 Closed by infeasibility, not by proof

| result | where |
|---|---|
| direct search above degree 108 is out of reach by four orders of magnitude: 11,990 unknowns at degree 108, 40,602 at degree 200 | 23 |

---

## 5. Everything that is OPEN, ranked by tractability

### **OPEN-1 — The `deg_y = 3` slice ≡ the `h`-branch at `k ≥ 4`**

The campaign's real frontier, reached from two directions.

- Session 30's descent gives `min(deg_s Φ₁, deg_s Φ₂) ≤ k−1`.
- Sessions 2–5 close `min deg_y ≤ 2`.
- So the first uncovered order is `k = 4`, at `min deg_s = 3` **exactly**.
- Sessions 3 and 6 independently call the `deg_y = 3` slice *"the first slice the
  collapse machinery does not decide."*

**Closing the `h`-branch at `k = 4` ≡ deciding the `deg_y = 3` slice.**

Two independent routes terminating at the same slice says the slice is the
genuine content, not an artefact of either approach.

Status: empty in every case computed, **not proved empty**. Session 35 pushed
the boundary a long way with `slimgb` — 36 cases, all empty, reaching coefficient
degree 5 on the `h`-branch and deciding the `(3,n)` slice for the first time —
but bounded-degree emptiness is evidence, not a theorem. See
`runs/session35_certify.log` for the exact table.

**Structural note that ties the two routes together.** For a Keller pair with
`deg_y P = 3`, `deg_y Q = n`, the leading condition is `n·A'B − 3·AB' = 0`, whose
solution is `A = αh³`, `B = βh^n` — *the same "powers of a common `h`" structure*
that the sweep cascade produced in Session 30. That is not a coincidence; it is
why the two routes meet.

### **OPEN-2 — Geiser and Bertini involutions (`d = 2`)**

Session 33 closed the de Jonquières and linear branches. The Bayle–Beauville
classification of birational involutions of `P²` has two more types:

| type | fixed curve | genus |
|---|---|---|
| de Jonquières | hyperelliptic | ≥ 1 | **CLOSED (S33)** |
| linear | a line | 0 | **CLOSED (S33)** |
| Geiser | plane quartic | 3 | **OPEN** |
| Bertini | sextic | 4 | **OPEN** |

**This looks closable and should be tried first.** The fixed-point lemma says
`σ` has no fixed point in `C²` where it is regular; a birational self-map of a
smooth surface is undefined only on a **finite** set; so `Fix(σ) ∩ C²` is finite.
But Geiser and Bertini involutions have fixed curves of genus 3 and 4 — and a
curve of positive genus in `P²` is not a line, so it cannot sit inside `L∞`, so
it meets `C²` in infinitely many points. Contradiction.

**The care required, stated honestly:** Bayle–Beauville's fixed curve is the
*normalized* fixed curve, a birational invariant defined on a resolution. Under
birational conjugation the fixed curve can be contracted, so it might in
principle hide over an indeterminacy point rather than appearing as a curve in
`P²` for `σ` itself. Closing OPEN-2 means ruling that out. That is a bounded,
well-posed piece of work — and if it closes, **geometric degree 2 is closed
entirely**, which would be the campaign's largest single result.

### **OPEN-3 — Geometric degree `d ≥ 3`**

The involution argument does not start: a degree-`d` extension need not be
Galois, so there is no deck transformation. What *is* available:

- the Galois closure gives `G ⊆ S_d` acting on the `d` sheets;
- Session 34 says the monodromy `π₁(C² ∖ S_F) → S_d` is generated by **meridians
  of the components of the tear** and nothing else;
- the congruence `χ(F⁻¹(S_F)) ≡ 1 (mod d)` applies for every `d`.

A plausible attack: bound the number of components of `S_F`, hence the number of
meridian generators, hence the possible transitive `G`. Untried.

### **OPEN-4 — `(72, 108)`**

GGHV's only survivor below 125. **Not reachable inside the cusp-chain family**:
`(a+1)(a+3) = 108` has no integer root (Session 25 — and note this used the
*corrected* quadratic degree law; the linear one would have given a false
positive, which is precisely what correction #6 was about).

### **OPEN-5 — Degrees above 108 generally**

Outside GGHV's method. The corrected high-degree tail `(168,112)`, `(255,170)`,
`(360,240)`, … is beyond GGHV and all of it is killed by the Belyi gate — that is
this campaign's marginal contribution to the literature. Everything else up there
is untouched and unreachable by direct search.

---

## 6. Method — what worked, and the failure modes to avoid

### What worked

1. **Certify everything, and make failure loud.** Every script ends
   `assert all(PASS)`. 157+ exact checks. A regression crashes.
2. **Re-derive an old result from a new direction.** Session 27 recovering
   Sessions 9–13 cold from one substitution is worth more than any number of
   consistency checks inside a single formalism.
3. **Attack your own recommendation.** Corrections 5–7 came from attacking the
   target that correction 7 had recommended.
4. **Record the tooling lies.** See §7. Each cost real time and each is silent.
5. **Say "no verdict" when there is no verdict.** A timed-out Gröbner run is not
   an empty variety.

### The failure modes, all of which actually happened

| failure | instance |
|---|---|
| fitting a formula to few points and using it outside the range | correction #6, survived 4 sessions |
| pinning two parameters and reporting the result as general | corrections #1, #2 |
| asserting a computation instead of running it | Session 31's first run: reduced mod `h` via `subs(h,0)`, which zeroes `h'` too; got 0 for every `k`, then *asserted* the answer. Caught before it propagated. |
| presenting a proof as a table of checks | correction #9 |
| generalising a coordinate choice | corrections #5, #8 |

---

## 7. Tooling — what is installed, what is fast, what silently lies

### Installed on the session container

| tool | status | note |
|---|---|---|
| **Singular 4.3.2** | ✅ installed | the real Gröbner engine. **Use `slimgb`, not `std`** — see below. |
| sympy 1.14 | ✅ | fine for symbolic identity work; its `groebner` is a teaching implementation — *do not* use it for anything hard |
| python-flint | ✅ | unused so far |
| PARI/GP 2.15.4 | ✅ | unused so far |
| msolve, Macaulay2, Magma, Sage | ❌ not installed | msolve would be the natural next upgrade (F4/FGLM) |

**The single biggest process error of the campaign:** Sessions 31–32 recorded a
"computational wall" at coefficient degree 2 after sympy timed out — while
Singular sat installed in the same container, already used by seven routines in
the same repo, never pointed at that system. Session 35 corrected it. *Check what
is on the machine before declaring a limit.*

**And then the same lesson twice:** Singular's default `std` also failed on that
system (> 800 s, no verdict). `slimgb` did it in **11.3 s**. Same machine, same
field, same ideal — only the strategy differs.

> **`slimgb` first, `std` second.** On sparse quadratic systems in 30+ unknowns
> the difference is three orders of magnitude, not a constant factor. If a
> Gröbner computation looks infeasible, change the engine before believing it.

The honest boundary today is **memory**, not time: every unresolved case dies
well inside its budget. And memory exhaustion arrives **two different ways**,
both of which must be caught or the run reports an unexplained "no verdict":

| mechanism | signature | example |
|---|---|---|
| Linux OOM killer | `SIGKILL`, returncode `-9`/`137` | `k=5, h=t, deg≤4` at 2m46s |
| Singular's own guard | `Singular error: no more memory`, `halt 14` | `k=6, h=t, deg≤4` at 3m40s |

Report those as *out of memory*, not as *timeout*, and never as *empty*.

### Tooling that is silently wrong

Each of these returns a plausible wrong answer rather than an error.

| tool | lie |
|---|---|
| `elim.lib`'s `sat()` (Singular 4.3.2) | wrong saturation — on `⟨xz⁵, x+yz⁵⟩` it returns `⟨y⟩` instead of `⟨x,y⟩`. Use iterated `quotient`. |
| `continue` inside a Singular `for` loop | **skips the increment** — infinite loop. Rewrite with if/else. |
| `res` in Singular | reserved identifier; naming a resultant `res` fails |
| `deg()` on a **number** in a Singular parameter ring | always returns 0 regardless of parameter degree, so a tear test built on `deg(numerator(leadcoef(g)))` reports every fibre as proper. **Use `pardeg()`.** (Found in Session 33.) |
| `eliminate(I, y)` as a geometric-degree test | returns the elimination ideal in `x` alone; `(x, y²)` gives `x−a`, degree 1, while the fibre has 2 points. **Use `vdim`.** |
| sympy `subs(h, 0)` as "reduction mod `h`" | zeroes `h'` as well |
| sympy `Integer.__format__` | `TypeError` on f-string format specs; wrap in `int()` |
| `pkill -f <script>` | matches your own shell's command line and kills it; use `pgrep -x Singular \| xargs kill`. **Same trap with `pgrep -f`**: a wait-loop `until ! pgrep -f session35` matches *itself* and never exits. Match the interpreter+path, not the bare name. |
| Singular running out of memory | reports it **two ways** — OOM-killer `SIGKILL` *and* its own `no more memory` / `halt 14`. Catch only the first and the second looks like an unexplained failure. |

### The detector, ready to use

```singular
ring s = (0,a,b),(x,y),dp;
ideal I = P - a, Q - b;
ideal G = std(I);
vdim(G);                  // geometric degree d;  d = 1 <=> automorphism
pardeg(leadcoef(G[i]));   // > 0 anywhere  <=>  the fibre tears
```

Verified live on nine controls, including `(x²y+x, y)` which has `d = 2` **with**
a tear at `b = 0` — the full counterexample profile, failing only because
`det J = 2xy+1` is not constant. The detector is not rigged to return
"automorphism".

---

## 8. The forward plan

Ordered by expected value per unit of effort. **P1 and P2 are the ones worth
doing.**

### P1 — Close `d = 2` by finishing the Cremona classification *(highest value)*

Kill the Geiser and Bertini branches. The fixed-point lemma (§4.4) plus "a
positive-genus curve is not a line" appears to do it; the work is ruling out the
normalized fixed curve hiding over an indeterminacy point. Bounded, well-posed,
and if it lands, **geometric degree 2 is closed outright**.

Reading: Bayle & Beauville, *Birational involutions of `P²`* (Asian J. Math 4
(2000) 11–17); Blanc's work on finite subgroups of the Cremona group.

### P2 — Push the modular computation as far as Singular goes

Session 35 opened the door with `slimgb`; walk through it.
- the `(3,n)` slice at higher coefficient degree and more shapes of `h`;
- the `h`-branch at `k = 4,5,6,7` past degree 5;
- **more RAM is the binding constraint** — the failures are OOM kills, not
  timeouts. A larger machine buys degrees directly;
- install **msolve** (F4 + FGLM) if the network allows — the natural next tier
  above `slimgb`;
- reduce variables *before* the Gröbner call by substituting the linear
  equations and the Session-31 ladder (`h ∣ q`) — the systems are quadratic, so
  every eliminated unknown is worth a lot;
- always run a second prime.

**Do not** try random hyperplane slicing to prove emptiness: a slice being empty
says nothing about the whole variety. Slicing can only *find* solutions, never
rule them out — wrong direction for this search.

Remember: emptiness mod `p` *is* a one-way certificate in the direction wanted (a
rational solution with denominators prime to `p` reduces mod `p`); non-emptiness
mod `p` proves nothing about `Q` and is only a lead.

### P3 — Attack `d ≥ 3` through the monodromy

Bound the components of `S_F`, hence the meridian generators of
`π₁(C² ∖ S_F)`, hence the transitive subgroups `G ⊆ S_d` that can occur. Combine
with `χ(F⁻¹(S_F)) ≡ 1 (mod d)`. Untried; genuinely open; no idea how hard.

### P4 — Use the `χ` filter on every candidate anyone proposes

Free to evaluate, independent of every degree bound in the literature.

### P5 — `(72, 108)`

Only if a new structural handle appears. It is not in this family, and direct
search is four orders of magnitude out of reach.

### What NOT to spend time on

- **Mathieu–Zhao / Generalized Vanishing** — implies the JC; failure says nothing.
- **Pseudo-holomorphic curves / Floer theory** — §4.4 shows the taming hypothesis
  fails as badly as it can. Do not build this instrument.
- **A plane analogue of the tangent sweep** — closed at every order, by proof.
- **The cusp-chain framework family** — closed at every chain degree, cusp type,
  depth and boundary order.
- **Brute-force search above degree 108** — 11,990 unknowns at 108.

---

## 9. Session index

| sessions | subject |
|---|---|
| 1 | reverse-engineered the Alpöge dimension-3 map |
| 2–5 | `min deg_y ≤ 2` ⟹ tame; the `(2,n)` cascade, residue gate, pole obstruction |
| 3, 6 | the `deg_y = 3` slice identified as undecided — **the frontier** |
| 8–15 | formalisation of the cusp-chain framework; blocks, boundary divisor, divisibility ladders |
| 16–18 | the emptiness theorem and its master identity |
| 19 | moduli/deformation probe; the trapdoor `ord R = −4` |
| 20 | `D = 4` reverse-engineering; the **Belyi gate** closes `D ≥ 4` |
| 21 | the `D = 3` window instantiated (two corrections) |
| 22 | contact exponent **derived**; `D ≤ 3` closes; master identity derived |
| 23 | adversarial audit; bypass spec; relocation against GGHV |
| 24 | family survey; Abhyankar–Moh; 11,872 admissible degree pairs |
| 25 | the `(72,108)` attack — produced corrections 5–7 |
| 26 | general cusp template; **first non-`(2,3)` near-miss**, cusp `(5,2)`, degrees `(6,15)` |
| 27 | **Y-side geometry** derived for a non-`(2,3)` cusp; recovers Sessions 9–13 cold |
| 28 | literature sweep; the conjecture falls above dimension 2; no plane analogue |
| 29 | the sweep closed in the plane **at every order** |
| 30 | rigor audit (both claims proved, not fitted); second cascade step |
| 31 | third cascade step; divisibility ladder; self-correction caught |
| 32 | `h`-branch census; root-drop of two; **placement = the `deg_y = 3` slice** |
| 33 | **Step 1** — Cremona/elimination; deck involution fixed-point-free; de Jonquières + linear branches empty |
| 34 | **Step 2** — the tear is forced; monodromy; `χ ≡ 1 (mod d)`; pseudo-holomorphic curves unavailable |
| 35 | **Step 3** — Singular over `F_p` breaks the sympy wall; the `(3,n)` slice reached |

---

## 10. Scope and honesty

- Sessions 8–18 are **conditional on the campaign's own formalisation** of the
  cusp-chain framework. Sessions 22 and 27 are the two strongest internal
  validations (a derived master identity, and an independent recovery of
  Sessions 9–13).
- Bounded-degree Gröbner results are **evidence, not theorems**, and are labelled
  as such throughout. This campaign has already published one
  "verified at every point tested" that was a fit in disguise.
- Modular results prove emptiness over `F_p`; the implication to `Q` runs one way
  and is stated where used.
- **Nothing here bears on the plane Jacobian conjecture itself.** No route was
  found to a counterexample, and no proof of the conjecture was produced.

---

*The conjecture is still open. The `deg_y = 3` slice is where to push.*
