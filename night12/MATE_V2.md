# night12 -- MATE SEARCH v2: results

Measurements only. Nothing in this file is a conclusion. **ring: Q** = exact
rational arithmetic; **ring: F_p** = the scheduling prime, which decides
nothing. Machinery: `v2_families.py` (targets and their derived
certificates), `v2.py` (carriers, stages, driver), `controls_v2.py`,
`verify_certs_v2.py` (the independent re-verification of section 8),
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
targets, the solver must FIND its mate. `controls_v2.py`, **PASS**, 4 checks,
0 failed.

| control | ok | detail |
| --- | --- | --- |
| V2-POS-1  P = x + y^2 | ok | deg Q = 1, bracket ok = True |
| V2-POS-2  P = y + tau(x), deg tau = 124 (ARM A shape, g = 0) | ok | deg Q = 1, bracket ok = True |
| V2-POS-3  P = A + B^2, A = x + y^2, B = y + A^11 (coordinate, smallest mate degree 22) | ok | deg Q = 22, bracket ok = True |
| V2-POS-4  P = A + B^2, A = x + y^2, B = y + A^21 (coordinate, smallest mate degree 42) | ok | deg Q = 42, bracket ok = True |

The four cover two different ways an EMPTY could be an artefact.

`V2-POS-2` covers DEGREE. It is the degenerate `g = 0` member of the very
family ARM A searches -- same `v = y + tau(x)`, quadratic term switched off,
which makes it a shear and therefore a coordinate -- at `deg P = 124`, run
through the ARM A stage list, the ARM A carriers and the ARM A solver path
with no special-casing. Its mate is found at the first stage and verified
coefficientwise over `Q`.

`V2-POS-3` and `V2-POS-4` cover SYSTEM SIZE and MATE DEGREE, which a shear
does not exercise: a shear's mate has degree 1 and sits in the first few
columns. They are built by the elementary chain `A = x + y^2`,
`B = y + A^k`, `P = A + B^2`, every step of which preserves the bracket, so
`[P, B] = 1` identically and `P` is a coordinate of degree `4k` whose
SMALLEST mate has degree `2k`. At `k = 11` and `k = 21` the solver had to
find a dense mate of degree 22 and 42 inside carriers of 505 and 1805
unknowns and reconstruct it rationally -- the same work ARM A's EMPTY stages
do, on a system that is consistent -- and did, with `[P,Q] - 1 = 0` expanded
coefficientwise over `Q` in both cases.

So an EMPTY in ARM A is not the machinery being unable to find a mate at
that degree, at that system size, or of that mate degree.

## 3. Per-P summary

One row per object, both arms. **certificate id** is the record hash: the
object's certificates are in `night12/V2_RECORDS/<id>.json`, and stage `k`
of that record is cited as `<id>.s<k>`. **U** is the unimodularity check --
for ARM A the Bezout identity `A*P_x + B*P_y = 1` expanded coefficientwise
over `Q`, for ARM B night14's char-0 U-test carried on the source record.
**mate system** is the largest system actually solved for that object
(unknowns after kernel deflation x nonzero Keller rows), at the stage named
in the next column. The re-verification column is section 8's independent
pass, `verify_certs_v2.py`.

| certificate id | arm | tag | deg P | U | SY | mate system (n x rows) | at stage | stages | verdict | re-verified |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `88870e2c21d9` | A | F2  T=1 a=0 | 124 | True | NON_COORDINATE | 2019 x 9412 | wide_triangle dQ<=187 | 4 | EMPTY_all_stages_tried | ok |
| `7aabbefe44c8` | A | F2  T=2 a=0 | 124 | True | NON_COORDINATE | 2022 x 15292 | wide_triangle dQ<=187 | 4 | EMPTY_all_stages_tried | ok |
| `09d8d1d05e63` | A | F2  T=61 a=0 | 124 | True | NON_COORDINATE | 2023 x 9221 | wide_triangle dQ<=187 | 4 | EMPTY_all_stages_tried | ok |
| `dada805afbd2` | A | F2  T=3 a=1 | 126 | True | NON_COORDINATE | 2407 x 41445 | wide_triangle dQ<=189 | 4 | EMPTY_all_stages_tried | ok |
| `524d0cc3ffe5` | A | F2  T=5 a=0 | 126 | True | NON_COORDINATE | 2085 x 10466 | wide_triangle dQ<=189 | 4 | EMPTY_all_stages_tried | ok |
| `ee69918807f6` | A | F2  T=1 a=1 | 128 | True | NON_COORDINATE | 2419 x 42210 | wide_triangle dQ<=191 | 4 | EMPTY_all_stages_tried | ok |
| `e244401b343d` | A | F2b T=2 a=2 | 128 | True | NON_COORDINATE | 2416 x 42018 | wide_triangle dQ<=191 | 4 | EMPTY_all_stages_tried | ok |
| `de46dd421875` | A | F2b T=3 a=0 | 130 | True | NON_COORDINATE | 2154 x 18380 | wide_triangle dQ<=193 | 4 | EMPTY_all_stages_tried | ok |
| `257de46f270b` | A | F2b T=5 a=-1 | 130 | True | NON_COORDINATE | 2477 x 42773 | wide_triangle dQ<=193 | 4 | EMPTY_all_stages_tried | ok |
| `91c9043bde61` | A | F2b T=61 a=1 | 130 | True | NON_COORDINATE | 2193 x 30558 | wide_triangle dQ<=193 | 4 | EMPTY_all_stages_tried | ok |
| `a0ab3b429039` | A | F2  T=1 a=-1 | 132 | True | NON_COORDINATE | 1585 x 33306 | wide_triangle dQ<=195 | 4 | EMPTY_all_stages_tried | ok |
| `be43beb153b0` | A | F2b T=2 a=0 | 132 | True | NON_COORDINATE | 2219 x 21045 | wide_triangle dQ<=195 | 4 | EMPTY_all_stages_tried | ok |
| `f4500b943c3b` | B | x + x^2*y | 3 | PASS (re-verification, char 0) | NON_COORDINATE | 2709 x 2793 | np_similar dQ<=126 | 5 | EMPTY_all_stages_tried | ok |
| `333b92b5a748` | B | night14 F3 a22d19d84467 | 6 | PASS (night14) | NON_COORDINATE | 2310 x 2394 | np_similar dQ<=126 | 5 | EMPTY_all_stages_tried | ok |
| `999bad8fc503` | B | night14 F1b c2005a8935aa | 9 | PASS (night14) | NON_COORDINATE | 917 x 1030 | np_similar dQ<=126 | 5 | EMPTY_all_stages_tried | ok |
| `4b274ede86db` | B | night14 F2b 3471c81e5940 | 9 | PASS (night14) | NON_COORDINATE | 2331 x 2534 | np_similar dQ<=126 | 5 | EMPTY_all_stages_tried | ok |
| `94079802c5b0` | B | night14 F2b 63a7aba444df | 9 | PASS (night14) | NON_COORDINATE | 2331 x 2534 | np_similar dQ<=126 | 5 | EMPTY_all_stages_tried | ok |
| `8bb5667fb3c6` | B | night14 F4 948919f80bd3 | 10 | PASS (night14) | NON_COORDINATE | 807 x 910 | np_similar dQ<=126 | 5 | EMPTY_all_stages_tried | ok |

Verdict tally over objects: {'EMPTY_all_stages_tried': 18}.
Verdict tally over stage evaluations: {'EMPTY_over_Q': 78}.

## 4. ARM A targets and their derived certificates

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

## 5. ARM A verdicts

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

## 6. ARM B verdicts (low-degree, escalating)

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

## 7. Certificates emitted

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

## 8. Independent re-verification

`verify_certs_v2.py` re-checks every v2 certificate without calling
`exact.decide` or `v2_families`. Carriers and Keller systems are rebuilt
from the recorded carrier parameters; the ARM A factor `v` is RECOVERED
from `P` itself by exact division `v = (P_y - h0)/(2*g)` and the Bezout
pair rebuilt from it, so the identity is re-derived rather than replayed;
`rank_full_column_exact` stages are re-run at a different scheduling
prime (`1000003`) and a different compression seed (`20260901`) than the run used,
and ARM B objects are re-tested with night14's Singular U-test in
characteristic 0.

| check | outcome | count |
| --- | --- | --- |
| A R_factorisation | True | 12 |
| A SY | True | 12 |
| A U_bezout | True | 12 |
| A lambda_exact | True | 14 |
| A rank_full_column_exact | True | 34 |
| B SY | True | 6 |
| B lambda_exact | True | 14 |
| B night14_U_test_char0 | PASS | 6 |
| B rank_full_column_exact | True | 16 |

All 78 stage certificates were re-checked, 48 object-level checks with
them. `v1`'s pass had to record `rank_full_column_exact` as
`not_recheckable`, because it re-ran nothing modular; here each such
stage is re-run at a second prime, so every v2 certificate without
exception has been re-derived.

**FAILURES: 0.**

## 9. What these verdicts do and do not say

1. **The targets are certified, not assumed.** Every ARM A object has an
   explicit Bezout identity proving its gradient unimodular and an explicit
   factorisation proving a fibre reducible, both checked coefficientwise
   over `Q`, plus an independent SY verdict. ARM B's objects carry night14's
   U-test and FIB-screen certificates as well as SY. Section 8 re-derives
   all of it a second time, independently of the run's own code path.
2. **Every EMPTY is support-relative and is labelled so.** The verdict is
   about the linear system on the carrier actually built. It is exact over
   `Q` on that carrier -- no modular computation decides anything -- but it
   is not a statement about all `Q` of that degree unless the carrier is the
   full triangle, which only the ARM A wide stage approaches, and that one
   is thinned (thinning index recorded per stage).
3. **Emptiness is never claimed beyond the stage tried.** Each stage records
   its own carrier and its own certificate; no stage's verdict is extended
   to a higher degree bound.
4. **The solver is known to find mates at this degree, at this system
   size and at a mate degree far above 1**, by controls V2-POS-2, V2-POS-3
   and V2-POS-4, so the ARM A EMPTYs are not a null instrument.
5. **Nothing here rests on a single code path.** Section 8 re-checks all
   78 stage certificates and 48 object-level certificates from the records
   alone, rebuilding carriers and Keller systems, re-deriving the Bezout
   identity from `P` itself, and re-running the rank certificates at a
   second prime; 0 failed.

