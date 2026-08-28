# night12 -- MATE SEARCH v2: results

Measurements only. Nothing in this file is a conclusion. **ring: Q** = exact
rational arithmetic; **ring: F_p** = the scheduling prime, which decides
nothing. Machinery: `v2_families.py` (targets and their derived
certificates), `v2.py` (carriers, stages, driver), `controls_v2.py`,
`exact.py` and `sy.py` from v1, both frozen.

The v1 results are in `V1_RESULTS.md`; this file is the v2 addendum, run
against the certified non-coordinate targets that night14 made available.

## 1. Hit gate

The gate: a mate `Q` certified over `Q` by expanding `[P,Q] - 1`
coefficientwise, on a `P` certified NON_COORDINATE. On a hit the run halts
and writes `night12/HIT_<hash>/`.

| quantity | value |
| --- | --- |
| ARM A objects (deg P 124-132) | 12 |
| ARM B objects (night14 crux + the brief's `x + x^2*y`) | 6 |
| total objects | 18 |
| stage evaluations | 78 |
| mates certified over Q | 0 |
| **hit-gate status** | **NOT TRIPPED -- 0 hits; the run did not halt** |

Every object in both arms is certified NON_COORDINATE, and every one
reached an exact emptiness verdict on every support tried. No mate was
found anywhere in v2, so the gate had nothing to fire on.

## 2. Controls

The v1 controls stand: `controls_v1.py`, **PASS**, 15 checks, 0 failed.

The V2 brief adds one: on a COORDINATE `P` of shape similar to the ARM A
targets, the solver must FIND its mate. `controls_v2.py`, **PASS**, 2 checks,
0 failed.

| control | ok | detail |
| --- | --- | --- |
| V2-POS-1  P = x + y^2 | ok | deg Q = 1, bracket ok = True |
| V2-POS-2  P = y + tau(x), deg tau = 124 (ARM A shape, g = 0) | ok | deg Q = 1, bracket ok = True |

`V2-POS-2` is the one that carries weight. It is the degenerate `g = 0`
member of the very family ARM A searches -- same `v = y + tau(x)`, quadratic
term switched off, which makes it a shear and therefore a coordinate -- at
`deg P = 124`, run through the ARM A stage list, the ARM A carriers and the
ARM A solver path with no special-casing. Its mate is found at the first
stage and verified coefficientwise over `Q`. So an EMPTY in ARM A is not the
machinery being unable to find a mate at that degree and shape.

## 3. ARM A targets and their derived certificates

Construction (night14 `PROSPECTOR.md` section 2, reparametrised to clear
denominators):

```
v = y + tau(x),  tau in Z[x], deg tau = T >= 1
g = c*(x - a)^n,  c, a, h0 in Z,  c, h0 != 0,  n >= 1
P = h0*v + g*v^2 + kappa            deg P = n + 2*max(1, T)
```

Two certificates per object, both expanded coefficientwise over `Q`.
Neither needs a Groebner basis, which matters because S1 times out on every
`P` at these degrees (see `V1_RESULTS.md` section 3).

**U -- unimodular gradient.** From `v_y = 1`, `v_x = tau'`:

```
P_y = h0 + 2*g*v
P_x = v_x*P_y + g'*v^2,        g' = c*n*(x-a)^(n-1)
```

and `2*(x-a)*g' = 2*n*g`, so `2*(x-a)*(g'*v^2) = n*v*(P_y - h0)`. Substituting
`g'*v^2 = P_x - v_x*P_y` and eliminating `v` via `h0 = P_y - 2*g*v` gives

```
1 = A*P_x + B*P_y,   A = 4*g*(x-a) / (n*h0^2)
                     B = ( h0 - (2*g/n)*(n*v + 2*(x-a)*v_x) ) / h0^2
```

with `A, B` in `Q[x,y]`. This is a Bezout certificate that `1` is in
`(P_x, P_y)`: the gradient is unimodular, so the critical locus is empty and
every fibre is smooth.

**R -- non-coordinate.** `P - kappa = v*(h0 + g*v)` identically, both factors
nonconstant, so the `kappa`-fibre is reducible. With U every fibre is smooth,
so a reducible fibre is a disconnected one, while a coordinate has every
fibre isomorphic to the affine line and in particular connected.

| tag | deg P | n | T | \|supp P\| | U verified | R verified | R factor degs | SY | places at inf | genus_newton |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F2  T=1 a=0 | 124 | 122 | 1 | 5 | True | True | [1, 123] | NON_COORDINATE | 2 | 122 |
| F2  T=2 a=0 | 124 | 120 | 2 | 9 | True | True | [2, 122] | NON_COORDINATE | 1 | 121 |
| F2  T=61 a=0 | 124 | 2 | 61 | 9 | True | True | [61, 63] | NON_COORDINATE | 1 | 62 |
| F2  T=3 a=1 | 126 | 120 | 3 | 371 | True | True | [3, 123] | NON_COORDINATE | 1 | 122 |
| F2  T=5 a=0 | 126 | 116 | 5 | 9 | True | True | [5, 121] | NON_COORDINATE | 1 | 120 |
| F2  T=1 a=1 | 128 | 126 | 1 | 384 | True | True | [1, 127] | NON_COORDINATE | 2 | 126 |
| F2b T=2 a=2 | 128 | 124 | 2 | 381 | True | True | [2, 126] | NON_COORDINATE | 1 | 125 |
| F2b T=3 a=0 | 130 | 124 | 3 | 14 | True | True | [3, 127] | NON_COORDINATE | 1 | 126 |
| F2b T=5 a=-1 | 130 | 120 | 5 | 378 | True | True | [5, 125] | NON_COORDINATE | 1 | 124 |
| F2b T=61 a=1 | 130 | 8 | 61 | 60 | True | True | [61, 69] | NON_COORDINATE | 1 | 68 |
| F2  T=1 a=-1 | 132 | 130 | 1 | 396 | True | True | [1, 131] | NON_COORDINATE | 2 | 130 |
| F2b T=2 a=0 | 132 | 128 | 2 | 13 | True | True | [2, 130] | NON_COORDINATE | 1 | 129 |

U verified **12/12**; R verified **12/12**; SY NON_COORDINATE **12/12**; genus_newton > 0 **12/12**.

## 4. ARM A verdicts

Stages per object: `deg Q <= deg P - 1`, `deg P + 31`, `deg P + 63` on the
Newton-polygon-similar carrier, then a **wide** stage at `deg Q <= deg P + 63`
on the full degree triangle thinned to 2500. The bound `deg P + 63` is the
one the brief sets. Cell format `VERDICT[cert]`; `lam` = exact lambda
certificate, `rank` = full-column-rank certificate, `sol` = exact solution.

The two carriers are **complementary, not nested**. The similar carrier is a
dense sample of one sub-polygon of the degree triangle; the wide carrier is a
stride-`t` sample spread over the whole triangle (before thinning it contains
the similar one, after thinning it does not). An EMPTY on each is a separate
statement, and neither is a claim about every `Q` of that degree.

| tag | deg P | dQ<=P-1 | dQ<=P+31 | dQ<=P+63 | wide dQ<=P+63 | wide n_raw -> n_used (thin) | outcome |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F2  T=1 a=0 | 124 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 17766 -> 2019 (t=3) | EMPTY_all_stages_tried |
| F2  T=2 a=0 | 124 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 17766 -> 2022 (t=3) | EMPTY_all_stages_tried |
| F2  T=61 a=0 | 124 | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | 17766 -> 2023 (t=3) | EMPTY_all_stages_tried |
| F2  T=3 a=1 | 126 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 18145 -> 2407 (t=3) | EMPTY_all_stages_tried |
| F2  T=5 a=0 | 126 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 18145 -> 2085 (t=3) | EMPTY_all_stages_tried |
| F2  T=1 a=1 | 128 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 18528 -> 2419 (t=3) | EMPTY_all_stages_tried |
| F2b T=2 a=2 | 128 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 18528 -> 2416 (t=3) | EMPTY_all_stages_tried |
| F2b T=3 a=0 | 130 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 18915 -> 2154 (t=3) | EMPTY_all_stages_tried |
| F2b T=5 a=-1 | 130 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 18915 -> 2477 (t=3) | EMPTY_all_stages_tried |
| F2b T=61 a=1 | 130 | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | 18915 -> 2193 (t=3) | EMPTY_all_stages_tried |
| F2  T=1 a=-1 | 132 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 19306 -> 1585 (t=4) | EMPTY_all_stages_tried |
| F2b T=2 a=0 | 132 | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | EMPTY[rank] | 19306 -> 2219 (t=3) | EMPTY_all_stages_tried |

Unknown counts on the similar carrier, per stage (min/median/max): 186 / 380 / 740.

Outcomes: {'EMPTY_all_stages_tried': 12}.
Certificates: {('EMPTY_over_Q', 'lambda_exact'): 14, ('EMPTY_over_Q', 'rank_full_column_exact'): 34}.

## 5. ARM B verdicts (low-degree, escalating)

Five structurally diverse objects from night14's 79 certified
U-PASS + SY-NON_COORDINATE records -- two positive-genus `F2b`, plus one each
of `F1b`, `F3`, `F4` -- together with `x + x^2*y`, which the brief names.
`deg Q` escalates 10, 30, 60, 100, 126.

**Only the last stage can decide anything.** The published degree bound means
a mate for an object of this size would need `deg Q >= 125`, so the stages at
`deg Q <= 10, 30, 60, 100` are calibration: their EMPTYs are honest but
support-relative and carry no weight against the bound. Every stage in this
file is recorded with `support_relative = true` and its full carrier
parameters; the `decisive` column marks the one stage per object that clears
the bound.

| tag | family | deg P | dQ<=10 | dQ<=30 | dQ<=60 | dQ<=100 | dQ<=126 (decisive) | n at dQ<=126 | outcome |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| night14 F1b c2005a8935aa | F1b | 9 | EMPTY[lam] | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | **EMPTY[rank]** | 917 | EMPTY_all_stages_tried |
| night14 F2b 63a7aba444df | F2b | 9 | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | **EMPTY[rank]** | 2331 | EMPTY_all_stages_tried |
| night14 F2b 3471c81e5940 | F2b | 9 | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | **EMPTY[rank]** | 2331 | EMPTY_all_stages_tried |
| night14 F3 a22d19d84467 | F3 | 6 | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | **EMPTY[rank]** | 2310 | EMPTY_all_stages_tried |
| night14 F4 948919f80bd3 | F4 | 10 | EMPTY[lam] | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | **EMPTY[rank]** | 807 | EMPTY_all_stages_tried |
| x + x^2*y | brief | 3 | EMPTY[lam] | EMPTY[lam] | EMPTY[rank] | EMPTY[rank] | **EMPTY[rank]** | 2709 | EMPTY_all_stages_tried |

Outcomes: {'EMPTY_all_stages_tried': 6}.
Certificates: {('EMPTY_over_Q', 'lambda_exact'): 14, ('EMPTY_over_Q', 'rank_full_column_exact'): 16}.

SY verdicts across ARM B: {'NON_COORDINATE': 6}.

## 6. Certificates emitted

| arm | (verdict, certificate) | count |
| --- | --- | --- |
| A | ('EMPTY_over_Q', 'rank_full_column_exact') | 34 |
| A | ('EMPTY_over_Q', 'lambda_exact') | 14 |
| B | ('EMPTY_over_Q', 'rank_full_column_exact') | 16 |
| B | ('EMPTY_over_Q', 'lambda_exact') | 14 |

`NOT_CERTIFIED` stage outcomes (never reported as emptiness): **0**.

Every `lambda_exact` record carries the lambda vector itself
(`lambda_vector`, entries `[[i,j],[num,den]]`) and a `lambda_reverified`
flag from an exact re-check at record time, so each certificate can be
verified from the record alone.

## 7. What these verdicts do and do not say

1. **The targets are certified, not assumed.** Every ARM A object has an
   explicit Bezout identity proving its gradient unimodular and an explicit
   factorisation proving a fibre reducible, both checked coefficientwise
   over `Q`, plus an independent SY verdict. ARM B's objects carry night14's
   U-test and FIB-screen certificates as well as SY.
2. **Every EMPTY is support-relative and is labelled so.** The verdict is
   about the linear system on the carrier actually built. It is exact over
   `Q` on that carrier -- no modular computation decides anything -- but it
   is not a statement about all `Q` of that degree unless the carrier is the
   full triangle, which only the ARM A wide stage approaches, and that one
   is thinned (thinning index recorded per stage).
3. **Emptiness is never claimed beyond the stage tried.** Each stage records
   its own carrier and its own certificate; no stage's verdict is extended
   to a higher degree bound.
4. **The solver is known to find mates at this degree and shape**, by
   control V2-POS-2, so the ARM A EMPTYs are not a null instrument.

