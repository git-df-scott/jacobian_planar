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

**4. Why 13 (a by-product).** Rigidity of the skeleton's Belyi datum needs
`#unknowns - #equations = 1`, i.e. `(5D+13)/6 = D`, i.e. `D = 13` exactly.
Confirmed by direct Groebner computation: the non-degenerate solution variety
has parameter dimension 1 (the scaling orbit alone) at `D = 13`, dimension 2
at `D = 7`, dimension 3 at `D = 1`, and `D >= 19` is over-determined.
Borisov's chain degree is forced, not found.

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

## Files

| file | contents |
|---|---|
| `singular/endgame_moduli.sing` | moduli scheme, components, reducedness, Zariski tangent space at the near-miss, obstruction-map table over `(D, J)` |
| `singular/rank_jumps.sing` | rank-jump census over `(D, J)`, resonance identification, closed form of the unlocking direction |
| `singular/monomial_twins.sing` | `[P,Q] = x^r` Newton-skeleton obstruction, admissible chain degrees, twin variety dimensions |
| `certify/session19_deformation_probe.py` | exact sympy certification of all of the above (19 checks), house style |

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

Note: `elim.lib`'s `sat()` returns an incorrect saturation for these ideals in
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

1. Re-referee the pole-fiber theorem (Session 13/14, Theorem 3) — it is now
   the single load-bearing hypothesis, and finding 2 says exactly how much
   slack would be needed to break it (one unit of pole order at `U = 0`).
2. Redo the `D = 4` admissibility test for the Second Framework's profile and
   for the isotope series.
3. The `(5D+13)/6 = D` rigidity count generalises: run it on the other
   published profiles to predict their forced chain degrees before building
   their decision systems.
