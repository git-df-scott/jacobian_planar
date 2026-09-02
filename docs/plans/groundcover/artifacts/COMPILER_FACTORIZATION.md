# AUDIT 2 — does the chain compiler factor through the TAIL? **REFUTED (with a sharp repair)**

Files read: `canon/campaign/audit_tracks/trackD_chain_map.py` (390 ln),
`trackD_pipeline.py` (155 ln), `TRACKD_CHAIN_MAP.md`, `canon/CROSSDOOR.md` §5,
`canon/CATCHES.md:58-60`. Test script: `groundcover/tailtest.py`,
`groundcover/detail.py`.

## The claim under audit

> `CROSSDOOR.md:71-75` —
> ```
> Tonight's dedup found reduced systems depend only on the chain TAIL.
> Predictor test: (last-2-segments, shape index) -> system hash has ZERO
> violations across every system ever generated here (16 groups).  Current
> library: 34 chains -> 26 distinct tails.
> ```
> `CROSSDOOR.md:78-79` — `If true, the chain-compiler extension only needs to compute each case's TAIL, not its full chain`

The 26-tail count reproduces exactly (`tailtest.py`: `distinct tail keys ... 26`,
and `distinct last-2-corner keys: 26`), so we are auditing the same partition.

## Where chain data enters — exactly two functions

**Entry point 1 — `reduced_candidates(ch, superset_c=False)`,
`trackD_chain_map.py:208-263`.** This is the *only* place chain corners are read.
It consumes precisely five things:

```
trackD_chain_map.py:210   a0, _, b0 = ch.A0          <-- the FIRST corner
trackD_chain_map.py:211   at, _, bt = ch.At          <-- last corner with l = 1
trackD_chain_map.py:212   a = ch.terminal[1]         <-- terminal denominator
trackD_chain_map.py:213   b = ch.terminal[2] + 1
trackD_chain_map.py:227   ap = ch.lower[0] if ch.lower else 1
trackD_chain_map.py:248   mp, np_ = sorted((ch.m, ch.n))
```

Every *intermediate* corner is invisible — `ch.At` (`:146-150`) scans for the
last `l == 1` corner and `ch.terminal` (`:152-154`) is `corners[-1]`; nothing
else iterates `ch.corners`.

**Entry point 2 — `superset_candidates(ch, rmax)`,
`trackD_pipeline.py:27-49`** (the fallback for chains the derived rules do not
close). It reads **only** `ch.terminal` and `(ch.m, ch.n)`; `r` and `c'` are
enumerated blind (`:38`, `:40`). This branch **does** factor through the tail,
trivially.

**Where it stops.** Downstream, `run_one` (`trackD_pipeline.py:79-97`) builds

```
trackD_pipeline.py:83-84   pair = SH.Pair(name, cd["NP"], cd["NQ"], [(cd["r"], 0, 1)],
                                          f"orig deg {ch.degrees()}, max {ch.maxdeg}")
```

so the coefficient system is a function of **`(NP, NQ, r)` alone**; `ch.name`,
`ch.degrees()` and `ch.maxdeg` are cosmetic strings. The whole question therefore
reduces to: *is `(NP, NQ, r)` a function of the tail?*

## The conditional half — PROVED

Given `c'` and the swap flag, the emitted polygons are built at
`trackD_chain_map.py:251-257`:

```
base = [(0, 0), (a, b - 1), (a, b)]      # + (0, cprime) if cprime > 0
eP, eQ = ((r, 1), (1, 0)) if not swap else ((1, 0), (r, 1))
NP = hull([(mp * i, mp * j) for (i, j) in base] + [eP])
NQ = hull([(np_ * i, np_ * j) for (i, j) in base] + [eQ])
```

The inputs are `a, b` (terminal corner), `r = (a + b_t)/a_t - 2`
(`:217, :221` — terminal + `A_t`), `mp, np_` (the family/shape index), `c'`,
`swap`. **`A_0` does not appear.** So:

> **PROPOSITION (the true statement).** The map
> `(A_t, A'_t, terminal, sorted(m,n), c', swap) -> (NP, NQ, r)` is well defined.
> The terminal-polygon invariants that suffice are: the terminal corner's
> denominator `a` and height `b-1`, the last regular corner `A_t` (through `r`
> only), the last lower corner `A'_t`, and the sorted degree multipliers.

This is why `check_eps` (`trackD_chain_map.py:267-288`) never needs the chain: it
re-derives `eps_P + eps_Q = (r+1, 1)` from the emitted polygons alone.

## The unconditional half — REFUTED

`A_0` *does* enter, at exactly one place — the `c'` ladder:

```
trackD_chain_map.py:232-243
    q = Fraction(bt, at - ap)
    s = q - 1
    c_pre = Fraction(b0) - s * a0            <-- reads A_0 = corners[0]
    if c_pre.denominator != 1 or c_pre < 0:
        ... cs = list(range(0, b + 1))
    elif superset_c:
        cs = list(range(0, b + 1))
    else:
        c0 = min(int(c_pre), b)
        cs = list(range(c0, -1, -a))
```

`A_0` is a **pre-tail** entry for every chain of length >= 3. Its influence is
partially masked by the clamp `min(int(c_pre), b)` — but only when
`int(c_pre) >= b`. Measured over the library (`tailtest.py`):

```
chains: 34   in-scope: 29
A0-clamped (c_pre >= b, so A0 drops out):  8
A0-LIVE:                                  21
```

So on **21 of 29 in-scope chains the c' ladder is genuinely `A_0`-dependent**,
and the factorization can only survive by accident of which chains are in the
library. It does not survive:

```
tail-key violations: 1
  tail (8,1,28)->(11,4,7) mn=(2,3) : 3 chains  identical-systems=False
```

## Concrete counterexample pair (same tail, different systems)

Both rows are in `CHAIN_ROWS` (`trackD_chain_map.py:113` and `:118`):

| chain | corners | `A_0` | `A_t` | terminal | `A'_t` | `(m,n)` |
|---|---|---|---|---|---|---|
| **X** = `(8,28)/11/4,7` | `[(8,28), (11/4,7)]` | `(8,28)` | `(8,28)` | `(11/4, 7)` | default `(1,0)` | `(3,2)` |
| **Y** = `(8,32)/8,28/11/4,7` | `[(8,32), (8,28), (11/4,7)]` | `(8,32)` | `(8,28)` | `(11/4, 7)` | default `(1,0)` | `(3,2)` |

Identical tails under **both** readings of "last two segments" — same last two
corners `(8,28), (11/4,7)`, same `A_t`, same `A'_t`, same sorted `(m,n)` — and
the compiler emits different shape families:

```
X:  a=4  b=8  r=2   c' values emitted: [4, 4, 0, 0]          (2 distinct c')
Y:  a=4  b=8  r=2   c' values emitted: [8, 8, 4, 4, 0, 0]    (3 distinct c')
```

Arithmetic: `q = 28/(8-1) = 4`, `s = 3`; `c_pre(X) = 28 - 3*8 = 4` but
`c_pre(Y) = 32 - 3*8 = 8`; `c0 = min(c_pre, b=8)` is `4` for X and `8` for Y, so
`cs = range(c0, -1, -4)` gives `[4,0]` vs `[8,4,0]`. Y therefore carries a shape
X does not:

```
Y[0]:  c'=8, eps=((2,1),(1,0))
       NP = [(0,0), (0,16), (2,1), (8,14), (8,16)]
       NQ = [(0,0), (0,24), (1,0), (12,21), (12,24)]
```

`(0,16)` / `(0,24)` are vertices of Y's polygons and of no shape X emits, so the
Newton-polygon pair — and hence the coefficient system, the parameter count and
the `dim_bound` — differ. **X is the published (8,28) case** (`TRACKD_CHAIN_MAP.md:90`:
"Prop 4.3 cases (1)(2) — (8,28) | reproduced exactly, `c′ = 4, 0`, `r = 2`"), so
this is not an artefact of a speculative row: it is the difference between GGHV's
own two cases and a three-case family.

A third chain `(8,40)/8,28/11/4,7` (`trackD_chain_map.py:119`, `A_0 = (8,40)`,
`c_pre = 16`) emits the *same* `[8,4,0]` as Y — clamped, hence agreeing with Y
by luck, not by structure.

## Why "zero predictor violations" is nonetheless true

The predictor is keyed on `(last-2-segments, shape index)`. Because
`cs = range(c0, -1, -a)` is a **descending arithmetic ladder with the same step
`a` and the same floor `0`**, a shorter ladder is always a *suffix* of a longer
one: `{4,0} ⊂ {8,4,0}`. Any shape present in both chains has the same `c'`, and
by the Proposition above the same `(NP,NQ,r)` and the same system hash. The
predictor sees agreement on the intersection and never sees the *missing* shape,
because a shape that is not generated cannot violate a hash comparison. The
zero-violation evidence is therefore **consistent with, but does not establish,**
the factorization. `CATCHES.md:58-60`'s stronger phrasing —

> `all four virgin cases sharing tail .../11/3,8 produce byte-identical 8-shape families`

— happens to hold for that tail because all four are `A_0`-clamped
(`tailtest.py` confirms the `(9,24)->(11/3,8)` group is `identical-systems=True`),
not because the compiler ignores `A_0`.

## What this costs, and the repair

**Cost.** The `CROSSDOOR.md:78` plan — "compute each case's TAIL, not its full
chain" — is **unsafe as written**: tail-only compilation would silently drop
shapes, and per `TRACKD_CHAIN_MAP.md:100-101` "A missed shape costs a
counterexample". The risk direction is the bad one.

**Repair (cheap, and preserves the whole benefit).** The extra datum is one
integer. Extend the key from the tail to

```
(A_t, A'_t, terminal, sorted(m,n),  cmax)   where   cmax = min(int(b0 - (b_t/(a_t-a')-1)*a0), b)
```

`cmax` is one rational evaluation from `A_0` and the tail — no chain traversal,
no polygon work — and by the Proposition the full shape family is then
determined, since `cs = range(cmax, -1, -a)` and each `c'` determines the system.
Tail-closure survives as **"(tail, cmax)-closure"**, the saturation argument is
unaffected (`cmax <= b` is bounded by terminal data, so the key set is still
finite), and the order-of-magnitude saving is kept. The library's 26 tails become
27 keys (the `(8,28)` group splits into `cmax = 4` and `cmax = 8`).

## Caveat on scope

This audit certifies the **shape-extraction** stage
(`reduced_candidates` -> `check_eps` -> `SH.Pair`). It does not re-run the y-adic
/ dual-number engine (`trackB1_shapes.SH.run_pair`), which was taken as a
black box consuming `(NP, NQ, r)`; if that engine were itself chain-aware the
refutation would only get stronger, never weaker.
