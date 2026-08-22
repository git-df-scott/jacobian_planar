# A fast, validated oracle for the pentagon system

The exported system `wave1/pent_L23.ms` is 59 variables, 66 conditions,
**degree 22, 1,080,147 monomials, 43 MB**.  Every Groebner attack on it has
ended in OOM or timeout.

That size is an artefact of the representation.  The conditions come from a
straight-line recursion (`wave1/w1_h1b_sparsity.py`) in which every
intermediate level is substituted away:

    Q[0] = 1 ;  Q[1] = x^2                       (gauges p_0_0 = 0, p_0_1 = 1)
    Q[k+1] = (1/(k+1)) * sum_{a=1..k} [ a*P[a]*Q[b]' - (k+1-a)*P[a]'*Q[b] ],  b = k+1-a
    conditions:  Q[j][i] = 0  for j = 13..23, i = 0..j-13     (1+2+...+11 = 66)

At a NUMERIC point the same conditions cost milliseconds.  `pentev.py`
evaluates all 66 directly from the recursion.

## Controls (all passing)

| control | result |
|---|---|
| `control.py` — evaluator vs the exported degree-22 polynomials, 2 independent random points | **66/66 match, both points** |
| `affine.py` — second differences along random lines in the late block | **0 conditions with nonzero 2nd difference**, 3 points |
| `oracle.py` POS — planted right-hand side (Example 10) | **consistent, solution recovered and re-verified** |
| `oracle.py` NEG — right-hand side perturbed off the column space | **inconsistent**, rank 13/14 |

The evaluator is therefore a faithful, independently checked implementation of
the same system msolve was being given.

## What the oracle does

The 66 conditions are **exactly affine** in the 13 late parameters
(p_12_*, p_13_*, p_14_*, p_15_*, p_16_8) -- verified, not assumed.  So for any
early point e,

    conditions = M(e) . late + v(e),      M is 66 x 13

and the system has a solution over the late block **iff**
`rank(M) == rank([M | -v])`.  Cost: 14 recursion evaluations plus a 66x14 rank
over F_p -- milliseconds, fixed memory, no Groebner.

Generic early points give rank(M)=13, rank([M|-v])=14, i.e. inconsistent --
the same signature Example 9 records for trackB1.

## Measured degree profile (`degprof.py`)

Per-variable degree of the 66 conditions, by finite differences at a random point:

    degree 1 : 14 variables   p_11_6, p_12_4..7, p_13_5..7, p_14_6..8, p_15_7, p_15_8, p_16_8
    degree 2 : 20 variables   rows 7..11
    degree 3 : 10 variables   rows 6,7
    degree 4-5: 8 variables   rows 4,5
    degree 6-9: 7 variables   rows 1,2,3   (worst: p_1_1 at degree 9)

**14 variables enter affinely, not 13** -- `p_11_6` is affine too and was not
previously counted.  So 14 can be eliminated by linear algebra rather than 13.

## Dimension count this enables

With the 14 affine variables eliminated, `col(M)` has dimension <= 14 inside
F_p^C where C is the number of conditions used.  Requiring `v` to lie in it is
`C - 14` conditions on the 43 remaining parameters (after the two gauges):

| top level J | conditions C | conditions on 43 params | expected dim |
|---|---|---|---|
| 20 | 36 | 22 | 21 |
| 22 | 55 | 41 | 2 |
| **23** | **66** | **52** | **-9  (overdetermined)** |

So the exported system becomes overdetermined **exactly at the top level**, and
the decisive transition is J=22 -> J=23.  This is a heuristic count, not a
proof: the map e -> (M(e), v(e)) is far from generic.

## Status

This directory contains instruments, not verdicts.  No witness has been found
and no emptiness has been proved.  Verdict language: EMPTY / NONEMPTY /
NO VERDICT, with timeout, OOM, segfault and empty output all NO VERDICT.
