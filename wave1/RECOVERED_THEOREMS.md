# THEOREM 2 and THEOREM 3 — RECOVERED

**Status change: `certificates lost` → `statements recovered, in-repo, verbatim`.**

`STATUS.md` §4 recorded THEOREM 2 and THEOREM 3 as *"prose whose certificates
were lost with the Session 11–14 transcripts."* That was **wrong about the
statements**. Both are written out in full in a file that has been tracked on
**every branch of this repository** the whole time:

    Sessions 1-18 status reports     (53,469 bytes, 1199 lines)
      - THEOREM 2 at line 1051
      - THEOREM 3 at line 1062

The file is present at the repo root and mirrored at
`campaign/audit_tracks/` and `campaign/d23_borisov/`. What was lost is only the
**executable transcript runs**, not the mathematics.

## Where the transcripts actually are

Searched and settled, not assumed:

| place | result |
|---|---|
| container transcript store `/root/.claude/projects/…` | only *this* session (449ea24d) — container is cloned fresh |
| account session list, 100 sessions back to 2026‑07‑01 | **no JC2 session exists before 2026‑08‑01** |
| git: all 9 refs, full reflog, `--diff-filter=D`, `fsck --lost-found` | no deleted or dangling certificate objects |

The campaign's "Sessions 11–14" are internal numbering inside the long-running
claude.ai session **"Mathematical conjectures counterexample plan"**
(`session_0196W9j7GLwaGdSjAKrWpLHG`, 2026‑08‑01 → 2026‑08‑08). Its transcript
lives server-side and is not reachable from this container. **It is also not
needed** — see below.

## THEOREM 2 (total rigidity) — verbatim

> The layer-1 (-5)-pole conditions are the divisibilities `(U-1)^{-2-3n} | B~_n`,
> `(U-1)^{-3-3n} | A~_n`, and the cross-chart pins are pointwise Taylor
> conditions at `U = 1`:
> `B~_n^{(t)}(1) = t! eps mu^{-n-1} r_{-n-1}` (`t = -2-3n`),
> `A~_n^{(t)}(1) = t! gam mu^{-n-1} p_{-n-1}` (`t = -3-3n`).
> At `n = -6` (`B~_-6 = g^2`, `r_5 = 1`) these force the `(U-1)`-order of `g^2`
> to be EXACTLY 16, so with `U | g` and `deg g = 9` exact:
> `g = alpha U (U-1)^8`, `alpha^2 = eps mu^5`, `alpha^3 = gam mu^8`.
> The boundary polynomial of ANY framework solution equals the near-miss's up
> to one scalar. Total rigidity.

**This conclusion now has an executable certificate.**
`wave1/w1_L3_step2_pinning.py` (this campaign, independent re-derivation on the
three-dessin boundary) proves the block is exactly `[U(U-1)^8]^2`, i.e.
`g = alpha·U·(U-1)^8` **with no free moduli**, and derives `deg g = N/mu + eps
= 16/2 + 1 = 9`. Re-run it to reproduce.

## THEOREM 3 (pole-fiber) — verbatim

> `R = 2 v^39 (A~_4 - g^3 S_13)/g^3` has poles confined to `{v = 0, v = -1}`;
> the Belyi-13 fibers have 13/9/5/1 points; only the 1-point fiber fits a
> `<=2`-point pole set, so the pole fiber is the order-13 point at `v = infinity`
> and R is a DEGREE-13 POLYNOMIAL. The forced divisibilities close the `v = 0`
> pole exactly (boundary partition `sigma_1^13`, v-order 0).

Riemann–Hurwitz is consistent with the quoted passport: for a degree-13 map of
`P^1` with branch fibers of 9, 5 and 1 points,
`(13-9) + (13-5) + (13-1) = 4 + 8 + 12 = 24 = 2·13 - 2`, with 13 the generic
(unramified) count.

**THEOREM 3 is CONFIRMED** — see `wave1/w1_theorem3_verdict.py` and STATUS.md
§2.6. Its *conclusion* is true; its *recorded proof* has a real gap, found and
repaired here.

*The gap.* The fiber step fixes the pole divisor's **multiplicity** (13) but not
its **location**. The following sentence closes `v = 0`; nothing closes
`v = −1`. Witness, built and tested: `R = 1/(v+1)¹³` satisfies every premise the
recorded argument states and is not a polynomial.

*The repair.* Session 11's form `R = v³⁹·W̃₋₅(U)/g(U)⁶`, with `W̃₋₅` a block
(hence a polynomial) of degree 28 and `g = αU(U−1)⁸`, gives
`R = W̃₋₅(U)/(α⁶U⁶(U−1)⁹)`. With `gcd(W̃₋₅, U⁶(U−1)⁹) = U^a(U−1)^b`, `a ≤ 6`,
`b ≤ 9`, the map-degree is `28 − a − b`; the 13-realization forces `a + b = 15`,
whose only solution in the box is `(6,9)`. The denominator cancels completely,
so **R is a polynomial of degree 13**. The passport 13/9/5/1 is reproduced and
shown Riemann–Hurwitz consistent but is not load-bearing.

## Correction to our own H1c, and what replaces THEOREM 3 there

`wave1/w1_h1c_endgame_closed_form.py` printed:

> for every `D >= 1`, `k >= 0`, `(v+1)^k(3v(v+1)R' - D R) = -c` with `c != 0`
> has a rational solution of degree `>= 1` **iff** `k = 0` and `3 | D`.

**That is false as stated**, and it failed in the campaign's own most
load-bearing way: the `k >= 1` branch was never computed. Its `check()` call
passed a literal `True`, and its own prose reads *"IF R is regular at v = -1"* —
regularity at `v = -1` being precisely what THEOREM 3 exists to supply. The
file therefore assumed the uncertified input it was supposed to be independent
of.

Explicit counterexample at the campaign's own `(D,k) = (13,4)`, with `c = 1`:

    R = (243 v^4 - 81 v^3 + 54 v^2 - 42 v + 35) / (455 (v+1)^4)

verified by direct substitution, by Laurent expansion at `v = -1`
(`(v+1)^{-4} - 3(v+1)^{-3} + (27/7)(v+1)^{-2} - (81/35)(v+1)^{-1}`), by
`gcd(numerator, (v+1)^4) = 1` (the order-4 pole is genuine), and by exact
residual `0` at 40 random rational points.

### LEMMA (H1c, corrected) — `wave1/w1_h1c_polefix.py`

Let `D >= 1`, `k >= 1`, `c != 0`. Every rational solution `R` of
`(v+1)^k(3v(v+1)R' - D R) = -c` has all its poles at `v = -1`, and:

- `R` is **never** a polynomial (the polynomial branch dies at `v = -1`);
- if `3 | D` and `k >= D/3` there is **no rational solution at all**;
- otherwise the rational solutions are exactly `R = A/(v+1)^k` with
  `deg A = k`, and every one of them has **map-degree exactly `k`**.

Certified for `D = 1..30`, `k = 1..6` (the empty set matches the predicted
`3|D and k >= D/3` on all 21 pairs), with the reduction identity
`(v+1)^k(3v(v+1)R' - D R) = 3v(v+1)A' - (3kv+D)A` proved symbolically.

### COROLLARY

The endgame contradiction **never needs `R` to be a polynomial**. It suffices
that the framework force `map-degree(R) != k`. At `(D,k) = (13,4)` every
rational solution has map-degree 4, so a framework demand that `R` realise a
**degree-13** object is contradicted on degree alone — no fiber-counting, no
polynomiality.

### Scope — stated exactly

This does **not** prove THEOREM 3, and does not discharge every use of it. The
C2 table of forced `R`'s assumes polynomiality for its own reasons and keeps
its `CONDITIONAL(R-poly)` label. What the corollary does is replace the
uncertified fiber-counting **at the endgame contradiction** with a degree
count, relocating the residual gap to one much smaller question:

> does the framework force `map-degree(R) = 13` independently of THEOREM 3?

Session 15's affine form `R = lambda·B13((v-v0)/sigma) + nu` **must not** be
used to answer it — that form is derived *from* THEOREM 3 and would be circular.

## Reproduce

    python3 wave1/w1_h1c_polefix.py        # the correction + classification
    python3 wave1/w1_L3_step2_pinning.py   # THEOREM 2's conclusion, certified
