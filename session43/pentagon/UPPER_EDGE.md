# The upper edge: a perfect-square theorem, and a degree-pair filter

`EDGE_LADDER.md` worked the **lower** edge of `N(P)` (the slope-2 edge from
`(1,0)` to `(8,14)`), where the ladder closes only for `d = 12..19`.  The
**upper** edge `(0,8) -> (8,16)` behaves better and gives a sharper result.

## The rungs are uniform at every d, and algebraic

Supports: `a_i` has y-range `[2i-2, i+8]`, `q_k` has `[2k-3, 12+k]`.  Taking the
**top** y-degree, `deg(a_i q_k') = deg(a_i' q_k) = (i+8)+(12+k)-1 = d+20`, which
is uniform for **every** rung `d = 0..19`.  Writing `ahat_i = p_{i+8,i}` and
`qhat_k = q_{12+k,k}`, the derivative contributes only through the degree, so

    top-y coefficient of rung d  =  4 * sum_{i+k=d+1} (3i - 2k) ahat_i qhat_k .

The right-hand side `x^2` sits at `y^0`, never at `y^(d+20)`, so **every rung is
homogeneous** — there is no inhomogeneous term anywhere, and the system is
algebraic rather than differential.

## The theorem

In generating functions `A(t) = sum ahat_i t^i`, `Qh(t) = sum qhat_k t^k`:

    sum_{i,k} (3i-2k) ahat_i qhat_k t^(i+k)  =  t (3 A' Qh - 2 A Qh')

so the whole system is `3 A' Qh = 2 A Qh'`, i.e. `(Qh^2/A^3)' = 0`, i.e.

    **Qh^2 = c A^3** ,   deg A = 8 ,  deg Qh = 12 ,  and 2*12 = 3*8 .

Every root of `A` therefore has even multiplicity:

    **A(t) = c0 G(t)^2  with deg G = 4,  and  Qh(t) = c1 G(t)^3 .**

`ahat_0 = p_8_0` and `ahat_8 = p_16_8` are two of the six mutable vertices, so
`A != 0`, `G(0) != 0` and `deg G = 4` exactly.

This removes **four** dimensions from `P` (nine coefficients to five parameters)
and determines **all thirteen** of `Q`'s top-row coefficients from one quartic.

## Controls

* top-y coefficient of the raw rung vs the `(3i-2k)` anti-diagonal sum, at every
  `d = 0..19`: **PASS**
* generating-function identity: **PASS**
* POSITIVE: `A = G^2`, `Qh = G^3` with `G` a free quartic satisfies every rung: **PASS**
* NEGATIVE: `A = (t-1)(t-2)^2(t-3)^2(t-5)^2(t-7)` (two simple roots) forces
  `Qh = 0`, killing the vertex `q_24_12`: **PASS**
* POSITIVE: `A = ((t-2)(t-3)(t-5)(t-7))^2` admits `Qh = z (t-2)^3(t-3)^3(t-5)^3(t-7)^3`: **PASS**

## Generalisation: a degree-pair filter that needs no `L`

Nothing above uses `(72,108)`.  For any pair with x-degrees `(m,n)` the same
computation gives `Qh^m = c A^n`, `deg A = m`, `deg Qh = n`, so with
`g = gcd(m,n)` every root of `A` has multiplicity divisible by `m/g`:

    **A must be a perfect (m/g)-th power.**

For `(8,12)`: `g = 4`, `m/g = 2`, a square.  This is a cheap exclusion instrument
requiring **only the Newton polygon** — not GGV's `A_0`/`B`/`L` apparatus, whose
unavailability above `max = 125` is what Session 41 recorded as Blocker 1 (804
admissible pairs "listable, not rankable").  Allocated to Codex as OPUS43-014
Task A, with `(72,108)` as the mandatory positive control: the filter must NOT
kill it, since `A = c0 G^2` is a nonempty 5-parameter family.

## Use

`build_reduced.py` adds the theorem to Codex's degree-2 polynomial-Q export
(`codex_p11zero/p11zero_full_sat_p1000003.ms`, 186 vars / 306 eqs), encoding it at
degree 2 by naming the intermediate powers `w = G^2`, `u = G^3`.  Result: 214
vars, 350 equations, still all degree 2.  Encoding controls (positive and
negative) **PASS**.  Queued to Singular, since 214 vars is past msolve's
exponent-hash ceiling.

## Status

The pentagon is still **NO VERDICT**.  Eight solver-free conditions now constrain
both edges of `N(P)`; they do not decide the interior.
