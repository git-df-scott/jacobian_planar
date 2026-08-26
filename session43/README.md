# Session 43

**No counterexample.** What follows is what was established, what was withdrawn,
and what is left. Read `AUDIT.md` before quoting any number: an earlier pass of
this session reported results that were wrong, and the corrections are material.

## The one-line summary

The July 2026 dimension-3 counterexample makes a new reduction available —
slice it back down to a surface — and that reduction is correct but, for
Alpöge's map, **subsumed by a 1986 theorem of Orevkov**. Along the way the tear
of that map turned out to be rational and completely stratifiable, which yielded
an exact Euler identity and a sharp structural constraint on the tear of *any*
planar counterexample.

## Results that survive audit

**1. The slice reduction.** For any `Sigma ≅ C^2` in the target of a
counterexample `F`, `S := F^{-1}(Sigma)` is smooth, `F|_S` is étale, and since
`F` is 3:1 *everywhere* it is non-injective for every `Sigma` — the collision
value is not a constraint. So `S ≅ C^2` for any such `Sigma` ⟹ **JC2 false**
(Keller is automatic: the Jacobian is a nowhere-zero regular function on `C^2`).

**2. The tear of Alpöge's map is rational.** `Delta` is quadratic in `w1` with a
**perfect-cube** discriminant `−4(3w2w3−4)^3`, so `mu^2 := 4−3w2w3` rationalizes:

```
w1 = (mu+1)(mu-2)^2/27r^2,  w2 = -(mu-2)(mu+2)/3r,  w3 = r
inverse:  r = w3,  mu = E/(4-3w2w3),   E = 27w1w3^2 - 9w2w3 + 8
```

`E` is the same invariant that appears in `disc_x` of the fibre cubic. This gives
the exact stratification `tear = (C*)^2 ⊔ C* ⊔ A^1`, with `C_sing = {mu=0}`.
Fibre sizes come out **{3, 1, 0}** — which is Gao (arXiv:2608.00222) Theorem 3.4,
derived here from scratch, so the machinery independently reproduces a published
theorem.

**3. An exact Euler identity.** For any dominant `F : C^2 -> C^2` with finite
fibres, geometric degree `d`, tear stratified with fibre `n_i` on `A_i`:

```
sum_i (d - n_i) chi(A_i) = d - 1
```

This **implies** the campaign's `chi(F^{-1}(S_F)) ≡ 1 (mod d)` and pins the value
rather than the residue.

**4. A constraint on the tear of any counterexample.** If the tear is
irreducible with constant fibre count `m`, then `(d-m)chi(A) = d-1`; since
`chi <= 1` for any irreducible affine curve, this forces `chi(A) = 1` **and
`m = 1`**. With Chau/Abhyankar–Moh (no tear component is `A^1`) and Abhyankar–Moh
(smooth + rational + one place at infinity ⟹ `A^1`), the tear must be
**singular** — a cuspidal rational curve with one place at infinity. Independent
of `d`: holds at 6 (smallest open degree), at 16 (Borisov's value at (108,72)),
everywhere.

**5. The pentagon bottom-edge seeds.** The never-run characteristic-zero RUR,
factored over ℚ: eliminant degree 9 splits **[1, 1, 2, 5]**. Checking *all* RUR
blocks (not a guessed index): no block vanishes on the quintic; `c8` and `d12`
vanish exactly on the 1+1+2 part. So **4 degenerate seeds + 5 admissible ones in
one Galois orbit, group S₅** — testing one admissible seed decides all five. This
resolves the retraction on `claude/opus-5-counterexample-plan-sep6yk` and matches
that branch's independent prime statistics.

**6. A validated linear reducer** (`msreduce.py`), with the coefficient guardrail
the campaign's first attempt lacked (products of residues must be reduced mod p
or msolve silently misreads them). Cross-validated: on the campaign's own
`seed0_p1000003.ms` it returns **123 vars / 241 equations**, exactly their
published endpoint, from code sharing none of theirs.

## Negative results, with their real strength stated

- **Plane slices: 7992 scanned, 0 survivors.** After the audit: 90 reach
  `chi(S)=1` (not 19), and all die — 18 by 1-dimensional centre, 72 by `H_1`.
  Dropping the unverified Chau citation entirely still gives 0. But see below:
  Orevkov subsumes this anyway.
- **Lane U** (the `(x,u)` normalization from Mondello's char-2 counterexample):
  the shape `P = x + x^2 Psi` is *forced*, and `Psi = c·u` is closed **exactly**.
  The 135-shape search finding 0 is **weak evidence** and the file says so: no
  member with `Psi_u != 0` is even an automorphism, so the search cannot be
  validated by recovering a planted solution.

## The correction that matters most

**Orevkov (1986): a planar Keller map of geometric degree 3 is an automorphism.**
Alpöge's map has geometric degree 3, so every slice has degree 3 or 1 and cannot
be a counterexample — whatever the Euler characteristic says. The scan is a
rediscovery, not a theorem. Confirmed floor: degrees **2,3,4,5 all excluded**
(Campbell 1973; Orevkov 1986; Domrina–Orevkov 1998 + Domrina 2000; Żołądek 2008),
**6 is open**. The lane lives only above the floor — hence `pathS_deg9.py`, which
slices `F∘F` (det J = 4, geometric degree **9**).

## Literature check that protects the campaign

A worry that Żołądek's "gcd ≤ 16 ⟹ automorphism" had closed the entire **B = 16**
program: **it has not.** GGV accept Heitmann's `B ≥ 16` and re-prove it, but
identify a **gap in Żołądek's Lemma 4.10**, on which his `B > 16` claim rests; no
erratum exists, and GGHV 2022 / Ramírez–Valqui 2025 still treat `B = 16` as live,
discarding `B=16` rows case-by-case rather than by citation. Corollary: any
`B = 16` counterexample has `max(deg) ≥ 125`, so (48,64) and (80,112) are dead.

## Compute ledger — failures, not verdicts

| system | result |
|---|---|
| corrected B=16 `d=8` (23 var / 30 eq, mostly **degree 4**) | OOM 13.9 GB, 14:32, 0 bytes |
| pentagon seed-extension (241 eq / 123 unk), first *uncapped* run | OOM 13.75 GB, 53:48, 0 bytes |
| `p11zero_full_sat` (186/306, hash-verified, never run before) | OOM 13.2 GB, 13:02, 0 bytes |

All three are **NO VERDICT**. Three independent frontier systems exceed this
box; the blocker is memory, not mathematics. The `d=8` system admits **no**
linear reduction (0 rounds), so it is genuinely hard rather than unreduced.

## Files

`chi_exact.py` (25/25 calibrations) · `pathS_tear_parametrized.py` (8/8) ·
`laneU_xu.py` (15/15) · `euler_identity.py` (4/4) · `tear_theorem.py` (16/16) ·
`msreduce.py` (3/3 + replication) · `pathS_scan2.py` · `pathS_graphs2.py` ·
`pathS_deg9.py` · `charp_ladder.py` · `AUDIT.md`.

`pathS_chi.py`, `pathS_scan.py`, `pathS_euler_filter.py`, `pathS_graphs.py` are
marked **WITHDRAWN** in place — kept only so the corrected numbers can be diffed
against the wrong ones.

## Standing rules added

1. Never report a validation suite as evidence unless its output has been read.
2. Calibrate every instrument on inputs of independently known value *before*
   aiming it at the problem, including at least one the instrument must get
   wrong if the suspected bug is present.
3. State the strength of a negative result: a search with no possible positive
   control does not exclude anything.
