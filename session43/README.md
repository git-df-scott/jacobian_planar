# Session 43

**No counterexample.** What follows is what was established, what was withdrawn,
and what is left. Read `AUDIT.md` before quoting any number: an earlier pass of
this session reported results that were wrong, and the corrections are material.

## The one-line summary

The July 2026 dimension-3 counterexample makes a new reduction available —
slice it back down to a surface — and that reduction is correct but, for
Alpöge's map, **subsumed by a 1986 theorem of Orevkov**. Along the way the tear
of that map turned out to be rational and completely stratifiable, which yielded
an exact Euler identity and a sharp structural constraint on the tear of *any*
planar counterexample.

## Results that survive audit

**1. The slice reduction.** For any `Sigma ≅ C^2` in the target of a
counterexample `F`, `S := F^{-1}(Sigma)` is smooth, `F|_S` is étale, and since
`F` is 3:1 *everywhere* it is non-injective for every `Sigma` — the collision
value is not a constraint. So `S ≅ C^2` for any such `Sigma` ⟹ **JC2 false**
(Keller is automatic: the Jacobian is a nowhere-zero regular function on `C^2`).

**2. The tear of Alpöge's map is rational.** `Delta` is quadratic in `w1` with a
**perfect-cube** discriminant `−4(3w2w3−4)^3`, so `mu^2 := 4−3w2w3` rationalizes:

```
w1 = (mu+1)(mu-2)^2/27r^2,  w2 = -(mu-2)(mu+2)/3r,  w3 = r
inverse:  r = w3,  mu = E/(4-3w2w3),   E = 27w1w3^2 - 9w2w3 + 8
```

`E` is the same invariant that appears in `disc_x` of the fibre cubic. This gives
the exact stratification `tear = (C*)^2 ⊔ C* ⊔ A^1`, with `C_sing = {mu=0}`.
Fibre sizes come out **{3, 1, 0}** — which is Gao (arXiv:2608.00222) Theorem 3.4,
derived here from scratch, so the machinery independently reproduces a published
theorem.

**3. An exact Euler identity.** For any dominant `F : C^2 -> C^2` with finite
fibres, geometric degree `d`, tear stratified with fibre `n_i` on `A_i`:

```
sum_i (d - n_i) chi(A_i) = d - 1
```

This **implies** the campaign's `chi(F^{-1}(S_F)) ≡ 1 (mod d)` and pins the value
rather than the residue.

**4. A constraint on the tear of any counterexample.** If the tear is
irreducible with constant fibre count `m`, then `(d-m)chi(A) = d-1`; since
`chi <= 1` for any irreducible affine curve, this forces `chi(A) = 1` **and
`m = 1`**. With Chau/Abhyankar–Moh (no tear component is `A^1`) and Abhyankar–Moh
(smooth + rational + one place at infinity ⟹ `A^1`), the tear must be
**singular** — a cuspidal rational curve with one place at infinity. Independent
of `d`: holds at 6 (smallest open degree), at 16 (Borisov's value at (108,72)),
everywhere.

**4b. A finite catalogue of admissible tears.** (E) constrains the whole
configuration at once, so it enumerates: at `d = 6` there are **83** admissible
configurations (up to 2 components, 1 deeper point, `chi >= -2`), each a concrete
Path C target. Enumerating also **corrected one of my own claims**: I had read
(E) as "the tear always contains a `chi = 1` component". False — the required
positive contribution can come from an isolated *deeper point*, which is a
stratum of `chi = 1` without being a component (7 of the 83 are of that kind).
The correct statement is about **strata**, not components. `tear_theorem.py` is
unaffected: it hypothesizes constant fibre count, i.e. no deeper strata.

**5. The pentagon bottom-edge seeds.** The never-run characteristic-zero RUR,
factored over ℚ: eliminant degree 9 splits **[1, 1, 2, 5]**. Checking *all* RUR
blocks (not a guessed index): no block vanishes on the quintic; `c8` and `d12`
vanish exactly on the 1+1+2 part. So **4 degenerate seeds + 5 admissible ones in
one Galois orbit, group S₅** — testing one admissible seed decides all five. This
resolves the retraction on `claude/opus-5-counterexample-plan-sep6yk` and matches
that branch's independent prime statistics.

**6. A validated linear reducer** (`msreduce.py`), with the coefficient guardrail
the campaign's first attempt lacked (products of residues must be reduced mod p
or msolve silently misreads them). Cross-validated: on the campaign's own
`seed0_p1000003.ms` it returns **123 vars / 241 equations**, exactly their
published endpoint, from code sharing none of theirs.

## Negative results, with their real strength stated

- **Plane slices: 7992 scanned, 0 survivors.** After the audit: 90 reach
  `chi(S)=1` (not 19), and all die — 18 by 1-dimensional centre, 72 by `H_1`.
  Dropping the unverified Chau citation entirely still gives 0. But see below:
  Orevkov subsumes this anyway.
- **Lane U** (the `(x,u)` normalization from Mondello's char-2 counterexample):
  the shape `P = x + x^2 Psi` is *forced*, and `Psi = c·u` is closed **exactly**.
  The 135-shape search finding 0 is **weak evidence** and the file says so: no
  member with `Psi_u != 0` is even an automorphism, so the search cannot be
  validated by recovering a planted solution.

## The correction that matters most

**Orevkov (1986): a planar Keller map of geometric degree 3 is an automorphism.**
Alpöge's map has geometric degree 3, so every slice has degree 3 or 1 and cannot
be a counterexample — whatever the Euler characteristic says. The scan is a
rediscovery, not a theorem. Confirmed floor: degrees **2,3,4,5 all excluded**
(Campbell 1973; Orevkov 1986; Domrina–Orevkov 1998 + Domrina 2000; Żołądek 2008),
**6 is open**. The lane lives only above the floor — hence `pathS_deg9.py`, which
slices `F∘F` (det J = 4, geometric degree **9**).

## Literature check that protects the campaign

A worry that Żołądek's "gcd ≤ 16 ⟹ automorphism" had closed the entire **B = 16**
program: **it has not.** GGV accept Heitmann's `B ≥ 16` and re-prove it, but
identify a **gap in Żołądek's Lemma 4.10**, on which his `B > 16` claim rests; no
erratum exists, and GGHV 2022 / Ramírez–Valqui 2025 still treat `B = 16` as live,
discarding `B=16` rows case-by-case rather than by citation. Corollary: any
`B = 16` counterexample has `max(deg) ≥ 125`, so (48,64) and (80,112) are dead.

## Compute ledger — failures, not verdicts

| system | result |
|---|---|
| corrected B=16 `d=8` (23 var / 30 eq, mostly **degree 4**) | OOM 13.9 GB, 14:32, 0 bytes |
| pentagon seed-extension (241 eq / 123 unk), first *uncapped* run | OOM 13.75 GB, 53:48, 0 bytes |
| `p11zero_full_sat` (186/306, hash-verified, never run before) | OOM 13.2 GB, 13:02, 0 bytes |

All three are **NO VERDICT**. Three independent frontier systems exceed this
box; the blocker is memory, not mathematics. The `d=8` system admits **no**
linear reduction (0 rounds), so it is genuinely hard rather than unreduced.

## Files

`chi_exact.py` (25/25 calibrations) · `pathS_tear_parametrized.py` (8/8) ·
`laneU_xu.py` (15/15) · `euler_identity.py` (4/4) · `tear_theorem.py` (16/16) ·
`msreduce.py` (3/3 + replication) · `pathS_scan2.py` · `pathS_graphs2.py` ·
`pathS_deg9.py` · `charp_ladder.py` · `AUDIT.md`.

`pathS_chi.py`, `pathS_scan.py`, `pathS_euler_filter.py`, `pathS_graphs.py` are
marked **WITHDRAWN** in place — kept only so the corrected numbers can be diffed
against the wrong ones.

## Standing rules added

1. Never report a validation suite as evidence unless its output has been read.
2. Calibrate every instrument on inputs of independently known value *before*
   aiming it at the problem, including at least one the instrument must get
   wrong if the suspected bug is present.
3. State the strength of a negative result: a search with no possible positive
   control does not exclude anything.

---

# Addendum — the C\* lane, and where it leaves the search

Everything below was added after the audit and is independent of it.

## 7. The C\*-descent theorem: session 39's Path A is closed

Session 39 proposed descending a dimension-3 counterexample along its C\*-action
and hoping the quotient is a planar counterexample. The census was queued but
never run, because nobody had the higher-degree maps in one place. Run here
(`descent_theorem.py`, **41/41**) on all seven known counterexamples — three
independent constructions, geometric degrees 3, 4, 6, 7, 12 — it closes.

**The exponent.** For source weights `(-1,m,n)` the invariant ring is free on
`x^m y, x^n z` (the `x`-exponent is forced), so those are the *only* weights
whose quotient is a plane at all. The 2×2 minors of that quotient's Jacobian
have gcd `x^k` with

```
k = max(m + n - 1, 0)
```

verified on the whole 5×5 grid.

**The forced square.** Every one of the seven maps is C\*-equivariant with
weights `(-1,1,2)`, and every one has

```
det JG = c · (F_p/x)^2        c a nonzero constant
```

a constant times a **perfect square**. This is structural, not coincidence: the
weight-`(-1)` component is forced to be `x·alpha`, and the descent's second
coordinate `v∘F = F_p^2 F_r` carries `alpha^2` out front. So the descent is
never Keller, and JC2 is untouched.

**The only escape is not one.** `k = 0` forces weights `(-1,0,0)` or `(-1,1,0)`,
and both are JC2 *verbatim* rather than a reduction of it:

- `(-1,0,0)`: `F = (ax, B(y,z), C(y,z))`, `det JF = a·{B,C}` — the trivial
  suspension of a plane map.
- `(-1,1,0)`: `F = (x A(u,z), y B(u,z), C(u,z))` with `u = xy`, and
  `det JF = {u·A·B, C}` in the `(u,z)` plane, **exactly**. Injectivity transfers
  both ways; the file exhibits an explicit collision being lifted, and an
  explicit automorphism being lifted with its inverse verified. If JC2 holds,
  Abhyankar–Moh collapses the family to `F = (ax, by, λz + μ(xy))`.

So a C\*-equivariant Keller map on `C^3` either descends to a non-Keller plane
map, or its descent *is* a planar counterexample. **C\*-descent cannot
manufacture one.**

Also recorded there: the units of `C[t,s]` are `C^*`, so a moving-line sweep
`Psi = gamma(t) + h(t,s)delta(t)` has `det = h_s·([g',d] + h[d',d])` with both
factors forced constant, hence `[delta',delta] = 0` and `Psi` triangular. **No
sweep of a moving line is ever a planar counterexample** — which is why the
tangent-sweep construction has no naive planar analogue.

## 8. Two obstructions turn out to be one, and it has one escape

The census found more than the square it was looking for: `alpha = F_p/x` is
**affine-linear** in the invariants in all seven maps.

```
alpoge d3  -3u-v+2      gallagher d3  -(3u-2v-2)/2     constructed d6  -3u-v+2
gao G d4   -4u-v+2      gallagher d6  -(19u-14v-14)/14 constructed d7  -9u-v+2
                        gallagher d12 -(87u-65v-65)/65
```

`alpha` linear means `F_p = a x^2 y + b x^3 z + c x` — exactly the "monomial
twist" shape that `pathS_highdegree.py` independently found blocking Path S (the
`z`-coefficient is the pure monomial `b x^3`, so the slice's centre `B(0,y)` is
constant and every slice is `C*×C`, never `C^2`). The Path S obstruction and the
descent obstruction are **the same fact**, and it has exactly one escape: a
counterexample with `deg alpha >= 2`.

`equivariant_ansatz.py` sets that up. For weights `(-1,1,2)` the weight-`w`
pieces of `C[x,y,z]` are free `C[u,v]`-modules on

```
weight -1 :  x          F_p = x·alpha
weight +1 :  y, xz      F_q = y·beta + xz·epsilon
weight +2 :  y^2, z     F_r = y^2·delta + z·gamma
```

so `det JF` is itself a polynomial `Psi(u,v)` and **Keller becomes a PDE in the
plane** for five unknown functions of two variables. `Psi` is derived
symbolically and checked against all seven maps. Its shape is the useful part:

> `Psi` is **trilinear** — linear in `alpha` (and its partials) and *bilinear* in
> `(beta, epsilon) × (gamma, delta)`.

So fixing `alpha` and `(beta, epsilon)` leaves a **linear** system for
`(gamma, delta)`: the collision-first linearity trick appears here for free, and
the `deg alpha >= 2` question is a finite exact search rather than a Gröbner
problem. Measured degrees: `alpha` stays at 1 in every map while
`beta, gamma, delta` reach 20, 21, 20 and `epsilon` reaches 9.

One guess of mine was wrong and is recorded as a measurement, not quietly
dropped: I expected `epsilon = 0` (the `xz` generator looked decorative). It is
**nonzero in all seven**, and its degree grows with the map.

## 9. Lane 7 — the never-run exact `F_p` collision-first sweep

**Verdict: no candidate.** ~176k exact `F_p` systems at `p = 1000003`,
cross-checked at `1000033`; **23/23 controls**, including a positive end-to-end
control (the Artin–Schreier pair over `F_3` is *found* by the full pipeline) and
a negative control proving the constant-row guard can fail if removed. Code in
`lane7/`, report in `lane7/lane7_report.md`. What it established:

1. **The rank profile is a delta function.** All 57,000 random dense `P` gave
   *identical* corank; `ker X_P` on the `Q`-triangle is exactly `span{1,P}`, so
   the stated gauge accounts for the entire generic nullity. There is no generic
   rank variation to exploit.
2. **Rank drops are an anti-signal**: nullity > 2 ⟺ `P` composite ⟺ provably
   inconsistent, since `[f(P₀),Q] = f'(P₀)[P₀,Q]`. 700 cases, no exceptions.
3. **The collision defect `delta(P) := Q(1,0) − Q(0,0)` is an invariant of `P`**,
   independent of the mate. So consistency ⟺ `[P,Q]=1` solvable **and**
   `delta(P) = 0`. This splits the search, and is what killed everything.
4. The coordinate stratum is closed **in closed form at (4,6)** too.
5. The `(4,6)` obstruction ideal is **not** the unit ideal — the surviving locus
   is codimension 3 in a 5-dimensional space, which is precisely why blind
   sweeps see nothing. A 120-trial random walk reporting "100% failure" was a
   **false negative**.

Its own stated gap: the level-2 death is randomized (20 sampled points of that
variety), not proved.

## Compute ledger, continued

| system | result |
|---|---|
| Singular `slimgb`, corrected B=16 `d=8` | **timeout 50:00**, 793 MB, no verdict |

Memory was never the blocker for Singular (793 MB against msolve's 13.9 GB) —
time was. Recorded as a failure, not a verdict.

## Where this leaves the search

The live chain is now explicit and short:

> find a C\*-equivariant dimension-3 counterexample with `deg alpha >= 2`
> → its `z`-linear component has a non-monomial `z`-coefficient
> → Path S slicing is no longer blocked at the first step.

`Psi`'s trilinearity makes step one an exact linear-algebra sweep rather than an
elimination problem. That is the next computation.
