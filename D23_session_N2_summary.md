# Session N2 Summary — D=23 Transfer Test (Borisov Second Framework)

One-line: **Phase 0 complete and certified (all 15 dessins, one degree-15
Galois orbit); Phase 1 endgame certified — the transfer mechanism applies and
kills at every prefactor exponent; verdict: Second Framework DIES conditional
on the L2–L4 layer rebuilds, by the 23/3 ∉ ℤ obstruction. Family-wide: every
chain degree in Borisov's entire published framework catalogue lies in
{13, 23} — none divisible by 3 — so the one obstruction conditionally covers
all of it.**

After four empty sessions, this session produced six committed, certified
deliverables plus a validated start on the next session's target.

## 0. Family-wide data verdict (d23_phase2_preview.py — gate-respecting)

Section 5 extraction + the certified general-D lemma: the isotope series
(k = 2..6, degrees (36k+27, 24k+18) = (12k+9)·(3,2)) all keep chain degree
D = 13 with the SAME target graph and (−5)-curve data as the First
Framework; the "complicated" framework ((108,72) = 36·(3,2)) reuses the
FF (−2)-curve Belyi map (D = 13). With T₁₃ (rank 14) and T₂₃ (rank 24)
exactly certified, the entire published family dies conditionally to the
single obstruction 3 ∤ D. (No Phase-2 tower work done — data extraction and
corollary only; the Phase 2 gate stays respected.)

## 1. Phase 0 (complete) — the degree-23 Belyi map nobody had computed

The paper gives only ramification data for the Second Framework's (-2)-curve
map. Derived here, certified exactly (12/12 ledger, PARI/GP + independent
sympy): B = c·t·a³b⁵ with master equation ab + 3ta′b + 5tab′ = 23(t−1)⁶.
Structure theorems: star-of-stars dessin, exactly 15 plane trees, and — the
arithmetic surprise — a **single Galois orbit over an irreducible degree-15
field** (D=13's analog lived in ℚ(√−3)). Completeness proven; all 15
embeddings' dessins computed by arc tracing (perfect bijection with the 15
necklaces); Borisov's Figure 28 dessin identified as the real embedding
β ≈ 0.1250089. Files: `d23_phase0_*.py`, `d23_phase0_certify.gp`,
`d23_belyi_data/`, `D23_phase0_report.md`.

## 2. Phase 1 — endgame certified, chain data certified, chart transferred

- **Endgame** (`d23_phase1_endgame.py`): T₂₃,ₖ(R) = (v+1)ᵏ(3v(v+1)R′ − 23R)
  = −c is impossible for every k ≥ 0 (k=0 forces deg R = 0 against the
  realization degree 23; k ≥ 1 dies at v = −1; kernel trivial, rank 24; the
  M≡0 branch dies because 3n = 23 has no integer solution). D=13 regression
  reproduces the Sessions 16–18 ledger exactly.
- **Chain data** (`d23_phase1_chaindata.py`): the paper's 31-curve chain and
  five φ*F formulas certified against intersection theory (blowup
  realizability, adjunction, harmonicity, chain-block projection formula
  = 23·F·F′ + five degree-1 sections = 28). **Two typos in the paper found,
  both forced by harmonicity.** Boundary valuations along all 31 chain curves
  ∝ (3,2); the chain layer is the contact demand val(y₁²−y₂³) ≥ −7 = exactly
  23 block vanishings; per-curve contact depths are exact multiples 23·{1..9}.
- **Chart L1** (`d23_phase1_chart.py`): SF's Z-stem matches FF's K̄-structure,
  so the (q,v)-chart, chart factor −x₂³/v³, and the Keller form
  J = −c·q⁻³v⁻⁶ transfer verbatim; pole cuts j−3i ≥ −15/−10.
- Verdict discipline and the honest gap list (L2 block cascade, L3 rigidity
  pins, L4 Keller pairing, L1 boxes): `D23_phase1_report.md`. Phase 2 stays
  gated (Phase 1 not yet an unconditional DIES).

## 3. Stretch — Session N3 started and de-risked

- Fig. 27 (deg-28 clean dessin) and Fig. 15 (FF control) fully parsed into
  combinatorial types (`D23_dessin_data.md`).
- The sqrt-series reduction for P²/(wR³) maps implemented and **validated by
  re-deriving the certified Session-7 FF (p,r) and its conjugate from random
  starts — exactly 2 solutions, no spurious** (`d23_n3_sqrtmethod.py`).
- SF (P,R) hunt (8 conditions h₁₅..h₂₂ = 0, deg-9 R), batched LM at ~29k
  restarts/min: **~7.46M complex restarts and ~1.19M real-restricted
  restarts, zero valid solutions.** Two conclusions, calibrated against the
  FF control (where the same machinery hits at ~1/1350 per restart in 8 real
  dims):
  1. The real-restricted zero (8 real dims, same effective difficulty as the
     FF control, ~880× the FF-expected hit count) is strong evidence that
     **no mirror-symmetric SF (−5)-curve dessin exists** — i.e. all dessins
     of the passport 14×2 / 9×3+1 / 1×23+5×1 are chiral (checkable
     combinatorially in N3), or their coefficients lie far outside the
     sampled radius.
  2. The complex zero in 16 real dims says only that blind multistart is the
     wrong tool at this dimension (solutions exist by Belyi theory);
     **Session N3 must construct, not search**: dessin-seeded Newton from the
     parsed Fig. 27 combinatorics, or exact solving (msolve / homotopy
     continuation) of the 8-equation sqrt-series system.

## Cross-checks that tie the epochs together

- D=13 regression of the endgame operator: rank 14 / infeasible — matches.
- The general collapse identity D((deg g)v + deg g − 1) − D·deg g·(v+1) = −D.
- The C6 ledger's e·val consistency (23·(−3,−2) at E₋₉₂ → 23·(−6,−4) at
  E₋₂₃′) and C7's independent reproduction of the paper's (−15,−10).

## Resume point (if interrupted)

Everything above is committed and pushed on
`claude/d23-borisov-transfer-test-vpr3m6` (PR #1). Next actions, in order:
(1) harvest SF (P,R) hunt results → polish → h-invariant + h₀ = −23·n₅
check → exact reconstruction (gp algdep); (2) L1 boxes (x-side degree split
along the modified long branch); (3) L2 block cascade on the SF near-miss;
(4) L3 rigidity pins; (5) unconditional endgame closure; then Phase 2.
