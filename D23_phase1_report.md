# D=23 Transfer Campaign — Phase 1 Report

Session N2, continuing from Phase 0 (complete: `D23_phase0_report.md`).

## VERDICT (task discipline, three-way language)

**The transfer mechanism APPLIES to the Second Framework and produces the
contradiction at the endgame layer.** Every hypothesis of the Sessions 16–18
endgame that can be checked against (a) the paper's published §4 data, (b) the
chain data certified this session, and (c) Phase 0's certified Belyi map,
holds exactly. Conditional on the four not-yet-rebuilt layers (list below,
each verified at the data level, none showing any sign of obstruction to
transfer), **the Second Framework DIES by the same one-line obstruction as
the First: 23/3 ∉ ℤ** — the cusp cannot osculate a 23-chain compatibly with
a constant Jacobian; equivalently 3n = 23 has no integer solution.

This is **not yet the clean unconditional DIES**: the honest label is
*"mechanism applies and produces the contradiction, modulo the layer-transfer
conditions L1–L4"*. It is emphatically not "mechanism doesn't apply", and
nothing found anywhere in the session points toward "applies but no
contradiction".

**Phase 2 gate**: per the task ("only if Phase 1 result is DIES cleanly"),
Phase 2 (isotope series) stays **locked** this session.

## What was certified unconditionally this session (all exact)

### 1. Endgame operator (d23_phase1_endgame.py)

With T_{23,k}(R) := (v+1)^k(3v(v+1)R′ − 23R), on polynomials of deg ≤ 23:

- **D=13 regression**: rank of T_{13,4} = 14 (kernel trivial), T(R)=1
  infeasible — matches the Sessions 16–18 certification ledger exactly.
- **E1**: kernel of 3v(v+1)R′ − 23R is trivial (rank 24 of 24).
- **E2**: 3v(v+1)R′ − 23R = γ ≠ 0 forces R = −γ/23, degree 0 — while the
  realization layer forces deg R = 23 (any affine image of the Phase-0
  certified degree-23 Shabat polynomial has degree exactly 23).
  Contradiction already at prefactor exponent k = 0.
- **E3**: for EVERY k ≥ 1, T_{23,k}(R) = γ ≠ 0 is infeasible outright
  (LHS vanishes at v = −1); redundant exact-LA certificates for k = 1..8.
  So the verdict does not depend on knowing the SF rigidity prefactor.
- **E4**: the M ≡ 0 branch: a rational solution of 3v(v+1)R′ = 23R needs
  leading exponent n with 3n = 23 — impossible. (General D: this branch
  admits rational solutions iff 3 | D. Both published frameworks have
  D ∈ {13, 23}, both ≢ 0 mod 3.)
- **E5**: the rigidity collapse identity transfers with the same constant:
  FF: 13(9v+8) − 117(v+1) = −13; SF (predicted shape g = αUv¹⁴, deg g = 15):
  23(15v+14) − 345(v+1) = −23; general identity
  D((deg g)v + deg g − 1) − D·deg g·(v+1) = −D certified symbolically.

### 2. Chain data certification (d23_phase1_chaindata.py) — the layer-1 grounding

The paper's 31-curve chain between the multiforks, plus its five φ*F
formulas, certified against intersection theory:

- **C1**: the 31-label sequence is a valid iterated-blowup chain (reduces to
  the bare (−5,−2) edge).
- **C2**: all self-intersections from adjunction are negative integers; the
  five (−1)-curves are exactly the five e=23 carriers E₋₉₂, E₋₆₉, E₋₄₆,
  E₋₂₃, E₋₂₃′ of the five φ*F formulas.
- **C3**: discrete harmonicity (φ*F)·E = 0 at every contracted curve — all
  155 pairs.
- **C4**: (φ*F)·E = F·φ_*E at every type-1 curve.
- **C5**: chain-block projection formula (φ*F_i·φ*F_j)|chain = **23**·F_i·F_j
  for all 25 pairs; the full 28·F_i·F_j is completed exactly by the five
  degree-1 forked-branch sections (28 = 1·23 + 5·1, the paper's own degree
  decomposition over the marked point).
- **C6**: solving the two discrete Dirichlet problems for the multifork
  pullbacks: integral non-negative multiplicities, and the (φ*y₁, φ*y₂)
  valuation ledger along all 31 chain curves — **every pair proportional to
  (3,2)**, interpolating from 23·(−3,−2) at E₋₉₂ to 23·(−6,−4) at E₋₂₃′.
- **C7**: the chain-layer contact count: the Y-side creation order
  (validated by reproducing the paper's stated (−15,−10) on curves 12,13,14)
  gives val_{(−2)mf}(y₁² − y₂³) = −7 = 3·(−10) + 23: **the SF chain layer is
  the contact demand val ≥ −7, i.e. exactly D = 23 block vanishings
  W_n = 0, n = −30..−8** — the precise analog of FF's val ≥ −5 / 13
  vanishings (Sessions 10–12).

**Two typos found in the paper's §4 φ* formulas**, each *forced* by
harmonicity (no other reading balances): φ*F₋₂'s "5E₋₂" must be 5E₋₁₂, and
φ*F₋₁'s "8E₋₃" must be 8E₋₁₃. Worth reporting to Borisov (his Question 6.7
invites exactly this kind of collaboration).

### 3. Published-data hypotheses (d23_phase1_hypotheses.py)

- **H1**: all published valuation/pole pairs ∝ (3,2): (−15,−10), (60,40),
  (105,70), (165,110), (270,180), (435,290). Same cusp c₂ = y₁²−y₂³.
- **H2**: (435,290) = 145·(3,2) (FF: (99,66) = 33·(3,2)).
- **H3**: deg-28 (−5)-map bookkeeping exact (RH: 54 = 2·28−2, genus 0), chain
  degree 23 = order of the {1}-marked point.
- **H4**: realization target = the Phase-0 certified polynomial, deg 23.
- **H5**: the SF (−5)-map has the Session-7 functional form P²/(wR³),
  deg P = 14, deg R = 9, predicted miracle cancellation deg(P²−wR³) = 5.

### 4. Chart layer L1 — core CLOSED (d23_phase1_chart.py)

The parsed Fig. 21 shows the SF Z-stem (−1)—(−3)—(−5)—(−2) and short branch
(−1)—0(−3) are identical in K̄-structure and creation order to the First
Framework's Z-stem; the chain breaks the same (−5)—(−2) edge, and the SF
long-branch modifications happen strictly beyond the (−2)-multifork.
Divisorial valuations of x₁, x₂ along existing curves are unchanged by later
point blowups, so the Sessions 8–16 chart transfers verbatim:
v = x₁x₂³ − 1, q = x₂/v³. Certified exactly: chart inversion, the monomial
rule x₁ⁱx₂ʲ = (v+1)ⁱ q^(j−3i) v^(3j−9i) (so the (−2)-pole support cut keeps
the same form with SF depths j−3i ≥ −15 / −10), and the chart factor
det d(q,v)/d(x₁,x₂) = −x₂³/v³ = −q³v⁶, hence **the Keller condition reads
J_(q,v) = −c·q⁻³v⁻⁶ exactly as in D=13**, with the kill point v = −1 at the
corner x₁x₂³ = 0 and the chain corner v = ∞ at the order-23 marked point.
Remaining L1 gap: only the total-degree support boxes (the [0,27]×[0,72]
analogs summing to 435/290), which need the x-side degree split along the
modified long branch.

## The conditional gap: layers L1(boxes)–L4 (the Sessions 8–15 analogs)

What separates "mechanism applies and kills at the endgame" from the
unconditional theorem, with the FF session that built each layer:

- **L1** (FF Session 8): ~closed — see item 4; open: support boxes only.
- **L2** (FF Sessions 10–12): block-level chain unification — C7's
  valuation-level equivalence (23 vanishings) promoted to the block cascade
  and the sqrt-reduction.
- **L3** (FF Sessions 12–13): boundary rigidity — Taylor pins forcing
  g = αU v¹⁴ (deg g = 15 = |−15|·3/3; E5's collapse identity already checks).
- **L4** (FF Sessions 13–16): pole-fiber/realization theorem and the Keller
  pairing producing T_{23,k} with its specific k (immaterial to the verdict:
  every k ≥ 0 is killed, E2+E3).

FF took 8 sessions for these; none of tonight's SF evidence resists transfer.

## Next-session roadmap

1. **N3**: SF (−5)-curve map (P,R), Session-7 style: derive + certify the
   deg-28 map with deg(P²−wR³) = 5, build the SF near-miss, certify the
   h-invariant 2P′Rw − P(R+3wR′) = h₀. (Attempted as stretch goal below.)
2. **N4–5**: L1 + L2 (chart, boxes, cascade) certified on the SF near-miss.
3. **N6**: L3 + L4 → unconditional SF emptiness; then Phase 2 unlock
   (isotope series).
