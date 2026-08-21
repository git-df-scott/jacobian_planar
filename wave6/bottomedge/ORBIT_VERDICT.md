# Bottom-edge orbit structure: SETTLED over Q (exact, not statistical)

`msolve -P 2` on `be_c2is1_q.ms` (char-0 rational parametrization,
`be_c2is1_q_param.out`, 386s) followed by exact factorization of the degree-9
eliminant in sympy.

## Theorem (computationally certified, char 0)

The degree-9 eliminant of the bottom-edge chart c2=1 factors over Q as

    (57x + 179) · (285000x + 769477) · (irreducible quadratic) · (irreducible quintic)

with the quadratic of negative discriminant (complex pair) and the quintic
having exactly one real root. The nine seeds split into Galois orbits of sizes
1, 1, 2, 5.

Multiplier-independent identification (gcds of RUR numerators with the factors,
so no convention on msolve's per-coordinate constants is needed):

- c8 and d12 numerators vanish at BOTH rational roots and are divisible by the
  quadratic; gcd with the quintic is 1.
- c1 vanishes nowhere on the variety.

Hence: **degenerate locus = {2 rational seeds} ∪ {quadratic orbit}, all with
c8 = d12 = 0; admissible locus = the quintic orbit, a SINGLE Galois orbit of
size 5 with c8, d12, c1 all nonvanishing.**

## Consequences

1. **The single-orbit claim retracted in 8492a76 is TRUE**, now by exact
   computation rather than 4-prime statistics. The retraction was still
   correct method: the statistical basis was insufficient; the conclusion
   happened to survive.
2. **The four-invisible-seeds gap is closed, correctly this time.** The
   pentagon system is defined over Q, "extends to a full solution" is
   Galois-invariant, and all five admissible seeds are conjugate — so ONE
   admissible seed decides the entire bottom edge (job #2's target).
3. The p=999983 census anomaly (degenerate=2) is explained exactly: the
   quadratic orbit is inert there. Every one of the 8 censused primes matches
   the factorization pattern: degenerate ∈ {2,4} = 2 + 2·[quad splits],
   admissible = #roots of quintic mod p (0,0,1,1,1,2,2,3 observed; Chebotarev
   mean for one quintic orbit = 1; observed mean 1.25 over 8 primes).
4. The provisional real-root parse of 9111c56 ("2 of 9, grouping possibly
   misaligned") is corrected: **3 of 9 seeds are real** — the two rational
   degenerate seeds and exactly one admissible seed. That unique real
   admissible seed is the canonical test point for char-0 lifting.
5. The prime sweep's orbit-structure purpose is now superseded; its remaining
   value is per-prime verification (all seeds verify against all 17 equations
   at every prime so far) and bad-prime detection. The sweep continues to
   completion of the 8-prime list.
