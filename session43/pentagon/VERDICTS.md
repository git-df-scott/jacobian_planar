# Six components of the pentagon, and what is actually established

## The verdicts

All computed with `msolve -g 2` in **characteristic 0**, so there is no
bad-prime caveat: a Gröbner basis of `[1]` means `1` is in the ideal, hence the
variety is empty over `C` by the Nullstellensatz.

| component | what it is | polys / vars | planted control | verdict |
|---|---|---|---|---|
| `sat`      | chart A pick 0, saturated at `g9_8` | 52 / 17 | 17 elts | **EMPTY** |
| `compA1`   | chart A pick 1, saturated at `g9_8` | 51 / 15 | 15 elts | **EMPTY** |
| `g98zero`  | chart B pick 0 (`g9_8 = 0`)         | 39 / 15 | 15 elts | **EMPTY** |
| `compB1`   | chart B pick 1                      | 61 / 18 | 18 elts | **EMPTY** |
| `compB2`   | chart B pick 2                      | 39 / 14 | 14 elts | **EMPTY** |
| `compC0`   | chart C, no assumptions, saturated  | 64 / 20 | 20 elts | **EMPTY** |

Chart C made **zero** multi-component decisions, so it is not one branch among
several — it is the whole `g9_8 != 0` region of its component.

## Controls, because `[1]` is exactly what a broken pipeline also prints

Erratum A16: msolve silently mis-parses parentheses and reports `[1]` — a FALSE
EMPTY — in zero seconds, exit 0, no warning. So every emitter here asserts its
output text contains no parenthesis, and every run is paired with a **planted
positive control**: replace each `f` by `f - f(p)` for a chosen point `p`, which
makes `p` a common solution, so the basis must *not* be `[1]`. Same emitter,
same variables, same file size. Every planted control returned a full-length
basis (14 to 20 elements), which is what proves msolve is genuinely parsing and
using all the polynomials at that size, and hence that the `[1]`s are real.

Plus the two standing controls: `x-1, x-2` -> `[1]`, and `x*y-1, x+y` -> a
2-element basis.

## Saturation, not the plain ideal

`g9_8 != 0` is an **open** condition, so the object is `I : g9_8^inf`, not `I`.
Testing `I` would be wrong — `I` has points with `g9_8 = 0` and those are not in
the chart. Done exactly, by dividing the explicit `g9_8` factors out and
adjoining `g9_8*t - 1`.

## What this DOES establish

On the repaired branch-1 witness (`h_8 = z^8`, `h_7 = 2z^8`, `h_6 = z^8`,
`g_12 = z^12`, `tau = 1`, gauges `h_{-1} = s`, `g_{-1} = s^2`), **with
`g8_6 = g8_7 = 0`**, the pentagon has NO solution. The two charts cover that
region with nothing excluded:

* `g9_8 != 0` — chart C, no assumptions, no branch choices: EMPTY
* `g9_8 = 0`  — chart B, all three branch components: EMPTY

## What this does NOT establish

**`g8_6 = g8_7 = 0` is still inherited, not proved here.** It came from the
level-8 pure-power gates `-8 g8_6^3` and `-4 g8_7^3`, which were computed in a
run that had already made its own branch choice at level 9. Discharging it
means running the descent with nothing pre-imposed (chart F), and that run is
**incomplete**: it dies at level 13 with a degenerate `zoo` value, because the
level-13 gate solution divides by `g9_11`, which an earlier substitution had
already set to zero.

That is the same failure as the `g9_8` case, and it is now a named rule:

> **A solve that divides by a parameter silently deletes that parameter's
> vanishing locus from the chart, and the deleted locus can be the one where
> the system is solvable.** Every solve needs its denominators inspected, not
> just its residual checked.

It was exactly this that made the `g9_8 = 0` chart invisible for so long — and
on that chart 47 of 51 conditions died at once. So the rule is not pedantic;
it is where the structure was hiding.

## Status

Pentagon: **NO VERDICT**. No explicit `(P,Q)`. Six components are EMPTY with
controls; the witness is not yet closed, because `g8_6 = g8_7 = 0` remains an
inherited assumption pending the chart-split repair of chart F.
