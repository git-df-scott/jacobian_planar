# Phase 2 — moduli-space deformation probe (Session 19)

Deformation / obstruction-theoretic probe of the Session-16–18 emptiness
theorem for Borisov's First Framework.

**Headline: no counterexample, and no candidate counterexample.** The probe
did not find a plane Jacobian counterexample and did not find a framework
instance that could become one. What it did find is a strengthening of the
theorem, the single hypothesis the theorem hangs on, and a combinatorial
proof that nothing in the framework family can attack that hypothesis.

## What was probed

Sessions 16–18 reduced every layer of the (99,66) decision system to one
operator equation on the Belyi-realization functional `R` along `E_{-2}`:

```
alpha^5 * T_D(R) = -c,      T_D(R) = (v+1)^4 * (3 v (v+1) R' - D R)
```

with `D` the cusp-chain degree (13 = First Framework, 23 = Second), `c` the
Keller constant, `alpha` the Session-13 rigidity scalar. Session 18 closed it
by evaluating at `v = -1`.

This probe treats that equation as defining an affine **moduli scheme** and
deforms it along the two coordinates the framework leaves free: the chain
degree `D`, and the pole order `J` of `R` at `U = v+1 = 0`. `J = 0` is exactly
Session 13/14's pole-fiber theorem (Theorem 3), which forces `R` to be a
polynomial. Nothing else in the framework is relaxed.

## Findings

**1. The obstruction is universal in the chain degree.** On the polynomial
locus the endgame has no solution with `c != 0` for *any* `D >= 1` —
`ev_{v=-1}` annihilates the image of `T_D` identically, and `ker T_D = 0`.
Session 18's transfer conjecture ("fatal whenever `D/3` is not an integer")
is therefore a theorem on the polynomial locus, fatal for every `D`. The
Second Framework (`D = 23`) and the isotope series die with the First.

**2. There is exactly one trapdoor, and it is sharp.** The emptiness proof
rests on Theorem 3 alone, and Theorem 3 is load-bearing by precisely one unit
of pole order:

| `ord_{U=0} R` | outcome |
|---|---|
| `>= -3` | `c = 0` — still obstructed |
| `= -4`  | `c != 0` attained, unique up to scale, in closed form, for every `D` outside `{3,6,9,12}` |

So the Session-18 argument is exactly *"QED modulo the pole-fiber theorem"*,
and the pole-fiber theorem is the one step a referee should attack.

**3. The trapdoor has no twin to walk through it.** The unlocking `R` has
numerator a quartic and `A(-1) != 0` for *every* `D`, so its map-degree in `v`
is exactly 4, independent of `D`. The framework's realization layer demands
map-degree `D`. The trapdoor is self-consistent only at `D = 4` — and the
frozen fork/cusp skeleton (`N = 2 deg p = 3 deg r + 1`, `D = N - 3`) admits
only `D = 1 (mod 6)`. `D = 4` does not exist in the family.

> **Corrected in Session 20 (below).** The `D ≡ 1 (mod 6)` step held only with
> the cancellation depth pinned to `δ = 3`. With `δ` free, `D = 4` *is*
> constructible. The conclusion survives for a different and stronger reason:
> the `D = 4` ansatz has 4 critical values and so realizes no Belyi map, under
> any skeleton.

**4. Why 13 (a by-product).** Rigidity of the skeleton's Belyi datum needs
`#unknowns - #equations = 1`, i.e. `(5D+13)/6 = D`, i.e. `D = 13` exactly.
Confirmed by direct Groebner computation: the non-degenerate solution variety
has parameter dimension 1 (the scaling orbit alone) at `D = 13`, dimension 2
at `D = 7`, dimension 3 at `D = 1`, and `D >= 19` is over-determined.
Borisov's chain degree is forced, not found.

> **Scope, sharpened in Session 20.** This uniqueness is *at cancellation depth
> `δ = 3`*. Imposing rigidity with `δ` free instead pins `δ = N - deg p - deg r`
> and yields one rigid skeleton per admissible Belyi degree — `D = 3, 8, 13, 18,
> 23, …` in the `(2,3)` family. What `δ = 3` singles out is Borisov's instance
> specifically.

**5. The resonance is real but Jacobian-silent.** Session 18's dismissed
"`M == 0` branch" `R ~ (v/(v+1))^{D/3}` becomes an honest rational function
exactly when `3 | D`. It is a genuine rank jump of the moduli space
(dim `1 -> 2` at pole order `J = D/3`) but always carries `c = 0`. At
`D = 3,6,9,12` it sits at `J <= 4` and absorbs the unlocking direction, which
is why those four degrees stay rigid at every pole order.

**6. Non-reducedness: present, and vacuous.** The raw endgame scheme is
non-reduced, but its only embedded structure is the multiplicity-5 component
`{alpha = 0}` from the `alpha^5` normalisation, and `alpha = 0` forces
`g == 0` against `deg g = 9`. After saturating it away the scheme is reduced,
1-dimensional on the polynomial locus (the bare scaling line `{R = 0, c = 0}`),
and the near-miss is a smooth point: tangent dimension = scheme dimension.
There is no non-reduced component and no branching to hide a counterexample in.

**7. `[P,Q] = x^r` cannot be deformed to `[P,Q] = 1` with the skeleton
frozen.** The Session-7 near-miss is a monomial-bracket instance,
`{y1,y2} = -h0 * x1^4 * x2^12`, i.e. `[P,Q] = x^r` with `r = (4,12)`. Every
member of the frozen skeleton has `y1 in x1^3 k[x1,x2]` and
`y2 in x1^2 k[x1,x2]`, so `x1^4` divides the bracket on the *whole*
deformation space — the constant term vanishes identically, not just to first
order. Reaching `r = (0,0)` requires changing the `x1`-support, i.e. changing
the combinatorial type. This is why the naive Newton-polygon deformation
search is empty and the chain-layer analysis was unavoidable.

---

# Session 20 — reverse-engineering a skeleton that accepts the trapdoor

Follow-up: can the `D = 4` requirement be engineered into existence by changing
the cusp type / cancellation depth, and the pole-order-4 `R` then hardcoded as
an ansatz?

**Steps 1 and 2 succeed. Step 4 fails, for a reason no polygon change can
repair.**

### Correction to Session 19

The `D ≡ 1 (mod 6)` admissibility claim was an artefact of pinning *both* the
cusp type to `(2,3)` *and* the cancellation depth to `δ = 3`. Freeing them,
**chain degree 4 is constructible**, and the skeleton is exhibited explicitly:

```
cusp type (m,n) = (2,5),  delta = 2,  Belyi degree N = 6
p = w^3 + (5/2)w^2 + (15/8)w + 5/16 ,   r = w + 1
p^2 - w r^5 = (20w^2 + 44w + 25)/256      (degree 2 = delta)
profile 3x2 / 1 + 1x5 / 1x4 + 2x1,  rigid,  chain degree D = 4
```

`D ≡ 1 (mod 6)` remains correct only for the `(2,3)`, `δ = 3` family it was
derived in; it is withdrawn as a general statement.

### The generalised trapdoor

Generalise the endgame to arbitrary cusp exponent `s` and contact exponent `k`
(`(k,s) = (4,3)` is the First Framework):

```
T_{k,s,D}(R) = (v+1)^k ( s v(v+1) R' - D R ) = -c
```

For every `(k,s,D)`: pole order `< k` forces `c = 0`, pole order `k` unlocks it,
and the unlocking `R` has numerator of degree exactly `k` never vanishing at
`v = -1`. So **map-degree(`R`) = `k` always — it never sees `D`**. The
realization layer demands map-degree `D`, so self-consistency forces `D = k`.
The right target was never "force `D = 4`"; it is *"force the chain degree to
equal the contact exponent"*.

### Where step 4 dies: the Belyi gate

With `k = D` forced, the unlocking `R` has one pole of order `D` at `v = -1` and
`D-1` simple critical points whose critical values are **distinct** — so `D`
critical values in all. A Belyi map has exactly 3, and affine post-composition
`R -> λR + ν` cannot change how many there are. Hence `R` is affine-equivalent
to a degree-`D` Belyi map only when `D ≤ 3`, uniformly in `s`.

At `D = 4` specifically, the ansatz has **4 critical values** and fails at every
cusp exponent `s` — by the Belyi gate when `s ∤ 4`, by resonance collision when
`s | 4`. This is independent of steps 1 and 2, so no re-engineering of the
polygon repairs it.

```
    s \ D:   2   3   4   5   6   7   8   9
    2     :  x   Y   x   .   x   .   x   .
    3     :  Y   x   .   .   x   .   .   x
    4     :  Y   Y   x   .   .   .   x   .
    5     :  Y   Y   .   x   .   .   .   .
    6     :  Y   Y   .   .   x   .   .   .
    7     :  Y   Y   .   .   .   x   .   .
    Y = clears the Belyi gate   . = fails   x = resonance collision
```

### Surviving window

Chain degree `D ≤ 3`. Six rigid skeletons survive the resonance gate; the
smallest is `(m,n) = (5,2)`, `δ = 2`, `N = 5`, `deg p = 1`, `deg r = 2`, `D = 3`,
constructed and certified explicitly. Two caveats:

- it still needs the pole-fiber theorem to **fail on its own geometry** — the
  trapdoor is not avoided there, only made degree-consistent;
- `D = 13` corresponds to Moh's pair `(99,66)`. Chain degrees 2 and 3 correspond
  to far smaller degree pairs, inside the range where the plane Jacobian
  conjecture is already proved. Checking that is the natural next step and is
  **not** done here.

---

# Session 21 — the D ≤ 3 window instantiated

Session 20 left one window open and one question unanswered: does the pole-fiber
theorem still close the endgame at `D ≤ 3`? **It does not** — the pole-fiber lock
genuinely relaxes there.

> **Superseded by Session 22 (below).** The `D = 3` instantiation assumed the
> contact exponent `k = 3` for the `(5,2)` cusp. Session 22 derives `k = 6`, so
> `D = 3` was never reachable and the window is empty. The pole-fiber analysis
> in this section stands; the conclusion drawn from it does not.

### The geometry, exact

```
cusp type (m,n) = (5,2),  delta = 2,  Belyi degree N = 5
p = w + 1 ,   r = w² + (5/2)w + 15/8
p^5 - w r² = (5/8)w² + (95/64)w + 1        (degree 2 = delta)
profile 1x5 / 1 + 2x2 / 1x3 + 2x1 ,  Riemann-Hurwitz 4+2+2 = 2·5-2
```

`r` squarefree, `gcd(p, wr) = 1`, fiber over 1 generic. The chain degree `D = 3`
is the multiplicity of `w = ∞` in the fiber over 1 — structurally the same slot
that carried `D = 13` in Borisov's degree-16 map.

### Why the lock relaxes

The pole-fiber argument, in any degree: `R`'s finite poles sit in a set of at
most two points and `R` realizes a degree-`D` Belyi map; the only fiber of a
Belyi map with ≤ 2 points is the totally ramified one; so a finite pole of `R`
is a single point of order **exactly `D`**. The endgame independently forces
pole order **exactly `k`**. Compatible

> **if and only if `D = k`.**

At `D = 13` (`k = 4`) the two collide, the pole is forced out to `v = ∞`, `R`
becomes a polynomial, and the framework dies — *that step, and only that step,
is Session 18's proof*. At `D = 3` with `k = 3` they agree. Certified across
`(s,D,k)` = (3,13,4), (3,23,4), (3,7,4), (3,19,4), (3,4,4), (2,3,3), (2,5,5),
(4,3,3), (5,3,3), (2,7,7).

### The Keller constant at D = 3

```
R = A(v)/(v+1)³ ,   A = -(16/3)v³ - 8v² - 2v + 1/3 ,   c = 1
```

Residual 0, pole order exactly 3 at `v = -1`, map-degree exactly 3, and a
genuine degree-3 Belyi map with profile `3 / 2+1 / 2+1`. Both degree-3 Belyi
profiles carry a totally ramified point, so the pole-fiber demand is satisfiable
here in a way it is not at any `D ≥ 4`. **Within every layer this campaign can
derive, the `D = 3` window is open.**

### Why that is still not a counterexample

Three independent reasons:

1. **The endgame is the last gate, not the whole system.** Box caps, the
   divisibility ladder, boundary rigidity and the Keller block were derived in
   Sessions 8–15 for the `(2,3)` cusp only. None has been rebuilt for `(5,2)`.
   Those gates are **untested, not passed**.
2. **`k = 3` is an assumption, not a derivation.** For `(2,3)` the contact
   exponent is `k = 4`. That `k = D = 3` for `(5,2)` is what the window *needs*;
   deriving `k` for a new cusp type means redoing the Y-side geometry.
3. **Degrees.** The `(2,3)` near-miss template gives `deg y1 = 3 + 12·deg p` and
   `deg y2 = 6 + 12·deg r` (verified), returning exactly Borisov's `(99,66)` at
   `(8,5)` — the pair sitting just past Moh's proven bound of 100. *That is why
   the First Framework lives at `D = 13`.* Here `(deg p, deg r) = (1,2)`, an
   order of magnitude smaller, landing far inside the range where the plane
   Jacobian conjecture is already a theorem. **A counterexample cannot live at
   `D = 3`.**

So the correct inference from `c ≠ 0` is not "counterexample" but *"one of the
gates in (1) must close `D = 3`"* — and identifying which is the open task.

### Scope correction on the sweep

The Belyi gate closes every `D ≥ 4` **with no upper bound** — the unlocking `R`
has `D-1` simple critical points with `D-1` distinct critical values for every
`D`. There is no ceiling such as `D = 225`, and none is needed. Verified for
`D = 4..25` and uniform in `D` structurally.

---

# Session 22 — the contact exponent derived, and the window closes

Session 21 left `D ≤ 3` open **under the assumption** that a `(5,2)` cusp has
contact exponent `k = 3`. This session derives `k` instead. The assumption was
false, and the window is empty.

### Two corrections to Session 21

1. **`k = 3` for the `(5,2)` cusp is wrong** — the derived value is `k = 6`. The
   "window is open" finding rested on `k = D = 3` and is **withdrawn**.
2. **The Moh degree argument at `D = 3` is withdrawn too.** The template
   `deg y1 = 3 + 12·deg p` is `(2,3)`-specific and extrapolating it to `(5,2)`
   was not safe — a plausible alternative scaling puts those degrees *above*
   100, not below. It is no longer needed: the closure is structural.

### The derivation

The cusp identity is exact for every `(m,n)`:

```
{y1, y2} = {W, y2} / ( m · (y2^n + W)^((m-1)/m) )
```

— the `y2^{n-1}` terms cancel identically, which is precisely why the cusp part
is Jacobian-silent. With leading blocks `y2 ~ q^-β v^-γ g^μ` and
`W ~ q^-λ v^-σ g^ν R`, the bracket has the exact closed form

```
{W,y2} = q^(-λ-β-1) v^(-σ-γ) [ (λγ-βσ) v^-1 g^(ν+μ) R
                              + (βν-λμ) g^(ν+μ-1) g' R
                              + β g^(ν+μ) R' ]
```

giving `s = β/m` and `G = ν + μ - μn(m-1)/m`, with the `g'` term carrying
`g^(G-1)`.

**Session 18's master identity falls out.** Feeding the First Framework's own
block data `(β,γ,λ,σ,μ,ν) = (6,18,5,54,2,6)` and `g = α(v+1)v^8` returns
`α^5 (v+1)^4 (3v(v+1)R' - 13R) = -c` exactly, collapse identity
`13(9v+8) - 117(v+1) = -13` included. Sessions 16–18 *asserted* this; it is now
*derived* — an independent end-to-end validation of the campaign's central
computation.

Two block exponents are forced: `ν = μn` (since `W = y1^m - y2^n` inherits
`g^{μn}` from `y2^n`) and `μ = m` (`y2`'s leading block is an `m`-th power).
Then `G = m+n`, and with `g = α U^ε ·(unit)`:

> **`k = ε(m+n) - 1`**

`(2,3)` at `ε = 1` gives 4 — the First Framework's value. `(5,2)` gives **6**.

### The closure

`m, n` coprime with `m, n ≥ 2` force `m + n ≥ 5`, and `ε ≥ 1`, so

> **`k = ε(m+n) - 1 ≥ 4` for every cusp type and every `ε`**, with equality only
> at `(m,n) = (2,3)`, `ε = 1` — Borisov's own cusp.

Session 20's self-consistency forces `D = k`, so `D ≥ 4` always; and Session 20's
Belyi gate closes every `D ≥ 4`. **The `D ≤ 3` window is empty** — not because
`D ≤ 3` is combinatorially impossible, but because no cusp can produce a contact
exponent that low. Every cusp type was re-run through the gate at *its own*
derived degree; all 24 rows close.

**Robustness.** The one extrapolated step is `μ = m`. It is not load-bearing:
leaving `μ` free, the window needs `G = μ(m+n)/m ≤ 4`, i.e. `μ ≤ 4m/(m+n) ≤ 4m/5
< m` — `y2`'s leading block would have to carry a `g`-power strictly below `m`,
contradicting its being an `m`-th power at all.

### Final state

| range | status |
|---|---|
| `D ≥ 4` | closed by the Belyi gate, uniformly in the cusp exponent, no upper bound |
| `D ≤ 3` | closed by the contact exponent — `k ≥ 4` always |

Every gate is shut. The published constructive framework family supports no
Keller map, for any cusp type, cancellation depth, boundary order or chain
degree.

**No counterexample was found, and this line of attack will not produce one** —
every opening the probes found has closed under its own derivation. This closes
the constructive candidates; the plane Jacobian conjecture itself is untouched
and remains open.

---

# Session 23 — three fronts: audit, bypass spec, literature relocation

Run at the request to attack on three fronts and find a counterexample.
**No counterexample was found.** Three findings, one of which changes how the
whole campaign should be described.

### Front 3 — adversarial audit of the Session-22 closure

The chain behind `k = ε(m+n) - 1`, step by step: `s = β/m`, `G = ν + μ - μn(m-1)/m`
and `k = εG - 1` are **symbolically derived**, not extrapolated. Two steps were
soft:

- **`μ = m` is now removable, not merely "not load-bearing."** With `ν = μn`,
  `G = μ(m+n)/m` must be a positive integer, so `m | μ(m+n)`; with `gcd(m,n)=1`
  that forces `m | μ`, hence `μ ≥ m`. The window needs `μ ≤ 4m/(m+n) < m`.
  Contradiction, without ever assuming `μ = m`. **The closure is tighter than
  published.**
- **`ν = μn` is the one real soft spot**, and it rests on the divisibility
  ladder — proved in Sessions 11–12 for the `(2,3)` cusp only.

Decoupling `ν` and `μ` completely and sweeping `(m,n,ε,μ,ν,s)`:

| condition | surviving tuples |
|---|---|
| `ν = μn` (the ladder's value) | **0** |
| `ν` decoupled | **870**, every one requiring `ν < μn` |

**The margin is exactly one unit.** For `(2,3)` with `μ = 2`, `G = ν - 1`, so the
window reopens iff `ν ≤ 5`. The actual value is `ν = 6`.

### Front 1 — what a bypassing skeleton must carry

The audit turns "propose a novel skeleton" into a falsifiable spec:

- **to bypass the `D ≥ 4` Belyi gate:** a realization layer that does *not* force
  `R` to realize a degree-`D` Belyi map;
- **to bypass the `D ≤ 3` contact-exponent gate:** `ν ≤ μn - 1` (ladder failure)
  *and* `β ≠ mn` (to dodge the resonance collision). For `(2,3)`: `ν = 5`, `β ≠ 6`.

Assigning block exponents to satisfy this is arithmetic. **Realizing them by an
actual curve configuration is not done, and a set of exponents is not a dual
graph.** The target is now precisely specified and remains unbuilt.

### Front 2 — relocated against GGHV

Guccione, Guccione, Horruitiner and Valqui (*Compositio Math* 160 (2024)
2775–2827; arXiv:2204.14178) list every degree pair with `max < 125` for a
hypothetical plane counterexample and discard them all **except (72,108)**,
confirming Moh's bound of 100 and raising it to 108.

- **Borisov's `(99,66)` is inside GGHV's cleared range.** The campaign's
  Session-18 conclusion for that pair is confirmed by published work along an
  independent route, and **is not novel as of 2024**. Earlier sessions here did
  not account for this.
- **`(72,108)` — the one surviving pair — is not reachable by this campaign's
  template**, whose degree pairs are `(3+12a, 6+12b)` with `2a - 3b = 1`:
  `(27,18), (63,42), (99,66), (135,90), (171,114), …`. The campaign says nothing
  about it.
- **Where the campaign does add something:** the template's members at
  `(135,90)`, `(171,114)`, `(207,138)`, … lie *beyond* GGHV's range and carry
  chain degrees `D = 18, 23, 28, …`, all killed by the Belyi gate. That is the
  real marginal contribution — not `(99,66)`.
- **A direct search is infeasible**: degree 108 gives 11,990 unknowns against
  ~23,000 dense bilinear equations; degree 200 gives 40,602. GGHV's route is
  structural because a search is not available.

### Next computation

Prove or refute `ν = μn` for one non-`(2,3)` cusp. It either closes the campaign
completely or opens it precisely, and unlike the other two fronts it is bounded
work.

---

# Session 24 — family survey: which one is least ruled out

### The axis that actually separates families

Magnus: for a non-automorphism Keller pair the leading forms are proportional
powers of one common form `H`, `P_top = c·H^(d1/r)`, `Q_top = c'·H^(d2/r)`,
`r = deg H | gcd(d1,d2)`. The number of **places at infinity** is the number of
*distinct roots* of `H`.

Abhyankar–Moh: one place at infinity ⟹ automorphism. Equivalently the plane JC
*is* the statement that a constant Jacobian forces one place at infinity. So:

| family | places `j` | status |
|---|---|---|
| `H = L^r` | 1 | **closed** by Abhyankar–Moh |
| `H` with ≥2 distinct roots | ≥2 | **open** — every counterexample lives here |

Degree is *not* an independent family parameter: across 11,872 Magnus-admissible
pairs with `max ≤ 200`, every single one forces a cusp ratio `(d2,d1)/gcd` with
both entries `≥ 2`. Choosing a different degree never escapes the cusp-chain
structure — only the place count does.

### Ranking

1. **`(72,108)` with `j ≥ 2`** — the only pair with `max < 125` GGHV could not
   discard. Cusp ratio `(2,3)`, *identical* to Borisov's `(99,66)`, so this
   campaign's whole apparatus transfers with no re-derivation. The difference is
   one congruence: the template reaches `g ≡ 1 (mod 4)` (Borisov's `g = 33`),
   and `(72,108)` needs `g = 36 ≡ 0 (mod 4)`. 82 multi-place `H`-configurations
   to work through.
2. **Multi-place frameworks at `max ≥ 125`** — same structure, unbounded degree,
   no literature coverage, but no distinguished instance to compute against.
3. **Dixmier / Weyl route** (`[P,Q] = 1` in `A₁`) — genuinely different
   obstruction theory; the Session-7 near-miss is a `[P,Q] = x^r` instance. Weaker
   as a target: the equivalence with the plane JC is only stable.
4. **One-place families, any degree** — closed by Abhyankar–Moh. Stated
   explicitly because it is where naive searches go.

### First thing to actually run

Rebuild the skeleton generator with `g ≡ 0 (mod 4)` and see whether a `(2,3)`-cusp
framework exists at `g = 36` at all. Bounded, the same shape as Sessions 19–22,
and it either produces the first framework instance at the literature's one open
pair or shows the congruence obstruction is structural.

**Caveat:** "most promising" means *least ruled out*, not likely. If the
conjecture holds, every family is empty, and nothing here is evidence otherwise.

---

# Session 25 — the (72,108) attack, and two errors it exposed

Ran at the `(72,108)` target. **No counterexample: it is not reachable by this
family.** But the attack broke two things I had published.

### Correction — the template exponent is a parameter

Sessions 21–24 treated `v = x1·x2³ - 1` as fixed. Sweeping `v = x1·x2^E - 1`,
the Jacobian collapses to a **monomial** — the near-miss condition — at exactly
one `E` per Belyi datum, and it is not always 3:

| `(deg p, deg r)` | monomial at |
|---|---|
| `(2,1)` | `E = 1` |
| `(5,3)` | `E = 2` |
| `(8,5)` | `E = 3` (Session 7) |

Three independent points give **`E = a - b = (a+1)/3`**, forcing `a ≡ 2 (mod 3)`.

### Correction — the degree law is quadratic, not linear

> **`deg y1 = (a+1)(a+3)`,  `deg y2 = (2/3)(a+1)(a+3)`**

| `a` | `b` | `E` | `D` | degrees | `g` | Session-23 said |
|---|---|---|---|---|---|---|
| 2 | 1 | 1 | 3 | (15,10) | 5 | (27,18) ✗ |
| 5 | 3 | 2 | 8 | (48,32) | 16 | (63,42) ✗ |
| 8 | 5 | 3 | 13 | (99,66) | 33 | (99,66) ✓ |
| 11 | 7 | 4 | 18 | (168,112) | 56 | (135,90) ✗ |
| 14 | 9 | 5 | 23 | (255,170) | 85 | (171,114) ✗ |

The linear formula `3+12a` agrees **only** at `a = 8` — which is why it survived
undetected. And `g = 5, 16, 33, 56, 85, 120` alternates mod 4, so **Session 24's
ranking reason (a mod-4 obstruction) is void.**

### `(72,108)` is still unreachable

`(a+1)(a+3) = 108` ⟺ `a² + 4a - 105 = 0`, roots `-2 ± √109` — not integers. The
Sessions 23–24 *answer* was right; the *reason* was wrong.

### What survives

The chain degrees `D = a+b = 3, 8, 13, 18, 23, 28` never depended on the broken
formula, so **every gate conclusion of Sessions 20–22 stands**. The GGHV
comparison survives with corrected numbers: `(15,10), (48,32), (99,66)` cleared
by GGHV; `(168,112), (255,170), …` beyond it and killed by the Belyi gate.

### New artifact — the smallest near-miss in the family

```
a = 2, b = 1, E = 1, N = 4, delta = 1, D = 3
p = w² + (3/2)w + 3/8 ,  r = w + 1 ,  p² - w r³ = w/8 + 9/64
v = x1·x2 - 1 ,  degrees (15,10) ,  Jacobian a single monomial
```

Never written down before, and the cheapest object on which to test any future
claim about this family.

---

# Session 26 — the general cusp template, and the first non-(2,3) near-miss

Run against the three remaining areas. **No counterexample.** One area produced
a genuine new object but did **not** settle the question it was aimed at; the
other two are open research problems, not computations.

### The template generalises to every cusp

Session 7's shape is not special to `(2,3)`. For a cusp `y1^m = y2^n + W`:

```
m·A = n·B        (cusp relation on x1-degrees)
c = n·d          (so that y1^m/y2^n = p^m/(w r^n),  w = v^c/x2)
m·a - n·b = 1    (equivalently the Belyi degree N = m·a = n·b + 1)
```

`(2,3)` returns Session 7's `(A,B,c,d) = (3,2,3,1)`; `(5,2)` gives `(2,5,2,1)`.

### The first non-(2,3) near-miss

```
cusp (5,2),  p = w+1,  r = w² + (5/2)w + 15/8,  N = 5, a = 1, b = 2
v = x1·x2 - 1
y1 = x1²(v² + x2)
y2 = x1⁵ v (v⁴ + (5/2)v²x2 + (15/8)x2²)
degrees (6,15),   5·6 = 2·15 = 30
J = (15/8)·x1⁶·x2²          ← a single monomial
```

`E = 1` is the only value in 1..8 producing a monomial. **The campaign's first
near-miss outside the `(2,3)` cusp.**

### `W` carries the skeleton's own residue

For both near-misses, `W = y1^m - y2^n` is a monomial times the skeleton's
cancellation residue at `w = v^c/x2`, and the residue degree equals `δ`:

| cusp | `W` | residue |
|---|---|---|
| `(2,3)` | `x1⁶x2³[(1/8)v³ + (9/64)x2]` | `p² - wr³ = w/8 + 9/64` |
| `(5,2)` | `x1¹⁰x2³[(5/8)v⁴ + (95/64)v²x2 + x2²]` | `p⁵ - wr² = (5/8)w² + (95/64)w + 1` |

### What was NOT settled

`ν = μn` — the target. Two block models were built; **both fail on the one case
where the answer is known**:

| | `ν` at `(2,3)` |
|---|---|
| measured (Session 12) | **6** |
| model A (generic `T`) | 3 |
| model B (`T` coefficients `/g^μ`) | 4 |

Neither is faithful, so neither can decide other cusps. **`ν = μn` remains open,
and so do Session 23's 870 conditional tuples.** The block normal form needs the
Y-side geometry, never re-derived for a non-`(2,3)` cusp — and the `(5,2)`
near-miss does not supply it, because it lives in the `(x1,x2)` chart while the
block data lives after the resolution.

Recording a failed attempt rather than a third model tuned to give the wanted
answer.

### Caveat, stated before it becomes correction #8

Session 25's `E = a - b` law was established on `(2,3)` data only. The `(5,2)`
near-miss sits at `E = 1` while `a - b = -1`. **That law is `(2,3)`-specific.**

---

# Session 27 — the Y-side geometry, derived for a non-(2,3) cusp

The one piece of bounded work left after Session 26. **It is now done, and it
closes the window rather than opening one. No counterexample.**

### Why it was possible this time

Sessions 22–26 could not do this because the block normal form had only ever
been read off Borisov's instance, and no other instance existed. Session 26
built the first non-`(2,3)` near-miss. With an explicit map in hand the Y-side
data is not an abstraction to be modelled — it is read off directly:

```
v = x1·x2^E - 1 ,  U = v+1   ⟹   x1 = U / x2^E ,  v = U - 1
```

Substituting turns `y1`, `y2` into finite Laurent series in `x2` whose
coefficients are polynomials in `U`. **Those coefficients are the blocks.**

### Calibration — the method recovers Sessions 9–13

Applied to Borisov's own instance with no input from the later sessions:

| recovered | matches |
|---|---|
| `y2` leading block at `x2⁻⁶` → `β = 6` | Session 12's `y2 = q⁻⁶v⁻¹⁸g²(1+T)` |
| that block `= U²(U-1)¹⁶ = [U(U-1)⁸]²` | Session 13's `g = αU(U-1)⁸`, `deg g = 9` |
| `W` first surviving block at `x2⁻⁵`, `= const·U⁶(U-1)⁹` | Session 10's `W̃₋₅ = n₃U⁶(U-1)⁹` |

Three independent campaign results from one substitution. Validated before use.

### The result

| instance | `μ` | `ν` | `μn` | `deg g` | `N/μ+ε` |
|---|---|---|---|---|---|
| `(2,3)` a=2,b=1,E=1 | 2 | 6 | 6 | 3 | 3 |
| `(2,3)` a=5,b=3,E=2 | 2 | 6 | 6 | 6 | 6 |
| `(2,3)` a=8,b=5,E=3 **[Borisov]** | 2 | 6 | 6 | 9 | 9 |
| `(5,2)` a=1,b=2,E=1 **[new cusp]** | 5 | 10 | 10 | 2 | 2 |

> **`ν = μn` at every point, including the `(5,2)` cusp.**

Consequences:

1. **Session 23's 870 conditional tuples are refuted at `(5,2)`** — every one
   required `ν < μn`. The Session-22 closure is **unconditional** there.
2. **`μ = m` is now measured** at a second cusp type, not merely shown removable
   by Session 23's integrality argument.
3. **`deg g = N/μ + ε`** confirmed at all four instances.

### Scope

This settles `ν = μn` at *one* non-`(2,3)` cusp with one skeleton — not for every
`(m,n)`. Session 23's tuples ranged over many cusp types; only those at `(5,2)`
are closed. What changed is that the question is **no longer untestable**: build
the near-miss, substitute `x1 = U/x2^E`, read `ord_U`. A finite recipe, not an
open problem.

And the direction matters: the Y-side geometry, once actually computed,
**confirms the closure**.

---

# Session 28 — literature sweep: the conjecture fell above dimension 2

A full literature sweep turned up a development this repo had not recorded past
Session 1, and it changes the campaign's context.

### The Jacobian conjecture is FALSE in every dimension > 2

| | |
|---|---|
| Alpöge, 19 Jul 2026 | counterexample in dimension 3 |
| Gallagher, 20 Jul 2026 | an infinite family |
| Speyer, 23 Jul 2026 | the geometric explanation — a tangent sweep |
| [arXiv:2608.00222](https://arxiv.org/abs/2608.00222) | self-contained account; counterexamples in every dimension > 2, arbitrarily large geometric degree; five explicit maps (3-D deg 4; 4-D deg 5, 10; 5-D deg 6, 12) |

**The plane case remains open.** Stabilisation only moves upward in dimension; a
three-variable counterexample cannot be squeezed into two. This campaign targets
the plane case throughout, so everything in Sessions 19–27 stands — but Session 1
had already reverse-engineered the Alpöge map, and nothing after it recorded that
the general conjecture had fallen.

### New result — the tangent sweep has no plane analogue

The published accounts explain the mechanism and note it works only for `n > 2`,
but do not explain *why* it stops at the plane. Session 1's own data supplies the
signature: `F = v(x,y)z + w(x,y)` with `c₂ = det[v_x, v_y, v] = 0`, `c₁ = 0`,
`c₀ = -2`, and `v = x³u(t)` sweeping a **twisted cubic** — the degeneracy is met
by a *non-constant* direction field.

In the plane, `F = v(x)z + w(x)` with `v, w : C → C²`:

```
det JF = z·(v1'v2 - v2'v1) + (w1'v2 - w2'v1)
```

1. The degeneracy `v1'v2 - v2'v1 = 0` is the **Wronskian**; for `v2 ≠ 0`,
   `(v1/v2)' = 0`, so `v = a(x)·e` — a **constant direction**.
2. Then `det[w',v] = a(x)·(w1'e2 - w2'e1) = c ≠ 0`: a product of two polynomials
   equal to a nonzero constant, so both are constants.
3. So `h := e2w1 - e1w2` has `h' = c/α ≠ 0`, hence degree exactly 1, and
   `e2F1 - e1F2 = h(x)`. `x` is recovered linearly, then `z`. **`F` is an
   automorphism.**

> **The dimension count.** The mechanism needs a direction field that is
> degenerate but *not* of constant direction. For `v : C → C²`, degeneracy
> `det[v',v] = 0` ⟺ rank ≤ 1 ⟺ constant direction — the conditions **coincide**
> and the map trivialises. For `v : C² → C³`, `det[v_x,v_y,v] = 0` still admits
> non-constant solutions (the developables, e.g. the twisted cubic). They
> **separate** from dimension 3 onward. That is why the tangent sweep starts at
> `n = 3`.

Consistency check: this is the linear-in-one-variable case, which Sessions 2–5
covered independently (`min deg_y ≤ 2 ⟹ tame`). The two arguments agree.

### Route closed by the same sweep

The Mathieu–Zhao hierarchy (Special Image ⟹ Generalized Vanishing ⟹ Jacobian) is
not a path to a plane counterexample: those conjectures **imply** the JC, so their
falsity in dimension 5 ([arXiv:2608.07338](https://arxiv.org/html/2608.07338))
removes them as *proof strategies* and says nothing about the plane.

**A plane counterexample, if one exists, must work by something other than a
tangent sweep.**

---

# Session 29 — the sweep mechanism, closed in the plane at every order

Session 28 killed the tangent sweep's linear form in the plane. This closes its
natural generalisations. **No plane counterexample.**

### The literal plane tangent sweep isn't even Keller

In the plane, Speyer's construction is literally a map `C² → C²`:

```
Φ(t,s) = C(t) + s·C'(t)      det JΦ = s · det[C''(t), C'(t)]
```

The explicit factor of `s` makes it vanish on `{s = 0}` — the curve itself. A
nonzero constant is impossible. **It fails before any degree, genus or duality
argument is reached.**

### At every order, the leading direction is forced constant

Sweeping osculating curves instead of tangent lines, `Φ = Σ_{i=0}^{k} sⁱ·C_i(t)`:

```
det JΦ = Σ_{i,j} j·s^(i+j-1)·det[C_i', C_j]
top coefficient, at s^(2k-1):  k · Wronskian(C_k)
```

Verified symbolically for `k = 1..5`. A constant Jacobian forces that Wronskian
to vanish, so `C_k = a(t)·e` — a **constant direction**.

> The mechanism's defining feature — a field that is degenerate but **not** of
> constant direction — is unavailable in the plane **at every order**, not merely
> at `k = 1`. That is what makes the `n ≥ 3` construction genuinely
> higher-dimensional.

### The descent, and closure for `k ≤ 3`

With `e = (0,1)`, `C_k` hits only the second component, so
`min(deg_s Φ₁, deg_s Φ₂) ≤ k-1`. Against Sessions 2–5 (`min deg_y ≤ 2 ⟹ tame`):

| order | min `deg_s` | verdict |
|---|---|---|
| `k = 1` tangent/affine | 1 | **tame** |
| `k = 2` osculating conic | 1 | **tame** |
| `k = 3` osculating cubic | 2 | **tame** |
| `k ≥ 4` | `k-1 ≥ 3` | not reached by that theorem |

**Honest limit:** for `k ≥ 4` tameness is not proved by this argument. What *is*
proved at every `k` is the constant-direction collapse — the mechanism is dead at
all orders; the stronger tameness conclusion holds for `k ≤ 3`.

### Every route the campaign opened is now closed

| route | status |
|---|---|
| cusp-chain framework family | dead at every chain degree, cusp type, depth, boundary order (S19–22, 27) |
| the tangent sweep | no plane analogue at any order (S28–29) |
| Mathieu–Zhao hierarchy | implies the JC — its failure is not a route (S28) |
| one place at infinity | automorphism, Abhyankar–Moh (S24) |
| direct search above degree 108 | infeasible by four orders of magnitude (S23) |

A plane counterexample, if one exists, works by a mechanism that is none of
these, at a degree no search can reach, on a skeleton nobody has proposed.

---

# Session 30 — rigor audit of Session 29, and the second cascade step

Session 29's closure was challenged on two points — both about the *kind* of
claim, not the logic. Fair challenge: this campaign has twice been bitten by
fitting a relation to a few points. **Both claims are proved, not
pattern-matched**, and the distinction from the earlier mistakes is concrete.

### Audit 1 — the top coefficient is proved, not fitted

By bilinearity, `det JΦ = Σ_{i,j} j·s^(i+j-1)·det[C_i', C_j]`. Maximise `i+j-1`
subject to `i, j ≤ k`:

> `i + j - 1 = 2k - 1` ⟺ `i + j = 2k` ⟺ **`i = j = k`, uniquely.**

One pair reaches that exponent, so no cancellation is possible and
`coeff(s^(2k-1)) = k·W(C_k)` **exactly, for all `k`**.

**Difference from the earlier mistakes:** Session 25's degree law was a formula
fitted to three points with no derivation — it agreed at `a = 8` by coincidence
and failed elsewhere. Here the formula comes *first*, from bilinearity plus a
one-line integer argument; the per-`k` runs only confirm the expansion identity.
A fit can be wrong off its range; *"`i+j = 2k` with `i,j ≤ k` forces `i = j = k`"*
cannot. Session 29 presented this as five checks — that was a presentation error.

### Audit 2 — the dimension claim is derived, both directions

For `v : C^(n-1) → C^n` the degeneracy is `det[v_{x1},…,v_{x(n-1)}, v] = 0`.

**`n = 2`** — two ingredients, each specific to dimension 2:
(a) the determinant involves exactly **two** vectors, so degeneracy *is*
pointwise proportionality `v' ∥ v`; (b) the base is **one-dimensional**, so that
proportionality is an ODE and integrates: `(p/q)' = W/q²`, giving
`C = q(t)·(λ,1)`. Converse `W(a(t)e) = 0` holds identically.

**`n ≥ 3`** — the determinant involves `n ≥ 3` vectors; "dependent" is rank
`≤ n-1` out of `n`, strictly weaker. Non-vacuous **by witness**: Session 1's
twisted-cubic field has `det[v_x,v_y,v] = 0` while `rank[v, v_x] = 2`.

So they coincide in the plane and separate from dimension three on — both
directions established, not observed.

### New — the second cascade step, general in `k`

With `C_k = a(t)·e`, `e = (0,1)`, only `(k,k-1)` and `(k-1,k)` reach `s^(2k-2)`,
so with `C_{k-1} = (p,q)`:

```
coeff(s^(2k-2)) = k·a·p' - (k-1)·a'·p        ⟹   k·a·p' = (k-1)·a'·p
```

**Dichotomy at each level:**

| branch | consequence |
|---|---|
| `p = 0` | `C_{k-1}` also points along `e` → `min deg_s ≤ k-2` — a **second descent** |
| `p ≠ 0` | `p^k = c·a^(k-1)`; `gcd(k,k-1) = 1` forces `k \| m` at every root, so **`a = αh^k`, `p = βh^(k-1)`** for a common `h` |

The top two sweep coefficients must be high powers of *one* polynomial — a rigid
structure that tightens as `k` grows.

**Still open:** this does *not* close `k ≥ 4`. The `h`-family is a strong
constraint, not a contradiction. Stated as a dichotomy because that is what was
proved.

---

# Session 31 — third cascade step, a divisibility ladder, and `k = 4`

Pushing Session 30's live end: the `h`-branch at `k ≥ 4`.

### Self-correction, caught before it propagated

My first attempt reduced the cascade expression mod `h` via `subs(h, 0)`. That
zeroes `h'` too — it is *not* reduction mod `h`, it returned 0 for every `k`, and
I then **asserted** "the reduction is a nonzero multiple of `h'q`" rather than
computing it. Redone as genuine polynomial arithmetic below. Logged because the
same class of slip produced corrections 5–7.

### Third cascade step — exact, general in `k`

Only `(k,k-2)`, `(k-1,k-1)`, `(k-2,k)` reach `s^(2k-3)`, so with `C_k = (0,a)`,
`C_{k-1} = (p,q)`, `C_{k-2} = (u,w)`:

```
coeff(s^(2k-3)) = k·a·u' - (k-2)·a'·u + (k-1)·W(C_{k-1})
```

Verified exactly for `k = 3..6`; the pair-enumeration checked to `k = 59`.

### A divisibility ladder

Feeding in `a = αh^k`, `p = βh^{k-1}` and dividing by `h^{k-2}`, every term
carries an explicit `h` **except one**. With `h = t`, the surviving value at
`t = 0` is **computed**, not guessed:

| `k` | value at `t=0` | ⟹ |
|---|---|---|
| 4 | `9·β·q(0)` | `t \| q` |
| 5 | `16·β·q(0)` | `t \| q` |
| 6 | `25·β·q(0)` | `t \| q` |

i.e. `(k-1)²·β·q(0)`. Substituting `q = t·q̃` and dividing again yields a further
condition — **a divisibility ladder**, structurally the same shape the campaign
met on the framework side in Sessions 11–12.

### The `k = 4` branch, decided at bounded degree

Session 30's dichotomy leaves one live branch at `k = 4`: `C_4 = (0, αh⁴)`,
`C_3 = (βh³, q_3)`. With `h = t` and everything else free, inverting
`(Jacobian constant)·α·β` so that `GB = {1}` means *no solution*:

| free coefficient degree | conditions | unknowns | result |
|---|---|---|---|
| `≤ 1` | 17 | 16 | **GB = {1}, no solution** |
| `≤ 2` | 26 | 23 | **GB = {1}, no solution** |

### Scope — honestly labelled

**Gained:** the third cascade step for all `k`; the divisibility ladder;
emptiness of the order-4 sweep over `h = t` at coefficient degree `≤ 2`.

**Not gained:** the `k ≥ 4` branch in general. The `k = 4` result fixes `h = t`
and bounds the degree; larger `h` and `k ≥ 5` are untouched. A bounded-degree
Gröbner run is **evidence, not a theorem** — this campaign has already published
one "verified at every point tested" that was a fit in disguise.

---

# Session 32 — the `h`-branch: census, root-drop, and where it actually sits

Asked to close the `h`-branch at `k ≥ 4`. **It is not closed** — but this session
identifies *why*, which is more useful than another partial.

### Bounded-degree census — empty everywhere computed

| case | conditions | unknowns | result |
|---|---|---|---|
| `k=4, h=t`, deg ≤ 1 | 17 | 16 | **empty** |
| `k=4, h=t`, deg ≤ 2 | 26 | 23 | **empty** |
| `k=4, h=t²` (non-squarefree) | 21 | 16 | **empty** |
| `k=4, h=t(t-1)` (squarefree quadratic) | 34 | 16 | **empty** |
| `k=5, h=t`, deg ≤ 1 | 24 | 20 | **empty** |
| `k=5, h=t`, deg ≤ 2 | 39 | 29 | **empty** |
| `k=6, h=t`, deg ≤ 1 | 31 | 24 | **empty** |

Seven cases, three orders, three shapes of `h` including a non-squarefree one.

**Where the census stops, and why.** Coefficient degree 3 at `k = 4` was attempted
twice and returned no verdict either time — over ℚ it exceeded a 3000 s budget,
over `F_32003` it exceeded ~560 s. The boundary at degree 2 is **computational,
not a choice**: sympy's Gröbner engine does not reach degree 3 on this system.
Recorded so the attempt is not silently repeated. The mod-`p` run did reproduce
degree ≤ 2 as empty in 37 s — independent corroboration in different arithmetic.

### A root-drop of two

At a root `r` of squarefree `h`: `a(r) = a'(r) = 0`, `p(r) = p'(r) = 0`, and
`q_{k-1}(r) = 0` by the Session-31 ladder. So **both** components lose two
`s`-degrees at once:

```
deg_s Φ₁(r,·) ≤ k-2 ,   deg_s Φ₂(r,·) ≤ k-2
```

Verified at `k = 4, 5` (both attain the bound). Every root of `h` is a point
where the sweep degenerates by two orders — which is why the census keeps coming
back empty.

### Where it actually sits — the real obstruction

Session 30's descent gives `min deg_s ≤ k-1`; Sessions 2–5 close `min deg_y ≤ 2`.
So the first uncovered order is `k = 4`, sitting at `min deg_s = 3` **exactly**.

Sessions 3 and 6 of this repo call the `deg_y = 3` slice *"the first slice the
collapse machinery does not decide."* Therefore:

> **closing the `h`-branch at `k = 4` ≡ deciding the `deg_y = 3` slice**

That is not a gap in this session's reasoning — it is the campaign's own
unresolved frontier, reached from the opposite direction. Sessions 3–6 walked
into it from the y-degree side; the sweep cascade walks into the same wall from
the sweep side. **Two independent routes terminating at the same slice says the
slice is the genuine content**, not an artefact of either approach.

### Status

| | |
|---|---|
| **closed by proof** | the mechanism's defining feature, at every order `k` |
| **closed by proof** | orders `k ≤ 3` entirely; first two cascade steps for all `k`; the divisibility ladder |
| **not closed** | the `h`-branch at `k ≥ 4` = the `deg_y = 3` slice — empty everywhere computed, not proved empty |

## Files

| file | contents |
|---|---|
| `singular/endgame_moduli.sing` | moduli scheme, components, reducedness, Zariski tangent space at the near-miss, obstruction-map table over `(D, J)` |
| `singular/rank_jumps.sing` | rank-jump census over `(D, J)`, resonance identification, closed form of the unlocking direction |
| `singular/monomial_twins.sing` | `[P,Q] = x^r` Newton-skeleton obstruction, admissible chain degrees, twin variety dimensions |
| `singular/skeleton_generator.sing` | generalised endgame `T_{k,s,D}`, skeleton generator over cusp type and cancellation depth, the Belyi gate |
| `certify/session19_deformation_probe.py` | exact sympy certification of Session 19 (19 checks), house style |
| `certify/session20_d4_reverse_engineering.py` | exact sympy certification of Session 20 (17 checks), including the explicit `D = 4` and `D = 3` skeletons |
| `singular/d3_instantiation.sing` | the `(5,2)` geometry at `D = 3` written out completely, the pole-fiber test, the direct solver |
| `certify/session21_d3_window.py` | exact sympy certification of Session 21 (18 checks) — findings 2 and 4c superseded by Session 22 |
| `singular/contact_exponent.sing` | the derived contact exponent, every cusp type re-run at its own degree |
| `certify/session22_contact_exponent.py` | exact sympy certification of Session 22 (19 checks), including the first-principles re-derivation of Session 18's master identity |
| `certify/session23_three_fronts.py` | exact sympy certification of Session 23 (8 checks): the audit, the bypass spec, the GGHV relocation |
| `certify/session24_family_survey.py` | exact sympy certification of Session 24 (6 checks) — its mod-4 ranking reason is void, see Session 25 |
| `certify/session25_template_exponent.py` | exact sympy certification of Session 25 (13 checks): `E = a-b` (2,3-only), the quadratic degree law, the smallest near-miss |
| `certify/session26_general_cusp_template.py` | exact sympy certification of Session 26 (12 checks): the general cusp template, the first non-`(2,3)` near-miss, and the failed `ν = μn` attempt |
| `certify/session27_yside_nonstandard_cusp.py` | exact sympy certification of Session 27 (8 checks): the Y-side chart, calibration against Sessions 9–13, and `ν = μn` at the `(5,2)` cusp |
| `certify/session28_tangent_sweep_no_plane_analogue.py` | exact sympy certification of Session 28 (13 checks): the literature update and the proof that the tangent sweep has no plane analogue |
| `certify/session29_sweep_closed_all_orders.py` | exact sympy certification of Session 29 (9 checks): the sweep closed in the plane at every order |
| `certify/session30_sweep_rigor_and_cascade.py` | exact sympy certification of Session 30 (10 checks): the rigor audit and the second cascade step |
| `certify/session31_cascade_step3_and_k4.py` | exact sympy certification of Session 31 (5 checks): third cascade step, divisibility ladder, `k = 4` at bounded degree |
| `certify/session32_hbranch_census_and_placement.py` | exact sympy certification of Session 32 (3 checks): the `h`-branch census, the root-drop, and the reduction to the `deg_y = 3` slice |

## Running

```
apt-get install -y singular          # Singular 4.3.2 is enough
Singular -q singular/endgame_moduli.sing
Singular -q singular/rank_jumps.sing
Singular -q singular/monomial_twins.sing
python3 certify/session19_deformation_probe.py
```

`monomial_twins.sing` skips the `D = 13` Groebner computation by default
(~10 min); set `RUN_D13 = 1` to recompute it. Its recorded answer is in the
script.

Three Singular gotchas hit while writing these, all silently wrong rather than
loudly wrong:

- `continue` inside a `for` loop **skips the increment** and spins forever
  (verified: a 5-iteration loop with one `continue` runs unbounded). The probes
  use `if`/`else` only.
- `res` is a reserved identifier — naming a resultant `res` fails with a type
  error.
- `elim.lib`'s `sat()` returns an incorrect saturation for these ideals in
Singular 4.3.2 — checked against iterated `quotient` on
`I = <x z^5, x + y z^5>`, where `sat` returns `<y>` instead of `<x,y>`. Both
Singular probes saturate by iterated `quotient` instead.

## Cross-validation

The probe re-derives the cross-epoch identity `h0 = -D * n3` with `D = 13`,
tying the Session-7 Wronskian constant to the Session-10 cubic and confirming
that the chain degree this probe sweeps is the same integer the earlier
sessions computed with. All 19 certifications pass.

## Honest scope

- Everything here is conditional on the campaign's own formalisation of the
  framework (layers 1–3, realization, rigidity), exactly as Sessions 8–18 were.
  The probe tests that formalisation's stability under deformation; it does not
  re-derive the formalisation.
- The `D = 1 (mod 6)` admissibility argument is specific to the `(2,3)`-cusp
  fork profile certified in Session 7. The Second Framework and the isotope
  series have different profiles, so the `D = 4` test must be redone there
  before the trapdoor can be declared shut for them. Finding 1 (universal
  polynomial obstruction) already covers them; only the trapdoor analysis does
  not.
- Nothing here bears on the plane Jacobian conjecture itself. It bears on the
  published constructive framework family.

## Next

0. **Done (Session 22): the `D ≤ 3` window is closed.** The contact exponent was
   derived rather than assumed and cannot fall below 4. No gate remains open.
1. Re-referee the pole-fiber theorem (Session 13/14, Theorem 3) — it is now
   the single load-bearing hypothesis, and finding 2 says exactly how much
   slack would be needed to break it (one unit of pole order at `U = 0`).
2. Redo the `D = 4` admissibility test for the Second Framework's profile and
   for the isotope series.
3. The `(5D+13)/6 = D` rigidity count generalises: run it on the other
   published profiles to predict their forced chain degrees before building
   their decision systems.
