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
