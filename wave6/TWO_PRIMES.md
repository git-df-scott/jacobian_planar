# Two primes, two engines each, certificates verified at both

| | p = 1000003 | p = 1000039 |
|---|---|---|
| system | seed-pinned, 92 vars / 209 eq | seed-pinned, 89 vars / 188 eq |
| how built | campaign's own export | **reconstructed** via the verified mapping |
| msolve | `[-1]` EMPTY | `[-1]` EMPTY |
| Singular `slimgb` | UNIT IDEAL → EMPTY | UNIT IDEAL → EMPTY |
| second depth | 73 vars → `[-1]` | 108-var export also produced |
| **certificate** | **53 terms, deg ≤ 5, `Σλᵢ Fᵢ = 1` verified** | **53 terms, deg ≤ 5, verified** |

**Both primes are like-for-like**: p = 1000039 was built by re-doing the seed
pinning myself, using the mapping `c_i ↔ c_i_{2i−2}`, `d_j ↔ d_j_{2j−3}`, which
was validated by reconstructing the campaign's own p = 1000003 export
**equation for equation, all 266 identical**.

Note p = 1000033 — my first attempt — was the wrong prime: the census gives it
**admissible = 0**, so no F_p-rational admissible seed exists to pin. Its three
crashes were on the unpinned system out of necessity, and are recorded as
NO VERDICT, never as evidence.

## The certificates are the same size at both primes

53 terms, maximum degree 5, at two unrelated primes, on two independently
reduced systems. That is what one expects if both are reductions of a single
certificate over ℚ with small coefficients — which is exactly the object that
would close characteristic zero.

## What is now established, stated honestly

**The admissible seed does not extend, at two independent primes, confirmed by
two independent engines, with an explicitly verified Nullstellensatz certificate
at each.** By the single-Galois-orbit result this decides all five admissible
seeds, not one.

**Still FITTED, not DERIVED.** Two primes are two data points. The
characteristic-zero statement requires the certificate with **rational**
coefficients, expanded exactly. That computation is in flight (`slimgb` over ℚ
and `modStd` on `char0_118v.ms`). Until it lands, this is not a proof over ℂ,
and the campaign's own rule — modular emptiness is unsound for contradictions —
still binds.
