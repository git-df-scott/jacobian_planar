# Tier 1: trackB1 over Q — NO VERDICT, and why

`trackB1_sat_p1000003.ms` (166 var / 284 eq, saturated on `c_1_0, c_8_14,
d_12_21, s_4_8`) is the one target where **NONEMPTY would mean a counterexample
candidate**: a solution is an admissible point of pentagon case (1).

## Result

    leaves: 2   EMPTY=1   NONEMPTY=0   NOVERDICT=1
    unresolved leaf: c_1_0!=0;  281 eq / 163 vars  (both engines: no verdict)
    VERDICT: NO VERDICT

The branch did exactly what was predicted: `c_1_0 = 0` dies **instantly** against
the saturation row `zsat·c_1_0·c_8_14·d_12_21·s_4_8 − 1`, which is a clean
confirmation that the saturation is doing its job. But the surviving branch is
281 equations in 163 variables — against a root of 284 in 166. Branching bought
**3 variables.**

## Why branching fails here, stated as a rule

trackB1 has only **2 single-monomial equations, and both involve `c_1_0`**:

    c_1_0 · d_0_1 = 0        c_1_0 · d_1_1 = 0

So one split exhausts the entire monomial structure and the tree is one node
deep. Compare the h-branch frontier: 6 monomial equations over 8 variables with
`c_46` in four of them, which collapsed into 15 easy leaves.

>  **Branching converts a wall into progress in proportion to the number of
>  *independent* monomial equations. One shared pivot variable gives one split,
>  and one split gives nothing.**

That is the second clean demonstration of the method's boundary tonight (the
first being the (9,27) systems), and it is worth more than another win: it says
when *not* to reach for it.

## What replaces it — CORRECTED

**The original text of this section said: "Reduce harder before branching …
the reduction — not the solver, and not the branching — is the lever here."
That was wrong, and following it produced every subsequent NO VERDICT.**

Measuring the reductions instead of trusting them:

| export | vars | max degree | total terms | outcome |
|---|---|---|---|---|
| `trackB1_sat_p1000003.ms` (**root**) | 166 | **5** | **8,774** | never given a real budget |
| `reduced_tb1deep_99v.ms` | 100 | 19 | 414,175 | Singular OOM, `halt 14` |
| `reduced_tb1deep_82v.ms` | 83 | — | ~1.5 M | `halt 1` |
| `reduced_tb1deep_60v.ms` | 61 | — | ~5.3 M | 240 MB, cannot load |

The forced chain trades variables for degree. Gröbner cost is **doubly
exponential in degree**, so dropping 66 variables to gain 14 degrees and 47× the
terms made the system strictly harder at every step. "81 variables is inside the
range where `slimgb` finishes in seconds" was reasoning from variable count
alone, and variable count is not what `slimgb` is sensitive to.

Worse: the root is the *easiest* form of the question and it is the one that
never got resources. `w6_branch_solve.py` defaults to `LEAF_MEM=4000000` (4 GB)
and `LEAF_T=120` (2 min) — so the NO VERDICT recorded above was the root being
given two minutes, while the degree-19 blowup got 9 GB and hours.

### The engines fail on different axes

- **msolve dies on VARIABLE COUNT.** On the root: `Enlarging exponent vector for
  hash table failed, esz = 33554432`. Its monomial hash table is dense in
  nvars — 2²⁵ monomials × 166 slots ≈ 22 GB. No tunable exists. msolve cannot
  ingest the root at all.
- **Singular `slimgb` dies on TERM COUNT** and uses sparse exponent vectors, so
  166 variables cost it nothing — it ingests the root at ~340 MB.

The campaign had these pointed backwards: the few-terms/many-vars root went to
msolve, the few-vars/many-terms reductions went to Singular.

### The structure the reduction was destroying

283 of 284 equations are **affine-linear in the whole 51-variable c-block**
(`A(d,s)·c = b(d,s)`), and all 284 are affine-linear in the 110-variable
d-block. The entire nonlinearity lives in the **4-variable s-block**. So both
big blocks eliminate by *Gaussian elimination*, at zero degree cost — exactly
what the chain was failing to do by substitution. See `wave6/w6_tb1_rank.py`
and its planted-solution control `wave6/w6_tb1_control.py`.

Probing at p = 1000003: inconsistent at every random `(d,s)` and every random
`(c,s)`. So the variety's projection is **not dominant in either direction** —
recorded as NO VERDICT on emptiness, never as EMPTY, since random points cannot
hit a proper closed subvariety.

### Two-prime and characteristic-zero forms now exist

`campaign/audit_tracks/trackB1_case1_full_p65521.ms` is the **same system at a
second prime** — 284/284 equations matching monomial-for-monomial, all 8,774
coefficients sharing a common integer lift (the saturation row differs only in
the name `w_sat` vs `zsat`). From that agreement the exact integer system was
reconstructed as `wave6/frontier/trackB1_sat_Q.ms` (degree 5, max coefficient
468), verified by reducing it back to both primes, 284/284 each.

**Run the root, not a reduction.**
