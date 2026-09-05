# The constructive route, made concrete — a working recipe, an explicit
# solution, and a proof of why it cannot reach the pentagon

Fable, 2026-08-23. Code: `fable_xcol/sweepcheck.py` (verified).
Motivated by `FABLE_STATE_OF_THE_ART.md`: the July 2026 counterexamples in
dimension ≥ 3 were built by a *construction* (tangent sweep of a plane curve),
while this campaign owns only elimination machinery. This is the first
construction attempted here.

## The general quadratic sweep in the plane

Sweep a parametrised plane curve `K(w)` in a direction field, with a
second-order term along a fixed vector `v`:

    T(g, w) = K(w) + g·mu(w)·K'(w) + g^2·rho(w)·v          (g = x, w = y)

Demanding `det J(T) = g^2` — which *is* our target `{P,Q} = x^2` — and
collecting powers of `g` gives, after eliminating (hand-derived, verified):

    V := det[K', K'']        E := det[v, K']        E' = det[v, K'']

    rho = - mu^2 V / (2E)                        (from the g^1 coefficient)

    **mu^3  =  2E / (V'E - 3 V E')**              (from the g^2 coefficient)

So a quadratic sweep solving `{P,Q} = x^2` exists **iff `2E/(V'E - 3VE')` is a
perfect cube** (and `rho` comes out polynomial). Note the weights: the
combination `V'E - 3VE'` pairs a first derivative against a third multiple —
the same 2:3 resonance that runs through the whole pentagon.

## A worked, verified solution

Take `K(w) = (w, w^3)`, `v = (0,1)`. Then `V = 6w`, `E = -1`, and

    mu^3 = 1/3   (constant, so mu is constant),   rho = 3 mu^2 w   (polynomial)

giving

    T1 = w + mu·g
    T2 = w^3 + 3 mu g w^2 + 3 mu^2 g^2 w

and `det J = 3 mu^3 g^2 = g^2` exactly. In `(x,y)` notation, and recognising the
binomial:

    **P = y + mu·x ,   Q = P^3 - x^3/3 ,   with mu^3 = 1/3**

Independent check (`sweepcheck.py`): `{P,Q} = x^2`, verified symbolically. The
one-line reason it works: `{P, P^3 - x^3/3} = -{P, x^3/3} = P_y x^2 = x^2`
because `P_y = 1`.

## Why the sweep cannot reach the pentagon — and it is not a small gap

A sweep of degree `k` in `g` produces `P` of x-degree at most `k`. The
quadratic sweep gives `deg_x P <= 2`; the worked example gives exactly 1. The
pentagon needs

    deg_x P = 8 ,  deg_x Q = 12 .

So **no linear or quadratic tangent sweep can carry the pentagon's Newton
polygon.** What such sweeps produce is precisely the degenerate stratum the
campaign already knows: `P` of low x-degree, all three `P`-vertices
(`p_8_0, p_14_8, p_16_8`) zero — families A/B/C.

This is a negative result, but a clarifying one. It says the constructive
mechanism that settled `n >= 3` does not transfer cheaply to the plane, and it
identifies exactly the obstruction: **degree in the swept parameter.** To reach
the pentagon you would need a degree-8 sweep — at which point the ansatz has as
many unknowns as the pentagon system itself, so it is not a shortcut.

## What *is* worth taking from this

1. **A structured ansatz.** A degree-`k` sweep is a *jet along a curve*:
   `P, Q` truncated Taylor expansions in `g` with coefficients built from one
   curve `K(w)` and its derivatives. That is a much smaller, highly structured
   subfamily of the full pentagon system. If a pentagon point happens to have
   sweep structure it would be found very cheaply. Worth one search before
   assuming it does not.
2. **The cube condition generalises.** For a degree-`k` sweep the analogue of
   `mu^3 = 2E/(V'E - 3VE')` will be a `k+1`-st-power condition on a similar
   Wronskian combination. That is exactly the same shape as the campaign's
   proved edge relations (`b_12^2 = c a_8^3` on *both* edges — see
   `FABLE_XCOLUMN.md`), which is suggestive: the edge relations may be the
   sweep condition seen from the polygon side.
3. **It confirms the degenerate families are not accidents.** They are the image
   of the whole low-degree sweep construction, which explains why every
   numerical search collapses onto them (`FABLE_CASE_MAP.md`, Correction 2) —
   they form a positive-dimensional attractor of exactly this shape.

## Status

No counterexample. The explicit pair above is a genuine solution of
`{P,Q} = x^2` but is degenerate (P linear in x), so it is not a pentagon point
and carries no consequence for the Jacobian conjecture. Pentagon and sub-case
(2): **NO VERDICT**.
