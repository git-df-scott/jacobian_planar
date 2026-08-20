# T1 — DISCREPANCIES between GGHV's degree-pair list and my mechanical rerun

Certifier: `gghv_audit/w5_gghv_certifier.py` (19/19 checks, log in `controls.log`).
Implementation: `gghv_audit/ggv_algorithms.py`, written only from the pseudocode
and definitions of arXiv:1708.07936v1 (papers/1708.07936.pdf).
Reference tables transcribed in `gghv_audit/ggv_reference_tables.py`.

## 0. What the rerun covers

GGHV (arXiv:2204.14178) does not enumerate degree pairs. Its Theorem 2.1 starts
from a ten-row table imported from [5] = arXiv:1708.07936 §§5–6. The mechanical
object to re-derive is therefore [5]'s Algorithms 1–9, and that is what was
re-implemented and run.

Result of the rerun over the full range: **34 cases with max(deg P, deg Q) ≤ 150
(one orientation), matching [5] §6 row for row, and 10 rows with max ≤ 124,
matching GGHV's §2 table row for row.**

The degree pairs the rerun produces with `105 ≤ max ≤ 124` are exactly

| deg pair | A0 | chain | final corner | (m,n) | GGHV node | class |
|---|---|---|---|---|---|---|
| (108,72) | (8,28) | — | (11⁄4, 7) | (3,2) | **left open by GGHV itself** | OPEN-IN-SOURCE |
| (72,108) | (9,27) | (9,24) | (11⁄3, 8) | (2,3) | GGHV §5 | NOT-RE-DERIVED-HERE |
| (80,112) | (4,12) | — | (7⁄4, 3) | (5,7) | "[4, §3.5]" | EXTERNAL-NOT-RE-DERIVED |
| (120,80) | (8,32) | (8,28) | (11⁄4, 7) | (3,2) | GGHV §3 | RE-DERIVED-KEY-STEP |

Counting ordered pairs, `gghv_audit/w5_pairs_105_124.py` (4/4 checks) decides all
**4560** ordered (deg P, deg Q) with 105 ≤ max ≤ 124 — the data are forced, since
g = gcd(deg P, deg Q) = v11(A₀), m = deg P/g, n = deg Q/g — and exactly **six**
arise: the two orientations of each of (72,108), (80,112), (80,120). The rest are
eliminated by the enumeration itself: 214 because the gcd forces m = 1 or n = 1,
4316 because no admissible complete chain has that v11(A₀), and 24 because chains
with that v11(A₀) exist but none carries that (m,n). **Zero pairs come back
NOT-ELIMINATED-BY-MY-RERUN.**

**No pair in 105 ≤ max ≤ 124 is produced by my rerun that GGHV does not list, and
none that GGHV lists is missed.** In that sense there is no discrepancy in the
enumeration. The discrepancies below are of two other kinds: places where my
rerun's *output* differs from the paper's printed tables (D1–D3), and places
where a kill is *not re-derived* (D4–D6).

---

## D1 — two length-1 admissible complete chains at M=35 that [5] §5 does not list

My rerun at v11(A0) ≤ 35 gives **16** distinct length-1 admissible complete chains;
[5] §5 reports 14. The two extras are

    A0=(8,24), A'0=(2,0), final corner (14⁄4, 6)
    A0=(9,24), A'0=(1,0), final corner (9⁄3, 6)

Exact divergence step: both survive Definition 2.19 (complete) and Definition 2.25
(admissible, vacuous for j=0) as written, but both have **I(A) = ∅** in
Definition 3.3 — for (14⁄4,6): the only admissible k is 1, bl−a = 10, ek = 1, and
gcd(b, (bl−a)/ek) = gcd(6,10) = 2 ≠ 1; for (9⁄3,6): gcd(6,9) = 3 ≠ 1. So neither
generates an (m,n)-family and neither contributes a degree pair.

Reading: [5]'s Algorithm 8 as printed produces them; [5]'s table evidently lists
only chains that survive Algorithm 9. **No effect on any degree pair.**

## D2 — four length-2 chains at M=35 that [5] §5 does not list

My rerun gives 11 distinct length-2 chains (keyed on (A0,A'0,A1,A'1,A2)); [5]
lists 7 (F18–F24), all 7 of which I reproduce exactly. The four extras are

    A0=(6,18), A'0=(6,0),  A1=(6,15), A'1=(1,0), A2=(7⁄3,4)
    A0=(6,18), A'0=(6,0),  A1=(6,15), A'1=(1,0), A2=(8⁄3,5)
    A0=(6,24), A'0=(6,0),  A1=(6,15), A'1=(1,0), A2=(7⁄3,4)
    A0=(6,24), A'0=(6,0),  A1=(6,15), A'1=(1,0), A2=(8⁄3,5)

Exact divergence step: Algorithm 2 line 7 accepts A' = (6,0) because
v_{1,−1}(6,0) = 6 > 0 and (6,0) ∈ PLLC; Algorithm 3's non-simple branch then
generates A1 = (6,15) from it, exactly as it does from A' = (6,15) via the
v_{1,−1}(A') < 0 branch. Both routes reach the same A1, the same A2 and the same
MN(A2). **No effect on any degree pair** — confirmed by the exact 34/34 match at
max ≤ 150.

## D3 — [5] §5's sentence "2 admissible complete chains of length 2" versus its
own table of seven length-2 families

[5] §5 states "14 admissible complete chains of length 1 and 2 admissible complete
chains of length 2", then prints a table of **seven** length-2 families F18–F24
built on seven distinct length-2 chains. My rerun finds all seven. The "2" in the
sentence is not reproducible and is not consistent with the paper's own table.
Recorded, no error claim.

## D4 — the (80,112) kill is not re-derivable from any source available here

GGHV's §2 table discards A0=(4,12), (m,n)=(5,7), max=112 — degree pair (80,112),
which is **inside** the 105 ≤ max ≤ 124 window — by citing only
"[4, section 3.5]" = *A Differential Equation for Polynomials related to the
Jacobian Conjecture*, Pro Mathematica 27 (2013), which is not on arXiv and is not
in `papers/`. GGHV gives no argument of its own for this row.

Class: **EXTERNAL-NOT-RE-DERIVED**. This is the only 105 ≤ max ≤ 124 kill that
rests entirely on a source this audit cannot open.

## D5 — the (72,108)-from-(9,27) and 84 and 99 kills are not re-derived here

GGHV §5's polynomial-system kills of max = 99 and of max = 108 from A0=(9,27),
and GGHV §3's kill of max = 84 (which uses [6, Theorem 7.3], Pro Mathematica 30
(2019), also unavailable), were not re-run. They are recorded as nodes in
`case_tree.json` with `reproduced_here: NO`.

Class: **NOT-RE-DERIVED-HERE** (not a discrepancy — a scope statement).

## D6 — sensitivity findings about [5]'s Algorithm 1

* Removing the ϑ-divisibility filter (Algorithm 1 line 16) enlarges PLLC from
  1266 to 1526 corners at xmax = 60 and re-admits **(6,3)** and **(8,4)** — the
  two corners whose exclusion is exactly what kills families F18–F21 and the
  max = 120 case. The filter is load-bearing for those kills.
* Removing the `v_{ρ,σ}(a,b) ≥ ρ` filter changes PLLC by **zero** corners at
  xmax = 60: within this range it is implied by the other conditions. Recorded as
  a redundancy in the printed algorithm, not as an error.
* Neither removal changes the max ≤ 150 case count (still 34), and neither does
  re-inserting (6,3) into PLLC by hand. The 34-case list is robust to those two
  filters at this bound; it is **not** robust to Definition 2.25 (dropping it
  gives 117 cases) nor to deleting the corner (1,0) (gives 10 cases).

---

## Positive controls reproduced (all in `controls.log`)

P1 (2,1) ∉ PLLC · P2 (6,3) ∉ PLLC · P3 (8,4) ∉ PLLC · P4 no admissible chain with
v11(A0) ≤ 15 · P5 the 14 published length-1 chains · P6 F18–F24 · P7 the 13
family-derived §6 cases · P8 the 9 further length-1 cases · P9 the 11 further
length-2 cases · P10 the length-3 case · P11 exactly 34 cases · P12 GGHV's
ten-row table.

## Negative controls (each required to break something)

N1 ϑ-filter removal re-admits (6,3),(8,4) so P2/P3 fail on that variant ·
N2b corrupting Proposition 3.2's Diophantine drops the count 34 → 0 ·
N2c deleting (1,0) from PLLC destroys 12 of the 14 published families, 34 → 10 ·
N3 dropping Definition 2.25 gives 721 chains / 117 cases instead of 260 / 34 ·
N4 a mutated reference row is not matched.
